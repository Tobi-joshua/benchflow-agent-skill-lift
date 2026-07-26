# Preflight (before any EXP-001 / EXP-002 run)

1. Stay on branch `cursor/safe-task-execution-skill-a21e` (or a worktree of that commit).
2. Do **not** edit `skills/safe-task-execution/SKILL.md` or the pre-registration JSON files.
3. Install BenchFlow pin: `uv tool install "benchflow>=0.6.2,<0.7"`
4. Clone SkillsBench at commit `9a1f4dd5f7659f75707435da3ce854b6e48321d1`.
5. Export provider credentials required by `claude-agent-acp`.
6. Run:

```bash
python3 scripts/validate_skills.py --skills-dir skills
python3 scripts/hash_library.py --skills-dir skills
```

7. Confirm hash equals:

`72685e220e282607ebad10ba1ff0c6aab591d34cd73a461e752f11aeb6696521`

If it differs: **STOP** and re-register both experiments.

8. Confirm model string with `bench agent show claude-agent-acp` (or a dry smoke task).

Only then execute control/treatment commands from `common.yaml`.
