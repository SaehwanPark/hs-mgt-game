use super::display::{PromptContext, print_block, style};

pub fn print_context_help(context: PromptContext) {
  print_block(&context_help_lines(context));
}

pub fn context_help_lines(context: PromptContext) -> Vec<String> {
  let mut lines = vec![style::section_heading(style::EMOJI_BRIEFING, "Help")];

  match context {
    PromptContext::ResumeChoice => {
      lines.push("  Resume continues your saved interactive session.".to_string());
      lines.push("  Start over deletes the autosave and begins a fresh run.".to_string());
    }
    PromptContext::PlayMode => {
      lines.push("  Interactive (Enter or i): choose each turn yourself.".to_string());
      lines
        .push("  Beginner (b): multiple-choice turns with pros, cons, and trade-offs.".to_string());
      lines.push("  Presets 1–3: watch a scripted five-turn strategy path.".to_string());
      lines.push(
        "  Read the executive dashboard above for starting cash, capacity, and trust.".to_string(),
      );
      lines.push(
        "  Reported access and quality may differ from true conditions during play.".to_string(),
      );
    }
    PromptContext::Seed => {
      lines.push(
        "  The seed fixes stochastic inputs (measurement noise, labor shocks, etc.).".to_string(),
      );
      lines.push(
        "  The same seed and commands always produce the same run for classroom replay."
          .to_string(),
      );
    }
    PromptContext::TurnCommand { turn } => {
      lines.extend(turn_help_lines(turn));
      lines.push("  Press Enter without typing to accept the listed defaults.".to_string());
    }
    PromptContext::BeginnerTurn { turn } => {
      lines.push(format!(
        "  Turn {turn}: pick 1, 2, or 3 to choose a curated option."
      ));
      lines.push("  Options mirror the three preset strategy paths for this decision.".to_string());
      lines.push(
        "  Recommendability is guidance only — outcomes still depend on rivals and payers."
          .to_string(),
      );
    }
    PromptContext::ReplayExport => {
      lines.push("  Replay artifacts record the full run for classroom analysis.".to_string());
      lines.push("  Press Enter to skip export.".to_string());
    }
  }

  lines.push(style::dim("  Type your choice again after reading help."));
  lines
}

fn turn_help_lines(turn: u32) -> Vec<String> {
  match turn {
    1 => vec![
      "  Turn 1 — capacity and payer posture: add staffed beds, spend capital, and bid a commercial rate.".to_string(),
      "  Higher beds and spend improve access but consume cash; aggressive rates may draw payer pushback.".to_string(),
    ],
    2 => vec![
      "  Turn 2 — state access mandate: advocacy spend and an access commitment signal responsiveness.".to_string(),
      "  Balance policy pressure relief against cash and credibility.".to_string(),
    ],
    3 => vec![
      "  Turn 3 — workforce pressure: retention spend and schedule relief affect workforce trust.".to_string(),
      "  Under-committing can erode labor cooperation.".to_string(),
    ],
    4 => vec![
      "  Turn 4 — regional access coalition: shared investment and access commitment.".to_string(),
      "  Coalition leverage depends on credible participation.".to_string(),
    ],
    5 => vec![
      "  Turn 5 — competitor capacity: defensive capital and access posture.".to_string(),
      "  Read the market competition briefing before choosing.".to_string(),
    ],
    _ => vec!["  Enter integers as shown in the field list.".to_string()],
  }
}

pub fn new_player_cue_lines() -> Vec<String> {
  vec![
    style::section_heading(style::EMOJI_BRIEFING, "New player"),
    "  Suggested flow each turn: uncertainty preview → executive briefing → your decision."
      .to_string(),
    "  Type ? or help anytime for context; q, quit, or exit saves and leaves (interactive only)."
      .to_string(),
    style::dim("  This note is shown once; use ? later for help.").to_string(),
  ]
}

pub fn turn_hint(turn: u32) -> Option<&'static str> {
  match turn {
    1 => Some("Tip: compare capital spend bound with how many beds you add."),
    2 => Some("Tip: advocacy spend is capped — pair it with a credible access commitment."),
    3 => Some("Tip: schedule relief must be at least 1; balance spend and commitment."),
    4 => Some("Tip: coalition investment and shared access move together."),
    5 => Some("Tip: defensive capital competes with cash reserves for access posture."),
    _ => None,
  }
}

fn guidance_has_no_outcome_spoilers(text: &str) -> bool {
  let lower = text.to_ascii_lowercase();
  ![
    "reject",
    "counter",
    "grant flexibility",
    "work action",
    "full partnership",
    "accelerate",
    "partialretreat",
    "state hash",
  ]
  .iter()
  .any(|token| lower.contains(token))
}

#[cfg(test)]
mod tests {
  use super::*;

  #[test]
  fn help_text_avoids_actor_outcome_spoilers() {
    for context in [
      PromptContext::ResumeChoice,
      PromptContext::PlayMode,
      PromptContext::Seed,
      PromptContext::TurnCommand { turn: 1 },
      PromptContext::BeginnerTurn { turn: 2 },
      PromptContext::ReplayExport,
    ] {
      let text = context_help_lines(context).join("\n");
      assert!(
        guidance_has_no_outcome_spoilers(&text),
        "help for {context:?} leaked spoilers"
      );
    }
  }

  #[test]
  fn turn_hints_avoid_actor_outcome_spoilers() {
    for turn in 1..=5 {
      if let Some(hint) = turn_hint(turn) {
        assert!(guidance_has_no_outcome_spoilers(hint));
      }
    }
  }
}
