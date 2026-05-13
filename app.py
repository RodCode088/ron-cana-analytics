import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Ron Caña Panamá Analytics",
    page_icon="📊",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    /* Cambiar color de los multiselect */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #0F6F3E !important;
    }
    
    /* Cambiar color de fondo del sidebar */
    [data-testid="stSidebar"] {
        background-color: #1E293B;
    }
    
    /* Cambiar color de texto del sidebar */
    [data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.title("Business Intelligence Case - Ron Caña Panamá")
st.markdown("---")

# Cargar datos
@st.cache_data
def load_data():
    ventas = pd.read_csv('outputs/ventas_transacciones.csv')
    ventas['fecha'] = pd.to_datetime(ventas['fecha'])
    return ventas

ventas = load_data()

# Coordenadas de ciudades de Panamá
coordenadas = {
    'Ciudad de Panamá': {'lat': 8.9936, 'lon': -79.5197},
    'David': {'lat': 8.4334, 'lon': -82.4274},
    'Colón': {'lat': 9.3592, 'lon': -79.9009},
    'Santiago': {'lat': 8.1036, 'lon': -80.9833},
    'Coronado': {'lat': 8.6167, 'lon': -79.9833},
    'Boquete': {'lat': 8.7789, 'lon': -82.4328},
    'Chitré': {'lat': 7.9622, 'lon': -80.4297},
    'Penonomé': {'lat': 8.5167, 'lon': -80.3500},
    'Bocas del Toro': {'lat': 9.3404, 'lon': -82.2410}
}

# Sidebar con filtros
st.sidebar.header("Filtros")

meses = st.sidebar.multiselect(
    "Seleccionar Mes(es)",
    options=sorted(ventas['mes'].unique()),
    default=sorted(ventas['mes'].unique())
)

canales = st.sidebar.multiselect(
    "Seleccionar Canal(es)",
    options=sorted(ventas['canal_venta'].unique()),
    default=sorted(ventas['canal_venta'].unique())
)

ciudades = st.sidebar.multiselect(
    "Seleccionar Ciudad(es)",
    options=sorted(ventas['ciudad'].unique()),
    default=sorted(ventas['ciudad'].unique())
)

# Filtrar datos
df_filtrado = ventas[
    (ventas['mes'].isin(meses)) &
    (ventas['canal_venta'].isin(canales)) &
    (ventas['ciudad'].isin(ciudades))
]

# KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    ingreso_total = df_filtrado['ingreso_total'].sum()
    st.metric("Ingreso Total", f"${ingreso_total/1e6:.2f}M")

with col2:
    utilidad_total = df_filtrado['utilidad_bruta'].sum()
    st.metric("Utilidad Bruta", f"${utilidad_total/1e6:.2f}M")

with col3:
    transacciones = len(df_filtrado)
    st.metric("Total Transacciones", f"{transacciones:,}")

with col4:
    ticket_promedio = df_filtrado['ingreso_total'].mean()
    st.metric("Ticket Promedio", f"${ticket_promedio:,.0f}")

st.markdown("---")

# Gráficos
col1, col2 = st.columns(2)

with col1:
    # Tendencia por mes
    ventas_mes = df_filtrado.groupby('mes')['ingreso_total'].sum().reset_index()
    fig1 = px.line(
        ventas_mes,
        x='mes',
        y='ingreso_total',
        title='Tendencia de Ingresos por Mes',
        labels={'mes': 'Mes', 'ingreso_total': 'Ingreso'}
    )
    fig1.update_traces(line_color='#0F6F3E', line_width=3)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Top 5 productos
    top_productos = df_filtrado.groupby('nombre_producto')['ingreso_total'].sum().nlargest(5).reset_index()
    fig2 = px.bar(
        top_productos,
        x='ingreso_total',
        y='nombre_producto',
        orientation='h',
        title='Top 5 Productos por Ingreso',
        labels={'ingreso_total': 'Ingreso', 'nombre_producto': 'Producto'}
    )
    fig2.update_traces(marker_color='#0F6F3E')
    st.plotly_chart(fig2, use_container_width=True)

col3, col4, col5 = st.columns(3)

with col3:
    # B2B vs B2C
    b2b_b2c = df_filtrado.groupby('tipo_cliente')['ingreso_total'].sum().reset_index()
    fig3 = px.pie(
        b2b_b2c,
        values='ingreso_total',
        names='tipo_cliente',
        title='Distribución B2B vs B2C',
        color_discrete_sequence=['#0F6F3E', '#94A3B8']
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    # Mapa geográfico
    ventas_ciudad = df_filtrado.groupby('ciudad')['ingreso_total'].sum().reset_index()
    ventas_ciudad['lat'] = ventas_ciudad['ciudad'].map(lambda x: coordenadas.get(x, {}).get('lat', 0))
    ventas_ciudad['lon'] = ventas_ciudad['ciudad'].map(lambda x: coordenadas.get(x, {}).get('lon', 0))
    
    fig_mapa = px.scatter_mapbox(
        ventas_ciudad,
        lat='lat',
        lon='lon',
        size='ingreso_total',
        hover_name='ciudad',
        hover_data={'ingreso_total': ':,.0f', 'lat': False, 'lon': False},
        title='Distribución Geográfica de Ventas',
        color_discrete_sequence=['#0F6F3E'],
        zoom=6,
        height=400
    )
    fig_mapa.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(center=dict(lat=8.5, lon=-80.5))
    )
    st.plotly_chart(fig_mapa, use_container_width=True)
with col5:
    # Ingresos por canal
    canales_ventas = df_filtrado.groupby('canal_venta')['ingreso_total'].sum().reset_index()
    fig4 = px.bar(
        canales_ventas,
        x='canal_venta',
        y='ingreso_total',
        title='Ingreso por Canal de Venta',
        labels={'canal_venta': 'Canal', 'ingreso_total': 'Ingreso'}
    )
    fig4.update_traces(marker_color='#0F6F3E')
    st.plotly_chart(fig4, use_container_width=True)

# Insights
st.markdown("---")
st.subheader("Insights Clave")

insights = f"""
- **Diciembre concentra 25% del ingreso anual** - Oportunidad de suavizar estacionalidad con campañas Q1-Q2
- **Edición Limitada: 10.5% de unidades pero 32% de ingresos** - Ratio 3.1x más ingreso por unidad
- **Horeca Premium: Margen 54.7%** vs Supermercados 53.5% - Priorizar canal Horeca
- **B2B representa 98.3% del ingreso** - Canal B2C subexplotado
- **Campañas incrementan ticket promedio 40%** - ROI positivo
"""

st.markdown(insights)

# Footer
st.markdown("---")
st.markdown("**Proyecto de Data Analytics** | Rodolfo Alabarca | [GitHub](https://github.com/RodCode088/ron-cana-analytics)")