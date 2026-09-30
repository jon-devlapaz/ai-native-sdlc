# Seed contract (SIMULATED): worktree check
**Status: `simulated — not confirmed by a human`.** Revision r1, 2026-09-28. Operator: an agent playing "Priya" (cautious; accepts suggestions about 1 time in 3). No person made these decisions. It does not authorize building anything.

## You are confirming (if a person adopts this)
- **Goal:** a small read-only tool that lists git worktrees and says for each whether it is in use, needs checking, or looks safe to remove, and why. It never removes anything.
- **What gets built:** the report only (names below are placeholders: `wt_report.py`, its flags).
- **What does not:** any removal command; scanning folders instead of asking git.
- **Simulated answers: 6 (5 decisions plus confirming the goal; the page counts the 5), human answers: 0.** In her own words: 3 (what counts as safe; the hidden-files refinement; choosing report-only). Accepted my suggestion or number: 3 (confirm the goal; 60-minute window; the acceptance checks).
- **Still unknown:** whether a person would agree with the persona's choices; how the checks behave on other machines.

## Decisions (all authority `simulated`)
| Decision | Answer | Source |
|---|---|---|
| Goal | as above | "Confirm." |
| Report only or also remove | Report only | "Option A sounds right—I don't trust myself to not accidentally delete something important" |
| In use | changed within 60 minutes | "60 minutes feels right—anything I touched in the last hour I probably care about" |
| Safe to remove | only if commits are merged into main or pushed somewhere recoverable | "Only if the commits are merged into main or pushed somewhere I can get them back from." (instinct, given before any suggestion) |
| Uncommitted and hidden files | never "safe" with uncommitted or untracked files; show hidden config like `.tink/`, skip `__pycache__`, `target`, `node_modules`, `.pytest_cache`, `dist`, `build` (the skip list is the interviewer's, changeable) | "A, but skip the `__pycache__` and build stuff—just show me the config files like `.tink/` that I'd actually miss." |
| Acceptance checks | the five below | "Your arrow." |

## Acceptance checks (placeholders: nothing is built; none has been run)
1. **Every worktree is listed, wherever it lives.** cmd: `python3 wt_report.py --json | python3 -c "import json,sys; print(len(json.load(sys.stdin)))"` | expect: the total of `git worktree list` across repos under ~/dev/active (3 extra worktrees today, plus main folders) | cwd: folder holding `wt_report.py`
2. **Risky work is never called safe.** cmd: `python3 wt_report.py --explain tink-wt-activation` | expect: a line saying NOT safe, 4 commits not on any remote and not merged into main | cwd: same
3. **It changes nothing on disk.** cmd: `touch /tmp/wt-marker && python3 wt_report.py --json >/dev/null && find ~/dev/active ~/dev/sandbox -path '*/.git/*' -newer /tmp/wt-marker | wc -l` | expect: `0` (may flake if an agent commits meanwhile) | cwd: same
4. **Config is shown, junk is not.** cmd: `python3 wt_report.py --json | grep -c "\.tink"` and the same for `__pycache__` | expect: at least 1, then exactly 0 | cwd: same
5. **A person reads the report and understands each verdict.** **Human-only: cannot run automatically, and has not been done in this simulated run.**

## Assumed (not confirmed by anyone)
- Laptop only, repos under ~/dev/active, one user (the operator did not object when it was stated).

## Evidence (read-only, 2026-09-28)
- 3 extra worktrees. `tink-skills-viewer`: 9 uncommitted files, last commit 21 min ago, newest changed file 1 min ago. `tink-route-wt-activation`: 1 uncommitted file, last commit 341 min ago, 3 commits on no remote. `tink-wt-activation`: clean, last commit 356 min ago, 4 commits on no remote. None has an upstream; neither activation branch is merged into main.
- The operator's guess that the 9-file worktree came from a crashed agent was **wrong**: it is in active use.
- `tink-skills-viewer` lives outside ~/dev/active but belongs to a repo inside it, so the tool must ask git for each repo's worktrees.
- Hidden (ignored) entries: `target/`, `.tink/`, several `__pycache__/` folders.
- **Inferred, not checked:** removing a worktree deletes its folder (including hidden files) but keeps the branch and commits.

## Riskiest items
1. The 60-minute window and the skip list are not the result of any measurement.
2. Half the answers were accepted suggestions from a persona built to accept about a third of them; that mix is a design of the test, not a finding about people.
3. Nothing here has been run.

## Adoption
A person must read this and start their own session or lean file with their own confirmation. The simulated session's operator cannot be changed to human.
