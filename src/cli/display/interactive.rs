use crate::debrief::educational_debrief;
use crate::model::{History, Ruleset};
use crate::replay::replay;

use super::print::{print_block, print_line};
use super::style::{
  self, EMOJI_DEBRIEF, EMOJI_SUCCESS, dim, label_value, section_heading, success,
};

pub fn print_interactive_results(seed: u64, history: &History, ruleset: &Ruleset) {
  let replayed = replay(history, ruleset).expect("interactive history should replay");
  let replay_matches = history
    .transitions
    .last()
    .is_some_and(|transition| replayed.final_state == transition.next);

  let mut lines = vec![
    section_heading(style::EMOJI_STRATEGY, "Interactive session complete"),
    label_value("Ruleset", ruleset.version),
    label_value("Run seed", &seed.to_string()),
  ];

  if replay_matches {
    lines.push(success(&format!(
      "{EMOJI_SUCCESS} Replay final state matches committed state"
    )));
  } else {
    lines.push(label_value(
      "Replay final state matches committed state",
      "false",
    ));
  }

  lines.push(section_heading(EMOJI_DEBRIEF, "Educational debrief"));
  for line in educational_debrief(history) {
    lines.push(format!("  - {line}"));
  }

  print_block(&lines);
}

pub fn print_demo_styled_header(seed: u64, ruleset_version: &str) {
  print_block(&[
    section_heading(style::EMOJI_STRATEGY, "Deterministic demo"),
    label_value("Ruleset", ruleset_version),
    label_value("Run seed", &seed.to_string()),
  ]);
}

pub fn print_demo_turn_separator() {
  print_line(&dim("────────────────────────────────────────"));
}

pub fn print_demo_actor_decision(actor: &str, decision: &str, rationale: &str) {
  print_line(&label_value(actor, &format!("{decision} ({rationale})")));
}

pub fn print_demo_event(actor: &str, description: &str) {
  print_line(&format!("  - {}: {}", dim(actor), description));
}

pub fn print_demo_effect(source: &str, metric: &str, delta: i32) {
  print_line(&format!(
    "  - {} changed {} by {}",
    dim(source),
    metric,
    delta
  ));
}

pub fn print_demo_replay_footer(replay_matches: bool) {
  if replay_matches {
    print_line(&success(&format!(
      "{EMOJI_SUCCESS} Replay final state matches committed state"
    )));
  } else {
    print_line(&label_value(
      "Replay final state matches committed state",
      "false",
    ));
  }
}

pub fn print_demo_debrief(history: &History) {
  let mut lines = vec![section_heading(EMOJI_DEBRIEF, "Educational debrief")];
  for line in educational_debrief(history) {
    lines.push(format!("  - {line}"));
  }
  print_block(&lines);
}
