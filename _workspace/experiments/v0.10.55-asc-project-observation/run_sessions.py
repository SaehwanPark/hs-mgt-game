#!/usr/bin/env python3
"""Capture ASC project visibility evidence for v0.10.55."""

import importlib.util
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_RUNNER_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.10.54-project-limit-recovery"
  / "run_sessions.py"
)
SPEC = importlib.util.spec_from_file_location(
  "project_limit_recovery_v054", SOURCE_RUNNER_PATH
)
SOURCE_RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SOURCE_RUNNER)

SOURCE_RUNNER.BATCH_ID = "v0.10.55-asc-project-observation"
SOURCE_RUNNER.CODE_VERSION = "0.10.55"
SOURCE_RUNNER.SOURCE_ARTIFACT = (
  "_workspace/experiments/v0.10.54-project-limit-recovery/results.json"
)
SOURCE_RUNNER.SOURCE_BATCH_ID = "v0.10.54-project-limit-recovery"
SOURCE_RUNNER.SOURCE_CODE_VERSION = "0.10.54"
SOURCE_RUNNER.LIMITATIONS = [
  "An ASC project is a game abstraction, not an empirical health-system constraint.",
  "Visible project details show traceability, not human comprehension or learning.",
  "The three-seed Hard matrix does not establish balance, winnability, strategy quality, calibration, or policy validity.",
  "Project validation hints, runtime tuning, and broader project guidance remain deferred.",
]


def project_visibility(run):
  month_seven = next(
    trace for trace in run["turn_trace"] if trace["turn"] == 7
  )
  observation_text = "\n".join(month_seven["observation"])
  retry_text = "\n".join(month_seven["observation_after_failure"] or [])
  return {
    "turn": 7,
    "clinic_network_visible": "ClinicNetwork" in observation_text,
    "asc_unit_visible": "AscUnit" in observation_text,
    "clinic_network_visible_after_failure": "ClinicNetwork" in retry_text,
    "asc_unit_visible_after_failure": "AscUnit" in retry_text,
    "observation": month_seven["observation"],
    "observation_after_failure": month_seven["observation_after_failure"],
  }


def source_hashes_by_seed():
  source = json.loads(
    (ROOT / SOURCE_RUNNER.SOURCE_ARTIFACT).read_text(encoding="utf-8")
  )
  return {
    run["seed"]: run["state_hashes"]
    for run in source["runs"]
  }


def build_artifact(runs):
  artifact = SOURCE_RUNNER.build_artifact(runs)
  visibility = [project_visibility(run) for run in runs]
  artifact["evidence_type"] = (
    "deterministic actor-visible ASC project observation coverage"
  )
  artifact["project_observation"] = {
    "checked_turn": 7,
    "run_count": len(visibility),
    "asc_visible_count": sum(item["asc_unit_visible"] for item in visibility),
    "clinic_visible_count": sum(
      item["clinic_network_visible"] for item in visibility
    ),
    "asc_visible_after_failure_count": sum(
      item["asc_unit_visible_after_failure"] for item in visibility
    ),
    "runs": visibility,
  }
  return artifact


def validate_artifact(artifact):
  SOURCE_RUNNER.validate_artifact(artifact)
  visibility = artifact["project_observation"]
  assert visibility["checked_turn"] == 7
  assert visibility["run_count"] == len(SOURCE_RUNNER.SEEDS)
  assert visibility["asc_visible_count"] == len(SOURCE_RUNNER.SEEDS)
  assert visibility["clinic_visible_count"] == len(SOURCE_RUNNER.SEEDS)
  assert visibility["asc_visible_after_failure_count"] == len(SOURCE_RUNNER.SEEDS)

  source_hashes = source_hashes_by_seed()
  for run, observation in zip(artifact["runs"], visibility["runs"]):
    assert run["state_hashes"] == source_hashes[run["seed"]]
    assert observation["asc_unit_visible"]
    assert observation["clinic_network_visible"]
    assert observation["asc_unit_visible_after_failure"]
    assert observation["clinic_network_visible_after_failure"]


def render_diagnostics(artifact):
  text = SOURCE_RUNNER.render_diagnostics(artifact)
  text = text.replace(
    "# Project-Limit Recovery Diagnostics v0.10.54",
    "# ASC Project Observation Diagnostics v0.10.55",
  )
  text = text.replace(
    "deterministic actor-visible project-limit recovery capture",
    "deterministic actor-visible ASC project observation capture",
  )
  summary = artifact["project_observation"]
  marker = "## Evidence Limits"
  section = "\n".join([
    "## Project Observation Coverage",
    "",
    f"- ASC project visible at month 7: {summary['asc_visible_count']}/{summary['run_count']} runs.",
    f"- ClinicNetwork visible at month 7: {summary['clinic_visible_count']}/{summary['run_count']} runs.",
    f"- Both projects remain visible after the rejected third-project command: {summary['asc_visible_after_failure_count']}/{summary['run_count']} runs.",
    "- State-hash sequences match the v0.10.54 source artifact; the correction changes observation text only.",
    "",
  ])
  return text.replace(marker, section + marker)


def main():
  os.chdir(ROOT)
  if SOURCE_RUNNER.code_version() != SOURCE_RUNNER.CODE_VERSION:
    raise RuntimeError(
      f"expected Cargo.toml version {SOURCE_RUNNER.CODE_VERSION}"
    )
  subprocess.run(
    ["cargo", "build", "--quiet", "--bin", "hs-mgt-game-mcp"],
    cwd=ROOT,
    check=True,
  )
  runs = []
  for seed in SOURCE_RUNNER.SEEDS:
    print(
      f"Running ASC project observation / {SOURCE_RUNNER.DIFFICULTY} / seed {seed}...",
      flush=True,
    )
    runs.append(SOURCE_RUNNER.run_session(seed))

  artifact = build_artifact(runs)
  validate_artifact(artifact)
  output_dir = Path(__file__).parent
  (output_dir / "results.json").write_text(
    json.dumps(artifact, indent=2) + "\n",
    encoding="utf-8",
  )
  (output_dir / "diagnostics.md").write_text(
    render_diagnostics(artifact),
    encoding="utf-8",
  )
  print(f"Wrote {output_dir / 'results.json'}")
  print(f"Wrote {output_dir / 'diagnostics.md'}")


if __name__ == "__main__":
  main()
