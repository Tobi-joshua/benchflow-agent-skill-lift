#!/usr/bin/env python3
"""Print a stable content hash for a skill library directory."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.skill_io import library_content_hash


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=ROOT / "skills")
    args = parser.parse_args(argv)
    print(library_content_hash(args.skills_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
