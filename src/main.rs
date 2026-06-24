use hs_mgt_game::cli::{describe_cli_error, run};

fn main() {
  match run() {
    Ok(()) => {}
    Err(error) => {
      eprintln!("Unable to run demo: {}", describe_cli_error(&error));
      std::process::exit(1);
    }
  }
}
