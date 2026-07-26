#!/usr/bin/env python3
"""Compute paired lift metrics from a trials JSON/JSONL file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.metrics import compute_paired_metrics, trials_from_records


def load_trials(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise SystemExit(f"empty trials file: {path}")
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "trials" in data:
        return list(data["trials"])
    raise SystemExit("JSON must be a list of trials or an object with a 'trials' array")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trials_file", type=Path, help="JSON or JSONL trials file")
    parser.add_argument(
        "--success-threshold",
        type=float,
        default=1.0,
        help="Reward threshold counting as success (default: 1.0)",
    )
    parser.add_argument(
        "--regression-tolerance",
        type=float,
        default=0.0,
        help="Ignore regressions smaller than this delta (default: 0)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to write metrics JSON",
    )
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    records = load_trials(args.trials_file)
    trials = trials_from_records(records)
    metrics = compute_paired_metrics(
        trials,
        success_threshold=args.success_threshold,
        regression_tolerance=args.regression_tolerance,
    )
    payload = metrics.to_dict()

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not args.quiet:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif args.output:
        print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
