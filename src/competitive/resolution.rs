use crate::model::{
  CompetitiveCommand, CompetitiveRuleset, CompetitiveTransition, CompetitiveWorldState, Difficulty,
  InvestDomain, MonitorTarget, PayerId, PlayerController, PledgeType, ProjectKind, RatePosture,
  RecruitRole, SystemMonthlyBatch,
};
use crate::sim::{ai_profile_for_system, observe_for_ai};

#[allow(dead_code)]
pub const DEFAULT_COMPETITIVE_SEED: u64 = 42;

pub fn month1_human_preset_batch() -> SystemMonthlyBatch {
  SystemMonthlyBatch {
    system_id: 0,
    commands: vec![
      CompetitiveCommand::Hold,
      CompetitiveCommand::Monitor {
        target: MonitorTarget::Northlake,
        depth: 1,
      },
    ],
    rationale: None,
  }
}

pub fn month1_preset_batches(difficulty: Difficulty) -> Vec<SystemMonthlyBatch> {
  let mut batches = vec![
    SystemMonthlyBatch {
      system_id: 0,
      commands: vec![
        CompetitiveCommand::Hold,
        CompetitiveCommand::Monitor {
          target: MonitorTarget::Northlake,
          depth: 1,
        },
      ],
      rationale: None,
    },
    SystemMonthlyBatch {
      system_id: 1,
      commands: vec![
        CompetitiveCommand::Invest {
          domain: InvestDomain::Beds,
          amount: 25,
        },
        CompetitiveCommand::Recruit {
          role: RecruitRole::Nurse,
          headcount: 2,
        },
      ],
      rationale: Some("AI (growth) invested in beds and recruited nurses".to_string()),
    },
  ];

  if difficulty.k_rivals() >= 2 {
    batches.push(SystemMonthlyBatch {
      system_id: 2,
      commands: vec![CompetitiveCommand::Commit {
        pledge_type: PledgeType::Access,
        level: 2,
      }],
      rationale: Some("AI (access) issued an access pledge".to_string()),
    });
  }
  if difficulty.k_rivals() >= 3 {
    batches.push(SystemMonthlyBatch {
      system_id: 3,
      commands: vec![CompetitiveCommand::Hold],
      rationale: Some("AI (margin) held to preserve flexibility".to_string()),
    });
  }
  if difficulty.k_rivals() >= 4 {
    batches.push(SystemMonthlyBatch {
      system_id: 4,
      commands: vec![CompetitiveCommand::Hold],
      rationale: Some("AI (political) held to preserve capital".to_string()),
    });
  }

  batches
}

pub fn build_monthly_batches_with_ai(
  prior: &CompetitiveWorldState,
  ruleset: &CompetitiveRuleset,
  seed: u64,
  human_batch: SystemMonthlyBatch,
) -> Result<Vec<SystemMonthlyBatch>, crate::model::CompetitiveValidationError> {
  let mut batches = vec![human_batch];

  for slot in &prior.players {
    let PlayerController::Ai(_) = slot.controller else {
      continue;
    };
    batches.push(compute_ai_batch(slot.system_id, prior, ruleset, seed)?);
  }

  batches.sort_by_key(|batch| batch.system_id);
  Ok(batches)
}

pub fn month1_batches_with_ai(
  prior: &CompetitiveWorldState,
  ruleset: &CompetitiveRuleset,
  seed: u64,
) -> Result<Vec<SystemMonthlyBatch>, crate::model::CompetitiveValidationError> {
  build_monthly_batches_with_ai(prior, ruleset, seed, month1_human_preset_batch())
}

pub fn compute_ai_batch(
  system_id: u32,
  prior: &CompetitiveWorldState,
  ruleset: &CompetitiveRuleset,
  seed: u64,
) -> Result<SystemMonthlyBatch, crate::model::CompetitiveValidationError> {
  let system = prior
    .systems
    .iter()
    .find(|system| system.system_id == system_id)
    .ok_or(crate::model::CompetitiveValidationError::UnknownSystemId { system_id })?;
  let profile = ai_profile_for_system(prior, system_id)
    .ok_or(crate::model::CompetitiveValidationError::UnknownSystemId { system_id })?;
  let observation = observe_for_ai(prior, system_id);
  Ok(crate::actors::compute_ai_batch(
    &observation,
    &profile,
    &system.resources,
    ruleset,
    seed,
  ))
}

pub fn resolve_preset_month1(
  prior: &CompetitiveWorldState,
  ruleset: &CompetitiveRuleset,
  seed: u64,
) -> Result<CompetitiveTransition, crate::model::CompetitiveValidationError> {
  super::month_loop::resolve_competitive_month(prior, ruleset, seed, month1_human_preset_batch())
}

pub fn format_competitive_command(cmd: &CompetitiveCommand) -> String {
  match cmd {
    CompetitiveCommand::Hold => "hold".to_string(),
    CompetitiveCommand::Recruit { role, headcount } => {
      let role_str = match role {
        RecruitRole::Nurse => "nurse",
        RecruitRole::Physician => "physician",
        RecruitRole::Admin => "admin",
      };
      format!("recruit role={} headcount={}", role_str, headcount)
    }
    CompetitiveCommand::Invest { domain, amount } => {
      let domain_str = match domain {
        InvestDomain::Beds => "beds",
        InvestDomain::Outpatient => "outpatient",
        InvestDomain::Technology => "technology",
      };
      format!("invest domain={} amount={}", domain_str, amount)
    }
    CompetitiveCommand::Monitor { target, depth } => {
      let target_str = match target {
        MonitorTarget::Northlake => "northlake",
        MonitorTarget::Summit => "summit",
        MonitorTarget::Valley => "valley",
        MonitorTarget::Metro => "metro",
      };
      format!("monitor target={} depth={}", target_str, depth)
    }
    CompetitiveCommand::Negotiate {
      payer,
      rate_posture,
    } => {
      let payer_str = match payer {
        PayerId::CarrierA => "carrier_a",
        PayerId::CarrierB => "carrier_b",
        PayerId::Medicaid => "medicaid",
        PayerId::Medicare => "medicare",
      };
      let posture_str = match rate_posture {
        RatePosture::Aggressive => "aggressive",
        RatePosture::Neutral => "neutral",
        RatePosture::Conservative => "conservative",
      };
      format!("negotiate payer={} rate_posture={}", payer_str, posture_str)
    }
    CompetitiveCommand::Commit { pledge_type, level } => {
      let pledge_str = match pledge_type {
        PledgeType::Access => "access",
        PledgeType::Quality => "quality",
        PledgeType::Workforce => "workforce",
      };
      format!("commit pledge_type={} level={}", pledge_str, level)
    }
    CompetitiveCommand::Project { kind, budget } => {
      let kind_str = match kind {
        ProjectKind::EhrEpic => "ehr_epic",
        ProjectKind::EhrCerner => "ehr_cerner",
        ProjectKind::Tower => "tower",
        ProjectKind::ClinicNetwork => "clinic_network",
      };
      format!("project kind={} budget={}", kind_str, budget)
    }
  }
}

pub fn resolution_summary_lines(transition: &CompetitiveTransition) -> Vec<String> {
  let mut lines = vec![
    format!(
      "Month {} resolved → Year {}, Month {} (turn {})",
      transition.prior.policy_calendar.month_index,
      transition.next.policy_calendar.year,
      transition.next.policy_calendar.month_in_year,
      transition.next.turn
    ),
    format!("State hash: {}", transition.state_hash),
  ];

  if let Some(human_system) = transition.prior.human_system() {
    lines.push("Player commands resolved:".to_string());
    if let Some(human_batch) = transition
      .aggregated
      .batch_for_system(human_system.system_id)
    {
      if human_batch.commands.is_empty() {
        lines.push("  (none)".to_string());
      } else {
        for cmd in &human_batch.commands {
          lines.push(format!("  • {}", format_competitive_command(cmd)));
        }
      }
    } else {
      lines.push("  (none)".to_string());
    }
  }

  let current_month = transition.prior.policy_calendar.month_index;
  let public_actions: Vec<_> = transition
    .next
    .public_action_log
    .iter()
    .filter(|entry| entry.month_index == current_month)
    .collect();

  lines.push(format!("Public actions logged: {}", public_actions.len()));
  for entry in &public_actions {
    lines.push(format!("  • {}", entry.summary));
  }

  lines.push(format!(
    "Pending effects queued: {}",
    transition.next.effect_queue.len()
  ));

  for event in &transition.events {
    let mut is_rival_private = false;
    if let Some(human_system) = transition.prior.human_system() {
      is_rival_private = transition
        .prior
        .systems
        .iter()
        .filter(|sys| sys.system_id != human_system.system_id)
        .any(|sys| event.description.starts_with(&format!("{}:", sys.name)));
    }
    if !is_rival_private {
      lines.push(format!("  • {}", event.description));
    }
  }

  if let Some(next_human) = transition.next.human_system() {
    lines.push("Next month starting resources:".to_string());
    lines.push(format!(
      "  • Cash: {} | Political Capital: {} | Active Project Draws: {}",
      next_human.resources.cash,
      next_human.resources.political_capital,
      next_human.resources.active_project_monthly_draws
    ));
  }

  lines
}

#[cfg(test)]
mod tests {

  use super::*;
  use crate::model::{Difficulty, default_competitive_ruleset};

  #[test]
  fn preset_batches_match_system_count_per_difficulty() {
    for difficulty in [
      Difficulty::Easy,
      Difficulty::Normal,
      Difficulty::Hard,
      Difficulty::Expert,
    ] {
      let batches = month1_preset_batches(difficulty);
      assert_eq!(batches.len(), (difficulty.k_rivals() + 1) as usize);
    }
  }

  #[test]
  fn resolve_preset_month1_succeeds_for_normal() {
    let ruleset = default_competitive_ruleset();
    let genesis =
      crate::competitive::genesis_competitive_world_with_ruleset(Difficulty::Normal, &ruleset);
    let transition = resolve_preset_month1(&genesis, &ruleset, 42).expect("resolve");
    assert_eq!(transition.next.turn, 1);
  }

  #[test]
  fn test_resolution_summary_lines_formatting() {
    let ruleset = default_competitive_ruleset();
    let genesis =
      crate::competitive::genesis_competitive_world_with_ruleset(Difficulty::Normal, &ruleset);
    let transition = resolve_preset_month1(&genesis, &ruleset, 42).expect("resolve");
    let lines = resolution_summary_lines(&transition);
    println!("--- public action details ---");
    for entry in &transition.next.public_action_log {
      println!(
        "entry.system_id={}, entry.summary='{}'",
        entry.system_id, entry.summary
      );
    }
    println!("-----------------------------");
    for line in &lines {
      println!("{}", line);
    }

    // Check that we render the player's resolved commands
    assert!(
      lines
        .iter()
        .any(|l| l.contains("Player commands resolved:"))
    );
    assert!(lines.iter().any(|l| l.contains("  • hold")));
    assert!(
      lines
        .iter()
        .any(|l| l.contains("  • monitor target=northlake depth=1"))
    );

    // Check that we render public action count and list details
    assert!(lines.iter().any(|l| l.contains("Public actions logged:")));

    // Check that we render next month starting resources
    assert!(
      lines
        .iter()
        .any(|l| l.contains("Next month starting resources:"))
    );
    assert!(
      lines
        .iter()
        .any(|l| l.contains("Cash:") && l.contains("Political Capital:"))
    );
  }
}
