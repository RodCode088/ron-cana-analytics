# calcular_insights.py
# Calcula los insights clave para el Insight Box

import pandas as pd

print("="*70)
print("🔍 CALCULANDO INSIGHTS CLAVE")
print("="*70)

# Cargar datos
df = pd.read_csv('outputs/ventas_transacciones.csv')

# ============================================
# INSIGHT 1: Concentración de Diciembre
# ============================================
ventas_mes = df.groupby('mes')['ingreso_total'].sum()
total_anual = df['ingreso_total'].sum()
ingreso_diciembre = ventas_mes[12]
porcentaje_diciembre = (ingreso_diciembre / total_anual * 100)

print(f"\n📅 INSIGHT 1: ESTACIONALIDAD")
print(f"   Diciembre representa: {porcentaje_diciembre:.1f}% del ingreso anual")
print(f"   Ingreso Diciembre: ${ingreso_diciembre:,.2f}")
print(f"   Ingreso Total Año: ${total_anual:,.2f}")

# ============================================
# INSIGHT 2: Producto Edición Limitada
# ============================================
# Filtrar Edición Limitada
ed_limitada = df[df['producto_id'] == 'RCP-EDLIM-750']

unidades_ed_lim = ed_limitada['cantidad'].sum()
total_unidades = df['cantidad'].sum()
porcentaje_unidades = (unidades_ed_lim / total_unidades * 100)

ingreso_ed_lim = ed_limitada['ingreso_total'].sum()
porcentaje_ingreso_ed_lim = (ingreso_ed_lim / total_anual * 100)

print(f"\n⭐ INSIGHT 2: EDICIÓN LIMITADA")
print(f"   % de unidades: {porcentaje_unidades:.1f}%")
print(f"   % de ingresos: {porcentaje_ingreso_ed_lim:.1f}%")
print(f"   Ratio: Genera {porcentaje_ingreso_ed_lim/porcentaje_unidades:.1f}x más ingreso por unidad")

# ============================================
# INSIGHT 3: Canal Supermercados vs Horeca
# ============================================
canal_analysis = df.groupby('canal_venta').agg({
    'ingreso_total': 'sum',
    'margen_porcentaje': 'mean'
}).round(2)

margen_super = canal_analysis.loc['Supermercados', 'margen_porcentaje']
margen_horeca = canal_analysis.loc['Horeca Premium', 'margen_porcentaje']
diferencia_margen = margen_horeca - margen_super

ingreso_super = canal_analysis.loc['Supermercados', 'ingreso_total']
ingreso_horeca = canal_analysis.loc['Horeca Premium', 'ingreso_total']

print(f"\n🏪 INSIGHT 3: CANALES")
print(f"   Supermercados:")
print(f"     - Ingreso: ${ingreso_super:,.2f}")
print(f"     - Margen: {margen_super:.1f}%")
print(f"   Horeca Premium:")
print(f"     - Ingreso: ${ingreso_horeca:,.2f}")
print(f"     - Margen: {margen_horeca:.1f}%")
print(f"   → Horeca tiene {diferencia_margen:.1f} puntos más de margen")

# ============================================
# INSIGHT 4: B2B vs B2C
# ============================================
b2b_ingreso = df[df['tipo_cliente'] == 'B2B']['ingreso_total'].sum()
b2c_ingreso = df[df['tipo_cliente'] == 'B2C']['ingreso_total'].sum()
porcentaje_b2b = (b2b_ingreso / total_anual * 100)
porcentaje_b2c = (b2c_ingreso / total_anual * 100)

print(f"\n💼 INSIGHT 4: SEGMENTACIÓN B2B/B2C")
print(f"   B2B: ${b2b_ingreso:,.2f} ({porcentaje_b2b:.1f}%)")
print(f"   B2C: ${b2c_ingreso:,.2f} ({porcentaje_b2c:.1f}%)")

# ============================================
# INSIGHT 5: Impacto de Campañas
# ============================================
ventas_con_campana = df[df['campana'].notna()]
ventas_sin_campana = df[df['campana'].isna()]

ticket_con = ventas_con_campana['ingreso_total'].mean()
ticket_sin = ventas_sin_campana['ingreso_total'].mean()
incremento_ticket = ((ticket_con - ticket_sin) / ticket_sin * 100)

ingreso_campanas = ventas_con_campana['ingreso_total'].sum()
porcentaje_ingreso_campanas = (ingreso_campanas / total_anual * 100)

print(f"\n📢 INSIGHT 5: CAMPAÑAS")
print(f"   Ingreso con campañas: ${ingreso_campanas:,.2f} ({porcentaje_ingreso_campanas:.1f}%)")
print(f"   Ticket promedio CON campaña: ${ticket_con:,.2f}")
print(f"   Ticket promedio SIN campaña: ${ticket_sin:,.2f}")
print(f"   → Incremento de ticket: {incremento_ticket:.1f}%")

# ============================================
# INSIGHT 6: Top Ciudad
# ============================================
ciudad_top = df.groupby('ciudad')['ingreso_total'].sum().sort_values(ascending=False)
ciudad_1 = ciudad_top.index[0]
ingreso_ciudad_1 = ciudad_top.iloc[0]
porcentaje_ciudad = (ingreso_ciudad_1 / total_anual * 100)

print(f"\n🌍 INSIGHT 6: CONCENTRACIÓN GEOGRÁFICA")
print(f"   {ciudad_1}: ${ingreso_ciudad_1:,.2f} ({porcentaje_ciudad:.1f}%)")

# ============================================
# RESUMEN PARA INSIGHT BOX
# ============================================
print("\n" + "="*70)
print("📝 INSIGHTS PARA TU DASHBOARD:")
print("="*70)

print(f"""
1. Diciembre concentra {porcentaje_diciembre:.0f}% del ingreso anual
   → Oportunidad: Suavizar estacionalidad con campañas Q1-Q2

2. Edición Limitada: {porcentaje_unidades:.1f}% de unidades pero {porcentaje_ingreso_ed_lim:.0f}% de ingresos
   → Estrategia: Expandir línea ultra-premium

3. Horeca Premium tiene {diferencia_margen:.0f} pts más margen que Supermercados
   → Recomendación: Priorizar canal Horeca en mix comercial

4. B2B representa {porcentaje_b2b:.0f}% del ingreso total
   → Potencial: Canal B2C está subexplotado

5. Campañas incrementan ticket promedio {incremento_ticket:.0f}%
   → ROI positivo - continuar estrategia promocional
""")

print("="*70) 