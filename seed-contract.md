# Intake confirmation receipt

**Seed contract — confirmed for intake; not approved for implementation**

Renamed from `pre-intent.md`. The original receipt and reviewed r2 draft below retain their historical wording and paths; the rename does not change their approval scope.

This receipt supersedes only the save-pending statements in the preserved r2 draft below. It does not approve execution or change the requirements or epistemic matrix.

```json
{
  "revision": "r2",
  "status": "pre-intent — confirmed for intake; not approved for implementation",
  "date": "2026-09-28T14:27:01.270020+00:00",
  "reviewer": "operator",
  "source": "Conversation: after the full r2 and plain-language restatement, operator said \"proceed. focus on practicality using the principle of pragmatic engineering\".",
  "reason": "Save the reviewed description only. Keep the first slice small and empirical; do not build additional machinery before measurements.",
  "approved_scope": "Save ai-native-sdlc/pre-intent.md with confirmation receipt only. No experiment, installation, cleanup, source change, commit, push, or PR authorization.",
  "reviewed_draft_sha256": "7955c21f26638df47234df56edb96a4374dddc7143f81923a265317b54e139a1",
  "independent_checker": "factory-checker-recovery",
  "independent_review": "checker-r2.json"
}
```

---

# Software-factory pre-intent — r2 — 2026-09-28

**PROPOSAL; root save UNCONFIRMED. Not implementation or experiment authorization.**
This external interview record is authorized at `/Users/jondev/.local/share/seed-me/sessions/a5666330-19f6-4018-bce9-ffd7c9175ee6/pre-intent-r2.md`; r1 remains unchanged historical evidence.
After independent checking and explicit human affirmation of this exact r2, save it only to `/Users/jondev/dev/active/ai-native-sdlc/pre-intent.md`. Do not substitute a `runs/` path. No checkout writes before that affirmation.

## Problem, accepted direction, and outcome

Build toward a minimal seed-to-PR software-factory harness, but first measure whether stage-scoped routing selects useful guidance without burdening plain tasks, and whether one temporary guide has a safe ownership/read/prune lifecycle.
Accepted direction: **ai-native-sdlc is the artifact home; first experiment is stage `test`; one real throwaway Git checkout; ten judged tasks, five fitting and five plain; one routed guide installed with ephemeral tracking, explicitly read, then pruned only after dry-run review and human confirmation.**
This first slice is empirical, not a complete factory implementation. Defer scaffold installation, multistage machinery, new code, tuning, evaluator/calibration expansion, and product goldens until the numbers exist.
Use a local disposable clone of ai-native-sdlc at the recorded revision, not an empty temporary directory. Its creation and all experiment writes await the later execution gate. Preserve evidence outside the prunable skill payload.

## Authority, later lifecycle, and step boundaries

Each step requires author/worker evidence, a different independent checker, then the actual human decision before advancement. No self-approval, fabricated receipts, silent stage advancement, or confidence-as-authorization.
Retain the later **plan → design → build → test → deploy** lifecycle. Every stage uses `tink-route --stage <stage>` with task prose as its router input. Each stage requires its actual human-recorded approval with **reviewer, source, and reason**; helpers never approve. Green is not safe: test success is evidence, not a safety, release, or deployment verdict. Independently verify each candidate head before landing; evidence for an earlier head is not acceptance of a later one.
These are future process requirements, not a claim that the current helper implements them all: its `decide` command accepts stages 1–3 only, and release authority remains external. [A/assets/_system/scripts/sdlc.py:225–233,366–371; A/assets/_system/SDLC.md:24,71–73]
Confirmation of r2 authorizes **only the root pre-intent save**. It does not authorize checkout creation, live calls, keys, installs, prompt execution, cleanup, source edits, commits, pushes, or a PR. Revised pre-intent content needs renewed content-bound confirmation.
The future independently checked experiment brief must bind actual commands, cwd, provenance, prompt bytes, permitted mutations, evidence destinations, and cleanup scope before human execution authorization. No live command is asserted settled here.
No commits are authorized. The eventual PR destination remains, using the existing Opening-a-PR playbook only after separate authorization; its commit/reset instructions are not present authority. Read-only playbook: `/Users/jondev/.pi/agent/git/github.com/McCune1224/pi-pstack/skills/poteto-mode/playbooks/opening-a-pr.md:5–9,25–33`.

## Frozen routing, baseline, and pre-network blocker

Every routing input must describe the actual task and capability need in prose; every experiment routing invocation must explicitly use **`--stage test`**, not rely on implicit stage context. Freeze current settings: model `jev-1.13.0`, threshold `0.60`, tri-gate on, rerank on, fits threshold `0.30`, multi off; top-k remains its inactive default `3`. Do not tune after outcomes. [R/src/tink_route/core/constants.py:6–22,53–55; R/src/tink_route/cli.py:103–130]
Proposed permanent **control-plane manifest** plain-name pins: **how, architect, swarm, interrogate, manage-tink**. Their installation/pinning is not claimed complete. Retain/protect them; they are not the temporary intervention and must never become prune targets. Verify baseline manifest protection before measurement; routing must not rewrite that baseline. These names and their publisher references stay OUTSIDE stage context. [R/src/tink_route/adapters/ledger.py:161–182,229–240]
The permanent baseline is distinct from the **testing-skillset candidate pin**, currently revision `a404763afd007ee280dc0c59a86402e12e5369d2`; record its actual members and payload hashes as control-plane evidence, not a stage-prompt roster. [C:2–13]
**Fail-closed pre-network audit:** capture the ACTUAL fully assembled pre-route stage prompt, including system/inherited context, automatic skill discovery, and injected task context. The independent checker must inspect those exact bytes before the first routing call: **ZERO guide names or rosters—baseline or candidates—and no inherited skill names, discovery metadata, publisher references, or other skill-context leaks.** The task must describe the need, and actual argv must carry `--stage test`. An approved plain-name manifest does NOT authorize a roster in the prompt. Missing, unavailable, or leaking assembled context blocks routing; any changed assembly requires a fresh audit. Docs, intended flags, and this proposal are not proof.
Router-internal candidate criteria remain control-plane routing data, not stage-agent context. Only the needed winning guide may enter stage context through a validated installed-file **direct read AFTER routing**, with no restart; do not preload baseline guides or candidate discovery context. [R/src/tink_route/core/engine.py:195–201; A/references/toolchain-routing.md:21–28]
The audit remains an explicit known uncertainty and pre-network blocker. Keep publisher/source provenance in evidence, not run prompts.

## Ten task candidates — verbatim router inputs

The independent checker judged S1–S5 fitting and P1–P5 plain. These are pre-run labels, **not measured router outcomes**. They are semantic inputs only, not authorization to implement the scenarios. The agent authors tasks and investigates fit; the operator need not author them or select a guide.

| ID | Expected class | Task |
|---|---|---|
| S1 | Fitting | Reproduce an interactive terminal wizard that hangs after Escape and resize. Drive deterministic keyboard inputs and retain a terminal transcript showing the failure. |
| S2 | Fitting | Profile an interactive command-line application whose memory grows across repeated prompt cycles. Capture repeatable input, memory observations, and evidence of the growth. |
| S3 | Fitting | Verify a browser dialog’s keyboard focus, Tab order, and focus restoration after closing it. Capture accessibility snapshots and a reproducible interaction trace. |
| S4 | Fitting | Reproduce a browser layout regression that appears only after scrolling and resizing. Capture before-and-after screenshots and console evidence at fixed viewport sizes. |
| S5 | Fitting | Audit an existing application verification guide and feature map against source and live user flows. Identify documentation drift separately from product regressions and retain coverage evidence. |
| P1 | Plain | What is 17 multiplied by 23? |
| P2 | Plain | Explain what a unit test is in one sentence. |
| P3 | Plain | Correct this sentence: “The tests has passed.” |
| P4 | Plain | Rename tmp to elapsed_ms in this snippet: `tmp = 12; print(tmp)`. |
| P5 | Plain | Return these words in alphabetical order: zebra, apple, pear. |

Capability grounding: `~/.tink-library/skills/control-cli/SKILL.md:3–15`, `control-ui/SKILL.md:3–15`, and `maintain-verification-skill/SKILL.md:25–37`. These are interview evidence citations only; guide names and this evidence roster must not be injected into stage prompts.

## Existing offline intake checks — not harness acceptance

A = `/Users/jondev/dev/active/ai-native-sdlc`; R = `/Users/jondev/dev/active/tink-route`; C = `/Users/jondev/.tink-library/skillsets/testing-skillset.json`.
These exact checks already ran without experiment writes or live routing. Their outputs prove only the stated intake contracts.

Cwd: `/Users/jondev/dev/active/ai-native-sdlc`
```sh
python3 -B scripts/package.py --check
```
Exit `0`; stderr empty; exact stdout:
```text
Package manifest matches all assets.
```
Contract: `A/scripts/package.py:26–31`.

Same cwd:
```sh
python3 -B assets/_system/scripts/sdlc.py --help
```
Exit `0`; stderr empty; exact stdout:
```text
usage: sdlc.py [-h] {new,status,decide,verify,lock-tests,skills} ...

Local workflow evidence. Human identity and release authority belong to the
forge.

positional arguments:
  {new,status,decide,verify,lock-tests,skills}

options:
  -h, --help            show this help message and exit
```
Parser availability only, not harness acceptance. [A/assets/_system/scripts/sdlc.py:357–388]

Cwd: `/Users/jondev/dev/active/tink-route`
```sh
PYTHONPATH=src:tests python3 -B -m unittest -v test_skillset.TestStageMappings.test_resolve_stage_mappings test_skillset.TestCliParserSkillsetOptions.test_cli_parser_skillset_options
```
Exit `0`; stdout empty; exact observed stderr:
```text
test_resolve_stage_mappings (test_skillset.TestStageMappings.test_resolve_stage_mappings) ... ok
test_cli_parser_skillset_options (test_skillset.TestCliParserSkillsetOptions.test_cli_parser_skillset_options) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```
The elapsed-time text is observed, variable, not a golden. These two method-level checks cover mappings/parser behavior; they exclude the class’s shelf-dependent test. [R/tests/test_skillset.py:56–68,94–101]
The earlier forced missing-key exit `2` is an error-path observation, not this experiment or proof that stage routing works. [R/src/tink_route/cli.py:316–323]
Do not run initializer `--check` during read-only intake: it still creates/removes a lock. Do not use bundled runtime operations as root-checkout operations: ROOT derives from the script location. Full workflow tests create temporary repositories and commits. [A/scripts/init.py:56–58,98–100,155–157; A/assets/_system/scripts/sdlc.py:20; A/tests/test_sdlc_workflow.py:22–35]

## Provenance observed; recheck before execution

A HEAD: `1096c493729d98fa56dd3bddeca109ea80618c45`; R editable-source HEAD: `0f9ed6e44a4527bad7285fd11954cd164ce6cef2`. [A/.git/refs/heads/main:1; R/.git/refs/heads/fix/rerank-fits-excerpts:1]
Binary path: `/Users/jondev/.local/bin/tink-route`; observed version output: `tink-route 0.6.0`; SHA-256: `1f462d3da133235d2194eb28695aafeec35cdc77bfd1dbdeed75ef1d2cd5dd89`.
Read-only SHA-256 observations of the reviewed editable sources follow; matching version strings do not establish binary/source equivalence.
```text
R/src/tink_route/cli.py                    df1f575c2fb91bcab1bc30ed6f17c2b5fdee929a8997264c21a67965e4fa447b
R/src/tink_route/core/constants.py         3363bcf6b64673dcb489fbb24fe9e7f0565bfde955e2c2d793ef45aea0aef23c
R/src/tink_route/core/engine.py            4465d4eb5c4759e202a5055c842f6c2eafd617b3226119982949890c2dbd6bb7
R/src/tink_route/core/models.py            b374c6feb2617e54439c47b273608ea2f29e313d212f6739aad5266868ebfe3b
R/src/tink_route/adapters/client.py        dd53451201be8f0f476911f3f52e0dcedd98bf8e944ae731e7a65435aefd1b1d
R/src/tink_route/adapters/ledger.py        5b932ef4eb0810ec1d59845ce0144a5402238fcecbcbe59093da89217aa7f628
R/src/tink_route/metadata.py               2caee498758cb0c87c666c686519190d2855e244083aec39a8bae108e8ab13e6
A/assets/_system/scripts/sdlc.py           9557cf723d20158791fbb9ec4cc8be429fcf4fca1f517b8fff5a57380eb19bdc
A/scripts/package.py                      9369d9cc68ca8df927ec75ab66cf4a8d713efb9ba138cceae395338143ba3e8c
A/scripts/init.py                         3d004e07d3ecbbc660c98d568592871dc257bb341bc9c4dcf03438e0cc0aafe1
```

## Future experiment requirements — pending human execution gate

Preserve exact router stdout, stderr, exit status, and **every returned score/field**, including uncertainty and errors; do not require upstream distributions the CLI does not return. Preserve actual prompt/argv, binary/source provenance, candidate hashes, and timing. Ten task invocations are not necessarily ten HTTP requests: reranking/retries exist. [R/src/tink_route/core/models.py:8–79; R/src/tink_route/adapters/client.py:74–127,185–235]
Judge actual winner fit independently against the task and selected guide; report fitting matches out of five and plain false positives out of five. Keep `no_skill_needed`, `no_match`, uncertainty, and operational errors distinct. No hindsight relabeling, success guarantees, or repeat-until-green calls. [R/src/tink_route/cli.py:417–425]
**Routing failure for ANY reason → work guideless within the already authorized task scope, record the cause, and never guess a guide or fallback.** This includes unavailable routing, missing credentials/library, errors, low confidence, or no usable match. An unsafe partial installation instead stops further mutation pending inspection; it does not justify an invented fallback or blind retry. A failed pre-network prompt audit permits no routing call.
Proposed mechanics for the later brief: nine recommendation-only invocations, then S1 as the sole install-enabled invocation with explicit ephemeral tracking under its separately approved mutation scope. No extra reroute or fallback to manufacture an installation. If it abstains or fails, retain the result, apply the guideless rule, and report lifecycle incomplete.
Completion requires evidence of one newly routed guide installed and tracked, baseline pins unchanged/protected, a contained entrypoint explicitly read only after routing with no restart, and a reviewed ledger-only dry-run followed by separate human confirmation before actual pruning. No `--all-unpinned`; evidence survives pruning. An install response alone is not reading. [A/references/toolchain-routing.md:21–35; R/src/tink_route/core/engine.py:195–201]
Check actual ledger ownership: pre-existing skills are not adopted. Installation can succeed while tracking fails; the lock is not rollback. Stop and inspect unsafe partial state before any further mutation. [R/src/tink_route/core/engine.py:66,123–133,185–202; A/references/toolchain-routing.md:37–41]
This empirical path does not claim the uninstalled SDLC wrapper enforces it. If that wrapper is later used, preserve router JSON: it normalizes router exit `1` to wrapper success. [A/assets/_system/scripts/sdlc.py:329–354,388]
After numbers, propose only warranted product work and separately reviewed machine goldens, including zero-roster prompt-audit blocking, baseline retention, guideless routing failure, ownership/read/prune boundaries, and matrix movement versus non-invalidating appends. None is an existing acceptance test or a present implementation commitment.

## Running harness patch log

Keep the existing `/Users/jondev/.local/share/seed-me/sessions/a5666330-19f6-4018-bce9-ffd7c9175ee6/patch-log.jsonl` running from this run: append observed harness defects, corrections, evidence references, and outcomes; never rewrite history. Active-lead owns its continuity. Retain it and promote it as run evidence after the authorized pre-intent save, within the next authorized artifact-write scope; root-save affirmation itself still authorizes only `pre-intent.md`.
This is the operational patch history, not another doubt ledger. Link uncertain items to the single epistemic matrix below; do not copy its uncertainty or movement state into the patch log.

## Epistemic matrix — born 2026-09-28; this run only

This inline matrix is the single home of doubt, separate from the ten-task table. Future stage papers point here, never copy it. The external revisions are interview records; after authorized root save, the root matrix is authoritative, not a second evolving copy.
- **Known knowns (disk receipts):** package manifest check and two router method checks passed as quoted above; installation/tracking are separable outcomes. [A/scripts/package.py:26–31; R/tests/test_skillset.py:56–62,94–101; R/src/tink_route/core/engine.py:123–133]
- **Known unknowns (named owners):** active-lead owns obtaining the actual zero-roster assembled-prompt audit, provenance recheck, ten measured outcomes, and ownership lifecycle evidence; the different independent checker reviews each before human advancement. Prompt audit is a pre-network blocker, not satisfied by frozen flags or plain-name pins.
- **Unknown knowns (unsigned-lesson hunt):** factory-intake-author owns reconciling lessons still carried only in interview/checker feedback with the reviewed disk contracts; retain discoveries here, without speculative extra scope. The earlier rejected brief is a lesson source, not implementation authority.
- **Danger zones (past surprises):** the earlier brief selected an entire test class while claiming to exclude its shelf-dependent method; initializer preview was mistaken for no-write; install locking was mistaken for atomic rollback. Counter-receipts: R/tests/test_skillset.py:64–90; A/scripts/init.py:56–58,98–100; R/src/tink_route/core/engine.py:123–133. Active-lead owns keeping those boundaries visible at each gate.
Each stage appends a dated stamp; never rewrite the matrix body. Preserve the movement log as an asset. **Only an item moving between boxes voids downstream approvals.** Small edits append without voiding. Pre-intent content-bound confirmation is a separate rule. Initial movement log: none; no stage has advanced.
2026-09-28 r2 intake clarification stamp: actual pre-route context must contain no guide roster or inherited names; restore guideless failure, later lifecycle approvals, and operational patch-log continuity. No cross-box movement is claimed; r1 remains retained. This is still pre-confirmation drafting, not stage advancement.
Current SDLC receipt hashing does not implement this matrix-specific rule; do not misrepresent it as enforcement. [A/assets/_system/scripts/sdlc.py:101–120]

## Remaining human decision

After the independent checker reads this actual external draft: **confirm or reject exact pre-intent r2 for saving to `/Users/jondev/dev/active/ai-native-sdlc/pre-intent.md` only.** Root save remains unconfirmed. A future independently checked experiment brief must bind specific commands before any live run. This is neither full factory acceptance nor readiness to implement.
