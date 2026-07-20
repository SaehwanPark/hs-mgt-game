#!/usr/bin/env python3
"""Close the already-supported competitive teachability queue item."""

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = Path(__file__).resolve().parent
SOURCE_PATH = (
  ROOT / "_workspace" / "experiments" / "v0.12.3-phase7-teachability-review"
)
AUDIT_SPEC = importlib.util.spec_from_file_location(
  "teachability_review_audit",
  SOURCE_PATH / "run_audit.py",
)
AUDIT = importlib.util.module_from_spec(AUDIT_SPEC)
assert AUDIT_SPEC.loader is not None
AUDIT_SPEC.loader.exec_module(AUDIT)


ARTIFACT_TYPE = "competitive_teachability_queue_closure"
BATCH_ID = "v0.12.8-teachability-queue-closure"
CODE_VERSION = "0.12.8"
SOURCE_BATCH_ID = "v0.12.3-phase7-teachability-review"

SOURCE_MARKERS = {
  "_workspace/experiments/v0.12.3-phase7-teachability-review/run_audit.py": [
    "REVIEW_STEPS = (",
    '"finding": "no_structural_gap"',
    'assert report["aggregate"]["gap_count"] == 0',
    'assert report["finding"] == "no_structural_gap"',
  ],
  "_workspace/experiments/v0.12.3-phase7-teachability-review/diagnostics.md": [
    "**Runs reviewed:** 18 of 18",
    "**Committed transitions reviewed:** 270",
    "No structural decision-to-debrief or source-context gap",
    "**Runtime promotion:** deferred",
  ],
  "docs/history/playtests/v0.12/playtest-findings-v0.12.3.md": [
    "## Promotion decision",
    "No structural player-facing, instructor-facing, or domain-review gap",
    "Runtime promotion remains deferred.",
  ],
}


def _source_marker_contract():
  result = {}
  for relative_path, markers in SOURCE_MARKERS.items():
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    assert not missing, f"{relative_path} missing markers: {missing}"
    result[relative_path] = {"markers": markers, "status": "supported"}
  return result


def _source_report():
  report = AUDIT.build_report()
  AUDIT.validate_report(report)
  return {
    "artifact_type": report["artifact_type"],
    "batch_id": report["batch_id"],
    "code_version": report["code_version"],
    "source_count": report["aggregate"]["source_count"],
    "run_count": report["aggregate"]["run_count"],
    "complete_run_count": report["aggregate"]["complete_run_count"],
    "transition_count": report["aggregate"]["transition_count"],
    "gap_count": report["aggregate"]["gap_count"],
    "finding": report["finding"],
    "runtime_promotion": report["runtime_promotion"],
    "sources": [
      {
        "source_id": source["source_id"],
        "source_code_version": source["source_code_version"],
        "campaign": source["campaign"],
        "run_count": source["run_count"],
        "complete_run_count": source["complete_run_count"],
        "transition_count": source["transition_count"],
        "status": source["status"],
        "coverage": {
          name: {
            "eligible_runs": coverage["eligible_runs"],
            "supported_runs": coverage["supported_runs"],
            "status": coverage["status"],
          }
          for name, coverage in source["coverage"].items()
        },
      }
      for source in report["sources"]
    ],
  }


def build_closure():
  return {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "source_batch_id": SOURCE_BATCH_ID,
    "closure_status": "complete_no_actionable_gap",
    "source_marker_contract": _source_marker_contract(),
    "source_report": _source_report(),
    "runtime_change_authorized": False,
    "runtime_promotion": "deferred",
    "queue_action": "remove_item_from_future_queue",
    "next_action": (
      "Wait for a new concrete comprehension, pacing, traceability, "
      "strategy-comparison, or debrief-use finding before opening another "
      "teachability slice."
    ),
    "evidence_limits": [
      "This is deterministic simulated-policy traceability evidence, not human or classroom evidence.",
      "No structural gap does not establish comprehension, debrief clarity, strategy quality, causality, balance, winnability, or optimality.",
      "The affiliation and competitive source lanes have different stage/month units and are audited with source-specific contracts.",
    ],
  }


def validate_closure(closure):
  assert closure["artifact_type"] == ARTIFACT_TYPE
  assert closure["batch_id"] == BATCH_ID
  assert closure["code_version"] == CODE_VERSION
  assert closure["source_batch_id"] == SOURCE_BATCH_ID
  assert closure["closure_status"] == "complete_no_actionable_gap"
  assert closure["runtime_change_authorized"] is False
  assert closure["runtime_promotion"] == "deferred"
  assert closure["queue_action"] == "remove_item_from_future_queue"
  report = closure["source_report"]
  assert report["source_count"] == 2
  assert report["run_count"] == 18
  assert report["complete_run_count"] == 18
  assert report["transition_count"] == 270
  assert report["gap_count"] == 0
  assert report["finding"] == "no_structural_gap"
  assert all(
    value["status"] == "supported"
    for value in closure["source_marker_contract"].values()
  )


def render_diagnostics(closure):
  report = closure["source_report"]
  lines = [
    "# Competitive Teachability Queue Closure — v0.12.8",
    "",
    "- **Closure status:** complete; no actionable structural gap",
    "- **Runtime change authorized:** no",
    "- **Runtime promotion:** deferred",
    "",
    "The v0.12.3 cross-campaign teachability review already satisfies the "
    "declared decision-context → action/response → transition → outcome → "
    "debrief chain with source-specific context contracts. This closure removes "
    "the completed item from the Future queue without inferring a human-learning "
    "or runtime-balance claim.",
    "",
    "## Evidence",
    "",
    f"- Sources: {report['source_count']}.",
    f"- Complete runs: {report['complete_run_count']}/{report['run_count']}.",
    f"- Committed transitions: {report['transition_count']}.",
    f"- Structural gaps: {report['gap_count']}.",
    "- Source-specific decision, response, transition, outcome, debrief, and context coverage: supported.",
    "",
    "## Queue decision",
    "",
    "Remove the competitive teachability and validation-loop item from the "
    "Future queue. Reopen it only when a concrete comprehension, pacing, "
    "traceability, strategy-comparison, or debrief-use finding is identified.",
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
