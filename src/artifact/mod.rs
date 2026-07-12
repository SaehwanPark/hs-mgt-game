mod affiliation;
mod competitive_session_save;
mod parse;
mod serialize;
mod session_save;
mod session_save_serialize;
mod text;
mod verify;

pub use affiliation::{
  deserialize_affiliation_replay, serialize_affiliation_replay, verify_affiliation_replay,
};
pub use competitive_session_save::{
  deserialize_competitive_session_save, serialize_competitive_session_save,
};
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
#[path = "affiliation_tests.rs"]
mod affiliation_tests;
#[cfg(test)]
#[path = "verify_tests.rs"]
mod verify_tests;
