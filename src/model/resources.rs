use super::competitive_command::ActionCost;
use super::{CompetitiveCommand, Difficulty};

pub const DEFAULT_POLITICAL_CAPITAL_CAP: u32 = 15;
pub const DEFAULT_POLITICAL_CAPITAL_REFRESH: u32 = 2;
pub const DEFAULT_STARTING_CASH: i32 = 60;
pub const DEFAULT_STARTING_POLITICAL_CAPITAL: u32 = 8;
pub const DEFAULT_MAX_CONCURRENT_PROJECTS: u32 = 2;
pub const DEFAULT_MAX_INVEST_AMOUNT: i32 = 40;
pub const DEFAULT_MIN_RECRUIT_HEADCOUNT: u32 = 1;
pub const DEFAULT_MAX_RECRUIT_HEADCOUNT: u32 = 10;
pub const DEFAULT_MIN_COMMIT_LEVEL: u32 = 1;
pub const DEFAULT_MAX_COMMIT_LEVEL: u32 = 5;
pub const DEFAULT_MIN_MONITOR_DEPTH: u32 = 1;
pub const DEFAULT_MAX_MONITOR_DEPTH: u32 = 3;

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct CompetitiveRuleset {
  pub version: &'static str,
  pub starting_cash: i32,
  pub starting_political_capital: u32,
  pub political_capital_cap: u32,
  pub political_capital_refresh: u32,
  pub max_concurrent_projects: u32,
  pub max_invest_amount: i32,
  pub min_recruit_headcount: u32,
  pub max_recruit_headcount: u32,
  pub min_commit_level: u32,
  pub max_commit_level: u32,
  pub min_monitor_depth: u32,
  pub max_monitor_depth: u32,
}

pub fn default_competitive_ruleset() -> CompetitiveRuleset {
  CompetitiveRuleset {
    version: "competitive-ruleset-0.1.30",
    starting_cash: DEFAULT_STARTING_CASH,
    starting_political_capital: DEFAULT_STARTING_POLITICAL_CAPITAL,
    political_capital_cap: DEFAULT_POLITICAL_CAPITAL_CAP,
    political_capital_refresh: DEFAULT_POLITICAL_CAPITAL_REFRESH,
    max_concurrent_projects: DEFAULT_MAX_CONCURRENT_PROJECTS,
    max_invest_amount: DEFAULT_MAX_INVEST_AMOUNT,
    min_recruit_headcount: DEFAULT_MIN_RECRUIT_HEADCOUNT,
    max_recruit_headcount: DEFAULT_MAX_RECRUIT_HEADCOUNT,
    min_commit_level: DEFAULT_MIN_COMMIT_LEVEL,
    max_commit_level: DEFAULT_MAX_COMMIT_LEVEL,
    min_monitor_depth: DEFAULT_MIN_MONITOR_DEPTH,
    max_monitor_depth: DEFAULT_MAX_MONITOR_DEPTH,
  }
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct PlayerResources {
  pub cash: i32,
  pub political_capital: u32,
  pub ap_budget: u32,
  pub active_projects: u32,
  pub active_project_monthly_draws: i32,
}

impl PlayerResources {
  pub fn genesis(difficulty: Difficulty, ruleset: &CompetitiveRuleset) -> Self {
    Self {
      cash: ruleset.starting_cash,
      political_capital: ruleset.starting_political_capital,
      ap_budget: difficulty.human_ap_per_month(),
      active_projects: 0,
      active_project_monthly_draws: 0,
    }
  }

  pub fn ap_remaining(&self, ap_spent: u32) -> u32 {
    self.ap_budget.saturating_sub(ap_spent)
  }

  pub fn refresh_political_capital(&mut self, ruleset: &CompetitiveRuleset) {
    let refreshed = self
      .political_capital
      .saturating_add(ruleset.political_capital_refresh);
    self.political_capital = refreshed.min(ruleset.political_capital_cap);
  }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum CompetitiveValidationError {
  ApBudgetExceeded { requested: u32, budget: u32 },
  InsufficientCash { required: i32, available: i32 },
  InsufficientPoliticalCapital { required: u32, available: u32 },
  TooManyConcurrentProjects { requested: u32, max: u32 },
  InvalidRecruitHeadcount { headcount: u32, min: u32, max: u32 },
  InvestAmountNonPositive,
  InvestAmountTooHigh { amount: i32, max: i32 },
  MonitorDepthOutOfRange { depth: u32, min: u32, max: u32 },
  CommitLevelOutOfRange { level: u32, min: u32, max: u32 },
  ProjectBudgetNonPositive,
  ProjectBudgetBelowDuration { budget: i32, resolve_months: u32 },
  ProjectBudgetNotDivisible { budget: i32, resolve_months: u32 },
  ProjectMonthlyDrawInfeasible { monthly_draw: i32, available: i32 },
  UnknownSystemId { system_id: u32 },
  BatchCountMismatch { expected: u32, provided: u32 },
  MonthIndexMismatch { expected: u32, provided: u32 },
  InvalidMedicaidPosture,
  InvalidMedicarePosture,
}

impl CompetitiveValidationError {
  pub fn message(&self) -> String {
    match self {
      CompetitiveValidationError::ApBudgetExceeded { requested, budget } => {
        format!("action points {requested} exceed monthly budget {budget}")
      }
      CompetitiveValidationError::InsufficientCash {
        required,
        available,
      } => {
        format!("cash required {required} exceeds available {available}")
      }
      CompetitiveValidationError::InsufficientPoliticalCapital {
        required,
        available,
      } => {
        format!("political capital {required} exceeds available {available}")
      }
      CompetitiveValidationError::TooManyConcurrentProjects { requested, max } => {
        format!("concurrent projects {requested} exceed limit {max}")
      }
      CompetitiveValidationError::InvalidRecruitHeadcount {
        headcount,
        min,
        max,
      } => {
        format!("recruit headcount {headcount} outside range {min}–{max}")
      }
      CompetitiveValidationError::InvestAmountNonPositive => {
        "invest amount must be positive".to_string()
      }
      CompetitiveValidationError::InvestAmountTooHigh { amount, max } => {
        format!("invest amount {amount} exceeds per-command limit {max}")
      }
      CompetitiveValidationError::MonitorDepthOutOfRange { depth, min, max } => {
        format!("monitor depth {depth} outside range {min}–{max}")
      }
      CompetitiveValidationError::CommitLevelOutOfRange { level, min, max } => {
        format!("commit level {level} outside range {min}–{max}")
      }
      CompetitiveValidationError::ProjectBudgetNonPositive => {
        "project budget must be positive".to_string()
      }
      CompetitiveValidationError::ProjectBudgetBelowDuration {
        budget,
        resolve_months,
      } => {
        format!(
          "project budget {budget} is too small for a non-zero monthly draw over {resolve_months} months"
        )
      }
      CompetitiveValidationError::ProjectBudgetNotDivisible {
        budget,
        resolve_months,
      } => {
        format!("project budget {budget} must be a multiple of duration {resolve_months} months")
      }
      CompetitiveValidationError::ProjectMonthlyDrawInfeasible {
        monthly_draw,
        available,
      } => {
        format!("project monthly draw {monthly_draw} exceeds available cash {available}")
      }
      CompetitiveValidationError::UnknownSystemId { system_id } => {
        format!("unknown system id {system_id}")
      }
      CompetitiveValidationError::BatchCountMismatch { expected, provided } => {
        format!("expected {expected} player batches, received {provided}")
      }
      CompetitiveValidationError::MonthIndexMismatch { expected, provided } => {
        format!("month index {provided} does not match current month {expected}")
      }
      CompetitiveValidationError::InvalidMedicaidPosture => {
        "Medicaid negotiations only support neutral posture".to_string()
      }
      CompetitiveValidationError::InvalidMedicarePosture => {
        "Medicare negotiations only support neutral posture".to_string()
      }
    }
  }
}

pub fn sum_action_costs(commands: &[CompetitiveCommand]) -> ActionCost {
  let mut total = ActionCost {
    action_points: 0,
    cash_cost: 0,
    political_capital: 0,
  };

  for command in commands {
    let cost = command.action_cost();
    total.action_points += cost.action_points;
    total.cash_cost += cost.cash_cost;
    total.political_capital += cost.political_capital;
  }

  total
}
