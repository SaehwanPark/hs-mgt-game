#!/usr/bin/env python3
"""Synthesize the v0.10.50-v0.10.52 Phase 7 evidence chain."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BATCH_ID = "v0.10.53-evidence-synthesis"
CODE_VERSION = "0.10.53"
CAMPAIGN = "competitive-regional-v1"
SOURCE_PATHS = [
  ROOT / "_workspace/experiments/v0.10.50-teachability-observation-capture/results.json",
  ROOT / "_workspace/experiments/v0.10.51-adversarial-resource-probe/results.json",
  ROOT / "_workspace/experiments/v0.10.52-decision-load-evidence/results.json",
]
EXPECTED_BATCHES = {
  "v0.10.50-teachability-observation-capture": "observation-driven teachability capture",
  "v0.10.51-adversarial-resource-probe": "resource validation and retry probes",
  "v0.10.52-decision-load-evidence": "turn-level pacing proxies",
}
EXPECTED_VERSIONS = {
  batch_id: batch_id.split("-")[0].removeprefix("v")
  for batch_id in EXPECTED_BATCHES
}
EXPECTED_MATRIX = {
  (profile_id, seed)
  for profile_id in (
    "fiscal_steward",
    "access_expansion_advocate",
    "first_time_executive",
  )
  for seed in (42, 43, 44)
}
CONTROL_BATCH_ID = "v0.10.51-adversarial-resource-probe"
CONTROL_ARTIFACT = (
  "_workspace/experiments/v0.10.50-teachability-observation-capture/results.json"
)
LIMITATIONS = [
  "The source artifacts are deterministic simulated-policy evidence, not human or classroom evidence.",
  "Cross-artifact continuity describes trace coverage and control identity; it does not establish causality, strategy quality, balance, or optimality.",
  "Pacing, validation, retry, and endpoint records do not measure cognitive load, comprehension, learning, or policy validity.",
  "Runtime and interface promotion remains deferred until a player-facing, instructor-facing, or domain-review gap is identified.",
]


def load_artifact(path):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def _runs(artifact):
  runs = artifact.get("runs", []) if isinstance(artifact, dict) else []
  return runs if isinstance(runs, list) else []


def _limited_dimension(limited_dimensions, name):
  if name not in limited_dimensions:
    limited_dimensions.append(name)


def _identity_supported(artifact, batch_id):
  return (
    isinstance(artifact, dict)
    and artifact.get("batch_id") == batch_id
    and artifact.get("code_version") == EXPECTED_VERSIONS.get(batch_id)
    and artifact.get("campaign") == CAMPAIGN
  )


def _audit_v050(artifact, limited_dimensions):
  runs = _runs(artifact)
  complete = [
    run for run in runs
    if isinstance(run, dict) and run.get("completion_status") == "complete"
  ]
  members = {
    (run.get("profile_id"), run.get("seed"))
    for run in runs
    if isinstance(run, dict)
  }
  if len(runs) != len(EXPECTED_MATRIX):
    _limited_dimension(limited_dimensions, "run coverage")
  if len(complete) != len(EXPECTED_MATRIX):
    _limited_dimension(limited_dimensions, "run completeness")
  if members != EXPECTED_MATRIX:
    _limited_dimension(limited_dimensions, "matrix continuity")
  if any(
    not isinstance(run, dict)
    or run.get("transition_count") != 24
    or run.get("retry_count") != 0
    for run in runs
  ):
    _limited_dimension(limited_dimensions, "24-month retry-free completion")
  return len(runs), len(complete)


def _audit_v051(artifact, limited_dimensions):
  runs = _runs(artifact)
  complete = [
    run for run in runs
    if isinstance(run, dict) and run.get("completion_status") == "complete"
  ]
  if len(runs) != 3:
    _limited_dimension(limited_dimensions, "run coverage")
  if len(complete) != 3:
    _limited_dimension(limited_dimensions, "run completeness")
  if any(
    not isinstance(run, dict)
    or run.get("transition_count") != 24
    or run.get("retry_count") != 5
    or len(run.get("expected_probe_failures", [])) != 5
    or len(run.get("validation_failures", [])) != 5
    or run.get("unexpected_failures")
    for run in runs
  ):
    _limited_dimension(limited_dimensions, "expected validation and retry probes")
  controls = artifact.get("control_runs", [])
  if not isinstance(controls, list) or len(controls) != 3:
    _limited_dimension(limited_dimensions, "control coverage")
  return len(runs), len(complete)


def _audit_v052(artifact, limited_dimensions):
  runs = _runs(artifact)
  complete_count = artifact.get("complete_run_count")
  if complete_count != 9:
    _limited_dimension(limited_dimensions, "run completeness")
  continuity = artifact.get("matrix_continuity", {})
  if (
    not isinstance(continuity, dict)
    or continuity.get("status") != "supported"
    or continuity.get("expected_member_count") != 9
    or continuity.get("observed_member_count") != 9
  ):
    _limited_dimension(limited_dimensions, "matrix continuity")
  summaries = artifact.get("profile_summaries", {})
  if not isinstance(summaries, dict) or set(summaries) != {
    "fiscal_steward",
    "access_expansion_advocate",
    "first_time_executive",
  }:
    _limited_dimension(limited_dimensions, "profile summaries")
  elif any(
    not isinstance(summary, dict)
    or summary.get("run_count") != 3
    or summary.get("seed_stable") is not True
    or summary.get("seeds") != [42, 43, 44]
    or summary.get("status") != "supported"
    for summary in summaries.values()
  ):
    _limited_dimension(limited_dimensions, "profile seed stability")
  return len(runs), complete_count if isinstance(complete_count, int) else 0


def audit_source(artifact, source_path):
  batch_id = artifact.get("batch_id", "unknown") if isinstance(artifact, dict) else "unknown"
  limited_dimensions = []
  if batch_id not in EXPECTED_BATCHES:
    _limited_dimension(limited_dimensions, "source identity")
  elif not _identity_supported(artifact, batch_id):
    _limited_dimension(limited_dimensions, "source identity")

  if batch_id == "v0.10.50-teachability-observation-capture":
    run_count, completed_run_count = _audit_v050(artifact, limited_dimensions)
  elif batch_id == "v0.10.51-adversarial-resource-probe":
    run_count, completed_run_count = _audit_v051(artifact, limited_dimensions)
  elif batch_id == "v0.10.52-decision-load-evidence":
    run_count, completed_run_count = _audit_v052(artifact, limited_dimensions)
  else:
    run_count, completed_run_count = len(_runs(artifact)), 0

  return {
    "source_path": source_path,
    "batch_id": batch_id,
    "code_version": artifact.get("code_version", "unknown") if isinstance(artifact, dict) else "unknown",
    "campaign": artifact.get("campaign", "unknown") if isinstance(artifact, dict) else "unknown",
    "expected_evidence": EXPECTED_BATCHES.get(batch_id, "unrecognized source"),
    "run_count": run_count,
    "completed_run_count": completed_run_count,
    "limited_dimensions": sorted(limited_dimensions),
    "status": "supported" if not limited_dimensions else "limited",
  }


def _matrix(artifact):
  return {
    (run.get("profile_id"), run.get("seed"))
    for run in _runs(artifact)
    if isinstance(run, dict)
  }


def _control_continuity(artifacts):
  by_batch = {
    artifact.get("batch_id"): artifact
    for artifact in artifacts
    if isinstance(artifact, dict)
  }
  capture = by_batch.get("v0.10.50-teachability-observation-capture", {})
  probe = by_batch.get(CONTROL_BATCH_ID, {})
  expected_controls = {
    (run.get("profile_name"), run.get("seed"), run.get("final_hash"))
    for run in _runs(capture)
    if isinstance(run, dict) and run.get("profile_id") == "first_time_executive"
  }
  observed_controls = {
    (run.get("profile_name"), run.get("seed"), run.get("final_hash"))
    for run in probe.get("control_runs", [])
    if isinstance(run, dict)
  }
  expected_profile = "First-Time Executive"
  supported = (
    probe.get("control_artifact") == CONTROL_ARTIFACT
    and len(expected_controls) == 3
    and len(observed_controls) == 3
    and all(
      profile_name.startswith(expected_profile)
      for profile_name, _, _ in observed_controls
    )
    and expected_controls == observed_controls
  )
  return {
    "status": "supported" if supported else "limited",
    "control_artifact": probe.get("control_artifact", "unknown"),
    "expected_member_count": len(expected_controls),
    "observed_member_count": len(observed_controls),
  }


def _matrix_continuity(artifacts):
  by_batch = {
    artifact.get("batch_id"): artifact
    for artifact in artifacts
    if isinstance(artifact, dict)
  }
  capture_matrix = _matrix(by_batch.get("v0.10.50-teachability-observation-capture", {}))
  pacing_matrix = _matrix(by_batch.get("v0.10.52-decision-load-evidence", {}))
  supported = capture_matrix == EXPECTED_MATRIX and pacing_matrix == EXPECTED_MATRIX
  return {
    "status": "supported" if supported else "limited",
    "expected_member_count": len(EXPECTED_MATRIX),
    "capture_member_count": len(capture_matrix),
    "pacing_member_count": len(pacing_matrix),
  }


def build_audit(paths=SOURCE_PATHS):
  sorted_paths = sorted(Path(path) for path in paths)
  artifacts = [load_artifact(path) for path in sorted_paths]
  reports = [
    audit_source(artifact, str(path.relative_to(ROOT)))
    for artifact, path in zip(artifacts, sorted_paths)
  ]
  observed_batches = {report["batch_id"] for report in reports}
  expected_batches = set(EXPECTED_BATCHES)
  missing_sources = sorted(expected_batches - observed_batches)
  unexpected_sources = sorted(observed_batches - expected_batches)
  source_gaps = [
    report["batch_id"]
    for report in reports
    if report["status"] != "supported"
  ]
  if missing_sources or unexpected_sources or source_gaps:
    source_coverage_status = "limited"
  else:
    source_coverage_status = "supported"
  source_coverage = {
    "status": source_coverage_status,
    "expected_source_count": len(expected_batches),
    "observed_source_count": len(reports),
    "missing_sources": missing_sources,
    "unexpected_sources": unexpected_sources,
    "limited_sources": sorted(source_gaps),
  }
  control_continuity = _control_continuity(artifacts)
  matrix_continuity = _matrix_continuity(artifacts)
  evidence_gaps = []
  if source_coverage["status"] != "supported":
    evidence_gaps.append({
      "type": "source coverage",
      "missing_sources": missing_sources,
      "unexpected_sources": unexpected_sources,
      "limited_sources": sorted(source_gaps),
    })
  if control_continuity["status"] != "supported":
    evidence_gaps.append({"type": "control continuity"})
  if matrix_continuity["status"] != "supported":
    evidence_gaps.append({"type": "matrix continuity"})
  if evidence_gaps:
    promotion_basis = (
      "Evidence coverage limitations were found; runtime promotion remains deferred "
      "until a separate player-facing, instructor-facing, or domain-review finding "
      "establishes an unexplained problem."
    )
  else:
    promotion_basis = (
      "The three source artifacts form a continuous descriptive evidence chain; "
      "no concrete unexplained player-facing, instructor-facing, or domain-review "
      "gap justifies runtime promotion."
    )
  return {
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "campaign": CAMPAIGN,
    "source_artifacts": [report["source_path"] for report in reports],
    "source_count": len(reports),
    "completed_source_count": sum(
      report["status"] == "supported" for report in reports
    ),
    "source_reports": reports,
    "source_coverage": source_coverage,
    "control_continuity": control_continuity,
    "matrix_continuity": matrix_continuity,
    "evidence_gaps": evidence_gaps,
    "evidence_gap_count": len(evidence_gaps),
    "runtime_promotion": "deferred",
    "promotion_basis": promotion_basis,
    "limitations": LIMITATIONS,
  }


def validate_audit(audit):
  assert audit["batch_id"] == BATCH_ID
  assert audit["code_version"] == CODE_VERSION
  assert audit["campaign"] == CAMPAIGN
  assert audit["source_count"] == 3
  assert audit["completed_source_count"] == 3
  assert audit["source_coverage"]["status"] == "supported"
  assert audit["control_continuity"]["status"] == "supported"
  assert audit["matrix_continuity"]["status"] == "supported"
  assert audit["evidence_gap_count"] == 0
  assert audit["runtime_promotion"] == "deferred"


def render_markdown(audit):
  lines = [
    f"# Phase 7 Evidence Synthesis {audit['code_version']}",
    "",
    f"- **Batch id:** {audit['batch_id']}",
    f"- **Campaign:** `{audit['campaign']}`",
    f"- **Source artifacts:** {audit['source_count']}",
    f"- **Supported source artifacts:** {audit['completed_source_count']} of {audit['source_count']}",
    "",
    "This is a deterministic read-only synthesis of existing evidence. It does not launch new sessions or change runtime behavior.",
    "",
    "## Source coverage",
    "",
    "| Source artifact | Expected evidence | Status | Limited dimensions |",
    "| --- | --- | --- | --- |",
  ]
  for report in audit["source_reports"]:
    limited = ", ".join(report["limited_dimensions"]) or "none"
    lines.append(
      f"| `{report['batch_id']}` | {report['expected_evidence']} | {report['status']} | {limited} |"
    )
  lines.extend([
    "",
    "## Continuity checks",
    "",
    f"Source coverage: `{audit['source_coverage']['status']}`.",
    f"Control continuity: `{audit['control_continuity']['status']}` for the v0.10.51 First-Time Executive controls.",
    f"Nine-member profile/seed matrix continuity: `{audit['matrix_continuity']['status']}`.",
    "",
    "## Promotion decision",
    "",
    f"Runtime promotion: {audit['runtime_promotion']}",
    "",
    audit["promotion_basis"],
    "",
    "The evidence chain describes visibility, validation compatibility, retries, and pacing proxies. It does not establish a causal strategy, balance, winnability, or educational claim.",
    "",
    "## Evidence gaps",
    "",
  ])
  if audit["evidence_gaps"]:
    lines.extend(
      f"- {json.dumps(gap, sort_keys=True)}"
      for gap in audit["evidence_gaps"]
    )
  else:
    lines.append("None identified.")
  lines.extend([
    "",
    "## Evidence limits",
    "",
  ])
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
  (output_dir / "audit.md").write_text(
    render_markdown(audit),
    encoding="utf-8",
  )


if __name__ == "__main__":
  main()
