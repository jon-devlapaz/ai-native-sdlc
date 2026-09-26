# SOP: Jev-Assisted Code Verification

Standard Operating Procedure for verifying code findings, triage candidates, and risk tiers using TypeSafe Jev before implementation.

## 1. Architectural Role Division

This procedure implements the System One / System Two division of labor:

- **System One (TypeSafe Jev)**. Evaluates atomic questions against structured JSON state in parallel. Returns model-estimated probabilities in under 300ms. Used for epistemic triage, risk scoring, safety checks, and convention alignment. Jev estimates likelihoods; it never grants authorization to edit files.
- **System Two (Generative Agent)**. Identifies candidate findings, proposes solutions, writes code patches, runs compilers, and executes test suites under human instruction.
- **Deterministic Tooling**. Compilers, linters (`ruff`), formatters (`cargo fmt`), and cryptographic hashes (`sha256sum`). Deterministic tool output always supersedes probabilistic model judgments.

## 2. Prerequisites (Step 0)

TypeSafe Jev requires explicit operator opt-in. The tool refuses calls without activation:
- Interactive session: run `/typesafe enable` and confirm the data notice.
- Headless or automated runs: set `PI_TYPESAFE_ENABLED=1` in the environment.
- Credentials: ensure an authenticated key exists at `~/.pi/agent/pi-typesafe/auth.json` or via `TYPESAFE_API_KEY`.

## 3. Jev Primitives and Question Construction

Jev answers three atomic primitives. Never combine multiple dimensions into a single question.

### Noul (Truth Verification)
Use Noul to check whether a specific factual statement about the state is supported.
- Example: "Does removing `tempfile` from `dev-dependencies` leave any unresolved imports in the test suite?"
- Returns: `noul` probability $P \in [0.0, 1.0]$.

### Score (Risk and Complexity Rubric)
Use Score to position a finding along an ordered, objective rubric.
- Example criteria:
  0: Zero runtime or test risk (dead comment, stale gitignore).
  1: Low risk requiring local test verification (unused import, redundant dev-dep).
  2: Moderate risk with potential side effects (internal logic refactor).
  3: High risk (breaking API change, schema migration).
- Returns: `score` position and probability distribution across rubric levels.

### Choice (Convention and Remediation Alignment)
Use Choice to select the appropriate fix pattern from mutually exclusive alternatives. The tool automatically appends a fallback option.
- Example criteria: `{ convert_to_unittest: "Convert to unittest.TestCase", switch_ci_to_pytest: "Switch CI to pytest", ignore_tests: "Keep unrun" }`.
- Returns: `choice` key and confidence score.

## 4. The 5-Step Verification Lifecycle

```
[Candidate Finding] ──> [Batch Jev Evaluation] ──> [Epistemic Routing]
                                                           │
               ┌───────────────────────────────────────────┴──────────────────────────────┐
               ▼                                                                          ▼
      Strong Evidence (P ≥ 0.85)                                                 Weak Evidence (P < 0.85)
               │                                                                          │
      [Propose for Execution]                                                    [Mechanical Probe or Escalation]
               │                                                                          │
      [Operator Authorization]                                                   [Human Gate via Questionnaire]
               │                                                                          │
      [Worker Implementation] ──> [Reviewer Verification] ──> [Verified Commit]
```

### Step 1. State Normalization
Structure the candidate finding into a clean JSON object. Group multiple findings under named keys (`items.<name>`):
```json
{
  "items": {
    "tink_tempfile": {
      "file": "tink/Cargo.toml",
      "issue": "tempfile = \"3.27.0\" is declared in both [dependencies] and [dev-dependencies]."
    }
  }
}
```

### Step 2. Batched Parallel Query
Package all Noul, Score, and Choice questions into a single request. Batching up to 32 questions executes in parallel with no latency penalty:
```json
{
  "state": { "items": { ... } },
  "questions": {
    "tempfile_safe": { "type": "noul", "instructions": "..." },
    "tempfile_risk": { "type": "score", "instructions": "...", "criteria": [...] }
  }
}
```

### Step 3. Epistemic Routing Matrix

Never use model confidence as authorization to act. Use probabilities only to classify evidence readiness:

| Metric | Range | Evidence Classification | Required Action |
| :--- | :--- | :--- | :--- |
| **Noul Truth** | $P \ge 0.85$ | Supported premise | Present finding to operator for implementation authorization. |
| **Noul Truth** | $0.65 \le P < 0.85$ | Ambiguous premise | Execute mechanical probe or grep before presenting. |
| **Noul Truth** | $P < 0.65$ | Unsupported premise | Reject finding or escalate as open uncertainty. |
| **Choice Confidence** | $\text{conf} \ge 0.85$ | Clear convention fit | Recommend selected convention in proposal. |
| **Choice Confidence** | $0.65 \le \text{conf} < 0.85$ | Borderline fit | Note alternatives alongside the leading option. |
| **Choice Confidence** | $\text{conf} < 0.65$ | Indeterminate fit | Escalate to human operator via structured questionnaire. |

### Step 4. Mechanical Validation
Probabilistic judgments must be confirmed by project checks:
- Python: `pytest` or `python3 -m unittest discover -s tests -v`.
- Rust: `cargo fmt --check` and `cargo test --quiet`.
- Cryptographic pins: `sha256sum <file>` against recorded manifest hashes.
If a mechanical test fails, halt immediately regardless of Jev probability scores. Deterministic results always override model judgments.

### Step 5. Dual-Agent Execution Separation
Never let the implementing agent approve its own change:
1. Operator authorizes the specific change.
2. `worker` subagent implements the fix and executes the local test suite.
3. `reviewer` subagent inspects `git diff`, re-runs test commands, and issues an explicit verdict (`APPROVE` or `CHANGES_REQUESTED`).
4. Only approved diffs are committed to git.
