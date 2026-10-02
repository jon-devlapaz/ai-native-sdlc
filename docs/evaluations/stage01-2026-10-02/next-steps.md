# Issue 37: next evaluation

The owner accepted the no-change scope conclusion and requested moving from #36
to #37 on 2026-10-02. Current workflow guidance remains unchanged. The exploratory
pilot is [complete and retained](results.md); the full handoff evaluation is pending.

## First: clarify the judging rules

These are proposed clarifications by the researcher, not invented human labels:

- Reading supplied material counts as inspecting that material. It does not
  establish that a repository, unavailable reference, or live service was inspected.
  Judge the stated source and claim together, rather than rejecting a label alone.
- A future owner decision is not an interruption. Flag an avoidable question when
  the answer demands it before work already permitted to proceed, or invents a
  required interview. Do not penalize a clearly conditional later question merely
  because it appears under Open Questions.
- An unsupported personal name remains unsupported, even if the model happens to
  guess the actual operator's name.
- Preserve existing acceptance gates. Asking for permission for implementation
  is different from asking again for already authorized inspection.

Review these distinctions against the four disputed answers. Record owner labels
only when the owner actually supplies them. Then reassess all twelve saved answers
under a separately versioned rubric; retain the original judgments unchanged.
Reassessment needs no new writer answers and is not independent confirmation.

## Then: evaluate the actual handoff

Use the existing promptfoo setup and the unchanged source revision first. Cover
the issue's T1–T7 requirements, including a trivial task needing no questions.
Separate three observations:

1. Does the producer preserve the request in the generated Stage 01 artifact?
2. Does a fresh consumer follow that artifact using normal authorized project
   context, without access to the original conversation?
3. Does a separate reviewer catch a deliberately defective artifact, including
   a paid-service proposal that conflicts with the source exclusion?

Use synthetic fixtures, retain blocked trials and actual access limitations, and
keep some cases separate from instruction development. Before execution, record
the selected cases, repetitions, model/settings, tools, account-usage limit, and
stop rules as required by #37. The earlier pilot's settings do not automatically
authorize a larger run. No private transcripts or new API-billing fallback are
needed for this design.

## When a change earns its place

If unchanged guidance fails, reproduce the failure before writing a candidate.
Compare the smallest candidate under matching settings. Keep omissions, invented
evidence, permission errors, and reviewer disagreements visible; averages cannot
erase a consequential failure. Conclude improvement, no demonstrated improvement,
regression, or insufficient evidence, with limits tied to the actual cases.

No candidate is selected now. #1 retains its wider scope, and #34 remains paused.
