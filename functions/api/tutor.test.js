import assert from "node:assert/strict";
import test from "node:test";

import { fallbackTutor, onRequestPost, sanitizeActions, sanitizeContext } from "./tutor.js";

const rawContext = {
  active_view: "dashboard",
  lesson: { id: "intro", title: "Introducción" },
  selection: { monthFrom: 1, monthTo: 12, channel: "", city: "", clientType: "" },
  kpis: { revenue: 1000, gross_profit: 550, weighted_margin_pct: 55, transactions: 10, units: 20, average_ticket: 100 },
  channels: [{ name: "Retail", revenue: 1000, margin_pct: 55 }],
  top_products: [{ name: "Añejo", revenue: 700 }],
  top_cities: [{ name: "Panamá", revenue: 900 }],
  available: { filters: { channels: ["Retail"], cities: ["Panamá"] } },
};

test("context is allowlisted and never includes row-level data", () => {
  const context = sanitizeContext({ ...rawContext, rows: [{ customer: "secret" }] });
  assert.equal(context.rows, undefined);
  assert.equal(context.kpis.transactions, 10);
});

test("unknown or invalid actions are removed", () => {
  const context = sanitizeContext(rawContext);
  const actions = sanitizeActions([
    { type: "navigate", target: "model", value: "", reason: "ok" },
    { type: "execute_javascript", target: "body", value: "hack", reason: "bad" },
    { type: "set_filter", target: "channel", value: "Unknown", reason: "bad" },
  ], context);
  assert.deepEqual(actions, [{ type: "navigate", target: "model", value: "", reason: "ok" }]);
});

test("fallback teaches the relational model with UI actions", () => {
  const result = fallbackTutor("Explícame el modelo relacional", sanitizeContext(rawContext));
  assert.equal(result.concept, "Modelo estrella");
  assert.deepEqual(
    result.actions.map(({ type, target }) => ({ type, target })),
    [
      { type: "show_table", target: "fact_ventas" },
      { type: "navigate", target: "model" },
      { type: "highlight", target: "model" },
    ],
  );
});

test("endpoint works without a Gemini key", async () => {
  const request = new Request("https://example.test/api/tutor", {
    method: "POST",
    body: JSON.stringify({ question: "Enséñame el mapa", context: rawContext }),
  });
  const response = await onRequestPost({ request, env: {} });
  const payload = await response.json();
  assert.equal(response.status, 200);
  assert.equal(payload.mode, "guided-fallback");
  assert.equal(payload.actions[0].target, "dashboard");
});
