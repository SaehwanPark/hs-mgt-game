#!/usr/bin/env python3
"""Audit strategy variation in an existing competitive evidence artifact."""

from collections import Counter
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BATCH_ID = "v0.10.48-strategy-diversity-evidence"
CODE_VERSION = "0.10.48"
CAMPAIGN = "competitive-regional-v1"
SOURCE_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.10.46-expert-clearability-evidence"
  / "results.json"
)
EXPECTED_PROFILES = [
  "Fiscal Caution",
  "Capacity Growth",
  "Balanced Strategy",
  "Naive First-Time",
]
EXPECTED_SEEDS = [42, 43, 44]
KNOWN_VERBS = {
  "monitor",
  "recruit",
  "invest",
  "negotiate",
  "commit",
  "project",
  "hold",
}
REQUIRED_TRACE_FIELDS = {
  "turn",
  "submitted_command",
  "latest_transition",
}
TRADEOFF_PATTERN = re.compile(
  r"cash moved from -?\d+ to (-?\d+), access from \d+ to (\d+), "
  r"quality from \d+ to (\d+), workforce trust from \d+ to (\d+), "
  r"community trust from \d+ to (\d+), and market share from \d+ to (\d+)"
)
LIMITATIONS = [
  "This is descriptive strategy-trace evidence, not a causal comparison.",
  "The source contains deterministic simulated-policy traces, not human or classroom sessions.",
  "A common action is a candidate dominance signal only; it is not proof of an optimal strategy.",
  "The tested profiles, seeds, and difficulty do not establish general balance, learning, or policy validity.",
]


def load_artifact(path=SOURCE_PATH):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def _argument(raw_command, name):
  match = re.search(rf"(?:^|\s){re.escape(name)}=([^\s]+)", raw_command)
  return match.group(1).lower() if match else ""


def _family(verb, raw_command):
  if verb == "hold":
    return "hold"
  argument_name = {
    "monitor": "target",
    "recruit": "role",
    "invest": "domain",
    "negotiate": "payer",
    "commit": "pledge_type",
    "project": "kind",
  }.get(verb)
  value = _argument(raw_command, argument_name) if argument_name else ""
  return f"{verb}:{value}" if value else verb


def parse_commands(command_text):
  commands = []
  for raw in str(command_text or "").split(";"):
    text = raw.strip()
    if not text:
      continue
    parts = text.split(maxsplit=1)
    verb = parts[0].lower()
    commands.append(
      {
        "raw": text,
        "verb": verb if verb in KNOWN_VERBS else "unknown",
        "family": _family(verb, text) if verb in KNOWN_VERBS else "unknown",
      }
    )
  return commands


def _final_tradeoff(debrief):
  for line in debrief or []:
    match = TRADEOFF_PATTERN.search(str(line))
    if match:
      values = [int(value) for value in match.groups()]
      return {
        "cash": values[0],
        "access": values[1],
        "quality": values[2],
        "workforce_trust": values[3],
        "community_trust": values[4],
        "market_share": values[5],
      }
  return None


def audit_run(run):
  trace = run.get("turn_trace", []) or []
  debrief = run.get("debrief", []) or []
  commands = []
  trajectory = []

  for entry in trace:
    turn_commands = parse_commands(entry.get("submitted_command", ""))
    commands.extend(
      {"turn": entry.get("turn"), **command}
      for command in turn_commands
    )
    trajectory.append(
      {
        "turn": entry.get("turn"),
        "families": [command["family"] for command in turn_commands],
      }
    )

  family_counts = Counter(
    command["family"] for command in commands if command["verb"] != "unknown"
  )
  non_hold_count = sum(command["verb"] != "hold" for command in commands)
  unknown_commands = [command for command in commands if command["verb"] == "unknown"]
  missing_trace_fields = [
    entry.get("turn")
    for entry in trace
    if not REQUIRED_TRACE_FIELDS <= set(entry)
  ]
  player_debrief_count = sum(
    isinstance(line, str) and line.startswith("Player:")
    for line in debrief
  )
  turn_count = len(trace)
  hold_rate = round(
    (len(commands) - non_hold_count) / len(commands),
    4,
  ) if commands else 0
  status = (
    "supported"
    if not unknown_commands and not missing_trace_fields and player_debrief_count
    else "limited"
  )

  return {
    "profile_name": run.get("profile_name", "unknown"),
    "seed": run.get("seed"),
    "difficulty": run.get("difficulty"),
    "completion_status": run.get("completion_status", "unknown"),
    "transition_count": run.get("transition_count", 0),
    "validation_failure_count": len(run.get("validation_failures", []) or []),
    "turn_count": turn_count,
    "command_count": len(commands),
    "non_hold_command_count": non_hold_count,
    "hold_rate": hold_rate,
    "action_family_counts": dict(sorted(family_counts.items())),
    "distinct_action_family_count": len(family_counts),
    "first_turn_families": trajectory[0]["families"] if trajectory else [],
    "trajectory": trajectory,
    "unknown_commands": unknown_commands,
    "missing_trace_fields": missing_trace_fields,
    "player_debrief_count": player_debrief_count,
    "final_tradeoff": _final_tradeoff(debrief),
    "status": status,
  }


def _profile_summary(runs):
  profiles = {}
  for run in runs:
    profile = run["profile_name"]
    summary = profiles.setdefault(
      profile,
      {
        "seeds": [],
        "distinct_trajectories": set(),
        "action_families": set(),
        "first_turn_families": set(),
      },
    )
    summary["seeds"].append(run["seed"])
    summary["distinct_trajectories"].add(
      json.dumps(run["trajectory"], sort_keys=True)
    )
    summary["action_families"].update(run["action_family_counts"])
    summary["first_turn_families"].update(run["first_turn_families"])

  return {
    profile: {
      "seeds": sorted(values["seeds"]),
      "distinct_trajectory_count": len(values["distinct_trajectories"]),
      "action_families": sorted(values["action_families"]),
      "first_turn_families": sorted(values["first_turn_families"]),
    }
    for profile, values in sorted(profiles.items())
  }


def build_audit(path=SOURCE_PATH):
  source = load_artifact(path)
  runs = [audit_run(run) for run in source.get("runs", [])]
  profile_summary = _profile_summary(runs)
  first_turn_sets = [
    set(summary["first_turn_families"])
    for summary in profile_summary.values()
  ]
  common_first_turn_families = (
    sorted(set.intersection(*first_turn_sets)) if first_turn_sets else []
  )
  return {
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "campaign": source.get("campaign", CAMPAIGN),
    "source_artifact": str(Path(path).relative_to(ROOT)),
    "profiles": source.get("profiles", []),
    "seeds": source.get("seeds", []),
    "difficulty": source.get("difficulty"),
    "run_count": len(runs),
    "completed_run_count": sum(
      run["completion_status"] == "complete" for run in runs
    ),
    "distinct_trajectory_count": len({
      json.dumps(run["trajectory"], sort_keys=True) for run in runs
    }),
    "profile_summary": profile_summary,
    "common_first_turn_families": common_first_turn_families,
    "runs": runs,
    "limitations": LIMITATIONS,
  }


def validate_audit(audit):
  assert audit["batch_id"] == BATCH_ID
  assert audit["code_version"] == CODE_VERSION
  assert audit["campaign"] == CAMPAIGN
  assert audit["profiles"] == EXPECTED_PROFILES
  assert audit["seeds"] == EXPECTED_SEEDS
  assert audit["run_count"] == len(audit["runs"])
  observed_matrix = {
    (run["profile_name"], run["seed"])
    for run in audit["runs"]
  }
  expected_matrix = {
    (profile, seed)
    for profile in EXPECTED_PROFILES
    for seed in EXPECTED_SEEDS
  }
  assert observed_matrix == expected_matrix

  for run in audit["runs"]:
    assert run["status"] in {"supported", "limited"}
    assert run["command_count"] == sum(
      len(turn["families"]) for turn in run["trajectory"]
    )
    assert run["distinct_action_family_count"] == len(
      run["action_family_counts"]
    )
    assert isinstance(run["final_tradeoff"], (dict, type(None)))


def render_markdown(audit):
  lines = [
    "# Strategy-Diversity Evidence Audit v0.10.48",
    "",
    f"- **Batch id:** {audit['batch_id']}",
    f"- **Campaign:** `{audit['campaign']}`",
    f"- **Difficulty:** `{audit['difficulty']}`",
    f"- **Source artifact:** `{audit['source_artifact']}`",
    f"- **Runs reviewed:** {audit['completed_run_count']} of {audit['run_count']}",
    "",
    "This deterministic read-only audit compares command-family trajectories and",
    "descriptive tradeoff records across existing simulated-policy runs. It does",
    "not infer causality, optimal strategy, or human learning.",
    "",
    "## Profile summary",
    "",
    "| Profile | Seeds | Distinct trajectories | Action families | First-turn families |",
    "| --- | --- | ---: | ---: | --- |",
  ]
  for profile, summary in audit["profile_summary"].items():
    lines.append(
      f"| {profile} | {', '.join(str(seed) for seed in summary['seeds'])} | "
      f"{summary['distinct_trajectory_count']} | "
      f"{len(summary['action_families'])} | "
      f"{', '.join(summary['first_turn_families'])} |"
    )
  lines.extend([
    "",
    "## Run summary",
    "",
    "| Profile | Seed | Status | Commands | Non-hold | Hold rate | Tradeoff record |",
    "| --- | ---: | --- | ---: | ---: | ---: | --- |",
  ])
  for run in audit["runs"]:
    lines.append(
      f"| {run['profile_name']} | {run['seed']} | {run['status']} | "
      f"{run['command_count']} | {run['non_hold_command_count']} | "
      f"{run['hold_rate']:.4f} | "
      f"{'present' if run['final_tradeoff'] else 'missing'} |"
    )
  lines.extend([
    "",
    "## Common first-turn action screen",
    "",
    "The following families appeared in every profile's first-turn family set:",
    "",
  ])
  if audit["common_first_turn_families"]:
    lines.extend(f"- `{family}`" for family in audit["common_first_turn_families"])
  else:
    lines.append("- None.")
  lines.extend([
    "",
    "This is a candidate common-action signal only. It is not evidence that an",
    "action dominates, improves outcomes, or should be made mandatory.",
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
  (output_dir / "diagnostics.md").write_text(
    render_markdown(audit),
    encoding="utf-8",
  )


if __name__ == "__main__":
  main()
