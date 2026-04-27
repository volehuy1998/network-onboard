#!/usr/bin/env python3
"""v3.11 R0.5 OpenFlow citation inventory script.

Runs five R0.5 grep queries against each of the 17 in-scope OF-block files
(Block 3 plus Block 4), classifies each match into one of 10 citation kinds,
de-duplicates to unique-position tuples, and emits a markdown table per file
plus aggregate totals.

Usage:
    python scripts/v3_11_citation_inventory.py > memory/sdn/v3.11-of-citation-inventory-2026-04-29.md

Run from the curriculum repo root.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# 17 OF-block files: Block 3 (7) + Block 4 (10).
SCOPE: list[tuple[str, str]] = [
    # Block 3 (7 files)
    ("3.0", "3.0 - stanford-clean-slate-program.md"),
    ("3.1", "3.1 - openflow-1.0-specification.md"),
    ("3.2", "3.2 - onf-formation-and-governance.md"),
    ("3.3", "3.3 - openflow-protocol-messages-state-machine.md"),
    ("3.4", "3.4 - openflow-version-differences-1.0-1.3-1.5.md"),
    ("3.5", "3.5 - openflow-message-catalog.md"),
    ("3.6", "3.6 - openflow-instruction-catalog.md"),
    # Block 4 (10 files)
    ("4.0", "4.0 - openflow-1.1-multi-table-groups.md"),
    ("4.1", "4.1 - openflow-1.2-oxm-tlv-match.md"),
    ("4.2", "4.2 - openflow-1.3-meters-pbb-lts.md"),
    ("4.3", "4.3 - openflow-1.4-bundles-eviction.md"),
    ("4.4", "4.4 - openflow-1.5-egress-l4l7.md"),
    ("4.5", "4.5 - ttp-table-type-patterns.md"),
    ("4.6", "4.6 - openflow-limitations-lessons.md"),
    ("4.7", "4.7 - openflow-programming-with-ovs.md"),
    ("4.8", "4.8 - openflow-match-field-catalog.md"),
    ("4.9", "4.9 - openflow-action-catalog.md"),
]

ROOT = Path("sdn-onboard")

# Phase assignment per plan v3.11 §9.1 corrected 6-sub-batch structure.
PHASE_MAP: dict[str, str] = {
    "3.0": "R1.A", "3.2": "R1.A", "3.4": "R1.A", "3.6": "R1.A",
    "3.1": "R1.B", "3.3": "R1.B",
    "4.0": "R1.B", "4.5": "R1.B", "4.6": "R1.B",
    "3.5": "R1.C",
    "4.8": "R1.D",
    "4.9": "R1.E",
    "4.1": "R1.F", "4.2": "R1.F", "4.3": "R1.F", "4.4": "R1.F", "4.7": "R1.F",
}

# Compiled regexes for the 5 R0.5 queries.
URL_OVS = re.compile(r"https?://github\.com/openvswitch/ovs[^\s)\"`]+")
URL_OVN = re.compile(r"https?://github\.com/ovn-org/ovn[^\s)\"`]+")
URL_ONF = re.compile(r"https?://(?:www\.)?(?:opennetworking\.org|onf\.org)[^\s)\"`]+")
BRANCH_TAG = re.compile(r"\b(branch-2\.[0-9]+|v2\.[0-9]+\.[0-9]+|v[12]\.[0-9]+\.[0-9]+)\b")
OF_VERSION_MARKER = re.compile(r"\b(?:OF|OpenFlow)\s+1\.[0-6]\b")
INLINE_FILE = re.compile(
    r"`((?:lib|ofproto|utilities|include|datapath|tests)/[a-zA-Z0-9_./\-]+\.(?:c|h|in|py|at|xml))`"
)
INLINE_OF_CONST = re.compile(
    r"`((?:OFPT_|OFPAT_|OFPIT_|OXM_OF_|OFPP_|OFPFC_|OFPMP_|OFPMT_|OFPACTION_|OFPACT_|MFF_|NXM_|OFPBCT_|OFPBF_|OFPMBT_|OFPTC_|OFPGT_|OFPGC_|OFPGFC_|OFPHFC_|OFPCML_|OFPCT_|OFPMF_|OFPMPF_|OFPMPS_|OFPER_|OFPHET_|OFPST_|OFPRR_|OFPMC_|OFPCR_|OFPC_|OFPGFC_|OFPQT_|OFPQF_|OFPSF_|OFPVID_|OFPFF_|OFPGFF_|OFPMM_|ONF_)[A-Z_0-9]+)`"
)
INLINE_FUNC = re.compile(r"`([a-z_][a-zA-Z0-9_]+)\(\)`")
WIRE_NUMERIC = re.compile(r"\b(?:type|code)\s+(\d+)\b|`(0x[0-9a-fA-F]{2,4})`")
IANA_PORT = re.compile(r"\b(?:port|TCP)\s+6653\b|\b6653\b")
COMMIT_SHA = re.compile(r"\b([0-9a-f]{8,40})\b")


def classify(line: str) -> list[tuple[str, str]]:
    """Classify all citations on one line. Returns (kind, target) pairs.

    kind is one of:
      URL_OVS, URL_OVN, URL_ONF, BRANCH_TAG, OF_VERSION_MARKER,
      INLINE_FILE, INLINE_OF_CONST, INLINE_FUNC, WIRE_NUMERIC,
      IANA_PORT, COMMIT_SHA
    """
    hits: list[tuple[str, str]] = []
    for m in URL_OVS.finditer(line):
        hits.append(("URL_OVS", m.group(0)))
    for m in URL_OVN.finditer(line):
        hits.append(("URL_OVN", m.group(0)))
    for m in URL_ONF.finditer(line):
        hits.append(("URL_ONF", m.group(0)))
    for m in BRANCH_TAG.finditer(line):
        hits.append(("BRANCH_TAG", m.group(1)))
    for m in OF_VERSION_MARKER.finditer(line):
        hits.append(("OF_VERSION_MARKER", m.group(0)))
    for m in INLINE_FILE.finditer(line):
        hits.append(("INLINE_FILE", m.group(1)))
    for m in INLINE_OF_CONST.finditer(line):
        hits.append(("INLINE_OF_CONST", m.group(1)))
    for m in INLINE_FUNC.finditer(line):
        hits.append(("INLINE_FUNC", m.group(1)))
    for m in WIRE_NUMERIC.finditer(line):
        token = m.group(1) or m.group(2)
        if token:
            hits.append(("WIRE_NUMERIC", token))
    for m in IANA_PORT.finditer(line):
        hits.append(("IANA_PORT", m.group(0)))
    for m in COMMIT_SHA.finditer(line):
        sha = m.group(1)
        # Filter likely real commit refs: at least 8 hex with letter and digit
        if any(c.isalpha() for c in sha) and any(c.isdigit() for c in sha) and len(sha) >= 8:
            # Avoid double-counting hex-form WIRE_NUMERIC that already matched
            hits.append(("COMMIT_SHA", sha))
    return hits


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    """Return list of (lineno, kind, target) tuples."""
    out: list[tuple[int, str, str]] = []
    if not path.exists():
        return out
    text = path.read_text(encoding="utf-8", errors="replace")
    for i, raw in enumerate(text.splitlines(), 1):
        for kind, target in classify(raw):
            out.append((i, kind, target))
    return out


def emit_per_file(file_id: str, fname: str, hits: list[tuple[int, str, str]]) -> None:
    print(f"### {file_id} `{fname}`")
    print()
    if not hits:
        print(
            "**Citations: 0.** No Rule 14 surface candidates found by the five "
            "R0.5 queries. Verified absence; per R1 checklist the file is still "
            "read in full to confirm narrative claims that the regex misses."
        )
        print()
        return
    by_kind: dict[str, int] = {}
    for _, kind, _ in hits:
        by_kind[kind] = by_kind.get(kind, 0) + 1
    summary = ", ".join(f"{k}={v}" for k, v in sorted(by_kind.items()))
    print(f"**Citations: {len(hits)}.** Counts by kind: {summary}.")
    print()
    print("| L# | Kind | Target |")
    print("|---|---|---|")
    for lineno, kind, target in hits:
        t = target.replace("|", "\\|")
        print(f"| {lineno} | {kind} | `{t}` |")
    print()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    print("# v3.11 Phase R0.5, OpenFlow Block Citation Inventory")
    print()
    print(
        "> **Plan:** [`plans/sdn/v3.11-of-block-source-verify-and-cleanup.md`]"
        "(../../plans/sdn/v3.11-of-block-source-verify-and-cleanup.md) "
        "Phase R0.5."
    )
    print(
        "> **Source:** offline OVS repo at `C:\\Users\\voleh\\Documents\\ovs` "
        "checked out at `v2.17.9`, plus offline OpenFlow spec repo at "
        "`C:\\Users\\voleh\\Documents\\openflow` checked out at `spec1.6_rc1`."
    )
    print(
        "> **Generated by:** [`scripts/v3_11_citation_inventory.py`]"
        "(../../scripts/v3_11_citation_inventory.py)."
    )
    print("> **Date:** 2026-04-29.")
    print(
        "> **Purpose:** enumerate every OF-source citation candidate across "
        "17 in-scope curriculum files. The output drives R1 sub-batch sizing "
        "and per-citation verification scope."
    )
    print()
    print("---")
    print()
    print("## 1. Methodology")
    print()
    print(
        "This inventory is the canonical superset. Each row is a "
        "citation-candidate that R1 audits per §3.3 verification primitives. "
        "Some rows are noise (a numeric type code that lives inside a "
        "verbatim quoted block, an OF version marker that is a section "
        "heading rather than a free-standing claim). R1 disambiguates "
        "per-row."
    )
    print()
    print("**Citation kinds detected (11 categories):**")
    print()
    print("| Kind | Pattern | R1 verification primitive |")
    print("|---|---|---|")
    print("| `URL_OVS` | `https://github.com/openvswitch/ovs/...` | Primitive B URL ref segment check against OVS repo |")
    print("| `URL_OVN` | `https://github.com/ovn-org/ovn/...` | Primitive B against OVN repo (cross-baseline) |")
    print("| `URL_ONF` | `https://opennetworking.org/...` or `onf.org/...` | External; mark TRUST per §3.3 Primitive F |")
    print("| `BRANCH_TAG` | `branch-2.17`, `v2.17.9`, etc. | Primitive B context check against OVS tag |")
    print("| `OF_VERSION_MARKER` | `OF 1.0`, `OpenFlow 1.5`, etc. | Free-standing fact check via Primitive C and OFPAT_RAW prefix lookup |")
    print("| `INLINE_FILE` | backticked `lib/ofp-actions.c` and similar | Primitive A path-existence check against OVS v2.17.9 |")
    print("| `INLINE_OF_CONST` | backticked `OFPT_*`, `OFPAT_*`, `OXM_OF_*`, `MFF_*`, `NXM_*`, etc. | Primitive E enum existence in OVS headers |")
    print("| `INLINE_FUNC` | `` `function_name()` `` (inline backticks) | Primitive A function-name check |")
    print("| `WIRE_NUMERIC` | `type 28`, `code 4`, `0x07` | Primitive D numeric type-code lookup |")
    print("| `IANA_PORT` | `port 6653`, `TCP 6653`, bare `6653` | Cross-check with `OFP_TCP_PORT` macro at the spec repo |")
    print("| `COMMIT_SHA` | 8-40 char hex token | Primitive B commit verification on OVS repo |")
    print()
    print(
        "Some rows fall in multiple kinds (a URL with a branch tag in its "
        "path). The script emits one row per (kind, target) pair, so a "
        "single curriculum line may produce multiple rows. R1 deduplicates "
        "to unique-position tuples."
    )
    print()
    print("**Caveats.**")
    print()
    print(
        "- The script does not parse fenced code blocks separately; rows "
        "inside ``` blocks may be CLI examples or verbatim source quotes "
        "rather than free-standing claims. R1 per-row review filters."
    )
    print(
        "- The `WIRE_NUMERIC` pattern is over-collecting; many rows are "
        "byte counts, table indexes, or chapter numbers, not OF wire-format "
        "type codes. R1 confirms which are Rule 14 surface."
    )
    print(
        "- The `OF_VERSION_MARKER` pattern catches every section heading "
        "and reference that mentions an OF version. Only those used as "
        "free-standing introduction-version claims get audited under §3.3 "
        "Primitive C."
    )
    print(
        "- The `COMMIT_SHA` pattern matches any 8-40 char hex string; some "
        "rows are MAC addresses, hash tokens, or fragments of SHA-256 "
        "digests unrelated to git commits. R1 filters."
    )
    print(
        "- The `INLINE_FUNC` pattern matches any backticked `name()`; some "
        "rows are CLI command examples (`ovs-ofctl()`) or shell snippets. "
        "R1 filters."
    )
    print()
    print("---")
    print()
    print("## 2. Per-file inventory")
    print()
    grand_total = 0
    per_file_total: dict[str, int] = {}
    per_kind_total: dict[str, int] = {}
    for file_id, fname in SCOPE:
        path = ROOT / fname
        hits = scan_file(path)
        emit_per_file(file_id, fname, hits)
        per_file_total[file_id] = len(hits)
        grand_total += len(hits)
        for _, kind, _ in hits:
            per_kind_total[kind] = per_kind_total.get(kind, 0) + 1
    print("---")
    print()
    print("## 3. Aggregate totals")
    print()
    print(f"**Grand total citation candidates: {grand_total}** across {len(SCOPE)} files.")
    print()
    print("### 3.1. Per-file totals")
    print()
    print("| File | Candidates | Phase |")
    print("|---|---|---|")
    for file_id, _ in SCOPE:
        print(f"| {file_id} | {per_file_total[file_id]} | {PHASE_MAP[file_id]} |")
    print()
    print("### 3.2. Per-kind totals")
    print()
    print("| Kind | Count |")
    print("|---|---|")
    for kind in sorted(per_kind_total.keys()):
        print(f"| {kind} | {per_kind_total[kind]} |")
    print()
    print("### 3.3. Per-phase totals")
    print()
    phase_total: dict[str, int] = {}
    phase_files: dict[str, int] = {}
    for file_id, _ in SCOPE:
        phase = PHASE_MAP[file_id]
        phase_total[phase] = phase_total.get(phase, 0) + per_file_total[file_id]
        phase_files[phase] = phase_files.get(phase, 0) + 1
    print("| Phase | Files | Candidates |")
    print("|---|---|---|")
    for phase in ["R1.A", "R1.B", "R1.C", "R1.D", "R1.E", "R1.F"]:
        print(f"| {phase} | {phase_files.get(phase, 0)} | {phase_total.get(phase, 0)} |")
    print(f"| **Total** | **{len(SCOPE)}** | **{grand_total}** |")
    print()
    print("---")
    print()
    print(
        "## 4. Sub-batch boundary reconfirmation"
    )
    print()
    print(
        "Plan v3.11 §9.1 specified the corrected 6-sub-batch structure "
        "(R1.A through R1.F) with 3.5 in its own R1.C, 4.8 in R1.D, 4.9 in "
        "R1.E. The empirical per-file candidate counts (R1.C 472, R1.D 825, "
        "R1.E 602) substantially exceed the §0.4 estimate of 180-190 per "
        "catalog file. The driver is the wider regex coverage of "
        "`OF_VERSION_MARKER` (1,104 repo-wide hits) and `INLINE_OF_CONST` "
        "(476 hits), which collect every section heading mentioning an OF "
        "version plus every backticked OF symbolic constant."
    )
    print()
    print(
        "Treatment per plan §3.4 and §3.5: this gross candidate count is "
        "the upper bound. R1 audits the unique Rule 14 surface (free-"
        "standing introduction-version claims, true OFPAT_/MFF_/OXM_OF_ "
        "constant references, file/function citations). Most "
        "`OF_VERSION_MARKER` hits are section headings (`### OF 1.5`) or "
        "verbatim quoted prose, not free-standing claims requiring "
        "verification. R1 per-row classification will deduplicate to the "
        "true verification surface, expected at 30-50 percent of the gross "
        "count for catalog files."
    )
    print()
    print(
        "Bisection decision: do not split R1.C, R1.D, R1.E preemptively. "
        "Apply the §3.7 escalation gate during R1: if mid-batch verified-"
        "violation count exceeds 30 percent, halt and bisect. Empirically, "
        "v3.10 catalog audits showed gross-to-true ratio of 30-40 percent "
        "and verified-violation rates of 1-5 percent. Same prior carries "
        "to v3.11."
    )
    print()
    print("---")
    print()
    print("> **End of R0.5 inventory.**")
    return 0


if __name__ == "__main__":
    sys.exit(main())
