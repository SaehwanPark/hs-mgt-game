#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum CampaignId {
  StabilizationV1,
  CompetitiveRegionalV1,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub enum Difficulty {
  Easy,
  Normal,
  Hard,
  Expert,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum CashRunwaySignal {
  Comfortable,
  Watch,
  Strained,
}

impl CashRunwaySignal {
  pub fn label(self) -> &'static str {
    match self {
      CashRunwaySignal::Comfortable => "COMFORTABLE",
      CashRunwaySignal::Watch => "WATCH",
      CashRunwaySignal::Strained => "STRAINED",
    }
  }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ConsultantOption {
  pub label: char,
  pub title: String,
  pub tradeoff_bullets: Vec<String>,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct PlayerObservation {
  pub org_name: String,
  pub reported_access_index: i32,
  pub prior_access_revision: Option<(u32, i32)>,
  pub reported_quality_index: i32,
  pub workforce_trust_summary: String,
  pub community_trust_summary: String,
  pub staffed_beds: i32,
  pub outpatient_capacity: i32,
  pub emergency_capacity: i32,
  pub icu_capacity: i32,
  pub obstetrics_capacity: i32,
  pub psychiatric_capacity: i32,
  pub cardiology_capacity: i32,
  pub oncology_capacity: i32,
  pub infusion_capacity: i32,
  pub nurses: i32,
  pub physicians: i32,
  pub admins: i32,
  pub in_flight_projects: String,
  pub cash_runway_signal: CashRunwaySignal,
  pub market_bullets: Vec<String>,
  pub policy_bullets: Vec<String>,
  pub annual_policy_review: Option<Vec<String>>,
  pub consultant_options: Vec<ConsultantOption>,
  pub intel_gaps: Vec<String>,
  pub rna_strike_active: bool,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct PolicyCalendar {
  pub month_index: u32,
  pub year: u32,
  pub month_in_year: u32,
}

impl CampaignId {
  pub fn as_str(self) -> &'static str {
    match self {
      CampaignId::StabilizationV1 => "stabilization-v1",
      CampaignId::CompetitiveRegionalV1 => "competitive-regional-v1",
    }
  }
}

impl Difficulty {
  pub fn k_rivals(self) -> u32 {
    match self {
      Difficulty::Easy => 1,
      Difficulty::Normal => 2,
      Difficulty::Hard => 3,
      Difficulty::Expert => 4,
    }
  }

  pub fn human_ap_per_month(self) -> u32 {
    match self {
      Difficulty::Easy => 4,
      Difficulty::Normal | Difficulty::Hard => 3,
      Difficulty::Expert => 2,
    }
  }

  pub fn cpu_ap_per_month(self) -> u32 {
    // Consumed by competitive AI turn resolver (slice I6).
    match self {
      Difficulty::Easy => 2,
      Difficulty::Normal | Difficulty::Hard => 3,
      Difficulty::Expert => 4,
    }
  }

  pub fn label(self) -> &'static str {
    match self {
      Difficulty::Easy => "Easy",
      Difficulty::Normal => "Normal",
      Difficulty::Hard => "Hard",
      Difficulty::Expert => "Expert",
    }
  }
}

impl PolicyCalendar {
  pub fn new_month(month_index: u32) -> Self {
    debug_assert!(month_index >= 1, "month_index must be >= 1");
    let month_in_year = ((month_index - 1) % 12) + 1;
    let year = ((month_index - 1) / 12) + 1;
    Self {
      month_index,
      year,
      month_in_year,
    }
  }

  pub fn advance(self) -> Self {
    Self::new_month(self.month_index + 1)
  }

  pub fn is_annual_tick(self) -> bool {
    self.month_in_year == 12
  }

  pub fn month_name(self) -> &'static str {
    match self.month_in_year {
      1 => "January",
      2 => "February",
      3 => "March",
      4 => "April",
      5 => "May",
      6 => "June",
      7 => "July",
      8 => "August",
      9 => "September",
      10 => "October",
      11 => "November",
      12 => "December",
      _ => "Unknown",
    }
  }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct CompetitiveRunConfig {
  pub seed: u64,
  pub difficulty: Difficulty,
}
