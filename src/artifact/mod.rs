mod parse;
mod serialize;
mod session_save;
mod session_save_serialize;
mod text;
mod verify;

pub use serialize::{REPLAY_ARTIFACT_VERSION, serialize_replay_artifact};
pub use session_save::{
  describe_session_save_error, deserialize_session_save, verify_session_save,
};
pub use session_save_serialize::{SESSION_SAVE_VERSION, serialize_session_save};
pub use verify::{
  describe_replay_artifact_error, deserialize_replay_artifact, verify_replay_artifact,
  write_replay_artifact,
};

#[cfg(test)]
#[path = "verify_tests.rs"]
mod verify_tests;
