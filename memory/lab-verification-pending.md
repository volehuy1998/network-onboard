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

- **Tracker status:** Initialized 2026-04-22 (session 16, Phase C kickoff)
- **Verified on real lab:** 0 / pending (chưa có host)
- **Last audit pass:** pending Phase C1a
- **Lab environment required:**
  - Ubuntu 22.04.3 LTS (kernel 5.15+)
  - OVS 2.17.9 (apt install openvswitch-switch)
  - OVN 22.03.8 (apt install ovn-central ovn-host)
  - Minimum 3 VM/container cho HA test
  - Dedicated physical NIC cho hw-offload labs (Block IX.5)

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

### Block IX — OVS Internals + Operations (15 file, highest density)

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| _Populated during C1a pass_ | | | | | |

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
