# analisis_exploratorio.py
# Análisis exploratorio del dataset de Ron Caña Panamá

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuración de visualización
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

print("="*70)
print("📊 ANÁLISIS EXPLORATORIO - RON CAÑA PANAMÁ")
print("="*70)

# ============================================
# 1. CARGAR DATOS
# ============================================
print("\n🔄 Cargando datos...\n")

df_ventas = pd.read_csv('outputs/ventas_transacciones.csv')
df_productos = pd.read_csv('outputs/dim_productos.csv')
df_clientes = pd.read_csv('outputs/dim_clientes.csv')

print(f"✅ Ventas cargadas: {len(df_ventas):,} transacciones")
print(f"✅ Productos: {len(df_productos)}")
print(f"✅ Clientes: {len(df_clientes)}")

# Convertir fecha a datetime
df_ventas['fecha'] = pd.to_datetime(df_ventas['fecha'])

# ============================================
# 2. RESUMEN EJECUTIVO
# ============================================
print("\n" + "="*70)
print("💼 RESUMEN EJECUTIVO 2024")
print("="*70)

ingreso_total = df_ventas['ingreso_total'].sum()
utilidad_total = df_ventas['utilidad_bruta'].sum()
margen_promedio = df_ventas['margen_porcentaje'].mean()
ticket_promedio = df_ventas['ingreso_total'].mean()
unidades_vendidas = df_ventas['cantidad'].sum()

print(f"\n💰 Ingreso Total:        ${ingreso_total:,.2f}")
print(f"💵 Utilidad Bruta:       ${utilidad_total:,.2f}")
print(f"📈 Margen Promedio:      {margen_promedio:.1f}%")
print(f"🛒 Ticket Promedio:      ${ticket_promedio:.2f}")
print(f"📦 Unidades Vendidas:    {unidades_vendidas:,}")
print(f"🧾 Transacciones:        {len(df_ventas):,}")

# ============================================
# 3. TOP PRODUCTOS
# ============================================
print("\n" + "="*70)
print("🏆 TOP 5 PRODUCTOS POR INGRESO")
print("="*70)

top_productos = df_ventas.groupby('nombre_producto').agg({
    'ingreso_total': 'sum',
    'cantidad': 'sum',
    'transaccion_id': 'count'
}).round(2)

top_productos.columns = ['Ingreso', 'Unidades', 'Transacciones']
top_productos = top_productos.sort_values('Ingreso', ascending=False).head(5)

print(top_productos.to_string())

# ============================================
# 4. ANÁLISIS POR CANAL
# ============================================
print("\n" + "="*70)
print("🏪 ANÁLISIS POR CANAL DE VENTA")
print("="*70)

canal_analysis = df_ventas.groupby('canal_venta').agg({
    'ingreso_total': ['sum', 'mean'],
    'utilidad_bruta': 'sum',
    'margen_porcentaje': 'mean',
    'transaccion_id': 'count'
}).round(2)

canal_analysis.columns = ['Ingreso Total', 'Ticket Promedio', 'Utilidad', 'Margen %', 'Num. Transacciones']
canal_analysis = canal_analysis.sort_values('Ingreso Total', ascending=False)

print(canal_analysis.to_string())

# ============================================
# 5. ANÁLISIS TEMPORAL
# ============================================
print("\n" + "="*70)
print("📅 ANÁLISIS TEMPORAL - VENTAS POR MES")
print("="*70)

ventas_mes = df_ventas.groupby('mes').agg({
    'ingreso_total': 'sum',
    'transaccion_id': 'count'
}).round(2)

ventas_mes.columns = ['Ingreso', 'Transacciones']

meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
         'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

for i, mes in enumerate(meses, 1):
    if i in ventas_mes.index:
        ing = ventas_mes.loc[i, 'Ingreso']
        trx = ventas_mes.loc[i, 'Transacciones']
        print(f"{mes:12s}: ${ing:>12,.2f}  ({trx:>4.0f} transacciones)")

# ============================================
# 6. ANÁLISIS GEOGRÁFICO
# ============================================
print("\n" + "="*70)
print("🌍 TOP 5 CIUDADES POR INGRESO")
print("="*70)

ciudades = df_ventas.groupby('ciudad').agg({
    'ingreso_total': 'sum',
    'transaccion_id': 'count'
}).round(2)

ciudades.columns = ['Ingreso', 'Transacciones']
ciudades = ciudades.sort_values('Ingreso', ascending=False).head(5)

print(ciudades.to_string())

# ============================================
# 7. ANÁLISIS DE CLIENTES
# ============================================
print("\n" + "="*70)
print("👥 SEGMENTACIÓN DE CLIENTES")
print("="*70)

segmentos = df_ventas.groupby('segmento_cliente').agg({
    'ingreso_total': 'sum',
    'utilidad_bruta': 'sum',
    'transaccion_id': 'count',
    'cliente_id': 'nunique'
}).round(2)

segmentos.columns = ['Ingreso', 'Utilidad', 'Transacciones', 'Clientes Únicos']
segmentos = segmentos.sort_values('Ingreso', ascending=False)

print(segmentos.to_string())

# ============================================
# 8. IMPACTO DE CAMPAÑAS
# ============================================
print("\n" + "="*70)
print("📢 IMPACTO DE CAMPAÑAS")
print("="*70)

# Ventas con campaña vs sin campaña
ventas_con_campana = df_ventas[df_ventas['campana'].notna()]
ventas_sin_campana = df_ventas[df_ventas['campana'].isna()]

print(f"\nTransacciones CON campaña:  {len(ventas_con_campana):,}")
print(f"Ingreso CON campaña:        ${ventas_con_campana['ingreso_total'].sum():,.2f}")
print(f"Ticket promedio CON:        ${ventas_con_campana['ingreso_total'].mean():.2f}")

print(f"\nTransacciones SIN campaña:  {len(ventas_sin_campana):,}")
print(f"Ingreso SIN campaña:        ${ventas_sin_campana['ingreso_total'].sum():,.2f}")
print(f"Ticket promedio SIN:        ${ventas_sin_campana['ingreso_total'].mean():.2f}")

# Top campañas
if len(ventas_con_campana) > 0:
    print("\n🏆 TOP CAMPAÑAS POR INGRESO:")
    top_campanas = ventas_con_campana.groupby('campana')['ingreso_total'].sum().sort_values(ascending=False).head(5)
    for campana, ingreso in top_campanas.items():
        print(f"  • {campana[:40]:40s}: ${ingreso:,.2f}")

# ============================================
# 9. MÉTRICAS OPERACIONALES
# ============================================
print("\n" + "="*70)
print("⚙️ MÉTRICAS OPERACIONALES")
print("="*70)

tasa_devolucion = (df_ventas['devolucion'].sum() / len(df_ventas) * 100)
dias_entrega_promedio = df_ventas['dias_entrega'].mean()
descuento_promedio = df_ventas['descuento_porcentaje'].mean()

print(f"\n📉 Tasa de Devolución:       {tasa_devolucion:.2f}%")
print(f"🚚 Días Entrega Promedio:    {dias_entrega_promedio:.1f} días")
print(f"🏷️  Descuento Promedio:       {descuento_promedio:.1f}%")

# ============================================
# 10. INSIGHTS CLAVE
# ============================================
print("\n" + "="*70)
print("💡 INSIGHTS CLAVE PARA PRESENTAR")
print("="*70)

# Mes más fuerte
mes_mas_fuerte = ventas_mes['Ingreso'].idxmax()
ingreso_mes_fuerte = ventas_mes['Ingreso'].max()

# Canal más rentable
canal_mas_rentable = canal_analysis['Margen %'].idxmax()
margen_canal = canal_analysis.loc[canal_mas_rentable, 'Margen %']

# Producto estrella
producto_estrella = top_productos.index[0]
ingreso_producto = top_productos.iloc[0]['Ingreso']

print(f"\n1. 🗓️  MES MÁS FUERTE:")
print(f"   {meses[mes_mas_fuerte-1]} con ${ingreso_mes_fuerte:,.2f}")

print(f"\n2. 🏪 CANAL MÁS RENTABLE:")
print(f"   {canal_mas_rentable} con {margen_canal:.1f}% de margen")

print(f"\n3. ⭐ PRODUCTO ESTRELLA:")
print(f"   {producto_estrella}")
print(f"   Generó ${ingreso_producto:,.2f} en el año")

print(f"\n4. 📊 CONCENTRACIÓN DE VENTAS:")
participacion_ptma = (df_ventas[df_ventas['ciudad'] == 'Ciudad de Panamá']['ingreso_total'].sum() / ingreso_total * 100)
print(f"   Ciudad de Panamá representa {participacion_ptma:.1f}% del ingreso total")

print(f"\n5. 💼 CLIENTES B2B vs B2C:")
b2b_ingreso = df_ventas[df_ventas['tipo_cliente'] == 'B2B']['ingreso_total'].sum()
b2c_ingreso = df_ventas[df_ventas['tipo_cliente'] == 'B2C']['ingreso_total'].sum()
print(f"   B2B: ${b2b_ingreso:,.2f} ({b2b_ingreso/ingreso_total*100:.1f}%)")
print(f"   B2C: ${b2c_ingreso:,.2f} ({b2c_ingreso/ingreso_total*100:.1f}%)")

print("\n" + "="*70)
print("✅ ANÁLISIS COMPLETADO")
print("="*70)
print("\n💾 Los datos están listos para importar a Power BI")
print("📊 Ubicación: outputs/ventas_transacciones.csv\n")