# EXP-001 scored runbook

**Experiment:** `exp-20260726-safe-task-cross-domain-01` (EXP-001)  
**Volume:** 13 tasks × 2 conditions × 3 repeats = **78** agent runs  
**Outputs:** `eval/runs/exp-001/` only  
**Do not** write into smoke or EXP-002 paths.  
**Do not** edit `skills/`, pre-registration JSON, or EXP YAML task sets.

## Preflight

```bash
cd ~/projects/benchflow-agent-skill-lift
git pull origin main
# optional: also pull runner branch if not merged yet
# git fetch origin cursor/exp-001-runner-a21e && git merge origin/cursor/exp-001-runner-a21e

python3 scripts/validate_skills.py --skills-dir skills
python3 scripts/hash_library.py --skills-dir skills
# must equal:
# 72685e220e282607ebad10ba1ff0c6aab591d34cd73a461e752f11aeb6696521

cd ~/projects/benchflow-agent-skill-lift/skillsbench
git rev-parse HEAD   # 9a1f4dd5f7659f75707435da3ce854b6e48321d1
uv sync --locked
uv run python -c "from importlib.metadata import version; print(version('benchflow'))"  # 0.6.3

sg docker -c 'docker info' | head -15
```

Auth (never paste into chat / git):

```bash
read -s ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY
```

## Launch (resumable)

```bash
cd ~/projects/benchflow-agent-skill-lift
export REPO_ROOT="$PWD"
export SKILLSBENCH_ROOT="$PWD/skillsbench"

# dry-run first (no API calls)
python3 scripts/run_exp001.py --docker-via sg --dry-run | head -40

# full scored EXP-001 (hours; paid)
python3 scripts/run_exp001.py --docker-via sg
```

Resume after interrupt: run the same command again — completed healthy trials are skipped.

## After runs

```bash
python3 scripts/run_exp001.py --aggregate-only
python3 scripts/compute_lift.py eval/runs/exp-001/trials.json \
  --output eval/runs/exp-001/metrics.json

unset ANTHROPIC_API_KEY
```

Then manually code `safety_violation` / `over_refusal` / trigger fields where needed, review metrics against pre-registration gates, and only then fill `results` / `decision` in the pre-registration JSON.

## Cost note

Smoke used ~$0.30–0.35 per condition on one task. Full EXP-001 is 78 runs — budget accordingly and watch the first few `progress.jsonl` rows before leaving it unattended.
