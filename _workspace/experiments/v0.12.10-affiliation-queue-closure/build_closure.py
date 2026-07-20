#!/usr/bin/env python3
"""Synchronize the completed affiliation queue item with its proposal evidence."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = Path(__file__).resolve().parent
ARTIFACT_TYPE = "affiliation_queue_closure"
BATCH_ID = "v0.12.10-affiliation-queue-closure"
CODE_VERSION = "0.12.10"
PROPOSAL_PATH = (
  "_workspace/experiments/v0.12.7-affiliation-runtime-boundary-proposal/proposal.json"
)

SOURCE_MARKERS = {
  "docs/history/milestones/affiliation-runtime-boundary-v0.12.7.md": [
    "The existing opt-in `regional-affiliation-v1` runtime already satisfies",
    "True state:",
    "Actor observation:",
    "Resolved inputs:",
    "History/replay:",
    "Deferred scope",
  ],
  "docs/decision-records/0010-regional-affiliation-runtime-slice.md": [
    "**Status:** Implemented in v0.12.0",
    "one localized",
    "Direct acquisition, national",
  ],
  "_workspace/experiments/v0.12.7-affiliation-runtime-boundary-proposal/diagnostics.md": [
    "existing bounded runtime satisfies the proposal contract",
    "Complete runs: 9/9.",
    "Committed stages: 54.",
    "New runtime changes authorized:** no",
  ],
}


def _markers():
  result = {}
  for relative_path, markers in SOURCE_MARKERS.items():
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    assert not missing, f"{relative_path} missing markers: {missing}"
    result[relative_path] = {"markers": markers, "status": "supported"}
  return result


def _proposal_summary():
  proposal = json.loads((ROOT / PROPOSAL_PATH).read_text(encoding="utf-8"))
  assert proposal["artifact_type"] == "affiliation_runtime_boundary_proposal"
  assert proposal["implementation_status"] == "existing_opt_in_runtime_confirmed"
  assert proposal["new_runtime_changes_authorized"] is False
  assert proposal["runtime_promotion"] == "deferred"
  assert len(proposal["minimum_contracts"]) == 6
  assert proposal["evidence_contract"]["run_count"] == 9
  assert proposal["evidence_contract"]["transition_count"] == 54
  assert proposal["evidence_contract"]["observation_count"] == 54
  assert all(
    value["status"] == "supported"
    for value in proposal["source_contract"].values()
  )
  return {
    "path": PROPOSAL_PATH,
    "source_code_version": proposal["code_version"],
    "implementation_status": proposal["implementation_status"],
    "minimum_contract_count": len(proposal["minimum_contracts"]),
    "run_count": proposal["evidence_contract"]["run_count"],
    "transition_count": proposal["evidence_contract"]["transition_count"],
    "observation_count": proposal["evidence_contract"]["observation_count"],
    "new_runtime_changes_authorized": proposal["new_runtime_changes_authorized"],
    "runtime_promotion": proposal["runtime_promotion"],
  }


def build_closure():
  return {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "closure_status": "complete_existing_runtime",
    "proposal": _proposal_summary(),
    "source_marker_contract": _markers(),
    "queue_action": "remove_item_from_future_queue",
    "runtime_change_authorized": False,
    "runtime_promotion": "deferred",
    "deferred_scope": [
      "direct acquisition branch",
      "national consolidation or multi-deal market",
      "private-equity rollups",
      "detailed transaction financing",
      "calibrated legal or antitrust forecasts",
      "generic actor-framework expansion",
      "changes to competitive-regional-v1",
    ],
    "next_action": (
      "Wait for new evidence identifying a concrete affiliation strategy, "
      "traceability, or educational gap before reopening this track."
    ),
    "evidence_limits": [
      "The proposal and artifact are deterministic source-boundary and trace evidence, not legal, antitrust, calibration, social-welfare, or human-learning evidence.",
      "The existing six-stage runtime is a bounded fictional affiliation abstraction, not a full acquisition simulator.",
    ],
  }


def validate_closure(closure):
  assert closure["artifact_type"] == ARTIFACT_TYPE
  assert closure["batch_id"] == BATCH_ID
  assert closure["code_version"] == CODE_VERSION
  assert closure["closure_status"] == "complete_existing_runtime"
  assert closure["queue_action"] == "remove_item_from_future_queue"
  assert closure["runtime_change_authorized"] is False
  assert closure["runtime_promotion"] == "deferred"
  proposal = closure["proposal"]
  assert proposal["minimum_contract_count"] == 6
  assert proposal["run_count"] == 9
  assert proposal["transition_count"] == 54
  assert proposal["observation_count"] == 54
  assert all(
    value["status"] == "supported"
    for value in closure["source_marker_contract"].values()
  )


def render_diagnostics(closure):
  proposal = closure["proposal"]
  lines = [
    "# Affiliation Queue Closure — v0.12.10",
    "",
    "- **Closure status:** complete; existing runtime satisfies the proposal",
    "- **New runtime change authorized:** no",
    "- **Runtime promotion:** deferred",
    "",
    "The v0.12.7 affiliation runtime-boundary proposal already reconciled the "
    "existing opt-in runtime with the minimum state, observation, resolved-input, "
    "history/replay, and debrief contracts. This cycle synchronizes the Future "
    "queue with that completed decision and adds no mechanism.",
    "",
    "## Evidence",
    "",
    f"- Proposal artifact: `{proposal['path']}`.",
    f"- Minimum contracts: {proposal['minimum_contract_count']}.",
    f"- Existing evidence: {proposal['run_count']}/9 runs and {proposal['transition_count']} stages.",
    f"- Typed observation context: {proposal['observation_count']} observations.",
    "- Source-marker audit: supported.",
    "",
    "## Queue decision",
    "",
    "Remove the affiliation/acquisition queue item. Keep broader acquisition, "
    "deal finance, legal forecasting, and generic actor expansion deferred.",
    "",
    "## Evidence limits",
    "",
  ]
  lines.extend(f"- {limit}" for limit in closure["evidence_limits"])
  lines.append("")
  return "\n".join(lines)


def main():
  closure = build_closure()
  validate_closure(closure)
  (OUTPUT_DIR / "closure.json").write_text(
    json.dumps(closure, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )
  (OUTPUT_DIR / "diagnostics.md").write_text(
    render_diagnostics(closure),
    encoding="utf-8",
  )
  print(f"Wrote closure artifact to {OUTPUT_DIR / 'closure.json'}")


if __name__ == "__main__":
  main()
