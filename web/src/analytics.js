export const MONTH_NAMES = [
  "Ene", "Feb", "Mar", "Abr", "May", "Jun",
  "Jul", "Ago", "Sep", "Oct", "Nov", "Dic",
];

export function filterRows(rows, filters) {
  return rows.filter((row) => (
    row.m >= filters.monthFrom
    && row.m <= filters.monthTo
    && (!filters.channel || row.ch === filters.channel)
    && (!filters.city || row.c === filters.city)
    && (!filters.clientType || row.ct === filters.clientType)
  ));
}

function sum(rows, key) {
  return rows.reduce((total, row) => total + Number(row[key] || 0), 0);
}

export function groupBySum(rows, groupKey, valueKey = "r") {
  const grouped = new Map();
  for (const row of rows) {
    grouped.set(row[groupKey], (grouped.get(row[groupKey]) || 0) + Number(row[valueKey] || 0));
  }
  return [...grouped.entries()].sort((a, b) => b[1] - a[1]);
}

export function summarize(rows) {
  const revenue = sum(rows, "r");
  const profit = sum(rows, "g");
  const campaign = rows.filter((row) => row.cp);
  const organic = rows.filter((row) => !row.cp);
  const channels = groupBySum(rows, "ch").map(([name, channelRevenue]) => {
    const channelRows = rows.filter((row) => row.ch === name);
    const channelProfit = sum(channelRows, "g");
    return {
      name,
      revenue: channelRevenue,
      margin: channelRevenue ? (channelProfit / channelRevenue) * 100 : 0,
    };
  });

  return {
    revenue,
    profit,
    margin: revenue ? (profit / revenue) * 100 : 0,
    transactions: rows.length,
    units: sum(rows, "u"),
    averageTicket: rows.length ? revenue / rows.length : 0,
    monthly: Array.from({ length: 12 }, (_, index) => (
      rows.filter((row) => row.m === index + 1).reduce((total, row) => total + row.r, 0)
    )),
    products: groupBySum(rows, "p").slice(0, 5).map(([name, value]) => ({ name, value })),
    cities: groupBySum(rows, "c").slice(0, 6).map(([name, value]) => ({ name, value })),
    channels,
    campaignTicket: campaign.length ? sum(campaign, "r") / campaign.length : null,
    organicTicket: organic.length ? sum(organic, "r") / organic.length : null,
  };
}

export function buildAiContext(summary, filters) {
  return {
    selection: filters,
    kpis: {
      revenue: Math.round(summary.revenue),
      gross_profit: Math.round(summary.profit),
      weighted_margin_pct: Number(summary.margin.toFixed(2)),
      transactions: summary.transactions,
      units: summary.units,
      average_ticket: Math.round(summary.averageTicket),
    },
    channels: summary.channels.slice(0, 6).map((item) => ({
      name: item.name,
      revenue: Math.round(item.revenue),
      margin_pct: Number(item.margin.toFixed(2)),
    })),
    top_products: summary.products.slice(0, 5).map((item) => ({
      name: item.name,
      revenue: Math.round(item.value),
    })),
    top_cities: summary.cities.slice(0, 5).map((item) => ({
      name: item.name,
      revenue: Math.round(item.value),
    })),
    campaign_ticket: summary.campaignTicket ? Math.round(summary.campaignTicket) : null,
    non_campaign_ticket: summary.organicTicket ? Math.round(summary.organicTicket) : null,
    caveat: "Datos sintéticos. La comparación de campañas es descriptiva; no demuestra causalidad ni ROI.",
  };
}

export function localBrief(summary) {
  if (!summary.transactions) return "No hay datos para esta selección. Amplía los filtros.";

  const topChannel = summary.channels[0];
  const marginLeader = [...summary.channels].sort((a, b) => b.margin - a.margin)[0];
  const topProduct = summary.products[0];
  const concentration = topProduct ? (topProduct.value / summary.revenue) * 100 : 0;
  const lines = [
    `• ${topChannel.name} lidera por ingreso con ${formatMoney(topChannel.revenue)}.`,
    `• ${marginLeader.name} presenta el mayor margen ponderado: ${marginLeader.margin.toFixed(1)}%.`,
    `• ${topProduct.name} concentra ${concentration.toFixed(1)}% del ingreso filtrado.`,
  ];

  if (summary.campaignTicket && summary.organicTicket) {
    const difference = (summary.campaignTicket / summary.organicTicket - 1) * 100;
    lines.push(`• El ticket durante campañas es ${difference >= 0 ? "+" : ""}${difference.toFixed(1)}%; es una asociación descriptiva, no ROI.`);
  }
  return lines.join("\n");
}

export function formatMoney(value, compact = true) {
  return new Intl.NumberFormat("es-PA", {
    style: "currency",
    currency: "USD",
    notation: compact ? "compact" : "standard",
    maximumFractionDigits: compact ? 2 : 0,
  }).format(value || 0);
}
