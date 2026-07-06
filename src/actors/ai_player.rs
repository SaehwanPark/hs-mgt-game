use crate::inputs::ai_player_tie_break;
use crate::model::{
  AiProfile, AiStyleWeights, CompetitiveCommand, CompetitiveRuleset, InvestDomain, MonitorTarget,
  PayerId, PledgeType, RatePosture, RecruitRole, SystemMonthlyBatch,
};
use crate::sim::{AiPlayerObservation, LaggedRivalAction, validate_competitive_batch};

const SATISFICING_MARGIN: i32 = 5;

pub fn compute_ai_batch(
  observation: &AiPlayerObservation,
  profile: &AiProfile,
  resources: &crate::model::PlayerResources,
  ruleset: &CompetitiveRuleset,
  seed: u64,
) -> SystemMonthlyBatch {
  let candidates = generate_candidates(observation, profile.style);
  let mut scored: Vec<(CompetitiveCommand, i32)> = candidates
    .into_iter()
    .filter_map(|command| {
      let batch = vec![command];
      if validate_competitive_batch(&batch, resources, ruleset).is_err() {
        return None;
      }
      Some((command, score_command(&command, profile.style, observation)))
    })
    .collect();

  if scored.is_empty() {
    return SystemMonthlyBatch::with_rationale(
      observation.system_id,
      vec![CompetitiveCommand::Hold],
      format!(
        "{} ({}) — no feasible candidates; holding.",
        profile.org_name,
        profile.style.style_label()
      ),
    );
  }

  scored.sort_by(|left, right| {
    right
      .1
      .cmp(&left.1)
      .then_with(|| format!("{:?}", left.0).cmp(&format!("{:?}", right.0)))
  });

  let style_primary = style_primary_command(profile.style);
  let style_score = score_command(&style_primary, profile.style, observation);
  let best_score = scored[0].1;

  let chosen = if scored.iter().any(|(cmd, _)| *cmd == style_primary)
    && best_score.saturating_sub(style_score) <= SATISFICING_MARGIN
  {
    style_primary
  } else {
    pick_among_tied_top(
      &scored,
      seed,
      observation.month_index,
      observation.system_id,
    )
  };

  let runner_up = scored
    .iter()
    .find(|(cmd, _)| *cmd != chosen)
    .map(|(cmd, score)| format!("{cmd:?} (score {score})"))
    .unwrap_or_else(|| "none".to_string());

  let rival_context = if observation.lagged_rival_actions.is_empty() {
    "no lagged public rival moves".to_string()
  } else {
    observation
      .lagged_rival_actions
      .iter()
      .map(|action| format!("{}: {}", action.rival_name, action.summary))
      .collect::<Vec<_>>()
      .join("; ")
  };

  let rationale = format!(
    "{} ({}) — observed: {rival_context}. Top candidate {:?} (score {best_score}); runner-up {runner_up}. Chose {:?} via satisficing/best-response.",
    profile.org_name,
    profile.style.style_label(),
    scored[0].0,
    chosen
  );

  SystemMonthlyBatch::with_rationale(observation.system_id, vec![chosen], rationale)
}

fn pick_among_tied_top(
  scored: &[(CompetitiveCommand, i32)],
  seed: u64,
  month_index: u32,
  system_id: u32,
) -> CompetitiveCommand {
  let top_score = scored[0].1;
  let tied: Vec<CompetitiveCommand> = scored
    .iter()
    .filter(|(_, score)| *score == top_score)
    .map(|(cmd, _)| *cmd)
    .collect();

  if tied.len() == 1 {
    return tied[0];
  }

  let index = (ai_player_tie_break(seed, month_index, system_id) as usize) % tied.len();
  tied[index]
}

fn generate_candidates(
  observation: &AiPlayerObservation,
  style: AiStyleWeights,
) -> Vec<CompetitiveCommand> {
  let mut candidates = vec![
    CompetitiveCommand::Hold,
    style_primary_command(style),
    CompetitiveCommand::Monitor {
      target: default_monitor_target(observation.system_id),
      depth: 1,
    },
  ];

  for action in &observation.lagged_rival_actions {
    candidates.extend(best_response_commands(action));
  }

  if !observation.intel_gaps.is_empty() {
    candidates.push(CompetitiveCommand::Monitor {
      target: default_monitor_target(observation.system_id),
      depth: 2,
    });
  }

  // Generate recruitment candidates for understaffed roles
  let target_nurses = (observation.staffed_beds + 4) / 5
    + (observation.emergency_capacity + 1) / 2
    + observation.icu_capacity
    + (observation.obstetrics_capacity + 1) / 2
    + (observation.psychiatric_capacity + 3) / 4
    + (observation.cardiology_capacity + 2) / 3
    + (observation.oncology_capacity + 2) / 3
    + (observation.infusion_capacity + 3) / 4
    + (observation.neurology_capacity + 2) / 3;
  let target_physicians = (observation.outpatient_capacity + 9) / 10
    + (observation.emergency_capacity + 3) / 4
    + (observation.icu_capacity + 1) / 2
    + (observation.obstetrics_capacity + 4) / 5
    + (observation.psychiatric_capacity + 9) / 10
    + (observation.cardiology_capacity + 7) / 8
    + (observation.oncology_capacity + 7) / 8
    + (observation.infusion_capacity + 14) / 15
    + (observation.neurology_capacity + 5) / 6;
  let target_admins = (observation.staffed_beds + observation.outpatient_capacity + 19) / 20
    + (observation.emergency_capacity + 9) / 10
    + (observation.icu_capacity + 4) / 5
    + (observation.obstetrics_capacity + 9) / 10
    + (observation.psychiatric_capacity + 14) / 15
    + (observation.cardiology_capacity + 11) / 12
    + (observation.oncology_capacity + 11) / 12
    + (observation.infusion_capacity + 19) / 20
    + (observation.neurology_capacity + 9) / 10;

  if observation.nurses < target_nurses {
    let diff = (target_nurses - observation.nurses) as u32;
    for headcount in [1, 2, 3] {
      if headcount <= diff {
        candidates.push(CompetitiveCommand::Recruit {
          role: RecruitRole::Nurse,
          headcount,
        });
      }
    }
  }

  if observation.physicians < target_physicians {
    let diff = (target_physicians - observation.physicians) as u32;
    for headcount in [1, 2, 3] {
      if headcount <= diff {
        candidates.push(CompetitiveCommand::Recruit {
          role: RecruitRole::Physician,
          headcount,
        });
      }
    }
  }

  if observation.admins < target_admins {
    let diff = (target_admins - observation.admins) as u32;
    for headcount in [1, 2, 3] {
      if headcount <= diff {
        candidates.push(CompetitiveCommand::Recruit {
          role: RecruitRole::Admin,
          headcount,
        });
      }
    }
  }

  candidates.sort_by_key(|command| format!("{command:?}"));
  candidates.dedup();
  candidates
}

fn style_primary_command(style: AiStyleWeights) -> CompetitiveCommand {
  match style.style_label() {
    "growth" => CompetitiveCommand::Invest {
      domain: InvestDomain::Beds,
      amount: 25,
    },
    "margin" => CompetitiveCommand::Negotiate {
      payer: PayerId::CarrierA,
      rate_posture: RatePosture::Aggressive,
    },
    "access" => CompetitiveCommand::Commit {
      pledge_type: PledgeType::Access,
      level: 2,
    },
    "political" => CompetitiveCommand::Commit {
      pledge_type: PledgeType::Quality,
      level: 2,
    },
    _ => CompetitiveCommand::Hold,
  }
}

fn best_response_commands(action: &LaggedRivalAction) -> Vec<CompetitiveCommand> {
  let summary = action.summary.to_ascii_lowercase();
  if summary.contains("investing") && summary.contains("beds") {
    return vec![
      CompetitiveCommand::Invest {
        domain: InvestDomain::Beds,
        amount: 20,
      },
      CompetitiveCommand::Recruit {
        role: RecruitRole::Nurse,
        headcount: 2,
      },
    ];
  }
  if summary.contains("investing") && summary.contains("emergency") {
    return vec![
      CompetitiveCommand::Invest {
        domain: InvestDomain::Emergency,
        amount: 30,
      },
      CompetitiveCommand::Recruit {
        role: RecruitRole::Nurse,
        headcount: 2,
      },
      CompetitiveCommand::Recruit {
        role: RecruitRole::Physician,
        headcount: 1,
      },
    ];
  }
  if summary.contains("investing") && (summary.contains("icu") || summary.contains("icuwing")) {
    return vec![
      CompetitiveCommand::Invest {
        domain: InvestDomain::Icu,
        amount: 30,
      },
      CompetitiveCommand::Recruit {
        role: RecruitRole::Nurse,
        headcount: 2,
      },
      CompetitiveCommand::Recruit {
        role: RecruitRole::Physician,
        headcount: 1,
      },
    ];
  }
  if summary.contains("pledge") && summary.contains("access") {
    return vec![
      CompetitiveCommand::Commit {
        pledge_type: PledgeType::Access,
        level: 2,
      },
      CompetitiveCommand::Invest {
        domain: InvestDomain::Outpatient,
        amount: 15,
      },
    ];
  }
  if summary.contains("recruiting") {
    return vec![
      CompetitiveCommand::Recruit {
        role: RecruitRole::Nurse,
        headcount: 2,
      },
      CompetitiveCommand::Invest {
        domain: InvestDomain::Beds,
        amount: 15,
      },
    ];
  }

  vec![]
}

fn default_monitor_target(system_id: u32) -> MonitorTarget {
  match system_id {
    1 => MonitorTarget::Summit,
    2 => MonitorTarget::Northlake,
    3 => MonitorTarget::Northlake,
    _ => MonitorTarget::Northlake,
  }
}

fn score_command(
  command: &CompetitiveCommand,
  style: AiStyleWeights,
  observation: &AiPlayerObservation,
) -> i32 {
  let cash_pressure = if observation.cash < 50 { -8 } else { 0 };
  let base = match command {
    CompetitiveCommand::Hold => (style.margin / 4) as i32,
    CompetitiveCommand::Invest {
      domain: InvestDomain::Beds,
      amount,
    } => {
      (style.growth * 2 + style.access) as i32
        + amount / 10
        + observation.market.regional_demand_index / 20
    }
    CompetitiveCommand::Invest {
      domain: InvestDomain::Outpatient,
      ..
    } => (style.growth + style.access * 2) as i32,
    CompetitiveCommand::Invest {
      domain: InvestDomain::Emergency,
      ..
    } => (style.growth + style.access * 2) as i32,
    CompetitiveCommand::Invest {
      domain: InvestDomain::Icu,
      ..
    } => (style.growth + style.access * 2) as i32,
    CompetitiveCommand::Invest {
      domain: InvestDomain::Obstetrics,
      ..
    } => (style.growth + style.access * 2) as i32,
    CompetitiveCommand::Invest {
      domain: InvestDomain::Psychiatric,
      ..
    } => (style.growth + style.access * 2) as i32,
    CompetitiveCommand::Invest {
      domain: InvestDomain::Cardiology,
      ..
    } => (style.growth + style.access * 2) as i32,
    CompetitiveCommand::Invest {
      domain: InvestDomain::Oncology,
      ..
    } => (style.growth + style.access * 2) as i32,
    CompetitiveCommand::Invest {
      domain: InvestDomain::Infusion,
      ..
    } => (style.growth + style.access * 2) as i32,
    CompetitiveCommand::Invest {
      domain: InvestDomain::Neurology,
      ..
    } => (style.growth + style.access * 2) as i32,
    CompetitiveCommand::Invest {
      domain: InvestDomain::Technology,
      ..
    } => (style.growth + style.margin) as i32,
    CompetitiveCommand::Recruit { headcount, .. } => {
      (style.access + style.growth) as i32 + (*headcount as i32)
    }
    CompetitiveCommand::Commit {
      pledge_type: PledgeType::Access,
      level,
    } => (style.access * 2 + style.political) as i32 + (*level as i32),
    CompetitiveCommand::Commit {
      pledge_type: PledgeType::Quality,
      level,
    } => (style.political * 2 + style.access) as i32 + (*level as i32),
    CompetitiveCommand::Commit {
      pledge_type: PledgeType::Workforce,
      level,
    } => (style.political + style.access) as i32 + (*level as i32),
    CompetitiveCommand::Negotiate { .. } => {
      (style.margin * 2) as i32 + observation.market.commercial_payer_pressure / 10
    }
    CompetitiveCommand::Monitor { depth, .. } => {
      10 + (style.margin / 2) as i32
        + (*depth as i32) * 2
        + if observation.intel_gaps.is_empty() {
          -4
        } else {
          6
        }
    }
    CompetitiveCommand::Project { .. } => (style.growth + style.political) as i32,
  };

  base + cash_pressure
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::competitive::genesis_competitive_world;
  use crate::model::Difficulty;
  use crate::sim::{LaggedRivalAction, ai_profile_for_system, observe_for_ai};

  fn resources_for(system_id: u32) -> crate::model::PlayerResources {
    genesis_competitive_world(Difficulty::Normal).systems[system_id as usize]
      .resources
      .clone()
  }

  #[test]
  fn ai_batch_is_deterministic_for_same_seed() {
    let world = genesis_competitive_world(Difficulty::Normal);
    let ruleset = crate::model::default_competitive_ruleset();
    let profile = ai_profile_for_system(&world, 1).expect("profile");
    let observation = observe_for_ai(&world, 1);
    let resources = resources_for(1);

    let first = compute_ai_batch(&observation, &profile, &resources, &ruleset, 42);
    let second = compute_ai_batch(&observation, &profile, &resources, &ruleset, 42);
    assert_eq!(first, second);
  }

  #[test]
  fn ai_batch_includes_non_empty_rationale() {
    let world = genesis_competitive_world(Difficulty::Normal);
    let ruleset = crate::model::default_competitive_ruleset();
    let profile = ai_profile_for_system(&world, 1).expect("profile");
    let observation = observe_for_ai(&world, 1);
    let resources = resources_for(1);

    let batch = compute_ai_batch(&observation, &profile, &resources, &ruleset, 42);
    let rationale = batch.rationale.expect("rationale");
    assert!(rationale.contains("Northlake"));
    assert!(rationale.contains("growth"));
  }

  #[test]
  fn ai_batch_passes_validation() {
    let world = genesis_competitive_world(Difficulty::Normal);
    let ruleset = crate::model::default_competitive_ruleset();

    for system_id in 1..=world.rival_count() as u32 {
      let profile = ai_profile_for_system(&world, system_id).expect("profile");
      let observation = observe_for_ai(&world, system_id);
      let resources = world.systems[system_id as usize].resources.clone();
      let batch = compute_ai_batch(&observation, &profile, &resources, &ruleset, 42);
      validate_competitive_batch(&batch.commands, &resources, &ruleset).expect("valid batch");
    }
  }

  #[test]
  fn best_response_commands_match_investing_summary() {
    let responses = best_response_commands(&LaggedRivalAction {
      system_id: 1,
      rival_name: "Northlake Health".to_string(),
      summary: "Northlake Health: investing 25 in Beds".to_string(),
    });
    assert!(responses.iter().any(|cmd| matches!(
      cmd,
      CompetitiveCommand::Invest {
        domain: InvestDomain::Beds,
        ..
      }
    )));
  }

  #[test]
  fn test_ai_candidate_generation_includes_neurology_staffing() {
    let mut observation = observe_for_ai(&genesis_competitive_world(Difficulty::Normal), 1);
    // Artificially give neurology capacity of 3 beds (target: 1 nurse, 1 physician, 1 admin)
    observation.neurology_capacity = 3;
    // Set starting staff to 0 so we have an obvious staffing deficit
    observation.nurses = 0;
    observation.physicians = 0;
    observation.admins = 0;
    // Beds and other capacities are set to 0 to isolate neurology staffing deficit
    observation.staffed_beds = 0;
    observation.outpatient_capacity = 0;
    observation.emergency_capacity = 0;
    observation.icu_capacity = 0;
    observation.obstetrics_capacity = 0;
    observation.psychiatric_capacity = 0;
    observation.cardiology_capacity = 0;
    observation.oncology_capacity = 0;
    observation.infusion_capacity = 0;

    let style = AiStyleWeights {
      growth: 1,
      margin: 1,
      access: 1,
      political: 1,
    };
    let candidates = generate_candidates(&observation, style);

    // Verify that recruitment commands for nurse, physician, and admin are generated
    assert!(candidates.iter().any(|cmd| matches!(
      cmd,
      CompetitiveCommand::Recruit {
        role: RecruitRole::Nurse,
        headcount: 1,
      }
    )));
    assert!(candidates.iter().any(|cmd| matches!(
      cmd,
      CompetitiveCommand::Recruit {
        role: RecruitRole::Physician,
        headcount: 1,
      }
    )));
    assert!(candidates.iter().any(|cmd| matches!(
      cmd,
      CompetitiveCommand::Recruit {
        role: RecruitRole::Admin,
        headcount: 1,
      }
    )));
  }
}
