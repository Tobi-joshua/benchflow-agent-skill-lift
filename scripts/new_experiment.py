#!/usr/bin/env python3
"""Create a pre-registration experiment record (EXPERIMENT_PROTOCOL.md)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.skill_io import library_content_hash

EXPERIMENTS_DIR = ROOT / "eval" / "experiments"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def next_experiment_id(day: date, slug: str, experiments_dir: Path) -> str:
    prefix = f"exp-{day.strftime('%Y%m%d')}-{slug}-"
    existing = []
    if experiments_dir.is_dir():
        for path in experiments_dir.glob(f"{prefix}*.json"):
            suffix = path.stem[len(prefix) :]
            if suffix.isdigit():
                existing.append(int(suffix))
    seq = max(existing, default=0) + 1
    return f"{prefix}{seq:02d}"


def build_record(
    *,
    experiment_id: str,
    hypothesis: str,
    mechanism: str,
    experiment_type: str,
    primary_metric: str,
    acceptance_threshold: str,
    rejection_condition: str,
    target_tasks: list[str],
    safety_risks: list[str],
    agent: str,
    model: str,
    skills_dir: Path | None,
    notes: str,
) -> dict:
    skills_hash = library_content_hash(skills_dir) if skills_dir and skills_dir.is_dir() else None
    return {
        "experiment_id": experiment_id,
        "status": "pre-registered",
        "date": date.today().isoformat(),
        "experiment_type": experiment_type,
        "hypothesis": hypothesis,
        "expected_mechanism": mechanism,
        "target_tasks": target_tasks,
        "primary_metric": primary_metric,
        "acceptance_threshold": acceptance_threshold,
        "rejection_condition": rejection_condition,
        "safety_risks": safety_risks,
        "controls": {
            "agent": agent,
            "model": model,
            "environment": "TBD",
            "baseline_skill_config": "empty / no-skill",
            "treatment_skill_config": str(skills_dir) if skills_dir else "TBD",
            "treatment_content_sha256": skills_hash,
        },
        "replication": {"R": 3, "notes": "See docs/EXPERIMENT_PROTOCOL.md"},
        "results": None,
        "failure_analysis": [],
        "decision": None,
        "notes": notes,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True, help="kebab-case slug, e.g. safety-core")
    parser.add_argument("--hypothesis", required=True)
    parser.add_argument("--mechanism", required=True)
    parser.add_argument(
        "--type",
        dest="experiment_type",
        default="single-skill",
        choices=[
            "baseline",
            "single-skill",
            "skill-combination",
            "trigger-quality",
            "ablation",
            "regression",
            "leave-one-domain-out",
            "safety-stress",
        ],
    )
    parser.add_argument("--primary-metric", default="absolute_lift")
    parser.add_argument(
        "--acceptance-threshold",
        default="absolute_lift > 0 on target set; regression_rate <= 0.15",
    )
    parser.add_argument(
        "--rejection-condition",
        default="critical safety regression OR leakage OR single-task-only lift",
    )
    parser.add_argument(
        "--target-tasks",
        default="",
        help="Comma-separated task IDs or class labels",
    )
    parser.add_argument(
        "--safety-risks",
        default="",
        help="Comma-separated hazard notes",
    )
    parser.add_argument("--agent", default="TBD")
    parser.add_argument("--model", default="TBD")
    parser.add_argument("--skills-dir", type=Path, default=None)
    parser.add_argument("--notes", default="")
    parser.add_argument(
        "--experiments-dir",
        type=Path,
        default=EXPERIMENTS_DIR,
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    slug = args.slug.strip().lower()
    if not SLUG_RE.match(slug):
        raise SystemExit("--slug must be lowercase kebab-case (a-z0-9-)")

    args.experiments_dir.mkdir(parents=True, exist_ok=True)
    experiment_id = next_experiment_id(date.today(), slug, args.experiments_dir)
    record = build_record(
        experiment_id=experiment_id,
        hypothesis=args.hypothesis,
        mechanism=args.mechanism,
        experiment_type=args.experiment_type,
        primary_metric=args.primary_metric,
        acceptance_threshold=args.acceptance_threshold,
        rejection_condition=args.rejection_condition,
        target_tasks=[t.strip() for t in args.target_tasks.split(",") if t.strip()],
        safety_risks=[t.strip() for t in args.safety_risks.split(",") if t.strip()],
        agent=args.agent,
        model=args.model,
        skills_dir=args.skills_dir,
        notes=args.notes,
    )

    out = args.experiments_dir / f"{experiment_id}.json"
    if args.dry_run:
        print(json.dumps(record, indent=2, sort_keys=True))
        return 0

    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
