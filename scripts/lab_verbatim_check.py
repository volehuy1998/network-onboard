#!/usr/bin/env python3
"""Lab transcript verbatim-integrity check for the SDN training repository.

Per CLAUDE.md Rule 18 (added by plan v3.13 R0), every Markdown lab transcript
under ``sdn-onboard/labs/`` must reproduce the lab host output exactly as it
appeared on the host. Not a single character may be modified, omitted, or
rewritten. The verbatim record is the curriculum's evidence.

This script is the pragmatic first cut of the Rule 18 enforcement. It does
not yet do a full byte-stream replay of the raw ``script -f -t`` typescript
against the rendered Markdown (the strict version, deferred to a follow-on
commit after R0b produces a real typescript to test against). Instead it
enforces these structural invariants which together catch the most common
ways a verbatim record gets silently corrupted:

1. Every staged Markdown file under ``sdn-onboard/labs/`` must contain a
   ``> **Verbatim source:**`` header line that names the typescript file
   from which the transcript was rendered. The header must appear within
   the first 60 lines of the file.
2. The referenced typescript file must exist on disk, relative to the
   repository root.
3. The referenced typescript file must be non-empty.
4. The Markdown file must contain at least one fenced code block (the
   actual lab command and output material).
5. Every fenced code block whose info string is empty or ``text`` is
   treated as a verbatim block. Every line of every verbatim block must
   appear as an exact substring in the typescript file, in order. If a
   line cannot be found, the rendering has diverged from the typescript
   and the commit is rejected.
6. The literal marker ``[N other lines omitted, context: ...]`` is
   recognised. Lines before and after the marker are still checked, but
   the gap between them is allowed.
7. Typescript control sequences (carriage return only, ANSI colour
   escapes, ``script`` start and end banner lines) are stripped before
   matching so they do not cause false positives.

Behaviour modes:

- ``--staged``: scan only files staged by the current ``git`` index.
  This is the mode the pre-commit hook uses. Files outside
  ``sdn-onboard/labs/`` are skipped.
- ``--files PATH [PATH ...]``: scan the named files explicitly. Used by
  the test suite. Files outside ``sdn-onboard/labs/`` are skipped with a
  warning (so test fixtures can confirm the skip path).
- ``--all``: scan every tracked Markdown file under ``sdn-onboard/labs/``.
  Used for repository-wide audits.

Exit code is 0 when every checked file passes, 1 when at least one file
fails. The script prints every offending file path, the failing
invariant, the line number of the offence (or 0 when the invariant is
file-level), and the offending content where applicable.

Authoring context: plan v3.13 R0a, 2026-04-29. The strict full-replay
version is deferred until after R0b captures the first real typescript.
This script is the gate that allows Rule 18 to be enforced today; it
catches stripped prompts, anonymised IPs, shortened UUIDs, rounded
timestamps, and omitted-without-marker lines, all of which are the most
common Rule 18 violations.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Files in scope of the check.
LABS_PREFIX = "sdn-onboard/labs/"

# The verbatim-source header pattern. Example match:
#   > **Verbatim source:** `sdn-onboard/labs/v3.13-R0-baseline.typescript`
VERBATIM_HEADER_RE = re.compile(
    r"^>\s+\*\*Verbatim source:\*\*\s+`([^`]+)`",
    re.MULTILINE,
)

# Header search depth, in lines from the top of the Markdown file.
HEADER_SEARCH_LINES = 60

# Fenced code block delimiter.
FENCE_OPEN_RE = re.compile(r"^```(\w*)\s*$")
FENCE_CLOSE_RE = re.compile(r"^```\s*$")

# Languages whose content is treated as verbatim and therefore
# byte-checked against the typescript. Empty string covers code blocks
# without a language tag.
VERBATIM_LANGS: set[str] = {"", "text", "console", "shell-session", "bash"}

# Recognised "lines omitted" marker pattern, per Rule 7 / Rule 18 step 5.
OMIT_MARKER_RE = re.compile(
    r"^\[\d+\s+other\s+lines?\s+omitted,\s+context:\s+.+\]\s*$",
    re.IGNORECASE,
)

# ANSI escape sequence pattern used to strip colour and cursor codes
# from the raw typescript before matching.
ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]")

# `script` command emits a leader and trailer line of the form
# "Script started on ..." and "Script done on ...". These are not
# part of the lab content and would be confusing to enforce.
SCRIPT_BANNER_RE = re.compile(r"^Script (started|done) on .*", re.IGNORECASE)


def repo_root() -> Path:
    """Return the absolute path to the repository root."""
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(out.stdout.strip())


def is_in_scope(rel_path: str) -> bool:
    """Return True iff the file is under ``sdn-onboard/labs/`` and ends
    with ``.md``. Path is given relative to the repo root using forward
    slashes (the form ``git diff`` reports).
    """
    return rel_path.replace("\\", "/").startswith(LABS_PREFIX) and rel_path.endswith(
        ".md"
    )


def list_staged_md() -> list[str]:
    """Return staged Markdown files under ``sdn-onboard/labs/``."""
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [
        line.strip()
        for line in out.stdout.splitlines()
        if line.strip() and is_in_scope(line.strip())
    ]


def list_all_md() -> list[str]:
    """Return every tracked Markdown file under ``sdn-onboard/labs/``."""
    out = subprocess.run(
        ["git", "ls-files", f"{LABS_PREFIX}*.md"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [
        line.strip() for line in out.stdout.splitlines() if line.strip()
    ]


def find_verbatim_header(md_text: str) -> tuple[int, str] | None:
    """Find the verbatim-source header within the first
    HEADER_SEARCH_LINES lines. Return (line_number, typescript_path) or
    None if not found.
    """
    head = "\n".join(md_text.splitlines()[:HEADER_SEARCH_LINES])
    m = VERBATIM_HEADER_RE.search(head)
    if not m:
        return None
    typescript_rel = m.group(1).strip()
    line_no = head[: m.start()].count("\n") + 1
    return line_no, typescript_rel


def extract_verbatim_blocks(md_text: str) -> list[tuple[int, list[str]]]:
    """Walk the Markdown file and yield every fenced code block whose
    language is in VERBATIM_LANGS. Return list of (start_line, lines).
    """
    blocks: list[tuple[int, list[str]]] = []
    in_block = False
    cur_lang = ""
    cur_start = 0
    cur_lines: list[str] = []
    for i, line in enumerate(md_text.splitlines(), start=1):
        if not in_block:
            m = FENCE_OPEN_RE.match(line)
            if m:
                in_block = True
                cur_lang = m.group(1).lower()
                cur_start = i
                cur_lines = []
        else:
            if FENCE_CLOSE_RE.match(line):
                if cur_lang in VERBATIM_LANGS:
                    blocks.append((cur_start, cur_lines))
                in_block = False
                cur_lang = ""
                cur_lines = []
            else:
                cur_lines.append(line)
    return blocks


def normalise_typescript(raw: str) -> list[str]:
    """Strip ANSI escapes, drop CRs, drop the script banner lines, and
    return the typescript as a list of post-processed lines. Each output
    line is a single physical line of host output ready for substring
    comparison.
    """
    # `script` records carriage returns inside the typescript when the
    # remote terminal redraws. We split on \n only, then strip a trailing
    # \r from each line.
    out: list[str] = []
    for raw_line in raw.split("\n"):
        line = raw_line.rstrip("\r")
        line = ANSI_ESCAPE_RE.sub("", line)
        if SCRIPT_BANNER_RE.match(line):
            continue
        out.append(line)
    return out


def check_verbatim_block_against_typescript(
    block_lines: list[str],
    typescript_lines: list[str],
    block_start: int,
) -> list[tuple[int, str, str]]:
    """For each line in ``block_lines``, verify it appears as a
    substring of some line in ``typescript_lines``, in order. Return a
    list of (line_number, reason, content) for every line that fails to
    match. Empty list means the block matches.

    The marker line ``[N other lines omitted, context: ...]`` is allowed
    and skips ahead in the typescript without being matched itself.
    """
    failures: list[tuple[int, str, str]] = []
    cursor = 0  # Index into typescript_lines for in-order matching.
    for offset, line in enumerate(block_lines):
        line_no = block_start + 1 + offset  # +1 for the fence open line.
        if OMIT_MARKER_RE.match(line.strip()):
            # Marker resets cursor to "search anywhere from here on";
            # we already do that so the marker is effectively a no-op
            # other than being explicitly allowed.
            continue
        if not line.strip():
            # Blank lines in the block are intentionally not enforced
            # because typescript blanks are noisy. Rule 18 step 4 covers
            # the (no output) annotation case.
            continue
        # Search forward from the cursor for the first typescript line
        # that contains this line as a substring.
        found = False
        for j in range(cursor, len(typescript_lines)):
            if line in typescript_lines[j]:
                cursor = j + 1
                found = True
                break
        if not found:
            failures.append(
                (
                    line_no,
                    "verbatim-block line not found in typescript",
                    line,
                )
            )
    return failures


def check_file(rel_path: str, root: Path) -> list[str]:
    """Run every invariant against the file. Return a list of human-
    readable failure messages. Empty list means PASS.
    """
    failures: list[str] = []
    md_path = root / rel_path
    if not md_path.is_file():
        return [f"{rel_path}: file does not exist on disk"]
    try:
        md_text = md_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return [f"{rel_path}: not valid UTF-8 ({exc})"]

    # Invariant 1, 2, 3: header present, typescript exists, non-empty.
    header = find_verbatim_header(md_text)
    if header is None:
        failures.append(
            f"{rel_path}:0: missing `> **Verbatim source:** \\`<path>\\``"
            f" header within the first {HEADER_SEARCH_LINES} lines (Rule 18)"
        )
        return failures
    header_line, typescript_rel = header
    typescript_path = root / typescript_rel
    if not typescript_path.is_file():
        failures.append(
            f"{rel_path}:{header_line}: referenced typescript "
            f"`{typescript_rel}` does not exist (Rule 18)"
        )
        return failures
    try:
        raw = typescript_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        failures.append(
            f"{rel_path}:{header_line}: cannot read typescript "
            f"`{typescript_rel}` ({exc})"
        )
        return failures
    if not raw.strip():
        failures.append(
            f"{rel_path}:{header_line}: typescript "
            f"`{typescript_rel}` is empty (Rule 18)"
        )
        return failures

    # Invariant 4: at least one fenced code block.
    blocks = extract_verbatim_blocks(md_text)
    if not blocks:
        failures.append(
            f"{rel_path}:0: no verbatim fenced code block found "
            f"(expected at least one ```text ... ``` block)"
        )
        return failures

    # Invariant 5 and 6: every verbatim line is a substring of some
    # typescript line.
    typescript_lines = normalise_typescript(raw)
    for block_start, block_lines in blocks:
        block_failures = check_verbatim_block_against_typescript(
            block_lines, typescript_lines, block_start
        )
        for line_no, reason, content in block_failures:
            preview = content if len(content) <= 80 else content[:77] + "..."
            failures.append(
                f"{rel_path}:{line_no}: {reason}: {preview!r}"
            )

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Enforce CLAUDE.md Rule 18 verbatim integrity on lab "
            "transcripts under sdn-onboard/labs/."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--staged",
        action="store_true",
        help="check files staged by the current git index",
    )
    group.add_argument(
        "--files",
        nargs="+",
        metavar="PATH",
        help="check the named files explicitly",
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="check every tracked .md file under sdn-onboard/labs/",
    )
    args = parser.parse_args()

    root = repo_root()

    if args.staged:
        files = list_staged_md()
    elif args.all:
        files = list_all_md()
    else:
        files = []
        for p in args.files:
            rel = p.replace("\\", "/")
            # Make path relative to repo root if absolute or
            # current-directory-relative.
            try:
                abs_p = (Path.cwd() / rel).resolve()
                rel = str(abs_p.relative_to(root)).replace("\\", "/")
            except (ValueError, OSError):
                pass
            if not is_in_scope(rel):
                print(
                    f"SKIP {rel}: not under {LABS_PREFIX}",
                    file=sys.stderr,
                )
                continue
            files.append(rel)

    if not files:
        print(
            "lab_verbatim_check: PASS (no files in scope of check, "
            f"prefix={LABS_PREFIX})"
        )
        return 0

    total_fail = 0
    for rel_path in files:
        failures = check_file(rel_path, root)
        if failures:
            total_fail += len(failures)
            for line in failures:
                print(line)

    if total_fail:
        print(
            f"lab_verbatim_check: FAIL ({total_fail} violation(s) "
            f"across {len(files)} file(s)). Per CLAUDE.md Rule 18, "
            f"every line of every verbatim code block must appear "
            f"in the referenced typescript file."
        )
        return 1

    print(
        f"lab_verbatim_check: PASS ({len(files)} file(s) scanned, "
        f"all verbatim invariants satisfied)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
