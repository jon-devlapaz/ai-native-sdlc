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

### Saved-answer reassessment completed

The [researcher reassessment](saved-answer-reassessment.json) records all twelve
unchanged answers by their original result ID and content hash. It applies the
clarifications above: control 4/4, short 4/4, long 3/4. The remaining long/sort
failure is the unsupported requester name, not merely the inspected-fact label.
The build answers do not block the authorized next inspection, so their later
questions alone do not fail the clarified permission rule.

These criteria were clarified after seeing the outputs. The current researcher
has seen the candidates and answers; this is not independent evidence or a new
writer trial. Original scores and the frozen archive are unchanged. The result
still provides no reason to add either instruction.

### Owner review recorded

Jon replied, “Yes, use those four judgments,” to the explicit four-answer review.
The [owner labels](owner-labels.json) record the question, reply, source answer IDs,
and answer hashes. Long/sort fails for the unsupported requester name; all three
build answers pass because future questions do not block permitted inspection.
Only those four answers have owner labels; the remaining eight do not.

Check the revised model judge against these four saved answers without disclosing
the labels in its prompts. This is calibration on reviewed examples, not an unseen
test or evidence that the judge is reliable for every handoff.

### Judge check completed

The revised `gpt-6.1-sol` judge matched all four owner labels in four calls, including
the unsupported-name reason. It received the original requests and answers, not
the labels. No writer answers were generated. The [per-answer results](calibration-results.json)
and [separate calibration archive](calibration-evidence.tar.gz) retain the complete
prompts, model replies, owner labels, usage, and error records.

The live run's local comparison assertion had a syntax error. The four model replies
were valid; the assertion was corrected and those same replies replayed offline.
The original failed comparison remains saved. The repaired comparison matched 4/4
with zero additional model calls. This validates these reviewed examples only;
the full handoff evaluation below remains pending.

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
