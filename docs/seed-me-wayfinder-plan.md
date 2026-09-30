# Plan: bringing wayfinder's ideas into seed-me (DRAFT r0, 2026-09-28)

Status: **proposal for the operator's review. Nothing here is implemented or approved.**
Source: the [wayfinder skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/wayfinder), read through fetched summaries (not the raw file line by line; `agents/openai.yaml` not opened), compared with seed-me and the UX review of the repo-triage session.

## Principle
Lean first. Each phase ships only what a dogfood run has shown to be needed, is small, and is proven by tests that fail before the change. Phases 2 and 3 wait for two more real sessions.

## What we take, and what we leave

| Wayfinder idea | Take? | Where it lands |
|---|---|---|
| Refer to everything by name, never a bare id | Yes | SKILL.md rule plus chat template; viewer already falls back to the question text |
| "Not yet specified" (fog of war) | Yes | "Still fuzzy" list |
| "Out of scope" as a first-class list | Yes | "Out of scope" list |
| One-line gist per decision, detail elsewhere | Already done | Settled list; still to do: collapse the repeated "All concerns" list |
| Human-in-the-loop: the agent never stands in for the human's side | Partly | Show accepted vs chosen counts (done in viewer); confirm step names the riskiest items |
| Prototype tickets (rough artifact to ground a decision) | Later | Optional step for visual/UX ideas |
| "No fog means no map" | Yes, as guidance | Batch low-stakes decisions as assumptions the user can veto |
| Research subagents in parallel (AFK) | Already planned | The earlier batch-probe brief (`seed-me-graph-investigate`) |
| Tracker-hosted map, claiming tickets, one ticket per session | No | Ours is local and single-user; revisit only if this becomes multi-user |

## Phases

### Phase 0 (done, uncommitted in the worktree)
Page fixes from the UX review: "Your turn / Ready for review" state, "you accepted the agent's suggestion" wording with an accepted-vs-chosen count, full answers with a toggle, facts as their own group so counts agree, plainer status text.

### Phase 1: mostly prose, one small schema addition
1. **Names, not ids.** SKILL.md rule: refer to each question by its title, never "Q3" or a node id, in chat and in the pre-intent. Replace "Decision 1 of 3 ready (2 parked)" with "Question 1 (2 more waiting after this)" in the Step 3 template.
2. **Assumptions with a veto** (decided: a separate `assumed` list, see Decision log; this item needs the small schema addition, so it is not prose-only). Use the rule seed-me already has (Step 2: ask only when two reasonable answers change implementation, risk, cost, reversibility, or product behavior, and `ledger-transitions.md` section 1: defaults are labeled assumptions, never user answers). Make it operational: the agent lists low-consequence defaults once as "I'll assume these unless you object" instead of one question each. Evidence for the change: in the repo-triage session all 8 decisions were accepted with an arrow.
3. **Show the alternative.** In each question, give two options with a one-line tradeoff, say what changes if the user picks the other, and how hard it is to undo. Flag invented numbers ("my number, change it?").
4. **Additive pre-intent changes** (decided: option B). Keep every current section. Add a five-line "You are confirming" box at the top (goal, what gets built, what does not, what you accepted unchanged, what is still unknown, plus any past decision this reverses), a plain-English line above each acceptance check with the exact command kept underneath, and a confirm request that names the three riskiest items.
5. **Rename the artifact to `seed-contract.md`** (interpretation of the operator's instruction "rename it to call it seed-contract.md"; correct me if "it" meant something else). Scope: the file seed-me saves, and the term "pre-intent" in SKILL.md and its references, from now on. Compatibility: existing `pre-intent.md` files stay valid and are not renamed; if a repo already has an unrelated `pre-intent.md`, seed-me writes `seed-contract.md` beside it. Historical receipts (for example `ai-native-sdlc/pre-intent.md`) are left alone. The chain contract's wording is updated to "seed contract" in the same change.
- **Verification:** contract tests assert the new wording (box, plain-English checks, names-not-ids, assumed list) and that the saved filename is `seed-contract.md`; an old-session compatibility test; one dogfood session.
- **Size:** about 60 lines of prose plus the `assumed` list (about 60 lines of code and tests). **Risk:** low to medium (the rename touches several files).

### Phase 2: "map margins" (needs a small schema addition)
Add two optional top-level lists to the ledger, validated by `session.py` and shown by the viewer and pre-intent:
- `out_of_scope`: entries of `{text, source}`; source must quote the user or cite evidence.
- `fuzzy` ("still fuzzy"): entries of `{text, note}`; a question too dim to state yet. It graduates by being removed and replaced by a real decision node.
- **Touches:** `session.py` (`STATE_FIELDS`, `validate`), `ledger-transitions.md`, `ledger-view.html`, SKILL.md, tests.
- **Verification:** validator tests (bad shapes rejected), an old-session compatibility test (missing lists load fine), a browser test for both lists, and a regression test for the old-schema round trip.
- **Size:** about 120 lines plus tests. **Risk:** medium (schema). **Gate:** do this only after two more sessions show fuzzy or out-of-scope items being lost. Otherwise keep them as prose sections.

### Phase 3 (later): fold the sections (a contract change)
From the UX review: the 12-section document is too long to review, and the checks are unreadable to a person.
- Fold Affected/Constraints/Deferred into "Boundaries"; fold Corrected premise/Evidence/Risks into "What we do not know yet"; drop "Owners and next steps" when there are no blockers.
- **Gate:** only if a reader still finds the document too long once the "You are confirming" box exists. **Touches:** SKILL.md contract section, contract tests, the chain contract's mapping table.

### Phase 4: prototype and human-in-the-loop rules (later)
- Optional "sketch it" step for visual or UX ideas: a throwaway mock the user reacts to before delegating a visual decision.
- If every decision in a session is an accepted suggestion, the pre-intent says so at the top and the confirm step asks for one custom answer.

## Dogfood gate and measures
Before Phases 2 and 3, run two real sessions: one ambiguous idea, one that starts from a machine finding (Stage 6 style). Log per session: turns, minutes, decisions asked, accepted as suggested vs changed, questions the user found unclear, edits after confirmation. If more than about 70% of questions are arrowed through, batching assumptions (Phase 1, item 2) should be the default.

## Decision log
- **2026-09-28, chosen by the operator ("A"):** an "I'll assume this unless you object" default is recorded in a separate `assumed` list (entries: wording and why it is a safe default). If the user objects it becomes a real decision node. It is not a new `authority` value, so `authority` keeps meaning who decided. Cap: about five assumptions per turn (agent's number, changeable).

- **2026-09-28, chosen by the operator ("B"):** ship the `assumed` list first. "Out of scope" and "Still fuzzy" stay plain prose sections in the pre-intent until a real session loses one; revisit after two more sessions (agent's number).

- **2026-09-28, chosen by the operator ("B"):** additive pre-intent changes now (box, plain-English checks, named riskiest items); folding sections is Phase 3 and waits. **Also:** rename the artifact to `seed-contract.md` (scope as written in Phase 1, item 5).

## Open decisions for the operator
None. Waiting for the go-ahead to build Phase 1.

## What is not verified
Wayfinder details come from fetched summaries. The repo-triage session is a single sample. No phase has been built.

## Research-driven changes (2026-09-28)
A critique grounded in research on clarifying questions, over-reliance on AI recommendations, and spec-driven tools led to two changes, both prose plus one reference file:
- **Instinct first for hard-to-undo questions** (a cognitive forcing function): show the question and evidence, ask for the user's instinct, and publish the node without a recommendation until they answer or say "show me". Every question also states the strongest case against the suggestion. Cheap and moderate questions still show everything at once.
- **Size gate:** the agent proposes Lean or Full. Lean is one editable `seed-contract.md` with no session, ledger, or viewer (`references/lean-path.md`); Full is the ledger flow.
Still open from the critique: probe for unstated requirements with concrete examples, let questions arrive later when the work hits a fork, close the loop with a minimal downstream stage plus outcome measures, and a teach-back at confirmation.
