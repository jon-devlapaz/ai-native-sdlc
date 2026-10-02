# Tight handoff evaluation — result

**Decision:** no demonstrated overall improvement. The proposed template candidate
is not accepted as a reliability improvement. Main assets remain unchanged while
issue 1 awaits the owner's disposition. No more model calls are planned.

## What ran

Nine approved provider turns: two fresh Claude writers, five fresh Codex consumers,
and two fresh Codex reviews. Three unchanged control writer answers were reused.
The final review included all original requests, normal project context, and the
workflow references actually given to the consumers. Original pilot scores and
owner labels were not overwritten. [Actual use and source revisions](run-summary.json).

| Sample | Producer | Consumer | Injected defect detected |
|---|---|---|---|
| Saved offline notes | Pass | Fail: turns unavailable design details into a prerequisite | Yes |
| Saved navigation | Pass | Fail: drops card-backed-trial exclusion | Yes |
| Saved trivial sorting | Fail: offers an accent-insensitive comparator | Pass | Yes |
| New uploader, candidate | Fail: unsupported originator identifier | Pass | Yes |
| New uploader, baseline | Fail: unsupported originator identifier | Fail: asserts an unsupported existing no-network guarantee | Yes |

These are model judgments, with reasoning retained in [the final assessment](final-assessment.json).
They are not five new owner labels. The separate researcher review agrees that
unsupported originator identifiers invalidate both new writer outputs and that
neither version earns an overall improvement claim. It also flags the lost trial
exclusion and the unnecessary design prerequisite. No actual trial, installation,
production write, or release occurred.

## Disagreements and limits

The reviewer additionally rejects both writers' statement that the client does not
use keys *for retry*. Since the supplied code has no retry, that wording does not
necessarily establish an unsupported claim about all client key handling. The
researcher does not treat it as a separate decisive failure. The candidate's claim
that batch lookup is simpler is unsupported and should remain a hypothesis.

The sort writer warned that its optional accent-insensitive comparator exceeded
case-only comparison. Offering it as an option still risks changing settled behavior,
although the consumer chose the valid lowercase comparator. This finding differs
from the earlier response-only score; retain both assessments rather than silently
replace the old score. None of the four actual owner labels changed.

One candidate consumer passes where its matched baseline fails, but both new writers
fabricate an originator identifier. One sample cannot establish a reliable effect
or attribute it to the template. The hard failure prevents accepting this candidate
as fixing the required behavior. The cause of the unsupported identifier is unknown;
no claim is made about where the model obtained it. The report omits its literal value.

The combined case covers T2/T5/T6-permission efficiently but cannot isolate each
factor. Earlier cases cover T1/T3/T4/T6-inspection and a trivial task. Contradictory
requirements and misleading-name variations were not newly exercised under this
reduced budget; this is narrower evidence than the original broad issue outline.
Consumers derive plans, not execute them. The holdout was authored by this researcher;
only its outputs were held out. Template differences can reveal variants despite
concealed labels. Requested Codex models are not independently backend-attested.

## Errors retained

The fourth call's review packet omitted the workflow references actually supplied
to consumers. Its two unsupported-workflow findings are invalid. The final ninth
call reviews all five handoffs with those references. No extra repair calls were made.

Local setup errors: an attempted runner edit used the wrong worktree path, then was
corrected in the main checkout; the first fresh-scaffold command refused a nonexistent
target directory, then succeeded after creation of the empty synthetic fixture.
Neither error consumed model turns or changed production projects.

## Mechanical results and issue 1

Baseline and candidate each passed all **277 existing tests**; package manifests
match. Fresh light/full scaffolds generate the intended templates, with nonempty
completion, scope, and frozen-contract prompts. The light definition gate remains
stage 3 and the full gates remain 1/2/3. No synthetic human approval was recorded.
[Candidate checks](candidate-checks.json), [fresh artifacts and statuses](fresh-scaffold.json).

The candidate changes six requested documentation assets plus manifest/version;
two existing test version expectations move to 1.18.3, with no assertions removed
or tests added. Runtime scripts and schemas are byte-unchanged. The initial draft
adds 498 whitespace-separated words; the targeted exclusion reminder adds 9 more.
Some generic numbered step placeholders were removed. The new wording remains a
reviewable [candidate patch](candidate.patch), not a proven operational improvement.

Recommended disposition: keep main unchanged and close issue 1 as not planned,
rather than ship the extra wording on this evidence. The owner may instead accept
it expressly as documentation clarification with unproven behavioral benefit.
The paused issue 34 likewise needs the owner's stop/resume disposition.

## Reuse

Read this report, `run-summary.json`, the cases and final assessment first. The
portable archive includes redacted prompts/replies, settings, runner versions,
source template snapshots, trial mappings, usage, context-error record, checks and
file hashes. Raw unredacted provider replies remain unchanged at the local runtime
path in the summary. No dependencies or authentication state are archived.
