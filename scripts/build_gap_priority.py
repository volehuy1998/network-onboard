#!/usr/bin/env python3
"""J.1 Step 3: Build gap priority file.

For each Tier A (MISSING) + Tier B (SHALLOW) keyword, suggest:
  - target_file: which curriculum file should host the 5-axis treatment
  - priority_level: CRITICAL / HIGH / MEDIUM / LOW
  - phase: J.3 / J.4 / J.5 / J.6 (per plan)

Output: memory/keyword-gap-priority.md
"""

from __future__ import annotations
import re
import subprocess
from pathlib import Path
from collections import defaultdict

REPO = Path(r"C:\Users\voleh\Documents\network-onboard")
REF = REPO / "sdn-onboard" / "doc" / "ovs-openflow-ovn-keyword-reference.md"
CURRICULUM_DIR = REPO / "sdn-onboard"
OUT = REPO / "memory" / "keyword-gap-priority.md"


# Reuse parser
def is_banned(name, context):
    text = (name + " " + context).lower()
    return any(re.search(pat, text, re.IGNORECASE) for pat in [
        r"\bdpdk\b", r"\bpmd\b", r"\bemc\b", r"\bsmc\b",
        r"\bmempool\b", r"netdev-dpdk", r"dpif-netdev/pmd", r"\bhugepage\b",
    ])


def detect_section(line, current):
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


def detect_entry(line, next_line=""):
    m = re.match(r"^- \*\*([^*]+)\*\*\s*[—\-–|]?\s*(.*)$", line)
    if m:
        name = m.group(1).strip()
        if name and not re.match(r"^[\s\W]*$", name):
            return (name, m.group(2).strip())
    m = re.match(r"^\*\*([^*]+)\*\*$", line)
    if m:
        name = m.group(1).strip()
        if name in ("Problem.", "Layered checklist.", "Likely root-cause categories.",
                    "Note.", "Warning.", "Source:", "Example:", "Synopsis:"):
            return None
        if name and not re.match(r"^[\s\W]*$", name):
            return (name, next_line.strip())
    return None


def detect_subsection_heading(line):
    m = re.match(r"^#### `?([^`]+)`?$", line)
    if m:
        return (m.group(1).strip().rstrip("`"), "CLI tool")
    return None


def detect_scenario(line):
    m = re.match(r"^### (\d+)\. (.+)$", line)
    if m:
        return (f"Scenario {m.group(1)}: {m.group(2).strip()}", "production troubleshoot")
    return None


def parse_ref():
    lines = REF.read_text(encoding="utf-8").splitlines()
    entries = []
    state = {"section": "", "section_name": "", "subsection": "", "subsection_name": ""}
    for i, line in enumerate(lines):
        state = detect_section(line, state)
        next_line = lines[i+1] if i+1 < len(lines) else ""
        entry = detect_entry(line, next_line) or detect_subsection_heading(line) or detect_scenario(line)
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
    unique = []
    for e in entries:
        key = (e["name"], e["section"])
        if key not in seen:
            seen.add(key)
            unique.append(e)
    return unique


def extract_short_names(name):
    candidates = [name]
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
    GENERIC_BLACKLIST = {"of", "it", "is", "as", "at", "to", "in", "on", "or", "no", "ct"}
    filtered = []
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


def grep_keyword(keyword, files):
    matched = []
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if keyword in content:
                matched.append(f.name)
        except Exception:
            continue
    return len(matched), matched


def grep_with_alternatives(name, files):
    candidates = extract_short_names(name)
    best_count = 0
    best_files = []
    best_alias = candidates[0] if candidates else name
    for cand in candidates:
        count, fm = grep_keyword(cand, files)
        if count > best_count:
            best_count = count
            best_files = fm
            best_alias = cand
    return best_count, best_files, best_alias


def classify_depth(file_count):
    if file_count == 0:
        return "MISSING"
    if file_count <= 2:
        return "SHALLOW"
    if file_count <= 9:
        return "BREADTH"
    return "WIDE"


def classify_tier(entry, depth):
    if entry["banned"]:
        return "D"
    return {"MISSING": "A", "SHALLOW": "B", "BREADTH": "C-OK", "WIDE": "C-DEEP"}[depth]


# Mapping REF section → suggested target curriculum file/Block per plan v3.5
def suggest_target(entry, matched_files):
    """Suggest target curriculum file based on REF subsection + existing matches."""
    sec = entry.get("subsection", "")
    name = entry["name"].lower()

    # Section 4 scenarios → distributed per plan Section 7
    if entry["section"] == "4":
        scenario_map = {
            "scenario 1": "20.2 - ovn-troubleshooting-deep-dive.md",
            "scenario 2": "20.2 - ovn-troubleshooting-deep-dive.md",
            "scenario 3": "13.9 - ovn-load-balancer-virtual-services.md",
            "scenario 4": "20.0 - ovs-ovn-systematic-debugging.md",
            "scenario 5": "10.1 - ovsdb-raft-clustering.md",
            "scenario 6": "11.0 - vxlan-geneve-stt.md",
            "scenario 7": "9.24 - ovs-conntrack-stateful-firewall.md",
            "scenario 8": "9.26 - ovs-revalidator-storm-forensic.md",
            "scenario 9": "4.3 - openflow-1.4-bundles-eviction.md",
            "scenario 10": "13.11 - ovn-gateway-router-distributed.md",
            "scenario 11": "20.5 - ovn-forensic-case-studies.md",
            "scenario 12": "13.0 - ovn-announcement-2015-rationale.md",
            "scenario 13": "13.10 - ovn-dhcp-dns-native.md",
            "scenario 14": "11.1 - overlay-mtu-pmtud-offload.md",
        }
        for key, target in scenario_map.items():
            if key in name:
                return target
        return "Block XX (unspecified)"

    # OVS section 1.x
    if entry["section"] == "1":
        if "1.1" in sec:  # daemons
            return "9.0 / 9.1 (OVS daemons) - existing or new"
        if "1.2" in sec:  # datapath
            if "ct" in name or "conntrack" in name or "alg" in name:
                return "9.24 - ovs-conntrack-stateful-firewall.md"
            if "kernel" in name or "datapath" in name:
                return "9.2 - ovs-kernel-datapath-megaflow.md"
            if "megaflow" in name or "microflow" in name or "ufid" in name:
                return "9.7 / 9.2 (megaflow + datapath)"
            if "recirc" in name:
                return "9.2 / 9.25"
            if "vlan" in name:
                return "9.20 - ovs-vlan-access-trunk.md"
            if "bond" in name:
                return "8.2 - linux-vlan-bonding-team.md (or new 9.x bond)"
            if "patch" in name or "internal" in name:
                return "13.4 - br-int-architecture-and-patch-ports.md"
            return "Block IX OVS internals (9.x)"
        if "1.3" in sec:  # OVSDB
            if "raft" in name or "cluster" in name:
                return "10.1 - ovsdb-raft-clustering.md"
            if "monitor" in name or "idl" in name:
                return "10.4 - ovsdb-idl-monitor-cond-client.md"
            return "Block X OVSDB (10.x)"
        if "1.4" in sec:  # CLI tools
            if "vsctl" in name:
                return "9.4 - ovs-vsctl-mastery.md"
            if "ofctl" in name:
                return "9.10 / 4.7 (ovs-ofctl)"
            if "appctl" in name:
                return "9.11 - ovs-appctl-reference-playbook.md"
            if "dpctl" in name:
                return "9.x ovs-dpctl (or expand 9.4)"
            if "pcap" in name or "tcpundump" in name:
                return "9.28 (NEW per plan J.3)"
            if "vtep-ctl" in name:
                return "9.29 (NEW per plan J.3)"
            if "ovs-pki" in name or "pki" in name:
                return "9.30 (NEW per plan J.3)"
            if "ovsdb-tool" in name:
                return "9.31 (NEW per plan J.3)"
            if "ovsdb-client" in name:
                return "10.7 - ovsdb-client-deep-playbook.md"
            return "Block IX CLI mastery"
        if "1.5" in sec:  # observability
            return "20.4 - ovs-daily-operator-playbook.md (or 9.27 CLI Anatomy)"
        return "Block IX/X (unspecified)"

    # OpenFlow section 2.x
    if entry["section"] == "2":
        if "2.1" in sec:  # pipeline model
            return "4.0 / 4.7 (multi-table pipeline)"
        if "2.2" in sec:  # match fields, actions, instructions
            # Try to detect match field vs action vs instruction
            if any(x in name for x in ["set_field", "output", "drop", "push_", "pop_",
                                        "dec_ttl", "set_queue", "ct(", "learn", "resubmit",
                                        "controller", "note", "sample", "encap", "decap",
                                        "copy_field", "conjunction", "group", "meter"]):
                return "4.9 - openflow-action-catalog.md"
            if any(x in name for x in ["apply-actions", "write-actions", "clear-actions",
                                        "write-metadata", "goto-table", "instruction"]):
                return "4.0 (instructions) or 4.9 (action catalog)"
            return "4.8 - openflow-match-field-catalog.md"
        if "2.3" in sec:  # messages & state machine
            return "3.3 (NEW per plan J.4)"
        if "2.4" in sec:  # version differences
            return "3.4 (NEW per plan J.4)"
        return "Block IV OpenFlow"

    # OVN section 3.x
    if entry["section"] == "3":
        if "3.1" in sec:  # daemons
            if "ic" in name and ("northd" in name or "ic-" in name or "interconnect" in name):
                return "13.15 (NEW per plan J.5)"
            if "vtep" in name:
                return "13.15 / 9.29 (NEW per plan)"
            if "northd" in name:
                return "13.0 / 13.8 (ovn-northd)"
            if "controller" in name:
                return "13.6 / 13.7 (ovn-controller)"
            return "13.0 / 13.1 (OVN architecture)"
        if "3.2" in sec:  # NB/SB schemas
            if "load_balancer" in name or "lb" in name:
                return "13.9 - ovn-load-balancer-virtual-services.md"
            if "logical_switch" in name or "lsp" in name or "ls_" in name:
                return "13.2 - ovn-logical-switches-routers.md"
            if "logical_router" in name or "lr_" in name or "static_route" in name:
                return "13.11 - ovn-gateway-router-distributed.md"
            if "nat" in name:
                return "13.11 / 13.3 (NAT)"
            if "acl" in name or "address_set" in name or "port_group" in name:
                return "13.3 - ovn-acl-lb-nat-port-groups.md"
            if "dhcp" in name or "dns" in name:
                return "13.10 - ovn-dhcp-dns-native.md"
            if "ipam" in name:
                return "13.12 - ovn-ipam-native-dynamic-static.md"
            if "ha_chassis" in name or "bfd" in name:
                return "13.x HA (or 13.11)"
            if "port_binding" in name:
                return "13.5 - port-binding-types-explained.md"
            if "mac_binding" in name or "fdb" in name:
                return "13.x mac learning (or 17.0)"
            return "Block XIII OVN schema (13.x)"
        if "3.3" in sec:  # pipeline + register + REGBIT
            if any(x in name for x in ["ls_in_", "ls_out_", "lr_in_", "lr_out_", "pipeline table"]):
                return "13.16 (NEW per plan J.5, CRITICAL)"
            if "regbit" in name or "mlf" in name or "register" in name or "reg" in name:
                return "13.17 (NEW per plan J.5)"
            if "geneve" in name or "tunnel" in name or "tlv" in name:
                return "11.0 / 13.17 (Geneve TLV)"
            if "chassis" in name or "redirect" in name:
                return "13.7 / 13.11 (chassis redirect)"
            return "13.16 / 13.17 (NEW per plan J.5)"
        if "3.4" in sec:  # CLI
            if "ic-" in name or "interconnect" in name:
                return "13.15 (NEW per plan J.5)"
            if "trace" in name and "detrace" not in name:
                return "20.7 - ovn-trace-tutorial-gradient.md"
            if "detrace" in name:
                return "20.7 / 20.5"
            if "appctl" in name:
                return "13.14 - ovn-nbctl-sbctl-reference-playbook.md"
            return "13.14 - ovn-nbctl-sbctl-reference-playbook.md"
        if "3.5" in sec:  # observability
            if "lflow-cache" in name:
                return "20.2 (lflow-cache stats expand)"
            if "inc-engine" in name:
                return "13.8 (build_lflows + inc-engine)"
            return "20.2 / 20.3 (OVN observability)"
        return "Block XIII OVN"

    return "(needs manual classification)"


def priority_within_tier(entry, file_count):
    """Higher priority = more critical to fix.

    Returns numeric: 100 (CRITICAL) / 75 (HIGH) / 50 (MEDIUM) / 25 (LOW).
    """
    name = entry["name"].lower()
    sec = entry.get("subsection", "")

    # CRITICAL: pipeline table IDs (foundational gap)
    if "3.3" in sec and any(x in name for x in [
        "ls_in_", "ls_out_", "lr_in_", "lr_out_",
        "pipeline table id", "logical port pipeline",
        "table sequence", "ingress pipeline", "egress pipeline",
    ]):
        return 100
    # CRITICAL: REGBIT + MLF + register convention
    if "3.3" in sec and any(x in name for x in ["regbit", "mlf", "register", "tunnel key"]):
        return 95

    # HIGH: OVN core daemons + NB/SB schema (3.1 + 3.2)
    if entry["section"] == "3" and any(x in sec for x in ["3.1", "3.2"]):
        return 75

    # HIGH: OF match field + action catalog (2.2)
    if "2.2" in sec:
        return 75

    # HIGH: OVS daemon + datapath internals (1.1, 1.2)
    if any(x in sec for x in ["1.1", "1.2"]):
        return 75

    # MEDIUM: OVSDB + CLI tools (1.3, 1.4, 3.4)
    if any(x in sec for x in ["1.3", "1.4", "3.4"]):
        return 50

    # MEDIUM: OF messages + version diff (2.3, 2.4)
    if any(x in sec for x in ["2.3", "2.4"]):
        return 50

    # MEDIUM: observability (1.5, 3.5)
    if any(x in sec for x in ["1.5", "3.5"]):
        return 50

    # MEDIUM: troubleshoot scenarios (4)
    if entry["section"] == "4":
        return 50

    # LOW: pipeline model overview (2.1)
    if "2.1" in sec:
        return 25

    return 25


def main():
    print("Parsing REF...")
    entries = parse_ref()
    files = sorted(CURRICULUM_DIR.glob("*.md"))
    print(f"  Curriculum: {len(files)} files, REF: {len(entries)} entries")

    print("Building gap priority list...")
    work_items = []
    for e in entries:
        if e["banned"]:
            continue
        count, matched, alias = grep_with_alternatives(e["name"], files)
        depth = classify_depth(count)
        tier = classify_tier(e, depth)
        if tier in ("A", "B"):  # only Tier A + B = work items
            work_items.append({
                **e,
                "file_count": count,
                "files": matched,
                "depth": depth,
                "tier": tier,
                "matched_via": alias,
                "target_file": suggest_target(e, matched),
                "priority": priority_within_tier(e, count),
            })

    # Sort by priority desc, then by section
    work_items.sort(key=lambda x: (-x["priority"], x["section"], x["subsection"], x["name"]))

    print(f"  Work items (Tier A + B): {len(work_items)}")

    # Group by phase
    phase_map = defaultdict(list)
    for w in work_items:
        sec = w["section"]
        ssec = w.get("subsection", "")
        if sec == "1":
            phase = "J.3 (OVS)"
        elif sec == "2":
            phase = "J.4 (OpenFlow)"
        elif sec == "3":
            phase = "J.5 (OVN)"
        elif sec == "4":
            phase = "J.6 (Troubleshoot distributed)"
        else:
            phase = "(unmapped)"
        phase_map[phase].append(w)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    out = []
    out.append("# Keyword Gap Priority (J.1 output)")
    out.append("")
    out.append(f"> **Source:** generated from `keyword-coverage-matrix.md` + plan v3.5 mapping")
    out.append(f"> **Total work items:** {len(work_items)} (Tier A MISSING + Tier B SHALLOW)")
    out.append(f"> **Generated by:** scripts/build_gap_priority.py")
    out.append("")
    out.append("## Priority levels")
    out.append("")
    out.append("- **100 CRITICAL**: OVN pipeline table IDs (LS_IN_*, LR_IN_*, etc.) — 0 file mention current")
    out.append("- **95 CRITICAL**: REGBIT + MLF + register convention")
    out.append("- **75 HIGH**: OVN core daemons + NB/SB schemas; OF match field + action catalog; OVS datapath internals")
    out.append("- **50 MEDIUM**: OVSDB + CLI tools + observability + OF messages + troubleshoot scenarios")
    out.append("- **25 LOW**: OF pipeline model overview")
    out.append("")
    out.append("## Phase distribution")
    out.append("")
    out.append("| Phase | Work items |")
    out.append("|-------|-----------|")
    for phase in sorted(phase_map.keys()):
        out.append(f"| {phase} | {len(phase_map[phase])} |")
    out.append("")
    out.append("---")
    out.append("")

    # Output by phase
    for phase in sorted(phase_map.keys()):
        items = phase_map[phase]
        if not items:
            continue
        out.append(f"## {phase} ({len(items)} work items)")
        out.append("")

        # Priority breakdown
        prio_count = defaultdict(int)
        for w in items:
            prio_count[w["priority"]] += 1
        prio_str = ", ".join(f"P{p}={c}" for p, c in sorted(prio_count.items(), reverse=True))
        out.append(f"_Priority breakdown: {prio_str}_")
        out.append("")

        out.append("| Priority | Tier | Keyword | Depth | Target file | Notes |")
        out.append("|----------|------|---------|-------|-------------|-------|")
        for w in items:
            name_safe = w["name"].replace("|", "\\|").replace("`", "")
            target_safe = w["target_file"].replace("|", "\\|")
            depth_indicator = f"{w['depth']} ({w['file_count']} file)" if w['file_count'] else "MISSING"
            notes = ""
            if w["matched_via"] != w["name"]:
                notes = f"matched via `{w['matched_via']}`"
            out.append(f"| P{w['priority']} | {w['tier']} | `{name_safe}` | {depth_indicator} | {target_safe} | {notes} |")
        out.append("")

    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Phase breakdown:")
    for phase in sorted(phase_map.keys()):
        print(f"  {phase}: {len(phase_map[phase])} items")


if __name__ == "__main__":
    main()
