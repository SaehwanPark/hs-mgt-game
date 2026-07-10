import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT / "scripts"))

from play_game import play_session  # noqa: E402
from run_automated_playtests import (  # noqa: E402
  TARGET_DIFFICULTY_SWEEP,
  code_version,
  policy_for_competitive,
  strategies_for_target,
)

BATCH_ID = "v0.10.40-consultant-advice-evidence"
CAMPAIGN = "competitive-regional-v1"
SEEDS = [42, 43, 44]
DIFFICULTIES = ["normal", "hard"]
EXPECTED_TRANSITIONS = 24
OPTION_RE = re.compile(r"^Option ([A-D]) — (.+)$")
TRADEOFF_RE = re.compile(r"^\s*Tradeoff: (.+)$")
COMMAND_OPTION = {
  "invest": "A",
  "recruit": "B",
  "monitor": "C",
  "commit": "D",
}


def parse_rendered_options(observation):
  options = []
  current = None
  for line in observation:
    match = OPTION_RE.match(line)
    if match:
      current = {
        "label": match.group(1),
        "title": match.group(2),
        "tradeoff_bullets": [],
      }
      options.append(current)
      continue
    match = TRADEOFF_RE.match(line)
    if match and current is not None:
      current["tradeoff_bullets"].append(match.group(1))
  return options


def normalize_options(options):
  return [
    {
      "label": option["label"],
      "title": option["title"],
      "tradeoff_bullets": option["tradeoff_bullets"],
    }
    for option in options
  ]


def command_alignment(command):
  aligned = []
  for part in command.lower().split(";"):
    verb = part.strip().split(maxsplit=1)[0] if part.strip() else ""
    if verb in COMMAND_OPTION:
      aligned.append(COMMAND_OPTION[verb])
  return aligned or ["none"]


def run_profile(seed, difficulty, name, policy):
  result = play_session(
    CAMPAIGN,
    seed=seed,
    difficulty=difficulty,
    policy_fn=policy_for_competitive(policy, difficulty, TARGET_DIFFICULTY_SWEEP),
    capture_trace=True,
  )
  if result is None:
    raise RuntimeError(f"No result for {name}/{seed}/{difficulty}")

  exact_matches = 0
  rendered_counts = Counter()
  stored_counts = Counter()
  alignment_counts = Counter()
  debrief_count = sum(
    "Consultant options shown:" in line for line in result["debrief"]
  )
  debrief_consultant_lines = [
    line for line in result["debrief"] if "Consultant options shown:" in line
  ]
  option_signatures = set()
  trace_rows = []

  for entry in result["turn_trace"]:
    transition = entry.get("latest_transition")
    if transition is None:
      continue
    rendered = parse_rendered_options(entry["observation"])
    stored = transition.get("consultant_options", [])
    normalized_rendered = normalize_options(rendered)
    normalized_stored = normalize_options(stored)
    if normalized_rendered == normalized_stored:
      exact_matches += 1
    rendered_counts[len(rendered)] += 1
    stored_counts[len(stored)] += 1
    option_signatures.add(tuple(option["title"] for option in stored))
    for label in command_alignment(entry["submitted_command"]):
      alignment_counts[label] += 1
    trace_rows.append({
      "turn": entry["turn"],
      "command": entry["submitted_command"],
      "rendered_option_count": len(rendered),
      "stored_option_count": len(stored),
      "rendered_matches_stored": normalized_rendered == normalized_stored,
      "rendered_options": normalized_rendered,
      "stored_options": normalized_stored,
    })

  return {
    "profile_name": name,
    "seed": seed,
    "difficulty": difficulty,
    "completion_status": (
      "complete" if len(result["history"]) == EXPECTED_TRANSITIONS else "incomplete"
    ),
    "transition_count": len(result["history"]),
    "validation_failures": result["validation_failures"],
    "state_hashes": [transition["state_hash"] for transition in result["history"]],
    "final_hash": result["history"][-1]["state_hash"] if result["history"] else None,
    "rendered_option_counts": dict(rendered_counts),
    "stored_option_counts": dict(stored_counts),
    "exact_observation_history_matches": exact_matches,
    "debrief_option_lines": debrief_count,
    "debrief_consultant_lines": debrief_consultant_lines,
    "distinct_option_signatures": len(option_signatures),
    "command_alignment_signal": dict(alignment_counts),
    "turn_trace": trace_rows,
  }


def render_diagnostics(artifact):
  lines = [
    f"# Consultant Advice Diagnostics for `{artifact['filename']}`",
    f"- **Batch id:** {artifact['batch_id']}",
    f"- **Code version:** {artifact['code_version']}",
    f"- **Campaign:** {artifact['campaign']}",
    f"- **Seeds:** {', '.join(str(seed) for seed in artifact['seeds'])}",
    f"- **Difficulties:** {', '.join(artifact['difficulties'])}",
    "- **Evidence type:** deterministic MCP capture of rendered consultant options, committed history, submitted commands, and debriefs",
    "",
    "## Run Results",
    "| Profile | Seed | Difficulty | Status | Months | Validation failures | Exact option/history matches | Debrief option lines | Distinct option signatures | Final hash |",
    "| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
  ]
  for run in artifact["runs"]:
    lines.append(
      f"| {run['profile_name']} | {run['seed']} | {run['difficulty']} | "
      f"{run['completion_status']} | {run['transition_count']} | "
      f"{len(run['validation_failures'])} | {run['exact_observation_history_matches']} | "
      f"{run['debrief_option_lines']} | {run['distinct_option_signatures']} | "
      f"{run['final_hash']} |"
    )
  lines.extend([
    "",
    "## Command-Alignment Signals",
    "The labels below are descriptive mappings from command families to the generic option categories; they do not measure advice uptake, advice quality, or learning.",
    "",
    "| Profile | Seed | Difficulty | A / invest | B / recruit | C / monitor | D / commit | None |",
    "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |",
  ])
  for run in artifact["runs"]:
    signal = run["command_alignment_signal"]
    lines.append(
      f"| {run['profile_name']} | {run['seed']} | {run['difficulty']} | "
      f"{signal.get('A', 0)} | {signal.get('B', 0)} | {signal.get('C', 0)} | "
      f"{signal.get('D', 0)} | {signal.get('none', 0)} |"
    )
  lines.extend([
    "",
    "## Evidence Limits",
    "- These runs test observation/history/debrief traceability, not consultant effectiveness.",
    "- Existing scripted profiles are repeated deterministic controls, not independent human-player samples.",
    "- Final metrics and hashes verify reproducibility and regression safety; they do not establish causal advice value.",
    "- Any runtime or rendering mismatch must be routed to a separate implementation slice rather than fixed by changing the evidence wrapper.",
  ])
  return "\n".join(lines) + "\n"


def validate_runs(runs):
  for run in runs:
    name = f"{run['profile_name']}/{run['seed']}/{run['difficulty']}"
    if run["completion_status"] != "complete":
      raise RuntimeError(f"{name}: incomplete competitive session")
    if run["validation_failures"]:
      raise RuntimeError(f"{name}: validation failures were captured")
    if run["exact_observation_history_matches"] != EXPECTED_TRANSITIONS:
      raise RuntimeError(f"{name}: rendered and committed options diverged")
    if run["rendered_option_counts"] != {4: EXPECTED_TRANSITIONS}:
      raise RuntimeError(f"{name}: expected four rendered options per month")
    if run["stored_option_counts"] != {4: EXPECTED_TRANSITIONS}:
      raise RuntimeError(f"{name}: expected four stored options per month")
    if run["debrief_option_lines"] != EXPECTED_TRANSITIONS:
      raise RuntimeError(f"{name}: debrief did not retain every advisory record")


def main():
  os.chdir(ROOT)
  subprocess.run(
    ["cargo", "build", "--quiet", "--bin", "hs-mgt-game-mcp"],
    check=True,
  )
  runs = []
  for seed in SEEDS:
    for difficulty in DIFFICULTIES:
      for name, policy in strategies_for_target(TARGET_DIFFICULTY_SWEEP).items():
        runs.append(run_profile(seed, difficulty, name, policy))

  validate_runs(runs)

  artifact = {
    "filename": "results.json",
    "batch_id": BATCH_ID,
    "code_version": code_version(),
    "campaign": CAMPAIGN,
    "seeds": SEEDS,
    "difficulties": DIFFICULTIES,
    "profiles": [run["profile_name"] for run in runs[0:4]],
    "evidence_type": "deterministic consultant advice traceability capture",
    "runs": runs,
  }
  output_dir = Path(__file__).parent
  (output_dir / "results.json").write_text(
    json.dumps(artifact, indent=2) + "\n", encoding="utf-8"
  )
  (output_dir / "diagnostics.md").write_text(
    render_diagnostics(artifact), encoding="utf-8"
  )
  print(f"wrote {output_dir / 'results.json'}")
  print(f"wrote {output_dir / 'diagnostics.md'}")


if __name__ == "__main__":
  main()
