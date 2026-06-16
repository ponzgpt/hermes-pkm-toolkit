"""Lightweight Markdown file operations for local PKM agents.

The local filesystem is the only database. These helpers are deliberately
small, synchronous, and dependency-free so an agent runtime can wrap them
directly as function-calling tools.
"""

from __future__ import annotations

from pathlib import Path


class VaultPathError(ValueError):
    """Raised when a requested path escapes the configured vault root."""


def _resolve_vault_path(vault_root: str | Path, relative_path: str | Path) -> Path:
    root = Path(vault_root).expanduser().resolve()
    target = (root / relative_path).expanduser().resolve()
    if target != root and root not in target.parents:
        raise VaultPathError(f"path escapes vault root: {relative_path}")
    return target


def read_md(vault_root: str | Path, relative_path: str | Path) -> str:
    """Read a Markdown file from the vault."""
    path = _resolve_vault_path(vault_root, relative_path)
    if path.suffix.lower() != ".md":
        raise VaultPathError("read_md only reads .md files")
    return path.read_text(encoding="utf-8")


def append_md(
    vault_root: str | Path,
    relative_path: str | Path,
    content: str,
    *,
    create: bool = True,
) -> str:
    """Append Markdown content to a file and return the written path."""
    path = _resolve_vault_path(vault_root, relative_path)
    if path.suffix.lower() != ".md":
        raise VaultPathError("append_md only writes .md files")
    if not path.exists() and not create:
        raise FileNotFoundError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    prefix = "" if not path.exists() or path.stat().st_size == 0 else "\n"
    path.open("a", encoding="utf-8").write(prefix + content.rstrip() + "\n")
    return str(path)


def write_md(
    vault_root: str | Path,
    relative_path: str | Path,
    content: str,
    *,
    overwrite: bool = False,
) -> str:
    """Write a Markdown file and return the written path."""
    path = _resolve_vault_path(vault_root, relative_path)
    if path.suffix.lower() != ".md":
        raise VaultPathError("write_md only writes .md files")
    if path.exists() and not overwrite:
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return str(path)


def search_local(
    vault_root: str | Path,
    query: str,
    *,
    glob_pattern: str = "**/*.md",
    case_sensitive: bool = False,
    max_results: int = 25,
) -> list[dict[str, object]]:
    """Search Markdown files in the vault for a text query."""
    root = Path(vault_root).expanduser().resolve()
    needle = query if case_sensitive else query.lower()
    results: list[dict[str, object]] = []

    for path in sorted(root.glob(glob_pattern)):
        if not path.is_file() or path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        haystack = text if case_sensitive else text.lower()
        if needle not in haystack:
            continue
        line_matches = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            comparable = line if case_sensitive else line.lower()
            if needle in comparable:
                line_matches.append({"line": line_number, "text": line.strip()})
                if len(line_matches) >= 5:
                    break
        results.append(
            {
                "path": str(path.relative_to(root)),
                "matches": line_matches,
            }
        )
        if len(results) >= max_results:
            break

    return results
