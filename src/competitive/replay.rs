use crate::model::{
  CompetitiveHistory, CompetitiveReplayError, CompetitiveRuleset, CompetitiveWorldState,
};

use super::regenerate_competitive_month;

pub fn regenerate_competitive_history(
  history: &CompetitiveHistory,
  ruleset: &CompetitiveRuleset,
  seed: u64,
) -> Result<CompetitiveWorldState, CompetitiveReplayError> {
  let mut current = history.genesis.clone();
  let mut prior_aggregated = None;

  for expected in &history.transitions {
    let regenerated = regenerate_competitive_month(
      &current,
      ruleset,
      seed,
      expected.aggregated.clone(),
      prior_aggregated.as_ref(),
    )
    .map_err(CompetitiveReplayError::Validation)?;

    if &regenerated != expected {
      return Err(CompetitiveReplayError::TransitionMismatch {
        turn: expected.next.turn,
      });
    }

    current = regenerated.next;
    prior_aggregated = Some(regenerated.aggregated);
  }

  Ok(current)
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::competitive::build_multi_month_resolution_history;
  use crate::model::Difficulty;

  #[test]
  fn regenerates_recorded_history_exactly() {
    let history = build_multi_month_resolution_history(Difficulty::Normal, 42, 3).expect("history");
    let final_state =
      regenerate_competitive_history(&history, &crate::model::default_competitive_ruleset(), 42)
        .expect("regenerated history");
    assert_eq!(final_state, *history.final_state());
  }

  #[test]
  fn rejects_tampered_recorded_transition() {
    let mut history =
      build_multi_month_resolution_history(Difficulty::Normal, 42, 2).expect("history");
    history.transitions[1].effects[0].delta += 1;
    let error =
      regenerate_competitive_history(&history, &crate::model::default_competitive_ruleset(), 42)
        .expect_err("tampered transition");
    assert_eq!(
      error,
      CompetitiveReplayError::TransitionMismatch { turn: 2 }
    );
  }
}
