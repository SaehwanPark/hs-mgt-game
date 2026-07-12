#!/usr/bin/env python3
"""Adapt the existing operating audit to the v0.11.11 artifact contract."""

import argparse
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.11.1-operating-loop-ai-validation"
  / "run_audit.py"
)
SPEC = importlib.util.spec_from_file_location(
  "current_all_tier_operating_audit",
  SOURCE_PATH,
)
SOURCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SOURCE)

SOURCE.ARTIFACT_TYPE = "post_change_all_tier_difficulty_validation"
SOURCE.BATCH_ID = "v0.11.11-phase7-post-change-all-tier-validation"
SOURCE.CODE_VERSION = "0.11.11"
SOURCE.CAMPAIGN = "competitive-regional-v1"
SOURCE.SEEDS = [42, 43, 44]
SOURCE.DIFFICULTIES = ["easy", "normal", "hard", "expert"]
SOURCE.PROFILES = [
  "Access First",
  "Commercial Focus",
  "Workforce Resilience",
  "Capital Modernization",
  "Coalition/Legitimacy",
]

load_artifact = SOURCE.load_artifact
build_audit = SOURCE.build_audit
validate_audit = SOURCE.validate_audit
render_markdown = SOURCE.render_markdown


def _metric_range(reports, metric):
  values = [
    report["final_outcomes"][metric]
    for report in reports
    if report.get("final_outcomes") and metric in report["final_outcomes"]
  ]
  if not values:
    return "N/A"
  return str(min(values)) if min(values) == max(values) else f"{min(values)}–{max(values)}"


def render_markdown(audit):
  lines = [SOURCE.render_markdown(audit).rstrip(), "", "## Strategy comparison", ""]
  lines.extend([
    "Profile and difficulty groupings below are descriptive simulated-policy "
    "diagnostics, not validated strategy classes or causal comparisons.",
    "",
    "| Profile | Runs | Distinct trajectories | Action families |",
    "| --- | ---: | ---: | --- |",
  ])
  for profile, counts in sorted(audit["action_counts_by_profile"].items()):
    reports = [
      report for report in audit["run_reports"] if report["profile"] == profile
    ]
    trajectories = {
      json.dumps(report["trajectory_signature"], sort_keys=True)
      for report in reports
    }
    lines.append(
      f"| {profile} | {len(reports)} | {len(trajectories)} | "
      f"{', '.join(sorted(counts))} |"
    )
  lines.extend([
    "",
    "| Difficulty | Runs | Distinct trajectories | Cash range | Access range | Workforce trust range |",
    "| --- | ---: | ---: | ---: | ---: | ---: |",
  ])
  for difficulty in SOURCE.DIFFICULTIES:
    reports = [
      report
      for report in audit["run_reports"]
      if report["difficulty"] == difficulty
    ]
    trajectories = {
      json.dumps(report["trajectory_signature"], sort_keys=True)
      for report in reports
    }
    lines.append(
      f"| {difficulty} | {len(reports)} | {len(trajectories)} | "
      f"{_metric_range(reports, 'cash')} | {_metric_range(reports, 'access')} | "
      f"{_metric_range(reports, 'workforce_trust')} |"
    )
  lines.append("")
  return "\n".join(lines)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "input",
    nargs="?",
    default=str(Path(__file__).with_name("results.json")),
  )
  parser.add_argument(
    "--output",
    default=str(Path(__file__).with_name("diagnostics.md")),
  )
  args = parser.parse_args()
  audit = build_audit(load_artifact(args.input))
  validate_audit(audit, strict=True)
  Path(args.output).write_text(render_markdown(audit), encoding="utf-8")
  print(f"All-tier diagnostics written to {args.output}")


if __name__ == "__main__":
  main()
