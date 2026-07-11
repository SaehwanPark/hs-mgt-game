import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BATCH_ID = "v0.10.45-instructor-debrief-use-audit"
CODE_VERSION = "0.10.45"
CAMPAIGN = "competitive-regional-v1"
SOURCE_PATHS = [
  ROOT / "_workspace/experiments/v0.10.37-rival-info-monitor-evidence/results.json",
  ROOT / "_workspace/experiments/v0.10.40-consultant-advice-evidence/results.json",
  ROOT / "_workspace/experiments/v0.10.41-consultant-advice-usage/results.json",
  ROOT / "_workspace/experiments/v0.10.43-rival-info-follow-through/results.json",
]

REVIEW_STEPS = (
  ("visibility", "Actor-visible observations, advice, or monitor signals"),
  ("response", "Submitted commands, selections, ignores, or fallbacks"),
  ("follow-through", "Operational action traces that can be compared later"),
  ("outcome", "Transition counts, state hashes, and final-run results"),
  ("explanation", "History or debrief material for retrospective explanation"),
)

LIMITATIONS = [
  "Coverage is traceability evidence, not causal evidence.",
  "The policies are deterministic simulated policies, not human or classroom sessions.",
  "The audit does not measure advice quality, monitor value, learning, balance, or calibration.",
  "A supported field does not establish that an instructor or learner will find it clear.",
]


def load_artifact(path):
  return json.loads(path.read_text(encoding="utf-8"))


def _turn_entries(run):
  entries = []
  for key in ("turn_trace", "trace"):
    value = run.get(key, [])
    if isinstance(value, list):
      entries.extend(entry for entry in value if isinstance(entry, dict))
  return entries


def _has_any_value(run, keys):
  if any(run.get(key) for key in keys):
    return True
  return any(entry.get(key) for entry in _turn_entries(run) for key in keys)


def _step_evidence(run, step_name):
  if step_name == "visibility":
    return _has_any_value(
      run,
      ("observation", "rendered_options", "options", "rival_information_examples"),
    )
  if step_name == "response":
    return _has_any_value(
      run,
      ("commands", "response_records", "selected_option_label", "command"),
    )
  if step_name == "follow-through":
    return _has_any_value(run, ("commands", "response_records", "command"))
  if step_name == "outcome":
    return bool(
      run.get("final_hash")
      and run.get("state_hashes")
      and run.get("transition_count") is not None
    )
  if step_name == "explanation":
    return _has_any_value(run, ("debrief", "debrief_option_lines"))
  raise ValueError(f"unknown review step: {step_name}")


def _status(covered, total):
  if covered == total and total > 0:
    return "supported"
  if covered > 0:
    return "limited"
  return "unsupported"


def audit_artifact(artifact, source_path=None):
  runs = artifact.get("runs", [])
  complete_runs = [
    run
    for run in runs
    if isinstance(run, dict) and run.get("completion_status") == "complete"
  ]
  review_steps = []
  for name, description in REVIEW_STEPS:
    covered = sum(_step_evidence(run, name) for run in complete_runs)
    review_steps.append(
      {
        "name": name,
        "description": description,
        "covered_runs": covered,
        "eligible_runs": len(complete_runs),
        "status": _status(covered, len(complete_runs)),
      }
    )
  return {
    "source_artifact": source_path or artifact.get("batch_id", "unknown"),
    "batch_id": artifact.get("batch_id", "unknown"),
    "code_version": artifact.get("code_version", "unknown"),
    "campaign": artifact.get("campaign", CAMPAIGN),
    "run_count": len(runs),
    "completed_run_count": len(complete_runs),
    "review_steps": review_steps,
  }


def build_audit(paths=SOURCE_PATHS):
  sorted_paths = sorted(Path(path) for path in paths)
  artifacts = [
    audit_artifact(load_artifact(path), str(path.relative_to(ROOT)))
    for path in sorted_paths
  ]
  return {
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "campaign": CAMPAIGN,
    "source_artifacts": [artifact["source_artifact"] for artifact in artifacts],
    "source_count": len(artifacts),
    "run_count": sum(artifact["run_count"] for artifact in artifacts),
    "completed_run_count": sum(
      artifact["completed_run_count"] for artifact in artifacts
    ),
    "artifacts": artifacts,
    "limitations": LIMITATIONS,
  }


def render_markdown(audit):
  lines = [
    "# Instructor Debrief-Use Audit v0.10.45",
    "",
    f"- **Batch id:** {audit['batch_id']}",
    f"- **Campaign:** `{audit['campaign']}`",
    f"- **Source artifacts:** {audit['source_count']}",
    f"- **Runs reviewed:** {audit['completed_run_count']} of {audit['run_count']}",
    "",
    "This is a deterministic read-only audit of existing evidence artifacts. "
    "It evaluates whether trace fields are present for review; it does not "
    "claim that the fields are clear to human instructors or learners.",
    "",
    "## Coverage",
    "",
    "| Source artifact | Visibility | Response | Follow-through | Outcome | Explanation |",
    "| --- | --- | --- | --- | --- | --- |",
  ]
  for artifact in audit["artifacts"]:
    statuses = {step["name"]: step["status"] for step in artifact["review_steps"]}
    lines.append(
      "| `{source}` | {visibility} | {response} | {follow} | {outcome} | {explanation} |".format(
        source=artifact["batch_id"],
        visibility=statuses["visibility"],
        response=statuses["response"],
        follow=statuses["follow-through"],
        outcome=statuses["outcome"],
        explanation=statuses["explanation"],
      )
    )
  lines.extend(
    [
      "",
      "## Interpretation",
      "",
      "All four source artifacts expose at least one complete trace for each "
      "review step. This supports inspectability of information-to-action "
      "records, not a claim that the records are pedagogically sufficient.",
      "",
      "The audit does not identify a concrete runtime, information, debrief, "
      "difficulty, balance, or scoring defect. Keep runtime promotion deferred "
      "until reviewer or instructor evidence identifies a gap that these "
      "artifacts cannot explain.",
      "",
      "## Evidence limits",
      "",
    ]
  )
  lines.extend(f"- {limitation}" for limitation in audit["limitations"])
  lines.append("")
  return "\n".join(lines)


def main():
  output_dir = Path(__file__).resolve().parent
  audit = build_audit()
  (output_dir / "results.json").write_text(
    json.dumps(audit, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )
  (output_dir / "audit.md").write_text(render_markdown(audit), encoding="utf-8")


if __name__ == "__main__":
  main()
