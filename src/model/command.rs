#[derive(Clone, Debug, PartialEq, Eq)]
pub enum PlayerCommand {
  StabilizeAccess {
    add_staffed_beds: i32,
    capital_spend: i32,
    requested_commercial_rate: i32,
  },
  RespondToStateAccessMandate {
    advocacy_spend: i32,
    access_commitment: i32,
  },
  RespondToWorkforcePressure {
    retention_spend: i32,
    schedule_relief_commitment: i32,
  },
  JoinRegionalAccessCoalition {
    coalition_investment: i32,
    shared_access_commitment: i32,
  },
  RespondToCompetitorCapacityMove {
    defensive_capital_commitment: i32,
    access_posture: i32,
  },
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ValidationError {
  NonPositiveCapacityChange,
  NegativeCapitalSpend {
    requested: i32,
  },
  CapitalSpendTooHigh {
    requested: i32,
    available_limit: i32,
  },
  NegativeAdvocacySpend {
    requested: i32,
  },
  AdvocacySpendTooHigh {
    requested: i32,
    available_limit: i32,
  },
  NonPositiveAccessCommitment,
  NegativeRetentionSpend {
    requested: i32,
  },
  RetentionSpendTooHigh {
    requested: i32,
    available_limit: i32,
  },
  NonPositiveScheduleRelief,
  ScheduleReliefTooHigh {
    requested: i32,
    available_limit: i32,
  },
  NegativeCoalitionInvestment {
    requested: i32,
  },
  CoalitionInvestmentTooHigh {
    requested: i32,
    available_limit: i32,
  },
  NonPositiveSharedAccessCommitment,
  SharedAccessCommitmentTooHigh {
    requested: i32,
    available_limit: i32,
  },
  NegativeDefensiveCapitalCommitment {
    requested: i32,
  },
  DefensiveCapitalCommitmentTooHigh {
    requested: i32,
    available_limit: i32,
  },
  NonPositiveAccessPosture,
  AccessPostureTooHigh {
    requested: i32,
    available_limit: i32,
  },
}
