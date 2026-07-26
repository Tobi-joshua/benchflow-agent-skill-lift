#!/usr/bin/env python3
"""Package skills/ into a Track-1 submission.zip (skills/ root layout)."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.skill_io import discover_skills, library_content_hash
from scripts.lib.validate import validate_library


def build_zip(skills_dir: Path, output: Path, *, skip_validate: bool = False) -> dict:
    skills_dir = skills_dir.resolve()
    if not skip_validate:
        report = validate_library(skills_dir, allow_empty=False)
        if not report.ok:
            errors = "; ".join(f"{i.skill}:{i.code}" for i in report.errors)
            raise SystemExit(f"validation failed: {errors}")

    packs = discover_skills(skills_dir)
    if not packs:
        raise SystemExit(f"no skills found under {skills_dir}")

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    written: list[str] = []
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(skills_dir.rglob("*")):
            if not path.is_file():
                continue
            if path.name == ".gitkeep":
                continue
            rel = path.relative_to(skills_dir).as_posix()
            arcname = f"skills/{rel}"
            zf.write(path, arcname=arcname)
            written.append(arcname)

    manifest = {
        "output": str(output),
        "skills_dir": str(skills_dir),
        "skill_count": len(packs),
        "skill_names": [p.name for p in packs],
        "content_sha256": library_content_hash(skills_dir),
        "files": written,
    }
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=ROOT / "skills")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "dist" / "submission.zip",
        help="Output zip path (default: dist/submission.zip)",
    )
    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="Package even if validation errors exist (not for release)",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    manifest = build_zip(args.skills_dir, args.output, skip_validate=args.skip_validate)
    if args.json:
        print(json.dumps(manifest, indent=2, sort_keys=True))
    else:
        print(f"wrote {manifest['output']}")
        print(f"skills: {', '.join(manifest['skill_names'])}")
        print(f"sha256: {manifest['content_sha256']}")
        print(f"files:  {len(manifest['files'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
