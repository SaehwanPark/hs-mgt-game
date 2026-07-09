import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT / "scripts"))

from play_game import play_session  # noqa: E402
from run_automated_playtests import code_version  # noqa: E402


BATCH_ID = "v0.10.37-rival-info-monitor-evidence"
CAMPAIGN = "competitive-regional-v1"
SEED = 42
EXPECTED_TRANSITIONS = 24
DIFFICULTIES = ["hard", "expert"]
POLICY_VARIANTS = ["monitored", "unmonitored"]

MONITOR_TARGETS = ["northlake", "summit", "valley", "metro"]
NON_MONITOR_COMMANDS = {
  2: "negotiate payer=carrier_a rate_posture=conservative; hold",
  4: "recruit role=nurse headcount=1; hold",
  6: "negotiate payer=medicaid rate_posture=neutral; hold",
  8: "commit pledge_type=workforce level=1; hold",
  10: "negotiate payer=carrier_a rate_posture=conservative; hold",
  12: "negotiate payer=medicare rate_posture=neutral; hold",
  14: "invest domain=emergency amount=3; hold",
  16: "negotiate payer=carrier_b rate_posture=conservative; hold",
  18: "commit pledge_type=quality level=1; hold",
  20: "negotiate payer=carrier_a rate_posture=conservative; hold",
  22: "invest domain=asc amount=3; hold",
  24: "hold",
}


def monitored_command(turn):
  if turn % 2 == 1:
    target = MONITOR_TARGETS[((turn - 1) // 2) % len(MONITOR_TARGETS)]
    return f"monitor target={target} depth=1; hold"
  return NON_MONITOR_COMMANDS.get(turn, "hold")


def unmonitored_command(turn):
  if turn % 2 == 1:
    return "hold"
  return NON_MONITOR_COMMANDS.get(turn, "hold")


def policy_for_variant(variant):
  def policy(_obs, _legal, turn):
    if variant == "monitored":
      return monitored_command(turn)
    return unmonitored_command(turn)

  return policy


def observation_lines(run, needle):
  count = 0
  examples = []
  for entry in run.get("turn_trace", []):
    for line in entry.get("observation", []):
      if needle in line:
        count += 1
        if len(examples) < 3:
          examples.append(f"month {entry.get('turn')}: {line}")
  return count, examples


def annotate_information_signals(run):
  monitor_count, monitor_examples = observation_lines(run, "monitor intel")
  public_count, public_examples = observation_lines(run, "observed, prior month")
  gap_count, gap_examples = observation_lines(run, "not publicly disclosed")
  no_signal_count, no_signal_examples = observation_lines(run, "no public signals")
  run["monitor_intel_line_count"] = monitor_count
  run["public_rival_line_count"] = public_count
  run["private_activity_gap_line_count"] = gap_count
  run["no_public_signal_line_count"] = no_signal_count
  run["rival_information_examples"] = {
    "monitor_intel": monitor_examples,
    "public_rival": public_examples,
    "private_activity_gap": gap_examples,
    "no_public_signal": no_signal_examples,
  }


def access_pledge_count(commands):
  return sum("commit pledge_type=access" in command.lower() for command in commands)


def final_hash(result):
  return result["history"][-1]["state_hash"] if result["history"] else None


def failed_run(difficulty, variant, error):
  return {
    "profile_id": f"rival_info_{variant}",
    "profile_name": f"Rival Information {variant.title()} / {difficulty}",
    "policy_variant": variant,
    "seed": SEED,
    "difficulty": difficulty,
    "completion_status": "failed",
    "run_error": error,
    "turn_trace": [],
    "commands": [],
    "access_pledge_count": 0,
    "validation_failures": [],
    "transition_count": 0,
    "state_hashes": [],
    "final_hash": None,
    "final_observation": [],
    "debrief": [],
    "monitor_intel_line_count": 0,
    "public_rival_line_count": 0,
    "private_activity_gap_line_count": 0,
    "no_public_signal_line_count": 0,
    "rival_information_examples": {},
  }


def run_variant(difficulty, variant):
  try:
    result = play_session(
      CAMPAIGN,
      seed=SEED,
      difficulty=difficulty,
      policy_fn=policy_for_variant(variant),
      capture_trace=True,
    )
  except RuntimeError as err:
    return failed_run(difficulty, variant, str(err))
  if result is None:
    return failed_run(difficulty, variant, "play_session returned no result")

  commands = [
    entry["submitted_command"]
    for entry in result.get("turn_trace", [])
    if entry["latest_transition"] is not None
  ]
  run = {
    "profile_id": f"rival_info_{variant}",
    "profile_name": f"Rival Information {variant.title()} / {difficulty}",
    "persona_prompt": (
      "Paired evidence policy for rival-information pressure. The monitored "
      "variant spends alternating odd months on rival monitoring; the "
      "unmonitored variant replaces those monitor months with hold while "
      "keeping the same non-monitor commands."
    ),
    "decision_source": (
      "deterministic paired policy from actor-visible MCP observations and "
      "legal command hints"
    ),
    "policy_variant": variant,
    "seed": SEED,
    "difficulty": difficulty,
    "completion_status": (
      "complete" if len(result["history"]) == EXPECTED_TRANSITIONS else "incomplete"
    ),
    "turn_trace": result.get("turn_trace", []),
    "commands": commands,
    "access_pledge_count": access_pledge_count(commands),
    "validation_failures": result["validation_failures"],
    "transition_count": len(result["history"]),
    "state_hashes": [transition["state_hash"] for transition in result["history"]],
    "final_hash": final_hash(result),
    "final_observation": result["final_observation"],
    "debrief": result["debrief"],
  }
  annotate_information_signals(run)

  return run


def main():
  os.chdir(ROOT)
  runs = []
  for difficulty in DIFFICULTIES:
    for variant in POLICY_VARIANTS:
      runs.append(run_variant(difficulty, variant))

  artifact = {
    "batch_id": BATCH_ID,
    "code_version": code_version(),
    "campaign": CAMPAIGN,
    "difficulty": ", ".join(DIFFICULTIES),
    "seed": SEED,
    "evidence_type": (
      "paired live MCP capture comparing monitored and unmonitored rival "
      "information policies at Hard and Expert difficulty"
    ),
    "runs": runs,
  }

  output_path = Path(__file__).with_name("results.json")
  output_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
  print(f"wrote {output_path}")


if __name__ == "__main__":
  main()
