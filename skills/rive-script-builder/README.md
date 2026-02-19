# rive-script-builder

[中文说明](README.zh-CN.md)

`rive-script-builder` is a cross-agent skill for generating and revising Rive Luau scripts with a clarification-first workflow.

## Highlights

- Protocol routing for Node, Layout, Converter, Path Effect, Transition Condition, Listener Action, Util, and Test.
- Explicit approval gate before code generation.
- Offline-first references with optional live docs sync.
- Debug/testing and editor wiring guides included.

## Install

Install from npm skill package:

```bash
npx skills add rive-script-builder-skill
```

Or install from a GitHub skill folder supported by your agent runtime.

## Quick Start (3 lines)

```text
1) Run: npx skills add rive-script-builder-skill
2) In chat: "Use rive-script-builder"
3) Ask: "Build a Path Effect script for rough crayon edges"
```

## Use

Trigger with `rive-script-builder` in your prompt, then follow the clarification and approval flow.

Example requests:

- "Build a Path Effect script for rough crayon edges."
- "Refactor this Rive Converter and add reverseConvert."
- "Debug why my Transition Condition flickers."

Optional live docs sync:

```bash
python3 scripts/sync_rive_docs.py sync
python3 scripts/sync_rive_docs.py search --query "PathEffect"
```

## Maintainer

- Author: `三秋十李 Sergio`
- Publisher: `RiveCN.com`
- Website: `https://RiveCN.com`

## License

MIT. See [LICENSE](LICENSE).
