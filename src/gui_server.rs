use std::net::SocketAddr;
use std::sync::{Arc, Mutex};

use axum::extract::{Path, Query, State};
use axum::http::{StatusCode, Uri, header};
use axum::response::{IntoResponse, Response};
use axum::routing::{get, post};
use axum::{Json, Router};
use serde::Deserialize;

use crate::mcp::{
  EndSessionRequest, GameSessionStore, GetActionCatalogRequest, GetHistoryRequest,
  GetPresentationRequest, GetRegionalWorldRequest, GetReplayRequest, GetResolutionRequest,
  LoadSessionRequest, McpErrorMessage, SaveSessionRequest, StartSessionRequest, SubmitTurnRequest,
  ValidateTurnRequest,
};

const DEFAULT_BIND: &str = "127.0.0.1:7878";
const HOST_ADAPTER_MARKER: &str = "<!-- HS_MGT_GAME_HOST_ADAPTER -->";

#[derive(Clone, Default)]
struct GuiState {
  store: Arc<Mutex<GameSessionStore>>,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct GuiStartSessionRequest {
  campaign: String,
  seed: Option<u64>,
  difficulty: Option<String>,
}

#[derive(Debug, Deserialize)]
struct CommandBody {
  command_text: String,
}

#[derive(Debug, Default, Deserialize)]
struct ResolutionQuery {
  turn: Option<u32>,
}

pub fn parse_bind_args(args: impl IntoIterator<Item = String>) -> Result<SocketAddr, String> {
  let mut args = args.into_iter();
  let _program = args.next();
  let mut bind = DEFAULT_BIND.to_string();
  while let Some(argument) = args.next() {
    match argument.as_str() {
      "--bind" => {
        bind = args
          .next()
          .ok_or_else(|| "--bind requires a loopback IP address and port".to_string())?;
      }
      "--help" | "-h" => {
        return Err(format!("usage: hs-mgt-game-gui [--bind {DEFAULT_BIND}]"));
      }
      _ => return Err(format!("unknown argument: {argument}")),
    }
  }
  let address = bind
    .parse::<SocketAddr>()
    .map_err(|error| format!("invalid bind address '{bind}': {error}"))?;
  ensure_loopback(address)?;
  Ok(address)
}

fn ensure_loopback(address: SocketAddr) -> Result<(), String> {
  if address.ip().is_loopback() {
    Ok(())
  } else {
    Err(format!(
      "GUI host must bind to a loopback address, not {}",
      address.ip()
    ))
  }
}

pub async fn run_gui_server(address: SocketAddr) -> Result<(), Box<dyn std::error::Error>> {
  ensure_loopback(address).map_err(std::io::Error::other)?;
  let listener = tokio::net::TcpListener::bind(address).await?;
  let local = listener.local_addr()?;
  println!("Health Policy Strategy Game GUI: http://{local}");
  println!("Keep this terminal running. Press Ctrl-C to stop; sessions are held in memory.");
  axum::serve(listener, gui_router())
    .with_graceful_shutdown(shutdown_signal())
    .await?;
  Ok(())
}

async fn shutdown_signal() {
  let _ = tokio::signal::ctrl_c().await;
}

fn gui_router() -> Router {
  Router::new()
    .route("/api/v1/sessions", post(start_session))
    .route(
      "/api/v1/sessions/{session_id}/presentation",
      get(get_presentation),
    )
    .route(
      "/api/v1/sessions/{session_id}/action-catalog",
      get(get_action_catalog),
    )
    .route(
      "/api/v1/sessions/{session_id}/validation",
      post(validate_turn),
    )
    .route("/api/v1/sessions/{session_id}/turns", post(submit_turn))
    .route(
      "/api/v1/sessions/{session_id}/resolution",
      get(get_resolution),
    )
    .route(
      "/api/v1/sessions/{session_id}/regional-world",
      get(get_regional_world),
    )
    .route("/api/v1/sessions/{session_id}/history", get(get_history))
    .route("/api/v1/sessions/{session_id}/replay", get(get_replay))
    .route("/api/v1/sessions/{session_id}/save", post(save_session))
    .route("/api/v1/sessions/{session_id}/load", post(load_session))
    .route("/api/v1/sessions/{session_id}/end", post(end_session))
    .fallback(get(static_asset))
    .with_state(GuiState::default())
}

async fn start_session(
  State(state): State<GuiState>,
  Json(request): Json<GuiStartSessionRequest>,
) -> Response {
  if request.campaign != "competitive-regional-v1" {
    return (
      StatusCode::BAD_REQUEST,
      Json(McpErrorMessage {
        error: "live GUI currently supports competitive-regional-v1 only".to_string(),
        code: Some("unsupported_gui_campaign".to_string()),
        resource_limit: None,
        hint: Some("Use cargo run for stabilization or regional affiliation.".to_string()),
      }),
    )
      .into_response();
  }
  with_store(&state, |store| {
    store.start_session(StartSessionRequest {
      campaign: request.campaign,
      seed: request.seed,
      difficulty: request.difficulty,
      scenario_path: None,
    })
  })
}

async fn get_presentation(
  State(state): State<GuiState>,
  Path(session_id): Path<String>,
) -> Response {
  with_store(&state, |store| {
    store.get_presentation(GetPresentationRequest { session_id })
  })
}

async fn get_action_catalog(
  State(state): State<GuiState>,
  Path(session_id): Path<String>,
) -> Response {
  with_store(&state, |store| {
    store.get_action_catalog(GetActionCatalogRequest { session_id })
  })
}

async fn validate_turn(
  State(state): State<GuiState>,
  Path(session_id): Path<String>,
  Json(body): Json<CommandBody>,
) -> Response {
  with_store(&state, |store| {
    store.validate_turn(ValidateTurnRequest {
      session_id,
      command_text: body.command_text,
    })
  })
}

async fn submit_turn(
  State(state): State<GuiState>,
  Path(session_id): Path<String>,
  Json(body): Json<CommandBody>,
) -> Response {
  with_store(&state, |store| {
    store.submit_turn(SubmitTurnRequest {
      session_id,
      command_text: body.command_text,
    })
  })
}

async fn get_resolution(
  State(state): State<GuiState>,
  Path(session_id): Path<String>,
  Query(query): Query<ResolutionQuery>,
) -> Response {
  with_store(&state, |store| {
    store.get_resolution(GetResolutionRequest {
      session_id,
      turn: query.turn,
    })
  })
}

async fn get_regional_world(
  State(state): State<GuiState>,
  Path(session_id): Path<String>,
) -> Response {
  with_store(&state, |store| {
    store.get_regional_world(GetRegionalWorldRequest { session_id })
  })
}

async fn get_history(State(state): State<GuiState>, Path(session_id): Path<String>) -> Response {
  with_store(&state, |store| {
    store.get_history(GetHistoryRequest { session_id })
  })
}

async fn get_replay(State(state): State<GuiState>, Path(session_id): Path<String>) -> Response {
  with_store(&state, |store| {
    store.get_replay(GetReplayRequest { session_id })
  })
}

async fn save_session(State(state): State<GuiState>, Path(session_id): Path<String>) -> Response {
  with_store(&state, |store| {
    store.save_session(SaveSessionRequest { session_id })
  })
}

async fn load_session(State(state): State<GuiState>, Path(session_id): Path<String>) -> Response {
  with_store(&state, |store| {
    store.load_session(LoadSessionRequest { session_id })
  })
}

async fn end_session(State(state): State<GuiState>, Path(session_id): Path<String>) -> Response {
  with_store(&state, |store| {
    store.end_session(EndSessionRequest { session_id })
  })
}

fn with_store<T>(
  state: &GuiState,
  run: impl FnOnce(&mut GameSessionStore) -> Result<T, McpErrorMessage>,
) -> Response
where
  T: serde::Serialize,
{
  match state.store.lock() {
    Ok(mut store) => match run(&mut store) {
      Ok(value) => Json(value).into_response(),
      Err(error) => {
        let status = if error.error.starts_with("unknown session") {
          StatusCode::NOT_FOUND
        } else {
          StatusCode::BAD_REQUEST
        };
        (status, Json(error)).into_response()
      }
    },
    Err(_) => (
      StatusCode::INTERNAL_SERVER_ERROR,
      Json(McpErrorMessage {
        error: "GUI session store lock failed".to_string(),
        code: Some("session_store_unavailable".to_string()),
        resource_limit: None,
        hint: None,
      }),
    )
      .into_response(),
  }
}

async fn static_asset(uri: Uri) -> Response {
  let path = uri.path();
  let (content_type, content) = match path {
    "/" | "/index.html" => (
      "text/html; charset=utf-8",
      include_str!("../gui/index.html").replace(
        HOST_ADAPTER_MARKER,
        r#"<script type="module" src="./host-adapter.mjs"></script>"#,
      ),
    ),
    "/app.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/app.mjs").to_string(),
    ),
    "/ambience-contract.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/ambience-contract.mjs").to_string(),
    ),
    "/asset-availability.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/asset-availability.mjs").to_string(),
    ),
    "/asset-credits-renderer.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/asset-credits-renderer.mjs").to_string(),
    ),
    "/asset-credits.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/asset-credits.mjs").to_string(),
    ),
    "/audio-cue-contract.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/audio-cue-contract.mjs").to_string(),
    ),
    "/audio-priority-contract.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/audio-priority-contract.mjs").to_string(),
    ),
    "/audio.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/audio.mjs").to_string(),
    ),
    "/consequence-links.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/consequence-links.mjs").to_string(),
    ),
    "/facility-components.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/facility-components.mjs").to_string(),
    ),
    "/first-month.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/first-month.mjs").to_string(),
    ),
    "/metric-visualizations.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/metric-visualizations.mjs").to_string(),
    ),
    "/music-stem-contract.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/music-stem-contract.mjs").to_string(),
    ),
    "/operational-overlays.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/operational-overlays.mjs").to_string(),
    ),
    "/host-adapter.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/host-adapter.mjs").to_string(),
    ),
    "/playtest.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/playtest.mjs").to_string(),
    ),
    "/regional-board.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/regional-board.mjs").to_string(),
    ),
    "/resolution-sequence.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/resolution-sequence.mjs").to_string(),
    ),
    "/scene.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/scene.mjs").to_string(),
    ),
    "/visual.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/visual.mjs").to_string(),
    ),
    "/audio-catalog.json" => (
      "application/json",
      include_str!("../gui/audio-catalog.json").to_string(),
    ),
    "/visual-catalog.json" => (
      "application/json",
      include_str!("../gui/visual-catalog.json").to_string(),
    ),
    _ => return StatusCode::NOT_FOUND.into_response(),
  };
  ([(header::CONTENT_TYPE, content_type)], content).into_response()
}

#[cfg(test)]
mod tests {
  use super::*;
  use tokio::io::{AsyncReadExt, AsyncWriteExt};

  #[test]
  fn bind_arguments_default_to_loopback_and_reject_remote_addresses() {
    assert_eq!(
      parse_bind_args(["gui".to_string()]).expect("default bind"),
      "127.0.0.1:7878".parse::<SocketAddr>().unwrap()
    );
    let error = parse_bind_args([
      "gui".to_string(),
      "--bind".to_string(),
      "0.0.0.0:7878".to_string(),
    ])
    .expect_err("remote bind must fail");
    assert!(error.contains("loopback"));
  }

  #[test]
  fn ipv4_and_ipv6_loopback_are_allowed() {
    assert!(ensure_loopback("127.0.0.1:0".parse().unwrap()).is_ok());
    assert!(ensure_loopback("[::1]:0".parse().unwrap()).is_ok());
    assert!(
      ensure_loopback(SocketAddr::new(
        std::net::IpAddr::from([192, 0, 2, 1]),
        7878
      ))
      .is_err()
    );
  }

  async fn test_server() -> (SocketAddr, tokio::task::JoinHandle<()>) {
    let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
    let address = listener.local_addr().unwrap();
    let task = tokio::spawn(async move {
      axum::serve(listener, gui_router()).await.unwrap();
    });
    (address, task)
  }

  async fn request(
    address: SocketAddr,
    method: &str,
    path: &str,
    body: Option<&str>,
  ) -> (u16, String) {
    let body = body.unwrap_or("");
    let mut stream = tokio::net::TcpStream::connect(address).await.unwrap();
    let request = format!(
      "{method} {path} HTTP/1.1\r\nHost: {address}\r\nContent-Type: application/json\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{body}",
      body.len()
    );
    stream.write_all(request.as_bytes()).await.unwrap();
    let mut response = Vec::new();
    stream.read_to_end(&mut response).await.unwrap();
    let response = String::from_utf8(response).unwrap();
    let (head, body) = response.split_once("\r\n\r\n").unwrap();
    let status = head
      .split_whitespace()
      .nth(1)
      .unwrap()
      .parse::<u16>()
      .unwrap();
    (status, body.to_string())
  }

  #[tokio::test]
  async fn live_gui_embeds_complete_offline_module_graph() {
    let (address, server) = test_server().await;
    let resources = [
      ("/host-adapter.mjs", include_str!("../gui/host-adapter.mjs")),
      (
        "/ambience-contract.mjs",
        include_str!("../gui/ambience-contract.mjs"),
      ),
      ("/app.mjs", include_str!("../gui/app.mjs")),
      (
        "/asset-availability.mjs",
        include_str!("../gui/asset-availability.mjs"),
      ),
      (
        "/asset-credits-renderer.mjs",
        include_str!("../gui/asset-credits-renderer.mjs"),
      ),
      (
        "/asset-credits.mjs",
        include_str!("../gui/asset-credits.mjs"),
      ),
      (
        "/audio-cue-contract.mjs",
        include_str!("../gui/audio-cue-contract.mjs"),
      ),
      (
        "/audio-priority-contract.mjs",
        include_str!("../gui/audio-priority-contract.mjs"),
      ),
      ("/audio.mjs", include_str!("../gui/audio.mjs")),
      (
        "/consequence-links.mjs",
        include_str!("../gui/consequence-links.mjs"),
      ),
      (
        "/facility-components.mjs",
        include_str!("../gui/facility-components.mjs"),
      ),
      ("/first-month.mjs", include_str!("../gui/first-month.mjs")),
      (
        "/metric-visualizations.mjs",
        include_str!("../gui/metric-visualizations.mjs"),
      ),
      (
        "/music-stem-contract.mjs",
        include_str!("../gui/music-stem-contract.mjs"),
      ),
      (
        "/operational-overlays.mjs",
        include_str!("../gui/operational-overlays.mjs"),
      ),
      ("/playtest.mjs", include_str!("../gui/playtest.mjs")),
      (
        "/regional-board.mjs",
        include_str!("../gui/regional-board.mjs"),
      ),
      (
        "/resolution-sequence.mjs",
        include_str!("../gui/resolution-sequence.mjs"),
      ),
      ("/scene.mjs", include_str!("../gui/scene.mjs")),
      ("/visual.mjs", include_str!("../gui/visual.mjs")),
      (
        "/audio-catalog.json",
        include_str!("../gui/audio-catalog.json"),
      ),
      (
        "/visual-catalog.json",
        include_str!("../gui/visual-catalog.json"),
      ),
    ];
    for (path, expected) in resources {
      let (status, body) = request(address, "GET", path, None).await;
      assert_eq!(status, 200, "{path}: {body}");
      assert_eq!(body, expected, "{path} did not return its embedded source");
    }
    for path in ["/", "/index.html"] {
      let (status, body) = request(address, "GET", path, None).await;
      assert_eq!(status, 200, "{path}: {body}");
      assert!(
        body.contains("host-adapter.mjs"),
        "{path} omitted host adapter"
      );
    }
    server.abort();
  }

  #[tokio::test]
  async fn live_transport_completes_one_competitive_month() {
    let (address, server) = test_server().await;

    let (status, html) = request(address, "GET", "/", None).await;
    assert_eq!(status, 200);
    assert!(html.contains("host-adapter.mjs"));

    let start_body = r#"{"campaign":"competitive-regional-v1","seed":42,"difficulty":"normal"}"#;
    let (status, body) = request(address, "POST", "/api/v1/sessions", Some(start_body)).await;
    assert_eq!(status, 200, "{body}");
    let started: serde_json::Value = serde_json::from_str(&body).unwrap();
    let session_id = started["session_id"].as_str().unwrap();

    let history_path = format!("/api/v1/sessions/{session_id}/history");
    let (status, body) = request(address, "GET", &history_path, None).await;
    assert_eq!(status, 200, "{body}");
    let history: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(history["schema_version"], "competitive-history-v1");
    assert_eq!(history["transition_count"], 0);
    assert!(history["transitions"].as_array().unwrap().is_empty());

    for suffix in ["presentation", "regional-world", "action-catalog"] {
      let path = format!("/api/v1/sessions/{session_id}/{suffix}");
      let (status, body) = request(address, "GET", &path, None).await;
      assert_eq!(status, 200, "{suffix}: {body}");
    }

    let replay_path = format!("/api/v1/sessions/{session_id}/replay");
    let (status, body) = request(address, "GET", &replay_path, None).await;
    assert_eq!(status, 200, "{body}");
    let replay: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(replay["schema_version"], "competitive-replay-v1");
    assert_eq!(replay["transition_count"], 0);
    assert!(replay["latest_state_hash"].is_null());

    let validation_path = format!("/api/v1/sessions/{session_id}/validation");
    let (status, body) = request(
      address,
      "POST",
      &validation_path,
      Some(r#"{"command_text":"hold"}"#),
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let validation: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(validation["valid"], true);

    let turns_path = format!("/api/v1/sessions/{session_id}/turns");
    let (status, body) = request(
      address,
      "POST",
      &turns_path,
      Some(r#"{"command_text":"hold"}"#),
    )
    .await;
    assert_eq!(status, 200, "{body}");

    let resolution_path = format!("/api/v1/sessions/{session_id}/resolution");
    let (status, body) = request(address, "GET", &resolution_path, None).await;
    assert_eq!(status, 200, "{body}");
    let resolution: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(resolution["schema_version"], "competitive-resolution-v1");

    let (status, body) = request(address, "GET", &history_path, None).await;
    assert_eq!(status, 200, "{body}");
    let history: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(history["schema_version"], "competitive-history-v1");
    assert_eq!(history["transition_count"], 1);
    assert_eq!(history["transitions"].as_array().unwrap().len(), 1);
    assert_eq!(
      history["transitions"][0]["state_hash"],
      resolution["replay"]["state_hash"]
    );
    let (status, body) = request(address, "GET", &replay_path, None).await;
    assert_eq!(status, 200, "{body}");
    let replay: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(replay["schema_version"], "competitive-replay-v1");
    assert_eq!(replay["transition_count"], 1);
    assert_eq!(
      replay["latest_state_hash"],
      history["transitions"][0]["state_hash"]
    );

    let load_path = format!("/api/v1/sessions/{session_id}/load");
    let (status, body) = request(address, "POST", &load_path, None).await;
    assert_eq!(status, 400, "{body}");
    let error: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(error["code"], "checkpoint_missing");

    let save_path = format!("/api/v1/sessions/{session_id}/save");
    let (status, body) = request(address, "POST", &save_path, None).await;
    assert_eq!(status, 200, "{body}");
    let saved: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(saved["schema_version"], "competitive-save-v1");
    assert_eq!(saved["operation"], "saved");
    assert_eq!(saved["transition_count"], 1);

    let (status, body) = request(
      address,
      "POST",
      &turns_path,
      Some(r#"{"command_text":"hold"}"#),
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let (status, body) = request(address, "POST", &load_path, None).await;
    assert_eq!(status, 200, "{body}");
    let loaded: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(loaded["schema_version"], "competitive-save-v1");
    assert_eq!(loaded["operation"], "loaded");
    assert_eq!(loaded["transition_count"], 1);
    assert_eq!(loaded["latest_state_hash"], saved["latest_state_hash"]);

    let end_path = format!("/api/v1/sessions/{session_id}/end");
    let (status, body) = request(address, "POST", &end_path, None).await;
    assert_eq!(status, 200, "{body}");
    let ended: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(ended["schema_version"], "competitive-end-session-v1");
    assert_eq!(ended["replay"]["transition_count"], 1);
    assert_eq!(ended["history"].as_array().unwrap().len(), 1);
    assert!(!ended["debrief"].as_array().unwrap().is_empty());

    let (status, body) = request(
      address,
      "GET",
      &format!("/api/v1/sessions/{session_id}/presentation"),
      None,
    )
    .await;
    assert_eq!(status, 404, "{body}");

    server.abort();
  }

  #[tokio::test]
  async fn live_transport_returns_structured_unknown_session_error() {
    let (address, server) = test_server().await;
    let (status, body) = request(
      address,
      "GET",
      "/api/v1/sessions/missing/presentation",
      None,
    )
    .await;
    assert_eq!(status, 404);
    let error: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert!(error["error"].as_str().unwrap().contains("unknown session"));
    let (status, body) = request(address, "GET", "/api/v1/sessions/missing/replay", None).await;
    assert_eq!(status, 404);
    let error: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert!(error["error"].as_str().unwrap().contains("unknown session"));
    let (status, body) = request(address, "POST", "/api/v1/sessions/missing/save", None).await;
    assert_eq!(status, 404);
    let error: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert!(error["error"].as_str().unwrap().contains("unknown session"));
    let (status, body) = request(address, "GET", "/api/v1/sessions/missing/history", None).await;
    assert_eq!(status, 404);
    let error: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert!(error["error"].as_str().unwrap().contains("unknown session"));
    server.abort();
  }

  #[tokio::test]
  async fn live_transport_rejects_unsupported_campaign() {
    let (address, server) = test_server().await;
    let body = r#"{"campaign":"stabilization-v1","seed":42,"difficulty":null}"#;
    let (status, body) = request(address, "POST", "/api/v1/sessions", Some(body)).await;
    assert_eq!(status, 400);
    let error: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(error["code"], "unsupported_gui_campaign");
    server.abort();
  }

  #[test]
  fn live_start_request_rejects_scenario_paths() {
    let request = r#"{"campaign":"competitive-regional-v1","seed":42,"difficulty":"normal","scenario_path":"/tmp/private.toml"}"#;
    assert!(serde_json::from_str::<GuiStartSessionRequest>(request).is_err());
  }
}
