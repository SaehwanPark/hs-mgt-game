const DEFAULTS = Object.freeze({
  schema_version: "semantic-container-v1",
  grid: "shared executive desktop grid",
  large_text_behavior: "Text reflows; labels and exact values remain visible.",
  narrow_width_behavior: "Header stacks above content; no information is hidden.",
  print_behavior: "Borders, labels, source/status text, and section headings remain printable.",
  source_status_rule: "Preserve visible source and status language; never add hidden severity.",
  reduced_motion: "Static; no transition is required for comprehension.",
});

const CONTAINERS = [
  {
    id: "board-packet",
    label: "Board packet",
    semantic_purpose: "Orient the player to the current actor-visible regional board.",
    icon: "▣",
    marker_pattern: "double-rule header",
    header_treatment: "Dark board header with period and source context.",
    compact_variant: "Two-line header with board title and current period.",
    expanded_variant: "Header, board scene, entity list, overlays, and linked consequences.",
    aria_label: "Board packet: actor-visible regional strategy board",
  },
  {
    id: "operations-ledger",
    label: "Operations ledger",
    semantic_purpose: "Show current operating commitments, resources, and visible status.",
    icon: "▤",
    marker_pattern: "ledger rule",
    header_treatment: "Tabular heading with period and host-reported status.",
    compact_variant: "Metric heading plus one visible status line.",
    expanded_variant: "Metric rows, exact values, source labels, and pending commitments.",
    aria_label: "Operations ledger: visible operating status and commitments",
  },
  {
    id: "intelligence-report",
    label: "Intelligence report",
    semantic_purpose: "Separate public signals and information gaps from owned detail.",
    icon: "◇",
    marker_pattern: "dotted signal rule",
    header_treatment: "Signal header with source and observation timing.",
    compact_variant: "Signal title, status token, and source line.",
    expanded_variant: "Briefing entries with written evidence, target links, and gaps.",
    aria_label: "Intelligence report: public signals and information gaps",
  },
  {
    id: "regulatory-letter",
    label: "Regulatory letter",
    semantic_purpose: "Present policy or oversight language as a bounded written notice.",
    icon: "⚖",
    marker_pattern: "formal side rule",
    header_treatment: "Formal notice header with actor family and visible source.",
    compact_variant: "Notice title, actor marker, and status.",
    expanded_variant: "Notice body, source, exact visible terms, and explicit uncertainty.",
    aria_label: "Regulatory letter: visible policy and oversight notice",
  },
  {
    id: "project-sheet",
    label: "Project sheet",
    semantic_purpose: "Track host-reported project commitments without promising outcomes.",
    icon: "◌",
    marker_pattern: "dashed process rule",
    header_treatment: "Process header with timing and source language.",
    compact_variant: "Project label, timing, and status token.",
    expanded_variant: "Process detail, visible milestones, pending effects, and source.",
    aria_label: "Project sheet: visible project commitments and timing",
  },
  {
    id: "news-wire",
    label: "News wire",
    semantic_purpose: "Group public market or community reports as dated visible signals.",
    icon: "↯",
    marker_pattern: "single signal rule",
    header_treatment: "News header with date/observed period and source.",
    compact_variant: "Headline, signal marker, and observed period.",
    expanded_variant: "Headlines, written equivalents, source labels, and missingness notes.",
    aria_label: "News wire: dated public market and community signals",
  },
  {
    id: "executive-action-queue",
    label: "Executive action queue",
    semantic_purpose: "Present host-catalogued decisions and local draft state.",
    icon: "▶",
    marker_pattern: "action bracket",
    header_treatment: "Action header with validation state and resource context.",
    compact_variant: "Action label, cost/context, and validation status.",
    expanded_variant: "Host fields, draft rows, validation result, and recoverable errors.",
    aria_label: "Executive action queue: host-catalogued decisions",
  },
  {
    id: "after-action-report",
    label: "After-action report",
    semantic_purpose: "Explain committed consequences and retrospective evidence.",
    icon: "↻",
    marker_pattern: "conclusion rule",
    header_treatment: "Result header with committed turn and state hash.",
    compact_variant: "Result headline, status, and hash/source line.",
    expanded_variant: "Resolution steps, before/after values, effects, history, and debrief.",
    aria_label: "After-action report: committed resolution and retrospective evidence",
  },
].map((entry) => Object.freeze({ ...DEFAULTS, ...entry }));

const FALLBACK = Object.freeze({
  ...DEFAULTS,
  id: "generic-container",
  label: "Information panel",
  semantic_purpose: "Visible information panel with generic structure.",
  icon: "•",
  marker_pattern: "single rule",
  header_treatment: "Shared heading and source/status line.",
  compact_variant: "Heading and visible summary.",
  expanded_variant: "Heading, text, source, and status.",
  aria_label: "Information panel",
});

const CONTAINER_BY_ID = new Map(CONTAINERS.map((entry) => [entry.id, entry]));

export const SEMANTIC_CONTAINER_CATALOG = Object.freeze({
  schema_version: "semantic-container-catalog-v1",
  containers: Object.freeze(CONTAINERS),
  fallback: FALLBACK,
});

export function semanticContainerFor(id) {
  return CONTAINER_BY_ID.get(String(id ?? "").trim().toLowerCase()) ?? FALLBACK;
}

export function semanticContainerClass(id) {
  return `semantic-container--${semanticContainerFor(id).id}`;
}

export function orderedSemanticContainers() {
  return [...CONTAINERS].sort((left, right) => left.id.localeCompare(right.id));
}
