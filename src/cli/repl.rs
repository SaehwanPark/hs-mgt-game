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
use super::guidance::print_context_help_with_topic;
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
      GlobalInput::Help { topic } => {
        print_context_help_with_topic(PromptContext::CompetitiveCommand, topic.as_deref());
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

fn get_verb_args(verb: &str) -> Option<&'static [(&'static str, &'static [&'static str])]> {
  match verb {
    "invest" => Some(&[
      ("domain", &["beds", "outpatient", "technology", "emergency"]),
      ("amount", &[]),
    ]),
    "recruit" => Some(&[
      ("role", &["nurse", "physician", "admin"]),
      ("headcount", &[]),
    ]),
    "monitor" => Some(&[
      ("target", &["northlake", "summit", "valley", "metro"]),
      ("depth", &[]),
    ]),
    "negotiate" => Some(&[
      ("payer", &["carrier_a", "carrier_b", "medicaid", "medicare"]),
      ("rate_posture", &["aggressive", "neutral", "conservative"]),
    ]),
    "commit" => Some(&[
      ("pledge_type", &["access", "quality", "workforce"]),
      ("level", &[]),
    ]),
    "project" => Some(&[
      (
        "kind",
        &[
          "ehr_epic",
          "ehr_cerner",
          "tower",
          "clinic_network",
          "emergency_pavilion",
        ],
      ),
      ("budget", &[]),
    ]),
    _ => None,
  }
}

fn complete_verb_candidates(line: &str, pos: usize, verbs: &[String]) -> (usize, Vec<String>) {
  let cursor = pos.min(line.len());
  let head = &line[..cursor];
  let segment_start = head.rfind(';').map(|idx| idx + 1).unwrap_or(0);
  let segment = &line[segment_start..cursor];
  let trimmed_start = segment.trim_start();
  let leading_ws = segment.len() - trimmed_start.len();
  let completion_start = segment_start + leading_ws;

  if trimmed_start.is_empty() {
    return (completion_start, verbs.to_vec());
  }

  let space_idx_opt = trimmed_start.rfind(char::is_whitespace);

  match space_idx_opt {
    None => {
      let prefix = trimmed_start.to_ascii_lowercase();
      let candidates = verbs
        .iter()
        .filter(|verb| verb.starts_with(&prefix))
        .cloned()
        .collect::<Vec<_>>();
      (completion_start, candidates)
    }
    Some(space_idx) => {
      let verb_token = trimmed_start.split_whitespace().next().unwrap_or("");
      let verb = verb_token.to_ascii_lowercase();

      let Some(schema) = get_verb_args(&verb) else {
        return (cursor, Vec::new());
      };

      let ws_char = trimmed_start[space_idx..].chars().next().unwrap();
      let ws_len = ws_char.len_utf8();

      let last_word = &trimmed_start[space_idx + ws_len..];
      let word_start = completion_start + space_idx + ws_len;

      if let Some(eq_offset) = last_word.find('=') {
        let key = &last_word[..eq_offset].to_ascii_lowercase();
        let val_prefix = &last_word[eq_offset + 1..].to_ascii_lowercase();
        let replacement_start = word_start + eq_offset + 1;

        let mut candidates = Vec::new();
        for &(k, enum_vals) in schema {
          if k == key {
            for &val in enum_vals {
              if val.starts_with(val_prefix) {
                candidates.push(val.to_string());
              }
            }
          }
        }
        (replacement_start, candidates)
      } else {
        let key_prefix = last_word.to_ascii_lowercase();
        let replacement_start = word_start;

        let prior_part = &trimmed_start[..space_idx];
        let mut present_keys = std::collections::HashSet::new();
        for token in prior_part.split_whitespace() {
          if let Some((k, _)) = token.split_once('=') {
            present_keys.insert(k.to_ascii_lowercase());
          }
        }

        let mut candidates = Vec::new();
        for &(k, _) in schema {
          if !present_keys.contains(k) && k.starts_with(&key_prefix) {
            candidates.push(format!("{}=", k));
          }
        }
        (replacement_start, candidates)
      }
    }
  }
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
      "negotiate".to_string(),
      "commit".to_string(),
      "project".to_string(),
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
  fn completes_argument_keys() {
    let (start, candidates) = complete_verb_candidates("invest ", 7, &verbs());
    assert_eq!(start, 7);
    assert_eq!(
      candidates,
      vec!["domain=".to_string(), "amount=".to_string()]
    );
  }

  #[test]
  fn completes_argument_keys_excluding_present() {
    let (start, candidates) = complete_verb_candidates("invest domain=beds ", 19, &verbs());
    assert_eq!(start, 19);
    assert_eq!(candidates, vec!["amount=".to_string()]);
  }

  #[test]
  fn completes_enum_values_for_key() {
    let (start, candidates) = complete_verb_candidates("invest domain=", 14, &verbs());
    assert_eq!(start, 14);
    assert_eq!(
      candidates,
      vec![
        "beds".to_string(),
        "outpatient".to_string(),
        "technology".to_string(),
        "emergency".to_string()
      ]
    );
  }

  #[test]
  fn completes_enum_values_with_prefix() {
    let (start, candidates) = complete_verb_candidates("invest domain=ou", 16, &verbs());
    assert_eq!(start, 14);
    assert_eq!(candidates, vec!["outpatient".to_string()]);
  }

  #[test]
  fn completes_in_second_batch_command() {
    let (start, candidates) = complete_verb_candidates("hold; recruit ", 14, &verbs());
    assert_eq!(start, 14);
    assert_eq!(
      candidates,
      vec!["role=".to_string(), "headcount=".to_string()]
    );
  }

  #[test]
  fn completes_with_multibyte_space() {
    let (start, candidates) = complete_verb_candidates("invest\u{3000}", 9, &verbs());
    assert_eq!(start, 9);
    assert_eq!(
      candidates,
      vec!["domain=".to_string(), "amount=".to_string()]
    );
  }
}
