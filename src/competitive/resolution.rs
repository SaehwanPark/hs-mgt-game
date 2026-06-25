use crate::model::{
  CompetitiveCommand, CompetitiveHistory, CompetitiveRuleset, CompetitiveTransition,
  CompetitiveWorldState, Difficulty, InvestDomain, MonitorTarget, PledgeType, RecruitRole,
  SystemMonthlyBatch, default_competitive_ruleset,
};
use crate::sim::{resolve_monthly_batches, transition_competitive};

pub fn month1_preset_batches(difficulty: Difficulty) -> Vec<SystemMonthlyBatch> {
  let mut batches = vec![
    SystemMonthlyBatch {
      system_id: 0,
      commands: vec![
        CompetitiveCommand::Hold,
        CompetitiveCommand::Monitor {
          target: MonitorTarget::Northlake,
          depth: 1,
        },
      ],
    },
    SystemMonthlyBatch {
      system_id: 1,
      commands: vec![
        CompetitiveCommand::Invest {
          domain: InvestDomain::Beds,
          amount: 25,
        },
        CompetitiveCommand::Recruit {
          role: RecruitRole::Nurse,
          headcount: 2,
        },
      ],
    },
  ];

  if difficulty.k_rivals() >= 2 {
    batches.push(SystemMonthlyBatch {
      system_id: 2,
      commands: vec![CompetitiveCommand::Commit {
        pledge_type: PledgeType::Access,
        level: 2,
      }],
    });
  }
  if difficulty.k_rivals() >= 3 {
    batches.push(SystemMonthlyBatch {
      system_id: 3,
      commands: vec![CompetitiveCommand::Hold],
    });
  }
  if difficulty.k_rivals() >= 4 {
    batches.push(SystemMonthlyBatch {
      system_id: 4,
      commands: vec![CompetitiveCommand::Hold],
    });
  }

  batches
}

pub fn resolve_preset_month1(
  prior: &CompetitiveWorldState,
  ruleset: &CompetitiveRuleset,
) -> Result<CompetitiveTransition, crate::model::CompetitiveValidationError> {
  let batches = month1_preset_batches(prior.difficulty);
  let aggregated = resolve_monthly_batches(prior, &batches, ruleset)?;
  transition_competitive(prior, aggregated, ruleset)
}

pub fn build_month1_resolution_history(
  difficulty: Difficulty,
) -> Result<CompetitiveHistory, crate::model::CompetitiveValidationError> {
  let ruleset = default_competitive_ruleset();
  let genesis = crate::competitive::genesis_competitive_world_with_ruleset(difficulty, &ruleset);
  let transition = resolve_preset_month1(&genesis, &ruleset)?;
  Ok(CompetitiveHistory {
    genesis,
    transitions: vec![transition],
  })
}

pub fn resolution_summary_lines(transition: &CompetitiveTransition) -> Vec<String> {
  let mut lines = vec![
    format!(
      "Month {} resolved → Year {}, Month {} (turn {})",
      transition.prior.policy_calendar.month_index,
      transition.next.policy_calendar.year,
      transition.next.policy_calendar.month_in_year,
      transition.next.turn
    ),
    format!(
      "Public actions logged: {}",
      transition
        .next
        .public_action_log
        .iter()
        .filter(|entry| entry.month_index == transition.prior.policy_calendar.month_index)
        .count()
    ),
    format!(
      "Pending effects queued: {}",
      transition.next.effect_queue.len()
    ),
    format!("State hash: {}", transition.state_hash),
  ];

  for event in &transition.events {
    lines.push(format!("  • {}", event.description));
  }

  lines
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::model::Difficulty;

  #[test]
  fn preset_batches_match_system_count_per_difficulty() {
    for difficulty in [
      Difficulty::Easy,
      Difficulty::Normal,
      Difficulty::Hard,
      Difficulty::Expert,
    ] {
      let batches = month1_preset_batches(difficulty);
      assert_eq!(batches.len(), (difficulty.k_rivals() + 1) as usize);
    }
  }

  #[test]
  fn resolve_preset_month1_succeeds_for_normal() {
    let ruleset = default_competitive_ruleset();
    let genesis =
      crate::competitive::genesis_competitive_world_with_ruleset(Difficulty::Normal, &ruleset);
    let transition = resolve_preset_month1(&genesis, &ruleset).expect("resolve");
    assert_eq!(transition.next.turn, 1);
  }
}
