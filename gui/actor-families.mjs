const FAMILY_DEFINITIONS = [
  {
    id: "payer",
    label: "Payer",
    monogram: "PY",
    glyph: "P",
    icon_shape: "hexagon",
    report_frame: "ledger",
    notification_style: "claim",
    sonic_tag: "identity-payer-pulse",
    source: "Visible payer actor-family ID",
    equivalent: "Payer label, P marker, ledger frame, and written notification",
  },
  {
    id: "regulator",
    label: "Regulator",
    monogram: "RG",
    glyph: "R",
    icon_shape: "shield",
    report_frame: "docket",
    notification_style: "directive",
    sonic_tag: "identity-regulator-ping",
    source: "Visible regulator actor-family ID",
    equivalent: "Regulator label, R marker, docket frame, and written notification",
  },
  {
    id: "labor",
    label: "Labor",
    monogram: "LB",
    glyph: "L",
    icon_shape: "stripe",
    report_frame: "agreement",
    notification_style: "workforce",
    sonic_tag: "identity-labor-tick",
    source: "Visible labor actor-family ID",
    equivalent: "Labor label, L marker, agreement frame, and written notification",
  },
  {
    id: "employer",
    label: "Employer",
    monogram: "ER",
    glyph: "E",
    icon_shape: "square",
    report_frame: "brief",
    notification_style: "market",
    sonic_tag: "identity-employer-chime",
    source: "Visible employer actor-family ID",
    equivalent: "Employer label, E marker, brief frame, and written notification",
  },
  {
    id: "community",
    label: "Community",
    monogram: "CM",
    glyph: "C",
    icon_shape: "circle",
    report_frame: "listening",
    notification_style: "community",
    sonic_tag: "identity-community-tone",
    source: "Visible community actor-family ID",
    equivalent: "Community label, C marker, listening frame, and written notification",
  },
  {
    id: "board",
    label: "Board",
    monogram: "BD",
    glyph: "B",
    icon_shape: "diamond",
    report_frame: "minutes",
    notification_style: "governance",
    sonic_tag: "identity-board-chord",
    source: "Visible board actor-family ID",
    equivalent: "Board label, B marker, minutes frame, and written notification",
  },
  {
    id: "policy-coalition",
    label: "Policy coalition",
    monogram: "PC",
    glyph: "PC",
    icon_shape: "double-ring",
    report_frame: "coalition",
    notification_style: "coalition",
    sonic_tag: "identity-coalition-layer",
    source: "Visible policy-coalition actor-family ID",
    equivalent: "Policy-coalition label, PC marker, coalition frame, and written notification",
  },
  {
    id: "independent-provider",
    label: "Independent provider",
    monogram: "IP",
    glyph: "IP",
    icon_shape: "triangle",
    report_frame: "practice",
    notification_style: "clinical",
    sonic_tag: "identity-provider-note",
    source: "Visible independent-provider actor-family ID",
    equivalent: "Independent-provider label, IP marker, practice frame, and written notification",
  },
];

const GENERIC_ACTOR_FAMILY = Object.freeze({
  id: "generic-actor",
  label: "Actor",
  monogram: "??",
  glyph: "?",
  icon_shape: "fallback",
  report_frame: "generic",
  notification_style: "generic",
  sonic_tag: null,
  source: "Missing or unknown actor-family ID",
  equivalent: "Actor label, generic marker, neutral frame, and written notification",
});

export const ACTOR_FAMILIES = Object.freeze(
  FAMILY_DEFINITIONS.map((family) => Object.freeze(family)),
);

const ACTOR_FAMILY_BY_ID = new Map(ACTOR_FAMILIES.map((family) => [family.id, family]));

export function actorFamilyFor(id) {
  return ACTOR_FAMILY_BY_ID.get(id) ?? GENERIC_ACTOR_FAMILY;
}

export function actorFamilySummary(id = "payer") {
  const family = actorFamilyFor(id);
  return {
    id: family.id,
    label: family.label,
    monogram: family.monogram,
    glyph: family.glyph,
    icon_shape: family.icon_shape,
    report_frame: family.report_frame,
    notification_style: family.notification_style,
    sonic_tag: family.sonic_tag,
    source: family.source,
    equivalent: family.equivalent,
  };
}
