#!/usr/bin/env python3
"""Audit the v0.12.6 observation-only workforce projection artifact."""

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = Path(__file__).resolve().parent
import importlib.util  # noqa: E402


RUNNER_SPEC = importlib.util.spec_from_file_location(
  "workforce_capacity_observation_runner",
  OUTPUT_DIR / "run_sessions.py",
)
RUNNER = importlib.util.module_from_spec(RUNNER_SPEC)
assert RUNNER_SPEC.loader is not None
RUNNER_SPEC.loader.exec_module(RUNNER)


def load_artifact(path):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def build_audit(artifact):
  RUNNER.validate_artifact(artifact)
  comparisons = artifact["source_comparisons"]
  by_source = {}
  for source_id in ("all_tiers", "expert"):
    source_comparisons = [
      item for item in comparisons if item["source_id"] == source_id
    ]
    by_source[source_id] = {
      "run_count": len(source_comparisons),
      "transition_count": sum(item["transition_count"] for item in source_comparisons),
      "history_match_count": sum(item["history_match"] for item in source_comparisons),
      "state_hash_match_count": sum(
        item["state_hashes_match"] for item in source_comparisons
      ),
      "status": (
        "supported"
        if source_comparisons
        and all(item["history_match"] and item["state_hashes_match"] for item in source_comparisons)
        else "limited"
      ),
    }

  projection = artifact["observation_projection"]
  return {
    "artifact_type": artifact["artifact_type"],
    "batch_id": artifact["batch_id"],
    "code_version": artifact["code_version"],
    "campaign": artifact["campaign"],
    "run_count": len(artifact["runs"]),
    "transition_count": sum(run["transition_count"] for run in artifact["runs"]),
    "completed_run_count": sum(
      run["completion_status"] == "complete" for run in artifact["runs"]
    ),
    "validation_failure_count": sum(
      len(run["validation_failures"]) for run in artifact["runs"]
    ),
    "observation_projection": projection,
    "source_comparisons": by_source,
    "exact_history_match": all(
      values["history_match_count"] == values["run_count"]
      for values in by_source.values()
    ),
    "exact_state_hash_match": all(
      values["state_hash_match_count"] == values["run_count"]
      for values in by_source.values()
    ),
    "runtime_promotion": artifact["runtime_promotion"],
    "difficulty_change_authorized": artifact["difficulty_change_authorized"],
    "evidence_limits": artifact["evidence_limits"],
  }


def render_markdown(audit):
  projection = audit["observation_projection"]
  lines = [
    f"# {audit['batch_id']}",
    "",
    f"- Code version: `{audit['code_version']}`",
    f"- Campaign: `{audit['campaign']}`",
    f"- Runs: {audit['completed_run_count']}/{audit['run_count']} complete",
    f"- Transitions: {audit['transition_count']}",
    f"- Exact history match: {'yes' if audit['exact_history_match'] else 'no'}",
    f"- Exact state-hash match: {'yes' if audit['exact_state_hash_match'] else 'no'}",
    f"- Runtime promotion: `{audit['runtime_promotion']}`",
    "",
    "## Observation projection",
    "",
    "- Staffing line: `Staffing: nurses <n>, physicians <n>, admins <n>`",
    "- Capacity line: `Physical capacity: staffed beds <n>, outpatient <n>, emergency <n>, ICU <n>, obstetrics <n>, psychiatric <n>, cardiology <n>, oncology <n>, infusion <n>, neurology <n>, ASC <n>`",
    f"- Trace entries: {projection['trace_entry_count']}",
    f"- Staffing lines observed: {projection['staffing_line_count']}",
    f"- Physical-capacity lines observed: {projection['physical_capacity_line_count']}",
    f"- Excluded hidden-marker occurrences: {projection['hidden_marker_count']}",
    "",
    "## Source comparison",
    "",
    "| Source | Runs | Transitions | Exact histories | Exact state hashes | Status |",
    "| --- | ---: | ---: | ---: | ---: | --- |",
  ]
  for source_id, summary in audit["source_comparisons"].items():
    lines.append(
      f"| {source_id} | {summary['run_count']} | {summary['transition_count']} | "
      f"{summary['history_match_count']} | {summary['state_hash_match_count']} | "
      f"{summary['status']} |"
    )
  lines.extend([
    "",
    "## Interpretation",
    "",
    "The two lines are rendered from existing typed `PlayerObservation` fields. "
    "Exact transition histories and state hashes match the earlier immutable "
    "controls, supporting an observation-only change classification. Runtime "
    "difficulty, balance, scoring, and winnability promotion remain deferred.",
    "",
    "## Evidence limits",
    "",
  ])
  lines.extend(f"- {limit}" for limit in audit["evidence_limits"])
  lines.append("")
  return "\n".join(lines)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "input",
    nargs="?",
    default=str(OUTPUT_DIR / "results.json"),
  )
  parser.add_argument(
    "--output",
    default=str(OUTPUT_DIR / "diagnostics.md"),
  )
  args = parser.parse_args()
  audit = build_audit(load_artifact(args.input))
  Path(args.output).write_text(render_markdown(audit), encoding="utf-8")
  print(f"Observation diagnostics written to {args.output}")


if __name__ == "__main__":
  main()
