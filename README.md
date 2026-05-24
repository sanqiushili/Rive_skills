# Rive Skills

[简体中文](README.zh-CN.md)

> These skills come from [RiveCN](https://rivecn.com).

**Current version:** `rive-script-builder v2.0.0`

This repository publishes reusable Rive-related skills.  
Currently, it contains one skill: `rive-script-builder`.

## Structure

```text
.
├─ skills/
│  └─ rive-script-builder/
│     ├─ SKILL.md
│     ├─ agents/openai.yaml
│     ├─ docs/
│     ├─ references/
│     └─ scripts/
└─ .github/workflows/   # optional CI/release workflows
```

## rive-script-builder

`rive-script-builder` is a cross-agent skill for building and revising Rive Luau scripts. It uses a clarification-first workflow only when the request is underspecified or risky.

## Protocol Coverage

- Node
- Layout
- Converter
- Path Effect
- Transition Condition
- Listener Action
- Util
- Test

## Highlights

- Direct code output when the request is clear.
- Pending plans only when the request needs clarification or higher-risk decisions.
- Context7 MCP lookup first (`/rive-app/rive-docs`).
- Local docs/references fallback when MCP is unavailable.
- Includes wiring guidance, debugging checklist, and test suggestions.

## Recommended Prerequisite (Optional)

Install and configure Context7 MCP in your AI client before using this skill.
This is recommended, not required.

- Local MCP server command:
  ```bash
  npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
  ```
- Remote MCP endpoint:
  ```text
  https://mcp.context7.com/mcp
  ```
- Official setup guide: [Context7 Installation](https://context7.com/docs/installation)

## Install

Skills.sh-style install from your GitHub repository:

```bash
npx skills add https://github.com/sanqiushili/Rive_skills --skill rive-script-builder
```

If your skill is indexed on Skills, you can also use:

```bash
npx skills add https://github.com/sanqiushili/Rive_skills@rive-script-builder
```

Reference: [Skills CLI](https://skills.sh/docs/cli)

## Usage

1. Trigger in chat: `Use rive-script-builder`
2. Describe your target behavior and protocol context
3. Review clarification questions or a pending implementation plan if needed
4. Receive Luau code and wiring steps directly when the request is clear

## MCP Lookup (Default)

By default, the skill queries Rive docs through Context7 MCP:

```text
resolve-library-id -> /rive-app/rive-docs
query-docs(libraryId="/rive-app/rive-docs", query="<your API/protocol question>")
```

If MCP is unavailable, the skill falls back to:

```bash
python3 skills/rive-script-builder/scripts/sync_rive_docs.py search --source auto --query "PathEffect"
```

## Example Requests

- "Build a Path Effect script for rough crayon edges."
- "Refactor this Rive Converter and add reverseConvert."
- "Debug why my Transition Condition flickers."

## Maintainer

- Author: `三秋十李 Sergio`
- Publisher: `RiveCN.com`
- Website: `https://RiveCN.com`

## License

`skills/rive-script-builder` is licensed under CC BY 4.0. Attribution is required. See `LICENSE`.
