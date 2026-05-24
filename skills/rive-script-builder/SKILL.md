---
name: rive-script-builder
description: Build and revise Rive Luau scripts across Node, Layout, Converter, Path Effect, Transition Condition, Listener Action, Util, and Test protocols. Use when the user asks to write or modify Rive scripts, choose protocols, wire script inputs or data binding, debug runtime behavior, or plan unit tests for script logic.
metadata:
  author: "三秋十李Sergio"
  publisher: "RiveCN.com"
  website: "https://RiveCN.com"
  short-description: "Rive scripting skill by 三秋十李Sergio @ RiveCN.com"
---

# Rive Script Builder

Build accurate, runnable Rive Luau scripts. Optimize for correct protocol choice,
valid Luau signatures, editor wiring, and minimal user back-and-forth.

Knowledge policy:
- Use embedded essentials in this file and local references for common protocol work.
- Prefer Context7 MCP lookup for exact or uncertain API details (library: `/rive-app/rive-docs`).
- If Context7 is unavailable, fall back to `sync_rive_docs.py` online/cache/offline chain.
- Never invent APIs, lifecycle methods, or editor menus.

## Fast Operating Mode

- If the user explicitly asks to write/fix/review code and the protocol is clear, proceed directly with a small implementation.
- If one or two details are ambiguous, make reasonable assumptions and state them before the code.
- Ask questions only when the answer changes protocol choice, data ownership, or editor wiring.
- Use a pending plan and wait for approval only for broad/unclear requests, risky rewrites, or multi-script architecture.

## Critical Rive Runtime Context

- Rive scripts run in Rive's sandboxed Luau VM, not Roblox, browser JavaScript, or normal Lua.
- Do not use file I/O, network, `os.execute`, `loadstring`, Roblox globals, or shared mutable module state for attachable scripts.
- Script names should be PascalCase; the main exported type should match the script name when practical.
- Every attachable script returns a factory function that creates a fresh instance per attachment.
- Use `late()` for Rive objects created in `init`, editor-assigned references, `Input<Data.X>`, and other values initialized later.
- `Input<Trigger>` defaults to `function() end`, not `late()` or `nil`.
- Primitive `Input<T>` values are read directly, for example `self.speed`, not `self.speed.value`.
- Normal script inputs are effectively read-only from scripts. Runtime writes should go through ViewModel data.
- `Color` is immutable; channel helpers return new colors.
- Keep callbacks bounded and deterministic. Long synchronous loops can be killed by the runtime.

## Non-Negotiable Contract

1. Parse user goal and recommend protocol(s) first.
2. Ask only high-impact unresolved questions.
3. For unclear/risky tasks, provide a "pending implementation plan" before writing code.
4. Wait for explicit approval only when the task needs that pending plan.
5. For approved or already-clear implementation requests, output:
- Luau script code
- Rive editor wiring steps
- Debug and test suggestions
6. Follow the user's language automatically.
7. If approval is required but missing, do not output final script code.

## Workflow

### Phase 0: Live Docs Lookup (When Needed)

Lookup order when exact API confirmation is needed:

1. Context7 MCP (primary)
2. `scripts/sync_rive_docs.py` (secondary fallback)

Context7 MCP primary call:

```text
resolve-library-id -> /rive-app/rive-docs
query-docs(libraryId="/rive-app/rive-docs", query="<target API/protocol question>")
```

Query templates:
- `docs/context7-query-recipes.md`

Fallback lookup commands:

```bash
cd /path/to/rive-script-builder
python3 scripts/sync_rive_docs.py search --source auto --query "PathEffect"
python3 scripts/sync_rive_docs.py show --source auto --path scripting/protocols/path-effect-scripts.mdx
```

Optional cache prewarm (recommended, not required):

```bash
cd /path/to/rive-script-builder
python3 scripts/sync_rive_docs.py sync
```

Resolve `scripts/sync_rive_docs.py` relative to this `SKILL.md`; do not assume a fixed global skill directory.

`auto` fallback chain:
- `search`: online -> cache -> offline
- `show`: online -> cache

If fallback happens, keep the reason explicit in output.
See `docs/live-docs-workflow.md`.
Offline knowledge includes full upstream mirror at `docs/source-scripting/`.

### Phase 1: Scope and Route

- Identify target protocol using `docs/protocol-router.md`.
- Use `docs/api-signature-cheatsheet.md` to lock exact method signatures.
- If exact API details are ambiguous, check matching files in `docs/source-scripting/api-reference/`.
- For data-driven scripts, align with `docs/data-binding-deep-dive.md` and `docs/script-inputs-deep-dive.md`.
- If multiple protocols are needed, propose the smallest viable combination and explain why.
- State assumptions explicitly.

### Phase 2: Clarify Uncertainty

- Ask only questions that change implementation decisions.
- Use `docs/clarification-checklists.md`.
- For interaction-heavy requests, use `docs/pointer-events-playbook.md` to narrow unresolved event-routing details.
- Skip questions already answered by user context.

### Phase 3: Present Pending Plan

Use this phase only when the request is broad, underspecified, or likely to require multiple scripts.

Present this structure before coding:

- Goal understanding
- Recommended protocol(s) and rationale
- Assumptions and constraints
- Implementation outline (functions, inputs, data flow)
- Rive wiring steps
- Debug and test plan
- Explicit confirmation request

If user does not approve, keep refining plan only.

### Phase 4: Implement

- Generate minimal, runnable, typed Luau script first when the request is clear or approved.
- Extend with requested behavior only.
- Reuse templates from `references/scaffold-templates.md`.
- For common tasks, start from `references/case-recipes.md` and adapt.
- Keep protocol lifecycle contracts valid.

### Phase 5: Deliver With Integration Guidance

Always include:

- Final Luau code
- Editor wiring instructions (where to attach, bind, and run)
- Debug checklist (Problems and Console)
- Test suggestions (especially Test scripts for Util logic)

Use `docs/editor-wiring-recipes.md` and `docs/debug-test-playbook.md`.
Use `docs/path-api-performance-notes.md` for path-heavy scripts.
Use `docs/quality-gates.md` as final quality checklist.

## Protocol and API Guardrails

- Never invent lifecycle functions, interfaces, or editor paths.
- Prefer `Vector` as the canonical vector type; `Vec2D` may exist as an alias but should not be the default in generated code.
- `Node.update(self)` is for input-change recomputation. `PathEffect.update(self, inPath)` receives host path data and returns replacement path data.
- Luau uses `~=`, `and`, `or`, `not`; do not output JavaScript/C syntax such as `!=`, `&&`, `||`, or `!`.
- Do not use `import`/`export default`; use Rive's `require("UtilName")` and `return` patterns.
- Do not mutate state in `draw`; rebuild paths in `update` or before drawing in `advance`.
- Do not mutate or `reset()` a `Path` again in the same frame after drawing it.
- Keep `TransitionCondition.evaluate` fast and side-effect free.
- Use `ListenerAction.perform` for side effects.
- For `PathEffect`, keep `update` deterministic; use `advance` only for time-based behavior.
- Remember: scripts cannot set normal input values; use context or view model access for writable data.
- Bind strings to Text Runs, not parent Text objects.
- Remove long-lived listeners when no longer needed to avoid leaks.
- Check `docs/common-errors-and-fixes.md` before final handoff.
- If required details are missing, ask before coding.

## Output Format

When approval is needed:

- Understanding
- Open questions
- Pending plan
- Confirmation prompt

For direct implementation, or after approval:

- Script code
- Wiring steps
- Debug plan
- Test plan

## Docs and References Map

- Live docs sync and fallback rules: `docs/live-docs-workflow.md`
- Cross-platform publishing guidance: `docs/publish-cross-platform.md`
- Protocol routing and method contracts: `docs/protocol-router.md`
- Signature and API quick reference: `docs/api-signature-cheatsheet.md`
- Clarification questions by protocol: `docs/clarification-checklists.md`
- Data binding deep dive: `docs/data-binding-deep-dive.md`
- Script inputs deep dive: `docs/script-inputs-deep-dive.md`
- Pointer events playbook: `docs/pointer-events-playbook.md`
- Path API and performance notes: `docs/path-api-performance-notes.md`
- Final quality gates: `docs/quality-gates.md`
- Context7 query templates: `docs/context7-query-recipes.md`
- Full mirror index: `docs/source-scripting-index.md`
- Full upstream mirror folder: `docs/source-scripting/`
- Editor attach and binding steps: `docs/editor-wiring-recipes.md`
- Debug and test workflow: `docs/debug-test-playbook.md`
- Common errors and fixes: `docs/common-errors-and-fixes.md`
- Minimal Luau templates: `references/scaffold-templates.md`
- Practical case recipes: `references/case-recipes.md`
