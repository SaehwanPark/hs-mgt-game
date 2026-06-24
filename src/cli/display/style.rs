use std::env;
use std::io::{self, IsTerminal};

pub const EMOJI_DASHBOARD: &str = "📊";
pub const EMOJI_STRATEGY: &str = "🎯";
pub const EMOJI_UNCERTAINTY: &str = "🔮";
pub const EMOJI_BRIEFING: &str = "📋";
pub const EMOJI_RESOLUTION: &str = "⚡";
pub const EMOJI_DEBRIEF: &str = "🎓";
pub const EMOJI_EXPORT: &str = "💾";
pub const EMOJI_SUCCESS: &str = "✅";
pub const EMOJI_WARNING: &str = "⚠️";

const BOLD: &str = "\x1b[1m";
const DIM: &str = "\x1b[2m";
const RESET: &str = "\x1b[0m";
const CYAN: &str = "\x1b[36m";
const GREEN: &str = "\x1b[32m";
const YELLOW: &str = "\x1b[33m";
const RED: &str = "\x1b[31m";

pub fn styling_enabled() -> bool {
  stream_styling_enabled(io::stdout().is_terminal())
}

fn stderr_styling_enabled() -> bool {
  stream_styling_enabled(io::stderr().is_terminal())
}

fn stream_styling_enabled(is_terminal: bool) -> bool {
  env::var_os("NO_COLOR").is_none() && is_terminal
}

pub fn section_heading(emoji: &str, text: &str) -> String {
  wrap_styled(
    styling_enabled(),
    &format!("{emoji} {text}"),
    &format!("{BOLD}{CYAN}{emoji} {text}{RESET}"),
  )
}

pub fn subsection(text: &str) -> String {
  wrap_styled(styling_enabled(), text, &format!("{BOLD}{text}{RESET}"))
}

pub fn label_value(label: &str, value: &str) -> String {
  if styling_enabled() {
    format!("{DIM}{label}:{RESET} {value}")
  } else {
    format!("{label}: {value}")
  }
}

pub fn dim(text: &str) -> String {
  wrap_styled(styling_enabled(), text, &format!("{DIM}{text}{RESET}"))
}

pub fn success(text: &str) -> String {
  wrap_styled(styling_enabled(), text, &format!("{GREEN}{text}{RESET}"))
}

pub fn warning(text: &str) -> String {
  wrap_styled(styling_enabled(), text, &format!("{YELLOW}{text}{RESET}"))
}

pub fn error(text: &str) -> String {
  wrap_styled(
    stderr_styling_enabled(),
    text,
    &format!("{RED}{text}{RESET}"),
  )
}

pub fn accent(text: &str) -> String {
  wrap_styled(styling_enabled(), text, &format!("{CYAN}{text}{RESET}"))
}

pub fn option_line(number: &str, label: &str, detail: &str) -> String {
  if styling_enabled() {
    format!(
      "  {BOLD}{number}.{RESET} {}: {}",
      accent(label),
      dim(detail)
    )
  } else {
    format!("  {number}. {label}: {detail}")
  }
}

pub(crate) fn wrap_styled(enabled: bool, plain: &str, styled: &str) -> String {
  if enabled {
    styled.to_string()
  } else {
    plain.to_string()
  }
}

#[cfg(test)]
pub(crate) fn section_heading_with(enabled: bool, emoji: &str, text: &str) -> String {
  wrap_styled(
    enabled,
    &format!("{emoji} {text}"),
    &format!("{BOLD}{CYAN}{emoji} {text}{RESET}"),
  )
}

#[cfg(test)]
pub(crate) fn error_with(enabled: bool, text: &str) -> String {
  wrap_styled(enabled, text, &format!("{RED}{text}{RESET}"))
}
