# Repository cleanup & history plan (checkpoint — no rewrite yet)

**Date:** 2026-07-27  
**Branch for this work:** `cursor/submission-assets-a21e`  
**Status:** Assets + docs updated in this phase. **Git history rewrite is NOT executed.**

---

## Current branch

```
cursor/submission-assets-a21e  (from main)
```

Operator machine may still be on `main` running EXP-001 — that is expected and independent.

## Recent commit list (`main`, newest first)

```
cecb0ca Merge branch 'cursor/exp001-brokenpipe-a21e'
b9a47f1 Ignore BrokenPipeError when dry-run output is piped to head.
45bf743 Merge branch 'cursor/exp-001-runner-a21e'
a2f66c7 Add resumable scored EXP-001 runner and runbook.
445f49e Merge branch 'cursor/safe-task-execution-skill-a21e'
b1f3f65 Note roadmap progress for candidate skill and smoke PASS.
7821a08 Add submission prep: Kaggle card, architecture, storyboard, writeup drafts.
928417e Record PASS local citation-check smoke pair with job artifacts.
… (earlier foundation + skill commits)
```

Default committer identity in this cloud agent environment:

- `user.name=Cursor Agent`
- `user.email=cursoragent@cursor.com`

---

## Files removed / replaced in this phase

| Action | Path |
|---|---|
| **Removed** | `docs/assets/architecture.svg` (replaced by PNG) |
| **Kept/verified** | `docs/assets/kaggle-card-560x280.png` (560×280) |
| **Added** | `docs/assets/architecture.png` |
| **Added** | `docs/assets/experiment-flow.png` |
| **Added** | `docs/assets/control-vs-treatment.png` |
| **Added** | `docs/assets/skill-lift-methodology.png` |
| **Added** | `docs/video/TITLE_CARD.png`, `END_CARD.png`, `DEMO_SCRIPT.md`, `SHOT_LIST.md` |

## Intentionally NOT deleted

- `skills/` and locked skill text
- `eval/configs/`, `eval/experiments/`
- `eval/runs/smoke/**` (research record)
- `eval/runs/exp-001/**` job outputs / progress (scored run in progress)
- Pre-registration JSON / hashes

## Local junk cleanup (working tree only)

Already gitignored (`__pycache__/`, `.env`, `skillsbench/`). Safe to delete locally:

```bash
find . -type d -name '__pycache__' -prune -exec rm -rf {} +
rm -f .env .envrc
# do NOT rm -rf eval/runs/exp-001 or smoke
```

## Proposed future history options (await confirmation)

### Option A — recommended for competition (default)

- Keep existing history.
- Continue final commits under your identity:

```bash
git config user.name "Tobi Joshua Samuel"
git config user.email "YOUR_EMAIL_HERE"
```

- No `filter-repo` / rebase.

### Option B — polished public squash (later)

- Create `release/kaggle` from final `main`.
- Squash to 1–3 narrative commits.
- Does **not** rewrite `main` history in place.

### Option C — rewrite all authors (discouraged now)

- `git filter-repo` mailmap rewrite of all commits.
- Changes every SHA; breaks PR links; high risk while EXP-001 is running.
- **Do not run until you explicitly confirm** after EXP-001 finishes and assets are finalized.

---

## Checkpoint question for you

Reply with one of:

1. **Keep history (Option A)** — only identity for future commits  
2. **Prepare squash branch later (Option B)** — after EXP-001  
3. **Rewrite authors (Option C)** — only with explicit go-ahead  

No history rewrite will be performed until you choose.
