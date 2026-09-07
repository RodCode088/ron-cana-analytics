import { describe, expect, it } from "vitest";
import { buildAiContext, filterRows, localBrief, summarize } from "./analytics.js";

const rows = [
  { m: 1, ch: "Retail", c: "Panamá", ct: "B2B", p: "A", r: 100, g: 50, u: 2, cp: null },
  { m: 2, ch: "Horeca", c: "David", ct: "B2C", p: "B", r: 200, g: 120, u: 1, cp: "Promo" },
];

describe("analytics data product", () => {
  it("filters by the complete selection", () => {
    const result = filterRows(rows, { monthFrom: 2, monthTo: 12, channel: "", city: "David", clientType: "B2C" });
    expect(result).toHaveLength(1);
    expect(result[0].p).toBe("B");
  });

  it("uses weighted margin", () => {
    const result = summarize(rows);
    expect(result.revenue).toBe(300);
    expect(result.profit).toBe(170);
    expect(result.margin).toBeCloseTo(56.666, 2);
  });

  it("sends only aggregated context to AI", () => {
    const context = buildAiContext(summarize(rows), { monthFrom: 1, monthTo: 12 });
    expect(context.kpis.transactions).toBe(2);
    expect(context).not.toHaveProperty("rows");
    expect(JSON.stringify(context)).not.toContain('"d"');
  });

  it("keeps the local fallback honest", () => {
    expect(localBrief(summarize(rows))).toContain("no ROI");
  });
});
