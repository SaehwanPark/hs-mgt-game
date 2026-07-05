use super::competitive_parse::competitive_command_help_lines;
use super::display::{PromptContext, print_block, style};

pub fn print_context_help_with_topic(context: PromptContext, topic: Option<&str>) {
  print_block(&context_help_lines_with_topic(context, topic));
}

pub fn context_help_lines_with_topic(context: PromptContext, topic: Option<&str>) -> Vec<String> {
  if let Some(t) = topic {
    if context == PromptContext::CompetitiveCommand {
      if let Some(help_lines) = command_topic_help_lines(t) {
        return help_lines;
      } else {
        return vec![
          style::section_heading(
            style::EMOJI_BRIEFING,
            &format!("Help: unknown topic '{}'", t),
          ),
          style::warning(&format!(
            "  No specific help available for '{}'. Available commands: hold, invest, recruit, monitor, negotiate, commit, project.",
            t
          )),
        ];
      }
    } else {
      return vec![
        style::section_heading(style::EMOJI_BRIEFING, &format!("Help: topic '{}'", t)),
        style::warning(
          "  Command-specific help is only available during the competitive campaign.",
        ),
        style::dim("  For general menu help, type ? or help without any topic."),
      ];
    }
  }
  context_help_lines(context)
}

pub fn context_help_lines(context: PromptContext) -> Vec<String> {
  let mut lines = vec![style::section_heading(style::EMOJI_BRIEFING, "Help")];

  match context {
    PromptContext::ResumeChoice => {
      lines.push("  Resume continues your saved interactive session.".to_string());
      lines.push("  Start over deletes the autosave and begins a fresh run.".to_string());
    }
    PromptContext::Campaign => {
      lines.push("  Stabilization (Enter or 1): the playable five-turn regional demo.".to_string());
      lines.push("  Competitive (2 or c): preview three monthly competitive turns.".to_string());
      lines.push("  Autosave resume applies to stabilization interactive runs only.".to_string());
    }
    PromptContext::Difficulty => {
      lines.push("  Difficulty sets rival count (K) and monthly action-point budgets.".to_string());
      lines.push("  Normal (Enter or 2) is the default competitive preview tier.".to_string());
    }
    PromptContext::PlayMode => {
      lines.push("  Interactive (Enter or i): choose each turn yourself.".to_string());
      lines
        .push("  Beginner (b): multiple-choice turns with pros, cons, and trade-offs.".to_string());
      lines.push("  Presets 1–3: watch a scripted five-turn strategy path.".to_string());
      lines.push(
        "  Read the executive dashboard above for starting cash, capacity, and trust.".to_string(),
      );
      lines.push(
        "  Reported access and quality may differ from true conditions during play.".to_string(),
      );
    }
    PromptContext::Seed => {
      lines.push(
        "  The seed fixes stochastic inputs and ties together reproducible classroom runs."
          .to_string(),
      );
      lines.push(
        "  The same seed and choices always produce the same outcome for a given campaign."
          .to_string(),
      );
    }
    PromptContext::TurnCommand { turn } => {
      lines.extend(turn_help_lines(turn));
      lines.push("  Press Enter without typing to accept the listed defaults.".to_string());
    }
    PromptContext::BeginnerTurn { turn } => {
      lines.push(format!(
        "  Turn {turn}: pick 1, 2, or 3 to choose a curated option."
      ));
      lines.push("  Options mirror the three preset strategy paths for this decision.".to_string());
      lines.push(
        "  Recommendability is guidance only — outcomes still depend on rivals and payers."
          .to_string(),
      );
    }
    PromptContext::ReplayExport => {
      lines.push("  Replay artifacts record the full run for classroom analysis.".to_string());
      lines.push("  Press Enter to skip export.".to_string());
    }
    PromptContext::ValidationDemo => {
      lines
        .push("  Preset batches exercise AP, cash, and political capital validation.".to_string());
      lines.push("  Demo 4 uses constrained political capital (2) to show PC failure.".to_string());
      lines.push("  Press Enter to skip the validation demo.".to_string());
    }
    PromptContext::CompetitiveCommand => {
      lines
        .push("  Enter one or more competitive commands using verb arg=value syntax.".to_string());
      lines.push("  Separate multiple commands with semicolons on one line.".to_string());
      lines.push("  Available commands:".to_string());
      for command_line in competitive_command_help_lines() {
        lines.push(format!(
          "    {}",
          format_competitive_help_line(&command_line)
        ));
      }
      // Note: Keep command details here aligned with `command_topic_help_lines` below to avoid doc drift.
      lines.push("  Command descriptions and resource costs:".to_string());
      lines.push("    hold: Do nothing. Costs 0 AP, $0 cash, 0 PC.".to_string());
      lines.push("    invest domain=beds|outpatient|technology|emergency amount=<int>: Expand capacity. Costs 1 AP, cash amount. Beds, outpatient services, technology, or emergency investments.".to_string());
      lines.push("    recruit role=nurse|physician|admin headcount=<int>: Hire personnel. Costs 1 AP, $5 cash per headcount. Delays: nurse (1 mo), admin (2 mo), physician (3 mo). Can lower trust.".to_string());
      lines.push("    monitor target=northlake|summit|valley|metro depth=<1-3>: View competitor activity. Costs AP equal to depth, $0 cash, 0 PC.".to_string());
      lines.push("    negotiate payer=carrier_a|carrier_b|medicaid|medicare rate_posture=aggressive|neutral|conservative: Set payer commercial bid or align public compliance. Commercial: 1 AP, $0 cash, 2 PC. Medicaid: 1 AP, $5 cash, 2 PC (neutral posture only). Medicare: 1 AP, $10 cash, 2 PC (neutral posture only).".to_string());
      lines.push("    commit pledge_type=access|quality|workforce level=<1-5>: Public commitments. Costs 1 AP, $0 cash, 1 PC.".to_string());
      lines.push("    project kind=ehr_epic|ehr_cerner|tower|clinic_network|emergency_pavilion budget=<int>: Multi-month capital projects. Costs 2 AP, monthly cash draw (budget/duration). Duration: epic/cerner (12 mo), tower (12 mo), clinic_network (9 mo), emergency_pavilion (6 mo). Max 2 concurrent projects.".to_string());
      lines.push("  Press Enter to use the fallback batch for this month.".to_string());
    }
  }

  lines.push(style::dim("  Type your choice again after reading help."));
  lines
}

fn format_competitive_help_line(line: &str) -> String {
  if line.starts_with("Separate ") {
    return style::dim(line);
  }

  if line.contains(char::is_whitespace) {
    let mut parts = line.splitn(2, char::is_whitespace);
    let verb = parts.next().unwrap_or_default();
    let rest = parts.next().unwrap_or("").trim();
    if rest.is_empty() {
      style::command_token(verb)
    } else {
      format!(
        "{} {}",
        style::command_token(verb),
        style::argument_token(rest)
      )
    }
  } else {
    style::command_token(line)
  }
}

fn turn_help_lines(turn: u32) -> Vec<String> {
  match turn {
    1 => vec![
      "  Turn 1 — capacity and payer posture: add staffed beds, spend capital, and bid a commercial rate.".to_string(),
      "  Higher beds and spend improve access but consume cash; above-target rates need visible payer leverage from reported access, capacity, or quality context.".to_string(),
    ],
    2 => vec![
      "  Turn 2 — state access mandate: advocacy spend and an access commitment signal responsiveness.".to_string(),
      "  Balance policy pressure relief against cash and credibility.".to_string(),
    ],
    3 => vec![
      "  Turn 3 — workforce pressure: retention spend and schedule relief affect workforce trust.".to_string(),
      "  Under-committing can erode labor cooperation.".to_string(),
    ],
    4 => vec![
      "  Turn 4 — regional access coalition: shared investment and access commitment.".to_string(),
      "  Coalition leverage depends on credible participation.".to_string(),
    ],
    5 => vec![
      "  Turn 5 — competitor capacity: defensive capital and access posture.".to_string(),
      "  Read the market competition briefing before choosing.".to_string(),
    ],
    _ => vec!["  Enter integers as shown in the field list.".to_string()],
  }
}

pub fn new_player_cue_lines() -> Vec<String> {
  vec![
    style::section_heading(style::EMOJI_BRIEFING, "New player"),
    "  Suggested flow each turn: uncertainty preview → executive briefing → your decision."
      .to_string(),
    "  Type ? or help anytime for context; q, quit, or exit saves and leaves (interactive only)."
      .to_string(),
    style::dim("  This note is shown once; use ? later for help.").to_string(),
  ]
}

pub fn turn_hint(turn: u32) -> Option<&'static str> {
  match turn {
    1 => Some(
      "Tip: compare capital spend, added beds, and rate posture; payers respond to visible leverage, not rate asks alone.",
    ),
    2 => Some("Tip: advocacy spend is capped — pair it with a credible access commitment."),
    3 => Some("Tip: schedule relief must be at least 1; balance spend and commitment."),
    4 => Some("Tip: coalition investment and shared access move together."),
    5 => Some("Tip: defensive capital competes with cash reserves for access posture."),
    _ => None,
  }
}

// Note: Keep command details here aligned with `PromptContext::CompetitiveCommand` help block above to avoid doc drift.
fn command_topic_help_lines(verb: &str) -> Option<Vec<String>> {
  let verb_lower = verb.trim().to_ascii_lowercase();
  match verb_lower.as_str() {
    "hold" => Some(vec![
      style::section_heading(style::EMOJI_BRIEFING, "Help: hold"),
      style::label_value("  Usage", &style::accent("hold")),
      style::label_value("  Description", "Do nothing for the current month."),
      style::label_value("  Resource Costs", "Costs 0 AP, $0 cash, 0 PC."),
      style::label_value(
        "  Strategic Guidance",
        "Use hold to pass the turn when cash is strained and you need to wait, or to observe rival activity without committing resources.",
      ),
    ]),
    "invest" => Some(vec![
      style::section_heading(style::EMOJI_BRIEFING, "Help: invest"),
      style::label_value(
        "  Usage",
        &format!(
          "{} {}",
          style::accent("invest"),
          style::dim("domain=beds|outpatient|technology|emergency amount=<int>")
        ),
      ),
      style::label_value("  Description", "Expand local service capacities."),
      style::label_value(
        "  Resource Costs",
        "Costs 1 AP, cash equal to the amount invested.",
      ),
      style::label_value("  Domains", ""),
      style::dim("    - beds: Expands staffed inpatient bed capacity."),
      style::dim("    - outpatient: Expands outpatient clinic services."),
      style::dim("    - technology: Upgrades system technology infrastructure."),
      style::dim("    - emergency: Expands emergency department bays."),
      style::label_value(
        "  Strategic Guidance",
        "Building capacity increases access and quality potential but consumes cash. Keep an eye on your cash runway before investing large amounts.",
      ),
    ]),
    "recruit" => Some(vec![
      style::section_heading(style::EMOJI_BRIEFING, "Help: recruit"),
      style::label_value(
        "  Usage",
        &format!(
          "{} {}",
          style::accent("recruit"),
          style::dim("role=nurse|physician|admin headcount=<int>")
        ),
      ),
      style::label_value("  Description", "Hire and onboard healthcare personnel."),
      style::label_value(
        "  Resource Costs",
        "Costs 1 AP, $5 cash per headcount, 0 PC.",
      ),
      style::label_value("  Onboarding Delays", ""),
      style::dim("    - nurse: 1 month delay (available next month)"),
      style::dim("    - admin: 2 months delay (available in 2 months)"),
      style::dim("    - physician: 3 months delay (available in 3 months)"),
      style::label_value(
        "  Strategic Guidance",
        "Hiring staff resolves capacity bottlenecks, but recruitment takes time. Sudden high-volume recruitment can strain short-term workforce trust.",
      ),
    ]),
    "monitor" => Some(vec![
      style::section_heading(style::EMOJI_BRIEFING, "Help: monitor"),
      style::label_value(
        "  Usage",
        &format!(
          "{} {}",
          style::accent("monitor"),
          style::dim("target=northlake|summit|valley|metro depth=<1-3>")
        ),
      ),
      style::label_value(
        "  Description",
        "Audit and spy on rival health system capacity and strategic moves.",
      ),
      style::label_value(
        "  Resource Costs",
        "Costs Action Points (AP) equal to depth, $0 cash, 0 PC.",
      ),
      style::label_value("  Depths", ""),
      style::dim("    - depth=1: Basic visibility into public actions and announcements."),
      style::dim("    - depth=2: Deeper capacity metrics and private project information."),
      style::dim("    - depth=3: Full strategic target detail and rationale observation."),
      style::label_value(
        "  Strategic Guidance",
        "Information is power; monitor rivals before making major market plays. Monitor costs AP but no cash, making it a great low-burn choice.",
      ),
    ]),
    "negotiate" => Some(vec![
      style::section_heading(style::EMOJI_BRIEFING, "Help: negotiate"),
      style::label_value(
        "  Usage",
        &format!(
          "{} {}",
          style::accent("negotiate"),
          style::dim(
            "payer=carrier_a|carrier_b|medicaid|medicare rate_posture=aggressive|neutral|conservative"
          )
        ),
      ),
      style::label_value(
        "  Description",
        "Renegotiate commercial payment rates with insurance carriers, or align public Medicaid/Medicare compliance.",
      ),
      style::label_value(
        "  Resource Costs",
        "Commercial (carrier_a/carrier_b): 1 AP, $0 cash, 2 PC.\n  Medicaid: 1 AP, $5 cash, 2 PC (neutral posture only).\n  Medicare: 1 AP, $10 cash, 2 PC (neutral posture only).",
      ),
      style::label_value("  Postures", ""),
      style::dim(
        "    - aggressive: Demand maximum rates (Commercial only). High revenue potential but risks contract renewal failure if you lack leverage.",
      ),
      style::dim(
        "    - neutral: Propose balanced rate increases (Commercial), or align Medicaid/Medicare compliance.",
      ),
      style::dim(
        "    - conservative: Offer concessions for a guaranteed renewal (Commercial only).",
      ),
      style::label_value(
        "  Strategic Guidance",
        "Commercial negotiations require leverage to succeed. Medicaid compliance alignment represents lobbying/compliance and does not increase market share; instead, it directly improves access index (+3) and reduces policy pressure (-3). Medicare compliance alignment represents quality reporting compliance and directly improves quality index (+3) and reduces policy pressure (-3).",
      ),
    ]),
    "commit" => Some(vec![
      style::section_heading(style::EMOJI_BRIEFING, "Help: commit"),
      style::label_value(
        "  Usage",
        &format!(
          "{} {}",
          style::accent("commit"),
          style::dim("pledge_type=access|quality|workforce level=<1-5>")
        ),
      ),
      style::label_value(
        "  Description",
        "Make public commitments to build trust and legitimacy with officials or resolve workforce disputes.",
      ),
      style::label_value("  Resource Costs", "Costs 1 AP, $0 cash, 1 PC."),
      style::label_value("  Pledges", ""),
      style::dim("    - access: Pledges to improve or protect healthcare access."),
      style::dim("    - quality: Pledges to enhance care quality indices."),
      style::dim("    - workforce: Pledges to accept RNA wage demands during workforce disputes."),
      style::label_value(
        "  Strategic Guidance",
        "Public commitments build political goodwill and long-term trust. Failing to meet your commitments will severely damage system credibility.",
      ),
    ]),
    "project" => Some(vec![
      style::section_heading(style::EMOJI_BRIEFING, "Help: project"),
      style::label_value(
        "  Usage",
        &format!(
          "{} {}",
          style::accent("project"),
          style::dim(
            "kind=ehr_epic|ehr_cerner|tower|clinic_network|emergency_pavilion budget=<int>"
          )
        ),
      ),
      style::label_value(
        "  Description",
        "Launch major multi-month infrastructure and capital projects.",
      ),
      style::label_value(
        "  Resource Costs",
        "Costs 2 AP (at start), monthly cash draw equal to budget divided by duration.",
      ),
      style::label_value("  Project Kinds & Durations", ""),
      style::dim("    - ehr_epic: EHR implementation. Duration 12 months."),
      style::dim("    - ehr_cerner: EHR implementation. Duration 12 months."),
      style::dim("    - tower: Facility tower construction. Duration 12 months."),
      style::dim("    - clinic_network: Clinic network expansion. Duration 9 months."),
      style::dim(
        "    - emergency_pavilion: Emergency department pavilion expansion. Duration 6 months.",
      ),
      style::label_value(
        "  Constraints",
        "Maximum of 2 concurrent projects allowed at any time.",
      ),
      style::label_value(
        "  Strategic Guidance",
        "Projects provide powerful long-term benefits but tie up monthly cash flow. Make sure your cash reserves can support the monthly draws over the duration.",
      ),
    ]),
    _ => None,
  }
}

#[cfg(test)]
fn guidance_has_no_outcome_spoilers(text: &str) -> bool {
  let lower = text.to_ascii_lowercase();
  ![
    "reject",
    "counter",
    "grant flexibility",
    "work action",
    "full partnership",
    "accelerate",
    "partialretreat",
    "state hash",
  ]
  .iter()
  .any(|token| lower.contains(token))
}

#[cfg(test)]
mod tests {
  use super::*;

  #[test]
  fn help_text_avoids_actor_outcome_spoilers() {
    for context in [
      PromptContext::ResumeChoice,
      PromptContext::PlayMode,
      PromptContext::Seed,
      PromptContext::TurnCommand { turn: 1 },
      PromptContext::BeginnerTurn { turn: 2 },
      PromptContext::ReplayExport,
      PromptContext::CompetitiveCommand,
    ] {
      let text = context_help_lines(context).join("\n");
      assert!(
        guidance_has_no_outcome_spoilers(&text),
        "help for {context:?} leaked spoilers"
      );
    }
  }

  #[test]
  fn turn_hints_avoid_actor_outcome_spoilers() {
    for turn in 1..=5 {
      if let Some(hint) = turn_hint(turn) {
        assert!(guidance_has_no_outcome_spoilers(hint));
      }
    }
  }

  #[test]
  fn competitive_help_lists_available_commands() {
    let text = context_help_lines(PromptContext::CompetitiveCommand).join("\n");
    assert!(text.contains("Available commands"));
    assert!(text.contains("invest"));
    assert!(text.contains("recruit"));
  }

  #[test]
  fn payer_help_mentions_leverage_without_spoilers() {
    let text = context_help_lines(PromptContext::TurnCommand { turn: 1 }).join("\n");

    assert!(text.contains("above-target rates"));
    assert!(text.contains("visible payer leverage"));
    assert!(guidance_has_no_outcome_spoilers(&text));
  }

  #[test]
  fn test_topic_help_for_valid_verbs() {
    for verb in [
      "hold",
      "invest",
      "recruit",
      "monitor",
      "negotiate",
      "commit",
      "project",
    ] {
      let help = context_help_lines_with_topic(PromptContext::CompetitiveCommand, Some(verb));
      let text = help.join("\n");
      assert!(text.contains("Help:"));
      assert!(text.contains("Usage"));
      assert!(text.contains("Description"));
      assert!(guidance_has_no_outcome_spoilers(&text));
    }
  }

  #[test]
  fn test_topic_help_for_invalid_verb() {
    let help =
      context_help_lines_with_topic(PromptContext::CompetitiveCommand, Some("invalid_verb"));
    let text = help.join("\n");
    assert!(text.contains("Help: unknown topic"));
    assert!(text.contains("No specific help available"));
  }

  #[test]
  fn test_topic_help_for_non_competitive_context() {
    let help = context_help_lines_with_topic(PromptContext::Campaign, Some("recruit"));
    let text = help.join("\n");
    assert!(text.contains("Help: topic 'recruit'"));
    assert!(text.contains("Command-specific help is only available"));
  }
}
