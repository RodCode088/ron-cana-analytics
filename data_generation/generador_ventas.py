# generador_ventas.py
# Generador inteligente de transacciones de Ron Caña Panamá

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from config import *

class GeneradorVentasRonCana:
    """
    Generador inteligente de transacciones con lógica de negocio realista
    """
    
    def __init__(self):
        print("🔄 Inicializando generador...")
        
        # Cargar dimensiones
        self.productos = pd.read_csv('outputs/dim_productos.csv')
        self.clientes = pd.read_csv('outputs/dim_clientes.csv')
        self.eventos = pd.read_csv('outputs/eventos_comerciales.csv')
        
        # Convertir fechas de eventos
        self.eventos['fecha_inicio'] = pd.to_datetime(self.eventos['fecha_inicio'])
        self.eventos['fecha_fin'] = pd.to_datetime(self.eventos['fecha_fin'])
        
        # Crear índice de eventos por fecha para búsqueda rápida
        self.eventos_por_fecha = {}
        for _, evento in self.eventos.iterrows():
            fecha_actual = evento['fecha_inicio']
            while fecha_actual <= evento['fecha_fin']:
                fecha_str = fecha_actual.strftime('%Y-%m-%d')
                if fecha_str not in self.eventos_por_fecha:
                    self.eventos_por_fecha[fecha_str] = []
                self.eventos_por_fecha[fecha_str].append(evento)
                fecha_actual += timedelta(days=1)
        
        print(f"✅ Cargados: {len(self.productos)} productos, {len(self.clientes)} clientes, {len(self.eventos)} eventos")
    
    
    def obtener_eventos_activos(self, fecha):
        """
        Obtiene los eventos activos en una fecha específica
        """
        fecha_str = fecha.strftime('%Y-%m-%d')
        return self.eventos_por_fecha.get(fecha_str, [])
    
    
    def calcular_probabilidad_venta_dia(self, fecha):
        """
        Calcula la probabilidad base de que ocurra una venta en este día
        Considera: estacionalidad mensual, día de semana, eventos
        """
        # Factor estacionalidad del mes
        factor_mes = ESTACIONALIDAD_MES[fecha.month]
        
        # Factor día de la semana (0=Lunes, 6=Domingo)
        factor_dia_semana = MULTIPLICADOR_DIA_SEMANA[fecha.weekday()]
        
        # Factor quincena (días de pago son más fuertes)
        dia = fecha.day
        if dia <= 7:
            factor_quincena = 0.85  # Inicio de mes, bajo
        elif dia <= 15:
            factor_quincena = 1.15  # Primera quincena, ALTA
        elif dia <= 23:
            factor_quincena = 0.90  # Media del mes
        else:
            factor_quincena = 1.10  # Fin de mes (pago quincenal)
        
        # Factor eventos (si hay evento activo, sube la probabilidad)
        eventos_hoy = self.obtener_eventos_activos(fecha)
        if eventos_hoy:
            # Usar el evento con mayor impacto
            factor_evento = max([e['impacto_ventas'] for e in eventos_hoy])
        else:
            factor_evento = 1.0
        
        # Probabilidad total = multiplicar todos los factores
        probabilidad = factor_mes * factor_dia_semana * factor_quincena * factor_evento
        
        return probabilidad
    
    
    def seleccionar_canal(self):
        """
        Selecciona un canal de venta según los pesos definidos en config
        """
        canales = list(CANALES.keys())
        pesos = [CANALES[c]['peso'] for c in canales]
        
        return random.choices(canales, weights=pesos, k=1)[0]
    
    
    def seleccionar_cliente_por_canal(self, canal):
        """
        Selecciona un cliente apropiado para el canal
        No todos los clientes pueden comprar por todos los canales
        """
        if canal == 'Horeca Premium':
            segmentos_validos = ['Hotel 5 Estrellas', 'Hotel 4 Estrellas', 'Restaurante Gourmet', 'Bar Top']
        elif canal == 'Retail Moderno':
            segmentos_validos = ['Licorería Especializada', 'Tienda Conveniencia']
        elif canal == 'Supermercados':
            segmentos_validos = ['Supermercado']
        elif canal == 'Ecommerce':
            segmentos_validos = ['Consumidor Final', 'Restaurante Gourmet', 'Bar Top']
        elif canal == 'Duty Free':
            segmentos_validos = ['Consumidor Final']  # Turistas
        elif canal == 'Corporativo':
            segmentos_validos = ['Corporativo']
        else:
            segmentos_validos = self.clientes['segmento'].unique().tolist()
        
        # Filtrar clientes del segmento válido
        clientes_validos = self.clientes[self.clientes['segmento'].isin(segmentos_validos)]
        
        if len(clientes_validos) == 0:
            # Fallback: cualquier cliente
            return self.clientes.sample(1).iloc[0]
        
        return clientes_validos.sample(1).iloc[0]
    
    
    def seleccionar_producto_por_canal(self, canal, eventos_activos):
        """
        Selecciona un producto apropiado para el canal
        Considera productos preferidos del canal y productos en campaña
        """
        productos_preferidos = CANALES[canal]['productos_preferidos']
        
        # Si hay evento activo con productos foco, priorizar esos
        if eventos_activos:
            productos_evento = []
            for evento in eventos_activos:
                productos_foco = evento['productos_foco'].split(',')
                productos_evento.extend(productos_foco)
            
            # 70% probabilidad de elegir producto del evento
            if random.random() < 0.7 and productos_evento:
                productos_disponibles = self.productos[
                    self.productos['producto_id'].isin(productos_evento)
                ]
                if len(productos_disponibles) > 0:
                    return productos_disponibles.sample(1).iloc[0]
        
        # Si no hay evento o no se seleccionó producto de evento,
        # usar productos preferidos del canal
        productos_canal = self.productos[
            self.productos['producto_id'].isin(productos_preferidos)
        ]
        
        if len(productos_canal) > 0:
            # 80% de las veces, usar producto preferido
            if random.random() < 0.8:
                return productos_canal.sample(1).iloc[0]
        
        # 20% de las veces, cualquier producto
        return self.productos.sample(1).iloc[0]
    
    
    def calcular_cantidad(self, producto, cliente, canal):
        """
        Calcula la cantidad a comprar según tipo de cliente y canal
        B2B compra más que B2C
        """
        if cliente['tipo_cliente'] == 'B2C':
            # Consumidor final: 1-3 botellas
            return random.randint(1, 3)
        
        # B2B: depende del segmento
        if cliente['segmento'] == 'Supermercado':
            return random.randint(24, 120)  # Cajas de 12
        elif cliente['segmento'] == 'Distribuidor Mayorista':
            return random.randint(100, 300)
        elif cliente['segmento'] in ['Hotel 5 Estrellas', 'Hotel 4 Estrellas']:
            return random.randint(6, 36)
        elif cliente['segmento'] in ['Restaurante Gourmet', 'Bar Top']:
            return random.randint(3, 24)
        elif cliente['segmento'] == 'Licorería Especializada':
            return random.randint(12, 48)
        elif cliente['segmento'] == 'Corporativo':
            return random.randint(20, 80)  # Pedidos grandes estacionales
        else:
            return random.randint(6, 24)
    
    
    def calcular_descuento(self, canal, eventos_activos, cantidad):
        """
        Calcula el descuento aplicable
        Considera: evento activo, canal, volumen
        """
        descuento_base = 0
        
        # Descuento por evento
        if eventos_activos:
            descuento_evento = max([e['descuento_adicional'] for e in eventos_activos])
            descuento_base += descuento_evento
        
        # Descuento aleatorio dentro del máximo del canal
        descuento_max_canal = CANALES[canal]['descuento_max']
        
        # 15% de probabilidad de descuento adicional
        if random.random() < PROBABILIDAD_DESCUENTO_EXTRA:
            descuento_base += random.uniform(0, descuento_max_canal)
        
        # Descuento por volumen (si compra mucho)
        if cantidad >= 50:
            descuento_base += 5
        elif cantidad >= 100:
            descuento_base += 10
        
        # Limitar descuento máximo a 30%
        return min(descuento_base, 30)
    
    
    def asignar_vendedor(self, cliente):
        """
        Asigna un vendedor según la zona del cliente
        """
        ciudad = cliente['ciudad']
        
        # Buscar vendedor de la zona
        vendedores_zona = [v for v in VENDEDORES if v['zona'] == ciudad]
        
        if vendedores_zona:
            return random.choice(vendedores_zona)
        
        # Si no hay vendedor de la zona, buscar por región amplia
        if 'Panamá' in ciudad:
            vendedores_zona = [v for v in VENDEDORES if 'Panamá' in v['zona']]
        
        if vendedores_zona:
            return random.choice(vendedores_zona)
        
        # Fallback: cualquier vendedor físico
        return random.choice([v for v in VENDEDORES if v['nombre'] != 'Ecommerce Bot'])
    
    
    def seleccionar_metodo_pago(self, cliente):
        """
        Selecciona método de pago según tipo de cliente
        """
        if cliente['tipo_cliente'] == 'B2B':
            # B2B usa más crédito y transferencia
            metodos = ['Transferencia', 'Crédito 30 días', 'Tarjeta Crédito']
            pesos = [0.50, 0.30, 0.20]
        else:
            # B2C usa más tarjeta y efectivo
            metodos = ['Tarjeta Crédito', 'Efectivo', 'Transferencia']
            pesos = [0.60, 0.25, 0.15]
        
        return random.choices(metodos, weights=pesos, k=1)[0]
    
    
    def generar_transaccion(self, fecha, transaccion_num):
        """
        Genera UNA transacción completa con toda su lógica
        """
        # 1. Seleccionar canal
        canal = self.seleccionar_canal()
        
        # 2. Seleccionar cliente apropiado
        cliente = self.seleccionar_cliente_por_canal(canal)
        
        # 3. Verificar eventos activos
        eventos_activos = self.obtener_eventos_activos(fecha)
        
        # 4. Seleccionar producto
        producto = self.seleccionar_producto_por_canal(canal, eventos_activos)
        
        # 5. Calcular cantidad
        cantidad = self.calcular_cantidad(producto, cliente, canal)
        
        # 6. Calcular descuento
        descuento_porcentaje = self.calcular_descuento(canal, eventos_activos, cantidad)
        
        # 7. Calcular precio unitario (con descuento aplicado)
        precio_lista = producto['precio_lista']
        precio_unitario = precio_lista * (1 - descuento_porcentaje / 100)
        
        # 8. Asignar vendedor
        vendedor = self.asignar_vendedor(cliente)
        
        # 9. Método de pago
        metodo_pago = self.seleccionar_metodo_pago(cliente)
        
        # 10. Calcular métricas financieras
        costo_unitario = producto['costo_unitario']
        costo_total = costo_unitario * cantidad
        ingreso_total = precio_unitario * cantidad
        utilidad_bruta = ingreso_total - costo_total
        margen_porcentaje = (utilidad_bruta / ingreso_total * 100) if ingreso_total > 0 else 0
        
        # 11. Simular anomalías
        es_devolucion = random.random() < PROBABILIDAD_DEVOLUCION
        dias_entrega = random.randint(DIAS_ENTREGA_MIN, DIAS_ENTREGA_MAX)
        
        # 12. Evento asociado (si aplica)
        evento_id = eventos_activos[0]['evento_id'] if eventos_activos else None
        campana = eventos_activos[0]['nombre'] if eventos_activos else None
        
        # 13. Construir la transacción
        transaccion = {
            'transaccion_id': f'TRX-2024-{transaccion_num:05d}',
            'fecha': fecha.strftime('%Y-%m-%d'),
            'año': fecha.year,
            'mes': fecha.month,
            'dia': fecha.day,
            'dia_semana': fecha.strftime('%A'),
            'semana_año': fecha.isocalendar()[1],
            
            # Cliente
            'cliente_id': cliente['cliente_id'],
            'nombre_cliente': cliente['nombre_cliente'],
            'tipo_cliente': cliente['tipo_cliente'],
            'segmento_cliente': cliente['segmento'],
            'ciudad': cliente['ciudad'],
            
            # Producto
            'producto_id': producto['producto_id'],
            'nombre_producto': producto['nombre_producto'],
            'categoria_producto': producto['categoria'],
            'subcategoria_producto': producto['subcategoria'],
            
            # Transacción
            'canal_venta': canal,
            'cantidad': cantidad,
            'precio_lista': round(precio_lista, 2),
            'descuento_porcentaje': round(descuento_porcentaje, 2),
            'precio_unitario': round(precio_unitario, 2),
            'costo_unitario': round(costo_unitario, 2),
            
            # Financiero
            'costo_total': round(costo_total, 2),
            'ingreso_total': round(ingreso_total, 2),
            'utilidad_bruta': round(utilidad_bruta, 2),
            'margen_porcentaje': round(margen_porcentaje, 2),
            
            # Operacional
            'vendedor_id': vendedor['id'],
            'vendedor_nombre': vendedor['nombre'],
            'metodo_pago': metodo_pago,
            'dias_entrega': dias_entrega,
            'devolucion': es_devolucion,
            
            # Campaña
            'evento_id': evento_id,
            'campana': campana
        }
        
        return transaccion
    
    
    def generar_dataset_completo(self):
        """
        Genera el dataset completo de transacciones
        Distribuye transacciones a lo largo del año con probabilidades realistas
        """
        print("\n🚀 Generando transacciones...")
        
        transacciones = []
        fecha_actual = FECHA_INICIO
        transaccion_num = 1
        
        # Crear barra de progreso simple
        total_dias = (FECHA_FIN - FECHA_INICIO).days + 1
        
        while fecha_actual <= FECHA_FIN:
            # Calcular probabilidad de venta para este día
            prob_dia = self.calcular_probabilidad_venta_dia(fecha_actual)
            
            # Número base de transacciones por día
            transacciones_base_dia = NUM_TRANSACCIONES_OBJETIVO / 365
            
            # Número de transacciones para este día (ajustado por probabilidad)
            num_transacciones_dia = int(transacciones_base_dia * prob_dia)
            
            # Agregar variabilidad aleatoria (+/- 30%)
            variacion = random.uniform(0.7, 1.3)
            num_transacciones_dia = int(num_transacciones_dia * variacion)
            
            # Generar las transacciones del día
            for _ in range(num_transacciones_dia):
                trx = self.generar_transaccion(fecha_actual, transaccion_num)
                transacciones.append(trx)
                transaccion_num += 1
            
            # Progreso
            if fecha_actual.day == 1:  # Mostrar al inicio de cada mes
                print(f"  ✓ {fecha_actual.strftime('%B %Y')}: {num_transacciones_dia} transacciones generadas")
            
            fecha_actual += timedelta(days=1)
        
        print(f"\n✅ Total generado: {len(transacciones)} transacciones")
        
        return pd.DataFrame(transacciones)
    
    
    def guardar_dataset(self):
        """
        Genera y guarda el dataset completo
        """
        df_ventas = self.generar_dataset_completo()
        
        # Guardar
        ruta_salida = 'outputs/ventas_transacciones.csv'
        df_ventas.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
        
        # Estadísticas
        print("\n" + "="*60)
        print("✅ DATASET DE VENTAS GENERADO")
        print("="*60)
        print(f"📁 Archivo guardado en: {ruta_salida}")
        print(f"📊 Total transacciones: {len(df_ventas):,}")
        print(f"💰 Ingreso total: ${df_ventas['ingreso_total'].sum():,.2f}")
        print(f"💵 Utilidad total: ${df_ventas['utilidad_bruta'].sum():,.2f}")
        print(f"📈 Margen promedio: {df_ventas['margen_porcentaje'].mean():.1f}%")
        print(f"🛒 Ticket promedio: ${df_ventas['ingreso_total'].mean():.2f}")
        print()
        print("📊 TRANSACCIONES POR MES:")
        ventas_mes = df_ventas.groupby('mes').size()
        for mes, cantidad in ventas_mes.items():
            nombre_mes = datetime(2024, mes, 1).strftime('%B')
            print(f"  {nombre_mes:12s}: {cantidad:4d} transacciones")
        print()
        print("🏪 VENTAS POR CANAL:")
        print(df_ventas.groupby('canal_venta')['ingreso_total'].sum().sort_values(ascending=False).apply(lambda x: f"${x:,.2f}"))
        print("="*60)
        
        return df_ventas


# Ejecutar
if __name__ == '__main__':
    generador = GeneradorVentasRonCana()
    df_ventas = generador.guardar_dataset()