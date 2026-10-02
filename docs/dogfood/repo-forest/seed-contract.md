# Seed contract: Repo forest (isometric view of local git repos)
status: confirmed (by user in chat, 2026-09-28: "confirmed")        revision: 1        date: 2026-09-28

## Now
- Trying to achieve: a simple, clean app that shows the git repos in `~/dev/active` as trees on an isometric board, with local git state shown as tree effects (v1 local-only).
- Settled: G, D1-D5.
- Uncertain: nothing blocking. C2, C3 and A1-A4 are agent proposals you have not yet confirmed.
- Needs you next: review C2, C3, A1-A5; then set `status: confirmed` (or edit anything you disagree with).

## Goal
G [user] "make a simple clean app to view all the git repos in my machine on a isometric board like they are trees"

## Decisions
D1 [user] Git state is shown as visual effects on each tree. Given examples: dirty = a dirty-looking tree, PRs = ornaments, extra branches = "another thing" — source: your message.
D2 [user] Scan scope is `~/dev/active` only (15 repos) — source: your reply to Q1, "dev active".
D3 [user] Delivery is a local web page (a small local script gathers repo state; the page renders it) — source: your reply to Q2, "local web page".
D4 [user] V1 is local-only (dirty state, branches, ahead/behind, last-commit age). PR ornaments come second — source: your reply to Q3, "local only first".
D5 [delegated] Visual vocabulary (the agent chose; you may override any row) — source: your reply to Q4, "use your creativity for this decision. i defer to you". Covers Q4 only.
  - Clean, up to date: healthy green tree.
  - Dirty: grime and mud speckle on trunk and leaves, heavier with more changed files; untracked files show as weeds at the base.
  - Extra local branches: small saplings around the trunk, capped at 5 with a "+N" mark.
  - Ahead of remote: taller crown with a few golden buds. Behind remote: trunk leans toward the remote side.
  - Last-commit age: leaves shift green -> autumn -> bare with light frost past ~90 days.
  - Repo with no commits: a seedling. Detached HEAD: a tree with a small tag hanging on it.
  - Reserved for later: PR ornaments (baubles on the crown). Stash count is not shown in v1, to stay simple.

## Constraints and exclusions
C1 [user] "simple clean" — source: your message.
C2 [agent] Proposed: read-only. The app never runs anything that changes a repo (no commit, checkout, fetch, gc), and runs git with `--no-optional-locks` because plain `git status` can refresh `.git/index`. — why: cheap safety for a viewer; not yet confirmed.
C3 [agent] Proposed: the server binds to 127.0.0.1 only. — why: it exposes local paths and repo state; not yet confirmed.

## Acceptance checks
All [agent] proposals. Assumes the app lives at `~/dev/active/repo-forest` (name and location not yet decided).
A1 [agent] cmd: `python3 server.py --json | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d)); print(sorted(d[0]))"` | expect: `15`, then a field list containing at least `name, path, dirty, branches, ahead, behind, last_commit_age` | cwd: `~/dev/active/repo-forest`
A2 [agent] cmd: `touch /tmp/rf-marker && python3 server.py --json >/dev/null && find ~/dev/active -path '*/.git/*' -newer /tmp/rf-marker | wc -l` | expect: `0` (read-only; may flake if another tool touches a repo during the run) | cwd: `~/dev/active/repo-forest`
A3 [agent] cmd: `python3 server.py --port 8140 & sleep 1; curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8140/; lsof -nP -iTCP:8140 -sTCP:LISTEN | grep -c '127.0.0.1'; kill %1` | expect: `200`, then `1` | cwd: `~/dev/active/repo-forest`
A4 [agent] cmd: `python3 server.py --json | python3 -c "import json,sys; n=[r['name'] for r in json.load(sys.stdin)]; print('socratink' in n and 'socratink-brain' in n)"` | expect: `True` (nested repo appears as its own tree) | cwd: `~/dev/active/repo-forest`
A5 [user] Open the page in a browser: 15 trees on an isometric board; a repo with uncommitted changes looks visibly different from a clean one; extra branches are visible. Judged by you by eye (a Playwright screenshot can support it later).

## Open questions
(none blocking)

## Evidence
E0 [evidence] Within `~/dev/active`: 15 repos, including 4 under a non-repo `skills/` folder and `socratink/socratink-brain`, a repo nested inside the `socratink` repo (`find`, 2026-09-28).
E1 [evidence] 50 git repos found within 5 levels of `~`: 37 under `~/dev` (15 under `dev/active`, 12 under `dev/archive`), 13 elsewhere. (`find ~ -maxdepth 5 -name .git`, 2026-09-28)
E2 [evidence] `gh auth status`: "Logged in to github.com account jon-devlapaz (keyring)". Node v26.8.1 and Python 3.13.12 are installed.
E3 [evidence] Groveboard already has an isometric grove-island hero and a forest design language: "the isometric grove island" (`groveboard/DESIGN.md:96,102`), with palette tokens (`grove-deep #143523`, `blight-red #c53929`, `harvest-gold #d49a30`, ...). A visual language for trees and "blight" already exists to reuse.
E4 [evidence] `groveboard/server.py` and `server.mjs` exist as a no-dependency static server pattern (`groveboard/README.md`).

## Dogfood log
2026-09-28 | repo-forest | ~8 turns (4 questions, 1 delegation) | ~15 min | acceptance checks needed an app name/path that did not exist yet (placeholders invented) | 0 edits after confirm so far
