"""Organization primitives for Hermes-friendly local workspaces.

These primitives encode simple structure and prompt hints. They do not claim to
be complete implementations of Johnny.Decimal, PARA, or GTD.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from pathlib import Path


SAFE_NAME_RE = re.compile(r"[^a-z0-9._-]+")


@dataclass(frozen=True)
class Primitive:
    """A folder, label, or instruction that a Hermes agent can use."""

    system: str
    key: str
    title: str
    path: str
    purpose: str
    agent_hint: str
    references: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


REFERENCES = {
    "johnny-decimal": (
        "https://johnnydecimal.com/",
        "https://johnnydecimal.com/documentation/introduction",
    ),
    "para": ("https://fortelabs.com/blog/para/",),
    "gtd": ("https://gettingthingsdone.com/what-is-gtd/",),
}


def slugify(value: str) -> str:
    """Return a conservative filesystem-safe slug."""
    clean = SAFE_NAME_RE.sub("-", value.strip().lower()).strip("-")
    return clean or "untitled"


def starter_primitives() -> tuple[Primitive, ...]:
    """Return a small default set for a new Hermes + Git workspace."""
    return (
        Primitive(
            system="inbox",
            key="00",
            title="Inbox",
            path="00-inbox",
            purpose="Default landing zone for unprocessed notes, files, and ideas.",
            agent_hint="Start here. Summarize what arrived, then propose where each item should go before moving anything.",
        ),
        Primitive(
            system="johnny-decimal",
            key="10-19",
            title="Operations",
            path="10-19-operations",
            purpose="Stable numbered area for recurring personal systems and admin work.",
            agent_hint="Use this for durable operating procedures, indexes, and recurring workflows.",
            references=REFERENCES["johnny-decimal"],
        ),
        Primitive(
            system="johnny-decimal",
            key="20-29",
            title="Projects",
            path="20-29-projects",
            purpose="Stable numbered area for active outcomes with a finish line.",
            agent_hint="Link each active project to a PARA project folder when the user needs more detail.",
            references=REFERENCES["johnny-decimal"],
        ),
        Primitive(
            system="johnny-decimal",
            key="30-39",
            title="Areas",
            path="30-39-areas",
            purpose="Stable numbered area for ongoing responsibilities.",
            agent_hint="Use for responsibilities that need maintenance but do not have a clear end date.",
            references=REFERENCES["johnny-decimal"],
        ),
        Primitive(
            system="johnny-decimal",
            key="40-49",
            title="Resources",
            path="40-49-resources",
            purpose="Stable numbered area for reference topics and reusable material.",
            agent_hint="Use for reusable knowledge that supports future work.",
            references=REFERENCES["johnny-decimal"],
        ),
        Primitive(
            system="johnny-decimal",
            key="90-99",
            title="Archive",
            path="90-99-archive",
            purpose="Stable numbered area for inactive or completed material.",
            agent_hint="Move things here only after the user approves the archive plan.",
            references=REFERENCES["johnny-decimal"],
        ),
        Primitive(
            system="para",
            key="projects",
            title="PARA Projects",
            path="projects",
            purpose="Active efforts with defined outcomes.",
            agent_hint="Prefer this for current work that should produce a concrete result.",
            references=REFERENCES["para"],
        ),
        Primitive(
            system="para",
            key="areas",
            title="PARA Areas",
            path="areas",
            purpose="Ongoing standards or responsibilities to maintain.",
            agent_hint="Use this when the work is continuous rather than finishable.",
            references=REFERENCES["para"],
        ),
        Primitive(
            system="para",
            key="resources",
            title="PARA Resources",
            path="resources",
            purpose="Reference material grouped by topic or interest.",
            agent_hint="Use this for material that may support many future projects.",
            references=REFERENCES["para"],
        ),
        Primitive(
            system="para",
            key="archives",
            title="PARA Archives",
            path="archives",
            purpose="Inactive items from the other PARA groups.",
            agent_hint="Archive only after confirming that the item is inactive.",
            references=REFERENCES["para"],
        ),
        Primitive(
            system="gtd",
            key="workflow",
            title="GTD Workflow",
            path="gtd",
            purpose="Capture, clarify, organize, reflect, and engage with commitments.",
            agent_hint="Turn inbox items into next actions, waiting-for items, someday/maybe items, or reference notes.",
            references=REFERENCES["gtd"],
        ),
    )


def filter_primitives(preset: str) -> tuple[Primitive, ...]:
    """Return primitives for a known preset."""
    if preset != "starter":
        raise ValueError(f"unknown preset: {preset}")
    return starter_primitives()


def primitive_paths(preset: str = "starter") -> tuple[Path, ...]:
    """Return relative folder paths for a preset."""
    return tuple(Path(item.path) for item in filter_primitives(preset))
