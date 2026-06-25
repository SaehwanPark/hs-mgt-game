mod effects;
mod observe;
mod observe_competitive;
mod resolve;
mod transition;
mod transition_competitive;
mod validate;
mod validate_competitive;

pub use observe::observe_for_player;
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
