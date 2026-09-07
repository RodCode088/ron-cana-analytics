from unittest.mock import patch

import pandas as pd

from data_generation.dim_clientes import crear_base_clientes
from data_generation.generador_ventas import GeneradorVentasRonCana


def test_client_dimension_is_reproducible():
    first = crear_base_clientes()
    second = crear_base_clientes()

    pd.testing.assert_frame_equal(first, second)
    assert len(first) == 100


def test_volume_discount_applies_highest_threshold_first():
    generator = GeneradorVentasRonCana.__new__(GeneradorVentasRonCana)

    with patch("data_generation.generador_ventas.random.random", return_value=1.0):
        assert generator.calcular_descuento("Supermercados", [], 49) == 0
        assert generator.calcular_descuento("Supermercados", [], 50) == 5
        assert generator.calcular_descuento("Supermercados", [], 100) == 10
