# Chain contract (DRAFT r0 — 2026-09-28)

Note (2026-09-28): the artifact seed-me saves is now called the **seed contract** (`seed-contract.md`); older text and files may still say "pre-intent".

Status: **draft for the operator's review. Nothing here is implemented or approved.**
Sources: the AI-Native SDLC Playbook (`references/ai-native-sdlc/`, chapters 1–14) and the
operator's addition, `seed-contract.md`, an epistemic precursor to `intent.md`.

Purpose: define, for every stage, what it consumes, what it emits, what triggers it, who
gates it, and what enforces it deterministically, so each stage can be aligned to the one
before it. Stage-scoped work must not invent its own interface; it conforms to this file or
proposes a change to it.

## 1. Principles

1. **The committed artifact is the only handoff.** A stage ends by committing one artifact;
   the next begins by reading it. No conversation state crosses a boundary.
2. **Acceptance is the trigger.** An accepted artifact starts the next stage. Humans
   concentrate at gates and review what the agent flagged; they do not start each stage.
3. **Authority is typed and travels.** Every decision carries `evidence | user | delegated`
   plus its source. Downstream artifacts may condense it but never drop or upgrade it.
4. **Advisory versus deterministic.** Skills and `CLAUDE.md` make violations rare; hooks,
   CI and branch protection make them close to impossible. A policy that must always hold
   needs a deterministic backer.
5. **Evidence comes from the toolchain, not the agent's claim.** Literal command output,
   check runs, screenshots. Local receipts track workflow; they are not release authority.
6. **The agent acts up to a gate and cannot pass it.** No self-approval, no invented
   reviewer, no fabricated sign-off.
7. **Upstream change stales downstream approvals.** Preserve feedback, revise, re-approve.
   Post-hoc changes to an upstream artifact are a measured rework signal.
8. **One source of truth per artifact.** Others hold a copy or a link.
9. **Weight matches consequence.** Routine work takes a light path; ceremony is not the default.

## 2. The spine: what must survive every handoff

| Field | Origin | Rule downstream |
|---|---|---|
| Goal | confirmed in Stage 0 | fixed; refinements are new decisions, a replacement goal is a new run |
| Constraints and exclusions | Stage 0 | never re-proposed as alternatives; conflicts are surfaced, not resolved silently |
| Decisions + authority + source | Stage 0 (`ledger.json`) | may be condensed, never re-typed; delegated stays delegated |
| Acceptance checks | Stage 0 | each is an exact command, expected output and where it runs; Stages 2–4 consume them verbatim and may add but not weaken |
| Risks and open items + owner | Stage 0 | become Stage 2 "areas of concern" or documented non-blocking deferrals with a revisit condition |
| Provenance link | every stage | `derived-from: <artifact path>@<content hash>, revision` in the header |

## 3. The chain

| # | Stage | Emits | Consumes | Trigger | Human gate | Deterministic enforcement | Evidence |
|---|---|---|---|---|---|---|---|
| 0 | Discover (seed-me) | `seed-contract.md` (+ ledger, viewer snapshot) | raw prompt, braindump, plan or hunch; or a machine finding (route B) | a person's idea, or Stage 6 | originator affirms the displayed revision label | ledger validator, atomic writes, single-decision pacing, citation rule | `ledger.json` with typed authority, and history |
| 1 | Plan (validate) | `intent.md`, `validation-report.md` | confirmed `seed-contract.md` + ledger, read-only | seed contract confirmed | product owner accepts, reading the warnings | read-only validator (separate context); hash link to seed contract; warn-only | report rows with receipts and finding codes |
| 2 | Design | `spec.md` | accepted `intent.md`, policy skills | intent accepted | product owner, plus tech lead for higher risk; flagged concerns routed to policy owners | skills (advisory); hooks or review re-check for must-hold policies | spec, prompt, skill versions in force |
| 3 | Build | `plan.md`, code | accepted `spec.md` (+ intent), `CLAUDE.md`, skills | spec accepted | engineer accepts the plan; architect for higher risk | plan mode is read-only until accepted; protected-path hooks; plan and diff kept in sync | `plan.md` revisions |
| 4 | Test | verification evidence, locked tests, eval results | plan and spec acceptance checks, `CLAUDE.md` commands | implementation in an isolated worktree | none for the mechanical check; the code owner sees its output at Stage 5 | test-file edit hook, CI, evals gating any `CLAUDE.md`/skill/hook change | literal toolchain output, check runs |
| 5 | Deploy | PR, `REVIEW-findings`, release | diff, `plan.md`, `spec.md`, `REVIEW.md` | PR opened | human code owner via branch protection; release manager for production | branch protection, production-gate hook, required CI | PR history is the audit record |
| 6 | Maintain | machine-originated Stage 0 input | telemetry, `bands.yaml`, tickets, channel messages | band breach, ticket, schedule, tag | service owner triages: fix, schedule or dismiss | deterministic detection script; tiered response; scoped permissions | detector log with tier and timestamp |

Policy plane (configuration of the chain, not stage artifacts): `CLAUDE.md`, skills, hooks,
managed settings, `REVIEW.md`, `bands.yaml`, eval suite. Changes to these are reviewed like
code, and eval-gated where they steer the agent.

## 4. Stage 0 to Stage 1: validation, not projection

`seed-contract.md` is the epistemic precursor: what is known, who decided it, and how each claim
is grounded. Stage 1 **validates** it against repo reality and emits a sharper `intent.md`.
The validator asks questions of the *repo*; it does not re-interview the user.

**Validator (settled, r1):** a separate agent context, powered by TypeSafe Jev, with one small
custom skill. Start lean; add checks only when dogfooding shows clusters of errors.
**Read-only:** it writes nothing to the repo and nothing to the seed-me ledger. Its only outputs are
its own two artifacts below. **Warn-only:** a finding never blocks; it is recorded.

Inputs: confirmed `seed-contract.md` (pinned by hash) and its `ledger.json`, read-only.
Outputs:

1. `intent.md`, one page, sharpened by evidence only (see the authority rule).
2. `validation-report.md`, one row per checked claim.

What it checks (all static and read-only for now):

| Check | Example |
|---|---|
| Claim still true | the cited `file:line` still contains the quoted text at the current HEAD |
| Claim freshness | cited sources unchanged since the seed contract's session start (stale watch) |
| Acceptance command is well-formed | binary exists, referenced test/script path exists, cwd exists |
| Constraint conflict | scope touches a path `CLAUDE.md` or a policy skill marks frozen or protected |
| Boundedness | affected systems named in the seed contract exist in the repo |

Not in scope yet: **executing** acceptance commands (even a read-only test run can write caches;
revisit when there is a throwaway-worktree rule), and any write-back to the ledger.

**Finding classes.** Every report row carries one code so dogfooding can cluster errors later:
`confirmed`, `corrected` (fact differs; receipt given), `stale`, `refuted`, `unverifiable`,
`malformed-check`, `constraint-conflict`. All non-`confirmed` rows are warnings.

**Authority rule.** The validator may state facts (`authority: evidence`, with a receipt). It may
not settle or narrow a decision. Where sharpening would need a choice, it leaves the original
wording and adds a flagged item; it never picks an interpretation on its own authority.
`intent.md` therefore has an explicit **Validation warnings** section, so the human accepting it
sees what the validator could not resolve.

**Consequence of warn-only + read-only.** Because it does not reopen ledger nodes, a refuted
claim leaves `seed-contract.md` and `intent.md` disagreeing. That is intentional and visible: the
disagreement is recorded as a `refuted`/`stale` row with its receipt, and the product owner
resolves it at the Stage 1 gate (accept as-is, or send back to seed-me by hand). The report is the
data for the self-improving loop; automated reopen is deferred until warning clusters justify it.

`intent.md` mapping (section content comes from the seed contract, corrected only by evidence):

| `seed-contract.md` | `intent.md` |
|---|---|
| Problem statement | 1. Problem |
| Proposed outcome | 2. Proposed outcome |
| Affected users and systems | 3. Affected users and systems |
| Constraints and boundaries | 4. Constraints |
| Open questions and deferrals | 5. Open questions (non-blocking only) |
| Acceptance criteria (exact commands) | **new** Acceptance checks, verbatim |
| Accepted decisions with authority | **new** Decisions, condensed, authority tag kept |
| (validator) | **new** Validation warnings, linking `validation-report.md` |
| Risks | carried to Stage 2 as areas of concern |
| Evidence, migration footer, suggested first slice | stay in `seed-contract.md`, linked by hash |
| Title and provenance | header: `derived-from: seed-contract.md@<sha256> rev <n>; validated-at: <HEAD sha>` |

Rules: `intent.md` fits about a page. Changing a settled decision in a confirmed seed contract
invalidates the downstream intent (principle 7).

Partition of "check against the repo" across stages:

| Stage | Question put to the repo |
|---|---|
| 1 validate | Is the ask real and current, and are its checks well-formed? |
| 2 spec | Does the design conform to organizational policy and design skills? |
| 3 plan | What is the implementation path (files, order, risks)? |

## 5. Entry routes

- **Route A, human.** Interactive seed-me interview, then confirmation, then projection.
- **Route B, machine (Stage 6).** No one to interview. Proposed (D2): the agent writes a
  seed contract whose facts are `authority: evidence`, whose consequential decisions stay
  `unresolved`, and whose gate is the service owner's triage. Nothing settles by
  `delegated` unless a pre-authorized policy exists for that decision class. It passes through the
  same validator, which is the point: route B has no interview, so validation is its only filter.

## 6. Where the current repos stand

| Repo | Covers | Gap against this contract |
|---|---|---|
| `tink-skills/seed-me` | Stage 0 route A | no route B; heavy output relative to Stage 1; nothing produces `intent.md` |
| `ai-native-sdlc` | run scaffolding, Stage 1–3 decisions, verification receipts, bug test locks | nothing reads `seed-contract.md`; no `intent.md` mapping; `decide` covers stages 1–3 only; no PR step; verification ships unconfigured |
| `tink-route` / `tink` | skill routing and installation (policy plane) | not yet tied to stage triggers |

## 7. Decisions

Settled (operator, 2026-09-28):

- **D1** Stage 1 validates the seed contract against the repo and emits `intent.md`; it is not a projection.
- **D1a** Validator is a separate agent context (TypeSafe Jev) with one custom skill; grow it only as dogfooding clusters errors.
- **D1b** Read-only. It writes nothing to the repo or the ledger.
- **D1c** Warn-only. Findings never block; they are recorded with a finding code.
- **D3** Artifact home is `runs/<slug>/` (as in `ai-native-sdlc`): it compartmentalizes work and allows multiple concurrent runs. The playbook's `intent/` folder is not used. Consequence: every stage artifact, `validation-report.md` included, lives under its run and is bound to that run's `run.json`.

Open:

- **D2** Route B: machine-written seed contract with unresolved decisions (proposed), then the same validator.
- **D4** How the light `brief.md` (intent + spec + plan merged) relates to the chain.
- **D5** Solo-operator roles: who fills product owner, tech lead and code owner, and how self-gates are prevented.
- **D6** Whether the spine fields in section 2 are enforced by a validator or only by convention.
- **D7** What Jev does inside the validator (classification of findings? claim extraction? the reasoning itself?). Not yet read; do not assume. Seed-me previously stripped its Jev routing (`3590a46`), so record why before reintroducing it.
- **D7 / D8** Under research (two pi subagents, model `meta/muse-spark-1.3-contributor`, dispatched 2026-09-28). Until reports return, D8 stays as the working assumption: no execution of acceptance commands.

## 8. Stage-scoped work units (for later dispatch)

Each unit gets one stage's chapter(s), this contract and the stage before it. Each proposes
changes as a reviewable diff and does not edit across its boundary. Cross-stage conflicts
return to the systems thinker and then the operator.

| Unit | Chapters | Repo scope | Deliverable |
|---|---|---|---|
| U0 seed-me | 2 | `tink-skills/skills/seed-me` | gap report and proposed changes: lighter output, route B, intent projection |
| U1 validate and intent | 2 | `ai-native-sdlc` stage 01 | validator skill (lean), `validation-report.md` and `intent.md` templates, finding codes, gate |
| U2 spec | 3, 6 | stage 02 | spec template consuming the spine, concerns from Stage 0 risks |
| U3 plan and build | 4, 5, 6, 7 | stage 03 | plan template, plan/diff sync, worktree rules |
| U4 test | 8, 9 | stage 04 | acceptance checks to `verification.json`, locks, evals |
| U5 deploy | 10, 11, 12 | stage 05 | PR step, `REVIEW.md` alignment, release gate |
| U6 maintain | 13 | stage 06 | route B emitter, `bands.yaml`, triage gate |
