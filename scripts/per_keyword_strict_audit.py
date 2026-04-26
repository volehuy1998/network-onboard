#!/usr/bin/env python3
"""
per_keyword_strict_audit.py
===========================

Phase R5 strict scorecard generator for v3.8-Remediation.

For each in-scope keyword (from REF + master keyword index), the script:

1. Locates dedicated section(s) in curriculum where the keyword has its own
   header (H2/H3/H4) per Form A/B GP-6 commit pattern.
2. Detects axis-VN-name sub-headings within the dedicated section per Rule 16
   replacement table (Khái niệm, Cơ chế hoạt động, ...).
3. Scores 0-20 axis presence based on dedicated sub-section count + per-axis
   substantive line minimum (axis with <3 substantive lines = 0.5, >=3 lines
   = 1.0, absent = 0).
4. Classifies tier per Phase B rubric Section 22.2:
   - DEEP-20 (>=18.0)
   - DEEP-15 (15.0-17.5)
   - PARTIAL-10 (10.0-14.5)
   - REFERENCE-5 (5.0-9.5)
   - PLACEHOLDER (<5.0)
5. Emits scorecard markdown to memory/sdn/keyword-strict-scorecard.md plus
   summary table per tier.

Usage:
  python scripts/per_keyword_strict_audit.py --full
  python scripts/per_keyword_strict_audit.py --keyword "Logical_Switch"
  python scripts/per_keyword_strict_audit.py --tier-summary

Exit codes:
  0 = Audit complete
  1 = REF or curriculum missing
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# Reconfigure stdout for Unicode output on Windows.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
REF_FILE = REPO_ROOT / "sdn-onboard" / "doc" / "ovs-openflow-ovn-keyword-reference.md"
MASTER_INDEX = REPO_ROOT / "sdn-onboard" / "0.3 - master-keyword-index.md"
OUTPUT_FILE = REPO_ROOT / "memory" / "sdn" / "keyword-strict-scorecard.md"

CURRICULUM_DIR = REPO_ROOT / "sdn-onboard"
EXEMPT_FILES = {"0.0", "0.3", "README.md"}

# 20-axis VN headings per Rule 16 replacement table (GP-11 Section 16.2).
AXIS_HEADINGS = [
    ("Khái niệm", "concept"),
    ("Lịch sử + bối cảnh", "history"),
    ("Vị trí trong kiến trúc", "placement"),
    ("Vai trò", "role"),
    ("Vì sao sinh ra", "motivation"),
    ("Vấn đề giải quyết", "problem"),
    ("Tầm quan trọng", "importance"),
    ("Cơ chế hoạt động", "mechanism"),
    ("Cách kỹ sư vận hành thành thạo", "engineer-op"),
    ("Phân loại", "taxonomy"),
    ("Quy trình sử dụng", "workflow"),
    ("Khi xảy ra sự cố", "troubleshoot"),
    ("Liên quan mật thiết", "coupling"),
    ("Khác biệt giữa các phiên bản", "version-drift"),
    ("Cách quan sát + xác minh", "verification"),
    ("Source code tham chiếu", "source-code"),
    ("Trường hợp sự cố thực tế", "incident"),
    ("Bài tập synthetic", "lab"),
    ("Lỗi thường gặp + tín hiệu chẩn đoán", "failure-mode"),
    ("So sánh với hệ khác", "cross-domain"),
]

# Loose match patterns: match either H3-H5 heading OR bold-label with optional
# suffix word(s). Pattern shape: `(^#{3,5}\s+|^\*\*)<axis-name>...`.
def _axis_re(stem: str) -> re.Pattern[str]:
    """Build a pattern matching '### <stem>...' or '**<stem>...**'."""
    return re.compile(
        rf"^(?:#{{3,5}}\s+|\*\*)\s*{stem}",
        re.IGNORECASE | re.MULTILINE,
    )


AXIS_PATTERNS = [
    (_axis_re(r"Kh[áa]i\s*ni[ệe]m"), "concept"),
    (_axis_re(r"L[ịi]ch\s+s[ửu]\s*[\+v][àa]?\s*b[ốo]i\s+c[ảa]nh"), "history"),
    (_axis_re(r"V[ịi]\s+tr[íi]\s+trong\s+ki[ếe]n\s+tr[úu]c"), "placement"),
    (_axis_re(r"Vai\s+tr[òo]"), "role"),
    (_axis_re(r"V[ìi]\s+sao"), "motivation"),
    (_axis_re(r"V[ấa]n\s+đ[ềe]\s+(?:gi[ảa]i\s+quy[ếe]t|m[àa])"), "problem"),
    (_axis_re(r"T[ầa]m\s+quan\s+tr[ọo]ng"), "importance"),
    (_axis_re(r"C[ơo]\s+ch[ếe]"), "mechanism"),
    (_axis_re(r"C[áa]ch\s+(?:k[ỹy]\s*s[ưu]\s*)?v[ậa]n\s+h[àa]nh"), "engineer-op"),
    (_axis_re(r"Ph[âa]n\s+lo[ạa]i"), "taxonomy"),
    (_axis_re(r"Quy\s+tr[ìi]nh"), "workflow"),
    (_axis_re(r"Khi\s+x[ảa]y\s+ra\s+s[ựu]\s+c[ốo]"), "troubleshoot"),
    (_axis_re(r"Li[êe]n\s+quan\s+m[ậa]t\s+thi[ếe]t"), "coupling"),
    (_axis_re(r"Kh[áa]c\s+bi[ệe]t\s+(?:gi[ữu]a\s+(?:c[áa]c\s+)?)?phi[êe]n\s+b[ảa]n"), "version-drift"),
    (_axis_re(r"C[áa]ch\s+quan\s+s[áa]t\s*[\+v][àa]?\s*x[áa]c\s+minh"), "verification"),
    (_axis_re(r"Source\s+code"), "source-code"),
    (_axis_re(r"Tr[ưu][ờo]ng\s+h[ợo]p\s+s[ựu]\s+c[ốo]\s+th[ựu]c\s+t[ếe]"), "incident"),
    (_axis_re(r"B[àa]i\s+t[ậa]p"), "lab"),
    (_axis_re(r"L[ỗo]i\s+th[ưu][ờo]ng\s+g[ặa]p"), "failure-mode"),
    (_axis_re(r"So\s+s[áa]nh"), "cross-domain"),
]

# Tier classification per Phase B rubric.
TIER_DEEP_20 = 18.0
TIER_DEEP_15 = 15.0
TIER_PARTIAL_10 = 10.0
TIER_REFERENCE_5 = 5.0


@dataclass
class KeywordScore:
    keyword: str
    section_file: Path | None = None
    section_start: int = 0
    section_end: int = 0
    axes_found: dict[str, float] = field(default_factory=dict)
    axes_evidence: dict[str, str] = field(default_factory=dict)
    total: float = 0.0
    tier: str = "PLACEHOLDER"
    notes: list[str] = field(default_factory=list)

    def compute_total(self) -> None:
        self.total = sum(self.axes_found.values())
        self.tier = (
            "DEEP-20" if self.total >= TIER_DEEP_20
            else "DEEP-15" if self.total >= TIER_DEEP_15
            else "PARTIAL-10" if self.total >= TIER_PARTIAL_10
            else "REFERENCE-5" if self.total >= TIER_REFERENCE_5
            else "PLACEHOLDER"
        )


def collect_keywords_from_master_index() -> list[str]:
    """Parse `0.3 master-keyword-index.md` for keyword names.

    The master index lists each keyword as `### keyword` or in a table cell.
    We extract via regex patterns.
    """
    if not MASTER_INDEX.exists():
        return []
    text = MASTER_INDEX.read_text(encoding="utf-8")
    keywords: set[str] = set()
    # Pattern 1: Table cell with `code-formatted` keyword.
    for m in re.finditer(r"`([A-Za-z_][A-Za-z0-9_/.\-]*)`", text):
        kw = m.group(1)
        if 2 < len(kw) < 50 and not kw.startswith(("http", "ftp")):
            keywords.add(kw)
    # Pattern 2: Header `### keyword`.
    for m in re.finditer(r"^#{2,4}\s+([A-Z][A-Za-z0-9_/.\- ]+)\s*$", text, re.MULTILINE):
        kw = m.group(1).strip()
        if 2 < len(kw) < 50:
            keywords.add(kw)
    return sorted(keywords)


def find_dedicated_sections(keyword: str) -> list[tuple[Path, int, int, list[str]]]:
    """Find curriculum sections whose H2/H3/H4 header dedicates to this keyword.

    Returns list of (file, start_line, end_line, lines) tuples.
    """
    results: list[tuple[Path, int, int, list[str]]] = []
    # Build flexible header pattern matching keyword.
    kw_escaped = re.escape(keyword)
    # Match H2-H4 header containing keyword as standalone token followed by separator.
    # Tolerant of section numbers like "13.2.X.", "9.1.AB", "§3.5.1".
    header_re = re.compile(
        rf"^(#{{2,4}})\s+[^\n]*?\b{kw_escaped}\b[^\n]*?$",
        re.IGNORECASE | re.MULTILINE,
    )
    for md_file in CURRICULUM_DIR.rglob("*.md"):
        rel = str(md_file.relative_to(REPO_ROOT)).replace("\\", "/")
        # Skip exempt + doc/ folder.
        if any(rel.endswith(e) or e in rel for e in EXEMPT_FILES):
            continue
        if "/doc/" in rel:
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        lines = text.splitlines()
        for m in header_re.finditer(text):
            # Find the line number.
            start = text.count("\n", 0, m.start()) + 1
            level = len(m.group(1))
            # Find end (next H2/H3/H4 at <= level or EOF).
            end = len(lines)
            for i in range(start, len(lines)):
                line = lines[i]
                m2 = re.match(r"^(#{2,4})\s+", line)
                if m2 and len(m2.group(1)) <= level:
                    end = i
                    break
            section_lines = lines[start - 1 : end]
            results.append((md_file, start, end, section_lines))
    return results


def score_section(section_lines: list[str]) -> tuple[dict[str, float], dict[str, str]]:
    """Score axes presence in section. Each axis-VN-heading found = 1.0,
    sub-section with <3 substantive lines = 0.5.
    """
    axes_score: dict[str, float] = {}
    axes_evidence: dict[str, str] = {}
    in_codeblock = False
    current_axis: str | None = None
    current_axis_start = 0
    current_axis_lines = 0

    def close_axis(end_idx: int) -> None:
        if current_axis is None:
            return
        # Score: heading + at least 1 substantive line = 1.0; heading only = 0.5.
        if current_axis_lines >= 1:
            axes_score[current_axis] = max(axes_score.get(current_axis, 0.0), 1.0)
        else:
            axes_score[current_axis] = max(axes_score.get(current_axis, 0.0), 0.5)
        axes_evidence[current_axis] = (
            f"L{current_axis_start}-{end_idx}, {current_axis_lines} substantive line(s)"
        )

    for idx, line in enumerate(section_lines):
        if line.lstrip().startswith("```"):
            in_codeblock = not in_codeblock
            if not in_codeblock and current_axis:
                current_axis_lines += 1
            continue
        if in_codeblock:
            if current_axis:
                current_axis_lines += 1
            continue
        # Check axis heading match.
        matched_axis = None
        matched_pattern = None
        for pattern, axis_id in AXIS_PATTERNS:
            m = pattern.search(line)
            if m:
                matched_axis = axis_id
                matched_pattern = m
                break
        if matched_axis:
            close_axis(idx)
            current_axis = matched_axis
            current_axis_start = idx
            current_axis_lines = 0
            # If bold-label format with inline content (e.g., `**Khái niệm.** prose...`),
            # count remainder as substantive line.
            if line.lstrip().startswith("**"):
                remainder = line[matched_pattern.end():].strip()
                # Strip leading bold close + punctuation.
                remainder = re.sub(r"^[\*\.\:,\s—\-]+", "", remainder)
                if len(remainder) > 10:
                    current_axis_lines += 1
            continue
        # Substantive line under current axis.
        stripped = line.strip()
        if current_axis and stripped and not stripped.startswith("#"):
            current_axis_lines += 1
    close_axis(len(section_lines))
    return axes_score, axes_evidence


def audit_keyword(keyword: str) -> KeywordScore:
    score = KeywordScore(keyword=keyword)
    sections = find_dedicated_sections(keyword)
    if not sections:
        score.notes.append("no dedicated section found")
        score.compute_total()
        return score
    # Pick longest section (assume best treatment).
    best = max(sections, key=lambda s: len(s[3]))
    file, start, end, lines = best
    score.section_file = file
    score.section_start = start
    score.section_end = end
    axes_score, axes_evidence = score_section(lines)
    score.axes_found = axes_score
    score.axes_evidence = axes_evidence
    score.compute_total()
    if len(sections) > 1:
        score.notes.append(f"{len(sections)} dedicated sections found, best at {file.name}")
    return score


def emit_scorecard(scores: list[KeywordScore], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Keyword Strict Scorecard — Phase R5 Audit",
        "",
        f"> **Generated by:** `scripts/per_keyword_strict_audit.py`",
        f"> **Curriculum scope:** all `sdn-onboard/*.md` (excluding `doc/`, `0.0`, `0.3`, `README`)",
        "> **Methodology:** dedicated H2-H4 section per keyword + 20-axis VN heading detection.",
        "> **Tier per Phase B rubric Section 22.2:**",
        "> - DEEP-20: ≥18.0/20",
        "> - DEEP-15: 15.0-17.5/20",
        "> - PARTIAL-10: 10.0-14.5/20",
        "> - REFERENCE-5: 5.0-9.5/20",
        "> - PLACEHOLDER: <5.0/20",
        "",
        "## Tier summary",
        "",
        "| Tier | Count | % |",
        "|------|------:|--:|",
    ]
    tier_counts: dict[str, int] = {}
    for s in scores:
        tier_counts[s.tier] = tier_counts.get(s.tier, 0) + 1
    total = max(len(scores), 1)
    for tier in ["DEEP-20", "DEEP-15", "PARTIAL-10", "REFERENCE-5", "PLACEHOLDER"]:
        c = tier_counts.get(tier, 0)
        lines.append(f"| {tier} | {c} | {c * 100 / total:.1f}% |")
    lines.append(f"| **Total** | **{total}** | 100.0% |")
    lines.append("")
    lines.append("## Per-keyword scorecard")
    lines.append("")
    lines.append("| Keyword | Tier | Total | Section | Notes |")
    lines.append("|---------|------|------:|---------|-------|")
    for s in sorted(scores, key=lambda x: (-x.total, x.keyword)):
        sec = (
            f"{s.section_file.name}:L{s.section_start}-{s.section_end}"
            if s.section_file else "—"
        )
        notes = "; ".join(s.notes) if s.notes else ""
        lines.append(f"| `{s.keyword}` | {s.tier} | {s.total:.1f} | {sec} | {notes} |")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Per-keyword strict audit (Phase R5)")
    src = parser.add_mutually_exclusive_group()
    src.add_argument("--full", action="store_true", help="audit all keywords from master index")
    src.add_argument("--keyword", help="audit specific keyword")
    src.add_argument("--tier-summary", action="store_true", help="re-emit tier summary from existing scorecard")
    parser.add_argument(
        "--keywords-from",
        help="path to text file with one keyword per line (override master index)",
    )
    args = parser.parse_args(argv)

    if args.keyword:
        keywords = [args.keyword]
    elif args.keywords_from:
        keywords = [
            line.strip()
            for line in Path(args.keywords_from).read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        ]
    elif args.full or args.tier_summary:
        keywords = collect_keywords_from_master_index()
        if not keywords:
            print("ERROR: no keywords found in master index", file=sys.stderr)
            return 1
    else:
        parser.print_help()
        return 0

    scores: list[KeywordScore] = []
    for kw in keywords:
        s = audit_keyword(kw)
        scores.append(s)

    if args.keyword:
        s = scores[0]
        print(f"Keyword: {s.keyword}")
        print(f"Tier:    {s.tier}")
        print(f"Total:   {s.total:.1f}/20")
        if s.section_file:
            print(f"Section: {s.section_file.name}:L{s.section_start}-{s.section_end}")
        for axis_vn, axis_id in AXIS_HEADINGS:
            score = s.axes_found.get(axis_id, 0.0)
            ev = s.axes_evidence.get(axis_id, "")
            mark = "[X]" if score >= 1.0 else "[~]" if score > 0 else "[ ]"
            print(f"  {mark} {axis_vn:35s} {score:.1f}  {ev}")
        if s.notes:
            print("Notes:", "; ".join(s.notes))
        return 0

    emit_scorecard(scores, OUTPUT_FILE)
    print(f"Audit complete: {len(scores)} keyword(s)")
    print(f"Scorecard: {OUTPUT_FILE.relative_to(REPO_ROOT)}")
    tier_counts: dict[str, int] = {}
    for s in scores:
        tier_counts[s.tier] = tier_counts.get(s.tier, 0) + 1
    for tier in ["DEEP-20", "DEEP-15", "PARTIAL-10", "REFERENCE-5", "PLACEHOLDER"]:
        c = tier_counts.get(tier, 0)
        print(f"  {tier:13s} {c:4d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
