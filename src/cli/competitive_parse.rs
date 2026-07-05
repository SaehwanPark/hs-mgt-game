use crate::model::{
  CliError, CompetitiveCommand, InvestDomain, MonitorTarget, PayerId, PledgeType, ProjectKind,
  RatePosture, RecruitRole,
};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct CompetitiveCommandSpec {
  pub verb: &'static str,
  pub usage: &'static str,
}

const COMPETITIVE_COMMAND_SPECS: [CompetitiveCommandSpec; 7] = [
  CompetitiveCommandSpec {
    verb: "hold",
    usage: "hold",
  },
  CompetitiveCommandSpec {
    verb: "invest",
    usage: "invest domain=beds|outpatient|technology amount=<int>",
  },
  CompetitiveCommandSpec {
    verb: "recruit",
    usage: "recruit role=nurse|physician|admin headcount=<int>",
  },
  CompetitiveCommandSpec {
    verb: "monitor",
    usage: "monitor target=northlake|summit|valley|metro depth=<1-3>",
  },
  CompetitiveCommandSpec {
    verb: "negotiate",
    usage: "negotiate payer=carrier_a|carrier_b|medicaid|medicare rate_posture=aggressive|neutral|conservative",
  },
  CompetitiveCommandSpec {
    verb: "commit",
    usage: "commit pledge_type=access|quality|workforce level=<1-5>",
  },
  CompetitiveCommandSpec {
    verb: "project",
    usage: "project kind=ehr_epic|ehr_cerner|tower|clinic_network budget=<int>",
  },
];

pub fn competitive_command_specs() -> &'static [CompetitiveCommandSpec] {
  &COMPETITIVE_COMMAND_SPECS
}

pub fn competitive_command_verbs() -> Vec<&'static str> {
  competitive_command_specs()
    .iter()
    .map(|spec| spec.verb)
    .collect()
}

pub fn parse_competitive_batch(input: &str) -> Result<Vec<CompetitiveCommand>, CliError> {
  let trimmed = input.trim();
  if trimmed.is_empty() {
    return Ok(vec![CompetitiveCommand::Hold]);
  }

  trimmed
    .split(';')
    .map(str::trim)
    .filter(|segment| !segment.is_empty())
    .map(parse_competitive_command)
    .collect()
}

pub fn parse_competitive_command(input: &str) -> Result<CompetitiveCommand, CliError> {
  let trimmed = input.trim();
  if trimmed.is_empty() {
    return Ok(CompetitiveCommand::Hold);
  }

  let comment_stripped = trimmed.split("//").next().unwrap_or(trimmed).trim();
  if comment_stripped.is_empty() {
    return Ok(CompetitiveCommand::Hold);
  }

  let mut parts = comment_stripped.split_whitespace();
  let verb = parts
    .next()
    .ok_or_else(|| CliError::InvalidCommandInput("empty command".to_string()))?
    .to_ascii_lowercase();

  let mut args = std::collections::HashMap::new();
  for token in parts {
    let Some((name, value)) = token.split_once('=') else {
      return Err(CliError::InvalidCommandInput(format!(
        "expected arg=value, got '{token}'"
      )));
    };
    args.insert(name.to_ascii_lowercase(), value.to_string());
  }

  match verb.as_str() {
    "hold" => Ok(CompetitiveCommand::Hold),
    "recruit" => {
      let role = parse_recruit_role(required_arg(&args, "role")?)?;
      let headcount = required_arg(&args, "headcount")?
        .parse::<u32>()
        .map_err(|_| {
          CliError::InvalidCommandInput("recruit headcount must be a positive integer".to_string())
        })?;
      Ok(CompetitiveCommand::Recruit { role, headcount })
    }
    "invest" => {
      let domain = parse_invest_domain(required_arg(&args, "domain")?)?;
      let amount = required_arg(&args, "amount")?.parse::<i32>().map_err(|_| {
        CliError::InvalidCommandInput("invest amount must be an integer".to_string())
      })?;
      Ok(CompetitiveCommand::Invest { domain, amount })
    }
    "monitor" => {
      let target = parse_monitor_target(required_arg(&args, "target")?)?;
      let depth = required_arg(&args, "depth")?.parse::<u32>().map_err(|_| {
        CliError::InvalidCommandInput("monitor depth must be an integer".to_string())
      })?;
      Ok(CompetitiveCommand::Monitor { target, depth })
    }
    "negotiate" => {
      let payer = parse_payer(required_arg(&args, "payer")?)?;
      let rate_posture = parse_rate_posture(required_arg(&args, "rate_posture")?)?;
      Ok(CompetitiveCommand::Negotiate {
        payer,
        rate_posture,
      })
    }
    "commit" => {
      let pledge_type = parse_pledge_type(required_arg(&args, "pledge_type")?)?;
      let level = required_arg(&args, "level")?.parse::<u32>().map_err(|_| {
        CliError::InvalidCommandInput("commit level must be an integer".to_string())
      })?;
      Ok(CompetitiveCommand::Commit { pledge_type, level })
    }
    "project" => {
      let kind = parse_project_kind(required_arg(&args, "kind")?)?;
      let budget = required_arg(&args, "budget")?.parse::<i32>().map_err(|_| {
        CliError::InvalidCommandInput("project budget must be an integer".to_string())
      })?;
      Ok(CompetitiveCommand::Project { kind, budget })
    }
    other => Err(CliError::InvalidCommandInput(format!(
      "unknown competitive verb '{other}'"
    ))),
  }
}

pub fn competitive_command_help_lines() -> Vec<String> {
  let mut lines = competitive_command_specs()
    .iter()
    .map(|spec| spec.usage.to_string())
    .collect::<Vec<_>>();
  lines.push("Separate multiple commands with ';' on one line.".to_string());
  lines
}

fn required_arg<'a>(
  args: &'a std::collections::HashMap<String, String>,
  key: &str,
) -> Result<&'a str, CliError> {
  args
    .get(key)
    .map(String::as_str)
    .ok_or_else(|| CliError::InvalidCommandInput(format!("missing required argument '{key}='")))
}

fn parse_recruit_role(value: &str) -> Result<RecruitRole, CliError> {
  match value.to_ascii_lowercase().as_str() {
    "nurse" => Ok(RecruitRole::Nurse),
    "physician" => Ok(RecruitRole::Physician),
    "admin" => Ok(RecruitRole::Admin),
    _ => Err(CliError::InvalidCommandInput(format!(
      "unknown recruit role '{value}'"
    ))),
  }
}

fn parse_invest_domain(value: &str) -> Result<InvestDomain, CliError> {
  match value.to_ascii_lowercase().as_str() {
    "beds" => Ok(InvestDomain::Beds),
    "outpatient" => Ok(InvestDomain::Outpatient),
    "technology" => Ok(InvestDomain::Technology),
    _ => Err(CliError::InvalidCommandInput(format!(
      "unknown invest domain '{value}'"
    ))),
  }
}

fn parse_monitor_target(value: &str) -> Result<MonitorTarget, CliError> {
  match value.to_ascii_lowercase().as_str() {
    "northlake" => Ok(MonitorTarget::Northlake),
    "summit" => Ok(MonitorTarget::Summit),
    "valley" => Ok(MonitorTarget::Valley),
    "metro" => Ok(MonitorTarget::Metro),
    _ => Err(CliError::InvalidCommandInput(format!(
      "unknown monitor target '{value}'"
    ))),
  }
}

fn parse_payer(value: &str) -> Result<PayerId, CliError> {
  match value.to_ascii_lowercase().as_str() {
    "carrier_a" => Ok(PayerId::CarrierA),
    "carrier_b" => Ok(PayerId::CarrierB),
    "medicaid" => Ok(PayerId::Medicaid),
    "medicare" => Ok(PayerId::Medicare),
    _ => Err(CliError::InvalidCommandInput(format!(
      "unknown payer '{value}'"
    ))),
  }
}

fn parse_rate_posture(value: &str) -> Result<RatePosture, CliError> {
  match value.to_ascii_lowercase().as_str() {
    "aggressive" => Ok(RatePosture::Aggressive),
    "neutral" => Ok(RatePosture::Neutral),
    "conservative" => Ok(RatePosture::Conservative),
    _ => Err(CliError::InvalidCommandInput(format!(
      "unknown rate posture '{value}'"
    ))),
  }
}

fn parse_pledge_type(value: &str) -> Result<PledgeType, CliError> {
  match value.to_ascii_lowercase().as_str() {
    "access" => Ok(PledgeType::Access),
    "quality" => Ok(PledgeType::Quality),
    "workforce" => Ok(PledgeType::Workforce),
    _ => Err(CliError::InvalidCommandInput(format!(
      "unknown pledge type '{value}'"
    ))),
  }
}

fn parse_project_kind(value: &str) -> Result<ProjectKind, CliError> {
  match value.to_ascii_lowercase().as_str() {
    "ehr_epic" => Ok(ProjectKind::EhrEpic),
    "ehr_cerner" => Ok(ProjectKind::EhrCerner),
    "tower" => Ok(ProjectKind::Tower),
    "clinic_network" => Ok(ProjectKind::ClinicNetwork),
    _ => Err(CliError::InvalidCommandInput(format!(
      "unknown project kind '{value}'"
    ))),
  }
}

#[cfg(test)]
mod competitive_parse_tests {
  use super::*;

  #[test]
  fn parse_hold_command() {
    let command = parse_competitive_command("hold").expect("hold");
    assert_eq!(command, CompetitiveCommand::Hold);
  }

  #[test]
  fn parse_invest_with_args() {
    let command = parse_competitive_command("invest domain=beds amount=25").expect("invest");
    assert_eq!(
      command,
      CompetitiveCommand::Invest {
        domain: InvestDomain::Beds,
        amount: 25,
      }
    );
  }

  #[test]
  fn parse_batch_with_semicolon() {
    let batch = parse_competitive_batch("hold; monitor target=northlake depth=1").expect("batch");
    assert_eq!(batch.len(), 2);
  }

  #[test]
  fn empty_batch_defaults_to_hold() {
    let batch = parse_competitive_batch("").expect("batch");
    assert_eq!(batch, vec![CompetitiveCommand::Hold]);
  }

  #[test]
  fn unknown_verb_is_error() {
    assert!(parse_competitive_command("invst domain=beds amount=1").is_err());
  }

  #[test]
  fn command_specs_match_help_lines_order() {
    let expected = competitive_command_specs()
      .iter()
      .map(|spec| spec.usage.to_string())
      .collect::<Vec<_>>();
    let mut actual = competitive_command_help_lines();
    let _ = actual.pop();
    assert_eq!(actual, expected);
  }

  #[test]
  fn command_verbs_are_unique() {
    let mut verbs = competitive_command_verbs();
    verbs.sort_unstable();
    verbs.dedup();
    assert_eq!(verbs.len(), competitive_command_specs().len());
  }
}
