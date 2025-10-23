# Proyecto Ciencia de Datos 2 – Ventas (Uruguay)

**Enriquecimiento con datos públicos (INE/CKAN + SNIG)**  
Fecha: 2025-10-23

Este repositorio (o carpeta) contiene un _pipeline_ reproducible para:

- Descargar datos públicos de Uruguay (población por departamento y un **proxy de actividad económica** basado en conteo de **empresas** por departamento), junto con la geometría departamental (GeoJSON).
- Enriquecer el dataset de ventas existente con nuevas columnas:
  - `intensidad_mercado` = ventas_total_depto / población_depto
  - `nivel_desarrollo_regional` = promedio de z-scores de Población y Empresas
- Ejecutar EDA con visualizaciones (mapa, correlaciones, dispersión)
- Exportar un CSV enriquecido para modelado

---

## Estructura sugerida

```
Proyecto-Ciencia-de-Datos2-Ventas_Ramallo/
├── src/
│   └── uy_enrichment.py
├── run_pipeline.py
├── requirements.txt
├── Proyecto_Ventas_UY_Enriquecido.ipynb
└── Presentacion_Ventas_UY_Insights.pptx
```

> **Nota:** Puedes copiar/pegar estos archivos dentro de tu repo actual o crear un branch nuevo y abrir un Pull Request.

---

## Fuentes de datos (APIs / descargas públicas)

- **Dataset de ventas (desde tu GitHub):**  
  `https://raw.githubusercontent.com/Gonrampsn4/Proyecto-Ciencia-de-Datos2-Ventas_Ramallo/main/dataset_ventas_3000.csv`

- **Población por Departamento (CKAN Uruguay, CSV – “Datos básicos de Juntas Departamentales”):**  
  `https://catalogodatos.gub.uy/dataset/7e7c97c8-a7cc-4f1f-9c85-a2c25ae28141/resource/5e1cf37b-201e-43b7-a5ba-66ee0e64e4d0/download/datosbasicosjds.csv`

- **Proxy de actividad económica (conteo de empresas por Departamento – Excel público):**  
  `https://catalogodatos.gub.uy/dataset/575ccb87-ae74-4dcd-ba4b-cf050bd8e08a/resource/e8e6f2e4-357e-4027-b91a-407b5d5501f7/download/empresasdei_20230330.xlsx`

- **Geometría de Departamentos (ArcGIS SNIG, GeoJSON vía API):**  
  `https://web.snig.gub.uy/arcgisserver/rest/services/Uruguay/SNIG_Catastro/MapServer/2/query?where=1%3D1&outFields=Nombre&outSR=4326&f=geojson`

> Si prefieres actualizar población con series más recientes del INE (p. ej., Revisión 2025), reemplaza la URL de población y ajusta el nombre de columna correspondiente.

---

## Instalación

1) Crea y activa un entorno (`venv` o Conda).  
2) Instala dependencias:

```bash
pip install -r requirements.txt
```

**Dependencias clave:**  
`pandas numpy requests geopandas mapclassify matplotlib openpyxl scipy`

---

## Ejecución rápida del pipeline (script)

```bash
python run_pipeline.py --ventas-url "https://raw.githubusercontent.com/Gonrampsn4/Proyecto-Ciencia-de-Datos2-Ventas_Ramallo/main/dataset_ventas_3000.csv"                        --out-csv "ventas_enriquecidas_uy.csv"
```

Esto generará el archivo `ventas_enriquecidas_uy.csv` con las columnas agregadas.  
Luego puedes abrir el notebook `Proyecto_Ventas_UY_Enriquecido.ipynb` para EDA y visualizaciones.

---

## Notebook

- **Proyecto_Ventas_UY_Enriquecido.ipynb**: descarga fuentes, normaliza departamentales, calcula **intensidad de mercado** e **índice de desarrollo regional**, crea gráficos y mapas, y exporta el CSV enriquecido.

---

## Presentación

- **Presentacion_Ventas_UY_Insights.pptx**: plantilla de 8 slides con Abstracto, Metadata, Hipótesis, Visualizaciones e Insights.  
  Exporta imágenes de los gráficos desde el notebook y pégalas en los placeholders.

---

## Git (subir a tu repo)

```bash
git checkout -b feature/enriquecimiento-uy
git add src/uy_enrichment.py run_pipeline.py requirements.txt Proyecto_Ventas_UY_Enriquecido.ipynb Presentacion_Ventas_UY_Insights.pptx README.md
git commit -m "Enriquecimiento UY: nuevas columnas, EDA, mapas y PPT ejecutiva"
git push origin feature/enriquecimiento-uy
```

Crea un Pull Request y describe brevemente:
- Fuentes utilizadas, cómo se integraron
- Nuevas columnas y fórmulas
- Gráficos clave y hallazgos iniciales

---

## Licencias y uso responsable

Verifica términos de uso del catálogo CKAN y del servicio SNIG. Para trabajos académicos, cita las fuentes y fechas de descarga.
