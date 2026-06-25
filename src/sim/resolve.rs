use crate::model::{
  AggregatedMonthlyActions, CompetitiveRuleset, CompetitiveValidationError, CompetitiveWorldState,
  SystemMonthlyBatch,
};

use super::validate_competitive::validate_competitive_batch;

pub fn resolve_monthly_batches(
  prior: &CompetitiveWorldState,
  batches: &[SystemMonthlyBatch],
  ruleset: &CompetitiveRuleset,
) -> Result<AggregatedMonthlyActions, CompetitiveValidationError> {
  if batches.len() != prior.systems.len() {
    return Err(CompetitiveValidationError::BatchCountMismatch {
      expected: prior.systems.len() as u32,
      provided: batches.len() as u32,
    });
  }

  let mut sorted = batches.to_vec();
  sorted.sort_by_key(|batch| batch.system_id);

  for batch in &sorted {
    let system = prior
      .systems
      .iter()
      .find(|system| system.system_id == batch.system_id)
      .ok_or(CompetitiveValidationError::UnknownSystemId {
        system_id: batch.system_id,
      })?;
    validate_competitive_batch(&batch.commands, &system.resources, ruleset)?;
  }

  Ok(AggregatedMonthlyActions {
    month_index: prior.policy_calendar.month_index,
    batches: sorted,
  })
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::competitive::genesis_competitive_world;
  use crate::model::{
    CompetitiveCommand, Difficulty, InvestDomain, MonitorTarget, PledgeType, RecruitRole,
    default_competitive_ruleset,
  };

  fn month1_preset_batches() -> Vec<SystemMonthlyBatch> {
    vec![
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
        rationale: None,
      },
      SystemMonthlyBatch {
        system_id: 0,
        commands: vec![
          CompetitiveCommand::Hold,
          CompetitiveCommand::Monitor {
            target: MonitorTarget::Northlake,
            depth: 1,
          },
        ],
        rationale: None,
      },
      SystemMonthlyBatch {
        system_id: 2,
        commands: vec![CompetitiveCommand::Commit {
          pledge_type: PledgeType::Access,
          level: 2,
        }],
        rationale: None,
      },
    ]
  }

  #[test]
  fn resolver_sorts_batches_by_system_id() {
    let prior = genesis_competitive_world(Difficulty::Normal);
    let ruleset = default_competitive_ruleset();
    let aggregated =
      resolve_monthly_batches(&prior, &month1_preset_batches(), &ruleset).expect("resolve");
    assert_eq!(aggregated.batches[0].system_id, 0);
    assert_eq!(aggregated.batches[1].system_id, 1);
    assert_eq!(aggregated.batches[2].system_id, 2);
    assert_eq!(aggregated.month_index, 1);
  }

  #[test]
  fn resolver_rejects_unknown_system_id() {
    let prior = genesis_competitive_world(Difficulty::Easy);
    let ruleset = default_competitive_ruleset();
    let batches = vec![
      SystemMonthlyBatch {
        system_id: 0,
        commands: vec![CompetitiveCommand::Hold],
        rationale: None,
      },
      SystemMonthlyBatch {
        system_id: 9,
        commands: vec![CompetitiveCommand::Hold],
        rationale: None,
      },
    ];
    assert!(matches!(
      resolve_monthly_batches(&prior, &batches, &ruleset),
      Err(CompetitiveValidationError::UnknownSystemId { system_id: 9 })
    ));
  }

  #[test]
  fn resolver_rejects_batch_count_mismatch() {
    let prior = genesis_competitive_world(Difficulty::Normal);
    let ruleset = default_competitive_ruleset();
    let batches = vec![SystemMonthlyBatch {
      system_id: 0,
      commands: vec![CompetitiveCommand::Hold],
      rationale: None,
    }];
    assert!(matches!(
      resolve_monthly_batches(&prior, &batches, &ruleset),
      Err(CompetitiveValidationError::BatchCountMismatch { .. })
    ));
  }
}
