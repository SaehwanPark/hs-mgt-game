use super::CompetitiveCommand;

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct SystemMonthlyBatch {
  pub system_id: u32,
  pub commands: Vec<CompetitiveCommand>,
  pub rationale: Option<String>,
}

impl SystemMonthlyBatch {
  pub fn new(system_id: u32, commands: Vec<CompetitiveCommand>) -> Self {
    Self {
      system_id,
      commands,
      rationale: None,
    }
  }

  pub fn with_rationale(
    system_id: u32,
    commands: Vec<CompetitiveCommand>,
    rationale: impl Into<String>,
  ) -> Self {
    Self {
      system_id,
      commands,
      rationale: Some(rationale.into()),
    }
  }
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct AggregatedMonthlyActions {
  pub month_index: u32,
  pub batches: Vec<SystemMonthlyBatch>,
}

impl AggregatedMonthlyActions {
  pub fn batch_for_system(&self, system_id: u32) -> Option<&SystemMonthlyBatch> {
    self
      .batches
      .iter()
      .find(|batch| batch.system_id == system_id)
  }
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::model::{InvestDomain, MonitorTarget};

  #[test]
  fn aggregated_actions_exposes_batch_by_system_id() {
    let aggregated = AggregatedMonthlyActions {
      month_index: 1,
      batches: vec![
        SystemMonthlyBatch {
          system_id: 0,
          commands: vec![CompetitiveCommand::Hold],
          rationale: None,
        },
        SystemMonthlyBatch {
          system_id: 1,
          commands: vec![CompetitiveCommand::Monitor {
            target: MonitorTarget::Northlake,
            depth: 1,
          }],
          rationale: Some("AI selected monitor action".to_string()),
        },
      ],
    };

    assert!(aggregated.batch_for_system(0).is_some());
    assert!(aggregated.batch_for_system(2).is_none());
    assert_eq!(
      aggregated
        .batch_for_system(1)
        .expect("batch")
        .commands
        .len(),
      1
    );
  }

  #[test]
  fn system_monthly_batch_stores_commands() {
    let batch = SystemMonthlyBatch {
      system_id: 0,
      commands: vec![CompetitiveCommand::Invest {
        domain: InvestDomain::Beds,
        amount: 20,
      }],
      rationale: None,
    };
    assert_eq!(batch.commands.len(), 1);
  }
}
