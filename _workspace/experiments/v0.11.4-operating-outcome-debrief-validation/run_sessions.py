#!/usr/bin/env python3
"""Capture the post-v0.11.3 operating-outcome debrief matrix."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from play_game import play_session


SEEDS = [42, 43, 44]
DIFFICULTIES = ["easy", "normal", "hard", "expert"]
CAMPAIGN = "competitive-regional-v1"
ARTIFACT_TYPE = "operating_outcome_debrief_validation"
BATCH_ID = "v0.11.4-operating-outcome-debrief-validation"
CODE_VERSION = "0.11.4"
RULESET = "competitive-ruleset-0.2.0"
STATE_HASH_SCHEMA = "competitive-state-hash-v9"
EXPECTED_MONTHS = 24
GOLDEN_CONTROL_HASH = "61357596d8800592"

PROFILES = {
  "Access First": [
    "recruit role=nurse headcount=1",
    "invest domain=beds amount=5",
    "invest domain=emergency amount=5",
    "commit pledge_type=access level=1",
    "monitor target=northlake depth=1",
  ],
  "Commercial Focus": [
    "negotiate payer=carrier_a rate_posture=aggressive",
    "negotiate payer=carrier_b rate_posture=neutral",
    "negotiate payer=medicare rate_posture=neutral",
    "monitor target=northlake depth=1",
    "hold",
  ],
  "Workforce Resilience": [
    "recruit role=nurse headcount=1",
    "recruit role=physician headcount=1",
    "commit pledge_type=workforce level=1",
    "recruit role=admin headcount=1",
    "hold",
  ],
  "Capital Modernization": [
    "invest domain=beds amount=5",
    "invest domain=outpatient amount=5",
    "invest domain=emergency amount=5",
    "invest domain=technology amount=5",
    "hold",
  ],
  "Coalition/Legitimacy": [
    "commit pledge_type=access level=1",
    "commit pledge_type=quality level=1",
    "negotiate payer=medicaid rate_posture=neutral",
    "commit pledge_type=workforce level=1",
    "monitor target=northlake depth=1",
  ],
}


def code_version():
  cargo = (ROOT / "Cargo.toml").read_text(encoding="utf-8")
  match = re.search(r'^version\s*=\s*"([^"]+)"', cargo, re.MULTILINE)
  return match.group(1) if match else "unknown"


def visible_resources(legal):
  text = "\n".join(str(line) for line in legal)
  match = re.search(
    r"Available resources:\s*AP\s+(?P<ap>\d+),\s*cash\s+(?P<cash>-?\d+),\s*"
    r"political capital\s+(?P<pc>\d+)",
    text,
  )
  if not match:
    return None
  return {key: int(value) for key, value in match.groupdict().items()}


def command_cost(command):
  text = command.casefold()
  if text == "hold":
    return {"ap": 0, "cash": 0, "pc": 0}
  if text.startswith("recruit "):
    return {"ap": 1, "cash": 5, "pc": 0}
  if text.startswith("invest "):
    amount = int(re.search(r"amount=(\d+)", text).group(1))
    return {"ap": 1, "cash": amount, "pc": 0}
  if text.startswith("monitor "):
    depth = int(re.search(r"depth=(\d+)", text).group(1))
    return {"ap": depth, "cash": 0, "pc": 0}
  if text.startswith("negotiate "):
    cash = 0
    if "payer=medicaid" in text:
      cash = 5
    elif "payer=medicare" in text:
      cash = 10
    return {"ap": 1, "cash": cash, "pc": 2}
  if text.startswith("commit "):
    return {"ap": 1, "cash": 0, "pc": 1}
  raise ValueError(f"unknown scripted command: {command}")


def affordable(command, resources):
  if command == "hold":
    return True
  if resources is None:
    return False
  cost = command_cost(command)
  return (
    cost["ap"] <= resources["ap"]
    and cost["pc"] <= resources["pc"]
    and cost["cash"] + 20 <= resources["cash"]
  )


def policy_for(profile):
  candidates = PROFILES[profile]

  def policy(_obs, legal, turn):
    start = (turn - 1) % len(candidates)
    ordered = candidates[start:] + candidates[:start]
    resources = visible_resources(legal)
    for command in ordered:
      if affordable(command, resources):
        return command
    return "hold"

  return policy


def capture(output_path):
  version = code_version()
  if version != CODE_VERSION:
    raise RuntimeError(f"expected package version {CODE_VERSION}, found {version}")

  subprocess.run(
    ["cargo", "build", "--quiet", "--bin", "hs-mgt-game-mcp"],
    cwd=ROOT,
    check=True,
  )

  control = play_session(
    CAMPAIGN,
    seed=42,
    difficulty="normal",
    policy_fn=lambda _obs, _legal, _turn: "hold",
  )
  if control["history"][0]["state_hash"] != GOLDEN_CONTROL_HASH:
    raise RuntimeError(
      "seed-42 Normal hold-control hash changed: "
      f"{control['history'][0]['state_hash']}"
    )

  runs = []
  for profile in PROFILES:
    for seed in SEEDS:
      for difficulty in DIFFICULTIES:
        print(f"Running {profile} / seed {seed} / {difficulty}")
        result = play_session(
          CAMPAIGN,
          seed=seed,
          difficulty=difficulty,
          policy_fn=policy_for(profile),
          capture_trace=True,
        )
        history = result["history"]
        runs.append({
          "profile": profile,
          "seed": seed,
          "difficulty": difficulty,
          "campaign": CAMPAIGN,
          "completion_status": "complete" if len(history) == EXPECTED_MONTHS else "incomplete",
          "transition_count": len(history),
          "history": history,
          "turn_trace": result.get("turn_trace", []),
          "final_observation": result["final_observation"],
          "debrief": result["debrief"],
          "validation_failures": result["validation_failures"],
          "state_hashes": [transition["state_hash"] for transition in history],
        })

  artifact = {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": version,
    "campaign": CAMPAIGN,
    "ruleset": RULESET,
    "state_hash_schema": STATE_HASH_SCHEMA,
    "seeds": SEEDS,
    "difficulties": DIFFICULTIES,
    "profiles": list(PROFILES),
    "policy_candidates": PROFILES,
    "expected_months": EXPECTED_MONTHS,
    "runs": runs,
  }
  output_path.parent.mkdir(parents=True, exist_ok=True)
  output_path.write_text(
    json.dumps(artifact, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )
  print(f"Wrote {len(runs)} runs to {output_path}")


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--output",
    default=str(Path(__file__).with_name("capture.json")),
  )
  args = parser.parse_args()
  capture(Path(args.output))


if __name__ == "__main__":
  main()
