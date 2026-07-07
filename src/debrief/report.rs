use crate::model::{
  AttributedEffect, CompetitiveCommand, CompetitiveHistory, CompetitiveWorldState, Event, History,
  InvestDomain, MonitorTarget, PayerId, PlayerCommand, PledgeType, ProjectKind, RatePosture,
  RecruitRole,
};
use crate::sim::is_public_command;

pub fn educational_debrief(history: &History) -> Vec<String> {
  let Some(last_transition) = history.transitions.last() else {
    return vec!["No committed transitions are available for debriefing.".to_string()];
  };

  let initial = &history.genesis;
  let final_state = &last_transition.next;
  let actor_rationales = history
    .transitions
    .iter()
    .map(|transition| {
      format!(
        "{}: {}",
        transition.actor_decision.actor, transition.actor_decision.rationale
      )
    })
    .collect::<Vec<_>>()
    .join(" | ");

  let effect_summary = history
    .transitions
    .iter()
    .flat_map(|transition| transition.effects.iter())
    .map(|effect| {
      format!(
        "{} changed {} by {}",
        effect.source, effect.metric, effect.delta
      )
    })
    .collect::<Vec<_>>()
    .join("; ");

  let revision_notes = history
    .transitions
    .iter()
    .filter(|transition| transition.observation.prior_access_revision != 0)
    .map(|transition| {
      format!(
        "turn {} revised the prior reported access estimate by {}",
        transition.prior.turn + 1,
        transition.observation.prior_access_revision
      )
    })
    .collect::<Vec<_>>()
    .join("; ");

  let mut lines = vec![
    format!(
      "Run-level tradeoff: cash moved from {} to {}, access from {} to {}, workforce trust from {} to {}, community trust from {} to {}, policy pressure from {} to {}, and commercial rate from {} to {}.",
      initial.cash,
      final_state.cash,
      initial.access_index,
      final_state.access_index,
      initial.workforce_trust,
      final_state.workforce_trust,
      initial.community_trust,
      final_state.community_trust,
      initial.policy_pressure,
      final_state.policy_pressure,
      initial.commercial_rate,
      final_state.commercial_rate
    ),
    format!("Actor rationales at decision time: {actor_rationales}"),
    if effect_summary.is_empty() {
      "Attributed mechanisms to inspect: none.".to_string()
    } else {
      format!("Attributed mechanisms to inspect: {effect_summary}.")
    },
    "Debrief prompt: Was the CEO's access strategy reasonable given the reported access values, the later policy response, the workforce retention tradeoff, the coalition investment choice, and the defensive response to rival capacity pressure?".to_string(),
    "Decision quality and outcome quality are separate: replay preserves what each actor observed and why each modeled response occurred.".to_string(),
  ];

  if !revision_notes.is_empty() {
    lines.push(format!(
      "Observation revision note: {revision_notes}. Prior committed observations remain unchanged in history; revisions affect only the current briefing."
    ));
  }

  // Append the instructor run summary & decision quality review
  lines.extend(instructor_run_summary(history));

  lines
}

pub fn instructor_run_summary(history: &History) -> Vec<String> {
  let mut lines = vec![
    "".to_string(),
    "=== INSTRUCTOR RUN SUMMARY & DECISION QUALITY REVIEW ===".to_string(),
    "Note: This summary distinguishes between player-observed reported metrics and true underlying states to evaluate decision quality vs outcome quality under uncertainty.".to_string(),
  ];

  if history.transitions.is_empty() {
    lines.push("No transitions available.".to_string());
    return lines;
  }

  for (idx, transition) in history.transitions.iter().enumerate() {
    let turn_idx = idx + 1;
    let observed_access = transition.observation.reported_access_index;
    let true_prior_access = transition.prior.access_index;
    let delta = observed_access - true_prior_access;
    let delta_sign = if delta >= 0 {
      format!("+{}", delta)
    } else {
      delta.to_string()
    };

    let cmd_desc = match &transition.command {
      PlayerCommand::StabilizeAccess {
        add_staffed_beds,
        capital_spend,
        requested_commercial_rate,
      } => {
        format!(
          "StabilizeAccess (beds: {}, capital: {}, rate: {})",
          add_staffed_beds, capital_spend, requested_commercial_rate
        )
      }
      PlayerCommand::RespondToStateAccessMandate {
        advocacy_spend,
        access_commitment,
      } => {
        format!(
          "RespondToStateAccessMandate (advocacy: {}, commitment: {})",
          advocacy_spend, access_commitment
        )
      }
      PlayerCommand::RespondToWorkforcePressure {
        retention_spend,
        schedule_relief_commitment,
      } => {
        format!(
          "RespondToWorkforcePressure (retention: {}, schedule_relief: {})",
          retention_spend, schedule_relief_commitment
        )
      }
      PlayerCommand::JoinRegionalAccessCoalition {
        coalition_investment,
        shared_access_commitment,
      } => {
        format!(
          "JoinRegionalAccessCoalition (investment: {}, commitment: {})",
          coalition_investment, shared_access_commitment
        )
      }
      PlayerCommand::RespondToCompetitorCapacityMove {
        defensive_capital_commitment,
        access_posture,
      } => {
        format!(
          "RespondToCompetitorCapacityMove (capital: {}, posture: {})",
          defensive_capital_commitment, access_posture
        )
      }
    };

    lines.push(format!(
      "Turn {} (Turn {} → {}):",
      turn_idx, transition.prior.turn, transition.next.turn
    ));
    lines.push(format!("  Player Action: {}", cmd_desc));
    lines.push(format!(
      "  Access Index: Observed = {}, True Prior = {} (Observation Gap = {})",
      observed_access, true_prior_access, delta_sign
    ));
    lines.push(format!(
      "  True Outcome: True Access = {}, Cash = {}, Workforce Trust = {}, Community Trust = {}",
      transition.next.access_index,
      transition.next.cash,
      transition.next.workforce_trust,
      transition.next.community_trust
    ));
  }

  lines
}

pub fn competitive_debrief(history: &CompetitiveHistory) -> Vec<String> {
  let final_state = history.final_state();
  let mut lines = vec![
    format!(
      "Competitive preview completed {} committed month(s).",
      history.transitions.len()
    ),
    format!(
      "Final state hash: {}",
      history
        .transitions
        .last()
        .map(|transition| transition.state_hash.as_str())
        .unwrap_or("none")
    ),
    format!(
      "Final calendar: Year {}, Month {}.",
      final_state.policy_calendar.year, final_state.policy_calendar.month_in_year
    ),
  ];
  lines.extend(competitive_final_tradeoff_lines(
    &history.genesis,
    final_state,
  ));

  let Some(human_system) = history.genesis.human_system() else {
    return lines;
  };
  let human_system_id = human_system.system_id;

  if !history.transitions.is_empty() {
    // Trace transitions
    for (idx, transition) in history.transitions.iter().enumerate() {
      let month_name = format!("Month {}", idx + 1);
      lines.push(format!("--- {} ---", month_name));

      if let Some(human_batch) = transition.aggregated.batch_for_system(human_system_id) {
        let cmds: Vec<String> = human_batch
          .commands
          .iter()
          .map(format_command_debrief)
          .collect();
        let cmd_str = if cmds.is_empty() {
          "none".to_string()
        } else {
          cmds.join("; ")
        };
        lines.push(format!("Player: {}", cmd_str));
      }

      let mut monitored_system_ids = std::collections::HashSet::new();
      if let Some(human_batch) = transition.aggregated.batch_for_system(human_system_id) {
        for cmd in &human_batch.commands {
          if let CompetitiveCommand::Monitor { target, .. } = cmd {
            monitored_system_ids.insert(target.system_id());
          }
        }
      }

      for system in &transition.prior.systems {
        if system.system_id == human_system_id {
          continue;
        }
        if let Some(rival_batch) = transition.aggregated.batch_for_system(system.system_id) {
          let mut cmd_strs = Vec::new();
          let observed = monitored_system_ids.contains(&system.system_id);
          let mut any_observed = false;
          for cmd in &rival_batch.commands {
            let formatted = format_command_debrief(cmd);
            if is_public_command(cmd) {
              cmd_strs.push(format!("{} (publicly disclosed)", formatted));
              any_observed = true;
            } else if observed {
              cmd_strs.push(format!("{} (observed via monitor)", formatted));
              any_observed = true;
            } else {
              cmd_strs.push("[Private Action] (unobserved by you)".to_string());
            }
          }
          let cmd_str = if cmd_strs.is_empty() {
            "none".to_string()
          } else {
            cmd_strs.join("; ")
          };
          lines.push(format!("Rival {}: {}", system.name, cmd_str));
          if let Some(rationale) = &rival_batch.rationale
            && any_observed
          {
            let visibility_label = if observed {
              "observed via monitor"
            } else {
              "observed via public disclosure"
            };
            lines.push(format!(
              "Rival {} rationale: {} ({})",
              system.name, rationale, visibility_label
            ));
          }
        }
      }
    }

    // Summary of mechanisms and events
    let mut events = Vec::new();
    let mut effects = Vec::new();
    for transition in &history.transitions {
      for event in &transition.events {
        events.push(format_event(event));
      }
      for effect in &transition.effects {
        effects.push(format_effect(effect));
      }
    }

    events.sort();
    events.dedup();
    effects.sort();
    effects.dedup();

    let effect_summary = if effects.is_empty() {
      "none".to_string()
    } else {
      effects.join("; ")
    };
    let event_summary = if events.is_empty() {
      "none".to_string()
    } else {
      events.join("; ")
    };
    lines.push(format!(
      "Attributed mechanisms to inspect: {}.",
      effect_summary
    ));
    lines.push(format!("Resolved events: {}.", event_summary));
  }

  lines.extend([
    "Recruitment lesson: nurse, physician, and admin hiring spends cash immediately, resolves after role-specific delays, and can lower workforce trust while added capacity is pending.".to_string(),
    "Capital project lesson: EHR Epic/Cerner, Tower, and Clinic Network projects consume Action Points and cash immediately, draw cash monthly over their duration (9 to 12 months), and are limited to a maximum of 2 concurrent projects. They are long-term strategic investments that require careful planning over the 24-month horizon.".to_string(),
    "Access pledge lesson: public access commitments build legitimacy, but the debrief reviews whether repeated pledges were paired with capacity, staffing, monitoring, or payer follow-through.".to_string(),
    "Decision quality and outcome quality remain separate: the MCP surface reports actor-visible observations plus committed transition summaries.".to_string(),
  ]);

  // Append the instructor run summary
  lines.extend(competitive_instructor_summary(history));

  lines
}

pub fn competitive_instructor_summary(history: &CompetitiveHistory) -> Vec<String> {
  let mut lines = vec![
    "".to_string(),
    "=== INSTRUCTOR RUN SUMMARY & DECISION QUALITY REVIEW ===".to_string(),
    "Note: In this competitive campaign, measurement noise and reporting delays are currently 0 (player observed state matches true state).".to_string(),
    "Rival actions and rationales that were unobserved during play are revealed below for post-run instructor evaluation:".to_string(),
  ];

  let Some(human_system) = history.genesis.human_system() else {
    lines.push("No human system found at genesis.".to_string());
    return lines;
  };
  let human_system_id = human_system.system_id;

  if history.transitions.is_empty() {
    lines.push("No transitions available.".to_string());
    return lines;
  }

  for (idx, transition) in history.transitions.iter().enumerate() {
    let month_idx = idx + 1;
    lines.push(format!("Month {}:", month_idx));

    // Player action
    if let Some(human_batch) = transition.aggregated.batch_for_system(human_system_id) {
      let cmds: Vec<String> = human_batch
        .commands
        .iter()
        .map(format_command_debrief)
        .collect();
      let cmd_str = if cmds.is_empty() {
        "none".to_string()
      } else {
        cmds.join("; ")
      };
      lines.push(format!("  Player: {}", cmd_str));
    }

    // Determine monitored targets
    let mut monitored_system_ids = std::collections::HashSet::new();
    if let Some(human_batch) = transition.aggregated.batch_for_system(human_system_id) {
      for cmd in &human_batch.commands {
        if let CompetitiveCommand::Monitor { target, .. } = cmd {
          monitored_system_ids.insert(target.system_id());
        }
      }
    }

    // Rivals
    for system in &transition.prior.systems {
      if system.system_id == human_system_id {
        continue;
      }
      if let Some(rival_batch) = transition.aggregated.batch_for_system(system.system_id) {
        let mut cmd_strs = Vec::new();
        for cmd in &rival_batch.commands {
          let formatted = format_command_debrief(cmd);
          if is_public_command(cmd) {
            cmd_strs.push(format!("{} (publicly disclosed)", formatted));
          } else {
            let observed = monitored_system_ids.contains(&system.system_id);
            if observed {
              cmd_strs.push(format!("{} (observed via monitor)", formatted));
            } else {
              cmd_strs.push(format!(
                "{} (unobserved during play - REVEALED FOR INSTRUCTOR REVIEW)",
                formatted
              ));
            }
          }
        }
        let cmd_str = if cmd_strs.is_empty() {
          "none".to_string()
        } else {
          cmd_strs.join("; ")
        };
        lines.push(format!("  Rival {}: {}", system.name, cmd_str));
        if let Some(rationale) = &rival_batch.rationale {
          let observed = monitored_system_ids.contains(&system.system_id);
          let mut any_public = false;
          for cmd in &rival_batch.commands {
            if is_public_command(cmd) {
              any_public = true;
            }
          }
          let observed_during_play = observed || any_public;
          if observed_during_play {
            let detail = if observed {
              "observed via monitor"
            } else {
              "observed via public disclosure"
            };
            lines.push(format!(
              "  Rival {} rationale: {} ({})",
              system.name, rationale, detail
            ));
          } else {
            lines.push(format!(
              "  Rival {} rationale: {} (unobserved during play - REVEALED FOR INSTRUCTOR REVIEW)",
              system.name, rationale
            ));
          }
        }
      }
    }
  }

  // Append decision-quality evaluation
  lines.extend(analyze_decision_quality(history));

  lines
}

fn analyze_decision_quality(history: &CompetitiveHistory) -> Vec<String> {
  let mut lines = vec![
    "".to_string(),
    "=== DECISION QUALITY EVALUATION ===".to_string(),
  ];

  let Some(human_system) = history.genesis.human_system() else {
    lines.push("No human system found for decision quality evaluation.".to_string());
    return lines;
  };
  let human_system_id = human_system.system_id;

  let mut warnings = Vec::new();

  for (idx, transition) in history.transitions.iter().enumerate() {
    let month_idx = idx + 1;
    let Some(human_prior) = transition
      .prior
      .systems
      .iter()
      .find(|s| s.system_id == human_system_id)
    else {
      continue;
    };
    let Some(human_next) = transition
      .next
      .systems
      .iter()
      .find(|s| s.system_id == human_system_id)
    else {
      continue;
    };

    // 1. Cash Runway Safety
    if human_next.resources.cash < 20 && human_next.resources.active_project_monthly_draws > 0 {
      warnings.push(format!(
        "  - Warning: Cash runway fell to {} in Month {} while carrying active project monthly draws of {}. Consider halting capital projects or deferring investments if cash is critically low.",
        human_next.resources.cash, month_idx, human_next.resources.active_project_monthly_draws
      ));
    }

    // 2. Workforce Trust Check
    if human_next.workforce_trust < 55 {
      let mut recruited = false;
      if let Some(human_batch) = transition.aggregated.batch_for_system(human_system_id) {
        for cmd in &human_batch.commands {
          if let CompetitiveCommand::Recruit { headcount, .. } = cmd {
            recruited |= *headcount > 0;
          }
        }
      }
      if recruited {
        warnings.push(format!(
          "  - Warning: Workforce trust dropped to {} in Month {} due to recruitment stress. Watch headcount additions to avoid severe staffing vacancies or burnout.",
          human_next.workforce_trust, month_idx
        ));
      }
    }

    // 3. Payer Posture Check
    if let Some(human_batch) = transition.aggregated.batch_for_system(human_system_id) {
      for cmd in &human_batch.commands {
        if let CompetitiveCommand::Negotiate {
          rate_posture: RatePosture::Aggressive,
          ..
        } = cmd
        {
          let low_leverage = human_prior.quality_index < 75 && human_prior.market_share_index < 20;
          if low_leverage {
            warnings.push(format!(
              "  - Warning: Attempted aggressive payer negotiation in Month {} with low leverage (Market Share = {}%, Quality = {}). Aggressive rates require strong market share (>= 20%) or quality (>= 75) to succeed.",
              month_idx, human_prior.market_share_index, human_prior.quality_index
            ));
          }
        }
      }
    }

    // 4. Rival Bed Capacity Check
    for rival_prior in &transition.prior.systems {
      if rival_prior.system_id == human_system_id {
        continue;
      }
      if let Some(rival_next) = transition
        .next
        .systems
        .iter()
        .find(|s| s.system_id == rival_prior.system_id)
      {
        let bed_diff = rival_next.staffed_beds - rival_prior.staffed_beds;
        if bed_diff >= 10 {
          let mut human_expanded = false;
          if let Some(human_batch) = transition.aggregated.batch_for_system(human_system_id) {
            for cmd in &human_batch.commands {
              match cmd {
                CompetitiveCommand::Invest {
                  domain: InvestDomain::Beds,
                  amount,
                } if *amount > 0 => {
                  human_expanded = true;
                }
                CompetitiveCommand::Recruit { headcount, .. } if *headcount > 0 => {
                  human_expanded = true;
                }
                CompetitiveCommand::Project {
                  kind: ProjectKind::Tower | ProjectKind::ClinicNetwork,
                  ..
                } => {
                  human_expanded = true;
                }
                _ => {}
              }
            }
          }
          let market_share_erosion = human_next.market_share_index < human_prior.market_share_index;
          if !human_expanded && market_share_erosion {
            warnings.push(format!(
              "  - Warning: Rival capacity expansion by {} ({}) went unanswered in Month {}. Northlake/Summit/Valley/Metro expanded capacity while you did not invest in beds, recruitment, or project capital, resulting in market share erosion.",
              rival_prior.name, bed_diff, month_idx
            ));
          }
        }
      }
    }

    // 5. ASC Deferrals Hook
    let target_nurses_icu = human_prior.icu_capacity;
    let nurses_icu = human_prior.nurses.min(target_nurses_icu);
    let remaining_nurses_obs = (human_prior.nurses - nurses_icu).max(0);

    let target_nurses_obs = (human_prior.obstetrics_capacity + 1) / 2;
    let nurses_obs = remaining_nurses_obs.min(target_nurses_obs);
    let remaining_nurses_ms = (remaining_nurses_obs - nurses_obs).max(0);

    let target_nurses_beds = (human_prior.staffed_beds + 4) / 5;
    let nurses_beds = remaining_nurses_ms.min(target_nurses_beds);
    let remaining_nurses_cardio = (remaining_nurses_ms - nurses_beds).max(0);

    let target_nurses_cardio = (human_prior.cardiology_capacity + 2) / 3;
    let nurses_cardio = remaining_nurses_cardio.min(target_nurses_cardio);
    let remaining_nurses_psych = (remaining_nurses_cardio - nurses_cardio).max(0);

    let target_nurses_psych = (human_prior.psychiatric_capacity + 3) / 4;
    let nurses_psych = remaining_nurses_psych.min(target_nurses_psych);
    let remaining_nurses_neuro = (remaining_nurses_psych - nurses_psych).max(0);

    let target_nurses_neuro = (human_prior.neurology_capacity + 2) / 3;
    let nurses_neuro = remaining_nurses_neuro.min(target_nurses_neuro);
    let remaining_nurses_oncology = (remaining_nurses_neuro - nurses_neuro).max(0);

    let target_nurses_oncology = (human_prior.oncology_capacity + 2) / 3;
    let nurses_oncology = remaining_nurses_oncology.min(target_nurses_oncology);
    let remaining_nurses_infusion = (remaining_nurses_oncology - nurses_oncology).max(0);

    let target_nurses_infusion = (human_prior.infusion_capacity + 3) / 4;
    let nurses_infusion = remaining_nurses_infusion.min(target_nurses_infusion);
    let remaining_nurses_asc = (remaining_nurses_infusion - nurses_infusion).max(0);

    let target_nurses_asc = (human_prior.asc_capacity + 1) / 2;
    let nurses_asc = remaining_nurses_asc.min(target_nurses_asc);

    let target_physicians_icu = (human_prior.icu_capacity + 1) / 2;
    let physicians_icu = human_prior.physicians.min(target_physicians_icu);
    let remaining_physicians_obs = (human_prior.physicians - physicians_icu).max(0);

    let target_physicians_obs = (human_prior.obstetrics_capacity + 4) / 5;
    let physicians_obs = remaining_physicians_obs.min(target_physicians_obs);
    let remaining_physicians_cardio = (remaining_physicians_obs - physicians_obs).max(0);

    let target_physicians_cardio = (human_prior.cardiology_capacity + 7) / 8;
    let physicians_cardio = remaining_physicians_cardio.min(target_physicians_cardio);
    let remaining_physicians_psych = (remaining_physicians_cardio - physicians_cardio).max(0);

    let target_physicians_psych = (human_prior.psychiatric_capacity + 9) / 10;
    let physicians_psych = remaining_physicians_psych.min(target_physicians_psych);
    let remaining_physicians_neuro = (remaining_physicians_psych - physicians_psych).max(0);

    let target_physicians_neuro = (human_prior.neurology_capacity + 5) / 6;
    let physicians_neuro = remaining_physicians_neuro.min(target_physicians_neuro);
    let remaining_physicians_oncology = (remaining_physicians_neuro - physicians_neuro).max(0);

    let target_physicians_oncology = (human_prior.oncology_capacity + 7) / 8;
    let physicians_oncology = remaining_physicians_oncology.min(target_physicians_oncology);
    let remaining_physicians_infusion =
      (remaining_physicians_oncology - physicians_oncology).max(0);

    let target_physicians_infusion = (human_prior.infusion_capacity + 14) / 15;
    let physicians_infusion = remaining_physicians_infusion.min(target_physicians_infusion);
    let remaining_physicians_asc = (remaining_physicians_infusion - physicians_infusion).max(0);

    let target_physicians_asc = (human_prior.asc_capacity + 3) / 4;
    let physicians_asc = remaining_physicians_asc.min(target_physicians_asc);

    let mut eff_asc = human_prior
      .asc_capacity
      .min(nurses_asc * 2)
      .min(physicians_asc * 4);

    if human_prior.system_id == 0
      && transition.prior.event_metadata.get("rna_strike_active") == Some(&"true".to_string())
    {
      eff_asc /= 2;
    }

    let asc_demand = (human_prior.asc_capacity + 7) / 8;
    let deferred_asc = (asc_demand - eff_asc).max(0);

    if deferred_asc > 0 {
      warnings.push(format!(
        "  - Warning: Ambulatory surgery center procedures were deferred due to capacity/staffing constraints, causing patient leakage in Month {}.",
        month_idx
      ));
    }
  }

  warnings.extend(access_pledge_follow_through_warnings(
    history,
    human_system_id,
  ));

  if warnings.is_empty() {
    lines.push("All strategic checks passed. The run demonstrated safe cash runway, balanced recruitment, appropriate payer rate postures, and adequate rival capacity responses.".to_string());
  } else {
    lines.extend(warnings);
  }

  lines
}

fn access_pledge_follow_through_warnings(
  history: &CompetitiveHistory,
  human_system_id: u32,
) -> Vec<String> {
  let mut warnings = Vec::new();
  let mut warned_months = std::collections::BTreeSet::new();

  for (idx, transition) in history.transitions.iter().enumerate() {
    let month_idx = idx + 1;
    if warned_months.contains(&month_idx) || !human_access_pledged(transition, human_system_id) {
      continue;
    }

    let window_end = (idx + 3).min(history.transitions.len());
    let pledge_months = history.transitions[idx..window_end]
      .iter()
      .enumerate()
      .filter_map(|(offset, window_transition)| {
        if human_access_pledged(window_transition, human_system_id) {
          Some(idx + offset + 1)
        } else {
          None
        }
      })
      .collect::<Vec<_>>();

    if pledge_months.len() < 2 {
      continue;
    }

    let has_follow_through = history.transitions[idx..window_end]
      .iter()
      .any(|window_transition| human_has_access_follow_through(window_transition, human_system_id));

    if has_follow_through {
      continue;
    }

    for pledged_month in &pledge_months {
      warned_months.insert(*pledged_month);
    }

    let months = pledge_months
      .iter()
      .map(|month| month.to_string())
      .collect::<Vec<_>>()
      .join(", ");
    warnings.push(format!(
      "  - Warning: Repeated public access pledges in Months {} had no capacity, staffing, monitoring, or payer follow-through in the same three-month window. Treat access pledges as legitimacy signals, not substitutes for durable operational action.",
      months
    ));
  }

  warnings
}

fn human_access_pledged(
  transition: &crate::model::CompetitiveTransition,
  human_system_id: u32,
) -> bool {
  transition
    .aggregated
    .batch_for_system(human_system_id)
    .is_some_and(|batch| {
      batch.commands.iter().any(|cmd| {
        matches!(
          cmd,
          CompetitiveCommand::Commit {
            pledge_type: PledgeType::Access,
            ..
          }
        )
      })
    })
}

fn human_has_access_follow_through(
  transition: &crate::model::CompetitiveTransition,
  human_system_id: u32,
) -> bool {
  transition
    .aggregated
    .batch_for_system(human_system_id)
    .is_some_and(|batch| {
      batch.commands.iter().any(|cmd| {
        matches!(
          cmd,
          CompetitiveCommand::Recruit { .. }
            | CompetitiveCommand::Invest { .. }
            | CompetitiveCommand::Monitor { .. }
            | CompetitiveCommand::Negotiate { .. }
            | CompetitiveCommand::Project { .. }
        )
      })
    })
}

fn format_command_debrief(cmd: &CompetitiveCommand) -> String {
  match cmd {
    CompetitiveCommand::Hold => "hold".to_string(),
    CompetitiveCommand::Recruit { role, headcount } => {
      let r = match role {
        RecruitRole::Nurse => "nurse",
        RecruitRole::Physician => "physician",
        RecruitRole::Admin => "admin",
      };
      format!("recruit role={} headcount={}", r, headcount)
    }
    CompetitiveCommand::Invest { domain, amount } => {
      let d = match domain {
        InvestDomain::Beds => "beds",
        InvestDomain::Outpatient => "outpatient",
        InvestDomain::Technology => "technology",
        InvestDomain::Emergency => "emergency",
        InvestDomain::Icu => "icu",
        InvestDomain::Obstetrics => "obstetrics",
        InvestDomain::Psychiatric => "psychiatric",
        InvestDomain::Cardiology => "cardiology",
        InvestDomain::Oncology => "oncology",
        InvestDomain::Infusion => "infusion",
        InvestDomain::Neurology => "neurology",
        InvestDomain::Asc => "asc",
      };
      format!("invest domain={} amount={}", d, amount)
    }
    CompetitiveCommand::Monitor { target, depth } => {
      let t = match target {
        MonitorTarget::Northlake => "northlake",
        MonitorTarget::Summit => "summit",
        MonitorTarget::Valley => "valley",
        MonitorTarget::Metro => "metro",
      };
      format!("monitor target={} depth={}", t, depth)
    }
    CompetitiveCommand::Negotiate {
      payer,
      rate_posture,
    } => {
      let p = match payer {
        PayerId::CarrierA => "carrier_a",
        PayerId::CarrierB => "carrier_b",
        PayerId::Medicaid => "medicaid",
        PayerId::Medicare => "medicare",
      };
      let rp = match rate_posture {
        RatePosture::Aggressive => "aggressive",
        RatePosture::Neutral => "neutral",
        RatePosture::Conservative => "conservative",
      };
      format!("negotiate payer={} rate_posture={}", p, rp)
    }
    CompetitiveCommand::Commit { pledge_type, level } => {
      let pt = match pledge_type {
        PledgeType::Access => "access",
        PledgeType::Quality => "quality",
        PledgeType::Workforce => "workforce",
      };
      format!("commit pledge_type={} level={}", pt, level)
    }
    CompetitiveCommand::Project { kind, budget } => {
      let k = match kind {
        ProjectKind::EhrEpic => "ehr_epic",
        ProjectKind::EhrCerner => "ehr_cerner",
        ProjectKind::Tower => "tower",
        ProjectKind::ClinicNetwork => "clinic_network",
        ProjectKind::EmergencyPavilion => "emergency_pavilion",
        ProjectKind::IcuWing => "icu_wing",
        ProjectKind::ObstetricsUnit => "obstetrics_unit",
        ProjectKind::PsychiatricUnit => "psychiatric_unit",
        ProjectKind::CardiologyUnit => "cardiology_unit",
        ProjectKind::OncologyUnit => "oncology_unit",
        ProjectKind::InfusionCenter => "infusion_center",
        ProjectKind::NeurologyUnit => "neurology_unit",
        ProjectKind::AscUnit => "asc_unit",
      };
      format!("project kind={} budget={}", k, budget)
    }
  }
}

fn competitive_final_tradeoff_lines(
  genesis: &CompetitiveWorldState,
  final_state: &CompetitiveWorldState,
) -> Vec<String> {
  let Some(initial_human) = genesis.human_system() else {
    return vec![
      "Final player tradeoff metrics unavailable: no human system at genesis.".to_string(),
    ];
  };
  let Some(final_human) = final_state.human_system() else {
    return vec![
      "Final player tradeoff metrics unavailable: no human system in final state.".to_string(),
    ];
  };

  vec![
    format!(
      "Final player tradeoff: {} cash moved from {} to {}, access from {} to {}, quality from {} to {}, workforce trust from {} to {}, community trust from {} to {}, and market share from {} to {}.",
      final_human.name,
      initial_human.resources.cash,
      final_human.resources.cash,
      initial_human.access_index,
      final_human.access_index,
      initial_human.quality_index,
      final_human.quality_index,
      initial_human.workforce_trust,
      final_human.workforce_trust,
      initial_human.community_trust,
      final_human.community_trust,
      initial_human.market_share_index,
      final_human.market_share_index
    ),
    format!(
      "Final player resources: political capital {}, active projects {}, active project monthly draws {}, staffed beds {}.",
      final_human.resources.political_capital,
      final_human.resources.active_projects,
      final_human.resources.active_project_monthly_draws,
      final_human.staffed_beds
    ),
  ]
}

fn format_event(event: &Event) -> String {
  format!("{}: {}", event.actor, event.description)
}

fn format_effect(effect: &AttributedEffect) -> String {
  format!(
    "{} changed {} by {}",
    effect.source, effect.metric, effect.delta
  )
}
