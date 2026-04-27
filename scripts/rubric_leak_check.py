#!/usr/bin/env python3
"""
rubric_leak_check.py
====================

Pre-commit hook enforcing GP-11 Internal-vs-Reader-Facing Language Separation
(memory/sdn/governance-principles.md Section 16, CLAUDE.md Rule 16).

Detects internal rubric/governance/plan terminology that has leaked into
reader-facing curriculum content (sdn-onboard/, haproxy-onboard/, etc.).

Version history:
  v1 (2026-04-26): Initial 13 patterns (axis bold-label, axis-numbered-reference,
                   cohort C/M/P, Phase G/R, Phase G/R batch, DEEP-N, PARTIAL-N,
                   REFERENCE-N, PLACEHOLDER, rubric meta-term, anti-gaming-meta,
                   GP-N reference, Form A/B per GP-).
  v2 (2026-04-27): +7 patterns from master audit OVS block findings:
                   axis-numbered-vn-heading, cohort-cornerstone-phrase,
                   tier-cornerstone-informal, tier-importance-bold-label,
                   phase-session-reference, cohort-batch-stamp-leftover,
                   stale-phase-compat-note. Total 20 patterns.
                   See plans/sdn/v3.9-ovs-block-hotfix.md Phase S0.

Usage:
  python scripts/rubric_leak_check.py --staged
  python scripts/rubric_leak_check.py --files A B C
  python scripts/rubric_leak_check.py --all
  python scripts/rubric_leak_check.py --allow-meta   # exempt memory/plan
  python scripts/rubric_leak_check.py --report       # full violation report
  python scripts/rubric_leak_check.py --warn-only    # advisory mode, no block

Exit codes:
  0 = PASS
  1 = FAIL (violation, commit reject)
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CURRICULUM_DIRS = (
    "sdn-onboard",
    "haproxy-onboard",
    "linux-onboard",
    "network-onboard",
)

# Files exempt from rubric-leak check (meta files, audit-aware audience).
EXEMPT_FILES_REL = {
    "sdn-onboard/0.3 - master-keyword-index.md",  # status code allowed
    "sdn-onboard/0.0 - how-to-read-this-series.md",
}

EXEMPT_DIRS = (
    "memory/",
    "plans/",
    "scripts/",
    "references/",
    "images/",
    ".github/",
    ".git/",
    "sdn-onboard/doc/",
    "haproxy-onboard/doc/",
    "linux-onboard/doc/",
    "network-onboard/doc/",
)

EXEMPT_TOP_FILES = {"CLAUDE.md", "CHANGELOG.md", "README.md"}

# Rubric leak patterns (regex, name, severity, suggested replacement).
LEAK_PATTERNS = [
    # Axis labels (most common Phase G v3.7 leak)
    (
        re.compile(r"\*\*Axis\s*\d+\b[^*]*\.\*\*", re.IGNORECASE),
        "axis-bold-label",
        "FAIL",
        "Replace **Axis N category.** with natural VN heading per GP-11 Section 16.2 table.",
    ),
    (
        re.compile(r"\bAxis\s+(?:1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20)\b"),
        "axis-numbered-reference",
        "FAIL",
        "Replace 'Axis N' inline reference with category name (Khái niệm, Cơ chế, ...).",
    ),
    # Cohort label
    (
        re.compile(r"\bcohort\s+[CMP]\d+\b", re.IGNORECASE),
        "cohort-label",
        "FAIL",
        "Replace 'cohort C7/M5/P21' with descriptive group name or omit.",
    ),
    # Phase plan reference
    (
        re.compile(r"\bPhase\s+[GR](?:[0-9]+(?:\.[0-9]+)*|\b)"),
        "phase-plan-reference",
        "FAIL",
        "Replace 'Phase G/R N' plan reference with prose 'expansion 2026-04' or omit.",
    ),
    (
        re.compile(r"\bPhase\s+[GR]\s+batch\s+\d+\b", re.IGNORECASE),
        "phase-batch-reference",
        "FAIL",
        "Replace 'Phase G batch N' with prose or omit.",
    ),
    # Tier labels
    (
        re.compile(r"\bDEEP-?\d{1,2}\b"),
        "tier-label-deep",
        "FAIL",
        "Replace 'DEEP-20/15' tier label with prose 'đầy đủ' or omit.",
    ),
    (
        re.compile(r"\bPARTIAL-?\d{1,2}\b"),
        "tier-label-partial",
        "FAIL",
        "Replace 'PARTIAL-10' tier label with prose or omit.",
    ),
    (
        re.compile(r"\bREFERENCE-?\d{1,2}\b"),
        "tier-label-reference",
        "FAIL",
        "Replace 'REFERENCE-5' tier label with prose or omit.",
    ),
    (
        re.compile(r"\bPLACEHOLDER\b"),
        "tier-label-placeholder",
        "FAIL",
        "Replace 'PLACEHOLDER' tier label with prose or omit.",
    ),
    # Rubric meta-term
    (
        re.compile(r"\brubric\s+(?:20-axis|20\s*axis|13[\s-]tiêu[\s-]chí)\b", re.IGNORECASE),
        "rubric-meta-term",
        "FAIL",
        "Replace 'rubric 20-axis / 13 tiêu chí' meta-reference with descriptive prose or omit.",
    ),
    # Anti-gaming meta-term
    (
        re.compile(r"\b(?:anti-gaming|gaming\s+pattern|cosmetic\s+stamp|cohort\s+stamp)\b", re.IGNORECASE),
        "anti-gaming-meta",
        "FAIL",
        "Replace governance meta-term with prose explanation if needed, or omit.",
    ),
    # Governance principle reference
    (
        re.compile(r"\bGP-(?:1|2|3|4|5|6|7|8|9|10|11)\b"),
        "governance-principle-reference",
        "FAIL",
        "Replace 'GP-N' governance reference (CLAUDE.md / memory/ only).",
    ),
    # Form A/B from GP-6 commit pattern
    (
        re.compile(r"\bForm\s+[AB]\s+(?:per|GP-)\b", re.IGNORECASE),
        "form-ab-reference",
        "FAIL",
        "Replace 'Form A/B per GP-6' commit-pattern reference (internal only).",
    ),
    # ====================================================================
    # V2 patterns (added 2026-04-27 per master audit OVS block findings)
    # See plans/sdn/v3.9-ovs-block-hotfix.md Phase S0 for context.
    # ====================================================================
    # Axis-numbered VN heading (e.g., 9.32 §9.32.1/§9.32.2 pattern).
    # Catches: ### 1. Khái niệm | ### 7. Tầm quan trọng | ### 20. So sánh
    (
        re.compile(
            r"^#{2,4}\s+\d{1,2}\.\s+("
            r"Khái\s*niệm|"
            r"Lịch\s*sử|"
            r"Vị\s*trí|"
            r"Vai\s*trò|"
            r"Vì\s*sao|"
            r"Vấn\s*đề|"
            r"Tầm\s*quan\s*trọng|"
            r"Cơ\s*chế|"
            r"Cách\s*kỹ\s*sư|"
            r"Phân\s*loại|"
            r"Quy\s*trình|"
            r"Khi\s*xảy\s*ra|"
            r"Liên\s*quan|"
            r"Khác\s*biệt|"
            r"Cách\s*quan\s*sát|"
            r"Source\s*code|"
            r"Trường\s*hợp|"
            r"Bài\s*tập|"
            r"Lỗi\s*thường|"
            r"So\s*sánh|"
            r"Cross[\s\-]?domain|"
            r"Comparison"
            r")\b",
            re.IGNORECASE | re.MULTILINE,
        ),
        "axis-numbered-vn-heading",
        "FAIL",
        "Replace '### N. Khái niệm' với '### Khái niệm' (drop axis number per Rule 16 §16.2).",
    ),
    # Cohort + cornerstone phrase in body (not strict cohort C/M/P\d label).
    # Catches: 'cohort cornerstone OVS datapath', 'cohort cornerstone classifier'
    (
        re.compile(r"\bcohort\s+cornerstone\b", re.IGNORECASE),
        "cohort-cornerstone-phrase",
        "FAIL",
        "Drop 'cohort cornerstone' qualifier — engineer reader không cần meta-tier reference.",
    ),
    # Informal tier reference: 'Tier 1 cornerstone', 'cornerstone tier 1 tuyệt đối'
    (
        re.compile(
            r"\b(?:[Tt]ier\s*\d+\s+cornerstone|cornerstone\s+tier\s*\d+(?:\s+tuyệt\s*đối)?)\b"
        ),
        "tier-cornerstone-informal",
        "FAIL",
        "Drop 'Tier N cornerstone' / 'cornerstone tier N tuyệt đối' phrasing — author tier-stamp leak.",
    ),
    # Tier importance bold label: '**Tier importance: cornerstone tuyệt đối**'
    (
        re.compile(
            r"\*\*\s*[Tt]ier\s+importance\s*:\s*cornerstone(?:\s+tuyệt\s*đối)?\s*\*\*"
        ),
        "tier-importance-bold-label",
        "FAIL",
        "Drop '**Tier importance: cornerstone tuyệt đối**' label — meta-rubric reference.",
    ),
    # Phase H/I/J/K/L/S session reference (V1 catches Phase G/R only).
    # Catches: 'Phase H session S39', 'Phase H session', 'Phase S0 session'
    (
        re.compile(r"\bPhase\s+[HIJKLS]\d*\s+session\b", re.IGNORECASE),
        "phase-session-reference",
        "FAIL",
        "Drop 'Phase H/S session SN' embedded reference — replace với '(mở rộng 2026-04)' nếu cần date.",
    ),
    # Cohort batch limit / compact treatment leftover (V3.7 Phase G gaming).
    # Catches: '(compact treatment per cohort batch limit)'
    (
        re.compile(
            r"\b(?:compact\s+treatment\s+per\s+cohort|cohort\s+batch\s+limit|per\s+cohort\s+batch)\b",
            re.IGNORECASE,
        ),
        "cohort-batch-stamp-leftover",
        "FAIL",
        "Drop '(compact treatment per cohort batch limit)' — internal commit-pattern reference.",
    ),
    # Stale Phase A/B/C/D/E/F compatibility note.
    # Catches: '(reference, giữ tương thích content Phase B)'
    (
        re.compile(
            r"\(\s*reference\s*,\s*giữ\s+tương\s+thích\s+content\s+Phase\s+[A-Z]\s*\)",
            re.IGNORECASE,
        ),
        "stale-phase-compat-note",
        "FAIL",
        "Drop '(reference, giữ tương thích content Phase B)' parenthetical — stale plan compatibility.",
    ),
]


@dataclass
class Leak:
    file: Path
    line: int
    column: int
    pattern_name: str
    severity: str
    matched: str
    suggestion: str

    def __str__(self) -> str:
        rel = self.file.relative_to(REPO_ROOT) if self.file.is_absolute() else self.file
        return (
            f"[{self.severity}] {self.pattern_name} {rel}:{self.line}:{self.column}: "
            f"matched '{self.matched}' — {self.suggestion}"
        )


def is_exempt(path: Path) -> bool:
    rel = str(path.relative_to(REPO_ROOT) if path.is_absolute() else path).replace("\\", "/")
    if rel in EXEMPT_FILES_REL:
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
        p = REPO_ROOT / line.strip()
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


def scan_file(file: Path, leaks: list[Leak]) -> None:
    """Scan file line-by-line. Skip code blocks (fenced ```...```)."""
    if not is_curriculum(file):
        return
    try:
        text = file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return
    in_codeblock = False
    for idx, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_codeblock = not in_codeblock
            continue
        if in_codeblock:
            continue
        for pattern, name, severity, suggestion in LEAK_PATTERNS:
            for m in pattern.finditer(line):
                leaks.append(
                    Leak(
                        file=file,
                        line=idx,
                        column=m.start() + 1,
                        pattern_name=name,
                        severity=severity,
                        matched=m.group(0),
                        suggestion=suggestion,
                    )
                )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Rubric leak check (GP-11 / CLAUDE.md Rule 16)"
    )
    src = parser.add_mutually_exclusive_group()
    src.add_argument("--staged", action="store_true")
    src.add_argument("--all", action="store_true")
    src.add_argument("--files", nargs="+")
    parser.add_argument("--allow-meta", action="store_true")
    parser.add_argument("--report", action="store_true", help="full per-file count")
    parser.add_argument("--warn-only", action="store_true")
    args = parser.parse_args(argv)

    if args.files:
        files = [REPO_ROOT / f if not Path(f).is_absolute() else Path(f) for f in args.files]
    elif args.all:
        files = get_all_curriculum_files()
    else:
        files = get_staged_files()
        if not files:
            print("rubric_leak_check: no staged .md files (PASS).")
            return 0

    leaks: list[Leak] = []
    for f in files:
        scan_file(f, leaks)

    if args.warn_only:
        # Treat as advisory only.
        for v in leaks:
            print(f"[WARN] {v}", file=sys.stderr)
        print(f"rubric_leak_check (warn-only): {len(leaks)} potential leak across {len(files)} file.")
        return 0

    if leaks:
        print("=== RUBRIC LEAK CHECK FAIL ===", file=sys.stderr)
        # Group by file for readability.
        per_file: dict[Path, list[Leak]] = {}
        for v in leaks:
            per_file.setdefault(v.file, []).append(v)
        for f, vs in sorted(per_file.items()):
            rel = f.relative_to(REPO_ROOT) if f.is_absolute() else f
            print(f"\n--- {rel} ({len(vs)} leak) ---", file=sys.stderr)
            for v in vs[:20]:
                print(f"  L{v.line}:{v.column} [{v.pattern_name}] '{v.matched}'", file=sys.stderr)
            if len(vs) > 20:
                print(f"  ... {len(vs) - 20} more", file=sys.stderr)
        print(
            f"\nTotal {len(leaks)} leak across {len(per_file)} file. "
            "Commit rejected per GP-11 / CLAUDE.md Rule 16. "
            "Run with --report for full detail or --warn-only to bypass.",
            file=sys.stderr,
        )
        return 1

    print(f"rubric_leak_check: PASS ({len(files)} file scanned).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
