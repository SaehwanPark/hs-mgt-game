#!/usr/bin/env python3
"""Audit command-to-effect traceability in an existing MCP evidence artifact."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BATCH_ID = "v0.10.47-command-effect-explainability"
CODE_VERSION = "0.10.47"
CAMPAIGN = "competitive-regional-v1"
SOURCE_PATH = (
  ROOT
  / "_workspace"
  / "experiments"
  / "v0.10.46-expert-clearability-evidence"
  / "results.json"
)

KNOWN_VERBS = {
  "monitor",
  "recruit",
  "invest",
  "negotiate",
  "commit",
  "project",
  "hold",
}

SIGNATURES = {
  "monitor": ("monitoring",),
  "recruit": ("recruiting", "delayed recruitment resolves"),
  "invest": ("investing", "capacity investment"),
  "negotiate": ("payer negotiation", "compliance alignment"),
  "commit": ("public pledge",),
  "project": ("capital project", "project"),
}

LIMITATIONS = [
  "Coverage is traceability evidence, not causal evidence.",
  "The source contains deterministic simulated-policy traces, not human or classroom sessions.",
  "Aggregated transition effects do not prove that a command caused an endpoint metric.",
  "A supported trace does not establish decision quality, balance, learning, or policy validity.",
]


def load_artifact(path=SOURCE_PATH):
  return json.loads(Path(path).read_text(encoding="utf-8"))


def parse_commands(command_text):
  commands = []
  for raw in str(command_text or "").split(";"):
    text = raw.strip()
    if not text:
      continue
    parts = text.split(maxsplit=1)
    verb = parts[0].lower()
    commands.append(
      {
        "raw": text,
        "verb": verb if verb in KNOWN_VERBS else "unknown",
        "args": parts[1] if len(parts) == 2 else "",
      }
    )
  return commands


def _argument(command, name):
  match = re.search(rf"(?:^|\s){re.escape(name)}=([^\s]+)", command["raw"])
  return match.group(1).lower() if match else ""


def _organization(run):
  for entry in run.get("turn_trace", []):
    for line in entry.get("observation", []):
      if isinstance(line, str) and line.startswith("Organization:"):
        return line.split(":", 1)[1].strip()
  return ""


def _player_text(transition, organization):
  events = transition.get("events", [])
  if organization:
    owner = organization.lower()
    events = [event for event in events if owner in str(event).lower()]
  else:
    events = []
  effects = transition.get("effects", [])
  return " ".join(str(value) for value in [*events, *effects]).lower()


def _signature_terms(command):
  verb = command["verb"]
  terms = list(SIGNATURES.get(verb, ()))
  if verb == "monitor":
    target = _argument(command, "target")
    if target:
      terms.insert(0, f"monitoring {target}")
  elif verb == "recruit":
    role = _argument(command, "role")
    if role:
      terms.insert(0, f"recruiting")
      terms.insert(1, role)
  elif verb == "invest":
    domain = _argument(command, "domain")
    if domain:
      terms.insert(0, f"investing")
      terms.insert(1, domain)
  elif verb == "negotiate":
    payer = _argument(command, "payer")
    if payer:
      terms.insert(0, payer)
  elif verb == "commit":
    pledge_type = _argument(command, "pledge_type")
    if pledge_type:
      terms.insert(0, f"public {pledge_type} pledge")
  elif verb == "project":
    kind = _argument(command, "kind")
    if kind:
      terms.insert(0, kind.replace("_", " "))
  return terms


def _matches(command, text):
  if command["verb"] == "hold":
    return True, "neutral action; no effect required"
  terms = _signature_terms(command)
  if command["verb"] == "recruit" and "recruiting" in text:
    return True, "player recruitment event/effect"
  if command["verb"] == "invest" and "investing" in text:
    return True, "player investment event/effect"
  if command["verb"] == "project" and "capital project" in text:
    return True, "player capital-project event/effect"
  if any(term in text for term in terms):
    return True, "action-specific event/effect"
  return False, "no action-specific event/effect matched"


def _debrief_command_present(debrief, command):
  verb = command["verb"]
  if verb == "unknown":
    return False
  raw = command["raw"].lower()
  for line in debrief:
    if not isinstance(line, str) or not line.startswith("Player:"):
      continue
    if raw in line.lower():
      return True
    if verb in line.lower() and all(
      token in line.lower()
      for token in re.findall(r"(?:target|role|domain|payer|pledge_type|kind)=([^\s;]+)", raw)
    ):
      return True
  return False


def audit_run(run):
  organization = _organization(run)
  trace = run.get("turn_trace", [])
  debrief = run.get("debrief", []) or []
  command_records = []
  deferred_records = []

  for index, entry in enumerate(trace):
    transition = entry.get("latest_transition") or {}
    immediate_text = _player_text(transition, organization)
    for command in parse_commands(entry.get("submitted_command", "")):
      immediate_match, reason = _matches(command, immediate_text)
      later_match = False
      if not immediate_match and command["verb"] not in {"hold", "unknown"}:
        for later_entry in trace[index + 1 :]:
          later_text = _player_text(later_entry.get("latest_transition") or {}, organization)
          later_match, later_reason = _matches(command, later_text)
          if later_match:
            reason = f"deferred {later_reason}"
            deferred_records.append(
              {"turn": entry.get("turn"), "command": command["raw"], "resolved_turn": later_entry.get("turn")}
            )
            break
      recorded = _debrief_command_present(debrief, command)
      command_records.append(
        {
          "turn": entry.get("turn"),
          "command": command["raw"],
          "verb": command["verb"],
          "transition_evidence": immediate_match or later_match,
          "debrief_evidence": recorded,
          "status": "supported" if (immediate_match or later_match) and recorded else "limited",
          "reason": reason,
        }
      )

  unsupported = [record for record in command_records if not record["transition_evidence"]]
  missing_debrief = [record for record in command_records if not record["debrief_evidence"]]
  non_hold = [record for record in command_records if record["verb"] != "hold"]
  if not non_hold:
    status = "supported"
  elif unsupported or missing_debrief:
    status = "limited"
  else:
    status = "supported"

  return {
    "profile_name": run.get("profile_name", "unknown"),
    "seed": run.get("seed"),
    "completion_status": run.get("completion_status", "unknown"),
    "command_count": len(command_records),
    "non_hold_command_count": len(non_hold),
    "supported_command_count": sum(record["status"] == "supported" for record in command_records),
    "unsupported_commands": unsupported,
    "missing_debrief_commands": missing_debrief,
    "deferred_follow_through": deferred_records,
    "commands": command_records,
    "coverage_status": status,
  }


def build_audit(path=SOURCE_PATH):
  source = load_artifact(path)
  runs = [audit_run(run) for run in source.get("runs", [])]
  return {
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "campaign": source.get("campaign", CAMPAIGN),
    "source_artifact": str(Path(path).relative_to(ROOT)),
    "run_count": len(runs),
    "completed_run_count": sum(run["completion_status"] == "complete" for run in runs),
    "runs": runs,
    "limitations": LIMITATIONS,
  }


def validate_audit(audit):
  assert audit["batch_id"] == BATCH_ID
  assert audit["code_version"] == CODE_VERSION
  assert audit["campaign"] == CAMPAIGN
  assert audit["run_count"] == len(audit["runs"])
  for run in audit["runs"]:
    assert run["coverage_status"] in {"supported", "limited"}
    assert run["command_count"] == len(run["commands"])
    for command in run["commands"]:
      assert {"turn", "command", "verb", "transition_evidence", "debrief_evidence", "status", "reason"} <= set(command)


def render_markdown(audit):
  lines = [
    "# Command-to-Effect Explainability Audit v0.10.47",
    "",
    f"- **Batch id:** {audit['batch_id']}",
    f"- **Campaign:** `{audit['campaign']}`",
    f"- **Source artifact:** `{audit['source_artifact']}`",
    f"- **Runs reviewed:** {audit['completed_run_count']} of {audit['run_count']}",
    "",
    "This deterministic read-only audit checks whether submitted player commands",
    "are retained in the debrief and linked to action-specific transition evidence.",
    "It does not infer causality or decision quality.",
    "",
    "## Coverage",
    "",
    "| Profile | Seed | Completion | Commands | Supported | Unmatched | Missing debrief | Status |",
    "| --- | ---: | --- | ---: | ---: | ---: | ---: | --- |",
  ]
  for run in audit["runs"]:
    lines.append(
      f"| {run['profile_name']} | {run['seed']} | {run['completion_status']} | "
      f"{run['command_count']} | {run['supported_command_count']} | "
      f"{len(run['unsupported_commands'])} | {len(run['missing_debrief_commands'])} | "
      f"{run['coverage_status']} |"
    )
  lines.extend(["", "## Unmatched commands", ""])
  unmatched = [
    (run["profile_name"], run["seed"], command)
    for run in audit["runs"]
    for command in run["unsupported_commands"]
  ]
  if unmatched:
    lines.extend([
      "| Profile | Seed | Turn | Command | Reason |",
      "| --- | ---: | ---: | --- | --- |",
    ])
    lines.extend(
      f"| {profile} | {seed} | {command['turn']} | `{command['command']}` | {command['reason']} |"
      for profile, seed, command in unmatched
    )
  else:
    lines.append("No unmatched commands were found in the reviewed traces.")
  lines.extend(["", "## Missing debrief command records", ""])
  missing_debrief = [
    (run["profile_name"], run["seed"], command)
    for run in audit["runs"]
    for command in run["missing_debrief_commands"]
  ]
  if missing_debrief:
    lines.extend([
      "| Profile | Seed | Turn | Command |",
      "| --- | ---: | ---: | --- |",
    ])
    lines.extend(
      f"| {profile} | {seed} | {command['turn']} | `{command['command']}` |"
      for profile, seed, command in missing_debrief
    )
  else:
    lines.append("No missing monthly player command records were found.")
  lines.extend([
    "",
    "## Interpretation",
    "",
    "Supported means that the trace contains an action-specific event/effect and a monthly `Player:` debrief record.",
    "A deferred match records later trace continuity; it does not establish that the command caused the later outcome.",
    "",
    "## Evidence limits",
    "",
  ])
  lines.extend(f"- {limitation}" for limitation in audit["limitations"])
  lines.append("")
  return "\n".join(lines)


def main():
  output_dir = Path(__file__).resolve().parent
  audit = build_audit()
  validate_audit(audit)
  (output_dir / "results.json").write_text(
    json.dumps(audit, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )
  (output_dir / "audit.md").write_text(render_markdown(audit), encoding="utf-8")


if __name__ == "__main__":
  main()
