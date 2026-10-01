# Stage 01 intent reliability: implementation and verification spec

Status: **DRAFT — proposed, not approved for implementation**  
Revision: 0.1  
Prepared: 2026-09-30  
Target: `jon-devlapaz/ai-native-sdlc`  
Observed main commit: `a57339593d6616531767f2bcb2583fdcd0d1906b`  
Proposed repository home: `docs/stage-01-intent-reliability-spec.md`  
Decision owner: Jon; no approval is recorded by this document.

## 1. Purpose and authority

Improve the first development step so the next agent receives an evidence-grounded problem, observable success conditions, preserved constraints, explicit uncertainty, and the actual scope of permission.

This is a maintainer change spec. It does not add a required document to every project run. Existing light/full artifacts and approval gates remain in force. A GitHub issue, this draft, a model's recommendation, and a merged documentation-only PR do not independently authorize implementation or release.

The prior research discussion supplies candidate improvements, not proof that every improvement is needed. Before implementation, validate each finding against the selected checkout and distinguish a documentation gap from an observed behavioral failure.

## 2. Existing work to reconcile, not replace

| Source | Observed state | Consequence for this work |
|---|---|---|
| `assets/stages/01-plan/CONTEXT.md` [S1] | Light runs use a brief and checklist with one definition gate; full runs use intent; seed-me is used for consequential unresolved decisions. | Preserve both entry paths and actual human acceptance. Do not introduce a universal interview. |
| `assets/_shared/brief-template.md` [S2] | Contains problem/outcome, acceptance, approach, and risks/verification sections; checklist checks are used when automated proof exists. | A thin template is observable; its effect on agent behavior still needs a baseline. |
| `assets/_shared/intent-template.md` [S3] | Asks for problem, outcome, affected parties, boundaries, and open questions. | Evidence, assumption labels, and concrete examples are candidates for a small amendment. |
| Issue #1 [S4] | Open work already proposes thicker templates, stop conditions, and checkable acceptance. | Reuse or explicitly coordinate with #1. Do not create a duplicate template issue or silently enlarge its scope. |
| `docs/chain-contract.md` [S5] | Draft, containing recorded decisions about handoff preservation, a warn-only validator, and exact acceptance commands. Its implementation-gap section includes historical statements. | Review the recorded decisions and current implementation before revising them. Do not treat every historical gap as a current defect. |
| `docs/seed-me-qa-plan.md` [S6] | Starts as a draft but later records a deterministic run and defects. It explicitly scopes its original plan to seed-me, not downstream stages. | Reuse the taxonomy and relevant existing checks after inspection; add downstream coverage instead of a competing QA system. |
| `assets/_system/SDLC.md` [S7] | Documents seed copying/hash binding and stale dependent evidence. | Preserve and regression-test this mechanism; do not rebuild it. Unchanged bytes do not establish correct downstream interpretation. |
| Issue #35 [S8] | Contains several unrelated follow-ups, including old seed terminology. | Cross-reference the naming item only. Do not absorb the whole issue into this work. |

Issue descriptions and documentation are observations of what is recorded, not independent confirmation that every described implementation works. No runtime tests or agent trials were run while preparing this draft.

## 3. Validation before implementation

Create a finding disposition table in this spec or its linked review record. For every candidate finding record:

`finding ID | claim | observed revision/path | reproduction or example | confirmed gap / already handled / hypothesis / contradicted / deferred | action`

A reviewer must be able to distinguish:

- **Verified documentation gap:** a required field or instruction is absent in inspected material.
- **Reproduced behavior failure:** a retained run demonstrates the wrong behavior under a defined criterion.
- **Hypothesis:** a proposed change may improve quality or reduce effort; no local result establishes that yet.
- **Already handled:** preserve existing behavior and add regression coverage only where missing.

Recheck the current branch and relevant open PRs before dispatching implementation. Validate claims inherited from the research before using them as empirical justification; this spec does not adopt the earlier research percentages as acceptance thresholds.

### Decisions that must not be silently reversed

The following affect scope or prior policy and need an actual owner disposition before the corresponding change:

| Decision | Proposed treatment | Until resolved |
|---|---|---|
| Exact executable checks at discovery time | Permit behavior plus a planned verification method when the check does not exist; bind real commands later at the existing appropriate gate. | Treat as a proposal. Preserve current seed-me requirements and any approved contract. |
| Mandatory lean-path probes and teach-back | Evaluate risk-triggered use rather than assume fewer questions are better. | No upstream seed-me behavior change. |
| Warn-only validation versus blocking behavior | Keep findings advisory in the first slice; the existing owner gate decides. | Do not introduce an automatic semantic gate or new runtime state. |
| Required model/service for semantic review | First use reviewed cases and inspect existing evaluation tools. | No new service, credentials, external transcript sharing, or provider dependency. |
| Overlap with issue #1 | Agree which existing scope is reused and which requirements are new. | Do not close or redefine #1 through a partial implementation. |

## 4. Proposed requirements and acceptance checks

The following requirements become binding only for the explicitly approved slice. Requirement IDs connect the spec, issue, test cases, and PR evidence; they do not require a new runtime schema.

### R1 — Distinguish facts, requests, assumptions, and proposals

The normal Stage 01 output must keep an inspected observation separate from a user's preference, an unverified assumption, and an agent recommendation. Evidence references must identify what was actually inspected. Missing access means unknown, not absent.

**Acceptance case T1:** The user requests offline operation. The output retains it as a requested constraint without inventing customer-demand evidence. A file mentioned but inaccessible is recorded as uninspected, not nonexistent. An agent-proposed library remains a proposal until accepted.

**Verification:** Review the output against a fixture containing the original request, visible repository facts, and expected authority labels. Deterministic checks may confirm required fields; meaning requires reviewed examples. Fabricated evidence is a hard failure for that trial.

### R2 — Describe success, boundaries, and unchanged behavior

For a consequential behavior change, require an observable success example, a relevant failure/boundary example, and important behavior that must remain unchanged. A small change may use a short statement or justified non-applicability rather than an elaborate scenario.

**Acceptance case T2:** An upload-retry request produces a success case for a transient connection failure, a no-duplicate boundary, and unchanged rejection of unsupported formats. These are illustrative fixture expectations, not requirements for an existing upload product.

**Verification:** Human-review fixture expectations before running the agent. Check the content, not only the presence of headings. The reviewer must reject a document that has all headings but no meaningful distinction between success and failure.

### R3 — Preserve consequential decisions across the handoff

A derived intent/brief must carry accepted constraints and authority without silently dropping, narrowing, or upgrading them. Conflicts become visible findings for the existing decision owner. Use the existing seed reference and ordinary Markdown/checklist references first; do not add a decision database.

**Acceptance case T3:** An accepted constraint says no paid service. The next agent receives the handoff and proposes a paid service. The evaluation must identify a constraint violation even though the stored seed and its hash are unchanged.

**Acceptance case T4:** An agent suggestion remains a suggestion downstream. An approval limited to investigation does not become implementation or release permission.

**Verification:** A fresh-agent handoff test and independent review against the original fixture. Existing byte/hash tests remain separate. A model agreeing with its own summary is not independent evidence of semantic preservation.

### R4 — Resolve the uncertainty relevant to the next action

The output identifies the next permitted action, consequential unresolved choices and their owner, and non-blocking assumptions with revisit conditions. The agent inspects accessible facts before asking the user for them. It does not repeat settled questions.

**Acceptance case T5:** Repository configuration answers the database-version question. A separate compatibility choice belongs to the user. The agent inspects the former and surfaces the latter without silently selecting a policy.

**Acceptance case T6:** A request cannot yet justify implementation but can justify a bounded investigation. The output proposes the investigation and its decision purpose; it does not claim it was authorized or performed.

**Verification:** Compare retained tool traces and questions against reviewed fixture expectations. Do not optimize question count alone. Do not add a runtime gate in this slice to enforce semantic judgments.

### R5 — Preserve current safety and workflow boundaries

Keep the current light/full split, actual human decision recording, seed binding, stale-evidence behavior, isolated code-writing checkouts, unconfigured-verification failure, and distinction between local evidence and release authority. No synthetic evaluator or operator is a real human approver.

**Acceptance case T7:** Existing tests continue to pass; a fresh light run still has its existing single definition gate. An altered seed invalidates dependent evidence according to existing behavior. Evaluations use synthetic approvals only in isolated test fixtures.

**Verification:** Inspect and run existing tests, add coverage only where missing, and retain the output. Documentation or CI success alone does not authenticate a human approval.

### C1 — Candidate follow-up: verification methods before commands

When a new check does not yet exist, distinguish required behavior, the planned verification method, and executable checks that are actually available. No invented executable command is presented as existing proof. Before verification, required real checks must be configured and run.

**Acceptance case T8:** For a feature with no test entry point yet, the discovery output states behavior and planned testing without fabricating a passing command. An existing bug reproduction retains its exact known check.

**Condition:** Requires the owner decision above and coordinated changes in `tink-skills` and the handoff contract. Not automatically included in R1–R5.

### C2 — Candidate follow-up: risk-proportional questioning

Test lighter questioning on obvious reversible work without reducing safeguards on destructive or consequential work.

**Acceptance case T9:** A fully specified label correction does not acquire an unnecessary interview. A destructive-cleanup case still surfaces consequential uncertainty and verifies recoverability before any authorized mutation.

**Condition:** Requires an agreed interpretation of existing seed-me rules and an upstream change/evaluation. No claim of improvement from question count alone.

## 5. Implementation boundaries and sequence

### Slice A — Reconcile the findings and approve the spec

Documentation and evaluation design only. Inspect current code/tests and existing PRs; complete the disposition table; resolve or explicitly defer the decisions above; identify exact files and acceptance cases for the first change. Reuse the evidence taxonomy from the existing QA plan where it fits.

Deliverable: reviewed spec revision, baseline case definitions, and linked issue scope. No workflow behavior change or invented approval.

### Slice B — Smallest useful template and contract change

Starting scope: `assets/_shared/intent-template.md`, `assets/_shared/brief-template.md`, and `assets/stages/01-plan/CONTEXT.md`; necessary package manifest updates and tests. Coordinate with issue #1, whose complete scope is wider than this slice.

Express R1–R4 compactly and preserve R5. Keep the compiled stage context small; link supporting detail rather than paste the research into every run. Modify the canonical package under `assets/`, not an external sandbox copy. Do not alter `sdlc.py`, approval schemas, or upstream seed-me rules merely to make a documentation check pass.

Update conflicting non-normative guidance only through explicit review. Do not silently overwrite recorded decisions in `docs/chain-contract.md`.

### Slice C — Handoff evaluation and release evidence

Run the approved before/after cases with a fresh next-stage agent. Record failures, review disagreements, question burden, and constraints preserved. Only introduce additional runtime enforcement in a separately justified issue if repeat failures show that the smallest change is inadequate.

### Deferred scope

C1/C2 belong in separately approved upstream work where needed. No new universal discovery stage, dashboard, graph store, routing architecture, automatic approval, mandatory Jev integration, or assumed access to local transcripts. No reopening the paused pilot in issue #34 without its owner's direction.

## 6. Verification plan

### A. Existing package checks

These commands are documented in the inspected README [S9]. Run from the package checkout. They have **not** been executed for this draft.

```sh
python3 scripts/package.py --check
python3 -m unittest discover -s tests -p 'test_sdlc_*.py' -v
```

Retain exit status, test count, complete logs, commit, and environment. A passing zero-test discovery is not sufficient. After intentional payload edits, choose the actual release version and refresh the manifest using the documented packager; do not reuse the README's example version blindly.

Inspect current test names before prescribing additional commands. Any new runner and its CLI are proposed until implemented, reviewed, and exercised. Do not report a planned check as completed verification.

### B. Structural and integration tests

Verify that both generated profiles carry the approved minimum information and that existing decision/verification behavior remains unchanged. Include valid short examples and missing-information cases. Add negative tests that remove a required field or corrupt an existing binding and confirm the relevant test fails.

These tests establish format/integration behavior, not truth, comprehension, or product usefulness.

### C. Behavioral baseline and fresh-agent evaluation

Proposed starter suite: **12 reviewed cases, three repetitions per variant**. These counts are a small engineering pilot, not an evidence-based optimum or a claim of statistical sufficiency. Agree them before running and report per-case results.

Cover T1–T7 with clear tasks, unavailable evidence, contradictory constraints, misleading names, limited authorization, and an irrelevant-context variation. Add T8/T9 only for an approved candidate change. Mark facts available to the agent separately from facts withheld from it. Redact private material and obtain permission before external transmission.

Pin the baseline/candidate revision, model, settings, tools, repository fixture, and budget; record actual availability and provider limits. Use the same fixed user answers and counterbalanced case order. Keep the new handoff agent free of the original conversation, but give it the normal authorized project context. It must explain the problem, constraints, uncertainty, success conditions, and next permission. Judge against the original case, not merely the generated specification.

Reviewers should not know which variant produced an output when practical. Use deterministic checks where meaningful; use a human-reviewed semantic rubric for meanings. Inspect disagreement instead of letting a single model be the final judge. Keep at least some cases out of prompt/template tuning and disclose any later changes to the suite.

Record each output and tool trace, trial ID, relevant requirement IDs, violated constraints, unsupported assertions, authorization errors, avoidable questions, and reviewer rationale. Failure to produce an output is a failure/blocked trial, not an omitted result.

### D. Proposed acceptance decision

For the approved starter suite:

- All applicable package, integration, and structural checks pass with nonzero relevant coverage.
- Every required case and repetition has an outcome and retained evidence.
- Any fabricated approval/evidence, unauthorized action, or dropped critical exclusion prevents accepting that candidate until resolved or the requirement is explicitly reconsidered by its owner. An average score cannot hide these failures.
- Required semantic expectations pass across the approved repetitions. Any tradeoff or regression needs explicit owner disposition rather than silent acceptance.
- Claim behavioral improvement only when a reproduced baseline failure is corrected or an agreed burden measure improves without degrading safety or correctness. When both variants pass, report no demonstrated improvement instead of inventing one.

Passing this suite means passing these cases. It does not prove universal understanding or guarantee future behavior.

## 7. GitHub packaging

Use one tracking issue to point to this spec, existing issue #1, and only the new independent work. Existing issues can be added as sub-issues [G1]; a checklist with references is enough when a deeper hierarchy adds no value.

The spec owns requirements and acceptance criteria. Issues own scope, dependencies, assignment, and status. PRs own the proposed diff, requirement-to-test mapping, actual evidence, review, and merge. Link to a particular spec revision; update it through review when requirements change instead of copying competing versions into issue comments.

An issue being opened or assigned does not authorize an agent to execute it. Use actual scope and the existing approval process.

### Draft tracking issue

**Title:** Stage 01: evidence-grounded intent and verifiable handoffs

**Body:**

> Convert the reviewed findings into a small, evaluated improvement to Stage 01. Canonical spec: `<actual spec URL and approved revision, when available>`.
>
> Begin with finding validation and reconciliation; do not implement every recommendation as a presumed defect.
>
> Existing related work: #1 (template changes), #35 (seed terminology only). `docs/chain-contract.md` and `docs/seed-me-qa-plan.md` must be reconciled, not duplicated.
>
> Work: validate and approve the slice; implement the coordinated template change; publish independent handoff evaluation. Candidate upstream changes C1/C2 remain deferred until separately approved.
>
> Completion requires the approved requirements mapped to retained checks, reviewed semantic results, and explicit disposition of failures. This issue is not implementation approval.

### Draft work item A

**Title:** Validate Stage 01 findings and reconcile the existing contracts

**Scope:** Slice A only. **Requirements:** disposition of R1–R5 and C1/C2.

**Done when:** current revision and related PRs inspected; every finding classified with evidence; #1 overlap recorded; prior-policy conflicts resolved or deferred; baseline cases and grading rules reviewed; spec approval records the actual source and scope. No behavior change.

### Existing work item B: coordinate with #1

**Proposed supplement, not an unapproved rewrite:** reference the accepted spec revision and R1–R5; identify the specific template/contract changes and tests; preserve #1's unrelated remaining scope. Use a linked narrow child only when necessary for independent delivery.

**Done for this slice when:** canonical assets and necessary manifest/tests updated; fresh light/full outputs inspected; existing checks pass; requirement/test evidence is attached. Do not close all of #1 unless its full acceptance criteria are met.

### Draft work item C

**Title:** Evaluate whether a fresh agent preserves Stage 01 decisions

**Dependencies:** reviewed spec/baseline; run baseline before behavior edits, candidate after item B.

**Done when:** suite, settings, traces, results, and review are retained; R1–R5 results are reported separately from structural checks; critical failures are resolved; conclusion states improvement, no demonstrated improvement, regression, or insufficient evidence. No external transcript sharing without permission.

### PR evidence template

```markdown
## Scope
Spec revision:
Issue(s):
Requirements changed:
Files changed:

## Evidence
| Requirement | Case/test | Revision | Result | Log/artifact |
|---|---|---|---|---|

## Review
Baseline comparison:
Failures and limitations:
Human decision and actual reference:
Remaining work:
Rollback/revert approach:
```

Use a plain issue reference for partial work. Use closing keywords only when the whole issue is satisfied. GitHub can automatically close a linked issue when its PR merges into the default branch [G2]; that mechanism is not evidence that every acceptance criterion was met.

## 8. Source record and limits

Repository observations were read through the connected GitHub integration. S1, S2, and S9 were fetched at the pinned commit above; S3/S7 were inspected earlier in this same conversation. S5/S6 were fetched from main and have the observed blob SHAs below. Reconcile changing sources at dispatch.

- **S1:** `assets/stages/01-plan/CONTEXT.md`; blob `f0307cde906dbb326b21574af4acda044fd70dae`.
- **S2:** `assets/_shared/brief-template.md`; blob `975f793e87b9284298864a43cdc4f2921b45cc31`.
- **S3:** `assets/_shared/intent-template.md`; blob `598dd7edb26fc4d311d7db4ffcae15a783af28cd`.
- **S4:** `jon-devlapaz/ai-native-sdlc#1`, open when inspected; title: “Thicken templates: stop conditions, freeze fields, verify claim shape.”
- **S5:** `docs/chain-contract.md`; blob `bfc74ab7b5146254ccc076fb56b96a86a0f4287c`.
- **S6:** `docs/seed-me-qa-plan.md`; blob `b1d17dc91df89fed9b73ac946b6ba1f9ca7a2d28`.
- **S7:** `assets/_system/SDLC.md`; earlier inspected sections document seed copying, approval binding, and verification boundaries. Runtime implementation not independently exercised here.
- **S8:** `jon-devlapaz/ai-native-sdlc#35`, open when inspected; title: “Known limits and small follow-ups from the launcher hardening.”
- **S9:** `README.md`; blob `ae5e9861f4be505777574f36020d799b9132ed8c`.
- **G1:** GitHub Docs, “Adding sub-issues,” accessed 2026-09-30: `https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues`.
- **G2:** GitHub Docs, “Linking a pull request to an issue,” accessed 2026-09-30: `https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue`.

No implementation, evaluation execution, GitHub issue creation, PR creation, or repository modification was performed while preparing this document. Source-backed observations are separated from proposed requirements and pilot thresholds. The spec needs review, not a fictional approval stamp.
