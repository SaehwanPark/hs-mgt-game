use crate::model::ReplayArtifactError;

pub fn escape_artifact_text(value: &str) -> String {
  let mut escaped = String::with_capacity(value.len());

  for ch in value.chars() {
    match ch {
      '\\' => escaped.push_str("\\\\"),
      '"' => escaped.push_str("\\\""),
      '\n' => escaped.push_str("\\n"),
      '\r' => escaped.push_str("\\r"),
      other => escaped.push(other),
    }
  }

  escaped
}

pub fn unescape_artifact_text(value: &str) -> Result<String, ReplayArtifactError> {
  let mut unescaped = String::with_capacity(value.len());
  let mut chars = value.chars();

  while let Some(ch) = chars.next() {
    if ch != '\\' {
      unescaped.push(ch);
      continue;
    }

    match chars.next() {
      Some('\\') => unescaped.push('\\'),
      Some('"') => unescaped.push('"'),
      Some('n') => unescaped.push('\n'),
      Some('r') => unescaped.push('\r'),
      Some(other) => {
        return Err(ReplayArtifactError::ParseError {
          line: 0,
          detail: format!("invalid escape sequence \\{other}"),
        });
      }
      None => {
        return Err(ReplayArtifactError::ParseError {
          line: 0,
          detail: "trailing escape in artifact text".to_string(),
        });
      }
    }
  }

  Ok(unescaped)
}
