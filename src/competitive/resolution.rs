use crate::model::{
  CompetitiveCommand, CompetitiveRuleset, CompetitiveTransition, CompetitiveWorldState, Difficulty,
  InvestDomain, MonitorTarget, PlayerController, PledgeType, RecruitRole, SystemMonthlyBatch,
};
use crate::sim::{ai_profile_for_system, observe_for_ai};

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

pub fn resolution_summary_lines(transition: &CompetitiveTransition) -> Vec<String> {
  let mut lines = vec![
    format!(
      "Month {} resolved → Year {}, Month {} (turn {})",
      transition.prior.policy_calendar.month_index,
      transition.next.policy_calendar.year,
      transition.next.policy_calendar.month_in_year,
      transition.next.turn
    ),
    format!(
      "Public actions logged: {}",
      transition
        .next
        .public_action_log
        .iter()
        .filter(|entry| entry.month_index == transition.prior.policy_calendar.month_index)
        .count()
    ),
    format!(
      "Pending effects queued: {}",
      transition.next.effect_queue.len()
    ),
    format!("State hash: {}", transition.state_hash),
  ];

  for event in &transition.events {
    lines.push(format!("  • {}", event.description));
  }

  lines
}

#[cfg(test)]
mod tests {

  use super::*;
  use crate::model::Difficulty;

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
}
