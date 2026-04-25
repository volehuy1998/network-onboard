#!/usr/bin/env python3
"""v3.6 Phase 1: Refine coverage matrix v2 (enhanced alias rules).

Builds on refine_coverage_matrix.py with 5 additional alias rules to
reduce false-positive MISSING in Tier A:

1. Strip ``Action: `` prefix from "Action: copy_field (OpenFlow 1.5+)".
2. Strip trailing parenthetical version notes ``(OpenFlow 1.5+)``,
   ``(Nicira extension, OVS 2.4+)``, ``(Type 19, OpenFlow 1.3+)``,
   ``(64 bits each, OF 1.3+ / OVS 2.4+)``.
3. Slash-split compound names like
   ``OFPT_ROLE_REQUEST / OFPT_ROLE_REPLY`` and
   ``OFPT_BUNDLE_OPEN / OFPT_BUNDLE_COMMIT / OFPT_BUNDLE_ADD_MESSAGE``
   into individual identifiers.
4. Range expand ``xreg0-xreg7`` to ``xreg0..xreg7``.
5. Vietnamese-aware match: curriculum prose may use translated form for
   conceptual entries like ``Pipeline Architecture``. Add a small
   bilingual dictionary so concept matches when prose uses Vietnamese.

Output: ``memory/sdn/keyword-coverage-matrix-v2.md``.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

REPO = Path(r"C:\Users\voleh\Documents\network-onboard")
REF = REPO / "sdn-onboard" / "doc" / "ovs-openflow-ovn-keyword-reference.md"
CURRICULUM_DIR = REPO / "sdn-onboard"
OUT = REPO / "memory" / "sdn" / "keyword-coverage-matrix-v2.md"


BANNED_REGEXES = [
    r"\bdpdk\b", r"\bpmd\b", r"\bemc\b", r"\bsmc\b",
    r"\bmempool\b", r"netdev-dpdk", r"dpif-netdev/pmd",
    r"\bhugepage\b",
]


def is_banned(name: str, context: str) -> bool:
    text = (name + " " + context).lower()
    return any(re.search(pat, text, re.IGNORECASE) for pat in BANNED_REGEXES)


SKIP_BOLD_LABELS = {
    "Problem.", "Layered checklist.", "Likely root-cause categories.",
    "Note.", "Warning.", "Source:", "Example:", "Synopsis:",
}


def detect_section(line: str, current: dict) -> dict:
    m = re.match(r"^## (\d)\. (.+)$", line)
    if m:
        current["section"] = m.group(1)
        current["section_name"] = m.group(2).strip()
        current["subsection"] = ""
        current["subsection_name"] = ""
        return current
    m = re.match(r"^### (\d)\.(\d) (.+)$", line)
    if m:
        current["subsection"] = f"{m.group(1)}.{m.group(2)}"
        current["subsection_name"] = m.group(3).strip()
    return current


def detect_entry(line: str, next_line: str = "") -> tuple[str, str] | None:
    m = re.match(r"^- \*\*([^*]+)\*\*\s*[—\-–|]?\s*(.*)$", line)
    if m:
        name = m.group(1).strip()
        if name and not re.match(r"^[\s\W]*$", name):
            return (name, m.group(2).strip())
    m = re.match(r"^\*\*([^*]+)\*\*$", line)
    if m:
        name = m.group(1).strip()
        if name in SKIP_BOLD_LABELS:
            return None
        if name and not re.match(r"^[\s\W]*$", name):
            return (name, next_line.strip())
    return None


def detect_subsection_heading(line: str) -> tuple[str, str] | None:
    m = re.match(r"^#### `?([^`]+)`?$", line)
    if m:
        return (m.group(1).strip().rstrip("`"), "CLI tool")
    return None


def detect_scenario(line: str) -> tuple[str, str] | None:
    m = re.match(r"^### (\d+)\. (.+)$", line)
    if m:
        return (f"Scenario {m.group(1)}: {m.group(2).strip()}", "production troubleshoot")
    return None


def parse_ref() -> list[dict]:
    lines = REF.read_text(encoding="utf-8").splitlines()
    entries: list[dict] = []
    state = {"section": "", "section_name": "", "subsection": "", "subsection_name": ""}
    for i, line in enumerate(lines):
        state = detect_section(line, state)
        next_line = lines[i + 1] if i + 1 < len(lines) else ""
        entry = (
            detect_entry(line, next_line)
            or detect_subsection_heading(line)
            or detect_scenario(line)
        )
        if not entry:
            continue
        name, context = entry
        bucket_match = re.search(r"Bucket[:\s|]+(\w+)", context)
        bucket = bucket_match.group(1) if bucket_match else state.get("section_name", "")
        entries.append({
            "name": name,
            "section": state.get("section", ""),
            "subsection": state.get("subsection", ""),
            "subsection_name": state.get("subsection_name", ""),
            "bucket": bucket,
            "banned": is_banned(name, context),
            "ref_line": i + 1,
        })
    seen = set()
    unique: list[dict] = []
    for e in entries:
        key = (e["name"], e["section"])
        if key not in seen:
            seen.add(key)
            unique.append(e)
    return unique


# Bilingual concept dictionary for high-level conceptual entries.
# When the REF entry is a topic header (not a specific identifier), the
# curriculum prose likely uses the Vietnamese form. The script tries each
# Vietnamese alias and reports the best match.
BILINGUAL_DICT: dict[str, list[str]] = {
    "Pipeline Architecture": ["multi-table pipeline", "kiến trúc pipeline"],
    "Table Chaining via goto_table": ["goto_table"],
    "Packet Metadata Fields": ["metadata"],
    "Action Set vs Action List": ["action set", "action list"],
    "Instructions vs Actions Distinction": ["instruction", "Apply-Actions", "Write-Actions"],
    "OpenFlow Reserved Port Numbers": ["OFPP_", "reserved port"],
    "Table 0 Ingress Pipeline": ["Table 0", "table=0"],
    "Single-Table vs Multi-Table Pipeline": ["multi-table", "single-table"],
    "Group Tables": ["group_id", "OFPGT_", "group table"],
    "Egress Tables": ["egress table", "OF 1.5"],
    "Packet Type Aware Pipeline": ["packet_type"],
    "Version Support Summary": ["OF 1.0", "OF 1.3", "OF 1.5"],
    "Northbound DB Management": ["NBDB", "Northbound DB"],
    "Southbound DB Management": ["SBDB", "Southbound DB"],
    "Chassis Configuration": ["external_ids:system-id", "ovn-encap-type"],
    "Integration Bridge": ["br-int"],
    "OVSDB Server Roles": ["active/backup", "Raft cluster role"],
    "RAFT Clustering": ["Raft", "raft"],
    "Inactivity Probes": ["inactivity_probe", "probe-interval"],
    "Northd Probe Interval": ["northd-probe-interval", "probe_interval"],
    "Leader Election": ["leader election", "raft_become_leader"],
    "Daemon Threading": ["set-n-threads", "n_threads"],
    "NB_Global Table": ["NB_Global", "nb_cfg"],
    "SB_Global Table": ["SB_Global"],
    "Ingress vs Egress Pipeline": ["LS_IN", "LS_OUT", "LR_IN", "LR_OUT"],
    "Logical Datapath Binding": ["Datapath_Binding"],
    "Tunnel Key Allocation": ["tunnel_key", "Geneve VNI"],
    "Logical Port Tunnel Key": ["tunnel_key", "Port_Binding tunnel"],
    "Standard Switch Table Sequence": ["LS_IN_PORT_SEC_L2", "LS_IN_ACL"],
    "Standard Router Table Sequence": ["LR_IN_ADMISSION", "LR_IN_IP_INPUT"],
    "VTEP Gateway Integration": ["vtep-ctl", "VTEP schema"],
    "Geneve TLV Encapsulation": ["Geneve TLV", "0x0102"],
    "Encapsulation Precedence": ["ovn-encap-type", "encap precedence"],
    "Distributed Gateway Routing": ["distributed gateway", "redirect-chassis"],
    "Distributed NAT": ["distributed NAT", "dnat_and_snat"],
    "DVR-style Logical Patches": ["patch port", "ovn-chassis-mac-mappings"],
    "MLF Local-Only Flag": ["MLF_LOCAL_ONLY"],
    "MLF Tunnel Metadata Encoding": ["MLF_", "tunnel metadata"],
    "OVN internal OVS register conventions": ["REGBIT_", "MFF_LOG_"],
    "OVN logical port pipeline table IDs": ["OFTABLE_LOG_INGRESS", "OFTABLE_"],
    "OVN logical port pipeline table IDs — LS_OUT stages": ["LS_OUT"],
    "OVN logical port pipeline table IDs — LR ingress stages": ["LR_IN"],
    "OVN logical port pipeline table IDs — LR egress stages": ["LR_OUT"],
    "Bridge subcommands": ["add-br", "del-br"],
    "Port subcommands": ["add-port", "del-port"],
    "Interface subcommands": ["set Interface", "list Interface"],
    "Controller subcommands": ["set-controller", "del-controller"],
    "Manager subcommands": ["set-manager", "del-manager"],
    "SSL subcommands": ["set-ssl", "del-ssl"],
    "Generic database subcommands": ["wait-until", "list "],
    "Other utilities": ["ovs-pcap", "ovs-tcpundump"],
    "ovs-appctl dpif/dump-flows BR": ["dpif/dump-flows"],
    "ovn-nbctl: Northbound DB CLI": ["ovn-nbctl"],
    "ovn-sbctl: Southbound DB CLI": ["ovn-sbctl"],
    "ovn-trace: Packet Tracing Tool": ["ovn-trace"],
    "ovn-detrace: OpenFlow-to-OVN Translation": ["ovn-detrace"],
    "ovn-appctl: Runtime Control": ["ovn-appctl"],
    "ovn-nbctl logical switch subcommands": ["ls-add", "ls-list"],
    "ovn-nbctl logical switch port subcommands": ["lsp-add", "lsp-set"],
    "ovn-nbctl logical router subcommands": ["lr-add", "lr-list"],
    "ovn-nbctl ACL subcommands": ["acl-add", "acl-list"],
    "ovn-nbctl load balancer subcommands": ["lb-add", "lb-list"],
    "ovn-nbctl static route subcommands": ["lr-route-add", "lr-route-list"],
    "ovn-nbctl NAT subcommands": ["lr-nat-add", "lr-nat-list"],
    "ovn-nbctl address set / port group subcommands": ["address_set", "port_group"],
    "ovn-nbctl DHCP options subcommands": ["dhcp-options-create", "dhcp_options"],
    "ovn-nbctl DNS subcommands": ["dns-add", "DNS table"],
    "ovn-nbctl BFD subcommands": ["bfd-add", "BFD"],
    "ovn-nbctl load-balancer health-check subcommands": ["lb-health-check", "Load_Balancer_Health_Check"],
    "ovn-nbctl generic DB subcommands": ["wait-until", "ovn-nbctl --wait"],
    "ovn-sbctl --leader-only": ["--leader-only"],
    "ovn-sbctl lflow-list --uuid": ["lflow-list", "--uuid"],
    "ovn-sbctl lflow-list --ovs": ["lflow-list", "--ovs"],
    "ovn-sbctl lflow-list --vflows": ["lflow-list", "--vflows"],
    "ovn-sbctl lsp-unbind": ["lsp-unbind"],
    "ovn-trace Simulation": ["ovn-trace", "microflow"],
    "ovn-trace Output Format": ["ovn-trace --detailed", "Logical_Flow"],
    "ovn-detrace Reverse Lookup": ["ovn-detrace"],
    "ovn-controller Flow Installation Tracing": ["ofctrl_seqno", "ovn-controller flow"],
    "Connection Tracking Zone Limits": ["ct_zone", "zone limit"],
    "SB Cluster State Monitoring": ["cluster/status", "sb-cluster"],
    "OVN Bug Tools": ["recompute", "inject-pkt"],
    "ovn-controller Flow Installation Metrics": ["ofctrl/", "engine/"],
    "OVN Logical Flow Cache": ["lflow-cache"],
    "Lflow Cache Size Limits": ["lflow-cache/show-stats", "limit-lflow-cache"],
    "OVN Database Monitoring": ["nbdb-monitor", "monitor_cond"],
    "Southbound Connection State": ["SB DB connection", "sb_pb"],
    "Datapath Binding Verification": ["Datapath_Binding", "tunnel_key"],
    "Port Binding Status Inspection": ["Port_Binding", "binding/show"],
    "Logical Flow Debugging": ["Logical_Flow", "lflow-list"],
    "OpenFlow Flow Correlation": ["cookie", "ovn-detrace"],
    "Multicast Group Debugging": ["IGMP_Group", "Multicast_Group"],
    "MAC Binding Inspection": ["MAC_Binding"],
    "DNS Resolution Debugging": ["DNS table", "ovn-controller dns"],
    "Meter and Rate Limiting": ["Meter", "meter-list"],
    "ACL Logging": ["acl-log", "acl_log"],
    "Load Balancer Health Monitoring": ["Service_Monitor", "Load_Balancer_Health_Check"],
    "BFD Health Detection": ["BFD", "bfd/show"],
    "HA Chassis Failover Verification": ["HA_Chassis_Group", "ha-chassis"],
    "Connector Inspection": ["ovs-vsctl get Open_vSwitch", "Connection table"],
    "write_metadata Instruction": ["write_metadata"],
    "Meter Table": ["meter-mod", "OFPMT_"],
    "Auxiliary Connections": ["auxiliary connection", "OFPT_HELLO aux"],
    "Connection State Machine: Steady State (ECHO keep-alive)": ["OFPT_ECHO", "echo_request"],
}


def expand_range(s: str) -> list[str]:
    """Expand ``xreg0-xreg7`` style ranges to a list of identifiers."""
    m = re.match(r"^([A-Za-z_]+)(\d+)-\1(\d+)$", s)
    if m:
        prefix, lo, hi = m.group(1), int(m.group(2)), int(m.group(3))
        if hi - lo <= 32:
            return [f"{prefix}{i}" for i in range(lo, hi + 1)]
    m = re.match(r"^([A-Za-z_]+)(\d+)-(\d+)$", s)
    if m and not re.match(r"^[A-Za-z_]+\d+-[A-Za-z_]", s):
        prefix, lo, hi = m.group(1), int(m.group(2)), int(m.group(3))
        if hi - lo <= 32:
            return [f"{prefix}{i}" for i in range(lo, hi + 1)]
    return []


def extract_short_names(name: str) -> list[str]:
    """Extract candidate short names with v2 enhancements."""
    candidates: list[str] = [name]

    stripped = re.sub(r"^(Action|Instruction|Match field|Field):\s+", "", name)
    if stripped != name:
        candidates.append(stripped)

    no_paren = re.sub(r"\s*\([^)]*\)\s*$", "", stripped).strip()
    if no_paren and no_paren not in candidates:
        candidates.append(no_paren)

    no_tool = re.sub(
        r"^(ovn-nbctl|ovn-sbctl|ovn-appctl|ovn-ic-nbctl|ovn-ic-sbctl|"
        r"ovs-vsctl|ovs-ofctl|ovs-appctl|ovs-dpctl|ovsdb-tool|ovsdb-client)\s+",
        "", no_paren,
    )
    if no_tool != no_paren and no_tool not in candidates:
        candidates.append(no_tool)
        if "/" in no_tool and "(" not in no_tool:
            for part in no_tool.split("/"):
                p = part.strip()
                if p and p not in candidates and len(p) >= 3:
                    candidates.append(p)

    no_table_suffix = re.sub(r"\s+table$", "", no_paren, flags=re.IGNORECASE).strip()
    if no_table_suffix != no_paren and no_table_suffix and no_table_suffix not in candidates:
        candidates.append(no_table_suffix)

    upper_to_proper = {
        "RAFT": "Raft",
        "OVN": "OVN",
        "OVS": "OVS",
        "JSON-RPC": "JSON-RPC",
    }
    for token, proper in upper_to_proper.items():
        if token in name and proper not in candidates and proper != token:
            for cand in list(candidates):
                replaced = cand.replace(token, proper)
                if replaced != cand and replaced not in candidates:
                    candidates.append(replaced)

    for src in (name, stripped, no_paren):
        if "/" in src and "(" not in src:
            for part in src.split("/"):
                p = part.strip()
                if p and p not in candidates and len(p) >= 3:
                    candidates.append(p)

    for src in list(candidates):
        expanded = expand_range(src)
        for e in expanded:
            if e not in candidates:
                candidates.append(e)

    m = re.match(r"^(.+?)\s*\(([^)]+)\)\s*$", name)
    if m:
        main = m.group(1).strip().rstrip("`").lstrip("`")
        paren = m.group(2).strip().strip("`")
        if main and main not in candidates:
            candidates.append(main)
        if paren:
            paren_clean = paren.replace("`", "").strip()
            if re.match(r"^[\w./_-]+$", paren_clean) and len(paren_clean) <= 40:
                candidates.append(paren_clean)
                if "." in paren_clean:
                    candidates.append(paren_clean.rsplit(".", 1)[1])
                if "/" in paren_clean:
                    for part in paren_clean.split("/"):
                        if part.strip():
                            candidates.append(part.strip())

    m = re.match(r"^(.+?):\s*(.+)$", name)
    if m:
        right = m.group(2).strip()
        if right and len(right) <= 30 and right not in candidates:
            candidates.append(right)

    m = re.match(r"^([\w._-]+(?:\s*/\s*[\w._-]+)*)\s+\(\d+\s*bits", name)
    if m:
        core = m.group(1).strip()
        if core and core not in candidates:
            candidates.append(core)
        if core and "/" in core:
            for part in core.split("/"):
                if part.strip() and part.strip() not in candidates:
                    candidates.append(part.strip())

    m = re.match(r"^`([^`]+)`$", name)
    if m:
        bt = m.group(1).strip()
        if bt not in candidates:
            candidates.append(bt)

    bilingual_key = name
    if name in BILINGUAL_DICT:
        for alt in BILINGUAL_DICT[name]:
            if alt not in candidates:
                candidates.append(alt)
    else:
        no_paren_key = re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()
        if no_paren_key in BILINGUAL_DICT:
            for alt in BILINGUAL_DICT[no_paren_key]:
                if alt not in candidates:
                    candidates.append(alt)
        no_action_key = re.sub(r"^Action:\s+", "", no_paren_key).strip()
        if no_action_key != no_paren_key and no_action_key in BILINGUAL_DICT:
            for alt in BILINGUAL_DICT[no_action_key]:
                if alt not in candidates:
                    candidates.append(alt)

    GENERIC_BLACKLIST = {
        "of", "it", "is", "as", "at", "to", "in", "on", "or", "no",
        "ct",
    }
    filtered: list[str] = []
    for c in candidates:
        cs = c.strip()
        if not cs:
            continue
        if cs.lower() in GENERIC_BLACKLIST:
            continue
        if len(cs) < 3:
            if not any(ch.isupper() or ch.isdigit() for ch in cs):
                continue
        filtered.append(cs)
    return filtered if filtered else [name]


LOOKUP_SPINE_FILES = {"0.3 - master-keyword-index.md"}


def grep_keyword(keyword: str, files: list[Path]) -> tuple[int, list[str]]:
    matched: list[str] = []
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if keyword in content:
                matched.append(f.name)
        except Exception:
            continue
    return len(matched), matched


def substantive_count(matched: list[str]) -> int:
    """Count matched files excluding lookup spine (0.3 master index)."""
    return sum(1 for m in matched if m not in LOOKUP_SPINE_FILES)


def grep_keyword_with_alternatives(
    name: str, files: list[Path]
) -> tuple[int, list[str], str, list[tuple[str, int]]]:
    candidates = extract_short_names(name)
    best_count = 0
    best_files: list[str] = []
    best_alias = candidates[0] if candidates else name
    trace: list[tuple[str, int]] = []
    for cand in candidates:
        count, files_matched = grep_keyword(cand, files)
        trace.append((cand, count))
        if count > best_count:
            best_count = count
            best_files = files_matched
            best_alias = cand
    return best_count, best_files, best_alias, trace


def classify_depth(file_count: int) -> str:
    if file_count == 0:
        return "MISSING"
    if file_count <= 2:
        return "SHALLOW"
    if file_count <= 9:
        return "BREADTH"
    return "WIDE"


def classify_tier(entry: dict, depth: str) -> str:
    if entry["banned"]:
        return "D"
    return {"MISSING": "A", "SHALLOW": "B", "BREADTH": "C-OK", "WIDE": "C-DEEP"}[depth]


def main() -> None:
    print("Parsing REF...")
    entries = parse_ref()
    print(f"  Total: {len(entries)}, In-scope: {sum(1 for e in entries if not e['banned'])}")

    print("Grepping curriculum (v2 enhanced aliases)...")
    files = sorted(CURRICULUM_DIR.glob("*.md"))
    print(f"  Curriculum file count: {len(files)}")

    matrix: list[dict] = []
    for i, e in enumerate(entries):
        count, matched, alias, trace = grep_keyword_with_alternatives(e["name"], files)
        sub_count = substantive_count(matched)
        depth = classify_depth(count)
        sub_depth = classify_depth(sub_count)
        tier = classify_tier(e, depth)
        sub_tier = classify_tier(e, sub_depth)
        matrix.append({
            **e,
            "file_count": count,
            "sub_count": sub_count,
            "files": matched,
            "depth": depth,
            "sub_depth": sub_depth,
            "tier": tier,
            "sub_tier": sub_tier,
            "matched_via": alias,
            "trace": trace,
        })
        if (i + 1) % 50 == 0:
            print(f"  Processed {i + 1}/{len(entries)}")

    stats: dict[str, int] = defaultdict(int)
    sub_stats_g: dict[str, int] = defaultdict(int)
    for m in matrix:
        stats[m["tier"]] += 1
        sub_stats_g[m["sub_tier"]] += 1
    print(f"  Tier A (MISSING in-scope): {stats['A']} | substantive: {sub_stats_g['A']}")
    print(f"  Tier B (SHALLOW in-scope): {stats['B']} | substantive: {sub_stats_g['B']}")
    print(f"  Tier C-OK (BREADTH 3-9 files): {stats['C-OK']} | substantive: {sub_stats_g['C-OK']}")
    print(f"  Tier C-DEEP (WIDE 10+ files): {stats['C-DEEP']} | substantive: {sub_stats_g['C-DEEP']}")
    print(f"  Tier D (BANNED): {stats['D']}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    out: list[str] = []
    out.append("# Keyword Coverage Matrix v2 (v3.6 Phase 1 output)")
    out.append("")
    out.append(f"> **Source:** parsed from `sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md`")
    out.append(f"> **Curriculum scope:** `sdn-onboard/*.md` (top-level only, {len(files)} files)")
    out.append(f"> **Generated by:** scripts/refine_coverage_matrix_v2.py")
    out.append("")
    out.append("## Refinement note v2")
    out.append("")
    out.append("Builds on v1 with 5 additional alias rules:")
    out.append("")
    out.append("1. Strip `Action: ` / `Instruction: ` / `Match field: ` prefix.")
    out.append("2. Strip trailing parenthetical version notes `(OpenFlow 1.5+)`, `(Nicira extension, OVS 2.4+)`.")
    out.append("3. Slash-split compound names like `OFPT_ROLE_REQUEST / OFPT_ROLE_REPLY`.")
    out.append("4. Range expand `xreg0-xreg7` to `xreg0..xreg7`.")
    out.append("5. Bilingual concept dictionary: high-level topic headers (e.g., `Pipeline Architecture`) try Vietnamese / specific identifier aliases.")
    out.append("")
    out.append("## Summary")
    out.append("")
    out.append("| Tier | Count | % | Action |")
    out.append("|------|-------|---|--------|")
    total_inscope = sum(1 for m in matrix if not m["banned"])
    for t, _label in [
        ("A", "MISSING in-scope"), ("B", "SHALLOW in-scope"),
        ("C-OK", "BREADTH"), ("C-DEEP", "WIDE"), ("D", "BANNED"),
    ]:
        c = stats[t]
        if t == "D":
            pct = f"{c * 100 / len(matrix):.1f}%"
        else:
            pct = f"{c * 100 / total_inscope:.1f}%" if total_inscope else "N/A"
        action_text = {
            "A": "TRUE gap candidate, manual classify",
            "B": "Upgrade to 5-axis if topic relevant",
            "C-OK": "Verify 5-axis exists; add if missing",
            "C-DEEP": "Spot-check coverage",
            "D": "Skip (PERMANENT BAN)",
        }[t]
        out.append(f"| {t} | {c} | {pct} | {action_text} |")
    out.append("")
    out.append(f"**Total in-scope:** {total_inscope}")
    out.append(f"**Build/upgrade work (Tier A + B):** {stats['A'] + stats['B']} keyword")
    out.append("")
    out.append("---")
    out.append("")

    grouped: dict[str, list[dict]] = defaultdict(list)
    for m in matrix:
        key = f"{m['section']}.{m['subsection']}" if m['subsection'] else m['section']
        grouped[key].append(m)

    for sec_key in sorted(grouped.keys()):
        sec_entries = grouped[sec_key]
        if not sec_entries:
            continue
        first = sec_entries[0]
        title = f"REF Section {sec_key}"
        if first.get("subsection_name"):
            title += f" — {first['subsection_name']}"
        out.append(f"## {title} ({len(sec_entries)} entries)")
        out.append("")
        sub_stats: dict[str, int] = defaultdict(int)
        for e in sec_entries:
            sub_stats[e["tier"]] += 1
        out.append(
            f"_Tier breakdown: A={sub_stats['A']}, B={sub_stats['B']}, "
            f"C-OK={sub_stats['C-OK']}, C-DEEP={sub_stats['C-DEEP']}, D={sub_stats['D']}_"
        )
        out.append("")
        out.append("| Keyword | Files | Sub | Depth | SubDepth | Tier | SubTier | Matched via | First 3 files |")
        out.append("|---------|-------|-----|-------|----------|------|---------|-------------|---------------|")
        for e in sec_entries:
            name_safe = e["name"].replace("|", "\\|").replace("`", "")
            via_safe = e["matched_via"].replace("|", "\\|").replace("`", "")
            files_brief = ", ".join(e["files"][:3])
            if len(e["files"]) > 3:
                files_brief += f", ... (+{len(e['files']) - 3})"
            via_show = via_safe if via_safe != name_safe else "(direct)"
            out.append(
                f"| `{name_safe}` | {e['file_count']} | {e['sub_count']} | {e['depth']} | {e['sub_depth']} | {e['tier']} | {e['sub_tier']} | {via_show} | {files_brief} |"
            )
        out.append("")

    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
