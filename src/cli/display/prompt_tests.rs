use super::prompt::{
  PromptContext, campaign_menu_lines, global_commands_footer, turn_command_prompt,
};
use crate::cli::default_interactive_commands;
use crate::model::default_ruleset;

#[test]
fn play_mode_footer_lists_interactive_beginner_and_global_commands() {
  let footer = global_commands_footer(PromptContext::PlayMode).join("\n");

  assert!(footer.contains("interactive"));
  assert!(footer.contains("beginner"));
  assert!(footer.contains("1/2/3"));
  assert!(footer.contains("q/quit"));
}

#[test]
fn seed_footer_documents_default_seed() {
  let footer = global_commands_footer(PromptContext::Seed).join("\n");

  assert!(footer.contains("default seed (42)"));
}

#[test]
fn campaign_menu_describes_competitive_twenty_four_month_campaign() {
  let menu = campaign_menu_lines().join("\n");

  assert!(menu.contains("24-month campaign"));
  assert!(!menu.contains("month-1"));
}

#[test]
fn competitive_command_footer_documents_fallback_batch() {
  let footer = global_commands_footer(PromptContext::CompetitiveCommand).join("\n");

  assert!(footer.contains("fallback batch"));
  assert!(footer.contains("q/quit"));
  assert!(!footer.contains("preset batch"));
}

#[test]
fn turn_command_prompt_lists_parameters_bounds_defaults_and_global_footer() {
  let ruleset = default_ruleset();
  let defaults = default_interactive_commands();
  let mut prompt = turn_command_prompt(1, &ruleset, &defaults[0]);
  prompt.extend(global_commands_footer(PromptContext::TurnCommand {
    turn: 1,
  }));
  let text = prompt.join("\n");

  assert!(text.contains("staffed_beds"));
  assert!(text.contains("capital_spend"));
  assert!(text.contains("requested_rate"));
  assert!(text.contains("0–40"));
  assert!(text.contains("8 18 112"));
  assert!(text.contains("Global: Enter"));
  assert!(text.contains("q/quit"));
}

#[test]
fn turn_three_prompt_includes_schedule_relief_bound() {
  let ruleset = default_ruleset();
  let defaults = default_interactive_commands();
  let prompt = turn_command_prompt(3, &ruleset, &defaults[2]).join("\n");

  assert!(prompt.contains("schedule_relief"));
  assert!(prompt.contains("1–20"));
}

#[test]
fn turn_five_prompt_includes_access_posture_bound() {
  let ruleset = default_ruleset();
  let defaults = default_interactive_commands();
  let prompt = turn_command_prompt(5, &ruleset, &defaults[4]).join("\n");

  assert!(prompt.contains("access_posture"));
  assert!(prompt.contains("1–15"));
}
