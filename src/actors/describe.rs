use crate::model::{
  ActorDecision, CoalitionDecision, CompetitorDecision, InsurerDecision, LaborDecision,
  StatePolicyDecision,
};

pub fn describe_actor_decision(decision: &ActorDecision) -> String {
  match decision {
    ActorDecision::Insurer(InsurerDecision::Accept) => "accept".to_string(),
    ActorDecision::Insurer(InsurerDecision::Counter { offered_rate }) => {
      format!("counter at {offered_rate}")
    }
    ActorDecision::Insurer(InsurerDecision::Reject) => "reject".to_string(),
    ActorDecision::StatePolicy(StatePolicyDecision::GrantFlexibility) => {
      "grant flexibility".to_string()
    }
    ActorDecision::StatePolicy(StatePolicyDecision::ProceedWithMandate) => {
      "proceed with mandate".to_string()
    }
    ActorDecision::StatePolicy(StatePolicyDecision::EscalateOversight) => {
      "escalate oversight".to_string()
    }
    ActorDecision::Labor(LaborDecision::Cooperative) => "cooperative".to_string(),
    ActorDecision::Labor(LaborDecision::LimitedSupport) => "limited support".to_string(),
    ActorDecision::Labor(LaborDecision::WorkAction) => "work action".to_string(),
    ActorDecision::Coalition(CoalitionDecision::FullPartnership) => "full partnership".to_string(),
    ActorDecision::Coalition(CoalitionDecision::LimitedParticipation) => {
      "limited participation".to_string()
    }
    ActorDecision::Coalition(CoalitionDecision::CoalitionWithdrawal) => {
      "coalition withdrawal".to_string()
    }
    ActorDecision::Competitor(CompetitorDecision::AccelerateExpansion) => {
      "accelerate expansion".to_string()
    }
    ActorDecision::Competitor(CompetitorDecision::HoldPosition) => "hold position".to_string(),
    ActorDecision::Competitor(CompetitorDecision::PartialRetreat) => "partial retreat".to_string(),
  }
}
