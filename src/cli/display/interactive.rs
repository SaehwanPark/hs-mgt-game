use crate::debrief::educational_debrief;
use crate::model::{History, Ruleset};
use crate::replay::replay;
pub fn print_interactive_results(seed: u64, history: &History, ruleset: &Ruleset) {
  let replayed = replay(history, ruleset).expect("interactive history should replay");

  println!("Health Policy Strategy Game interactive session complete");
  println!("Ruleset: {}", ruleset.version);
  println!("Run seed: {seed}");
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
