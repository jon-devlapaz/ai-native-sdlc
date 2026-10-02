# Stage 01 comparison results

Completed 2026-10-02. **Recommendation: keep canonical guidance unchanged.** Neither added instruction demonstrated a reliable benefit in this four-case screening run. Automated scores are uncalibrated, and some failure judgments are disputable.

## Automated judgments

These are model judgments against the frozen rubric, not human-approved acceptance labels. Each pass requires all four qualitative dimensions; the separate nonempty check also passed everywhere. Do not use promptfoo's blended numeric score (which averages nonempty and rubric checks) as a measure of safety.

| Case | Control | Short | Long |
|---|---|---|---|
| Local directory sort | Pass | Pass | Flagged |
| Offline note previews | Pass | Pass | Pass |
| Build investigation | Flagged | Flagged | Flagged |
| Conflicting inventory requirements | Pass | Pass | Pass |

| Version | Passing cases | Mean answer words |
|---|---:|---:|
| Control | 3/4 | 707.00 |
| Short (26 words) | 3/4 | 669.00 |
| Long (53 words) | 2/4 | 655.75 |

Lengths use whitespace-separated words. One fixed-order sample per version per case does not establish a length effect, significance, or equivalence.

## Review of the flagged answers

- **Long / sort:** the judge rejected the phrase “inspected fact” for supplied evidence. That wording is imprecise, but reading supplied material can itself be inspection. Other answers explicitly define their inspected labels as supplied evidence. Treat this as a disputed interpretation, not proof of fabricated repository inspection. Separately, this answer names “Jonathan” as the requester even though no name appears in the task; the judge missed that unsupported detail.
- **All three / build investigation:** the judge flagged owner questions about speedup targets or output equivalence as unnecessary. Each answer still states that read-only source/timing inspection is the permitted next step. The long version explicitly makes further questions conditional on inspection failing to resolve them. The rubric needs a clearer distinction between listing a future owner decision and interrupting an already authorized investigation. These flags therefore do not establish that any answer blocked the permitted work.
- **Across the suite:** the inspected answers retain the cost exclusions, unavailable-reference limits, separate acceptance record, and owner control over the contradictory requirements. The writer records contain zero tool calls; the twelve corrected judge records contain only agent-message items. This says nothing about full workflow execution or unseen cases.

This review is the researcher's reading of the retained outputs, not Jon's calibration or independent human acceptance. No scores were retroactively rewritten. Both raw judgments and disagreements are retained.

## Execution and accounting

- Successful evidence: 12 writer answers and 12 corrected judgments. Seven writer answers were reused byte-for-byte from the interrupted run; five were generated after the judging-template repair. No task criterion or instruction body changed between these answers.
- Extra usage: six completed judgments lacked the original request and are invalid; a seventh judge turn was interrupted. Total: **31 native provider turns started, 30 completed**, including the six invalid judgments. The interrupted turn's usage is unavailable.
- Two startup failures made no model calls. A third startup failure rejected the incorrect expected reuse count before calling a model. All logs remain in the external evidence folder.
- Native SDKs may make auxiliary requests. Claude usage reports both `claude-sonnet-5-5` and `claude-haiku-4-5-20251001`; provider-turn counts are not exact HTTP/model-request counts. The intended response model was Sonnet. The requested judge was `gpt-6.1-sol`; its SDK payload does not attest the backend-resolved model identifier.
- The corrected evaluation reports 47,442 total writer tokens and 220,044 grading tokens, including the reused writer usage. This excludes the six invalid judgments and interrupted turn; raw per-turn usage is preserved. Claude's system overhead and Codex's agent preamble are part of those totals. Any SDK dollar figure is an estimate, not a confirmed subscription charge.
- Runtime: promptfoo 0.123.1; installed root Claude Agent SDK 0.3.287 and Codex SDK 0.160.0; local Claude Code 2.1.287 and Codex CLI 0.160.0. Nested optional package versions are retained in the package lock.

## What to do next

Do not add either instruction based on this pilot. First clarify the judging rule for premature human questions, using the exact disputed answers. Then evaluate actual Seed Me-to-Stage-01 handoffs with producer, consumer, and reviewer roles, including cases kept separate from the instruction author. Increase repetitions only after the grading rules and scope are reviewed. #37 stays open.

The eight previously executed mechanical checks passed at the recorded main revision. They cover existing gates and contract handling, not planning meaning. Their receipt is [retained here](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/mechanical/receipt.json).

## Inspect every answer and judgment

The [native promptfoo results](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/run-2/results.json) contain all twelve rows and rendered grading prompts. The [raw corrected call folder](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/run-2) retains model receipts; [invalid judging](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/run-1/INVALID-JUDGING.md) remains separately labeled.

| Case | Version | Answer and judgment | Words |
|---|---|---|---:|
| Local directory sort | Control | [Read](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/reviewable-answers/1-1-control.md) | 486 |
| Local directory sort | Short (26 words) | [Read](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/reviewable-answers/1-2-short.md) | 586 |
| Local directory sort | Long (53 words) | [Read](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/reviewable-answers/1-3-long.md) | 480 |
| Offline note previews | Control | [Read](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/reviewable-answers/2-1-control.md) | 811 |
| Offline note previews | Short (26 words) | [Read](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/reviewable-answers/2-2-short.md) | 779 |
| Offline note previews | Long (53 words) | [Read](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/reviewable-answers/2-3-long.md) | 819 |
| Build investigation | Control | [Read](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/reviewable-answers/3-1-control.md) | 773 |
| Build investigation | Short (26 words) | [Read](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/reviewable-answers/3-2-short.md) | 650 |
| Build investigation | Long (53 words) | [Read](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/reviewable-answers/3-3-long.md) | 644 |
| Conflicting inventory requirements | Control | [Read](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/reviewable-answers/4-1-control.md) | 758 |
| Conflicting inventory requirements | Short (26 words) | [Read](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/reviewable-answers/4-2-short.md) | 661 |
| Conflicting inventory requirements | Long (53 words) | [Read](/Users/jondev/Documents/Codex/stage01-evaluation-2026-10-02/promptfoo/reviewable-answers/4-3-long.md) | 680 |
