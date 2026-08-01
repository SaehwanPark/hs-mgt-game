mod counterfactual;
mod report;

pub use counterfactual::counterfactual_difference_lines;
pub use report::{
  affiliation_debrief, competitive_debrief, competitive_distributional_summary,
  competitive_end_session_debrief, competitive_instructor_summary, competitive_player_debrief,
  educational_debrief, instructor_run_summary,
};

#[cfg(test)]
#[path = "counterfactual_tests.rs"]
mod counterfactual_tests;
#[cfg(test)]
#[path = "report_tests.rs"]
mod report_tests;
