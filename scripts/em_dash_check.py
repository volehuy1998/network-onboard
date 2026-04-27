#!/usr/bin/env python3
"""Em-dash check for the SDN training repository.

Per CLAUDE.md Rule 17 (added by plan v3.9.1 Phase Q-1), the em-dash character
(Unicode U+2014, the long horizontal dash with the width of approximately one
M) is forbidden anywhere in this repository. This script enforces that rule
at pre-commit time.

Behaviour:
- ``--staged``: scan only staged .md files (.md added or modified). This is
  the mode used by the pre-commit hook.
- ``--all``: scan every .md file in the repository. Used for repository-wide
  audit during plan v3.9.1 Phase Q-1.C and Phase Q8 final audit.
- ``--files PATH [PATH ...]``: scan a specific list of files.

Exit code is 0 when no em-dash is found, 1 when at least one em-dash is found.
The script prints every offending file path, line number, and the offending
line content.

Allowed characters that are NOT em-dash:
- ``-`` (U+002D HYPHEN-MINUS)
- ``‐`` (U+2010 HYPHEN)
- ``–`` (U+2013 EN DASH, used for numeric ranges such as ``OVS 2.5-2.6``)
- ``−`` (U+2212 MINUS SIGN)

Only U+2014 EM DASH triggers a failure.

The script is intentionally simple. It does not consult ``.gitignore``; the
caller is expected to pass only files that should be checked. It reads files
in UTF-8 and treats decoding errors as a failure (a corrupted .md file is a
larger problem than this script needs to solve).

Authoring context: plan v3.9.1 Phase Q-1.B, 2026-04-28.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

EM_DASH = chr(0x2014)  # U+2014 EM DASH, the character we are forbidding.

# Files allowed to contain em-dash. Empty by user directive 2026-04-28
# ("no em-dash allowed!!!"). Reserved for narrow tooling or test fixture use
# only; review every addition.
ALLOWLIST: set[str] = set()


def find_em_dash_in_file(path: Path) -> list[tuple[int, str]]:
    """Return a list of ``(line_number, line_content)`` tuples for every line
    in ``path`` that contains the em-dash character. Line numbers start at 1.
    """
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        # Treat a non-UTF-8 .md as a hard failure rather than silently
        # passing.
        return [(0, f"<file is not valid UTF-8: {exc}>")]
    hits: list[tuple[int, str]] = []
    for lineno, line in enumerate(content.splitlines(), start=1):
        if EM_DASH in line:
            hits.append((lineno, line.rstrip("\n")))
    return hits


def get_staged_md_files() -> list[Path]:
    """Return the list of .md files currently staged for commit, relative to
    the repository root."""
    try:
        out = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            text=True,
        )
    except subprocess.CalledProcessError:
        return []
    return [
        Path(line.strip())
        for line in out.splitlines()
        if line.strip().endswith(".md")
    ]


def get_all_md_files(repo_root: Path) -> list[Path]:
    """Return every .md file tracked by git in the repository."""
    try:
        out = subprocess.check_output(
            ["git", "ls-files", "*.md"],
            cwd=str(repo_root),
            text=True,
        )
    except subprocess.CalledProcessError:
        return []
    return [
        repo_root / line.strip()
        for line in out.splitlines()
        if line.strip()
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Reject em-dash (U+2014) in .md files per CLAUDE.md Rule 17. "
            "Exit 0 if clean, 1 if any em-dash is found."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--staged",
        action="store_true",
        help="Scan only staged .md files (pre-commit hook mode).",
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="Scan every .md file tracked by git.",
    )
    group.add_argument(
        "--files",
        nargs="+",
        type=Path,
        metavar="PATH",
        help="Scan the specified .md files.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Path to the repository root. Defaults to git rev-parse output.",
    )
    args = parser.parse_args(argv)

    if args.repo_root is not None:
        repo_root = args.repo_root.resolve()
    else:
        try:
            out = subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"], text=True
            )
            repo_root = Path(out.strip()).resolve()
        except subprocess.CalledProcessError:
            print(
                "ERROR: not in a git repository and --repo-root was not "
                "given.",
                file=sys.stderr,
            )
            return 2

    if args.staged:
        files = [repo_root / p for p in get_staged_md_files()]
    elif args.all:
        files = get_all_md_files(repo_root)
    else:
        files = [p.resolve() for p in args.files]

    files = [p for p in files if p.is_file()]

    total_hits = 0
    failing_files = 0
    for path in files:
        rel = path.relative_to(repo_root) if path.is_relative_to(repo_root) else path
        rel_str = str(rel).replace("\\", "/")
        if rel_str in ALLOWLIST:
            continue
        hits = find_em_dash_in_file(path)
        if not hits:
            continue
        failing_files += 1
        total_hits += len(hits)
        print(f"--- {rel_str} ({len(hits)} em-dash hit) ---")
        for lineno, line in hits:
            display_line = line if len(line) <= 200 else line[:200] + "..."
            print(f"  L{lineno}: {display_line}")

    if total_hits == 0:
        print(f"em_dash_check: PASS ({len(files)} file(s) scanned, 0 em-dash).")
        return 0

    print(
        f"em_dash_check: FAIL ({total_hits} em-dash across {failing_files} "
        f"file(s)). Per CLAUDE.md Rule 17, em-dash (U+2014) is forbidden. "
        f"Replace with comma, period, colon, parentheses, or a bulleted list."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
