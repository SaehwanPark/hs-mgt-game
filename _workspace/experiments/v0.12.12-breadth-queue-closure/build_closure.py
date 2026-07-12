#!/usr/bin/env python3
"""Close the breadth queue item after auditing the existing bounded surface."""

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = Path(__file__).resolve().parent
ARTIFACT_TYPE = "simulation_breadth_queue_closure"
BATCH_ID = "v0.12.12-breadth-queue-closure"
CODE_VERSION = "0.12.12"
ALL_TIER_PATH = (
  "_workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/results.json"
)
CURRENT_CODE_PATH = (
  "_workspace/experiments/v0.11.12-phase7-current-code-teachability-capture/results.json"
)
TEACHABILITY_REVIEW_PATH = (
  "_workspace/experiments/v0.12.3-phase7-teachability-review/results.json"
)

SOURCE_MARKERS = {
  "src/model/competitive_command.rs": [
    "pub enum InvestDomain",
    "Emergency,",
    "Neurology,",
    "Asc,",
    "pub enum PayerId",
    "Medicaid,",
    "Medicare,",
    "pub enum ProjectKind",
    "ClinicNetwork,",
  ],
  "src/model/competitive_world.rs": [
    "pub struct HealthSystemState",
    "pub emergency_capacity",
    "pub monthly_unmet_demand",
    "pub struct CompetitiveWorldState",
    "pub effect_queue: Vec<PendingEffect>",
  ],
  "src/model/campaign.rs": [
    "pub struct PlayerObservation",
    "pub monthly_treated_volume",
    "pub monthly_unmet_demand",
    "pub market_bullets",
    "pub intel_gaps",
  ],
  "src/sim/observe_competitive.rs": [
    "pub fn observe_for_human",
    "Rival {} (observed, prior month): {}",
    "private activity last month (not publicly disclosed)",
  ],
  "src/debrief/report.rs": [
    "Attributed mechanisms to inspect:",
    "Rival actions and rationales that were unobserved during play",
    "Capital project lesson:",
    "Decision quality and outcome quality remain separate:",
  ],
  "docs/playtest-findings-v0.11.11.md": [
    "60/60 runs completed",
    "Ten distinct command trajectories",
    "No common first-month action",
    "Final tradeoff ranges remain varied",
  ],
  "docs/playtest-findings-v0.11.12.md": [
    "9/9 runs completed",
    "No structural matrix, history/hash, trace, or debrief gap",
  ],
}


def _source_markers():
  result = {}
  for relative_path, markers in SOURCE_MARKERS.items():
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    assert not missing, f"{relative_path} missing markers: {missing}"
    result[relative_path] = {"markers": markers, "status": "supported"}
  return result


def _all_tier_evidence():
  artifact = json.loads((ROOT / ALL_TIER_PATH).read_text(encoding="utf-8"))
  assert artifact["artifact_type"] == "post_change_all_tier_difficulty_validation"
  assert artifact["runtime_promotion"] == "deferred"
  runs = artifact["runs"]
  assert len(runs) == 60
  assert all(run["completion_status"] == "complete" for run in runs)
  trajectories = {
    tuple(line for line in run["debrief"] if line.startswith("Player: "))
    for run in runs
  }
  first_commands = Counter(
    next(line for line in run["debrief"] if line.startswith("Player: "))
    for run in runs
  )
  return {
    "path": ALL_TIER_PATH,
    "code_version": artifact["code_version"],
    "run_count": len(runs),
    "transition_count": sum(
      sum(line.startswith("Player: ") for line in run["debrief"])
      for run in runs
    ),
    "distinct_command_trajectories": len(trajectories),
    "first_command_counts": dict(sorted(first_commands.items())),
    "no_dominant_first_command": max(first_commands.values()) < len(runs) / 2,
    "runtime_promotion": artifact["runtime_promotion"],
  }


def _current_code_evidence():
  artifact = json.loads((ROOT / CURRENT_CODE_PATH).read_text(encoding="utf-8"))
  assert artifact["artifact_type"] == "current_code_teachability_capture"
  assert artifact["runtime_promotion"] == "deferred"
  runs = artifact["runs"]
  assert len(runs) == 9
  assert all(run["completion_status"] == "complete" for run in runs)
  return {
    "path": CURRENT_CODE_PATH,
    "code_version": artifact["code_version"],
    "run_count": len(runs),
    "transition_count": sum(len(run["commands"]) for run in runs),
    "runtime_promotion": artifact["runtime_promotion"],
  }


def _teachability_review():
  artifact = json.loads((ROOT / TEACHABILITY_REVIEW_PATH).read_text(encoding="utf-8"))
  assert artifact["finding"] == "no_structural_gap"
  assert artifact["runtime_promotion"] == "deferred"
  aggregate = artifact["aggregate"]
  assert aggregate == {
    "source_count": 2,
    "run_count": 18,
    "complete_run_count": 18,
    "transition_count": 270,
    "gap_count": 0,
    "gaps": [],
  }
  return {
    "path": TEACHABILITY_REVIEW_PATH,
    "code_version": artifact["code_version"],
    **aggregate,
    "finding": artifact["finding"],
    "runtime_promotion": artifact["runtime_promotion"],
  }


def build_closure():
  return {
    "artifact_type": ARTIFACT_TYPE,
    "batch_id": BATCH_ID,
    "code_version": CODE_VERSION,
    "closure_status": "complete_no_unexplained_breadth_gap",
    "breadth_inventory": [
      {
        "category": "service_line_and_capacity",
        "mechanisms": [
          "staffed beds",
          "outpatient",
          "emergency",
          "ICU",
          "obstetrics",
          "psychiatric",
          "cardiology",
          "oncology",
          "infusion",
          "neurology",
          "ASC",
        ],
        "actor": "human and AI health-system controllers",
        "observation": "own typed capacity, staffing, demand, treated volume, and unmet demand",
        "tradeoff": "cash/AP/project delay versus access, quality, and operating outcomes",
        "status": "supported_existing_boundary",
      },
      {
        "category": "operating_and_community_outcomes",
        "mechanisms": [
          "access",
          "quality",
          "workforce trust",
          "community trust",
          "market share",
          "operating margin",
          "treated volume",
          "unmet demand",
        ],
        "actor": "human health-system controller and affected modeled institutions",
        "observation": "reported own-system metrics and permitted market signals",
        "tradeoff": "organizational resources and legitimacy versus access, trust, and margin",
        "status": "supported_bounded_proxy",
      },
      {
        "category": "capital_and_market_interaction",
        "mechanisms": [
          "delayed projects",
          "payer posture",
          "public access commitments",
          "rival monitoring",
          "lagged public rival actions",
        ],
        "actor": "human system, AI rivals, and bounded payer command surface",
        "observation": "public, monitored, and private rival information paths",
        "tradeoff": "information/AP and cash timing versus direct action and competitive position",
        "status": "supported_existing_boundary",
      },
      {
        "category": "public_payer_interaction",
        "mechanisms": ["Medicaid negotiation", "Medicare negotiation"],
        "actor": "player payer-command interaction; not a full strategic public-payer actor",
        "observation": "bounded payer posture and resulting player-owned effects",
        "tradeoff": "compliance cost and posture constraints versus access and policy pressure",
        "status": "supported_bounded_effect",
      },
      {
        "category": "strategic_rivals_and_debrief",
        "mechanisms": [
          "style-weighted AI rivals",
          "public disclosure",
          "monitor-revealed actions",
          "private action markers",
          "post-run rationale review",
        ],
        "actor": "AI rival health-system controllers",
        "observation": "lagged/public/monitored signals; private actions withheld during play",
        "tradeoff": "monitoring cost and uncertainty versus defensive or growth action",
        "status": "supported_existing_boundary",
      },
    ],
    "actor_observation_boundary": {
      "true_state": [
        "all health systems",
        "queued effects",
        "market fields",
        "policy and event metadata",
        "private rival actions",
      ],
      "player_observation": [
        "human system reported metrics and typed capacity",
        "permitted market and policy signals",
        "lagged public rival actions",
        "monitor results",
        "explicit intelligence gaps",
      ],
      "private_during_play": [
        "unobserved rival private actions",
        "unobserved rival rationales",
      ],
      "debrief": [
        "committed events and effects",
        "attributed mechanisms",
        "post-run instructor rationale review",
      ],
    },
    "evidence": {
      "all_tier": _all_tier_evidence(),
      "current_code": _current_code_evidence(),
      "teachability_review": _teachability_review(),
    },
    "source_marker_contract": _source_markers(),
    "queue_action": "remove_item_from_future_queue",
    "runtime_change_authorized": False,
    "runtime_promotion": "deferred",
    "deferred_scope": [
      "full US health-system model",
      "individual patient simulation",
      "validated distributional outcome categories",
      "full Medicare payment reproduction",
      "full Medicaid eligibility rules",
      "national policy lifecycle modeling",
      "generalized strategic actor frameworks",
      "portfolio optimization",
      "broad scenario-authoring infrastructure",
    ],
    "next_action": (
      "Require new playtest, instructor, scenario, debrief, or domain-review "
      "evidence naming a concrete unexplained breadth or strategic-actor gap "
      "before reopening this track."
    ),
    "evidence_limits": [
      "The inventory describes bounded game abstractions, not calibrated clinical, financial, legal, or policy quantities.",
      "The evidence is deterministic simulated-policy trace evidence, not human learning, classroom effectiveness, or comprehension evidence.",
      "No individual patient, public-payer utility, social-welfare, equilibrium, or general winnability claim is made.",
      "The closure removes the current queue item but does not assert that broader modeling could never be useful.",
    ],
  }


def validate_closure(closure):
  assert closure["artifact_type"] == ARTIFACT_TYPE
  assert closure["batch_id"] == BATCH_ID
  assert closure["code_version"] == CODE_VERSION
  assert closure["closure_status"] == "complete_no_unexplained_breadth_gap"
  assert len(closure["breadth_inventory"]) == 5
  assert closure["queue_action"] == "remove_item_from_future_queue"
  assert closure["runtime_change_authorized"] is False
  assert closure["runtime_promotion"] == "deferred"
  all_tier = closure["evidence"]["all_tier"]
  assert all_tier["run_count"] == 60
  assert all_tier["transition_count"] == 1440
  assert all_tier["distinct_command_trajectories"] == 10
  assert all_tier["no_dominant_first_command"] is True
  current = closure["evidence"]["current_code"]
  assert current["run_count"] == 9
  assert current["transition_count"] == 216
  review = closure["evidence"]["teachability_review"]
  assert review["complete_run_count"] == 18
  assert review["transition_count"] == 270
  assert review["gap_count"] == 0
  assert all(
    value["status"] == "supported"
    for value in closure["source_marker_contract"].values()
  )


def render_diagnostics(closure):
  evidence = closure["evidence"]
  all_tier = evidence["all_tier"]
  current = evidence["current_code"]
  review = evidence["teachability_review"]
  lines = [
    "# Simulation Breadth and Strategic Actors Queue Closure — v0.12.12",
    "",
    "- **Closure status:** complete; no unexplained breadth gap",
    "- **New runtime change authorized:** no",
    "- **Runtime promotion:** deferred",
    "",
    "The existing competitive campaign already contains bounded capacity and",
    "service-line choices, operating and community proxies, delayed capital,",
    "payer interactions, rival information boundaries, and debrief attribution.",
    "The evidence does not authorize a new actor, patient, or outcome model.",
    "",
    "## Evidence",
    "",
    f"- All-tier source: {all_tier['run_count']} complete runs and {all_tier['transition_count']} transitions.",
    f"- Distinct command trajectories: {all_tier['distinct_command_trajectories']}; no dominant first command: {all_tier['no_dominant_first_command']}.",
    f"- Current-code source: {current['run_count']} complete runs and {current['transition_count']} transitions.",
    f"- Cross-campaign review: {review['complete_run_count']}/{review['run_count']} complete runs, {review['transition_count']} transitions, {review['gap_count']} structural gaps.",
    "- Source-marker audit: supported.",
    "",
    "## Queue decision",
    "",
    "Remove the breadth and strategic-actors item from the Future queue. Keep",
    "broader modeling deferred and require a new concrete unexplained gap before",
    "reopening the track.",
    "",
    "## Evidence limits",
    "",
  ]
  lines.extend(f"- {limit}" for limit in closure["evidence_limits"])
  lines.append("")
  return "\n".join(lines)


def main():
  closure = build_closure()
  validate_closure(closure)
  (OUTPUT_DIR / "closure.json").write_text(
    json.dumps(closure, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )
  (OUTPUT_DIR / "diagnostics.md").write_text(
    render_diagnostics(closure),
    encoding="utf-8",
  )
  print(f"Wrote closure artifact to {OUTPUT_DIR / 'closure.json'}")


if __name__ == "__main__":
  main()
