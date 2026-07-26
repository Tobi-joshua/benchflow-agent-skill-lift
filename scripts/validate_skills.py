#!/usr/bin/env python3
"""Validate a skill library for structure, triggers, and leakage smells."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.validate import validate_library


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=ROOT / "skills",
        help="Skill library directory (default: ./skills)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON report",
    )
    parser.add_argument(
        "--strict-empty",
        action="store_true",
        help="Fail if the library has zero skills",
    )
    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Exit non-zero when warnings are present",
    )
    args = parser.parse_args(argv)

    report = validate_library(args.skills_dir, allow_empty=not args.strict_empty)
    payload = {
        "library_dir": str(report.library_dir),
        "skill_count": report.skill_count,
        "ok": report.ok and not (args.fail_on_warning and report.warnings),
        "errors": [i.__dict__ for i in report.errors],
        "warnings": [i.__dict__ for i in report.warnings],
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"library: {report.library_dir}")
        print(f"skills:  {report.skill_count}")
        if not report.issues:
            print("ok: no issues")
        for issue in report.issues:
            print(f"{issue.severity.upper()}: [{issue.skill}] {issue.code}: {issue.message}")

    if not report.ok:
        return 1
    if args.fail_on_warning and report.warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
