#!/usr/bin/env python3
"""Build and validate the v0.12.5 workforce-capacity design contract."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = Path(__file__).resolve().parent
ARTIFACT_TYPE = "workforce_capacity_difficulty_design_gate"
BATCH_ID = "v0.12.5-workforce-capacity-design"
CODE_VERSION = "0.12.5"

SAFE_TYPED_FIELDS = [
  "nurses",
  "physicians",
  "admins",
  "staffed_beds",
  "outpatient_capacity",
  "emergency_capacity",
  "icu_capacity",
  "obstetrics_capacity",
  "psychiatric_capacity",
  "cardiology_capacity",
  "oncology_capacity",
  "infusion_capacity",
  "neurology_capacity",
  "asc_capacity",
]
HIDDEN_FIELDS = [
  "role_targets",
  "effective_capacity",
  "allocation_queues",
  "pending_hire_outcomes",
  "rival_private_workforce_state",
  "future_actor_responses",
]
SOURCE_MARKERS = {
  "src/model/campaign.rs": [
    "pub nurses: i32",
    "pub staffed_beds: i32",
  ],
  "src/sim/observe_competitive.rs": [
    "workforce_trust_summary:",
    "nurses: human.nurses",
    "Labor market note: recruit commands",
  ],
  "src/mcp/session.rs": [
    "fn format_competitive_observation(",
    "Workforce trust:",
  ],
  "src/sim/transition_competitive.rs": [
    '"staffing capacity constraint"',
    "understaffing reduces operational capacity",
  ],
  "src/debrief/report.rs": [
    "Attributed mechanisms to inspect:",
    "Decision quality and outcome quality remain separate:",
  ],
}


def _source_contract():
  result = {}
  for relative_path, markers in SOURCE_MARKERS.items():
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    assert not missing, f"{relative_path} is missing markers: {missing}"
    result[relative_path] = {"markers": markers, "status": "supported"}
  return result


def build_design():
  return {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "candidate_signal": {
      "dimension": "workforce_capacity",
      "source_artifact": "_workspace/experiments/v0.12.4-difficulty-depth-evidence/results.json",
      "all_tier_counts": {
        "easy": 0,
        "normal": 15,
        "hard": 30,
        "expert": 160,
      },
      "interpretation": "descriptive operating-pressure signal, not causal difficulty evidence",
    },
    "current_visible_context": [
      "workforce_trust_summary",
      "nursing vacancy wording",
      "prior_month_operations",
      "labor_market_delay_and_cost_note",
      "state_conditioned_consultant_options",
      "staffing_events_and_attributed_debrief_mechanisms",
    ],
    "typed_fields_omitted_by_mcp": SAFE_TYPED_FIELDS,
    "observation_context_follow_up_required": True,
    "proposed_next_projection": {
      "source": "PlayerObservation",
      "lines": [
        "Staffing: nurses <n>, physicians <n>, admins <n>",
        "Physical capacity: staffed beds <n>, outpatient <n>, emergency <n>, ICU <n>, obstetrics <n>, psychiatric <n>, cardiology <n>, oncology <n>, infusion <n>, neurology <n>, ASC <n>",
      ],
      "purpose": "make the existing workforce-capacity decision context inspectable before commands",
      "not_a_new_mechanism": True,
    },
    "hidden_fields_excluded": HIDDEN_FIELDS,
    "preserved_contracts": [
      "deterministic transitions",
      "immutable history",
      "state hashes",
      "replay verification",
      "command grammar and legality",
      "competitive seed-42 golden path",
      "debrief attribution",
    ],
    "next_implementation_verification": [
      "focused MCP session-boundary test for exact safe labels and values",
      "rerun the v0.12.4 75-run/1800-transition compatible evidence matrix",
      "compare pre/post history and state hashes exactly",
      "keep runtime difficulty, balance, scoring, and winnability promotion deferred",
    ],
    "runtime_difficulty_change_authorized": False,
    "runtime_promotion": "deferred",
    "source_contract": _source_contract(),
    "evidence_limits": [
      "This is a design and observation-contract review, not human-learning evidence.",
      "The v0.12.4 signal is deterministic simulated-policy evidence, not causal balance or winnability evidence.",
      "Current typed fields are safe to project but their presence does not establish comprehension or educational effectiveness.",
    ],
  }


def validate_design(design):
  assert design["artifact_type"] == ARTIFACT_TYPE
  assert design["batch_id"] == BATCH_ID
  assert design["code_version"] == CODE_VERSION
  assert design["observation_context_follow_up_required"] is True
  assert design["runtime_difficulty_change_authorized"] is False
  assert design["runtime_promotion"] == "deferred"
  assert design["typed_fields_omitted_by_mcp"] == SAFE_TYPED_FIELDS
  assert not set(design["typed_fields_omitted_by_mcp"]) & set(design["hidden_fields_excluded"])
  assert design["proposed_next_projection"]["source"] == "PlayerObservation"
  assert design["proposed_next_projection"]["not_a_new_mechanism"] is True
  assert len(design["source_contract"]) == len(SOURCE_MARKERS)
  for contract in design["source_contract"].values():
    assert contract["status"] == "supported"


def render_markdown(design):
  signal = design["candidate_signal"]
  projection = design["proposed_next_projection"]
  lines = [
    "# Workforce Capacity Difficulty Design Gate v0.12.5",
    "",
    "- **Decision:** observation-context follow-up required",
    "- **Runtime difficulty change authorized:** no",
    "- **Runtime promotion:** deferred",
    "",
    "The v0.12.4 artifact identifies a workforce-capacity pressure signal, but "
    "the current MCP formatter omits safe typed staffing and physical-capacity "
    "fields from the decision-time observation.",
    "",
    "## Candidate signal",
    "",
    f"- Dimension: `{signal['dimension']}`",
    "- All-tier bottleneck counts: Easy 0, Normal 15, Hard 30, Expert 160.",
    "- Interpretation: descriptive operating-pressure signal, not causal "
    "difficulty, balance, or winnability evidence.",
    "",
    "## Proposed next projection",
    "",
    f"- Source: `{projection['source']}`",
  ]
  lines.extend(f"- `{line}`" for line in projection["lines"])
  lines.extend(
    [
      "",
      "These lines use only existing typed Riverside observation fields. They do "
      "not expose role targets, effective allocations, pending hire outcomes, "
      "rival private workforce state, or future actor responses.",
      "",
      "## Verification gate",
      "",
    ]
  )
  lines.extend(f"- {item}" for item in design["next_implementation_verification"])
  lines.extend(["", "## Evidence limits", ""])
  lines.extend(f"- {item}" for item in design["evidence_limits"])
  return "\n".join(lines) + "\n"


def main():
  design = build_design()
  validate_design(design)
  (OUTPUT_DIR / "design.json").write_text(
    json.dumps(design, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )
  (OUTPUT_DIR / "diagnostics.md").write_text(
    render_markdown(design),
    encoding="utf-8",
  )
  print("validated workforce-capacity design gate; observation follow-up required; runtime promotion deferred")


if __name__ == "__main__":
  main()
