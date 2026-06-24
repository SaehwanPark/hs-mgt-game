use crate::model::{History, ReplayError, ReplayVerification, Ruleset};
use crate::sim::transition;

pub fn replay(history: &History, ruleset: &Ruleset) -> Result<ReplayVerification, ReplayError> {
  let mut state = history.genesis.clone();

  for committed in &history.transitions {
    let replayed = transition(
      &state,
      committed.command.clone(),
      committed.resolved_inputs.clone(),
      ruleset,
    )
    .map_err(ReplayError::InvalidTransition)?;

    if replayed.state_hash != committed.state_hash {
      return Err(ReplayError::StateHashMismatch {
        turn: replayed.next.turn,
        expected: committed.state_hash.clone(),
        actual: replayed.state_hash,
      });
    }

    state = replayed.next;
  }

  Ok(ReplayVerification { final_state: state })
}
