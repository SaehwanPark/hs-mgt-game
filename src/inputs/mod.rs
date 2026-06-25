mod resolve;
mod rng;
mod streams;

pub use resolve::resolve_inputs;

pub fn ai_player_tie_break(seed: u64, month_index: u32, system_id: u32) -> u32 {
  use rng::{bounded_u32, stream_rng};
  use streams::STREAM_AI_PLAYER_BASE;

  bounded_u32(
    stream_rng(seed, month_index, STREAM_AI_PLAYER_BASE + system_id),
    0,
    u32::MAX,
  )
}

#[cfg(test)]
#[path = "resolve_tests.rs"]
mod resolve_tests;
