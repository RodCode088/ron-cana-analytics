# dim_clientes.py
# Genera la base de clientes de Ron Caña Panamá

import pandas as pd
import random
from config import CIUDADES

def crear_base_clientes():
    """
    Crea la base de 80 clientes distribuidos por tipo y geografía
    """
    
    clientes = []
    
    # ============================================
    # HOTELES 5 ESTRELLAS (8 clientes)
    # ============================================
    hoteles_5_estrellas = [
        {'nombre': 'Hotel Bristol Panamá', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'The Santa María Golf & Country Club', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'American Trade Hotel', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Sortis Hotel & Casino', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Dreams Delight Playa Bonita', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Westin Playa Bonita', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Gamboa Rainforest Resort', 'ciudad': 'Colón'},
        {'nombre': 'The Haven & Spa', 'ciudad': 'Coronado'}
    ]
    
    for i, hotel in enumerate(hoteles_5_estrellas, 1):
        clientes.append({
            'cliente_id': f'CLI-H5-{i:03d}',
            'nombre_cliente': hotel['nombre'],
            'tipo_cliente': 'B2B',
            'segmento': 'Hotel 5 Estrellas',
            'ciudad': hotel['ciudad'],
            'rating_crediticio': 'A+',
            'frecuencia_compra': 'Alta',
            'ticket_promedio_estimado': random.randint(2500, 4000),
            'activo': True
        })
    
    # ============================================
    # HOTELES 4 ESTRELLAS (12 clientes)
    # ============================================
    hoteles_4_estrellas = [
        {'nombre': 'Hotel Central', 'ciudad': 'David'},
        {'nombre': 'Hotel Isla Verde', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Hotel Riande Continental', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Best Western Plus', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Radisson Summit Golf', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Hotel Milano', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'City of David Hotel', 'ciudad': 'David'},
        {'nombre': 'Hotel Castilla', 'ciudad': 'David'},
        {'nombre': 'Hotel Santiago Plaza', 'ciudad': 'Santiago'},
        {'nombre': 'Hotel Guayacanes', 'ciudad': 'Boquete'},
        {'nombre': 'Hotel Hibiscus', 'ciudad': 'Chitré'},
        {'nombre': 'Hotel Dos Mares', 'ciudad': 'Colón'}
    ]
    
    for i, hotel in enumerate(hoteles_4_estrellas, 1):
        clientes.append({
            'cliente_id': f'CLI-H4-{i:03d}',
            'nombre_cliente': hotel['nombre'],
            'tipo_cliente': 'B2B',
            'segmento': 'Hotel 4 Estrellas',
            'ciudad': hotel['ciudad'],
            'rating_crediticio': random.choice(['A+', 'A', 'A']),
            'frecuencia_compra': 'Media-Alta',
            'ticket_promedio_estimado': random.randint(1200, 2200),
            'activo': True
        })
    
    # ============================================
    # RESTAURANTES GOURMET (15 clientes)
    # ============================================
    restaurantes_gourmet = [
        {'nombre': 'Manolo Caracol', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Maito', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Donde José', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Intimo', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Fonda Lo Que Hay', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'La Posta', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Tantalo Kitchen', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Makoto', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Las Clementinas', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Azafrán', 'ciudad': 'David'},
        {'nombre': 'Restaurante Karlota', 'ciudad': 'Boquete'},
        {'nombre': 'The Rock', 'ciudad': 'Boquete'},
        {'nombre': 'Il Baretto', 'ciudad': 'Coronado'},
        {'nombre': 'Restaurante Los Camisones', 'ciudad': 'Santiago'},
        {'nombre': 'El Trapiche', 'ciudad': 'Ciudad de Panamá'}
    ]
    
    for i, rest in enumerate(restaurantes_gourmet, 1):
        clientes.append({
            'cliente_id': f'CLI-RG-{i:03d}',
            'nombre_cliente': rest['nombre'],
            'tipo_cliente': 'B2B',
            'segmento': 'Restaurante Gourmet',
            'ciudad': rest['ciudad'],
            'rating_crediticio': random.choice(['A+', 'A', 'A', 'B+']),
            'frecuencia_compra': 'Alta',
            'ticket_promedio_estimado': random.randint(800, 1500),
            'activo': True
        })
    
    # ============================================
    # RESTAURANTES CASUAL PREMIUM (10 clientes)
    # ============================================
    restaurantes_casual = [
        {'nombre': 'Crepes & Waffles', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Madrigal', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Mercado de Mariscos', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Parrillada Gaucha', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Beirut', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Napoli Pizza', 'ciudad': 'David'},
        {'nombre': 'Restaurante El Ancla', 'ciudad': 'Colón'},
        {'nombre': 'Restaurante Mirador', 'ciudad': 'Santiago'},
        {'nombre': 'Big Daddy', 'ciudad': 'Boquete'},
        {'nombre': 'La Vespa', 'ciudad': 'Coronado'}
    ]
    
    for i, rest in enumerate(restaurantes_casual, 1):
        clientes.append({
            'cliente_id': f'CLI-RC-{i:03d}',
            'nombre_cliente': rest['nombre'],
            'tipo_cliente': 'B2B',
            'segmento': 'Restaurante Casual Premium',
            'ciudad': rest['ciudad'],
            'rating_crediticio': random.choice(['A', 'B+', 'B']),
            'frecuencia_compra': 'Media',
            'ticket_promedio_estimado': random.randint(400, 900),
            'activo': True
        })
    
    # ============================================
    # BARES TOP / SPEAKEASY (8 clientes)
    # ============================================
    bares = [
        {'nombre': 'Pedro Mandinga Rum Bar', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'La Rana Dorada', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Istmo Brew Pub', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Unplugged', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Lounge Bar Raices', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Barlovento', 'ciudad': 'Bocas del Toro'},
        {'nombre': 'Zanzibar', 'ciudad': 'Bocas del Toro'},
        {'nombre': 'Casa Brewing Co', 'ciudad': 'David'}
    ]
    
    for i, bar in enumerate(bares, 1):
        clientes.append({
            'cliente_id': f'CLI-BAR-{i:03d}',
            'nombre_cliente': bar['nombre'],
            'tipo_cliente': 'B2B',
            'segmento': 'Bar Top',
            'ciudad': bar['ciudad'],
            'rating_crediticio': random.choice(['A', 'B+', 'B+']),
            'frecuencia_compra': 'Alta',
            'ticket_promedio_estimado': random.randint(600, 1100),
            'activo': True
        })
    
    # ============================================
    # SUPERMERCADOS (6 clientes)
    # ============================================
    supermercados = [
        {'nombre': 'Super 99 Central', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Rey Multiplaza', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Riba Smith Paitilla', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Super 99 David', 'ciudad': 'David'},
        {'nombre': 'El Machetazo Colón', 'ciudad': 'Colón'},
        {'nombre': 'Super Centro Santiago', 'ciudad': 'Santiago'}
    ]
    
    for i, super in enumerate(supermercados, 1):
        clientes.append({
            'cliente_id': f'CLI-SUP-{i:03d}',
            'nombre_cliente': super['nombre'],
            'tipo_cliente': 'B2B',
            'segmento': 'Supermercado',
            'ciudad': super['ciudad'],
            'rating_crediticio': 'A+',
            'frecuencia_compra': 'Alta',
            'ticket_promedio_estimado': random.randint(6000, 10000),
            'activo': True
        })
    
    # ============================================
    # LICORERÍAS ESPECIALIZADAS (12 clientes)
    # ============================================
    licorerías = [
        {'nombre': 'La Europea Premium', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'The Wine Bar', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Licores y Vinos PTY', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Vinoteca 507', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Licorería Premium Costa del Este', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'El Bodegón', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Licorería El Padrino', 'ciudad': 'David'},
        {'nombre': 'Licores Premium David', 'ciudad': 'David'},
        {'nombre': 'Licorería Central Colón', 'ciudad': 'Colón'},
        {'nombre': 'Licorería La Bodega', 'ciudad': 'Santiago'},
        {'nombre': 'Vinos y Licores Chitré', 'ciudad': 'Chitré'},
        {'nombre': 'Licorería Penonomé', 'ciudad': 'Penonomé'}
    ]
    
    for i, lic in enumerate(licorerías, 1):
        clientes.append({
            'cliente_id': f'CLI-LIC-{i:03d}',
            'nombre_cliente': lic['nombre'],
            'tipo_cliente': 'B2B',
            'segmento': 'Licorería Especializada',
            'ciudad': lic['ciudad'],
            'rating_crediticio': random.choice(['A+', 'A', 'A', 'B+']),
            'frecuencia_compra': 'Media-Alta',
            'ticket_promedio_estimado': random.randint(1500, 2800),
            'activo': True
        })
    
    # ============================================
    # TIENDAS DE CONVENIENCIA (5 clientes)
    # ============================================
    conveniencia = [
        {'nombre': 'Delta Vía España', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Delta Costa del Este', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': '7-Eleven Albrook', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Delta David', 'ciudad': 'David'},
        {'nombre': 'Minisuper Express Colón', 'ciudad': 'Colón'}
    ]
    
    for i, conv in enumerate(conveniencia, 1):
        clientes.append({
            'cliente_id': f'CLI-CONV-{i:03d}',
            'nombre_cliente': conv['nombre'],
            'tipo_cliente': 'B2B',
            'segmento': 'Tienda Conveniencia',
            'ciudad': conv['ciudad'],
            'rating_crediticio': random.choice(['A', 'B+', 'B']),
            'frecuencia_compra': 'Media',
            'ticket_promedio_estimado': random.randint(300, 700),
            'activo': True
        })
    
    # ============================================
    # DISTRIBUIDORES MAYORISTAS (3 clientes)
    # ============================================
    distribuidores = [
        {'nombre': 'Distribuidora Melo', 'ciudad': 'Colón'},
        {'nombre': 'Distribuciones Chiriquí', 'ciudad': 'David'},
        {'nombre': 'Distribuidora Central PTY', 'ciudad': 'Ciudad de Panamá'}
    ]
    
    for i, dist in enumerate(distribuidores, 1):
        clientes.append({
            'cliente_id': f'CLI-DIST-{i:03d}',
            'nombre_cliente': dist['nombre'],
            'tipo_cliente': 'B2B',
            'segmento': 'Distribuidor Mayorista',
            'ciudad': dist['ciudad'],
            'rating_crediticio': 'A+',
            'frecuencia_compra': 'Baja',  # Compran mucho pero no seguido
            'ticket_promedio_estimado': random.randint(12000, 20000),
            'activo': True
        })
    
    # ============================================
    # CLIENTES CORPORATIVOS (6 clientes)
    # ============================================
    corporativos = [
        {'nombre': 'Cable & Wireless Panamá', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Copa Airlines', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Banco General', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'ASSA Compañía de Seguros', 'ciudad': 'Ciudad de Panamá'},
        {'nombre': 'Grupo Melo', 'ciudad': 'Colón'},
        {'nombre': 'Cervecería Nacional', 'ciudad': 'Ciudad de Panamá'}
    ]
    
    for i, corp in enumerate(corporativos, 1):
        clientes.append({
            'cliente_id': f'CLI-CORP-{i:03d}',
            'nombre_cliente': corp['nombre'],
            'tipo_cliente': 'B2B',
            'segmento': 'Corporativo',
            'ciudad': corp['ciudad'],
            'rating_crediticio': 'A+',
            'frecuencia_compra': 'Baja',  # Compras estacionales grandes
            'ticket_promedio_estimado': random.randint(3500, 6000),
            'activo': True
        })
    
    # ============================================
    # CONSUMIDORES FINALES (15 clientes)
    # ============================================
    nombres_personas = [
        'Juan Pérez', 'María González', 'Carlos Rodríguez', 'Ana Martínez',
        'Roberto Chen', 'Laura Sánchez', 'Diego Morales', 'Sofía Vargas',
        'Andrés Castro', 'Valentina Díaz', 'Fernando Ortiz', 'Camila Torres',
        'Luis Herrera', 'Isabella Ramírez', 'Gabriel Flores'
    ]
    
    ciudades_consumidores = ['Ciudad de Panamá'] * 10 + ['David'] * 2 + ['Coronado', 'Boquete', 'Colón']
    
    for i, nombre in enumerate(nombres_personas, 1):
        clientes.append({
            'cliente_id': f'CLI-FINAL-{i:03d}',
            'nombre_cliente': nombre,
            'tipo_cliente': 'B2C',
            'segmento': 'Consumidor Final',
            'ciudad': ciudades_consumidores[i-1],
            'rating_crediticio': random.choice(['A', 'B+', 'B', 'B', 'C']),
            'frecuencia_compra': 'Baja',
            'ticket_promedio_estimado': random.randint(50, 200),
            'activo': True
        })
    
    return pd.DataFrame(clientes)


def guardar_base_clientes():
    """
    Guarda la base de clientes en CSV
    """
    df_clientes = crear_base_clientes()
    
    # Guardar
    ruta_salida = 'outputs/dim_clientes.csv'
    df_clientes.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
    
    # Mostrar resumen
    print("="*60)
    print("✅ BASE DE CLIENTES GENERADA")
    print("="*60)
    print(f"📁 Archivo guardado en: {ruta_salida}")
    print(f"👥 Total de clientes: {len(df_clientes)}")
    print()
    print("📊 DISTRIBUCIÓN POR SEGMENTO:")
    print(df_clientes['segmento'].value_counts())
    print()
    print("🌍 DISTRIBUCIÓN POR CIUDAD:")
    print(df_clientes['ciudad'].value_counts())
    print()
    print("💼 B2B vs B2C:")
    print(df_clientes['tipo_cliente'].value_counts())
    print()
    print("📋 VISTA PREVIA:")
    print(df_clientes[['cliente_id', 'nombre_cliente', 'segmento', 'ciudad', 'ticket_promedio_estimado']].head(10).to_string(index=False))
    print("="*60)
    
    return df_clientes


if __name__ == '__main__':
    guardar_base_clientes()