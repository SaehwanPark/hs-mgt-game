#!/usr/bin/env python3
"""Audit Phase 7 decision-to-debrief coherence across committed artifacts."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = Path(__file__).resolve().parent
ARTIFACT_TYPE = "phase7_teachability_review"
BATCH_ID = "v0.12.3-phase7-teachability-review"
CODE_VERSION = "0.12.3"

REVIEW_STEPS = (
  ("decision_context", "actor-visible observation, legal commands, submitted command"),
  ("action_response", "validation and safe response records"),
  ("transition_follow_through", "accepted transition and state-hash alignment"),
  ("outcome_context", "complete history, final hash, and completion"),
  ("debrief_explanation", "source-specific retrospective explanation markers"),
  ("strategy_comparison", "declared profile and seed matrix remains identifiable"),
)

LIMITATIONS = [
  "This is deterministic simulated-policy traceability evidence, not human or classroom evidence.",
  "Supported observation and debrief markers do not establish comprehension, clarity, strategy quality, causality, balance, winnability, or optimality.",
  "Cross-campaign coverage is structural; affiliation stages and competitive months are not interchangeable units.",
  "Source-specific actor responses, legal abstractions, and policy mechanisms remain design abstractions.",
]

SOURCE_CONTRACTS = {
  "affiliation": {
    "path": "_workspace/experiments/v0.12.2-affiliation-observation-context/results.json",
    "artifact_type": "regional-affiliation-observation-context",
    "batch_id": "v0.12.2-affiliation-observation-context",
    "source_code_version": "0.12.2",
    "campaign": "regional-affiliation-v1",
    "difficulty": None,
    "profiles": ["independent", "deferred", "pursuit"],
    "seeds": [42, 43, 44],
    "transitions_per_run": 6,
    "context_name": "commitments, alternatives, assumptions",
    "debrief_markers": (
      "decision quality:",
      "actor utility and social welfare are separate:",
      "alternatives for discussion:",
    ),
  },
  "competitive": {
    "path": "_workspace/experiments/v0.11.12-phase7-current-code-teachability-capture/results.json",
    "artifact_type": "current_code_teachability_capture",
    "batch_id": "v0.11.12-phase7-current-code-teachability-capture",
    "source_code_version": "0.11.12",
    "campaign": "competitive-regional-v1",
    "difficulty": "hard",
    "profiles": [
      "fiscal_steward",
      "access_expansion_advocate",
      "first_time_executive",
    ],
    "seeds": [42, 43, 44],
    "transitions_per_run": 24,
    "context_name": "consultant options and advisory comparison",
    "debrief_markers": (
      "decision quality and outcome quality remain separate:",
      "attributed mechanisms to inspect:",
      "=== decision quality evaluation ===",
    ),
  },
}


def load_artifact(path):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def _text(values):
  return "\n".join(str(value) for value in values).casefold()


def _turn_entries(run):
  if not isinstance(run, dict):
    return []
  trace = run.get("turn_trace")
  return trace if isinstance(trace, list) else []


def _observation(entry):
  value = entry.get("observation") if isinstance(entry, dict) else None
  return value if isinstance(value, list) else []


def _history(run):
  value = run.get("history") if isinstance(run, dict) else None
  return value if isinstance(value, list) else []


def _source_context_ok(source_id, entry):
  lines = _observation(entry)
  if source_id == "affiliation":
    commitment_lines = [line for line in lines if str(line).startswith("Commitments:")]
    alternative_lines = [line for line in lines if str(line).startswith("Alternative:")]
    assumption_lines = [line for line in lines if str(line).startswith("Assumption:")]
    return (
      len(commitment_lines) == 1
      and len(alternative_lines) >= 2
      and len(assumption_lines) == 2
    )

  option_lines = [line for line in lines if str(line).startswith("Option ")]
  tradeoff_lines = [line for line in lines if str(line).startswith("  Tradeoff:")]
  return len(option_lines) >= 4 and len(tradeoff_lines) >= 4


def _debrief_ok(source_id, run, contract):
  debrief = run.get("debrief") if isinstance(run, dict) else None
  if not isinstance(debrief, list) or not debrief:
    return False
  text = _text(debrief)
  return all(marker in text for marker in contract["debrief_markers"])


def _step_status(present):
  return "supported" if present else "limited"


def _run_report(source_id, run, contract, index):
  issues = []
  entries = _turn_entries(run)
  history = _history(run)
  history_hashes = [
    item.get("state_hash")
    for item in history
    if isinstance(item, dict)
  ]

  decision_context = bool(entries)
  action_response = bool(entries)
  transition_follow_through = bool(entries)
  context_supported = bool(entries)

  if not isinstance(run, dict):
    issues.append("run is not an object")
    decision_context = False
    action_response = False
    transition_follow_through = False
    context_supported = False
  else:
    if len(entries) != contract["transitions_per_run"]:
      issues.append("turn_trace count does not match the source contract")
    if len(history) != contract["transitions_per_run"]:
      issues.append("history count does not match the source contract")
    if run.get("completion_status") != "complete":
      issues.append("completion_status is not complete")

    for entry_index, entry in enumerate(entries):
      if not isinstance(entry, dict):
        issues.append(f"turn_trace entry {entry_index + 1} is malformed")
        decision_context = False
        action_response = False
        transition_follow_through = False
        context_supported = False
        continue

      required = {
        "turn",
        "observation",
        "legal_commands",
        "submitted_command",
        "validation_failures",
        "latest_transition",
        "done_after_submit",
      }
      if not required <= set(entry):
        issues.append(f"turn_trace entry {entry_index + 1} is missing fields")
        decision_context = False
        action_response = False

      if not isinstance(entry.get("observation"), list) or not entry.get("observation"):
        issues.append(f"turn_trace entry {entry_index + 1} has no observation")
        decision_context = False
      if not isinstance(entry.get("legal_commands"), list) or not entry.get("legal_commands"):
        issues.append(f"turn_trace entry {entry_index + 1} has no legal command surface")
        decision_context = False
      if not isinstance(entry.get("submitted_command"), str) or not entry.get("submitted_command"):
        issues.append(f"turn_trace entry {entry_index + 1} has no submitted command")
        decision_context = False
      failures = entry.get("validation_failures")
      if not isinstance(failures, list):
        issues.append(f"turn_trace entry {entry_index + 1} has malformed validation failures")
        action_response = False
      elif failures and not isinstance(entry.get("retry_commands"), list):
        issues.append(f"turn_trace entry {entry_index + 1} has no retry record")
        action_response = False

      transition = entry.get("latest_transition")
      if not isinstance(transition, dict) or not transition.get("state_hash"):
        issues.append(f"turn_trace entry {entry_index + 1} has no transition hash")
        transition_follow_through = False
      elif entry_index >= len(history_hashes):
        issues.append(f"turn_trace entry {entry_index + 1} has no history transition")
        transition_follow_through = False
      elif transition.get("state_hash") != history_hashes[entry_index]:
        issues.append(f"turn_trace entry {entry_index + 1} hash is out of alignment")
        transition_follow_through = False

      if not _source_context_ok(source_id, entry):
        context_supported = False
        issues.append(
          f"turn_trace entry {entry_index + 1} is missing {contract['context_name']}"
        )

    if [entry.get("turn") for entry in entries if isinstance(entry, dict)] != list(
      range(1, contract["transitions_per_run"] + 1)
    ):
      issues.append("turn_trace turns are not contiguous")
      decision_context = False

  outcome_context = (
    isinstance(run, dict)
    and run.get("completion_status") == "complete"
    and len(history) == contract["transitions_per_run"]
    and run.get("state_hashes") == history_hashes
    and bool(history_hashes)
    and run.get("final_hash") == history_hashes[-1]
  )
  if not outcome_context:
    issues.append("outcome, history, or state-hash contract is incomplete")

  debrief_explanation = _debrief_ok(source_id, run, contract)
  if not debrief_explanation:
    issues.append("debrief is missing source-specific explanation markers")

  return {
    "index": index,
    "profile_id": run.get("profile_id") if isinstance(run, dict) else None,
    "profile_name": run.get("profile_name") if isinstance(run, dict) else None,
    "seed": run.get("seed") if isinstance(run, dict) else None,
    "completion_status": run.get("completion_status") if isinstance(run, dict) else None,
    "transition_count": len(history),
    "steps": {
      "decision_context": _step_status(decision_context),
      "action_response": _step_status(action_response),
      "transition_follow_through": _step_status(transition_follow_through),
      "outcome_context": _step_status(outcome_context),
      "debrief_explanation": _step_status(debrief_explanation),
      "context": _step_status(context_supported),
    },
    "issues": sorted(set(issues)),
    "status": "supported" if not issues else "limited",
  }


def _expected_matrix(contract):
  return {
    (profile, seed)
    for profile in contract["profiles"]
    for seed in contract["seeds"]
  }


def audit_source(source_id, artifact, contract):
  issues = []
  if not isinstance(artifact, dict):
    raise AssertionError(f"{source_id}: artifact is not an object")

  identity_issues = []
  expected_identity = {
    "artifact_type": contract["artifact_type"],
    "batch_id": contract["batch_id"],
    "code_version": contract["source_code_version"],
    "campaign": contract["campaign"],
    "difficulty": contract["difficulty"],
    "profiles": contract["profiles"],
    "seeds": contract["seeds"],
  }
  for key, expected in expected_identity.items():
    if artifact.get(key) != expected:
      identity_issues.append(f"{key} does not match the pinned source contract")
  if identity_issues:
    raise AssertionError(f"{source_id}: {'; '.join(identity_issues)}")
  if artifact.get("runtime_promotion") != "deferred":
    issues.append("runtime_promotion is not deferred")

  runs = artifact.get("runs")
  if not isinstance(runs, list):
    raise AssertionError(f"{source_id}: runs is not a list")
  expected_matrix = _expected_matrix(contract)
  actual_matrix = {
    (run.get("profile_id"), run.get("seed"))
    for run in runs
    if isinstance(run, dict)
  }
  if actual_matrix != expected_matrix:
    issues.append("profile/seed matrix does not match the pinned source contract")

  run_reports = [
    _run_report(source_id, run, contract, index)
    for index, run in enumerate(runs)
  ]
  issues.extend(issue for report in run_reports for issue in report["issues"])

  coverage = {}
  for step_name, description in REVIEW_STEPS:
    if step_name == "strategy_comparison":
      supported = actual_matrix == expected_matrix and len(runs) == len(expected_matrix)
      coverage[step_name] = {
        "description": description,
        "eligible_runs": len(runs),
        "supported_runs": len(runs) if supported else 0,
        "status": _step_status(supported),
      }
      if not supported:
        issues.append("strategy profile/seed comparison coverage is incomplete")
      continue

    supported_runs = sum(
      report["steps"].get(step_name) == "supported"
      for report in run_reports
    )
    coverage[step_name] = {
      "description": description,
      "eligible_runs": len(run_reports),
      "supported_runs": supported_runs,
      "status": _step_status(supported_runs == len(run_reports) and bool(run_reports)),
    }

  if source_id == "competitive":
    control = artifact.get("control", {})
    if control.get("first_transition_hash") != "61357596d8800592":
      issues.append("competitive control hash does not match the pinned golden boundary")
  else:
    control = None

  return {
    "source_id": source_id,
    "source_path": contract["path"],
    "source_code_version": contract["source_code_version"],
    "campaign": contract["campaign"],
    "difficulty": contract["difficulty"],
    "profiles": contract["profiles"],
    "seeds": contract["seeds"],
    "context_contract": contract["context_name"],
    "run_count": len(runs),
    "complete_run_count": sum(
      report["completion_status"] == "complete" for report in run_reports
    ),
    "transition_count": sum(report["transition_count"] for report in run_reports),
    "control": control,
    "coverage": coverage,
    "runs": run_reports,
    "issues": sorted(set(issues)),
    "status": "supported" if not issues else "limited",
  }


def build_report(artifacts=None):
  artifacts = artifacts or {
    source_id: load_artifact(ROOT / contract["path"])
    for source_id, contract in SOURCE_CONTRACTS.items()
  }
  sources = [
    audit_source(source_id, artifacts[source_id], contract)
    for source_id, contract in SOURCE_CONTRACTS.items()
  ]
  gaps = [
    {
      "source_id": source["source_id"],
      "issue": issue,
    }
    for source in sources
    for issue in source["issues"]
  ]
  return {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "source_artifacts": [source["source_path"] for source in sources],
    "review_steps": [
      {"name": name, "description": description}
      for name, description in REVIEW_STEPS
    ],
    "sources": sources,
    "aggregate": {
      "source_count": len(sources),
      "run_count": sum(source["run_count"] for source in sources),
      "complete_run_count": sum(source["complete_run_count"] for source in sources),
      "transition_count": sum(source["transition_count"] for source in sources),
      "gap_count": len(gaps),
      "gaps": gaps,
    },
    "finding": "no_structural_gap" if not gaps else "structural_gap",
    "runtime_promotion": "deferred",
    "evidence_limits": LIMITATIONS,
  }


def validate_report(report):
  assert report["artifact_type"] == ARTIFACT_TYPE
  assert report["batch_id"] == BATCH_ID
  assert report["code_version"] == CODE_VERSION
  assert report["aggregate"]["source_count"] == 2
  assert report["aggregate"]["run_count"] == 18
  assert report["aggregate"]["complete_run_count"] == 18
  assert report["aggregate"]["transition_count"] == 270
  assert report["aggregate"]["gap_count"] == 0
  assert report["finding"] == "no_structural_gap"
  assert report["runtime_promotion"] == "deferred"
  for source in report["sources"]:
    assert source["status"] == "supported"
    assert source["complete_run_count"] == source["run_count"] == 9
    for coverage in source["coverage"].values():
      assert coverage["status"] == "supported"
      assert coverage["supported_runs"] == coverage["eligible_runs"]


def render_markdown(report):
  lines = [
    "# Phase 7 Teachability Evidence Review v0.12.3",
    "",
    "- **Status:** supported",
    "- **Source artifacts:** 2",
    f"- **Runs reviewed:** {report['aggregate']['complete_run_count']} of {report['aggregate']['run_count']}",
    f"- **Committed transitions reviewed:** {report['aggregate']['transition_count']}",
    "- **Runtime promotion:** deferred",
    "",
    "This deterministic read-only audit checks the decision-context → "
    "action/response → transition → outcome → debrief chain while preserving "
    "source-specific context contracts.",
    "",
    "## Coverage",
    "",
    "| Source | Version | Campaign | Runs | Transitions | Decision | Response | Transition | Outcome | Debrief | Context | Matrix | Status |",
    "| --- | --- | --- | ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- |",
  ]
  for source in report["sources"]:
    coverage = source["coverage"]
    values = [
      source["source_id"],
      source["source_code_version"],
      source["campaign"],
      str(source["run_count"]),
      str(source["transition_count"]),
      coverage["decision_context"]["status"],
      coverage["action_response"]["status"],
      coverage["transition_follow_through"]["status"],
      coverage["outcome_context"]["status"],
      coverage["debrief_explanation"]["status"],
      "supported" if source["status"] == "supported" else "limited",
      coverage["strategy_comparison"]["status"],
      source["status"],
    ]
    lines.append("| " + " | ".join(values) + " |")

  lines.extend(
    [
      "",
      "## Finding",
      "",
      "No structural decision-to-debrief or source-context gap was identified "
      "in the reviewed artifacts. This supports continued evidence-only work; "
      "it does not justify runtime balance or transition promotion.",
      "",
      "## Evidence limits",
      "",
    ]
  )
  lines.extend(f"- {limitation}" for limitation in report["evidence_limits"])
  return "\n".join(lines) + "\n"


def main():
  report = build_report()
  validate_report(report)
  (OUTPUT_DIR / "results.json").write_text(
    json.dumps(report, indent=2) + "\n",
    encoding="utf-8",
  )
  (OUTPUT_DIR / "diagnostics.md").write_text(
    render_markdown(report),
    encoding="utf-8",
  )
  print(
    "validated 2 sources, 18 runs, 270 transitions, "
    "zero structural gaps; runtime promotion deferred"
  )


if __name__ == "__main__":
  main()
