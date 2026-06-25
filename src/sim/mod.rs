mod effects;
mod observe;
mod transition;
mod validate;
mod validate_competitive;

pub use observe::observe_for_player;
pub use transition::transition;
pub use validate_competitive::{validate_competitive_batch, validate_competitive_command};

#[cfg(test)]
#[path = "transition_tests.rs"]
mod transition_tests;
#[cfg(test)]
#[path = "validate_competitive_tests.rs"]
mod validate_competitive_tests;
