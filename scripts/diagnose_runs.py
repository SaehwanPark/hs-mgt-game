#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

def parse_command_verb(cmd):
  if isinstance(cmd, str):
    return cmd
  if isinstance(cmd, dict):
    return list(cmd.keys())[0]
  return "Unknown"

def parse_summary_command_verbs(command_text):
  verbs = []
  for verb in ["Monitor", "Recruit", "Invest", "Negotiate", "Commit", "Project", "Hold"]:
    verbs.extend([verb] * command_text.count(verb))
  return verbs

def parse_summary_project_kinds(command_text):
  kinds = []
  for token in command_text.replace(";", " ").split():
    if token.startswith("kind="):
      kinds.append(token.split("=", 1)[1].strip())
  kinds.extend(re.findall(r"kind:\s*([A-Za-z]+)", command_text))
  return kinds

def classify_strategy(hold_count, verb_counts):
  total_commands = hold_count + sum(verb_counts.values())
  if total_commands == 0:
    return "Passive"
  
  if hold_count / total_commands >= 0.70:
    return "Conservative / Passive"
    
  non_hold_total = sum(verb_counts.values())
  if non_hold_total == 0:
    return "Conservative / Passive"
    
  # Check heuristics
  capacity_verbs = verb_counts.get("Invest", 0) + verb_counts.get("Project", 0)
  if capacity_verbs / non_hold_total >= 0.40:
    return "Capacity-Builder"
    
  if verb_counts.get("Negotiate", 0) / non_hold_total >= 0.40:
    return "Revenue-Optimizer"
    
  if verb_counts.get("Commit", 0) / non_hold_total >= 0.40:
    return "Public-Committed"
    
  if verb_counts.get("Monitor", 0) / non_hold_total >= 0.40:
    return "Intel-Gatherer"
    
  if verb_counts.get("Recruit", 0) / non_hold_total >= 0.40:
    return "Workforce-Focused"
    
  return "Balanced Strategy"

def analyze_single_run(file_path):
  try:
    with open(file_path, 'r') as f:
      data = json.load(f)
  except Exception as e:
    print(f"Error reading {file_path}: {e}", file=sys.stderr)
    return None

  # Basic check
  if "genesis" not in data or "transitions" not in data:
    print(f"Skipping {file_path}: does not match CompetitiveHistory structure.", file=sys.stderr)
    return None

  genesis = data["genesis"]
  transitions = data["transitions"]
  
  difficulty = genesis.get("difficulty", "Normal")
  rival_count = len(genesis.get("systems", [])) - 1
  total_turns = len(transitions)
  
  # Map system_id -> name
  system_names = {sys["system_id"]: sys["name"] for sys in genesis.get("systems", [])}
  
  # Initialize stats per system
  system_stats = {}
  for sys_id, name in system_names.items():
    system_stats[sys_id] = {
      "name": name,
      "holds": 0,
      "verbs": Counter(),
      "burnout_events": 0,
      "resource_trajectories": defaultdict(list)
    }

  # Walk transitions
  for transition in transitions:
    aggregated = transition.get("aggregated", {})
    next_state = transition.get("next", {})
    
    # Process commands in this month's batches
    batches = aggregated.get("batches", [])
    for batch in batches:
      sys_id = batch.get("system_id")
      if sys_id not in system_stats:
        continue
      
      commands = batch.get("commands", [])
      for cmd in commands:
        verb = parse_command_verb(cmd)
        if verb == "Hold":
          system_stats[sys_id]["holds"] += 1
        else:
          system_stats[sys_id]["verbs"][verb] += 1
          
    # Track resources from the resulting state
    next_systems = next_state.get("systems", [])
    for sys_state in next_systems:
      sys_id = sys_state.get("system_id")
      if sys_id not in system_stats:
        continue
      
      res = sys_state.get("resources", {})
      stats = system_stats[sys_id]
      stats["resource_trajectories"]["cash"].append(res.get("cash", 0))
      stats["resource_trajectories"]["political_capital"].append(res.get("political_capital", 0))
      stats["resource_trajectories"]["staffed_beds"].append(sys_state.get("staffed_beds", 0))
      stats["resource_trajectories"]["nurses"].append(sys_state.get("nurses", 0))
      stats["resource_trajectories"]["physicians"].append(sys_state.get("physicians", 0))
      stats["resource_trajectories"]["admins"].append(sys_state.get("admins", 0))
      stats["resource_trajectories"]["access_index"].append(sys_state.get("access_index", 0))
      stats["resource_trajectories"]["quality_index"].append(sys_state.get("quality_index", 0))
      stats["resource_trajectories"]["workforce_trust"].append(sys_state.get("workforce_trust", 0))
      stats["resource_trajectories"]["community_trust"].append(sys_state.get("community_trust", 0))
      stats["resource_trajectories"]["market_share_index"].append(sys_state.get("market_share_index", 0))

    # Look for events/burnout
    events = transition.get("events", [])
    for ev in events:
      ev_str = str(ev).lower()
      for sys_id, name in system_names.items():
        if name.lower() in ev_str and ("burnout" in ev_str or "understaffing" in ev_str):
          system_stats[sys_id]["burnout_events"] += 1

  # Package run info
  return {
    "filename": os.path.basename(file_path),
    "difficulty": difficulty,
    "rival_count": rival_count,
    "total_turns": total_turns,
    "system_stats": system_stats
  }

def analyze_playtest_batch(file_path, data):
  competitive = data.get("campaigns", {}).get("competitive-regional-v1", [])
  stabilization = data.get("campaigns", {}).get("stabilization-v1", [])
  if not competitive and not stabilization:
    print(f"Skipping {file_path}: playtest batch has no campaign results.", file=sys.stderr)
    return None

  profile_stats = {}
  for result in competitive:
    strategy = result.get("strategy", "Unknown")
    stats = profile_stats.setdefault(strategy, {
      "sessions": 0,
      "holds": 0,
      "verbs": Counter(),
      "validation_failures": 0,
      "cash": [],
      "access": [],
      "beds": [],
      "workforce_trust": [],
      "community_trust": [],
      "political_capital": [],
      "hashes": [],
      "active_projects": [],
      "active_project_draws": [],
      "project_kinds": Counter()
    })
    stats["sessions"] += 1
    stats["validation_failures"] += len(result.get("validation_failures", []))
    for transition in result.get("transitions", []):
      for verb in parse_summary_command_verbs(transition.get("command", "")):
        if verb == "Hold":
          stats["holds"] += 1
        else:
          stats["verbs"][verb] += 1
      for kind in parse_summary_project_kinds(transition.get("command", "")):
        stats["project_kinds"][kind] += 1
    metrics = result.get("metrics", {})
    for key, target in [
      ("Cash", "cash"),
      ("Access", "access"),
      ("Beds", "beds"),
      ("WorkforceTrust", "workforce_trust"),
      ("CommunityTrust", "community_trust"),
      ("PC", "political_capital"),
      ("ActiveProjects", "active_projects"),
      ("ActiveProjectDraws", "active_project_draws")
    ]:
      value = metrics.get(key)
      if value is not None and value != "N/A":
        stats[target].append(int(value))
    if metrics.get("Hash") and metrics["Hash"] != "N/A":
      stats["hashes"].append(metrics["Hash"])

  return {
    "filename": os.path.basename(file_path),
    "code_version": data.get("code_version", "unknown"),
    "seeds": data.get("seeds", []),
    "stabilization_sessions": len(stabilization),
    "competitive_sessions": len(competitive),
    "profile_stats": profile_stats
  }

def format_metric_range(values):
  if not values:
    return "N/A"
  if min(values) == max(values):
    return str(values[0])
  return f"{min(values)}-{max(values)}"

def print_run_markdown(run_data):
  print(f"## Diagnostic Report for `{run_data['filename']}`")
  print(f"- **Difficulty:** {run_data['difficulty']}")
  print(f"- **Rivals:** {run_data['rival_count']}")
  print(f"- **Turns Simulated:** {run_data['total_turns']} months\n")
  
  # Final State Table
  print("### Final Health System Metrics")
  print("| Health System | Cash | Staffed Beds | Nurses | Physicians | Admins | Access | Quality | Workforce Trust | Community Trust | Market Share |")
  print("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
  for sys_id, stats in run_data["system_stats"].items():
    traj = stats["resource_trajectories"]
    last_cash = traj["cash"][-1] if traj["cash"] else "N/A"
    last_beds = traj["staffed_beds"][-1] if traj["staffed_beds"] else "N/A"
    last_nurses = traj["nurses"][-1] if traj["nurses"] else "N/A"
    last_physicians = traj["physicians"][-1] if traj["physicians"] else "N/A"
    last_admins = traj["admins"][-1] if traj["admins"] else "N/A"
    last_access = traj["access_index"][-1] if traj["access_index"] else "N/A"
    last_quality = traj["quality_index"][-1] if traj["quality_index"] else "N/A"
    last_wf_trust = traj["workforce_trust"][-1] if traj["workforce_trust"] else "N/A"
    last_ct_trust = traj["community_trust"][-1] if traj["community_trust"] else "N/A"
    last_share = traj["market_share_index"][-1] if traj["market_share_index"] else "N/A"
    
    print(f"| {stats['name']} | {last_cash} | {last_beds} | {last_nurses} | {last_physicians} | {last_admins} | {last_access} | {last_quality} | {last_wf_trust} | {last_ct_trust} | {last_share}% |")
  print()

  # Command Choice and Strategy Table
  print("### Strategic Profile Summary")
  print("| Health System | Holds | Action Commands | Top Non-Hold Verb | Strategic Classification | Burnout/Penalty Events |")
  print("| --- | ---: | ---: | --- | --- | ---: |")
  for sys_id, stats in run_data["system_stats"].items():
    holds = stats["holds"]
    non_holds = sum(stats["verbs"].values())
    top_verb = stats["verbs"].most_common(1)
    top_verb_str = f"{top_verb[0][0]} ({top_verb[0][1]})" if top_verb else "None"
    strategy = classify_strategy(holds, stats["verbs"])
    print(f"| {stats['name']} | {holds} | {non_holds} | {top_verb_str} | {strategy} | {stats['burnout_events']} |")
  print()

def print_aggregated_markdown(runs):
  print("## Aggregated Diagnostics across Multiple Runs")
  print(f"- **Total Sessions Analyzed:** {len(runs)}")
  
  difficulties = Counter([r["difficulty"] for r in runs])
  diff_str = ", ".join([f"{k} ({v})" for k, v in difficulties.items()])
  print(f"- **Difficulty Distribution:** {diff_str}\n")

  # Compute ranges for Player System (ID 0)
  player_final_cash = []
  player_final_access = []
  player_final_wf_trust = []
  player_final_ct_trust = []
  player_strategies = Counter()
  
  for run in runs:
    player_stats = run["system_stats"].get(0)
    if not player_stats:
      continue
    traj = player_stats["resource_trajectories"]
    if traj["cash"]:
      player_final_cash.append(traj["cash"][-1])
    if traj["access_index"]:
      player_final_access.append(traj["access_index"][-1])
    if traj["workforce_trust"]:
      player_final_wf_trust.append(traj["workforce_trust"][-1])
    if traj["community_trust"]:
      player_final_ct_trust.append(traj["community_trust"][-1])
      
    strategy = classify_strategy(player_stats["holds"], player_stats["verbs"])
    player_strategies[strategy] += 1

  if player_final_cash:
    print("### Player Health System Outcome Ranges")
    print("| Metric | Minimum | Maximum | Average |")
    print("| --- | ---: | ---: | ---: |")
    print(f"| Cash | {min(player_final_cash)} | {max(player_final_cash)} | {sum(player_final_cash)/len(player_final_cash):.1f} |")
    print(f"| Access | {min(player_final_access)} | {max(player_final_access)} | {sum(player_final_access)/len(player_final_access):.1f} |")
    print(f"| Workforce Trust | {min(player_final_wf_trust)} | {max(player_final_wf_trust)} | {sum(player_final_wf_trust)/len(player_final_wf_trust):.1f} |")
    print(f"| Community Trust | {min(player_final_ct_trust)} | {max(player_final_ct_trust)} | {sum(player_final_ct_trust)/len(player_final_ct_trust):.1f} |")
    print()

    print("### Player Strategy Profile Distribution")
    print("| Strategy Profile | Occurrence Count | Percentage |")
    print("| --- | ---: | ---: |")
    for strat, count in player_strategies.items():
      pct = (count / len(runs)) * 100
      print(f"| {strat} | {count} | {pct:.1f}% |")
    print()

def print_playtest_batch_markdown(batch):
  print(f"## Playtest Batch Diagnostics for `{batch['filename']}`")
  print(f"- **Code version:** {batch['code_version']}")
  print(f"- **Seeds:** {', '.join(str(seed) for seed in batch['seeds'])}")
  print(f"- **Stabilization sessions:** {batch['stabilization_sessions']}")
  print(f"- **Competitive sessions:** {batch['competitive_sessions']}\n")

  print("### Competitive Profile Outcomes")
  print("| Profile | Sessions | Cash | Access | Beds | Workforce Trust | Community Trust | PC | Validation Failures | Representative Hashes |")
  print("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
  for profile, stats in batch["profile_stats"].items():
    hashes = ", ".join(stats["hashes"][:3]) if stats["hashes"] else "N/A"
    print(
      f"| {profile} | {stats['sessions']} | "
      f"{format_metric_range(stats['cash'])} | "
      f"{format_metric_range(stats['access'])} | "
      f"{format_metric_range(stats['beds'])} | "
      f"{format_metric_range(stats['workforce_trust'])} | "
      f"{format_metric_range(stats['community_trust'])} | "
      f"{format_metric_range(stats['political_capital'])} | "
      f"{stats['validation_failures']} | {hashes} |"
    )
  print()

  print("### Competitive Action Frequency Signals")
  print("| Profile | Holds | Action Commands | Project Commands | Top Non-Hold Verb | Strategy Classification |")
  print("| --- | ---: | ---: | ---: | --- | --- |")
  for profile, stats in batch["profile_stats"].items():
    non_holds = sum(stats["verbs"].values())
    project_commands = stats["verbs"].get("Project", 0)
    top_verb = stats["verbs"].most_common(1)
    top_verb_str = f"{top_verb[0][0]} ({top_verb[0][1]})" if top_verb else "None"
    strategy = classify_strategy(stats["holds"], stats["verbs"])
    print(f"| {profile} | {stats['holds']} | {non_holds} | {project_commands} | {top_verb_str} | {strategy} |")
  print()

  print("### Competitive Project Coverage")
  print("| Profile | Project Kinds | Final Active Projects | Final Monthly Draws |")
  print("| --- | --- | ---: | ---: |")
  for profile, stats in batch["profile_stats"].items():
    project_kinds = ", ".join(
      f"{kind} ({count})" for kind, count in stats["project_kinds"].most_common()
    ) or "None"
    print(
      f"| {profile} | {project_kinds} | "
      f"{format_metric_range(stats['active_projects'])} | "
      f"{format_metric_range(stats['active_project_draws'])} |"
    )
  print()

  print("### Evidence Limits")
  print("- Batch diagnostics use MCP transition summaries, final observations, and debriefs; they are not full replay artifacts.")
  print("- These diagnostics support gameplay and explanation review, not human-learning, empirical calibration, or policy-validity claims.")
  print("- Treat formula tuning or runtime expansion as a separate follow-up requiring stronger evidence.\n")

def main():
  parser = argparse.ArgumentParser(description="Strategy-Space Diagnostics for Health Policy Strategy Game")
  parser.add_argument("inputs", nargs="+", help="Paths to replay JSON files or directories containing replay files")
  parser.add_argument("--output", help="Output file path (saves as markdown; defaults to printing to stdout)")
  
  args = parser.parse_args()
  
  # Resolve inputs (handling directories)
  files = []
  for path in args.inputs:
    if os.path.isdir(path):
      for entry in os.listdir(path):
        if entry.endswith(".json"):
          files.append(os.path.join(path, entry))
    else:
      files.append(path)
      
  if not files:
    print("Error: No JSON replay files found.", file=sys.stderr)
    sys.exit(1)
    
  # Analyze
  runs = []
  batches = []
  for file in files:
    try:
      with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    except Exception as e:
      print(f"Error reading {file}: {e}", file=sys.stderr)
      continue

    if data.get("artifact_type") == "automated_playtest_batch":
      res = analyze_playtest_batch(file, data)
      if res:
        batches.append(res)
    else:
      res = analyze_single_run(file)
      if res:
        runs.append(res)
      
  if not runs and not batches:
    print("Error: No runs could be successfully parsed.", file=sys.stderr)
    sys.exit(1)
    
  # Redirect output if requested
  original_stdout = sys.stdout
  if args.output:
    try:
      sys.stdout = open(args.output, "w")
    except Exception as e:
      print(f"Error opening output file {args.output}: {e}", file=sys.stderr)
      sys.exit(1)
      
  # Print reports
  print("# Strategy-Space Diagnostic Report")
  print("This diagnostic summary maps strategic actions, outcome distributions, and strategy-cluster classifications.\n")
  
  for batch in batches:
    print_playtest_batch_markdown(batch)
    print("---")

  for run in runs:
    print_run_markdown(run)
    print("---")
    
  if len(runs) > 1:
    print_aggregated_markdown(runs)
    
  # Clean up stdout redirect
  if args.output:
    sys.stdout.close()
    sys.stdout = original_stdout
    print(f"Diagnostic report written successfully to {args.output}")

if __name__ == "__main__":
  main()
