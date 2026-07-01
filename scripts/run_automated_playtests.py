import sys
import os
import re
import subprocess

# Add scripts directory to path to allow import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from play_game import play_session

SEEDS = [42, 43, 44]

def is_stabilization_legal(legal):
  return len(legal) == 1

def policy_fiscal(obs, legal, turn):
  if is_stabilization_legal(legal):
    commands = ["4 10 104", "4 5", "8 5", "6 5", "8 5"]
    return commands[turn - 1]
  else:  # competitive
    commands = [
      "monitor target=northlake depth=1; hold",
      "recruit role=nurse headcount=2; hold",
      "commit pledge_type=access level=1; hold"
    ]
    return commands[turn - 1]

def policy_growth(obs, legal, turn):
  if is_stabilization_legal(legal):
    commands = ["12 25 115", "15 9", "15 9", "15 9", "15 9"]
    return commands[turn - 1]
  else:  # competitive
    commands = [
      "invest domain=beds amount=25",
      "recruit role=nurse headcount=6",
      "negotiate payer=carrier_a rate_posture=aggressive"
    ]
    return commands[turn - 1]

def policy_balanced(obs, legal, turn):
  if is_stabilization_legal(legal):
    commands = ["8 18 112", "10 7", "14 8", "12 8", "14 8"]
    return commands[turn - 1]
  else:  # competitive
    commands = [
      "monitor target=northlake depth=1; recruit role=nurse headcount=4",
      "invest domain=beds amount=15; commit pledge_type=access level=2",
      "negotiate payer=carrier_a rate_posture=neutral; hold"
    ]
    return commands[turn - 1]

def parse_stabilization_metrics(obs, debrief=None):
  metrics = {"Cash": "N/A", "Access": "N/A", "Beds": "N/A", "WorkforceTrust": "N/A", "CommunityTrust": "N/A", "Policy": "N/A"}
  # Helper to parse lists of observations
  text = "\n".join(obs)
  debrief_text = "\n".join(debrief or [])
  
  cash_m = re.search(r"Cash:\s*(\d+)", text)
  if cash_m:
    metrics["Cash"] = cash_m.group(1)
    
  access_m = re.search(r"Reported access index:\s*(\d+)", text)
  if access_m:
    metrics["Access"] = access_m.group(1)

  beds_m = re.search(r"Staffed beds:\s*(\d+)", text)
  if beds_m:
    metrics["Beds"] = beds_m.group(1)
    
  wf_m = re.search(r"Workforce trust:\s*(\d+)", text)
  if wf_m:
    metrics["WorkforceTrust"] = wf_m.group(1)

  ct_m = re.search(r"Community trust:\s*(\d+)", text)
  if ct_m:
    metrics["CommunityTrust"] = ct_m.group(1)
    
  pol_m = re.search(r"Policy pressure:\s*(\d+)", text)
  if pol_m:
    metrics["Policy"] = pol_m.group(1)

  tradeoff_m = re.search(
    r"cash moved from \d+ to (\d+), access from \d+ to (\d+), workforce trust from \d+ to (\d+), community trust from \d+ to (\d+), policy pressure from \d+ to (\d+)",
    debrief_text
  )
  if tradeoff_m:
    metrics["Cash"] = tradeoff_m.group(1)
    metrics["Access"] = tradeoff_m.group(2)
    metrics["WorkforceTrust"] = tradeoff_m.group(3)
    metrics["CommunityTrust"] = tradeoff_m.group(4)
    metrics["Policy"] = tradeoff_m.group(5)

  return metrics

def parse_competitive_metrics(obs, history=None, debrief=None):
  metrics = {"Cash": "N/A", "Access": "N/A", "Beds": "N/A", "WorkforceTrust": "N/A", "CommunityTrust": "N/A", "PC": "N/A", "Hash": "N/A"}
  text = "\n".join(obs)
  debrief_text = "\n".join(debrief or [])

  # Check Riverside Community Health metrics block
  riverside_block = ""
  lines = text.split("\n")
  in_riverside = False
  for line in lines:
    if "RIVERSIDE COMMUNITY HEALTH" in line.upper():
      in_riverside = True
    elif in_riverside and len(line.strip()) == 0:
      # Blank line after block ends
      pass
    elif in_riverside and ("NORTHLAKE" in line.upper() or "SUMMIT" in line.upper() or "VALLEY" in line.upper()):
      in_riverside = False
    
    if in_riverside:
      riverside_block += line + "\n"

  cash_m = re.search(r"Cash runway:\s*\$?(-?\d+)", riverside_block)
  if not cash_m:
    cash_m = re.search(r"Cash:\s*\$?(-?\d+)", riverside_block)
  if cash_m:
    metrics["Cash"] = cash_m.group(1)

  access_m = re.search(r"Reported access:\s*(\d+)", riverside_block)
  if access_m:
    metrics["Access"] = access_m.group(1)

  beds_m = re.search(r"Staffed beds:\s*(\d+)", riverside_block)
  if beds_m:
    metrics["Beds"] = beds_m.group(1)

  wf_m = re.search(r"Workforce trust:\s*(\d+)", riverside_block)
  if not wf_m:
    wf_m = re.search(r"Workforce:\s*(\d+)", riverside_block)
  if wf_m:
    metrics["WorkforceTrust"] = wf_m.group(1)

  ct_m = re.search(r"Community trust:\s*(\d+)", riverside_block)
  if not ct_m:
    ct_m = re.search(r"Community:\s*(\d+)", riverside_block)
  if ct_m:
    metrics["CommunityTrust"] = ct_m.group(1)

  pc_m = re.search(r"Political capital:\s*(\d+)", riverside_block)
  if pc_m:
    metrics["PC"] = pc_m.group(1)

  if history:
    metrics["Hash"] = history[-1]["state_hash"]

  tradeoff_m = re.search(
    r"cash moved from -?\d+ to (-?\d+), access from \d+ to (\d+), quality from \d+ to \d+, workforce trust from \d+ to (\d+), community trust from \d+ to (\d+), and market share from \d+ to \d+",
    debrief_text
  )
  if tradeoff_m:
    metrics["Cash"] = tradeoff_m.group(1)
    metrics["Access"] = tradeoff_m.group(2)
    metrics["WorkforceTrust"] = tradeoff_m.group(3)
    metrics["CommunityTrust"] = tradeoff_m.group(4)

  resource_m = re.search(
    r"Final player resources: political capital (\d+), active projects \d+, active project monthly draws -?\d+, staffed beds (\d+)",
    debrief_text
  )
  if resource_m:
    metrics["PC"] = resource_m.group(1)
    metrics["Beds"] = resource_m.group(2)

  return metrics

def numeric_values(results, key):
  values = []
  for result in results:
    value = result["metrics"].get(key, "N/A")
    if value != "N/A":
      values.append(int(value))
  return values

def format_range(results, key):
  values = numeric_values(results, key)
  if not values:
    return "N/A"
  if min(values) == max(values):
    return str(values[0])
  return f"{min(values)}-{max(values)}"

def print_range_summary(title, results, keys):
  print("====================================================")
  print(title)
  print("====================================================")
  print(f"Sessions: {len(results)}")
  for key in keys:
    print(f"{key}: {format_range(results, key)}")
  print()

def run_tests():
  subprocess.run(
    ["cargo", "build", "--quiet", "--bin", "hs-mgt-game-mcp"],
    check=True
  )

  strategies = {
    "Fiscal Caution": policy_fiscal,
    "Capacity Growth": policy_growth,
    "Balanced Strategy": policy_balanced
  }

  print("====================================================")
  print("STARTING AUTOMATED GAMEPLAY PLAYTEST RUNS")
  print("====================================================\n")

  # 1. Run Stabilization Campaigns
  stab_results = []
  for seed in SEEDS:
    for name, policy in strategies.items():
      print(f"Running stabilization campaign for '{name}' with seed {seed}...")
      res = play_session("stabilization-v1", seed=seed, policy_fn=policy)
      if res:
        metrics = parse_stabilization_metrics(res["final_observation"], res["debrief"])
        stab_results.append({"seed": seed, "strategy": name, "metrics": metrics})
        print(f"  -> Done. Final Cash: {metrics['Cash']}, Reported Access: {metrics['Access']}\n")
      else:
        print(f"  -> Failed to execute run for '{name}' with seed {seed}\n")

  # 2. Run Competitive Campaigns
  comp_results = []
  for seed in SEEDS:
    for name, policy in strategies.items():
      print(f"Running competitive regional campaign for '{name}' with seed {seed}...")
      res = play_session("competitive-regional-v1", seed=seed, policy_fn=policy)
      if res:
        metrics = parse_competitive_metrics(res["final_observation"], res["history"], res["debrief"])
        comp_results.append({"seed": seed, "strategy": name, "metrics": metrics})
        print(f"  -> Done. Final Hash: {metrics['Hash']}\n")
      else:
        print(f"  -> Failed to execute run for '{name}' with seed {seed}\n")

  expected_sessions = len(SEEDS) * len(strategies)
  if len(stab_results) != expected_sessions or len(comp_results) != expected_sessions:
    raise RuntimeError(
      "Automated playtest batch incomplete: "
      f"stabilization {len(stab_results)}/{expected_sessions}, "
      f"competitive {len(comp_results)}/{expected_sessions}"
    )

  # Print Comparison Tables
  print("====================================================")
  print("STABILIZATION CAMPAIGN COMPARISON SUMMARY")
  print("====================================================")
  print(f"{'Seed':<6} | {'Strategy':<20} | {'Cash':<6} | {'Access':<8} | {'Beds':<6} | {'Workforce':<9} | {'Community':<9}")
  print("-" * 84)
  for result in stab_results:
    m = result["metrics"]
    print(f"{result['seed']:<6} | {result['strategy']:<20} | {m['Cash']:<6} | {m['Access']:<8} | {m['Beds']:<6} | {m['WorkforceTrust']:<9} | {m['CommunityTrust']:<9}")
  print()

  print("====================================================")
  print("COMPETITIVE CAMPAIGN COMPARISON SUMMARY")
  print("====================================================")
  print(f"{'Seed':<6} | {'Strategy':<20} | {'Final Hash':<16} | {'Cash':<6} | {'Access':<8} | {'Beds':<6} | {'Workforce':<9} | {'Community':<9} | {'PC':<4}")
  print("-" * 111)
  for result in comp_results:
    m = result["metrics"]
    print(f"{result['seed']:<6} | {result['strategy']:<20} | {m['Hash']:<16} | {m['Cash']:<6} | {m['Access']:<8} | {m['Beds']:<6} | {m['WorkforceTrust']:<9} | {m['CommunityTrust']:<9} | {m['PC']:<4}")
  print()

  print_range_summary(
    "STABILIZATION SEED-VARIATION RANGES",
    stab_results,
    ["Cash", "Access", "WorkforceTrust", "CommunityTrust", "Policy"]
  )
  print_range_summary(
    "COMPETITIVE SEED-VARIATION RANGES",
    comp_results,
    ["Cash", "Access", "Beds", "WorkforceTrust", "CommunityTrust", "PC"]
  )

if __name__ == "__main__":
  run_tests()
