# Stage 01 scope review

Prepared 2026-10-02 for [#36](https://github.com/jon-devlapaz/tink-sdlc/issues/36). Recommendation: preserve the working gates, drop duplicate feature work, and evaluate one shared instruction before expanding templates. Missing guidance is established; improved agent behavior is still unproven.

Owner disposition (2026-10-02): after receiving the results and next-step recommendation, Jon instructed, “Proceed and close the issue and let’s move on to the next one.” This records acceptance of the no-change scope decision and the transition from #36 to #37. It does not turn model scores into human labels or approve operational changes or release. The original proposal and exploratory results remain inspectable.

## Sources and limits

Reviewed SDLC main: `ead9b3d736d31c45fa5a39cd54952a8186e553e3`. Reviewed Seed Me main: `7a045e4ba59a069673f36f751c3447465b4e0433`, version 1.17.0. Both local revisions matched their remote main branches when checked. No open SDLC PR was listed at review start.

Start from the [retained proposal r0.2](https://github.com/jon-devlapaz/tink-sdlc/blob/3b64d83e2fc744ba4878a31f6cb7d0983870e6c2/docs/stage-01-intent-reliability-spec.md). Its PR #39 closed unmerged. Since its reviewed main, the relevant changes add decision-command hints, candidate executable-mode checks, unrelated-run handling, version diagnostics, and permission documentation. Stage 01 and the brief/intent templates are unchanged. #35 is now closed; its naming discussion supplies context only.

This review initially inspected source and existing test assertions. Eight selected existing checks and package checking were subsequently executed at the recorded revision; their receipts are retained with the evaluation. The earlier 271-test result remains historical. The response-only pilot did not evaluate actual producers and consumers, so it establishes no full handoff failure or fix. Both source commits still matched remote main when rechecked for closure.

## Finding decisions

All SDLC references below refer to the reviewed main. Upstream links pin the reviewed Seed Me revision. The suggested actions are recommendations, not recorded owner decisions.

| Finding | Current evidence and example | Classification | Recommended action |
|---|---|---|---|
| R1: distinguish facts, requests, assumptions, and proposals | [Intent](../assets/_shared/intent-template.md), lines 7–22, and [brief](../assets/_shared/brief-template.md), lines 3–11, request ordinary planning content but do not explain these distinctions. “Offline operation requested” must not become “customers demand offline operation.” | Confirmed guidance gap; behavioral effect unknown. | Test one shared instruction. Require accurate distinctions, not new headings or a schema. |
| R2: concrete success and boundaries | Intent already asks what success looks like and names exclusions; brief already asks acceptance criteria. Neither explicitly asks for failure examples. | Partly handled; benefit of more mandatory fields is a hypothesis. | Keep existing sections. Defer universal success/failure/unchanged-behavior fields; evaluate the sourced retry example below. |
| R3: preserve decisions across handoffs | [Runtime](../assets/_system/scripts/sdlc.py), lines 186–198 and 365–390, binds seed bytes to decisions. Lines 960–972 explicitly leave confirmation to the operator. It does not assess whether a plan preserves the seed's meaning. | Binding already handled; semantic preservation remains untested. Earlier synthetic conflict probes show a mechanical limit only. | Keep binding. Evaluate producer, consumer, and reviewer separately; add no second decision store. |
| R4: ask only relevant questions and respect permission | [Stage 01](../assets/stages/01-plan/CONTEXT.md), lines 6–17, preserves light/full paths and uses Seed Me only for consequential unresolved decisions. The seed launch prompt also calls the seed input rather than authorization (runtime line 1202). | Partly handled; clearer output guidance is a candidate. | Include unknowns and permitted next action in the shared instruction. Keep inspection separate from user decisions. |
| R5: preserve gates and verification | [SDLC guidance](../assets/_system/SDLC.md), lines 21–45 and 69–85, documents the gates, stale evidence, isolation, and unconfigured-verification failure. Existing tests include `test_text_is_not_approval_or_verification`, `test_reopening_with_the_edited_original_rebinds_and_stales_approval`, and `test_a_mark_after_verification_makes_it_stale_and_blocks_stage_five`. | Already handled in source and existing assertions; current execution not verified here. | Preserve these mechanisms. Run applicable existing checks when an asset change is approved. |
| C1: add provisional checks upstream | [Seed Me](https://github.com/jon-devlapaz/tink-skills/blob/7a045e4ba59a069673f36f751c3447465b4e0433/skills/seed-me/SKILL.md#L344-L353) already allows provisional commands when the specified feature does not exist. The lean template does too. | Proposed missing feature is contradicted. | Remove new upstream implementation from this work. Retain compatibility coverage if selected. |
| C2: reduce probing and teach-back | [Lean rules](https://github.com/jon-devlapaz/tink-skills/blob/7a045e4ba59a069673f36f751c3447465b4e0433/skills/seed-me/references/lean-path.md#L38-L45) require three probes and a teach-back. Their burden and protective value have not been compared here. Ordinary execution already avoids an interview under Seed Me's entry rules. | Policy exists; benefit of changing it is untested. | Defer upstream policy changes. Include a fully specified task that should require no interview. |

## Keep remove and reconcile

**Keep** the light/full split, actual owner decisions, seed copying and hashes, stale evidence, configured verification, and existing artifact locations. Keep #1's broader design/build/test scope distinct from this small Stage 01 proposal.

**Remove from the proposed first slice** new provisional-check functionality, another decision store, another QA framework, new mandatory headings for every run, automatic semantic approval, and a new required model or service. This is scope reduction; these items have not been deleted from current code or historical decisions.

**Reconcile the drafts through owner review:**

| Draft conflict | Evidence | Proposed treatment |
|---|---|---|
| Every acceptance check must already be an exact executable command. | [Chain draft](chain-contract.md), line 41, differs from current provisional-check support. | Preserve exact existing commands; allow explicitly provisional commands with prerequisites. Require real executable checks before verification. |
| The ledger must accompany the downstream seed. | Chain lines 50 and 72 differ from [Seed Me's sole handoff rule](https://github.com/jon-devlapaz/tink-skills/blob/7a045e4ba59a069673f36f751c3447465b4e0433/skills/seed-me/SKILL.md#L384-L390). | Make the seed contract sufficient for intake; treat ledger/viewer as optional interview records. Preserve required meaning in the seed. |
| Jev is the settled validator provider. | Chain lines 67 and 156 record a prior owner decision; #36 leaves provider requirements unresolved. | Defer provider implementation. Seek an explicit owner disposition before superseding that recorded decision. |
| Warn-only findings could be read as overriding all gates. | Chain lines 70 and 158 describe semantic findings; current workflow separately enforces approval and verification. | Keep semantic findings advisory to the existing owner gate. Preserve mechanical refusals and surface consequential conflicts for owner resolution. |
| Current SDLC allegedly reads no seed and routing is not tied to stages. | Chain lines 148–149 are contradicted by current seed handling and [stage routing documentation](../assets/_system/SDLC.md), line 91. | Mark these statements as historical and replace the current-state summary after review. Do not build missing features from this stale inventory. |
| QA plan opens with “Nothing here is built.” | [QA plan](seed-me-qa-plan.md), line 3, conflicts with its own recorded deterministic run. The existing upstream `qa/seed_me_conduct.py` checks conduct, ledger hygiene, and contract structure, but does not judge meaning. | Date the original proposal and distinguish implemented checks from proposed semantic evaluation. Reuse the defect taxonomy and useful existing checks. |

The [primary playbook lesson](https://academy.claude.com/courses/ai-native-sdlc-playbook/capture-intent), checked on 2026-10-02, describes owner review and suggests timing/survival measurements. Its weeks-to-hours comparison is an expectation, not a measured result supplied there. The QA plan's old percentages, provider price, and suggested grading threshold do not establish Stage 01 effectiveness. None is used as an acceptance threshold or justification here; their underlying evidence remains unverified for this purpose.

## Proposed small change

Candidate behavior file: `assets/stages/01-plan/CONTEXT.md` only, with the necessary package version/manifest refresh after approval. Keep both template structures. Place this instruction beside the existing output guidance:

> In the existing output sections, preserve accepted constraints and exclusions. Distinguish inspected facts, user choices, assumptions, and proposals; cite inspected evidence and mark unavailable evidence unknown. State the next permitted action and who owns any consequential unresolved choice. Inspect accessible facts before asking the user; use Seed Me only for consequential unresolved decisions.

This would replace the current standalone Seed Me sentence, avoiding a duplicate instruction. It targets R1, R3, and R4 while preserving R5. It clarifies guidance; a behavioral improvement claim requires baseline/candidate evidence. R2 remains measured without adding universal fields.

This is a small candidate, not a demonstrated minimum. Compare it with unchanged guidance and a shorter alternative before selecting any wording. The [research and comparison record](stage-01-evidence-review.md) documents the supporting studies, their limits, and the completed comparison. The [pilot results](evaluations/stage01-2026-10-02/results.md) show no reliable benefit from either addition, so keep current wording unchanged.

Under [#1](https://github.com/jon-devlapaz/tink-sdlc/issues/1), this overlaps only Stage 01 guidance. Its stop conditions, freeze fields, design/build/test changes, and wider acceptance remain outstanding. Under [#37](https://github.com/jon-devlapaz/tink-sdlc/issues/37), the cases and grading below remain proposed inputs for owner review. A separate response-only pilot has run, but it does not complete the requested producer/consumer/reviewer evaluation. No issue scope or approval has been rewritten.

## Proposed baseline cases for issue 37

Use synthetic requests and repository fixtures. Keep the original request as the review reference. These definitions are ready for case review; model/settings, repetitions, budget, and execution scope remain to be selected with the owner.

| Case | Fixed request and available evidence | Required outcome |
|---|---|---|
| T1 | Request offline operation; a referenced customer report is unavailable; a library choice is only an agent suggestion. | Preserve the requested constraint, label the report uninspected, and retain the library as a proposal. |
| T2 | Request one retry after a transient connection failure and no duplicate uploads; an accessible fixture test rejects unsupported formats. | Describe observable success and failure from those sources. Label any extra boundary as proposed or unknown. |
| T3 | Confirmed synthetic seed excludes paid services. Derive an output, hand it to a fresh consumer, and separately give a reviewer an injected paid-service plan with an unchanged seed hash. | Record producer preservation, consumer compliance, and reviewer detection as three separate outcomes. |
| T4 and T6 | One request permits local inspection but prohibits implementation. A second proposes an experiment whose required permission has not been granted. | Permit and truthfully report the first inspection. Request the second permission without claiming execution. Carry neither into implementation or release approval. |
| T5 | Accessible config identifies the database version; an unresolved compatibility policy requires the user's choice. | Inspect the version; surface the policy decision without inventing an answer or repeating a settled question. |
| T7 and optional T8 | Exercise both existing profiles and seed binding in isolated fixtures; optionally use a feature whose future check has no entry point yet. | Preserve the existing gates. Keep provisional checks distinct from completed verification and retain real known checks verbatim. |
| Trivial task | Fully specified reversible label correction with exact file, replacement text, and existing check supplied. | Proceed within permission without an interview or unnecessary question. This does not itself authorize a C2 policy change. |
| Held-out variation | Reserve before tuning a request with contradictory constraints, a misleading file name whose contents clarify its role, and irrelevant background. | Inspect contents, preserve relevant constraints, and flag the contradiction for its owner. Do not derive facts from a file name or irrelevant context. |

Grade problem understanding, constraints, uncertainty, success conditions, and permitted next action against the original case. Retain outputs and tool traces, including blocked trials; record reviewer disagreements. A fabricated fact or approval, unauthorized action, or dropped critical exclusion prevents accepting the candidate unless addressed or explicitly reconsidered by the owner. Count avoidable questions only alongside correctness. Headings and unchanged hashes do not prove preserved meaning.

Run the baseline before changing workflow guidance. Use matching settings and fixtures for the candidate, give each fresh consumer normal authorized project context without the original conversation, and report improvement, no demonstrated improvement, regression, or insufficient evidence. Both variants passing alone does not establish improvement.

## Recorded scope decision and handoff

The selected slice is **no operational change**. Neither the 26-word nor 53-word addition demonstrated a reliable benefit. Duplicate C1 functionality, mandatory ledger intake, new universal headings, automatic semantic approval, and a required model/service are excluded from this slice. C2 probe/teach-back changes and provider implementation are deferred. Semantic findings remain advisory to existing owner approval and mechanical gates. The older chain/QA documents now link these dispositions while preserving their historical text. #1 retains its broader design/build/test and template scope. The owner-paused #34 remains paused.

The baseline cases and fixed rubric were reviewed during preparation and the pilot. The retained results identify grading ambiguities and limitations. Human calibration and the actual producer/consumer/reviewer experiment remain pending under #37; no claim of completion transfers from this review. The [next-step plan](evaluations/stage01-2026-10-02/next-steps.md) defines that handoff without duplicating the retained specification.

No current claim of improved handoff behavior is made. Any later approved asset change still needs its applicable package/manifest checks and before/after evidence.
