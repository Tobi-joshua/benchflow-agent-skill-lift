"""Discover and load Agent Skill packs from a library directory."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from scripts.lib.frontmatter import FrontmatterError, parse_frontmatter

TOURIST_FILENAMES = frozenset(
    {
        "readme.md",
        "changelog.md",
        "installation_guide.md",
        "quick_reference.md",
        "contributing.md",
    }
)


@dataclass(frozen=True)
class SkillPack:
    """One skill directory with parsed SKILL.md metadata."""

    path: Path
    name: str
    description: str
    body: str
    frontmatter: dict = field(default_factory=dict)

    @property
    def skill_md(self) -> Path:
        return self.path / "SKILL.md"

    def word_counts(self) -> dict[str, int]:
        return {
            "description_words": len(self.description.split()),
            "body_words": len(self.body.split()),
        }


def discover_skills(library_dir: Path) -> list[SkillPack]:
    """Return skill packs under ``library_dir/*/SKILL.md``, sorted by name."""
    library_dir = Path(library_dir)
    if not library_dir.is_dir():
        raise FileNotFoundError(f"skills library not found: {library_dir}")

    packs: list[SkillPack] = []
    for skill_md in sorted(library_dir.glob("*/SKILL.md")):
        packs.append(load_skill(skill_md.parent))
    return packs


def load_skill(skill_dir: Path) -> SkillPack:
    skill_dir = Path(skill_dir)
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise FileNotFoundError(f"missing SKILL.md: {skill_md}")

    text = skill_md.read_text(encoding="utf-8")
    try:
        meta, body = parse_frontmatter(text)
    except FrontmatterError as exc:
        raise FrontmatterError(f"{skill_md}: {exc}") from exc

    name = str(meta.get("name") or "").strip()
    description = str(meta.get("description") or "").strip()
    if not name:
        name = skill_dir.name
    return SkillPack(
        path=skill_dir.resolve(),
        name=name,
        description=description,
        body=body,
        frontmatter=meta,
    )


def iter_skill_files(skill_dir: Path) -> Iterator[Path]:
    """Yield files under a skill pack (files only)."""
    skill_dir = Path(skill_dir)
    for path in sorted(skill_dir.rglob("*")):
        if path.is_file():
            yield path


def library_content_hash(library_dir: Path) -> str:
    """Stable SHA-256 over relative paths and file bytes in a library."""
    import hashlib

    library_dir = Path(library_dir).resolve()
    digest = hashlib.sha256()
    if not library_dir.is_dir():
        digest.update(b"missing")
        return digest.hexdigest()

    paths = [p for p in library_dir.rglob("*") if p.is_file()]
    for path in sorted(paths, key=lambda p: p.relative_to(library_dir).as_posix()):
        rel = path.relative_to(library_dir).as_posix()
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()
