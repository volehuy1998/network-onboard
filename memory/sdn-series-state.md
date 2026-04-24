# SDN Onboard Series — State Tracker

> Trạng thái từng Part trong series 20 Block / 116 file. Claude đọc file này để
> biết Part nào đã viết, Part nào đang viết, Part nào chưa đạt target depth.
> **Tên Part phải khớp 100% với `sdn-onboard/README.md` (source of truth).**

**Release hiện tại:** `v3.1-OperatorMaster` (tag 2026-04-24), post-audit 2026-04-25 phát hiện 1 CRITICAL + 7 HIGH finding. v3.1.1 patch sprint in progress 2026-04-25.

**Baseline:** Ubuntu 22.04 LTS + OVS 2.17.9 (jammy-updates) + OVN 22.03.8 (LTS) + kernel 5.15 + Mininet 2.3.0. Upgrade path Ubuntu 24.04 + OVS 3.3 + OVN 24.03.

**Version mapping per block:**

| Ubuntu LTS | OVS | OVN | Kernel | Block context |
|------------|-----|-----|--------|---------------|
| 20.04 | 2.13 | 20.06 | 5.4 | Legacy baseline (deprecated) |
| 22.04 | 2.17.9 | 22.03.8 | 5.15 | Curriculum baseline |
| 24.04 | 3.3 | 24.03 | 6.8 | Upgrade path + future |

Status codes:
- **DONE** — content viết đầy đủ, professor-style 6/6 review PASS
- **PARTIAL** — content phase đang viết hoặc thiếu hands-on / POE / Capstone
- **SHALLOW** — content tồn tại nhưng depth < 250 dòng, cần expand v3.2
- **CRITICAL** — trụ cột foundation mà thiếu nghiêm trọng Anatomy + POE + Key Topic
- **SKELETON** — Rule 10 skeleton only (không áp dụng v3.1+)

---

## Block 0 — Orientation (3 file, 830 dòng)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 0.0 | How to read this series | 148 | DONE | Meta orientation + reading path + convention markers |
| 0.1 | Lab environment setup | 340 | DONE | Ubuntu 22.04 + 3 mode (single-node / two-node chassis pair / kolla). Rule 10 content viết S4 |
| 0.2 | End-to-end packet journey | 342 | DONE | Cross-cutting synthesis, anchor cho mọi topic |

## Block I — Động lực ra đời SDN (3 file, 736 dòng)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 1.0 | Networking industry before SDN (1984-2008) | 198 | DONE | Vendor lock-in + STP 40-50% block + VLAN 4096 + chassis oversubscription |
| 1.1 | Data center pain points | 274 | DONE | VXLAN scalability + RFC 7348 quote + 4 pain point dimension + NSH SFC RFC 8300 |
| 1.2 | Five drivers why SDN | 264 | DONE | Göransson 5 driver analysis (Ch 2.5) + intent-based networking |

## Block II — Tiền thân SDN (5 file, 1.077 dòng)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 2.0 | DCAN, Open Signaling, GSMP | 140 | PARTIAL | Audit P6.N1 MED: thiếu phản biện + Hiểu sai callout |
| 2.1 | Ipsilon + Active Networking | 199 | PARTIAL | Audit P6.N1 MED: thiếu phản biện |
| 2.2 | NAC, Orchestration, Virtualization | 197 | PARTIAL | Audit P6.N1 MED: thiếu Hiểu sai callout |
| 2.3 | ForCES + 4D Project | 219 | DONE | 4D paper analysis + Ethane lineage + `ccr05-4d.pdf` URL verified |
| 2.4 | Ethane (direct ancestor) | 322 | DONE | Casado PhD thesis 2007 + NOX + Nicira founding + Ethane → OpenFlow 1.0 lineage |

## Block III — Khai sinh OpenFlow (3 file, 973 dòng)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 3.0 | Stanford Clean Slate Program | 218 | DONE | NSF FIND + DARPA + McKeown/Shenker/Casado/Parulkar + Nicira 08/2007 + VMware $1.26B |
| 3.1 | OpenFlow 1.0 spec (31/12/2009) | 371 | DONE | 12-tuple match + 8 actions + spec evolution 0.8-1.0.1 |
| 3.2 | ONF formation and governance | 384 | DONE | ONF press release 21/03/2011 + 6 founding operators + 2018 ON.Lab merger |

## Block IV — OpenFlow evolution (10 file, 5.477 dòng)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 4.0 | OF 1.1 multi-table + groups | 375 | PARTIAL | Audit P4.B4.1 HIGH: thiếu hands-on GE |
| 4.1 | OF 1.2 OXM TLV match | 328 | PARTIAL | Audit P4.B4.1 HIGH: thiếu GE + Capstone + POE |
| 4.2 | OF 1.3 meters + PBB + LTS | 255 | PARTIAL | Audit P4.B4.1 HIGH: thiếu hands-on |
| 4.3 | OF 1.4 bundles + eviction | 294 | PARTIAL | Audit P4.B4.1 HIGH: thiếu hands-on |
| 4.4 | OF 1.5 egress + L4/L7 | 323 | PARTIAL | Audit P4.B4.1 HIGH: thiếu hands-on |
| 4.5 | TTP (Table Type Patterns) | 252 | PARTIAL | Audit P4.B4.1 HIGH: thiếu hands-on |
| 4.6 | OpenFlow limitations + Lessons | 416 | DONE | Google B4 SIGCOMM 2013 + P4 lineage + 2 Capstone POE |
| 4.7 | OpenFlow programming với OVS | 764 | DONE | 2 GE + 1 Capstone POE + 8 action + multi-table 3-stage |
| 4.8 | OpenFlow match field catalog | 926 | DONE | Template B 9-attribute anatomy, 60+ match field, 12 nhóm. S41 Phase H.3 |
| 4.9 | OpenFlow action catalog | 1544 | DONE | Template C 8-attribute anatomy, 40+ action tier 1+2+3. S42-S44 Phase H.4 |

## Block V — Mô hình SDN thay thế (3 file, 983 dòng)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 5.0 | SDN via APIs (NETCONF + YANG) | 365 | DONE | RFC 6241 + RFC 7950 + RESTCONF + BGP-LS + Cisco ACI + Juniper Contrail |
| 5.1 | Hypervisor overlays (NVP → NSX) | 305 | DONE | Nicira NVP 2011 + NSX-V/NSX-T + Juniper Contrail BGP EVPN |
| 5.2 | Opening device (whitebox) | 313 | DONE | OCP + SONiC + Cumulus + ONIE + merchant silicon |

## Block VI — Mô hình SDN mới nổi (2 file, 652 dòng)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 6.0 | P4 programmable data plane | 361 | DONE | Bosshart CCR 2014 + PISA + P4_16 overview |
| 6.1 | Flow Objectives abstraction | 291 | DONE | ONOS Flow Objectives 3 type (Filtering/Forwarding/Next) |

## Block VII — Controller ecosystem (6 file, 1.478 dòng)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 7.0 | NOX / POX / Ryu / Faucet | 258 | DONE | 4 Python-based lineage. NOX 2008 → POX 2011 → Ryu 2012 → Faucet 2015 |
| 7.1 | OpenDaylight architecture | 180 | DONE | LF 08/04/2013 + Hydrogen → Argon release train + maintenance-only 2026 |
| 7.2 | ONOS service provider scale | 158 | DONE | ON.Lab + AT&T 2012-2014 + Atomix + Trellis SD-Fabric + merge ONF 10/2018 |
| 7.3 | Vendor controllers (ACI / Contrail) | 191 | DONE | Cisco ACI + Juniper Contrail + NSX-T + Arista CloudVision |
| 7.4 | Faucet pipeline + operations | 272 | DONE | 4 bảng cốt lõi + Prometheus via Gauge |
| 7.5 | Ryu flow management | 419 | DONE | Event system + OFPFlowMod + REST API + traffic stats |

## Block VIII — Linux networking primer (4 file, 837 dòng)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 8.0 | Linux namespaces + cgroups | 194 | DONE | 7 namespace type + ip netns + cgroup v1 vs v2 |
| 8.1 | Linux bridge + veth + macvlan | 254 | DONE | brctl vs ip link + macvlan 4 mode + ipvlan L2/L3 + br-int pattern |
| 8.2 | Linux VLAN + bonding + team | 182 | DONE | 802.1Q + bonding 7 mode + LACP + team deprecate RHEL 9 |
| 8.3 | tc qdisc + conntrack | 207 | DONE | tc qdisc taxonomy + HTB/HFSC/fq_codel + conntrack + OVS ct() |

## Block IX — OpenvSwitch internals (28 file, 15.120 dòng — cluster mạnh nhất curriculum)

### Core foundation (9.0-9.5)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 9.0 | OVS history 2007-present | 258 | DONE | Nicira → NSDI 2015 → LF 2016 |
| 9.1 | OVS 3-component architecture | 749 | DONE (Phase I S63) | 6 Anatomy + 23 offline + §9.1.Y ofproto-dpif xlate tier 2 |
| 9.2 | OVS kernel datapath + megaflow | 878 | DONE (Phase H S40) | 4 Anatomy + 19 offline + EMC+SMC+upcall+ukey lifecycle |
| 9.3 | OVS userspace DPDK + AF_XDP | 209 | DONE | DPDK PMD + AF_XDP + trade-off matrix |
| 9.4 | OVS CLI tools playbook | 1406 | DONE (Phase H S38) | 15 Anatomy exemplar. 6-layer troubleshooting playbook |
| 9.5 | HW offload (switchdev + ASAP² + DOCA) | 318 | DONE | NVIDIA DOCA deep-dive |

### Operations playbook (9.6-9.14)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 9.6 | Bonding + LACP | 162 | SHALLOW | Audit P1.S1/P4.B9.2 MED: v3.2 expand target 400 |
| 9.7 | Port mirroring + packet capture | 154 | SHALLOW | Audit P1.S1/P4.B9.2 MED: v3.2 expand target 400 |
| 9.8 | Flow monitoring (sFlow/NetFlow/IPFIX) | 152 | SHALLOW | Audit P1.S1/P4.B9.2 MED: v3.2 expand target 400 |
| 9.9 | QoS policing + shaping + metering | 649 | DONE | Expand Phase D session 25 |
| 9.10 | TLS + PKI hardening | 174 | SHALLOW | Audit P1.S1/P4.B9.2 MED: v3.2 expand target 400 |
| 9.11 | ovs-appctl reference playbook | 1170 | DONE (Phase H S39) | 22 Anatomy exemplar (strongest Anatomy density) |
| 9.12 | Upgrade + rolling restart | 172 | SHALLOW | Audit P1.S1/P4.B9.2 MED: v3.2 expand target 400 |
| 9.13 | libvirt + docker integration | 202 | DONE | CNI pattern + ovs-docker helper |
| 9.14 | Incident response decision tree | 1494 | DONE (Phase G.2) | 6 Anatomy + 5 Capstone + 5 POE + 20-symptom matrix |

### Deep internals + applied + firewall + debug (9.15-9.27)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 9.15 | ofproto classifier TSS | 407 | DONE (Phase H S45) | 2 Anatomy + subtable internals + Patricia trie |
| 9.16 | OVS connection manager + failover | 433 | DONE (Phase H S45) | 3 Anatomy + multi-controller + OFPT_ROLE wire format |
| 9.17 | OVS performance benchmark methodology | 276 | DONE | iperf + netperf + pktgen + DPDK testpmd |
| 9.18 | OVS native L3 routing | 317 | DONE | dec_ttl action + multi-table router recipe |
| 9.19 | OVS flow table granularity | 278 | DONE | microflow vs megaflow trade-off |
| 9.20 | OVS VLAN access + trunk | 337 | DONE | 4 type (access/trunk/native-tagged/native-untagged) |
| 9.21 | Mininet for OVS labs | 571 | DONE | Python topology API + custom topology class |
| 9.22 | OVS multi-table pipeline | 447 | DONE (Phase D) | goto_table + resubmit |
| 9.23 | OVS stateless ACL firewall | 346 | DONE (Phase D) | Single-table 5-tuple match + default-deny |
| 9.24 | OVS conntrack stateful firewall | 671 | DONE (Phase D) | 3 GE + 3 POE + 5 Key Topic |
| 9.25 | OVS flow debugging + ofproto/trace | 1046 | DONE (Phase G.1.1) | 10 GE + 4 POE |
| 9.26 | OVS revalidator storm forensic | 1185 | DONE (Phase E.B + G.3.2) | 2 Anatomy + 3 case study + 4 GE + 1 Capstone + 5 POE |
| 9.27 | OVS+OVN packet journey end-to-end | 659 | DONE (Phase G.1.2) | 2 GE + 1 Capstone + 5 POE |

## Block X — OVSDB management (7 file, 1.995 dòng)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 10.0 | OVSDB RFC 7047 schema + transactions | 196 | DONE | 10 operations + monitor_cond |
| 10.1 | OVSDB Raft clustering | 199 | DONE | 3-node bootstrap + cluster lifecycle |
| 10.2 | OVSDB backup + restore + compact + RBAC | 231 | DONE | Compact + RBAC Manager.role |
| 10.3 | OVSDB transaction ACID semantics | 321 | DONE | wait/assert/nb_cfg prerequisites + mutate conflict |
| 10.4 | OVSDB IDL + monitor_cond client | 386 | DONE | Conditional replication + reconnect + performance |
| 10.5 | OVSDB performance benchmarking | 297 | DONE | 5 section performance characteristics + bottleneck detect |
| 10.6 | OVSDB security mTLS + RBAC advanced | 365 | DONE | Cert rotation zero-downtime + multi-tenant RBAC + audit log |

## Block XI — Overlay encapsulation (5 file, 2.196 dòng)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 11.0 | VXLAN + Geneve + STT | 213 | DONE | RFC 7348 (VXLAN) + RFC 8926 (Geneve) + 3 protocol comparison |
| 11.1 | Overlay MTU + PMTUD + offload | 213 | DONE | RFC 1191 PMTUD + tunnel MTU math + NIC offload |
| 11.2 | BGP EVPN control plane overlay | 157 | DONE | RFC 7432 + 5 EVPN route types + leaf-spine DC |
| 11.3 | GRE tunnel lab | 742 | DONE (Phase D session 26) | Lab 14 USC full + 3-node OSPF + Wireshark dissector |
| 11.4 | IPsec tunnel lab | 871 | DONE (Phase D session 27) | Lab 15 USC full + strongSwan + GRE over IPsec |

## Block XII — SDN trong Data Center (3 file, 483 dòng)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 12.0 | DC network topologies (Clos + leaf-spine) | 143 | SHALLOW | Audit P1.S3 LOW: skeleton block XII |
| 12.1 | DC overlay integration (VXLAN + EVPN) | 178 | SHALLOW | |
| 12.2 | Micro-segmentation + service chaining | 162 | SHALLOW | |

## Block XIII — OVN foundation (14 file, 4.444 dòng — CRITICAL depth gap per audit)

### Core (13.0-13.6) — Audit P4.B13.1 CRITICAL

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 13.0 | OVN announcement 2015 + rationale | 153 | **CRITICAL** | Audit P4.B13.1 CRITICAL. v3.2 target 350 dòng + Anatomy |
| 13.1 | OVN NBDB + SBDB architecture | 505 | **CRITICAL** | Audit P4.B13.1. v3.2 target 700 dòng + Anatomy |
| 13.2 | OVN Logical Switches + Routers | 399 | **CRITICAL** | Audit P4.B13.1. v3.2 target 700 dòng + 3 GE POE |
| 13.3 | OVN ACL + LB + NAT + Port_Group | 411 | **CRITICAL** | Audit P4.B13.5 HIGH: shallow so với 9.24 conntrack. v3.2 target 800 dòng |
| 13.4 | br-int architecture + patch ports | 142 | **CRITICAL** | Audit P4.B13.4 MED: 142 dòng critical foundation. v3.2 target 500 dòng |
| 13.5 | Port_Binding types (OVN-native) | 182 | **CRITICAL** | v3.2 target 400 dòng + 8 type Anatomy per type |
| 13.6 | HA chassis group + BFD | 183 | **CRITICAL** | 2 Capstone BFD đã có. v3.2 expand BFD deep 400 dòng |

### Extended (13.7-13.12)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 13.7 | ovn-controller internals | 491 | DONE (Phase H) | 2 Anatomy + 2 GE + main_loop + I-P engine |
| 13.8 | ovn-northd translation | 260 | DONE | build_lflows step-by-step |
| 13.9 | OVN Load_Balancer internals | 218 | DONE | ct_lb + VIP + Service_Monitor |
| 13.10 | OVN DHCP + DNS native | 327 | DONE | DHCP options catalog |
| 13.11 | OVN gateway router (distributed) | 516 | DONE (Phase H) | 1 Anatomy + 19-23 stage Template D |
| 13.12 | OVN IPAM native (dynamic + static) | 254 | DONE | |

### Migration (13.13)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 13.13 | OVS to OVN migration guide | 403 | DONE | NB schema mapping + phase rollout + rollback |

## Block XIV — P4 Programmable (Expert, 3 file, 1.354 dòng)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 14.0 | P4 language fundamentals | 507 | DONE (Phase F S36a) | P4_16 + PSA + PISA + BMv2 |
| 14.1 | Tofino PISA silicon | 356 | DONE (Phase F S36b) | Barefoot → Intel 2019 → EOL 2023 |
| 14.2 | P4Runtime + gNMI integration | 491 | DONE (Phase F S36c) | P4Runtime gRPC + Stratum + ONOS |

## Block XV — Service Mesh + K8s (Expert, 3 file, 1.090 dòng — K8s deprioritized per user 2026-04-23)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 15.0 | Service mesh integration | 474 | DONE (Phase F S36g) | Istio + Linkerd + Cilium eBPF + OVN-K8s |
| 15.1 | OVN-Kubernetes CNI deep-dive | 368 | DEFERRED | K8s priority thấp per user 2026-04-23 |
| 15.2 | Cilium eBPF internals | 248 | DEFERRED | K8s priority thấp |

## Block XVI — Kernel + DPDK (Expert, 3 file, 1.630 dòng)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 16.0 | DPDK + AF_XDP + kernel tuning | 636 | DONE (Phase F S36d) | EAL + PMD + hugepage + NUMA + profiling |
| 16.1 | DPDK advanced PMD memory | 434 | DONE | Hugepages 2MB vs 1GB + NUMA + cache line |
| 16.2 | AF_XDP + XDP programs | 560 | DONE (Phase F S36f) | 4-ring + libbpf+libxdp + XDP return codes |

## Block XVII-XIX — OVN Advanced forensic case study (3 file, 3.084 dòng)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 17.0 | OVN L2 forwarding + FDB poisoning | 1196 | DONE (production forensic) | VLAN 3808 case study + FDP-620 |
| 18.0 | OVN ARP responder + BUM suppression | 499 | DONE | ARP responder + BUM suppress mechanism |
| 19.0 | OVN multichassis binding + PMTUD | 1389 | DONE (production forensic) | FDP-620 root cause + RARP activation-strategy + 3 Lab |

## Block XX — Operational Excellence (7 file, 7.999 dòng — Phase G)

| Part | Tên | Dòng | Status | Notes |
|------|-----|------|--------|-------|
| 20.0 | OVS+OVN systematic debugging | 788 | DONE (Phase G.1.4) | 5-layer model + 8 scenario + 3 case study |
| 20.1 | OVS+OVN security hardening | 1334 | DONE (Phase G.3.3) | 4-layer audit trail + port_security + cert rotation + 2 GE + Capstone POE |
| 20.2 | OVN troubleshooting deep-dive | 1627 | DONE (Phase G.3.1) | `ovn-trace` + 21 ovn-appctl + 16-symptom matrix + 3 GE + Capstone POE |
| 20.3 | OVN daily operator playbook | 1554 | DONE (Phase G.5.1) | 10 task category + 2 workflow e2e + 3 GE + Capstone POE |
| 20.4 | OVS daily operator playbook | 1422 | DONE (Phase G.5.2) | Sister 20.3 OVS pure + 4 CLI layer distinguish |
| 20.5 | OVN forensic case studies | 842 | DONE (Phase G.2.3) | 3 distributed control plane case + 3 design lesson + Capstone POE |
| 20.6 | OVS/OpenFlow/OVN retrospective 2007-2024 | 432 | DONE (Phase G.4) | 5 thời kỳ + 10 meta-lesson + 6 frontier |

---

## Thống kê tổng

- **Total file:** 116
- **Total line:** ~52.649
- **Total Block:** 20 (0-XX, bỏ XIV-XVI Expert + VI+VII+XII)
- **DONE:** ~100/116 (86%)
- **PARTIAL:** ~6/116 (5%, mostly Block IV OF spec historical)
- **SHALLOW:** ~9/116 (8%, Block IX Ops 9.6-9.12 + Block XII toàn bộ)
- **CRITICAL (audit flag):** 7/116 (6%, Block XIII Core 13.0-13.6)
- **DEFERRED:** 2/116 (Block XV 15.1 + 15.2, K8s deprioritized)

## Release roadmap

| Tag | Status | Scope |
|-----|--------|-------|
| v3.1-OperatorMaster | ✅ Released 2026-04-24 | Full Phase A-H + audit 2026-04-23 baseline. 116 file, 52.6K dòng |
| **v3.1.1-patch** | 🔧 In progress 2026-04-25 | Dead URL + Rule 11 prose + dependency map + memory tracker. ~10-15h |
| **v3.2-FullDepth** | 📋 Planned | Block XIII Core +2K dòng + Block IX Ops expand + Block IV GE hands-on + CLI Anatomy standardize. ~40-60h |
| v4.0 | 💭 Long-term | New Part based on user feedback + production lab verify |

## Known critical gaps (from audit 2026-04-25)

1. **P4.B13.1 CRITICAL** — Block XIII Core (7 file 13.0-13.6) avg 283 dòng. Target v3.2 500 dòng/file.
2. **P4.B13.2 HIGH** — 0 POE toàn Block XIII (14 file). Target v3.2 10/14 POE.
3. **P4.B13.3 HIGH** — 0 Key Topic callout Block XIII. Target v3.1.1/v3.2 5 callout.
4. **P4.B4.1 HIGH** — 6 file Block IV (4.0-4.5) thiếu hands-on hoàn toàn. Target v3.2 6 GE.
5. **P4.B9.2 MED** — 5 file Block IX Ops (9.6/9.7/9.8/9.10/9.12) < 200 dòng. Target v3.2 400 dòng.

## References

- `memory/audit-2026-04-25-master-report.md` — Latest master audit
- `memory/file-dependency-map.md` — File cross-reference map (Rule 2)
- `memory/session-log.md` — Latest session log
- `sdn-onboard/README.md` — Source of truth for TOC
- `CLAUDE.md` — Project working memory + Rules
- `CHANGELOG.md` — Release history
