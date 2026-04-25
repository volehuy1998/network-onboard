# File Dependency Map

> Map of cross-file dependencies across the repo. When editing file A, MUST check every file that A references or is referenced by, to avoid sync errors.
>
> **How to use:** before commit, look up the table below, find the file being edited, check the "Related Files" column.

---

## Main dependency table

### Tier 1: README files (TOC and navigation)

| File | Main content | Related Files, MUST check when editing |
|------|--------------|----------------------------------------|
| `README.md` (root) | Repo entry point, lists all series (Linux, Cisco, SDN, HAProxy) | `haproxy-onboard/README.md`, `sdn-onboard/README.md`, `linux-onboard/`, `network-onboard/` |
| `haproxy-onboard/README.md` | TOC for 29 Parts, Knowledge Dependency Map, Appendix A (Version Evolution Tracker, 52 entries, 12 categories) | `README.md` (root, version refs), every `*.md` Part file (Part name must match TOC), `memory/haproxy-series-state.md` (Part name must match) |
| `sdn-onboard/README.md` | TOC for 20 Parts (17 foundation + 3 advanced), dependency graph, log file metadata | `README.md` (root, SDN section), `sdn-onboard/17.0`, `18.0`, `19.0` (section titles must match TOC) |

### Tier 2: Content files (Parts)

| File | Main content | Related Files |
|------|--------------|---------------|
| `haproxy-onboard/1.0 - haproxy-history-and-architecture.md` | Part 1, history, architecture, process model | `haproxy-onboard/README.md` (TOC entry, dependency graph, Appendix A if version-specific), `README.md` (root, summary) |
| `linux-onboard/file-descriptor-deep-dive.md` | FD deep-dive, TLPI 3-table, epoll, CLOEXEC (1261 lines, 14 figures) | 14 SVGs in `images/fd-*.svg` (Tier 5), `README.md` (root, if linked) |

> **Template for new Parts:** copy the row above and adjust. Every new Part must be added here.

### Tier 3: Reference files

| File | Main content | Related Files |
|------|--------------|---------------|
| (Standalone reference file no longer needed; Version Evolution Tracker integrated into `haproxy-onboard/README.md` Appendix A) | (n/a) | (n/a) |

> **Note:** `haproxy-onboard/references/haproxy-version-evolution.md` was migrated into `haproxy-onboard/README.md` Appendix A (session 2026-03-30). The original file should be removed locally (`git rm`).

### Tier 4: Memory and config files

| File | Main content | Related Files |
|------|--------------|---------------|
| `CLAUDE.md` | Working memory, rules, current state | `memory/session-log.md`, `memory/haproxy-series-state.md`, `memory/sdn-series-state.md`, `memory/audit-index.md`, `memory/rule-11-dictionary.md` |
| `memory/session-log.md` | Latest session log | `CLAUDE.md` (Current State section) |
| `memory/haproxy-series-state.md` | Per-Part status (HAProxy series) | `haproxy-onboard/README.md` (TOC) |
| `memory/sdn-series-state.md` | Per-Part status (SDN series) | `sdn-onboard/README.md` (TOC) |
| `memory/audit-index.md` | Audit log TOC | `memory/audit-2026-04-25-summary.md`, `CHANGELOG.md` |
| `memory/rule-11-dictionary.md` | Rule 11 Vietnamese prose dictionary | `CLAUDE.md` Rule 11 §11.2 (pointer back) |

### Tier 2b: SDN onboard, advanced (Parts 17-19)

| File | Main content | Related Files |
|------|--------------|---------------|
| `sdn-onboard/README.md` | Rev 5 (post-v3.2 2026-04-25): TOC for 20 blocks (Block 0 + I to XX). 116 files. Baseline OVS 2.17.9 + OVN 22.03.8 + Ubuntu 22.04 + upgrade path OVS 3.3 + OVN 24.03 + Ubuntu 24.04. Mermaid dependency graph. 7 reading paths. Appendix A Version Evolution Tracker. Appendix B RFC references. Appendix C Bibliography. Scope: OVS + OpenFlow + OVN standalone (no OpenStack/Neutron/kolla). | `README.md` (root, SDN section), every Part file Block 0 to XX, 3 OVN advanced files `17.0/18.0/19.0`, `plans/sdn-foundation-architecture.md` |
| `sdn-onboard/17.0 - ovn-l2-forwarding-and-fdb-poisoning.md` | OVN L2 Forwarding, FDB Poisoning case study VLAN 3808, multichassis/claim high-level, FDP-620 trigger conditions (1178 lines, production log forensics) | `README.md` (root, SDN section), `sdn-onboard/README.md` (TOC), `sdn-onboard/18.0` (cross-ref if 18.0 references 17.0), `sdn-onboard/19.0` (bidirectional cross-refs: Part 17 §17.6 to Part 19 §19.2/§19.4/§19.5/§19.6) |
| `sdn-onboard/18.0 - ovn-arp-responder-and-bum-suppression.md` | OVN ARP Responder, BUM suppression (496 lines, rewritten 2026-04-10) | `sdn-onboard/README.md` (TOC), `sdn-onboard/17.0` (cross-references for tunnel key, localnet port, MC_FLOOD from Part 17) |
| `sdn-onboard/19.0 - ovn-multichassis-binding-and-pmtud.md` | OVN multichassis binding lifecycle + Geneve PMTUD bug FDP-620 root cause + RARP activation-strategy + 3 Labs (1379 lines) | `sdn-onboard/README.md` (TOC), `sdn-onboard/17.0` (live migration trigger, localnet, Chassis/Claim baseline), `README.md` (root, SDN section) |

> **Rule:** when editing SDN 17.0, check whether SDN 18.0 references localnet/MC_UNKNOWN, and whether SDN 19.0 cross-refs live migration/multichassis from Part 17. When editing 18.0, check whether 17.0 has reused concepts. When editing 19.0, check consistency with Part 17 §17.2 (Chassis/Claim) and §17.6 (live migration trigger).

### Tier 2c: Block IX, Open vSwitch internals + operations (15 files)

> Dependency chain: 9.0 history, 9.1 architecture, 9.2 kernel datapath, 9.3 userspace datapath, 9.4 CLI playbook, 9.5 HW offload, 9.6 bonding, 9.7 mirror, 9.8 sFlow/NetFlow/IPFIX, 9.9 QoS, 9.10 TLS, 9.11 appctl reference, 9.12 upgrade, 9.13 libvirt/docker, 9.14 incident response (Capstone).

| File | Main content | Related Files |
|------|--------------|---------------|
| `sdn-onboard/9.0 - ovs-history-2007-present.md` | OVS 2007 Nicira to NSDI 2015 to Linux Foundation 2016, version timeline, comparison vs Linux bridge | `plans/sdn-foundation-architecture.md` §3.3 Block IX, `sdn-onboard/README.md` TOC |
| `sdn-onboard/9.1 - ovs-3-component-architecture.md` | ovs-vswitchd + ovsdb-server + openvswitch.ko, netlink genl family upcall, 6 Anatomy + 23 offline + §9.1.Y ofproto-dpif xlate tier 2 (749 lines, S63 Phase I) | §3.3 Block IX, Part 8.1 (Linux bridge prereq), Part 10 (OVSDB), Part 9.15 (classifier) |
| `sdn-onboard/9.2 - ovs-kernel-datapath-megaflow.md` | microflow to megaflow to ukeys, handler/revalidator threads, NSDI 2015 numbers, EMC+SMC+upcall+ukey lifecycle (878 lines, S40 Phase H) | §3.3 Block IX, 9.1 (prereq), Part 13 (OVN uses megaflow installation path) |
| `sdn-onboard/9.3 - ovs-userspace-dpdk-afxdp.md` | DPDK PMD + hugepages + NUMA, AF_XDP alternative, trade-off matrix | §3.3 Block IX, 9.2 (prereq), 9.5 (DPDK vs DOCA comparison) |
| `sdn-onboard/9.4 - ovs-cli-tools-playbook.md` | ovs-vsctl/ofctl/appctl/dpctl, 6-layer troubleshooting playbook, Capstone Block IX Lab 2 (1406 lines, S38 Phase H) | §3.3 Block IX, 9.3 (prereq), 9.5 (CLI verifies DOCA offload counters) |
| `sdn-onboard/9.5 - hw-offload-switchdev-asap2-doca.md` | switchdev, ASAP² eSwitch, 3 DPIFs comparison, OVS-DOCA internals, vDPA, BlueField DPU, megaflow scaling 200K to 2M | §3.3 Block IX (entry 9.5), 9.3 (trade-off), 9.4 (CLI for `ovs-appctl coverage/show` DOCA counters), Part 8.1 (Linux bridge/veth prereq) |
| `sdn-onboard/9.6 - bonding-and-lacp.md` | 3 bond modes (active-backup/balance-slb/balance-tcp), LACP active/passive/off, fast-timer, fallback-ab, `bond/show`, `lacp/show` (297 lines, v3.2 P2) | 9.1 prereq, Part 8.2 (Linux VLAN bonding), Compass Ch E |
| `sdn-onboard/9.7 - port-mirroring-and-packet-capture.md` | Mirror table OVSDB schema, canonical `--id=@` atomic idiom, local SPAN, RSPAN, cleanup auto-GC (275 lines, v3.2 P2) | 9.1 prereq, 9.6 OVSDB idiom, Compass Ch G |
| `sdn-onboard/9.8 - flow-monitoring-sflow-netflow-ipfix.md` | sFlow (RFC 3176 sampling), NetFlow v5/v9 (RFC 3954), IPFIX (RFC 7011 template negotiation), atomic idiom for all 3, collector stack goflow2/nfdump/ntopng (252 lines, v3.2 P2) | 9.1, 9.7, Compass Ch H |
| `sdn-onboard/9.9 - qos-policing-shaping-metering.md` | OVS configure via tc/rte_sched, ingress policing, egress shaping linux-htb recipe, OF 1.3+ meter-based policing, CIR/PIR 2-color marking, explicit destroy QoS/Queue (no auto-GC) (649 lines) | 9.1, Part 8.3 (tc/qdisc), Part 4.2 (OF 1.3 meters), Compass Ch I + USC Lab 9 |
| `sdn-onboard/9.10 - tls-pki-hardening.md` | ptcp vs ssl (production: ssl), ovs-pki workflow, openssl s_client verification, CA rotation add-then-switch, cipher suite restriction (258 lines, v3.2 P2) | 9.1, Part 10.0 (Manager/Controller URIs), Compass Ch K |
| `sdn-onboard/9.11 - ovs-appctl-reference-playbook.md` | Unix-socket RPC architecture, vlog control, coverage/show, memory/show, ofproto/trace, dpctl/dpif/upcall introspection, DPDK PMD telemetry, tunnel neighbor tables (1170 lines, S39 Phase H) | 9.4 prereq (6-layer playbook), Compass Ch L + R |
| `sdn-onboard/9.12 - upgrade-and-rolling-restart.md` | 3 golden rules (schema before binary, 1 daemon at a time, no kernel+OVS together), 5-step choreography, --bundle atomic, failure modes, in-place vs cordon-and-replace (248 lines, v3.2 P2) | 9.1, 10.0 (OVSDB schema), Compass Ch P + 19 |
| `sdn-onboard/9.13 - libvirt-docker-integration.md` | libvirt virtualport=openvswitch, external_ids:iface-id contract, libvirt troubleshoot, ovs-docker helper, manual veth attach, CNI plugin pattern | 9.1, Part 8.1, Compass Ch S + T |
| `sdn-onboard/9.14 - incident-response-decision-tree.md` | 4-layer mental model (OVSDB/OpenFlow/datapath/wire), 5-branch decision tree, Appendix C reconciliation. Capstone (1494 lines, Phase G.2 + v3.2): 6 Anatomy + 5 Capstone + 5 POE + 20-symptom matrix | 9.4, 9.6, 9.11, Part 13.6 (HA Chassis Group), Compass Ch 20 + Appendix C |

### Tier 2d: Block 0, content written

| File | Main content | Related Files |
|------|--------------|---------------|
| `sdn-onboard/0.0 - how-to-read-this-series.md` | Meta orientation: series positioning, 4 reading paths (linear/OVS-only/OVN-focused/incident-responder), convention markers (Key Topic, Guided Exercise, Lab, Trouble Ticket, version annotation), CCNA/RHCSA/CKA mapping (148 lines) | `sdn-onboard/README.md` (TOC), `sdn-onboard/0.1` (lab modes A/B/C reference) |
| `sdn-onboard/0.1 - lab-environment-setup.md` | Lab setup: 3 modes (single-node / two-node chassis pair / multi-node kolla), Ubuntu 22.04 baseline (kernel 5.15, OVS 2.17.9, OVN 22.03.8 jammy-updates), Mininet 2.3.0 from source, kolla-ansible version matrix, health check playbook, teardown/reset, Guided Exercise 1 (340 lines) | `sdn-onboard/README.md` (baseline OVS/OVN/Ubuntu must match), `plans/sdn-foundation-architecture.md` §3.3 Block 0 |

> **Version sync rule:** when editing baseline OVS/OVN/Ubuntu version in `sdn-onboard/README.md`, MUST update `0.1` §0.1.2 + §0.1.3 (package version block + version annotation) in parallel. Conversely, version mismatch in `0.1` requires checking `README.md` Appendix A Version Evolution Tracker.

### Tier 2f: Block I, content written

| File | Main content | Related Files |
|------|--------------|---------------|
| `sdn-onboard/1.0 - networking-industry-before-sdn.md` | Block I Part 1.0: vendor-proprietary unified control/data/management (1984-2008), vendor lock-in 3 layers, East-West traffic explosion (Jupiter SIGCOMM 2015, Facebook Fabric 2014, Roy SIGCOMM 2015), 3 technical limits (STP 40-50% block, VLAN 4096, chassis oversubscription 8.7:1 Cat 6513), 3 operational limits (CLI/expect, config drift, change velocity), Guided Exercise 1 POE (174 CLI commands, 20-switch VLAN 100), 10 references (198 lines) | `sdn-onboard/README.md` (TOC Block I), `plans/sdn-foundation-architecture.md` §3.3 Block I, `sdn-onboard/1.1` (forward ref: DC pain points), `sdn-onboard/1.2` (forward ref: 5 drivers) |

> **Block I rule:** when editing 1.0, MUST check forward references in 1.1 + 1.2 (when written). Historical claims (Ethane year, IEEE, kolla-ansible versions) must be consistent. When writing 1.1/1.2, MUST NOT repeat 1.0 content (Rule non-repetition); reference section number only ("as 1.0.4 stated").

### Tier 2g: Block II skeleton refined

> Dependency chain: 2.0 to 2.1 to 2.2 to 2.3 to 2.4 (2.4 depends on 2.3 for 4D Project lineage into Ethane).

| File | Main content | Related Files |
|------|--------------|---------------|
| `sdn-onboard/2.0 - dcan-open-signaling-gsmp.md` | DCAN (Cambridge 1995) / OPENSIG (Aurel Lazar Columbia) / GSMP RFC 3292 (06/2002 from Ipsilon) / GSMP message structure vs OF 1.0 12-tuple / legacy: switch controlled by external entity. v3.2 P5 added 2 Hiểu sai callouts (144 lines) | TOC Block II, §3.3 Block II, `sdn-onboard/2.1` (GSMP variant Ipsilon), `sdn-onboard/1.2` (forward ref) |
| `sdn-onboard/2.1 - ipsilon-and-active-networking.md` | Ipsilon IP Switching (Peter Newman 1996, RFC 1953/1987) / Ipsilon to MPLS lineage / DARPA Active Networking 1996-2001 / capsules vs programmable switches / why AN did not commercialize / legacy to P4. v3.2 P5 added 2 Hiểu sai (203 lines) | TOC, §3.3 Block II, `sdn-onboard/2.0` (GSMP prereq), Block VI Part 6.x P4 (forward ref) |
| `sdn-onboard/2.2 - nac-orchestration-virtualization.md` | NAC (RADIUS RFC 2865 + COPS RFC 2748 + 802.1X) / HP OpenView/IBM Tivoli orchestration / VMware vDS 2009 + XenServer OVS 2009 / legacy: modular plugin architecture. v3.2 P5 added 2 Hiểu sai (201 lines) | TOC, §3.3 Block II, `sdn-onboard/2.0` (controller motif prereq), `sdn-onboard/4.1` + Block XIII 13.5 (forward ref modular match/plugin) |
| `sdn-onboard/2.3 - forces-and-4d-project.md` | ForCES WG (RFC 3654/3746/5810) / ForCES CE/FE vs OpenFlow split / why ForCES did not commercialize / 4D Project authors (Rexford/Greenberg/Hjalmtýsson/Maltz/Myers/Zhang) / 4 planes Decision/Dissemination/Discovery/Data / 4D to Ethane lineage (219 lines) | TOC, §3.3 Block II, `sdn-onboard/2.0` (prereq), `sdn-onboard/2.4` (4D to Ethane lineage) |
| `sdn-onboard/2.4 - ethane-the-direct-ancestor.md` | Ethane SIGCOMM 2007 authors (Casado/Freedman/Pettit/Luo/McKeown/Shenker) / centralized policy + flow-based forwarding / NOX controller (CCR 07/2008) / Casado PhD thesis 2007 + Nicira founding / Ethane to OpenFlow 1.0 (CCR 04/2008 + spec 31/12/2009). Capstone Block II Lab (322 lines) | TOC, §3.3 Block II, `sdn-onboard/2.3` (4D prereq), Block IV OpenFlow (forward ref), Block V (Nicira NVP to NSX) |

### Tier 2h: Block III skeleton refined

> Dependency chain: 3.0 to 3.1 to 3.2 (3.2 depends on 3.1 for spec ownership transition Stanford to ONF).

| File | Main content | Related Files |
|------|--------------|---------------|
| `sdn-onboard/3.0 - stanford-clean-slate-program.md` | Clean Slate funded 2006-2012 (NSF FIND + DARPA + industry consortium) / key researchers (McKeown/Shenker/Casado/Parulkar) / Stanford Gates Building deployment 2008-2009 (8-10 HP ProCurve 5400 + NOX) / CCR 04/2008 foundational paper 7 authors / Nicira founding 08/2007 to VMware acquisition 07/2012 (1.26 B USD) (218 lines) | TOC Block III, §3.3 Block III, `sdn-onboard/2.4` (Casado PhD prereq), `sdn-onboard/3.1` (forward ref), Block V (forward ref NVP to NSX) |
| `sdn-onboard/3.1 - openflow-1.0-specification.md` | spec 1.0.0 (31/12/2009, 42 pages, Stanford shepherd) / TCP 6633 plain + TCP 6653 TLS (IANA 09/2013) / message types 3 groups / 12-tuple match (ofp_match §A.2.3) / 8 actions (§A.2.6) / flow entry anatomy / single-table cross-product explosion + OVS resubmit NXM workaround (371 lines) | TOC, §3.3 Block III, `sdn-onboard/3.0` (Stanford history prereq), `sdn-onboard/3.2` (forward ref), `sdn-onboard/2.0` (cross-ref GSMP 12-tuple §2.0.4), Part 4.x (forward ref multi-table 1.1, group table 1.3) |
| `sdn-onboard/3.2 - onf-formation-and-governance.md` | ONF press release 21/03/2011 / 6 founding operators (DT/FB/Google/MS/Verizon/Yahoo) + 17 early adopters / working groups / Stanford to ONF spec ownership transition / ONF vs IETF/IEEE/OCP comparison / 2018 ON.Lab merger to ONOS+CORD+SD-RAN + OpenFlow 1.5.1 last revision (03/2015). Capstone Lab (384 lines) | TOC, §3.3 Block III, `sdn-onboard/3.1` (prereq), Block IV (forward ref), Block VII (forward ref ONOS) |

### Tier 2i: Block IV (10 files)

| File | Main content | Related Files |
|------|--------------|---------------|
| `sdn-onboard/4.0 - openflow-1.1-multi-table-groups.md` | OF 1.1 release 28/02/2011 / multi-table pipeline + GOTO_TABLE / instructions vs actions / 4 group types (ALL/SELECT/INDIRECT/FAST_FAILOVER) / MPLS native / use case multi-tenant. v3.2 P3 hands-on GE (434 lines) | TOC Block IV, §3.3 Block IV, `sdn-onboard/3.1` (cross-product explosion §3.1.7), `sdn-onboard/4.1` (forward ref OXM) |
| `sdn-onboard/4.1 - openflow-1.2-oxm-tlv-match.md` | OF 1.2 release 05/12/2011 / OXM TLV format / IPv6 match fields / controller roles EQUAL/MASTER/SLAVE / migration 1.0 to 1.2. v3.2 P3 hands-on GE (371 lines) | TOC, §3.3 Block IV, `sdn-onboard/4.0` (prereq), `sdn-onboard/4.2` (forward ref IPv6), Block VII (forward ref controllers) |
| `sdn-onboard/4.2 - openflow-1.3-meters-pbb-ipv6.md` | OF 1.3 release timeline 1.3.0 to 1.3.5 (2012-2015) / meter table per-flow QoS / per-connection auxiliary channels / PBB 802.1ah / IPv6 extension headers / why 1.3 = LTS. v3.2 P3 hands-on GE (297 lines) | TOC, §3.3 Block IV, `sdn-onboard/4.1` (OXM prereq), `sdn-onboard/4.3` (forward ref) |
| `sdn-onboard/4.3 - openflow-1.4-bundles-eviction.md` | OF 1.4 release 14/10/2013 / bundles atomic transaction (OPEN/CLOSE/COMMIT/DISCARD + ATOMIC/ORDERED) / flow entry eviction with importance / optical port extensions / adoption reality OVS 2.5 partial. v3.2 P3 hands-on GE (344 lines) | TOC, §3.3 Block IV, `sdn-onboard/4.2` (1.3 prereq), `sdn-onboard/4.4` (1.5), `sdn-onboard/16.1` (forward ref optical) |
| `sdn-onboard/4.4 - openflow-1.5-egress-l4l7.md` | OF 1.5 release 1.5.0 (19/12/2014) + 1.5.1 (26/03/2015) final / egress tables / TCP flags matching / packet type aware / current state 2026: OVS 2.10+ partial, vendor zero. v3.2 P3 hands-on GE (370 lines) | TOC, §3.3 Block IV, `sdn-onboard/4.3` (1.4 prereq), `sdn-onboard/4.6` (forward ref lessons), Block VI Part 6.0 (forward ref P4) |
| `sdn-onboard/4.5 - ttp-table-type-patterns.md` | silicon subset OF spec problem (Broadcom Trident2, Intel FM6000) / TTP analogy HTTP Accept / ONF TS-017 spec (15/08/2014, YANG-based) / Flow Objectives ONOS alternative (forward ref Block VI). v3.2 P3 hands-on GE (290 lines) | TOC, §3.3 Block IV, `sdn-onboard/4.4` (prereq), `sdn-onboard/6.1` (Flow Objectives forward ref) |
| `sdn-onboard/4.6 - openflow-limitations-lessons.md` | 5 limitations (flow-table explosion Broadcom Trident2 4K ACL / controller latency 1-5ms DevoFlow SIGCOMM 2011 / distribution scale Atomix Raft / silicon mismatch / L4-L7 gap) / Google B4 SIGCOMM 2013 fork / lesson to P4 + API SDN. Capstone (416 lines) | TOC, §3.3 Block IV, all 4.0-4.5, `sdn-onboard/5.0` + `6.0`, `sdn-onboard/9.2`, `sdn-onboard/10.1` |
| `sdn-onboard/4.7 - openflow-programming-with-ovs.md` | flow grammar + -O flag / 12-tuple match + NXM/OXM extensions / 8+ actions / multi-table 3-stage L3 routing recipe (USC Lab 6) / conntrack 5-flow stateful firewall recipe (Compass Ch 9 + USC Lab 8) / groups + meters / flow hygiene monitor/replace-flows/diff-flows (764 lines) | Block IV 4.0-4.6 prereq, Part 9.1 (OVS arch), Part 9.9 (QoS meter), 9.11 (ofproto/trace), Part 13.x (OVN uses OF) |
| `sdn-onboard/4.8 - openflow-match-field-catalog.md` | 60+ match fields Template B 9-attribute anatomy. 12 groups: Metadata + Register + L2 + ARP + IPv4 + IPv6 + L4 + ICMP + Tunnel + Conntrack + MPLS + misc. Prerequisite chain table 12 rows. Lazy wildcarding (926 lines, S41 Phase H.3) | TOC Block IV, 4.0-4.5 (OF spec evolution), 4.9 (action catalog sibling), 9.2 (megaflow), 9.15 (classifier TSS), `ovs-fields(7)` |
| `sdn-onboard/4.9 - openflow-action-catalog.md` | 40+ actions Template C 8-attribute anatomy tier 1+2+3. Action Set vs Apply-Actions execution order 12-priority (1544 lines, S42-S44 Phase H.4) | TOC Block IV, 4.8 (match catalog sibling), 9.24 (ct action), 13.3 (OVN ACL conjunction), 13.11 (check_pkt_larger PMTUD), `ovs-actions(7)` |

### Tier 2j: Block XIII expansion (v3.2 P1 closed CRITICAL gap)

> Dependency chain: 13.0 to 13.1 to 13.2 to 13.3 to 13.4 to 13.5 to 13.6.

| File | Main content | Related Files |
|------|--------------|---------------|
| `sdn-onboard/13.0 - ovn-announcement-2015-rationale.md` | OVN announcement 01/2015 (Pfaff/Pettit) / why 8 years after OVS / 3-pillar NBDB + northd + SBDB + controller. v3.2 P1 author deep-dive + 3 tech + 2 commercial motivations + 4 alternative comparison + GE 3-tier compilation (337 lines) | TOC Block XIII, `sdn-onboard/3.0` (Nicira lineage), `sdn-onboard/5.1` (NSX context), `sdn-onboard/9.0` (OVS pure context), `sdn-onboard/13.1` (architecture detail) |
| `sdn-onboard/13.1 - ovn-nbdb-sbdb-architecture.md` | NBDB schema 17 tables + SBDB schema 15 tables. v3.2 P1 Anatomy `ovn-nbctl show` + `list Datapath_Binding`, 2 Hiểu sai + Key Topic, GE NBDB to SBDB timing (624 lines) | TOC, `sdn-onboard/13.0` (rationale), `sdn-onboard/13.2` (LS+LR consume), `sdn-onboard/13.7` (ovn-controller IDL), `sdn-onboard/13.8` (northd compile) |
| `sdn-onboard/13.2 - ovn-logical-switches-and-routers.md` | LS pipeline 27+10 stages + LR pipeline 19-23+7 stages (Template D). v3.2 P1 Anatomy `ls-list` + `lflow-list`, 2 Hiểu sai + Key Topic, Capstone POE 3-tier ping trace (546 lines) | TOC, `sdn-onboard/13.1` (schema prereq), `sdn-onboard/13.3` (ACL/LB consume), `sdn-onboard/13.11` (LR detail), `sdn-onboard/4.9` (action catalog) |
| `sdn-onboard/13.3 - ovn-acl-lb-nat-port-group.md` | OVN ACL expression syntax + allow-related + conjunction + LB deep + Service_Monitor + NAT patterns. v3.2 P1 Anatomy `acl-list` 9-attribute + 2 Hiểu sai + Key Topic Port_Group scale + Capstone POE 1000-VM segmentation (563 lines) | TOC, `sdn-onboard/13.1` (schema), `sdn-onboard/13.2` (pipeline), `sdn-onboard/9.24` (conntrack OVS sibling), `sdn-onboard/4.9` (conjunction action) |
| `sdn-onboard/13.4 - br-int-architecture-and-patch-ports.md` | br-int role + ovn-controller ownership + external bridge pattern (br-ex/br-provider via ovn-bridge-mappings) + patch port zero-copy cross-bridge. v3.2 P1 3-bridge pattern + kernel `ovs_vport_receive()` tail-call + 4 failure modes + 2 GE 2-chassis + flow count + Capstone POE TCAM utilization (566 lines) | TOC, §3.3 Block XIII, `sdn-onboard/9.1` (OVS 3-component), `sdn-onboard/9.4` (CLI baseline), `sdn-onboard/13.5` (localnet triggers patch port), `sdn-onboard/13.3` (prereq) |
| `sdn-onboard/13.5 - port-binding-types-ovn-native.md` | Port_Binding SBDB schema + 8 types (vif/localnet/l2gateway/l3gateway/chassisredirect/patch/localport/virtual) + diagnosis. v3.2 P1 claim Raft propagation + Anatomy `list Port_Binding` + GE claim workflow + 5-step debug (455 lines) | TOC, `sdn-onboard/13.1` (NBDB/SBDB), `sdn-onboard/13.4` (br-int + patch port auto-creation), `sdn-onboard/13.6` (chassisredirect lifecycle) |
| `sdn-onboard/13.6 - ha-chassis-group-and-bfd.md` | HA_Chassis_Group NBDB schema + HA_Chassis priority + BFD session RFC 5880 + failover 3-5s + sub-second tuning + Part 19 cross-ref. v3.2 P1 RFC 5880 packet format + state machine + timing math + Anatomy `bfd/show` 11-attribute + 13-step failover timeline + 11-step Capstone (469 lines) | TOC, `sdn-onboard/13.5` (chassisredirect prereq), `sdn-onboard/19.0` (live migration uses HA_Chassis_Group), `sdn-onboard/11.1` (MTU/PMTUD multichassis) |

### Tier 2l: Block XX, Operational Excellence (7 files)

| File | Main content | Related Files |
|------|--------------|---------------|
| `sdn-onboard/20.0 - ovs-ovn-systematic-debugging.md` | Phase G.1.4 + v3.2 P4: isolation-first philosophy + 5-layer model + 8 common scenarios + 3 production case studies + Anatomy Template A `coverage/show` (815 lines) | TOC Block XX, `sdn-onboard/9.14` (incident decision tree, OVS-specific), `sdn-onboard/9.25` (ofproto/trace), `sdn-onboard/0.2` (packet journey anchor), `sdn-onboard/13.7` (ovn-controller internals) |
| `sdn-onboard/20.1 - ovs-ovn-security-hardening.md` | Phase G.3.3 + v3.2 P4: 3-layer defense-in-depth + port_security + ACL default-deny + audit logging + 4-layer audit trail + RBAC + mTLS + incident response 5-step + compliance logging + Anatomy ACL audit (1399 lines) | TOC Block XX, `sdn-onboard/13.3` (ACL foundation), `sdn-onboard/9.10` (TLS), `sdn-onboard/18.0` (ARP poisoning threat model) |
| `sdn-onboard/20.2 - ovn-troubleshooting-deep-dive.md` | Phase G.3.1: `ovn-trace` 11 options + 9 subsections + `ovn-detrace` chain + Port_Binding 8 types × 22 failure modes + `ovn-appctl` 21 commands (7 Anatomy) + MAC_Binding/FDB/Service_Monitor triage + 16-symptom matrix + 3 GE + Capstone POE (1627 lines) | TOC Block XX, `sdn-onboard/13.1` (NBDB/SBDB schema), `sdn-onboard/13.2` (LS pipeline), `sdn-onboard/13.5` (Port_Binding 8 type), `sdn-onboard/13.7` (ovn-controller main_loop), `sdn-onboard/13.8` (northd compile), `sdn-onboard/13.11` (LR pipeline), `sdn-onboard/9.25` (ofproto/trace), `sdn-onboard/9.27` (3-tier diagnostic), `sdn-onboard/20.0` (debug framework) |
| `sdn-onboard/20.3 - ovn-daily-operator-playbook.md` | Phase G.5.1: 10 task categories (health/inventory/port-lifecycle/ACL/LB+NAT/DHCP+DNS/gateway/conntrack/performance/backup) + 2 e2e workflow scripts + 3 GE + Capstone POE + Anatomy Template A for 10+ commands (1554 lines) | TOC Block XX, `sdn-onboard/13.1`-`13.12` (OVN concepts apply), `sdn-onboard/20.0` (debug framework), `sdn-onboard/20.1` (security workflow), `sdn-onboard/20.2` (troubleshooting tools), `sdn-onboard/9.26` (forensic prevention) |
| `sdn-onboard/20.4 - ovs-daily-operator-playbook.md` | Phase G.5.2 (sister to 20.3 OVS pure): 10 task categories + 2 workflow scripts + 3 GE + Capstone POE + 4 CLI layer distinction (vsctl/ofctl/dpctl/appctl) (1422 lines) | TOC Block XX, `sdn-onboard/9.1` (OVS 3-component prereq), `sdn-onboard/9.2` (kernel DP), `sdn-onboard/9.3` (DPDK), `sdn-onboard/9.4` (CLI playbook), `sdn-onboard/9.11` (ovs-appctl), `sdn-onboard/9.15` (classifier), `sdn-onboard/9.22` (multi-table), `sdn-onboard/9.24` (conntrack), `sdn-onboard/9.25` (flow debug), `sdn-onboard/9.26` (forensic), `sdn-onboard/20.0` + `20.3` (siblings) |
| `sdn-onboard/20.5 - ovn-forensic-case-studies.md` | Phase G.2.3: 3 case studies (Port_Binding migration race, northd bulk tenant deletion memory cascade, MAC_Binding ARP scan exploit) + 3 design lessons + 2 GE + Capstone POE (842 lines) | TOC Block XX, `sdn-onboard/13.1` (SBDB Raft), `sdn-onboard/13.5` (Port_Binding), `sdn-onboard/13.7` (I-P engine), `sdn-onboard/13.8` (northd build_lflows), `sdn-onboard/20.2` (troubleshooting), `sdn-onboard/9.26` (OVS sister forensic) |
| `sdn-onboard/20.6 - ovs-openflow-ovn-retrospective-2007-2024.md` | Phase G.4: 5-era retrospective narrative 2007-2024 + 10 universal meta-lessons + 6 frontier 2024-2030 trends (432 lines) | TOC Block XX, `sdn-onboard/1.0`-`1.2` (pre-SDN context), `sdn-onboard/2.4` (Ethane), `sdn-onboard/3.0`-`3.2` (OpenFlow birth), `sdn-onboard/4.0`-`4.6` (OF evolution), `sdn-onboard/5.1` (NSX), `sdn-onboard/9.0` (OVS history), `sdn-onboard/13.0` (OVN announcement) |

### Tier 2m: Cross-block backfill (v3.1.1 + v3.2)

For brevity, the following blocks have full per-file dependency entries in extended documentation; consult `git show <commit>` for the verbose pre-slim version. Summary by block:

- **Block V (5.0/5.1/5.2):** API SDN (NETCONF/YANG), Hypervisor overlays NVP-NSX, Whitebox device. All DONE.
- **Block VI (6.0/6.1):** P4 fundamentals + Flow Objectives ONOS abstraction. All DONE.
- **Block VII (7.0-7.5):** Controller ecosystem (NOX/POX/Ryu/Faucet, ODL, ONOS, vendor controllers, Faucet pipeline, Ryu management). All DONE.
- **Block VIII (8.0-8.3):** Linux primer (namespaces+cgroups, bridge+veth+macvlan, VLAN+bonding+team, tc+conntrack). All DONE.
- **Block IX deep internals (9.15-9.21/9.23):** classifier TSS, connmgr, performance benchmark, native L3 routing, flow table granularity, VLAN access/trunk, Mininet, stateless ACL. All DONE.
- **Block X (10.0-10.6):** OVSDB RFC 7047, Raft, backup/RBAC, ACID, IDL, performance, security mTLS. All DONE.
- **Block XI (11.0-11.4):** VXLAN/Geneve/STT, MTU/PMTUD, BGP EVPN, GRE Lab 14, IPsec Lab 15. All DONE.
- **Block XII (12.0-12.2):** DC topologies (Clos+leaf-spine), DC overlay integration, micro-segmentation+SFC. All DONE (SHALLOW depth, low priority).
- **Block XIII extended (13.7-13.13):** ovn-controller internals, northd translation, Load_Balancer, DHCP+DNS native, gateway router, IPAM, OVS-to-OVN migration. All DONE.
- **Block XIV (14.0-14.2):** P4 language fundamentals, Tofino PISA silicon, P4Runtime+gNMI. All DONE (Phase F).
- **Block XV (15.0-15.2):** Service mesh (DONE), OVN-K8s CNI (DEFERRED), Cilium eBPF (DEFERRED). 15.1+15.2 deprioritized 2026-04-23.
- **Block XVI (16.0-16.2):** DPDK+AF_XDP+kernel tuning, DPDK advanced PMD, AF_XDP+XDP programs. All DONE.

### Tier 2n: v3.5-KeywordBackbone (Phase J.1 → J.7, 9 NEW + 6 EXPAND)

| File | Main content | Related Files |
|------|--------------|---------------|
| `sdn-onboard/0.3 - master-keyword-index.md` | NEW J.2 v3.5 (1153 dòng). Vietnamese DEEP adaptation của REF, lookup spine cho 320+ keyword 5-axis classification. 5 phần: I OVS (80) + II OpenFlow (110) + III OVN (120+) + IV BANNED (10) + V cross-link map (50+). Mỗi entry status code DEEP/BREADTH/SHALLOW + cross-link Phần curriculum. | TOC Block 0, REF (sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md), tất cả Phần X.Y curriculum được index |
| `sdn-onboard/3.3 - openflow-protocol-messages-state-machine.md` | NEW J.4.c v3.5 (553 dòng). 16 OFPT_* messages chia 4 nhóm + state machine 4-stage (HELLO → FEATURES → Steady → AUX) + auxiliary connections OF 1.3+ + bundle OF 1.4+. Verify ONF spec 1.3.5/1.4/1.5.1 + IANA port 6653. | TOC Block III, `3.1` (OF 1.0 spec), `4.0-4.5` (version evolution detail), `9.16` (OVS connection manager), `9.30` (TLS cert) |
| `sdn-onboard/3.4 - openflow-version-differences-1.0-1.3-1.5.md` | NEW J.4.c v3.5 (426 dòng). 8 version diff features (single→multi-table, NXM→OXM, group, meter, bundle, egress, copy_field, packet_type) + migration matrix + decision tree. Verify ONF spec + OVS NEWS file. | TOC Block III, `3.1` + `3.3` (foundation), `4.0-4.5` (per-version detail) |
| `sdn-onboard/9.28 - ovs-pcap-tcpundump-utility.md` | NEW J.3 v3.5 (269 dòng). Pure pcap reformatter cho ofproto/trace workflow. Anti-pattern tcpdump -x thiếu Ethernet header. Verify ovs-pcap(1) + ovs-tcpundump(1) man page. | TOC Block IX, `9.4` (ovs-vsctl), `9.11` (ovs-appctl), `9.25` (ofproto/trace), `20.0` (debugging), `20.7` (tracing gradient) |
| `sdn-onboard/9.29 - vtep-ctl-vtep-schema.md` | NEW J.3 v3.5 (347 dòng). HW VXLAN gateway integration cho bare metal. 7 nhóm command + bind-ls workflow. Lab synthetic ovs-vtep simulator. Verify vtep-ctl(8) man page + vtep.ovsschema. | TOC Block IX, `10.0` (OVSDB schema), `11.0` (VXLAN), `13.5` (Port_Binding type=vtep), `13.0` (OVN architecture) |
| `sdn-onboard/9.30 - ovs-pki-pki-helper.md` | NEW J.3 v3.5 (293 dòng). SSL/TLS bootstrap cho mTLS. 7 commands + two-CA hierarchy (controllerca + switchca). Anti-pattern req+sign trên production. Verify ovs-pki(8) man page. | TOC Block IX, `10.6` (OVSDB SSL/RBAC), `20.1` (security hardening), `13.0` (OVN architecture mTLS) |
| `sdn-onboard/9.31 - ovsdb-tool-offline-utility.md` | NEW J.3 v3.5 (378 dòng). 15 commands chia 5 nhóm (creation/schema/integrity/inspection/cluster). Anatomy bootstrap 3-node OVN_Southbound Raft cluster. Verify ovsdb-tool(1) man page + ovsdb/raft.c. | TOC Block IX, `10.0` (OVSDB schema), `10.1` (Raft cluster), `10.2` (backup-restore), `9.30` (PKI cho cluster cert) |
| `sdn-onboard/13.15 - ovn-interconnect-multi-region.md` | NEW J.5.a v3.5 (618 dòng). Federated 4-database architecture (NB+SB local + IC_NB+IC_SB central), ovn-ic + ovn-ic-northd daemon, Transit Switch + Transit Router + AvailabilityZone. 2-region lab + 3-region capstone POE. Verify ovn-ic(8) + ovn-ic-nbctl(8) + ovn-ic-sbctl(8) man page. | TOC Block XIII, `13.0` (OVN architecture), `13.1` (NB/SB DB), `10.1` (Raft), `11.0` (Geneve), `9.31` (cluster bootstrap) |
| `sdn-onboard/13.16 - ovn-logical-pipeline-table-id-map.md` | NEW J.5.c.ii v3.5 (579 dòng). **CRITICAL gap closure**: 26 LS_IN + 10 LS_OUT + 20 LR_IN + 7 LR_OUT = 63 stage thực (verified northd/northd.c PIPELINE_STAGES branch-22.03). controller/lflow.h OFTABLE_*. Công thức ánh xạ logical → OF table. | TOC Block XIII, `13.7` (ovn-controller physical.c), `13.8` (northd build_lflows), `13.17` (register convention), `11.0` (Geneve), `20.7` (tracing gradient) |
| `sdn-onboard/13.17 - ovn-register-conventions-regbit-mlf.md` | NEW J.5.c.i v3.5 (516 dòng). Foundation cho 13.16. Verify include/ovn/logical-fields.h (MFF_LOG_DATAPATH/FLAGS/INPORT/OUTPORT, 13 MLF flag, ct_label bit) + northd/northd.c (15 REGBIT reg0 + 5 REGBIT reg9). Geneve TLV class 0x0102. | TOC Block XIII, `4.8` (OF register reg0-15), `9.24` (ct family), `11.0` (Geneve TLV), `13.7` + `13.8` (compile + physical), `13.16` (pipeline IDs reference register) |
| `sdn-onboard/4.8 - openflow-match-field-catalog.md` (EXPAND) | EXPAND J.4.a v3.5 (+295 dòng = 1221). Section 4.8.15 backfill 12 missing match field 9-attribute Anatomy: in_phy_port, ipv6_flabel, ipv6_exthdr, pbb_isid, mpls_tc/bos, sctp_src/dst, tunnel_id, xreg, xxreg, NSH spi/si/c1-c4, packet_type. | (existing dependencies) + `13.17` (register convention reg0-15) |
| `sdn-onboard/4.9 - openflow-action-catalog.md` (EXPAND) | EXPAND J.4.b v3.5 (+231 dòng = 1775). Section 4.9.29 backfill 12 missing action 8-attribute Anatomy: copy_field, push/pop_pbb, set_mpls_ttl, dec_mpls_ttl, copy_ttl_in/out, set_nw_ttl, encap/decap NSH, controller userdata, note, sample, conjunction full. | (existing dependencies) + `13.17` (NSH context) |
| `sdn-onboard/13.14 - ovn-nbctl-sbctl-reference-playbook.md` (EXPAND) | EXPAND J.5.d v3.5 (+337 dòng = 997). Section 13.14.9 backfill: exhaustive 30+ ovn-nbctl options chia 8 nhóm + ovn-trace microflow expression syntax (24 field) + ovn-detrace cookie→Logical_Flow mapping + 5-step debug workflow. | (existing dependencies) + `20.2` (ovn-trace + ovn-detrace use case), `20.7` (tracing gradient) |
| `sdn-onboard/20.2 - ovn-troubleshooting-deep-dive.md` (EXPAND) | EXPAND J.5.e v3.5 (+104 dòng = 1731). Section 20.2.15 backfill: 5 lflow-cache external_ids tunable (ovn-enable/limit/memlimit/trim-limit/trim-wmark-perc) Anatomy + decision matrix tuning. | (existing dependencies) + `13.7 §13.7.3` (I-P engine) |
| `sdn-onboard/13.11 - ovn-gateway-router-distributed.md` (EXPAND) | EXPAND J.5.b v3.5 (+167 dòng = 683). Section 13.11.9: reside-on-redirect-chassis distributed gateway (TRUE GAP closure 0→1 file), Logical_Router_Policy 4 action (allow/drop/reroute/jump), Logical_Router_Static_Route ECMP + route_table VRF + BFD. | (existing dependencies) + `13.16 §13.16.6` (LR_IN_GW_REDIRECT stage) |
| `sdn-onboard/13.9 - ovn-load-balancer-internals.md` (EXPAND) | EXPAND J.5.b v3.5 (+176 dòng = 627). Section 13.9.X: selection_fields consistent hashing 6 field, hairpin_snat_ip rewrite, Load_Balancer_Group aggregation, Load_Balancer_Health_Check 4 options + Service_Monitor. | (existing dependencies) + `13.16 §13.16.4` (LS_IN_LB stage 12 + hairpin stage 13-15) |
| `sdn-onboard/20.0 - ovs-ovn-systematic-debugging.md` (EXPAND) | EXPAND J.6 v3.5 (+75 dòng = 890). Section 20.0.X: master cross-link table mapping 14 REF Section 4 production scenarios → existing curriculum file:section. Audit-driven (no duplicate, all 14 đã coverage). | (existing dependencies) + REF Section 4 (offline source) |

### Tier 2o: v3.6-ContentDepth (Phase 1 → Phase 4, 3 EXPAND + 3 NEW memory/script)

| File | Main content | Related Files |
|------|--------------|---------------|
| `sdn-onboard/4.9 - openflow-action-catalog.md` (EXPAND v3.6) | EXPAND Phase 2 v3.6 (+77 dòng = 1852). Section 4.9.31 backfill 3 NXM Nicira action 8-attribute Anatomy: fin_timeout (TCP FIN/RST timeout shrink), push:FIELD (NXAST_STACK_PUSH), pop:FIELD (NXAST_STACK_POP). Cross-link 9.24 conntrack timeout, 4.7 learn template, 9.25 ofproto/trace stack debug. | (existing dependencies) + `9.24` (ct() timeout alternative), `4.7` (learn template), `9.25` (ofproto/trace) |
| `sdn-onboard/13.14 - ovn-nbctl-sbctl-reference-playbook.md` (EXPAND v3.6) | EXPAND Phase 2 v3.6 (+7 dòng = 1003). Section 13.14.9.1 thêm 2 ovn-nbctl flag missing: --print-wait-time (transaction wait latency tracking) + -u <path> (daemon socket separation cho multi-tenant). Verify ovn-nbctl(8) man page qua WebFetch. | (existing dependencies) + `20.2 §lflow-cache` (convergence latency tuning) |
| `sdn-onboard/9.7 - port-mirroring-and-packet-capture.md` (EXPAND v3.6) | EXPAND Phase 3 v3.6 (+39 dòng = 313). Section 9.7.9 ovs-tcpdump shortcut wrapper Anatomy: tự động Mirror table tạm + tcpdump + cleanup atomic. Anti-pattern long-running capture (Mirror lock cost). | (existing dependencies) + `9.4` (ovs-vsctl Mirror), `9.28` (ovs-pcap đọc lại) |
| `scripts/refine_coverage_matrix_v2.py` | NEW Phase 1 v3.6 (501 dòng). Audit script v2 + v3 với 9 alias rule (Action/Instruction/Match field prefix strip, version paren strip, slash split, range expand, bilingual concept dict 80+, tool prefix strip, table suffix strip, case-aware uppercase-to-proper, lookup spine separate). Output dual-tier matrix (strict + substantive count). | sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md (REF input), sdn-onboard/*.md (curriculum), memory/sdn/keyword-coverage-matrix-v2.md (output) |
| `memory/sdn/keyword-coverage-matrix-v2.md` | NEW Phase 1 v3.6 (1100+ dòng). Refined coverage matrix dual-tier (Strict count + Substantive count loại 0.3). 383 entry total, well-covered strict 80% + substantive 72%. | scripts/refine_coverage_matrix_v2.py (generator), memory/sdn/keyword-true-gap-final.md (manual classify) |
| `memory/sdn/keyword-true-gap-final.md` | NEW Phase 1+2 v3.6 (200+ dòng). Manual classify 21 strict Tier A → 7 candidate gap → 5 TRUE gap (đã đóng) + 14-16 false-positive (đã có content qua slash form / Anatomy template / cross-link). Decision log Phase 2+3 skip rationale. | scripts/refine_coverage_matrix_v2.py (input), CHANGELOG.md (Release reference), plans/sdn/v3.6-content-depth.md (acceptance gate evidence) |

### Tier 5: Image files (SVG to Markdown captions)

| File | Main content | Related Files |
|------|--------------|---------------|
| `images/fd-kernel-3-table-model.svg` | Figure 1-1: TLPI Three-Table Model (pure, no fork/exec) | `linux-onboard/file-descriptor-deep-dive.md` (caption ~line 141) |
| `images/fd-exercise1-initial-open-read.svg` | Figure 1-2: GE 2 baseline (1 FD, 1 OFD, pos=5) | (caption ~line 195) |
| `images/fd-exercise1-after-dup.svg` | Figure 1-3: GE 2 after `dup()` (FD 3,4 to OFD "A") | (caption ~line 228) |
| `images/fd-exercise1-after-open-independent.svg` | Figure 1-4: GE 2 after independent `open()` (2 OFDs) | (caption ~line 250) |
| `images/fd-exercise1-read-offset-sharing.svg` | Figure 1-5: GE 2 final (`open()` + `dup()` + `fork()`) | (caption ~line 346) |
| `images/fd-exercise2-dup-write.svg` | Figure 1-6: GE 3 Part E (dup write sequential) | (caption ~line 402) |
| `images/fd-exercise2-open-write.svg` | Figure 1-7: GE 3 Part F (open write overwrite) | (caption ~line 427) |
| `images/fd-exercise2-fork-write.svg` | Figure 1-8: GE 3 Part G (fork write across processes) | (caption ~line 457) |
| `images/fd-exercise3-status-flags-sharing.svg` | Figure 1-9: GE 4 (status flags shared via OFD) | (caption ~line 545) |
| `images/fd-exercise4-lseek-cross-process.svg` | Figure 1-10: GE 5 (`lseek` across processes) | (caption ~line 623) |
| `images/fd-epoll-architecture.svg` | Figure 1-11: epoll architecture (Interest List, Ready List, Kernel Callback) | (caption ~line 823) |
| `images/fd-select-poll-vs-epoll.svg` | Figure 1-12: comparison of `select()` / `poll()` / `epoll` | (caption ~line 839) |
| `images/fd-fork-exec-cloexec.svg` | Figure 1-13: `fork()` + `exec()` on FD table, CLOEXEC | (caption ~line 1017) |
| `images/fd-leak-and-cloexec.svg` | Figure 1-14: FD leak comparison (with/without CLOEXEC) | (caption ~line 1023) |

> **Tier 5 rule (document-design Rule 8):** when editing SVG, MUST read and update caption in the SAME batch. Do NOT commit an SVG without caption verification. Run `svg-caption-consistency.py` before commit.

> **Lesson learned (2026-03-30):** `fd-kernel-3-table-model.svg` was rewritten from a combined diagram to pure TLPI model, but the caption still described `fork()` and `socket:443`. Cause: Tier 5 did not exist at the time; cross-file sync check missed it entirely.

---

## Specific sync rules

### When changing version references (HAProxy, Ubuntu)

Must check ALL of:

1. `README.md` (root), HAProxy section.
2. `haproxy-onboard/README.md`, TOC descriptions + Appendix A (Version Evolution Tracker).
3. EVERY Part file already written, inline version annotations (`> **Version note:**`).

**Lesson learned (2026-03-29):** edited `haproxy-onboard/README.md` from HAProxy 3.2 to 2.0, but FORGOT `README.md` (root) which still said "HAProxy 3.2". Caught by professor-style review, fixed in commit `3535f14`.

### When adding a new Part

1. Create file: `haproxy-onboard/X.0 - <name>.md` or `sdn-onboard/X.Y - <name>.md`.
2. Update `<series>/README.md`: TOC entry + Mermaid dependency graph + reading path.
3. Update `memory/<series>-state.md`: add new row.
4. Update `memory/file-dependency-map.md` (this file): add new entry.
5. If version-specific content: update Appendix A in `<series>/README.md`.

### When editing a Mermaid dependency graph

1. Edit graph in `<series>/README.md`.
2. Update reading path description (same file, just below graph).
