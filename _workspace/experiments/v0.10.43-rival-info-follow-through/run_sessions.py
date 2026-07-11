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
from run_automated_playtests import code_version  # noqa: E402


BATCH_ID = "v0.10.43-rival-info-follow-through"
CAMPAIGN = "competitive-regional-v1"
SEEDS = [42, 43, 44]
DIFFICULTIES = ["hard", "expert"]
VARIANTS = ["monitor-reactive", "monitor-ignoring", "unmonitored"]
EXPECTED_TRANSITIONS = 24

MONITOR_TARGETS = ["northlake", "summit", "valley", "metro"]
BASE_COMMANDS = {
  2: "negotiate payer=carrier_a rate_posture=conservative; hold",
  4: "recruit role=nurse headcount=1; hold",
  6: "negotiate payer=medicaid rate_posture=neutral; hold",
  8: "commit pledge_type=workforce level=1; hold",
  10: "negotiate payer=carrier_a rate_posture=conservative; hold",
  12: "negotiate payer=medicare rate_posture=neutral; hold",
  14: "invest domain=emergency amount=3; hold",
  16: "negotiate payer=carrier_b rate_posture=conservative; hold",
  18: "commit pledge_type=quality level=1; hold",
  20: "negotiate payer=carrier_a rate_posture=conservative; hold",
  22: "invest domain=asc amount=3; hold",
  24: "hold",
}
RESOURCES_RE = re.compile(
  r"Available resources: AP (\d+), cash (\d+), political capital (\d+)"
)
MONITOR_SIGNAL_RE = re.compile(r"\(monitor intel, month (\d+)\):")
HEADCOUNT_RE = re.compile(r"headcount=(\d+)")
AMOUNT_RE = re.compile(r"amount=(\d+)")


def monitor_command(turn):
  if turn % 2 == 1:
    target = MONITOR_TARGETS[((turn - 1) // 2) % len(MONITOR_TARGETS)]
    return f"monitor target={target} depth=1; hold"
  return BASE_COMMANDS.get(turn, "hold")


def unmonitored_command(turn):
  if turn % 2 == 1:
    return "hold"
  return BASE_COMMANDS.get(turn, "hold")


def classify_monitor_signal(signal_text):
  text = signal_text.lower()
  if "payer" in text or "carrier" in text or "negotiat" in text:
    return "payer"
  if "invest" in text or "capacity" in text or "beds" in text:
    return "capacity"
  if "recruit" in text or "workforce" in text or "nurse" in text:
    return "workforce"
  if "pledge" in text or "access" in text:
    return "access"
  return "other"


def extract_monitor_signals(observation, observation_turn):
  signals = []
  for line in observation:
    match = MONITOR_SIGNAL_RE.search(line)
    if match:
      signals.append({
        "observation_turn": observation_turn,
        "source_month": int(match.group(1)),
        "signal_kind": classify_monitor_signal(line),
        "signal_text": line,
      })
  return signals


def parse_resources(legal):
  for line in legal:
    match = RESOURCES_RE.search(line)
    if match:
      return tuple(int(value) for value in match.groups())
  return None


def parse_active_project_draw(observation):
  return sum(
    int(match.group(1))
    for line in observation
    if (match := re.search(r"(\d+)k/mo draw", line))
  )


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
      match = HEADCOUNT_RE.search(part)
      if not match:
        return False, "recruitment headcount was not visible"
      required_cash += 5 * int(match.group(1))
    elif verb == "invest":
      match = AMOUNT_RE.search(part)
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
    else:
      return False, f"unsupported response command verb {verb!r}"
  if required_ap > ap:
    return False, "visible action points were insufficient"
  if required_cash > cash:
    return False, "visible cash was insufficient after active draws"
  if required_political_capital > political_capital:
    return False, "visible political capital was insufficient"
  return True, None


def response_command_for_signal(signal, legal, observation):
  signal_kind = signal["signal_kind"]
  text = signal["signal_text"].lower()
  if signal_kind == "payer":
    if "carrierb" in text or "carrier_b" in text:
      command = "negotiate payer=carrier_b rate_posture=neutral; hold"
    else:
      command = "negotiate payer=carrier_a rate_posture=neutral; hold"
  elif signal_kind == "capacity":
    command = "invest domain=beds amount=3; hold"
  elif signal_kind == "workforce":
    command = "recruit role=nurse headcount=1; hold"
  elif signal_kind == "access":
    command = "commit pledge_type=access level=1; hold"
  else:
    return "hold", "visible monitor signal was not mapped to a response"

  affordable, reason = visible_command_budget(command, legal, observation)
  if not affordable:
    return "hold", reason
  return command, None


def final_hash(result):
  return result["history"][-1]["state_hash"] if result["history"] else None


def failed_run(seed, difficulty, variant, error):
  return {
    "profile_id": f"rival_info_{variant}",
    "profile_name": f"Rival Information {variant} / {difficulty}",
    "policy_variant": variant,
    "seed": seed,
    "difficulty": difficulty,
    "completion_status": "failed",
    "run_error": error,
    "turn_trace": [],
    "commands": [],
    "validation_failures": [],
    "transition_count": 0,
    "state_hashes": [],
    "final_hash": None,
    "final_observation": [],
    "debrief": [],
    "response_records": [],
    "monitor_signal_count": 0,
  }


def run_variant(seed, difficulty, variant):
  response_records = []

  def policy(observation, legal, turn):
    signals = extract_monitor_signals(observation, turn)
    if variant == "monitor-reactive" and signals:
      selected_signal = signals[-1]
      command, fallback_reason = response_command_for_signal(
        selected_signal,
        legal,
        observation,
      )
      mode = "responded" if command != "hold" else "safe-hold"
      for signal in signals:
        response_records.append({
          **signal,
          "response_turn": turn,
          "response_command": command,
          "decision_mode": mode,
          "used_signal": signal is selected_signal,
          "fallback_reason": fallback_reason,
        })
      return command

    command = monitor_command(turn) if variant != "unmonitored" else unmonitored_command(turn)
    if variant == "monitor-ignoring" and signals:
      for signal in signals:
        response_records.append({
          **signal,
          "response_turn": turn,
          "response_command": command,
          "decision_mode": "ignored",
          "used_signal": False,
          "fallback_reason": None,
        })
    return command

  try:
    result = play_session(
      CAMPAIGN,
      seed=seed,
      difficulty=difficulty,
      policy_fn=policy,
      capture_trace=True,
    )
  except RuntimeError as err:
    return failed_run(seed, difficulty, variant, str(err))
  if result is None:
    return failed_run(seed, difficulty, variant, "play_session returned no result")

  commands = [
    entry["submitted_command"]
    for entry in result.get("turn_trace", [])
    if entry["latest_transition"] is not None
  ]
  signal_count = sum(
    len(extract_monitor_signals(entry["observation"], entry["turn"]))
    for entry in result.get("turn_trace", [])
  )
  return {
    "profile_id": f"rival_info_{variant}",
    "profile_name": f"Rival Information {variant} / {difficulty}",
    "persona_prompt": (
      "Deterministic monitor follow-through policy. Reactive runs respond only "
      "to monitor intel visible in the immediately preceding MCP observation; "
      "control runs either ignore or do not receive that intel."
    ),
    "decision_source": "actor-visible MCP observation and legal resource hints",
    "policy_variant": variant,
    "seed": seed,
    "difficulty": difficulty,
    "completion_status": (
      "complete" if len(result["history"]) == EXPECTED_TRANSITIONS else "incomplete"
    ),
    "turn_trace": result.get("turn_trace", []),
    "commands": commands,
    "validation_failures": result["validation_failures"],
    "transition_count": len(result["history"]),
    "state_hashes": [transition["state_hash"] for transition in result["history"]],
    "final_hash": final_hash(result),
    "final_observation": result["final_observation"],
    "debrief": result["debrief"],
    "response_records": response_records,
    "monitor_signal_count": signal_count,
  }


def validate_runs(runs):
  expected = len(SEEDS) * len(DIFFICULTIES) * len(VARIANTS)
  if len(runs) != expected:
    raise AssertionError(f"expected {expected} runs, got {len(runs)}")
  for run in runs:
    if run["completion_status"] != "complete":
      raise AssertionError(f"incomplete run: {run['profile_name']}")
    if run["transition_count"] != EXPECTED_TRANSITIONS:
      raise AssertionError(f"wrong transition count: {run['profile_name']}")
    if run["validation_failures"]:
      raise AssertionError(f"validation failure: {run['profile_name']}")
    for record in run["response_records"]:
      if record["response_turn"] != record["observation_turn"]:
        raise AssertionError("monitor responses must use the next visible observation")

  for seed in SEEDS:
    for difficulty in DIFFICULTIES:
      controls = {
        run["policy_variant"]: run
        for run in runs
        if run["seed"] == seed and run["difficulty"] == difficulty
      }
      if controls["monitor-ignoring"]["state_hashes"] != controls["unmonitored"]["state_hashes"]:
        raise AssertionError(f"observation-only control hashes diverged for {seed}/{difficulty}")


def render_diagnostics(artifact):
  lines = [
    "# Rival Information Follow-Through Diagnostics",
    "",
    f"- **Batch id:** {artifact['batch_id']}",
    f"- **Code version:** {artifact['code_version']}",
    f"- **Evidence type:** {artifact['evidence_type']}",
    "",
    "## Run Summary",
    "",
    "| Variant | Seed | Difficulty | Status | Transitions | Signals | Responses | Safe hold | Final hash |",
    "| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |",
  ]
  for run in artifact["runs"]:
    modes = Counter(record["decision_mode"] for record in run["response_records"])
    lines.append(
      f"| {run['policy_variant']} | {run['seed']} | {run['difficulty']} | "
      f"{run['completion_status']} | {run['transition_count']} | "
      f"{run['monitor_signal_count']} | {modes.get('responded', 0)} | "
      f"{modes.get('safe-hold', 0)} | {run['final_hash']} |"
    )
  lines.extend([
    "",
    "## Follow-Through Records",
    "",
    "| Variant | Seed | Difficulty | Signal month | Response month | Kind | Mode | Command |",
    "| --- | ---: | --- | ---: | ---: | --- | --- | --- |",
  ])
  for run in artifact["runs"]:
    for record in run["response_records"]:
      lines.append(
        f"| {run['policy_variant']} | {run['seed']} | {run['difficulty']} | "
        f"{record['source_month']} | {record['response_turn']} | "
        f"{record['signal_kind']} | {record['decision_mode']} | "
        f"{record['response_command']} |"
      )
  lines.extend([
    "",
    "These are deterministic simulated-policy traces. They establish visible "
    "signal-to-command traceability only; they do not establish causal value, "
    "decision quality, human learning, balance, or policy validity.",
    "",
  ])
  return "\n".join(lines)


def main():
  os.chdir(ROOT)
  subprocess.run(
    ["cargo", "build", "--quiet", "--bin", "hs-mgt-game-mcp"],
    check=True,
  )
  runs = [
    run_variant(seed, difficulty, variant)
    for seed in SEEDS
    for difficulty in DIFFICULTIES
    for variant in VARIANTS
  ]
  validate_runs(runs)
  artifact = {
    "filename": "results.json",
    "batch_id": BATCH_ID,
    "code_version": code_version(),
    "campaign": CAMPAIGN,
    "seeds": SEEDS,
    "difficulties": DIFFICULTIES,
    "variants": VARIANTS,
    "evidence_type": (
      "deterministic MCP capture comparing monitor-reactive, monitor-ignoring, "
      "and unmonitored simulated policies"
    ),
    "runs": runs,
  }
  output_dir = Path(__file__).parent
  (output_dir / "results.json").write_text(
    json.dumps(artifact, indent=2) + "\n",
    encoding="utf-8",
  )
  (output_dir / "diagnostics.md").write_text(
    render_diagnostics(artifact),
    encoding="utf-8",
  )
  print(f"wrote {output_dir / 'results.json'}")
  print(f"wrote {output_dir / 'diagnostics.md'}")


if __name__ == "__main__":
  main()
