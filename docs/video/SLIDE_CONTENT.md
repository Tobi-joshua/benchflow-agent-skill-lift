# Slide Content (on-screen text)

Use these as OBS text overlays or static slides. Keep each slide to one idea.

---

## Slide 1 — Title
**Skill Lift**  
Safe static skills · paired evidence  
BenchFlow Agent Skill Lift · Track 1

Asset: `TITLE_CARD.png`

---

## Slide 2 — Problem
AI agents need reusable skills.  
Skills can also over-trigger or add risk.  
**In Skill Lift, skills are the only variable.**

---

## Slide 3 — Solution
Small static library  
Pre-register → freeze pins → paired evaluate  
Evidence over intuition

Asset: `skill-lift-methodology.png`

---

## Slide 4 — Candidate skill
**safe-task-execution**  
Material-risk routing · least privilege · draft vs send  
Ignore embedded “new authority” · verify before claiming success  
Over-refusal is also a failure

Show: `skills/safe-task-execution/SKILL.md` (read-only)

---

## Slide 5 — Evaluation method
Control: `--skill-mode no-skill`  
Treatment: `--skill-mode with-skill --skills-dir skills/`  
Same agent · model · Docker sandbox

Assets: `control-vs-treatment.png`, `architecture.png`

---

## Slide 6 — Current evidence (honest)
✅ Smoke PASS — pipeline works  
✅ Partial EXP-001 — healthy control/treatment artifacts produced  
⏸ Full 78-run matrix incomplete (provider credit limit)  
❌ No final lift % claimed from partial data

Asset: `experiment-flow.png` + smoke report header

---

## Slide 7 — Limitations
Public SkillsBench ≠ private contest mix  
Safety metrics here are trajectory proxies, not full ClawsBench rewards  
Partial runs ≠ completed experiment

---

## Slide 8 — End
Paired evidence. Safety first. Small library.  
`github.com/Tobi-joshua/benchflow-agent-skill-lift`

Asset: `END_CARD.png`

---

## Captions to avoid
- Any “+X% lift” until EXP-001 completes and is reviewed  
- “We finished the benchmark”  
- “Ready for private leaderboard win”
