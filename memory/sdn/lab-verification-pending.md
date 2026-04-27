# Lab Verification Pending Inventory

> Central tracker for every Exercise/Lab/CLI output in `sdn-onboard` that needs verification on a real lab host (Ubuntu 22.04 + OVS 2.17.9 + OVN 22.03.8). Populated incrementally; verified incrementally when user has a lab host.
>
> **Convention.** Every CLI output in Exercise/Lab/in-line code block is classified as:
>
> - **verified-lab**: actually run, output verbatim (Rule 7/7a compliant).
> - **doc-plausible**: expected output based on compass_artifact + man page + USC lab PDF, not yet run.
> - **structural-only**: schema/syntax placeholder only (e.g., `ovs-nbctl show` template), not a specific output.
> - **authoritative-external**: verbatim from RFC/spec/upstream doc (no lab verification needed).

---

## Metadata

- **Tracker status:** populated 2026-04-22 (session 16, C1a first pass); extended 2026-04-23 Phase E (+Part 9.26).
- **Verified on real lab:** 0, pending. User confirmed 2026-04-23 session 35: "no lab environment yet, will notify when available".
- **Last audit pass:** Phase E Scope D fact-check audit (2026-04-22), 108 files total curriculum.
- **Lab environment required:**
  - Ubuntu 22.04.3 LTS (kernel 5.15+).
  - OVS 2.17.9 (`apt install openvswitch-switch`).
  - OVN 22.03.8 (`apt install ovn-central ovn-host`).
  - Minimum 3 VMs/containers for HA test.
  - Dedicated physical NIC for hw-offload labs (Block IX.5 + 9.26 revalidator storm reproducer).

**Status update 2026-04-23 (end Phase E):**

- User confirmed no lab host available. Save state, await user notify.
- Total exercise inventory: 54 (original C1a) + 3 (9.26 new: `upcall/show` Exercise 1, `coverage/show` Exercise 2, Capstone POE "reducing flow-limit") = **57 exercises pending C1b verification**.
- Priority HIGH additions: Part 9.26 Capstone POE (reproduce stale ukey leak scenario, verify `upcall/show` output, measure dump duration threshold).
- Priority MEDIUM additions: Part 9.26 Exercise 1 + 2 (CLI output verification on OVS 2.17.9).

**Status update 2026-04-25 (post v3.2):**

- Curriculum at 116 files. New exercises since C1a: Block XIII Core 13.0-13.6 each got at least 1 GE + Capstone POE (v3.2 P1), Block IV 4.0-4.5 each got 1 hands-on GE (v3.2 P3), Anatomy templates added in 20.0/20.1/9.27 (v3.2 P4). Estimated total: ~63 exercises pending lab verification.

---

## C1a summary (Exercise inventory at session 16)

Systemic grep `^### .*(?:Guided Exercise|Lab|Capstone|Trouble Ticket)` across 70 files = **54 exercise/lab/capstone headings**. Distribution:

| Block | Exercises | Capstone | Type mix |
|-------|-----------|----------|----------|
| 0 | 1 (0.1 Ex1) | 0 | Procedural (version verify) |
| I | 2 (1.0 Ex1, 1.1 Ex1) | 1 (1.2 Block I POE) | POE + measurement |
| II | 0 | 1 (2.4 Block II research audit) | Analyze |
| III | 0 | 1 (3.2 Block III POE) | POE (first-flow install) |
| IV | 2 (4.7 Ex1/Ex2) | 1 (4.6 Block IV POE) | POE (FAST_FAILOVER) |
| V | 0 | 1 (5.2 Block V troubleshoot) | Trouble Ticket |
| VI | 0 | 0 | None (P4 theoretical) |
| VII | 1 (7.0 Ex1 Ryu) | 1 (7.3 Block VII compare) | Procedural + analyze |
| VIII | 3 (8.0-8.2) | 1 (8.3 Block VIII POE) | POE (stateful firewall) |
| IX | 14 (9.0-9.13) | 1 (9.14 Block IX 6-layer) | Mix procedural + POE + diagnostic |
| X | 3 (10.0-10.2) | 0 | Procedural (OVSDB ops) |
| XI | 5 (11.0-11.4) | 0 | Procedural + POE (tunnel) |
| XII | 1 (12.1 design) | 0 | Design task |
| XIII | 4 (13.1-13.3, 13.5) | 1 (13.6 Block XIII HA) | Procedural (OVN workflow) |
| XVII | 2 Guided + 1 Lab | 0 | POE + Trouble Ticket (FDB poisoning) |
| XVIII | 2 Guided + 1 Lab | 0 | POE (ARP responder) |
| XIX | Multi (Lab ENV setup) | 0 | POE (multichassis) |

**Output type distribution (estimated):**

| Origin type | Count est. | Files |
|-------------|------------|-------|
| verified-lab | 0 | (none until C1b) |
| doc-plausible | ~45 | most exercises with compass + USC lab source |
| structural-only | ~9 | schema dumps, workflow templates |
| authoritative-external | ~200+ (in-prose) | RFC quotes, spec fragments |

**Priority matrix for C1b (when lab host available):**

- **HIGH**: Capstone Block I-IV + Block VIII-XIII (8 capstones with numeric output: failover latency, throughput, CPU, command counts).
- **MEDIUM**: Guided Exercises Block IX OVS internals (14 exercises with CLI output specific to 2.17.9).
- **LOW**: Historical/narrative exercises Block II-III, design tasks Block XII.

## C4 URL audit summary (session 16)

Systemic `curl -L --max-time 8` check on 384 unique URLs:

- **379 OK (98.7%)**: 200/301/302 status.
- **5 issues (1.3%)**:
  - `http://10.0.0.3/`: placeholder IP in CLI demo (no fix needed).
  - `http://odl-controller:8181/restconf/...`: placeholder hostname in demo (no fix needed).
  - `https://about.netflix.com/en/company-info`: 404 (Netflix moved page). Replaced with IR page.
  - `https://about.youtube/press/`: 404 (YouTube press moved). Replaced with blog company history.
  - `https://archive.openflow.org/wk/index.php/OpenFlow_1.1`: 000 timeout. Replaced with ONF spec archive.

Files with dead URLs (now fixed in v3.1.1):
- `1.2 - five-drivers-why-sdn.md` (Netflix + YouTube refs).
- `4.0 - openflow-1.1-multi-table-groups.md` (OpenFlow archive).

---

## Priority classification

- **HIGH**: Capstone Exercise, Lab with numeric output dependencies (throughput, failover time, packet count).
- **MEDIUM**: Guided Exercise with CLI output specific to OVS/OVN version.
- **LOW**: Structural output (schema dump, list commands), unlikely to drift across versions.

---

## Block IX inventory sample (highest density)

| File | Section | Type | Origin | Priority | Status |
|------|---------|------|--------|----------|--------|
| 9.22 | Guided Exercise 1, `ofproto/trace` 3-table pipeline (USC Lab 6) | CLI verbatim + POE goto_table reverse | OVS.pdf Lab 6 p116-135 + `ovs-appctl` man | HIGH | doc-plausible (Phase D S23) |
| 9.22 | `ovs-appctl ofproto/trace` output format | CLI verbatim | OVS.pdf Lab 6 p19-20 Figure 37 | HIGH | doc-plausible |
| 9.23 | Guided Exercise 1, `ofproto/trace` verify permit + deny (USC Lab 7) | CLI verbatim + POE priority ordering | OVS.pdf Lab 7 p141-156 + OpenFlow 1.3.5 §5.3 | HIGH | doc-plausible (Phase D S23) |
| 9.23 | `ovs-ofctl dump-flows` output priority ordering | CLI verbatim | OVS.pdf Lab 7 p13 Figure 19 | MEDIUM | doc-plausible |
| 9.23 | POE stateless bidirectional breaking, iperf test | POE, measured | compass Ch 8 priority + OVS tutorial | HIGH | doc-plausible |
| 9.24 | Guided Exercise 1, POE TCP reply auto-allowed | POE, measured | OVS.pdf Lab 8 p11-15 + netfilter docs | HIGH | doc-plausible (Phase D S22) |
| 9.24 | Guided Exercise 2, TCP lifecycle 5 state transitions via `conntrack -E` | Measured CLI output | OVS.pdf Lab 8 p16-18 + conntrack-tools 1.4.6 | HIGH | doc-plausible |
| 9.24 | Guided Exercise 3, UDP conntrack POE (pseudo-state bidirectional) | POE, measured | compass Ch 9 + `ovs-fields(7)` ct_state bitfield | MEDIUM | doc-plausible |
| 9.24 | `ovs-dpctl dump-conntrack` output TCP ESTABLISHED + ICMP echo | CLI verbatim | OVS.pdf Lab 8 p15-18 Figures 27/33/35 | HIGH | doc-plausible |
| 9.24 | `conntrack -E` event stream NEW/UPDATE/DESTROY | CLI verbatim | OVS.pdf Lab 8 p16-18 Figure 30/34 + conntrack-tools man | HIGH | doc-plausible |

(Other blocks have similar tables, populated incrementally during C1a pass. Most are still placeholders pending full inventory.)

---

## Lab setup playbook (for future C1b session)

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

Minimum 3 VMs to test HA_Chassis_Group + BFD failover:

- chassis-1, chassis-2, chassis-3 each running `ovn-controller`.
- `ovn-central` separate for NBDB/SBDB.
- Or: 1 VM running all 4 roles (dev mode).

### Execution workflow (future C1b)

```
1. Read memory/lab-verification-pending.md.
2. Filter by Priority=HIGH, Status=pending.
3. For each entry:
   a. Set up pre-conditions in lab VM.
   b. Run command batch, capture stdout + stderr.
   c. Copy verbatim output (Rule 7a, no truncation).
   d. Diff against file's current output.
   e. If match: mark verified-lab.
   f. If diff: update file with real output, note version/config delta.
   g. Update status in this tracker.
4. Commit: docs(sdn): lab verification Block X, N exercises verified.
```

---

## Notes

- **Fabricated output ban.** Per CLAUDE.md Rule 7a, after C1b NO output may remain `doc-plausible` in file content. Anything that cannot be verified must be removed or replaced with `structural-only` placeholder.
- **Version pinning.** OVS 2.17 and OVN 22.03 are LTS releases. If lab host runs a different version, note version delta in output annotation.
- **Reproducibility target.** A reader running the same command on the same version must see the same output (ignoring UUIDs, timestamps).

---

## 2026-04-27 additions (Plan v3.9 Phase S5: 9.12 expansion)

Phần 9.12 Upgrade choreography rewrite (247 → 572 lines, full 20-axis treatment).
New lab-pending entries:

### 9.12.11 Real upgrade transcript (curated)

- **Status:** doc-plausible (curated from upstream `tests/ovsdb-server.at` + OpenStack neutron-ovs-agent doc pattern).
- **Priority:** HIGH (cornerstone-adjacent procedure).
- **Lab requirement:** OpenStack Yoga compute node + 50-host fleet simulation OR single-host minimal.
- **Verification target:** capture verbatim output cho 5-step rolling restart sequence:
  - `ovs-vsctl get Open_vSwitch . ovs-version` (pre + post)
  - `ovsdb-client backup` size + timing
  - `apt install openvswitch-switch=...` package install log
  - `ovs-appctl -t ovsdb-server exit --cleanup` graceful exit log + downtime measurement
  - `ovsdb-tool needs-conversion` decision output
  - `systemctl reload-or-restart openvswitch-switch` restart log + ofproto state restore
  - Total fleet upgrade time measurement
- **Rule 7a target:** verbatim system log per Phần 9.12 §9.12.11 transcript window.

### 9.12.18 Guided Exercise 1 (rolling restart không mất ping)

- **Status:** doc-plausible.
- **Priority:** HIGH.
- **Setup:** test bridge `br-test` + 2 internal port `tap1`, `tap2`.
- **Expected:** ping loss < 1% qua restart window.
- **Verification target:** measure actual loss percentage on real lab.

### 9.12.18 Guided Exercise 2 (schema convert dry-run)

- **Status:** doc-plausible.
- **Priority:** MEDIUM.
- **Setup:** create test DB + test schema, run convert, verify show-log output.
- **Verification target:** verbatim output of `ovsdb-tool show-log` post-convert.

### 9.12.20 Cluster choreography 10-step procedure

- **Status:** doc-plausible (compass Ch N pattern).
- **Priority:** HIGH (production HA scenario).
- **Setup:** 3-node OVSDB Raft cluster.
- **Verification target:** full per-node leave-recreate-rejoin transcript với cluster/status output.

Total new lab-pending entries: 4 (3 GE + 1 cluster procedure).
