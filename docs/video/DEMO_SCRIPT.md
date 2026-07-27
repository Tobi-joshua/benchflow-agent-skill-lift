# Demo Script (2–3 minutes)

**Working title:** Skill Lift — Measuring Safe Static Skills  
**Track:** BenchFlow Agent Skill Lift · Track 1 Static Skills  
**Target length:** 150–180 seconds  
**Visual system:** ink/slate + amber lift accent  
**Assets:** `TITLE_CARD.png`, `END_CARD.png`, `docs/assets/*.png`

## Voiceover script

**[0:00 TITLE]**  
Agent skills are widely shipped and weakly measured. In Skill Lift, models and harness stay fixed — skills are the only variable.

**[0:15 METHOD]**  
This repository is a measurement instrument. We pre-register hypotheses, freeze pins, then compare the same tasks with and without our library.

**[0:35 SKILL]**  
Our candidate is `safe-task-execution`: a thin scope and safety router. It activates on material risk — untrusted instructions, sensitive data, external send, destructive actions — not on ordinary local work.

**[0:55 CONTROL VS TREATMENT]**  
Control runs with `--skill-mode no-skill`. Treatment mounts only our repository `skills/` directory. Same agent, same model, same Docker sandbox.

**[1:15 PIPELINE]**  
Unscored smoke on `citation-check` proved the full path: Docker, Claude ACP, verifier rewards, and trial JSON. That was pipeline proof — not a lift claim.

**[1:40 EXPERIMENTS]**  
Scored EXP-001 measures cross-domain paired lift and safety proxies. EXP-002 is a negative control for over-triggering. We start with EXP-001 and inspect cost and logs before expanding.

**[2:10 PRINCIPLES]**  
Less is more. Procedures, not lookup tables. Safety constrains capability. Negative results are first-class.

**[2:30 CLOSE]**  
Skill Lift: paired evidence, safety first, small library.

## On-screen captions (burn-in optional)

| Time | Caption |
|---|---|
| 0:00 | Skill Lift |
| 0:15 | Skills are the variable |
| 0:35 | safe-task-execution |
| 0:55 | Control vs Treatment |
| 1:15 | Smoke PASS · unscored |
| 1:40 | EXP-001 → then EXP-002 |
| 2:30 | Paired evidence |

## Recording notes

- Do not show API keys, `.env`, or credential dialogs.
- Do not claim private-leaderboard wins.
- Say “unscored smoke” and “pre-registered” once each.
- Prefer quiet narration; minimal music bed if any.
