use crate::competitive::{genesis_competitive_world_with_ruleset, genesis_roster_lines};
use crate::model::{Difficulty, PlayerController, PlayerResources, default_competitive_ruleset};

use super::genesis_competitive_world;

#[test]
fn genesis_system_count_matches_difficulty_k_plus_one() {
  for difficulty in [
    Difficulty::Easy,
    Difficulty::Normal,
    Difficulty::Hard,
    Difficulty::Expert,
  ] {
    let world = genesis_competitive_world(difficulty);
    assert_eq!(
      world.systems.len(),
      (difficulty.k_rivals() + 1) as usize,
      "{difficulty:?}"
    );
    assert_eq!(world.players.len(), world.systems.len());
  }
}

#[test]
fn genesis_assigns_human_to_system_zero_and_ai_to_rivals() {
  let world = genesis_competitive_world(Difficulty::Hard);
  assert!(matches!(
    world.players[0].controller,
    PlayerController::Human
  ));
  assert_eq!(world.systems[0].name, "Riverside Community Health");

  for slot in &world.players[1..] {
    assert!(matches!(slot.controller, PlayerController::Ai(_)));
    assert_ne!(slot.system_id, 0);
  }
}

#[test]
fn genesis_is_deterministic_for_same_difficulty() {
  let first = genesis_competitive_world(Difficulty::Normal);
  let second = genesis_competitive_world(Difficulty::Normal);
  assert_eq!(first, second);
}

#[test]
fn genesis_human_resources_match_ruleset_defaults() {
  let ruleset = default_competitive_ruleset();
  let world = genesis_competitive_world_with_ruleset(Difficulty::Normal, &ruleset);
  let human = world.systems.first().expect("human system");
  assert_eq!(
    human.resources,
    PlayerResources::genesis(Difficulty::Normal, &ruleset)
  );
}

#[test]
fn genesis_ai_resources_use_cpu_ap_budget() {
  let world = genesis_competitive_world(Difficulty::Expert);
  let cpu_ap = Difficulty::Expert.cpu_ap_per_month();
  for system in world.systems.iter().skip(1) {
    assert_eq!(system.resources.ap_budget, cpu_ap);
  }
}

#[test]
fn genesis_roster_lines_include_all_systems() {
  let world = genesis_competitive_world(Difficulty::Normal);
  let lines = genesis_roster_lines(&world);
  assert_eq!(lines.len(), 3);
  assert!(lines[0].contains("Riverside Community Health"));
  assert!(lines[0].contains("human player"));
  assert!(lines[1].contains("Northlake Health"));
  assert!(lines[2].contains("Summit Care"));
}

#[test]
fn genesis_rivals_resources_scale_by_difficulty() {
  // Easy
  let easy_world = genesis_competitive_world(Difficulty::Easy);
  assert_eq!(easy_world.systems[0].resources.cash, 60); // human invariant
  assert_eq!(easy_world.systems[0].resources.political_capital, 8); // human invariant
  assert_eq!(easy_world.systems[1].resources.cash, 40); // Easy rival
  assert_eq!(easy_world.systems[1].resources.political_capital, 5); // Easy rival

  // Normal
  let normal_world = genesis_competitive_world(Difficulty::Normal);
  assert_eq!(normal_world.systems[0].resources.cash, 60);
  assert_eq!(normal_world.systems[0].resources.political_capital, 8);
  assert_eq!(normal_world.systems[1].resources.cash, 60);
  assert_eq!(normal_world.systems[1].resources.political_capital, 8);

  // Hard
  let hard_world = genesis_competitive_world(Difficulty::Hard);
  assert_eq!(hard_world.systems[0].resources.cash, 60);
  assert_eq!(hard_world.systems[0].resources.political_capital, 8);
  assert_eq!(hard_world.systems[1].resources.cash, 80);
  assert_eq!(hard_world.systems[1].resources.political_capital, 12);

  // Expert
  let expert_world = genesis_competitive_world(Difficulty::Expert);
  assert_eq!(expert_world.systems[0].resources.cash, 60);
  assert_eq!(expert_world.systems[0].resources.political_capital, 8);
  assert_eq!(expert_world.systems[1].resources.cash, 100);
  assert_eq!(expert_world.systems[1].resources.political_capital, 15);
}
