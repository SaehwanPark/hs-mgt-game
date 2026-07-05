#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct ActionCost {
  pub action_points: u32,
  pub cash_cost: i32,
  pub political_capital: u32,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum RecruitRole {
  Nurse,
  Physician,
  Admin,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum InvestDomain {
  Beds,
  Outpatient,
  Technology,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum MonitorTarget {
  Northlake,
  Summit,
  Valley,
  Metro,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum PayerId {
  CarrierA,
  CarrierB,
  Medicaid,
  Medicare,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum RatePosture {
  Aggressive,
  Neutral,
  Conservative,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum PledgeType {
  Access,
  Quality,
  Workforce,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum ProjectKind {
  EhrEpic,
  EhrCerner,
  Tower,
  ClinicNetwork,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum CompetitiveCommand {
  Hold,
  Recruit {
    role: RecruitRole,
    headcount: u32,
  },
  Invest {
    domain: InvestDomain,
    amount: i32,
  },
  Monitor {
    target: MonitorTarget,
    depth: u32,
  },
  Negotiate {
    payer: PayerId,
    rate_posture: RatePosture,
  },
  Commit {
    pledge_type: PledgeType,
    level: u32,
  },
  Project {
    kind: ProjectKind,
    budget: i32,
  },
}

impl RecruitRole {
  pub fn recruit_delay_months(self) -> u32 {
    match self {
      RecruitRole::Nurse => 1,
      RecruitRole::Physician => 3,
      RecruitRole::Admin => 2,
    }
  }
}

impl ProjectKind {
  pub fn resolve_months(self) -> u32 {
    match self {
      ProjectKind::EhrEpic | ProjectKind::EhrCerner => 12,
      ProjectKind::Tower => 12,
      ProjectKind::ClinicNetwork => 9,
    }
  }
}

impl MonitorTarget {
  pub fn system_id(self) -> u32 {
    match self {
      MonitorTarget::Northlake => 1,
      MonitorTarget::Summit => 2,
      MonitorTarget::Valley => 3,
      MonitorTarget::Metro => 4,
    }
  }
}

impl CompetitiveCommand {
  pub fn action_cost(&self) -> ActionCost {
    match self {
      CompetitiveCommand::Hold => ActionCost {
        action_points: 0,
        cash_cost: 0,
        political_capital: 0,
      },
      CompetitiveCommand::Recruit { headcount, .. } => ActionCost {
        action_points: 1,
        cash_cost: 5 * (*headcount as i32),
        political_capital: 0,
      },
      CompetitiveCommand::Invest { amount, .. } => ActionCost {
        action_points: 1,
        cash_cost: *amount,
        political_capital: 0,
      },
      CompetitiveCommand::Monitor { depth, .. } => ActionCost {
        action_points: *depth,
        cash_cost: 0,
        political_capital: 0,
      },
      CompetitiveCommand::Negotiate { payer, .. } => ActionCost {
        action_points: 1,
        cash_cost: match payer {
          PayerId::Medicaid => 5,
          PayerId::Medicare => 10,
          _ => 0,
        },
        political_capital: 2,
      },
      CompetitiveCommand::Commit { .. } => ActionCost {
        action_points: 1,
        cash_cost: 0,
        political_capital: 1,
      },
      CompetitiveCommand::Project { kind, budget } => ActionCost {
        action_points: 2,
        cash_cost: project_monthly_draw(*budget, kind.resolve_months()),
        political_capital: 0,
      },
    }
  }

  pub fn is_project(&self) -> bool {
    matches!(self, CompetitiveCommand::Project { .. })
  }
}

pub(crate) fn project_monthly_draw(budget: i32, resolve_months: u32) -> i32 {
  if resolve_months == 0 {
    return budget;
  }
  budget / (resolve_months as i32)
}
