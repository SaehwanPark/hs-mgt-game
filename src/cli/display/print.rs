use std::io::{self, Write};

use super::forecast::turn_uncertainty_preview_header;
use super::style::{
  self, EMOJI_BRIEFING, EMOJI_RESOLUTION, EMOJI_UNCERTAINTY, EMOJI_WARNING, dim, section_heading,
  subsection, warning,
};

pub fn print_blank() {
  println!();
}

pub fn print_line(line: &str) {
  if line.is_empty() {
    print_blank();
    return;
  }

  println!("{line}");
}

pub fn print_lines(lines: &[String]) {
  for line in lines {
    print_line(line);
  }
}

pub fn print_block(lines: &[String]) {
  print_blank();
  print_lines(lines);
  print_blank();
}

pub fn print_prompt_block(lines: &[String]) {
  print_blank();
  print_lines(lines);
}

pub fn print_turn_uncertainty_block(turn_number: u32, lines: &[String]) {
  let mut block = vec![section_heading(
    EMOJI_UNCERTAINTY,
    &turn_uncertainty_preview_header(turn_number),
  )];
  block.extend(lines.iter().cloned());
  print_block(&block);
}

pub fn print_turn_briefing_block(turn_number: u32, lines: &[String]) {
  let mut block = vec![section_heading(
    EMOJI_BRIEFING,
    &format!("Turn {turn_number} executive briefing"),
  )];

  for line in lines {
    if line.starts_with("Turn ") {
      continue;
    }

    if line.contains("Prior access measurement revision") || line.contains("revision") {
      block.push(warning(line));
    } else {
      block.push(line.clone());
    }
  }

  print_block(&block);
}

pub fn print_turn_resolution_block(lines: &[String]) {
  let mut block = Vec::new();

  for line in lines {
    if line.starts_with("Turn ") && line.contains("resolved:") {
      block.push(section_heading(EMOJI_RESOLUTION, line.trim()));
      continue;
    }

    if line.contains("State hash:") {
      block.push(dim(line));
      continue;
    }

    block.push(line.clone());
  }

  print_block(&block);
}

pub fn print_pre_run_dashboard(lines: &[String]) {
  let mut block = Vec::new();

  for line in lines {
    if line == "Executive dashboard" {
      block.push(section_heading(
        style::EMOJI_DASHBOARD,
        "Executive dashboard",
      ));
      continue;
    }

    if line.contains("Observation note") {
      block.push(warning(&format!("{EMOJI_WARNING} {line}")));
      continue;
    }

    block.push(line.clone());
  }

  print_block(&block);
}

pub fn print_strategy_previews(lines: &[String]) {
  let mut block = vec![subsection("Strategy previews")];
  block.extend(lines.iter().map(|line| style::dim(line)));
  print_block(&block);
}

pub fn eprint_error(message: &str) {
  let _ = writeln!(io::stderr(), "{}", style::error(message));
}
