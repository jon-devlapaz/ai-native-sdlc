# Resolve issues 1 and 37

## Intent and scope

Finish the requested template work and evaluate the producer-to-consumer handoff.
Keep existing approval, isolation, verification, and release rules. Issue 34 needs
its own owner disposition because the owner explicitly paused that pilot.

## Proposed execution

- Eight synthetic cases, one sample per version. Seven development cases cover
  T1–T6 and the trivial no-question case. One additional compression case is held
  out of output inspection and candidate tuning until the candidate is frozen.
- Three separate sessions per case/version: Claude Sonnet producer; Codex
  gpt-6-luna consumer; Codex gpt-6.1-sol reviewer. Medium reasoning/effort.
- Producer reads the original request, project context, Stage 01 contract and
  selected template. Consumer gets only the resulting artifact and authorized
  project context. It describes and derives the next plan, not actual execution.
- Reviewer sees original request and context, both real outputs, and a deliberately
  defective downstream plan. It reports producer preservation, consumer compliance,
  and defect detection separately. It does not receive the variant label.
- Existing promptfoo native SDK setup and ChatGPT/Claude subscription logins only.
  No API billing fallback, private source conversations, actual production access,
  retries, or permission/approval fabrication.
- At most 48 provider turns across baseline and one candidate, serial execution,
  120-second limit per turn. Stop on missing output, invalid reviewer JSON, timeout,
  provider error, or limit reached; retain blocked trials. No automatic repeats.
- Codex account starts with 44% weekly capacity remaining. Before each three-call case, check account capacity; stop if it shows 20%
  or less remaining. Claude limit/error also
  stops the run; its remaining capacity is not known in advance.
- Baseline development results precede asset changes. Freeze the one candidate
  before either held-out run. Counterbalance baseline/candidate order for the
  held-out case. Disclose that the same researcher authored the case definitions:
  this is output holdout, not an independently authored or secret benchmark.

## Template candidate (#1)

Only the six requested templates/contracts plus the package manifest/version.
Use small prompts for missing scope, completion, frozen interfaces, real proof,
isolation, skill status, and review disposition. Reuse existing gates and avoid
adding the unevidenced 26/53-word guidance. Do not change scripts or runtime schemas.
Treat missing guidance as a documentation clarification until behavioral results
show a benefit. Record file/word changes and every retained/removed instruction.

## Checks and conclusion

Run the package manifest check and existing SDLC tests requested by issue 37’s
verification plan. Inspect fresh light/full scaffold outputs. Mechanical checks
and semantic results are separate; synthetic approvals are confined to fixtures.
Record observed failures, reviewer disagreements, account use, complete replies,
source digests and stop/error records. Review critical findings directly.

A passing pair is no demonstrated improvement. Report insufficient evidence if
access limits or missing trials prevent comparison. Passing this small suite does
not establish universal reliability. Close issues only after the requested work
and disposition of findings are recorded; do not claim the paused pilot ran.

## Authorization

Owner instruction: “Proceed goal is 0 issues.” This authorizes resolving the
backlog. The exact larger evaluation scope above is ready for owner review under
the previously agreed issue 37 execution gate; it has not been run yet.
