use hs_mgt_game::cli::{describe_cli_error, eprint_error, run};
use hs_mgt_game::model::SessionOutcome;

fn main() {
  match run() {
    Ok(SessionOutcome::Completed)
    | Ok(SessionOutcome::CompetitivePreview)
    | Ok(SessionOutcome::QuitSaved)
    | Ok(SessionOutcome::QuitNoSave) => {}
    Err(error) => {
      eprint_error(&format!(
        "Unable to run demo: {}",
        describe_cli_error(&error)
      ));
      std::process::exit(1);
    }
  }
}
