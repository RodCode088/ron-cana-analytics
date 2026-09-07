"""Validate the CSV model and export the browser data product used by the class."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.metrics import compute_kpis, validate_sales_data


OUTPUT_PATH = ROOT / "web" / "public" / "data" / "dashboard.json"

CITY_COORDINATES = {
    "Ciudad de Panamá": {"lat": 8.9936, "lon": -79.5197},
    "David": {"lat": 8.4334, "lon": -82.4274},
    "Colón": {"lat": 9.3592, "lon": -79.9009},
    "Santiago": {"lat": 8.1036, "lon": -80.9833},
    "Coronado": {"lat": 8.6167, "lon": -79.9833},
    "Boquete": {"lat": 8.7789, "lon": -82.4328},
    "Chitré": {"lat": 7.9622, "lon": -80.4297},
    "Penonomé": {"lat": 8.5167, "lon": -80.3500},
    "Bocas del Toro": {"lat": 9.3404, "lon": -82.2410},
}

CODE_EXAMPLES = {
    "metrics": {
        "label": "KPIs y contrato de datos",
        "language": "python",
        "path": "analysis/metrics.py",
        "ranges": [(44, 118), (121, 175)],
        "lesson": "Una métrica debe tener una sola definición reutilizable y comprobable.",
    },
    "generator": {
        "label": "Generador sintético",
        "language": "python",
        "path": "data_generation/generador_ventas.py",
        "ranges": [(15, 33), (198, 225), (355, 415)],
        "lesson": "Las semillas y reglas explícitas hacen que una simulación sea repetible.",
    },
    "data_product": {
        "label": "Build del data product",
        "language": "python",
        "path": "scripts/build_dashboard_data.py",
        "ranges": [(1, 45), (110, 205)],
        "lesson": "El build valida antes de publicar y entrega al navegador solo lo necesario.",
    },
    "tutor_api": {
        "label": "Tutor Gemini seguro",
        "language": "javascript",
        "path": "functions/api/tutor.js",
        "ranges": [(1, 65), (115, 180), (230, 325)],
        "lesson": "El modelo propone acciones, pero la aplicación valida cada una antes de ejecutarla.",
    },
}


def records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    """Convert a frame to JSON-native values with null instead of NaN."""

    return json.loads(frame.to_json(orient="records", date_format="iso", force_ascii=False))


def column_type(series: pd.Series) -> str:
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    if pd.api.types.is_integer_dtype(series):
        return "integer"
    if pd.api.types.is_numeric_dtype(series):
        return "decimal"
    if "fecha" in series.name:
        return "date"
    return "text"


def table_metadata(
    table_id: str,
    label: str,
    frame: pd.DataFrame,
    primary_key: str,
    foreign_keys: dict[str, str] | None = None,
    source: str = "embedded",
) -> dict[str, Any]:
    foreign_keys = foreign_keys or {}
    columns = []
    for name in frame.columns:
        role = "attribute"
        if name == primary_key:
            role = "primary_key"
        elif name in foreign_keys:
            role = "foreign_key"
        elif pd.api.types.is_numeric_dtype(frame[name]) and name not in {"año", "mes", "dia", "semana_año"}:
            role = "measure"
        columns.append(
            {
                "name": name,
                "type": column_type(frame[name]),
                "role": role,
                "references": foreign_keys.get(name),
            }
        )
    return {
        "id": table_id,
        "label": label,
        "row_count": int(len(frame)),
        "primary_key": primary_key,
        "source": source,
        "columns": columns,
        "sample": records(frame.head(8)),
    }


def code_payload() -> dict[str, dict[str, str]]:
    payload = {}
    for key, config in CODE_EXAMPLES.items():
        source_path = ROOT / config["path"]
        lines = source_path.read_text(encoding="utf-8").splitlines()
        chunks = []
        for index, (start, end) in enumerate(config["ranges"]):
            if index:
                chunks.append("\n# ... fragmento intermedio omitido ...\n" if config["language"] == "python" else "\n// ... fragmento intermedio omitido ...\n")
            chunks.extend(f"{line_number:>4}  {lines[line_number - 1]}" for line_number in range(start, min(end, len(lines)) + 1))
        payload[key] = {
            "label": config["label"],
            "language": config["language"],
            "path": config["path"],
            "lesson": config["lesson"],
            "content": "\n".join(chunks),
        }
    return payload


def build_payload() -> dict[str, Any]:
    outputs = ROOT / "outputs"
    sales = pd.read_csv(outputs / "ventas_transacciones.csv")
    products = pd.read_csv(outputs / "dim_productos.csv")
    clients = pd.read_csv(outputs / "dim_clientes.csv")
    events = pd.read_csv(outputs / "eventos_comerciales.csv")

    report = validate_sales_data(sales, products, clients, events)
    if not report.valid:
        raise ValueError(f"El contrato de datos falló: {report.to_dict()}")

    source_hash = hashlib.sha256(
        (outputs / "ventas_transacciones.csv").read_bytes()
    ).hexdigest()[:12]

    rows = []
    for row in sales.itertuples(index=False):
        rows.append(
            {
                "id": row.transaccion_id,
                "d": row.fecha,
                "m": int(row.mes),
                "c": row.ciudad,
                "ch": row.canal_venta,
                "ct": row.tipo_cliente,
                "seg": row.segmento_cliente,
                "cid": row.cliente_id,
                "p": row.nombre_producto,
                "pid": row.producto_id,
                "cat": row.categoria_producto,
                "r": round(float(row.ingreso_total), 2),
                "g": round(float(row.utilidad_bruta), 2),
                "u": int(row.cantidad),
                "disc": round(float(row.descuento_porcentaje), 2),
                "ret": bool(row.devolucion),
                "eid": None if pd.isna(row.evento_id) else row.evento_id,
                "cp": None if pd.isna(row.campana) else row.campana,
            }
        )

    tables = [
        table_metadata(
            "fact_ventas",
            "Fact Ventas",
            sales,
            "transaccion_id",
            {
                "producto_id": "dim_productos.producto_id",
                "cliente_id": "dim_clientes.cliente_id",
                "evento_id": "dim_eventos.evento_id",
            },
            source="rows",
        ),
        table_metadata("dim_productos", "Dim Productos", products, "producto_id"),
        table_metadata("dim_clientes", "Dim Clientes", clients, "cliente_id"),
        table_metadata("dim_eventos", "Dim Eventos", events, "evento_id"),
    ]

    return {
        "meta": {
            "dataset": "Ron Caña Panamá — ventas sintéticas 2024",
            "data_through": str(pd.to_datetime(sales["fecha"]).max().date()),
            "source_hash": source_hash,
            "synthetic": True,
            "quality": report.to_dict(),
            "baseline": compute_kpis(sales),
            "privacy": "Los archivos importados por el usuario permanecen en su navegador.",
        },
        "dimensions": {
            "months": sorted(int(value) for value in sales["mes"].unique()),
            "channels": sorted(sales["canal_venta"].unique().tolist()),
            "cities": sorted(sales["ciudad"].unique().tolist()),
            "client_types": sorted(sales["tipo_cliente"].unique().tolist()),
            "coordinates": CITY_COORDINATES,
        },
        "relational": {
            "tables": tables,
            "relations": [
                {"from": "dim_productos", "from_key": "producto_id", "to": "fact_ventas", "to_key": "producto_id", "cardinality": "1:*"},
                {"from": "dim_clientes", "from_key": "cliente_id", "to": "fact_ventas", "to_key": "cliente_id", "cardinality": "1:*"},
                {"from": "dim_eventos", "from_key": "evento_id", "to": "fact_ventas", "to_key": "evento_id", "cardinality": "1:*"},
            ],
            "data": {
                "dim_productos": records(products),
                "dim_clientes": records(clients),
                "dim_eventos": records(events),
            },
        },
        "code": code_payload(),
        "rows": rows,
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(
        f"Data product: {len(payload['rows']):,} rows, "
        f"{len(payload['relational']['tables'])} tables, "
        f"hash {payload['meta']['source_hash']} -> {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()
