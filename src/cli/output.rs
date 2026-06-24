use crate::actors::describe_actor_decision;
use crate::debrief::educational_debrief;
use crate::model::{History, Ruleset};
use crate::replay::replay;

pub fn print_demo(seed: u64, history: &History, ruleset: &Ruleset) {
  let replayed = replay(history, ruleset).expect("demo history should replay");

  println!("Health Policy Strategy Game deterministic demo");
  println!("Ruleset: {}", ruleset.version);
  println!("Run seed: {seed}");
  for transition in &history.transitions {
    println!(
      "Turn: {} -> {}",
      transition.prior.turn, transition.next.turn
    );
    println!(
      "Resolved inputs: measurement_noise {}, delayed_access_report {}, labor_sick_call_delta {}, policy_signal {}, coalition_leverage_signal {}, access_measurement_revision {}",
      transition.resolved_inputs.measurement_noise,
      transition.resolved_inputs.delayed_access_report,
      transition.resolved_inputs.labor_sick_call_delta,
      transition.resolved_inputs.policy_signal,
      transition.resolved_inputs.coalition_leverage_signal,
      transition.resolved_inputs.access_measurement_revision
    );
    println!(
      "CEO observation: access {}, quality {}, prior access revision {}, policy briefing: {}",
      transition.observation.reported_access_index,
      transition.observation.reported_quality_index,
      transition.observation.prior_access_revision,
      transition.observation.policy_briefing
    );
    println!(
      "{} decision: {} ({})",
      transition.actor_decision.actor,
      describe_actor_decision(&transition.actor_decision.decision),
      transition.actor_decision.rationale
    );
    println!("Events:");
    for event in &transition.events {
      println!("  - {}: {}", event.actor, event.description);
    }
    println!("Effects:");
    for effect in &transition.effects {
      println!(
        "  - {} changed {} by {}",
        effect.source, effect.metric, effect.delta
      );
    }
    println!("Next state hash: {}", transition.state_hash);
  }
  println!(
    "Replay final state matches committed state: {}",
    history
      .transitions
      .last()
      .is_some_and(|transition| replayed.final_state == transition.next)
  );
  println!("Educational debrief:");
  for line in educational_debrief(history) {
    println!("  - {line}");
  }
}
