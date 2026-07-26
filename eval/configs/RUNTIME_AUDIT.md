# Runtime Compatibility Audit — EXP-001 / EXP-002

**Date:** 2026-07-26  
**Scope:** Read-only compatibility audit against SkillsBench commit  
`9a1f4dd5f7659f75707435da3ce854b6e48321d1` and the BenchFlow version resolved by that commit’s `uv.lock`.  
**Forbidden actions (honored):** no scored runs; no dependency install; no task execution; no edits to skill, pre-registration, library hash, hypotheses, metrics, thresholds, task selections, or YAML configs.

---

## Final preflight decision

**NO-GO for scored EXP-001 / EXP-002 runs.**

| Gate | Result |
|---|---|
| SkillsBench pin inspectable | PASS |
| BenchFlow resolvable at the locked version | PASS (`0.6.3` on PyPI; locked) |
| `bench eval run` + required flags present in locked package | PASS (static inspection of wheel) |
| Agent id `claude-agent-acp` registered | PASS |
| Model id `claude-sonnet-4-6` accepted by Anthropic / mentioned in BenchFlow 0.6.3 ACP code | PASS (static); live provider acceptance **not** exercised here |
| Environment installed via `uv sync --locked` | NOT DONE (by design) |
| Unscored smoke pair (mounting, jobs-dir, verifier, trials export) | NOT DONE |

**Interpretation:** The earlier “unpublished `>=0.6.2,<0.7`” blocker is **not confirmed**. SkillsBench’s committed lock resolves a public PyPI release `benchflow==0.6.3`. CLI syntax and agent id match the frozen YAML templates. Scored runs remain **NO-GO** until the locked environment is installed and one unscored control/treatment smoke pair succeeds.

---

## SkillsBench commit

| Field | Value |
|---|---|
| Repo | `https://github.com/benchflow-ai/skillsbench` |
| Commit | `9a1f4dd5f7659f75707435da3ce854b6e48321d1` |
| Commit subject | `Rename task metadata sections to sandbox (#1037)` |
| Inspection method | Local checkout of that SHA; read `pyproject.toml`, `uv.lock`, `.python-version`, `README.md`, `CONTRIBUTING.md`, `experiments/README.md` |

---

## 1. Python version required

| Source | Value |
|---|---|
| `pyproject.toml` `requires-python` | `>=3.12` |
| `.python-version` | `3.12` |
| BenchFlow `0.6.3` `Requires-Python` | `>=3.12` |

**Use Python 3.12** (exact SkillsBench pin file).

---

## 2. How BenchFlow is declared in `pyproject.toml`

At SkillsBench `9a1f4dd…`:

```toml
dependencies = [
    "benchflow[sandbox-daytona]>=0.6.3,<0.7",
    ...
]
```

Notes:
- Constraint is **`>=0.6.3,<0.7`**, not `>=0.6.2,<0.7`.
- Extra `sandbox-daytona` is for Daytona only.
- Docker is a core sandbox provider and does **not** require an optional extra.

---

## 3. Exact BenchFlow version resolved in `uv.lock`

SkillsBench at this commit does **not** pin BenchFlow to a GitHub `main` commit.  
`uv.lock` resolves a **PyPI registry** release:

| Field | Value |
|---|---|
| Package | `benchflow` |
| Resolved version | **`0.6.3`** |
| Source | `registry = "https://pypi.org/simple"` |
| Wheel | `benchflow-0.6.3-py3-none-any.whl` |
| Wheel hash | `sha256:e032bcb4894dd3f59f98204366a7282e5ae6058289d1bd8c2fce56e2c972efc6` |
| Sdist hash | `sha256:3c1842282027c0a1ece24b79958b6661b130f027b51e915926cf44db110edbff` |
| Wheel upload time (lock) | `2026-06-16T20:47:49.461Z` |

There is **no BenchFlow git SHA** in this lockfile. The reproducible identity is **PyPI `benchflow==0.6.3`** as hashed above.

PyPI also currently publishes `0.5.2`, `0.6.2`, `0.6.3`, `0.6.4`, and `0.6.5` (latest observed during audit: `0.6.5`). So `>=0.6.2,<0.7` is resolvable; the concern that `0.6.2+` is unpublished is incorrect for current PyPI.

---

## 4. Does `bench eval run` exist?

**Yes**, in BenchFlow `0.6.3`:

- Console scripts: `bench` and `benchflow` → `benchflow.cli.main:app`
- Typer sub-app: `eval`
- Command: `run` (`@eval_app.command("run")` → `eval_run`)

Verified by inspecting the published wheel (entry points + `benchflow/cli/main.py`). Not live-executed in this audit.

---

## 5. Required CLI flags — validity in `0.6.3`

All flags used by `eval/configs/common.yaml` are present on `bench eval run` in `0.6.3`:

| Flag | Present | Notes |
|---|---|---|
| `--tasks-dir` | Yes | Local tasks directory |
| `--agent` | Yes | Agent name |
| `--model` | Yes | Model option alias |
| `--skill-mode` | Yes | Help: `no-skill`, `with-skill`, or `self-gen` |
| `--skills-dir` | Yes | Skills directory to deploy |
| `--sandbox` | Yes | Bound to parameter `environment`; providers: `docker`, `daytona`, `modal` |
| `--jobs-dir` | Yes | Output directory |

Skill modes confirmed in `benchflow/skill_policy.py`: `no-skill`, `with-skill`, `self-gen`.

---

## 6. Registered Claude ACP agent identifier

**Exact registry key:** `claude-agent-acp`

From `benchflow/agents/registry.py` in `0.6.3`:

- `name="claude-agent-acp"`
- Description: Claude Code via ACP
- Install pin: `@agentclientprotocol/claude-agent-acp@0.40.0`
- Skill mount path: `$HOME/.claude/skills`
- `requires_env=["ANTHROPIC_API_KEY"]` (may be replaced by subscription auth; see §8)
- `api_protocol="anthropic-messages"`
- ACP model config id: `"model"`

This matches the frozen config `agent: claude-agent-acp`.

---

## 7. Is `claude-sonnet-4-6` accepted by that agent?

| Evidence | Finding |
|---|---|
| Anthropic public model listing (prior context) | `claude-sonnet-4-6` is an active recommended model id |
| BenchFlow `0.6.3` ACP runtime | Uses bare ids; comments/examples include `"claude-sonnet-4-6"` as the expected bare form for Claude ACP |
| SkillsBench experiment YAML at this commit | Older examples use ids like `claude-sonnet-4-5@20250929`, not a negative signal against `4-6` |
| Live `bench eval run` / provider call | **Not performed** |

**Audit status:** Accept as the planned model pin for config purposes. Treat live acceptance as a smoke-test gate, not a scored-run assumption.

---

## 8. Authentication method

For `claude-agent-acp` in BenchFlow `0.6.3`:

1. **API key (primary / validated env):** `ANTHROPIC_API_KEY`
2. **Subscription auth substitute:** host file `~/.claude/.credentials.json` (`claude login` on Linux), declared via `subscription_auth` with `replaces_env="ANTHROPIC_API_KEY"`
3. SkillsBench docs also mention OAuth-token env wiring for dogfooding; BenchFlow precedence is **API key over subscription/OAuth** when both are present

Docker local runs additionally require a working Docker daemon (see §9). Daytona/Modal need their own credentials only if those sandboxes are used (not required by current freeze).

---

## 9. Docker support in the resolved runtime

**Yes — first-class / built-in.**

From `benchflow/sandbox/providers.py` in `0.6.3`:

- Providers: `docker` (extra=`None`), `daytona` (extra=`sandbox-daytona`), `modal` (extra=`sandbox-modal`)
- Docker does not require an optional dependency extra

SkillsBench README also documents `--sandbox docker` for local-only runs.

**Prerequisites for our freeze:**

- Docker Engine + Compose plugin available to the user running `bench`
- Ability to build task images from each task’s `environment/Dockerfile`
- Network policy left to task.md (`network_mode: follow-task` in current config)

---

## 10. Is `uv run bench` required or preferred?

| Path | Role at SkillsBench `9a1f4dd…` |
|---|---|
| `uv sync --locked` | **Required for reproducing the committed dependency graph** (README / CONTRIBUTING / experiments README) |
| `uv run bench …` | **Preferred for experiment reproducibility** against the locked env (`experiments/README.md` shows this path) |
| `uv tool install "benchflow>=0.6.2,<0.7"` then bare `bench …` | Documented for day-to-day CLI authoring in CONTRIBUTING/AGENTS.md; **can float** within the open range (today up to `0.6.5`) and **may diverge** from `uv.lock`’s `0.6.3` |
| `uv lock --upgrade-package benchflow` | **Do not run** — would refresh the lock and break the pin |

**Audit recommendation:** Prefer

```bash
git clone https://github.com/benchflow-ai/skillsbench.git
cd skillsbench
git checkout 9a1f4dd5f7659f75707435da3ce854b6e48321d1
uv sync --locked
uv run bench --help
```

If a global tool install is used anyway, pin exactly: `uv tool install --python 3.12 "benchflow==0.6.3"` (still inferior to `uv run bench` from the locked SkillsBench env for matching transitive deps).

---

## Exact verified CLI syntax (static)

Control (no skills):

```bash
uv run bench eval run \
  --tasks-dir "${SKILLSBENCH_ROOT}/tasks/${TASK_ID}" \
  --agent claude-agent-acp \
  --model claude-sonnet-4-6 \
  --skill-mode no-skill \
  --sandbox docker \
  --jobs-dir "${JOBS_DIR}/control/${TASK_ID}/r${REPEAT}"
```

Treatment (repo skills library):

```bash
uv run bench eval run \
  --tasks-dir "${SKILLSBENCH_ROOT}/tasks/${TASK_ID}" \
  --agent claude-agent-acp \
  --model claude-sonnet-4-6 \
  --skill-mode with-skill \
  --skills-dir "${REPO_ROOT}/skills" \
  --sandbox docker \
  --jobs-dir "${JOBS_DIR}/treatment/${TASK_ID}/r${REPEAT}"
```

These match the frozen templates in `eval/configs/common.yaml`, except the preferred launcher is `uv run bench` from the SkillsBench locked environment rather than an unconstrained global `bench`.

---

## Mismatches with current configuration

Compared to `eval/configs/common.yaml` + `eval/configs/PREFLIGHT.md` (**YAML not changed in this step**):

| # | Current config | SkillsBench / BenchFlow `0.6.3` evidence | Severity |
|---|---|---|---|
| M1 | `benchflow.package_constraint: "benchflow>=0.6.2,<0.7"` | SkillsBench `pyproject` wants `>=0.6.3,<0.7`; lock pins **`==0.6.3`** | Medium — open range can float to `0.6.4`/`0.6.5` |
| M2 | PREFLIGHT / implied install: `uv tool install "benchflow>=0.6.2,<0.7"` | Reproducible path is SkillsBench checkout + `uv sync --locked` + `uv run bench` | High for reproducibility |
| M3 | Narrative risk that `>=0.6.2` is unpublished / main-only | False for this pin: PyPI has `0.6.2`–`0.6.5`; lock uses registry `0.6.3` | Informational (blocker cleared) |
| M4 | Commands invoke bare `bench` | Prefer `uv run bench` under locked SkillsBench env | Medium |
| M5 | Model pin not smoke-tested | Static acceptance only | Medium until smoke |
| M6 | No install / Docker / auth verification yet | Required before scored runs | Blocking |

No mismatch found for: agent id, skill modes, sandbox=`docker`, flag names, SkillsBench git commit, or command shape of `bench eval run`.

---

## Exact proposed corrections (do **not** apply yet)

1. **Runtime source of truth:** SkillsBench commit `9a1f4dd…` + committed `uv.lock` → BenchFlow **`0.6.3`** (PyPI), not an open `>=0.6.2` tool install and not BenchFlow git `main`.
2. When YAML is later edited (separate step), change documentation/pins to something equivalent to:
   - `skillsbench.git_commit: 9a1f4dd5f7659f75707435da3ce854b6e48321d1`
   - `benchflow.resolved_version: "0.6.3"`
   - `benchflow.source: "pypi (skillsbench uv.lock)"`
   - `install: uv sync --locked`
   - `launcher: uv run bench`
   - Optional fallback only: `uv tool install --python 3.12 "benchflow==0.6.3"`
3. Keep agent `claude-agent-acp` and model `claude-sonnet-4-6`.
4. Keep control/treatment flag templates; prefix with `uv run` when executing from SkillsBench.
5. After install: run **one unscored smoke pair** on a single task (control + treatment). Verify skill mount, `--jobs-dir` outputs, verifier artifacts, and trial JSON conversion. **Do not** add smoke results to the scored set.
6. Only then proceed to scored EXP-001 / EXP-002.

---

## Explicit non-runtime reminder (unchanged by this audit)

EXP-001 safety metrics remain **trajectory-coded proxies** on public SkillsBench tasks, not ClawsBench safety rewards. That limitation must stay explicit in eventual conclusions. It does not change this runtime GO/NO-GO.

---

## Audit checklist (answers)

1. **Python:** `>=3.12` (prefer `3.12`)
2. **pyproject BenchFlow declaration:** `benchflow[sandbox-daytona]>=0.6.3,<0.7`
3. **uv.lock BenchFlow resolution:** PyPI **`benchflow==0.6.3`** (no git commit; hashes above)
4. **`bench eval run`:** exists
5. **Flags:** `--tasks-dir`, `--agent`, `--model`, `--skill-mode`, `--skills-dir`, `--sandbox`, `--jobs-dir` all valid
6. **Agent id:** `claude-agent-acp`
7. **Model `claude-sonnet-4-6`:** statically plausible / referenced; live acceptance deferred to smoke
8. **Auth:** `ANTHROPIC_API_KEY` or `~/.claude/.credentials.json` via `claude login`
9. **Docker:** supported (built-in provider)
10. **`uv run bench`:** preferred for locked reproducibility; bare `bench` only if tool-installed to **exactly** `0.6.3`

**Decision: NO-GO** for scored runs until locked install + unscored smoke succeed.
