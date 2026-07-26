# Experiment Protocol

Mandatory operating process for designing, running, recording, comparing, and accepting skill experiments in this repository.

Strategy and hypotheses: [`RESEARCH_PLAN.md`](./RESEARCH_PLAN.md).  
Promotion norms and Definition of Done: [`AGENTS.md`](../AGENTS.md).  
Project framing: [`README.md`](../README.md).

This document specifies **how** every experiment is executed. It does not restate contest rules or the research roadmap.

---

## Purpose

Agent performance conflates model, harness, environment, prompt, and skills. Without a paired control, a high pass rate can be mistaken for skill quality.

Every claim of the form “skill configuration *S* helps” requires a **controlled paired comparison** in which the only intended difference between baseline and treatment is the skill configuration. Uncontrolled changes (model swap, timeout change, different task revision) invalidate the comparison.

This protocol exists to make that pairing repeatable, auditable, and hard to game accidentally.

---

## Experimental Unit

| Term | Definition |
|------|------------|
| **Task** | A fixed evaluable unit (instruction, environment, verifier/oracle contract). Identified by stable ID and pinned revision (git commit / registry digest). |
| **Agent** | The ACP harness used to solve the task (e.g. Claude Code ACP, Codex ACP, Gemini CLI). |
| **Model** | Exact model identifier string used for the run. |
| **Environment** | Sandbox backend and image/build inputs (Docker/Daytona/Modal as applicable), network mode, resource limits, and dependency pins. |
| **Skill library** | The set of skill packs mounted for the run (path + git commit or content hash). Includes the empty set for baseline. |
| **Baseline run** | A rollout with skill mode / library fixed to the control configuration (usually empty / `no-skill`). |
| **Treatment run** | A rollout identical to baseline except for the declared skill configuration under test. |
| **Verifier result** | Deterministic score/reward emitted after hardening (typically pass/fail or scalar in the task’s range). |
| **Safety outcome** | Classification of whether the trajectory/state incurred a safety-relevant failure (violation, critical over-action, probe/exfil attempt, severe over-refusal that blocks legitimate completion). Recorded even when the verifier is capability-only. |

A **paired trial** is one baseline run and one treatment run that share task, agent, model, environment, limits, and seeds (where supported), differing only in skill library.

---

## Experiment Types

| Type | Question | Typical control vs treatment |
|------|----------|------------------------------|
| **Baseline experiment** | What is unaugmented performance on the task set? | Empty library only (establishes reference rates). |
| **Single-skill experiment** | Does skill *A* help alone? | Empty vs `{A}`. |
| **Skill-combination experiment** | Do *A+B* interact? | Empty vs `{A}`, `{B}`, `{A,B}` (full factorial when feasible). |
| **Trigger-quality experiment** | Does a description/routing change improve activation correctness? | Same body; only frontmatter/`description` (or router text) differs. |
| **Ablation experiment** | Which component earns its keep? | Full pack vs pack minus scripts / minus references / shortened body / safety clauses removed. |
| **Regression experiment** | Where does a config hurt? | Empty vs candidate; analyze tasks with negative paired Δ. |
| **Leave-one-domain-out experiment** | Does benefit survive unseen domains? | Train/tune on all domains except *D*; evaluate paired lift on *D*. |
| **Safety stress test** | Does the config increase unsafe or over-refusal behavior? | Empty vs candidate on a safety-oriented or hazard-enriched task slice; score capability and safety jointly. |

Experiments may nest (e.g. single-skill + leave-one-domain-out) but must declare a single primary type and primary metric.

---

## Mandatory Controls

For any paired comparison, hold constant:

- model identifier  
- agent harness (+ relevant harness settings)  
- task ID and task revision  
- environment image / Dockerfile digest / sandbox class  
- dependency versions that affect solvability  
- task prompt body (no skill-name hints added for treatment)  
- seeds / temperature / sampling settings where the stack supports them  
- agent timeout, verifier timeout, and token/cost caps  

**Only intended variable:** skill configuration (which packs are mounted and their exact contents).

If a control cannot be held equal, the run is **non-comparable**. Either fix the control and rerun, or label the result exploratory (not eligible for promotion decisions).

---

## Experiment Lifecycle

```text
Proposal
  → Pre-registration
  → Baseline
  → Treatment
  → Verification
  → Failure analysis
  → Replication
  → Decision
```

| Stage | Required output |
|-------|-----------------|
| Proposal | Short statement of why the change is worth measuring |
| Pre-registration | Locked plan (see below) before treatment results influence the plan |
| Baseline | Recorded control runs for the declared task set |
| Treatment | Recorded treatment runs under the declared skill config |
| Verification | Metrics computed; integrity checks (healthy trials only) |
| Failure analysis | Autopsy for misses/regressions/safety events |
| Replication | Minimum repeats met; variance reported |
| Decision | Keep / revise / reject / rollback, with gate checklist |

Skipping pre-registration after peeking at treatment outcomes is not allowed for promotion-grade claims.

---

## Pre-registration

Before running treatment (ideally before baseline if baseline is not already on file), record:

1. **Hypothesis** — falsifiable claim (link `RESEARCH_PLAN.md` H# when applicable).  
2. **Expected mechanism** — what procedural gap closes, or what interference is removed.  
3. **Target tasks or task classes** — explicit list or inclusion rule; note held-out sets.  
4. **Primary metric** — usually mean paired lift on the target set.  
5. **Safety risks** — which hazard classes could worsen.  
6. **Acceptance threshold** — numeric or rule-based bar for the primary metric **and** regression/safety constraints.  
7. **Rejection condition** — what result kills or blocks promotion regardless of average lift.

Pre-registration may live in an experiment record (see Experiment Records). Changing acceptance thresholds after seeing results requires marking the study **post hoc** (ineligible as sole promotion evidence).

---

## Metrics

Let \(N\) be the number of tasks in the evaluation set.  
For task \(i\), let \(b_{i,r}\) and \(t_{i,r}\) be baseline and treatment rewards on repeat \(r = 1..R\).  
Use task-level means \(\bar b_i = \frac{1}{R}\sum_r b_{i,r}\), \(\bar t_i = \frac{1}{R}\sum_r t_{i,r}\) when \(R > 1\).

### Core capability

| Metric | Definition |
|--------|------------|
| **Baseline success rate** | \(B = \frac{1}{N}\sum_i \mathbf{1}[\bar b_i \ge \tau]\) (threshold \(\tau\) per task convention; often \(\tau = 1\) for binary reward). |
| **Treatment success rate** | \(T = \frac{1}{N}\sum_i \mathbf{1}[\bar t_i \ge \tau]\). |
| **Absolute skill lift** | \(\Delta = \frac{1}{N}\sum_i (\bar t_i - \bar b_i)\) (preferred primary). Macro success lift \(T - B\) may be reported alongside. |
| **Relative improvement** | \((T - B) / \max(1 - B, \varepsilon)\) when reporting headroom closed; state \(\varepsilon\) if used. |
| **Regression rate** | \(\frac{1}{N}\sum_i \mathbf{1}[\bar t_i < \bar b_i - \delta]\) (default \(\delta = 0\); document if a tolerance is used). |

### Trigger diagnostics (when trajectories allow coding)

Define, per task (or per prompt probe in trigger-quality studies):

- Relevant skill should activate: set \(\mathcal{R}\)  
- Skills that did activate/read: set \(\mathcal{A}\)

| Metric | Definition |
|--------|------------|
| **Trigger precision** | \(\lvert\mathcal{A} \cap \mathcal{R}\rvert / \lvert\mathcal{A}\rvert\) (avoid div-by-zero: mark N/A if \(\mathcal{A}=\emptyset\)). |
| **Trigger recall** | \(\lvert\mathcal{A} \cap \mathcal{R}\rvert / \lvert\mathcal{R}\rvert\). |
| **Unnecessary-trigger rate** | Fraction of runs where a skill outside \(\mathcal{R}\) was activated/read, or activation occurred on explicit non-trigger probes. |

### Safety and cost

| Metric | Definition |
|--------|------------|
| **Safety violation rate** | Fraction of runs with a recorded safety violation (critical events may be counted separately). |
| **Over-refusal rate** | Fraction of runs that fail or abstain on legitimate work primarily due to unjustified refusal/paralysis (trajectory-coded). |
| **Execution cost** | Tokens, wall time, and/or \$ cost per run; report mean and distribution. |
| **Variance across runs** | Per-task or pooled variance/SD of rewards; for lift, prefer paired bootstrap CIs over \(\Delta\) when \(N\) and \(R\) allow. |

Infra failures (sandbox crash, auth, OOM) are **excluded** from capability metrics and logged separately; they do not count as skill regressions.

---

## Replication Requirements

| Claim level | Minimum expectation |
|-------------|---------------------|
| Exploratory / debug | \(R \ge 1\) allowed; label exploratory |
| Promotion-supporting (single config) | \(R \ge 3\) trials per task×condition when cost allows; if cost-constrained, \(R \ge 3\) on a predeclared subset plus \(R \ge 1\) on the remainder, stated up front |
| Safety stress | At least as many healthy trials as the matched capability slice; do not accept “no violation observed” from \(R = 1\) on a tiny set |

**Nondeterminism:** If baseline and treatment disagree across repeats, report task-level means and uncertainty; do not cherry-pick a single lucky trial. A promotion claim requires the pre-registered threshold on the **aggregated** paired metric, not on a best-of-\(R\) selective read.

Unhealthy trials (infra) must be rerun when possible; document residual holes.

---

## Failure Classification

Assign one **primary** class per failed or regressed trial (secondary tags allowed):

| Class | Meaning |
|-------|---------|
| **Discovery failure** | Skill available but never found/listed/opened. |
| **Trigger failure** | Wrong skill activated, or correct skill not selected despite discovery. |
| **Instruction-following failure** | Skill read; agent does not follow material procedures. |
| **Execution failure** | Follows guidance but errs in code/tool use/environment actions. |
| **Verifier failure** | Output nearly right but fails deterministic checks (format/tolerance/path). |
| **Context interference** | Skill content distracts or crowds out a working approach. |
| **Skill conflict** | Multiple skills give incompatible procedures. |
| **Safety regression** | Treatment increases violations / critical unsafe actions vs baseline. |
| **Over-refusal** | Treatment blocks legitimate completion via excessive refusal. |
| **Environment failure** | Missing deps, sandbox/network/resource issues unrelated to skill quality. |
| **Measurement failure** | Mis-paired controls, wrong skill mount, contaminated baseline, scoring bug. |

Measurement and environment failures invalidate the pair for promotion evidence until corrected.

---

## Acceptance Gates

A candidate may be promoted into `skills/` only if **all** gates pass. Positive average lift alone is insufficient.

1. **Measurable positive lift** — Primary paired metric meets the pre-registered acceptance threshold on the declared evaluation set.  
2. **No serious safety regression** — No increase in critical safety violations; safety stress outcome acceptable under pre-registered rule.  
3. **Acceptable regression rate** — Regression rate under the pre-registered cap; severe single-task collapses explained and mitigated or accepted explicitly.  
4. **Evidence of generalization** — At least one of: held-out tasks, leave-one-domain-out, or multi-domain positive Δ without relying on a single authoring task.  
5. **Reproducible results** — Replication requirements met; commit/hash of skill config recorded.  
6. **Clear applicability boundaries** — Description states use and non-trigger conditions; no unbounded “use always” packs without evidence.  
7. **No task leakage** — No task IDs, oracle/verifier coupling, or instance answers (see `AGENTS.md`).  
8. **Documented limitations** — Known regressions, harness caveats, and non-goals written in the experiment record.

`AGENTS.md` Definition of Done still applies; this section is the experimental evidence bar behind that checklist.

---

## Rejection and Rollback

| Decision | When |
|----------|------|
| **Reject** | Pre-registered rejection condition hit; leakage; critical safety regression; pure single-task overfitting; measurement invalid and not repaired. |
| **Revise** | Mechanism plausible but triggers, length, conflicts, or scripts need changes; or regression rate slightly over cap with a clear fix. |
| **Disable** | Was shipped; new evidence shows harm; keep files in ablations/history but remove from submission root immediately. |
| **Remove / rollback** | Shipped skill fails gates on re-eval; revert `skills/` to last known-good library version and record the rollback experiment ID. |

Rejected candidates must not remain in `skills/`. Prefer moving them to an ablations/candidates area when those trees exist; until then, keep them out of the submission root and reference the experiment ID in the record.

---

## Experiment Records

Every promotion-grade experiment must record at least:

- **experiment_id** (see Naming)  
- date, operator (human or agent)  
- hypothesis + mechanism  
- pre-registration block (thresholds, risks, rejection rule)  
- task set definition + held-out notes  
- agent, model, environment pins  
- baseline skill config + treatment skill config (paths + git commit or content hash)  
- \(R\), unhealthy-trial log  
- metrics table (core + safety/cost as applicable)  
- regression list (task IDs + Δ)  
- failure class histogram + links/pointers to trajectories  
- decision: keep / revise / reject / rollback  
- next action  

Exploratory runs may use a shorter record but cannot be the sole basis for promotion.

---

## Naming and Versioning

### Experiment IDs

```text
exp-<YYYYMMDD>-<short-slug>-<nn>
```

Examples: `exp-20260726-safety-core-01`, `exp-20260728-xlsx-lodo-02`.

- `short-slug`: lowercase kebab-case, ≤ 32 chars.  
- `nn`: two-digit sequence for the day/slug.

### Skill versions

```text
<skill-name>@v<major>.<minor>
```

- **major** — incompatible guidance/trigger change or safety posture change.  
- **minor** — clarifications, script fixes, reference edits that preserve intent.

Library snapshots for submission candidates:

```text
library@v<major>.<minor>
```

Record the library version and constituent skill versions in the experiment that justified promotion.

---

## Reproducibility Checklist

Use before declaring an experiment complete:

- [ ] Pre-registration filled **before** treatment-informed threshold changes  
- [ ] Task set pinned (IDs + revision)  
- [ ] Agent, model, environment, limits identical across baseline and treatment  
- [ ] Only skill configuration differs  
- [ ] Skill config hash/commit recorded for both conditions  
- [ ] Healthy-trial policy applied; infra failures logged  
- [ ] \(R\) meets the claim level  
- [ ] Absolute lift, regression rate, and safety outcomes computed  
- [ ] Failures classified; regressions listed  
- [ ] Generalization evidence noted or explicitly marked missing (blocks promotion)  
- [ ] Leakage review done for any skill content under test  
- [ ] Decision recorded with experiment ID  
- [ ] If promoting: `AGENTS.md` Definition of Done checklist completed  

If any box is unchecked, the result is not promotion-grade.
