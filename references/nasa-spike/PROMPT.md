# NASA-spike integration prompt (ai-native-sdlc)

This folder holds 6 artifacts salvaged from the archived `agentic-se-skills`
repo (NASA Systems Engineering handbook lineage), pre-screened by Jev as
alpha for ai-native-sdlc. Nothing here is wired in. Your job: for each
artifact, decide PROMOTE (integrate), ADAPT (distill then integrate), or
DROP (leave quarantined). Ask the operator when the decision changes
user-visible behavior or stage contracts.

## Context to load first

- `references/lifecycle-stages.md` — stage contracts index (01-plan … 06-maintain)
- `references/toolchain-routing.md` — existing skill-routing doctrine
- `references/sop-jev-code-verification.md` — existing verification SOP
- `_shared/REVIEW.md` and the stage `CONTEXT.md` files in `assets/` for the
  stage you are touching

## Artifact questions

### 1. requirements-taxonomy.md
- Stage 01-plan takes reviewed briefs as definition input. Where exactly do
  goal/objective/requirement/constraint/assumption labels attach — brief
  template, stage gate checklist, or reviewer guidance?
- The router rule ("never promote goals into requirements") — is this a new
  gate in 01-plan, or a review-scope line in `_shared/REVIEW.md`?
- Its citations point at `source-grounding.md` + extraction pages that do not
  exist here. Strip, vendor, or rewrite them?

### 2. verification-vs-validation.md
- ai-native-sdlc verifies against requirements (stage 04-test) but has no
  validation concept. Does validation become a 05-deploy gate, a review-scope
  item, or its own checklist?
- What counts as a validation signal for a local workflow (no production
  telemetry)? Define it or drop the artifact.
- Same dangling-citation question as above.

### 3. interface-contracts.md
- Which stage owns boundary contracts — 02-design, 03-build, or both?
  What is the minimal contract shape (owner, I/O, errors, version, rollback,
  open questions) vs the full 6-step playbook?
- How does a boundary contract relate to existing verification evidence?
  Does it create a new receipt type or ride on existing ones?

### 4–6. nasa_se_codebase_assessment_{rubric,scorecard,findings_template}.md
- The rubric is 413 lines. Do we vendor it whole, distill a local checklist,
  or reference it as an optional deep-assessment?
- Who runs an assessment — which stage, which role, on what trigger
  (release-readiness, intake audit, refactor gate)?
- Where do scorecard outputs live — run receipts, a new assessment record,
  or outside the run entirely?

## Decision rules

- Prefer ADAPT over PROMOTE: distill to the smallest text that changes a
  stage contract, template, or checklist. Do not vendor bulk.
- One artifact per change; keep stage contracts owning their outputs.
- Prove with the repo's own gates (`package.py` checks, pytest suite).
  Report what ran and what remains unverified.
- Never commit. Leave promoted text staged or unstaged per operator direction.
