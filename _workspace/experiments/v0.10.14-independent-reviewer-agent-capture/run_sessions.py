import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT / "scripts"))

from play_game import play_session  # noqa: E402
from run_automated_playtests import code_version  # noqa: E402


BATCH_ID = "v0.10.14-independent-reviewer-agent-capture"
CAMPAIGN = "competitive-regional-v1"
DIFFICULTIES = ["normal", "hard"]
SEEDS = [42, 43, 44]
EXPECTED_TRANSITIONS = 24
MAX_ACCESS_PLEDGES_PER_RUN = 1


def observation_text(obs):
  return "\n".join(obs).lower()


def riverside_block(obs):
  block = []
  in_riverside = False
  for line in "\n".join(obs).split("\n"):
    upper = line.upper()
    if "RIVERSIDE COMMUNITY HEALTH" in upper:
      in_riverside = True
    elif in_riverside and any(name in upper for name in ("NORTHLAKE", "SUMMIT", "VALLEY")):
      in_riverside = False
    if in_riverside:
      block.append(line)
  return "\n".join(block)


def parse_metric(obs, label):
  match = re.search(rf"{re.escape(label)}:\s*(-?\d+)", riverside_block(obs), re.IGNORECASE)
  return int(match.group(1)) if match else None


def access_pledge_count(commands):
  return sum("commit pledge_type=access" in command.lower() for command in commands)


def final_hash(result):
  return result["history"][-1]["state_hash"] if result["history"] else None


def with_hold(command):
  parts = [part.strip().lower() for part in command.split(";") if part.strip()]
  return command if "hold" in parts else f"{command}; hold"


def rival_target(turn):
  return ["northlake", "summit", "valley"][(turn - 1) % 3]


def reviewer_fiscal_steward(obs, _legal, turn):
  workforce = parse_metric(obs, "Workforce trust")
  cash = parse_metric(obs, "Cash")
  if turn in (1, 6, 12, 18):
    return with_hold(f"monitor target={rival_target(turn)} depth=1")
  if workforce is not None and workforce < 55 and turn in (2, 9, 16):
    return with_hold("commit pledge_type=workforce level=1")
  if turn in (3, 11, 20):
    return with_hold("negotiate payer=medicare rate_posture=neutral")
  if turn in (4, 14):
    return with_hold("negotiate payer=carrier_a rate_posture=conservative")
  if cash is None or cash >= 16:
    if turn in (5, 13):
      return with_hold("invest domain=emergency amount=4")
    if turn in (8, 17):
      return with_hold("recruit role=nurse headcount=1")
  return "hold"


def reviewer_access_operator(obs, _legal, turn):
  access = parse_metric(obs, "Access")
  workforce = parse_metric(obs, "Workforce trust")
  if turn == 1:
    return with_hold("commit pledge_type=access level=1")
  if turn in (2, 10, 18):
    return with_hold("negotiate payer=medicaid rate_posture=neutral")
  if workforce is not None and workforce < 55 and turn in (3, 11, 19):
    return with_hold("recruit role=nurse headcount=1")
  if access is not None and access < 75:
    if turn in (4, 12):
      return with_hold("invest domain=outpatient amount=4")
    if turn in (7, 15):
      return with_hold("invest domain=psychiatric amount=3")
    if turn in (9, 17):
      return with_hold("invest domain=emergency amount=3")
  if turn in (5, 13, 21):
    return with_hold(f"monitor target={rival_target(turn)} depth=1")
  if turn in (6, 14, 22):
    return with_hold("negotiate payer=medicare rate_posture=neutral")
  return "hold"


def reviewer_competitive_analyst(obs, _legal, turn):
  text = observation_text(obs)
  if turn in (1, 2, 3, 7, 11, 15, 19, 23):
    return with_hold(f"monitor target={rival_target(turn)} depth=1")
  if "northlake" in text and turn in (4, 12):
    return with_hold("negotiate payer=carrier_a rate_posture=neutral")
  if "summit" in text and turn in (8, 16):
    return with_hold("negotiate payer=carrier_b rate_posture=conservative")
  if turn in (5, 13):
    return with_hold("invest domain=cardiology amount=3")
  if turn in (6, 14):
    return with_hold("recruit role=admin headcount=1")
  if turn in (10, 18):
    return with_hold("invest domain=asc amount=3")
  if turn in (20, 22):
    return with_hold("commit pledge_type=quality level=1")
  return "hold"


PROFILES = [
  {
    "id": "reviewer_fiscal_steward",
    "name": "Reviewer Fiscal Steward",
    "prompt": (
      "Independent reviewer policy prioritizing solvency, workforce trust, "
      "neutral public-payer posture, conservative commercial negotiation, and "
      "low-cost monitoring before growth."
    ),
    "policy": reviewer_fiscal_steward,
  },
  {
    "id": "reviewer_access_operator",
    "name": "Reviewer Access Operator",
    "prompt": (
      "Independent reviewer policy using one early access pledge, then shifting "
      "to staffing, public-payer negotiation, and modest service-line capacity."
    ),
    "policy": reviewer_access_operator,
  },
  {
    "id": "reviewer_competitive_analyst",
    "name": "Reviewer Competitive Analyst",
    "prompt": (
      "Independent reviewer policy rotating rival monitoring and using modest "
      "targeted investments or payer posture changes when rival cues are visible."
    ),
    "policy": reviewer_competitive_analyst,
  },
]


def run_profile(profile, seed, difficulty):
  result = play_session(
    CAMPAIGN,
    seed=seed,
    difficulty=difficulty,
    policy_fn=profile["policy"],
    capture_trace=True,
  )
  if result is None:
    raise RuntimeError(f"profile {profile['id']} returned no result")
  if result["validation_failures"]:
    raise RuntimeError(
      f"profile {profile['id']} / {difficulty} / seed {seed} had "
      f"{len(result['validation_failures'])} validation failures"
    )
  if len(result["history"]) != EXPECTED_TRANSITIONS:
    raise RuntimeError(
      f"profile {profile['id']} / {difficulty} / seed {seed} completed "
      f"{len(result['history'])}/{EXPECTED_TRANSITIONS} transitions"
    )

  commands = [
    entry["submitted_command"]
    for entry in result.get("turn_trace", [])
    if entry["latest_transition"] is not None
  ]
  pledges = access_pledge_count(commands)
  if pledges > MAX_ACCESS_PLEDGES_PER_RUN:
    raise RuntimeError(
      f"profile {profile['id']} / {difficulty} / seed {seed} made {pledges} "
      f"access pledges, expected at most {MAX_ACCESS_PLEDGES_PER_RUN}"
    )

  return {
    "profile_id": profile["id"],
    "profile_name": f"{profile['name']} / {difficulty} / seed {seed}",
    "persona_prompt": profile["prompt"],
    "policy_source": "independent observation-conditioned reviewer policy",
    "seed": seed,
    "difficulty": difficulty,
    "turn_trace": result["turn_trace"],
    "commands": commands,
    "access_pledge_count": pledges,
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
    "batch_id": BATCH_ID,
    "code_version": code_version(),
    "campaign": CAMPAIGN,
    "difficulty": "normal, hard",
    "seed": "42, 43, 44",
    "profiles": [profile["id"] for profile in PROFILES],
    "evidence_type": (
      "live observation-by-observation MCP capture matrix using independent "
      "observation-conditioned reviewer policies"
    ),
    "runs": runs,
  }

  output_path = Path(__file__).with_name("results.json")
  output_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
  print(f"wrote {output_path}")


if __name__ == "__main__":
  main()
