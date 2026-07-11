#!/usr/bin/env python3
"""Audit event-specific debrief use across existing Phase 7 artifacts."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BATCH_ID = "v0.10.57-debrief-use-audit"
CODE_VERSION = "0.10.57"
CAMPAIGN = "competitive-regional-v1"

SOURCE_CONTRACTS = {
  "v0.10.43-rival-info-follow-through": {
    "batch_id": "v0.10.43-rival-info-follow-through",
    "path": "_workspace/experiments/v0.10.43-rival-info-follow-through/results.json",
    "lane": "rival-pressure",
    "explanation_markers": ("rival ", "monitor", "decision quality"),
  },
  "v0.10.50-teachability-observation-capture": {
    "batch_id": "v0.10.50-teachability-observation-capture",
    "path": "_workspace/experiments/v0.10.50-teachability-observation-capture/results.json",
    "lane": "strategy-tradeoff",
    "explanation_markers": ("final player tradeoff", "decision quality"),
  },
  "v0.10.51-adversarial-resource-probe": {
    "batch_id": "v0.10.51-adversarial-resource-probe",
    "path": "_workspace/experiments/v0.10.51-adversarial-resource-probe/results.json",
    "lane": "resource-retry",
    "explanation_markers": ("capital project lesson", "decision quality"),
  },
  "v0.10.54-project-limit-recovery": {
    "batch_id": "v0.10.54-project-limit-recovery",
    "path": "_workspace/experiments/v0.10.54-project-limit-recovery/results.json",
    "lane": "project-recovery",
    "explanation_markers": ("maximum of 2 concurrent projects",),
  },
  "v0.10.55-asc-project-observation": {
    "batch_id": "v0.10.55-asc-project-observation",
    "path": "_workspace/experiments/v0.10.55-asc-project-observation/results.json",
    "lane": "project-recovery",
    "explanation_markers": ("maximum of 2 concurrent projects",),
  },
  "v0.10.56-project-recovery-use": {
    "batch_id": "v0.10.56-project-recovery-use",
    "path": "_workspace/experiments/v0.10.56-project-recovery-use/results.json",
    "lane": "project-recovery",
    "explanation_markers": ("maximum of 2 concurrent projects",),
  },
}

REVIEW_STEPS = (
  ("visibility", "Actor-visible observations, advice, or rival signals"),
  ("response", "Submitted commands, validation failures, or retries"),
  ("follow-through", "Accepted transitions after the observed response"),
  ("outcome", "Transition counts, state hashes, and final results"),
  ("explanation", "Event-specific debrief material for retrospective review"),
)

LIMITATIONS = [
  "Coverage is traceability evidence, not causal evidence.",
  "The source policies are deterministic simulated policies, not human or classroom sessions.",
  "The audit does not measure debrief clarity, learning, strategy quality, balance, or calibration.",
  "A supported trace does not establish that an instructor or learner will find the explanation sufficient.",
]


def load_artifact(path):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def _turn_entries(run):
  if not isinstance(run, dict):
    return []
  entries = []
  for key in ("turn_trace", "trace"):
    value = run.get(key, [])
    if isinstance(value, list):
      entries.extend(entry for entry in value if isinstance(entry, dict))
  return entries


def _has_any_value(run, keys):
  if not isinstance(run, dict):
    return False
  if any(run.get(key) for key in keys):
    return True
  return any(entry.get(key) for entry in _turn_entries(run) for key in keys)


def _debrief_contains(run, markers):
  if not isinstance(run, dict):
    return False
  debrief = run.get("debrief", [])
  if not isinstance(debrief, list):
    return False
  text = "\n".join(str(line) for line in debrief).casefold()
  return all(marker.casefold() in text for marker in markers)


def _has_recovery_chain(run):
  for entry in _turn_entries(run):
    failures = entry.get("validation_failures", [])
    if not failures:
      continue
    if (
      entry.get("turn_after_failure") == entry.get("turn")
      and entry.get("observation_after_failure") == entry.get("observation")
      and entry.get("retry_commands")
    ):
      return True
  return False


def _step_evidence(run, step_name, contract):
  if step_name == "visibility":
    return _has_any_value(
      run,
      (
        "observation",
        "final_observation",
        "rendered_options",
        "options",
        "rival_information_examples",
        "monitor_signal_count",
      ),
    )
  if step_name == "response":
    return _has_any_value(
      run,
      (
        "commands",
        "response_records",
        "selected_option_label",
        "submitted_command",
        "planned_command",
        "validation_failures",
        "expected_probe_failures",
      ),
    )
  if step_name == "follow-through":
    return _has_recovery_chain(run) or (
      _has_any_value(run, ("commands", "response_records", "submitted_command"))
      and _has_any_value(run, ("latest_transition", "state_hashes"))
    )
  if step_name == "outcome":
    return bool(
      isinstance(run, dict)
      and run.get("final_hash")
      and run.get("state_hashes")
      and run.get("transition_count") is not None
    )
  if step_name == "explanation":
    return _debrief_contains(run, contract["explanation_markers"])
  raise ValueError(f"unknown review step: {step_name}")


def _status(covered, total):
  if covered == total and total > 0:
    return "supported"
  if covered > 0:
    return "limited"
  return "unsupported"


def _run_report(run, contract):
  if not isinstance(run, dict):
    return {
      "profile_name": "malformed run",
      "seed": None,
      "completion_status": "malformed",
      "status": "limited",
      "step_evidence": {name: False for name, _ in REVIEW_STEPS},
      "missing_steps": [name for name, _ in REVIEW_STEPS],
    }

  evidence = {
    name: _step_evidence(run, name, contract)
    for name, _ in REVIEW_STEPS
  }
  missing = [name for name, present in evidence.items() if not present]
  return {
    "profile_name": run.get("profile_name", "unknown"),
    "seed": run.get("seed"),
    "completion_status": run.get("completion_status", "unknown"),
    "status": "supported" if not missing else "limited",
    "step_evidence": evidence,
    "missing_steps": missing,
  }


def audit_artifact(artifact, contract, source_path=None):
  runs = artifact.get("runs", []) if isinstance(artifact, dict) else []
  batch_id = artifact.get("batch_id", "unknown") if isinstance(artifact, dict) else "unknown"
  code_version = artifact.get("code_version", "unknown") if isinstance(artifact, dict) else "unknown"
  campaign = artifact.get("campaign", "unknown") if isinstance(artifact, dict) else "unknown"
  identity_supported = (
    batch_id == contract["batch_id"]
    and code_version == contract["batch_id"].split("-", 1)[0].removeprefix("v")
    and campaign == CAMPAIGN
  )
  if not isinstance(runs, list):
    runs = []
  complete_runs = [
    run
    for run in runs
    if isinstance(run, dict) and run.get("completion_status") == "complete"
  ]
  review_steps = []
  for name, description in REVIEW_STEPS:
    covered = sum(_step_evidence(run, name, contract) for run in complete_runs)
    review_steps.append(
      {
        "name": name,
        "description": description,
        "covered_runs": covered,
        "eligible_runs": len(complete_runs),
        "status": _status(covered, len(complete_runs)),
      }
    )

  run_reports = [_run_report(run, contract) for run in runs]
  evidence_gaps = [
    {
      "profile_name": report["profile_name"],
      "seed": report["seed"],
      "missing_steps": report["missing_steps"],
    }
    for report in run_reports
    if report["missing_steps"]
  ]
  if not identity_supported:
    evidence_gaps.insert(
      0,
      {
        "profile_name": "source identity",
        "seed": None,
        "missing_steps": ["source_identity"],
      },
    )
  if not runs or len(complete_runs) != len(runs):
    evidence_gaps.insert(
      0,
      {
        "profile_name": "source completeness",
        "seed": None,
        "missing_steps": ["completed_runs"],
      },
    )
  return {
    "source_artifact": source_path or contract["path"],
    "batch_id": batch_id,
    "code_version": code_version,
    "campaign": campaign,
    "identity_status": "supported" if identity_supported else "limited",
    "lane": contract["lane"],
    "run_count": len(runs),
    "completed_run_count": len(complete_runs),
    "review_steps": review_steps,
    "run_reports": run_reports,
    "evidence_gaps": evidence_gaps,
    "status": "supported" if identity_supported and not evidence_gaps else "limited",
  }


def _hashes_by_seed(artifact):
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
    comparisons.append(
      {
        "earlier": earlier_id,
        "later": later_id,
        "seed_count": len(seeds),
        "status": "supported" if not mismatches and seeds else "limited",
        "mismatched_seeds": mismatches,
      }
    )
  return {
    "status": "supported" if all(
      comparison["status"] == "supported" for comparison in comparisons
    ) else "limited",
    "comparisons": comparisons,
  }


def build_audit(paths=None):
  contracts = list(SOURCE_CONTRACTS.values())
  if paths is None:
    paths = [ROOT / contract["path"] for contract in contracts]
  artifacts = [load_artifact(path) for path in paths]
  reports = [
    audit_artifact(
      artifact,
      contract,
      str(Path(path).relative_to(ROOT)),
    )
    for artifact, contract, path in zip(artifacts, contracts, paths)
  ]
  evidence_gaps = [
    {
      "batch_id": report["batch_id"],
      **gap,
    }
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
    "completed_source_count": sum(report["status"] == "supported" for report in reports),
    "source_reports": reports,
    "hash_continuity": hash_continuity(artifacts),
    "evidence_gaps": evidence_gaps,
    "evidence_gap_count": len(evidence_gaps),
    "runtime_promotion": "deferred",
    "promotion_basis": (
      "This audit measures event-specific trace continuity in existing artifacts. "
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
  assert audit["evidence_gap_count"] == 0
  assert all(
    report["identity_status"] == "supported"
    and report["status"] == "supported"
    for report in audit["source_reports"]
  )
  assert audit["hash_continuity"]["status"] == "supported"
  assert audit["runtime_promotion"] == "deferred"
  assert audit["source_artifacts"] == [
    contract["path"] for contract in SOURCE_CONTRACTS.values()
  ]


def render_markdown(audit):
  lines = [
    "# Debrief-Use Audit v0.10.57",
    "",
    f"- **Batch id:** {audit['batch_id']}",
    f"- **Campaign:** `{audit['campaign']}`",
    f"- **Source artifacts:** {audit['source_count']}",
    f"- **Runs reviewed:** {audit['completed_run_count']} of {audit['run_count']}",
    "",
    "This is a deterministic read-only audit of existing Phase 7 evidence. It "
    "checks event-specific trace continuity without launching sessions or changing runtime behavior.",
    "",
    "## Coverage",
    "",
    "| Source artifact | Lane | Visibility | Response | Follow-through | Outcome | Explanation |",
    "| --- | --- | --- | --- | --- | --- | --- |",
  ]
  for report in audit["source_reports"]:
    statuses = {step["name"]: step["status"] for step in report["review_steps"]}
    lines.append(
      f"| `{report['batch_id']}` | {report['lane']} | {statuses['visibility']} | "
      f"{statuses['response']} | {statuses['follow-through']} | "
      f"{statuses['outcome']} | {statuses['explanation']} |"
    )

  lines.extend([
    "",
    "## Project-recovery hash continuity",
    "",
  ])
  for comparison in audit["hash_continuity"]["comparisons"]:
    lines.append(
      f"- `{comparison['earlier']}` → `{comparison['later']}`: "
      f"{comparison['status']} ({comparison['seed_count']} seeds; "
      f"mismatches: {', '.join(str(seed) for seed in comparison['mismatched_seeds']) or 'none'})."
    )

  lines.extend([
    "",
    "## Promotion decision",
    "",
    f"Runtime promotion: {audit['runtime_promotion']}.",
    "",
    audit["promotion_basis"],
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
