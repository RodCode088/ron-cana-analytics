from pathlib import Path

import pandas as pd

from analysis.metrics import compute_dynamic_insights, compute_kpis, validate_sales_data


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"


def load_data():
    return (
        pd.read_csv(OUTPUTS / "ventas_transacciones.csv"),
        pd.read_csv(OUTPUTS / "dim_productos.csv"),
        pd.read_csv(OUTPUTS / "dim_clientes.csv"),
        pd.read_csv(OUTPUTS / "eventos_comerciales.csv"),
    )


def test_dataset_contract_is_valid():
    sales, products, clients, events = load_data()
    report = validate_sales_data(sales, products, clients, events)

    assert report.valid, report.to_dict()
    assert report.row_count == 4_234


def test_canonical_kpis_match_current_data_product():
    sales, *_ = load_data()
    kpis = compute_kpis(sales)

    assert kpis["revenue"] == 7_020_235.54
    assert kpis["gross_profit"] == 3_805_656.04
    assert kpis["weighted_margin_pct"] == 54.21
    assert kpis["transactions"] == 4_234


def test_dynamic_insights_do_not_claim_roi_or_causality():
    sales, *_ = load_data()
    text = " ".join(item["finding"] for item in compute_dynamic_insights(sales)).lower()

    assert "no roi" in text
    assert "no causalidad" in text
