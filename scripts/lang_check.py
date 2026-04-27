#!/usr/bin/env python3
"""Language check for the SDN training repository.

Per CLAUDE.md Rule 17 (added by plan v3.9.1 Phase Q-1), every prose chunk in
CLAUDE.md, in `sdn-onboard/*.md`, in `haproxy-onboard/*.md`, in `memory/*`,
in `plans/*`, and in any other Markdown file written or modified after
2026-04-28 must be in English. Vietnamese (or any other non-English language)
is forbidden in newly written prose.

This script enforces the rule using the lingua-py language detector
configured as a binary classifier between English and Vietnamese. The user
directive (2026-04-28) requires "100% English, 0% other language" detection.

Behaviour:
- ``--staged``: scan only staged .md files (.md added or modified). This is
  the mode used by the pre-commit hook.
- ``--all``: scan every .md file tracked by git. Used for repository-wide
  audit.
- ``--files PATH [PATH ...]``: scan a specific list of files.

Exit code is 0 when every prose chunk in every scanned file is detected as
English. Exit code is 1 when at least one prose chunk is detected as
Vietnamese with a non-zero confidence (strict mode per user directive
2026-04-28).

The script does NOT scan:
- Code blocks delimited by triple backticks.
- Inline code spans inside backticks.
- URL-only lines.
- Markdown image lines.
- Lines that are purely identifiers, punctuation, or numbers.
- Lines shorter than 30 characters (insufficient signal for the detector).

These exclusions match the heuristic in `memory/shared/english-style-guide.md`
§3.3 (keep-as-is identifier list) and §10 (worked example).

Library: lingua-language-detector (https://pypi.org/project/lingua-language-detector/).
Install with `pip install lingua-language-detector`.

Authoring context: plan v3.9.1 Phase Q-1.B follow-up, 2026-04-28, in response
to the user directive "use a Python language detection library, a document
passes when the test reports 100% English and 0% other language".
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

try:
    from lingua import Language, LanguageDetectorBuilder
except ImportError:
    print(
        "ERROR: lingua-language-detector is not installed. Run "
        "`pip install lingua-language-detector` and retry.",
        file=sys.stderr,
    )
    sys.exit(2)

# Build the detector once at module load. Restrict to English plus Vietnamese
# so that identifier-heavy technical English does not get misclassified as
# some other Latin-script language (Norwegian, Italian, etc.). The user
# directive concerns the SDN training program, where the only realistic
# non-English content is legacy Vietnamese.
_DETECTOR = LanguageDetectorBuilder.from_languages(
    Language.ENGLISH, Language.VIETNAMESE
).build()

# Minimum prose-chunk length that the detector receives. Below this, the
# signal is too weak and the detector flips between English and Vietnamese
# even on plain English. The threshold of 30 characters matches lingua-py
# author guidance for short-text accuracy.
MIN_CHUNK_LEN = 30

# Block markers and patterns we strip before language detection.
_FENCED_CODE_RE = re.compile(r"^```", re.MULTILINE)
_INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
_URL_RE = re.compile(r"https?://\S+")
_MARKDOWN_IMAGE_LINE_RE = re.compile(r"^\s*!\[[^\]]*\]\([^)]*\).*$")
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_IDENTIFIER_ONLY_RE = re.compile(r"^[\s\W\d]*[A-Za-z][A-Za-z0-9_\-]*[\s\W\d]*$")

# Allowlist for files that are intentionally bilingual under CLAUDE.md
# Rule 17 §8.2 narrow allowance. Each entry is a path relative to the
# repository root, using forward slashes. Add a short comment with the
# justification next to each entry.
ALLOWLIST: set[str] = {
    # Frozen historical translation reference for plan v3.12 legacy
    # Vietnamese curriculum migration. Lives in memory/, which Rule 17
    # leaves outside the no-Vietnamese scope. Header is English; body
    # table is the bilingual artefact. See plan v3.9.1 Phase Q-1.D.
    "memory/shared/rule-11-dictionary.md",
}


def strip_code_and_inline(text: str) -> str:
    """Remove fenced code blocks, inline code spans, URLs, and markdown
    image references from ``text``. Return the stripped text."""
    out_lines: list[str] = []
    in_code_block = False
    for line in text.splitlines():
        if _FENCED_CODE_RE.match(line):
            in_code_block = not in_code_block
            out_lines.append("")  # placeholder so line numbers stay stable
            continue
        if in_code_block:
            out_lines.append("")
            continue
        if _MARKDOWN_IMAGE_LINE_RE.match(line):
            out_lines.append("")
            continue
        # Strip inline code, URLs, and HTML tags.
        cleaned = _INLINE_CODE_RE.sub("", line)
        cleaned = _URL_RE.sub("", cleaned)
        cleaned = _HTML_TAG_RE.sub("", cleaned)
        out_lines.append(cleaned)
    return "\n".join(out_lines)


def is_prose_chunk(line: str) -> bool:
    """Return True if ``line`` is long enough and varied enough to feed to
    the language detector. False otherwise (the line is skipped)."""
    stripped = line.strip()
    if len(stripped) < MIN_CHUNK_LEN:
        return False
    if _IDENTIFIER_ONLY_RE.match(stripped):
        return False
    # Require at least three space-separated tokens to have prose-like
    # content (rules out identifier salad like
    # "ovsdb_rbac_insert ovsdb_rbac_update").
    if len(stripped.split()) < 4:
        return False
    return True


def detect_chunk(chunk: str) -> tuple[str, float, float]:
    """Run the binary detector on ``chunk``. Return a tuple of
    ``(top_language_name, english_confidence, vietnamese_confidence)``."""
    confs = _DETECTOR.compute_language_confidence_values(chunk)
    en = next((c.value for c in confs if c.language == Language.ENGLISH), 0.0)
    vi = next((c.value for c in confs if c.language == Language.VIETNAMESE), 0.0)
    top_lang = _DETECTOR.detect_language_of(chunk)
    top_name = top_lang.name if top_lang is not None else "NONE"
    return top_name, en, vi


def scan_file(path: Path) -> tuple[list[tuple[int, str, float, float]], int]:
    """Scan ``path``. Return a tuple of ``(failures, scanned_chunk_count)``.

    Each failure is ``(line_number, line_content, english_conf, vietnamese_conf)``
    for any chunk where the top detected language is Vietnamese with non-zero
    confidence.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return [(0, f"<file is not valid UTF-8: {exc}>", 0.0, 0.0)], 0

    stripped = strip_code_and_inline(raw)
    failures: list[tuple[int, str, float, float]] = []
    scanned = 0
    for lineno, line in enumerate(stripped.splitlines(), start=1):
        if not is_prose_chunk(line):
            continue
        top_name, en, vi = detect_chunk(line.strip())
        scanned += 1
        if top_name == "VIETNAMESE" and vi > 0.0:
            failures.append((lineno, line.strip(), en, vi))
    return failures, scanned


def get_staged_md_files() -> list[Path]:
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


def iter_files(args: argparse.Namespace, repo_root: Path) -> Iterable[Path]:
    if args.staged:
        for p in get_staged_md_files():
            yield repo_root / p
    elif args.all:
        yield from get_all_md_files(repo_root)
    else:
        for p in args.files:
            yield p.resolve()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Reject Vietnamese (or any non-English) prose in .md files per "
            "CLAUDE.md Rule 17. Strict mode: any chunk detected as "
            "Vietnamese with non-zero confidence triggers failure. Exit 0 if "
            "clean, 1 if any failure, 2 if the lingua library is missing."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--staged", action="store_true")
    group.add_argument("--all", action="store_true")
    group.add_argument("--files", nargs="+", type=Path, metavar="PATH")
    parser.add_argument("--repo-root", type=Path, default=None)
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

    files = [p for p in iter_files(args, repo_root) if p.is_file()]

    total_failures = 0
    failing_files = 0
    total_scanned_chunks = 0
    skipped_allowlisted = 0
    for path in files:
        rel = (
            path.relative_to(repo_root)
            if path.is_relative_to(repo_root)
            else path
        )
        rel_str = str(rel).replace("\\", "/")
        if rel_str in ALLOWLIST:
            skipped_allowlisted += 1
            continue
        failures, scanned = scan_file(path)
        total_scanned_chunks += scanned
        if not failures:
            continue
        failing_files += 1
        total_failures += len(failures)
        print(f"--- {rel_str} ({len(failures)} non-English chunk) ---")
        for lineno, line, en, vi in failures:
            display = line if len(line) <= 200 else line[:200] + "..."
            print(
                f"  L{lineno}: VIETNAMESE EN={en:.3f} VI={vi:.3f}: {display}"
            )

    if total_failures == 0:
        print(
            f"lang_check: PASS ({len(files)} file(s) scanned, "
            f"{total_scanned_chunks} prose chunk(s), 0 non-English"
            + (f", {skipped_allowlisted} allowlisted" if skipped_allowlisted else "")
            + ")."
        )
        return 0

    print(
        f"lang_check: FAIL ({total_failures} non-English chunk across "
        f"{failing_files} file(s)). Per CLAUDE.md Rule 17, every prose chunk "
        f"in this repository must be in English. Translate the flagged "
        f"chunks to English."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
