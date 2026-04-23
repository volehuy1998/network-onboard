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
| Rule 6 Quality Gate Checklist C | PASS | fact-check, URL, file integrity, prose, em-dash all PASS |

## Rollout plan (S39 → S50)

- [ ] **S39** — H.2.2 Expand Part 9.11 ovs-appctl reference (215 → ~800). 20+ appctl target × Anatomy block.
- [ ] **S40** — H.2.3 Part 9.2 kernel datapath deep-dive (+200 dòng SMC, EMC, upcall, revalidator, ukey).
- [ ] **S41** — H.3 Match Fields: 4.1 + expand với IPv6/ARP/ICMP/MPLS/tun/conj_id/pkt_mark, Template B.
- [ ] **S42** — H.4.1 Actions output+control: output/drop/flood/all/controller/local/in_port/table/normal, Template C.
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
