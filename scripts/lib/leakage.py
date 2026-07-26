"""Heuristics for task-leakage and integrity smells in skill packs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# Patterns that strongly suggest task-instance coupling or eval tampering.
LEAKAGE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("oracle_path", re.compile(r"\boracle/solve\.sh\b", re.I)),
    ("verifier_path", re.compile(r"\bverifier/test(?:_outputs)?\.(?:sh|py)\b", re.I)),
    ("reward_path", re.compile(r"/logs/verifier/reward\.txt", re.I)),
    ("tasks_tree", re.compile(r"\btasks/[a-z0-9][a-z0-9\-_]+/", re.I)),
    ("instruction_md", re.compile(r"\binstruction\.md\b", re.I)),
    ("grader_tamper", re.compile(r"\b(?:conftest\.py|sitecustomize\.py)\b", re.I)),
    ("sandbox_escape", re.compile(r"\b(?:sandbox escape|escape the sandbox)\b", re.I)),
    ("exfil_hint", re.compile(r"\b(?:exfiltrat|data exfil)\w*\b", re.I)),
]

# Soft smells — reported as warnings, not hard failures by default.
WARNING_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("harness_home_path", re.compile(r"~/\.(?:claude|codex|gemini)/skills", re.I)),
    ("absolute_root_skill", re.compile(r"/root/\.claude/skills/", re.I)),
]


@dataclass(frozen=True)
class LeakFinding:
    skill: str
    path: str
    code: str
    severity: str  # "error" | "warning"
    excerpt: str


def scan_text(skill_name: str, rel_path: str, text: str) -> list[LeakFinding]:
    findings: list[LeakFinding] = []
    for code, pattern in LEAKAGE_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(
                LeakFinding(
                    skill=skill_name,
                    path=rel_path,
                    code=code,
                    severity="error",
                    excerpt=_excerpt(text, match.start()),
                )
            )
    for code, pattern in WARNING_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(
                LeakFinding(
                    skill=skill_name,
                    path=rel_path,
                    code=code,
                    severity="warning",
                    excerpt=_excerpt(text, match.start()),
                )
            )
    return findings


def scan_skill_dir(skill_dir: Path, skill_name: str) -> list[LeakFinding]:
    findings: list[LeakFinding] = []
    skill_dir = Path(skill_dir)
    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".txt", ".py", ".sh", ".json", ".yml", ".yaml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(skill_dir).as_posix()
        findings.extend(scan_text(skill_name, rel, text))
    return findings


def _excerpt(text: str, index: int, radius: int = 60) -> str:
    start = max(0, index - radius)
    end = min(len(text), index + radius)
    snippet = text[start:end].replace("\n", " ")
    return snippet.strip()
