#!/usr/bin/env python3
"""
Sync and query Rive docs from GitHub for the rive-script-builder skill.

Usage:
  python3 scripts/sync_rive_docs.py sync
  python3 scripts/sync_rive_docs.py status
  python3 scripts/sync_rive_docs.py search --query "PathEffect" --source auto
  python3 scripts/sync_rive_docs.py show --path scripting/protocols/path-effect-scripts.mdx --source auto
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Iterable

DEFAULT_REPO = "https://github.com/rive-app/rive-docs.git"
DEFAULT_BRANCH = "main"
SPARSE_PATHS = ["scripting"]

GITHUB_OWNER = "rive-app"
GITHUB_REPO = "rive-docs"
RAW_BASE = "https://raw.githubusercontent.com"

SEARCH_SOURCES = ("auto", "online", "cache", "offline")
SHOW_SOURCES = ("auto", "online", "cache")
OFFLINE_EXTENSIONS = (".md", ".mdx")


class SourceError(Exception):
    pass


def run(cmd: list[str], cwd: Path | None = None) -> str:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        stderr = proc.stderr.strip() or "(no stderr)"
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\\n{stderr}")
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
    mp.write_text(json.dumps(meta, indent=2) + "\\n")
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


def skill_docs_root() -> Path:
    return Path(__file__).resolve().parents[1] / "docs"


def skill_references_root() -> Path:
    return Path(__file__).resolve().parents[1] / "references"


def skill_offline_roots() -> list[tuple[str, Path]]:
    roots: list[tuple[str, Path]] = []
    docs = skill_docs_root()
    refs = skill_references_root()
    if docs.exists():
        roots.append(("docs", docs))
    if refs.exists():
        roots.append(("references", refs))
    return roots


def iter_offline_docs(root: Path) -> Iterable[Path]:
    files: list[Path] = []
    for ext in OFFLINE_EXTENSIONS:
        files.extend(root.rglob(f"*{ext}"))
    return sorted(path for path in files if path.is_file())


def compile_pattern(query: str, case_sensitive: bool) -> re.Pattern[str]:
    flags = 0 if case_sensitive else re.IGNORECASE
    try:
        return re.compile(query, flags)
    except re.error as exc:
        raise SourceError(f"invalid regex query: {exc}") from exc


def request_text(url: str, timeout: float = 20.0, accept: str = "*/*") -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "rive-script-builder/1.0",
            "Accept": accept,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        reason = exc.reason if hasattr(exc, "reason") else "http error"
        raise SourceError(f"http {exc.code}: {reason}") from exc
    except urllib.error.URLError as exc:
        raise SourceError(f"network error: {exc.reason}") from exc


def raw_url(path: str, branch: str) -> str:
    clean = path.lstrip("/")
    return f"{RAW_BASE}/{GITHUB_OWNER}/{GITHUB_REPO}/{branch}/{clean}"


def fetch_online_file(path: str, branch: str) -> list[str]:
    text = request_text(raw_url(path, branch), accept="text/plain")
    return text.splitlines()


def _normalize_repo_path(path: str) -> str | None:
    p = path.strip()
    if not p:
        return None
    if p.startswith("/"):
        p = p[1:]

    # strip anchors/query fragments
    qpos = p.find("?")
    hpos = p.find("#")
    cut = len(p)
    if qpos >= 0:
        cut = min(cut, qpos)
    if hpos >= 0:
        cut = min(cut, hpos)
    p = p[:cut]

    if not p.startswith("scripting/"):
        return None

    if p.endswith("/"):
        return None

    if not p.endswith(".mdx"):
        p = p + ".mdx"

    return p


def _collect_strings(obj: object, out: list[str]) -> None:
    if isinstance(obj, str):
        out.append(obj)
        return
    if isinstance(obj, list):
        for item in obj:
            _collect_strings(item, out)
        return
    if isinstance(obj, dict):
        for value in obj.values():
            _collect_strings(value, out)


def fetch_online_index_paths(branch: str) -> list[str]:
    text = request_text(raw_url("docs.json", branch), accept="application/json")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SourceError(f"invalid docs.json: {exc}") from exc

    all_strings: list[str] = []
    _collect_strings(data, all_strings)

    paths: list[str] = []
    seen: set[str] = set()
    for value in all_strings:
        normalized = _normalize_repo_path(value)
        if normalized is None:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        paths.append(normalized)

    if not paths:
        raise SourceError("no scripting paths found in docs.json")

    return paths


def _path_relevance(path: str, query: str) -> int:
    tokens = [t for t in re.split(r"[^A-Za-z0-9]+", query.lower()) if t]
    if not tokens:
        return 0
    pl = path.lower()
    return sum(1 for t in tokens if t in pl)


def _collect_hits_from_lines(
    source: str,
    rel_path: str,
    lines: list[str],
    pattern: re.Pattern[str],
    limit: int,
    out_hits: list[tuple[str, str, int, str]],
) -> None:
    for i, line in enumerate(lines, start=1):
        if pattern.search(line):
            snippet = line.strip()
            if len(snippet) > 180:
                snippet = snippet[:177] + "..."
            out_hits.append((source, rel_path, i, snippet))
            if len(out_hits) >= limit:
                return


def search_online(query: str, limit: int, case_sensitive: bool, branch: str) -> list[tuple[str, str, int, str]]:
    pattern = compile_pattern(query, case_sensitive)
    paths = fetch_online_index_paths(branch)

    # prioritize likely files by path relevance
    paths.sort(key=lambda p: _path_relevance(p, query), reverse=True)

    hits: list[tuple[str, str, int, str]] = []
    readable_files = 0

    for path in paths:
        try:
            lines = fetch_online_file(path, branch)
        except SourceError:
            continue

        readable_files += 1
        _collect_hits_from_lines("online", path, lines, pattern, limit, hits)
        if len(hits) >= limit:
            break

    if readable_files == 0:
        raise SourceError(f"online files unavailable on branch '{branch}'")

    return hits


def search_cache(cache_dir: Path, query: str, limit: int, case_sensitive: bool) -> list[tuple[str, str, int, str]]:
    root = cache_dir / "scripting"
    if not root.exists():
        raise SourceError("cache missing scripting/ (run sync to prewarm)")

    pattern = compile_pattern(query, case_sensitive)
    hits: list[tuple[str, str, int, str]] = []

    for file_path in sorted(root.rglob("*.mdx")):
        rel = str(file_path.relative_to(cache_dir))
        lines = file_path.read_text(errors="ignore").splitlines()
        _collect_hits_from_lines("cache", rel, lines, pattern, limit, hits)
        if len(hits) >= limit:
            break

    return hits


def search_offline(query: str, limit: int, case_sensitive: bool) -> list[tuple[str, str, int, str]]:
    roots = skill_offline_roots()
    if not roots:
        raise SourceError("offline docs/references not found")

    pattern = compile_pattern(query, case_sensitive)
    hits: list[tuple[str, str, int, str]] = []

    for root_name, root_path in roots:
        for file_path in iter_offline_docs(root_path):
            rel_inside_root = file_path.relative_to(root_path).as_posix()
            rel = f"{root_name}/{rel_inside_root}"
            lines = file_path.read_text(errors="ignore").splitlines()
            _collect_hits_from_lines("offline", rel, lines, pattern, limit, hits)
            if len(hits) >= limit:
                break
        if len(hits) >= limit:
            break

    return hits


def read_cache_file(cache_dir: Path, path: str) -> list[str]:
    target = (cache_dir / path).resolve()
    try:
        target.relative_to(cache_dir)
    except ValueError as exc:
        raise SourceError("path must be inside cache dir") from exc

    if not target.exists() or not target.is_file():
        raise SourceError(f"cache file not found: {target}")

    return target.read_text(errors="ignore").splitlines()


def slice_lines(lines: list[str], start: int, end: int | None) -> list[tuple[int, str]]:
    s = max(1, start)
    e = min(len(lines), end if end else len(lines))
    if e < s:
        raise SourceError("invalid range")
    return [(i, lines[i - 1]) for i in range(s, e + 1)]


def print_hits(source: str, hits: list[tuple[str, str, int, str]]) -> None:
    print(f"source={source}")
    if not hits:
        print("No matches.")
        return

    for _, rel, ln, snippet in hits:
        print(f"{rel}:{ln}: {snippet}")


def print_file_slice(source: str, path: str, rows: list[tuple[int, str]]) -> None:
    print(f"source={source}")
    print(f"path={path}")
    for ln, text in rows:
        print(f"{ln:4}: {text}")


def _cache_dir_from_args(args: argparse.Namespace) -> Path:
    raw = getattr(args, "cache_dir", None)
    if raw is None:
        raw = str(default_cache_dir())
    return Path(raw).resolve()


def cmd_status(args: argparse.Namespace) -> int:
    cache_dir = _cache_dir_from_args(args)
    mp = metadata_path(cache_dir)
    if not mp.exists():
        print("No metadata found. Run `sync` first.")
        return 1
    data = json.loads(mp.read_text())
    print(json.dumps(data, indent=2))
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    cache_dir = _cache_dir_from_args(args)
    try:
        meta_file = sync_repo(cache_dir, args.repo, args.branch)
    except Exception as exc:
        print(f"sync failed: {exc}", file=sys.stderr)
        return 1

    print(f"Synced to: {cache_dir}")
    print(f"Metadata: {meta_file}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    cache_dir = _cache_dir_from_args(args)

    def _online() -> list[tuple[str, str, int, str]]:
        return search_online(args.query, args.limit, args.case_sensitive, args.branch)

    def _cache() -> list[tuple[str, str, int, str]]:
        return search_cache(cache_dir, args.query, args.limit, args.case_sensitive)

    def _offline() -> list[tuple[str, str, int, str]]:
        return search_offline(args.query, args.limit, args.case_sensitive)

    try:
        if args.source == "online":
            hits = _online()
            print_hits("online", hits)
            return 0

        if args.source == "cache":
            hits = _cache()
            print_hits("cache", hits)
            return 0

        if args.source == "offline":
            hits = _offline()
            print_hits("offline", hits)
            return 0

        # auto: online -> cache -> offline
        try:
            hits = _online()
            print_hits("online", hits)
            return 0
        except SourceError as exc_online:
            print(f"fallback: online failed ({exc_online}); trying cache", file=sys.stderr)

        try:
            hits = _cache()
            print_hits("cache", hits)
            return 0
        except SourceError as exc_cache:
            print(f"fallback: cache failed ({exc_cache}); trying offline", file=sys.stderr)

        hits = _offline()
        print_hits("offline", hits)
        return 0

    except SourceError as exc:
        print(f"search failed: {exc}", file=sys.stderr)
        return 1


def cmd_show(args: argparse.Namespace) -> int:
    cache_dir = _cache_dir_from_args(args)

    try:
        if args.source == "online":
            lines = fetch_online_file(args.path, args.branch)
            rows = slice_lines(lines, args.start, args.end)
            print_file_slice("online", args.path, rows)
            return 0

        if args.source == "cache":
            lines = read_cache_file(cache_dir, args.path)
            rows = slice_lines(lines, args.start, args.end)
            print_file_slice("cache", args.path, rows)
            return 0

        # auto: online -> cache
        try:
            lines = fetch_online_file(args.path, args.branch)
            rows = slice_lines(lines, args.start, args.end)
            print_file_slice("online", args.path, rows)
            return 0
        except SourceError as exc_online:
            print(f"fallback: online failed ({exc_online}); trying cache", file=sys.stderr)

        lines = read_cache_file(cache_dir, args.path)
        rows = slice_lines(lines, args.start, args.end)
        print_file_slice("cache", args.path, rows)
        return 0

    except SourceError as exc:
        print(f"show failed: {exc}", file=sys.stderr)
        return 1


def add_cache_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--cache-dir",
        default=str(default_cache_dir()),
        help="Local cache directory",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sync/search/show Rive docs cache")
    add_cache_arg(parser)

    sub = parser.add_subparsers(dest="cmd", required=True)

    p_sync = sub.add_parser("sync", help="Clone/update docs cache (optional prewarm)")
    add_cache_arg(p_sync)
    p_sync.add_argument("--repo", default=DEFAULT_REPO)
    p_sync.add_argument("--branch", default=DEFAULT_BRANCH)
    p_sync.set_defaults(func=cmd_sync)

    p_status = sub.add_parser("status", help="Show local cache metadata")
    add_cache_arg(p_status)
    p_status.set_defaults(func=cmd_status)

    p_search = sub.add_parser("search", help="Search docs across online/cache/offline sources")
    add_cache_arg(p_search)
    p_search.add_argument("--query", required=True)
    p_search.add_argument("--limit", type=int, default=20)
    p_search.add_argument("--case-sensitive", action="store_true")
    p_search.add_argument("--branch", default=DEFAULT_BRANCH)
    p_search.add_argument("--source", choices=SEARCH_SOURCES, default="auto")
    p_search.set_defaults(func=cmd_search)

    p_show = sub.add_parser("show", help="Show a docs file from online/cache source")
    add_cache_arg(p_show)
    p_show.add_argument("--path", required=True, help="Path relative to repo/cache root")
    p_show.add_argument("--start", type=int, default=1)
    p_show.add_argument("--end", type=int)
    p_show.add_argument("--branch", default=DEFAULT_BRANCH)
    p_show.add_argument("--source", choices=SHOW_SOURCES, default="auto")
    p_show.set_defaults(func=cmd_show)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
