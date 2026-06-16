# Hermes-PKM-Toolkit

Modular cognitive protocols for local-first AI agents working on plain-text PKM vaults.

Hermes-PKM-Toolkit is a small library of system prompts, file-operation tools, and framework-specific directives for agents such as Hermes or Moltbot. It helps an agent work inside Markdown/Obsidian-style folders without introducing a database, backend service, or hidden state.

The local filesystem is the database. Git is the audit log. Markdown is the interface.

## Philosophy

- **A la carte modules:** load only GTD, only Johnny.Decimal, only PARA, or any combination.
- **Plain text first:** everything important is visible as `.md`, `.json`, or Python source.
- **Agent-readable and human-readable:** every module contains human guidance and agent instructions.
- **No heavy infrastructure:** no SQL, no vector database, no server requirement.
- **Review before mutation:** agents should propose moves, writes, and archive operations before applying them.

## Repository layout

```text
Hermes-PKM-Toolkit/
  00_CORE/
    hermes_base_system_prompt.md
    file_ops.py
    generic_file_ops_tools.json
  01_JOHNNY_DECIMAL/
    HUMANS_jd_guide.md
    AGENT_jd_instructions.md
    jd_routing_tools.json
  02_GTD/
    HUMANS_gtd_guide.md
    AGENT_gtd_instructions.md
    gtd_triage_tools.json
  03_PARA/
    HUMANS_para_guide.md
    AGENT_para_instructions.md
    para_archiving_tools.json
```

## How to integrate with a local agent

1. Load `00_CORE/hermes_base_system_prompt.md` as the base system prompt.
2. Expose `00_CORE/file_ops.py` through the JSON schemas in `00_CORE/generic_file_ops_tools.json`.
3. Add one or more module overrides:
   - `01_JOHNNY_DECIMAL/AGENT_jd_instructions.md`
   - `02_GTD/AGENT_gtd_instructions.md`
   - `03_PARA/AGENT_para_instructions.md`
4. Register the module-specific tool schemas if your agent runtime supports function calling.
5. Point the agent at a local Markdown vault, ideally under Git.

Example stack:

```text
Hermes agent
  + base system prompt
  + GTD instructions
  + Johnny.Decimal instructions
  + generic file tools
  + GTD/JD tool schemas
  -> local Obsidian vault in iCloud/Dropbox/local disk
  -> Git commits for reviewable changes
```

## Tool schema format

Tool definitions use an OpenAI-style function calling shape:

```json
{
  "type": "function",
  "function": {
    "name": "read_md",
    "description": "Read a Markdown file from the local vault.",
    "parameters": {
      "type": "object",
      "properties": {},
      "required": []
    }
  }
}
```

The schemas are intentionally runtime-neutral. Hermes, Moltbot, or another local agent can map them to Python handlers, MCP tools, shell wrappers, or native function calls.

## Module selection

| Use case | Load modules |
|---|---|
| Quick capture and next actions | `00_CORE` + `02_GTD` |
| Structured knowledge vault | `00_CORE` + `01_JOHNNY_DECIMAL` |
| Project/resource management | `00_CORE` + `03_PARA` |
| Full local PKM operating system | `00_CORE` + all modules |

## Safety model

- Treat every write, move, rename, and archive as a proposed diff.
- Never invent top-level folder systems without user confirmation.
- Never delete content through these primitives.
- Prefer appending to inboxes and logs over destructive rewrites.
- Keep secrets out of prompts, logs, and committed files.
- Use Git commits as checkpoints when an agent changes the vault.

## Status

Early-stage toolkit for local agent workflows in the Machines Do It Better ecosystem. The current scope is deliberately small: prompts, JSON tool schemas, and safe Python file primitives.

## License

MIT. See `LICENSE`.
