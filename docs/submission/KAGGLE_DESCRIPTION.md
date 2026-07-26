# Kaggle Project Description (draft)

Paste/adapt into the Kaggle writeup or project page. Keep claims scoped to evidence you have.

---

## Title

**Safe Task Execution: a thin static skill measured with paired lift**

## Subtitle

Track 1 — Static Skills · BenchFlow Agent Skill Lift

## Overview

Agent skills are modular instruction packs that change what an agent does under a fixed model and harness. In Skill Lift, organizers hold models, harness, and private tasks constant — **the skill library is the only variable**. We treat that setup as a measurement instrument, not a prompt-engineering contest.

This project ships a deliberately small Track‑1 library centered on one candidate skill, `safe-task-execution`: lightweight scope and safety routing for completing authorized work under least privilege. It is designed to fire on **material risk** (untrusted instructions, sensitive data, external send/share, destructive actions, unclear authority) and to stay quiet on ordinary local work.

## Method

1. **Pre-register** hypotheses, metrics, and keep/revise/reject gates before scored runs.
2. **Freeze pins:** SkillsBench commit, BenchFlow `0.6.3` via locked `uv sync`, agent `claude-agent-acp`, model `claude-sonnet-4-6`, library content hash.
3. **Paired evaluation:** identical tasks with `--skill-mode no-skill` vs `--skill-mode with-skill --skills-dir <repo>/skills`.
4. **Safety-aware interpretation:** capability lift alone is insufficient; over-refusal and unsafe shortcuts are first-class failure modes.
5. **Negative control (EXP-002):** tasks that should not trigger the skill — expect near-zero trigger rate and near-zero lift.

## What we have measured so far

**Unscored smoke (PASS):** one `citation-check` control/treatment pair on the locked runtime.

| Condition | Skill mode | Verifier reward | Notes |
|---|---|---|---|
| Control | `no-skill` | 0.0 | No custom skill mounted |
| Treatment | `with-skill` | 1.0 | Repo `skills/` mounted; `safe-task-execution` referenced in artifacts |

This validates Docker sandboxing, agent auth, verifier extraction, and trial JSON conversion. **It is not a scored lift result** and must not be read as proof of general improvement.

**Scored EXP-001 / EXP-002:** pre-registered and frozen; not executed yet.

## Design principles

- Less is more — prefer one sharp meta-skill over a noisy pack.
- Procedures, not lookup tables — no memorized public-task answers.
- Progressive disclosure — rich `description` for routing; lean body.
- Safety constrains capability — unsafe “success” is a loss.
- Negative results are first-class — regressions kill skills.

## Limitations (explicit)

- Public SkillsBench ≠ private Skill Lift mix.
- EXP-001 safety metrics on public tasks are **trajectory-coded proxies**, not full ClawsBench safety rewards (ClawsBench task materials are still forthcoming publicly).
- Single-task smoke cannot establish mean lift, variance, or trigger precision.

## Reproducibility

- Branch: `cursor/safe-task-execution-skill-a21e`
- Library hash: `72685e220e282607ebad10ba1ff0c6aab591d34cd73a461e752f11aeb6696521`
- SkillsBench: `9a1f4dd5f7659f75707435da3ce854b6e48321d1`
- Runtime: `uv sync --locked` then `uv run bench …` (do not refresh BenchFlow in the lockfile)

## Next measurement step

Run **EXP-001** first (cross-domain paired evaluation), inspect cost/logs/outputs, then decide whether to launch EXP-002.
