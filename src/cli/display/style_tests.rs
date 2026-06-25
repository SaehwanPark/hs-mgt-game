use crate::cli::display::style::{
  argument_token_with, command_token_with, error_with, section_heading_with,
};

#[test]
fn styled_helpers_return_plain_text_when_disabled() {
  assert_eq!(
    section_heading_with(false, "📊", "Dashboard"),
    "📊 Dashboard"
  );
  assert!(!section_heading_with(false, "📊", "Dashboard").contains("\x1b["));
  assert_eq!(error_with(false, "failed"), "failed");
}

#[test]
fn styled_helpers_include_ansi_when_enabled() {
  let heading = section_heading_with(true, "📊", "Dashboard");
  assert!(heading.contains("\x1b["));
  assert!(heading.contains("Dashboard"));

  let err = error_with(true, "failed");
  assert!(err.contains("\x1b["));
  assert!(err.contains("failed"));
}

#[test]
fn command_and_argument_tokens_support_plain_and_ansi_modes() {
  assert_eq!(command_token_with(false, "invest"), "invest");
  assert_eq!(argument_token_with(false, "domain=beds"), "domain=beds");

  let command = command_token_with(true, "invest");
  assert!(command.contains("\x1b["));
  assert!(command.contains("invest"));

  let argument = argument_token_with(true, "domain=beds");
  assert!(argument.contains("\x1b["));
  assert!(argument.contains("domain=beds"));
}
