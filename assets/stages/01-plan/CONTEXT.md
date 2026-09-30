# Stage 01: Define intent

Inputs: originator's request and `_shared/intent-template.md` for full runs.
Read the run's `run.json` to select its profile.

For light runs, write `runs/<slug>/brief.md` with problem, acceptance criteria,
approach, risks, and verification. Define the implementation checklist as
item definitions in `runs/<slug>/checklist.json` (id, description, verify, and a `check` whenever an automated proof exists). Combine stages 01–03
into one human-reviewed definition. Light runs have ONE definition gate, recorded as stage 3 (`sdlc.py decide <run> 3 ...`): the approved `brief.md` + `checklist.json` are the intent, design and plan.
For full runs, write `runs/<slug>/01-plan/output/intent.md`.
Use `seed-me` only for consequential unresolved decisions.
Output: `runs/<slug>/brief.md` and `runs/<slug>/checklist.json` (light runs), or
`runs/<slug>/01-plan/output/intent.md` (full runs).

Gate: actual human acceptance recorded with `sdlc.py decide`; text status tags
are not approval evidence. Follow `_system/scripts/status.sh <slug>`.
See `_system/SDLC.md` for rejection, stale inputs, and authority boundaries.

## Skills

Skillset: `planning-skillset` (pin: `.tink/skillsets/planning-skillset.json`).
- Once per machine/library, after reviewing the pin (it selects exact upstream code):
  `tink library fetch .tink/skillsets/planning-skillset.json`
- At stage open, compile the required disciplines, then start a NEW session so
  `AGENTS.md` is re-read: `tink use planning-skillset --snapshot runs/<slug>/01-plan`
- For a capability gap: `tink-route --receipt runs/<slug>/skills.jsonl "<what you need>"`
  (asks this stage's shelf, the skillset named in the rules block above; prints the skill on stdout.
  Exit 1 means nothing on the shelf fits, and a `Hint:` line may name a skill on another stage's shelf that
  was not delivered; exit 1 or 2 means continue without a skill).
