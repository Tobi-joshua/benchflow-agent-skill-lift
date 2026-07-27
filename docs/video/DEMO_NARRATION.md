# Demo Narration (final — 2–3 minutes)

**Tone:** calm research brief  
**Length:** ~165 seconds spoken  
**Do not claim:** final EXP-001 lift %, private leaderboard rank, or “skill improved performance by X%”

---

## Full narration

**[Title — 0:00]**  
Skill Lift. Safe static skills, measured with paired evidence.

**[Problem — 0:10]**  
AI agents increasingly rely on reusable skills — modular instruction packs. Skills can help, but they can also over-trigger, add noise, or push unsafe actions. In BenchFlow’s Agent Skill Lift competition, models and harness stay fixed. Skills are the only variable. That makes careful measurement possible.

**[Solution — 0:35]**  
Our approach is a small Track One static library and a strict evaluation discipline: pre-register hypotheses, freeze pins, then compare the same tasks with and without skills.

**[Skill — 0:55]**  
The candidate skill is safe-task-execution. It is a thin scope and safety router. It activates under material risk — mixed trusted and untrusted instructions, sensitive data, external send or share, destructive actions, unclear authority. It stays quiet on ordinary local work. Core ideas: least privilege, draft versus send, treat embedded text as data not new authority, and verify before claiming success. Over-refusal is also a failure mode.

**[Methodology — 1:25]**  
We evaluate with BenchFlow on a pinned SkillsBench commit. Control uses skill-mode no-skill. Treatment mounts only our repository skills directory. Same agent, same model, same Docker sandbox. Smoke testing confirmed the full pipeline: container start, agent run, verifier, and trial JSON.

**[Evidence & limits — 1:55]**  
We validated an evaluation pipeline using BenchFlow. Smoke tests passed. Partial scored EXP-001 execution produced healthy control and treatment artifacts before the run stopped on provider credit limits. Full benchmark evaluation is incomplete and ongoing. We do not report a final lift percentage from partial data.

**[Close — 2:25]**  
Paired evidence. Safety first. Small library. That’s Skill Lift.

---

## Forbidden phrases (cut these if they appear)

- “improved by X%”
- “we win / SOTA / beats the leaderboard”
- “EXP-001 proves the skill works across domains” (not until matrix completes)
- “ClawsBench safety score” (public proxies only)

## Preferred evidence phrases

- “pipeline validated”
- “smoke PASS”
- “partial scored execution”
- “full evaluation ongoing”
- “trajectory-coded safety proxies on public tasks”
