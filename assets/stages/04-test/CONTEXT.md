# Stage 04: Verify

Inputs: approved run artifacts, candidate checkout, `_system/verification.json`,
and the accepted `test-lock.json` for bug runs.
Run `_system/scripts/verify.sh <slug>`; no alternate runner bypasses the gate.

Outputs: generated `runs/<slug>/04-test/output/test-log.md` and `verification.json`.
The gate requires successful configured checks bound to current candidate and
input digests. Missing configuration, execution errors, stale inputs, changed test
baselines, and timeouts fail. A file's existence never proves success.

Gate: verification passes on current evidence and a human reviewer accepts the
result; a green local run alone is not release approval.

Failures return to stage 03. Incorrect reproduction tests require independent
review and a replacement run; do not weaken assertions to obtain green output.
Local locking detects changes. Strict enforcement requires trusted CI with an
independently retrieved baseline and protected runner/policy, as in `_system/SDLC.md`.

## Skills

Skillset: `testing-skillset` (pin: `.tink/skillsets/testing-skillset.json`).
- Once per machine/library, after reviewing the pin (it selects exact upstream code):
  `tink library fetch .tink/skillsets/testing-skillset.json`
- At stage open, compile the required disciplines, then start a NEW session so
  `AGENTS.md` is re-read: `tink use testing-skillset --snapshot runs/<slug>/04-test`
  The launcher does this for you: `python3 _system/scripts/sdlc.py stage <slug> 4`.
- For a capability gap: `tink-route --receipt runs/<slug>/skills.jsonl "<what you need>"`
  (asks this stage's shelf, the skillset named in the rules block above; prints the skill on stdout.
  Exit 1 means nothing on the shelf fits, and a `Hint:` line may name a skill on another stage's shelf that
  was not delivered; exit 1 or 2 means continue without a skill).
