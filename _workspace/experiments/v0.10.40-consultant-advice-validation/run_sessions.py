import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT / "scripts"))

from play_game import play_session  # noqa: E402
from run_automated_playtests import (  # noqa: E402
  code_version,
  parse_competitive_metrics,
  policy_balanced,
  policy_fiscal,
  policy_growth,
  policy_naive_first_time,
)


BATCH_ID = "v0.10.40-consultant-advice-validation"
CAMPAIGN = "competitive-regional-v1"
SEEDS = [42, 43, 44]
DIFFICULTIES = ["normal", "hard"]
EXPECTED_TRANSITIONS = 24
OPTION_LABELS = ("A", "B", "C", "D")
POLICIES = {
  "Fiscal Caution": policy_fiscal,
  "Capacity Growth": policy_growth,
  "Balanced Strategy": policy_balanced,
  "Naive First-Time": policy_naive_first_time,
}


def parse_observation_options(observation):
  header = "STRATEGY CONSULTANT NOTES — Advisory, not binding"
  errors = []
  if header not in observation:
    errors.append("missing consultant header")

  options = []
  current = None
  for line in observation:
    stripped = line.strip()
    match = re.fullmatch(r"Option ([A-D]) — (.+)", stripped)
    if match:
      current = {
        "label": match.group(1),
        "title": match.group(2),
        "tradeoff_bullets": [],
      }
      options.append(current)
      continue
    if stripped.startswith("Tradeoff: ") and current is not None:
      current["tradeoff_bullets"].append(stripped.removeprefix("Tradeoff: "))

  labels = [option["label"] for option in options]
  if labels != list(OPTION_LABELS):
    errors.append(f"option labels were {labels!r}, expected {list(OPTION_LABELS)!r}")
  for option in options:
    if not option["title"]:
      errors.append(f"option {option['label']} has an empty title")
    if not option["tradeoff_bullets"]:
      errors.append(f"option {option['label']} has no tradeoff bullet")
    if "optimal" in option["title"].lower() or "correct" in option["title"].lower():
      errors.append(f"option {option['label']} is presented as ranked or correct")

  context = tuple(
    line.strip()
    for line in observation
    if line.strip().startswith((
      "Cash runway:",
      "Workforce trust:",
      "Community trust:",
      "Intel gap:",
    ))
  )
  signature = tuple(
    (option["label"], option["title"], tuple(option["tradeoff_bullets"]))
    for option in options
  )
  return options, context, signature, errors


def parse_debrief_options(debrief):
  month_options = {}
  month_comparisons = set()
  current_month = None
  option_pattern = re.compile(r"([A-D]) — (.*?)(?=; [A-D] — |$)")

  for line in debrief:
    month_match = re.fullmatch(r"--- Month (\d+) ---", line.strip())
    if month_match:
      current_month = int(month_match.group(1))
      continue
    if current_month is None:
      continue
    if line.startswith("Consultant options shown: "):
      month_options[current_month] = {
        label: title.strip()
        for label, title in option_pattern.findall(
          line.removeprefix("Consultant options shown: ")
        )
      }
    if line.startswith("Advisory comparison: "):
      month_comparisons.add(current_month)

  return month_options, month_comparisons


def final_hash(result):
  return result["history"][-1]["state_hash"] if result.get("history") else None


def run_case(seed, difficulty, profile_name, policy):
  result = play_session(
    CAMPAIGN,
    seed=seed,
    difficulty=difficulty,
    policy_fn=policy,
    capture_trace=True,
  )
  if result is None:
    raise RuntimeError("play_session returned no result")

  trace = result.get("turn_trace", [])
  accepted = [entry for entry in trace if entry.get("latest_transition") is not None]
  run_errors = []
  signatures = set()
  contexts = {}
  advice_months = {}

  for entry in accepted:
    options, context, signature, errors = parse_observation_options(
      entry.get("observation", [])
    )
    month = entry["turn"]
    advice_months[month] = {
      "context": context,
      "options": options,
      "signature": signature,
      "submitted_command": entry["submitted_command"],
    }
    signatures.add(signature)
    contexts.setdefault(context, set()).add(signature)
    run_errors.extend(f"month {month}: {error}" for error in errors)

  debrief_options, debrief_comparisons = parse_debrief_options(result["debrief"])
  if len(accepted) != EXPECTED_TRANSITIONS:
    run_errors.append(
      f"accepted transitions were {len(accepted)}, expected {EXPECTED_TRANSITIONS}"
    )
  if result["validation_failures"]:
    run_errors.append(
      f"validation failures were recorded: {len(result['validation_failures'])}"
    )
  if len(advice_months) != EXPECTED_TRANSITIONS:
    run_errors.append(
      f"advice observations covered {len(advice_months)} months, expected {EXPECTED_TRANSITIONS}"
    )
  if len(debrief_options) != EXPECTED_TRANSITIONS:
    run_errors.append(
      f"debrief retained {len(debrief_options)} option lines, expected {EXPECTED_TRANSITIONS}"
    )
  if debrief_comparisons != set(range(1, EXPECTED_TRANSITIONS + 1)):
    run_errors.append("debrief advisory-comparison lines did not cover every month")

  for month, evidence in advice_months.items():
    retained = debrief_options.get(month, {})
    expected = {option["label"]: option["title"] for option in evidence["options"]}
    if retained != expected:
      run_errors.append(f"month {month}: debrief titles differ from observed titles")

  if len(signatures) < 2:
    run_errors.append("no state-conditioned option variation was observed")
  if len(contexts) < 2:
    run_errors.append("fewer than two visible observation contexts were observed")
  if any(len(context_signatures) != 1 for context_signatures in contexts.values()):
    run_errors.append(
      "the same visible observation context produced multiple option signatures"
    )

  metrics = parse_competitive_metrics(
    result["final_observation"],
    result["history"],
    result["debrief"],
  )
  return {
    "profile_id": re.sub(r"[^a-z0-9]+", "_", profile_name.lower()).strip("_"),
    "profile_name": f"{profile_name} / {difficulty} / seed {seed}",
    "decision_source": (
      "existing deterministic policy from actor-visible MCP observations and "
      "legal command hints; consultant text was captured, not scored"
    ),
    "policy": profile_name,
    "seed": seed,
    "difficulty": difficulty,
    "completion_status": "complete" if not run_errors else "failed",
    "turn_trace": trace,
    "commands": [entry["submitted_command"] for entry in accepted],
    "validation_failures": result["validation_failures"],
    "transition_count": len(result["history"]),
    "state_hashes": [transition["state_hash"] for transition in result["history"]],
    "final_hash": final_hash(result),
    "final_observation": result["final_observation"],
    "debrief": result["debrief"],
    "advice_month_count": len(advice_months),
    "debrief_option_month_count": len(debrief_options),
    "debrief_comparison_month_count": len(debrief_comparisons),
    "distinct_option_signature_count": len(signatures),
    "visible_context_count": len(contexts),
    "metrics": metrics,
    "assertion_errors": run_errors,
  }


def diagnostics_markdown(artifact):
  lines = [
    f"# Consultant Advice Validation Diagnostics — `{artifact['batch_id']}`",
    "",
    f"- Code version: `{artifact['code_version']}`",
    f"- Campaign: `{artifact['campaign']}`",
    f"- Matrix: four existing policies × seeds `{artifact['seeds']}` × difficulties `{artifact['difficulties']}`",
    "- Evidence type: simulated-agent MCP traceability and debrief-retention validation",
    "",
    "## Run outcomes",
    "",
    "| Profile | Status | Months | Advice months | Debrief options | Debrief comparisons | Signatures | Validation failures | Final hash |",
    "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
  ]
  for run in artifact["runs"]:
    lines.append(
      f"| {run['profile_name']} | {run['completion_status']} | "
      f"{run['transition_count']} | {run['advice_month_count']} | "
      f"{run['debrief_option_month_count']} | {run['debrief_comparison_month_count']} | "
      f"{run['distinct_option_signature_count']} | {len(run['validation_failures'])} | "
      f"{run['final_hash']} |"
    )
  lines.extend([
    "",
    "## Interpretation",
    "",
    "- The capture verifies that the existing advice surface is present, varies with visible observation categories, and remains available for month-by-month debrief comparison.",
    "- Submitted commands are retained beside the options for discussion; this artifact does not score advice adherence or identify a correct action.",
    "- Normal/Hard coverage exercises the same observation boundary under two fixtures; it is not a difficulty, balance, or Expert-winnability claim.",
    "",
    "## Evidence limits",
    "",
    "- These are deterministic simulated-agent policies, not human classroom observations.",
    "- Repeated policy/seed coverage is evidence about reproducibility and inspectability, not independent player samples.",
    "- No advice-quality, learning, calibration, policy-validity, or advisor-market conclusion is made.",
    "- No runtime tuning, roster, payroll, hiring, AI advice behavior, or transition change is justified by this artifact alone.",
  ])
  return "\n".join(lines) + "\n"


def main():
  os.chdir(ROOT)
  subprocess.run(
    ["cargo", "build", "--quiet", "--bin", "hs-mgt-game-mcp"],
    check=True,
  )

  runs = []
  for difficulty in DIFFICULTIES:
    for seed in SEEDS:
      for profile_name, policy in POLICIES.items():
        print(f"Running {profile_name} / {difficulty} / seed {seed}...")
        runs.append(run_case(seed, difficulty, profile_name, policy))

  artifact = {
    "batch_id": BATCH_ID,
    "code_version": code_version(),
    "campaign": CAMPAIGN,
    "seeds": SEEDS,
    "difficulties": DIFFICULTIES,
    "profiles": list(POLICIES),
    "evidence_type": (
      "simulated-agent MCP traceability validation for deterministic consultant "
      "options and retained competitive debrief history"
    ),
    "runs": runs,
  }
  output_dir = Path(__file__).parent
  output_dir.joinpath("results.json").write_text(
    json.dumps(artifact, indent=2) + "\n",
    encoding="utf-8",
  )
  output_dir.joinpath("diagnostics.md").write_text(
    diagnostics_markdown(artifact),
    encoding="utf-8",
  )
  failures = [
    f"{run['profile_name']}: {error}"
    for run in runs
    for error in run["assertion_errors"]
  ]
  if failures:
    raise SystemExit("Advice validation failed:\n- " + "\n- ".join(failures))
  print(f"wrote {output_dir / 'results.json'}")
  print(f"wrote {output_dir / 'diagnostics.md'}")


if __name__ == "__main__":
  main()
