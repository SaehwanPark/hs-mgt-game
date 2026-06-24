#[derive(Clone, Debug, PartialEq, Eq)]
pub enum GlobalInput {
  Quit,
  Help,
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

  match lower.as_str() {
    "q" | "quit" | "exit" => GlobalInput::Quit,
    "?" | "help" => GlobalInput::Help,
    _ => GlobalInput::Payload(trimmed.to_string()),
  }
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
    assert_eq!(parse_global_input("?\n"), GlobalInput::Help);
    assert_eq!(parse_global_input("help\n"), GlobalInput::Help);
    assert_eq!(parse_global_input("HELP\n"), GlobalInput::Help);
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
