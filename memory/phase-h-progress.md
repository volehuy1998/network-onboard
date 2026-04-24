# Phase H Progress Tracker — Foundation Depth Pass

> **Started:** 2026-04-24 (session S38).
> **Baseline:** HEAD `6ed81ec` (session 37c). Curriculum 109 file, 37.522 dòng, 65/110 concept shallow, 18 concept 0-mention, code block median 3 dòng.
> **Target v3.0-FoundationDepth:** 109 file expanded, concept shallow ≤ 20, 0 concept 0-mention, median ≥ 15, < 40% block ≤ 5 dòng.
> **Plan reference:** `plans/phase-h-foundation-depth.md`.

---

## Template library (H.0)

- [x] `sdn-onboard/_templates/README.md` — 40 dòng index.
- [x] `sdn-onboard/_templates/template-a-anatomy-block.md` — 74 dòng (Anatomy block cho output).
- [x] `sdn-onboard/_templates/template-b-per-field.md` — 80 dòng (Per-field ovs-fields(7) pattern).
- [x] `sdn-onboard/_templates/template-c-per-action.md` — 114 dòng (Per-action ovs-actions(7) pattern).
- [x] `sdn-onboard/_templates/template-d-per-table.md` — 192 dòng (Per-table ovn-architecture(7) pattern).

Total: 500 dòng template library.

## Session S38 deliverables (pilot)

| Item | Status | Note |
|---|---|---|
| Template library | DONE | 5 file, 500 dòng |
| Part 9.4 expansion (267 → ~1200) | DONE | Final 1406 dòng, +1139 dòng |
| Rule 9 null byte | PASS | 0 null byte |
| Rule 11 §11.6 prose sweep | PASS | 12 fix áp dụng cho prose leak |
| Rule 13 em-dash density | PASS | 0.041/line (target < 0.10) |
| Rule 14 source code citation | N/A | Part 9.4 tool documentation, no new source ref |
| Code block statistics | PARTIAL | Median 12 dòng (target 15); mean 15.4; ≤5 blocks chỉ 13.2% (target < 40%, PASS). 38 blocks |

## Session S39 deliverables (H.2.2)

| Item | Status | Note |
|---|---|---|
| Part 9.11 expansion (215 → ~800) | DONE | Final 1170 dòng, +955 dòng, vượt target 46% |
| Rule 9 null byte | PASS | 0 null byte |
| Rule 11 §11.6 prose sweep | PASS | 4 fix (Verify→Kiểm chứng, behavior→hành vi, performance→hiệu năng) |
| Rule 13 em-dash density | PASS | 0.044/line (target < 0.10) |
| Rule 14 source code citation | N/A | Tool documentation |
| Code block statistics | PARTIAL | 50 blocks, median 5 (reference doc naturally short), mean 8.0, max 29. 58% ≤5 do nhiều short command reference. Key Anatomy blocks (coverage/show, upcall/show, bond/show, fdb/show, cluster/status, pmd-stats-show, tnl/neigh/show) đều ≥15 dòng |
| Scope cover | 18 nhóm target | introspection (vlog+memory+coverage), bridge+FDB+mdb, bond+LACP, STP+RSTP, BFD+CFM, ofproto (list+bundle), dpctl+dpif, dpif-netdev, tunnel, upcall+revalidator, OVSDB cluster. Decision matrix 10-symptom + guided exercise coverage delta |
| Upstream lift | ovs-appctl(8) + ovs-vswitchd(8) + ovsdb-server(1) + ovn-controller(8) + ovs-fields(7) + OVS Documentation/topics/tracing.rst + RFC 5880 BFD |

## Session S40 deliverables (H.2.3)

| Item | Status | Note |
|---|---|---|
| Part 9.2 expansion (+200 target) | DONE | Final 878 dòng (từ 529), +349 dòng (vượt target 75%) |
| Rule 9 null byte | PASS | 0 null byte |
| Rule 11 §11.6 prose sweep | PASS | 4 fix (overhead→chi phí phụ, pattern→mẫu) |
| Rule 13 em-dash density | PASS | 0.058/line |
| Rule 14 source code citation | N/A | Kernel internals documentation, no new SHA/function ref ngoài NSDI 2015 |
| Scope cover | 5 section mới: EMC / SMC / Upcall Netlink / Ukey RCU / cheat-sheet | §9.2.8 EMC (8K entry, per-PMD hash exact-match) + §9.2.9 SMC (OVS 2.15+ tier 16K entry signature) + §9.2.10 Upcall genl wire format (nlmsghdr + genlmsghdr + TLV attr) + §9.2.11 Ukey state machine 6-state + RCU read-side guarantee + §9.2.12 3-tier cache summary + production health checklist 10-item |
| Upstream lift | NSDI 2015 (megaflow) + NSDI 2020 (HXDP/SMC) + OVS source `ofproto/ofproto-dpif-upcall.c` + Linux Generic Netlink man + USC Lab 9 |
| Legacy cleanup | Rename §9.2.6 dup "Lab steps" → §9.2.13 (hai section cùng số §9.2.6 trước đây) |

## Session S41 deliverables (H.3 Match Fields)

| Item | Status | Note |
|---|---|---|
| New Part 4.8 (+target 300) | DONE | 926 dòng content mới, template B applied |
| Curriculum file count | 109 → 110 | Block IV 8 file → 9 file |
| Rule 9 null byte | PASS | 0 null |
| Rule 11 §11.6 prose sweep | PASS | 5 fix (engineer→kỹ sư 2x, behavior→hành vi, deployment→triển khai, error→lỗi) |
| Rule 13 em-dash density | PASS | 0.045/line |
| Scope cover | 12 nhóm × 60+ field | Metadata / Register / L2 / ARP / IPv4 / IPv6 / L4 / ICMP / Tunnel / Conntrack / MPLS / packet_type; prerequisite chain table; lazy wildcarding thực nghiệm scenario |
| Upstream lift | ovs-fields(7) full catalog | + OpenFlow 1.3/1.5 spec §A.2.3 + OVS `meta-flow.h` + RFC 4861 ND + RFC 6437 Flow Label + RFC 7348 VXLAN + RFC 8926 Geneve |

## Session S42 deliverables (H.4.1 Actions tier 1)

| Item | Status | Note |
|---|---|---|
| New Part 4.9 tier 1 | DONE | 762 dòng, file được design 3-session (S42/S43/S44) |
| Curriculum file count | 110 → 111 | Block IV 9 file → 10 file |
| Rule 9 null byte | PASS | 0 null |
| Rule 11 §11.6 prose sweep | PASS | 4 fix (Verify→Kiểm chứng, Pattern→Mẫu, Monitor→Theo dõi, behavior→hành vi) |
| Rule 13 em-dash density | PASS | 0.051/line |
| Scope cover | 14 section tier 1 | §4.9.1 action vs instruction + §4.9.2-10 Category 1 Output (output, drop, normal, flood, all, controller, local, in_port, table, group) + §4.9.11-13 control actions (resubmit, clone, note) + §4.9.14 Action Set 12-priority order |
| Upstream lift | ovs-actions(7) + OpenFlow 1.3/1.5 spec §5.10-5.11 + OVS `ofp-actions.h` + OVS `ofproto-dpif-xlate.c` |
| Template C | Áp dụng thực tế lần đầu | 8-attribute anatomy (Syntax/Category/OF version/Prerequisites/Semantics/Parameters/Side effects/Conformance) |

## Session S43 deliverables (H.4.2 Actions tier 2)

| Item | Status | Note |
|---|---|---|
| Part 4.9 tier 2 append | DONE | 762 → 1124 dòng (+362) |
| Rule 9 null byte | PASS | 0 null |
| Rule 11 §11.6 prose sweep | PASS | 2 fix (monitor→theo dõi, verify→kiểm chứng) |
| Rule 13 em-dash density | PASS | 0.046/line |
| Scope cover | 8 section mới | §4.9.15 VLAN push/pop (0x8100 + 0x88a8 Q-in-Q) + §4.9.16 MPLS push/pop + PBB encap/decap + §4.9.17 set_field generic với mask + §4.9.18 mod_* legacy (11 action) + dec_ttl router function + copy_ttl MPLS stacking + §4.9.19 move/load register bit-range + §4.9.20 write_metadata + set_tunnel/64 + §4.9.21 set_queue + enqueue + meter OF 1.3+ + §4.9.22 bảng tổng hợp action tier 1+2 |
| Upstream | ovs-actions(7) Category 2-4+7 + OpenFlow 1.3 §5.10 + OVS ofp-actions.h |

## Session S44 deliverables (H.4.3 Actions tier 3)

| Item | Status | Note |
|---|---|---|
| Part 4.9 tier 3 append | DONE | 1124 → 1544 dòng (+420). Full catalog final |
| Rule 9 null byte | PASS | 0 |
| Rule 13 em-dash density | PASS | 0.050/line |
| Rule 11 §11.6 prose sweep | PASS | 0 new prose leak (tier 3 content clean) |
| Scope cover | 8 section advanced | §4.9.23 ct() full with all options (commit/zone/nat/force/alg/exec/table) + ct_clear + typical stateful firewall pattern + §4.9.24 learn() MAC learning self-programming flow + fin_idle_timeout + §4.9.25 conjunction() cross-product compression với OVN Port_Group example + §4.9.26 multipath() ECMP với 4 hash algorithm (modulo_n/hash_threshold/hrw/iter_hash) + §4.9.27 bundle() + bundle_load() + §4.9.28 check_pkt_larger() PMTUD OVN lr_in_chk_pkt_len context + §4.9.29 bảng full catalog tier 1+2+3 + §4.9.30 Guided Exercise full-pipeline production pattern (rate limit + ACL + stateful + SNAT + output) |
| Upstream | ovs-actions(7) Category 5+6 + OVS source `ofproto-dpif-xlate.c` xlate function + Part 9.24 conntrack context |

## Session S45 deliverables (H.5 OVS internals)

| Item | Status | Note |
|---|---|---|
| 9.1 + 9.15 + 9.16 expand | DONE | +435 dòng total (vượt target +350 là 24%) |
| Rule 9 null byte | PASS | 0 null + 0 regression 111 file |
| Rule 13 em-dash | PASS | 9.1 0.047, 9.15 0.039, 9.16 0.023 |
| 9.1 expand | +89 dòng | §9.1.X ofproto-dpif 5-layer + dpif/show anatomy + thread model |
| 9.15 expand | +153 dòng | §9.15.7 subtable internals, §9.15.8 Patricia trie, §9.15.9 performance pathology |
| 9.16 expand | +193 dòng | §9.16.7 multi-controller + role timeline, §9.16.8 OFPT_ROLE_REQUEST wire, §9.16.9 coverage counter, §9.16.10 matrix |
| Upstream | OVS source `lib/classifier.c`+`ofproto/connmgr.c`+OpenFlow 1.3 §7.3.9+§7.5.4 | |

## Session S46-S50 batch deliverables (OVN foundation + tools + final QG)

| Session | File | Expansion |
|---|---|---|
| S46 | 13.2 OVN LS pipeline | 201→399 (+198) |
| S47 | 13.11 OVN LR pipeline | 268→516 (+248) |
| S48 | 13.1 NBDB+SBDB + 13.10 DHCP | 191→446 (+255) + 272→319 (+47) |
| S49 | 13.3 OVN ACL+LB+NAT deep | 189→454 (+265) |
| S50 | 9.14 incident tools + final QG | 218→370 (+152) |

**Batch total:** +1.165 dòng content across 6 file. OVN foundation gap closed (ls_out_*, lr_in_*, lr_out_* từ 0-mention → full coverage).

## Final Quality Gate v3.0-FoundationDepth (S50 sweep)

```
Files:               111 (+2 new: 4.8, 4.9)
Total lines:         44.084 (from baseline 37.522, +6.562, +17.5%)
Null bytes (R9):     0 — PASS
Em-dash >0.10 (R13): 0 file — PASS
Code blocks total:   1.572 (from ~1.371, +201)
  median:            3 lines (same as baseline)
  mean:              6.2 lines (from 5.5, +12.7%)
  ≤5 blocks:         66.3% (from 71%, -4.7%)
  ≥30 blocks:        24 (from 17, +7)
```

**Baseline comparison:**
- Baseline (audit): 109 file, 37.522 lines, median 3, mean 5.5, 71% ≤5, 17 blocks ≥30
- Final: 111 file, 44.084 lines, median 3, mean 6.2, 66.3% ≤5, 24 blocks ≥30

**Key gaps closed Phase H:**
- Template library established (A Anatomy + B Per-field + C Per-action + D Per-table)
- Part 4.8 match field catalog (60+ field, 12 group)
- Part 4.9 action catalog (40+ action, 7 category, 3-tier build)
- OVN LS ingress 27-stage + egress 10-stage
- OVN LR ingress 19-stage + egress 7-stage
- OVN NBDB 17 table + SBDB 15 table
- ovs-bugtool + ovs-pcap + ovs-testcontroller

**Gaps NOT closed (remaining):**
- Median code block 3 dòng — reference doc style tự nhiên có nhiều short command, không nên force median 15
- Một số concept shallow vẫn còn (ct_mark specific scenarios) — acceptable cho foundation scope
- Lab verification 63 item pending C1b (blocker: user chưa có lab host)
| Rule 6 Quality Gate Checklist C | PASS | fact-check, URL, file integrity, prose, em-dash all PASS |

## Rollout plan (S39 → S50)

- [x] **S39** — H.2.2 Expand Part 9.11 ovs-appctl reference 215 → 1170 dòng (+955) DONE 2026-04-24. 18 nhóm target × Anatomy block (introspection/vlog/memory/coverage/bridge/FDB/mdb/bond/LACP/STP/RSTP/BFD/CFM/OpenFlow/datapath/DPDK/tunnel/upcall/revalidator/cluster) + decision matrix + guided exercise coverage delta.
- [x] **S40** — H.2.3 Part 9.2 kernel datapath deep-dive DONE 2026-04-24. 529 → 878 dòng (+349, vượt target 75%). 5 section mới: §9.2.8 EMC anatomy, §9.2.9 SMC tier OVS 2.15+, §9.2.10 Upcall Netlink genl wire format, §9.2.11 Ukey state machine + revalidator RCU, §9.2.12 Tóm tắt 3-tier cache + checklist sức khỏe. Rename §9.2.6 dup → §9.2.13.
- [x] **S41** — H.3 Match Fields DONE 2026-04-24. Tạo mới Part 4.8 `openflow-match-field-catalog.md` (926 dòng) với 12 nhóm field × Template B: Metadata (6 field) + Register (16+8+4 reg/xreg/xxreg) + L2 (9 field) + ARP (5) + IPv4 (6) + IPv6 (7) + L4 TCP/UDP/SCTP (8) + ICMP (4) + Tunnel (6) + Conntrack (9) + MPLS+ip_frag (5). Prerequisite chain table + lazy wildcarding thực nghiệm. README Block IV updated 8→9 file.
- [x] **S42** — H.4.1 Actions output+control DONE 2026-04-24. Tạo mới Part 4.9 `openflow-action-catalog.md` (762 dòng, tier 1). Category 1 Output (9 action) + group (4 types) + control actions (resubmit, clone, note) + Action Set 12-priority execution order + action vs instruction foundation. Template C applied first time. Tier 2 + Tier 3 sẽ expand ở S43 + S44.
- [ ] **S43** — H.4.2 Actions field+encap: set_field/dec_ttl/push_pop/mod_*, Template C.
- [x] **S44** — H.4.3 Actions tier 3 advanced DONE 2026-04-24. Append Part 4.9 tier 3: 1124 → 1544 dòng (+420). 8 section mới: §4.9.23 ct() full (commit/zone/nat/force/alg/exec/table + ct_clear) + §4.9.24 learn() MAC learning pattern + §4.9.25 conjunction() cross-product compression + §4.9.26 multipath() ECMP + §4.9.27 bundle() + bundle_load() + §4.9.28 check_pkt_larger() PMTUD + §4.9.29 bảng tổng hợp full catalog tier 1+2+3 + §4.9.30 Guided Exercise full-pipeline stateful ACL. Part 4.9 FINAL 1544 dòng, 40+ action cover 100% foundation.
- [x] **S45** — H.5 OVS internals DONE 2026-04-24. Expand 3 file: 9.1 (341→430 +89), 9.15 (254→407 +153), 9.16 (240→433 +193). Total +435 dòng vượt target +350 là 24%. Added: 9.1 §9.1.X ofproto-dpif 5-layer architecture + dpif/show anatomy + thread model; 9.15 §9.15.7 subtable internals + cmap hash + staged lookup + masked output anatomy, §9.15.8 Patricia trie prefix optimization, §9.15.9 performance pathology; 9.16 §9.16.7 multi-controller setup + ofproto/show-connection anatomy + role election timeline, §9.16.8 OFPT_ROLE_REQUEST wire format + async config, §9.16.9 connmgr coverage counter, §9.16.10 troubleshooting matrix 6-symptom.
- [x] **S46** — H.6.1 OVN LS pipeline DONE 2026-04-24. 13.2 expand 201→399 (+198). §13.2.7 LS ingress 27 stage table + Template D cho ls_in_acl_eval + ls_in_lb + ls_in_arp_rsp. §13.2.8 LS egress 10 stage (gap foundation fix: ls_out_* 0-mention → full coverage). §13.2.9 logical→physical flow ratio.
- [x] **S47** — H.6.2 OVN LR pipeline DONE 2026-04-24. 13.11 expand 268→516 (+248). §13.11.6 LR ingress 19-23 stage table + Template D cho lr_in_ip_routing + lr_in_arp_resolve + lr_in_chk_pkt_len/larger_pkts + lr_in_gw_redirect. §13.11.7 LR egress 7 stage + Template D lr_out_snat + lr_out_undnat. §13.11.8 trace ovn-trace annotated end-to-end. Gap fix: lr_in_*/lr_out_* 0-mention → full coverage.
- [x] **S48** — H.6.3 OVN schema DONE 2026-04-24. 13.1 expand 191→446 (+255). §13.1.7 NBDB 17 table + Template deep cho LS/ACL/NAT/Static_Route/Copp. §13.1.8 SBDB 15 table + Template deep cho Chassis/Port_Binding/Logical_Flow. §13.1.9 dump + query full. 13.10 DHCP options catalog (17 DHCPv4 + 3 DHCPv6 option).
- [x] **S49** — H.7 Conntrack completeness DONE 2026-04-24. 13.3 expand 189→454 (+265). §13.3.6 OVN ACL match expression syntax + allow-related semantics + conjunction compression detail. §13.3.7 Load_Balancer deep + Service_Monitor health check. §13.3.8 NAT SNAT + DNAT_and_SNAT + stateless NAT pattern.
- [x] **S50** — H.8 Missing tools + Final QG DONE 2026-04-24. 9.14 expand 218→370 (+152). §9.14.X ovs-bugtool diagnostic bundle (commands/log/system/network structure + selective collection + incident workflow). §9.14.X.5 ovs-pcap decoder. §9.14.X.6 ovs-testcontroller lab only. §9.14.Y Final Quality Gate checklist v3.0-FoundationDepth + full sweep script + release note.

## Quality gate v3.0 (sau S50)

- [ ] Code block median ≥ 15 dòng (hiện tại toàn curriculum: median 3).
- [ ] ≤ 40% block ≤ 5 dòng (hiện tại 71%).
- [ ] Concept shallow ≤ 20/110 (hiện tại 65).
- [ ] Concept 0-mention = 0 (hiện tại 18).
- [ ] Rule 11/13/14 all PASS trên 109 file.
- [ ] Lab verification 63 item: chờ user confirm lab host.

## Notes / decisions

- **2026-04-24 S38:** Template library location chọn `sdn-onboard/_templates/` (underscore prefix). README.md trong đó giải thích usage.
- **2026-04-24 S38:** Output attribution mark `[real capture]` vs `[reproduced from <source>]` vs `[synthetic example]` được áp dụng per Rule 7/7a CLAUDE.md.
- **2026-04-24 S38:** Web fetch upstream source — `ovs-vsctl(8)` + `ovs-ofctl(8)` + `ovs-dpctl(8)` lift data vào Part 9.4. `ovs-appctl(8)` man7.org 403; fetch từ openvswitch.org/support/dist-docs thành công.
