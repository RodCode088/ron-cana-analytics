# Ron Caña Analytics Lab

Una clase interactiva de analytics engineering construida sobre datos sintéticos de una marca ficticia de ron premium. La interfaz reproduce la lógica visual de un reporte de Power BI y permite recorrer el dato desde el KPI hasta el modelo, el registro y el código que lo calcula.

## Qué se puede hacer

- Explorar KPIs, tendencias, canales, productos, clientes y un mapa de Panamá.
- Filtrar todo el reporte desde visuales, mapa o panel lateral.
- Navegar un modelo estrella con `fact_ventas`, `dim_productos`, `dim_clientes` y `dim_eventos`.
- Inspeccionar registros, buscar y cambiar de tabla.
- Leer fragmentos reales del pipeline Python y de la Function que integra Gemini.
- Seguir una clase guiada de ocho lecciones.
- Preguntar al tutor AI; puede explicar, resaltar y mover la interfaz con acciones validadas.
- Generar entre 500 y 20.000 transacciones reproducibles mediante una semilla.
- Importar un CSV sintético compatible sin enviar sus filas al servidor ni a Gemini.
- Continuar usando el recorrido local si Gemini no está configurado o no responde.

## Arquitectura

```text
CSV sintéticos ──> validación Python ──> data product JSON
                                              │
                                              v
                                  Vite + Chart.js + Leaflet
                                   │       │        │
                                   │       │        └─ mapa OpenStreetMap
                                   │       └─ visuales y filtros cruzados
                                   └─ modelo, datos, código y laboratorio
                                              │
                                contexto agregado y sin filas
                                              v
                              Cloudflare Pages Function /api/tutor
                                              │
                              acciones cerradas y validadas
                                              v
                                   Gemini 3.7 Flash (opcional)
```

El navegador conserva los datasets importados o generados. El tutor recibe únicamente un contexto agregado: KPIs, filtros, rankings compactos, vista activa y lección actual. Las acciones generadas por el modelo pasan por una lista permitida tanto en el servidor como en el cliente; el modelo no ejecuta JavaScript ni modifica datos arbitrariamente.

## Ejecutar el proyecto

Requisitos: Python 3.11 o posterior y Node.js 20 o posterior.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
python scripts/build_dashboard_data.py

Set-Location web
npm install
npm run dev
```

La aplicación se abre normalmente en `http://localhost:5173`. En desarrollo Vite no ejecuta Pages Functions, por lo que el tutor usa automáticamente el recorrido determinístico local.

Para probar la aplicación completa con la Function local:

```powershell
Set-Location web
npm run build
Set-Location ..
npx wrangler pages dev web/dist
```

Guarda la clave solo en `.dev.vars` para desarrollo local:

```dotenv
GEMINI_API_KEY=tu_clave_de_google_ai_studio
```

No confirmes ni subas ese archivo al repositorio.

## Contrato para importar CSV

La plantilla está en `web/public/data/plantilla_ventas.csv`. Las columnas mínimas son:

```text
fecha,ciudad,canal_venta,tipo_cliente,nombre_producto,cantidad,ingreso_total,utilidad_bruta
```

También se aceptan opcionalmente `segmento_cliente`, `cliente_id`, `producto_id`, `categoria_producto`, `descuento_porcentaje`, `devolucion`, `evento_id` y `campana`.

El importador descarta filas con fecha o métricas inválidas y nunca sobrescribe los CSV originales. Si una ciudad importada no pertenece al catálogo geográfico de la demo, participa en KPIs y gráficos, pero no aparece como burbuja en el mapa.

## Calidad y pruebas

```powershell
python -m pytest -q

Set-Location web
npm test
npm run build

Set-Location ..\functions
npm test
```

Las pruebas cubren reglas del generador, integridad referencial, métricas, filtros, laboratorio CSV, generación reproducible, contrato privado del tutor y validación de acciones AI. El workflow de GitHub Actions repite generación, pruebas y build en cada cambio.

## Desplegar en Cloudflare Pages

1. Crea una clave en Google AI Studio. No la pongas en código ni en variables `VITE_*`.
2. Autentica Wrangler con tu cuenta de Cloudflare.
3. Construye el data product y la web.
4. Crea el proyecto de Pages y configura `GEMINI_API_KEY` como secreto de producción.
5. Despliega `web/dist`; la carpeta `functions/` se publica como Pages Functions.

```powershell
python scripts/build_dashboard_data.py
Set-Location web
npm ci
npm run build
Set-Location ..

npx wrangler pages project create ron-cana-intelligence
npx wrangler pages secret put GEMINI_API_KEY --project-name ron-cana-intelligence
npx wrangler pages deploy web/dist --project-name ron-cana-intelligence
```

Como control opcional de abuso, crea un namespace KV y enlázalo a la Function con el nombre `TUTOR_LIMIT`. El límite incluido es orientativo y no sustituye un rate limiter atómico para producción.

## Nota sobre Gemini gratuito

La demo funciona sin Gemini gracias al tutor guiado local. Al activar el nivel gratuito, Google puede usar el contenido procesado para mejorar sus productos; por eso esta implementación envía solo agregados y debe utilizarse con datos sintéticos o no sensibles. Los límites dependen del proyecto y del modelo y deben revisarse en Google AI Studio antes de una demostración pública.

## Estructura principal

```text
analysis/metrics.py                 contrato, calidad, KPIs e insights
data_generation/                   dimensiones y generador transaccional
scripts/build_dashboard_data.py    construcción del data product web
web/                               interfaz Vite estilo Power BI
functions/api/tutor.js             tutor Gemini para Cloudflare Pages
tests/                              pruebas Python
Dashboard_Ron_cana.pblx.pbix       reporte original de referencia
wrangler.jsonc                      configuración de Cloudflare Pages
```
