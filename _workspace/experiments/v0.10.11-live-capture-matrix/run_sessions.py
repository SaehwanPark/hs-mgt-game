import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT / "scripts"))

from play_game import play_session  # noqa: E402


CODE_VERSION = "0.10.11"
CAMPAIGN = "competitive-regional-v1"
DIFFICULTIES = ["normal", "hard"]
SEEDS = [42, 43, 44]


PROFILES = [
  {
    "id": "solvency_monitor",
    "name": "Solvency Monitor",
    "prompt": (
      "Protect cash runway first, use monitoring to understand rivals, and make "
      "small operational investments only when the observation still shows room."
    ),
  },
  {
    "id": "access_operations",
    "name": "Access Operations",
    "prompt": (
      "Prioritize access through staffing, outpatient capacity, Medicaid posture, "
      "and one public access pledge when operational follow-through is plausible."
    ),
  },
  {
    "id": "workforce_quality",
    "name": "Workforce Quality",
    "prompt": (
      "Stabilize workforce trust, avoid repeated public commitments, and use "
      "quality or workforce pledges only after monitoring and staffing moves."
    ),
  },
]


def observation_text(obs):
  return "\n".join(obs)


def parse_metric(obs, label):
  match = re.search(rf"{label}:\s*(-?\d+)", observation_text(obs))
  return int(match.group(1)) if match else None


def parse_workforce_trust(obs):
  numeric = parse_metric(obs, "Workforce trust")
  if numeric is not None:
    return numeric
  match = re.search(r"Workforce trust:\s*([A-Za-z-]+)", observation_text(obs))
  if not match:
    return None
  labels = {
    "critical": 35,
    "strained": 45,
    "moderate": 55,
    "stable": 65,
    "strong": 75,
  }
  return labels.get(match.group(1).lower())


def cash_signal(obs):
  match = re.search(r"Cash runway:\s*([A-Za-z]+)", observation_text(obs))
  return match.group(1).lower() if match else "unknown"


def has_visible_rivals(obs):
  text = observation_text(obs).lower()
  return any(name in text for name in ("northlake", "summit", "valley"))


def access_pledge_count(commands):
  return sum("commit pledge_type=access" in command.lower() for command in commands)


def live_policy(profile_id):
  def policy(obs, _legal, turn):
    trust = parse_workforce_trust(obs) or 0
    runway = cash_signal(obs)
    rivals = has_visible_rivals(obs)

    if profile_id == "solvency_monitor":
      if turn in (1, 6, 12, 18) and rivals:
        return "monitor target=northlake depth=1; hold"
      if runway in ("strong", "stable") and turn in (2, 10):
        return "recruit role=nurse headcount=2; hold"
      if runway in ("strong", "stable") and turn == 4:
        return "negotiate payer=carrier_a rate_posture=conservative; hold"
      if turn == 16:
        return "commit pledge_type=quality level=1; hold"
      return "hold"

    if profile_id == "access_operations":
      if turn == 1:
        return "monitor target=northlake depth=1; commit pledge_type=access level=1"
      if turn == 2:
        return "recruit role=nurse headcount=2; negotiate payer=medicaid rate_posture=neutral"
      if runway in ("strong", "stable") and turn in (3, 8):
        return "invest domain=outpatient amount=2; hold"
      if turn in (5, 11, 17) and rivals:
        return "monitor target=summit depth=1; hold"
      if trust < 55 and turn in (7, 13):
        return "commit pledge_type=workforce level=1; hold"
      if turn == 15:
        return "negotiate payer=medicare rate_posture=neutral; hold"
      return "hold"

    if turn in (1, 7, 13, 19) and rivals:
      return "monitor target=northlake depth=1; hold"
    if trust < 55 and turn in (2, 9):
      return "recruit role=nurse headcount=2; hold"
    if trust < 60 and turn == 4:
      return "commit pledge_type=workforce level=1; hold"
    if turn == 6:
      return "negotiate payer=carrier_a rate_posture=neutral; hold"
    if runway in ("strong", "stable") and turn == 10:
      return "invest domain=emergency amount=2; hold"
    if turn == 16:
      return "commit pledge_type=quality level=1; hold"
    return "hold"

  return policy


def final_hash(result):
  return result["history"][-1]["state_hash"] if result["history"] else None


def run_profile(profile, seed, difficulty):
  result = play_session(
    CAMPAIGN,
    seed=seed,
    difficulty=difficulty,
    policy_fn=live_policy(profile["id"]),
    capture_trace=True,
  )
  if result is None:
    raise RuntimeError(f"profile {profile['id']} returned no result")

  commands = [
    entry["submitted_command"]
    for entry in result.get("turn_trace", [])
    if entry["latest_transition"] is not None
  ]
  return {
    "profile_id": profile["id"],
    "profile_name": f"{profile['name']} / {difficulty} / seed {seed}",
    "persona_prompt": profile["prompt"],
    "seed": seed,
    "difficulty": difficulty,
    "turn_trace": result["turn_trace"],
    "commands": commands,
    "access_pledge_count": access_pledge_count(commands),
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
    for seed in SEEDS:
      for profile in PROFILES:
        runs.append(run_profile(profile, seed, difficulty))

  artifact = {
    "batch_id": "v0.10.11-live-capture-matrix",
    "code_version": CODE_VERSION,
    "campaign": CAMPAIGN,
    "difficulty": "normal, hard",
    "seed": "42, 43, 44",
    "evidence_type": (
      "live observation-by-observation MCP capture matrix with deterministic "
      "persona policies"
    ),
    "runs": runs,
  }

  output_path = Path(__file__).with_name("results.json")
  output_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
  print(f"wrote {output_path}")


if __name__ == "__main__":
  main()
