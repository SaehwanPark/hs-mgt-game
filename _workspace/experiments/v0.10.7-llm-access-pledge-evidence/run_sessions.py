import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT / "scripts"))

from play_game import play_session  # noqa: E402


CODE_VERSION = "0.10.7"
CAMPAIGN = "competitive-regional-v1"
DIFFICULTY = "hard"
SEED = 42

PROFILES = [
  {
    "id": "fiscal_steward",
    "name": "Fiscal Steward",
    "prompt": (
      "Fiscal Steward prioritizing solvency, measured capacity growth, payer "
      "discipline, and risk monitoring under hard competitive pressure."
    ),
    "commands": [
      "monitor target=northlake depth=1; negotiate payer=carrier_a rate_posture=conservative",
      "recruit role=nurse headcount=4",
      "invest domain=emergency amount=2; monitor target=summit depth=1",
      "negotiate payer=medicare rate_posture=neutral",
      "hold",
      "invest domain=outpatient amount=2; recruit role=admin headcount=2",
      "monitor target=valley depth=1",
      "negotiate payer=carrier_b rate_posture=conservative",
      "hold",
      "recruit role=physician headcount=2",
      "commit pledge_type=quality level=1",
      "hold",
      "hold",
      "hold",
      "hold",
      "hold",
      "hold",
      "hold",
      "hold",
      "hold",
      "commit pledge_type=workforce level=1",
      "hold",
      "hold",
      "hold",
    ],
    "post_run_rationale": (
      "Did not repeat access pledges. The persona avoided access commitments "
      "that could create recurring obligations without confirmed capacity and "
      "payer support, using quality and workforce pledges instead."
    ),
  },
  {
    "id": "access_expansion_advocate",
    "name": "Access Expansion Advocate",
    "prompt": (
      "Access Expansion Advocate prioritizing Medicaid/community access, "
      "workforce stability, and outpatient capacity under hard-mode constraints."
    ),
    "commands": [
      "monitor target=northlake depth=1; commit pledge_type=access level=2",
      "recruit role=nurse headcount=2; negotiate payer=medicaid rate_posture=neutral",
      "invest domain=outpatient amount=2; hold",
      "hold",
      "hold",
      "negotiate payer=carrier_a rate_posture=neutral; hold",
      "recruit role=physician headcount=1; invest domain=emergency amount=1",
      "monitor target=valley depth=1; hold",
      "commit pledge_type=workforce level=1; recruit role=nurse headcount=1",
      "invest domain=psychiatric amount=1; hold",
      "negotiate payer=medicare rate_posture=neutral",
      "hold",
      "monitor target=northlake depth=1; invest domain=obstetrics amount=1",
      "hold",
      "negotiate payer=carrier_b rate_posture=neutral",
      "hold",
      "hold",
      "monitor target=summit depth=1; hold",
      "hold",
      "hold",
      "hold",
      "hold",
      "hold",
      "hold",
    ],
    "post_run_rationale": (
      "Used one access pledge in month 1 to signal the persona's priority, "
      "then shifted to outpatient, emergency, psychiatric, obstetrics, "
      "Medicaid negotiation, and staffing actions."
    ),
  },
  {
    "id": "first_time_executive",
    "name": "First-Time Executive",
    "prompt": (
      "First-Time Executive, cautious learner prioritizing workforce stability, "
      "baseline intelligence, and affordable access without overcommitting."
    ),
    "commands": [
      "monitor target=northlake depth=1; recruit role=admin headcount=1",
      "monitor target=summit depth=1; hold",
      "monitor target=valley depth=1; recruit role=nurse headcount=2",
      "negotiate payer=medicaid rate_posture=neutral; hold",
      "invest domain=outpatient amount=2; recruit role=physician headcount=1",
      "commit pledge_type=access level=1; hold",
      "invest domain=emergency amount=2; recruit role=nurse headcount=2",
      "negotiate payer=carrier_a rate_posture=neutral; hold",
      "recruit role=admin headcount=1; hold",
      "monitor target=northlake depth=1; hold",
      "invest domain=beds amount=2; recruit role=nurse headcount=1",
      "commit pledge_type=workforce level=1; hold",
      "hold",
      "invest domain=psychiatric amount=1; hold",
      "hold",
      "hold",
      "hold",
      "hold",
      "hold",
      "monitor target=valley depth=1; hold",
      "hold",
      "hold",
      "hold",
      "hold",
    ],
    "post_run_rationale": (
      "Made one modest access pledge early, then avoided stacking public "
      "commitments until workforce, monitoring, and service capacity had more support."
    ),
  },
]


def policy_for(commands):
  def policy(_obs, _legal, turn):
    return commands[turn - 1]

  return policy


def access_pledge_count(commands):
  return sum("commit pledge_type=access" in command.lower() for command in commands)


def run_profile(profile):
  result = play_session(
    CAMPAIGN,
    seed=SEED,
    difficulty=DIFFICULTY,
    policy_fn=policy_for(profile["commands"]),
  )
  if result is None:
    raise RuntimeError(f"profile {profile['id']} returned no result")

  return {
    "profile_id": profile["id"],
    "profile_name": profile["name"],
    "persona_prompt": profile["prompt"],
    "seed": SEED,
    "difficulty": DIFFICULTY,
    "commands": profile["commands"],
    "access_pledge_count": access_pledge_count(profile["commands"]),
    "validation_failures": result["validation_failures"],
    "transition_count": len(result["history"]),
    "state_hashes": [transition["state_hash"] for transition in result["history"]],
    "final_observation": result["final_observation"],
    "debrief": result["debrief"],
    "post_run_rationale": profile["post_run_rationale"],
  }


def main():
  os.chdir(ROOT)
  runs = [run_profile(profile) for profile in PROFILES]
  artifact = {
    "batch_id": "v0.10.7-llm-access-pledge-evidence",
    "code_version": CODE_VERSION,
    "campaign": CAMPAIGN,
    "difficulty": DIFFICULTY,
    "seed": SEED,
    "evidence_type": "sub-agent generated command plans replayed through MCP",
    "runs": runs,
  }

  output_path = Path(__file__).with_name("results.json")
  output_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
  print(f"wrote {output_path}")


if __name__ == "__main__":
  main()
