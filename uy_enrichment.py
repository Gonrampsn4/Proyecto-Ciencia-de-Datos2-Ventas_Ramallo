# -*- coding: utf-8 -*-
"""
Funciones utilitarias para enriquecer un dataset de ventas de Uruguay
con población por departamento y una proxy de actividad económica (conteo de empresas).
También incluye helpers para normalizar nombres de departamento y calcular nuevas columnas.
"""

from __future__ import annotations

import io
import json
import requests
import pandas as pd
import numpy as np
from scipy.stats import zscore

# URLs públicas (modificables)
VENTAS_URL_DEFAULT = "https://raw.githubusercontent.com/Gonrampsn4/Proyecto-Ciencia-de-Datos2-Ventas_Ramallo/main/dataset_ventas_3000.csv"
POBLACION_URL = "https://catalogodatos.gub.uy/dataset/7e7c97c8-a7cc-4f1f-9c85-a2c25ae28141/resource/5e1cf37b-201e-43b7-a5ba-66ee0e64e4d0/download/datosbasicosjds.csv"
EMPRESAS_XLSX_URL = "https://catalogodatos.gub.uy/dataset/575ccb87-ae74-4dcd-ba4b-cf050bd8e08a/resource/e8e6f2e4-357e-4027-b91a-407b5d5501f7/download/empresasdei_20230330.xlsx"
DEPARTAMENTOS_GEOJSON_URL = "https://web.snig.gub.uy/arcgisserver/rest/services/Uruguay/SNIG_Catastro/MapServer/2/query?where=1%3D1&outFields=Nombre&outSR=4326&f=geojson"


def norm_depto(s: str) -> str:
    if pd.isna(s):
        return s
    s = str(s).strip().upper()
    repl = {
        "SAN JOS\u00c9": "SAN JOSÉ",
        "SAN JOSE": "SAN JOSÉ",
        "TREINTA Y TRES": "TREINTA Y TRES",
        "MONTEVIDEO": "MONTEVIDEO",
        "CANELONES": "CANELONES",
        "MALDONADO": "MALDONADO",
        "COLONIA": "COLONIA",
        "ROCHA": "ROCHA",
        "LAVALLEJA": "LAVALLEJA",
        "FLORIDA": "FLORIDA",
        "DURAZNO": "DURAZNO",
        "SORIANO": "SORIANO",
        "RIO NEGRO": "RÍO NEGRO",
        "R\u00cdO NEGRO": "RÍO NEGRO",
        "PAYSANDU": "PAYSANDÚ",
        "PAYSAND\u00da": "PAYSANDÚ",
        "SALTO": "SALTO",
        "ARTIGAS": "ARTIGAS",
        "RIVERA": "RIVERA",
        "TACUAREMBO": "TACUAREMBÓ",
        "TACUAREMB\u00d3": "TACUAREMBÓ",
        "CERRO LARGO": "CERRO LARGO",
        "FLORES": "FLORES",
    }
    return repl.get(s, s)


def load_ventas(ventas_url: str = VENTAS_URL_DEFAULT) -> pd.DataFrame:
    return pd.read_csv(ventas_url)


def load_poblacion(url: str = POBLACION_URL) -> pd.DataFrame:
    df = pd.read_csv(url)
    # Identificar columna de departamento
    pop_dept_cols = [c for c in df.columns if "depar" in c.lower() or c.lower()=="departamento"]
    if not pop_dept_cols:
        raise ValueError("No se encuentra columna de Departamento en población.")
    df["Departamento"] = df[pop_dept_cols[0]].apply(norm_depto)
    # Identificar columna de población
    cand_pop = [c for c in df.columns if "poblac" in c.lower() or "habit" in c.lower()]
    if not cand_pop:
        raise ValueError("No se encuentra columna de población en el CSV de población.")
    df = df[["Departamento", cand_pop[0]]].rename(columns={cand_pop[0]:"Poblacion"})
    return df


def load_empresas(url: str = EMPRESAS_XLSX_URL) -> pd.DataFrame:
    resp = requests.get(url)
    resp.raise_for_status()
    emp = pd.read_excel(io.BytesIO(resp.content))
    emp_dept_cols = [c for c in emp.columns if "depar" in c.lower() or c.lower()=="departamento"]
    if not emp_dept_cols:
        raise ValueError("No se encuentra columna de Departamento en Excel de empresas.")
    emp["Departamento"] = emp[emp_dept_cols[0]].apply(norm_depto)
    empresas_por_depto = emp.groupby("Departamento", as_index=False).size().rename(columns={"size":"Empresas"})
    return empresas_por_depto


def enrich_ventas_with_context(ventas: pd.DataFrame,
                               poblacion: pd.DataFrame,
                               empresas_por_depto: pd.DataFrame) -> pd.DataFrame:
    # Detectar columna departamento en ventas
    dept_cols = [c for c in ventas.columns if c.lower() in ["departamento","depto","region","provincia","estado"]]
    if not dept_cols:
        raise ValueError("No encuentro columna de departamento en ventas.")
    ventas["Departamento"] = ventas[dept_cols[0]].apply(norm_depto)

    # Detectar columna de monto/importe
    val_cols = [c for c in ventas.columns if any(k in c.lower() for k in ["monto","importe","total","venta","revenue","price","amount"])]
    if not val_cols:
        raise ValueError("No encuentro columna de monto/importe en ventas.")
    monto_col = val_cols[0]

    # Agregación
    ventas_depto = (ventas
                    .groupby("Departamento", as_index=False)
                    .agg(ventas_total=(monto_col,"sum"),
                         operaciones=("Departamento","count"),
                         ticket_promedio=(monto_col,"mean")))

    panel = (ventas_depto
             .merge(poblacion[["Departamento","Poblacion"]], on="Departamento", how="left")
             .merge(empresas_por_depto, on="Departamento", how="left"))

    panel["Empresas"] = panel["Empresas"].fillna(0).astype(int)

    # Nuevas métricas
    panel["intensidad_mercado"] = panel["ventas_total"] / panel["Poblacion"]
    panel["z_pop"] = zscore(panel["Poblacion"].fillna(panel["Poblacion"].median()))
    panel["z_emp"] = zscore(panel["Empresas"].fillna(panel["Empresas"].median()))
    panel["nivel_desarrollo_regional"] = (panel["z_pop"] + panel["z_emp"]) / 2.0

    return panel


def save_panel(panel: pd.DataFrame, path: str = "ventas_enriquecidas_uy.csv") -> None:
    panel.to_csv(path, index=False, encoding="utf-8")
