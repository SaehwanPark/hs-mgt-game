#!/usr/bin/env python3
"""Synthesize existing competitive teachability evidence without new runs."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BATCH_ID = "v0.10.49-teachability-gate-synthesis"
CODE_VERSION = "0.10.49"
CAMPAIGN = "competitive-regional-v1"
SOURCE_PATHS = [
  ROOT / "_workspace/experiments/v0.10.45-instructor-debrief-use-audit/results.json",
  ROOT / "_workspace/experiments/v0.10.46-expert-clearability-evidence/results.json",
  ROOT / "_workspace/experiments/v0.10.47-command-effect-explainability/results.json",
  ROOT / "_workspace/experiments/v0.10.48-strategy-diversity-evidence/results.json",
]
EXPECTED_BATCHES = {
  "v0.10.45-instructor-debrief-use-audit": "instructor debrief-use coverage",
  "v0.10.46-expert-clearability-evidence": "Expert clearability",
  "v0.10.47-command-effect-explainability": "command-to-effect traceability",
  "v0.10.48-strategy-diversity-evidence": "strategy diversity",
}
LIMITATIONS = [
  "This synthesis is traceability and completion evidence, not causal evidence.",
  "The source policies are deterministic simulated policies, not human or classroom evidence.",
  "Endpoint differences and distinct command trajectories do not establish strategy value, dominance, or optimality.",
  "Supported trace fields do not establish that an instructor or learner finds the debrief clear or educationally effective.",
]


def load_artifact(path):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def _status(covered, eligible):
  if eligible > 0 and covered == eligible:
    return "supported"
  if covered > 0:
    return "limited"
  return "unsupported"


def _dimension(name, covered, eligible, description):
  return {
    "name": name,
    "description": description,
    "covered_runs": covered,
    "eligible_runs": eligible,
    "status": _status(covered, eligible),
  }


def _entries(run, name):
  value = run.get(name, []) if isinstance(run, dict) else []
  return value if isinstance(value, list) else []


def _run_dimensions(runs, eligible=None):
  complete = [
    run for run in runs
    if isinstance(run, dict) and run.get("completion_status") == "complete"
  ]
  eligible = len(complete) if eligible is None else eligible
  visibility = sum(
    bool(run.get("final_observation"))
    or any(entry.get("observation") for entry in _entries(run, "turn_trace") if isinstance(entry, dict))
    for run in complete
  )
  response = sum(
    bool(run.get("commands"))
    or any(entry.get("submitted_command") for entry in _entries(run, "turn_trace") if isinstance(entry, dict))
    for run in complete
  )
  follow_through = sum(
    bool(run.get("commands"))
    or any(entry.get("latest_transition") for entry in _entries(run, "turn_trace") if isinstance(entry, dict))
    for run in complete
  )
  outcome = sum(
    bool(run.get("final_hash"))
    and bool(run.get("state_hashes"))
    and run.get("transition_count") is not None
    for run in complete
  )
  explanation = sum(bool(run.get("debrief")) for run in complete)
  return {
    "visibility": _dimension("visibility", visibility, eligible, "Actor-visible observations or reports"),
    "response": _dimension("response", response, eligible, "Submitted commands or policy responses"),
    "follow-through": _dimension("follow-through", follow_through, eligible, "Operational action traces"),
    "outcome": _dimension("outcome", outcome, eligible, "Hashes, transitions, and final results"),
    "explanation": _dimension("explanation", explanation, eligible, "History or debrief material"),
  }


def _audit_instructor_summary(artifact):
  reports = artifact.get("artifacts", [])
  eligible = len(reports)
  covered = sum(
    all(step.get("status") == "supported" for step in report.get("review_steps", []))
    for report in reports
  )
  dimensions = {
    "visibility": _dimension("visibility", covered, eligible, "Actor-visible observations or reports"),
    "response": _dimension("response", covered, eligible, "Submitted commands or policy responses"),
    "follow-through": _dimension("follow-through", covered, eligible, "Operational action traces"),
    "outcome": _dimension("outcome", covered, eligible, "Hashes, transitions, and final results"),
    "explanation": _dimension("explanation", covered, eligible, "History or debrief material"),
  }
  return dimensions, eligible


def _audit_specialized(artifact):
  batch_id = artifact.get("batch_id", "")
  raw_runs = artifact.get("runs", [])
  runs = raw_runs if isinstance(raw_runs, list) else []
  eligible = len(runs)
  if batch_id == "v0.10.46-expert-clearability-evidence":
    complete = sum(
      isinstance(run, dict) and run.get("completion_status") == "complete"
      for run in runs
    )
    dimensions = _run_dimensions(runs, eligible)
    dimensions["clearability"] = _dimension(
      "clearability", complete, eligible, "Completion of the full Expert campaign"
    )
    return dimensions, eligible
  if batch_id == "v0.10.47-command-effect-explainability":
    supported = sum(
      isinstance(run, dict) and run.get("coverage_status") == "supported"
      for run in runs
    )
    return {
      "command-to-effect traceability": _dimension(
        "command-to-effect traceability",
        supported,
        eligible,
        "Action-specific transition evidence and monthly debrief records",
      )
    }, eligible
  if batch_id == "v0.10.48-strategy-diversity-evidence":
    supported = sum(
      isinstance(run, dict) and run.get("status") == "supported"
      for run in runs
    )
    return {
      "strategy diversity": _dimension(
        "strategy diversity",
        supported,
        eligible,
        "Descriptive command-family variation and final tradeoff records",
      )
    }, eligible
  return _run_dimensions(runs), eligible


def audit_source(artifact, source_path):
  batch_id = artifact.get("batch_id", "unknown")
  if batch_id == "v0.10.45-instructor-debrief-use-audit":
    dimensions, eligible = _audit_instructor_summary(artifact)
  else:
    dimensions, eligible = _audit_specialized(artifact)
  limited_dimensions = sorted(
    name for name, dimension in dimensions.items()
    if dimension["status"] != "supported"
  )
  expected_label = EXPECTED_BATCHES.get(batch_id)
  return {
    "source_artifact": source_path,
    "batch_id": batch_id,
    "code_version": artifact.get("code_version", "unknown"),
    "campaign": artifact.get("campaign", "unknown"),
    "run_count": artifact.get("run_count", len(artifact.get("runs", []))),
    "completed_run_count": artifact.get("completed_run_count", eligible),
    "expected_evidence": expected_label or "unrecognized source",
    "dimensions": dimensions,
    "limited_dimensions": limited_dimensions,
    "status": "supported" if expected_label and not limited_dimensions else "limited",
  }


def _matrix(artifact):
  runs = artifact.get("runs", [])
  if not isinstance(runs, list):
    return set()
  return {
    (run.get("profile_name"), run.get("seed"))
    for run in runs
    if isinstance(run, dict)
  }


def _matrix_continuity(artifacts):
  by_batch = {artifact.get("batch_id"): artifact for artifact in artifacts}
  source_batches = [
    "v0.10.46-expert-clearability-evidence",
    "v0.10.47-command-effect-explainability",
    "v0.10.48-strategy-diversity-evidence",
  ]
  matrices = {batch: _matrix(by_batch[batch]) for batch in source_batches if batch in by_batch}
  expected = matrices.get(source_batches[0], set())
  matching = all(matrix == expected for matrix in matrices.values()) and len(matrices) == len(source_batches)
  return {
    "status": "supported" if matching and expected else "limited",
    "expected_member_count": len(expected),
    "source_matrices": {
      batch: sorted([list(member) for member in matrix])
      for batch, matrix in sorted(matrices.items())
    },
  }


def build_audit(paths=SOURCE_PATHS):
  sorted_paths = sorted(Path(path) for path in paths)
  artifacts = [
    load_artifact(path)
    for path in sorted_paths
  ]
  reports = [
    audit_source(artifact, str(path.relative_to(ROOT)))
    for artifact, path in zip(artifacts, sorted_paths)
  ]
  matrix_continuity = _matrix_continuity(artifacts)
  incomplete_sources = [
    report["batch_id"] for report in reports if report["status"] != "supported"
  ]
  unexplained_gaps = []
  observed_batches = {report["batch_id"] for report in reports}
  expected_batches = set(EXPECTED_BATCHES)
  missing_batches = sorted(expected_batches - observed_batches)
  unexpected_batches = sorted(observed_batches - expected_batches)
  if incomplete_sources or missing_batches or unexpected_batches:
    unexplained_gaps.append(
      {
        "type": "source coverage",
        "incomplete_sources": sorted(incomplete_sources),
        "missing_sources": missing_batches,
        "unexpected_sources": unexpected_batches,
      }
    )
  if matrix_continuity["status"] != "supported":
    unexplained_gaps.append(
      {
        "type": "matrix continuity",
        "expected_member_count": matrix_continuity["expected_member_count"],
      }
    )
  if unexplained_gaps:
    promotion_basis = (
      "Evidence coverage gaps were found; runtime promotion remains deferred "
      "until a separate player-facing, instructor-facing, or domain-review "
      "finding establishes an unexplained problem."
    )
  else:
    promotion_basis = (
      "No concrete unexplained player-facing, instructor-facing, or domain-review gap was found; "
      "traceability and endpoint differences are not causal evidence."
    )
  return {
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "campaign": CAMPAIGN,
    "source_artifacts": [report["source_artifact"] for report in reports],
    "source_count": len(reports),
    "completed_source_count": len(reports) - len(incomplete_sources),
    "artifacts": reports,
    "matrix_continuity": matrix_continuity,
    "unexplained_gaps": unexplained_gaps,
    "unexplained_gap_count": len(unexplained_gaps),
    "runtime_promotion": "deferred",
    "promotion_basis": promotion_basis,
    "limitations": LIMITATIONS,
  }


def validate_audit(audit):
  assert audit["batch_id"] == BATCH_ID
  assert audit["code_version"] == CODE_VERSION
  assert audit["campaign"] == CAMPAIGN
  assert audit["source_count"] == 4
  assert audit["completed_source_count"] == 4
  assert {report["batch_id"] for report in audit["artifacts"]} == set(EXPECTED_BATCHES)
  assert all(report["campaign"] == CAMPAIGN for report in audit["artifacts"])
  assert audit["matrix_continuity"]["status"] == "supported"
  assert audit["runtime_promotion"] == "deferred"
  assert audit["unexplained_gap_count"] == 0
  assert not any(report["status"] != "supported" for report in audit["artifacts"])


def render_markdown(audit):
  lines = [
    "# Teachability-Gate Synthesis v0.10.49",
    "",
    f"- **Batch id:** {audit['batch_id']}",
    f"- **Campaign:** `{audit['campaign']}`",
    f"- **Source artifacts:** {audit['source_count']}",
    f"- **Completed source audits:** {audit['completed_source_count']} of {audit['source_count']}",
    "",
    "This is a deterministic read-only synthesis of existing evidence. It does not launch new sessions or change runtime behavior.",
    "",
    "## Evidence coverage",
    "",
    "| Source artifact | Expected evidence | Status | Limited dimensions |",
    "| --- | --- | --- | --- |",
  ]
  for report in audit["artifacts"]:
    limited = ", ".join(report["limited_dimensions"]) or "none"
    lines.append(
      f"| `{report['batch_id']}` | {report['expected_evidence']} | {report['status']} | {limited} |"
    )
  lines.extend(
    [
      "",
      "## Matrix continuity",
      "",
      f"The v0.10.46–v0.10.48 matrix is `{audit['matrix_continuity']['status']}` with {audit['matrix_continuity']['expected_member_count']} expected profile/seed members.",
      "",
      "## Promotion decision",
      "",
      f"Runtime promotion: {audit['runtime_promotion']}",
      "",
      audit["promotion_basis"],
      "",
      "A future runtime or interface slice still requires a player-facing, instructor-facing, or domain-review finding that current observations, histories, diagnostics, and debriefs cannot explain.",
      "",
      "## Unexplained gaps",
      "",
    ]
  )
  if audit["unexplained_gaps"]:
    lines.extend(
      f"- {json.dumps(gap, sort_keys=True)}"
      for gap in audit["unexplained_gaps"]
    )
  else:
    lines.append("None identified.")
  lines.extend(
    [
      "",
      "## Evidence limits",
      "",
    ]
  )
  lines.extend(f"- {limitation}" for limitation in audit["limitations"])
  lines.append("")
  return "\n".join(lines)


def main():
  output_dir = Path(__file__).resolve().parent
  audit = build_audit()
  validate_audit(audit)
  (output_dir / "results.json").write_text(
    json.dumps(audit, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )
  (output_dir / "audit.md").write_text(render_markdown(audit), encoding="utf-8")


if __name__ == "__main__":
  main()
