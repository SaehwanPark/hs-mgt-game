use crate::actors::compute_ai_batch;
use crate::model::{
  CompetitiveCommand, CompetitiveHistory, CompetitiveRuleset, CompetitiveTransition,
  CompetitiveWorldState, Difficulty, MonitorTarget, PlayerController, SystemMonthlyBatch,
  default_competitive_ruleset,
};
use crate::sim::{observe_for_ai, resolve_monthly_batches, transition_competitive};

pub const DEFAULT_COMPETITIVE_SEED: u64 = 42;

pub fn month1_human_preset_batch() -> SystemMonthlyBatch {
  SystemMonthlyBatch::new(
    0,
    vec![
      CompetitiveCommand::Hold,
      CompetitiveCommand::Monitor {
        target: MonitorTarget::Northlake,
        depth: 1,
      },
    ],
  )
}

pub fn build_monthly_batches_with_ai(
  world: &CompetitiveWorldState,
  ruleset: &CompetitiveRuleset,
  seed: u64,
  human_batch: SystemMonthlyBatch,
) -> Vec<SystemMonthlyBatch> {
  let mut batches = vec![human_batch];

  for slot in &world.players {
    let PlayerController::Ai(profile) = slot.controller else {
      continue;
    };
    let system = world
      .systems
      .iter()
      .find(|system| system.system_id == slot.system_id)
      .expect("player slot must reference a system");
    let observation = observe_for_ai(world, slot.system_id);
    batches.push(compute_ai_batch(
      &observation,
      &profile,
      &system.resources,
      ruleset,
      seed,
    ));
  }

  batches.sort_by_key(|batch| batch.system_id);
  batches
}

pub fn month1_preset_batches(difficulty: Difficulty) -> Vec<SystemMonthlyBatch> {
  let ruleset = default_competitive_ruleset();
  let genesis = crate::competitive::genesis_competitive_world_with_ruleset(difficulty, &ruleset);
  build_monthly_batches_with_ai(
    &genesis,
    &ruleset,
    DEFAULT_COMPETITIVE_SEED,
    month1_human_preset_batch(),
  )
}

pub fn resolve_month1_with_ai(
  prior: &CompetitiveWorldState,
  ruleset: &CompetitiveRuleset,
  seed: u64,
) -> Result<CompetitiveTransition, crate::model::CompetitiveValidationError> {
  let batches = build_monthly_batches_with_ai(prior, ruleset, seed, month1_human_preset_batch());
  let aggregated = resolve_monthly_batches(prior, &batches, ruleset)?;
  transition_competitive(prior, aggregated, ruleset)
}

pub fn resolve_preset_month1(
  prior: &CompetitiveWorldState,
  ruleset: &CompetitiveRuleset,
) -> Result<CompetitiveTransition, crate::model::CompetitiveValidationError> {
  resolve_month1_with_ai(prior, ruleset, DEFAULT_COMPETITIVE_SEED)
}

pub fn build_month1_resolution_history(
  difficulty: Difficulty,
) -> Result<CompetitiveHistory, crate::model::CompetitiveValidationError> {
  build_month1_resolution_history_with_seed(difficulty, DEFAULT_COMPETITIVE_SEED)
}

pub fn build_month1_resolution_history_with_seed(
  difficulty: Difficulty,
  seed: u64,
) -> Result<CompetitiveHistory, crate::model::CompetitiveValidationError> {
  let ruleset = default_competitive_ruleset();
  let genesis = crate::competitive::genesis_competitive_world_with_ruleset(difficulty, &ruleset);
  let transition = resolve_month1_with_ai(&genesis, &ruleset, seed)?;
  Ok(CompetitiveHistory {
    genesis,
    transitions: vec![transition],
  })
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

  for batch in &transition.aggregated.batches {
    if let Some(rationale) = &batch.rationale {
      let system_name = transition
        .prior
        .systems
        .iter()
        .find(|system| system.system_id == batch.system_id)
        .map(|system| system.name.as_str())
        .unwrap_or("unknown system");
      lines.push(format!("  AI {system_name}: {rationale}"));
    }
  }

  for event in &transition.events {
    lines.push(format!("  • {}", event.description));
  }

  lines
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::model::Difficulty;
  use crate::sim::ai_profile_for_system;

  #[test]
  fn ai_batches_match_system_count_per_difficulty() {
    for difficulty in [
      Difficulty::Easy,
      Difficulty::Normal,
      Difficulty::Hard,
      Difficulty::Expert,
    ] {
      let batches = month1_preset_batches(difficulty);
      assert_eq!(batches.len(), (difficulty.k_rivals() + 1) as usize);
      assert!(
        batches
          .iter()
          .filter(|batch| batch.rationale.is_some())
          .count()
          == difficulty.k_rivals() as usize
      );
    }
  }

  #[test]
  fn resolve_month1_with_ai_succeeds_for_normal() {
    let ruleset = default_competitive_ruleset();
    let genesis =
      crate::competitive::genesis_competitive_world_with_ruleset(Difficulty::Normal, &ruleset);
    let transition =
      resolve_month1_with_ai(&genesis, &ruleset, DEFAULT_COMPETITIVE_SEED).expect("resolve");
    assert_eq!(transition.next.turn, 1);
    assert!(ai_profile_for_system(&genesis, 1).is_some());
  }

  #[test]
  fn ai_batches_are_stable_for_seed_42() {
    let ruleset = default_competitive_ruleset();
    let genesis =
      crate::competitive::genesis_competitive_world_with_ruleset(Difficulty::Normal, &ruleset);
    let first = build_monthly_batches_with_ai(
      &genesis,
      &ruleset,
      DEFAULT_COMPETITIVE_SEED,
      month1_human_preset_batch(),
    );
    let second = build_monthly_batches_with_ai(
      &genesis,
      &ruleset,
      DEFAULT_COMPETITIVE_SEED,
      month1_human_preset_batch(),
    );
    assert_eq!(first, second);
  }
}
