use std::io::{self, IsTerminal};

use rustyline::completion::{Completer, Pair};
use rustyline::error::ReadlineError;
use rustyline::highlight::Highlighter;
use rustyline::hint::Hinter;
use rustyline::validate::Validator;
use rustyline::{Config, Context, Editor, Helper};

use crate::model::CliError;

use super::competitive_parse::competitive_command_verbs;
use super::display::{PromptContext, print_line, print_prompt_block, style};
use super::guidance::print_context_help;
use super::input::{GlobalInput, ReadLineOutcome, parse_global_input};
use super::io::stdin_uses_fallback_input;

#[derive(Clone, Debug)]
struct CompetitiveVerbCompleter {
  verbs: Vec<String>,
}

impl Helper for CompetitiveVerbCompleter {}
impl Hinter for CompetitiveVerbCompleter {
  type Hint = String;
}
impl Highlighter for CompetitiveVerbCompleter {}
impl Validator for CompetitiveVerbCompleter {}

impl Completer for CompetitiveVerbCompleter {
  type Candidate = Pair;

  fn complete(
    &self,
    line: &str,
    pos: usize,
    _ctx: &Context<'_>,
  ) -> Result<(usize, Vec<Pair>), ReadlineError> {
    let (start, candidates) = complete_verb_candidates(line, pos, &self.verbs);
    let pairs = candidates
      .into_iter()
      .map(|candidate| Pair {
        display: candidate.clone(),
        replacement: candidate,
      })
      .collect::<Vec<_>>();
    Ok((start, pairs))
  }
}

pub fn read_competitive_command_line(prompt_lines: &[String]) -> Result<ReadLineOutcome, CliError> {
  loop {
    print_prompt_block(prompt_lines);
    let input = read_line()?;

    match parse_global_input(&input) {
      GlobalInput::Quit => return Ok(ReadLineOutcome::Quit),
      GlobalInput::Help => {
        print_context_help(PromptContext::CompetitiveCommand);
      }
      GlobalInput::Payload(payload) => return Ok(ReadLineOutcome::Payload(payload)),
    }
  }
}

fn read_line() -> Result<String, CliError> {
  if io::stdin().is_terminal() && !stdin_uses_fallback_input() {
    return match read_line_with_completion() {
      Ok(line) => Ok(line),
      Err(ReadlineError::Interrupted | ReadlineError::Eof) => Ok("quit".to_string()),
      Err(_) => read_line_from_stdin(),
    };
  }

  read_line_from_stdin()
}

fn read_line_with_completion() -> Result<String, ReadlineError> {
  let helper = CompetitiveVerbCompleter {
    verbs: competitive_command_verbs()
      .into_iter()
      .map(str::to_string)
      .collect(),
  };
  let config = Config::builder().auto_add_history(false).build();
  let mut editor = Editor::with_config(config)?;
  editor.set_helper(Some(helper));

  // Keep prompt color in display output to avoid terminal cursor width issues.
  print_line(&format!(
    "  {}",
    style::command_prompt_label(
      "riverside> (Type ? or help for detailed command descriptions, Tab: complete command verbs)"
    )
  ));
  editor.readline("> ")
}

fn read_line_from_stdin() -> Result<String, CliError> {
  let mut input = String::new();
  io::stdin()
    .read_line(&mut input)
    .map_err(|_| CliError::InputUnavailable)?;
  Ok(input)
}

fn complete_verb_candidates(line: &str, pos: usize, verbs: &[String]) -> (usize, Vec<String>) {
  let cursor = pos.min(line.len());
  let head = &line[..cursor];
  let segment_start = head.rfind(';').map(|idx| idx + 1).unwrap_or(0);
  let segment = &line[segment_start..cursor];
  let trimmed_start = segment.trim_start();
  let leading_ws = segment.len() - trimmed_start.len();
  let completion_start = segment_start + leading_ws;

  if trimmed_start.contains(char::is_whitespace) {
    return (cursor, Vec::new());
  }

  let prefix = trimmed_start.to_ascii_lowercase();
  let candidates = verbs
    .iter()
    .filter(|verb| verb.starts_with(&prefix))
    .cloned()
    .collect::<Vec<_>>();
  (completion_start, candidates)
}

#[cfg(test)]
mod tests {
  use super::complete_verb_candidates;

  fn verbs() -> Vec<String> {
    vec![
      "hold".to_string(),
      "invest".to_string(),
      "recruit".to_string(),
      "monitor".to_string(),
    ]
  }

  #[test]
  fn completes_from_empty_segment() {
    let (start, candidates) = complete_verb_candidates("", 0, &verbs());
    assert_eq!(start, 0);
    assert!(candidates.contains(&"hold".to_string()));
    assert!(candidates.contains(&"invest".to_string()));
  }

  #[test]
  fn completes_from_prefix() {
    let (start, candidates) = complete_verb_candidates("inv", 3, &verbs());
    assert_eq!(start, 0);
    assert_eq!(candidates, vec!["invest".to_string()]);
  }

  #[test]
  fn only_completes_after_last_semicolon() {
    let (start, candidates) = complete_verb_candidates("hold; rec", 9, &verbs());
    assert_eq!(start, 6);
    assert_eq!(candidates, vec!["recruit".to_string()]);
  }

  #[test]
  fn does_not_complete_argument_position() {
    let (start, candidates) = complete_verb_candidates("invest domain=", 14, &verbs());
    assert_eq!(start, 14);
    assert!(candidates.is_empty());
  }
}
