"""Command-line entry points for Hermes starter primitives."""

from __future__ import annotations

import argparse
import json

from .planner import build_agent_plan
from .primitives import filter_primitives
from .scaffold import build_scaffold_plan, write_scaffold


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Hermes-friendly local workspace primitives."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser(
        "plan", help="Generate a reviewable local LLM agent workflow plan."
    )
    plan_parser.add_argument("objective", help="Automation objective to plan")
    plan_parser.add_argument(
        "--backend",
        default="openai-compatible",
        help="Target backend label, for example ollama or openai-compatible",
    )
    plan_parser.add_argument(
        "--context",
        action="append",
        default=[],
        help="Additional context line. Can be passed multiple times.",
    )

    primitives_parser = subparsers.add_parser(
        "primitives", help="Print organization primitives as JSON."
    )
    primitives_parser.add_argument("--preset", default="starter")

    scaffold_parser = subparsers.add_parser(
        "scaffold", help="Preview or write a Hermes starter workspace."
    )
    scaffold_parser.add_argument("root", help="Workspace folder to create or preview")
    scaffold_parser.add_argument("--preset", default="starter")
    scaffold_parser.add_argument(
        "--write",
        action="store_true",
        help="Create folders plus HERMES.md and hermes-primitives.json.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.command == "plan":
        plan = build_agent_plan(
            args.objective,
            backend=args.backend,
            extra_context=args.context,
        )
        print(plan.to_json())
        return

    if args.command == "primitives":
        payload = [primitive.to_dict() for primitive in filter_primitives(args.preset)]
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    if args.command == "scaffold":
        plan = build_scaffold_plan(args.root, preset=args.preset)
        if args.write:
            created = write_scaffold(plan)
            for path in created:
                print(path)
        else:
            print(plan.manifest_json(), end="")
        return


if __name__ == "__main__":
    main()
