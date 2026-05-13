# dim_productos.py
# Genera el catálogo de productos de Ron Caña Panamá

import pandas as pd

def crear_catalogo_productos():
    """
    Crea el catálogo completo con los 14 productos de Ron Caña
    """
    
    productos = [
        # ============================================
        # CATEGORÍA: ENTRADA (Entry Level)
        # ============================================
        {
            'producto_id': 'RCP-BL-750',
            'nombre_producto': 'Ron Caña Blanco Artesanal',
            'categoria': 'Blanco',
            'subcategoria': 'Entry',
            'precio_lista': 18.00,
            'costo_unitario': 7.50,
            'formato': '750ml',
            'años_añejamiento': 0,
            'descripcion': 'Ron blanco artesanal destilado tres veces',
            'activo': True
        },
        {
            'producto_id': 'RCP-SP-750',
            'nombre_producto': 'Ron Caña Spiced',
            'categoria': 'Especialidad',
            'subcategoria': 'Entry',
            'precio_lista': 22.00,
            'costo_unitario': 9.00,
            'formato': '750ml',
            'años_añejamiento': 0,
            'descripcion': 'Ron especiado con canela, vainilla y clavo',
            'activo': True
        },
        
        # ============================================
        # CATEGORÍA: CORE (Productos principales)
        # ============================================
        {
            'producto_id': 'RCP-A5-750',
            'nombre_producto': 'Ron Caña Añejo 5 Años',
            'categoria': 'Añejo',
            'subcategoria': 'Core',
            'precio_lista': 32.00,
            'costo_unitario': 14.00,
            'formato': '750ml',
            'años_añejamiento': 5,
            'descripcion': 'Añejado 5 años en barricas de roble americano',
            'activo': True
        },
        {
            'producto_id': 'RCP-A5-375',
            'nombre_producto': 'Ron Caña Añejo 5 Años',
            'categoria': 'Añejo',
            'subcategoria': 'Core',
            'precio_lista': 18.00,
            'costo_unitario': 8.00,
            'formato': '375ml',
            'años_añejamiento': 5,
            'descripcion': 'Media botella - Añejado 5 años',
            'activo': True
        },
        {
            'producto_id': 'RCP-A8-750',
            'nombre_producto': 'Ron Caña Añejo 8 Años',
            'categoria': 'Añejo',
            'subcategoria': 'Core',
            'precio_lista': 42.00,
            'costo_unitario': 18.00,
            'formato': '750ml',
            'años_añejamiento': 8,
            'descripcion': 'Añejado 8 años - Perfil complejo',
            'activo': True
        },
        {
            'producto_id': 'RCP-RE-750',
            'nombre_producto': 'Ron Caña Reserva Especial',
            'categoria': 'Añejo',
            'subcategoria': 'Core',
            'precio_lista': 38.00,
            'costo_unitario': 16.50,
            'formato': '750ml',
            'años_añejamiento': 6,
            'descripcion': 'Blend especial de 6 años',
            'activo': True
        },
        
        # ============================================
        # CATEGORÍA: PREMIUM
        # ============================================
        {
            'producto_id': 'RCP-EA12-750',
            'nombre_producto': 'Ron Caña Extra Añejo 12 Años',
            'categoria': 'Extra Añejo',
            'subcategoria': 'Premium',
            'precio_lista': 68.00,
            'costo_unitario': 28.00,
            'formato': '750ml',
            'años_añejamiento': 12,
            'descripcion': 'Extra añejo 12 años - Premium',
            'activo': True
        },
        {
            'producto_id': 'RCP-SO15-750',
            'nombre_producto': 'Ron Caña Solera 15 Años',
            'categoria': 'Extra Añejo',
            'subcategoria': 'Premium',
            'precio_lista': 85.00,
            'costo_unitario': 36.00,
            'formato': '750ml',
            'años_añejamiento': 15,
            'descripcion': 'Método Solera - 15 años',
            'activo': True
        },
        {
            'producto_id': 'RCP-SB-750',
            'nombre_producto': 'Ron Caña Single Barrel',
            'categoria': 'Premium',
            'subcategoria': 'Premium',
            'precio_lista': 72.00,
            'costo_unitario': 30.00,
            'formato': '750ml',
            'años_añejamiento': 10,
            'descripcion': 'Barrica única - Edición numerada',
            'activo': True
        },
        
        # ============================================
        # CATEGORÍA: ULTRA PREMIUM
        # ============================================
        {
            'producto_id': 'RCP-EDLIM-750',
            'nombre_producto': 'Ron Caña Edición Limitada Roble Europeo',
            'categoria': 'Ultra Premium',
            'subcategoria': 'Ultra Premium',
            'precio_lista': 180.00,
            'costo_unitario': 75.00,
            'formato': '750ml',
            'años_añejamiento': 12,
            'descripcion': 'Edición limitada - Barricas roble europeo',
            'activo': True
        },
        {
            'producto_id': 'RCP-CASKP-750',
            'nombre_producto': 'Ron Caña Cask Finish Oporto',
            'categoria': 'Ultra Premium',
            'subcategoria': 'Ultra Premium',
            'precio_lista': 155.00,
            'costo_unitario': 65.00,
            'formato': '750ml',
            'años_añejamiento': 14,
            'descripcion': 'Finalizado en barricas de vino Oporto',
            'activo': True
        },
        {
            'producto_id': 'RCP-XO18-750',
            'nombre_producto': 'Ron Caña XO 18 Años',
            'categoria': 'Ultra Premium',
            'subcategoria': 'Ultra Premium',
            'precio_lista': 245.00,
            'costo_unitario': 105.00,
            'formato': '750ml',
            'años_añejamiento': 18,
            'descripcion': 'Extra Old - Máxima expresión',
            'activo': True
        },
        
        # ============================================
        # CATEGORÍA: GIFT SETS
        # ============================================
        {
            'producto_id': 'RCP-KIT-DEG',
            'nombre_producto': 'Kit Degustación Premium',
            'categoria': 'Gift',
            'subcategoria': 'Gift',
            'precio_lista': 48.00,
            'costo_unitario': 22.00,
            'formato': '3x200ml',
            'años_añejamiento': 0,  # Mix de edades
            'descripcion': 'Set degustación: Añejo 5, 8 y 12 años',
            'activo': True
        },
        {
            'producto_id': 'RCP-GIFT-A8',
            'nombre_producto': 'Gift Set Añejo 8 Años + 2 Copas',
            'categoria': 'Gift',
            'subcategoria': 'Gift',
            'precio_lista': 65.00,
            'costo_unitario': 28.00,
            'formato': 'Set',
            'años_añejamiento': 8,
            'descripcion': 'Estuche regalo con botella y 2 copas premium',
            'activo': True
        }
    ]
    
    # Convertir la lista de productos a DataFrame (tabla)
    df = pd.DataFrame(productos)
    
    # Calcular columnas adicionales
    df['margen_porcentaje'] = ((df['precio_lista'] - df['costo_unitario']) / df['precio_lista'] * 100).round(1)
    df['utilidad_unitaria'] = (df['precio_lista'] - df['costo_unitario']).round(2)
    
    return df


def guardar_catalogo():
    """
    Guarda el catálogo en un archivo CSV
    """
    # Crear el catálogo
    df_productos = crear_catalogo_productos()
    
    # Guardar en CSV
    ruta_salida = 'outputs/dim_productos.csv'
    df_productos.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
    
    # Mostrar resumen
    print("="*60)
    print("✅ CATÁLOGO DE PRODUCTOS GENERADO")
    print("="*60)
    print(f"📁 Archivo guardado en: {ruta_salida}")
    print(f"📦 Total de productos: {len(df_productos)}")
    print()
    print("📊 RESUMEN POR CATEGORÍA:")
    print(df_productos['categoria'].value_counts())
    print()
    print("💰 RANGO DE PRECIOS:")
    print(f"   Mínimo: ${df_productos['precio_lista'].min():.2f}")
    print(f"   Máximo: ${df_productos['precio_lista'].max():.2f}")
    print(f"   Promedio: ${df_productos['precio_lista'].mean():.2f}")
    print()
    print("📋 VISTA PREVIA:")
    print(df_productos[['producto_id', 'nombre_producto', 'precio_lista', 'margen_porcentaje']].to_string(index=False))
    print("="*60)
    
    return df_productos


# Este código se ejecuta cuando corres el archivo directamente
if __name__ == '__main__':
    guardar_catalogo()