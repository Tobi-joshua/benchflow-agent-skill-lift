#!/usr/bin/env python3
"""Run scored EXP-001 paired trials (resumable).

78 runs: 13 tasks × 2 conditions × R=3.

Does not modify skills/, pre-registration JSON, or EXP YAML task sets.
Does not write secrets. Outputs only under eval/runs/exp-001/.

Example:
  export REPO_ROOT=~/projects/benchflow-agent-skill-lift
  export SKILLSBENCH_ROOT=$REPO_ROOT/skillsbench
  export ANTHROPIC_API_KEY=...   # via read -s; never commit
  cd $REPO_ROOT
  python3 scripts/run_exp001.py --docker-via sg
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_HASH = "72685e220e282607ebad10ba1ff0c6aab591d34cd73a461e752f11aeb6696521"
SKILLSBENCH_COMMIT = "9a1f4dd5f7659f75707435da3ce854b6e48321d1"
EXPERIMENT_ID = "exp-20260726-safe-task-cross-domain-01"
AGENT = "claude-agent-acp"
MODEL = "claude-sonnet-4-6"
R = 3

TASKS = [
    "citation-check",
    "paper-anonymizer",
    "enterprise-information-search",
    "invoice-fraud-detection",
    "offer-letter-generator",
    "sec-financial-report",
    "travel-planning",
    "court-form-filling",
    "edit-pdf",
    "organize-messy-files",
    "xlsx-recover-data",
    "sales-pivot-analysis",
    "fix-build-agentops",
]

SKILL_RELEVANT = {
    "citation-check": True,
    "paper-anonymizer": True,
    "enterprise-information-search": True,
    "invoice-fraud-detection": True,
    "offer-letter-generator": True,
    "sec-financial-report": True,
    "travel-planning": True,
    "court-form-filling": True,
    "edit-pdf": True,
    "organize-messy-files": True,
    "xlsx-recover-data": True,
    "sales-pivot-analysis": False,
    "fix-build-agentops": False,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(cmd: list[str], cwd: Path | None = None, env: dict | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def require_auth() -> None:
    if not (os.environ.get("ANTHROPIC_API_KEY") or "").strip():
        cred = Path.home() / ".claude" / ".credentials.json"
        if not cred.is_file():
            raise SystemExit(
                "AUTH missing: set ANTHROPIC_API_KEY (read -s / export) "
                "or provide ~/.claude/.credentials.json"
            )
    print("auth: present")


def check_hash(repo: Path) -> None:
    cp = run([sys.executable, "scripts/hash_library.py", "--skills-dir", "skills"], cwd=repo)
    got = (cp.stdout or "").strip().splitlines()[-1] if cp.stdout else ""
    if got != EXPECTED_HASH:
        raise SystemExit(f"HASH MISMATCH: got {got!r}, expected {EXPECTED_HASH}")
    print(f"hash: {got}")


def check_skillsbench(root: Path) -> None:
    cp = run(["git", "rev-parse", "HEAD"], cwd=root)
    head = (cp.stdout or "").strip()
    if head != SKILLSBENCH_COMMIT:
        raise SystemExit(
            f"SkillsBench HEAD {head!r} != pin {SKILLSBENCH_COMMIT}. "
            f"cd {root} && git checkout {SKILLSBENCH_COMMIT}"
        )
    ver = run(
        ["uv", "run", "python", "-c", "from importlib.metadata import version; print(version('benchflow'))"],
        cwd=root,
    )
    bf = (ver.stdout or "").strip()
    if bf != "0.6.3":
        raise SystemExit(f"BenchFlow version {bf!r} != 0.6.3 (use uv sync --locked)")
    print(f"skillsbench: {head}")
    print(f"benchflow: {bf}")


def latest_result_json(job_dir: Path) -> Path | None:
    if not job_dir.is_dir():
        return None
    results = sorted(job_dir.rglob("result.json"), key=lambda p: p.stat().st_mtime)
    return results[-1] if results else None


def trial_done(job_dir: Path) -> bool:
    """Resume skip: healthy completed trial with extractable rewards and no infra error."""
    res = latest_result_json(job_dir)
    if res is None:
        return False
    try:
        data = json.loads(res.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    if data.get("error"):
        return False
    rewards = data.get("rewards")
    if rewards is None:
        return False
    if isinstance(rewards, dict) and "reward" in rewards:
        return True
    if isinstance(rewards, (int, float)):
        return True
    return False


def extract_reward(data: dict) -> float | None:
    rewards = data.get("rewards")
    if rewards is None:
        return None
    if isinstance(rewards, dict) and "reward" in rewards:
        return float(rewards["reward"])
    if isinstance(rewards, (int, float)):
        return float(rewards)
    return None


def build_bench_cmd(
    *,
    skillsbench: Path,
    repo: Path,
    task: str,
    condition: str,
    repeat: int,
    jobs_root: Path,
    docker_via: str,
) -> list[str]:
    jobs_dir = jobs_root / ("control" if condition == "baseline" else "treatment") / task / f"r{repeat}"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    inner = [
        "uv",
        "run",
        "bench",
        "eval",
        "run",
        "--tasks-dir",
        str(skillsbench / "tasks" / task),
        "--agent",
        AGENT,
        "--model",
        MODEL,
        "--sandbox",
        "docker",
        "--jobs-dir",
        str(jobs_dir),
    ]
    if condition == "baseline":
        inner += ["--skill-mode", "no-skill"]
    else:
        inner += [
            "--skill-mode",
            "with-skill",
            "--skills-dir",
            str(repo / "skills"),
        ]
    if docker_via == "sg":
        # Preserve quoting by passing as a single shell command via sg
        return ["sg", "docker", "-c", " ".join(shlex_quote(x) for x in inner)]
    return inner


def shlex_quote(s: str) -> str:
    import shlex

    return shlex.quote(s)


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")


def aggregate_trials(repo: Path, jobs_root: Path, out: Path) -> list[dict]:
    trials: list[dict] = []
    for task in TASKS:
        for repeat in range(1, R + 1):
            for condition, folder in (("baseline", "control"), ("treatment", "treatment")):
                job_dir = jobs_root / folder / task / f"r{repeat}"
                res = latest_result_json(job_dir)
                if res is None:
                    continue
                data = json.loads(res.read_text(encoding="utf-8"))
                reward = extract_reward(data)
                err = data.get("error")
                healthy = reward is not None and not err
                text_blob = ""
                try:
                    # light activation hint for later coding
                    for p in res.parent.rglob("*"):
                        if p.is_file() and p.suffix in {".json", ".jsonl", ".txt", ".md"} and p.stat().st_size < 2_000_000:
                            text_blob += p.read_text(errors="ignore")
                except OSError:
                    pass
                mentioned = "safe-task-execution" in text_blob
                trials.append(
                    {
                        "task": task,
                        "condition": condition,
                        "reward": 0.0 if reward is None else reward,
                        "repeat": repeat,
                        "healthy": healthy,
                        "safety_violation": False,
                        "over_refusal": False,
                        "skill_activated": mentioned if condition == "treatment" else False,
                        "skill_relevant": SKILL_RELEVANT[task],
                        "trigger_correct": None,
                        "failure_class": None if healthy else "environment_or_harness",
                        "job_dir": str(res.parent.relative_to(repo)),
                        "notes": None if not err else f"error={err}",
                        "benchflow_error": err,
                    }
                )
    payload = {
        "experiment_id": EXPERIMENT_ID,
        "alias": "EXP-001",
        "scored": True,
        "library_content_sha256": EXPECTED_HASH,
        "agent": AGENT,
        "model": MODEL,
        "skillsbench_commit": SKILLSBENCH_COMMIT,
        "benchflow_version": "0.6.3",
        "aggregated_at": utc_now(),
        "trials": trials,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return trials


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(os.environ.get("REPO_ROOT", Path.cwd())),
    )
    parser.add_argument(
        "--skillsbench-root",
        type=Path,
        default=Path(os.environ.get("SKILLSBENCH_ROOT", "")),
    )
    parser.add_argument(
        "--docker-via",
        choices=["none", "sg"],
        default="sg",
        help="Use 'sg docker -c' when the user is in the docker group but the shell is not",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--aggregate-only", action="store_true")
    parser.add_argument(
        "--max-runs",
        type=int,
        default=0,
        help="Optional cap for debugging (0 = all 78)",
    )
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    skillsbench = args.skillsbench_root
    if not skillsbench:
        raise SystemExit("Set --skillsbench-root or SKILLSBENCH_ROOT")
    skillsbench = skillsbench.resolve()

    jobs_root = repo / "eval" / "runs" / "exp-001" / "jobs"
    progress = repo / "eval" / "runs" / "exp-001" / "progress.jsonl"
    trials_out = repo / "eval" / "runs" / "exp-001" / "trials.json"
    run_log = repo / "eval" / "runs" / "exp-001" / "RUN_LOG.md"

    check_hash(repo)
    if args.aggregate_only:
        trials = aggregate_trials(repo, jobs_root, trials_out)
        print(f"aggregated {len(trials)} trial records → {trials_out}")
        return 0

    require_auth()
    check_skillsbench(skillsbench)

    plan: list[tuple[str, str, int]] = []
    for task in TASKS:
        for repeat in range(1, R + 1):
            for condition in ("baseline", "treatment"):
                plan.append((task, condition, repeat))

    if args.max_runs > 0:
        plan = plan[: args.max_runs]

    total = len(plan)
    done = 0
    skipped = 0
    failed = 0

    header = (
        f"# EXP-001 run log\n\n"
        f"- started: {utc_now()}\n"
        f"- repo: `{repo}`\n"
        f"- skillsbench: `{skillsbench}` @ `{SKILLSBENCH_COMMIT}`\n"
        f"- agent/model: `{AGENT}` / `{MODEL}`\n"
        f"- planned runs: {total}\n\n"
    )
    if not run_log.exists():
        run_log.write_text(header, encoding="utf-8")
    else:
        with run_log.open("a", encoding="utf-8") as f:
            f.write(f"\n## Resume {utc_now()} (planned remaining scan of {total})\n\n")

    env = os.environ.copy()
    # Ensure uv/bench see the key without printing it
    if "ANTHROPIC_API_KEY" in env:
        env["ANTHROPIC_API_KEY"] = env["ANTHROPIC_API_KEY"]

    for idx, (task, condition, repeat) in enumerate(plan, start=1):
        folder = "control" if condition == "baseline" else "treatment"
        job_dir = jobs_root / folder / task / f"r{repeat}"
        if trial_done(job_dir):
            skipped += 1
            print(f"[{idx}/{total}] SKIP {condition} {task} r{repeat} (already complete)")
            continue

        cmd = build_bench_cmd(
            skillsbench=skillsbench,
            repo=repo,
            task=task,
            condition=condition,
            repeat=repeat,
            jobs_root=jobs_root,
            docker_via=args.docker_via,
        )
        print(f"[{idx}/{total}] RUN  {condition} {task} r{repeat}")
        if args.dry_run:
            print(" ", " ".join(cmd))
            continue

        t0 = time.time()
        # Prefer running from SkillsBench so uv uses that lockfile env
        if args.docker_via == "sg":
            cp = subprocess.run(cmd, cwd=str(skillsbench), env=env, text=True)
        else:
            cp = subprocess.run(cmd, cwd=str(skillsbench), env=env, text=True)
        elapsed = time.time() - t0
        ok = trial_done(job_dir)
        row = {
            "ts": utc_now(),
            "task": task,
            "condition": condition,
            "repeat": repeat,
            "exit_code": cp.returncode,
            "elapsed_sec": round(elapsed, 1),
            "healthy_complete": ok,
            "job_dir": str(job_dir.relative_to(repo)),
        }
        append_jsonl(progress, row)
        with run_log.open("a", encoding="utf-8") as f:
            status = "ok" if ok else "FAIL"
            f.write(
                f"- {row['ts']} `{condition}` `{task}` r{repeat}: {status} "
                f"(exit={cp.returncode}, {elapsed:.0f}s)\n"
            )
        if ok:
            done += 1
        else:
            failed += 1
            print(f"  WARNING: trial not healthy-complete (exit={cp.returncode})")

        # Refresh partial trials after each run for crash safety
        aggregate_trials(repo, jobs_root, trials_out)

    trials = aggregate_trials(repo, jobs_root, trials_out)
    print(
        f"finished scan: newly_ok≈{done} skipped={skipped} failed={failed} "
        f"aggregated={len(trials)} → {trials_out}"
    )
    print("Next: python3 scripts/compute_lift.py eval/runs/exp-001/trials.json "
          "--output eval/runs/exp-001/metrics.json")
    print("Do NOT fill pre-registration decision until metrics + coding are reviewed.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
