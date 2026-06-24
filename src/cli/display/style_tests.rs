use crate::cli::display::style::{error_with, section_heading_with};

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
