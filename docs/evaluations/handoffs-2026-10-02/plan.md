# Tight plan for issues 1 and 37

This replaces the unexecuted 48-call proposal. No model calls have run under it.
Owner direction: “Proceed goal is 0 issues,” then “I don’t want to spend a lot of
usage on this keep it tight and high signal.”

## Scope and call cap

At most **nine provider turns**, no repetitions or automatic retries:

1. Reuse three unchanged control answers from the saved pilot: offline notes,
   no-paid-services navigation, and the trivial sorting task. The source assets
   are byte-identical to the current baseline. Three fresh gpt-6-luna consumers
   derive next plans from the saved artifacts and normal authorized project context.
2. One gpt-6.1-sol reviewer checks those three handoffs and three deliberately bad
   downstream plans. Producer preservation, consumer compliance, and detection are
   reported separately. This baseline development review precedes any asset edit.
3. Apply and freeze the six-file template proposal and manifest/version. Do not
   tune it on the new case's output.
4. A new combined uploader case covers retry/boundary behavior, inspectable database
   version versus owner compatibility policy, and a proposed production experiment
   lacking permission. Run candidate first, then unchanged baseline from its pinned
   snapshot: one Claude Sonnet writer and one gpt-6-luna consumer each (four calls).
5. One fresh gpt-6.1-sol reviewer checks all five handoffs, compares the two new
   handoffs with variant labels concealed, and checks injected defective plans. The current researcher also
   reads all outputs and records any disagreement; this is not an owner label.

The new case's outputs are held out until the candidate is frozen. Its definition
was authored by this researcher, so this is output holdout, not an independently
created benchmark. Combining risks is efficient but does not isolate each causal
factor. One sample per case is not a reliability estimate. Saved writers are
historical reuse, not fresh producer trials. Consumers derive plans, not execute.

## Exact inputs and controls

Requests, authorized context, expectations, and injected defects are in `cases.json`.
Saved answers retain result IDs and hashes. `settings.json` pins requested models
and medium effort. `run.mjs` retains prompts, replies, tool metadata, usage, errors,
and input hashes. Original pilot and calibration archives remain unchanged.

Use existing promptfoo native SDK setup and subscription logins only, with no API
billing fallback or private conversations. Tools/network are prohibited for these
response-only calls. Separate fresh sessions; consumer never gets original request.
Reviewer uses source request plus actual outputs; later owner questions do not fail
unless they block already permitted work. Supplied-file reading is not live access.

120 seconds per turn. Stop the whole run on timeout, provider error, missing output,
invalid review JSON, or the nine-call cap. Before each batch (up to three turns),
check remaining Codex capacity; stop at 20% or less. Start snapshot was 44% remaining.
Claude limit/error also stops execution; its remaining capacity is unavailable.
No resets, extra credits, or automatic repeated calls.

## Issue 1 and mechanical evidence

Only the six requested templates/contracts and package manifest/version. Add small
prompts for scope/stopping, frozen interfaces, proof, isolation, skill status, and
review disposition. Keep runtime scripts, schemas and actual human gates unchanged.
The earlier 26/53-word addition remains unselected. Missing guidance justifies a
clarification; claim behavioral benefit only where matched evidence supports it.

Baseline package check passes and all 277 existing SDLC tests pass. Repeat relevant
package checks on the candidate and inspect fresh light/full artifacts. Mechanical
results do not prove preserved meaning or authenticate approval. Synthetic decisions
stay in labeled fixtures. No actual pilot stage is advanced by this experiment.

## Completion and limits

Report each dimension, critical failure and reviewer disagreement. A passing pair
means no demonstrated improvement; incomplete comparisons mean insufficient evidence.
T1/T3/T4/T6-inspection/trivial use retained cases; T2/T5/T6-permission use the new
combined case. T7 remains mechanical compatibility coverage. The retained specification
is [revision 0.2](https://github.com/jon-devlapaz/ai-native-sdlc/blob/3b64d83e2fc744ba4878a31f6cb7d0983870e6c2/docs/stage-01-intent-reliability-spec.md).

The nine-call scope awaits the earlier agreed issue 37 review. The 48-call request
is withdrawn. Issue 34 still requires the owner's choice: stop it or review its plan.
Do not close incomplete work as successfully implemented.
