#!/usr/bin/env python3
"""Inventory Vietnamese prose chunks per file in sdn-onboard.

Plan v3.12 scoping tool. Walks every Markdown file under sdn-onboard,
runs the same chunker as scripts/lang_check.py, classifies each prose
chunk with the lingua-py binary classifier (English vs. Vietnamese,
strict mode), and emits a per-file count of non-English chunks.

The output is a TSV that the v3.12 plan uses to decide cohort
sequencing. We do NOT enforce, we only count.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import lang_check  # noqa: E402

REPO_ROOT = ROOT
SDN_DIR = REPO_ROOT / "sdn-onboard"


def scan_file_count(path: Path) -> tuple[int, int]:
    """Return (vi_chunks, total_chunks) for one file."""
    failures, total = lang_check.scan_file(path)
    return (len(failures), total)


def main() -> int:
    files = sorted(SDN_DIR.glob("*.md"))
    print("file\ttotal_chunks\tvi_chunks\tvi_pct\ttotal_lines")
    grand_vi = 0
    grand_total = 0
    grand_lines = 0
    cohorts: dict[str, list[tuple[str, int, int]]] = {
        "clean": [],
        "light": [],
        "medium": [],
        "heavy": [],
    }
    for path in files:
        try:
            vi, total = scan_file_count(path)
        except Exception as exc:
            print(f"{path.name}\tERR\tERR\tERR\t{exc}")
            continue
        with path.open(encoding="utf-8", errors="replace") as fh:
            line_count = sum(1 for _ in fh)
        pct = (vi / total * 100) if total else 0.0
        print(f"{path.name}\t{total}\t{vi}\t{pct:.1f}\t{line_count}")
        grand_vi += vi
        grand_total += total
        grand_lines += line_count
        if vi == 0:
            cohorts["clean"].append((path.name, vi, line_count))
        elif vi <= 10:
            cohorts["light"].append((path.name, vi, line_count))
        elif vi <= 50:
            cohorts["medium"].append((path.name, vi, line_count))
        else:
            cohorts["heavy"].append((path.name, vi, line_count))
    print()
    if grand_total > 0:
        gpct = grand_vi / grand_total * 100
    else:
        gpct = 0.0
    print(
        f"# TOTAL files={len(files)} chunks={grand_total} "
        f"vi_chunks={grand_vi} pct={gpct:.1f}% lines={grand_lines}"
    )
    print()
    for name, items in cohorts.items():
        items.sort(key=lambda row: row[1], reverse=True)
        print(f"# COHORT {name}: {len(items)} file(s)")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
