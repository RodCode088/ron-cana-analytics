import { describe, expect, it } from "vitest";
import { generateSyntheticRows, normalizeCsvRows, REQUIRED_FIELDS } from "./data-lab.js";

const dimensions = {
  channels: ["E-commerce", "Retail"],
  cities: ["Panamá", "Colón"],
};

describe("laboratorio de datos", () => {
  it("genera datos determinísticos, válidos y compatibles con el dashboard", () => {
    const first = generateSyntheticRows(25, 42, dimensions);
    const second = generateSyntheticRows(25, 42, dimensions);

    expect(first).toEqual(second);
    expect(first).toHaveLength(25);
    expect(first.every((row) => row.r > 0 && row.g > 0 && row.u > 0)).toBe(true);
    expect(new Set(first.map((row) => row.id)).size).toBe(25);
  });

  it("normaliza el contrato CSV a las claves compactas de la aplicación", () => {
    const rows = normalizeCsvRows([{
      fecha: "2025-03-12",
      ciudad: "Panamá",
      canal_venta: "E-commerce",
      tipo_cliente: "B2C",
      nombre_producto: "Ron de prueba",
      cantidad: "2",
      ingreso_total: "80.50",
      utilidad_bruta: "43.25",
    }]);

    expect(rows[0]).toMatchObject({
      d: "2025-03-12",
      m: 3,
      c: "Panamá",
      ch: "E-commerce",
      ct: "B2C",
      p: "Ron de prueba",
      u: 2,
      r: 80.5,
      g: 43.25,
    });
  });

  it("rechaza archivos sin las columnas obligatorias", () => {
    expect(() => normalizeCsvRows([{ fecha: "2025-01-01" }])).toThrow(
      `Faltan columnas: ${REQUIRED_FIELDS.slice(1).join(", ")}`,
    );
  });
});
