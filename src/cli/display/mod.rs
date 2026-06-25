mod briefing;
mod dashboard;
mod executive_report;
mod forecast;
mod interactive;
mod print;
mod prompt;
pub mod style;

pub use briefing::{turn_executive_briefing, turn_resolution_summary};
pub use dashboard::{
  describe_strategy_commitments, executive_dashboard, print_pre_run_briefing, strategy_commitments,
  strategy_previews,
};
pub use executive_report::render_executive_report;
pub use forecast::turn_uncertainty_preview;
pub use interactive::{
  print_demo_actor_decision, print_demo_debrief, print_demo_effect, print_demo_event,
  print_demo_replay_footer, print_demo_styled_header, print_demo_turn_separator,
  print_interactive_results,
};
pub use print::{
  eprint_error, print_block, print_line, print_prompt_block, print_turn_briefing_block,
  print_turn_resolution_block, print_turn_uncertainty_block,
};
pub use prompt::{
  PromptContext, campaign_menu_lines, difficulty_menu_lines, format_command_prompt,
  global_commands_footer, play_mode_menu_lines, replay_export_prompt_lines,
  resume_choice_prompt_lines, seed_prompt_lines,
};

#[cfg(test)]
#[path = "briefing_tests.rs"]
mod briefing_tests;
#[cfg(test)]
#[path = "dashboard_tests.rs"]
mod dashboard_tests;
#[cfg(test)]
#[path = "executive_report_tests.rs"]
mod executive_report_tests;
#[cfg(test)]
#[path = "forecast_tests.rs"]
mod forecast_tests;
#[cfg(test)]
#[path = "prompt_tests.rs"]
mod prompt_tests;
#[cfg(test)]
#[path = "style_tests.rs"]
mod style_tests;
