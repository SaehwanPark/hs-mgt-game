mod resolve;
mod resolve_affiliation;
mod resolve_competitive;
mod rng;
mod streams;

pub use resolve::resolve_inputs;
pub use resolve_affiliation::resolve_affiliation_inputs;
pub use resolve_competitive::resolve_competitive_inputs;

pub fn ai_player_tie_break(seed: u64, month_index: u32, system_id: u32) -> u32 {
  use rng::stream_rng;
  use streams::STREAM_AI_PLAYER_BASE;

  stream_rng(seed, month_index, STREAM_AI_PLAYER_BASE + system_id) as u32
}

#[cfg(test)]
#[path = "resolve_tests.rs"]
mod resolve_tests;
