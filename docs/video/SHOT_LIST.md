# Demo Shot List + Recording Plan

**Total:** ~2:45  
**Resolution:** 1920×1080  
**Title/end cards:** `docs/video/TITLE_CARD.png`, `docs/video/END_CARD.png`

## Shot list

| # | Time | Visual source | Action |
|---|---|---|---|
| 1 | 0:00–0:12 | `TITLE_CARD.png` | Hold full-bleed; fade in title |
| 2 | 0:12–0:28 | `docs/assets/skill-lift-methodology.png` | Slow push-in |
| 3 | 0:28–0:48 | Terminal or editor: `skills/safe-task-execution/SKILL.md` | Highlight description triggers (no edits) |
| 4 | 0:48–1:08 | `docs/assets/control-vs-treatment.png` | Hold; optional cursor to left/right labels |
| 5 | 1:08–1:28 | `docs/assets/architecture.png` | Hold |
| 6 | 1:28–1:48 | `docs/assets/experiment-flow.png` | Hold |
| 7 | 1:48–2:10 | Smoke report snippet / `eval/runs/smoke/SMOKE_REPORT.md` header | Show PASS table only |
| 8 | 2:10–2:30 | README status table or EXP cards | Emphasize EXP-001 in progress / EXP-002 queued |
| 9 | 2:30–2:45 | `END_CARD.png` | Hold repo URL |

## Executable recording plan (no video tool in CI)

1. Install OBS Studio (or QuickTime screen recording).
2. Create a scene collection named `skill-lift-demo`.
3. Add image sources for each PNG above; order matches shot list.
4. Record narration separately (Audacity) using `DEMO_SCRIPT.md`, then sync.
5. Export H.264 MP4, 1920×1080, ≤50 Mbps, filename `docs/video/skill-lift-demo-draft.mp4` (gitignored until final).
6. Upload to Kaggle writeup / unlisted YouTube as needed.

## Checklist

- [ ] Title card readable at 100% and 50% scale
- [ ] No secrets on screen
- [ ] Smoke clearly labeled unscored
- [ ] End card URL correct
- [ ] Captions match script claims

## Out of scope

- Auto-generating final MP4 in this repo agent environment (no dedicated video compositor). Assets + plan are the deliverable until local recording.
