# Docs Folder Purpose

Use this folder for normative knowledge that the skill should treat as source-of-truth when offline:

- protocol routing and lifecycle constraints
- API signatures and guardrails
- clarification checklists
- editor wiring rules
- debug and test procedures
- publishing/distribution guidance

Do not place large generated outputs or one-off examples here.

## Retrieval Priority

Use this order when answering:
1. Context7 MCP (`/rive-app/rive-docs`)
2. Local curated docs in this folder
3. `references/` templates and recipes
4. `docs/source-scripting/` mirror for full offline coverage

## Current Core Docs

- `api-signature-cheatsheet.md`
- `protocol-router.md`
- `clarification-checklists.md`
- `data-binding-deep-dive.md`
- `script-inputs-deep-dive.md`
- `pointer-events-playbook.md`
- `path-api-performance-notes.md`
- `editor-wiring-recipes.md`
- `debug-test-playbook.md`
- `common-errors-and-fixes.md`
- `quality-gates.md`
- `context7-query-recipes.md`
- `live-docs-workflow.md`
- `publish-cross-platform.md`

## Full Mirror (Offline)

- `source-scripting/` keeps a full local mirror of the upstream `rive-docs/scripting` docs (`.mdx` files).
- This is used as the offline fallback knowledge base when live lookup is unavailable.
