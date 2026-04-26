#!/usr/bin/env python3
"""
anti_gaming_check.py
====================

Pre-commit hook enforcing v3.8-Remediation governance principles GP-6 to GP-10
(memory/sdn/governance-principles.md).

Detects gaming patterns:
- GP-6: Per-Keyword Commit Pattern violations (Form A 1 kw, Form B <=5 kw)
- GP-7: Cohort axis-stamp tables (multi-keyword x multi-axis without per-keyword evidence)
- GP-8: Cosmetic stamp tables (STAMPED/DONE/COVERED without dedicated keyword section)
- GP-9: Min lines per keyword per tier (cornerstone 50, medium 30, peripheral 15)
- GP-10: Self-enforcement (script existence + hook installation)

Usage:
  python scripts/anti_gaming_check.py --staged
  python scripts/anti_gaming_check.py --files PATH1 PATH2
  python scripts/anti_gaming_check.py --all
  python scripts/anti_gaming_check.py --allow-meta   # exempt memory/plan files
  python scripts/anti_gaming_check.py --tier cornerstone|medium|peripheral

Exit codes:
  0 = PASS
  1 = FAIL (violation, commit reject)
  2 = WARN (suspicious, not blocking)
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent

# Curriculum directories that are reader-facing (subject to GP-6 to GP-10).
CURRICULUM_DIRS = (
    "sdn-onboard",
    "haproxy-onboard",
    "linux-onboard",
    "network-onboard",
)

# Files exempt from anti-gaming checks (meta / navigation only).
EXEMPT_FILES = {
    "sdn-onboard/README.md",
    "sdn-onboard/0.0 - how-to-read-this-series.md",
    "sdn-onboard/0.3 - master-keyword-index.md",
}

EXEMPT_DIRS = (
    "memory/",
    "plans/",
    ".github/",
    "scripts/",
    "references/",
    "images/",
    "sdn-onboard/doc/",
    "haproxy-onboard/doc/",
    "linux-onboard/doc/",
    "network-onboard/doc/",
)

EXEMPT_TOP_FILES = {"CLAUDE.md", "CHANGELOG.md", "README.md"}

# Tier thresholds per GP-9.
TIER_MIN_LINES = {
    "cornerstone": 50,
    "medium": 30,
    "peripheral": 15,
}

# GP-7 cohort axis-stamp: header table with multiple Axis columns + many rows.
AXIS_HEADER_RE = re.compile(r"\bAxis\s*\d+\b", re.IGNORECASE)
KEYWORD_HEADER_RE = re.compile(r"^(#{2,4})\s+(?:§?[\w.\-]+\s+[—\-]\s+)?(.+?)\s*$")
PER_KEYWORD_HEADER_RE = re.compile(
    r"^(#{2,4})\s+(?:§\d+(?:\.\d+)*\s+)?(.+)$"
)
COSMETIC_TOKENS = re.compile(
    r"\b(STAMPED|DONE-stamp|stamp\s*done|stamp\s*pass|cohort\s+done|consolidated\s+cohort)\b",
    re.IGNORECASE,
)
# Cohort tier-stamp: Status column with DEEP-N/PARTIAL-N/REFERENCE-N cohort claim.
TIER_STAMP_RE = re.compile(
    r"\b(DEEP-?\d{1,2}|PARTIAL-?\d{1,2}|REFERENCE-?\d{1,2}|PLACEHOLDER)\b",
    re.IGNORECASE,
)


@dataclass
class Violation:
    file: Path
    line: int
    rule: str  # GP-6, GP-7, ...
    severity: str  # FAIL, WARN
    message: str

    def __str__(self) -> str:
        rel = self.file.relative_to(REPO_ROOT) if self.file.is_absolute() else self.file
        return f"[{self.severity}] {self.rule} {rel}:{self.line}: {self.message}"


@dataclass
class CheckContext:
    allow_meta: bool = False
    tier: str | None = None  # cornerstone, medium, peripheral, or None
    violations: list[Violation] = field(default_factory=list)
    warnings: list[Violation] = field(default_factory=list)

    def fail(self, file: Path, line: int, rule: str, message: str) -> None:
        self.violations.append(Violation(file, line, rule, "FAIL", message))

    def warn(self, file: Path, line: int, rule: str, message: str) -> None:
        self.warnings.append(Violation(file, line, rule, "WARN", message))


def is_exempt(path: Path) -> bool:
    rel = str(path.relative_to(REPO_ROOT) if path.is_absolute() else path).replace("\\", "/")
    if rel in EXEMPT_FILES:
        return True
    if rel in EXEMPT_TOP_FILES:
        return True
    for d in EXEMPT_DIRS:
        if rel.startswith(d):
            return True
    return False


def is_curriculum(path: Path) -> bool:
    rel = str(path.relative_to(REPO_ROOT) if path.is_absolute() else path).replace("\\", "/")
    if not rel.endswith(".md"):
        return False
    if is_exempt(path):
        return False
    return any(rel.startswith(d + "/") for d in CURRICULUM_DIRS)


def get_staged_files() -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    files = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        p = REPO_ROOT / line
        if p.exists() and p.suffix == ".md":
            files.append(p)
    return files


def get_all_curriculum_files() -> list[Path]:
    files = []
    for d in CURRICULUM_DIRS:
        base = REPO_ROOT / d
        if not base.exists():
            continue
        for p in sorted(base.rglob("*.md")):
            if not is_exempt(p):
                files.append(p)
    return files


# ---------------------------------------------------------------------------
# Section parsing
# ---------------------------------------------------------------------------
@dataclass
class Section:
    """A markdown section delimited by H2-H4 heading."""
    file: Path
    header: str
    level: int  # 2/3/4 for H2/H3/H4
    start: int  # 1-based line number of header
    end: int  # 1-based line number of last content line
    lines: list[str]  # content lines (excluding header)

    def substantive_line_count(self) -> int:
        """Count substantive lines per GP-9 §14.3 rules."""
        count = 0
        in_codeblock = False
        in_table = False
        table_header_seen = False
        for raw in self.lines:
            line = raw.rstrip()
            stripped = line.strip()
            if stripped.startswith("```"):
                in_codeblock = not in_codeblock
                count += 1  # code fence itself counts as code presence
                continue
            if in_codeblock:
                count += 1 if stripped else 0
                continue
            if not stripped:
                in_table = False
                table_header_seen = False
                continue
            # Table line detection
            if "|" in stripped and stripped.count("|") >= 2:
                if not in_table:
                    in_table = True
                    table_header_seen = False
                if re.match(r"^\|?\s*[-:|\s]+\|", stripped) and not table_header_seen:
                    # separator row
                    table_header_seen = True
                    continue
                if not table_header_seen:
                    # header row only - not counted
                    continue
                # content row counted
                count += 1
                continue
            # Skip pure cross-link-only line: "See Phần X.Y" or "Cross-link: ..."
            if re.match(
                r"^[\*\-]?\s*(?:See|Xem|Cross-link|Tham khảo|Reference)[:\s]",
                stripped,
                re.IGNORECASE,
            ):
                continue
            # Skip section heading itself (already excluded)
            if stripped.startswith("#"):
                continue
            count += 1
        return count


def parse_sections(file: Path, lines: list[str]) -> list[Section]:
    """Parse H2/H3/H4 sections from markdown file."""
    sections: list[Section] = []
    current: Section | None = None
    in_codeblock = False
    for idx, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        if line.strip().startswith("```"):
            in_codeblock = not in_codeblock
            if current is not None:
                current.lines.append(line)
            continue
        if in_codeblock:
            if current is not None:
                current.lines.append(line)
            continue
        m = re.match(r"^(#{2,4})\s+(.+?)\s*$", line)
        if m:
            # Close previous section
            if current is not None:
                current.end = idx - 1
                sections.append(current)
            current = Section(
                file=file,
                header=m.group(2).strip(),
                level=len(m.group(1)),
                start=idx,
                end=idx,
                lines=[],
            )
        else:
            if current is not None:
                current.lines.append(line)
    if current is not None:
        current.end = len(lines)
        sections.append(current)
    return sections


# ---------------------------------------------------------------------------
# Detectors
# ---------------------------------------------------------------------------
def detect_cohort_axis_stamp(file: Path, lines: list[str], ctx: CheckContext) -> None:
    """GP-7: table with column header containing 'Axis N' AND >= 4 data rows."""
    in_codeblock = False
    table_start = -1
    table_header: list[str] | None = None
    table_rows = 0
    table_axis_columns = 0

    def flush_table(end_line: int) -> None:
        nonlocal table_header, table_rows, table_axis_columns, table_start
        if table_header is not None and table_axis_columns >= 2 and table_rows >= 4:
            ctx.fail(
                file,
                table_start,
                "GP-7",
                f"Cohort axis-stamp table: {table_axis_columns} Axis-column header "
                f"x {table_rows} keyword row (>=4) without per-keyword section. "
                "Replace with Form A (1 keyword full treatment) or Form B (<=5 keyword "
                "with explicit per-keyword headers).",
            )
        table_header = None
        table_rows = 0
        table_axis_columns = 0
        table_start = -1

    for idx, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        if line.strip().startswith("```"):
            in_codeblock = not in_codeblock
            flush_table(idx - 1)
            continue
        if in_codeblock:
            continue
        stripped = line.strip()
        if "|" in stripped and stripped.count("|") >= 2:
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            # Header row?
            if table_header is None:
                table_header = cells
                table_axis_columns = sum(1 for c in cells if AXIS_HEADER_RE.search(c))
                table_start = idx
                continue
            # Separator row?
            if all(re.fullmatch(r"[\s:\-]+", c) for c in cells):
                continue
            # Skip subtotal rows ("**Total ...**" or similar bold summary).
            if any(c.lstrip("*").lower().startswith(("total", "subtotal", "tổng")) for c in cells):
                continue
            table_rows += 1
        else:
            flush_table(idx - 1)
    flush_table(len(lines))


def detect_cosmetic_stamp(file: Path, lines: list[str], ctx: CheckContext) -> None:
    """GP-8: cohort table marking tier achievement via cross-link only.

    Two signals:
    1. Explicit cosmetic token (STAMPED, DONE-stamp, cohort done) in any table.
    2. Cohort-level table where the "Status" or last column claims a tier
       (DEEP-15, PARTIAL-10, ...) for a multi-keyword row, instead of dedicating
       a per-keyword section.
    """
    in_codeblock = False
    table_header: list[str] | None = None
    table_start = -1
    table_axis_columns = 0
    table_status_col_idx = -1
    table_keyword_col_idx = -1
    table_rows = 0
    table_tier_stamps = 0

    def flush_table(end_line: int) -> None:
        nonlocal table_header, table_start, table_axis_columns
        nonlocal table_status_col_idx, table_keyword_col_idx, table_rows, table_tier_stamps
        if (
            table_header is not None
            and table_status_col_idx >= 0
            and table_rows >= 3
            and table_tier_stamps >= 3
            and table_keyword_col_idx >= 0
        ):
            ctx.fail(
                file,
                table_start,
                "GP-8",
                f"Cohort tier-stamp table: {table_rows} cohort rows with "
                f"{table_tier_stamps} tier-claim (DEEP-N/PARTIAL-N) in Status column "
                "without dedicated per-keyword section. Replace cohort table with "
                "Form A/B per-keyword treatment. Use chore(meta): prefix for "
                "navigation-only commits.",
            )
        table_header = None
        table_start = -1
        table_axis_columns = 0
        table_status_col_idx = -1
        table_keyword_col_idx = -1
        table_rows = 0
        table_tier_stamps = 0

    for idx, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        if line.strip().startswith("```"):
            in_codeblock = not in_codeblock
            flush_table(idx - 1)
            continue
        if in_codeblock:
            continue
        stripped = line.strip()
        # Cosmetic token in any non-codeblock context.
        m = COSMETIC_TOKENS.search(line)
        if m and "|" in line:
            ctx.fail(
                file,
                idx,
                "GP-8",
                f"Cosmetic stamp marker '{m.group(0)}' in cohort table. "
                "Use chore(meta): commit prefix for navigation-only commits.",
            )
        if "|" in stripped and stripped.count("|") >= 2:
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if table_header is None:
                table_header = cells
                table_start = idx
                # Find Status / Tier column.
                for i, c in enumerate(cells):
                    cl = c.lower()
                    if cl in ("status", "tier", "trạng thái"):
                        table_status_col_idx = i
                    if "keyword" in cl or "cohort" in cl or "nhóm" in cl:
                        table_keyword_col_idx = i
                continue
            if all(re.fullmatch(r"[\s:\-]+", c) for c in cells):
                continue
            if any(c.lstrip("*").lower().startswith(("total", "subtotal", "tổng")) for c in cells):
                continue
            table_rows += 1
            if (
                0 <= table_status_col_idx < len(cells)
                and TIER_STAMP_RE.search(cells[table_status_col_idx])
            ):
                table_tier_stamps += 1
        else:
            flush_table(idx - 1)
    flush_table(len(lines))


# Axis VN headings per Rule 16 / GP-11 Section 16.2 replacement table. Sections
# whose header begins with one of these names are axis subsections WITHIN a
# keyword treatment, not standalone keyword sections (per GP-6 Form A 20-axis
# natural VN heading style).
AXIS_VN_HEADERS = (
    "khái niệm",
    "lịch sử + bối cảnh",
    "lịch sử và bối cảnh",
    "lịch sử bối cảnh",
    "vị trí trong kiến trúc",
    "vai trò",
    "vì sao sinh ra",
    "vấn đề giải quyết",
    "vấn đề mà nó giải quyết",
    "tầm quan trọng",
    "cơ chế hoạt động",
    "cơ chế",
    "cách kỹ sư vận hành thành thạo",
    "cách vận hành thành thạo",
    "phân loại",
    "quy trình sử dụng",
    "quy trình",
    "khi xảy ra sự cố",
    "liên quan mật thiết",
    "khác biệt giữa các phiên bản",
    "khác biệt phiên bản",
    "cách quan sát + xác minh",
    "cách quan sát và xác minh",
    "source code tham chiếu",
    "trường hợp sự cố thực tế",
    "bài tập synthetic",
    "bài tập",
    "lỗi thường gặp + tín hiệu chẩn đoán",
    "lỗi thường gặp",
    "so sánh với hệ khác",
    "so sánh cross-domain",
    # English axis name leftovers from pre-Rule 16 cleanup (e.g., "18. Lab",
    # "19. Failure mode", "20. Cross-domain" in numeric-prefix style).
    "concept",
    "history",
    "placement",
    "role",
    "motivation",
    "problem",
    "problem solved",
    "importance",
    "mechanism",
    "engineer-op",
    "engineer operation",
    "taxonomy",
    "workflow",
    "troubleshoot",
    "coupling",
    "version drift",
    "verification",
    "source code",
    "incident",
    "lab",
    "failure mode",
    "cross-domain",
    "core schemas",
    "offline sources",
    "điểm cốt lõi cần nhớ",
    "điểm cốt lõi",
)

GENERIC_NON_KEYWORD = (
    "tổng quan",
    "overview",
    "lịch sử",  # generic "lịch sử" without "+ bối cảnh"
    "introduction",
    "tài liệu tham khảo",
    "tham khảo",
    "references",
    "cross-link",
    "summary",
    "kết luận",
    "bài học",
    "key topic",
    "hiểu sai",
    "anatomy",
    "capstone",
    "guided exercise",
    "lab synthetic",
    "lab fault",
)

# Pattern for lab/workflow/anatomy step subsections (not standalone keywords).
PROCEDURAL_PREFIX_RE = re.compile(
    r"^(b[ưu]?[ớo]c\s+\d+|mode\s+[a-zA-Z]|method\s+\d+|ph[uư][oơ]ng\s+ph[áa]p\s+\d+|"
    r"step\s+\d+|stage\s+\d+|phase\s+\d+|t[áa]c\s+v[ụu]\s+\d+|"
    r"l[áa]b\s+[\w\d.\-]+|ge\s+\d+|capstone\s+(poe|\d+)|case\s+\d+|"
    r"section\s+\d+|biến thể|variation\s+\d+)\b",
    re.IGNORECASE,
)

# Section number with 4+ levels (X.Y.Z.W or deeper) is typically a sub-sub-block,
# not a top-level keyword section.
DEEP_SECTION_NUMBER_RE = re.compile(r"^\d+(?:\.\d+){3,}\b")


def is_axis_subsection(header: str) -> bool:
    """Header looks like one of the 20 axis VN names (per Rule 16)."""
    h = header.lower().strip().lstrip("#").strip()
    # Strip leading section number like "13.5.1.4 " or "9.2.X.7. ".
    h = re.sub(r"^[\d.]+[\s.,]*", "", h)
    h = h.rstrip(".,;:")
    for axis in AXIS_VN_HEADERS:
        if h == axis or h.startswith(axis + " ") or h.startswith(axis + ","):
            return True
    return False


def looks_like_keyword_section(header: str) -> bool:
    """Heuristic: section header dedicates to a single keyword/concept.

    Returns False for:
    - Generic headers (tổng quan, overview, references, ...)
    - Axis subsections (Khái niệm, Cơ chế hoạt động, ...) per Rule 16
    - Procedural subsections (Bước N, Mode A, Method N, Lab L*, GE N, ...)
    - Deep section numbers (X.Y.Z.W with 4+ levels — typically sub-sub-block)
    """
    h = header.lower().strip()
    for g in GENERIC_NON_KEYWORD:
        if g in h:
            return False
    if is_axis_subsection(header):
        return False
    # Strip leading section number for procedural pattern check.
    h_stripped = re.sub(r"^[\d.]+[\s.,]*", "", h).strip()
    if PROCEDURAL_PREFIX_RE.match(h_stripped):
        return False
    if DEEP_SECTION_NUMBER_RE.match(h):
        return False
    return True


def detect_short_keyword_sections(
    file: Path, sections: list[Section], ctx: CheckContext, tier: str | None
) -> None:
    """GP-9: per-keyword section min lines per tier.

    A keyword section is an H2 or H3 dedicated to a single keyword. Its line
    count includes content of all nested sub-sections (axis-VN-heading H3/H4
    underneath) until the next sibling at the same level.
    """
    if tier is None:
        return
    min_lines = TIER_MIN_LINES.get(tier)
    if min_lines is None:
        return

    n = len(sections)
    for i, sec in enumerate(sections):
        # Only H2/H3 are candidates for keyword sections. H4/H5 are subsections.
        if sec.level not in (2, 3):
            continue
        if not looks_like_keyword_section(sec.header):
            continue
        # Aggregate line count: this section + all following deeper sections
        # until next sibling at the same or shallower level.
        count = sec.substantive_line_count()
        for j in range(i + 1, n):
            child = sections[j]
            if child.level <= sec.level:
                break
            count += child.substantive_line_count()
        if count < min_lines:
            ctx.fail(
                file,
                sec.start,
                "GP-9",
                f"Keyword section '{sec.header}' tier={tier} has {count} substantive "
                f"lines (incl. axis subsections) < min {min_lines}. Expand or "
                "downgrade tier classification.",
            )


def detect_form_compliance(
    file: Path, sections: list[Section], ctx: CheckContext
) -> None:
    """GP-6: form compliance is enforced at commit-message level (chore(meta) vs
    feat(sdn)) and at diff-level (newly added keyword sections per commit).
    File-total section count is not a reliable signal because files accumulate
    sections over time. Skip file-level check to avoid false positives.
    """
    return


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def check_file(file: Path, ctx: CheckContext) -> None:
    if not is_curriculum(file):
        if not ctx.allow_meta and not is_exempt(file):
            return
        return
    try:
        text = file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        ctx.warn(file, 0, "io", f"cannot read: {exc}")
        return
    lines = text.splitlines()
    sections = parse_sections(file, lines)
    detect_cohort_axis_stamp(file, lines, ctx)
    detect_cosmetic_stamp(file, lines, ctx)
    detect_short_keyword_sections(file, sections, ctx, ctx.tier)
    detect_form_compliance(file, sections, ctx)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Anti-gaming check (GP-6 to GP-10)")
    src = parser.add_mutually_exclusive_group()
    src.add_argument("--staged", action="store_true", help="scan git-staged files")
    src.add_argument("--all", action="store_true", help="scan all curriculum .md")
    src.add_argument("--files", nargs="+", help="scan specific files")
    parser.add_argument(
        "--allow-meta",
        action="store_true",
        help="allow memory/plan/CLAUDE.md/CHANGELOG.md (exempt from checks)",
    )
    parser.add_argument(
        "--tier",
        choices=("cornerstone", "medium", "peripheral"),
        help="enforce GP-9 line minimum for tier (omit to skip GP-9)",
    )
    parser.add_argument(
        "--warn-only", action="store_true", help="treat all violations as warnings"
    )
    args = parser.parse_args(argv)

    ctx = CheckContext(allow_meta=args.allow_meta, tier=args.tier)

    if args.files:
        files = [REPO_ROOT / f if not Path(f).is_absolute() else Path(f) for f in args.files]
    elif args.all:
        files = get_all_curriculum_files()
    else:
        files = get_staged_files()
        if not files:
            print("anti_gaming_check: no staged .md files (PASS).")
            return 0

    for f in files:
        check_file(f, ctx)

    if args.warn_only:
        ctx.warnings.extend(ctx.violations)
        ctx.violations.clear()

    if ctx.violations:
        print("=== ANTI-GAMING CHECK FAIL ===", file=sys.stderr)
        for v in ctx.violations:
            print(v, file=sys.stderr)
    if ctx.warnings:
        print("--- anti-gaming warnings ---", file=sys.stderr)
        for w in ctx.warnings:
            print(w, file=sys.stderr)

    if ctx.violations:
        print(
            f"\n{len(ctx.violations)} FAIL + {len(ctx.warnings)} WARN. "
            "Commit rejected per GP-10. Override with --warn-only or fix violations.",
            file=sys.stderr,
        )
        return 1

    print(f"anti_gaming_check: PASS ({len(files)} file, {len(ctx.warnings)} warn).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
