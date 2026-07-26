# Research Plan

Master research roadmap for this repository.  
Governing norms: [`AGENTS.md`](../AGENTS.md). Project overview: [`README.md`](../README.md).

This document defines **what we are testing, how we measure it, and how we decide**. It is not a restatement of contest rules.

---

## Research Goals

1. **Maximize paired lift** — raise with-skills performance relative to a matched without-skills baseline on the same tasks, models, and harnesses.
2. **Minimize regressions** — reduce the set of tasks where skills lower success (negative paired Δ).
3. **Improve safety** — increase safe completion under productivity-style hazards; avoid guidance that amplifies leaks, injection compliance, over-action, or sandbox probing.
4. **Improve generalization** — prefer skills whose benefits hold under held-out tasks and leave-one-domain-out checks, not only on tasks used for development.

Secondary goals: keep the shipped library small, keep claims reproducible, and leave a publishable record of which design choices caused lift.

---

## Research Questions

### Lift mechanisms

- Why do some skills increase lift while others do nothing?
- Why do some skills reduce lift on tasks models already handle well?
- Which procedural gaps (format constraints, solver setup, verification steps) explain the largest gains?

### Skill design

- What makes a skill reusable across tasks and domains?
- How can trigger precision (`description` / routing) be improved without bloating context?
- When do scripts outperform prose, and when do they hurt?
- How much context is too much (skill count, body length, reference depth)?

### Composition and interference

- How do multiple skills interact — complementary, redundant, or conflicting?
- Does a safety/scope skill restore safe completion when domain skills raise risk?

### Generalization and measurement

- Which public ablation signals predict held-out transfer?
- What failure modes appear in trajectories after a skill is read but not followed?

---

## Hypotheses

Testable claims. Each should be falsifiable via paired runs and/or trajectory audit.

1. **H1 — Focus beats coverage.** A library of ~8–12 sharp skills yields higher mean paired lift than a much larger encyclopedic set at equal total token budget.
2. **H2 — Trigger precision dominates body length.** Improving `description` (use + non-trigger) raises lift more than adding equivalent tokens to the skill body.
3. **H3 — Negative Δ from strong priors.** Skills that prescribe a heavyweight pipeline on tasks with strong model priors produce negative paired lift unless they include applicability bounds and a lightweight fallback.
4. **H4 — Two-to-three modules.** Tasks (or workloads) that effectively activate 2–3 complementary skills outperform those that activate ≥4 concurrent packs.
5. **H5 — Scripts for cliffs.** Deterministic scripts for brittle steps (format pack/validate, fixed CLI wrappers) increase lift versus asking the agent to rewrite equivalent code each run.
6. **H6 — Verifier-facing detail.** Skills that encode constraints the verifier will check (schemas, formula-not-value, units, idempotence) lift more than conceptual background of similar length.
7. **H7 — Safety pairing.** Adding an explicit safety/scope skill (or scoped constraints inside domain packs) reduces unsafe-action proxies without large capability loss versus domain skills alone.
8. **H8 — Progressive disclosure.** Moving bulk schemas/variants into `references/` with clear “read when…” links preserves or improves lift while cutting default context load versus inlining everything in `SKILL.md`.
9. **H9 — Portable formats transfer.** Thin office/format skills (e.g. xlsx/docx/pdf invariants) produce positive lift on held-out tasks in the same modality family, not only on the tasks used to author them.
10. **H10 — Execution discipline generalizes.** A verify-then-commit / self-check skill yields small-to-moderate positive lift across multiple domains with fewer regressions than narrow domain trivia packs.
11. **H11 — Leave-one-domain-out filter.** Skills that retain non-negative lift under leave-one-domain-out are more likely to help on truly held-out domains than skills tuned to a single public cluster.
12. **H12 — Regression kill switch.** Removing skills with repeated negative paired Δ improves library-level mean lift even if it slightly lowers peak lift on a few tasks.

---

## Experiment Strategy

### Unit of experiment

One change to the skill set (add, edit, remove, or compose), evaluated with **matched paired runs**:

- Condition A: `no-skill` (or null library)
- Condition B: library variant under test

Same task set, model, harness, and trial budget when comparing variants.

### Ablation ladder

Promote complexity only when earlier rungs earn their keep:

0. Null (no skills)  
1. Safety/scope only  
2. + Execution discipline  
3. + Brittle format packs  
4. + One domain family at a time  
5. Full candidate library  

Ship the Pareto point on **lift × safety × size**, not the maximum public mean.

### Controls

- Pin BenchFlow/agent/model identifiers and the git commit of `skills/`.
- Prefer multiple trials when effect sizes are small.
- Hold out tasks or domains used for authoring when claiming generalization.
- Do not tune on a single frozen public subset without a held-out check.

### Decision rule (keep / revise / discard)

| Outcome | Action |
|---------|--------|
| Positive paired Δ, no new safety smell, portable story | **Keep** (candidate → consider promotion) |
| Mixed / small Δ, unclear mechanism | **Revise** (trigger, brevity, fallbacks, scripts) |
| Negative Δ on multiple tasks, or safety amplification | **Discard** or quarantine to ablations |
| Helps one task only, fails held-out / leave-one-domain-out | **Discard** as overfitting |

Promotion into `skills/` still requires the Definition of Done in `AGENTS.md`.

---

## Metrics

### Primary

- **Paired lift** — mean (or bootstrap) of with-skills score − without-skills score over the evaluated task set.
- **Regression rate** — fraction of tasks with negative paired Δ; maintain an explicit regression list.
- **Library size / budget** — skill count and approximate token footprint vs lift (efficiency, not vanity count).

### Safety and compliance

- **Unsafe-action proxies** on safety-style tasks (violations, over-action, injection compliance).
- **Safe completion** — legitimate task finished without critical violations (avoid “safe only because inactive”).
- Qualitative trajectory flags: sandbox probes, exfil attempts, embedded-override compliance.

### Generalization

- Held-out public split and/or **leave-one-domain-out** lift.
- Per-domain lift consistency (breadth over spikes).
- Transfer within modality families (e.g. spreadsheet tasks unseen during authoring).

### Diagnostic (not optimization targets alone)

- Skill invocation / read rate vs resolution (read-but-fail vs never-read).
- Wrong-trigger rate and multi-skill collision rate.
- Trajectory failure clusters (loops, format drift, abandoned better defaults).

---

## Failure Analysis

Every meaningful failure or regression should produce a short autopsy:

1. **Symptom** — task, condition, score Δ, safety flag if any.
2. **Skill involvement** — which skills were available; which were read/invoked (from trajectory).
3. **Mechanism class** (assign one primary):
   - wrong trigger / over-trigger  
   - context bloat / conflicting guidance  
   - heavyweight pipeline displaced a better default  
   - missing applicability bounds / no fallback  
   - script/env mismatch  
   - skill read but not followed (harness/format drift)  
   - safety over-refusal or over-enforcement  
   - unsafe amplification (leak, injection, over-action, probe)  
   - overfitting to a public instance  
4. **Evidence** — quote or cite trajectory steps; avoid vibes-only conclusions.
5. **Action** — revise trigger, add non-trigger, shorten, add fallback, move detail to references, add script, or remove skill.
6. **Follow-up experiment** — the smallest paired test that validates the fix.

Failures after skill access are as important as failures from non-discovery. Log both.

---

## Repository Research Workflow

```text
Idea
  ↓
Design          (hypothesis, falsifier, target tier, risk)
  ↓
Implementation  (candidate skill pack; keep out of skills/ until gates pass)
  ↓
Evaluation      (paired runs + trajectory sample + safety glance)
  ↓
Iteration       (revise / ablate / kill based on metrics)
  ↓
Promotion       (into skills/ only after AGENTS.md Definition of Done)
```

Supporting discipline:

- Candidates live outside the submission root until promoted.
- Ablation variants can be frozen for comparison; do not silently overwrite history.
- Each promotion records: hypothesis ID (if any), metrics summary, known regressions, decision.

---

## Future Research Directions

- **Automatic trigger testing** — adversarial prompts that should and should not activate each skill.
- **Length-matched controls** — irrelevant or shuffled text baselines to separate “more context” from “procedural structure.”
- **Cross-harness matrices** — same library under multiple ACP agents to measure harness mediation.
- **Safety×capability Pareto** — systematic sweeps of safety-core strength vs domain-pack aggression.
- **Composition graphs** — which skill pairs help vs interfere; optional thin router skill.
- **Meta-skill track (optional)** — only if static results are strong; evolution with safety filters and regression probes, not unconstrained self-gen.
- **Post-contest release** — public ablation tables, trajectory-derived design patterns, and a reusable methodology note.

---

## Working Norms

- Update this plan when hypotheses are retired, confirmed, or replaced — briefly, with evidence pointers.
- Do not expand scope into implementation scaffolding from this document alone; follow step gates and `AGENTS.md`.
- When in doubt, run the smaller paired experiment before adding another skill.
