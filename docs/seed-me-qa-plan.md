# seed-me QA plan: verification, validation, and where Jev fits (DRAFT r0, 2026-09-29)

Status at initial drafting (2026-09-29): proposal. The later deterministic run
below records implemented conduct checks; it does not establish semantic quality.
Jev facts came from docs.typesafe.ai summaries, without a verified API trial.

Review disposition (2026-10-02, issue #36): retain this defect taxonomy and the
existing conduct checks. Provider requirements and probe-policy changes are
deferred. Historical prices, percentages, and suggested thresholds are not local
acceptance evidence. The [scope review](stage-01-scope-review.md) and
[evaluation record](evaluations/stage01-2026-10-02/README.md) describe current
evidence; issue #37 owns the pending full handoff evaluation.
Scope: quality of seed-me itself. Downstream stages are out of scope for now.

## Two questions, kept apart
- **Verification:** did we build seed-me the way its own spec says? (conformance: rules followed, formats stable, gates enforced)
- **Validation:** does seed-me help a person decide better and understand what was decided? (usefulness, agency, comprehension)

## Known defects, from real runs so far (the seed of the taxonomy)
| # | Defect class | Real instance | Status |
|---|---|---|---|
| 1 | Anchoring / rubber-stamping | 8 of 8 decisions accepted by arrow in the repo-triage run | mitigated for hard-to-undo questions only |
| 2 | Stale premise | Q1 answer kept saying "reuse its scanner" after a fact showed it was not built | rule + validator added; the live session is still stale |
| 3 | Unverified guess accepted | operator guessed the 9-file worktree was a crashed agent's; checking showed it was in use | caught by the interviewer, no rule yet |
| 4 | Sloppy definition | draft defined "safe" so a clean worktree with 4 unpushed commits would pass | caught by an operator, no rule yet |
| 5 | Format drift | the Karpathy contract's check lines had no `cmd:` label, so 0 of 4 real contracts parse the same way | open |
| 6 | Instruction deviation | interviewer started a session before the goal was confirmed | prose rule exists, not checked |
| 7 | Missing signposting | lean path never printed the ledger link | fixed |
| 8 | Unenforced guidance | "about five assumptions per turn", "at most two ungrounded questions" | convention only |
| 9 | Unverified layer | browser tests cannot run in the maintainer's sandbox; visuals checked by hand | open |
| 10 | Invented facts in demos | a demo used made-up numbers ("412 files") | lesson, no rule |

## Layers
1. **L0, deterministic (exists):** 65+ tests. Add *mutation checks*: seed a defect into the skill text or validator and confirm a test goes red. This measures the tests.
2. **L1, conduct rubric (new):** score every interviewer turn against atomic rules. Cheap checks in code first (regex: `Ledger:` line present, `Option A:`/`Option B:`, `Undo cost:`). Fuzzy checks go to Jev.
3. **L2, claim grounding (new):** every quoted `path:line` in a turn is string-matched against the file at that commit (code). A quote that matches is then judged supports / contradicts / says-nothing against the claim (Jev, the citation-check pattern from its cookbook).
4. **L3, simulated-operator suite (new):** a fixed set of idea + persona pairs, including engram operators, run against each skill version; compare per-rule pass rates across versions.
5. **L4, human dogfood (exists):** the real signal. Its labels calibrate L1 to L3.

## Where Jev fits (and does not)
Jev returns a probability over your options (`choice`, `score`) or a yes-probability (`noul`); several questions ride in one request cheaply; the docs steer it to snap judgments, extractive questions, small state, and to keep counting and date arithmetic in code.

**Good uses**
- Turn-level fuzzy rules, one atomic `noul` each, state = the single turn: *Is Option B a real alternative or a strawman? Does this turn bundle two decisions? Does it use jargon a first-time user would not know? Does the confidence stated match the evidence shown? On a hard-to-undo question, did the suggestion appear before the user's instinct?*
- Relevance: `score` (1-5) of how well each "What I found" line bears on the question.
- Operator-leakage detector over each operator reply: does it show knowledge it should not have (skill terms, ledger ids)?
- Defect clustering: a `choice` that assigns each failed check to a class in the table above. This is the "add machinery only when dogfooding clusters errors" rule made mechanical.
- Session-level: did the interviewer verify a factual guess before accepting it? (over the one exchange)

**Not Jev (keep in code or tests):** counting turns or options, parsing check lines, comparing timestamps, running tests, deciding whether a fact is true (needs tools), generating fixtures or defective turns.

## Making the judge trustworthy (QA of the QA)
- **Calibration set:** ~40 real interviewer turns that you label pass/fail per rule. Measure Jev's agreement; set a threshold per rule; below it, route to human review (the cookbook uses 0.8 as a starting point, which is unproven for these rules).
- **Mutation set:** scripted defective turns (delete the undo cost, put the suggestion first, bundle two questions, make B a strawman). Jev must flag them; this measures recall.
- **Pin the model** (`jev-1.13.0`) and log, per call: model, question, probabilities, threshold, auto or review. Alarm when the pinned model changes.
- **Never let the judge grade its own inputs unchecked:** exact-match and code checks run first; Jev sees only what code cannot decide.

## Data and cost
- Transcripts exist for this work: 2 Claude project transcripts in `~/.claude/projects/-Users-jondev-dev-active/` (this session has about 25 question turns) and 56 pi session folders. The 4 simulated-operator runs are the cleanest source: their content is fictional persona talk plus machine facts.
- Cost is small on the docs' reported price ($42 per billion input tokens): about 12 questions x 700 tokens x 25 turns is roughly 0.2M tokens, well under a cent. The real costs are your labeling time and privacy.
- **Privacy:** turns contain file paths and repo names. Sending them to a third-party API needs your explicit go-ahead. Mitigation: start with the simulated runs, redact paths, never send secrets.

## First slice (proposal)
1. A defect log file (this table) kept current.
2. `qa/conduct_rules.py` with the code-only rules (no Jev), run over the 4 simulated-run transcripts and this session: already useful, free, deterministic.
3. A labeling sheet of 40 turns for you (or a sampled 20), then the Jev rules on top.
4. Mutation checks for the existing tests.

## Open decisions
1. May turns (redacted) be sent to TypeSafe, and is there an API key to use?
2. Where does the suite live: inside `skill-eval-loop` (which already has JSONL tasks, traces, graders, and a judge-model rubric path) or in `tink-skills/qa/`?
3. How much labeling are you willing to do (20 or 40 turns)?

## First deterministic run (2026-09-29) — `tink-skills/qa/seed_me_conduct.py`
Ran on this session's transcript (20 checked turns), the 12 saved seed-me sessions, and the 4 contract files. 13 checker tests pass; the tests caught two bugs in the checker itself ("medium-high" slipping past the confidence rule; a turn missing Option B being ignored instead of flagged).

**Real findings (all in current-epoch turns, all by the interviewer):**
- `Confidence: medium-high` used in 3 turns; the template allows only low | medium | high.
- `Undo cost: if wrong…` (free text, not cheap | moderate | hard) in 2 operator-facing turns, the hidden-files question in both runs.
- Chat used a bare `Q1` once, and the lean-path template's own ids (G, D1, Q1) sit in tension with the names-not-ids rule.
- The Karpathy simulated contract: 0 of its check lines carry the `` cmd: ` `` label (the format-drift defect, now detected automatically).
- Ledgers: all 12 valid; 4 sessions accept 70% or more of decisions as suggested (5/5, 6/7, 7/7, 4/4); 6 sessions have decision sources that neither quote the user nor cite a turn, including a `delegated` decision justified by "Jev yes_build p=1.0" — a model score standing in for the user's delegation.

**Historic (before the rule existed, fixed since):** no `Ledger:` link on the first lean-run turn; turns before the calibration and "against" lines existed.
**False positives to expect:** design questions asked in the run format outside a run; the 450-word length flag.

## Defects found by the backup-cleanup runs (2026-09-29), and where they went
| # | Defect | Fixed by |
|---|---|---|
| 11 | A probe asked after the finding was revealed is not independent evidence | SKILL.md: ask open probes first; record "NOT independent" otherwise |
| 12 | A "repo to protect" was empty; a "redundant" folder held the only copy of 25 commits; framings were carried without checking | SKILL.md: confirm what a unit is before treating it as one |
| 13 | Operator summaries miscounted twice and called a decision an action already taken | SKILL.md and agent-mode.md: numbers come from commands; keep "decided" apart from "done" |
| 14 | An engram operator stamped an inference "documented" | agent-mode.md: check provenance claims against its material |
| 15 | The contract said "delete right away" and "nothing before the vault is safe" | SKILL.md local review: read decisions against each other for contradictions |
| 16 | "Durable" copies shared one disk; no independent backup existed | SKILL.md: recoverability probe for anything that deletes, moves, or replaces |
| 17 | A teach-back by an agent that sees the contract repeats it | agent-mode.md: record as weak evidence; a human's own words are still owed |
| 18 | A decision only the human can make (may the notes go on GitHub) | agent-mode.md: defer to the human owner; never fabricate |
