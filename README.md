# BenchFlow Agent Skill Lift

A research repository for designing, ablating, and submitting **safe, generalizable agent skills** for the [BenchFlow Agent Skill Lift](https://www.kaggle.com/competitions/skill-lift) competition.

We treat the contest as a measurement instrument: the same models, harness, and private tasks for everyone — **skills are the only variable**. Our goal is a small library that produces real paired lift on held-out work, without safety regressions.

Governance and contributor norms live in [`AGENTS.md`](./AGENTS.md).

---

## Motivation

Agent skills — modular folders of instructions, scripts, and references — are widely shipped and weakly measured. When an agent succeeds, it is often unclear whether the model or the skill deserved credit. SkillsBench shows that curated skills can raise pass rates substantially on average, yet individual skills can also regress tasks or add nothing. Self-authored skills are frequently flat or negative. ClawsBench further shows that domain skills can improve capability while increasing unsafe actions unless explicitly constrained.

Most teams are still guessing. This repository exists to replace guesswork with **paired, safety-aware evidence**.

---

## What is BenchFlow Agent Skill Lift?

[Skill Lift](https://www.kaggle.com/competitions/skill-lift) is a Kaggle competition hosted by BenchFlow. Participants submit a skill set; organizers hold fixed a panel of frontier models, the BenchFlow harness, and a private task mix. Each task is run with and without the submission. **Lift** is the paired difference.

The private mix includes capability tasks in the SkillsBench style and safety tasks drawn from ClawsBench-style productivity environments. Critical unsafe behavior can drive a task score as low as −1.0. Public SkillsBench tasks support practice and ablation; final ranking uses the private set only.

Two tracks exist with separate leaderboards: **Static Skills** (a frozen library) and **Meta-Skills** (skills that author and refine other skills under an organizer-run evolution loop).

---

## Our Research Objective

Build the highest-performing **and safest** static skill library we can defend scientifically:

- Maximize mean paired lift on held-out tasks.
- Preserve compliance and safety under productivity hazard classes.
- Generalize beyond the public corpus (breadth across domains, not spikes on memorized tasks).
- Document which design choices caused lift — suitable for a rigorous competition writeup and for reuse after the contest ends.

Primary focus: **Track 1 — Static Skills**. Meta-Skills remain optional and secondary.

---

## Research Philosophy

Aligned with [`AGENTS.md`](./AGENTS.md):

1. **Paired evaluation is sacred** — claims require with-skills vs without-skills comparisons.
2. **Less is more** — a small set of sharp skills beats a large, noisy library.
3. **Procedures, not lookup tables** — class-level guidance that transfers to unseen domains.
4. **Safety constrains capability** — unsafe success is worse than careful completion.
5. **Evidence over intuition** — SkillsBench and ClawsBench as priors; our ablations as the update.
6. **Negative results are first-class** — regressions are recorded and used to kill bad skills.

---

## Repository Structure

High-level target layout (not all paths exist yet):

| Path | Role |
|------|------|
| [`AGENTS.md`](./AGENTS.md) | Constitution — principles and operating rules |
| `README.md` | Project overview (this file) |
| [`docs/`](./docs/) | Research plan and experiment protocol |
| [`scripts/`](./scripts/) | Validation, packaging, experiment records, lift metrics |
| `skills/` | Shipped skill library (submission root) |
| `eval/experiments/` | Pre-registration and result records |
| `tests/` | Tooling unit tests and fixtures |

The competition artifact is the contents of `skills/`, packaged via `scripts/package_submission.py`.

---

## Design Principles

- **Tiered library:** safety/scope → execution discipline → brittle formats → thin domain packs.
- **Progressive disclosure:** rich `description` for routing; lean `SKILL.md` body; details in `references/` on demand.
- **Harness portability:** skills must work under BenchFlow’s neutral mount and multi-agent discovery paths.
- **Promotion gates:** structure, non-leakage, ablation support, and safety review before a skill enters `skills/`.
- **Ablation ladder:** null → safety-only → workflow → formats → domains → full; ship the Pareto point on lift × safety × size.

---

## Development Roadmap

| Phase | Focus |
|-------|--------|
| **0 — Foundations** | Constitution (`AGENTS.md`), overview (`README.md`), research norms |
| **1 — Scaffolding** | Repository layout, packaging, skill hygiene tests |
| **2 — Core library** | Safety/scope and execution-discipline skills |
| **3 — Transfer packs** | High-reuse format and portable procedural skills |
| **4 — Measured domain thins** | Domain skills only where ablations show stable lift |
| **5 — Public evaluation** | Paired runs on SkillsBench; regression and safety review |
| **6 — Submission** | Frozen `skills/` zip, writeup, private-set readiness |
| **7 — Post-contest** | Publish ablations and reusable methodology |

Phases may overlap; promotion always requires evidence.

---

## Competition Strategy

- Enter **Static Skills** as the primary track.
- Keep the shipped library small and ablation-justified.
- Use the public corpus for development and leave-one-domain-out checks — not as a memorization target.
- Treat safety as a first-class score component, not a post-hoc filter.
- Write the Kaggle writeup as a research note: what lifted, what regressed, and why we expect private transfer.

Detailed operating rules for agents and contributors: [`AGENTS.md`](./AGENTS.md).

---

## Repository Status

**Foundation + evaluation tooling.** Governance docs and the first `scripts/` utilities are in place (validate, package, experiment pre-registration, paired-lift metrics). Candidate skills have not been authored yet.

This repository will grow only through deliberate, reviewable steps — not speculative scaffolding.

### Tooling quick start

```bash
python3 scripts/validate_skills.py
python3 scripts/new_experiment.py --slug example --hypothesis '...' --mechanism '...'
python3 scripts/compute_lift.py path/to/trials.json
python3 scripts/package_submission.py   # requires skills in skills/
python3 -m unittest discover -s tests -v
```

---

## How Contributors Can Help

We welcome contributions that improve **measured safe lift** or the research apparatus around it:

- Propose or refine portable skills with clear triggers and applicability bounds.
- Run and report paired ablations (including negative results).
- Improve leakage, budget, and safety hygiene checks.
- Strengthen docs once handbook files exist — without contradicting [`AGENTS.md`](./AGENTS.md).

Before contributing code or skills, read [`AGENTS.md`](./AGENTS.md). Prefer small PRs with a hypothesis and an evaluation story.

---

## Disclaimer

This is an independent research repository for participation in BenchFlow’s Agent Skill Lift competition. It is not affiliated with, endorsed by, or sponsored by BenchFlow, Kaggle, or the model providers used in evaluation, beyond use of their public benchmarks, documentation, and contest rules.

Evaluation outcomes depend on organizer-held private tasks, model panels, and harness versions outside our control. Public results do not guarantee private ranking. Nothing in this repository is permission to bypass sandbox, grader, or safety controls.

Competition rules, deadlines, and rubrics are defined by the organizers; participants are responsible for compliance.
