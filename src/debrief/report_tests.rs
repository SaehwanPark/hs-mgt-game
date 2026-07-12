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
  assert!(debrief_str.contains("Consultant options shown"));
  assert!(
    !debrief_str
      .to_lowercase()
      .contains("consultant option is correct")
  );
}

#[test]
fn competitive_debrief_includes_player_owned_monthly_operating_results() {
  let mut history = build_multi_month_resolution_history(Difficulty::Normal, 42, 3)
    .expect("should build competitive history");
  let human_system_id = history.genesis.human_system().unwrap().system_id;

  for (month_index, transition) in history.transitions.iter_mut().enumerate() {
    let human = transition
      .next
      .systems
      .iter_mut()
      .find(|system| system.system_id == human_system_id)
      .expect("human system should remain in the committed next state");
    human.monthly_demand = 30 + month_index as i32;
    human.monthly_treated_volume = 20 + month_index as i32;
    human.monthly_unmet_demand = 10;
    human.monthly_operating_revenue = 40 + month_index as i32;
    human.monthly_operating_cost = 45 + month_index as i32;
    human.monthly_operating_margin = -5;

    let rival = transition
      .next
      .systems
      .iter_mut()
      .find(|system| system.system_id != human_system_id)
      .expect("a normal campaign should include a rival");
    rival.monthly_demand = 99;
    rival.monthly_treated_volume = 99;
    rival.monthly_unmet_demand = 0;
    rival.monthly_operating_revenue = 999;
    rival.monthly_operating_cost = 1;
    rival.monthly_operating_margin = 998;
  }

  let debrief = competitive_debrief(&history).join("\n");

  assert_eq!(debrief.matches("Operating result:").count(), 3);
  assert!(debrief.contains(
    "Operating result: treated 20/30 demand units (10 unmet); operating revenue 40, operating cost 45, operating margin -5."
  ));
  assert!(debrief.contains(
    "Operating result: treated 21/31 demand units (10 unmet); operating revenue 41, operating cost 46, operating margin -5."
  ));
  assert!(debrief.contains(
    "Operating result: treated 22/32 demand units (10 unmet); operating revenue 42, operating cost 47, operating margin -5."
  ));
  assert!(!debrief.contains("treated 99/99 demand units"));
  assert!(!debrief.contains("operating revenue 999"));
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

#[test]
fn test_competitive_debrief_rationale_visibility() {
  let history = build_multi_month_resolution_history(Difficulty::Normal, 42, 1)
    .expect("should build competitive history");

  let human_system_id = history.genesis.human_system().unwrap().system_id;
  let rival_system = history
    .genesis
    .systems
    .iter()
    .find(|s| s.system_id != human_system_id)
    .unwrap();
  let rival_id = rival_system.system_id;

  // 1. Private action only, not monitored -> Rationale should be unobserved by student,
  //    revealed for instructor.
  {
    let mut private_unmonitored_history = history.clone();

    // Set human commands to Hold (not monitoring anyone)
    if let Some(pos) = private_unmonitored_history.transitions[0]
      .aggregated
      .batches
      .iter()
      .position(|b| b.system_id == human_system_id)
    {
      private_unmonitored_history.transitions[0]
        .aggregated
        .batches[pos]
        .commands = vec![crate::model::CompetitiveCommand::Hold];
    }

    // Set rival commands to Hold (private action) and add a rationale
    if let Some(pos) = private_unmonitored_history.transitions[0]
      .aggregated
      .batches
      .iter()
      .position(|b| b.system_id == rival_id)
    {
      private_unmonitored_history.transitions[0]
        .aggregated
        .batches[pos]
        .commands = vec![crate::model::CompetitiveCommand::Hold];
      private_unmonitored_history.transitions[0]
        .aggregated
        .batches[pos]
        .rationale = Some("Rival private rationale test".to_string());
    }

    let debrief_str = competitive_debrief(&private_unmonitored_history).join("\n");
    let summary_str = competitive_instructor_summary(&private_unmonitored_history).join("\n");

    // Student should NOT see the rationale or private actions
    let parts: Vec<&str> = debrief_str
      .split("=== INSTRUCTOR RUN SUMMARY & DECISION QUALITY REVIEW ===")
      .collect();
    let student_debrief = parts[0];
    assert!(!student_debrief.contains("Rival private rationale test"));
    assert!(student_debrief.contains("[Private Action] (unobserved by you)"));

    // Instructor should see it as unobserved during play
    assert!(summary_str.contains(
      "Rival private rationale test (unobserved during play - REVEALED FOR INSTRUCTOR REVIEW)"
    ));
  }

  // 2. Private action only, but monitored -> Rationale should be observed via monitor
  {
    let mut private_monitored_history = history.clone();

    // Find the MonitorTarget corresponding to the rival system
    let rival_name = rival_system.name.to_lowercase();
    let target = if rival_name.contains("northlake") {
      crate::model::MonitorTarget::Northlake
    } else if rival_name.contains("summit") {
      crate::model::MonitorTarget::Summit
    } else if rival_name.contains("valley") {
      crate::model::MonitorTarget::Valley
    } else {
      crate::model::MonitorTarget::Metro
    };

    // Set human commands to Monitor target
    if let Some(pos) = private_monitored_history.transitions[0]
      .aggregated
      .batches
      .iter()
      .position(|b| b.system_id == human_system_id)
    {
      private_monitored_history.transitions[0].aggregated.batches[pos].commands =
        vec![crate::model::CompetitiveCommand::Monitor { target, depth: 1 }];
    }

    // Set rival commands to Hold (private action) and add a rationale
    if let Some(pos) = private_monitored_history.transitions[0]
      .aggregated
      .batches
      .iter()
      .position(|b| b.system_id == rival_id)
    {
      private_monitored_history.transitions[0].aggregated.batches[pos].commands =
        vec![crate::model::CompetitiveCommand::Hold];
      private_monitored_history.transitions[0].aggregated.batches[pos].rationale =
        Some("Rival monitored rationale test".to_string());
    }

    let debrief_str = competitive_debrief(&private_monitored_history).join("\n");
    let summary_str = competitive_instructor_summary(&private_monitored_history).join("\n");

    // Student should see the rationale observed via monitor
    let parts: Vec<&str> = debrief_str
      .split("=== INSTRUCTOR RUN SUMMARY & DECISION QUALITY REVIEW ===")
      .collect();
    let student_debrief = parts[0];
    assert!(student_debrief.contains("Rival monitored rationale test (observed via monitor)"));

    // Instructor should see it observed via monitor
    assert!(summary_str.contains("Rival monitored rationale test (observed via monitor)"));
  }

  // 3. Public action present, not monitored -> Rationale should be observed via public disclosure
  {
    let mut public_history = history.clone();

    // Set human commands to Hold
    if let Some(pos) = public_history.transitions[0]
      .aggregated
      .batches
      .iter()
      .position(|b| b.system_id == human_system_id)
    {
      public_history.transitions[0].aggregated.batches[pos].commands =
        vec![crate::model::CompetitiveCommand::Hold];
    }

    // Set rival commands to Recruit (public action) and add a rationale
    if let Some(pos) = public_history.transitions[0]
      .aggregated
      .batches
      .iter()
      .position(|b| b.system_id == rival_id)
    {
      public_history.transitions[0].aggregated.batches[pos].commands =
        vec![crate::model::CompetitiveCommand::Recruit {
          role: crate::model::RecruitRole::Nurse,
          headcount: 1,
        }];
      public_history.transitions[0].aggregated.batches[pos].rationale =
        Some("Rival public rationale test".to_string());
    }

    let debrief_str = competitive_debrief(&public_history).join("\n");
    let summary_str = competitive_instructor_summary(&public_history).join("\n");

    // Student should see the rationale observed via public disclosure
    let parts: Vec<&str> = debrief_str
      .split("=== INSTRUCTOR RUN SUMMARY & DECISION QUALITY REVIEW ===")
      .collect();
    let student_debrief = parts[0];
    assert!(
      student_debrief.contains("Rival public rationale test (observed via public disclosure)")
    );

    // Instructor should see it observed via public disclosure
    assert!(summary_str.contains("Rival public rationale test (observed via public disclosure)"));
  }
}

#[test]
fn competitive_debrief_warns_on_repeated_access_pledges_without_follow_through() {
  let mut history = build_multi_month_resolution_history(Difficulty::Normal, 42, 3)
    .expect("should build competitive history");
  let human_system_id = history.genesis.human_system().unwrap().system_id;

  set_human_commands(
    &mut history,
    human_system_id,
    0,
    vec![crate::model::CompetitiveCommand::Commit {
      pledge_type: crate::model::PledgeType::Access,
      level: 3,
    }],
  );
  set_human_commands(
    &mut history,
    human_system_id,
    1,
    vec![crate::model::CompetitiveCommand::Commit {
      pledge_type: crate::model::PledgeType::Access,
      level: 2,
    }],
  );
  set_human_commands(
    &mut history,
    human_system_id,
    2,
    vec![crate::model::CompetitiveCommand::Hold],
  );

  let summary = competitive_instructor_summary(&history).join("\n");

  assert!(summary.contains("Repeated public access pledges in Months 1, 2"));
  assert!(summary.contains("not substitutes for durable operational action"));
}

#[test]
fn competitive_debrief_accepts_access_pledges_with_follow_through() {
  let mut history = build_multi_month_resolution_history(Difficulty::Normal, 42, 3)
    .expect("should build competitive history");
  let human_system_id = history.genesis.human_system().unwrap().system_id;

  set_human_commands(
    &mut history,
    human_system_id,
    0,
    vec![crate::model::CompetitiveCommand::Commit {
      pledge_type: crate::model::PledgeType::Access,
      level: 3,
    }],
  );
  set_human_commands(
    &mut history,
    human_system_id,
    1,
    vec![
      crate::model::CompetitiveCommand::Commit {
        pledge_type: crate::model::PledgeType::Access,
        level: 2,
      },
      crate::model::CompetitiveCommand::Recruit {
        role: crate::model::RecruitRole::Nurse,
        headcount: 1,
      },
    ],
  );

  let summary = competitive_instructor_summary(&history).join("\n");

  assert!(!summary.contains("Repeated public access pledges"));
}

#[test]
fn competitive_debrief_includes_access_pledge_lesson() {
  let history = build_multi_month_resolution_history(Difficulty::Normal, 42, 1)
    .expect("should build competitive history");

  let debrief = competitive_debrief(&history).join("\n");

  assert!(debrief.contains("Access pledge lesson:"));
  assert!(debrief.contains("capacity, staffing, monitoring, or payer follow-through"));
}

#[test]
fn competitive_debrief_notes_low_cash_access_pledges_without_follow_through() {
  let mut history = build_multi_month_resolution_history(Difficulty::Normal, 42, 3)
    .expect("should build competitive history");
  let human_system_id = history.genesis.human_system().unwrap().system_id;

  set_human_commands(
    &mut history,
    human_system_id,
    0,
    vec![crate::model::CompetitiveCommand::Commit {
      pledge_type: crate::model::PledgeType::Access,
      level: 3,
    }],
  );
  set_human_commands(
    &mut history,
    human_system_id,
    1,
    vec![crate::model::CompetitiveCommand::Commit {
      pledge_type: crate::model::PledgeType::Access,
      level: 2,
    }],
  );
  set_final_human_cash(&mut history, human_system_id, 10);

  let debrief = competitive_debrief(&history).join("\n");

  assert!(debrief.contains("Access follow-through note:"));
  assert!(debrief.contains("2 public access pledge(s), 0 durable follow-through action(s)"));
  assert!(!debrief.contains("Access follow-through note: Warning:"));
}

#[test]
fn competitive_debrief_skips_access_follow_through_note_when_follow_through_matches_pledges() {
  let mut history = build_multi_month_resolution_history(Difficulty::Normal, 42, 3)
    .expect("should build competitive history");
  let human_system_id = history.genesis.human_system().unwrap().system_id;

  set_human_commands(
    &mut history,
    human_system_id,
    0,
    vec![
      crate::model::CompetitiveCommand::Commit {
        pledge_type: crate::model::PledgeType::Access,
        level: 3,
      },
      crate::model::CompetitiveCommand::Recruit {
        role: crate::model::RecruitRole::Nurse,
        headcount: 1,
      },
    ],
  );
  set_human_commands(
    &mut history,
    human_system_id,
    1,
    vec![
      crate::model::CompetitiveCommand::Commit {
        pledge_type: crate::model::PledgeType::Access,
        level: 2,
      },
      crate::model::CompetitiveCommand::Monitor {
        target: crate::model::MonitorTarget::Northlake,
        depth: 1,
      },
    ],
  );
  set_final_human_cash(&mut history, human_system_id, 10);

  let debrief = competitive_debrief(&history).join("\n");

  assert!(!debrief.contains("Access follow-through note:"));
}

#[test]
fn competitive_debrief_counts_follow_through_actions_not_months() {
  let mut history = build_multi_month_resolution_history(Difficulty::Normal, 42, 3)
    .expect("should build competitive history");
  let human_system_id = history.genesis.human_system().unwrap().system_id;

  set_human_commands(
    &mut history,
    human_system_id,
    0,
    vec![crate::model::CompetitiveCommand::Commit {
      pledge_type: crate::model::PledgeType::Access,
      level: 3,
    }],
  );
  set_human_commands(
    &mut history,
    human_system_id,
    1,
    vec![
      crate::model::CompetitiveCommand::Commit {
        pledge_type: crate::model::PledgeType::Access,
        level: 2,
      },
      crate::model::CompetitiveCommand::Recruit {
        role: crate::model::RecruitRole::Nurse,
        headcount: 1,
      },
      crate::model::CompetitiveCommand::Monitor {
        target: crate::model::MonitorTarget::Northlake,
        depth: 1,
      },
    ],
  );
  set_final_human_cash(&mut history, human_system_id, 10);

  let debrief = competitive_debrief(&history).join("\n");

  assert!(!debrief.contains("Access follow-through note:"));
}

#[test]
fn competitive_debrief_skips_access_follow_through_note_when_cash_is_adequate() {
  let mut history = build_multi_month_resolution_history(Difficulty::Normal, 42, 3)
    .expect("should build competitive history");
  let human_system_id = history.genesis.human_system().unwrap().system_id;

  set_human_commands(
    &mut history,
    human_system_id,
    0,
    vec![crate::model::CompetitiveCommand::Commit {
      pledge_type: crate::model::PledgeType::Access,
      level: 3,
    }],
  );
  set_human_commands(
    &mut history,
    human_system_id,
    1,
    vec![crate::model::CompetitiveCommand::Commit {
      pledge_type: crate::model::PledgeType::Access,
      level: 2,
    }],
  );
  set_final_human_cash(&mut history, human_system_id, 20);

  let debrief = competitive_debrief(&history).join("\n");

  assert!(!debrief.contains("Access follow-through note:"));
}

fn set_human_commands(
  history: &mut crate::model::CompetitiveHistory,
  human_system_id: u32,
  transition_idx: usize,
  commands: Vec<crate::model::CompetitiveCommand>,
) {
  let pos = history.transitions[transition_idx]
    .aggregated
    .batches
    .iter()
    .position(|batch| batch.system_id == human_system_id)
    .expect("human batch");
  history.transitions[transition_idx].aggregated.batches[pos].commands = commands;
}

fn set_final_human_cash(
  history: &mut crate::model::CompetitiveHistory,
  human_system_id: u32,
  cash: i32,
) {
  let final_transition = history.transitions.last_mut().expect("final transition");
  let pos = final_transition
    .next
    .systems
    .iter()
    .position(|system| system.system_id == human_system_id)
    .expect("human final system");
  final_transition.next.systems[pos].resources.cash = cash;
}
