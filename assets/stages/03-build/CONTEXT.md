# Stage 03: Implement

Inputs: current approved spec for full runs, or combined brief for light runs.
Output: `runs/<slug>/03-build/output/plan.md` for full runs, the approved checklist definitions
in `runs/<slug>/checklist.json` for both profiles, and code in an isolated worktree/clone.
Items should carry a `check` whenever an automated proof exists; `verify` runs it and no mark is needed.

Inspect code, write the plan, and obtain the actual stage 3 human acceptance before
implementation. An explicit user instruction to execute a reviewed proposal is
implementation authority; never fabricate separate role approvals.
Each concurrent writer needs its own checkout. Use the serialized skill wrapper
in `_system/SDLC.md`; no shared writable skill symlinks or automatic lockfile rewrites.

For bug fixes, reproduce the expected failure first, obtain independent acceptance,
and record protected test inputs with `sdlc.py lock-tests`. Implement and verify in
a loop with stage 04. Update the plan when scope changes and renew stale decisions.
Mark items only with `sdlc.py mark <slug> <item-id> passed|failed --evidence <text>`; never hand-edit receipts.
