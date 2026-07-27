# Screen Recording Guide (OBS / local)

Record a **2–3 minute** Kaggle demo locally. This environment cannot produce the final MP4 for you.

## Install (Ubuntu)

```bash
sudo apt update
sudo apt install -y obs-studio
```

Optional: `sudo apt install -y simplescreenrecorder` as a backup.

## OBS setup (once)

1. Open OBS → **Scenes** → create `SkillLift-Demo`.
2. **Sources** (add in order; hide/show per shot):
   - Image: `docs/video/TITLE_CARD.png`
   - Image: `docs/assets/skill-lift-methodology.png`
   - Image: `docs/assets/architecture.png`
   - Image: `docs/assets/control-vs-treatment.png`
   - Image: `docs/assets/experiment-flow.png`
   - Image: `docs/video/END_CARD.png`
   - Display/Window Capture: terminal + editor (for live repo shots)
3. **Settings → Output:** MP4, 1920×1080, 30 fps, quality balanced.
4. Mic: test level; leave headroom so narration is clear.

## Timed recording checklist

| Time | Show | Say / do |
|---|---|---|
| 0:00 | TITLE_CARD | Start narration from `DEMO_NARRATION.md` |
| 0:10 | methodology.png or speak over title | Problem: skills help and can over-trigger |
| 0:30 | Editor: `skills/safe-task-execution/SKILL.md` | Scroll description + operating procedure only (**read-only**) |
| 1:00 | control-vs-treatment.png | Explain no-skill vs with-skill mounts |
| 1:20 | Terminal (optional): `python3 scripts/run_exp001.py --help` or dry-run head | Show runner exists; **do not** paste API keys |
| 1:40 | `eval/runs/smoke/SMOKE_REPORT.md` header table | Smoke PASS = pipeline proof |
| 2:00 | `eval/runs/exp-001/progress.jsonl` or RUN_LOG (partial) | “Partial scored runs; full matrix incomplete” |
| 2:20 | END_CARD | Repo URL; stop recording |

## Safety on camera

- Never show `ANTHROPIC_API_KEY`, `.env`, or browser billing pages.
- Never open credential files.
- If a terminal history might contain secrets, use a fresh shell.

## Export & place

1. Stop recording → save as `docs/video/skill-lift-demo-draft.mp4` (gitignored).
2. Watch once against `DEMO_NARRATION.md`.
3. Upload the final file to Kaggle / unlisted YouTube; paste the link in the writeup.

## If credits stop EXP-001 mid-run

That is OK for the video. Say:

> We built and validated an evaluation pipeline using BenchFlow. Initial smoke and partial execution confirm the system works; full benchmark evaluation is ongoing.

Do **not** invent completion counts or lift metrics.
