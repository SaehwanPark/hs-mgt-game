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
    "Capital project lesson: EHR Epic/Cerner, Tower, and Clinic Network projects consume Action Points and cash immediately, draw cash monthly over their duration (9 to 12 months), and are limited to a maximum of 2 concurrent projects. They are long-term strategic investments that do not resolve within a short three-month preview but are critical in longer horizons.".to_string(),
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
  }

  if warnings.is_empty() {
    lines.push("All strategic checks passed. The run demonstrated safe cash runway, balanced recruitment, appropriate payer rate postures, and adequate rival capacity responses.".to_string());
  } else {
    lines.extend(warnings);
  }

  lines
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
