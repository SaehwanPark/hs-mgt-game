mod report;

pub use report::{
  affiliation_debrief, competitive_debrief, competitive_instructor_summary, educational_debrief,
  instructor_run_summary,
};

#[cfg(test)]
#[path = "report_tests.rs"]
mod report_tests;
