mod parse;
mod serialize;
mod text;
mod verify;

pub use serialize::{REPLAY_ARTIFACT_VERSION, serialize_replay_artifact};
pub use verify::{
  describe_replay_artifact_error, deserialize_replay_artifact, verify_replay_artifact,
  write_replay_artifact,
};

#[cfg(test)]
#[path = "verify_tests.rs"]
mod verify_tests;
