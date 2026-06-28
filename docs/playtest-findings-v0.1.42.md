# Playtest Findings Report (v0.1.42)

**Date:** 2026-06-28  
**Slice:** Gameplay testing via local stdio MCP server (`stabilization-v1` and `competitive-regional-v1` campaigns)  
**Codebase:** v0.1.42; 86 tests; GitHub Actions CI  
**Playtesters:** `player_fiscal` (Fiscal Cautious), `player_growth` (Capacity Expansion), `player_balanced` (Strategic Balanced)

---

## 1. Playtest Sessions Summary

We ran three automated test players with distinct strategy profiles to play the game via the local Model Context Protocol stdio server. All runs were executed on seed `42` with default parameters.

### Stabilization Campaign (`stabilization-v1` - 5 Turns)

| Strategy Profile | Ending Cash | Reported Access | Workforce Trust | Community Trust | Rate Path | Result / Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Fiscal Cautious** | 64 | 75 (+5) | 64 (+2) | 69 (+3) | 104% | Completed; stable runway; moderate policy pressure |
| **Capacity Growth** | 15 | 92 (+22) | 67 (+5) | 73 (+7) | 100% (Bid Rejected) | Completed; severe cash depletion; high trust/access |
| **Balanced Strategy** | 32 | 89 (+19) | 68 (+6) | 73 (+7) | 100% (Bid Rejected) | Completed; moderate cash reserves; high trust/access |

### Competitive Campaign (`competitive-regional-v1` - 3 Months, Normal Difficulty)

| Strategy Profile | Ending Cash | Staffed Beds | Access Index | Workforce Trust | Community Trust | Political Capital | Insolvency Risk |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Fiscal Cautious** | 50 | 122 (+2) | 70 (+2) | 58 (-4) | 65 (-1) | 12 (+4) | **Low** (Stable cash runway) |
| **Capacity Growth** | 5 | 129 (+9) | 70 (+2) | 54 (-6) | 64 (-2) | 12 (+4) | **Critical** (Severely depleted cash) |
| **Balanced Strategy** | 25 | 125 (+5) | 73 (+5) | 56 (-6) | 66 (+6) | 11 (+3) | **High** (Tight cash, ongoing negotiations) |

---

## 2. Playtest Rubric Evaluation

We evaluated the gameplay against the six dimensions of the project's observation rubric (defined in the external playtest protocol), scoring each from 1 (poor/failing) to 5 (excellent).

### 1. Comprehension: 5/5
- **Evidence:** The test agents successfully navigated command parameters, legal boundaries, and resources. Both the stabilization inputs (numeric fields) and the competitive command grammar (e.g. `invest domain=beds amount=25; ...`) were easily parsed by the server without syntax errors. The autocomplete and help logs are highly informative.

### 2. Strategic Tension: 4.5/5
- **Evidence:** The central tension between cash preservation and access expansion is extremely prominent. Commercial insurers reject rate increases if access or quality is deemed "adequate" (occurring for both growth and balanced players in stabilization Turn 1 when requesting rate paths of 115% and 112% under 71 reported access). This forces the player to manage cash runway carefully instead of spamming investments.

### 3. Causal Transparency: 4/5
- **Evidence:** The debrief reports clearly attribute outcomes to decisions and events. In competitive Month 1, the impact of Northlake's aggressive bed investments (-25 cash) is immediately visible in the next month's report. The delayed resolution of nurse recruitment (+4 staffed beds arriving a month late) is highly transparent.

### 4. Pacing: 5/5
- **Evidence:** The turn-based structure allows deliberate decision-making. Information density is high but logical (separating reported metrics, intelligence logs, and policy briefings). No information overload was encountered.

### 5. Action Overload: 4.5/5
- **Evidence:** The Action Point (AP) economy in the competitive campaign (3 AP per month on Normal difficulty) effectively restricts option overload, forcing players to prioritize (e.g., deciding whether to spend 1 AP to monitor a rival or save it for direct recruitment/capacity moves).

### 6. Debrief Value: 5/5
- **Evidence:** The debrief at the end of the sessions successfully distinguishes between *decision quality* (making reasonable commitments with incomplete observations) and *outcome quality* (dealing with labor shocks or aggressive competitor behavior). Stakeholder credibility (e.g., labor union responses to schedule relief) is clearly explained.

---

## 3. Analytical Evaluation

### A. Winnability and Clearability

- **Game is Winnable:** Yes. A fiscally cautious approach can easily navigate both stabilization (ending with 64 cash) and competitive campaigns (ending with 50 cash) without risk of default, while slowly improving access and building political capital.
- **High Strategic Difficulty:** The capacity-expansion "Growth" strategy is extremely high-risk. On Normal difficulty, going all-in on beds and nurse recruitment depleted cash to 5 by Month 3. While it increased beds from 120 to 129, it left the system highly vulnerable to default if negotiations with Carrier A do not yield rate increases in Month 4.
- **Pacing is Fair:** The game does not force instant defeat; rather, it allows players to recover by scaling back investments and utilizing public access commitments (which cost 0 cash but increase reported access).

### B. Entertainment and Strategy Depth

- **Non-Determinism is Consequential:** Random monthly events (such as the Month 1 and Month 2 labor market shocks, which added +5 and +6 pressure to nurse recruitment timelines) prevented players from predicting exact transition outcomes.
- **No Dominant Strategy:**
  - *Growth* achieves high access (Access Index 92 in stabilization) but runs a severe insolvency risk.
  - *Fiscal Caution* secures the runway but results in low access improvement, rising policy pressure (from 30 to 48 in stabilization), and strained workforce trust.
  - *Balanced* provides the best compromise but requires high cognitive planning to avoid cash depletion.
- **Competitor Observability:** The "fog-of-war" created by lagging public reports of rival actions (e.g., seeing Northlake Health's Month 1 expansion only in Month 2) makes the `monitor` command a vital tool rather than a generic utility.

---

## 4. Identified Issues and Potential Fixes

1. **Insurer Bargaining Opacity:**
   - *Issue:* It is not immediately obvious to players what threshold of reported access/quality makes a rate request acceptable. In stabilization Turn 1, the insurer rejected both 112% and 115% rate requests because reported access (71) was "adequate".
   - *Fix:* In interactive beginner mode or help files, add a brief tooltip explaining that commercial insurers require leverage (e.g., high capacity/quality or low competitor capacity) to accept above-inflation rate hikes.
2. **Workforce Attrition Speed:**
   - *Issue:* Recruitment is highly expensive (recruit 6 nurses costs 30 cash) and is subject to delays and shocks. If rivals recruit simultaneously, workforce trust is strained.
   - *Fix:* Ensure the debrief details how rival recruitment actions affect salary inflation and attrition rates to make the labor market competitive dynamics clearer.

---

## 5. Summary of Changed/Verified Files

- **`docs/playtest-findings-v0.1.42.md`** (this file): Documented the playtest run findings.
- **`Cargo.toml`**: Bumped version to `0.1.43` per versioning policy for the upcoming release.
- **`CHANGELOG.md`**: Updated to document the playtest release.
