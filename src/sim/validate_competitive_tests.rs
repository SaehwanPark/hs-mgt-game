use crate::model::{
  CompetitiveCommand, CompetitiveValidationError, Difficulty, InvestDomain, MonitorTarget, PayerId,
  PlayerResources, PledgeType, ProjectKind, RatePosture, RecruitRole, default_competitive_ruleset,
};
use crate::sim::{validate_competitive_batch, validate_competitive_command};

fn genesis_resources(difficulty: Difficulty) -> PlayerResources {
  PlayerResources::genesis(difficulty, &default_competitive_ruleset())
}

#[test]
fn hold_costs_zero_action_points() {
  let cost = CompetitiveCommand::Hold.action_cost();
  assert_eq!(cost.action_points, 0);
  assert_eq!(cost.cash_cost, 0);
  assert_eq!(cost.political_capital, 0);
}

#[test]
fn catalog_cost_spot_checks_per_verb() {
  assert_eq!(
    CompetitiveCommand::Recruit {
      role: RecruitRole::Nurse,
      headcount: 2,
    }
    .action_cost()
    .cash_cost,
    10
  );
  assert_eq!(
    CompetitiveCommand::Invest {
      domain: InvestDomain::Beds,
      amount: 15,
    }
    .action_cost()
    .cash_cost,
    15
  );
  assert_eq!(
    CompetitiveCommand::Monitor {
      target: MonitorTarget::Northlake,
      depth: 2,
    }
    .action_cost()
    .action_points,
    2
  );
  assert_eq!(
    CompetitiveCommand::Negotiate {
      payer: PayerId::CarrierA,
      rate_posture: RatePosture::Neutral,
    }
    .action_cost()
    .political_capital,
    2
  );
  assert_eq!(
    CompetitiveCommand::Commit {
      pledge_type: PledgeType::Access,
      level: 3,
    }
    .action_cost()
    .political_capital,
    1
  );
  assert_eq!(
    CompetitiveCommand::Project {
      kind: ProjectKind::EhrEpic,
      budget: 60,
    }
    .action_cost()
    .cash_cost,
    5
  );
  assert_eq!(
    CompetitiveCommand::Project {
      kind: ProjectKind::EhrEpic,
      budget: 60,
    }
    .action_cost()
    .action_points,
    2
  );
}

#[test]
fn valid_hold_batch_passes() {
  let resources = genesis_resources(Difficulty::Normal);
  let batch = vec![CompetitiveCommand::Hold];
  assert!(validate_competitive_batch(&batch, &resources, &default_competitive_ruleset()).is_ok());
}

#[test]
fn ap_batch_exceeding_budget_fails() {
  let resources = genesis_resources(Difficulty::Normal);
  let batch = vec![
    CompetitiveCommand::Invest {
      domain: InvestDomain::Technology,
      amount: 10,
    },
    CompetitiveCommand::Recruit {
      role: RecruitRole::Nurse,
      headcount: 1,
    },
    CompetitiveCommand::Negotiate {
      payer: PayerId::CarrierA,
      rate_posture: RatePosture::Aggressive,
    },
    CompetitiveCommand::Commit {
      pledge_type: PledgeType::Quality,
      level: 2,
    },
  ];
  let error = validate_competitive_batch(&batch, &resources, &default_competitive_ruleset())
    .expect_err("batch should exceed AP budget");
  assert!(matches!(
    error,
    CompetitiveValidationError::ApBudgetExceeded {
      requested: 4,
      budget: 3,
    }
  ));
}

#[test]
fn insufficient_cash_for_invest_fails() {
  let mut resources = genesis_resources(Difficulty::Easy);
  resources.cash = 25;
  let batch = vec![CompetitiveCommand::Invest {
    domain: InvestDomain::Beds,
    amount: 30,
  }];
  let error = validate_competitive_batch(&batch, &resources, &default_competitive_ruleset())
    .expect_err("invest should exceed cash");
  assert!(matches!(
    error,
    CompetitiveValidationError::InsufficientCash { .. }
  ));
}

#[test]
fn negotiate_and_commit_pc_overspend_fails() {
  let mut resources = genesis_resources(Difficulty::Normal);
  resources.political_capital = 2;
  let batch = vec![
    CompetitiveCommand::Negotiate {
      payer: PayerId::CarrierB,
      rate_posture: RatePosture::Conservative,
    },
    CompetitiveCommand::Commit {
      pledge_type: PledgeType::Access,
      level: 1,
    },
  ];
  let error = validate_competitive_batch(&batch, &resources, &default_competitive_ruleset())
    .expect_err("batch should exceed political capital");
  assert!(matches!(
    error,
    CompetitiveValidationError::InsufficientPoliticalCapital {
      required: 3,
      available: 2,
    }
  ));
}

#[test]
fn third_concurrent_project_fails() {
  let mut resources = genesis_resources(Difficulty::Easy);
  resources.active_projects = 2;
  let batch = vec![CompetitiveCommand::Project {
    kind: ProjectKind::Tower,
    budget: 48,
  }];
  let error = validate_competitive_batch(&batch, &resources, &default_competitive_ruleset())
    .expect_err("third project should fail");
  assert!(matches!(
    error,
    CompetitiveValidationError::TooManyConcurrentProjects {
      requested: 3,
      max: 2,
    }
  ));
}

#[test]
fn recruit_headcount_out_of_range_fails() {
  let ruleset = default_competitive_ruleset();
  let error = validate_competitive_command(
    &CompetitiveCommand::Recruit {
      role: RecruitRole::Admin,
      headcount: 11,
    },
    &ruleset,
  )
  .expect_err("headcount should be invalid");
  assert!(matches!(
    error,
    CompetitiveValidationError::InvalidRecruitHeadcount { .. }
  ));
}

#[test]
fn monitor_depth_out_of_range_fails() {
  let ruleset = default_competitive_ruleset();
  let error = validate_competitive_command(
    &CompetitiveCommand::Monitor {
      target: MonitorTarget::Summit,
      depth: 4,
    },
    &ruleset,
  )
  .expect_err("depth should be invalid");
  assert!(matches!(
    error,
    CompetitiveValidationError::MonitorDepthOutOfRange { .. }
  ));
}

#[test]
fn commit_level_out_of_range_fails() {
  let ruleset = default_competitive_ruleset();
  let error = validate_competitive_command(
    &CompetitiveCommand::Commit {
      pledge_type: PledgeType::Quality,
      level: 0,
    },
    &ruleset,
  )
  .expect_err("level should be invalid");
  assert!(matches!(
    error,
    CompetitiveValidationError::CommitLevelOutOfRange { .. }
  ));
}

#[test]
fn empty_batch_passes() {
  let resources = genesis_resources(Difficulty::Normal);
  assert!(validate_competitive_batch(&[], &resources, &default_competitive_ruleset()).is_ok());
}

#[test]
fn project_budget_smaller_than_duration_fails() {
  let ruleset = default_competitive_ruleset();
  let error = validate_competitive_command(
    &CompetitiveCommand::Project {
      kind: ProjectKind::EhrEpic,
      budget: 5,
    },
    &ruleset,
  )
  .expect_err("budget below resolve months should fail");
  assert!(matches!(
    error,
    CompetitiveValidationError::ProjectBudgetBelowDuration {
      budget: 5,
      resolve_months: 12,
    }
  ));
}

#[test]
fn project_budget_not_divisible_by_duration_fails() {
  let ruleset = default_competitive_ruleset();
  let error = validate_competitive_command(
    &CompetitiveCommand::Project {
      kind: ProjectKind::EhrEpic,
      budget: 15,
    },
    &ruleset,
  )
  .expect_err("budget not divisible by duration should fail");
  assert!(matches!(
    error,
    CompetitiveValidationError::ProjectBudgetNotDivisible {
      budget: 15,
      resolve_months: 12,
    }
  ));
}
