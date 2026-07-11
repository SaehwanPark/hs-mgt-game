#!/usr/bin/env python3
"""Audit decision-to-debrief coherence across existing Phase 7 artifacts."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BATCH_ID = "v0.10.58-debrief-coherence-audit"
CODE_VERSION = "0.10.58"
CAMPAIGN = "competitive-regional-v1"

SOURCE_CONTRACTS = {
  "v0.10.43-rival-info-follow-through": {
    "batch_id": "v0.10.43-rival-info-follow-through",
    "path": "_workspace/experiments/v0.10.43-rival-info-follow-through/results.json",
    "lane": "rival-pressure",
    "context": "partial",
    "debrief_markers": (
      "final player tradeoff:",
      "attributed mechanisms to inspect:",
      "decision quality and outcome quality remain separate:",
      "=== decision quality evaluation ===",
    ),
  },
  "v0.10.50-teachability-observation-capture": {
    "batch_id": "v0.10.50-teachability-observation-capture",
    "path": "_workspace/experiments/v0.10.50-teachability-observation-capture/results.json",
    "lane": "strategy-tradeoff",
    "context": "not_applicable",
    "debrief_markers": (
      "final player tradeoff:",
      "attributed mechanisms to inspect:",
      "decision quality and outcome quality remain separate:",
      "=== decision quality evaluation ===",
    ),
  },
  "v0.10.51-adversarial-resource-probe": {
    "batch_id": "v0.10.51-adversarial-resource-probe",
    "path": "_workspace/experiments/v0.10.51-adversarial-resource-probe/results.json",
    "lane": "resource-retry",
    "context": "not_applicable",
    "debrief_markers": (
      "final player tradeoff:",
      "attributed mechanisms to inspect:",
      "decision quality and outcome quality remain separate:",
      "=== decision quality evaluation ===",
    ),
  },
  "v0.10.54-project-limit-recovery": {
    "batch_id": "v0.10.54-project-limit-recovery",
    "path": "_workspace/experiments/v0.10.54-project-limit-recovery/results.json",
    "lane": "project-recovery",
    "context": "delayed",
    "debrief_markers": (
      "final player tradeoff:",
      "attributed mechanisms to inspect:",
      "decision quality and outcome quality remain separate:",
      "=== decision quality evaluation ===",
    ),
  },
  "v0.10.55-asc-project-observation": {
    "batch_id": "v0.10.55-asc-project-observation",
    "path": "_workspace/experiments/v0.10.55-asc-project-observation/results.json",
    "lane": "project-recovery",
    "context": "delayed",
    "debrief_markers": (
      "final player tradeoff:",
      "attributed mechanisms to inspect:",
      "decision quality and outcome quality remain separate:",
      "=== decision quality evaluation ===",
    ),
  },
  "v0.10.56-project-recovery-use": {
    "batch_id": "v0.10.56-project-recovery-use",
    "path": "_workspace/experiments/v0.10.56-project-recovery-use/results.json",
    "lane": "project-recovery",
    "context": "delayed",
    "debrief_markers": (
      "final player tradeoff:",
      "attributed mechanisms to inspect:",
      "decision quality and outcome quality remain separate:",
      "=== decision quality evaluation ===",
    ),
  },
}

REVIEW_STEPS = (
  ("decision_context", "Actor-visible information and legal commands before each choice"),
  ("action_response", "Submitted commands, validation failures, and safe retries"),
  ("transition_follow_through", "Accepted effects, events, and committed state hashes"),
  ("delayed_or_partial_context", "Lagged rival signals or visible pending project context"),
  ("outcome_context", "Final tradeoff, transition count, and hash sequence"),
  ("debrief_explanation", "Month-level actions and retrospective decision-quality framing"),
)

LIMITATIONS = [
  "Coverage is traceability evidence, not causal evidence.",
  "The source policies are deterministic simulated policies, not human or classroom sessions.",
  "The audit does not measure debrief clarity, learning, strategy quality, balance, or calibration.",
  "Decision-versus-outcome separation in text does not establish that a decision was good or bad.",
  "Project ceilings, rival behavior, and delayed effects remain gameplay abstractions.",
]


def load_artifact(path):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def _turn_entries(run):
  if not isinstance(run, dict):
    return []
  for key in ("turn_trace", "trace"):
    value = run.get(key)
    if isinstance(value, list):
      return [entry for entry in value if isinstance(entry, dict)]
  return []


def _text(values):
  return "\n".join(str(value) for value in values).casefold()


def _run_text(run):
  entries = _turn_entries(run)
  values = list(run.get("debrief", [])) if isinstance(run, dict) else []
  for entry in entries:
    values.extend(entry.get("observation", []))
    values.extend(entry.get("events", []))
    transition = entry.get("latest_transition", {})
    if isinstance(transition, dict):
      values.extend(transition.get("events", []))
      values.extend(transition.get("effects", []))
  return _text(values)


def _trace_text(run):
  values = []
  for entry in _turn_entries(run):
    values.extend(entry.get("observation", []))
    values.extend(entry.get("events", []))
    transition = entry.get("latest_transition", {})
    if isinstance(transition, dict):
      values.extend(transition.get("events", []))
      values.extend(transition.get("effects", []))
  return _text(values)


def _step(name, description, status, limited_turns=None, evidence_gaps=None):
  return {
    "name": name,
    "description": description,
    "status": status,
    "limited_turns": sorted(limited_turns or []),
    "evidence_gaps": evidence_gaps or [],
  }


def _decision_context(run):
  limited_turns = []
  gaps = []
  for entry in _turn_entries(run):
    turn = entry.get("turn")
    if not entry.get("observation"):
      limited_turns.append(turn)
      gaps.append({"turn": turn, "reason": "missing actor-visible observation"})
    if not entry.get("legal_commands"):
      limited_turns.append(turn)
      gaps.append({"turn": turn, "reason": "missing legal command surface"})
    if not (entry.get("submitted_command") or entry.get("planned_command")):
      limited_turns.append(turn)
      gaps.append({"turn": turn, "reason": "missing submitted or planned command"})
  limited_turns = sorted(set(limited_turns))
  return _step(
    "decision_context",
    REVIEW_STEPS[0][1],
    "supported" if _turn_entries(run) and not gaps else "limited",
    limited_turns,
    gaps,
  )


def _action_response(run):
  limited_turns = []
  gaps = []
  entries = _turn_entries(run)
  for entry in entries:
    failures = entry.get("validation_failures", [])
    if not failures:
      continue
    turn = entry.get("turn")
    if entry.get("turn_after_failure") != turn:
      limited_turns.append(turn)
      gaps.append({"turn": turn, "reason": "rejected command changed the turn"})
    observation_after_failure = entry.get("observation_after_failure")
    if observation_after_failure is not None and observation_after_failure != entry.get("observation"):
      limited_turns.append(turn)
      gaps.append({"turn": turn, "reason": "rejected command changed the observation"})
    if observation_after_failure is None and not run.get("expected_probe_failures"):
      limited_turns.append(turn)
      gaps.append({"turn": turn, "reason": "rejected command has no preserved observation record"})
    if not entry.get("retry_commands"):
      limited_turns.append(turn)
      gaps.append({"turn": turn, "reason": "validation failure has no safe retry"})
  return _step(
    "action_response",
    REVIEW_STEPS[1][1],
    "supported" if entries and not gaps else "limited",
    limited_turns,
    gaps,
  )


def _transition_follow_through(run):
  limited_turns = []
  gaps = []
  entries = _turn_entries(run)
  for entry in entries:
    transition = entry.get("latest_transition")
    if not isinstance(transition, dict) or not transition.get("state_hash"):
      turn = entry.get("turn")
      limited_turns.append(turn)
      gaps.append({"turn": turn, "reason": "missing committed transition state hash"})
  return _step(
    "transition_follow_through",
    REVIEW_STEPS[2][1],
    "supported" if entries and not gaps else "limited",
    limited_turns,
    gaps,
  )


def _delayed_or_partial_context(run, contract):
  if contract["context"] == "not_applicable":
    return _step("delayed_or_partial_context", REVIEW_STEPS[3][1], "not_applicable")

  text = _trace_text(run)
  if contract["context"] == "partial":
    markers = ("observed, prior month", "monitor intel", "observed via monitor")
  else:
    markers = ("in-flight projects:",)
    present = any(
      line.casefold().startswith("in-flight projects:")
      and line.casefold() != "in-flight projects: none"
      for entry in _turn_entries(run)
      for line in entry.get("observation", [])
    )
  if contract["context"] == "partial":
    present = any(marker in text for marker in markers)
  if present:
    return _step("delayed_or_partial_context", REVIEW_STEPS[3][1], "supported")
  return _step(
    "delayed_or_partial_context",
    REVIEW_STEPS[3][1],
    "limited",
    evidence_gaps=[
      {
        "reason": f"missing {contract['context']} context markers: {', '.join(markers)}",
      }
    ],
  )


def _outcome_context(run):
  gaps = []
  entries = _turn_entries(run)
  transition_count = run.get("transition_count") if isinstance(run, dict) else None
  state_hashes = run.get("state_hashes") if isinstance(run, dict) else None
  if run.get("completion_status") != "complete":
    gaps.append({"reason": "run is not complete"})
  if not isinstance(state_hashes, list) or len(state_hashes) != transition_count:
    gaps.append({"reason": "state-hash sequence does not match transition count"})
  if not run.get("final_hash") or not run.get("final_observation"):
    gaps.append({"reason": "missing final hash or observation"})
  if len(entries) != transition_count:
    gaps.append({"reason": "turn trace does not match transition count"})
  return _step(
    "outcome_context",
    REVIEW_STEPS[4][1],
    "supported" if not gaps else "limited",
    evidence_gaps=gaps,
  )


def _debrief_explanation(run, contract):
  debrief = run.get("debrief", []) if isinstance(run, dict) else []
  text = _text(debrief)
  gaps = []
  entries = _turn_entries(run)
  month_count = sum(line.casefold().startswith("--- month ") for line in debrief)
  player_count = sum(line.casefold().startswith("player:") for line in debrief)
  for marker in contract["debrief_markers"]:
    if marker.casefold() not in text:
      gaps.append({"reason": f"missing debrief marker: {marker}"})
  if month_count < len(entries) or player_count < len(entries):
    gaps.append({"reason": "debrief does not preserve each month-level player action"})
  return _step(
    "debrief_explanation",
    REVIEW_STEPS[5][1],
    "supported" if not gaps else "limited",
    evidence_gaps=gaps,
  )


def _run_report(run, contract):
  if not isinstance(run, dict):
    return {
      "profile_name": "malformed run",
      "seed": None,
      "completion_status": "malformed",
      "status": "limited",
      "review_steps": [
        _step(name, description, "limited", evidence_gaps=[{"reason": "malformed run"}])
        for name, description in REVIEW_STEPS
      ],
    }

  steps = [
    _decision_context(run),
    _action_response(run),
    _transition_follow_through(run),
    _delayed_or_partial_context(run, contract),
    _outcome_context(run),
    _debrief_explanation(run, contract),
  ]
  return {
    "profile_name": run.get("profile_name", "unknown"),
    "seed": run.get("seed"),
    "completion_status": run.get("completion_status", "unknown"),
    "status": "supported" if all(step["status"] != "limited" for step in steps) else "limited",
    "review_steps": steps,
  }


def audit_artifact(artifact, contract, source_path=None):
  if not isinstance(artifact, dict):
    artifact = {}
  runs = artifact.get("runs", [])
  if not isinstance(runs, list):
    runs = []
  expected_version = contract["batch_id"].split("-", 1)[0].removeprefix("v")
  identity_supported = (
    artifact.get("batch_id") == contract["batch_id"]
    and artifact.get("code_version") == expected_version
    and artifact.get("campaign") == CAMPAIGN
  )
  run_reports = [_run_report(run, contract) for run in runs]
  complete_runs = [
    run for run in runs
    if isinstance(run, dict) and run.get("completion_status") == "complete"
  ]
  evidence_gaps = []
  if not identity_supported:
    evidence_gaps.append({"profile_name": "source identity", "seed": None, "missing_steps": ["source_identity"]})
  if not runs or len(complete_runs) != len(runs):
    evidence_gaps.append({"profile_name": "source completeness", "seed": None, "missing_steps": ["completed_runs"]})
  for report in run_reports:
    missing = [
      step["name"] for step in report["review_steps"] if step["status"] == "limited"
    ]
    if missing:
      evidence_gaps.append({
        "profile_name": report["profile_name"],
        "seed": report["seed"],
        "missing_steps": missing,
      })
  review_steps = []
  for name, description in REVIEW_STEPS:
    source_steps = [
      step for report in run_reports for step in report["review_steps"] if step["name"] == name
    ]
    limited = [step for step in source_steps if step["status"] == "limited"]
    not_applicable = [step for step in source_steps if step["status"] == "not_applicable"]
    status = "limited" if limited else "not_applicable" if len(not_applicable) == len(source_steps) else "supported"
    limited_turns = sorted({
      turn
      for step in source_steps
      for turn in step.get("limited_turns", [])
    })
    step_gaps = [
      gap
      for step in source_steps
      for gap in step.get("evidence_gaps", [])
    ]
    review_steps.append({
      "name": name,
      "description": description,
      "status": status,
      "covered_runs": len(source_steps) - len(limited),
      "eligible_runs": len(source_steps),
      "limited_turns": limited_turns,
      "evidence_gaps": step_gaps,
    })
  return {
    "source_artifact": source_path or contract["path"],
    "batch_id": artifact.get("batch_id", "unknown"),
    "code_version": artifact.get("code_version", "unknown"),
    "campaign": artifact.get("campaign", "unknown"),
    "identity_status": "supported" if identity_supported else "limited",
    "lane": contract["lane"],
    "context": contract["context"],
    "run_count": len(runs),
    "completed_run_count": len(complete_runs),
    "review_steps": review_steps,
    "run_reports": run_reports,
    "evidence_gaps": evidence_gaps,
    "status": "supported" if identity_supported and not evidence_gaps else "limited",
  }


def _hashes_by_seed(artifact):
  if not isinstance(artifact, dict):
    return {}
  return {
    run.get("seed"): run.get("state_hashes")
    for run in artifact.get("runs", [])
    if isinstance(run, dict)
  }


def hash_continuity(artifacts):
  by_batch = {
    artifact.get("batch_id"): artifact
    for artifact in artifacts
    if isinstance(artifact, dict)
  }
  pairs = (
    ("v0.10.54-project-limit-recovery", "v0.10.55-asc-project-observation"),
    ("v0.10.55-asc-project-observation", "v0.10.56-project-recovery-use"),
  )
  comparisons = []
  for earlier_id, later_id in pairs:
    earlier = _hashes_by_seed(by_batch.get(earlier_id, {}))
    later = _hashes_by_seed(by_batch.get(later_id, {}))
    seeds = sorted(set(earlier) | set(later))
    mismatches = [seed for seed in seeds if earlier.get(seed) != later.get(seed)]
    comparisons.append({
      "earlier": earlier_id,
      "later": later_id,
      "seed_count": len(seeds),
      "status": "supported" if not mismatches and seeds else "limited",
      "mismatched_seeds": mismatches,
    })
  return {
    "status": "supported" if all(item["status"] == "supported" for item in comparisons) else "limited",
    "comparisons": comparisons,
  }


def build_audit(paths=None):
  contracts = list(SOURCE_CONTRACTS.values())
  if paths is None:
    paths = [ROOT / contract["path"] for contract in contracts]
  artifacts = [load_artifact(path) for path in paths]
  reports = [
    audit_artifact(artifact, contract, str(Path(path).relative_to(ROOT)))
    for artifact, contract, path in zip(artifacts, contracts, paths)
  ]
  evidence_gaps = [
    {"batch_id": report["batch_id"], **gap}
    for report in reports
    for gap in report["evidence_gaps"]
  ]
  return {
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "campaign": CAMPAIGN,
    "source_artifacts": [report["source_artifact"] for report in reports],
    "source_count": len(reports),
    "run_count": sum(report["run_count"] for report in reports),
    "completed_run_count": sum(report["completed_run_count"] for report in reports),
    "completed_source_count": sum(
      report["run_count"] > 0 and report["completed_run_count"] == report["run_count"]
      for report in reports
    ),
    "source_reports": reports,
    "review_steps": [
      {
        "name": name,
        "description": description,
        "status": "limited" if any(
          step["name"] == name and step["status"] == "limited"
          for report in reports for step in report["review_steps"]
        ) else "supported",
      }
      for name, description in REVIEW_STEPS
    ],
    "hash_continuity": hash_continuity(artifacts),
    "evidence_gaps": evidence_gaps,
    "evidence_gap_count": len(evidence_gaps),
    "status": "supported" if not evidence_gaps else "limited",
    "runtime_promotion": "deferred",
    "promotion_basis": (
      "This audit measures decision-to-debrief trace coherence in existing artifacts. "
      "Runtime or interface promotion requires separate player-facing, instructor-facing, "
      "or domain-review evidence of an unexplained problem."
    ),
    "limitations": LIMITATIONS,
  }


def validate_audit(audit):
  assert audit["batch_id"] == BATCH_ID
  assert audit["code_version"] == CODE_VERSION
  assert audit["campaign"] == CAMPAIGN
  assert audit["source_count"] == len(SOURCE_CONTRACTS)
  assert audit["completed_source_count"] == len(SOURCE_CONTRACTS)
  assert audit["run_count"] == audit["completed_run_count"]
  assert audit["evidence_gap_count"] == len(audit["evidence_gaps"])
  assert audit["hash_continuity"]["status"] == "supported"
  assert audit["runtime_promotion"] == "deferred"
  assert audit["source_artifacts"] == [
    contract["path"] for contract in SOURCE_CONTRACTS.values()
  ]


def render_markdown(audit):
  lines = [
    "# Debrief-Coherence Audit v0.10.58",
    "",
    f"- **Batch id:** {audit['batch_id']}",
    f"- **Campaign:** `{audit['campaign']}`",
    f"- **Source artifacts:** {audit['source_count']}",
    f"- **Runs reviewed:** {audit['completed_run_count']} of {audit['run_count']}",
    "",
    "This deterministic read-only audit joins decision-time observations, commands, "
    "accepted transitions, delayed or partial context, outcomes, and retrospective debrief markers.",
    "",
    "## Coverage",
    "",
    "| Source artifact | Lane | Decision context | Action response | Transition follow-through | Delayed/partial context | Outcome context | Debrief explanation |",
    "| --- | --- | --- | --- | --- | --- | --- | --- |",
  ]
  for report in audit["source_reports"]:
    statuses = {step["name"]: step["status"] for step in report["review_steps"]}
    lines.append(
      f"| `{report['batch_id']}` | {report['lane']} | {statuses['decision_context']} | "
      f"{statuses['action_response']} | {statuses['transition_follow_through']} | "
      f"{statuses['delayed_or_partial_context']} | {statuses['outcome_context']} | "
      f"{statuses['debrief_explanation']} |"
    )
  lines.extend(["", "## Hash continuity", ""])
  for comparison in audit["hash_continuity"]["comparisons"]:
    lines.append(
      f"- `{comparison['earlier']}` → `{comparison['later']}`: {comparison['status']} "
      f"({comparison['seed_count']} seeds; mismatches: "
      f"{', '.join(str(seed) for seed in comparison['mismatched_seeds']) or 'none'})."
    )
  lines.extend([
    "",
    "## Promotion decision",
    "",
    f"Runtime promotion: {audit['runtime_promotion']}.",
    "",
    audit["promotion_basis"],
    "",
    "Decision-versus-outcome separation is a traceability marker, not a quality judgment.",
    "",
    "## Evidence gaps",
    "",
  ])
  if audit["evidence_gaps"]:
    for gap in audit["evidence_gaps"]:
      lines.append(
        f"- `{gap['batch_id']}` / {gap['profile_name']} / seed {gap['seed']}: "
        f"missing {', '.join(gap['missing_steps'])}."
      )
  else:
    lines.append("None identified in the reviewed source shapes.")
  lines.extend(["", "## Evidence limits", ""])
  lines.extend(f"- {limitation}" for limitation in audit["limitations"])
  lines.append("")
  return "\n".join(lines)


def main():
  output_dir = Path(__file__).parent
  audit = build_audit()
  validate_audit(audit)
  (output_dir / "results.json").write_text(
    json.dumps(audit, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )
  (output_dir / "audit.md").write_text(
    render_markdown(audit),
    encoding="utf-8",
  )


if __name__ == "__main__":
  main()
