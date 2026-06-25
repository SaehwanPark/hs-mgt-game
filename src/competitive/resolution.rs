use crate::model::{
  CompetitiveCommand, CompetitiveHistory, CompetitiveRuleset, CompetitiveTransition,
  CompetitiveWorldState, Difficulty, InvestDomain, MonitorTarget, PayerId, PlayerController,
  PledgeType, RatePosture, RecruitRole, SystemMonthlyBatch, default_competitive_ruleset,
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
      rationale: None,
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
      rationale: Some("AI (growth) invested in beds and recruited nurses".to_string()),
    },
  ];

  if difficulty.k_rivals() >= 2 {
    batches.push(SystemMonthlyBatch {
      system_id: 2,
      commands: vec![CompetitiveCommand::Commit {
        pledge_type: PledgeType::Access,
        level: 2,
      }],
      rationale: Some("AI (access) issued an access pledge".to_string()),
    });
  }
  if difficulty.k_rivals() >= 3 {
    batches.push(SystemMonthlyBatch {
      system_id: 3,
      commands: vec![CompetitiveCommand::Hold],
      rationale: Some("AI (margin) held to preserve flexibility".to_string()),
    });
  }
  if difficulty.k_rivals() >= 4 {
    batches.push(SystemMonthlyBatch {
      system_id: 4,
      commands: vec![CompetitiveCommand::Hold],
      rationale: Some("AI (political) held to preserve capital".to_string()),
    });
  }

  batches
}

pub fn month1_batches_with_ai(
  prior: &CompetitiveWorldState,
  ruleset: &CompetitiveRuleset,
  seed: u64,
) -> Result<Vec<SystemMonthlyBatch>, crate::model::CompetitiveValidationError> {
  let mut batches = Vec::with_capacity(prior.systems.len());
  batches.push(SystemMonthlyBatch {
    system_id: 0,
    commands: vec![
      CompetitiveCommand::Hold,
      CompetitiveCommand::Monitor {
        target: MonitorTarget::Northlake,
        depth: 1,
      },
    ],
    rationale: None,
  });

  for slot in &prior.players {
    let PlayerController::Ai(_) = slot.controller else {
      continue;
    };
    batches.push(compute_ai_batch(slot.system_id, prior, ruleset, seed)?);
  }
  Ok(batches)
}

pub fn compute_ai_batch(
  system_id: u32,
  prior: &CompetitiveWorldState,
  ruleset: &CompetitiveRuleset,
  seed: u64,
) -> Result<SystemMonthlyBatch, crate::model::CompetitiveValidationError> {
  let system = prior
    .systems
    .iter()
    .find(|system| system.system_id == system_id)
    .ok_or(crate::model::CompetitiveValidationError::UnknownSystemId { system_id })?;
  let slot = prior
    .players
    .iter()
    .find(|slot| slot.system_id == system_id)
    .ok_or(crate::model::CompetitiveValidationError::UnknownSystemId { system_id })?;
  let PlayerController::Ai(profile) = slot.controller else {
    return Ok(SystemMonthlyBatch {
      system_id,
      commands: vec![CompetitiveCommand::Hold],
      rationale: Some("Non-AI slot fallback to hold".to_string()),
    });
  };

  let response_target = lagged_public_pressure_target(prior, system_id);
  let mut options = vec![
    (
      vec![
        CompetitiveCommand::Invest {
          domain: InvestDomain::Beds,
          amount: 25,
        },
        CompetitiveCommand::Recruit {
          role: RecruitRole::Nurse,
          headcount: 2,
        },
      ],
      "capacity build (beds + nursing hiring)",
      (profile.style.growth * 3 + profile.style.margin) as i64,
    ),
    (
      vec![CompetitiveCommand::Commit {
        pledge_type: PledgeType::Access,
        level: 2,
      }],
      "public access pledge to strengthen trust",
      (profile.style.access * 3 + profile.style.political) as i64,
    ),
    (
      vec![CompetitiveCommand::Negotiate {
        payer: PayerId::CarrierA,
        rate_posture: RatePosture::Aggressive,
      }],
      "private payer negotiation for margin defense",
      (profile.style.margin * 3 + profile.style.growth) as i64,
    ),
    (
      vec![CompetitiveCommand::Monitor {
        target: response_target,
        depth: 1,
      }],
      "monitor rival actions and wait",
      (profile.style.political * 2 + profile.style.access) as i64,
    ),
  ];

  if has_rival_invest_pressure(prior, system_id) {
    options[0].2 += 30;
    options[3].2 += 10;
  }
  if has_rival_access_pressure(prior, system_id) {
    options[1].2 += 30;
    options[2].2 += 10;
  }

  let mut best_idx = 0usize;
  let mut best_score = i64::MIN;
  for (idx, (commands, _, score)) in options.iter().enumerate() {
    if !commands_fit_budget(commands, &system.resources, ruleset) {
      continue;
    }
    let tie_roll = ai_tie_break_roll(
      seed,
      prior.policy_calendar.month_index,
      system_id,
      idx as u32,
    );
    let composite = (*score * 1000) + tie_roll as i64;
    if composite > best_score {
      best_score = composite;
      best_idx = idx;
    }
  }

  let (commands, label, score) = options.swap_remove(best_idx);
  let rationale = format!(
    "AI system {system_id} ({}) selected '{}' using style={} and lagged month-{} public log (score={score}).",
    profile.org_name,
    label,
    profile.style.style_label(),
    prior.policy_calendar.month_index.saturating_sub(1),
  );
  Ok(SystemMonthlyBatch {
    system_id,
    commands,
    rationale: Some(rationale),
  })
}

fn has_rival_invest_pressure(world: &CompetitiveWorldState, system_id: u32) -> bool {
  let lagged = world.policy_calendar.month_index.saturating_sub(1);
  world.public_action_log.iter().any(|entry| {
    entry.month_index == lagged
      && entry.system_id != system_id
      && entry.summary.to_lowercase().contains("invest")
  })
}

fn has_rival_access_pressure(world: &CompetitiveWorldState, system_id: u32) -> bool {
  let lagged = world.policy_calendar.month_index.saturating_sub(1);
  world.public_action_log.iter().any(|entry| {
    entry.month_index == lagged
      && entry.system_id != system_id
      && (entry.summary.to_lowercase().contains("access")
        || entry.summary.to_lowercase().contains("pledge"))
  })
}

fn lagged_public_pressure_target(world: &CompetitiveWorldState, system_id: u32) -> MonitorTarget {
  let lagged = world.policy_calendar.month_index.saturating_sub(1);
  let mut counts = [0u32; 5];
  for entry in &world.public_action_log {
    if entry.month_index == lagged
      && entry.system_id != system_id
      && (entry.system_id as usize) < counts.len()
    {
      counts[entry.system_id as usize] += 1;
    }
  }
  let mut best_id = 1u32;
  let mut best_count = 0u32;
  for candidate in [1u32, 2, 3, 4] {
    let c = counts[candidate as usize];
    if c > best_count {
      best_count = c;
      best_id = candidate;
    }
  }
  match best_id {
    2 => MonitorTarget::Summit,
    3 => MonitorTarget::Valley,
    4 => MonitorTarget::Metro,
    _ => MonitorTarget::Northlake,
  }
}

fn commands_fit_budget(
  commands: &[CompetitiveCommand],
  resources: &crate::model::PlayerResources,
  ruleset: &CompetitiveRuleset,
) -> bool {
  crate::sim::validate_competitive_batch(commands, resources, ruleset).is_ok()
}

fn ai_tie_break_roll(seed: u64, month_index: u32, system_id: u32, option_idx: u32) -> u32 {
  let stream_id = ai_stream_id(system_id);
  let base = seed
    .wrapping_add((month_index as u64).wrapping_mul(0x517c_c1b7_2722_0a95))
    .wrapping_add((stream_id as u64).wrapping_mul(0x6c62_272e_07bb_0142))
    .wrapping_add((option_idx as u64).wrapping_mul(0x9e37_79b9_7f4a_7c15));
  splitmix64(base) as u32
}

fn ai_stream_id(system_id: u32) -> u32 {
  // Named stream mapping: ai_player_{id} -> stable numeric stream id.
  10_000 + system_id
}

fn splitmix64(mut z: u64) -> u64 {
  z = z.wrapping_add(0x9e37_79b9_7f4a_7c15);
  z = (z ^ (z >> 30)).wrapping_mul(0xbf58_476d_1ce4_e5b9);
  z = (z ^ (z >> 27)).wrapping_mul(0x94d0_49bb_1331_11eb);
  z ^ (z >> 31)
}

pub fn resolve_preset_month1(
  prior: &CompetitiveWorldState,
  ruleset: &CompetitiveRuleset,
  seed: u64,
) -> Result<CompetitiveTransition, crate::model::CompetitiveValidationError> {
  let batches = month1_batches_with_ai(prior, ruleset, seed)?;
  let aggregated = resolve_monthly_batches(prior, &batches, ruleset)?;
  transition_competitive(prior, aggregated, ruleset)
}

pub fn build_month1_resolution_history(
  difficulty: Difficulty,
  seed: u64,
) -> Result<CompetitiveHistory, crate::model::CompetitiveValidationError> {
  let ruleset = default_competitive_ruleset();
  let genesis = crate::competitive::genesis_competitive_world_with_ruleset(difficulty, &ruleset);
  let transition = resolve_preset_month1(&genesis, &ruleset, seed)?;
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
    let transition = resolve_preset_month1(&genesis, &ruleset, 42).expect("resolve");
    assert_eq!(transition.next.turn, 1);
  }
}
