use crate::model::{DEFAULT_SEED, PlayerCommand, Ruleset};

use super::style::{self, EMOJI_BRIEFING};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum PromptContext {
  ResumeChoice,
  Campaign,
  Difficulty,
  PlayMode,
  Seed,
  TurnCommand { turn: u32 },
  BeginnerTurn { turn: u32 },
  ReplayExport,
  ValidationDemo,
  CompetitiveCommand,
}

pub fn global_commands_footer(context: PromptContext) -> Vec<String> {
  let line = match context {
    PromptContext::ResumeChoice => {
      "Global: r → resume · n → start over · ?/help · q/quit/exit".to_string()
    }
    PromptContext::Campaign => {
      "Global: Enter/1 → stabilization · 2/c/C → competitive preview · ?/help · q/quit/exit"
        .to_string()
    }
    PromptContext::Difficulty => {
      "Global: Enter/2 → normal · 1/3/4 → other tiers · ?/help · q/quit/exit".to_string()
    }
    PromptContext::PlayMode => {
      "Global: Enter/i → interactive · b → beginner · 1/2/3 → presets · ?/help · q/quit/exit"
        .to_string()
    }
    PromptContext::Seed => {
      format!("Global: Enter → default seed ({DEFAULT_SEED}) · ?/help · q/quit/exit")
    }
    PromptContext::TurnCommand { .. } => {
      "Global: Enter → defaults · ?/help · q/quit/exit".to_string()
    }
    PromptContext::BeginnerTurn { .. } => {
      "Global: 1/2/3 → choose option · ?/help · q/quit/exit".to_string()
    }
    PromptContext::ReplayExport => "Global: Enter → skip export · ?/help · q/quit/exit".to_string(),
    PromptContext::ValidationDemo => {
      "Global: 1–5 → preset batch · Enter → skip · ?/help · q/quit/exit".to_string()
    }
    PromptContext::CompetitiveCommand => {
      "Global: Enter → fallback batch · ?/help · q/quit/exit".to_string()
    }
  };

  vec![style::subsection("Global commands"), format!("  {line}")]
}

pub fn resume_choice_prompt_lines() -> Vec<String> {
  vec![
    style::section_heading(style::EMOJI_STRATEGY, "Saved session found"),
    style::label_value("Resume", "r — continue where you left off"),
    style::label_value("Start over", "n — delete autosave and begin fresh"),
  ]
}

pub fn competitive_resume_choice_prompt_lines() -> Vec<String> {
  vec![
    style::section_heading(style::EMOJI_STRATEGY, "Saved competitive campaign found"),
    style::label_value("Resume", "r — continue where you left off"),
    style::label_value("Start over", "n — delete autosave and begin fresh"),
  ]
}

pub fn campaign_menu_lines() -> Vec<String> {
  vec![
    style::section_heading(style::EMOJI_STRATEGY, "Choose campaign"),
    style::dim("  Enter or 1 → Regional stabilization demo (five-turn playable)"),
    style::dim("  2 or c → Competitive regional market (24-month campaign)"),
    style::dim("  3 or a → Regional affiliation decision (six-stage scenario)"),
  ]
}

pub fn difficulty_menu_lines() -> Vec<String> {
  vec![
    style::section_heading(style::EMOJI_STRATEGY, "Choose difficulty"),
    style::option_line(
      "1",
      "Easy",
      "1 AI rival · 4 AP/month (Rivals: 40 cash / 5 PC, Conservative)",
    ),
    style::option_line(
      "2",
      "Normal",
      "2 AI rivals · 3 AP/month (Rivals: 60 cash / 8 PC, Moderate) (default)",
    ),
    style::option_line(
      "3",
      "Hard",
      "3 AI rivals · 3 AP/month (Rivals: 80 cash / 12 PC, Aggressive)",
    ),
    style::option_line(
      "4",
      "Expert",
      "4 AI rivals · 2 AP/month (Rivals: 100 cash / 15 PC, Aggressive)",
    ),
  ]
}

pub fn play_mode_menu_lines() -> Vec<String> {
  vec![
    style::section_heading(style::EMOJI_STRATEGY, "Choose play mode"),
    style::dim("  Enter or i → Interactive (standard)"),
    style::dim("  b → Beginner (guided multiple choice)"),
    style::option_line("1", "Access stabilization", "preset strategy path"),
    style::option_line("2", "Fiscal caution", "preset strategy path"),
    style::option_line("3", "Aggressive bargaining", "preset strategy path"),
  ]
}

pub fn seed_prompt_lines() -> Vec<String> {
  vec![
    style::subsection("Run seed"),
    style::label_value(
      "Enter a positive integer",
      &format!("or press Enter for default {DEFAULT_SEED}"),
    ),
  ]
}

pub fn replay_export_prompt_lines() -> Vec<String> {
  vec![
    style::section_heading(style::EMOJI_EXPORT, "Export replay artifact?"),
    style::label_value("Path", "enter a file path, or press Enter to skip"),
  ]
}

pub fn turn_command_prompt(
  turn_number: u32,
  ruleset: &Ruleset,
  default_command: &PlayerCommand,
) -> Vec<String> {
  let (title, field_lines) = turn_field_lines(turn_number, ruleset);
  let mut lines = vec![style::section_heading(
    EMOJI_BRIEFING,
    &format!("Turn {turn_number} — {title}"),
  )];

  lines.push(style::subsection("Enter integers (space-separated):"));
  lines.extend(field_lines);
  lines.push(String::new());
  lines.push(style::subsection("Defaults"));
  lines.push(format!("  {}", default_command_values(default_command)));

  lines
}

fn turn_field_lines(turn_number: u32, ruleset: &Ruleset) -> (&'static str, Vec<String>) {
  match turn_number {
    1 => (
      "Capacity and payer posture",
      vec![
        field_line("staffed_beds", "beds to add (>0)", None),
        field_line(
          "capital_spend",
          "$ spend",
          Some(format!("0–{}", ruleset.max_capital_spend)),
        ),
        field_line("requested_rate", "commercial rate bid", None),
      ],
    ),
    2 => (
      "State access mandate",
      vec![
        field_line(
          "advocacy_spend",
          "$ spend",
          Some(format!("0–{}", ruleset.max_advocacy_spend)),
        ),
        field_line("access_commitment", "access units", Some(">0".to_string())),
      ],
    ),
    3 => (
      "Workforce pressure",
      vec![
        field_line(
          "retention_spend",
          "$ spend",
          Some(format!("0–{}", ruleset.max_retention_spend)),
        ),
        field_line(
          "schedule_relief",
          "schedule relief units",
          Some(format!("1–{}", ruleset.max_schedule_relief_commitment)),
        ),
      ],
    ),
    4 => (
      "Regional access coalition",
      vec![
        field_line(
          "coalition_investment",
          "$ investment",
          Some(format!("0–{}", ruleset.max_coalition_investment)),
        ),
        field_line(
          "shared_access_commitment",
          "shared access units",
          Some(format!("1–{}", ruleset.max_shared_access_commitment)),
        ),
      ],
    ),
    5 => (
      "Competitor capacity",
      vec![
        field_line(
          "defensive_capital",
          "$ defensive capital",
          Some(format!("0–{}", ruleset.max_defensive_capital_commitment)),
        ),
        field_line(
          "access_posture",
          "access posture units",
          Some(format!("1–{}", ruleset.max_access_posture)),
        ),
      ],
    ),
    _ => ("Unknown turn", vec![]),
  }
}

fn field_line(name: &str, description: &str, range: Option<String>) -> String {
  let range_suffix = range.map(|value| format!(" ({value})")).unwrap_or_default();

  if style::styling_enabled() {
    format!(
      "  {}  {}{}",
      style::accent(&format!("{name:<24}")),
      style::dim(description),
      style::dim(&range_suffix)
    )
  } else {
    format!("  {name:<24}  {description}{range_suffix}")
  }
}

fn default_command_values(command: &PlayerCommand) -> String {
  match command {
    PlayerCommand::StabilizeAccess {
      add_staffed_beds,
      capital_spend,
      requested_commercial_rate,
    } => format!("{add_staffed_beds} {capital_spend} {requested_commercial_rate}"),
    PlayerCommand::RespondToStateAccessMandate {
      advocacy_spend,
      access_commitment,
    } => format!("{advocacy_spend} {access_commitment}"),
    PlayerCommand::RespondToWorkforcePressure {
      retention_spend,
      schedule_relief_commitment,
    } => format!("{retention_spend} {schedule_relief_commitment}"),
    PlayerCommand::JoinRegionalAccessCoalition {
      coalition_investment,
      shared_access_commitment,
    } => format!("{coalition_investment} {shared_access_commitment}"),
    PlayerCommand::RespondToCompetitorCapacityMove {
      defensive_capital_commitment,
      access_posture,
    } => format!("{defensive_capital_commitment} {access_posture}"),
  }
}

pub fn format_command_prompt(
  turn_number: u32,
  ruleset: &Ruleset,
  default_command: &PlayerCommand,
) -> String {
  let mut lines = turn_command_prompt(turn_number, ruleset, default_command);
  lines.extend(global_commands_footer(PromptContext::TurnCommand {
    turn: turn_number,
  }));
  lines.join("\n")
}
