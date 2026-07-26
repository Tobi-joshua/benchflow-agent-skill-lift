# Demo Video Storyboard (2–3 minutes)

**Working title:** *Skill Lift — Measuring Safe Static Skills*  
**Length target:** 150–180 seconds  
**Tone:** research brief, not product hype  
**Visual base:** ink/slate lab aesthetic + amber “lift” accent (match Kaggle card)

Do **not** claim private-leaderboard results. Smoke is pipeline proof only; scored EXP-001/002 are still pending.

---

## Shot list

| # | Time | Visual | Voiceover / on-screen text |
|---|---|---|---|
| 1 | 0:00–0:12 | Full-bleed Kaggle card (`docs/assets/kaggle-card-560x280.png`) | “Agent skills are widely shipped and weakly measured. Skill Lift fixes the models and harness — skills are the only variable.” |
| 2 | 0:12–0:28 | Architecture diagram: governance → skills → paired runs | “This repo is a research instrument: pre-register hypotheses, freeze pins, then measure paired with/without lift.” |
| 3 | 0:28–0:48 | Open `skills/safe-task-execution/SKILL.md`; highlight description triggers | “Candidate skill: `safe-task-execution` — a thin scope/safety router. Triggers on material risk, not on ordinary tool use.” |
| 4 | 0:48–1:05 | Split screen: `no-skill` vs `with-skill` CLI | “Same task, agent, model, sandbox. Control mounts nothing. Treatment mounts only our `skills/` directory.” |
| 5 | 1:05–1:35 | Smoke run footage or screenshots: Docker up → agent → verifier | “Unscored smoke on `citation-check` proved the full path: Docker, Claude ACP, verifier rewards, trial JSON.” |
| 6 | 1:35–1:55 | Table: control reward 0.0 / treatment 1.0; caption “pipeline, not claim” | “One smoke pair is not a lift result. It shows we can distinguish conditions cleanly before paying for scored runs.” |
| 7 | 1:55–2:20 | EXP-001 / EXP-002 cards: cross-domain + negative control | “Next: EXP-001 for cross-domain lift and safety proxies; EXP-002 as a negative control for over-triggering.” |
| 8 | 2:20–2:45 | Closing card: repo URL + Track 1 Static Skills | “Small library. Paired evidence. Safety as a first-class constraint — not a post-hoc filter.” |

---

## B-roll checklist

- [ ] `git status` on `cursor/safe-task-execution-skill-a21e`
- [ ] `python3 scripts/hash_library.py` showing locked hash
- [ ] `uv run bench --version` → 0.6.3
- [ ] Smoke `result.json` snippets (redact any secrets; none should be present)
- [ ] Architecture SVG / mermaid render

## Audio notes

- One narrator; calm pace; no background music bed that masks terms.
- Say “unscored smoke” and “pre-registered” explicitly once each.
- Avoid “we win” / “SOTA” language.

## Export targets

- Primary: 1080p landscape for Kaggle/writeup embed  
- Optional square crop of closing card for social  

## Out of scope for this video

- Full EXP-001/002 result claims  
- ClawsBench private tasks (not available publicly)  
- Any API keys, `.env`, or credential screens
