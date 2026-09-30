# Lean pre-intent (experiment r0, 2026-09-28)

One living markdown file, edited by the user and the agent. No server, no ledger, no enforcement.
Rigor lives downstream (Stage 1 validator, gates). Here the rule is: typed but soft.
Location: `runs/<slug>/pre-intent.md`. History: git (or plain file copies) if wanted.

## Conventions (the only rules)
1. Every item has an id (`G`, `D1`, `C1`, `A1`, `Q1`, `E1`) and an author tag: `[user]`, `[agent]`, `[evidence]`.
2. The agent never writes a decision as `[user]` unless it quotes the user's words or cites the chat turn.
   Agent-originated facts are `[evidence]` with a `file:line` quote. Everything else the agent writes is `[agent]` (a proposal).
3. Proposed changes to existing text go in a blockquote under the item, never in the item body:
   `> agent proposes (YYYY-MM-DD): <new wording> — why: <reason>`
   The user accepts by moving the wording into the item and deleting the blockquote; rejects by deleting it.
4. Human edits are never overwritten. The agent responds to edits only when asked (chat), never on its own.
5. One question at a time. The agent marks the current one `NEXT`.
6. Accepting wording is not approval to implement. Confirmation is the user changing `status:` to `confirmed`.

## Template

```markdown
# Pre-intent: <title>
status: draft | confirmed        revision: 1        date: YYYY-MM-DD

## Now  (agent keeps these four lines current)
- Trying to achieve: ...
- Settled: ... (ids)
- Uncertain: ... (ids)
- Needs you next: ... (id)

## Goal
G [user] <one sentence>

## Decisions
D1 [user|delegated|evidence] <decision> — source: <user's words / chat turn / file:line>

## Constraints and exclusions
C1 [user] ...

## Acceptance checks
A1 [user|agent] cmd: `<exact command>` | expect: <expected output> | cwd: <path>

## Open questions
Q1 NEXT [agent] <question> — owner: <who decides> — why it matters: ...
> agent proposes (date): ...

## Evidence
E1 [evidence] "<quoted line>" (<path>:<line>)
```

## What we are testing
- Does this produce a usable `pre-intent.md` with much less machinery than seed-me?
- Can you return after a break and read `Now` to know where things stand?
- Later: do the Stage 1 validator's warnings and your post-acceptance edits look better or worse than with the heavy version?

## Dogfood log (append one line per run)
`date | slug | turns | minutes | things that were awkward | edits after confirm`
