import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT / "scripts"))

from play_game import play_session  # noqa: E402
from run_automated_playtests import code_version  # noqa: E402


BATCH_ID = "v0.10.15-live-llm-difficulty-gate"
CAMPAIGN = "competitive-regional-v1"
SEED = 42
EXPECTED_TRANSITIONS = 24


RUNS = [
  {
    "profile_id": "live_fiscal_steward",
    "profile_name": "Live Fiscal Steward",
    "difficulty": "normal",
    "persona_prompt": (
      "Live sub-agent profile prioritizing solvency, workforce trust, cautious "
      "payer posture, and monitoring while avoiding unsupported access pledges."
    ),
    "decision_source": (
      "month-by-month sub-agent decisions from actor-visible MCP observations "
      "and legal command hints"
    ),
    "commands": [
      "monitor target=northlake depth=1; hold",
      "negotiate payer=carrier_a rate_posture=conservative; hold",
      "recruit role=nurse headcount=2; hold",
      "monitor target=summit depth=1; hold",
      "invest domain=outpatient amount=2; hold",
      "commit pledge_type=workforce level=1; hold",
      "monitor target=northlake depth=1; hold",
      "negotiate payer=medicaid rate_posture=neutral; hold",
      "hold",
      "monitor target=summit depth=1; hold",
      "hold",
      "commit pledge_type=quality level=1; hold",
      "monitor target=northlake depth=1; hold",
      "negotiate payer=carrier_a rate_posture=conservative; hold",
      "hold",
      "monitor target=summit depth=1; hold",
      "hold",
      "hold",
      "monitor target=northlake depth=1; hold",
      "negotiate payer=medicare rate_posture=neutral; hold",
      "hold",
      "monitor target=summit depth=1; hold",
      "hold",
      "hold",
    ],
    "live_validation_retries": [],
    "live_rationale": (
      "Conservative solvency-first play used regular monitoring, conservative "
      "commercial payer posture, neutral public-payer alignment, one small "
      "nurse recruitment, one small outpatient investment, and low workforce "
      "and quality pledges while avoiding access pledge overcommitment."
    ),
  },
  {
    "profile_id": "live_fiscal_steward",
    "profile_name": "Live Fiscal Steward",
    "difficulty": "hard",
    "persona_prompt": (
      "Live sub-agent profile prioritizing solvency, workforce trust, cautious "
      "payer posture, and monitoring under Hard pressure while avoiding "
      "unsupported access pledges."
    ),
    "decision_source": (
      "month-by-month sub-agent decisions from actor-visible MCP observations "
      "and legal command hints"
    ),
    "commands": [
      "monitor target=northlake depth=1; hold",
      "recruit role=nurse headcount=2; hold",
      "monitor target=summit depth=1; hold",
      "negotiate payer=carrier_a rate_posture=conservative; hold",
      "hold",
      "monitor target=northlake depth=1; hold",
      "hold",
      "recruit role=nurse headcount=2; hold",
      "monitor target=summit depth=1; hold",
      "negotiate payer=carrier_a rate_posture=conservative; hold",
      "hold",
      "monitor target=northlake depth=1; hold",
      "hold",
      "hold",
      "monitor target=summit depth=1; hold",
      "negotiate payer=carrier_a rate_posture=conservative; hold",
      "hold",
      "monitor target=northlake depth=1; hold",
      "hold",
      "hold",
      "monitor target=summit depth=1; hold",
      "negotiate payer=carrier_a rate_posture=conservative; hold",
      "hold",
      "hold",
    ],
    "live_validation_retries": [],
    "live_rationale": (
      "Hard pressure was treated as a liquidity and credibility problem: "
      "low-depth monitoring, small nurse recruitment while cash was viable, "
      "conservative Carrier A negotiations, and no access pledges."
    ),
  },
  {
    "profile_id": "live_competitive_analyst",
    "profile_name": "Live Competitive Analyst",
    "difficulty": "normal",
    "persona_prompt": (
      "Live decision profile monitoring rivals, responding with targeted "
      "payer, capacity, and staffing choices, and avoiding hidden-state "
      "assumptions."
    ),
    "decision_source": (
      "month-by-month local agent decisions from actor-visible MCP observations "
      "and legal command hints after the delegated sub-agent did not return"
    ),
    "commands": [
      "monitor target=northlake depth=1; hold",
      "monitor target=summit depth=1; hold",
      "monitor target=valley depth=1; hold",
      "negotiate payer=carrier_a rate_posture=neutral; hold",
      "invest domain=cardiology amount=4; hold",
      "hold",
      "monitor target=northlake depth=1; hold",
      "negotiate payer=carrier_b rate_posture=neutral; hold",
      "invest domain=asc amount=4; hold",
      "hold",
      "monitor target=summit depth=1; hold",
      "negotiate payer=medicare rate_posture=neutral; hold",
      "invest domain=cardiology amount=4; hold",
      "hold",
      "monitor target=valley depth=1; hold",
      "negotiate payer=carrier_a rate_posture=neutral; hold",
      "invest domain=asc amount=4; hold",
      "hold",
      "monitor target=northlake depth=1; hold",
      "negotiate payer=medicare rate_posture=neutral; hold",
      "invest domain=technology amount=4; hold",
      "hold",
      "monitor target=summit depth=1; hold",
      "hold",
    ],
    "live_validation_retries": [],
    "live_rationale": (
      "The profile rotated rival monitoring, answered visible commercial "
      "aggression with neutral payer posture, used neutral Medicare alignment "
      "for quality and policy pressure, and made small cardiology, ASC, and "
      "technology investments while preserving cash runway."
    ),
  },
  {
    "profile_id": "live_competitive_analyst",
    "profile_name": "Live Competitive Analyst",
    "difficulty": "hard",
    "persona_prompt": (
      "Live sub-agent profile monitoring rivals, responding with targeted "
      "payer, capacity, and staffing choices under Hard pressure, and avoiding "
      "hidden-state assumptions."
    ),
    "decision_source": (
      "month-by-month sub-agent decisions from actor-visible MCP observations "
      "and legal command hints"
    ),
    "commands": [
      "monitor target=northlake depth=1; hold",
      "monitor target=summit depth=1; hold",
      "monitor target=valley depth=1; hold",
      "hold",
      "negotiate payer=medicare rate_posture=neutral; hold",
      "hold",
      "monitor target=northlake depth=1; hold",
      "negotiate payer=carrier_a rate_posture=neutral; hold",
      "invest domain=asc amount=3; hold",
      "hold",
      "monitor target=summit depth=1; hold",
      "negotiate payer=medicare rate_posture=neutral; hold",
      "invest domain=asc amount=3; hold",
      "hold",
      "monitor target=valley depth=1; hold",
      "negotiate payer=carrier_a rate_posture=neutral; hold",
      "invest domain=asc amount=3; hold",
      "hold",
      "monitor target=northlake depth=1; hold",
      "negotiate payer=medicare rate_posture=neutral; hold",
      "invest domain=asc amount=3; hold",
      "hold",
      "monitor target=summit depth=1; hold",
      "hold",
    ],
    "live_validation_retries": [],
    "live_rationale": (
      "The profile rotated rival monitoring, answered commercial pressure with "
      "neutral Carrier A posture, used neutral Medicare negotiation for "
      "quality and policy pressure, and made small ASC investments while cash "
      "runway remained viable."
    ),
  },
  {
    "profile_id": "live_access_operator",
    "profile_name": "Live Access Operator",
    "difficulty": "normal",
    "persona_prompt": (
      "Live sub-agent profile protecting access and community trust with "
      "operational follow-through through staffing, payer negotiation, "
      "monitoring, and modest capacity while avoiding repeated unsupported "
      "access pledges."
    ),
    "decision_source": (
      "month-by-month sub-agent decisions from actor-visible MCP observations "
      "and legal command hints"
    ),
    "commands": [
      "monitor target=northlake depth=1; recruit role=nurse headcount=4",
      "negotiate payer=carrier_a rate_posture=neutral; recruit role=nurse headcount=4",
      "monitor target=summit depth=1; invest domain=beds amount=10",
      "negotiate payer=carrier_b rate_posture=neutral; recruit role=nurse headcount=2",
      "monitor target=valley depth=1",
      "commit pledge_type=access level=1",
      "negotiate payer=carrier_a rate_posture=neutral; monitor target=northlake depth=1",
      "negotiate payer=carrier_b rate_posture=neutral; monitor target=summit depth=1",
      "commit pledge_type=workforce level=1; monitor target=valley depth=1",
      "monitor target=metro depth=1",
      "monitor target=northlake depth=1",
      "negotiate payer=carrier_a rate_posture=neutral",
      "monitor target=summit depth=1",
      "negotiate payer=carrier_b rate_posture=neutral; monitor target=valley depth=1",
      "monitor target=metro depth=1",
      "monitor target=northlake depth=1",
      "negotiate payer=carrier_a rate_posture=neutral; monitor target=summit depth=1",
      "commit pledge_type=workforce level=1",
      "monitor target=valley depth=1",
      "negotiate payer=carrier_b rate_posture=neutral; monitor target=metro depth=1",
      "monitor target=northlake depth=1",
      "negotiate payer=carrier_a rate_posture=neutral; monitor target=summit depth=1",
      "monitor target=valley depth=1",
      "negotiate payer=carrier_b rate_posture=neutral; monitor target=metro depth=1",
    ],
    "live_validation_retries": [
      {
        "turn": None,
        "command": None,
        "error": "Local wrapper-policy error before submission: legal_commands was a list, not a string.",
      },
      {
        "turn": 4,
        "command": "negotiate payer=carrier_b rate_posture=neutral; recruit role=nurse headcount=3",
        "error": "cash required 15 exceeds available 10",
      },
    ],
    "live_rationale": (
      "The run front-loaded staffing, modest bed investment, neutral payer "
      "negotiation, and monitoring. It made one access pledge after operational "
      "follow-through, then shifted toward surveillance and neutral payer work "
      "when cash was exhausted."
    ),
  },
  {
    "profile_id": "live_access_operator",
    "profile_name": "Live Access Operator",
    "difficulty": "hard",
    "persona_prompt": (
      "Live sub-agent profile protecting access and community trust under Hard "
      "pressure with operational follow-through through staffing, payer "
      "negotiation, monitoring, and modest capacity while avoiding repeated "
      "unsupported access pledges."
    ),
    "decision_source": (
      "month-by-month sub-agent decisions from actor-visible MCP observations "
      "and legal command hints"
    ),
    "commands": [
      "commit pledge_type=workforce level=1; monitor target=northlake depth=1",
      "monitor target=northlake depth=2; commit pledge_type=access level=1",
      "negotiate payer=carrier_a rate_posture=neutral; recruit role=nurse headcount=1",
      "monitor target=summit depth=1; invest domain=outpatient amount=6",
      "negotiate payer=carrier_b rate_posture=conservative; recruit role=admin headcount=1",
      "invest domain=technology amount=6; monitor target=northlake depth=1",
      "recruit role=nurse headcount=1; monitor target=valley depth=1",
      "commit pledge_type=workforce level=1; monitor target=summit depth=1",
      "negotiate payer=medicaid rate_posture=neutral; invest domain=beds amount=5",
      "recruit role=physician headcount=1; monitor target=northlake depth=1",
      "commit pledge_type=quality level=1; invest domain=technology amount=4",
      "negotiate payer=medicare rate_posture=neutral; monitor target=metro depth=1",
      "commit pledge_type=workforce level=1; monitor target=northlake depth=1",
      "monitor target=northlake depth=2; hold",
      "negotiate payer=carrier_a rate_posture=conservative; commit pledge_type=workforce level=1",
      "invest domain=emergency amount=4; monitor target=summit depth=1",
      "commit pledge_type=workforce level=1; monitor target=northlake depth=1",
      "negotiate payer=carrier_b rate_posture=neutral; monitor target=valley depth=1",
      "commit pledge_type=workforce level=1; monitor target=northlake depth=1",
      "monitor target=northlake depth=1; commit pledge_type=access level=1",
      "commit pledge_type=workforce level=1; monitor target=northlake depth=1",
      "commit pledge_type=workforce level=1; monitor target=northlake depth=1",
      "commit pledge_type=workforce level=1; monitor target=northlake depth=1",
      "negotiate payer=carrier_a rate_posture=neutral; monitor target=summit depth=1",
    ],
    "live_validation_retries": [
      {
        "turn": 1,
        "command": "project kind=clinic_network budget=12; recruit role=nurse headcount=2",
        "error": "project budget 12 must be a multiple of duration 9 months",
      },
      {
        "turn": 13,
        "command": "recruit role=nurse headcount=1; invest domain=outpatient amount=5",
        "error": "cash required 10 exceeds available 4",
      },
      {
        "turn": 17,
        "command": "recruit role=admin headcount=1; commit pledge_type=quality level=1",
        "error": "cash required 5 exceeds available 0",
      },
      {
        "turn": 19,
        "command": "recruit role=nurse headcount=1; invest domain=beds amount=4",
        "error": "cash required 9 exceeds available 0",
      },
      {
        "turn": 21,
        "command": "negotiate payer=medicaid rate_posture=neutral; invest domain=technology amount=3",
        "error": "cash required 8 exceeds available 0",
      },
      {
        "turn": 22,
        "command": "monitor target=metro depth=1; recruit role=physician headcount=1",
        "error": "cash required 5 exceeds available 0",
      },
      {
        "turn": 23,
        "command": "commit pledge_type=workforce level=1; invest domain=outpatient amount=3",
        "error": "cash required 3 exceeds available 0",
      },
    ],
    "live_rationale": (
      "The run used wrapper observations and legal hints, limited access "
      "pledges to two low-level commitments, and emphasized workforce "
      "commitments, monitoring, payer negotiation, staffing, and small capacity "
      "or technology actions. Cash depletion forced late-month no-cash fallback "
      "commands."
    ),
  },
]


def policy_for(commands):
  def policy(_obs, _legal, turn):
    return commands[turn - 1]

  return policy


def access_pledge_count(commands):
  return sum("commit pledge_type=access" in command.lower() for command in commands)


def final_hash(result):
  return result["history"][-1]["state_hash"] if result["history"] else None


def run_case(case):
  result = play_session(
    CAMPAIGN,
    seed=SEED,
    difficulty=case["difficulty"],
    policy_fn=policy_for(case["commands"]),
    capture_trace=True,
  )
  if result is None:
    raise RuntimeError(
      f"profile {case['profile_id']} / {case['difficulty']} returned no result"
    )
  if len(result["history"]) != EXPECTED_TRANSITIONS:
    raise RuntimeError(
      f"profile {case['profile_id']} / {case['difficulty']} completed "
      f"{len(result['history'])}/{EXPECTED_TRANSITIONS} transitions"
    )

  commands = [
    entry["submitted_command"]
    for entry in result.get("turn_trace", [])
    if entry["latest_transition"] is not None
  ]
  return {
    "profile_id": case["profile_id"],
    "profile_name": f"{case['profile_name']} / {case['difficulty']} / seed {SEED}",
    "persona_prompt": case["persona_prompt"],
    "decision_source": case["decision_source"],
    "seed": SEED,
    "difficulty": case["difficulty"],
    "turn_trace": result["turn_trace"],
    "commands": commands,
    "access_pledge_count": access_pledge_count(commands),
    "live_validation_retries": case["live_validation_retries"],
    "validation_failures": result["validation_failures"],
    "transition_count": len(result["history"]),
    "state_hashes": [transition["state_hash"] for transition in result["history"]],
    "final_hash": final_hash(result),
    "final_observation": result["final_observation"],
    "debrief": result["debrief"],
    "live_rationale": case["live_rationale"],
  }


def main():
  os.chdir(ROOT)
  runs = [run_case(case) for case in RUNS]
  artifact = {
    "batch_id": BATCH_ID,
    "code_version": code_version(),
    "campaign": CAMPAIGN,
    "difficulty": "normal, hard",
    "seed": SEED,
    "profiles": sorted({case["profile_id"] for case in RUNS}),
    "evidence_type": (
      "live month-by-month sub-agent decisions captured from actor-visible MCP "
      "observations and replayed through the observation-by-observation wrapper"
    ),
    "runs": runs,
  }

  output_path = Path(__file__).with_name("results.json")
  output_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
  print(f"wrote {output_path}")


if __name__ == "__main__":
  main()
