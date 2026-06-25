mod effects;
mod effects_competitive;
mod observe;
mod observe_ai;
mod observe_competitive;
mod resolve;
mod transition;
mod transition_competitive;
mod validate;
mod validate_competitive;

pub use effects_competitive::{
  apply_due_pending_effects, apply_institution_phase, apply_month_start_tick,
};
pub use observe::observe_for_player;
pub use observe_ai::{
  AiPlayerObservation, LaggedRivalAction, ai_profile_for_system, observe_for_ai,
};
pub use observe_competitive::observe_for_human;
pub use resolve::resolve_monthly_batches;
pub use transition::transition;
pub use transition_competitive::transition_competitive;
pub use validate_competitive::{validate_competitive_batch, validate_competitive_command};

#[cfg(test)]
#[path = "transition_tests.rs"]
mod transition_tests;
#[cfg(test)]
#[path = "validate_competitive_tests.rs"]
mod validate_competitive_tests;
