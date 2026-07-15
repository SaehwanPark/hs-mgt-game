const IDENTITIES = [
  {
    id: "riverside",
    label: "Riverside",
    symbol: "▣",
    token_class: "identity-riverside",
    source: "Visible system identity",
    equivalent: "Player system identity",
    matches: ["riverside"],
  },
  {
    id: "northlake",
    label: "Northlake",
    symbol: "◇",
    token_class: "identity-northlake",
    source: "Visible system identity",
    equivalent: "Public rival identity",
    matches: ["northlake"],
  },
  {
    id: "summit",
    label: "Summit",
    symbol: "◈",
    token_class: "identity-summit",
    source: "Visible system identity",
    equivalent: "Public rival identity",
    matches: ["summit"],
  },
  {
    id: "generic-institution",
    label: "Institution",
    symbol: "◆",
    token_class: "identity-generic",
    source: "Visible identity fallback",
    equivalent: "Institution identity unavailable",
    matches: [],
  },
];

const MARKERS = [
  ["facility", "Facility", "▥", "marker-facility", "Visible facility context", "Facility marker"],
  ["demand", "Demand", "⌁", "marker-demand", "Visible demand overlay", "Demand marker"],
  ["capacity", "Capacity", "▤", "marker-capacity", "Visible capacity overlay", "Capacity marker"],
  ["project", "Project", "◌", "marker-project", "Visible project process", "Project marker"],
  ["staffing", "Staffing", "♙", "marker-staffing", "Visible workforce context", "Staffing marker"],
  ["payer-policy", "Payer/policy", "⚖", "marker-payer-policy", "Visible payer or policy context", "Payer/policy marker"],
  ["timeline", "Timeline", "↳", "marker-timeline", "Visible process timing", "Timeline marker"],
  ["generic", "Visible information", "•", "marker-generic", "Visible category fallback", "Category marker unavailable"],
].map(([id, label, symbol, token_class, source, equivalent]) => ({
  id,
  label,
  symbol,
  token_class,
  source,
  equivalent,
}));

const STATUSES = [
  ["stable", "Stable", "●", "status-stable", "Visible status language"],
  ["watch", "Watch", "▲", "status-watch", "Visible status language"],
  ["constrained", "Constrained", "!", "status-constrained", "Visible status language"],
  ["critical", "Critical", "×", "status-critical", "Visible status language"],
  ["improving", "Improving", "↗", "status-improving", "Visible status language"],
  ["uncertain", "Uncertain", "?", "status-uncertain", "Visible status language"],
  ["delayed", "Delayed", "…", "status-delayed", "Visible status language"],
  ["revised", "Revised", "↻", "status-revised", "Visible status language"],
  ["reported", "Reported", "•", "status-reported", "Visible status language"],
].map(([id, label, symbol, token_class, source]) => ({
  id,
  label,
  symbol,
  token_class,
  source,
  equivalent: `${label} status text and symbol`,
}));

export const VISUAL_CATALOG = Object.freeze({
  schema_version: "visual-catalog-v1",
  identities: Object.freeze(IDENTITIES.map((entry) => Object.freeze({ ...entry }))),
  markers: Object.freeze(MARKERS.map((entry) => Object.freeze({ ...entry }))),
  statuses: Object.freeze(STATUSES.map((entry) => Object.freeze({ ...entry }))),
  third_party_assets: Object.freeze([]),
});

const identityById = new Map(IDENTITIES.map((entry) => [entry.id, entry]));
const markerById = new Map(MARKERS.map((entry) => [entry.id, entry]));
const statusById = new Map(STATUSES.map((entry) => [entry.id, entry]));

function normalized(value) {
  return String(value ?? "").trim().toLowerCase();
}

function visibleIdentityParts(value) {
  if (typeof value === "string") {
    const text = normalized(value);
    return { id: text, name: text };
  }
  return {
    id: normalized(value?.id),
    name: normalized(value?.name),
  };
}

export function visualIdentityFor(value = {}) {
  const { id, name } = visibleIdentityParts(value);
  for (const entry of IDENTITIES) {
    if (id === entry.id) return entry;
    if (entry.matches.some((match) => new RegExp(`\\b${match}\\b`).test(name))) return entry;
  }
  return identityById.get("generic-institution");
}

export function visualMarkerFor(value = {}) {
  const text = typeof value === "string"
    ? normalized(value)
    : normalized(`${value?.id ?? ""} ${value?.marker ?? ""} ${value?.kind ?? ""} ${value?.label ?? ""}`);
  if (!text) return markerById.get("generic");
  const patterns = [
    ["payer-policy", /payer|policy|regulat/],
    ["staffing", /staff|nurs|workforce|vacanc/],
    ["capacity", /capacity|bed|volume/],
    ["demand", /demand|access|unmet/],
    ["project", /project|capital|technology|construction/],
    ["timeline", /timeline|pending|delay|milestone|process/],
    ["facility", /facility|inpatient|outpatient|clinic|hospital/],
  ];
  for (const [id, pattern] of patterns) {
    if (pattern.test(text)) return markerById.get(id);
  }
  return markerById.get("generic");
}

export function visualStatusFor(value = {}) {
  const text = normalized(typeof value === "string" ? value : value?.id ?? value?.status);
  return statusById.get(text) ?? null;
}
