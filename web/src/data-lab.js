const REQUIRED_FIELDS = [
  "fecha",
  "ciudad",
  "canal_venta",
  "tipo_cliente",
  "nombre_producto",
  "cantidad",
  "ingreso_total",
  "utilidad_bruta",
];

function lcg(seed) {
  let state = Number(seed) || 2024;
  return () => {
    state = (state * 1664525 + 1013904223) % 4294967296;
    return state / 4294967296;
  };
}

function pick(values, random) {
  return values[Math.floor(random() * values.length)];
}

export function generateSyntheticRows(count, seed, dimensions) {
  const random = lcg(seed);
  const products = [
    ["Ron Caña Blanco Artesanal", 18, 0.58],
    ["Ron Caña Añejo 8 Años", 42, 0.57],
    ["Ron Caña Extra Añejo 12 Años", 63, 0.55],
    ["Ron Caña Edición Limitada Roble Europeo", 180, 0.52],
    ["Gift Set Añejo 8 Años + 2 Copas", 62, 0.54],
  ];
  const channels = dimensions.channels;
  const cities = dimensions.cities;
  return Array.from({ length: count }, (_, index) => {
    const month = 1 + Math.floor(random() * 12);
    const day = 1 + Math.floor(random() * 27);
    const [product, price, baseMargin] = pick(products, random);
    const clientType = random() < 0.82 ? "B2B" : "B2C";
    const units = clientType === "B2B" ? 6 + Math.floor(random() * 80) : 1 + Math.floor(random() * 4);
    const discount = random() < 0.28 ? Math.floor(random() * 16) : 0;
    const revenue = price * units * (1 - discount / 100);
    const margin = Math.max(0.38, baseMargin - discount / 220);
    return {
      id: `LAB-${seed}-${String(index + 1).padStart(5, "0")}`,
      d: `2024-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`,
      m: month,
      c: pick(cities, random),
      ch: pick(channels, random),
      ct: clientType,
      seg: clientType === "B2B" ? "Cliente Comercial" : "Consumidor Final",
      cid: `LAB-CLI-${Math.floor(random() * 120) + 1}`,
      p: product,
      pid: `LAB-PROD-${products.findIndex((item) => item[0] === product) + 1}`,
      cat: "Ron Premium",
      r: Number(revenue.toFixed(2)),
      g: Number((revenue * margin).toFixed(2)),
      u: units,
      disc: discount,
      ret: random() < 0.02,
      eid: null,
      cp: null,
    };
  });
}

export function normalizeCsvRows(parsedRows) {
  if (!Array.isArray(parsedRows) || !parsedRows.length) {
    throw new Error("El CSV no contiene filas.");
  }
  const headers = Object.keys(parsedRows[0]);
  const missing = REQUIRED_FIELDS.filter((field) => !headers.includes(field));
  if (missing.length) throw new Error(`Faltan columnas: ${missing.join(", ")}`);

  const normalized = parsedRows.flatMap((row, index) => {
    const revenue = Number(row.ingreso_total);
    const profit = Number(row.utilidad_bruta);
    const units = Number(row.cantidad);
    const date = String(row.fecha || "").slice(0, 10);
    const month = Number(date.slice(5, 7));
    if (!date || month < 1 || month > 12 || !Number.isFinite(revenue) || !Number.isFinite(profit) || !Number.isFinite(units)) return [];
    return [{
      id: `CSV-${String(index + 1).padStart(5, "0")}`,
      d: date,
      m: month,
      c: String(row.ciudad).trim(),
      ch: String(row.canal_venta).trim(),
      ct: String(row.tipo_cliente).trim() || "Sin clasificar",
      seg: String(row.segmento_cliente || "Importado").trim(),
      cid: String(row.cliente_id || `CSV-CLI-${index + 1}`),
      p: String(row.nombre_producto).trim(),
      pid: String(row.producto_id || `CSV-PROD-${index + 1}`),
      cat: String(row.categoria_producto || "Importado").trim(),
      r: revenue,
      g: profit,
      u: Math.round(units),
      disc: Number(row.descuento_porcentaje || 0),
      ret: String(row.devolucion || "").toLowerCase() === "true",
      eid: row.evento_id || null,
      cp: row.campana || null,
    }];
  });
  if (!normalized.length) throw new Error("Ninguna fila contiene fecha y métricas válidas.");
  return normalized;
}

export { REQUIRED_FIELDS };
