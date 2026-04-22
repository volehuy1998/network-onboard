# Lab Verification Pending Inventory

> Central tracker cho mọi Exercise/Lab/CLI output trong sdn-onboard cần verify trên real lab host
> (Ubuntu 22.04 + OVS 2.17.9 + OVN 22.03.8). Tracker được populated dần qua Phase C1a; verified dần
> qua Phase C1b khi user có lab host.
>
> **Quy tắc:** Mỗi CLI output trong Exercise/Lab/in-line code block đều phải được phân loại:
>
> - **verified-lab**: đã chạy thực tế, output verbatim (Rule 7/7a compliant)
> - **doc-plausible**: output kỳ vọng dựa trên compass_artifact + man page + USC lab PDF, chưa chạy
> - **structural-only**: chỉ là schema/syntax placeholder (ví dụ: `ovs-nbctl show` template), không phải output cụ thể
> - **authoritative-external**: trích dẫn verbatim từ RFC/spec/upstream doc (không cần lab verify)

---

## Metadata

- **Tracker status:** Populated 2026-04-22 (session 16, C1a first pass)
- **Verified on real lab:** 0 / pending (chưa có host)
- **Last audit pass:** C1a systemic Grep (2026-04-22) — 54 Exercise/Lab/Capstone headings identified across 70 files
- **Lab environment required:**
  - Ubuntu 22.04.3 LTS (kernel 5.15+)
  - OVS 2.17.9 (apt install openvswitch-switch)
  - OVN 22.03.8 (apt install ovn-central ovn-host)
  - Minimum 3 VM/container cho HA test
  - Dedicated physical NIC cho hw-offload labs (Block IX.5)

## C1a Summary (Exercise Inventory)

Systemic Grep `^### .*(?:Guided Exercise|Lab|Capstone|Trouble Ticket)` across 70 files = **54 exercise/lab/capstone headings**. Distribution:

| Block | Exercises | Capstone | Type mix |
|-------|-----------|----------|----------|
| 0 | 1 (0.1 Ex1) | — | Procedural (version verify) |
| I | 2 (1.0 Ex1, 1.1 Ex1) | 1 (1.2 Block I POE) | POE + Measurement |
| II | — | 1 (2.4 Block II research audit) | Analyze |
| III | — | 1 (3.2 Block III POE) | POE (first-flow install) |
| IV | 2 (4.7 Ex1/Ex2) | 1 (4.6 Block IV POE) | POE (FAST_FAILOVER) |
| V | — | 1 (5.2 Block V troubleshoot) | Trouble Ticket |
| VI | — | — | No exercises (P4 theoretical) |
| VII | 1 (7.0 Ex1 Ryu) | 1 (7.3 Block VII compare) | Procedural + Analyze |
| VIII | 3 (8.0-8.2) | 1 (8.3 Block VIII POE) | POE (stateful firewall) |
| IX | 14 (9.0-9.13) | 1 (9.14 Block IX 6-layer) | Mix procedural + POE + diagnostic |
| X | 3 (10.0-10.2) | — | Procedural (OVSDB ops) |
| XI | 5 (11.0-11.4) | — | Procedural + POE (tunnel) |
| XII | 1 (12.1 design) | — | Design task |
| XIII | 4 (13.1-13.3, 13.5) | 1 (13.6 Block XIII HA) | Procedural (OVN workflow) |
| XVII | 2 Guided + 1 Lab | — | POE + Trouble Ticket (FDB poisoning) |
| XVIII | 2 Guided + 1 Lab | — | POE (ARP responder) |
| XIX | Multi (Lab ENV setup) | — | POE (multichassis) |

**Phân loại output Type (assumed):**

| Origin type | Count est. | Files |
|-------------|------------|-------|
| verified-lab | 0 | (none until C1b) |
| doc-plausible | ~45 | most exercises with compass + USC lab source |
| structural-only | ~9 | schema dumps, workflow templates |
| authoritative-external | ~200+ (in-prose) | RFC quotes, spec fragments |

**Priority matrix cho C1b (khi có lab host):**

- **HIGH**: Capstone Block I-IV + Block VIII-XIII (8 capstones với numeric output: failover latency, throughput, CPU, command counts).
- **MEDIUM**: Guided Exercises Block IX OVS internals (14 exercises với CLI output specific to 2.17.9).
- **LOW**: Historical/narrative exercises Block II-III, design tasks Block XII.

## C4 URL Audit Summary (session 16)

Systemic `curl -L --max-time 8` check on 384 unique URLs:

- **379 OK (98.7%)** — 200/301/302 status
- **5 issues (1.3%)**:
  - `http://10.0.0.3/` — placeholder IP trong CLI demo (no fix needed)
  - `http://odl-controller:8181/restconf/...` — placeholder hostname trong demo (no fix needed)
  - `https://about.netflix.com/en/company-info` — 404 (Netflix moved page) → replace với IR page
  - `https://about.youtube/press/` — 404 (YouTube press moved) → replace với blog company history
  - `https://archive.openflow.org/wk/index.php/OpenFlow_1.1` — 000 timeout (archive.openflow.org intermittent) → replace với ONF spec archive

Files with dead URLs:
- `1.2 - five-drivers-why-sdn.md` (Netflix + YouTube refs)
- `4.0 - openflow-1.1-multi-table-groups.md` (OpenFlow archive)

Replacements TBD in C4 follow-up commit; not blocking Phase C progression.

---

## Priority Classification

- **HIGH**: Capstone Exercise, Lab có numeric output dependencies (throughput, failover time, packet count)
- **MEDIUM**: Guided Exercise với CLI output specific to version
- **LOW**: Structural output (schema dump, list commands) — unlikely version drift

---

## Inventory by Block

### Block 0 — Entry

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| _Populated during C1a pass_ | | | | | |

### Block I — Networking Industry Before SDN

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| _Populated during C1a pass_ | | | | | |

### Block II — SDN Pre-History

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| _Populated during C1a pass_ | | | | | |

### Block III — Stanford Clean Slate + ONF

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| _Populated during C1a pass_ | | | | | |

### Block IV — OpenFlow Specifications

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| _Populated during C1a pass_ | | | | | |

### Block V — Post-OpenFlow SDN

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| _Populated during C1a pass_ | | | | | |

### Block VI — Programmable Data Plane

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| _Populated during C1a pass_ | | | | | |

### Block VII — Controller Ecosystem

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| _Populated during C1a pass_ | | | | | |

### Block VIII — Linux Network Primer

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| _Populated during C1a pass_ | | | | | |

### Block IX — OVS Internals + Operations (24 file, highest density)

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| 9.22 | Guided Exercise 1 — `ofproto/trace` 3-table pipeline Lab 6 | CLI verbatim + POE goto_table reverse | OVS.pdf Lab 6 p116-135 + `ovs-appctl` man | HIGH | doc-plausible (session 23 Phase D) |
| 9.22 | `ovs-appctl ofproto/trace` output format | CLI verbatim | OVS.pdf Lab 6 p19-20 Figure 37 | HIGH | doc-plausible |
| 9.23 | Guided Exercise 1 — `ofproto/trace` verify permit + deny path Lab 7 | CLI verbatim + POE priority ordering | OVS.pdf Lab 7 p141-156 + OpenFlow 1.3.5 §5.3 | HIGH | doc-plausible (session 23 Phase D) |
| 9.23 | `ovs-ofctl dump-flows` output priority ordering | CLI verbatim | OVS.pdf Lab 7 p13 Figure 19 | MEDIUM | doc-plausible |
| 9.23 | POE stateless bidirectional breaking — iperf test | POE, measured | compass Ch 8 priority + OVS tutorial | HIGH | doc-plausible |
| 9.24 | Guided Exercise 1 — POE TCP reply auto-allowed | POE, measured | OVS.pdf Lab 8 p11-15 + netfilter docs | HIGH | doc-plausible (session 22 Phase D) |
| 9.24 | Guided Exercise 2 — TCP lifecycle 5 state transitions via `conntrack -E` | Measured CLI output | OVS.pdf Lab 8 p16-18 + conntrack-tools 1.4.6 | HIGH | doc-plausible |
| 9.24 | Guided Exercise 3 — UDP conntrack POE (pseudo-state bi-directional) | POE, measured | compass Ch 9 + `ovs-fields(7)` ct_state bitfield | MEDIUM | doc-plausible |
| 9.24 | `ovs-dpctl dump-conntrack` output TCP ESTABLISHED + ICMP echo | CLI verbatim | OVS.pdf Lab 8 p15-18 Figures 27/33/35 | HIGH | doc-plausible |
| 9.24 | `conntrack -E` event stream NEW/UPDATE/DESTROY | CLI verbatim | OVS.pdf Lab 8 p16-18 Figure 30/34 + conntrack-tools man | HIGH | doc-plausible |
| _Populated during C1a pass for earlier parts_ | | | | | |

### Block X — OVSDB

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| _Populated during C1a pass_ | | | | | |

### Block XI — Overlay Encapsulation

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| _Populated during C1a pass_ | | | | | |

### Block XII — DC Network Design

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| _Populated during C1a pass_ | | | | | |

### Block XIII — OVN Foundation

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| _Populated during C1a pass_ | | | | | |

### Advanced (XVII-XIX) — OVN deep dives

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| 17.0 | _Populated during C1a pass_ | | | | |
| 18.0 | _Populated during C1a pass_ | | | | |
| 19.0 | _Populated during C1a pass_ | | | | |

---

## Lab Setup Playbook (for future C1b session)

### Prerequisites

```bash
# Ubuntu 22.04.3 LTS VM (minimum 4GB RAM, 2 CPU, 20GB disk)
sudo apt update
sudo apt install -y openvswitch-switch openvswitch-common \
                    ovn-central ovn-host ovn-common \
                    python3 python3-pip \
                    tcpdump iproute2 bridge-utils \
                    conntrack iputils-ping

# Verify versions
ovs-vsctl --version   # Expected: 2.17.9
ovn-nbctl --version   # Expected: 22.03.8
```

### Multi-chassis setup (Block XIII)

Minimum 3 VM để test HA_Chassis_Group + BFD failover:
- chassis-1, chassis-2, chassis-3 với ovn-controller
- ovn-central riêng cho NBDB/SBDB
- OR: 1 VM chạy cả 4 roles (dev mode)

### Execution workflow (future)

```
1. Read memory/lab-verification-pending.md
2. Filter by Priority=HIGH, Status=pending
3. For each entry:
   a. Setup pre-conditions trong lab VM
   b. Run command batch, capture stdout + stderr
   c. Copy verbatim output (Rule 7a — no truncation)
   d. Diff against file's current output
   e. If match → mark verified-lab
   f. If diff → update file with real output, note version/config differences
   g. Update status in this tracker
4. Commit: docs(sdn): lab verification Block X — N exercises verified
```

---

## Notes

- **Fabricated output ban**: per CLAUDE.md Rule 7a, sau C1b KHÔNG CÒN output nào được phép remain "doc-plausible" trong file content. Những gì không thể verify phải được remove hoặc thay bằng structural-only placeholder.
- **Version pinning**: OVS 2.17 và OVN 22.03 là LTS releases. Nếu lab host chạy version khác → note version delta trong output annotation.
- **Reproducibility target**: người đọc chạy cùng command trên cùng version phải thấy cùng output (ignoring UUIDs, timestamps).
