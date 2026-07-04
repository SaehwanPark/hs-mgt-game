#[derive(Clone, Debug, PartialEq, Eq)]
pub enum GlobalInput {
  Quit,
  Help { topic: Option<String> },
  Payload(String),
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ReadLineOutcome {
  Quit,
  Payload(String),
}

pub fn parse_global_input(raw: &str) -> GlobalInput {
  let trimmed = raw.trim();
  let lower = trimmed.to_ascii_lowercase();

  if lower == "q" || lower == "quit" || lower == "exit" {
    return GlobalInput::Quit;
  }

  if lower == "?" || lower == "help" {
    return GlobalInput::Help { topic: None };
  }

  let mut parts = trimmed.split_whitespace();
  if let Some(first) = parts.next() {
    let first_lower = first.to_ascii_lowercase();
    if first_lower == "help" || first_lower == "?" {
      let rest: Vec<&str> = parts.collect();
      if !rest.is_empty() {
        return GlobalInput::Help {
          topic: Some(rest.join(" ")),
        };
      }
    }
  }

  GlobalInput::Payload(trimmed.to_string())
}

#[cfg(test)]
mod tests {
  use super::*;

  #[test]
  fn quit_aliases_are_recognized() {
    assert_eq!(parse_global_input("q\n"), GlobalInput::Quit);
    assert_eq!(parse_global_input("QUIT\n"), GlobalInput::Quit);
    assert_eq!(parse_global_input("exit\n"), GlobalInput::Quit);
  }

  #[test]
  fn help_aliases_are_recognized() {
    assert_eq!(parse_global_input("?\n"), GlobalInput::Help { topic: None });
    assert_eq!(
      parse_global_input("help\n"),
      GlobalInput::Help { topic: None }
    );
    assert_eq!(
      parse_global_input("HELP\n"),
      GlobalInput::Help { topic: None }
    );
  }

  #[test]
  fn help_with_topics_are_recognized() {
    assert_eq!(
      parse_global_input("help recruit\n"),
      GlobalInput::Help {
        topic: Some("recruit".to_string())
      }
    );
    assert_eq!(
      parse_global_input("? invest\n"),
      GlobalInput::Help {
        topic: Some("invest".to_string())
      }
    );
    assert_eq!(
      parse_global_input("HELP\tproject\n"),
      GlobalInput::Help {
        topic: Some("project".to_string())
      }
    );
    assert_eq!(
      parse_global_input("?  hold \n"),
      GlobalInput::Help {
        topic: Some("hold".to_string())
      }
    );
  }

  #[test]
  fn non_global_input_returns_payload() {
    assert_eq!(
      parse_global_input("1 2 3\n"),
      GlobalInput::Payload("1 2 3".to_string())
    );
    assert_eq!(
      parse_global_input("\n"),
      GlobalInput::Payload(String::new())
    );
  }
}
