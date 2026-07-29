use std::collections::BTreeMap;

use crate::model::{History, WorldState};

type MetricReader = (&'static str, fn(&WorldState) -> i32);

const METRICS: [MetricReader; 9] = [
  ("cash", |state| state.cash),
  ("staffed_beds", |state| state.staffed_beds),
  ("access_index", |state| state.access_index),
  ("quality_index", |state| state.quality_index),
  ("workforce_trust", |state| state.workforce_trust),
  ("community_trust", |state| state.community_trust),
  ("commercial_rate", |state| state.commercial_rate),
  ("policy_pressure", |state| state.policy_pressure),
  ("turn", |state| state.turn as i32),
];

/// Render a descriptive, text-first comparison of two committed histories.
///
/// The comparison is intentionally not a causal model: it reports committed
/// differences and whether the recorded resolved inputs match, without
/// recalculating either history or ranking the commands.
pub fn counterfactual_difference_lines(baseline: &History, alternative: &History) -> Vec<String> {
  let mut lines = vec![
    "=== COUNTERFACTUAL DIFFERENCE VIEW ===".to_string(),
    "Differences are descriptive comparisons of committed runs; they do not establish causal certainty or strategy value.".to_string(),
  ];

  if baseline.genesis != alternative.genesis {
    lines.push("Cannot compare: baseline and alternative genesis states differ.".to_string());
    lines.push(
      "Written fallback: provide histories created from the same starting state.".to_string(),
    );
    return lines;
  }

  lines.push("Genesis parity: same starting state.".to_string());
  let aligned_count = baseline
    .transitions
    .len()
    .min(alternative.transitions.len());
  if baseline.transitions.len() != alternative.transitions.len() {
    lines.push(format!(
      "Alignment: limited to {aligned_count} turn(s); baseline has {}, alternative has {}.",
      baseline.transitions.len(),
      alternative.transitions.len()
    ));
  } else {
    lines.push(format!(
      "Alignment: {} turn(s).",
      baseline.transitions.len()
    ));
  }

  let resolved_inputs_match = baseline
    .transitions
    .iter()
    .zip(alternative.transitions.iter())
    .all(|(left, right)| left.resolved_inputs == right.resolved_inputs);
  lines.push(format!(
    "Resolved-input parity: {}.",
    if resolved_inputs_match {
      "same recorded inputs"
    } else {
      "different recorded inputs; do not treat differences as a counterfactual attribution"
    }
  ));

  if aligned_count == 0 {
    lines.push("No aligned committed turns are available.".to_string());
    return lines;
  }

  let mut difference_count = 0;
  for (baseline_transition, alternative_transition) in baseline
    .transitions
    .iter()
    .zip(alternative.transitions.iter())
    .take(aligned_count)
  {
    if baseline_transition.next.turn != alternative_transition.next.turn {
      lines.push(format!(
        "Turn alignment mismatch: baseline next turn {}, alternative next turn {}.",
        baseline_transition.next.turn, alternative_transition.next.turn
      ));
      continue;
    }

    lines.push(format!("--- Turn {} ---", baseline_transition.next.turn));
    lines.push(format!(
      "Baseline command: {:?}",
      baseline_transition.command
    ));
    lines.push(format!(
      "Alternative command: {:?}",
      alternative_transition.command
    ));

    let state_start = lines.len();
    for (metric, read) in METRICS {
      let baseline_value = read(&baseline_transition.next);
      let alternative_value = read(&alternative_transition.next);
      if baseline_value != alternative_value {
        difference_count += 1;
        lines.push(format!(
          "Committed state difference: {metric} {baseline_value} → {alternative_value} ({:+}).",
          alternative_value - baseline_value
        ));
      }
    }
    if lines.len() == state_start {
      lines.push("Committed state difference: none.".to_string());
    }

    let mut effects = BTreeMap::new();
    for effect in &baseline_transition.effects {
      *effects.entry((effect.source, effect.metric)).or_insert(0) -= effect.delta;
    }
    for effect in &alternative_transition.effects {
      *effects.entry((effect.source, effect.metric)).or_insert(0) += effect.delta;
    }
    effects.retain(|_, delta| *delta != 0);
    if effects.is_empty() {
      lines.push("Attributed effect difference: none.".to_string());
    } else {
      for ((source, metric), delta) in effects {
        difference_count += 1;
        lines.push(format!(
          "Attributed effect difference: {source} / {metric} ({delta:+})."
        ));
      }
    }
  }

  lines.push(format!(
    "Comparison summary: {difference_count} committed difference(s) shown; no option is marked correct."
  ));
  lines
}
