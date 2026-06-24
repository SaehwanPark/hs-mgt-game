use hs_mgt_game::cli::{describe_cli_error, eprint_error, run};

fn main() {
  match run() {
    Ok(()) => {}
    Err(error) => {
      eprint_error(&format!(
        "Unable to run demo: {}",
        describe_cli_error(&error)
      ));
      std::process::exit(1);
    }
  }
}
