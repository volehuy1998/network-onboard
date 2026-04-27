#!/usr/bin/env python3
"""Em-dash check for the SDN training repository.

Per CLAUDE.md Rule 17 (added by plan v3.9.1 Phase Q-1), the em-dash character
(Unicode U+2014, the long horizontal dash with the width of approximately one
M) is forbidden in any newly written or modified content. This script
enforces that rule at pre-commit time.

Behaviour:
- ``--staged``: scan only the lines added or modified by the staged
  changeset. This is the mode used by the pre-commit hook. Pre-existing
  em-dashes in legacy lines that the staged change does not touch are NOT
  flagged. This matches plan v3.9.1 §11.5: "rejects any staged file
  containing an em-dash in newly added or modified lines".
- ``--all``: scan every line of every .md file tracked by git.
  Used for repository-wide audit during plan v3.9.1 Phase Q8 final audit
  and during plan v3.12 curriculum-wide migration.
- ``--files PATH [PATH ...]``: scan every line of the specified .md files.

Exit code is 0 when no em-dash is found, 1 when at least one em-dash is
found. The script prints every offending file path, line number (or hunk
position for ``--staged``), and the offending line content.

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

Authoring context: plan v3.9.1 Phase Q-1.B, 2026-04-28; rewritten in
Phase Q-1.E (2026-04-28) to do diff-only scanning in ``--staged`` mode per
plan §11.5 intent (the original Q-1.B implementation did whole-file
scanning, which conflicted with the §8.3 mixed-language transition policy).
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

EM_DASH = chr(0x2014)  # U+2014 EM DASH, the character we are forbidding.

# Files allowed to contain em-dash. Empty by user directive 2026-04-28
# ("no em-dash allowed!!!"). Reserved for narrow tooling or test fixture use
# only; review every addition.
ALLOWLIST: set[str] = set()


def find_em_dash_in_file(path: Path) -> list[tuple[int, str]]:
    """Return ``(line_number, line_content)`` for every line in ``path`` that
    contains the em-dash character. Line numbers start at 1.
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


_HUNK_HEADER_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def find_em_dash_in_staged_diff(file_rel_path: str) -> list[tuple[int, str]]:
    """Scan only the added or modified lines of a staged change to ``file_rel_path``.

    ``file_rel_path`` must be the path relative to the repository root, using
    forward slashes. The function runs ``git diff --cached --unified=0`` for
    that file, parses each hunk, and returns ``(new_line_number, line)`` for
    every added line ('+') that contains an em-dash. It ignores deleted lines
    ('-') and context lines (no prefix) so that em-dashes in pre-existing
    legacy content are not flagged.

    For a brand-new file, every line is added, so the function returns the
    same result as a whole-file scan.
    """
    try:
        out = subprocess.check_output(
            [
                "git",
                "diff",
                "--cached",
                "--unified=0",
                "--no-color",
                "--no-renames",
                "--",
                file_rel_path,
            ],
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.CalledProcessError:
        return []
    hits: list[tuple[int, str]] = []
    new_lineno = 0
    in_hunk = False
    for raw in out.splitlines():
        if raw.startswith("+++") or raw.startswith("---"):
            # File header line, not part of a hunk.
            continue
        m = _HUNK_HEADER_RE.match(raw)
        if m:
            new_lineno = int(m.group(1))
            in_hunk = True
            continue
        if not in_hunk:
            continue
        if raw.startswith("+"):
            content = raw[1:]
            if EM_DASH in content:
                hits.append((new_lineno, content.rstrip("\n")))
            new_lineno += 1
        elif raw.startswith("-"):
            # Deleted line, does not advance new_lineno.
            continue
        else:
            # Context line. With --unified=0 there should be none, but
            # tolerate them just in case (older git versions emit a leading
            # backslash for "\ No newline at end of file").
            if raw.startswith("\\"):
                continue
            new_lineno += 1
    return hits


def get_staged_md_files() -> list[str]:
    """Return the list of .md files currently staged for commit, relative to
    the repository root, using forward slashes."""
    try:
        out = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            text=True,
        )
    except subprocess.CalledProcessError:
        return []
    return [
        line.strip().replace("\\", "/")
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
            "Reject em-dash (U+2014) in newly written or modified .md "
            "content per CLAUDE.md Rule 17. Exit 0 if clean, 1 if any "
            "em-dash is found."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--staged",
        action="store_true",
        help=(
            "Scan only the lines added or modified by the staged "
            "changeset (pre-commit hook mode). Pre-existing em-dashes "
            "in legacy lines that the staged change does not touch are "
            "NOT flagged."
        ),
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="Scan every line of every .md file tracked by git.",
    )
    group.add_argument(
        "--files",
        nargs="+",
        type=Path,
        metavar="PATH",
        help="Scan every line of the specified .md files.",
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

    total_hits = 0
    failing_files = 0
    files_scanned = 0

    if args.staged:
        rel_paths = get_staged_md_files()
        for rel in rel_paths:
            if rel in ALLOWLIST:
                continue
            files_scanned += 1
            hits = find_em_dash_in_staged_diff(rel)
            if not hits:
                continue
            failing_files += 1
            total_hits += len(hits)
            print(f"--- {rel} ({len(hits)} em-dash hit in staged diff) ---")
            for lineno, line in hits:
                display_line = line if len(line) <= 200 else line[:200] + "..."
                print(f"  L{lineno} (added): {display_line}")
    else:
        if args.all:
            file_paths = get_all_md_files(repo_root)
        else:
            file_paths = [p.resolve() for p in args.files]
        file_paths = [p for p in file_paths if p.is_file()]
        for path in file_paths:
            rel = (
                path.relative_to(repo_root)
                if path.is_relative_to(repo_root)
                else path
            )
            rel_str = str(rel).replace("\\", "/")
            if rel_str in ALLOWLIST:
                continue
            files_scanned += 1
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
        mode = "staged-diff" if args.staged else "whole-file"
        print(
            f"em_dash_check: PASS ({files_scanned} file(s) scanned, "
            f"0 em-dash, mode={mode})."
        )
        return 0

    mode = "staged-diff" if args.staged else "whole-file"
    print(
        f"em_dash_check: FAIL ({total_hits} em-dash across {failing_files} "
        f"file(s), mode={mode}). Per CLAUDE.md Rule 17, em-dash (U+2014) is "
        f"forbidden in newly written or modified content. Replace with "
        f"comma, period, colon, parentheses, or a bulleted list."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
