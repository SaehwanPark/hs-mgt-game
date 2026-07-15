use crate::model::{ActionCost, CompetitiveCommand};

use super::presentation::ReadOnlyResources;

pub const ACTION_CATALOG_SCHEMA_VERSION: &str = "competitive-actions-v1";
pub const VALIDATION_SCHEMA_VERSION: &str = "competitive-validation-v1";

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ActionCatalogEnvelope {
  pub schema_version: String,
  pub session_id: String,
  pub campaign: String,
  pub turn: u32,
  pub resources: ReadOnlyResources,
  pub actions: Vec<ActionSpec>,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ActionSpec {
  pub id: String,
  pub label: String,
  pub command_template: String,
  pub parameters: Vec<ActionParameter>,
  pub delay_label: String,
  pub uncertainty_label: String,
  pub constraint_label: String,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ActionParameter {
  pub name: String,
  pub label: String,
  pub input_type: String,
  pub options: Vec<String>,
  pub min: Option<i32>,
  pub max: Option<i32>,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ValidateTurnEnvelope {
  pub schema_version: String,
  pub session_id: String,
  pub valid: bool,
  pub canonical_command_text: String,
  pub cost: Option<ActionCost>,
  pub previews: Vec<ActionPreview>,
  pub errors: Vec<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, schemars::JsonSchema)]
pub struct ActionPreview {
  pub action_id: String,
  pub canonical_command: String,
  pub cost: ActionCost,
  pub delay_label: String,
  pub uncertainty_label: String,
  pub constraint_label: String,
}

pub fn competitive_action_catalog(
  session_id: String,
  turn: u32,
  resources: ReadOnlyResources,
) -> ActionCatalogEnvelope {
  ActionCatalogEnvelope {
    schema_version: ACTION_CATALOG_SCHEMA_VERSION.to_string(),
    session_id,
    campaign: "competitive-regional-v1".to_string(),
    turn,
    resources,
    actions: vec![
      action(
        "hold",
        "Hold",
        "hold",
        Vec::new(),
        "Current month proceeds without a new player action",
        "Operating result remains host-resolved",
        "No additional action-point, cash, or political-capital cost",
      ),
      action(
        "invest",
        "Invest in capacity",
        "invest domain={{domain}} amount={{amount}}",
        vec![
          options_parameter(
            "domain",
            "Capacity domain",
            &[
              "beds",
              "outpatient",
              "technology",
              "emergency",
              "icu",
              "obstetrics",
              "psychiatric",
              "cardiology",
              "oncology",
              "infusion",
              "neurology",
              "asc",
            ],
          ),
          number_parameter("amount", "Cash amount", Some(1), Some(40)),
        ],
        "Spend is committed now; capacity result is host-resolved",
        "Operating and capacity result remains stochastic",
        "Host validates amount, domain, and available resources",
      ),
      action(
        "recruit",
        "Recruit staff",
        "recruit role={{role}} headcount={{headcount}}",
        vec![
          options_parameter("role", "Role", &["nurse", "physician", "admin"]),
          number_parameter("headcount", "Headcount", Some(1), Some(10)),
        ],
        "Role-specific staffing delay is host-reported",
        "Candidate response and operating effect remain uncertain",
        "Host validates headcount and available resources",
      ),
      action(
        "monitor",
        "Monitor a rival",
        "monitor target={{target}} depth={{depth}}",
        vec![
          options_parameter(
            "target",
            "Public rival target",
            &["northlake", "summit", "valley", "metro"],
          ),
          number_parameter("depth", "Observation depth", Some(1), Some(3)),
        ],
        "Information may arrive after the monitored interval",
        "Private activity can remain unobserved",
        "Host validates target, depth, and action points",
      ),
      action(
        "negotiate",
        "Negotiate payer posture",
        "negotiate payer={{payer}} rate_posture={{rate_posture}}",
        vec![
          options_parameter(
            "payer",
            "Payer",
            &["carrier_a", "carrier_b", "medicaid", "medicare"],
          ),
          options_parameter(
            "rate_posture",
            "Rate posture",
            &["aggressive", "neutral", "conservative"],
          ),
        ],
        "Payer response is visible after host resolution",
        "Payer response and operating effect remain uncertain",
        "Host validates payer posture and political capital",
      ),
      action(
        "commit",
        "Make a public pledge",
        "commit pledge_type={{pledge_type}} level={{level}}",
        vec![
          options_parameter(
            "pledge_type",
            "Pledge type",
            &["access", "quality", "workforce"],
          ),
          number_parameter("level", "Commitment level", Some(1), Some(5)),
        ],
        "Commitment is reviewed through later host observations",
        "Follow-through and institutional response remain uncertain",
        "Host validates level and political capital",
      ),
      action(
        "project",
        "Start a capital or technology project",
        "project kind={{kind}} budget={{budget}}",
        vec![
          options_parameter(
            "kind",
            "Project kind",
            &[
              "ehr_epic",
              "ehr_cerner",
              "tower",
              "clinic_network",
              "emergency_pavilion",
              "icu_wing",
              "obstetrics_unit",
              "psychiatric_unit",
              "cardiology_unit",
              "oncology_unit",
              "infusion_center",
              "neurology_unit",
              "asc_unit",
            ],
          ),
          number_parameter("budget", "Project budget", Some(1), None),
        ],
        "Project-kind resolution delay is host-reported",
        "Completion and operating result remain uncertain",
        "Host validates budget, duration, project slots, and resources",
      ),
    ],
  }
}

pub fn validation_envelope(
  session_id: String,
  command_text: &str,
  commands: &[CompetitiveCommand],
  valid: bool,
  errors: Vec<String>,
) -> ValidateTurnEnvelope {
  let segments = command_text
    .split(';')
    .map(str::trim)
    .filter(|segment| !segment.is_empty())
    .collect::<Vec<_>>();
  let previews = commands
    .iter()
    .enumerate()
    .map(|(index, command)| {
      action_preview(
        command,
        segments.get(index).copied().unwrap_or("hold").to_string(),
      )
    })
    .collect::<Vec<_>>();
  let cost = if commands.is_empty() {
    None
  } else {
    Some(crate::model::sum_action_costs(commands))
  };
  ValidateTurnEnvelope {
    schema_version: VALIDATION_SCHEMA_VERSION.to_string(),
    session_id,
    valid,
    canonical_command_text: if command_text.trim().is_empty() {
      "hold".to_string()
    } else {
      command_text.trim().to_string()
    },
    cost,
    previews,
    errors,
  }
}

fn action(
  id: &str,
  label: &str,
  command_template: &str,
  parameters: Vec<ActionParameter>,
  delay_label: &str,
  uncertainty_label: &str,
  constraint_label: &str,
) -> ActionSpec {
  ActionSpec {
    id: id.to_string(),
    label: label.to_string(),
    command_template: command_template.to_string(),
    parameters,
    delay_label: delay_label.to_string(),
    uncertainty_label: uncertainty_label.to_string(),
    constraint_label: constraint_label.to_string(),
  }
}

fn options_parameter(name: &str, label: &str, options: &[&str]) -> ActionParameter {
  ActionParameter {
    name: name.to_string(),
    label: label.to_string(),
    input_type: "select".to_string(),
    options: options.iter().map(|option| (*option).to_string()).collect(),
    min: None,
    max: None,
  }
}

fn number_parameter(
  name: &str,
  label: &str,
  min: Option<i32>,
  max: Option<i32>,
) -> ActionParameter {
  ActionParameter {
    name: name.to_string(),
    label: label.to_string(),
    input_type: "number".to_string(),
    options: Vec::new(),
    min,
    max,
  }
}

fn action_preview(command: &CompetitiveCommand, canonical_command: String) -> ActionPreview {
  let action_id = action_id(command);
  let (delay_label, uncertainty_label, constraint_label) = action_labels(&action_id);
  ActionPreview {
    action_id,
    canonical_command,
    cost: command.action_cost(),
    delay_label,
    uncertainty_label,
    constraint_label,
  }
}

fn action_id(command: &CompetitiveCommand) -> String {
  match command {
    CompetitiveCommand::Hold => "hold",
    CompetitiveCommand::Invest { .. } => "invest",
    CompetitiveCommand::Recruit { .. } => "recruit",
    CompetitiveCommand::Monitor { .. } => "monitor",
    CompetitiveCommand::Negotiate { .. } => "negotiate",
    CompetitiveCommand::Commit { .. } => "commit",
    CompetitiveCommand::Project { .. } => "project",
  }
  .to_string()
}

fn action_labels(action_id: &str) -> (String, String, String) {
  match action_id {
    "hold" => (
      "Current month proceeds without a new player action".to_string(),
      "Operating result remains host-resolved".to_string(),
      "No additional action-point, cash, or political-capital cost".to_string(),
    ),
    "invest" => (
      "Spend is committed now; capacity result is host-resolved".to_string(),
      "Operating and capacity result remains stochastic".to_string(),
      "Host validates amount, domain, and available resources".to_string(),
    ),
    "recruit" => (
      "Role-specific staffing delay is host-reported".to_string(),
      "Candidate response and operating effect remain uncertain".to_string(),
      "Host validates headcount and available resources".to_string(),
    ),
    "monitor" => (
      "Information may arrive after the monitored interval".to_string(),
      "Private activity can remain unobserved".to_string(),
      "Host validates target, depth, and action points".to_string(),
    ),
    "negotiate" => (
      "Payer response is visible after host resolution".to_string(),
      "Payer response and operating effect remain uncertain".to_string(),
      "Host validates payer posture and political capital".to_string(),
    ),
    "commit" => (
      "Commitment is reviewed through later host observations".to_string(),
      "Follow-through and institutional response remain uncertain".to_string(),
      "Host validates level and political capital".to_string(),
    ),
    "project" => (
      "Project-kind resolution delay is host-reported".to_string(),
      "Completion and operating result remain uncertain".to_string(),
      "Host validates budget, duration, project slots, and resources".to_string(),
    ),
    _ => (
      "Host-reported delay".to_string(),
      "Outcome remains uncertain".to_string(),
      "Host validates this action".to_string(),
    ),
  }
}
