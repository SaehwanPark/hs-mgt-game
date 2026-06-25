use crate::model::{
  CompetitiveCommand, CompetitiveRuleset, CompetitiveValidationError, PlayerResources,
  project_monthly_draw, sum_action_costs,
};

pub fn validate_competitive_command(
  command: &CompetitiveCommand,
  ruleset: &CompetitiveRuleset,
) -> Result<(), CompetitiveValidationError> {
  match command {
    CompetitiveCommand::Hold => Ok(()),
    CompetitiveCommand::Recruit { headcount, .. } => {
      if *headcount < ruleset.min_recruit_headcount || *headcount > ruleset.max_recruit_headcount {
        return Err(CompetitiveValidationError::InvalidRecruitHeadcount {
          headcount: *headcount,
          min: ruleset.min_recruit_headcount,
          max: ruleset.max_recruit_headcount,
        });
      }
      Ok(())
    }
    CompetitiveCommand::Invest { amount, .. } => {
      if *amount <= 0 {
        return Err(CompetitiveValidationError::InvestAmountNonPositive);
      }
      if *amount > ruleset.max_invest_amount {
        return Err(CompetitiveValidationError::InvestAmountTooHigh {
          amount: *amount,
          max: ruleset.max_invest_amount,
        });
      }
      Ok(())
    }
    CompetitiveCommand::Monitor { depth, .. } => {
      if *depth < ruleset.min_monitor_depth || *depth > ruleset.max_monitor_depth {
        return Err(CompetitiveValidationError::MonitorDepthOutOfRange {
          depth: *depth,
          min: ruleset.min_monitor_depth,
          max: ruleset.max_monitor_depth,
        });
      }
      Ok(())
    }
    CompetitiveCommand::Commit { level, .. } => {
      if *level < ruleset.min_commit_level || *level > ruleset.max_commit_level {
        return Err(CompetitiveValidationError::CommitLevelOutOfRange {
          level: *level,
          min: ruleset.min_commit_level,
          max: ruleset.max_commit_level,
        });
      }
      Ok(())
    }
    CompetitiveCommand::Project { kind, budget } => {
      if *budget <= 0 {
        return Err(CompetitiveValidationError::ProjectBudgetNonPositive);
      }
      let monthly_draw = project_monthly_draw(*budget, kind.resolve_months());
      if monthly_draw <= 0 {
        return Err(CompetitiveValidationError::ProjectMonthlyDrawInfeasible {
          monthly_draw,
          available: 0,
        });
      }
      Ok(())
    }
    CompetitiveCommand::Negotiate { .. } => Ok(()),
  }
}

pub fn validate_competitive_batch(
  commands: &[CompetitiveCommand],
  resources: &PlayerResources,
  ruleset: &CompetitiveRuleset,
) -> Result<(), CompetitiveValidationError> {
  for command in commands {
    validate_competitive_command(command, ruleset)?;
  }

  let totals = sum_action_costs(commands);
  let new_projects = commands
    .iter()
    .filter(|command| command.is_project())
    .count() as u32;

  if totals.action_points > resources.ap_budget {
    return Err(CompetitiveValidationError::ApBudgetExceeded {
      requested: totals.action_points,
      budget: resources.ap_budget,
    });
  }

  let concurrent_projects = resources.active_projects.saturating_add(new_projects);
  if concurrent_projects > ruleset.max_concurrent_projects {
    return Err(CompetitiveValidationError::TooManyConcurrentProjects {
      requested: concurrent_projects,
      max: ruleset.max_concurrent_projects,
    });
  }

  if totals.political_capital > resources.political_capital {
    return Err(CompetitiveValidationError::InsufficientPoliticalCapital {
      required: totals.political_capital,
      available: resources.political_capital,
    });
  }

  let cash_required = resources.active_project_monthly_draws + totals.cash_cost;
  if cash_required > resources.cash {
    return Err(CompetitiveValidationError::InsufficientCash {
      required: cash_required,
      available: resources.cash,
    });
  }

  Ok(())
}
