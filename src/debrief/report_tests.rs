use crate::competitive::build_multi_month_resolution_history;
use crate::debrief::{
  competitive_debrief, competitive_instructor_summary, educational_debrief, instructor_run_summary,
};
use crate::model::Difficulty;
use crate::test_support::demo_history;

#[test]
fn debrief_includes_actor_rationales() {
  let history = demo_history();
  let debrief = educational_debrief(&history).join("\n");

  assert!(debrief.contains("commercial_insurer:"));
  assert!(debrief.contains("state_policy_officials:"));
  assert!(debrief.contains("nursing_workforce:"));
  assert!(debrief.contains("regional_provider_coalition:"));
  assert!(debrief.contains("competitor_health_system:"));
  assert!(debrief.contains("Reported access"));
  assert!(debrief.contains("Access commitment"));
  assert!(debrief.contains("coalition investment choice"));
}

#[test]
fn debrief_includes_attributed_tradeoff() {
  let history = demo_history();
  let debrief = educational_debrief(&history).join("\n");

  assert!(debrief.contains("cash moved from 100 to 32"));
  assert!(debrief.contains("access from 70 to 89"));
  assert!(debrief.contains("capacity investment changed cash by -18"));
  assert!(debrief.contains("state policy response changed community_trust by 2"));
  assert!(debrief.contains("workforce response changed cash by"));
  assert!(debrief.contains("coalition response changed cash by"));
  assert!(debrief.contains("competitor response changed cash by"));
}

#[test]
fn identical_histories_produce_identical_debriefs() {
  let first = demo_history();
  let second = demo_history();

  assert_eq!(educational_debrief(&first), educational_debrief(&second));
}

#[test]
fn debrief_notes_observation_revisions_without_rewriting_history() {
  let history = demo_history();
  let debrief = educational_debrief(&history).join("\n");

  assert!(debrief.contains("Observation revision note:"));
  assert!(debrief.contains("Prior committed observations remain unchanged"));
  assert_eq!(history.transitions[0].observation.prior_access_revision, 0);
}

#[test]
fn test_instructor_run_summary_stabilization() {
  let history = demo_history();
  let summary = instructor_run_summary(&history);
  let summary_str = summary.join("\n");

  assert!(summary_str.contains("=== INSTRUCTOR RUN SUMMARY & DECISION QUALITY REVIEW ==="));
  assert!(summary_str.contains("Observed ="));
  assert!(summary_str.contains("True Prior ="));
  assert!(summary_str.contains("Turn 1 (Turn 0 → 1)"));
}

#[test]
fn test_competitive_instructor_summary_and_debrief() {
  let history = build_multi_month_resolution_history(Difficulty::Normal, 42, 3)
    .expect("should build competitive history");

  let summary = competitive_instructor_summary(&history);
  let summary_str = summary.join("\n");

  assert!(summary_str.contains("=== INSTRUCTOR RUN SUMMARY & DECISION QUALITY REVIEW ==="));
  assert!(summary_str.contains("Month 1:"));
  assert!(summary_str.contains("Rival"));
  assert!(summary_str.contains("unobserved during play - REVEALED FOR INSTRUCTOR REVIEW"));

  let debrief = competitive_debrief(&history);
  let debrief_str = debrief.join("\n");
  assert!(debrief_str.contains("=== INSTRUCTOR RUN SUMMARY & DECISION QUALITY REVIEW ==="));
  assert!(debrief_str.contains("Competitive preview completed 3 committed month(s)"));
}

#[test]
fn test_competitive_decision_quality_warnings() {
  let history = build_multi_month_resolution_history(Difficulty::Normal, 42, 1)
    .expect("should build competitive history");

  // By default, the run should pass all checks
  let summary_pass = competitive_instructor_summary(&history);
  let summary_pass_str = summary_pass.join("\n");
  assert!(summary_pass_str.contains("All strategic checks passed."));

  // 1. Cash runway warning
  {
    let mut runway_history = history.clone();
    if let Some(mut human_next) = runway_history.transitions[0].next.human_system().cloned() {
      human_next.resources.cash = 15;
      human_next.resources.active_project_monthly_draws = 5;
      if let Some(pos) = runway_history.transitions[0]
        .next
        .systems
        .iter()
        .position(|s| s.system_id == human_next.system_id)
      {
        runway_history.transitions[0].next.systems[pos] = human_next;
      }
    }
    let summary = competitive_instructor_summary(&runway_history);
    let summary_str = summary.join("\n");
    assert!(summary_str.contains(
      "Warning: Cash runway fell to 15 in Month 1 while carrying active project monthly draws of 5"
    ));
  }

  // 2. Workforce trust warning
  {
    let mut workforce_history = history.clone();
    let human_system_id = workforce_history.genesis.human_system().unwrap().system_id;
    if let Some(batch) = workforce_history.transitions[0]
      .aggregated
      .batch_for_system(human_system_id)
    {
      let mut updated_batch = batch.clone();
      updated_batch
        .commands
        .push(crate::model::CompetitiveCommand::Recruit {
          role: crate::model::RecruitRole::Nurse,
          headcount: 5,
        });
      let pos = workforce_history.transitions[0]
        .aggregated
        .batches
        .iter()
        .position(|b| b.system_id == human_system_id)
        .unwrap();
      workforce_history.transitions[0].aggregated.batches[pos] = updated_batch;
    }
    if let Some(mut human_next) = workforce_history.transitions[0]
      .next
      .human_system()
      .cloned()
    {
      human_next.workforce_trust = 50;
      if let Some(pos) = workforce_history.transitions[0]
        .next
        .systems
        .iter()
        .position(|s| s.system_id == human_next.system_id)
      {
        workforce_history.transitions[0].next.systems[pos] = human_next;
      }
    }
    let summary = competitive_instructor_summary(&workforce_history);
    let summary_str = summary.join("\n");
    assert!(
      summary_str
        .contains("Warning: Workforce trust dropped to 50 in Month 1 due to recruitment stress")
    );
  }

  // 3. Payer negotiation warning
  {
    let mut negotiation_history = history.clone();
    let human_system_id = negotiation_history
      .genesis
      .human_system()
      .unwrap()
      .system_id;
    if let Some(batch) = negotiation_history.transitions[0]
      .aggregated
      .batch_for_system(human_system_id)
    {
      let mut updated_batch = batch.clone();
      updated_batch
        .commands
        .push(crate::model::CompetitiveCommand::Negotiate {
          payer: crate::model::PayerId::CarrierA,
          rate_posture: crate::model::RatePosture::Aggressive,
        });
      let pos = negotiation_history.transitions[0]
        .aggregated
        .batches
        .iter()
        .position(|b| b.system_id == human_system_id)
        .unwrap();
      negotiation_history.transitions[0].aggregated.batches[pos] = updated_batch;
    }
    if let Some(mut human_prior) = negotiation_history.transitions[0]
      .prior
      .human_system()
      .cloned()
    {
      human_prior.quality_index = 50;
      human_prior.market_share_index = 10;
      if let Some(pos) = negotiation_history.transitions[0]
        .prior
        .systems
        .iter()
        .position(|s| s.system_id == human_prior.system_id)
      {
        negotiation_history.transitions[0].prior.systems[pos] = human_prior;
      }
    }
    let summary = competitive_instructor_summary(&negotiation_history);
    let summary_str = summary.join("\n");
    assert!(summary_str.contains("Warning: Attempted aggressive payer negotiation in Month 1 with low leverage (Market Share = 10%, Quality = 50)"));
  }

  // 4. Rival Bed Capacity response warning
  {
    let mut capacity_history = history.clone();
    let human_system_id = capacity_history.genesis.human_system().unwrap().system_id;
    let rival_id = capacity_history.transitions[0]
      .prior
      .systems
      .iter()
      .find(|s| s.system_id != human_system_id)
      .unwrap()
      .system_id;

    if let Some(mut rival_prior) = capacity_history.transitions[0]
      .prior
      .systems
      .iter()
      .find(|s| s.system_id == rival_id)
      .cloned()
    {
      rival_prior.staffed_beds = 100;
      if let Some(pos) = capacity_history.transitions[0]
        .prior
        .systems
        .iter()
        .position(|s| s.system_id == rival_id)
      {
        capacity_history.transitions[0].prior.systems[pos] = rival_prior;
      }
    }
    if let Some(mut rival_next) = capacity_history.transitions[0]
      .next
      .systems
      .iter()
      .find(|s| s.system_id == rival_id)
      .cloned()
    {
      rival_next.staffed_beds = 115;
      if let Some(pos) = capacity_history.transitions[0]
        .next
        .systems
        .iter()
        .position(|s| s.system_id == rival_id)
      {
        capacity_history.transitions[0].next.systems[pos] = rival_next;
      }
    }

    if let Some(mut human_prior) = capacity_history.transitions[0]
      .prior
      .human_system()
      .cloned()
    {
      human_prior.market_share_index = 30;
      if let Some(pos) = capacity_history.transitions[0]
        .prior
        .systems
        .iter()
        .position(|s| s.system_id == human_system_id)
      {
        capacity_history.transitions[0].prior.systems[pos] = human_prior;
      }
    }
    if let Some(mut human_next) = capacity_history.transitions[0].next.human_system().cloned() {
      human_next.market_share_index = 25;
      if let Some(pos) = capacity_history.transitions[0]
        .next
        .systems
        .iter()
        .position(|s| s.system_id == human_system_id)
      {
        capacity_history.transitions[0].next.systems[pos] = human_next;
      }
    }

    if let Some(batch) = capacity_history.transitions[0]
      .aggregated
      .batch_for_system(human_system_id)
    {
      let mut updated_batch = batch.clone();
      updated_batch.commands.retain(|cmd| {
        !matches!(
          cmd,
          crate::model::CompetitiveCommand::Invest { .. }
            | crate::model::CompetitiveCommand::Project { .. }
        )
      });
      let pos = capacity_history.transitions[0]
        .aggregated
        .batches
        .iter()
        .position(|b| b.system_id == human_system_id)
        .unwrap();
      capacity_history.transitions[0].aggregated.batches[pos] = updated_batch;
    }

    let summary = competitive_instructor_summary(&capacity_history);
    let summary_str = summary.join("\n");
    assert!(summary_str.contains("Warning: Rival capacity expansion by"));
  }
}
