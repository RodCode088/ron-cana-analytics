import Chart from "chart.js/auto";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import Papa from "papaparse";

import "./styles.css";
import {
  MONTH_NAMES,
  buildAiContext,
  filterRows,
  formatMoney,
  groupBySum,
  summarize,
} from "./analytics.js";
import { generateSyntheticRows, normalizeCsvRows, REQUIRED_FIELDS } from "./data-lab.js";
import { LESSONS, QUICK_QUESTIONS } from "./lessons.js";


const POWER_BI_COLORS = ["#118dff", "#12239e", "#e66c37", "#6b007b", "#e044a7", "#744ec2", "#d9b300"];
const CLIENT_ACTIONS = new Set(["navigate", "set_filter", "highlight", "show_code", "show_table", "reset_filters", "start_tour", "next_lesson"]);
const $ = (selector) => document.querySelector(selector);

const state = {
  data: null,
  sourceRows: [],
  rows: [],
  filtered: [],
  summary: null,
  datasetLabel: "Demo original",
  activeView: "dashboard",
  charts: {},
  map: null,
  mapLayer: null,
  tableId: "fact_ventas",
  tablePage: 1,
  tableSearch: "",
  codeId: "metrics",
  lessonIndex: 0,
  tourActive: false,
  toastTimer: null,
};

Chart.defaults.color = "#605e5c";
Chart.defaults.font.family = '"Segoe UI", Arial, sans-serif';
Chart.defaults.font.size = 10;
Chart.defaults.borderColor = "#edebe9";

function populateSelect(element, values, allLabel = null, formatter = (value) => value) {
  element.replaceChildren();
  if (allLabel) element.add(new Option(allLabel, ""));
  values.forEach((value) => element.add(new Option(formatter(value), value)));
}

function deriveDimensions(rows) {
  return {
    months: [...new Set(rows.map((row) => row.m))].sort((a, b) => a - b),
    channels: [...new Set(rows.map((row) => row.ch).filter(Boolean))].sort(),
    cities: [...new Set(rows.map((row) => row.c).filter(Boolean))].sort(),
    client_types: [...new Set(rows.map((row) => row.ct).filter(Boolean))].sort(),
  };
}

function configureFilters({ reset = false } = {}) {
  const dimensions = deriveDimensions(state.rows);
  const previous = reset ? {} : currentFilters();
  populateSelect($("#monthFrom"), dimensions.months, null, (month) => MONTH_NAMES[month - 1]);
  populateSelect($("#monthTo"), dimensions.months, null, (month) => MONTH_NAMES[month - 1]);
  populateSelect($("#channelFilter"), dimensions.channels, "Todos");
  populateSelect($("#cityFilter"), dimensions.cities, "Todas");
  populateSelect($("#clientFilter"), dimensions.client_types, "Todos");
  $("#monthFrom").value = dimensions.months.includes(previous.monthFrom) ? String(previous.monthFrom) : String(dimensions.months[0] || 1);
  $("#monthTo").value = dimensions.months.includes(previous.monthTo) ? String(previous.monthTo) : String(dimensions.months.at(-1) || 12);
  $("#channelFilter").value = dimensions.channels.includes(previous.channel) ? previous.channel : "";
  $("#cityFilter").value = dimensions.cities.includes(previous.city) ? previous.city : "";
  $("#clientFilter").value = dimensions.client_types.includes(previous.clientType) ? previous.clientType : "";
}

function currentFilters() {
  return {
    monthFrom: Number($("#monthFrom")?.value || 1),
    monthTo: Number($("#monthTo")?.value || 12),
    channel: $("#channelFilter")?.value || "",
    city: $("#cityFilter")?.value || "",
    clientType: $("#clientFilter")?.value || "",
  };
}

function baselineForCurrentRows() {
  return summarize(state.rows);
}

function chartOptions(overrides = {}) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 280 },
    plugins: {
      legend: { display: false },
      tooltip: { padding: 9, cornerRadius: 2, backgroundColor: "rgba(32,32,32,.94)" },
    },
    scales: {
      x: { grid: { display: false }, ticks: { maxRotation: 0 } },
      y: { beginAtZero: true, grid: { color: "#edebe9" } },
    },
    ...overrides,
  };
}

function upsertChart(name, selector, config) {
  state.charts[name]?.destroy();
  state.charts[name] = new Chart($(selector), config);
}

function setFilter(target, value) {
  const selector = { channel: "#channelFilter", city: "#cityFilter", clientType: "#clientFilter", monthFrom: "#monthFrom", monthTo: "#monthTo" }[target];
  if (!selector) return false;
  const select = $(selector);
  if (![...select.options].some((option) => option.value === String(value))) return false;
  select.value = String(value);
  renderDashboard();
  return true;
}

function renderCharts(summary) {
  upsertChart("trend", "#trendChart", {
    type: "line",
    data: {
      labels: MONTH_NAMES,
      datasets: [{
        data: summary.monthly,
        borderColor: "#118dff",
        backgroundColor: "rgba(17,141,255,.12)",
        borderWidth: 2,
        pointRadius: 2,
        pointHoverRadius: 5,
        tension: .25,
        fill: true,
      }],
    },
    options: chartOptions({
      onClick: (_event, elements) => {
        if (!elements.length) return;
        const month = elements[0].index + 1;
        setFilter("monthFrom", month);
        setFilter("monthTo", month);
        showToast(`Filtro aplicado: ${MONTH_NAMES[month - 1]}`);
      },
      scales: { x: { grid: { display: false } }, y: { beginAtZero: true, ticks: { callback: (value) => formatMoney(value) } } },
    }),
  });

  upsertChart("channel", "#channelChart", {
    type: "bar",
    data: {
      labels: summary.channels.map((item) => item.name),
      datasets: [{ data: summary.channels.map((item) => item.revenue), backgroundColor: POWER_BI_COLORS, borderRadius: 1 }],
    },
    options: chartOptions({
      indexAxis: "y",
      onClick: (_event, elements) => {
        if (!elements.length) return;
        const value = summary.channels[elements[0].index].name;
        setFilter("channel", value);
        showToast(`Canal seleccionado: ${value}`);
      },
      scales: { x: { ticks: { callback: (value) => formatMoney(value) } }, y: { grid: { display: false } } },
    }),
  });

  upsertChart("products", "#productChart", {
    type: "bar",
    data: {
      labels: summary.products.map((item) => item.name.replace("Ron Caña ", "")),
      datasets: [{ data: summary.products.map((item) => item.value), backgroundColor: "#12239e", borderRadius: 1 }],
    },
    options: chartOptions({
      indexAxis: "y",
      onClick: (_event, elements) => {
        if (!elements.length) return;
        const product = summary.products[elements[0].index].name;
        setView("data");
        selectTable("fact_ventas");
        $("#tableSearch").value = product;
        state.tableSearch = product.toLowerCase();
        renderDataTable();
        showToast("Producto abierto en el explorador de datos");
      },
      scales: { x: { ticks: { callback: (value) => formatMoney(value) } }, y: { grid: { display: false } } },
    }),
  });

  const clientGroups = groupBySum(state.filtered, "ct");
  upsertChart("client", "#clientChart", {
    type: "doughnut",
    data: {
      labels: clientGroups.map(([name]) => name),
      datasets: [{ data: clientGroups.map(([, value]) => value), backgroundColor: ["#118dff", "#e66c37", "#744ec2"], borderColor: "#fff", borderWidth: 2 }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "58%",
      onClick: (_event, elements) => {
        if (!elements.length) return;
        const value = clientGroups[elements[0].index][0];
        setFilter("clientType", value);
        showToast(`Tipo de cliente: ${value}`);
      },
      plugins: { legend: { display: true, position: "bottom", labels: { boxWidth: 9, usePointStyle: true } } },
    },
  });
}

function initMap() {
  state.map = L.map("map", { zoomControl: true, attributionControl: true }).setView([8.55, -80.45], 6);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: "© OpenStreetMap",
  }).addTo(state.map);
  state.mapLayer = L.layerGroup().addTo(state.map);
}

function renderMap() {
  if (!state.map) initMap();
  state.mapLayer.clearLayers();
  const cityRevenue = groupBySum(state.filtered, "c");
  const maxRevenue = cityRevenue[0]?.[1] || 1;
  for (const [city, revenue] of cityRevenue) {
    const coordinate = state.data.dimensions.coordinates[city];
    if (!coordinate) continue;
    const radius = 7 + Math.sqrt(revenue / maxRevenue) * 19;
    L.circleMarker([coordinate.lat, coordinate.lon], {
      radius,
      color: "#0b5cab",
      weight: 1,
      fillColor: "#118dff",
      fillOpacity: .58,
    })
      .bindTooltip(`<strong>${city}</strong><br>${formatMoney(revenue, false)}`)
      .on("click", () => {
        setFilter("city", city);
        showToast(`Ciudad seleccionada: ${city}`);
      })
      .addTo(state.mapLayer);
  }
  setTimeout(() => state.map.invalidateSize(), 0);
}

function renderDashboard() {
  const filters = currentFilters();
  if (filters.monthFrom > filters.monthTo) {
    $("#monthTo").value = String(filters.monthFrom);
  }
  state.filtered = filterRows(state.rows, currentFilters());
  state.summary = summarize(state.filtered);
  const summary = state.summary;
  const baseline = baselineForCurrentRows();
  const share = (value, total) => total ? `${((value / total) * 100).toFixed(1)}% del dataset` : "Sin datos";

  $("#revenueKpi").textContent = formatMoney(summary.revenue);
  $("#profitKpi").textContent = formatMoney(summary.profit);
  $("#marginKpi").textContent = `${summary.margin.toFixed(1)}%`;
  $("#transactionsKpi").textContent = summary.transactions.toLocaleString("es-PA");
  $("#unitsKpi").textContent = `${summary.units.toLocaleString("es-PA")} unidades`;
  $("#ticketKpi").textContent = formatMoney(summary.averageTicket, false);
  $("#revenueDelta").textContent = share(summary.revenue, baseline.revenue);
  $("#profitDelta").textContent = share(summary.profit, baseline.profit);
  $("#selectionSummary").textContent = `${summary.transactions.toLocaleString("es-PA")} filas · ${state.datasetLabel}`;

  const contextParts = [];
  if (filters.channel) contextParts.push(filters.channel);
  if (filters.city) contextParts.push(filters.city);
  if (filters.clientType) contextParts.push(filters.clientType);
  contextParts.push(`${MONTH_NAMES[filters.monthFrom - 1]}–${MONTH_NAMES[filters.monthTo - 1]}`);
  $("#filterContext").textContent = contextParts.join(" · ");
  renderCharts(summary);
  renderMap();
}

function setView(view) {
  if (!["dashboard", "model", "data", "code", "lab"].includes(view)) return;
  state.activeView = view;
  document.querySelectorAll("[data-page]").forEach((page) => page.classList.toggle("active", page.dataset.page === view));
  document.querySelectorAll(".rail-button").forEach((button) => button.classList.toggle("active", button.dataset.view === view));
  if (view === "dashboard") setTimeout(() => state.map?.invalidateSize(), 0);
  if (view === "data") renderDataTable();
}

function renderModel() {
  const canvas = $("#modelCanvas");
  canvas.replaceChildren();
  const positions = {
    dim_productos: { left: 35, top: 55 },
    dim_clientes: { left: 35, top: 245 },
    dim_eventos: { left: 35, top: 435 },
    fact_ventas: { left: 390, top: 225 },
  };

  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.classList.add("model-lines");
  svg.setAttribute("viewBox", "0 0 800 640");
  svg.innerHTML = `
    <path d="M250 135 C320 135 320 275 390 275"/><text x="275" y="145">1</text><text x="370" y="268">*</text>
    <path d="M250 325 C320 325 320 315 390 315"/><text x="275" y="318">1</text><text x="370" y="308">*</text>
    <path d="M250 515 C320 515 320 355 390 355"/><text x="275" y="505">1</text><text x="370" y="348">*</text>`;
  canvas.append(svg);

  for (const table of state.data.relational.tables) {
    const node = document.createElement("article");
    node.className = `model-table ${table.id === "fact_ventas" ? "fact" : "dimension"}`;
    node.dataset.tableId = table.id;
    node.style.left = `${positions[table.id].left}px`;
    node.style.top = `${positions[table.id].top}px`;
    const header = document.createElement("header");
    header.textContent = `${table.label}  (${table.row_count.toLocaleString("es-PA")})`;
    const list = document.createElement("ul");
    table.columns.slice(0, 10).forEach((column) => {
      const item = document.createElement("li");
      const name = document.createElement("span");
      name.textContent = column.name;
      if (["primary_key", "foreign_key"].includes(column.role)) name.classList.add("key");
      const type = document.createElement("span");
      type.textContent = column.role === "primary_key" ? "PK" : column.role === "foreign_key" ? "FK" : column.type;
      item.append(name, type);
      list.append(item);
    });
    node.append(header, list);
    node.addEventListener("click", () => showModelDetail(table.id));
    canvas.append(node);
  }
}

function showModelDetail(tableId) {
  const table = state.data.relational.tables.find((item) => item.id === tableId);
  if (!table) return;
  document.querySelectorAll(".model-table").forEach((node) => node.classList.toggle("selected", node.dataset.tableId === tableId));
  const detail = $("#modelDetail");
  detail.replaceChildren();
  const title = document.createElement("h2");
  title.textContent = table.label;
  const description = document.createElement("p");
  description.textContent = tableId === "fact_ventas"
    ? "Tabla central con el grano de una transacción. Contiene medidas y claves que conectan el contexto descriptivo."
    : "Dimensión descriptiva. Su clave primaria aparece muchas veces como clave foránea en la tabla de hechos.";
  const list = document.createElement("dl");
  list.replaceChildren();
  const details = [
    ["Filas", table.row_count.toLocaleString("es-PA")],
    ["Clave primaria", table.primary_key],
    ["Rol", tableId === "fact_ventas" ? "Hechos" : "Dimensión"],
  ];
  details.forEach(([term, value]) => {
    const dt = document.createElement("dt");
    const dd = document.createElement("dd");
    dt.textContent = term;
    dd.textContent = value;
    list.append(dt, dd);
  });
  const columns = document.createElement("div");
  table.columns.forEach((column) => {
    const chip = document.createElement("span");
    chip.className = "column-chip";
    chip.textContent = `${column.name} · ${column.role}`;
    columns.append(chip);
  });
  const openButton = document.createElement("button");
  openButton.className = "action-button";
  openButton.textContent = "Abrir registros";
  openButton.addEventListener("click", () => {
    setView("data");
    selectTable(tableId);
  });
  detail.append(title, description, list, columns, openButton);
}

function factRowsForTable() {
  return state.rows.map((row) => ({
    transaccion_id: row.id,
    fecha: row.d,
    cliente_id: row.cid,
    producto_id: row.pid,
    evento_id: row.eid,
    ciudad: row.c,
    canal_venta: row.ch,
    tipo_cliente: row.ct,
    nombre_producto: row.p,
    cantidad: row.u,
    ingreso_total: row.r,
    utilidad_bruta: row.g,
    descuento_porcentaje: row.disc,
    devolucion: row.ret,
    campana: row.cp,
  }));
}

function tableRows(tableId) {
  return tableId === "fact_ventas" ? factRowsForTable() : state.data.relational.data[tableId] || [];
}

function selectTable(tableId) {
  if (!state.data.relational.tables.some((table) => table.id === tableId)) return;
  state.tableId = tableId;
  state.tablePage = 1;
  $("#tableSelect").value = tableId;
  renderDataTable();
}

function renderDataTable() {
  const rows = tableRows(state.tableId);
  const query = state.tableSearch;
  const filtered = query ? rows.filter((row) => Object.values(row).some((value) => String(value ?? "").toLowerCase().includes(query))) : rows;
  const pageSize = 50;
  const pages = Math.max(1, Math.ceil(filtered.length / pageSize));
  state.tablePage = Math.min(state.tablePage, pages);
  const pageRows = filtered.slice((state.tablePage - 1) * pageSize, state.tablePage * pageSize);
  const columns = pageRows[0] ? Object.keys(pageRows[0]) : [];
  const table = $("#dataTable");
  table.replaceChildren();
  const head = document.createElement("thead");
  const headRow = document.createElement("tr");
  columns.forEach((column) => {
    const cell = document.createElement("th");
    cell.textContent = column;
    headRow.append(cell);
  });
  head.append(headRow);
  const body = document.createElement("tbody");
  pageRows.forEach((row) => {
    const tr = document.createElement("tr");
    columns.forEach((column) => {
      const td = document.createElement("td");
      td.textContent = row[column] === null || row[column] === undefined ? "—" : String(row[column]);
      td.title = td.textContent;
      tr.append(td);
    });
    body.append(tr);
  });
  table.append(head, body);
  $("#tableCount").textContent = `${filtered.length.toLocaleString("es-PA")} registros`;
  $("#pageStatus").textContent = `Página ${state.tablePage} de ${pages}`;
  $("#prevPage").disabled = state.tablePage <= 1;
  $("#nextPage").disabled = state.tablePage >= pages;
}

function renderCodeFiles() {
  const container = $("#codeFiles");
  container.replaceChildren();
  Object.entries(state.data.code).forEach(([id, file]) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `code-file ${id === state.codeId ? "active" : ""}`;
    const label = document.createElement("strong");
    label.textContent = file.label;
    const path = document.createElement("span");
    path.textContent = file.path;
    button.append(label, path);
    button.addEventListener("click", () => selectCode(id));
    container.append(button);
  });
  selectCode(state.codeId);
}

function selectCode(codeId) {
  const file = state.data.code[codeId];
  if (!file) return;
  state.codeId = codeId;
  document.querySelectorAll(".code-file").forEach((button, index) => {
    const id = Object.keys(state.data.code)[index];
    button.classList.toggle("active", id === codeId);
  });
  $("#codeTitle").textContent = file.label;
  $("#codePath").textContent = file.path;
  $("#codeLesson").textContent = file.lesson;
  $("#codeContent").textContent = file.content;
}

function renderLesson(moveInterface = false) {
  const lesson = LESSONS[state.lessonIndex];
  const lessonBody = lesson.body.replace(
    "{transactions}",
    state.rows.length.toLocaleString("es-PA"),
  );
  $("#lessonCounter").textContent = `Lección ${state.lessonIndex + 1} de ${LESSONS.length}`;
  $("#lessonProgress").value = state.lessonIndex + 1;
  $("#lessonProgress").max = LESSONS.length;
  $("#lessonTitle").textContent = lesson.title;
  $("#lessonBody").textContent = lessonBody;
  $("#previousLesson").disabled = state.lessonIndex === 0;
  $("#nextLesson").textContent = state.lessonIndex === LESSONS.length - 1 ? "Finalizar" : "Siguiente";
  if (moveInterface) {
    setView(lesson.view);
    highlightTarget(lesson.target, 6000);
  }
  if (state.tourActive) {
    $("#tourStep").textContent = `Paso ${state.lessonIndex + 1} de ${LESSONS.length}`;
    $("#tourTitle").textContent = lesson.title;
    $("#tourBody").textContent = lessonBody;
    $("#tourPopover").hidden = false;
  }
}

function nextLesson() {
  if (state.lessonIndex >= LESSONS.length - 1) {
    stopTour();
    addMessage("assistant", "Recorrido completado. Ya puedes explorar libremente o preguntarme por cualquier parte del proyecto.", "Clase completada");
    return;
  }
  state.lessonIndex += 1;
  renderLesson(true);
}

function previousLesson() {
  state.lessonIndex = Math.max(0, state.lessonIndex - 1);
  renderLesson(true);
}

function startTour() {
  state.lessonIndex = 0;
  state.tourActive = true;
  $("#tutorPanel").classList.add("open");
  renderLesson(true);
}

function stopTour() {
  state.tourActive = false;
  $("#tourPopover").hidden = true;
  clearHighlights();
}

function clearHighlights() {
  document.querySelectorAll(".tour-highlight").forEach((element) => element.classList.remove("tour-highlight"));
}

function highlightTarget(target, duration = 3500) {
  clearHighlights();
  const element = document.querySelector(`[data-tour-target="${CSS.escape(target)}"]`);
  if (!element) return;
  element.classList.add("tour-highlight");
  element.scrollIntoView({ behavior: "smooth", block: "center" });
  if (!state.tourActive) setTimeout(() => element.classList.remove("tour-highlight"), duration);
}

function addMessage(role, text, concept = "", actions = []) {
  const message = document.createElement("div");
  message.className = `message ${role}`;
  if (concept) {
    const label = document.createElement("span");
    label.className = "concept";
    label.textContent = concept;
    message.append(label);
  }
  const content = document.createElement("span");
  content.textContent = text;
  message.append(content);
  if (actions.length) {
    const chips = document.createElement("div");
    chips.className = "action-chips";
    actions.forEach((action) => {
      const chip = document.createElement("span");
      chip.className = "action-chip";
      chip.textContent = `${action.type}: ${action.target || action.value}`;
      chips.append(chip);
    });
    message.append(chips);
  }
  $("#chatMessages").append(message);
  $("#chatMessages").scrollTop = $("#chatMessages").scrollHeight;
}

function localTutor(question) {
  const normalized = question.toLowerCase();
  if (/modelo|relaci|estrella|tabla|clave/.test(normalized)) return { concept: "Modelo estrella", explanation: "La tabla fact_ventas almacena el evento medible y las dimensiones aportan contexto. Abro la tabla central y termino en el diagrama para que puedas comprobar la relación.", actions: [{ type: "show_table", target: "fact_ventas", value: "", reason: "Mostrar hechos" }, { type: "navigate", target: "model", value: "", reason: "Abrir modelo" }, { type: "highlight", target: "model", value: "", reason: "Resaltar relaciones" }], check_question: "¿Cuál es el grano de fact_ventas?", mode: "client-fallback" };
  if (/código|codigo|python|kpi|margen/.test(normalized)) return { concept: "Métrica canónica", explanation: "El margen ponderado se calcula como utilidad total dividida por ingreso total. Abro la definición real para evitar que la interfaz y el análisis usen fórmulas distintas.", actions: [{ type: "show_code", target: "metrics", value: "", reason: "Mostrar KPIs" }], check_question: "¿Por qué no usamos el promedio simple de porcentajes?", mode: "client-fallback" };
  if (/mapa|zona|ciudad/.test(normalized)) return { concept: "Geografía", explanation: "Cada burbuja agrega ingreso por ciudad y puede actuar como filtro del resto del reporte.", actions: [{ type: "navigate", target: "dashboard", value: "", reason: "Abrir reporte" }, { type: "highlight", target: "map", value: "", reason: "Resaltar mapa" }], check_question: "¿Qué otra medida compararías por ciudad?", mode: "client-fallback" };
  if (/csv|subir|import|sintét|sintet|gener/.test(normalized)) return { concept: "Laboratorio", explanation: "Puedes generar una muestra reproducible o importar el contrato CSV. Las filas permanecen en el navegador.", actions: [{ type: "navigate", target: "lab", value: "", reason: "Abrir laboratorio" }], check_question: "¿Qué valida el contrato antes de analizar?", mode: "client-fallback" };
  const channel = state.summary.channels[0];
  return { concept: "Lectura descriptiva", explanation: `El contexto tiene ${state.summary.transactions.toLocaleString("es-PA")} transacciones y ${formatMoney(state.summary.revenue, false)} de ingreso. ${channel ? `${channel.name} lidera por escala.` : ""} Recuerda: los datos son sintéticos y no prueban causalidad.`, actions: [{ type: "navigate", target: "dashboard", value: "", reason: "Mostrar evidencia" }, { type: "highlight", target: "kpis", value: "", reason: "Resaltar KPIs" }], check_question: "¿Qué dimensión explorarías a continuación?", mode: "client-fallback" };
}

function tutorContext() {
  const base = buildAiContext(state.summary, currentFilters());
  const lesson = LESSONS[state.lessonIndex];
  return {
    ...base,
    active_view: state.activeView,
    lesson: {
      ...lesson,
      body: lesson.body.replace("{transactions}", state.rows.length.toLocaleString("es-PA")),
    },
    available: {
      filters: {
        channels: deriveDimensions(state.rows).channels,
        cities: deriveDimensions(state.rows).cities,
      },
    },
  };
}

function validClientAction(action) {
  if (!CLIENT_ACTIONS.has(action?.type)) return false;
  const allowedViews = ["dashboard", "model", "data", "code", "lab"];
  const allowedHighlights = ["kpis", "trend", "channel", "products", "map", "filters", "model", "data-grid", "code-viewer", "tutor", "lab"];
  const allowedTables = state.data.relational.tables.map((table) => table.id);
  const allowedCode = Object.keys(state.data.code);
  if (action.type === "navigate") return allowedViews.includes(action.target);
  if (action.type === "highlight") return allowedHighlights.includes(action.target);
  if (action.type === "show_table") return allowedTables.includes(action.target);
  if (action.type === "show_code") return allowedCode.includes(action.target);
  if (action.type === "set_filter") {
    const dimensions = deriveDimensions(state.rows);
    return (action.target === "channel" && dimensions.channels.includes(action.value))
      || (action.target === "city" && dimensions.cities.includes(action.value))
      || (action.target === "clientType" && dimensions.client_types.includes(action.value))
      || (["monthFrom", "monthTo"].includes(action.target) && Number(action.value) >= 1 && Number(action.value) <= 12);
  }
  return true;
}

function applyTutorActions(actions) {
  const applied = [];
  (Array.isArray(actions) ? actions : []).slice(0, 4).forEach((action) => {
    if (!validClientAction(action)) return;
    if (action.type === "navigate") setView(action.target);
    if (action.type === "set_filter") setFilter(action.target, action.value);
    if (action.type === "highlight") highlightTarget(action.target);
    if (action.type === "show_code") { setView("code"); selectCode(action.target); highlightTarget("code-viewer"); }
    if (action.type === "show_table") { setView("data"); selectTable(action.target); highlightTarget("data-grid"); }
    if (action.type === "reset_filters") resetFilters();
    if (action.type === "start_tour") startTour();
    if (action.type === "next_lesson") nextLesson();
    applied.push(action);
  });
  return applied;
}

async function askTutor(event) {
  event?.preventDefault();
  const question = $("#tutorQuestion").value.trim();
  if (!question) return;
  addMessage("user", question);
  $("#tutorQuestion").value = "";
  $("#askTutor").disabled = true;
  $("#tutorMode").textContent = "Analizando contexto…";

  let result;
  try {
    const response = await fetch("/api/tutor", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ question, context: tutorContext() }),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    result = await response.json();
  } catch {
    result = localTutor(question);
  }

  const actions = applyTutorActions(result.actions);
  addMessage("assistant", `${result.explanation}${result.check_question ? `\n\nComprueba: ${result.check_question}` : ""}`, result.concept, actions);
  $("#tutorMode").textContent = result.mode === "gemini" ? "Gemini 3.7 Flash" : "Modo guiado local";
  $("#tutorRequestId").textContent = result.request_id ? result.request_id.slice(0, 8) : "local";
  $("#askTutor").disabled = false;
}

function updateRows(rows, label, custom = true) {
  state.rows = rows;
  state.datasetLabel = label;
  configureFilters({ reset: true });
  const datasetBadge = $("#datasetBadge");
  datasetBadge.classList.toggle("custom", custom);
  datasetBadge.replaceChildren();
  const statusDot = document.createElement("i");
  const statusText = document.createTextNode(
    ` ${label} · ${rows.length.toLocaleString("es-PA")} filas`,
  );
  datasetBadge.append(statusDot, statusText);
  $("#labStatus").textContent = `${label}: ${rows.length.toLocaleString("es-PA")} filas listas para explorar.`;
  state.tablePage = 1;
  renderDashboard();
  if (state.activeView === "data") renderDataTable();
  showToast(`${label} cargado correctamente`);
}

function resetFilters() {
  configureFilters({ reset: true });
  renderDashboard();
  showToast("Filtros restablecidos");
}

function showToast(message) {
  clearTimeout(state.toastTimer);
  $("#toast").textContent = message;
  $("#toast").classList.add("show");
  state.toastTimer = setTimeout(() => $("#toast").classList.remove("show"), 2600);
}

function bindEvents() {
  document.querySelectorAll(".rail-button").forEach((button) => button.addEventListener("click", () => setView(button.dataset.view)));
  document.querySelectorAll(".filters-pane select").forEach((select) => select.addEventListener("change", renderDashboard));
  $("#resetFilters").addEventListener("click", resetFilters);
  $("#toggleTutorButton").addEventListener("click", () => $("#tutorPanel").classList.toggle("open"));
  $("#closeTutor").addEventListener("click", () => $("#tutorPanel").classList.remove("open"));
  $("#startTourButton").addEventListener("click", startTour);
  $("#previousLesson").addEventListener("click", previousLesson);
  $("#nextLesson").addEventListener("click", nextLesson);
  $("#tourNext").addEventListener("click", nextLesson);
  $("#tutorForm").addEventListener("submit", askTutor);
  $("#tableSelect").addEventListener("change", (event) => selectTable(event.target.value));
  $("#tableSearch").addEventListener("input", (event) => { state.tableSearch = event.target.value.trim().toLowerCase(); state.tablePage = 1; renderDataTable(); });
  $("#prevPage").addEventListener("click", () => { state.tablePage -= 1; renderDataTable(); });
  $("#nextPage").addEventListener("click", () => { state.tablePage += 1; renderDataTable(); });
  $("#copyCode").addEventListener("click", async () => { await navigator.clipboard.writeText(state.data.code[state.codeId].content); showToast("Código copiado"); });
  $("#rowCountInput").addEventListener("input", (event) => { $("#rowCountOutput").value = Number(event.target.value).toLocaleString("es-PA"); });
  $("#generateDataButton").addEventListener("click", () => {
    const count = Number($("#rowCountInput").value);
    const seed = Number($("#seedInput").value);
    const dimensions = deriveDimensions(state.sourceRows);
    updateRows(generateSyntheticRows(count, seed, dimensions), `Muestra generada · seed ${seed}`);
    setView("dashboard");
  });
  $("#csvInput").addEventListener("change", (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    if (file.size > 8_000_000) { $("#labStatus").textContent = "El archivo supera 8 MB."; return; }
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: ({ data, errors }) => {
        try {
          if (errors.length) throw new Error(errors[0].message);
          if (data.length > 25_000) throw new Error("El archivo supera 25.000 filas.");
          updateRows(normalizeCsvRows(data), `CSV · ${file.name}`);
          setView("dashboard");
        } catch (error) {
          $("#labStatus").textContent = `No se pudo cargar: ${error.message}`;
        }
      },
    });
  });
  $("#restoreDataButton").addEventListener("click", () => updateRows(state.sourceRows, "Demo original", false));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") { $("#tutorPanel").classList.remove("open"); stopTour(); }
  });
}

function setupStaticUi() {
  state.data.relational.tables.forEach((table) => $("#tableSelect").add(new Option(`${table.label} (${table.row_count.toLocaleString("es-PA")})`, table.id)));
  REQUIRED_FIELDS.forEach((field) => { const code = document.createElement("code"); code.textContent = field; $("#requiredFields").append(code); });
  QUICK_QUESTIONS.forEach((question) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = question;
    button.addEventListener("click", () => { $("#tutorQuestion").value = question; askTutor(); });
    $("#quickQuestions").append(button);
  });
  $("#dataQualityBadge").textContent = state.data.meta.quality.valid ? "✓ Contrato válido" : "Contrato con errores";
  renderModel();
  showModelDetail("fact_ventas");
  renderCodeFiles();
  renderLesson();
  addMessage("assistant", "Bienvenido. Puedo explicarte el reporte, abrir el modelo, mostrar el código y mover la interfaz mediante acciones seguras. Inicia el recorrido o hazme una pregunta.", "Tutor interactivo");
}

async function init() {
  const response = await fetch("/data/dashboard.json");
  if (!response.ok) throw new Error("No se pudo cargar el data product.");
  state.data = await response.json();
  state.sourceRows = state.data.rows;
  state.rows = state.sourceRows;
  configureFilters({ reset: true });
  setupStaticUi();
  bindEvents();
  updateRows(state.sourceRows, "Demo original", false);
}

init().catch((error) => {
  $("#workspace").textContent = `No pudimos abrir la clase: ${error.message}`;
});
