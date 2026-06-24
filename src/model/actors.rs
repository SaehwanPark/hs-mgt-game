#[derive(Clone, Debug, PartialEq, Eq)]
pub enum InsurerDecision {
  Accept,
  Counter { offered_rate: i32 },
  Reject,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum StatePolicyDecision {
  GrantFlexibility,
  ProceedWithMandate,
  EscalateOversight,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum LaborDecision {
  Cooperative,
  LimitedSupport,
  WorkAction,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum CoalitionDecision {
  FullPartnership,
  LimitedParticipation,
  CoalitionWithdrawal,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ActorDecision {
  Insurer(InsurerDecision),
  StatePolicy(StatePolicyDecision),
  Labor(LaborDecision),
  Coalition(CoalitionDecision),
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ActorDecisionRecord {
  pub actor: &'static str,
  pub decision: ActorDecision,
  pub rationale: String,
}
