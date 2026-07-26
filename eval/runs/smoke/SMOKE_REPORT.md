# Smoke Test Report — unscored control/treatment pair

**Final decision: FAIL**

**Exact remaining blocker:** Anthropic authentication is not available to this cloud-agent runner. No `ANTHROPIC_API_KEY` (or Claude subscription credentials file) is present in the process environment, and this session cannot interactively `read` a secret without exposing it into chat or committed files.

**Branch:** `cursor/safe-task-execution-skill-a21e`  
**Library hash:** `72685e220e282607ebad10ba1ff0c6aab591d34cd73a461e752f11aeb6696521` (unchanged)  
**SkillsBench commit:** `9a1f4dd5f7659f75707435da3ce854b6e48321d1`  
**Python / BenchFlow:** 3.12.3 / 0.6.3 (`uv sync --locked`)  
**Agent / model:** `claude-agent-acp` / `claude-sonnet-4-6` (unchanged)  
**Selected task:** `citation-check` (unchanged)  
**Scored experiment impact:** none — outputs only under `eval/runs/smoke/`; EXP-001/EXP-002 untouched

---

## Attempt 1 — infrastructure/authentication failure (2026-07-26)

Preserved under `eval/runs/smoke/archive/attempt-1-auth-fail/`.

| Item | Result |
|---|---|
| Classification | Infrastructure / authentication failure (not a skill failure) |
| Control launch | Started; errored before sandbox |
| Treatment launch | Started; errored before sandbox |
| Error (both) | `ANTHROPIC_API_KEY required for model 'claude-sonnet-4-6' but not set` |
| Sandbox start | No (`environment_setup_time_sec = 0`) |
| Verifier | Not executed (`rewards = null`) |
| Harness skill policy | Control `skill_mode=no-skill` / `skill_source=none`; treatment `with-skill` / `custom_runtime` / `effective_skills_dir=/workspace/skills` |
| Trial JSON | Written with `healthy=false` (schema-valid) |

Frozen skill, hash, pre-regs, and scored paths were not modified.

---

## Attempt 2 — authenticated rerun (2026-07-26)

**Status: NOT EXECUTED — authentication still unavailable**

### Preflight before intended rerun

| Check | Result |
|---|---|
| Branch `cursor/safe-task-execution-skill-a21e` | PASS |
| Library hash matches lock | PASS |
| SkillsBench `9a1f4dd…` | PASS |
| Python 3.12 | PASS |
| BenchFlow 0.6.3 | PASS |
| Docker available | PASS |
| `claude-agent-acp` registered | PASS |
| Auth present (`ANTHROPIC_API_KEY` or `~/.claude/.credentials.json`) | **FAIL** |
| Auth accepted by harness | **NOT TESTED** (credential absent) |

### Auth discovery (presence only; no values inspected or printed)

- Process env: `ANTHROPIC_API_KEY` absent
- Alternate env names checked: absent
- Claude credentials file: absent
- `/run/secrets` / Cursor secret mounts: none
- Any process environ containing `ANTHROPIC_API_KEY`: none
- Cloud environment record for this run: `null` (no saved environment with injected secrets)
- Interactive `read -s` / PowerShell secure prompt: not usable in this non-interactive cloud agent without pasting into chat (forbidden)

### Commands that would be rerun unchanged

Control:

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

Treatment:

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

Attempt 2 intentionally **did not** re-invoke these commands without credentials, to avoid another identical pre-sandbox auth error and to avoid any risk of writing secret material into logs.

### Attempt 2 verification checklist

| # | Check | Status |
|---|---|---|
| 1 | Authentication accepted | FAIL — not present |
| 2 | Both jobs launch | NOT RUN |
| 3 | Both sandboxes start | NOT RUN |
| 4 | Agent connects | NOT RUN |
| 5 | Control has no custom skill | NOT RUN (Attempt 1 harness fields only) |
| 6 | Treatment mounts `safe-task-execution` | NOT RUN (Attempt 1 harness fields only) |
| 7 | Verifier executes | NOT RUN |
| 8 | Reward extractable | NOT RUN |
| 9 | Trial JSON schema-valid | Attempt 1 PASS with `healthy=false`; Attempt 2 no new healthy trials |
| 10 | Failure classes distinguishable | PASS (Attempt 1 classified `environment_auth`) |
| 11 | No credentials in repo/git diff | PASS |

---

## How to supply auth for the next rerun (outside this chat)

Do **not** paste the key into Cursor chat, YAML, Markdown, JSON, or a committed `.env`.

Preferred for Cursor Cloud: add `ANTHROPIC_API_KEY` as a **Cloud Agent / environment secret** for a saved environment attached to this repo, then restart the agent so the key is injected only into the process environment.

Local / SSH runner alternative:

```bash
read -s ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY
# then the two uv run bench commands above
unset ANTHROPIC_API_KEY
```

After auth is present, re-run Step 15 unchanged (same task/agent/model/commands/output roots).

---

## Artifacts layout

```
eval/runs/smoke/
  SMOKE_REPORT.md          # this report
  trials.json              # latest smoke trials (still unhealthy / blocked)
  archive/attempt-1-auth-fail/
    jobs/...               # preserved Attempt 1 outputs
    trials.json
  jobs/...                 # current tree (Attempt 1 copies until a successful rerun supersedes)
```

No outputs under `eval/runs/exp-001/` or `eval/runs/exp-002/`.

---

## Final decision

**FAIL** — authenticated smoke pair could not be executed because the runner still has no Anthropic credential.

**Scored EXP-001 / EXP-002 remain NO-GO.**
