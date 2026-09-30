# Seed contract: Tidy ~/Downloads (lean path)
status: draft        revision: 1        date: 2026-09-28

## You are confirming
- Goal: decide whether ~/Downloads needs a tool; if not, record why and a light habit. **Result: build nothing.**
- What gets built: nothing. A weekly manual sweep, plus one measurable trigger (below) that says when to build the script after all.
- What does not: any script, watcher, or deletion. If the trigger fires, the preview-then-apply script (D1) and Trash-only rule (D4, D5) apply.
- Accepted unchanged: 2 of 2 suggestions (chosen by you: 3)
- Still unknown: how fast the folder grows; whether the Finder permission prompt is acceptable (untested).
- Three riskiest items: (1) the "100 items" trigger is **my invented number**; (2) both suggestions (Trash method, build nothing) were accepted by arrow; (3) the trigger command has run once, today, and says 30.

## Now
- Settled: build nothing; weekly sweep; trigger `ls -1 ~/Downloads | wc -l` stays under 100.
- Uncertain: growth rate.
- Needs you next: confirm this seed contract (set `status: confirmed`, or say "confirm").

## Goal
G [user] "Decide whether `~/Downloads` needs a tool at all. If it does, build the smallest safe one: a script that shows a plan of moves and applies only what you approve. If it doesn't, record why and a light weekly habit instead." — chat: "confirm the goal"

## Decisions
D1 [user] Keep option A: a script you run by hand, with preview then apply — chat: "Keep A"
D2 [user] Cut option B: no background watcher — chat: "cut B"
D4 [user] Deletion is only ever a move to the Trash; never `rm` — chat: "only to Trash, never rm" (instinct given first, before any suggestion was shown)
D5 [delegated] If it ever trashes, it asks Finder to do it (so "Put Back" works); needs a one-time macOS permission — chat: "your arrow" (accepts my suggestion A)
D3 [user] Leaning: "C is probably enough" — chat: "C is probably enough". Superseded by D6.
D6 [delegated] Build nothing. Do a weekly manual sweep; build the script (D1) only if the trigger fires — chat: "your arrow" (accepts my suggestion A)

## Assumed (not confirmed by you)
S1 [agent] macOS only — why it is safe: this is your machine and both answers build the same script.
S2 [agent] One user, one folder (~/Downloads), no subfolder recursion — why it is safe: the folder has 4 sub-folders and moving whole folders is enough.

## Constraints and exclusions
C1 [user] Never delete automatically — chat: "Nothing is ever deleted automatically" (from the draft you kept). At your request it may only move to the Trash, never `rm` (D4).

## Acceptance checks
A1 [agent] The folder stays small.
   cmd: `ls -1 ~/Downloads | wc -l` | expect: a number under 100 (today: 30) | cwd: any. If it reaches 100, build the script (D1). **100 is my number; change it.**

## Open questions
None blocking. Deferred: which weekday to sweep (your choice, no effect on the contract).

## Evidence
E1 [evidence] 32 items in ~/Downloads: 13 pdf, 4 folders, 4 dmg, 4 html, 2 no extension, 5 other (python scandir, 2026-09-28).
E2 [evidence] 3 files are over 200 MB; median age 5.3 days; oldest 193 days; 1 file older than 90 days (same scan).
E3 [evidence] No tidy tools installed: hazel, fdupes, rmlint, dupeguru not found (`command -v`, 2026-09-28).
E4 [evidence] The user's Trash directory exists at ~/.Trash (`test -d ~/.Trash`), so a "move to Trash" is recoverable while `rm` is not.
E5 [evidence] ~/Downloads totals 1.7G on disk (`du -sh`, 2026-09-28).
