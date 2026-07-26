"""Minimal YAML frontmatter parser for SKILL.md (stdlib only)."""

from __future__ import annotations

from typing import Any


class FrontmatterError(ValueError):
    """Raised when frontmatter is missing or unparsable."""


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse leading ``---`` frontmatter into a flat dict and body string.

    Supports simple ``key: value`` scalars and single-level nested maps under
    ``metadata:``. This is intentionally narrow — skill packs must keep
    frontmatter simple for harness portability.
    """
    if not text.startswith("---"):
        raise FrontmatterError("SKILL.md must start with YAML frontmatter (---)")

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("SKILL.md must start with YAML frontmatter (---)")

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise FrontmatterError("Unterminated frontmatter block")

    meta: dict[str, Any] = {}
    current_map: dict[str, Any] | None = None
    current_key: str | None = None

    for raw in lines[1:end]:
        if not raw.strip():
            continue
        if raw.startswith(" ") or raw.startswith("\t"):
            if current_map is None or current_key is None:
                raise FrontmatterError(f"Unexpected indented line: {raw!r}")
            if ":" not in raw:
                raise FrontmatterError(f"Invalid nested frontmatter line: {raw!r}")
            nested_key, nested_val = raw.split(":", 1)
            current_map[nested_key.strip()] = _parse_scalar(nested_val.strip())
            continue

        if ":" not in raw:
            raise FrontmatterError(f"Invalid frontmatter line: {raw!r}")
        key, val = raw.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val == "":
            current_key = key
            current_map = {}
            meta[key] = current_map
        else:
            current_key = None
            current_map = None
            meta[key] = _parse_scalar(val)

    body = "\n".join(lines[end + 1 :])
    if body.startswith("\n"):
        body = body[1:]
    return meta, body


def _parse_scalar(value: str) -> Any:
    if value == "":
        return ""
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    lower = value.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    if lower == "null" or lower == "~":
        return None
    try:
        if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
            return int(value)
    except ValueError:
        pass
    return value
