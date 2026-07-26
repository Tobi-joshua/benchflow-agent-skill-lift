"""Skill library validation rules aligned with AGENTS.md gates."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from scripts.lib.leakage import LeakFinding, scan_skill_dir
from scripts.lib.skill_io import TOURIST_FILENAMES, SkillPack, discover_skills


@dataclass
class ValidationIssue:
    skill: str
    code: str
    severity: str
    message: str


@dataclass
class ValidationReport:
    library_dir: Path
    skill_count: int
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_library(
    library_dir: Path,
    *,
    max_description_words: int = 120,
    max_body_words: int = 2500,
    allow_empty: bool = True,
) -> ValidationReport:
    library_dir = Path(library_dir)
    report = ValidationReport(library_dir=library_dir, skill_count=0)

    if not library_dir.is_dir():
        report.issues.append(
            ValidationIssue(
                skill="*",
                code="missing_library",
                severity="error",
                message=f"library directory does not exist: {library_dir}",
            )
        )
        return report

    packs = discover_skills(library_dir)
    report.skill_count = len(packs)
    if not packs and not allow_empty:
        report.issues.append(
            ValidationIssue(
                skill="*",
                code="empty_library",
                severity="error",
                message="library contains no skill packs",
            )
        )
        return report

    seen_names: dict[str, str] = {}
    for pack in packs:
        _validate_pack(
            pack,
            report,
            max_description_words=max_description_words,
            max_body_words=max_body_words,
        )
        prev = seen_names.get(pack.name)
        if prev:
            report.issues.append(
                ValidationIssue(
                    skill=pack.name,
                    code="duplicate_name",
                    severity="error",
                    message=f"duplicate skill name {pack.name!r} in {prev} and {pack.path.name}",
                )
            )
        else:
            seen_names[pack.name] = pack.path.name

    return report


def _validate_pack(
    pack: SkillPack,
    report: ValidationReport,
    *,
    max_description_words: int,
    max_body_words: int,
) -> None:
    if pack.name != pack.path.name:
        report.issues.append(
            ValidationIssue(
                skill=pack.path.name,
                code="name_mismatch",
                severity="error",
                message=f"frontmatter name {pack.name!r} != directory {pack.path.name!r}",
            )
        )
    if not pack.description:
        report.issues.append(
            ValidationIssue(
                skill=pack.path.name,
                code="missing_description",
                severity="error",
                message="frontmatter description is required (router text)",
            )
        )
    elif "use when" not in pack.description.lower() and "when" not in pack.description.lower():
        report.issues.append(
            ValidationIssue(
                skill=pack.path.name,
                code="weak_description_trigger",
                severity="warning",
                message="description should include when-to-use / trigger guidance",
            )
        )

    counts = pack.word_counts()
    if counts["description_words"] > max_description_words:
        report.issues.append(
            ValidationIssue(
                skill=pack.path.name,
                code="description_too_long",
                severity="warning",
                message=f"description has {counts['description_words']} words (budget {max_description_words})",
            )
        )
    if counts["body_words"] > max_body_words:
        report.issues.append(
            ValidationIssue(
                skill=pack.path.name,
                code="body_too_long",
                severity="warning",
                message=f"body has {counts['body_words']} words (budget {max_body_words})",
            )
        )

    for path in pack.path.iterdir():
        if path.is_file() and path.name.lower() in TOURIST_FILENAMES:
            report.issues.append(
                ValidationIssue(
                    skill=pack.path.name,
                    code="tourist_file",
                    severity="error",
                    message=f"disallowed tourist file inside skill pack: {path.name}",
                )
            )

    for finding in scan_skill_dir(pack.path, pack.path.name):
        report.issues.append(_from_leak(finding))


def _from_leak(finding: LeakFinding) -> ValidationIssue:
    return ValidationIssue(
        skill=finding.skill,
        code=f"leak:{finding.code}",
        severity=finding.severity,
        message=f"{finding.path}: {finding.excerpt}",
    )
