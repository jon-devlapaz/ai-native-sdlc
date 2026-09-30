# Seed contract (SIMULATED): what to do with ~/home-cleanup-backup, Karpathy-engram operator
**Status: `simulated — not confirmed by a human`.** Revision r1, 2026-09-29. Operator: an agent playing **engram: andrej-karpathy (a simulation of his public record, not the person)**. Its words are inferences from that material, never statements by him. No person made these decisions, and the one that only a person can make is still open (below). This authorizes nothing: no deletion, no move, no export.

## You are confirming (if the owner adopts this)
- **Goal:** decide, folder by folder, what in `~/home-cleanup-backup` (1.9 GB) to keep, move, or delete, with one reason each. Nothing that exists nowhere else is marked for deletion.
- **What gets done:** nothing by this session. It produces a decision list; every action is the owner's.
- **What does not:** deleting anything on a same-disk copy alone; deleting the seven trial installers before the owner checks them; deleting anything, including Paper, before the vault is backed up.
- **Simulated answers: 8 (7 decisions plus confirming the goal), human answers: 0.** The operator volunteered its own rule on 3 (protect unique work first; folder names are not evidence; ask the owner before exporting the notes). It accepted my option on 4 (the installer split, the document split, the deletion rule, the durable-copy definition).
- **Still unknown:** whether the vault's notes may go on GitHub. Only the owner can say.

## Decisions (all authority `simulated`)
| Decision | Answer |
|---|---|
| Order | Protect what exists nowhere else first; only then decide the rest. |
| Names | A folder's name ("trash", "redundant") is not evidence. |
| Installers (8, 1,440 MB) | Paper (141 MB, already installed): delete, but only after the vault is backed up (nothing is cleaned up first). The other seven (1,299 MB): the owner checks whether each is re-downloadable and still wanted first. |
| Trash-folder documents (107) | 72 with an identical copy elsewhere: delete, but see "durable copy" below. 35 others (34 unique + 1 whose only copy is in another backup folder): move to one durable folder; the owner reviews later. |
| Deletion rule | A folder may be marked delete only if every file has a durable identical copy and every git repo in it is clean and fully on a remote; otherwise move for review. |
| Durable copy | A same-disk copy does not count. Durable means a git repo with a remote, or an independent backup. So the 72 duplicates and the fully duplicated personal-documents folder are "delete after the owner confirms an independent copy". |
| Protecting the vault | Ask the owner first whether the notes may go on GitHub. If yes, a private repo; if not, a git bundle plus a copy of the uncommitted files. Commit or set aside the 45 uncommitted files first. No cleanup until the vault is independently backed up. |

**Totals, from code:** delete about 147 MB (conditional except Paper 141 MB); owner verifies 1,299 MB; move for review about 505 MB.

## Knowledge map
- **What we know, with proof:**
  - The vault (`desktop/research-to-organize/socratink-research-vault-redundant-2026-08-12`) has no remote, 25 commits found in no other repo on the machine, and 45 uncommitted files; observed 2026-09-29; re-check before any export.
  - The second "no-remote repo" (`ChatGPT/socratink`) has **0 commits** and one `.DS_Store`; it needs no protection. Earlier statements that two repos needed protecting were wrong.
  - Eight installers: only Paper matches an installed app (a fuzzy match). Observed 2026-09-29.
  - 72 of the trash folder's 107 documents have an identical copy elsewhere on the same disk; 34 have none; 1 only in another backup folder. Observed 2026-09-29; re-check if ~/dev is reorganized.
  - There is no Time Machine destination, and ~/Documents and ~/Desktop show no cloud sync. Observed 2026-09-29; re-check if a backup is set up.
  - Space is not pressing (27% used).
- **What we know we don't know:**
  - Whether the vault's notes may go on GitHub. Owner: the human owner. Find out: read the notes.
  - Whether the seven installers are still downloadable. Owner: the human owner.
  - Whether the 72 duplicates' other copies sit inside git repos with a remote. Owner: the interviewer, cheap to check later.
- **What is true but nobody has read:** the contents of the 34 unique documents, the 11,384 unique files in the desktop copy, and the vault's notes.
- **What could surprise us:**
  Probe: pre-mortem — answer: the "durable" copies turn out to be on the same disk with no independent backup — changed: durable now needs a git remote or an independent backup (NOT independent of Probe 3: asked in the same message)
  Probe: counter-example — answer: the owner later cleans the folder that holds the "safe" copies and both vanish — changed: nothing beyond the durable-copy rule (restates Probe 3)
  Probe: outside view — answer: nobody asked whether any of this is independently backed up; it is not (no Time Machine, no cloud sync) — changed: the same-disk-copy rule, and the 72 deletions became conditional
  Where we did not look: cloud storage, external drives, other machines; near-duplicate files; files over 50 MB; ~/Library; the contents of any note or document; whether the duplicate copies sit in remote-backed repos.
  We would know we were wrong if: the owner tries to restore a file marked "delete" and no copy exists; or the vault turns out to hold notes that are on no other machine after it was "protected".

## Acceptance checks (commands exist today; none has been run by an owner)
1. **The vault has nothing that exists only on this laptop.** cmd: `git -C ~/home-cleanup-backup/desktop/research-to-organize/socratink-research-vault-redundant-2026-08-12 log --branches --not --remotes --oneline | wc -l` | expect: `0` (today: `25`, so it fails until a remote exists and is pushed) | cwd: any
2. **The vault has no uncommitted work left behind.** cmd: `git -C ~/home-cleanup-backup/desktop/research-to-organize/socratink-research-vault-redundant-2026-08-12 --no-optional-locks status --porcelain | wc -l` | expect: `0` (today: `45`) | cwd: any
3. **The owner confirms an independent copy exists for every file on the delete list.** **Human-only: no tool exists yet, and it has not been done.**

## Evidence (read-only, 2026-09-29)
Folder sizes and dates; per-folder duplicate counts by sha256 against about 411,000 other files; `tmutil destinationinfo`; git state per repo; the engram files (the operator's "Don't be a hero" label is in its material; its "documented junk pattern" label for installers is not).

## Teach-back (by the simulated operator, so weak evidence)
The operator restated the plan in one paragraph. It **found one real mismatch:** the contract said "delete Paper right away" but also "no cleanup until the vault is backed up"; it read Paper as coming after protection, and the contract now says so. Otherwise its paragraph closely repeats the contract text it was shown, so it proves little. It did not name the one decision it would change first. A human's own-words teach-back is still owed.

## Riskiest items
1. The vault decision is deferred to a human, and until it is made nothing here is safe to act on.
2. The operator's summaries miscounted twice; every number above comes from code.
3. Probes 1 and 2 are not independent evidence.

## Adoption
The owner reads this and answers the open question; then starts their own session or lean file with their own confirmation. The simulated session's operator cannot be changed to human.
