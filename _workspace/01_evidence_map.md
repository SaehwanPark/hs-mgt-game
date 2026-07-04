# Evidence Map - Competitive Autocomplete Hardening (Phase 1)

## Scope
This slice is a purely technical UI/UX enhancement for the competitive command-line interface.

## Sources Reviewed
1. **docs/cli-command-grammar-draft.md** (Section: Autocomplete)
   - *Key finding:* Defines the expectations for Tab autocompletion:
     - Verb completion (already implemented).
     - Argument key completion (e.g., typing `invest ` and Tab cycles `domain=` and `amount=`).
     - Enum value completion (e.g., typing `invest domain=` and Tab cycles `beds`, `outpatient`, `technology`).
     - No filesystem completion.

## Mechanisms and Abstractions
1. **State-Free Text Completion:**
   - The autocompletion candidates are derived solely from the command grammar schema and the user's typed line prefix.
   - The command schema defines static arguments and enum domains for each verb.
