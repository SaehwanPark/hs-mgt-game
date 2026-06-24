mod display;
mod error;
mod export;
mod io;
mod output;
mod parse;
mod session;
mod strategy;

pub use display::{
  describe_strategy_commitments, eprint_error, executive_dashboard, format_command_prompt,
  print_line, print_pre_run_briefing, strategy_commitments, strategy_previews,
  turn_executive_briefing, turn_resolution_summary,
};
pub use error::describe_cli_error;
pub use io::{parse_play_mode_choice, parse_seed_choice, read_play_mode_choice, read_seed_choice};
pub use output::print_demo;
pub use parse::{
  describe_command_defaults, parse_coalition_command, parse_policy_command,
  parse_stabilize_access_command, parse_workforce_command,
};
pub use session::{read_run_config, run, run_interactive_history, run_session};
pub use strategy::{
  build_history_for_strategy, build_history_interactive, default_interactive_commands,
  strategy_plan,
};

#[cfg(test)]
#[path = "io_tests.rs"]
mod io_tests;
#[cfg(test)]
#[path = "parse_tests.rs"]
mod parse_tests;
#[cfg(test)]
#[path = "strategy_tests.rs"]
mod strategy_tests;
