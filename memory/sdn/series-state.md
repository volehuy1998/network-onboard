# SDN Onboard Series, State Tracker

> Status of every Part in the 20-Block / 116-file series. Read this to know which Parts are done, in progress, or below target depth. **Part names must match `sdn-onboard/README.md` 100% (the source of truth).**

**Current release:** `v3.6-ContentDepth` (tag 2026-04-26). Verdict A. Coverage strict 80% well-covered (305/383), substantive 72% (275/383). Comprehensive tier 2 source-code coverage cho 5 trụ cột mission core. Permanent ban directive established cho DPDK/BPF/XDP/BGP/K8S. Audit script v2 + v3 với 9 alias rule giảm false-positive 87%.

**Previous releases:** `v3.5-KeywordBackbone` (2026-04-25, framework + master index 0.3 + 9 NEW + 4 EXPAND), `v3.4-DeepFoundation` (Sequence H+O CLOSE).

**Baseline:** Ubuntu 22.04 LTS + OVS 2.17.9 (jammy-updates) + OVN 22.03.8 (LTS) + kernel 5.15 + Mininet 2.3.0. Upgrade path: Ubuntu 24.04 + OVS 3.3 + OVN 24.03.

**Version mapping per block:**

| Ubuntu LTS | OVS | OVN | Kernel | Block context |
|------------|-----|-----|--------|---------------|
| 20.04 | 2.13 | 20.06 | 5.4 | Legacy baseline (deprecated) |
| 22.04 | 2.17.9 | 22.03.8 | 5.15 | Curriculum baseline |
| 24.04 | 3.3 | 24.03 | 6.8 | Upgrade path + future |

**Status codes:**

- **DONE**: content fully written, professor-style 6/6 review PASS.
- **PARTIAL**: content phase in progress, or missing hands-on / POE / Capstone.
- **SHALLOW**: content exists but depth < 250 lines (was target for v3.2 expand, now closed).
- **CRITICAL**: foundation pillar with severe gaps (Anatomy + POE + Key Topic missing; was closed by v3.2).
- **SKELETON**: Rule 10 skeleton only (does not apply post-v3.1).

---

## Block 0, Orientation (3 files, 830 lines)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 0.0 | How to read this series | 148 | DONE | Meta orientation + reading paths + convention markers |
| 0.1 | Lab environment setup | 340 | DONE | Ubuntu 22.04 + 3 modes (single-node / two-node chassis pair / kolla) |
| 0.2 | End-to-end packet journey | 342 | DONE | Cross-cutting synthesis, anchor for every topic |
| 0.3 | Master Keyword Index — Vietnamese DEEP adaptation của REF | 1153 | DONE (Phase J.2 v3.5) | NEW J.2.a/b/c (LAST per max-quality). Lookup spine giữa REF (offline EN) và curriculum (VN teaching). 5 phần: I OVS 80 entry, II OpenFlow 110 entry, III OVN 120+ entry, IV BANNED 10 entry, V cross-link map 50+. Mỗi entry 5-axis 1-line + status code (DEEP/BREADTH/SHALLOW/MISSING/BANNED) + cross-link Phần curriculum. |

## Block I, Why SDN was needed (3 files, 736 lines)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 1.0 | Networking industry before SDN (1984-2008) | 198 | DONE | Vendor lock-in + STP 40-50% block + VLAN 4096 + chassis oversubscription |
| 1.1 | Data center pain points | 274 | DONE | VXLAN scalability + RFC 7348 quote + 4 pain dimensions + NSH SFC RFC 8300 |
| 1.2 | Five drivers why SDN | 264 | DONE | Göransson 5-driver analysis + intent-based networking |

## Block II, Pre-SDN ancestors (5 files, ~1090 lines)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 2.0 | DCAN, Open Signaling, GSMP | 144 | DONE (v3.2 P5) | 2 Hiểu sai callout added in S64 (P6.N1 closed) |
| 2.1 | Ipsilon + Active Networking | 203 | DONE (v3.2 P5) | 2 Hiểu sai callout added |
| 2.2 | NAC, Orchestration, Virtualization | 201 | DONE (v3.2 P5) | 2 Hiểu sai callout added |
| 2.3 | ForCES + 4D Project | 219 | DONE | 4D paper analysis + Ethane lineage |
| 2.4 | Ethane (direct ancestor) | 322 | DONE | Casado PhD 2007 + NOX + Nicira + Ethane to OpenFlow lineage |

## Block III, OpenFlow birth (5 files, 1952 lines, v3.5 J.4.c added 3.3 + 3.4)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 3.0 | Stanford Clean Slate Program | 218 | DONE | NSF FIND + DARPA + McKeown/Shenker/Casado/Parulkar + Nicira 08/2007 |
| 3.1 | OpenFlow 1.0 spec (31/12/2009) | 371 | DONE | 12-tuple match + 8 actions + spec evolution 0.8 to 1.0.1 |
| 3.2 | ONF formation and governance | 384 | DONE | ONF press release 21/03/2011 + 6 founding operators + 2018 ON.Lab merger |
| 3.3 | OpenFlow protocol messages + state machine | 553 | DONE (Phase J.4.c) | NEW. 16 OFPT_* messages chia 4 nhóm + state machine 4-stage + auxiliary connection. Verify ONF spec 1.3.5 + 1.4 + 1.5.1 + IANA port 6653. Bundle atomic vs sequential FLOW_MOD POE. Cross-link 3.1/4.0-4.5/9.16/9.30. |
| 3.4 | OpenFlow version differences 1.0/1.3/1.5 | 426 | DONE (Phase J.4.c) | NEW. 8 version diff (single→multi-table, NXM→OXM, group, meter, bundle, egress, copy_field, packet_type). Migration matrix OF 1.0 → 1.3 → 1.5. Decision tree chọn version. Cross-link 4.0-4.5 + OVS NEWS. |

## Block IV, OpenFlow evolution (10 files, ~5756 lines)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 4.0 | OF 1.1 multi-table + groups | 434 | DONE (v3.2 P3) | Hands-on GE added (+59) |
| 4.1 | OF 1.2 OXM TLV match | 371 | DONE (v3.2 P3) | Hands-on GE ARP+TCP flags (+43) |
| 4.2 | OF 1.3 meters + PBB + LTS | 297 | DONE (v3.2 P3) | Meter rate-limit GE (+42) |
| 4.3 | OF 1.4 bundles + eviction | 344 | DONE (v3.2 P3) | Bundle atomic GE (+50) |
| 4.4 | OF 1.5 egress + L4/L7 | 370 | DONE (v3.2 P3) | Egress simulation GE (+47) |
| 4.5 | TTP (Table Type Patterns) | 290 | DONE (v3.2 P3) | TTP capability discovery GE (+38) |
| 4.6 | OpenFlow limitations + lessons | 416 | DONE | Google B4 SIGCOMM 2013 + P4 lineage + 2 Capstone POE |
| 4.7 | OpenFlow programming with OVS | 764 | DONE | 2 GE + 1 Capstone POE + 8 actions + multi-table 3-stage |
| 4.8 | OpenFlow match field catalog | 1221 | DONE (Phase H S41 + J.4.a v3.5) | Template B 9-attribute anatomy, 60+ match fields, 12 groups + section 4.8.15-17 backfill 12 missing field (in_phy_port, ipv6_flabel, ipv6_exthdr, pbb_isid, mpls_tc/bos, sctp_src/dst, tunnel_id, xreg0-7, xxreg0-3, NSH spi/si/c1-c4, packet_type) |
| 4.9 | OpenFlow action catalog | 1775 | DONE (Phase H S42-S44 + J.4.b v3.5) | Template C 8-attribute anatomy, 40+ actions across 3 tiers + section 4.9.29-30 backfill 12 missing action (copy_field, push/pop_pbb, set_mpls_ttl, dec_mpls_ttl, copy_ttl_in/out, set_nw_ttl, decap/encap NSH, controller userdata, note, sample, conjunction full) |

## Block V, Alternative SDN models (3 files, 983 lines)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 5.0 | SDN via APIs (NETCONF + YANG) | 365 | DONE | RFC 6241 + RFC 7950 + RESTCONF + BGP-LS + Cisco ACI + Juniper Contrail |
| 5.1 | Hypervisor overlays (NVP to NSX) | 305 | DONE | Nicira NVP 2011 + NSX-V/NSX-T + Juniper Contrail BGP EVPN |
| 5.2 | Opening device (whitebox) | 313 | DONE | OCP + SONiC + Cumulus + ONIE + merchant silicon |

## Block VI, Emerging SDN models (2 files, 652 lines)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 6.0 | P4 programmable data plane | 361 | DONE | Bosshart CCR 2014 + PISA + P4_16 overview |
| 6.1 | Flow Objectives abstraction | 291 | DONE | ONOS Flow Objectives 3 types (Filtering/Forwarding/Next) |

## Block VII, Controller ecosystem (6 files, 1478 lines)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 7.0 | NOX / POX / Ryu / Faucet | 258 | DONE | 4 Python lineage. NOX 2008 to POX 2011 to Ryu 2012 to Faucet 2015 |
| 7.1 | OpenDaylight architecture | 180 | DONE | LF 08/04/2013 + Hydrogen to Argon release train + maintenance-only 2026 |
| 7.2 | ONOS service provider scale | 158 | DONE | ON.Lab + AT&T 2012-2014 + Atomix + Trellis SD-Fabric + ONF merge 10/2018 |
| 7.3 | Vendor controllers (ACI / Contrail) | 191 | DONE | Cisco ACI + Juniper Contrail + NSX-T + Arista CloudVision |
| 7.4 | Faucet pipeline + operations | 272 | DONE | 4 core tables + Prometheus via Gauge |
| 7.5 | Ryu flow management | 419 | DONE | Event system + OFPFlowMod + REST API + traffic stats |

## Block VIII, Linux networking primer (4 files, ~1713 lines, Block VIII tier 2 expand 2026-04-25)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 8.0 | Linux namespaces + cgroups | 382 | DONE (Block VIII.1) | Tier 2: clone/unshare/setns syscall internals + lifecycle ref counting + OVS daemon namespace pattern + Anatomy lsns + Capstone POE refute per-container ovs-vswitchd |
| 8.1 | Linux bridge + veth + macvlan | 430 | DONE (Block VIII.2) | Tier 2: drivers/net/veth.c veth_xmit + veth_xdp_xmit + bridge forwarding + so sánh OVS internal port + Anatomy bridge fdb + Capstone POE 1000 container scale |
| 8.2 | Linux VLAN + bonding + team | 426 | DONE (Block VIII.3) | Tier 2: bonding driver bond_xmit_hash + LACP 4-substate state machine + xmit_hash_policy encap3+4 + so sánh OVS bond + Anatomy /proc/net/bonding + Capstone POE balance-rr vs LACP overlay |
| 8.3 | tc qdisc + conntrack | 475 | DONE (Block VIII.4) | Tier 2: kernel queueing path sch_* modules + HTB token bucket source + nf_conntrack hash table + zone implementation + Anatomy tc -s + conntrack -S + Capstone POE nf_conntrack_max sizing |

## Block IX, Open vSwitch internals (28 files, ~15500 lines, strongest cluster)

### Core foundation (9.0-9.5)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 9.0 | OVS history 2007-present | 258 | DONE | Nicira to NSDI 2015 to LF 2016 |
| 9.1 | OVS 3-component architecture | 749 | DONE (Phase I S63) | 6 Anatomy + 23 offline + §9.1.Y ofproto-dpif xlate tier 2 |
| 9.2 | OVS kernel datapath + megaflow | 878 | DONE (Phase H S40) | 4 Anatomy + 19 offline + EMC+SMC+upcall+ukey lifecycle |
| 9.3 | OVS userspace DPDK + AF_XDP | 209 | DONE | DPDK PMD + AF_XDP + trade-off matrix |
| 9.4 | OVS CLI tools playbook | 1406 | DONE (Phase H S38) | 15 Anatomy. 6-layer troubleshooting playbook |
| 9.5 | HW offload (switchdev + ASAP² + DOCA) | 318 | DONE | NVIDIA DOCA deep-dive |

### Operations playbook (9.6-9.14, all v3.2 expand closed)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 9.6 | Bonding + LACP | 297 | DONE (v3.2 P2) | Anatomy `bond/show` 10-attribute + 4 failure modes |
| 9.7 | Port mirroring + packet capture | 275 | DONE (v3.2 P2) | Anatomy `list Mirror` 9-attribute + 4 failure modes |
| 9.8 | Flow monitoring (sFlow/NetFlow/IPFIX) | 252 | DONE (v3.2 P2) | Anatomy `list sFlow` 9-attribute + capacity planning |
| 9.9 | QoS policing + shaping + metering | 649 | DONE | Expand Phase D session 25 |
| 9.10 | TLS + PKI hardening | 258 | DONE (v3.2 P2) | Anatomy `list SSL` 9-attribute + 4 failure modes |
| 9.11 | ovs-appctl reference playbook | 1170 | DONE (Phase H S39) | 22 Anatomy (strongest density) |
| 9.12 | Upgrade + rolling restart | 248 | DONE (v3.2 P2) | Anatomy pre-upgrade checklist + 2 Hiểu sai golden 3 rules |
| 9.13 | libvirt + docker integration | 202 | DONE | CNI pattern + ovs-docker helper |
| 9.14 | Incident response decision tree | 1494 | DONE (Phase G.2) | 6 Anatomy + 5 Capstone + 5 POE + 20-symptom matrix |

### Deep internals + applied + firewall + debug (9.15-9.27)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 9.15 | ofproto classifier TSS | 407 | DONE (Phase H S45) | 2 Anatomy + subtable internals + Patricia trie |
| 9.16 | OVS connection manager + failover | 433 | DONE (Phase H S45) | 3 Anatomy + multi-controller + OFPT_ROLE wire format |
| 9.17 | OVS performance benchmark methodology | 276 | DONE | iperf + netperf + pktgen + DPDK testpmd |
| 9.18 | OVS native L3 routing | 317 | DONE | dec_ttl action + multi-table router recipe |
| 9.19 | OVS flow table granularity | 278 | DONE | microflow vs megaflow trade-off |
| 9.20 | OVS VLAN access + trunk | 337 | DONE | 4 types (access/trunk/native-tagged/native-untagged) |
| 9.21 | Mininet for OVS labs | 571 | DONE | Python topology API + custom topology class |
| 9.22 | OVS multi-table pipeline | 447 | DONE (Phase D) | goto_table + resubmit |
| 9.23 | OVS stateless ACL firewall | 346 | DONE (Phase D) | Single-table 5-tuple match + default-deny |
| 9.24 | OVS conntrack stateful firewall | 671 | DONE (Phase D) | 3 GE + 3 POE + 5 Key Topic |
| 9.25 | OVS flow debugging + ofproto/trace | 1046 | DONE (Phase G.1.1) | 10 GE + 4 POE |
| 9.26 | OVS revalidator storm forensic | 1185 | DONE (Phase E.B + G.3.2) | 2 Anatomy + 3 case study + 4 GE + 1 Capstone + 5 POE |
| 9.27 | OVS+OVN packet journey end-to-end | 696 | DONE (v3.2 P4) | 2 GE + 1 Capstone + Anatomy `tnl/ports/show` + `bfd/show` |

### CLI mastery utilities (9.28-9.31, Phase J.3 v3.5-KeywordBackbone)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 9.28 | ovs-pcap + ovs-tcpundump utility | 269 | DONE (Phase J.3) | NEW. Pure pcap reformatter cho `ofproto/trace` workflow. Verify upstream `ovs-pcap(1)` + `ovs-tcpundump(1)` man page. Anatomy + GE replay packet ICMP qua trace. Anti-pattern `tcpdump -x` thiếu Ethernet header. |
| 9.29 | vtep-ctl + VTEP schema | 347 | DONE (Phase J.3) | NEW. HW VXLAN gateway integration cho bare metal. 7 nhóm command (Physical_Switch/Port, Logical_Switch/Router, MAC binding local/remote, Manager, Database). Bind LSWITCH với physical port:VLAN. Lab synthetic dùng `ovs-vtep` simulator. Verify upstream `vtep-ctl(8)` + vtep.ovsschema. |
| 9.30 | ovs-pki PKI helper | 293 | DONE (Phase J.3) | NEW. SSL/TLS bootstrap cho mTLS giữa chassis ↔ SB DB. 7 commands (init/req/sign/req+sign/verify/fingerprint/self-sign). Two-CA hierarchy (controllerca + switchca). Anti-pattern `req+sign` trên production chassis. Verify upstream `ovs-pki(8)`. |
| 9.31 | ovsdb-tool offline utility | 378 | DONE (Phase J.3) | NEW. 15 commands chia 5 nhóm: creation (create/create-cluster/join-cluster), schema management (convert/needs-conversion/version), inspection (query/transact/show-log), cluster integrity (check-cluster/cluster-to-standalone), maintenance (compact). Anatomy bootstrap 3-node SB cluster from scratch. Verify upstream `ovsdb-tool(1)`. |

## Block X, OVSDB management (8 files, ~2584 lines, Phase I.B2 added 10.7)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 10.0 | OVSDB RFC 7047 schema + transactions | 196 | DONE | 10 operations + monitor_cond |
| 10.1 | OVSDB Raft clustering | 412 | DONE (Phase I.A3 S66') | Tier 2 raft.c source-code internals: raft_run + raft_become_leader/follower + raft_handle_append_request + log compaction + snapshot RPC + edge case bầu leader + Anatomy cluster/status 10-attribute |
| 10.2 | OVSDB backup + restore + compact + RBAC | 231 | DONE | Compact + RBAC Manager.role |
| 10.3 | OVSDB transaction ACID semantics | 321 | DONE | wait/assert/nb_cfg prerequisites + mutate conflict |
| 10.4 | OVSDB IDL + monitor_cond client | 386 | DONE | Conditional replication + reconnect + performance |
| 10.5 | OVSDB performance benchmarking | 297 | DONE | 5 sections + bottleneck detection |
| 10.6 | OVSDB security mTLS + RBAC advanced | 365 | DONE | Cert rotation zero-downtime + multi-tenant RBAC + audit log |
| 10.7 | ovsdb-client deep playbook | 589 | DONE (Phase I.B2 S68') | 7 nhóm chức năng (schema/dump/transact/monitor/wait+lock/backup/convert), 5 Anatomy + GE Port_Binding race + Capstone POE chọn tool đúng |

## Block XI, Overlay encapsulation (5 files, ~3088 lines, Block XI tier 2 expand 2026-04-25)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 11.0 | VXLAN + Geneve + STT | 551 | DONE (Block XI.B1) | Tier 2: Geneve packet format byte-by-byte + IANA TLV class 0x0102 + put_encapsulation source + header math + Anatomy + Capstone VXLAN vs Geneve cho OVN |
| 11.1 | Overlay MTU + PMTUD + offload | 517 | DONE (Block XI.B2) | Tier 2: PMTUD packet flow + black hole + TCP MSS clamp + OVN check_pkt_larger source + NIC offload tunnel-aware + Anatomy + Capstone shrink tenant vs bump underlay |
| 11.2 | BGP EVPN control plane overlay | 408 | DONE (Block XI.B3) | Tier 2: Type 2 NLRI byte-by-byte + Type 3/4/5 deep + Symmetric vs Asymmetric IRB + OVN+BGP-EVPN integration use cases + Anatomy + Capstone BGP EVPN cho OVN intra-cluster |
| 11.3 | GRE tunnel lab | 742 | DONE (Phase D S26) | Lab 14 USC + 3-node OSPF + Wireshark dissector |
| 11.4 | IPsec tunnel lab | 871 | DONE (Phase D S27) | Lab 15 USC + strongSwan + GRE over IPsec |

## Block XII, SDN in Data Centers (3 files, 483 lines)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 12.0 | DC network topologies (Clos + leaf-spine) | 143 | SHALLOW | Audit P1.S3 LOW |
| 12.1 | DC overlay integration (VXLAN + EVPN) | 178 | SHALLOW | |
| 12.2 | Micro-segmentation + service chaining | 162 | SHALLOW | |

## Block XIII, OVN foundation (18 files, ~8401 lines, v3.5 J.5.a/c added 13.15 IC + 13.16 pipeline IDs + 13.17 register)

### Core (13.0-13.6, all v3.2 P1 expanded)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 13.0 | OVN announcement 2015 + rationale | 337 | DONE (v3.2 P1) | Author deep-dive Pfaff/Pettit/Shuhaa, 3 technical + 2 commercial motivations |
| 13.1 | OVN NBDB + SBDB architecture | 624 | DONE (v3.2 P1) | Anatomy `ovn-nbctl show` + `list Datapath_Binding`, 2 Hiểu sai + Key Topic |
| 13.2 | OVN Logical Switches + Routers | 546 | DONE (v3.2 P1) | Anatomy `ls-list` + `lflow-list`, 27+10 stage, Capstone POE 3-tier ping trace |
| 13.3 | OVN ACL + LB + NAT + Port_Group | 563 | DONE (v3.2 P1) | Anatomy `ovn-nbctl acl-list` 9-attribute, Capstone POE 1000-VM segmentation |
| 13.4 | br-int architecture + patch ports | 566 | DONE (v3.2 P1) | 3-bridge pattern, kernel `ovs_vport_receive()` tail-call, Capstone POE TCAM |
| 13.5 | Port_Binding types (OVN-native) | 455 | DONE (v3.2 P1) | 8 Port_Binding types, claim Raft propagation, Anatomy + 5-step debug |
| 13.6 | HA chassis group + BFD | 469 | DONE (v3.2 P1) | RFC 5880 BFD packet + state machine + timing math, 11-step Capstone |

### Extended (13.7-13.12)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 13.7 | ovn-controller internals | 657 | DONE (Phase H + Phase I.A2 S65') | Tier 2 §13.7.8 controller/physical.c source: physical_run + consider_port_binding + put_encapsulation Geneve TLV class 0x0102 + Port_Binding claim race + Anatomy debug/dump-local-bindings + GE Geneve TLV trace 2-chassis |
| 13.8 | ovn-northd translation | 465 | DONE (Phase I.A1 S64') | Tier 2 §13.8.5-8 source: northd.c + ovnnb_db_run + build_lflows + I-P engine 2-node + Anatomy inc-engine/show + parallel build_lflows_thread + Capstone POE n-threads |
| 13.9 | OVN Load_Balancer internals | 627 | DONE (+ J.5.b v3.5) | ct_lb + VIP + Service_Monitor + section 13.9.X backfill J.5.b: selection_fields consistent hashing, hairpin_snat_ip, Load_Balancer_Group aggregation, Load_Balancer_Health_Check 4 options + Service_Monitor |
| 13.10 | OVN DHCP + DNS native | 327 | DONE | DHCP options catalog |
| 13.11 | OVN gateway router (distributed) | 683 | DONE (Phase H + J.5.b v3.5) | 1 Anatomy + 19-23 stages Template D + section 13.11.9 backfill J.5.b: reside-on-redirect-chassis distributed gateway option (TRUE GAP closure: 0→1 file), Logical_Router_Policy 4 action (allow/drop/reroute/jump), Logical_Router_Static_Route ECMP + route_table VRF + BFD fast failover |
| 13.12 | OVN IPAM native (dynamic + static) | 254 | DONE | |

### Migration (13.13)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 13.13 | OVS to OVN migration guide | 403 | DONE | NB schema mapping + phase rollout + rollback |
| 13.14 | ovn-nbctl + ovn-sbctl reference playbook | 997 | DONE (Phase I.B1 S67' + J.5.d v3.5) | Sister cho 9.11. 97 lệnh ovn-nbctl 12 nhóm + 15 lệnh ovn-sbctl. Daemon mode, 10 Anatomy, decision matrix 11 row, GE multi-tier tenant, Capstone POE Rule 5 trụ cột. + section 13.14.9 backfill J.5.d: exhaustive 30+ options chia 8 nhóm (DB connection, wait=sb/hv, idempotency guard, format, daemon mode), ovn-trace microflow expression syntax (24 field), ovn-detrace cookie→Logical_Flow mapping, 5-step debug workflow Anatomy combine ovn-trace + dump-flows + ovn-detrace |

### Foundation depth (13.15 + 13.16 + 13.17, Phase J.5.a/c v3.5-KeywordBackbone)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 13.15 | OVN Inter-Connect federated multi-region | 618 | DONE (Phase J.5.a) | NEW Phase J.5.a. Federated 4-database architecture (NB+SB local + IC_NB+IC_SB central), ovn-ic + ovn-ic-northd daemon, Transit Switch + Transit Router + AvailabilityZone, 2-region lab synthetic, 3-region capstone POE design. Đóng forward-ref 9.31→13.15. Source verified man page ovn-ic(8) + ovn-ic-nbctl(8) + ovn-ic-sbctl(8) + OVN architecture doc. BAN BGP-agent maintained: chỉ static route + link 11.2 cho overview. |
| 13.16 | OVN logical pipeline, bản đồ table ID toàn bộ stage trên br-int | 579 | DONE (Phase J.5.c.ii) | NEW Phase J.5.c.ii. **CRITICAL gap closure** (0/63 stage được mention trước đây). Source verified branch-22.03: northd/northd.c PIPELINE_STAGES (26 LS_IN + 10 LS_OUT + 20 LR_IN + 7 LR_OUT = 63 stage thực, không phải 64 như REF claim), controller/lflow.h OFTABLE_* (table 0, 8-33, 37-39, 40-49, 64-72). Công thức ánh xạ logical→OF table. 3 Anatomy + 2 GE + 1 Capstone POE. Cross-link 11+ Phần. Version drift 22.03→24.03→24.09 documented. |
| 13.17 | OVN register conventions, REGBIT và MLF flags | 516 | DONE (Phase J.5.c.i) | NEW Phase J.5.c.i. Foundation cho 13.16 pipeline IDs. Source verified branch-22.03: include/ovn/logical-fields.h (MFF_LOG_DATAPATH/FLAGS/INPORT/OUTPORT, 13 MLF flag, ct_label bit), northd/northd.c (15 REGBIT reg0 + 5 REGBIT reg9), Geneve TLV class 0x0102. 2 Anatomy + 1 GE + 1 Capstone POE. Cross-link tới 4.8/9.24/11.0/13.7/13.8/13.16/20.7. |

## Block XIV, P4 Programmable (Expert, 3 files, 1354 lines)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 14.0 | P4 language fundamentals | 507 | DONE (Phase F S36a) | P4_16 + PSA + PISA + BMv2 |
| 14.1 | Tofino PISA silicon | 356 | DONE (Phase F S36b) | Barefoot to Intel 2019 to EOL 2023 |
| 14.2 | P4Runtime + gNMI integration | 491 | DONE (Phase F S36c) | P4Runtime gRPC + Stratum + ONOS |

## Block XV, Service Mesh + K8s (Expert, deprioritized 2026-04-23)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 15.0 | Service mesh integration | 474 | DONE (Phase F S36g) | Istio + Linkerd + Cilium eBPF + OVN-K8s |
| 15.1 | OVN-Kubernetes CNI deep-dive | 368 | DEFERRED | K8S deprioritized per user 2026-04-23 |
| 15.2 | Cilium eBPF internals | 248 | DEFERRED | K8S deprioritized |

## Block XVI, Kernel + DPDK (Expert, 3 files, 1630 lines)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 16.0 | DPDK + AF_XDP + kernel tuning | 636 | DONE (Phase F S36d) | EAL + PMD + hugepage + NUMA + profiling |
| 16.1 | DPDK advanced PMD memory | 434 | DONE | Hugepages 2MB vs 1GB + NUMA + cache line |
| 16.2 | AF_XDP + XDP programs | 560 | DONE (Phase F S36f) | 4-ring + libbpf+libxdp + XDP return codes |

## Block XVII-XIX, OVN Advanced forensic case studies (3 files, 3084 lines)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 17.0 | OVN L2 forwarding + FDB poisoning | 1196 | DONE (production forensic) | VLAN 3808 case study + FDP-620 |
| 18.0 | OVN ARP responder + BUM suppression | 499 | DONE | ARP responder + BUM suppress mechanism |
| 19.0 | OVN multichassis binding + PMTUD | 1389 | DONE (production forensic) | FDP-620 root cause + RARP activation-strategy + 3 Labs |

## Block XX, Operational Excellence (8 files, ~8690 lines, Phase G + Phase I.B3 added 20.7)

| Part | Title | Lines | Status | Notes |
|------|-------|-------|--------|-------|
| 20.0 | OVS+OVN systematic debugging | 890 | DONE (Phase G.1.4 + v3.2 P4 + J.6 v3.5) | 5-layer model + 8 scenarios + 3 case studies + Anatomy `coverage/show`. + section 20.0.X backfill J.6: master cross-link table mapping REF Section 4 14 production scenarios → existing curriculum file:section (lookup spine, no duplicate). Audit-driven decision: 14/14 scenario đã coverage substantial trong existing 20.0/20.2/20.5/9.26/13.x; cross-link table thay vì 1200 dòng duplicate. |
| 20.1 | OVS+OVN security hardening | 1399 | DONE (Phase G.3.3 + v3.2 P4) | 4-layer audit trail + Anatomy ACL audit + port_security |
| 20.2 | OVN troubleshooting deep-dive | 1731 | DONE (Phase G.3.1 + J.5.e v3.5) | `ovn-trace` + 21 ovn-appctl + 16-symptom matrix + 3 GE + Capstone POE. + section 20.2.15 backfill J.5.e: 5 lflow-cache external_ids tunable (ovn-enable-lflow-cache, ovn-limit-lflow-cache, ovn-memlimit-lflow-cache-kb, ovn-trim-limit-lflow-cache, ovn-trim-wmark-perc-lflow-cache) Anatomy + decision matrix tuning + anti-pattern. |
| 20.3 | OVN daily operator playbook | 1554 | DONE (Phase G.5.1) | 10 task categories + 2 e2e workflows + 3 GE + Capstone POE |
| 20.4 | OVS daily operator playbook | 1422 | DONE (Phase G.5.2) | Sister to 20.3 OVS pure + 4 CLI layer distinction |
| 20.5 | OVN forensic case studies | 842 | DONE (Phase G.2.3) | 3 distributed control plane cases + 3 design lessons + Capstone POE |
| 20.6 | OVS/OpenFlow/OVN retrospective 2007-2024 | 432 | DONE (Phase G.4) | 5 eras + 10 meta-lessons + 6 frontier trends |
| 20.7 | Packet flow tracing tutorial gradient L1-L5 | 691 | DONE (Phase I.B3 S69') | Sư phạm gradient L1 hello-world to L5 production forensic. 5 level cross-link 9.25/9.27/13.7.8/13.8.5/20.2. ASCII decision tree workflow chọn level. Capstone POE sinh viên tự design trace scenario. |

---

## Total statistics (post-v3.4-DeepFoundation)

- **Total files:** 119 (3 NEW từ Phase I: 13.14, 10.7, 20.7; rest existing expanded)
- **Total lines:** ~61,826 (verified `find sdn-onboard -name '*.md' | xargs wc -l`)
- **Tier 2 coverage:** All HIGHEST + HIGH + MEDIUM tier files DONE. LOW tier (history + DC applied) stays at current depth per North Star relevance analysis.
- **Total Blocks:** 20 (0 to XX)
- **DONE:** ~110/119 (92%)
- **PARTIAL:** 0/119
- **SHALLOW:** 3/119 (2%, only Block XII)
- **CRITICAL (audit flag):** 0/119
- **DEFERRED:** 2/119 (Block XV 15.1 + 15.2, K8S deprioritized)

## Release roadmap

| Tag | Status | Scope |
|-----|--------|-------|
| v3.1-OperatorMaster | RELEASED 2026-04-24 | Full Phase A to H + audit baseline. 116 files, 52.6K lines |
| v3.1.1-OperatorMaster-patch | RELEASED 2026-04-25 | Dead URL + Rule 11 prose + dependency map + memory tracker. 7 commits |
| v3.2-FullDepth | RELEASED 2026-04-25 | Block XIII Core +1584 + Block IX Ops +516 + Block IV GE +279 + CLI Anatomy +112 + Block II narrative +12 |
| v3.3-ArchitectMaster | RELEASED 2026-04-25 | Phase I 6 sessions: Sequence A (3 expand) 13.8 northd source +205 + 13.7 physical.c +166 + 10.1 raft.c +213; Sequence B (3 NEW) 13.14 ovn-nbctl/sbctl 660 + 10.7 ovsdb-client 589 + 20.7 tracing gradient 691. Tier 2 source-code internals + tools mastery + debug pedagogical gradient. |
| v3.3.1-OverlayMaster | UNRELEASED 2026-04-25 | 0.2 truncation fix (+404) + Block XI Overlay tier 2 (11.0/11.1/11.2 +1263). Foundation anchor 12-stage tour fully implemented + Geneve packet format byte-by-byte + PMTUD black hole + EVPN Type 2 NLRI deep + IRB modes + OVN integration use cases. |
| v3.3.2-LinuxPrimer | UNRELEASED 2026-04-25 | Block VIII Linux primer tier 2 (8.0/8.1/8.2/8.3 +876). Kernel source-code level: clone/unshare/setns syscall + veth driver + bonding LACP state machine + nf_conntrack zones + 4 Anatomy + 4 Capstone POE. |
| v3.4-DeepFoundation | RELEASED 2026-04-25 | Tag aggregate cho mọi tier 2 work post-v3.3. 23 commits, +4,577 net lines, 20 files. Block VIII (4 file) + Block X 10.0 + Block XI (3 file) + Block IX (9.0/9.13/9.17/9.18/9.19/9.20) + Block XIII (13.9/13.10/13.12) + 0.2 truncation fix. PERMANENT BAN directive codified for DPDK/BPF/XDP/BGP/K8S. |
| v4.0 | Long-term | New Parts based on user feedback + production lab verify |

## Closed gaps (audit 2026-04-25)

| ID | Severity | Description | Closure |
|----|----------|-------------|---------|
| P4.B13.1 | CRITICAL | Block XIII Core 7 files avg 283 lines | v3.2 expanded to 3560 total (+80%) |
| P4.B13.2 | HIGH | 0 POE in Block XIII | v3.2 added 4 Capstone POE |
| P4.B13.3 | HIGH | 0 Key Topic in Block XIII | v3.2 added 6 Key Topic + 10 Hiểu sai |
| P4.B4.1 | HIGH | Block IV 4.0-4.5 missing hands-on | v3.2 added 6 Guided Exercise |
| P4.B9.2 | MED | Block IX Ops 5 files < 200 lines | v3.2 expanded to 1330 total (+63%) |
| P5.C1 | MED | 20.0/20.1/9.27 missing Anatomy tagging | v3.2 added 3 Anatomy Template A |
| P6.N1 | MED | Block II 2.0/2.1/2.2 missing Hiểu sai | v3.2 added 6 Hiểu sai callout |
| P3.R11.1 | HIGH | 96 prose leaks ~30 files | v3.1.1 fixed via 3-pass sed batch |
| P1.D1 | HIGH | 44 files missing dependency map | v3.1.1 backfilled |
| P6.U1 | LOW | Dead URLs (academic papers + product) | v3.1.1 fixed 6 URLs |

## Plan v3.12 status (curriculum-wide English migration, as of 2026-04-29)

> **Owner directive (2026-04-28).** Every explanatory prose text in the repository must be written in plain technical English per [`memory/shared/english-style-guide.md`](../shared/english-style-guide.md). Every file modified after 2026-04-28 must be all-English. Em-dash (U+2014) is forbidden anywhere in the repository (Rule 17). Pre-commit enforcement: `scripts/em_dash_check.py` and `scripts/lang_check.py` (lingua-py strict mode).

### R1.M (13 OVN advanced + Block XX + README) status

| File | State | Detail |
|------|-------|--------|
| 17.0 | DONE full English | Closed in commit ea200be (sweep "hàm") and earlier R1.M run. lang_check + em_dash_check PASS whole-file. |
| 19.0 | DONE full English | Closed in commit 7e66e07. Lab 1 layer 6, Labs 2 and 3, Exam Prep table, 16-term ISO 10241-1 glossary, 6-category command reference, references list. Anchor link to 17.0 §17.6 updated to post-migration English slug. |
| 20.2 | DONE full English | Closed in commit 4047a1e (already staged; full file English). |
| 13.3 ovn-acl-lb-nat-port-groups | DONE full English | Closed in commit 33065ba. 1,802 lines, 674 prose chunks. End-to-end translation across §13.3.1 through §13.3.10 (foundation, anatomy, callouts, workflow, deep dives, capstone POE), §13.3.X ACL-as-NBDB-table 17-axis deep dive, §13.3.Y NBDB companion tables quick reference, §13.3.Z NAT-as-NBDB-table 17-axis deep dive, and §13.3.W full block of five companion-table deep dives (Address_Set, Port_Group, Logical_Router_Static_Route, Logical_Router_Policy, Forwarding_Group). lang_check PASS whole-file, em_dash_check PASS whole-file. Language status callout: "English (full migration complete, 2026-04-29)". |
| README.md | DONE full English | Closed in commit 977f48e. 558 lines, 323 prose chunks. All seven reading paths, all 20-block table of contents, conventions table, and three appendices (A version evolution, B RFC reference, C bibliography) translated. GP-11 leaks (`Phase G` line 5, `Phase H session` lines 155 and 156) removed. Language status callout: "English (full migration complete, 2026-04-29)". |
| Other R1.M files (10 of 13) | DONE pre-session | The 13-file scope per the existing tracker has 10 files already DONE before this session; the 3 in-flight were 17.0, 19.0, 20.2, all closed this session. |

### R1.N (7 heavy catalog files) status

| File | State | Detail |
|------|-------|--------|
| 13.5 port-binding-types-ovn-native | DONE full English | Closed in commit 7e66e07. Sections §13.5.1 through §13.5.14, including Anatomy Template A, Guided Exercise, 5-step diagnostic, Key takeaways, References, 10-table SBDB quick reference. Em-dashes in section headings replaced. |
| 13.14 ovn-nbctl-sbctl-reference-playbook | DONE full English | Closed in commit 4047a1e (already staged at session start; full file English). |
| 10.1 ovsdb-raft-clustering | DONE full English (sweep) | Single residual fragment "Output mẫu" fixed in commit ea200be. |
| 3.5 openflow-message-catalog | DONE full English | Closed in commit a11c3b4. 1,219 lines, 271 prose chunks. All eight subsections translated end-to-end (§3.5.1 OFPT_HELLO, §3.5.2 FEATURES, §3.5.3 FLOW_MOD, §3.5.4 PACKET_IN, §3.5.5 BARRIER, §3.5.6 peripheral catalogue (5 sub-sections), §3.5.7 bundle and async (5 sub-sections), §3.5.8 OFPMP_* multipart catalogue (5 sub-sections plus 16-row table)). |
| 13.19 ovn-pipeline-stage-catalog | NOT STARTED | About 1,408 Vietnamese-diacritic prose lines, the largest residual file. |
| 4.8 openflow-match-field-catalog | NOT STARTED | About 1,101 Vietnamese-diacritic prose lines. |
| 4.9 openflow-action-catalog | PARTIAL | Header through §4.9.34 translated across 12 commits (72ef39d, 80389b3, 6ccf0f1, 44a9fa0, ebc28ef, 73f6e4e, 1565120, fe0ded3, 70a9c43, 205e0a9). About 327 of 419 prose chunks now English, 78 percent migration progress. Sections English: §4.9.1 foundation, §4.9.2-§4.9.16 Category 1+2, §4.9.17-§4.9.21 Category 3+4+7, §4.9.22 aggregate tier table, §4.9.23-§4.9.28 advanced primitives, §4.9.29 v3.5 backfill (12 actions), §4.9.30 source-code citation, §4.9.31 v3.6 NXM stack/timeout backfill, §4.9.32 output cornerstone deep-dive, §4.9.33.1-§4.9.33.14 cornerstone deep-dives (drop, set_field, mod_dl_src/dst, dec_ttl, mod_nw_src/dst, mod_tp_src/dst, push_vlan, pop_vlan, learn, conjunction, ct), §4.9.34 cross-reference for peripheral action group (4-row navigation table). Remaining (about 92 chunks): §4.9.35.1-5 MPLS+PBB peripheral (push_pbb, pop_pbb, set_mpls_ttl, dec_mpls_ttl, copy_ttl_in), §4.9.36.1-5 NSH+observability peripheral (decap, encap, controller userdata, note, sample), §4.9.37.1-6 NXM stack+register peripheral plus source-code citation. |

### Remaining v3.12 phases (not yet started)

| Phase | Description | Blocker |
|-------|-------------|---------|
| R2 | Final regression audit (lang_check whole-repo, em_dash_check whole-repo, GP-11 leak scan) | Cannot run cleanly until R1.M and R1.N close. |
| R3 | CHANGELOG Reckoning #9 entry | Pending R1 closure. |
| R4 | Dictionary update (`memory/shared/rule-11-dictionary.md` final freeze note) | Pending R1 closure. |
| R5 | Version tag (e.g. `v4.2-EnglishComplete`) | **BLOCKED by Rule 15.** Requires user written sign-off captured in the tag commit message, plus a fresh `per_keyword_rubric_audit.py` scorecard within 24 hours. Cannot be executed by the agent autonomously. |

### Residual prose-line audit (post-2026-04-29 third pass)

| File | Vietnamese prose chunks (lang_check whole-file) |
|------|--------------------------------------------------|
| 13.19 | About 1,408 lines (not yet measured per chunk) |
| 4.8 | About 1,101 lines |
| 4.9 | About 827 lines |
| 13.3 | 0 (closed in commit 33065ba) |
| README.md | 0 (closed in commit 977f48e) |
| 3.5 | 0 (closed in commit a11c3b4) |
| **Total residual chunks (estimate)** | **About 3,300 prose chunks across three remaining heavy files** |

Residual diacritic-bearing fragments outside the count above are non-Vietnamese proper nouns (`Università di Pisa` in 1.1, `Gísli Hjálmtýsson` and `Reykjavík` in 2.3) and pass `lang_check` cleanly.

### Honest closure path (next sessions)

1. One heavy file per session at quality (deepest first by line count, or smallest first by total budget). Each session ends with a `fix(sdn): R1.X v3.12 close <FILE> full English migration` commit and pre-commit checks PASS.
2. Remaining files in priority order: 13.3 (deep-dive sections only), then 4.9, 4.8, 13.19. After all four files close, run R2 regression audit.
3. R3 CHANGELOG Reckoning #9 plus R4 dictionary update in the same session.
4. R5 tag requires the owner's explicit written sign-off per Rule 15.

### Lessons captured this session (2026-04-29)

- The previous automated run produced "Language status: full migration complete" callouts on three partially-translated files (13.5, 19.0, README). The user audit caught it; commit 4047a1e corrected the false claims to honest "Mixed" callouts, and 7e66e07 closed 13.5 and 19.0 honestly. README and 3.5 closed honestly with full-English callouts in commits 977f48e and a11c3b4 after whole-file lang_check verification.
- This is the same anti-pattern flagged by the v3.7 to v3.8 reckoning. Future automation runs must include a per-file diacritic chunk-count verification before stamping any "complete" callout.
- Per-section batched Edit calls work well for files up to roughly 600 lines; for larger files (1,000 plus lines) the work splits naturally into multiple sessions with honest "Mixed" callouts marking the migration boundary.

## References

- [`audit-2026-04-25-summary.md`](audit-2026-04-25-summary.md): consolidated audit summary
- [`file-dependency-map.md`](file-dependency-map.md): file cross-reference map (Rule 2)
- [`session-log.md`](session-log.md): session-by-session journal
- [`sdn-onboard/README.md`](../../sdn-onboard/README.md): TOC source of truth
- [`CLAUDE.md`](../../CLAUDE.md): project working memory + Rules
- [`CHANGELOG.md`](../../CHANGELOG.md): release history
- [`plans/sdn/v3.12-curriculum-wide-english-migration.md`](../../plans/sdn/v3.12-curriculum-wide-english-migration.md): v3.12 plan (R0 to R5 phases)
- [`memory/shared/english-style-guide.md`](../shared/english-style-guide.md): English style policy
