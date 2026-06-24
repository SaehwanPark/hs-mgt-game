use crate::model::{PlayerCommand, Ruleset, ValidationError};

pub fn validate_command(command: &PlayerCommand, ruleset: &Ruleset) -> Result<(), ValidationError> {
  match command {
    PlayerCommand::StabilizeAccess {
      add_staffed_beds,
      capital_spend,
      requested_commercial_rate: _,
    } => {
      if *add_staffed_beds <= 0 {
        return Err(ValidationError::NonPositiveCapacityChange);
      }

      if *capital_spend < 0 {
        return Err(ValidationError::NegativeCapitalSpend {
          requested: *capital_spend,
        });
      }

      if *capital_spend > ruleset.max_capital_spend {
        return Err(ValidationError::CapitalSpendTooHigh {
          requested: *capital_spend,
          available_limit: ruleset.max_capital_spend,
        });
      }
    }
    PlayerCommand::RespondToStateAccessMandate {
      advocacy_spend,
      access_commitment,
    } => {
      if *advocacy_spend < 0 {
        return Err(ValidationError::NegativeAdvocacySpend {
          requested: *advocacy_spend,
        });
      }

      if *advocacy_spend > ruleset.max_advocacy_spend {
        return Err(ValidationError::AdvocacySpendTooHigh {
          requested: *advocacy_spend,
          available_limit: ruleset.max_advocacy_spend,
        });
      }

      if *access_commitment <= 0 {
        return Err(ValidationError::NonPositiveAccessCommitment);
      }
    }
    PlayerCommand::RespondToWorkforcePressure {
      retention_spend,
      schedule_relief_commitment,
    } => {
      if *retention_spend < 0 {
        return Err(ValidationError::NegativeRetentionSpend {
          requested: *retention_spend,
        });
      }

      if *retention_spend > ruleset.max_retention_spend {
        return Err(ValidationError::RetentionSpendTooHigh {
          requested: *retention_spend,
          available_limit: ruleset.max_retention_spend,
        });
      }

      if *schedule_relief_commitment <= 0 {
        return Err(ValidationError::NonPositiveScheduleRelief);
      }

      if *schedule_relief_commitment > ruleset.max_schedule_relief_commitment {
        return Err(ValidationError::ScheduleReliefTooHigh {
          requested: *schedule_relief_commitment,
          available_limit: ruleset.max_schedule_relief_commitment,
        });
      }
    }
    PlayerCommand::JoinRegionalAccessCoalition {
      coalition_investment,
      shared_access_commitment,
    } => {
      if *coalition_investment < 0 {
        return Err(ValidationError::NegativeCoalitionInvestment {
          requested: *coalition_investment,
        });
      }

      if *coalition_investment > ruleset.max_coalition_investment {
        return Err(ValidationError::CoalitionInvestmentTooHigh {
          requested: *coalition_investment,
          available_limit: ruleset.max_coalition_investment,
        });
      }

      if *shared_access_commitment <= 0 {
        return Err(ValidationError::NonPositiveSharedAccessCommitment);
      }

      if *shared_access_commitment > ruleset.max_shared_access_commitment {
        return Err(ValidationError::SharedAccessCommitmentTooHigh {
          requested: *shared_access_commitment,
          available_limit: ruleset.max_shared_access_commitment,
        });
      }
    }
    PlayerCommand::RespondToCompetitorCapacityMove {
      defensive_capital_commitment,
      access_posture,
    } => {
      if *defensive_capital_commitment < 0 {
        return Err(ValidationError::NegativeDefensiveCapitalCommitment {
          requested: *defensive_capital_commitment,
        });
      }

      if *defensive_capital_commitment > ruleset.max_defensive_capital_commitment {
        return Err(ValidationError::DefensiveCapitalCommitmentTooHigh {
          requested: *defensive_capital_commitment,
          available_limit: ruleset.max_defensive_capital_commitment,
        });
      }

      if *access_posture <= 0 {
        return Err(ValidationError::NonPositiveAccessPosture);
      }

      if *access_posture > ruleset.max_access_posture {
        return Err(ValidationError::AccessPostureTooHigh {
          requested: *access_posture,
          available_limit: ruleset.max_access_posture,
        });
      }
    }
  }

  Ok(())
}

pub fn requested_commercial_rate(command: &PlayerCommand) -> Option<i32> {
  match command {
    PlayerCommand::StabilizeAccess {
      requested_commercial_rate,
      ..
    } => Some(*requested_commercial_rate),
    PlayerCommand::RespondToStateAccessMandate { .. } => None,
    PlayerCommand::RespondToWorkforcePressure { .. } => None,
    PlayerCommand::JoinRegionalAccessCoalition { .. } => None,
    PlayerCommand::RespondToCompetitorCapacityMove { .. } => None,
  }
}
