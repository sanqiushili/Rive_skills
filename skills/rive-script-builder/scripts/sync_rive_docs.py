#!/usr/bin/env python3
"""
Sync and query Rive docs from GitHub for the rive-script-builder skill.

Usage:
  python3 scripts/sync_rive_docs.py sync
  python3 scripts/sync_rive_docs.py status
  python3 scripts/sync_rive_docs.py search --query "PathEffect"
  python3 scripts/sync_rive_docs.py show --path scripting/protocols/path-effect-scripts.mdx
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

DEFAULT_REPO = "https://github.com/rive-app/rive-docs.git"
DEFAULT_BRANCH = "main"
SPARSE_PATHS = ["scripting"]


def run(cmd: list[str], cwd: Path | None = None) -> str:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        stderr = proc.stderr.strip() or "(no stderr)"
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{stderr}")
    return proc.stdout.strip()


def ensure_git() -> None:
    if shutil.which("git") is None:
        raise RuntimeError("git not found. Please install git first.")


def default_cache_dir() -> Path:
    return Path.home() / ".cache" / "rive-script-builder" / "rive-docs"


def metadata_path(cache_dir: Path) -> Path:
    return cache_dir / ".rive-docs-meta.json"


def write_metadata(cache_dir: Path, repo: str, branch: str) -> Path:
    commit = run(["git", "rev-parse", "HEAD"], cwd=cache_dir)
    commit_date = run(["git", "show", "-s", "--format=%cI", "HEAD"], cwd=cache_dir)
    meta = {
        "repo": repo,
        "branch": branch,
        "cache_dir": str(cache_dir),
        "commit": commit,
        "commit_date": commit_date,
        "sparse_paths": SPARSE_PATHS,
    }
    mp = metadata_path(cache_dir)
    mp.parent.mkdir(parents=True, exist_ok=True)
    mp.write_text(json.dumps(meta, indent=2) + "\n")
    return mp


def apply_sparse_checkout(cache_dir: Path) -> None:
    run(["git", "sparse-checkout", "set", *SPARSE_PATHS], cwd=cache_dir)


def sync_repo(cache_dir: Path, repo: str, branch: str) -> Path:
    ensure_git()
    cache_dir.parent.mkdir(parents=True, exist_ok=True)

    if (cache_dir / ".git").exists():
        run(["git", "remote", "set-url", "origin", repo], cwd=cache_dir)
        run(["git", "fetch", "--depth", "1", "origin", branch], cwd=cache_dir)
        run(["git", "checkout", "-B", branch, f"origin/{branch}"], cwd=cache_dir)
        apply_sparse_checkout(cache_dir)
    else:
        run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--filter=blob:none",
                "--sparse",
                "--branch",
                branch,
                repo,
                str(cache_dir),
            ]
        )
        apply_sparse_checkout(cache_dir)

    return write_metadata(cache_dir, repo, branch)


def iter_docs(cache_dir: Path) -> Iterable[Path]:
    root = cache_dir / "scripting"
    if not root.exists():
        return []
    return sorted(root.rglob("*.mdx"))


def cmd_status(args: argparse.Namespace) -> int:
    cache_dir = Path(args.cache_dir).resolve()
    mp = metadata_path(cache_dir)
    if not mp.exists():
        print("No metadata found. Run `sync` first.")
        return 1
    data = json.loads(mp.read_text())
    print(json.dumps(data, indent=2))
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    cache_dir = Path(args.cache_dir).resolve()
    try:
        meta_file = sync_repo(cache_dir, args.repo, args.branch)
    except Exception as exc:
        print(f"sync failed: {exc}", file=sys.stderr)
        return 1

    print(f"Synced to: {cache_dir}")
    print(f"Metadata: {meta_file}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    cache_dir = Path(args.cache_dir).resolve()
    if not cache_dir.exists():
        print("Cache not found. Run `sync` first.", file=sys.stderr)
        return 1

    flags = 0 if args.case_sensitive else re.IGNORECASE
    pattern = re.compile(args.query, flags)

    hits: list[tuple[str, int, str]] = []
    for file_path in iter_docs(cache_dir):
        rel = file_path.relative_to(cache_dir)
        lines = file_path.read_text(errors="ignore").splitlines()
        for i, line in enumerate(lines, start=1):
            if pattern.search(line):
                snippet = line.strip()
                if len(snippet) > 180:
                    snippet = snippet[:177] + "..."
                hits.append((str(rel), i, snippet))
                if len(hits) >= args.limit:
                    break
        if len(hits) >= args.limit:
            break

    if not hits:
        print("No matches.")
        return 0

    for rel, ln, snippet in hits:
        print(f"{rel}:{ln}: {snippet}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    cache_dir = Path(args.cache_dir).resolve()
    target = (cache_dir / args.path).resolve()

    try:
        target.relative_to(cache_dir)
    except ValueError:
        print("Path must be inside cache dir.", file=sys.stderr)
        return 1

    if not target.exists() or not target.is_file():
        print(f"File not found: {target}", file=sys.stderr)
        return 1

    lines = target.read_text(errors="ignore").splitlines()

    start = max(1, args.start)
    end = min(len(lines), args.end if args.end else len(lines))
    if end < start:
        print("Invalid range.", file=sys.stderr)
        return 1

    for i in range(start, end + 1):
        print(f"{i:4}: {lines[i - 1]}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sync/search/show Rive docs cache")
    parser.add_argument(
        "--cache-dir",
        default=str(default_cache_dir()),
        help="Local cache directory",
    )

    sub = parser.add_subparsers(dest="cmd", required=True)

    p_sync = sub.add_parser("sync", help="Clone/update docs cache")
    p_sync.add_argument("--repo", default=DEFAULT_REPO)
    p_sync.add_argument("--branch", default=DEFAULT_BRANCH)
    p_sync.set_defaults(func=cmd_sync)

    p_status = sub.add_parser("status", help="Show local cache metadata")
    p_status.set_defaults(func=cmd_status)

    p_search = sub.add_parser("search", help="Search in cached docs")
    p_search.add_argument("--query", required=True)
    p_search.add_argument("--limit", type=int, default=20)
    p_search.add_argument("--case-sensitive", action="store_true")
    p_search.set_defaults(func=cmd_search)

    p_show = sub.add_parser("show", help="Show one cached doc file")
    p_show.add_argument("--path", required=True, help="Path relative to cache root")
    p_show.add_argument("--start", type=int, default=1)
    p_show.add_argument("--end", type=int)
    p_show.set_defaults(func=cmd_show)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
