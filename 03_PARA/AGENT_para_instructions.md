# Agent override: PARA routing

Load this instruction when the user wants Hermes to organize material with PARA.

## Core behavior

Route by actionability, not by topic first.

## Decision tree

1. Does this support a current outcome with a finish line?
   - Route to `1-Projects`.
2. Is this an ongoing responsibility or standard to maintain?
   - Route to `2-Areas`.
3. Is this reference material that may support future work?
   - Route to `3-Resources`.
4. Is this inactive, completed, or no longer needed for current work?
   - Propose `4-Archives`.

## Project spin-up policy

When creating a project, include:

- project name;
- desired outcome;
- next action;
- related area, if any;
- review date, if known.

## Archive policy

Do not archive automatically. Always show:

- source path;
- archive destination;
- why it appears inactive;
- what links or references may break.

Use `spin_up_project` to create a new project structure. Use `move_to_archive` only after explicit approval.
