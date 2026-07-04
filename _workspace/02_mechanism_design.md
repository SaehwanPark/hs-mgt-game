# Mechanism Design - Competitive Autocomplete Hardening (Phase 2)

## Scope
Defines the technical autocompletion engine for the competitive command CLI.

## 1. REPL Autocomplete State Machine
The autocompleter parses the segment of the line from the start or from the last semicolon (`;`) up to the cursor position `pos`.

1. **Active Segment Extraction:**
   - Find the last index of `;` before `pos`. Let this be `segment_start`.
   - The active segment is `line[segment_start..pos]`.
   - The offset where completion begins is `segment_start + leading_whitespace_offset`.

2. **Tokenizer & Context Identification:**
   - Split the active segment by whitespace.
   - If there is 1 token and the cursor is right at its end (no trailing whitespace), we are in **Verb Completion** mode.
   - If there are multiple tokens, or if there is a trailing space after the first token, we look at the first token as the `verb`.
   - If the `verb` is not a valid competitive verb, abort completion (return empty candidates).
   - If it is valid, identify the word currently under the cursor (from the last space before the cursor to the cursor).
   - If the current word contains `=`:
     - Split at `=` into `key` and `val_prefix`.
     - We are in **Enum Value Completion** mode for the argument `key`.
   - Otherwise, we are in **Argument Key Completion** mode.

3. **Argument & Enum Value Mapping:**
   - **invest**: `domain` (`beds`, `outpatient`, `technology`), `amount` (integer)
   - **recruit**: `role` (`nurse`, `physician`, `admin`), `headcount` (integer)
   - **monitor**: `target` (`northlake`, `summit`, `valley`, `metro`), `depth` (integer)
   - **negotiate**: `payer` (`carrier_a`, `carrier_b`), `rate_posture` (`aggressive`, `neutral`, `conservative`)
   - **commit**: `pledge_type` (`access`, `quality`), `level` (integer)
   - **project**: `kind` (`ehr_epic`, `ehr_cerner`, `tower`, `clinic_network`), `budget` (integer)

4. **Argument Key Deduplication:**
   - During **Argument Key Completion**, exclude keys that are already present as tokens in the current command segment.
