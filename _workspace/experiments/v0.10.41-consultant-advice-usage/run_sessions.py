import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT / "scripts"))

from play_game import play_session  # noqa: E402
from run_automated_playtests import (  # noqa: E402
  TARGET_DIFFICULTY_SWEEP,
  code_version,
  policy_for_competitive,
  strategies_for_target,
)

BATCH_ID = "v0.10.41-consultant-advice-usage"
CAMPAIGN = "competitive-regional-v1"
SEEDS = [42, 43, 44]
DIFFICULTIES = ["normal", "hard"]
PROFILES = ["Fiscal Caution", "Naive First-Time"]
EXPECTED_TRANSITIONS = 24
OPTION_RE = re.compile(r"^Option ([A-D]) — (.+)$")
TRADEOFF_RE = re.compile(r"^\s*Tradeoff: (.+)$")
RESOURCES_RE = re.compile(
  r"Available resources: AP (\d+), cash (\d+), political capital (\d+)"
)
DRAW_RE = re.compile(r"(\d+)k/mo draw")


def parse_rendered_options(observation):
  options = []
  current = None
  for line in observation:
    match = OPTION_RE.match(line)
    if match:
      current = {
        "label": match.group(1),
        "title": match.group(2),
        "tradeoff_bullets": [],
      }
      options.append(current)
      continue
    match = TRADEOFF_RE.match(line)
    if match and current is not None:
      current["tradeoff_bullets"].append(match.group(1))
  return options


def normalize_options(options):
  return [
    {
      "label": option["label"],
      "title": option["title"],
      "tradeoff_bullets": option["tradeoff_bullets"],
    }
    for option in options
  ]


def parse_resources(legal):
  for line in legal:
    match = RESOURCES_RE.search(line)
    if match:
      return tuple(int(value) for value in match.groups())
  return None


def parse_active_project_draw(observation):
  draws = []
  for line in observation:
    match = DRAW_RE.search(line)
    if match:
      draws.append(int(match.group(1)))
  return sum(draws)


def select_option(observation, options, profile_name):
  text = "\n".join(observation).upper()
  available = {option["label"] for option in options}
  priorities = {
    "Fiscal Caution": [
      ("C", "rival intelligence gap", "INTEL GAP" in text),
      ("B", "visible nursing pressure", "WORKFORCE TRUST: STRAINED" in text or "VACANCY" in text),
      ("D", "access scrutiny", "ACCESS" in text and ("SCRUTINY" in text or "MANDATE" in text)),
      ("A", "low reported access with runway capacity", low_access_with_runway(text)),
    ],
    "Naive First-Time": [
      ("B", "visible nursing pressure", "WORKFORCE TRUST: STRAINED" in text or "VACANCY" in text),
      ("D", "access scrutiny", "ACCESS" in text and ("SCRUTINY" in text or "MANDATE" in text)),
      ("A", "low reported access with runway capacity", low_access_with_runway(text)),
      ("C", "rival intelligence gap", "INTEL GAP" in text),
    ],
  }
  for label, reason, condition in priorities[profile_name]:
    if condition and label in available:
      return {
        "label": label,
        "mode": "selected",
        "reason": reason,
        "cue": reason,
      }
  return {
    "label": None,
    "mode": "declined",
    "reason": "no selected option was supported by a visible cue",
    "cue": None,
  }


def low_access_with_runway(text):
  access = re.search(r"REPORTED ACCESS INDEX: (\d+)", text)
  return bool(
    access
    and int(access.group(1)) <= 70
    and ("CASH RUNWAY: COMFORTABLE" in text or "CASH RUNWAY: WATCH" in text)
  )


def build_option_command(label, legal, observation):
  resources = parse_resources(legal)
  if resources is None:
    return None, "visible resource line was missing"
  ap, cash, political_capital = resources
  project_draw = parse_active_project_draw(observation)
  if ap < 1:
    return None, "insufficient action points"
  if label == "A":
    if cash < project_draw + 6:
      return None, "insufficient cash for investment and active project draws"
    return "invest domain=beds amount=6; hold", None
  if label == "B":
    if cash < project_draw + 5:
      return None, "insufficient cash for recruitment and active project draws"
    return "recruit role=nurse headcount=1; hold", None
  if label == "C":
    return "monitor target=northlake depth=1; hold", None
  if label == "D":
    if political_capital < 1:
      return None, "insufficient political capital"
    return "commit pledge_type=access level=1; hold", None
  return None, f"unsupported consultant option label {label!r}"


def visible_command_budget(command, legal, observation):
  resources = parse_resources(legal)
  if resources is None:
    return False, "visible resource line was missing"
  ap, cash, political_capital = resources
  required_ap = 0
  required_cash = parse_active_project_draw(observation)
  required_political_capital = 0
  for part in command.lower().split(";"):
    words = part.strip().split()
    if not words or words[0] == "hold":
      continue
    verb = words[0]
    required_ap += 1
    if verb == "recruit":
      match = re.search(r"headcount=(\d+)", part)
      if not match:
        return False, "recruitment headcount was not visible"
      required_cash += 5 * int(match.group(1))
    elif verb == "invest":
      match = re.search(r"amount=(\d+)", part)
      if not match:
        return False, "investment amount was not visible"
      required_cash += int(match.group(1))
    elif verb == "monitor":
      match = re.search(r"depth=(\d+)", part)
      if not match:
        return False, "monitor depth was not visible"
      required_ap += int(match.group(1)) - 1
    elif verb == "commit":
      required_political_capital += 1
    elif verb == "negotiate":
      required_political_capital += 2
      if "payer=medicaid" in part:
        required_cash += 5
      elif "payer=medicare" in part:
        required_cash += 10
    elif verb == "project":
      return False, "project draw and concurrency were not fully visible"
    else:
      return False, f"unsupported command verb {verb!r}"
  if required_ap > ap:
    return False, "inherited command exceeded visible action points"
  if required_cash > cash:
    return False, "inherited command exceeded visible cash after active draws"
  if required_political_capital > political_capital:
    return False, "inherited command exceeded visible political capital"
  return True, None


def command_alignment(command):
  mapping = {"invest": "A", "recruit": "B", "monitor": "C", "commit": "D"}
  labels = []
  for part in command.lower().split(";"):
    verb = part.strip().split(maxsplit=1)[0] if part.strip() else ""
    if verb in mapping:
      labels.append(mapping[verb])
  return labels or ["none"]


def advice_policy(base_policy, profile_name, decisions):
  def policy(observation, legal, turn):
    options = parse_rendered_options(observation)
    decision = select_option(observation, options, profile_name)
    command = None
    fallback_reason = None
    if decision["label"] is not None:
      command, fallback_reason = build_option_command(
        decision["label"], legal, observation
      )
    if command is None:
      command = base_policy(observation, legal, turn)
      if decision["label"] is not None:
        decision["mode"] = "fallback"
        decision["reason"] = fallback_reason or "selected option was not executable"
    else:
      decision["mode"] = "followed"
    budget_ok, budget_reason = visible_command_budget(command, legal, observation)
    if not budget_ok:
      command = "hold"
      decision["mode"] = "safe-hold"
      decision["reason"] = budget_reason
    decisions.append({
      "turn": turn,
      "options": normalize_options(options),
      "selected_option_label": decision["label"],
      "decision_mode": decision["mode"],
      "decision_reason": decision["reason"],
      "visible_cue": decision["cue"],
      "command": command,
      "command_alignment": command_alignment(command),
    })
    return command

  return policy


def load_control_hashes():
  path = ROOT / "_workspace/experiments/v0.10.40-consultant-advice-evidence/results.json"
  artifact = json.loads(path.read_text(encoding="utf-8"))
  return {
    (run["profile_name"], run["seed"], run["difficulty"]): run["state_hashes"]
    for run in artifact["runs"]
    if run["profile_name"] in PROFILES
  }


def run_profile(seed, difficulty, profile_name, base_policy, mode, control_hashes):
  decisions = []
  policy = policy_for_competitive(base_policy, difficulty, TARGET_DIFFICULTY_SWEEP)
  if mode == "advice-aware":
    policy = advice_policy(policy, profile_name, decisions)
  result = play_session(
    CAMPAIGN,
    seed=seed,
    difficulty=difficulty,
    policy_fn=policy,
    capture_trace=True,
  )
  if result is None:
    raise RuntimeError(f"No result for {profile_name}/{mode}/{seed}/{difficulty}")

  exact_matches = 0
  trace_rows = []
  for index, entry in enumerate(result["turn_trace"]):
    transition = entry.get("latest_transition")
    if transition is None:
      continue
    rendered = normalize_options(parse_rendered_options(entry["observation"]))
    stored = normalize_options(transition.get("consultant_options", []))
    matches = rendered == stored
    if matches:
      exact_matches += 1
    if mode == "advice-aware":
      decision = decisions[index]
    else:
      decision = {
        "options": rendered,
        "selected_option_label": None,
        "decision_mode": "ignored",
        "decision_reason": "control policy does not inspect consultant options",
        "visible_cue": None,
        "command": entry["submitted_command"],
        "command_alignment": command_alignment(entry["submitted_command"]),
      }
    trace_rows.append({
      "turn": entry["turn"],
      "command": entry["submitted_command"],
      "rendered_options": rendered,
      "stored_options": stored,
      "rendered_matches_stored": matches,
      **decision,
    })

  state_hashes = [transition["state_hash"] for transition in result["history"]]
  expected_hashes = control_hashes.get((profile_name, seed, difficulty))
  control_hash_match = state_hashes == expected_hashes if mode == "control" else None
  return {
    "profile_name": profile_name,
    "mode": mode,
    "seed": seed,
    "difficulty": difficulty,
    "completion_status": "complete" if len(state_hashes) == EXPECTED_TRANSITIONS else "incomplete",
    "transition_count": len(state_hashes),
    "validation_failures": result["validation_failures"],
    "state_hashes": state_hashes,
    "final_hash": state_hashes[-1] if state_hashes else None,
    "control_hash_match": control_hash_match,
    "exact_observation_history_matches": exact_matches,
    "debrief_option_lines": sum(
      "Consultant options shown:" in line for line in result["debrief"]
    ),
    "trace": trace_rows,
  }


def validate_runs(runs):
  for run in runs:
    name = f"{run['profile_name']}/{run['mode']}/{run['seed']}/{run['difficulty']}"
    if run["completion_status"] != "complete":
      raise RuntimeError(f"{name}: incomplete competitive session")
    if run["validation_failures"]:
      raise RuntimeError(f"{name}: validation failures were captured")
    if run["exact_observation_history_matches"] != EXPECTED_TRANSITIONS:
      raise RuntimeError(f"{name}: rendered and committed options diverged")
    if run["debrief_option_lines"] != EXPECTED_TRANSITIONS:
      raise RuntimeError(f"{name}: debrief did not retain every advisory record")
    if run["mode"] == "control" and not run["control_hash_match"]:
      raise RuntimeError(f"{name}: control hashes changed from v0.10.40")
    if len(run["trace"]) != EXPECTED_TRANSITIONS:
      raise RuntimeError(f"{name}: decision trace is incomplete")


def render_diagnostics(artifact):
  lines = [
    f"# Consultant Advice Usage Diagnostics for `{artifact['filename']}`",
    f"- **Batch id:** {artifact['batch_id']}",
    f"- **Code version:** {artifact['code_version']}",
    f"- **Evidence type:** {artifact['evidence_type']}",
    "",
    "## Run Results",
    "| Profile | Mode | Seed | Difficulty | Months | Validation failures | Exact continuity | Debrief records | Final hash | Control hashes |",
    "| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | --- | --- |",
  ]
  for run in artifact["runs"]:
    lines.append(
      f"| {run['profile_name']} | {run['mode']} | {run['seed']} | {run['difficulty']} | "
      f"{run['transition_count']} | {len(run['validation_failures'])} | "
      f"{run['exact_observation_history_matches']} | {run['debrief_option_lines']} | "
      f"{run['final_hash']} | {run['control_hash_match'] if run['control_hash_match'] is not None else 'n/a'} |"
    )
  lines.extend([
    "",
    "## Advice-Aware Decision Signals",
    "These counts describe deterministic policy choices and command alignment. They do not measure advice uptake, quality, causal impact, or learning.",
    "",
    "| Profile | Seed | Difficulty | Followed | Fallback | Safe hold | Declined | A | B | C | D |",
    "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
  ])
  for run in artifact["runs"]:
    if run["mode"] != "advice-aware":
      continue
    modes = Counter(row["decision_mode"] for row in run["trace"])
    labels = Counter(
      row["selected_option_label"]
      for row in run["trace"]
      if row["selected_option_label"] is not None
    )
    lines.append(
      f"| {run['profile_name']} | {run['seed']} | {run['difficulty']} | "
      f"{modes.get('followed', 0)} | {modes.get('fallback', 0)} | "
      f"{modes.get('safe-hold', 0)} | {modes.get('declined', 0)} | "
      f"{labels.get('A', 0)} | {labels.get('B', 0)} | {labels.get('C', 0)} | "
      f"{labels.get('D', 0)} |"
    )
  lines.extend([
    "",
    "## Evidence Limits",
    "- Advice-aware and control policies are deterministic simulated agents, not human players.",
    "- Changing the policy changes commands and outcomes; paired runs do not establish causal advice value.",
    "- The capture tests visible option interpretation, fallback behavior, and observation/history/debrief continuity.",
    "- A future advisor-market slice remains deferred unless a separate finding identifies a concrete limitation in the generic baseline.",
  ])
  return "\n".join(lines) + "\n"


def main():
  os.chdir(ROOT)
  subprocess.run(
    ["cargo", "build", "--quiet", "--bin", "hs-mgt-game-mcp"],
    check=True,
  )
  control_hashes = load_control_hashes()
  strategies = strategies_for_target(TARGET_DIFFICULTY_SWEEP)
  runs = []
  for seed in SEEDS:
    for difficulty in DIFFICULTIES:
      for profile_name in PROFILES:
        base_policy = strategies[profile_name]
        runs.append(run_profile(
          seed, difficulty, profile_name, base_policy, "control", control_hashes
        ))
        runs.append(run_profile(
          seed, difficulty, profile_name, base_policy, "advice-aware", control_hashes
        ))

  validate_runs(runs)
  artifact = {
    "filename": "results.json",
    "batch_id": BATCH_ID,
    "code_version": code_version(),
    "campaign": CAMPAIGN,
    "seeds": SEEDS,
    "difficulties": DIFFICULTIES,
    "profiles": PROFILES,
    "evidence_type": "deterministic MCP capture of advice-aware and advice-ignoring simulated policy decisions",
    "runs": runs,
  }
  output_dir = Path(__file__).parent
  (output_dir / "results.json").write_text(
    json.dumps(artifact, indent=2) + "\n", encoding="utf-8"
  )
  (output_dir / "diagnostics.md").write_text(
    render_diagnostics(artifact), encoding="utf-8"
  )
  print(f"wrote {output_dir / 'results.json'}")
  print(f"wrote {output_dir / 'diagnostics.md'}")


if __name__ == "__main__":
  main()
