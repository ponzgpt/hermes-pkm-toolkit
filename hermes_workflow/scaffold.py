"""Scaffold a Hermes-friendly local workspace."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from .primitives import Primitive, filter_primitives


@dataclass(frozen=True)
class ScaffoldPlan:
    """A filesystem scaffold that can be previewed or written."""

    root: Path
    preset: str
    primitives: tuple[Primitive, ...]

    def directories(self) -> tuple[Path, ...]:
        return tuple(self.root / primitive.path for primitive in self.primitives)

    def hermes_markdown(self) -> str:
        lines = [
            "# HERMES.md",
            "",
            "This workspace is organized with starter primitives from `test-repo-hermes`.",
            "Hermes should inspect this file before moving, renaming, or classifying files.",
            "",
            "## Operating rules",
            "",
            "- Start with `00-inbox` for unprocessed material.",
            "- Propose a plan before moving files.",
            "- Prefer small Git commits that the user can review.",
            "- Do not delete or archive material without explicit approval.",
            "- Keep secrets out of prompts, logs, and committed files.",
            "",
            "## Primitives",
            "",
        ]
        for primitive in self.primitives:
            lines.extend(
                [
                    f"### {primitive.path} - {primitive.title}",
                    "",
                    f"- System: `{primitive.system}`",
                    f"- Key: `{primitive.key}`",
                    f"- Purpose: {primitive.purpose}",
                    f"- Agent hint: {primitive.agent_hint}",
                    "",
                ]
            )
        return "\n".join(lines).rstrip() + "\n"

    def manifest_json(self) -> str:
        payload = {
            "preset": self.preset,
            "directories": [str(path.relative_to(self.root)) for path in self.directories()],
            "primitives": [primitive.to_dict() for primitive in self.primitives],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def build_scaffold_plan(root: str | Path, preset: str = "starter") -> ScaffoldPlan:
    return ScaffoldPlan(
        root=Path(root),
        preset=preset,
        primitives=filter_primitives(preset),
    )


def write_scaffold(plan: ScaffoldPlan) -> list[Path]:
    """Write a scaffold without overwriting existing files."""
    created: list[Path] = []
    plan.root.mkdir(parents=True, exist_ok=True)

    for directory in plan.directories():
        directory.mkdir(parents=True, exist_ok=True)
        created.append(directory)

    files = {
        plan.root / "HERMES.md": plan.hermes_markdown(),
        plan.root / "hermes-primitives.json": plan.manifest_json(),
    }
    for path, content in files.items():
        if path.exists():
            raise FileExistsError(f"{path} already exists")
        path.write_text(content, encoding="utf-8")
        created.append(path)

    return created
