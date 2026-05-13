# Análisis de Ventas - Ron Caña Panamá 2024

Proyecto de Data Analytics end-to-end: generación de datos sintéticos, análisis exploratorio y visualización ejecutiva para una destilería premium ficticia en Panamá.

## Objetivo

Desarrollar un análisis completo de ventas demostrando habilidades en:
- Generación de datasets realistas con Python
- Análisis exploratorio de datos
- Modelado dimensional
- Visualización ejecutiva en Power BI
- Storytelling con datos

## Estructura del Proyecto
proyecto_ron_premium/
├── data_generation/
│   ├── config.py
│   ├── dim_productos.py
│   ├── dim_clientes.py
│   ├── eventos_comerciales.py
│   └── generador_ventas.py
├── outputs/
│   ├── dim_productos.csv
│   ├── dim_clientes.csv
│   ├── eventos_comerciales.csv
│   └── ventas_transacciones.csv
├── analysis/
│   ├── analisis_exploratorio.py
│   └── calcular_insights.py
├── app.py
└── README.md
## Contexto del Negocio

**Empresa:** Ron Caña Panamá  
**Fundación:** 2018  
**Sector:** Destilería de licores premium  

**Segmento Objetivo:** Adultos 27-55 años, NSE A/B, conocedores de licores premium

## Dataset Generado

- 4,234 transacciones del año 2024
- 14 productos con pricing realista
- 80 clientes segmentados B2B y B2C
- 10 campañas comerciales
- 9 ciudades de Panamá

## Insights Principales

**Estacionalidad**  
Diciembre concentra 24.8% del ingreso anual - oportunidad de suavizar estacionalidad con campañas Q1-Q2

**Productos Premium**  
Edición Limitada: 10.5% de unidades pero 32% de ingresos - ratio 3.1x más ingreso por unidad

**Rentabilidad por Canal**  
Horeca Premium: Margen 54.7%  
Supermercados: Margen 53.5%

**Segmentación**  
B2B: 98.3% del ingreso  
B2C: 1.7% del ingreso - canal subexplotado

**Efectividad de Campañas**  
Incremento de ticket promedio: +39.7% - ROI positivo

## Tecnologías

- Python 3.10+ (pandas, numpy, datetime)
- Power BI Desktop (Modelado dimensional, DAX)
- Streamlit (Dashboard web interactivo)
- Plotly (Visualizaciones interactivas)
- Git & GitHub

## Reproducir

**Requisitos:**
```bash
pip install pandas numpy streamlit plotly
```

**Generar Datasets:**
```bash
python data_generation/dim_productos.py
python data_generation/dim_clientes.py
python data_generation/eventos_comerciales.py
python data_generation/generador_ventas.py
```

**Análisis:**
```bash
python analysis/analisis_exploratorio.py
python analysis/calcular_insights.py
```

**Ejecutar Demo Web:**
```bash
streamlit run app.py
```

## Dashboard en Power BI

1. Abrir Power BI Desktop
2. Importar CSV de outputs/
3. Crear relaciones (esquema estrella)
4. Construir visualizaciones

## Demo Web Interactiva

Dashboard interactivo con filtros en tiempo real:

**[Ver Demo en Vivo](https://ron-cana-analytics-sn4ycdsnuse6vw2o7rryxw.streamlit.app/)**

Características:
- Filtros dinámicos por mes, canal y ciudad
- KPIs que se actualizan en tiempo real
- Gráficos interactivos con Plotly
- Mapa geográfico de distribución de ventas
- Análisis comparativo de canales y productos

## Habilidades Demostradas

**Técnicas:**  
Python, pandas, numpy, Generación de datos sintéticos, Modelado dimensional, Power BI, DAX, Streamlit, Plotly, Git & GitHub

**De Negocio:**  
Pricing strategy, Análisis de rentabilidad, Segmentación de clientes, Storytelling con datos

## Autor

**Rodolfo Alabarca**  
Data Analyst | Business Intelligence

[LinkedIn](https://www.linkedin.com/posts/rodolfo-alabarca-16b187239_dataanalytics-powerbi-python-share-7460153616096636928-fg5Z?utm_source=share&utm_medium=member_desktop&rcm=ACoAADtK1CMB-lBQ0mC2JiYVXMyVj-sVjdIvaes) | [GitHub](https://github.com/RodCode088)

