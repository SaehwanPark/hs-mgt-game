#!/usr/bin/env python3
"""Build and validate the v0.12.7 affiliation runtime-boundary proposal."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = Path(__file__).resolve().parent
ARTIFACT_TYPE = "affiliation_runtime_boundary_proposal"
BATCH_ID = "v0.12.7-affiliation-runtime-boundary-proposal"
CODE_VERSION = "0.12.7"
CAMPAIGN = "regional-affiliation-v1"
EVIDENCE_PATH = "_workspace/experiments/v0.12.2-affiliation-observation-context/results.json"

SOURCE_MARKERS = {
  "docs/decision-records/0010-regional-affiliation-runtime-slice.md": [
    "**Status:** Implemented in v0.12.0",
    "true affiliation state",
    "explicit resolved inputs",
    "debrief output separating actor utility",
  ],
  "src/model/affiliation.rs": [
    "pub struct AffiliationWorldState",
    "pub struct AffiliationObservation",
    "pub struct AffiliationResolvedInputs",
    "pub struct AffiliationTransition",
    "pub struct AffiliationHistory",
    "pub struct AffiliationReplayArtifact",
  ],
  "src/affiliation/observe.rs": [
    "pub fn observe_affiliation",
    "alternatives",
    "assumptions",
  ],
  "src/inputs/resolve_affiliation.rs": [
    "pub fn resolve_affiliation_inputs(",
    "stream_rng",
  ],
  "src/affiliation/transition.rs": [
    "pub fn resolve_affiliation_turn(",
    "let inputs = resolve_affiliation_inputs",
    "pub fn replay_affiliation(",
  ],
  "src/artifact/affiliation.rs": [
    "pub fn serialize_affiliation_replay",
    "pub fn verify_affiliation_replay",
  ],
  "src/mcp/session.rs": [
    "fn format_affiliation_observation(",
    '"Commitments: community',
    'format!("Alternative: {alternative}")',
    'format!("Assumption: {assumption}")',
    "fn affiliation_legal_commands(",
  ],
  "src/debrief/report.rs": [
    "Regional affiliation debrief",
    "Actor utility and social welfare are separate",
    "Alternatives for discussion",
  ],
  "src/scenario/mod.rs": [
    "pub fn initial_affiliation_world_state",
    "pub fn validate_regional_affiliation_scenario",
  ],
  "scenarios/regional-affiliation-v1.toml": [
    'campaign_id = "regional-affiliation-v1"',
    "learning_objectives = [",
    "[affiliation]",
  ],
}

MINIMUM_CONTRACTS = {
  "true_state": [
    "scenario_id, stage, status, and turn",
    "Riverside cash, access, quality, workforce trust, community trust, and market share",
    "partner condition, fit, autonomy need, and continuity risk",
    "commitments, review state, integration progress, and actor response state",
  ],
  "actor_observation": [
    "reported partner condition and existing Riverside metrics",
    "commitment totals, review status, public labor/payer/community signals",
    "alternatives and visible assumptions at the MCP boundary",
  ],
  "resolved_inputs": [
    "partner report noise and partner response",
    "review, labor, payer, and community responses",
    "integration drag and continuity shock",
  ],
  "deterministic_core": [
    "resolve stochastic inputs before transition evaluation",
    "validate the stage-specific command against the prior snapshot",
    "apply one deterministic transition and compute a versioned state hash",
  ],
  "history_and_replay": [
    "retain prior state, command, observation, resolved inputs, actor decisions, effects, next state, and hash",
    "replay observations and resolved inputs against append-only transitions",
    "serialize and verify a versioned affiliation replay artifact",
  ],
  "debrief": [
    "report Riverside organizational outcomes separately from actor responses",
    "separate actor utility and social welfare",
    "invite comparison of independence and deferral alternatives",
  ],
}

DEFERRED_SCOPE = [
  "direct acquisition branch",
  "national consolidation or multi-deal market",
  "private-equity rollups",
  "detailed transaction financing",
  "calibrated legal or antitrust forecasts",
  "new generic actor framework",
  "changes to competitive-regional-v1",
]


def _source_contract():
  result = {}
  for relative_path, markers in SOURCE_MARKERS.items():
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    assert not missing, f"{relative_path} missing markers: {missing}"
    result[relative_path] = {"markers": markers, "status": "supported"}
  return result


def _evidence_contract():
  artifact = json.loads((ROOT / EVIDENCE_PATH).read_text(encoding="utf-8"))
  assert artifact["artifact_type"] == "regional-affiliation-observation-context"
  assert artifact["code_version"] == "0.12.2"
  assert artifact["campaign"] == CAMPAIGN
  assert artifact["runtime_promotion"] == "deferred"
  runs = artifact["runs"]
  assert len(runs) == 9
  assert sum(len(run["history"]) for run in runs) == 54
  observation_count = 0
  for run in runs:
    assert run["completion_status"] == "complete"
    assert not run["validation_failures"]
    assert len(run["turn_trace"]) == 6
    for entry in run["turn_trace"]:
      observation = entry["observation"]
      assert any(line.startswith("Commitments:") for line in observation)
      assert sum(line.startswith("Alternative:") for line in observation) >= 2
      assert sum(line.startswith("Assumption:") for line in observation) == 2
      observation_count += 1
  return {
    "path": EVIDENCE_PATH,
    "code_version": artifact["code_version"],
    "run_count": len(runs),
    "transition_count": sum(len(run["history"]) for run in runs),
    "observation_count": observation_count,
    "status": "supported",
  }


def build_proposal():
  return {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "campaign": CAMPAIGN,
    "implementation_status": "existing_opt_in_runtime_confirmed",
    "new_runtime_changes_authorized": False,
    "runtime_promotion": "deferred",
    "minimum_contracts": MINIMUM_CONTRACTS,
    "source_contract": _source_contract(),
    "evidence_contract": _evidence_contract(),
    "deferred_scope": DEFERRED_SCOPE,
    "decision": (
      "The existing regional-affiliation-v1 runtime satisfies the bounded "
      "state/observation/resolved-input/history/replay/debrief proposal. "
      "No additional runtime slice is authorized without a new concrete "
      "evidence gap."
    ),
    "evidence_limits": [
      "This is a source-boundary and deterministic trace review, not human-learning, classroom, calibration, legal-validity, or policy-forecast evidence.",
      "The 9-run/54-stage artifact supports contract coverage for named policies and seeds; it does not establish general balance, winnability, or social-welfare validity.",
      "Affiliation response and review outcomes are stylized game abstractions and must not be read as legal or antitrust predictions.",
    ],
  }


def validate_proposal(proposal):
  assert proposal["artifact_type"] == ARTIFACT_TYPE
  assert proposal["batch_id"] == BATCH_ID
  assert proposal["code_version"] == CODE_VERSION
  assert proposal["campaign"] == CAMPAIGN
  assert proposal["implementation_status"] == "existing_opt_in_runtime_confirmed"
  assert proposal["new_runtime_changes_authorized"] is False
  assert proposal["runtime_promotion"] == "deferred"
  assert len(proposal["minimum_contracts"]) == 6
  assert all(
    contract["status"] == "supported"
    for contract in proposal["source_contract"].values()
  )
  assert proposal["evidence_contract"]["run_count"] == 9
  assert proposal["evidence_contract"]["transition_count"] == 54
  assert proposal["evidence_contract"]["observation_count"] == 54
  assert proposal["deferred_scope"]


def render_markdown(proposal):
  evidence = proposal["evidence_contract"]
  lines = [
    "# Affiliation Runtime Boundary Proposal — v0.12.7",
    "",
    "- **Decision:** existing bounded runtime satisfies the proposal contract",
    "- **New runtime changes authorized:** no",
    "- **Runtime promotion:** deferred",
    "",
    "The opt-in `regional-affiliation-v1` runtime already implements the "
    "minimum contract required by the affiliation-first design gate. This "
    "version reconciles the proposal, source boundaries, and committed evidence; "
    "it does not add another affiliation mechanism.",
    "",
    "## Contract coverage",
    "",
    "| Contract | Status |",
    "| --- | --- |",
  ]
  for name in proposal["minimum_contracts"]:
    lines.append(f"| {name.replace('_', ' ').title()} | supported |")
  lines.extend([
    "",
    "## Evidence",
    "",
    f"- Source artifact: `{evidence['path']}` (code version `{evidence['code_version']}`).",
    f"- Complete runs: {evidence['run_count']}/9.",
    f"- Committed stages: {evidence['transition_count']}.",
    f"- Observations with typed commitments, alternatives, and assumptions: {evidence['observation_count']}.",
    "- Source-marker audit: all required state, observation, input, transition, replay, MCP, scenario, and debrief markers supported.",
    "",
    "## Boundary decision",
    "",
    "- The runtime remains an opt-in `regional-affiliation-v1` scenario and does not alter `competitive-regional-v1`.",
    "- Stochastic outcomes are resolved before deterministic transition evaluation and retained in append-only transitions.",
    "- The debrief distinguishes Riverside outcomes, actor responses, actor utility, social welfare, and decision quality.",
    "- Direct acquisition, deal finance, national markets, legal forecasts, and generic actor-framework expansion remain deferred.",
    "",
    "## Evidence limits",
    "",
  ])
  lines.extend(f"- {limit}" for limit in proposal["evidence_limits"])
  lines.append("")
  return "\n".join(lines)


def main():
  proposal = build_proposal()
  validate_proposal(proposal)
  (OUTPUT_DIR / "proposal.json").write_text(
    json.dumps(proposal, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )
  (OUTPUT_DIR / "diagnostics.md").write_text(
    render_markdown(proposal),
    encoding="utf-8",
  )
  print(f"Wrote proposal artifact to {OUTPUT_DIR / 'proposal.json'}")


if __name__ == "__main__":
  main()
