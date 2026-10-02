# Stage 01 evaluation handoff

**Status:** completed exploratory pilot; no reliable improvement demonstrated. Keep current workflow guidance. [Results and disagreements](results.md). This does not complete issue #37.

## Next steps

1. Completed: the owner reviewed the four disputed judgments; [labels are recorded](owner-labels.json).
2. Completed: clarified the rubric and checked the model judge against those four labels; [agreement is 4/4](calibration-results.json). Original scores are preserved, and the eight other answers remain researcher assessments without owner labels.
3. Evaluate actual Seed Me-to-Stage-01 handoffs: does the writer preserve the request, does the next agent follow it, and does a reviewer catch an intentionally flawed plan? Start with existing guidance. Keep some cases unseen while developing changes.
4. Add wording only for a reproduced failure that it fixes without new problems. Keep issue #34 paused. The owner accepted the no-change scope decision and requested closure of #36; continue through the [#37 plan](next-steps.md).

## Save and reuse this run

The [portable evidence archive](evidence.tar.gz) contains requests, instruction versions, runner, configuration, dependency lock, all answers and judgments, invalid-run records, error logs, research notes, and mechanical-check receipts. It excludes installed dependencies and authentication state. [File manifest](evidence-manifest.json); [archive checksum](evidence.tar.gz.sha256).

The [separate calibration archive](calibration-evidence.tar.gz) adds the owner labels,
four judge replies, and the local comparison repair. The original archive is unchanged.

This directory is the Git record. The archive is the unchanged snapshot captured before publication; subsequent closure and next-step decisions live in the surrounding documents.

After extraction, start with the archive's `README.md` and portable `reports/results.md`. The raw records remain unchanged. File hashes detect byte changes; they do not validate the judgments.

## Prompt for the next session

> Continue issue #37 from docs/evaluations/stage01-2026-10-02/next-steps.md. Read the results and disputed answers first. Keep operational guidance unchanged. Clarify the grading rules and use saved answers before generating more. Preserve original results and distinguish owner judgments from model scores. The next experiment should evaluate actual handoffs, with cases kept separate from instruction development. Keep #34 paused; document any new execution scope and account-usage limit before running it.
