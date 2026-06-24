use std::io;

use crate::artifact::{describe_replay_artifact_error, write_replay_artifact};
use crate::inputs::resolve_inputs;
use crate::model::{
  CliError, History, PlayMode, PlayerCommand, ReplayArtifact, Ruleset, RunConfig, default_ruleset,
  genesis_state,
};
use crate::sim::{observe_for_player, transition};

use super::display::{
  print_interactive_results, print_pre_run_briefing, turn_executive_briefing,
  turn_resolution_summary,
};
use super::export::read_replay_export_path;
use super::io::{read_command_line, read_play_mode_choice, read_seed_choice};
use super::output::print_demo;
use super::parse::{
  describe_command_defaults, parse_coalition_command, parse_policy_command,
  parse_stabilize_access_command, parse_workforce_command,
};
use super::strategy::{build_history_for_strategy, default_interactive_commands, strategy_plan};

pub fn run() -> Result<(), CliError> {
  let ruleset = default_ruleset();
  read_run_config().and_then(|config| run_session(config, &ruleset))
}

pub fn read_run_config() -> Result<RunConfig, CliError> {
  print_pre_run_briefing(&genesis_state());
  let play_mode = read_play_mode_choice()?;
  let seed = read_seed_choice()?;
  Ok(RunConfig { seed, play_mode })
}
pub fn run_session(config: RunConfig, ruleset: &Ruleset) -> Result<(), CliError> {
  let history = match config.play_mode {
    PlayMode::Preset(strategy) => {
      println!("Selected preset: {}", strategy_plan(strategy).name);
      build_history_for_strategy(strategy, config.seed, ruleset)
        .map_err(CliError::InvalidStrategyPlan)?
    }
    PlayMode::Interactive => {
      println!("Selected play mode: Interactive");
      run_interactive_history(config.seed, ruleset)?
    }
  };

  match config.play_mode {
    PlayMode::Preset(_) => print_demo(config.seed, &history, ruleset),
    PlayMode::Interactive => print_interactive_results(config.seed, &history, ruleset),
  }

  if std::io::IsTerminal::is_terminal(&io::stdin()) {
    if let Some(path) = read_replay_export_path()? {
      let artifact = ReplayArtifact {
        seed: config.seed,
        play_mode: config.play_mode,
        ruleset_version: ruleset.version.to_string(),
        history,
      };

      match write_replay_artifact(&path, &artifact) {
        Ok(()) => println!("Replay artifact written to {path}"),
        Err(error) => eprintln!(
          "Replay export failed: {}",
          describe_replay_artifact_error(&error)
        ),
      }
    }
  }

  Ok(())
}
pub fn run_interactive_history(seed: u64, ruleset: &Ruleset) -> Result<History, CliError> {
  let genesis = genesis_state();
  let mut state = genesis.clone();
  let mut transitions = Vec::new();
  let defaults = default_interactive_commands();

  let turn_readers: [(&str, fn(&str) -> Result<PlayerCommand, CliError>); 4] = [
    (
      "Turn 1 command (capacity and payer posture): staffed_beds capital_spend requested_rate",
      parse_stabilize_access_command,
    ),
    (
      "Turn 2 command (state access mandate): advocacy_spend access_commitment",
      parse_policy_command,
    ),
    (
      "Turn 3 command (workforce pressure): retention_spend schedule_relief",
      parse_workforce_command,
    ),
    (
      "Turn 4 command (regional access coalition): coalition_investment shared_access_commitment",
      parse_coalition_command,
    ),
  ];

  for (turn_index, (prompt, parse_command)) in turn_readers.iter().enumerate() {
    let turn_number = turn_index as u32 + 1;
    let default_hint = describe_command_defaults(&defaults[turn_index]);
    let inputs = resolve_inputs(seed, &state, ruleset);
    let observation = observe_for_player(&state, &inputs);

    for line in turn_executive_briefing(&state, &observation, turn_number) {
      println!("{line}");
    }

    let command = parse_command(&read_command_line(&format!("{prompt}\n  {default_hint}"))?)?;
    let transition =
      transition(&state, command, inputs, ruleset).map_err(CliError::InvalidInteractiveCommand)?;

    for line in turn_resolution_summary(&transition) {
      println!("{line}");
    }

    state = transition.next.clone();
    transitions.push(transition);
  }

  Ok(History {
    genesis,
    transitions,
  })
}
