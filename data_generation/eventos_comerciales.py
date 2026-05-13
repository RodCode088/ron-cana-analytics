# eventos_comerciales.py
# Define las campañas y eventos comerciales de 2024

import pandas as pd
from datetime import datetime

def crear_eventos_comerciales():
    """
    Crea el calendario de eventos comerciales de Ron Caña Panamá 2024
    """
    
    eventos = [
        {
            'evento_id': 'EVT-001',
            'nombre': 'Lanzamiento Cask Finish Oporto',
            'fecha_inicio': '2024-01-20',
            'fecha_fin': '2024-01-27',
            'tipo': 'Lanzamiento Producto',
            'impacto_ventas': 1.8,  # 80% más ventas en esos días
            'productos_foco': 'RCP-CASKP-750',
            'canales_aplicables': 'Horeca Premium,Ecommerce',
            'descuento_adicional': 0,
            'descripcion': 'Lanzamiento de nueva edición Cask Finish'
        },
        {
            'evento_id': 'EVT-002',
            'nombre': 'San Valentín - Gifts',
            'fecha_inicio': '2024-02-10',
            'fecha_fin': '2024-02-14',
            'tipo': 'Campaña Estacional',
            'impacto_ventas': 1.5,
            'productos_foco': 'RCP-GIFT-A8,RCP-KIT-DEG',
            'canales_aplicables': 'Ecommerce,Retail Moderno',
            'descuento_adicional': 10,
            'descripcion': 'Promoción especial regalos San Valentín'
        },
        {
            'evento_id': 'EVT-003',
            'nombre': 'Feria del Ron Panamá 2024',
            'fecha_inicio': '2024-03-22',
            'fecha_fin': '2024-03-24',
            'tipo': 'Evento Industria',
            'impacto_ventas': 2.8,
            'productos_foco': 'RCP-EDLIM-750,RCP-KIT-DEG,RCP-XO18-750',
            'canales_aplicables': 'Ecommerce,Duty Free',
            'descuento_adicional': 0,
            'descripcion': 'Participación en feria nacional del ron'
        },
        {
            'evento_id': 'EVT-004',
            'nombre': 'Semana Santa',
            'fecha_inicio': '2024-03-25',
            'fecha_fin': '2024-03-31',
            'tipo': 'Campaña Estacional',
            'impacto_ventas': 1.4,
            'productos_foco': 'RCP-A5-750,RCP-A8-750',
            'canales_aplicables': 'Retail Moderno,Supermercados',
            'descuento_adicional': 15,
            'descripcion': 'Promoción Semana Santa'
        },
        {
            'evento_id': 'EVT-005',
            'nombre': 'Día del Padre',
            'fecha_inicio': '2024-06-10',
            'fecha_fin': '2024-06-16',
            'tipo': 'Campaña Estacional',
            'impacto_ventas': 2.1,
            'productos_foco': 'RCP-GIFT-A8,RCP-EA12-750,RCP-SB-750',
            'canales_aplicables': 'Ecommerce,Retail Moderno,Supermercados',
            'descuento_adicional': 12,
            'descripcion': 'Campaña especial Día del Padre'
        },
        {
            'evento_id': 'EVT-006',
            'nombre': 'Aniversario Ron Caña (6 años)',
            'fecha_inicio': '2024-08-15',
            'fecha_fin': '2024-08-18',
            'tipo': 'Evento Marca',
            'impacto_ventas': 1.7,
            'productos_foco': 'RCP-EDLIM-750',
            'canales_aplicables': 'Ecommerce,Horeca Premium',
            'descuento_adicional': 0,
            'descripcion': 'Celebración aniversario de la marca'
        },
        {
            'evento_id': 'EVT-007',
            'nombre': 'Fiestas Patrias',
            'fecha_inicio': '2024-10-28',
            'fecha_fin': '2024-11-03',
            'tipo': 'Campaña Patriótica',
            'impacto_ventas': 1.6,
            'productos_foco': 'RCP-A8-750,RCP-RE-750',
            'canales_aplicables': 'Retail Moderno,Supermercados',
            'descuento_adicional': 10,
            'descripcion': 'Promoción fiestas patrias de Panamá'
        },
        {
            'evento_id': 'EVT-008',
            'nombre': 'Black Friday',
            'fecha_inicio': '2024-11-29',
            'fecha_fin': '2024-12-01',
            'tipo': 'Promoción',
            'impacto_ventas': 3.5,
            'productos_foco': 'RCP-A5-750,RCP-A8-750,RCP-KIT-DEG',
            'canales_aplicables': 'Ecommerce,Retail Moderno',
            'descuento_adicional': 25,
            'descripcion': 'Black Friday - descuentos agresivos'
        },
        {
            'evento_id': 'EVT-009',
            'nombre': 'Regalos Corporativos Navidad',
            'fecha_inicio': '2024-12-01',
            'fecha_fin': '2024-12-15',
            'tipo': 'B2B Corporativo',
            'impacto_ventas': 2.4,
            'productos_foco': 'RCP-GIFT-A8,RCP-EDLIM-750,RCP-SO15-750',
            'canales_aplicables': 'Corporativo',
            'descuento_adicional': 8,
            'descripcion': 'Campaña regalos corporativos fin de año'
        },
        {
            'evento_id': 'EVT-010',
            'nombre': 'Temporada Navideña',
            'fecha_inicio': '2024-12-15',
            'fecha_fin': '2024-12-31',
            'tipo': 'Campaña Estacional',
            'impacto_ventas': 2.2,
            'productos_foco': 'RCP-GIFT-A8,RCP-A8-750,RCP-EA12-750',
            'canales_aplicables': 'Ecommerce,Retail Moderno,Supermercados,Horeca Premium',
            'descuento_adicional': 12,
            'descripcion': 'Temporada navideña general'
        }
    ]
    
    df = pd.DataFrame(eventos)
    
    # Convertir fechas a datetime
    df['fecha_inicio'] = pd.to_datetime(df['fecha_inicio'])
    df['fecha_fin'] = pd.to_datetime(df['fecha_fin'])
    
    # Calcular duración
    df['duracion_dias'] = (df['fecha_fin'] - df['fecha_inicio']).dt.days + 1
    
    return df


def guardar_eventos():
    """
    Guarda los eventos en CSV
    """
    df_eventos = crear_eventos_comerciales()
    
    ruta_salida = 'outputs/eventos_comerciales.csv'
    df_eventos.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
    
    print("="*60)
    print("✅ EVENTOS COMERCIALES GENERADOS")
    print("="*60)
    print(f"📁 Archivo guardado en: {ruta_salida}")
    print(f"📅 Total de eventos: {len(df_eventos)}")
    print()
    print("📊 EVENTOS POR TIPO:")
    print(df_eventos['tipo'].value_counts())
    print()
    print("📋 CALENDARIO 2024:")
    print(df_eventos[['nombre', 'fecha_inicio', 'fecha_fin', 'impacto_ventas']].to_string(index=False))
    print("="*60)
    
    return df_eventos


if __name__ == '__main__':
    guardar_eventos()