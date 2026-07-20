export const METRIC_VISUALIZATION_SCHEMA = "metric-visualization-v1";

const CATALOG = [
  {
    id: "sparkline",
    label: "Sparkline",
    semantic_purpose: "Show a compact numeric trend across supplied visible periods.",
    precision_rule: "Use the source precision; do not add decimal places.",
    uncertainty_rule: "Show uncertainty as text beside the line; never as an implied probability.",
    missingness_rule: "Leave missing periods visibly unconnected and label them missing.",
    exact_text_rule: "Keep every supplied period and exact value in text.",
    color_independent_rule: "Use a line, period labels, and text; color is supplementary.",
    large_text_rule: "Keep the line bounded while allowing labels and exact text to reflow.",
    screenshot_fixture: "numeric trend with a missing middle period",
  },
  {
    id: "delta",
    label: "Month-over-month delta",
    semantic_purpose: "Show the visible change between two supplied periods.",
    precision_rule: "Subtract only values supplied at the same precision as the source.",
    uncertainty_rule: "State when either comparison value is uncertain or not comparable.",
    missingness_rule: "Do not calculate a delta when either period is missing.",
    exact_text_rule: "Show both source values and the resulting visible delta in text.",
    color_independent_rule: "Use an explicit increase, decrease, or unchanged label.",
    large_text_rule: "Stack the two values and delta label when text grows.",
    screenshot_fixture: "visible increase with exact source values",
  },
  {
    id: "capacity-bar",
    label: "Capacity bar",
    semantic_purpose: "Compare visible used and available capacity without implying a forecast.",
    precision_rule: "Use supplied capacity units; do not convert to a percentage unless supplied.",
    uncertainty_rule: "Place uncertainty text beside the bar, not in its length.",
    missingness_rule: "Show an empty patterned track and missing label when capacity is absent.",
    exact_text_rule: "Show used, total, and unit text exactly as supplied.",
    color_independent_rule: "Use a patterned fill, track, and written used/total values.",
    large_text_rule: "Keep the bar shallow and let the exact values stack below it.",
    screenshot_fixture: "staffed capacity compared with visible total",
  },
  {
    id: "staffing-composition",
    label: "Staffing composition",
    semantic_purpose: "Show visible staffing categories as a bounded composition.",
    precision_rule: "Use supplied headcounts or category units; do not infer workforce quality.",
    uncertainty_rule: "Keep uncertain category labels visible beside their segment text.",
    missingness_rule: "Show unavailable categories explicitly instead of redistributing them.",
    exact_text_rule: "Retain every category and exact supplied count in the legend.",
    color_independent_rule: "Give each category a distinct pattern and written label.",
    large_text_rule: "Move the category legend below the composition when text grows.",
    screenshot_fixture: "three visible staffing categories",
  },
  {
    id: "project-progress",
    label: "Project progress",
    semantic_purpose: "Show visible completed and remaining project units without promising completion.",
    precision_rule: "Use supplied completed and total units; do not invent elapsed percentages.",
    uncertainty_rule: "Keep pending effect and completion uncertainty as written text.",
    missingness_rule: "Show progress as unavailable when completed or total is absent.",
    exact_text_rule: "Show completed, total, timing, and status text exactly as supplied.",
    color_independent_rule: "Use a progress track plus completed/total labels and patterns.",
    large_text_rule: "Stack progress labels and status below the track.",
    screenshot_fixture: "visible project units completed of total",
  },
  {
    id: "payer-mix",
    label: "Payer-mix summary",
    semantic_purpose: "Show supplied payer categories as a visible mix, not a market estimate.",
    precision_rule: "Use the source’s supplied units or shares; do not normalize missing categories.",
    uncertainty_rule: "Label provisional or stale category values next to their text.",
    missingness_rule: "Keep missing payer categories explicit and do not fill them from context.",
    exact_text_rule: "Show each payer category and exact supplied value in text.",
    color_independent_rule: "Use segment patterns and payer names in a written legend.",
    large_text_rule: "Stack the mix legend below the track when needed.",
    screenshot_fixture: "two supplied payer categories and one missing category",
  },
  {
    id: "trust-trend",
    label: "Trust or legitimacy trend",
    semantic_purpose: "Show the sequence of visible trust or legitimacy labels without scoring it.",
    precision_rule: "Preserve categorical source language; do not convert labels to a numeric score.",
    uncertainty_rule: "Keep revised, stale, or uncertain labels visible at their periods.",
    missingness_rule: "Show missing periods as gaps rather than interpolating trust.",
    exact_text_rule: "Show each period’s exact visible label and source text.",
    color_independent_rule: "Use point shapes, connecting rules, and written categories.",
    large_text_rule: "Allow period/category labels to wrap below the trend.",
    screenshot_fixture: "moderate-to-high visible trust labels",
  },
  {
    id: "uncertainty-interval",
    label: "Visible uncertainty interval",
    semantic_purpose: "Show a host-supplied visible interval without calling it a probability.",
    precision_rule: "Retain the lower, estimate, and upper precision supplied by the source.",
    uncertainty_rule: "Label the interval as visible uncertainty and retain its source wording.",
    missingness_rule: "Show an unavailable interval when any required bound is missing.",
    exact_text_rule: "Show lower, estimate, upper, unit, and source text in the DOM.",
    color_independent_rule: "Use a whisker, point, end caps, and written bounds.",
    large_text_rule: "Stack bound labels below the whisker when text grows.",
    screenshot_fixture: "host-supplied lower, estimate, and upper values",
  },
].map((entry) => Object.freeze({ ...entry }));

export const METRIC_VISUALIZATION_PROOF_FIXTURES = Object.freeze([
  Object.freeze({ label: "Monthly margin", visualization_kind: "sparkline", exact_text: "Monthly margin: +12, +11, unavailable, +14 units", source: "PlayerObservation.monthly_margin", values: [{ period: "Jan", value: 12, display: "+12 units" }, { period: "Feb", value: 11, display: "+11 units" }, { period: "Mar", display: "Unavailable", status: "missing" }, { period: "Apr", value: 14, display: "+14 units" }] }),
  Object.freeze({ label: "Unmet demand change", visualization_kind: "delta", exact_text: "Unmet demand: 18 to 21 units; visible change +3 units", source: "PlayerObservation.monthly_unmet_demand", values: [{ period: "Prior", value: 18, display: "18 units" }, { period: "Current", value: 21, display: "21 units" }] }),
  Object.freeze({ label: "Staffed beds", visualization_kind: "capacity-bar", value: 118, max: 160, exact_text: "Staffed beds: 118 of 160 beds", source: "PlayerObservation.staffed_beds" }),
  Object.freeze({ label: "Staffing composition", visualization_kind: "staffing-composition", exact_text: "Nurses 24; physicians 12; other staff unavailable", source: "PlayerObservation.staffing", values: [{ label: "Nurses", value: 24, display: "24" }, { label: "Physicians", value: 12, display: "12" }, { label: "Other staff", display: "Unavailable", status: "missing" }] }),
  Object.freeze({ label: "Capital project", visualization_kind: "project-progress", value: 3, max: 6, exact_text: "Capital project: 3 of 6 visible units; completion remains uncertain", source: "PlayerObservation.active_projects", status: "uncertain", uncertainty: "Completion timing remains uncertain." }),
  Object.freeze({ label: "Payer mix", visualization_kind: "payer-mix", exact_text: "Medicare 44%; Medicaid unavailable; commercial 31%", source: "PlayerObservation.payer_mix", values: [{ label: "Medicare", value: 44, display: "44%" }, { label: "Medicaid", display: "Unavailable", status: "missing" }, { label: "Commercial", value: 31, display: "31%" }] }),
  Object.freeze({ label: "Workforce trust", visualization_kind: "trust-trend", exact_text: "Workforce trust: moderate, moderate, high", source: "PlayerObservation.workforce_trust_summary", values: [{ period: "Jan", value: 1, display: "Moderate" }, { period: "Feb", value: 1, display: "Moderate" }, { period: "Mar", value: 2, display: "High" }] }),
  Object.freeze({ label: "Visible access interval", visualization_kind: "uncertainty-interval", lower: 62, estimate: 68, upper: 74, exact_text: "Visible access interval: 62–68–74 points", source: "PlayerObservation.access_interval", status: "uncertain", uncertainty: "Visible interval; not a probability." }),
]);

const FALLBACK = Object.freeze({
  id: "generic-metric",
  label: "Visible metric",
  semantic_purpose: "Show a host-supplied metric with written exact values.",
  precision_rule: "Preserve source precision.",
  uncertainty_rule: "Keep visible uncertainty text beside the metric.",
  missingness_rule: "Show unavailable when the source omits a value.",
  exact_text_rule: "Keep exact source text available.",
  color_independent_rule: "Use written labels and patterns.",
  large_text_rule: "Allow the written metric to reflow.",
  screenshot_fixture: "generic visible metric fallback",
});

const CATALOG_BY_ID = new Map(CATALOG.map((entry) => [entry.id, entry]));

function text(value, fallback = "Unavailable") {
  const normalized = String(value ?? "").trim();
  return normalized || fallback;
}

function finite(value) {
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

function escapeXml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

function normalizedValues(metric) {
  const supplied = Array.isArray(metric?.values)
    ? metric.values
    : metric?.value !== undefined
      ? [{ period: metric.period, value: metric.value, display: metric.value }]
      : [];
  return supplied.map((entry, index) => ({
    period: text(entry?.period, `Period ${index + 1}`),
    label: text(entry?.label, text(entry?.period, `Period ${index + 1}`)),
    value: finite(entry?.value),
    max: finite(entry?.max ?? metric?.max),
    display: text(entry?.display ?? entry?.value, "Unavailable"),
    status: text(entry?.status, entry?.value === undefined || finite(entry?.value) === null ? "missing" : "reported"),
    source: text(entry?.source ?? metric?.source, "Visible metric source unavailable"),
  }));
}

export function metricVisualizationFor(id) {
  return CATALOG_BY_ID.get(String(id ?? "").trim().toLowerCase()) ?? FALLBACK;
}

export function orderedMetricVisualizations() {
  return [...CATALOG].sort((left, right) => left.id.localeCompare(right.id));
}

export function metricVisualizationModel(metric = {}, kind = metric?.visualization_kind) {
  const contract = metricVisualizationFor(kind);
  const values = normalizedValues(metric);
  const lower = finite(metric?.lower);
  const estimate = finite(metric?.estimate ?? metric?.value);
  const upper = finite(metric?.upper);
  const missing = values.filter((entry) => entry.value === null);
  const suppliedText = values.length
    ? values.map((entry) => `${entry.period}: ${entry.display}`).join("; ")
    : text(metric?.value, "Unavailable");
  const exactText = text(metric?.exact_text, `${text(metric?.label, "Metric")}: ${suppliedText}`);
  const source = text(metric?.source, "Visible metric source unavailable");
  const status = text(metric?.status, missing.length ? "missing" : "reported");
  const uncertainty = text(metric?.uncertainty, contract.uncertainty_rule);
  return Object.freeze({
    schema_version: METRIC_VISUALIZATION_SCHEMA,
    id: contract.id,
    label: text(metric?.label, contract.label),
    values,
    lower,
    estimate,
    upper,
    source,
    status,
    uncertainty,
    missingness: text(metric?.missingness, missing.length ? `${missing.length} supplied period(s) missing.` : "No supplied periods are missing."),
    exact_text: exactText,
    accessible_text: `${exactText}. Status: ${status}. Source: ${source}.`,
    precision_rule: contract.precision_rule,
    color_independent_rule: contract.color_independent_rule,
    large_text_rule: contract.large_text_rule,
  });
}

function formatNumber(value) {
  return value === null ? "Unavailable" : String(value);
}

function pointsFor(values, width, height) {
  const numeric = values.map((entry) => entry.value).filter((value) => value !== null);
  if (numeric.length < 2) return "";
  const min = Math.min(...numeric);
  const max = Math.max(...numeric);
  const span = max - min || 1;
  const step = width / Math.max(values.length - 1, 1);
  return values
    .map((entry, index) => entry.value === null ? null : `${(index * step).toFixed(2)},${(height - ((entry.value - min) / span) * height).toFixed(2)}`)
    .filter(Boolean)
    .join(" ");
}

function svgText(x, y, value, className = "label") {
  return `<text class="${className}" x="${x}" y="${y}">${escapeXml(value)}</text>`;
}

function renderTrack(model) {
  const last = model.values.at(-1)?.value;
  const maximum = finite(model.values.at(-1)?.max);
  const ratio = last !== null && maximum > 0 ? Math.max(0, Math.min(1, last / maximum)) : null;
  return `<rect class="track" x="12" y="24" width="236" height="18" rx="3" />${ratio === null ? '<rect class="missing-pattern" x="12" y="24" width="236" height="18" rx="3" />' : `<rect class="value-pattern" x="12" y="24" width="${(236 * ratio).toFixed(2)}" height="18" rx="3" />`}`;
}

function renderComposition(model) {
  const numeric = model.values.map((entry) => entry.value ?? 0);
  const total = numeric.reduce((sum, value) => sum + value, 0);
  if (!total) return '<rect class="missing-pattern" x="12" y="24" width="236" height="18" rx="3" />';
  let offset = 12;
  return numeric.map((value, index) => {
    const width = 236 * value / total;
    const segment = `<rect class="segment-pattern segment-${index % 3}" x="${offset.toFixed(2)}" y="24" width="${width.toFixed(2)}" height="18" />`;
    offset += width;
    return segment;
  }).join("");
}

function renderUncertainty(model) {
  if (model.lower === null || model.estimate === null || model.upper === null) {
    return '<rect class="missing-pattern" x="12" y="30" width="236" height="6" rx="3" />';
  }
  const span = model.upper - model.lower || 1;
  const x = (value) => 12 + ((value - model.lower) / span) * 236;
  return `<line class="interval" x1="${x(model.lower).toFixed(2)}" y1="33" x2="${x(model.upper).toFixed(2)}" y2="33" /><line class="cap" x1="${x(model.lower).toFixed(2)}" y1="24" x2="${x(model.lower).toFixed(2)}" y2="42" /><line class="cap" x1="${x(model.upper).toFixed(2)}" y1="24" x2="${x(model.upper).toFixed(2)}" y2="42" /><circle class="estimate" cx="${x(model.estimate).toFixed(2)}" cy="33" r="5" />`;
}

export function renderMetricVisualizationSvg(metric = {}, kind = metric?.visualization_kind) {
  const contract = metricVisualizationFor(kind);
  const model = metricVisualizationModel(metric, kind);
  const title = `${model.label}: ${model.exact_text}`;
  const common = `<title>${escapeXml(title)}</title><desc>${escapeXml(model.accessible_text)}</desc>`;
  let graphic = "";
  if (contract.id === "sparkline" || contract.id === "trust-trend") {
    const points = pointsFor(model.values, 236, 30);
    graphic = points
      ? `<polyline class="trend-line" points="${points}" transform="translate(12 12)" />`
      : '<rect class="missing-pattern" x="12" y="24" width="236" height="18" rx="3" />';
  } else if (contract.id === "delta") {
    const previous = model.values.at(-2)?.value;
    const current = model.values.at(-1)?.value;
    const delta = previous !== null && current !== null ? current - previous : null;
    graphic = svgText(12, 38, delta === null ? "Delta unavailable" : `Visible change: ${delta > 0 ? "+" : ""}${formatNumber(delta)}`, "delta-label");
  } else if (contract.id === "uncertainty-interval") {
    graphic = renderUncertainty(model);
  } else if (contract.id === "staffing-composition" || contract.id === "payer-mix") {
    graphic = renderComposition(model);
  } else {
    graphic = renderTrack(model);
  }
  const exact = svgText(12, 62, model.exact_text, "exact-label");
  const status = svgText(12, 76, `${model.status} · ${model.source}`, "source-label");
  return `<svg xmlns="http://www.w3.org/2000/svg" class="metric-visual metric-visual--${escapeXml(contract.id)}" viewBox="0 0 260 86" role="img" aria-label="${escapeXml(model.accessible_text)}">${common}${graphic}${exact}${status}</svg>`;
}
