use crate::model::History;

pub fn educational_debrief(history: &History) -> Vec<String> {
  let Some(last_transition) = history.transitions.last() else {
    return vec!["No committed transitions are available for debriefing.".to_string()];
  };

  let initial = &history.genesis;
  let final_state = &last_transition.next;
  let actor_rationales = history
    .transitions
    .iter()
    .map(|transition| {
      format!(
        "{}: {}",
        transition.actor_decision.actor, transition.actor_decision.rationale
      )
    })
    .collect::<Vec<_>>()
    .join(" | ");

  let effect_summary = history
    .transitions
    .iter()
    .flat_map(|transition| transition.effects.iter())
    .map(|effect| {
      format!(
        "{} changed {} by {}",
        effect.source, effect.metric, effect.delta
      )
    })
    .collect::<Vec<_>>()
    .join("; ");

  let revision_notes = history
    .transitions
    .iter()
    .filter(|transition| transition.observation.prior_access_revision != 0)
    .map(|transition| {
      format!(
        "turn {} revised the prior reported access estimate by {}",
        transition.prior.turn + 1,
        transition.observation.prior_access_revision
      )
    })
    .collect::<Vec<_>>()
    .join("; ");

  let mut lines = vec![
    format!(
      "Run-level tradeoff: cash moved from {} to {}, access from {} to {}, workforce trust from {} to {}, community trust from {} to {}, policy pressure from {} to {}, and commercial rate from {} to {}.",
      initial.cash,
      final_state.cash,
      initial.access_index,
      final_state.access_index,
      initial.workforce_trust,
      final_state.workforce_trust,
      initial.community_trust,
      final_state.community_trust,
      initial.policy_pressure,
      final_state.policy_pressure,
      initial.commercial_rate,
      final_state.commercial_rate
    ),
    format!("Actor rationales at decision time: {actor_rationales}"),
    format!("Attributed mechanisms to inspect: {effect_summary}."),
    "Debrief prompt: Was the CEO's access strategy reasonable given the reported access values, the later policy response, the workforce retention tradeoff, the coalition investment choice, and the defensive response to rival capacity pressure?".to_string(),
    "Decision quality and outcome quality are separate: replay preserves what each actor observed and why each modeled response occurred.".to_string(),
  ];

  if !revision_notes.is_empty() {
    lines.push(format!(
      "Observation revision note: {revision_notes}. Prior committed observations remain unchanged in history; revisions affect only the current briefing."
    ));
  }

  lines
}
