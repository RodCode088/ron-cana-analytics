"""Data contracts and reusable business metrics.

The dashboard, export pipeline, and tests all depend on this module so that a
metric has one definition everywhere it is displayed.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

import pandas as pd


REQUIRED_SALES_COLUMNS = {
    "transaccion_id",
    "fecha",
    "mes",
    "cliente_id",
    "tipo_cliente",
    "ciudad",
    "producto_id",
    "nombre_producto",
    "canal_venta",
    "cantidad",
    "ingreso_total",
    "utilidad_bruta",
    "evento_id",
    "campana",
}


@dataclass(frozen=True)
class DataQualityReport:
    valid: bool
    row_count: int
    checks: dict[str, bool]
    details: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_sales_data(
    sales: pd.DataFrame,
    products: pd.DataFrame | None = None,
    clients: pd.DataFrame | None = None,
    events: pd.DataFrame | None = None,
) -> DataQualityReport:
    """Validate the transaction fact table and optional dimensions."""

    missing_columns = sorted(REQUIRED_SALES_COLUMNS - set(sales.columns))
    checks: dict[str, bool] = {
        "required_columns": not missing_columns,
        "non_empty": not sales.empty,
    }
    details: dict[str, Any] = {"missing_columns": missing_columns}

    if missing_columns:
        return DataQualityReport(False, len(sales), checks, details)

    checks.update(
        {
            "unique_transaction_ids": not sales["transaccion_id"].duplicated().any(),
            "positive_quantities": bool((sales["cantidad"] > 0).all()),
            "non_negative_revenue": bool((sales["ingreso_total"] >= 0).all()),
            "non_negative_profit": bool((sales["utilidad_bruta"] >= 0).all()),
            "valid_months": bool(sales["mes"].between(1, 12).all()),
        }
    )

    if products is not None:
        orphan_products = int((~sales["producto_id"].isin(products["producto_id"])).sum())
        checks["product_references"] = orphan_products == 0
        details["orphan_products"] = orphan_products
    if clients is not None:
        orphan_clients = int((~sales["cliente_id"].isin(clients["cliente_id"])).sum())
        checks["client_references"] = orphan_clients == 0
        details["orphan_clients"] = orphan_clients
    if events is not None:
        orphan_events = int(
            (sales["evento_id"].notna() & ~sales["evento_id"].isin(events["evento_id"])).sum()
        )
        checks["event_references"] = orphan_events == 0
        details["orphan_events"] = orphan_events

    details["nulls"] = {
        column: int(count)
        for column, count in sales.isna().sum().items()
        if count and column not in {"evento_id", "campana"}
    }
    checks["no_unexpected_nulls"] = not details["nulls"]
    return DataQualityReport(all(checks.values()), len(sales), checks, details)


def compute_kpis(sales: pd.DataFrame) -> dict[str, float | int]:
    """Return KPI definitions shared by every interface."""

    if sales.empty:
        return {
            "revenue": 0.0,
            "gross_profit": 0.0,
            "weighted_margin_pct": 0.0,
            "transactions": 0,
            "units": 0,
            "average_ticket": 0.0,
        }

    revenue = float(sales["ingreso_total"].sum())
    profit = float(sales["utilidad_bruta"].sum())
    return {
        "revenue": round(revenue, 2),
        "gross_profit": round(profit, 2),
        "weighted_margin_pct": round((profit / revenue * 100) if revenue else 0, 2),
        "transactions": int(len(sales)),
        "units": int(sales["cantidad"].sum()),
        "average_ticket": round(float(sales["ingreso_total"].mean()), 2),
    }


def compute_dynamic_insights(sales: pd.DataFrame) -> list[dict[str, str]]:
    """Build descriptive insights for the currently selected slice.

    These statements deliberately avoid causal and ROI claims. The source data
    is synthetic and does not include campaign cost or an experimental control.
    """

    if sales.empty:
        return [{"title": "Sin datos", "finding": "Amplía los filtros para analizar resultados."}]

    kpis = compute_kpis(sales)
    revenue = float(kpis["revenue"])
    month_revenue = sales.groupby("mes")["ingreso_total"].sum().sort_values(ascending=False)
    product_revenue = sales.groupby("nombre_producto")["ingreso_total"].sum().sort_values(ascending=False)
    channel = sales.groupby("canal_venta").agg(
        revenue=("ingreso_total", "sum"), profit=("utilidad_bruta", "sum")
    )
    channel["margin"] = channel["profit"].div(channel["revenue"]).mul(100)

    top_month = int(month_revenue.index[0])
    top_product = str(product_revenue.index[0])
    top_channel = str(channel["margin"].idxmax())
    campaign_sales = sales[sales["campana"].notna()]
    non_campaign_sales = sales[sales["campana"].isna()]

    insights = [
        {
            "title": "Concentración temporal",
            "finding": f"El mes {top_month} aporta {month_revenue.iloc[0] / revenue * 100:.1f}% del ingreso seleccionado.",
        },
        {
            "title": "Producto líder",
            "finding": f"{top_product} concentra {product_revenue.iloc[0] / revenue * 100:.1f}% del ingreso.",
        },
        {
            "title": "Margen por canal",
            "finding": f"{top_channel} registra el mayor margen ponderado ({channel.loc[top_channel, 'margin']:.1f}%).",
        },
    ]

    if not campaign_sales.empty and not non_campaign_sales.empty:
        uplift = (
            campaign_sales["ingreso_total"].mean() / non_campaign_sales["ingreso_total"].mean() - 1
        ) * 100
        insights.append(
            {
                "title": "Asociación con campañas",
                "finding": f"El ticket observado durante campañas es {uplift:+.1f}% frente a periodos sin campaña; es asociación, no ROI y no causalidad.",
            }
        )
    return insights
