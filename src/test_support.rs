use crate::cli::build_history_for_strategy;
use crate::model::{
  DEFAULT_SEED, History, PlayMode, ReplayArtifact, StrategyPath, default_ruleset,
};

pub fn demo_history() -> History {
  let ruleset = default_ruleset();
  build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset).unwrap()
}

pub fn sample_replay_artifact(play_mode: PlayMode, history: History) -> ReplayArtifact {
  ReplayArtifact {
    seed: DEFAULT_SEED,
    play_mode,
    ruleset_version: default_ruleset().version.to_string(),
    history,
  }
}
