import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT / "scripts"))

from play_game import play_session  # noqa: E402
from run_automated_playtests import (  # noqa: E402
  TARGET_BASELINE,
  TARGET_DIFFICULTY_ADAPTIVE,
  code_version,
  policy_balanced,
  policy_fiscal,
  policy_for_competitive,
  policy_growth,
  policy_naive_first_time,
)


BATCH_ID = "v0.10.13-live-static-adaptive-capture"
CAMPAIGN = "competitive-regional-v1"
DIFFICULTIES = ["normal", "hard"]
SEEDS = [42, 43, 44]
EXPECTED_TRANSITIONS = 24
POLICY_VARIANTS = [
  {
    "id": "static",
    "name": "Static",
    "target": TARGET_BASELINE,
    "description": "Base deterministic profile policy with no adaptive wrapper.",
  },
  {
    "id": "adaptive",
    "name": "Adaptive",
    "target": TARGET_DIFFICULTY_ADAPTIVE,
    "description": "Existing difficulty-adaptive wrapper applied to Hard runs.",
  },
]

PROFILES = [
  {
    "id": "fiscal_caution",
    "name": "Fiscal Caution",
    "prompt": (
      "Protect cash runway, use lower-risk commitments, and avoid aggressive "
      "spending while still completing the competitive campaign."
    ),
    "policy": policy_fiscal,
  },
  {
    "id": "capacity_growth",
    "name": "Capacity Growth",
    "prompt": (
      "Prioritize access, beds, service-line capacity, and recruitment even "
      "under financial and rival pressure."
    ),
    "policy": policy_growth,
  },
  {
    "id": "balanced_strategy",
    "name": "Balanced Strategy",
    "prompt": (
      "Trade off cash, access, workforce trust, payer negotiations, and rival "
      "monitoring without optimizing a single metric."
    ),
    "policy": policy_balanced,
  },
  {
    "id": "naive_first_time",
    "name": "Naive First-Time",
    "prompt": (
      "Use cautious first-time-player choices from the legal command hints and "
      "player-facing surface without implementation knowledge."
    ),
    "policy": policy_naive_first_time,
  },
]


def access_pledge_count(commands):
  return sum("commit pledge_type=access" in command.lower() for command in commands)


def final_hash(result):
  return result["history"][-1]["state_hash"] if result["history"] else None


def run_profile(profile, variant, seed, difficulty):
  policy = policy_for_competitive(
    profile["policy"],
    difficulty,
    variant["target"],
  )
  result = play_session(
    CAMPAIGN,
    seed=seed,
    difficulty=difficulty,
    policy_fn=policy,
    capture_trace=True,
  )
  if result is None:
    raise RuntimeError(f"profile {profile['id']} returned no result")
  if result["validation_failures"]:
    raise RuntimeError(
      f"profile {profile['id']} / {variant['id']} / {difficulty} / seed {seed} "
      f"had {len(result['validation_failures'])} validation failures"
    )
  if len(result["history"]) != EXPECTED_TRANSITIONS:
    raise RuntimeError(
      f"profile {profile['id']} / {variant['id']} / {difficulty} / seed {seed} "
      f"completed {len(result['history'])}/{EXPECTED_TRANSITIONS} transitions"
    )

  commands = [
    entry["submitted_command"]
    for entry in result.get("turn_trace", [])
    if entry["latest_transition"] is not None
  ]
  return {
    "profile_id": profile["id"],
    "profile_name": (
      f"{profile['name']} / {variant['name']} / {difficulty} / seed {seed}"
    ),
    "persona_prompt": profile["prompt"],
    "policy_variant": variant["id"],
    "policy_variant_name": variant["name"],
    "policy_target": variant["target"],
    "policy_variant_description": variant["description"],
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
      for variant in POLICY_VARIANTS:
        for profile in PROFILES:
          runs.append(run_profile(profile, variant, seed, difficulty))

  artifact = {
    "batch_id": BATCH_ID,
    "code_version": code_version(),
    "campaign": CAMPAIGN,
    "difficulty": "normal, hard",
    "seed": "42, 43, 44",
    "policy_variants": [variant["id"] for variant in POLICY_VARIANTS],
    "evidence_type": (
      "live observation-by-observation MCP capture matrix comparing static "
      "and difficulty-adaptive deterministic policies"
    ),
    "runs": runs,
  }

  output_path = Path(__file__).with_name("results.json")
  output_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
  print(f"wrote {output_path}")


if __name__ == "__main__":
  main()
