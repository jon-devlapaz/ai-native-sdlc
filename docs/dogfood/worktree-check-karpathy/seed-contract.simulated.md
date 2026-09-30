# Seed contract (SIMULATED): worktree check, Karpathy-engram operator
**Status: `simulated — not confirmed by a human`.** Revision r1, 2026-09-29. Operator: an agent playing **engram: andrej-karpathy (a simulation of his public record, not the person)**, brief built by `engram_brief.py` from `PERSON`, `MIND`, `CONSTITUTION`, `STAKES`, `FIDELITY`. Its words are inferences from that material, never statements by him. No person made these decisions. This does not authorize building anything. Same idea and interviewer as `../worktree-check/` (persona-only operator), for comparison.

## You are confirming (if a person adopts this)
- **Goal:** a small read-only tool that lists a person's git worktrees and, for each, says whether it looks in use, needs checking, or is safe to remove, and shows the evidence (uncommitted files, count and subjects of commits on no remote, time since last change). It never removes anything.
- **What gets built:** the report only. Names (`wt_report.py`, its flags, the fixture scripts) are placeholders.
- **What does not:** any removal command.
- **Simulated answers: 7 (6 decisions plus confirming the goal), human answers: 0.** The operator volunteered its own rule on 3 decisions (report only; unpushed commits mean "check first"; what "in use" means). It accepted my option but changed it on 3 (recoverable commits; the hidden-files rule; the acceptance checks). It accepted none of my suggestions unchanged.
- **Still unknown:** whether a person would agree; how the tool behaves on other machines; the skip list and the 60-minute window are untested guesses.

## Decisions (all authority `simulated`)
| Decision | Answer |
|---|---|
| Report only or also remove | Report only. |
| Unpushed commits | They make a worktree "check first"; the verdict shows the count and the commit subjects. |
| What "in use" means | The newest file change, not the last commit time; a 60-minute window kept as one tunable constant (the interviewer's number). |
| Recoverable commits | A commit is recoverable if some remote contains it (`git branch -r --contains`). A merge into main counts only when main is on a remote. A repo with no remote makes every worktree with commits "check first". |
| Never-committed files | Untracked files always block "safe". An ignored file not on the skip list blocks "safe" and is named. Regenerable folders (`__pycache__`, `target`, `node_modules`, `.pytest_cache`, `dist`, `build`) do not block, but are listed collapsed on one line ("skipped: target/, __pycache__/") so a stale list shows up. The skip list is one constant next to the window. |
| Acceptance checks | The five below. |

## Acceptance checks (placeholders: nothing is built; none has been run)
1. **Real machine: every worktree is listed, wherever it lives.** `python3 wt_report.py --json | python3 -c "import json,sys; print(len(json.load(sys.stdin)))"` | expect: the total of `git worktree list` across repos under ~/dev/active | cwd: folder holding `wt_report.py`
2. **Fixture: one throwaway repo, four worktrees, one verdict each.** `T=$(mktemp -d) && bash tests/make_fixture.sh "$T" && python3 wt_report.py --json --root "$T" | python3 tests/verdicts.py` | expect: `unpushed: check first (2 commits on no remote, subjects shown)`, `untracked: check first`, `config: check first (names .tink/; skipped: __pycache__/)`, `fresh: in use` | cwd: same
3. **Real machine: it changes nothing on disk.** `touch /tmp/wt-marker && python3 wt_report.py --json >/dev/null && find ~/dev/active ~/dev/sandbox -path '*/.git/*' -newer /tmp/wt-marker | wc -l` | expect: `0` (may flake if an agent commits meanwhile) | cwd: same
4. **Fixture: a repo with no remote.** `T=$(mktemp -d) && bash tests/make_no_remote_fixture.sh "$T" && python3 wt_report.py --json --root "$T" | python3 tests/verdicts.py` | expect: every worktree with commits is `check first` | cwd: same
5. **A person reads the report and understands each verdict.** **Human-only: cannot run automatically, and has not been done in this simulated run.**

## Assumed (not confirmed by anyone)
- One laptop, one user, repos under ~/dev/active (the operator did not object).

## Evidence (read-only, 2026-09-28/29)
- 3 extra worktrees, none with an upstream: `tink-wt-activation` clean, 4 commits on no remote; `tink-route-wt-activation` 1 uncommitted file, 3 commits on no remote; `tink-skills-viewer` 11 uncommitted files, 6 commits on no remote, newest changed file 4 minutes old at the time.
- In `tink`, `tink-route`, and `tink-skills`, local `main` has no commits missing from a remote.
- Ignored entries seen: `target/`, `.tink/`, `__pycache__/` folders.
- **A flaw the operator found in the interviewer's draft:** the draft defined "safe" as "nothing uncommitted, nothing unsaved," which would have passed `tink-wt-activation` (clean, but 4 commits on no remote).
- **Inferred, not checked:** removing a worktree deletes its folder including ignored files, but keeps the branch and commits.

## Riskiest items
1. The 60-minute window and the skip list are guesses.
2. The operator is a model of a public record answering about someone else's idea: it shows how such a mind would push on the design, not what you or that person would decide.
3. Nothing here has been run.

## Adoption
A person must read this and start their own session or lean file with their own confirmation. The simulated session's operator cannot be changed to human.
