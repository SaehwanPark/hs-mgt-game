use crate::actors::describe_actor_decision;
use crate::model::{History, Ruleset};
use crate::replay::replay;

use super::display::{
  print_demo_actor_decision, print_demo_debrief, print_demo_effect, print_demo_event,
  print_demo_replay_footer, print_demo_styled_header, print_demo_turn_separator, print_line, style,
};

pub fn print_demo(seed: u64, history: &History, ruleset: &Ruleset) {
  let replayed = replay(history, ruleset).expect("demo history should replay");

  print_demo_styled_header(seed, ruleset.version);

  for transition in &history.transitions {
    print_demo_turn_separator();
    print_line(&style::subsection(&format!(
      "Turn {} → {}",
      transition.prior.turn, transition.next.turn
    )));
    print_line(&style::label_value(
      "Resolved inputs",
      &format!(
        "measurement_noise {}, delayed_access_report {}, labor_sick_call_delta {}, policy_signal {}, coalition_leverage_signal {}, access_measurement_revision {}",
        transition.resolved_inputs.measurement_noise,
        transition.resolved_inputs.delayed_access_report,
        transition.resolved_inputs.labor_sick_call_delta,
        transition.resolved_inputs.policy_signal,
        transition.resolved_inputs.coalition_leverage_signal,
        transition.resolved_inputs.access_measurement_revision
      ),
    ));
    print_line(&style::label_value(
      "CEO observation",
      &format!(
        "access {}, quality {}, prior access revision {}, policy briefing: {}",
        transition.observation.reported_access_index,
        transition.observation.reported_quality_index,
        transition.observation.prior_access_revision,
        transition.observation.policy_briefing
      ),
    ));
    print_demo_actor_decision(
      transition.actor_decision.actor,
      &describe_actor_decision(&transition.actor_decision.decision),
      &transition.actor_decision.rationale,
    );
    print_line(&style::subsection("Events"));
    for event in &transition.events {
      print_demo_event(event.actor, &event.description);
    }
    print_line(&style::subsection("Effects"));
    for effect in &transition.effects {
      print_demo_effect(effect.source, effect.metric, effect.delta);
    }
    print_line(&style::dim(&format!(
      "Next state hash: {}",
      transition.state_hash
    )));
  }

  let replay_matches = history
    .transitions
    .last()
    .is_some_and(|transition| replayed.final_state == transition.next);
  print_demo_replay_footer(replay_matches);
  print_demo_debrief(history);
}
