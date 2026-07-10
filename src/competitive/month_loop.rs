use crate::inputs::resolve_competitive_inputs;
use crate::model::{
  AggregatedMonthlyActions, CompetitiveCommand, CompetitiveHistory, CompetitiveRuleset,
  CompetitiveTransition, CompetitiveValidationError, CompetitiveWorldState, Difficulty,
  SystemMonthlyBatch, default_competitive_ruleset,
};
use crate::sim::{
  apply_institution_phase, apply_month_start_tick, observe_for_human, resolve_monthly_batches,
  transition_competitive,
};

use super::resolution::{build_monthly_batches_with_ai, month1_human_preset_batch};

pub fn human_batch_for_month(turn: u32) -> SystemMonthlyBatch {
  if turn == 0 {
    month1_human_preset_batch()
  } else {
    SystemMonthlyBatch::new(0, vec![CompetitiveCommand::Hold])
  }
}

pub fn resolve_competitive_month(
  prior: &CompetitiveWorldState,
  ruleset: &CompetitiveRuleset,
  seed: u64,
  human_batch: SystemMonthlyBatch,
  prior_aggregated: Option<&AggregatedMonthlyActions>,
) -> Result<CompetitiveTransition, CompetitiveValidationError> {
  let consultant_options = observe_for_human(prior, prior_aggregated).consultant_options;
  let mut working = prior.clone();
  let inputs = resolve_competitive_inputs(
    seed,
    working.policy_calendar.month_index,
    working.policy_calendar.is_annual_tick(),
  );
  let mut pre_events = Vec::new();
  apply_month_start_tick(&mut working, &inputs, &mut pre_events);

  let batches = build_monthly_batches_with_ai(&working, ruleset, seed, human_batch)?;
  let aggregated = resolve_monthly_batches(&working, &batches, ruleset)?;
  let mut transition = transition_competitive(&working, aggregated.clone(), ruleset)?;

  let mut institution_events = Vec::new();
  apply_institution_phase(&mut transition.next, &aggregated, &mut institution_events);

  transition
    .events
    .splice(0..0, pre_events.into_iter().chain(institution_events));
  transition.state_hash = crate::model::hash_competitive_state(&transition.next, ruleset);
  transition.consultant_options = consultant_options;

  Ok(transition)
}

pub fn build_multi_month_resolution_history(
  difficulty: Difficulty,
  seed: u64,
  months: u32,
) -> Result<CompetitiveHistory, CompetitiveValidationError> {
  let ruleset = default_competitive_ruleset();
  let genesis = crate::competitive::genesis_competitive_world_with_ruleset(difficulty, &ruleset);
  let mut transitions = Vec::with_capacity(months as usize);
  let mut current = genesis.clone();
  let mut prior_aggregated = None;

  for _ in 0..months {
    let human_batch = human_batch_for_month(current.turn);
    let transition = resolve_competitive_month(
      &current,
      &ruleset,
      seed,
      human_batch,
      prior_aggregated.as_ref(),
    )?;
    current = transition.next.clone();
    prior_aggregated = Some(transition.aggregated.clone());
    transitions.push(transition);
  }

  Ok(CompetitiveHistory {
    genesis,
    transitions,
  })
}

pub fn build_month1_resolution_history(
  difficulty: Difficulty,
  seed: u64,
) -> Result<CompetitiveHistory, CompetitiveValidationError> {
  build_multi_month_resolution_history(difficulty, seed, 1)
}

#[cfg(test)]
mod loop_tests {
  use super::*;

  #[test]
  fn three_month_history_advances_turn_and_calendar() {
    let history = build_multi_month_resolution_history(Difficulty::Normal, 42, 3).expect("history");
    assert_eq!(history.transitions.len(), 3);
    assert_eq!(history.final_state().turn, 3);
    assert_eq!(history.final_state().policy_calendar.month_index, 4);
    assert_eq!(history.transitions[0].consultant_options.len(), 4);
    assert_eq!(history.transitions[2].consultant_options.len(), 4);
  }

  #[test]
  fn two_month_history_includes_environment_events() {
    let history = build_multi_month_resolution_history(Difficulty::Normal, 42, 2).expect("history");
    assert_eq!(history.transitions.len(), 2);
    assert!(
      history.transitions[1]
        .events
        .iter()
        .any(|event| event.actor == "environment")
    );
  }

  #[test]
  fn human_fallback_uses_month_one_preset_then_hold() {
    assert_eq!(human_batch_for_month(0), month1_human_preset_batch());
    assert_eq!(
      human_batch_for_month(1),
      SystemMonthlyBatch::new(0, vec![CompetitiveCommand::Hold])
    );
    assert_eq!(
      human_batch_for_month(2),
      SystemMonthlyBatch::new(0, vec![CompetitiveCommand::Hold])
    );
  }
}
