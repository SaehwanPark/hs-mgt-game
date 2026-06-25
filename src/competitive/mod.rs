mod fixtures;
mod genesis;

pub use fixtures::{mock_observation_annual_month, mock_observation_month1};
pub use genesis::{
  genesis_competitive_world, genesis_competitive_world_with_ruleset, genesis_roster_lines,
};

use crate::model::{
  CompetitiveCommand, InvestDomain, MonitorTarget, PayerId, PledgeType, ProjectKind, RatePosture,
  RecruitRole,
};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct ValidationDemo {
  pub id: u32,
  pub label: &'static str,
  pub commands: &'static [CompetitiveCommand],
  pub political_capital_override: Option<u32>,
}

pub const VALIDATION_DEMOS: &[ValidationDemo] = &[
  ValidationDemo {
    id: 1,
    label: "hold + monitor northlake depth=1 (valid, 1 AP)",
    commands: &[
      CompetitiveCommand::Hold,
      CompetitiveCommand::Monitor {
        target: MonitorTarget::Northlake,
        depth: 1,
      },
    ],
    political_capital_override: None,
  },
  ValidationDemo {
    id: 2,
    label: "invest + recruit + negotiate + commit (AP budget exceeded)",
    commands: &[
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
    ],
    political_capital_override: None,
  },
  ValidationDemo {
    id: 3,
    label: "invest beds 40 + recruit nurse x5 (insufficient cash at genesis)",
    commands: &[
      CompetitiveCommand::Invest {
        domain: InvestDomain::Beds,
        amount: 40,
      },
      CompetitiveCommand::Recruit {
        role: RecruitRole::Nurse,
        headcount: 5,
      },
    ],
    political_capital_override: None,
  },
  ValidationDemo {
    id: 4,
    label: "negotiate + commit (political capital exceeded at low PC)",
    commands: &[
      CompetitiveCommand::Negotiate {
        payer: PayerId::CarrierB,
        rate_posture: RatePosture::Conservative,
      },
      CompetitiveCommand::Commit {
        pledge_type: PledgeType::Access,
        level: 1,
      },
    ],
    political_capital_override: Some(2),
  },
  ValidationDemo {
    id: 5,
    label: "project ehr_epic budget=60 (valid, 2 AP + 5 cash draw)",
    commands: &[CompetitiveCommand::Project {
      kind: ProjectKind::EhrEpic,
      budget: 60,
    }],
    political_capital_override: None,
  },
];

pub fn validation_demo_by_id(id: u32) -> Option<&'static ValidationDemo> {
  VALIDATION_DEMOS.iter().find(|demo| demo.id == id)
}

pub fn validation_resources_for_demo(
  demo_id: u32,
  difficulty: crate::model::Difficulty,
  ruleset: &crate::model::CompetitiveRuleset,
) -> crate::model::PlayerResources {
  let mut resources = crate::model::PlayerResources::genesis(difficulty, ruleset);
  if let Some(demo) = validation_demo_by_id(demo_id) {
    if let Some(pc) = demo.political_capital_override {
      resources.political_capital = pc;
    }
  }
  resources
}

pub fn validation_demo_menu_lines() -> Vec<String> {
  VALIDATION_DEMOS
    .iter()
    .map(|demo| format!("  {} — {}", demo.id, demo.label))
    .collect()
}
