# Live Docs Workflow (GitHub Sync)

Use this workflow to keep answers aligned with latest Rive docs without relying only on local static references.

## Why

- Rive APIs can evolve.
- Local references may lag behind.
- This workflow pulls the latest docs snapshot from GitHub and queries it on demand.

## Script Location

- `scripts/sync_rive_docs.py`

Recommended stable invocation:

```bash
python3 "$CODEX_HOME/skills/rive-script-builder/scripts/sync_rive_docs.py" <subcommand>
```

## Phase 0 Commands

1. Sync latest docs snapshot:

```bash
python3 "$CODEX_HOME/skills/rive-script-builder/scripts/sync_rive_docs.py" sync
```

2. Check local snapshot metadata:

```bash
python3 "$CODEX_HOME/skills/rive-script-builder/scripts/sync_rive_docs.py" status
```

3. Search for keywords:

```bash
python3 "$CODEX_HOME/skills/rive-script-builder/scripts/sync_rive_docs.py" search --query "PathEffect"
```

4. Inspect specific file:

```bash
python3 "$CODEX_HOME/skills/rive-script-builder/scripts/sync_rive_docs.py" show --path scripting/protocols/path-effect-scripts.mdx
```

## Default Sync Source

- Repo: `https://github.com/rive-app/rive-docs.git`
- Branch: `main`
- Sparse checkout paths: `scripting`
- Default cache dir: `~/.cache/rive-script-builder/rive-docs`

## Fallback Rule

If sync fails (no network, sandbox restrictions, GitHub unavailable):

1. Continue with offline references in this skill.
2. State clearly that latest remote docs could not be fetched.
3. Avoid inventing APIs; keep assumptions explicit.

## Safety Rule

- Always prefer exact signatures from `api-signature-cheatsheet.md` if remote checks are unavailable.
- If remote docs and local references conflict, prefer remote snapshot and note the difference.
