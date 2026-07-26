# Smoke Test Report — unscored control/treatment pair

**Final decision: FAIL**

**Execution date:** 2026-07-26  
**Repo git commit:** `3ac2aa79e91262e5858e06e5fa32647a56fde8ee` (branch `cursor/safe-task-execution-skill-a21e`; includes these smoke artifacts)  
**Library hash:** `72685e220e282607ebad10ba1ff0c6aab591d34cd73a461e752f11aeb6696521` (matches lock)  
**SkillsBench commit:** `9a1f4dd5f7659f75707435da3ce854b6e48321d1`  
**Python version:** 3.12.3 (via SkillsBench `uv sync --locked`)  
**BenchFlow version:** 0.6.3 (locked; confirmed with `importlib.metadata.version`)  
**Agent / model:** `claude-agent-acp` / `claude-sonnet-4-6`  
**Selected task:** `citation-check` (from frozen EXP-001 set)  
**Scored experiment impact:** none — outputs only under `eval/runs/smoke/`; EXP-001/EXP-002 results untouched

---

## Purpose

Runtime and data-pipeline validation only. Not a scored EXP-001/EXP-002 trial.

---

## Preflight checks

| Check | Result |
|---|---|
| Branch `cursor/safe-task-execution-skill-a21e` | PASS |
| Library hash matches locked value | PASS |
| SkillsBench at `9a1f4dd…` | PASS |
| `uv sync --locked` (SkillsBench; `uv.lock` not refreshed) | PASS |
| Python 3.12 in locked env | PASS |
| BenchFlow 0.6.3 in locked env | PASS |
| `claude-agent-acp` registered (`uv run bench agent show`) | PASS |
| `claude-sonnet-4-6` accepted by harness for that agent | PASS (static + run accepted model id; failed later on missing API key) |
| Docker available | PASS (installed + `dockerd` started in this environment; client/server 29.1.3) |
| Authentication available | **FAIL** — `ANTHROPIC_API_KEY` unset; no `~/.claude/.credentials.json` |

---

## Exact commands

SkillsBench root used for this smoke: `/tmp/skillsbench-audit`  
Repo root: `/workspace`

### Control (no-skill)

```bash
cd /tmp/skillsbench-audit
uv run bench eval run \
  --tasks-dir "/tmp/skillsbench-audit/tasks/citation-check" \
  --agent claude-agent-acp \
  --model claude-sonnet-4-6 \
  --skill-mode no-skill \
  --sandbox docker \
  --jobs-dir "/workspace/eval/runs/smoke/jobs/control/citation-check/r1"
```

### Treatment (repo skills only)

```bash
cd /tmp/skillsbench-audit
uv run bench eval run \
  --tasks-dir "/tmp/skillsbench-audit/tasks/citation-check" \
  --agent claude-agent-acp \
  --model claude-sonnet-4-6 \
  --skill-mode with-skill \
  --skills-dir "/workspace/skills" \
  --sandbox docker \
  --jobs-dir "/workspace/eval/runs/smoke/jobs/treatment/citation-check/r1"
```

---

## Launch status

| Condition | Launch | Exit | Job dir |
|---|---|---|---|
| Control | Started; errored before sandbox/agent | 1 | `eval/runs/smoke/jobs/control/citation-check/r1/2026-07-26__19-02-25` |
| Treatment | Started; errored before sandbox/agent | 1 | `eval/runs/smoke/jobs/treatment/citation-check/r1/2026-07-26__19-02-41` |

Shared blocker from both `result.json` files:

> `ANTHROPIC_API_KEY required for model 'claude-sonnet-4-6' but not set.`

Environment setup time was `0.0s` in both summaries — Docker task images were not built/started for these attempts.

---

## Skill absence / presence evidence

Auth failed before container start, so **in-container skill discovery was not exercised**.  
Harness-level skill policy fields were still recorded and are useful partial evidence:

| Field | Control | Treatment |
|---|---|---|
| `skill_mode` | `no-skill` | `with-skill` |
| `skill_source` | `none` | `custom_runtime` |
| `requested_skills_dir` | `null` | `/workspace/skills` |
| `effective_skills_dir` | `null` | `/workspace/skills` |
| `skills_sandbox_dir` | `null` | `/skills` |
| `include_task_skills` | `false` | `false` |

**Control:** custom skill not requested / source `none` — PASS for harness-level absence.  
**Treatment:** mounts repo `skills/` as custom runtime (`safe-task-execution` lives there) — PASS for harness-level mount intent.  
**In-sandbox discoverability / trajectory activation:** NOT VERIFIED (auth blocker).

---

## Verifier status

**Not run.** Both jobs errored before agent execution; `rewards` is `null`; `verifier_errored` remains 0 in summaries because the verifier never executed.

---

## Trial JSON compatibility

Wrote `eval/runs/smoke/trials.json` from the smoke job metadata:

- Conditions: `baseline` / `treatment`
- `healthy: false` for both (auth/infra failure, not task failure)
- `reward: 0.0` placeholder with `rewards_raw: null` noted
- Validates against `eval/configs/trials.schema.json` (structural required fields; `jsonschema` check also run via SkillsBench env)

`scripts/compute_lift.py` correctly refuses to score when no healthy paired trials exist — confirms environment failures are distinguishable from task/skill outcomes.

**Not** written into EXP-001/EXP-002 paths. Metrics for those experiments were not calculated.

---

## Environment vs task/skill failure distinguishability

| Signal | Observed |
|---|---|
| `error` text | missing `ANTHROPIC_API_KEY` |
| `rewards` | `null` |
| `healthy` in smoke trials | `false` |
| `failure_class` | `environment_auth` |
| Verifier outcome | absent (not a task fail) |

This matches the frozen protocol rule: infra/auth failures must not enter paired lift denominators.

---

## Secrets / credentials

- No API key values were available in the environment.
- Smoke artifacts were scanned for token-like patterns before commit.
- Logs under `eval/runs/smoke/logs/` are local aids; `*.log` is gitignored.
- This report intentionally records only variable **names**, never secret values.

---

## Acceptance gate checklist

| Gate | Status |
|---|---|
| Exact locked versions installed | PASS (`BenchFlow 0.6.3`, Python 3.12) |
| Library hash still matches | PASS |
| Control and treatment both execute end-to-end | **FAIL** (auth) |
| Treatment skill mounted; control has no skill exposure | PARTIAL (harness fields only; no sandbox proof) |
| Verifier result extractable | **FAIL** (verifier not reached) |
| Trial JSON validates against schema | PASS (with `healthy=false`) |
| Smoke outputs isolated from scored outputs | PASS |
| No secrets committed | PASS |

---

## Warnings / blockers

1. **Blocker (fatal for this smoke):** Anthropic authentication is not configured in this cloud-agent environment (`ANTHROPIC_API_KEY` missing; no Claude subscription credentials file).
2. Docker was not preinstalled; it was installed and `dockerd` started successfully for this session. Future scored hosts must provide Docker (or an approved alternate sandbox recorded before first scored run — not done here; freeze remains `docker`).
3. Because auth failed before sandbox start, skill filesystem mount and trajectory discovery remain unproven.
4. Frozen YAML was **not** changed. Open-range installs were **not** used.

---

## Final decision

**FAIL** — unscored smoke pair did not clear the acceptance gate.

**Scored EXP-001 / EXP-002 remain NO-GO.**

### Required before re-running smoke

1. Provide Anthropic auth to the runner (`ANTHROPIC_API_KEY` or `claude login` → `~/.claude/.credentials.json`) without committing secrets.
2. Re-run the same two commands under `eval/runs/smoke/` only.
3. Confirm in-container skill absence/presence, verifier artifacts, and healthy trial JSON extraction.
4. Only after a PASS smoke report: proceed to scored experiments.
