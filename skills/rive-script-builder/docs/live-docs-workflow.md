# Live Docs Workflow (Context7 First)

Use this workflow to keep answers aligned with latest Rive docs while preserving offline reliability.

## Why

- Rive APIs can evolve.
- Local docs may lag behind.
- Context7-first lookup minimizes stale guidance and avoids manual scraping logic.

## Primary Live Source (MCP)

Preferred library:
- `/rive-app/rive-docs`

Primary sequence:
1. Resolve library ID (once per session if needed).
2. Query docs with focused protocol/API questions.

Example:

```text
resolve-library-id("rive-docs") -> /rive-app/rive-docs
query-docs(libraryId="/rive-app/rive-docs", query="Path Effect update and advance behavior")
```

## Secondary Source (Fallback Script)

- `scripts/sync_rive_docs.py`

Recommended invocation when MCP is unavailable:

```bash
cd /path/to/rive-script-builder
python3 scripts/sync_rive_docs.py <subcommand>
```

Resolve `scripts/sync_rive_docs.py` relative to the active `SKILL.md`; do not assume a fixed global skill directory.

## Fallback Lookup (No Token Required)

Search:

```bash
cd /path/to/rive-script-builder
python3 scripts/sync_rive_docs.py search --source auto --query "Path Effect"
```

Show file:

```bash
cd /path/to/rive-script-builder
python3 scripts/sync_rive_docs.py show --source auto --path scripting/protocols/path-effect-scripts.mdx
```

Source behavior:
- `search --source auto`: `online -> cache -> offline`
- `show --source auto`: `online -> cache`

Offline search scope:
- `docs/` (curated rules)
- `references/` (templates/recipes)
- `docs/source-scripting/` (full mirrored upstream scripting docs)

Each result prints source markers:
- `source=online`
- `source=cache`
- `source=offline`

If fallback happens, the script prints explicit fallback reasons (for example 403/429/network errors).

## Fallback Online Search Mechanics

Fallback online search does not use GitHub code-search API token auth.
It fetches `docs.json` from the target branch as the online index, then reads matching files from raw GitHub content.

## Optional Cache Prewarm (Fallback Path)

`sync` is optional. Use it to reduce repeated remote requests and improve offline continuity:

```bash
cd /path/to/rive-script-builder
python3 scripts/sync_rive_docs.py sync
```

Other cache commands:

```bash
cd /path/to/rive-script-builder
python3 scripts/sync_rive_docs.py status
python3 scripts/sync_rive_docs.py search --source cache --query "PathEffect"
python3 scripts/sync_rive_docs.py show --source cache --path scripting/protocols/path-effect-scripts.mdx
```

## Default Remote Source (Fallback Path)

- Repo: `rive-app/rive-docs`
- Branch: `main`
- Online target path: `scripting/`
- Default cache dir: `~/.cache/rive-script-builder/rive-docs`

## No-Token Limits (Fallback Path)

This workflow does not require GitHub token by default.
Potential limitations in no-token mode:
- lower API rate limits
- occasional 403/429 responses

The fallback script handles this via automatic fallback to cache/offline docs/references.

## Safety Rules

- If online and offline docs/references conflict, prefer online and note the difference.
- If Context7 and fallback sources conflict, prefer Context7 and note the difference.
- If online access fails, never invent APIs; rely on `api-signature-cheatsheet.md` and state assumptions explicitly.
