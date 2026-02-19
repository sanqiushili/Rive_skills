---
name: rive-script-builder
description: Build and revise Rive Luau scripts across Node, Layout, Converter, Path Effect, Transition Condition, Listener Action, Util, and Test protocols. Use when the user asks to write or modify Rive scripts, choose protocols, wire script inputs or data binding, debug runtime behavior, or plan unit tests for script logic.
metadata:
  author: "三秋十李 Sergio"
  publisher: "RiveCN.com"
  website: "https://RiveCN.com"
  short-description: "Rive scripting skill by 三秋十李 Sergio @ RiveCN.com"
---

# Rive Script Builder

Build Rive Luau scripts with a strict clarification-first workflow.

Knowledge policy:
- Prefer local skill references in this folder first (offline-safe mode).
- When network is available, refresh from GitHub docs snapshot before coding.
- Never invent APIs, lifecycle methods, or editor menus.

## Non-Negotiable Contract

1. Parse user goal and recommend protocol(s) first.
2. Ask only high-impact unresolved questions.
3. Provide a "pending implementation plan" before writing code.
4. Wait for explicit approval (for example: "同意", "开始写", "approved", "go ahead").
5. After approval, output:
- Luau script code
- Rive editor wiring steps
- Debug and test suggestions
6. Follow the user's language automatically.
7. If approval is missing, do not output final script code.

## Workflow

### Phase 0: Refresh Live Docs (Recommended)

Try to refresh docs snapshot before implementation:

```bash
python3 "$CODEX_HOME/skills/rive-script-builder/scripts/sync_rive_docs.py" sync
```

Then query needed details:

```bash
python3 "$CODEX_HOME/skills/rive-script-builder/scripts/sync_rive_docs.py" search --query "PathEffect"
python3 "$CODEX_HOME/skills/rive-script-builder/scripts/sync_rive_docs.py" show --path scripting/protocols/path-effect-scripts.mdx
```

If sync fails, continue with offline references and state fallback explicitly.
See `references/live-docs-workflow.md`.

### Phase 1: Scope and Route

- Identify target protocol using `references/protocol-router.md`.
- Use `references/api-signature-cheatsheet.md` to lock exact method signatures.
- If multiple protocols are needed, propose the smallest viable combination and explain why.
- State assumptions explicitly.

### Phase 2: Clarify Uncertainty

- Ask only questions that change implementation decisions.
- Use `references/clarification-checklists.md`.
- Skip questions already answered by user context.

### Phase 3: Present Pending Plan

Present this structure before coding:

- Goal understanding
- Recommended protocol(s) and rationale
- Assumptions and constraints
- Implementation outline (functions, inputs, data flow)
- Rive wiring steps
- Debug and test plan
- Explicit confirmation request

If user does not approve, keep refining plan only.

### Phase 4: Implement After Approval

- Generate minimal, runnable, typed Luau script first.
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

Use `references/editor-wiring-recipes.md` and `references/debug-test-playbook.md`.

## Protocol and API Guardrails

- Never invent lifecycle functions, interfaces, or editor paths.
- Keep `TransitionCondition.evaluate` fast and side-effect free.
- Use `ListenerAction.perform` for side effects.
- For `PathEffect`, keep `update` deterministic; use `advance` only for time-based behavior.
- Remember: scripts cannot set normal input values; use context or view model access for writable data.
- Remove long-lived listeners when no longer needed to avoid leaks.
- Check `references/common-errors-and-fixes.md` before final handoff.
- If required details are missing, ask before coding.

## Output Format

Before approval:

- Understanding
- Open questions
- Pending plan
- Confirmation prompt

After approval:

- Script code
- Wiring steps
- Debug plan
- Test plan

## Reference Map

- Live docs sync and fallback rules: `references/live-docs-workflow.md`
- Protocol routing and method contracts: `references/protocol-router.md`
- Signature and API quick reference: `references/api-signature-cheatsheet.md`
- Clarification questions by protocol: `references/clarification-checklists.md`
- Minimal Luau templates: `references/scaffold-templates.md`
- Practical case recipes: `references/case-recipes.md`
- Editor attach and binding steps: `references/editor-wiring-recipes.md`
- Debug and test workflow: `references/debug-test-playbook.md`
- Common errors and fixes: `references/common-errors-and-fixes.md`
