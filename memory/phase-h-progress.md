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
| Rule 6 Quality Gate Checklist C | PASS | fact-check, URL, file integrity, prose, em-dash all PASS |

## Rollout plan (S39 → S50)

- [x] **S39** — H.2.2 Expand Part 9.11 ovs-appctl reference 215 → 1170 dòng (+955) DONE 2026-04-24. 18 nhóm target × Anatomy block (introspection/vlog/memory/coverage/bridge/FDB/mdb/bond/LACP/STP/RSTP/BFD/CFM/OpenFlow/datapath/DPDK/tunnel/upcall/revalidator/cluster) + decision matrix + guided exercise coverage delta.
- [x] **S40** — H.2.3 Part 9.2 kernel datapath deep-dive DONE 2026-04-24. 529 → 878 dòng (+349, vượt target 75%). 5 section mới: §9.2.8 EMC anatomy, §9.2.9 SMC tier OVS 2.15+, §9.2.10 Upcall Netlink genl wire format, §9.2.11 Ukey state machine + revalidator RCU, §9.2.12 Tóm tắt 3-tier cache + checklist sức khỏe. Rename §9.2.6 dup → §9.2.13.
- [x] **S41** — H.3 Match Fields DONE 2026-04-24. Tạo mới Part 4.8 `openflow-match-field-catalog.md` (926 dòng) với 12 nhóm field × Template B: Metadata (6 field) + Register (16+8+4 reg/xreg/xxreg) + L2 (9 field) + ARP (5) + IPv4 (6) + IPv6 (7) + L4 TCP/UDP/SCTP (8) + ICMP (4) + Tunnel (6) + Conntrack (9) + MPLS+ip_frag (5). Prerequisite chain table + lazy wildcarding thực nghiệm. README Block IV updated 8→9 file.
- [x] **S42** — H.4.1 Actions output+control DONE 2026-04-24. Tạo mới Part 4.9 `openflow-action-catalog.md` (762 dòng, tier 1). Category 1 Output (9 action) + group (4 types) + control actions (resubmit, clone, note) + Action Set 12-priority execution order + action vs instruction foundation. Template C applied first time. Tier 2 + Tier 3 sẽ expand ở S43 + S44.
- [ ] **S43** — H.4.2 Actions field+encap: set_field/dec_ttl/push_pop/mod_*, Template C.
- [ ] **S44** — H.4.3 Actions advanced: ct/learn/note/conjunction/multipath/bundle/resubmit/group, Template C.
- [ ] **S45** — H.5 OVS internals: 9.1 + 9.15 + 9.16 classifier/subtable/staged/TSS/connmgr.
- [ ] **S46** — H.6.1 OVN LS pipeline: 13.2 with ls_in_* 27 stage + ls_out_* 10 stage, Template D.
- [ ] **S47** — H.6.2 OVN LR pipeline: 13.11 with lr_in_* 19 stage + lr_out_* 7 stage, Template D.
- [ ] **S48** — H.6.3 OVN schema: 13.1 + 13.10 NB 13 table + SB 10 table deep dive.
- [ ] **S49** — H.7 Conntrack: 9.24 + 13.3 ct_nat/ct_commit/ct_alg/ct_mark/ct_label deep dive.
- [ ] **S50** — H.8 Missing tools + final quality gate: ovs-bugtool + ovs-pcap + Rule 11/13/14 sweep full 109 file.

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
