# test-repo-hermes

Starter primitives for running Hermes agents against a simple local Git workspace.

`test-repo-hermes` is not trying to replace Hermes. Hermes is the local agent/runtime layer. This repo provides the small, boring, useful structure that a non-programmer can give Hermes on day one: folders, labels, prompt hints, and references based on Johnny.Decimal, PARA, and GTD.

## What this project does

The project turns well-known personal organization systems into code primitives that can be scaffolded into a local folder and committed to Git:

- **Johnny.Decimal primitives** for stable numbered places where files and notes can live.
- **PARA primitives** for projects, areas, resources, and archives.
- **GTD primitives** for capture, clarify, organize, reflect, and engage workflows.
- **Hermes prompt hints** so a local agent knows how to use the workspace without needing the user to be a programmer.

The current CLI generates a safe starter workspace. It does not call an LLM and it does not overwrite existing files unless a future command explicitly supports that.

## What this adds to Hermes

Hermes can run local agents, but a new user still needs a usable local operating system: where to put inputs, how to name work, what an agent should read first, and how to keep actions reviewable in Git.

This repository adds that missing starter layer:

1. A tiny Python implementation of organization primitives.
2. A scaffold command that creates a ready-to-commit workspace.
3. A `HERMES.md` instruction file that tells the agent how to work safely.
4. Tests that keep the structure deterministic as the project grows.

The intended user is someone who wants local AI automation but does not want to design an information architecture from scratch.

## Status

Early-stage, under active development. The current code is intentionally small and dependency-free so it can be audited easily and used as a foundation for future Hermes/OpenClaw/Ollama workflows.

## Getting started

Requirements:

- Python 3.10+
- No third-party dependencies

Clone and run the tests:

```bash
git clone https://github.com/ponzgpt/test-repo-hermes.git
cd test-repo-hermes
python3 -m unittest discover -s tests
```

Preview the starter primitives:

```bash
python3 -m hermes_workflow.cli primitives --preset starter
```

Create a local Hermes starter workspace:

```bash
python3 -m hermes_workflow.cli scaffold ./my-hermes-workspace --preset starter --write
```

The scaffold creates folders such as:

```text
my-hermes-workspace/
  HERMES.md
  00-inbox/
  10-19-operations/
  20-29-projects/
  30-39-areas/
  40-49-resources/
  90-99-archive/
  projects/
  areas/
  resources/
  archives/
  gtd/
```

## Example Hermes workflow

After scaffolding, open the generated workspace in Git and ask Hermes to:

```text
Read HERMES.md, inspect 00-inbox, and propose a GTD next-action list.
Do not move files yet. Produce a plan and Git diff first.
```

That gives the agent a small local map before it touches files. The user can review the plan, commit changes, or ask Hermes to refine the structure.

## References and licensing notes

This project implements lightweight interoperability primitives inspired by public descriptions of these systems. It does not copy proprietary templates, courses, diagrams, or paid materials.

- Johnny.Decimal: https://johnnydecimal.com/
- Johnny.Decimal introduction: https://johnnydecimal.com/documentation/introduction
- PARA method: https://fortelabs.com/blog/para/
- GTD overview: https://gettingthingsdone.com/what-is-gtd/

## Roadmap / planned features

- Add a richer Johnny.Decimal index generator for user-defined areas, categories, and IDs.
- Add PARA import helpers that can classify existing folders into projects, areas, resources, and archives.
- Add GTD inbox processing primitives for next actions, waiting-for, someday/maybe, and reference material.
- Add a Hermes runbook format for repeatable local agent sessions.
- Add examples for Ollama/OpenAI-compatible local endpoints once the workspace primitives are stable.

## How Codex will be used

Codex is useful here because this project is small, testable, and maintenance-heavy:

- refine primitives without breaking scaffold output;
- review pull requests for filesystem-safety regressions;
- generate tests for edge cases in folder names and user-provided labels;
- keep README examples and release notes accurate;
- run security sweeps before adding commands that write, move, or classify user files.

The intended workflow is issue-driven development, reviewed pull requests, and tests for each new primitive.

## License

MIT. See [LICENSE](LICENSE).
