import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT / "scripts"))

from play_game import play_session  # noqa: E402
from run_automated_playtests import code_version  # noqa: E402


BATCH_ID = "v0.10.24-access-debrief-validation"
CAMPAIGN = "competitive-regional-v1"
SEED = 42
DIFFICULTIES = ["normal", "hard"]
EXPECTED_TRANSITIONS = 24
NOTE_PREFIX = "Access follow-through note:"


PROFILES = [
  {
    "id": "access_pledge_under_followed",
    "name": "Access Pledge Under-Followed",
    "expected_note": True,
    "prompt": (
      "Stress-test the v0.10.23 debrief note by combining repeated public "
      "access pledges, low ending cash, and limited durable operational "
      "follow-through."
    ),
    "commands": [
      "invest domain=beds amount=40; commit pledge_type=access level=1",
      "recruit role=admin headcount=1; commit pledge_type=access level=1",
      "commit pledge_type=access level=1; hold",
    ],
  },
  {
    "id": "single_access_pledge_low_cash_control",
    "name": "Single Access Pledge Low-Cash Control",
    "expected_note": False,
    "prompt": (
      "Control run that reaches low cash but makes only one access pledge, so "
      "the repeated-pledge note should remain absent."
    ),
    "commands": [
      "invest domain=beds amount=40; commit pledge_type=access level=1",
      "recruit role=admin headcount=1; hold",
    ],
  },
  {
    "id": "access_pledge_followed_control",
    "name": "Access Pledge Followed Control",
    "expected_note": False,
    "prompt": (
      "Control run with repeated access pledges but enough durable "
      "follow-through actions to avoid the explanatory note."
    ),
    "commands": [
      "invest domain=beds amount=40; commit pledge_type=access level=1",
      "recruit role=admin headcount=1; commit pledge_type=access level=1",
    ],
  },
]


def command_for_month(profile, turn):
  commands = profile["commands"]
  if turn <= len(commands):
    return commands[turn - 1]
  return "hold"


def access_pledge_count(commands):
  return sum("commit pledge_type=access" in command.lower() for command in commands)


def follow_through_count(commands):
  durable_verbs = ("monitor ", "recruit ", "invest ", "negotiate ", "project ")
  count = 0
  for command_text in commands:
    for command in command_text.lower().split(";"):
      if command.strip().startswith(durable_verbs):
        count += 1
  return count


def final_hash(result):
  return result["history"][-1]["state_hash"] if result["history"] else None


def debrief_has_note(debrief):
  return any(line.startswith(NOTE_PREFIX) for line in debrief)


def run_profile(profile, difficulty):
  def policy(_obs, _legal, turn):
    return command_for_month(profile, turn)

  result = play_session(
    CAMPAIGN,
    seed=SEED,
    difficulty=difficulty,
    policy_fn=policy,
    capture_trace=True,
  )
  if result is None:
    raise RuntimeError(f"profile {profile['id']} returned no result")
  if result["validation_failures"]:
    raise RuntimeError(
      f"profile {profile['id']} / {difficulty} had "
      f"{len(result['validation_failures'])} validation failures"
    )
  if len(result["history"]) != EXPECTED_TRANSITIONS:
    raise RuntimeError(
      f"profile {profile['id']} / {difficulty} completed "
      f"{len(result['history'])}/{EXPECTED_TRANSITIONS} transitions"
    )

  accepted_commands = [
    entry["submitted_command"]
    for entry in result.get("turn_trace", [])
    if entry["latest_transition"] is not None
  ]
  note_present = debrief_has_note(result["debrief"])
  if note_present != profile["expected_note"]:
    raise RuntimeError(
      f"profile {profile['id']} / {difficulty} expected note "
      f"{profile['expected_note']} but observed {note_present}"
    )

  return {
    "profile_id": profile["id"],
    "profile_name": f"{profile['name']} / {difficulty} / seed {SEED}",
    "persona_prompt": profile["prompt"],
    "seed": SEED,
    "difficulty": difficulty,
    "expected_note": profile["expected_note"],
    "note_present": note_present,
    "access_pledge_count": access_pledge_count(accepted_commands),
    "durable_follow_through_count": follow_through_count(accepted_commands),
    "turn_trace": result["turn_trace"],
    "commands": accepted_commands,
    "validation_failures": result["validation_failures"],
    "transition_count": len(result["history"]),
    "state_hashes": [transition["state_hash"] for transition in result["history"]],
    "final_hash": final_hash(result),
    "final_observation": result["final_observation"],
    "debrief": result["debrief"],
  }


def main():
  os.chdir(ROOT)
  runs = []
  for difficulty in DIFFICULTIES:
    for profile in PROFILES:
      runs.append(run_profile(profile, difficulty))

  artifact = {
    "batch_id": BATCH_ID,
    "code_version": code_version(),
    "campaign": CAMPAIGN,
    "difficulty": ", ".join(DIFFICULTIES),
    "seed": SEED,
    "evidence_type": (
      "bounded MCP debrief validation for the v0.10.23 access follow-through "
      "note using trigger and control command policies"
    ),
    "note_prefix": NOTE_PREFIX,
    "runs": runs,
  }

  output_path = Path(__file__).with_name("results.json")
  output_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
  print(f"wrote {output_path}")


if __name__ == "__main__":
  main()
