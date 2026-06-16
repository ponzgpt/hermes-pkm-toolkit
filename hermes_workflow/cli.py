"""Command-line entry point for generating a local-agent workflow plan."""

from __future__ import annotations

import argparse

from .planner import build_agent_plan


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a reviewable local LLM agent workflow plan."
    )
    parser.add_argument("objective", help="Automation objective to plan")
    parser.add_argument(
        "--backend",
        default="openai-compatible",
        help="Target backend label, for example ollama or openai-compatible",
    )
    parser.add_argument(
        "--context",
        action="append",
        default=[],
        help="Additional context line. Can be passed multiple times.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    plan = build_agent_plan(
        args.objective,
        backend=args.backend,
        extra_context=args.context,
    )
    print(plan.to_json())


if __name__ == "__main__":
    main()
