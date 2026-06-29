use crate::model::{Observation, PlayerCommand, Ruleset, StrategyPath, WorldState};

use super::display::style;
use super::strategy::strategy_plan;

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct BeginnerOption {
  pub label: &'static str,
  pub pros: &'static str,
  pub cons: &'static str,
  pub tradeoff: &'static str,
  pub recommendability: &'static str,
  pub command: PlayerCommand,
}

pub fn beginner_options(turn: u32) -> [BeginnerOption; 3] {
  [
    option_for_turn(StrategyPath::AccessStabilization, turn),
    option_for_turn(StrategyPath::FiscalCaution, turn),
    option_for_turn(StrategyPath::AggressiveBargaining, turn),
  ]
}

pub fn format_beginner_menu(
  turn: u32,
  _state: &WorldState,
  _observation: &Observation,
  _ruleset: &Ruleset,
) -> Vec<String> {
  let mut lines = vec![style::section_heading(
    style::EMOJI_BRIEFING,
    &format!("Turn {turn} — choose an option"),
  )];

  for (index, option) in beginner_options(turn).iter().enumerate() {
    lines.push(String::new());
    lines.push(style::option_line(
      &(index + 1).to_string(),
      option.label,
      option.recommendability,
    ));
    lines.push(format!("    Pros: {}", option.pros));
    lines.push(format!("    Cons: {}", option.cons));
    lines.push(format!("    Trade-off: {}", option.tradeoff));
  }

  lines.push(String::new());
  lines.push(style::subsection("Enter 1, 2, or 3"));
  lines
}

pub fn parse_beginner_choice(input: &str, turn: u32) -> Result<PlayerCommand, String> {
  let trimmed = input.trim();
  if trimmed.is_empty() {
    return Err("enter 1, 2, or 3".to_string());
  }

  let choice = trimmed
    .parse::<usize>()
    .map_err(|_| format!("'{trimmed}' is not a valid option"))?;

  if !(1..=3).contains(&choice) {
    return Err(format!("option {choice} is not available; use 1, 2, or 3"));
  }

  Ok(beginner_options(turn)[choice - 1].command.clone())
}

fn option_for_turn(path: StrategyPath, turn: u32) -> BeginnerOption {
  let plan = strategy_plan(path);
  let (label, pros, cons, tradeoff, recommendability, command) = match (path, turn) {
    (StrategyPath::AccessStabilization, 1) => (
      "Balanced capacity build",
      "Adds meaningful beds and spend; moderate rate bid",
      "Uses more cash than cautious paths",
      "Access gains vs reserves",
      "Recommended",
      plan.first_command.clone(),
    ),
    (StrategyPath::FiscalCaution, 1) => (
      "Measured expansion",
      "Preserves more cash; still adds beds",
      "Smaller access lift; less leverage for payer talks",
      "Fiscal buffer vs access pace",
      "Situational",
      plan.first_command.clone(),
    ),
    (StrategyPath::AggressiveBargaining, 1) => (
      "Lean operations, hard bargain",
      "Minimal capital spend; high rate bid",
      "Little capacity added; weak visible leverage for a high rate ask",
      "Revenue ambition vs relationship risk",
      "High risk",
      plan.first_command.clone(),
    ),
    (StrategyPath::AccessStabilization, 2) => (
      "Credible mandate response",
      "Solid advocacy and access commitment",
      "Meaningful advocacy spend",
      "Policy relief vs cash",
      "Recommended",
      plan.second_command.clone(),
    ),
    (StrategyPath::FiscalCaution, 2) => (
      "Measured compliance",
      "Lower advocacy spend",
      "May leave policy pressure elevated",
      "Cost control vs scrutiny",
      "Situational",
      plan.second_command.clone(),
    ),
    (StrategyPath::AggressiveBargaining, 2) => (
      "Minimal engagement",
      "Lowest advocacy spend",
      "Weak access signal to regulators",
      "Savings vs oversight risk",
      "High risk",
      plan.second_command.clone(),
    ),
    (StrategyPath::AccessStabilization, 3) => (
      "Workforce stabilization",
      "Strong retention and schedule relief",
      "Higher spend",
      "Trust recovery vs budget",
      "Recommended",
      plan.third_command.clone(),
    ),
    (StrategyPath::FiscalCaution, 3) => (
      "Targeted retention",
      "Moderate workforce investment",
      "May not fully ease pressure",
      "Partial relief vs cost",
      "Situational",
      plan.third_command.clone(),
    ),
    (StrategyPath::AggressiveBargaining, 3) => (
      "Defer workforce spending",
      "Preserves cash",
      "Low schedule relief risks labor friction",
      "Short-term savings vs trust",
      "High risk",
      plan.third_command.clone(),
    ),
    (StrategyPath::AccessStabilization, 4) => (
      "Full coalition partner",
      "Strong shared access signal",
      "Higher coalition investment",
      "Regional leverage vs spend",
      "Recommended",
      plan.fourth_command.clone(),
    ),
    (StrategyPath::FiscalCaution, 4) => (
      "Limited coalition role",
      "Lower investment",
      "Reduced coalition leverage",
      "Participation vs cost",
      "Situational",
      plan.fourth_command.clone(),
    ),
    (StrategyPath::AggressiveBargaining, 4) => (
      "Token participation",
      "Minimal coalition spend",
      "Partners may offer less support",
      "Visibility vs credibility",
      "High risk",
      plan.fourth_command.clone(),
    ),
    (StrategyPath::AccessStabilization, 5) => (
      "Defensive capacity match",
      "Solid defensive capital and access posture",
      "Uses meaningful reserves",
      "Market position vs cash",
      "Recommended",
      plan.fifth_command.clone(),
    ),
    (StrategyPath::FiscalCaution, 5) => (
      "Guarded response",
      "Moderate defensive spend",
      "May concede share if rival expands",
      "Selective defense vs cost",
      "Situational",
      plan.fifth_command.clone(),
    ),
    (StrategyPath::AggressiveBargaining, 5) => (
      "Minimal defense",
      "Low capital commitment",
      "Vulnerable if rival accelerates",
      "Cash preservation vs share loss",
      "High risk",
      plan.fifth_command.clone(),
    ),
    _ => panic!("beginner options support the five-turn demo only"),
  };

  BeginnerOption {
    label,
    pros,
    cons,
    tradeoff,
    recommendability,
    command,
  }
}

#[cfg(test)]
#[path = "beginner_tests.rs"]
mod beginner_tests;
