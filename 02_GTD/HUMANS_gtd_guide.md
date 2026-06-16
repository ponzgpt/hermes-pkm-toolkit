# GTD module guide

Use this module when the user needs fast capture and trusted follow-up.

GTD is useful for chaotic input: ideas, tasks, messages, obligations, and open loops. The agent's first job is not to organize perfectly. It is to capture reliably, clarify later, and keep next actions visible.

## What this module provides

- A simple inbox-first operating mode.
- Agent instructions for appending tasks as Markdown checkboxes.
- A function-calling schema for adding items with optional context tags.

## Minimal files

```text
00_Inbox.md
Next_Actions.md
Waiting_For.md
Someday_Maybe.md
Reference.md
```

The only required file is `00_Inbox.md`. Other files can be created after the user approves the workflow.

## When to use

- The user is overwhelmed.
- The user needs quick capture from voice, chat, or notes.
- The agent should not decide structure yet.
- Tasks need context tags such as `@home`, `@computer`, `@errand`, or `@waiting`.

## Recommended workflow

1. Capture everything into `00_Inbox.md`.
2. Use checkboxes for actionable items.
3. Add context tags only when obvious.
4. During triage, classify each item as next action, waiting-for, someday/maybe, calendar, project, or reference.
5. Ask before moving items out of the inbox.

Reference: https://gettingthingsdone.com/what-is-gtd/
