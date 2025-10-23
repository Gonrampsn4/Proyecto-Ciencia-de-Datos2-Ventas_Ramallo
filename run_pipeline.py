# -*- coding: utf-8 -*-
"""
Script CLI para ejecutar el pipeline de enriquecimiento:
- Descarga ventas (URL)
- Descarga población (CKAN)
- Descarga empresas (CKAN)
- Calcula intensidad_mercado y nivel_desarrollo_regional
- Exporta CSV
"""

import argparse
from src.uy_enrichment import (
    load_ventas, load_poblacion, load_empresas,
    enrich_ventas_with_context, save_panel, VENTAS_URL_DEFAULT
)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ventas-url", default=VENTAS_URL_DEFAULT, help="URL CSV de ventas")
    parser.add_argument("--out-csv", default="ventas_enriquecidas_uy.csv", help="Archivo de salida CSV")
    args = parser.parse_args()

    ventas = load_ventas(args.ventas_url)
    poblacion = load_poblacion()
    empresas = load_empresas()

    panel = enrich_ventas_with_context(ventas, poblacion, empresas)
    save_panel(panel, args.out_csv)
    print(f"Listo. Archivo generado: {args.out_csv}")

if __name__ == "__main__":
    main()
