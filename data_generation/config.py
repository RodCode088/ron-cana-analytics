# Config.py
# Configuración central del proyecto Ron Caña Panamá

from datetime import datetime

#=====================================================
# CONFIGURACIÓN GENERAL
#=====================================================

EMPRESA = {
    'nombre': 'Ron Caña Panamá',
    'fundacion': 2018,
    'slogan': 'Ron panameño de alta gama'
}

FECHA_INICIO = datetime(2024, 1, 1)
FECHA_FIN = datetime(2024, 12, 31)
NUM_TRANSACCIONES_OBJETIVO = 4200

#=====================================================
#ESTACIONALIDAD - Patrones de Ventas
#=====================================================

# CADA MES TIENE UN MULTIPLICADOR DE VENTAS
# 1.0 = ventas normales
# 0.7 =30% menos ventas
# 1.4 = 40% más ventas

ESTACIONALIDAD_MES = {
    1: 0.70,     # Enero - Caída post navidad
    2: 0.75,     # Febrero - Bajo
    3: 0.85,     # Marzo - Recuperación
    4: 0.80,     # Abril- Normal-bajo
    5: 0.90,     # Mayo - Normal
    6: 0.95,     # Junio - Día del Padre
    7: 0.95,     # Julio - Verano
    8: 0.85,     # Agosto - Normal
    9: 0.85,     # Septiembre - Bajo
    10: 0.95,    #Octubre - Preparación fin de año
    11: 1.15,   #Noviembre - Black Friday
    12: 1.40    #Diciembre - PICO (Navidad)
} 

# Muliplicador por día de la semana
# Sábado es el día más fuerte
MULTIPLICADOR_DIA_SEMANA = {
    0: 0.70,    # Lunes
    1: 0.75,    # Martes
    2: 0.80,    # Miércoles
    3: 0.90,    # Jueves
    4: 1.10,    # Viernes
    5: 1.30,    # Sábado - DÍA FUERTE
    6: 0.95     # Domingo
}

# ======================================================
#CANALES DE VENTA
# ======================================================

CANALES = {
    'Horeca Premium': {
        'peso': 0.25,                       # 25% de las ventas
        'ticket_min': 800,                  # Compra mínima $800
        'ticket_max': 4500,                 # Compra máxima $4500
        'frecuencia_dias_promedio': 7,      # Compran cada 7 días
        'descuento_max': 15,                # Máximo 15% descuento
        'productos_preferidos': ['RCP-EA12-750', 'RCP-A8-750', 'RCP-S015-750']
    },
    'Retail Moderno': {
        'peso': 0.30,
        'ticket_min': 150,
        'ticket_max': 1200,
        'frecuencia_dias_promedio': 14,
        'descuento_max': 20,
        'productos_preferidos': ['RCP-A5-750', 'RCP-A8-750', 'RCP-BL-750']
    },
    'Supermercados': {
        'peso': 0.20,
        'ticket_min': 3000,
        'ticket_max': 12000,
        'frecuencia_dias_promedio': 7,
        'descuento_max': 18,
        'productos_preferidos': ['RECP-A5-750', 'RCP-BL-750', 'RCP-SP-750']
    },
    'Ecommerce': {
        'peso': 0.12,
        'ticket_min': 50,
        'ticket_max': 350,
        'freceuncia_dias_promedio': 30,
        'descuento_max': 25,
        'productos_preferidos': ['RCP-GIFT-A8', 'RCP-KIT-DEG', 'RCP-EDLIM-750']
    },
    'Duty Free': {
        'peso': 0.08,
        'ticket_min: 200,'
        'ticket_max': 15000,
        'frecuencia_dias_promedio': 60,
        'descuento_max': 10,
        'productos_preferidos': ['RCP-X018-750', 'RCP-S015-750', 'RCP-EDLIM-750']
    },
    'Corporativo': {
        'peso':0.05,
        'ticket_min': 2000,
        'ticket_max': 8000,
        'frecuencia_dias_promedio': 90,
        'descuento_max': 12,
        'productos_preferidos': ['RECP-GIFT-A8', 'RCP-EDLIM-750']
    }
}

#==================================================================================
# GEOGRAFÍA - CUIDADES DE PANAMÁ
#==================================================================================

CIUDADES = {
    'Ciudad de Panamá': {
        'peso': 0.55,                               # 55% de cleintes aquí
        'poder_adquisitivo': 1.2                    # Pueden pagar 20%más
    },
    'David': {
        'peso': 0.12,
        'poder_adquisitivo': 0.95
    },
    'Colón': {
        'peso': 0.08,
        'poder_adquisitivo': 0.85
    },
    'Santiago': {
        'peso': 0.05,
        'poder_adquisitivo': 0.90
    },
    'Coronado': {
        'peso': 0.04,
        'poder_adquisitivo': 1.15
    },
    'Boquete': {
        'peso': 0.04,
        'poder_adquisitivo': 1.0
    },
    'Chitré': {
        'peso': 0.05,
        'poder_adquisitivo': 0.85
    },
    'Penonomé': {
        'peso': 0.03,
        'poder_adquisitivo': 0.80
    },
    'Bocas del Toro': {
        'peso': 0.02,
        'poder_adquisitivo': 0.90
    }
}

#===========================================================
#MÉTODOS DE PAGO
#===========================================================

METODOS_PAGO = {
    'Tarjeta Crédito': 0.45,                # 45% usan tarjeta
    'Transferencia': 0.30,                  # 30% transferencia
    'Efectivo': 0.15,                       # 15% efectivo
    'Crédito 30 días': 0.10                 # 10% crédito (soloB2B)
}
#======================================================================
# VENDEDORES
#======================================================================

VENDEDORES = [
    {'id': 'VEN-001', 'nombre': 'Carlos Mendoza', 'zona': 'Ciudad de Panamá'},
    {'id': 'VEN-002', 'nombre': 'María Gonzáles', 'zona': 'Ciudad de Panamá'},
    {'id': 'VEN-003', 'nombre': 'Roberto Chen', 'zona': 'Colón'},
    {'id': 'VEN-004', 'nombre': 'Ana Pérez', 'zona': 'David'},
    {'id': 'VEN-005', 'nombre': 'Luuis Castillo', 'zona': 'Santiago'},
    {'id': 'VEN-006', 'nombre': 'Ecommerce Bot', 'zona': 'Online'},
]

#==========================================================================
# CONFIGURACIÓN DE ANOMALÍAS
#===========================================================================

PROBABILIDAD_DEVOLUCION = 0.02                # 2% de transacciones tiene devolución 
PROBABILIDAD_DESCUENTO_EXTRA = 0.15             # 15% tienen descuento adicional
DIAS_ENTREGA_MIN = 1 
DIAS_ENTREGA_MAX = 5

print("✅ Configuración cargada correctamente")