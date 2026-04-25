# Plan v3.5-KeywordBackbone — Foundation Backbone qua Keyword Reference

> **Trạng thái:** Draft v2 2026-04-25, chờ user confirm khung sườn để chuyển qua execute.
> **Tạo:** 2026-04-25 sau khi user thêm `sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md` (REF, 2617 dòng).
> **Owner:** VO LE.
> **Mandate user verbatim:** *"kiến thức nền tảng phải vững chải, am hiểu mọi công cụ và cách sử dụng chúng thông qua các keyword cú pháp, keyword về thuật ngữ được nêu trong khái niệm, kiến trúc."*
> **Source-of-truth:** `sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md`.
> **Baseline curriculum:** v3.4-DeepFoundation, 119 file, ~63K dòng, verdict A.
> **Mục tiêu plan:** đưa curriculum lên **v3.5-KeywordBackbone**: mỗi keyword in-scope của REF có 5-axis classification (Bucket | Context | Purpose | Activity | Mechanism), cross-link qua master index.

> **Ghi chú quan trọng:** Plan này định nghĩa **khung sườn** (mục lục + mục đích) cho từng file mới + EXPAND. **Content writing** (5-axis depth + Anatomy + GE + POE) sẽ thực hiện trong từng phase, mỗi commit độc lập. KHÔNG viết content tổng thể trong 1 commit. Plan KHÔNG phải là content; plan là roadmap để build content.

---

## -2. Progress Tracker (LIVE — cập nhật mỗi khi hoàn thành phase lớn)

> **Cập nhật cuối:** 2026-04-25 sau J.5.e commit `e4b7d2d`. PR #51: 44 commits, ~14K+ additions cumulative.

### Phase status (14 phases tổng)

| # | Phase | Status | Commit | Lines added | Note |
|---|-------|--------|--------|-------------|------|
| 1 | J.1 Audit (inventory + matrix + priority) | ✅ DONE | `af29ae3` | +1351 | 250 work items mapped, 3 memory file + 3 Python script |
| 2 | J.5.c.i 13.17 register + REGBIT + MLF | ✅ DONE | `12f62ce` | +516 | NEW. Foundation cho 13.16. branch-22.03 verified |
| 3 | J.5.c.ii 13.16 pipeline table IDs | ✅ DONE | `6b54484` | +579 | NEW. **CRITICAL gap closure** (0/63 stages) |
| 4 | J.3 NEW (9.28-9.31) | ✅ DONE | `63fb8db` | +1287 | 4 NEW utility files: ovs-pcap/tcpundump, vtep-ctl, ovs-pki, ovsdb-tool |
| 5 | J.4.c (3.3 OF messages + 3.4 version diff) | ✅ DONE | `2feaa60` | +979 | 2 NEW Block III files |
| 6 | J.4.a + J.4.b (4.8 + 4.9 expand) | ✅ DONE | `a470b28` | +526 | 12 missing match field + 12 missing action |
| 7 | J.5.a 13.15 OVN Inter-Connect | ✅ DONE | `0a35079` | +621 | NEW. Closes forward-ref `9.31 → 13.15` |
| 8 | J.5.d 13.14 expand (options + ovn-trace + ovn-detrace) | ✅ DONE | `327ce65` | +337 | 30+ ovn-nbctl options + microflow expression syntax |
| 9 | J.5.e 20.2 lflow-cache tunables | ✅ DONE | `e4b7d2d` | +104 | 5 external_ids tunable Anatomy |
| — | J.3 EXPAND (9.4 + 9.11 + 9.27) | ⏸ DEFERRED | — | — | Marginal value low; existing files đã comprehensive (1406+1170+696 dòng); J.5.d đã làm pattern tương tự cho 13.14 |
| 10 | J.5.b 13.x schema completeness | ⏳ TODO | — | est ~200 | 50+ NB/SB column 5-axis Anatomy backfill |
| 11 | J.6 Distributed troubleshoot scenarios | ⏳ TODO | — | est ~1300 | 12 scenario × ~100 dòng across 12 file native |
| 12 | J.2 Master index 0.3 (LAST per max-quality) | ⏳ TODO | — | est ~3000 | Vietnamese DEEP adaptation của REF, build với knowledge gained |
| 13 | J.7 Validation + Release v3.5 | ⏳ TODO | — | est ~50 | Re-grep matrix, spot-check, tag + GitHub Release |

### Cumulative metrics

| Metric | Value |
|--------|-------|
| Phases done | 9/14 (64%) |
| Phases active todo | 4 (J.5.b + J.6 + J.2 + J.7) |
| Phase deferred | 1 (J.3 EXPAND) |
| Files NEW | 9 (13.17, 13.16, 9.28, 9.29, 9.30, 9.31, 3.3, 3.4, 13.15) |
| Files EXPAND | 4 (4.8, 4.9, 13.14, 20.2) |
| Lines added (curriculum) | ~6900 |
| Lines added (plan + REF + memory + scripts) | ~3400 |
| Total session content | ~10,300 dòng |
| Quality gates pass rate | 100% (Rule 9, 11, 13, 14) |
| Forward-ref broken | 0 (closed by J.5.a) |

### Gap matrix improvement (verified)

| Tier | Trước session | Sau session | Δ |
|------|---------------|-------------|---|
| A MISSING | 197 | 184 | -13 |
| B SHALLOW | 53 | 60 | +7 (some moved up từ MISSING) |
| C-OK BREADTH | 51 | 50 | -1 |
| C-DEEP WIDE | 82 | 89 | +7 |

### Decisions made trong execution

| Decision | Rationale | Phase |
|----------|-----------|-------|
| J.5.c trước J.5.a | Pipeline IDs là foundation, register cần biết trước IC | J.5 ordering |
| J.4.c trước J.4.a/b | NEW file (3.3 + 3.4) trước EXPAND (4.8 + 4.9) cho lower regression risk | J.4 ordering |
| J.3 EXPAND DEFERRED | Existing 9.4/9.11/9.27 đã comprehensive; J.5.d covered similar pattern cho 13.14 | J.3 ordering |
| 13.15 cite BAN BGP | Per North Star, chỉ static route, không expand `ovn-bgp-agent` | J.5.a |
| File 13.17 fix REF version drift | REF mô tả 24.03+, baseline 22.03.8 có REGBIT layout khác | J.5.c.i |
| Pipeline 63 stages (không phải 64) | Verified `northd/northd.c` PIPELINE_STAGES count | J.5.c.ii |

---

## -1. Changelog plan

| Version | Date | Change |
|---------|------|--------|
| v1 (draft) | 2026-04-25 (chiều) | Initial draft, 489 dòng, 13 section. Đề xuất 1 file 20.8 dedicated bundling 14 scenarios. |
| v2 | 2026-04-25 (tối) | Rewrite sau user feedback Q1-Q5: (1) Q2 REVERSED (no bundling, distribute 14 scenario vào 13 file native), (2) Q3 deep mode 0.3 ~3000 dòng, (3) Q4 OVN 22.03.8 baseline + version note, (4) Q5 sequencing J.3→J.4→J.5 (J.5.c trước trong J.5). Thêm Section 5 detailed mục lục cho 10 NEW file + Section 6 detailed sections cho 10 EXPAND file + Section 7 distributed scenario mapping. Tổng 1337 dòng. |
| v2.1 (current) | 2026-04-25 (tối, sau session execute) | Thêm Section -2 Progress Tracker LIVE. Document execution decisions: J.3 EXPAND deferred per redundancy, J.5.c trước J.5.a per foundation principle, J.4.c trước J.4.a/b per NEW-before-EXPAND. 9/14 phase done, 4 active todo + 1 deferred. |

---

## 0. Decision log (sau Q&A 2026-04-25)

| # | Question | Quyết định | Note |
|---|----------|-----------|------|
| Q1 | DPDK/PMD/SMC/EMC/mempool keyword skip 5-axis? | **YES** (skip) | PERMANENT BAN từ North Star, mark "Out of scope" trong master index 0.3 |
| Q2 | 14 troubleshooting scenarios bundle vào 1 file 20.8? | **NO** (distribute) | User reject bundling. Mỗi scenario distribute vào file native technology + nhận full Forensic Anatomy depth (~80–100 dòng/scenario). |
| Q3 | Master index 0.3 lookup-only (~1800) hay deep (~3000)? | **DEEP** (~3000) | User: "không quan tâm thời gian + chi phí, chỉ quan tâm chất lượng". |
| Q4 | Pipeline table IDs version anchor: 22.03.8 hay multi-version? | **22.03.8 baseline + version note callout** | Nhất quán state tracker. Multi-version sẽ noise hóa file. Version drift annotate per Rule 14. |
| Q5 | Sequencing: J.5 trước hay tuần tự J.3→J.4→J.5? | **Tuần tự ưu tiên depth-first per understanding** | J.3 OVS familiar → J.4 OpenFlow well-doc → J.5 OVN khó nhất. Trong J.5: 13.16 pipeline IDs làm TRƯỚC vì underpins 13.x khác. |

---

## 1. Nguyên tắc chỉ đạo

1. **REF là backbone tuyệt đối.** Không tự thêm topic ngoài REF trừ khi user yêu cầu cụ thể.
2. **5-axis là chuẩn duy nhất.** Mỗi keyword in-scope có treatment dạng `Bucket | Context | Purpose | Activity | Mechanism` ở ÍT NHẤT một file curriculum, kèm Example + Source citation theo Rule 14.
3. **PERMANENT BAN giữ nguyên.** Skip DPDK/PMD/SMC/EMC/mempool 5-axis. Existing 9.3 + 16.x stay as-is.
4. **No bundling.** Không gom nhiều scenario/topic vào 1 file consolidated. Distribute vào file native technology (per feedback `feedback_no_bundling.md`).
5. **Khung sườn trước, content sau.** Plan này định nghĩa mục lục + mục đích chi tiết. Content viết sau khi user confirm khung sườn.
6. **Vietnamese prose discipline (Rule 11).** Keyword tên giữ English. Prose Vietnamese. Bold label section heading Vietnamese.
7. **Verify, never estimate (Rule 14 + Second North Star).** Mọi commit SHA / function name / table column verified qua MCP GitHub.
8. **Single sub-task per commit.** Mỗi keyword group hoặc mỗi file = 1 commit độc lập, reviewable in isolation.
9. **Quality > Speed.** Effort không giới hạn, miễn quality đạt.

---

## 2. Inventory REF (verified counts từ grep)

REF cấu trúc 5 section, tổng **~325 keyword entries + 14 troubleshooting playbook + 1 source index**.

| Section | Lines | Subsection | Số entry | In-scope | BANNED |
|---------|-------|------------|----------|----------|--------|
| 1. OVS | 11–388 | 1.1 Architecture & daemons | 5 | 5 | 0 |
|        |       | 1.2 Datapath & forwarding internals | ~30 | ~25 | ~5 (DPDK datapath, EMC, SMC, PMD, mempool) |
|        |       | 1.3 OVSDB | ~15 | 15 | 0 |
|        |       | 1.4 CLI tools & every option | ~10 tools, 100+ flag/subcommand | tất cả non-DPDK | 0 |
|        |       | 1.5 Observability | ~15 | ~10 | ~5 (dpif-netdev/pmd-*, netdev-dpdk/get-mempool-info) |
| 2. OpenFlow | 391–1290 | 2.1 Pipeline model | ~10 | 10 | 0 |
|             |          | 2.2 Match fields | 60+ | 60+ | 0 |
|             |          | 2.2 Actions | 40+ | 40+ | 0 |
|             |          | 2.2 Instructions | 6 | 6 | 0 |
|             |          | 2.3 Messages & state machine | 16 OFPT_* + 4-state SM + AUX | tất cả | 0 |
|             |          | 2.4 Version differences | 8 features | 8 | 0 |
| 3. OVN | 1293–2186 | 3.1 Architecture & daemons | ~17 | 17 | 0 |
|        |           | 3.2 NB schemas | ~25 tables/columns | 25 | 0 |
|        |           | 3.2 SB schemas | ~25 tables/columns | 25 | 0 |
|        |           | 3.3 Pipeline tables | 64 (28 LS_IN + 11 LS_OUT + 19 LR_IN + 6 LR_OUT) | 64 | 0 |
|        |           | 3.3 Register conventions + REGBIT + MLF | ~20 | 20 | 0 |
|        |           | 3.4 CLI tools | ovn-nbctl 100, ovn-sbctl 15, ovn-trace, ovn-detrace, ovn-ic-nbctl, ovn-appctl | tất cả | 0 |
|        |           | 3.5 Observability | ~25 | 25 | 0 |
| 4. Cross-cutting troubleshooting playbook | 2192–2614 | 14 production scenarios | 14 | 14 | 0 |
| 5. Source index | 2475–2557 | URL authoritative | ~40 URL | 40 | 0 |

**Total in-scope:** ~310 keyword entries + 14 scenarios + ~40 URL = **~365 items cần curriculum coverage**.
**BANNED:** ~10 entries (DPDK + PMD + EMC + SMC + mempool family).

---

## 3. Audit gap (verified bằng grep, sample 37 keyword)

### Group A: OVN pipeline table IDs

| Keyword | Files | Verdict |
|---------|-------|---------|
| `LS_IN_PORT_SEC_L2` | 0 | MISSING |
| `LS_IN_PRE_ACL` | 0 | MISSING |
| `LS_IN_ACL_HINT` | 0 | MISSING |
| `LS_IN_LB` | 0 | MISSING |
| `LS_IN_DHCP_OPTIONS` | 0 | MISSING |
| `LR_IN_ADMISSION` | 0 | MISSING |
| `LR_IN_IP_INPUT` | 0 | MISSING |
| `LR_IN_DNAT` | 0 | MISSING |
| `LR_IN_ARP_RESOLVE` | 0 | MISSING |
| `LR_OUT_SNAT` | 0 | MISSING |

**100% MISSING. CRITICAL gap.**

### Group B: OpenFlow match fields & extension keywords

| Keyword | Files | Verdict |
|---------|-------|---------|
| `in_phy_port` | 0 | MISSING |
| `ipv6_flabel` | 0 | MISSING |
| `ipv6_exthdr` | 1 | SHALLOW |
| `pbb_isid` | 0 | MISSING |
| `mpls_tc` | 2 | SHALLOW |
| `mpls_bos` | 3 | SHALLOW |
| `sctp_src` | 1 | SHALLOW |
| `tunnel_id` | 1 | SHALLOW |
| `xxreg0` | 2 | SHALLOW |
| `MLF_LOCAL_ONLY` | 0 | MISSING |
| `REGBIT_PORT_SEC_DROP` | 0 | MISSING |

**8/11 MISSING/SHALLOW.** 4.8 match field catalog có 60+ field nhưng chưa exhaustive.

### Group C: OpenFlow protocol messages

| Keyword | Files | Verdict |
|---------|-------|---------|
| `OFPT_HELLO` | 4 | LIKELY OK |
| `OFPT_FEATURES_REQUEST` | 3 | LIKELY OK |
| `OFPT_PACKET_IN` | 4 | LIKELY OK |
| `OFPT_BARRIER_REQUEST` | 1 | SHALLOW |
| `OFPT_ROLE_REQUEST` | 2 | SHALLOW |
| `OFPT_BUNDLE_OPEN` | 0 | MISSING |
| `OFPT_TABLE_STATUS` | 0 | MISSING |
| `OFPT_SET_ASYNC` | 2 | SHALLOW |
| `OFPT_REQUESTFORWARD` | 0 | MISSING |
| `OFPT_MULTIPART_REQUEST` | 0 | MISSING |

**5/10 MISSING/SHALLOW.** State machine 4-stage chưa có file dedicated.

### Group D: CLI tool minor utility

| Keyword | Files | Verdict |
|---------|-------|---------|
| `vtep-ctl` | 0 | MISSING |
| `ovs-pcap` | 1 | SHALLOW |
| `ovsdb-tool needs-conversion` | 0 | MISSING |
| `ovs-vsctl wait-until` | 1 | SHALLOW |
| `ovn-ic-northd` | 0 | MISSING |
| `ovn-ic-nbctl` | 0 | MISSING |

**5/6 MISSING/SHALLOW.**

### Tổng quan

37 keyword critical → **24/37 MISSING/SHALLOW (~65%)**. Extrapolate sang ~310 in-scope keyword: **~200 keyword cần work** (Tier A MISSING + Tier B SHALLOW upgrade).

---

## 4. Phase structure overview (J.1 → J.7)

| Phase | Goal | Output | Effort |
|-------|------|--------|--------|
| J.1 | Inventory + coverage matrix | 3 memory file (inventory, matrix, gap-priority) | 1–2 session |
| J.2 | Master index Vietnamese (DEEP) | NEW `0.3 - master-keyword-index.md` ~3000 dòng | 2 session |
| J.3 | OVS section backfill | 4 NEW + 5 EXPAND | 3 session |
| J.4 | OpenFlow section backfill | 2 NEW + 2 EXPAND | 3 session |
| J.5 | OVN section backfill (gap nhất) | 3 NEW + 4 EXPAND, 13.16 LÀM TRƯỚC | 4 session |
| J.6 | 14 troubleshoot scenarios distributed | EXPAND ~14 file (mỗi file +80-100 dòng) | 2 session |
| J.7 | Validate + Release | Tag v3.5-KeywordBackbone + GitHub Release | 1 session |
| **Tổng** | | **10 NEW + ~22 EXPAND/touch unique** | **~16 session** |

---

## 5. Khung sườn chi tiết — NEW files (mục lục + mục đích cho TỪNG file)

### 5.1. NEW `sdn-onboard/0.3 - master-keyword-index.md` (Phase J.2, ~3000 dòng, DEEP)

**Mục đích:**
File này là **lookup spine** của curriculum. Học viên gặp keyword bất kỳ trong log/CLI/spec → tra ngay vào 0.3 → biết chính xác file nào trong curriculum dạy keyword đó. Đồng thời là Vietnamese adaptation của REF: mỗi entry có 5-10 dòng giải thích bằng tiếng Việt (deep), KHÔNG chỉ một-dòng-lookup. Không duplicate REF (REF giữ làm offline source-of-truth English), nhưng deep enough để học viên đọc Vietnamese hiểu được trước khi mở REF.

**Mục lục:**

```
0.3.0  Mục đích + cách sử dụng index
0.3.1  Quy ước (5-axis explanation, status code DEEP/BREADTH/SHALLOW/MISSING/BANNED)
0.3.2  Khung sườn 5-axis (Bucket | Context | Purpose | Activity | Mechanism)
0.3.3  Cách tra cứu nhanh

Phần I — OVS keyword index
  0.3.I.1  Architecture & daemons (5 entry)
    - ovs-vswitchd, ovsdb-server, ovs-monitor-ipsec, ovs-tcpdump, control socket convention
  0.3.I.2  Datapath internals (25 entry in-scope, 5 BANNED note)
    - kernel datapath (openvswitch.ko), netdev/userspace datapath, ofproto/dpif, megaflow,
      megaflow wildcarding, microflow concept, recirc + recirc_id, conntrack family
      (ct, ct_state, ct_zone, ct_mark, ct_label, ALG, NAT), learn action, UFID,
      Interface type internal, Interface type patch, vlan_mode 4 type, bond_mode 3 type
    - BANNED note: DPDK datapath, EMC, SMC, PMD threads, mempool
  0.3.I.3  OVSDB (15 entry)
    - schema, transactional model, monitor / monitor-cond / monitor-cond-since,
      IDL synchronization, Raft cluster, replication, role-based access,
      ovsdb-tool offline ops, ovsdb-server remote (unix:/tcp:/ssl:)
  0.3.I.4  CLI tools (10 tool, sub-entry per option)
    - ovs-vsctl: 30 subcommand + 15 option
    - ovs-ofctl: 10 command + 10 option
    - ovs-appctl: target / format / pretty / vlog/list / vlog/set
    - ovs-dpctl: low-level datapath ops
    - ovs-pcap + ovs-tcpundump: offline pcap reformatter
    - ovsdb-tool: 15 command (offline)
    - ovsdb-client: 10 command (online)
    - ovs-pki: 7 command
    - ovs-testcontroller, vtep-ctl
  0.3.I.5  Observability (10 entry in-scope, 5 BANNED note)
    - coverage/show, dpif/show, dpif/dump-flows, ofproto/trace, fdb/show, bond/show,
      lacp/show, vlog/list, vlog/set, memory/show, upcall/show, dpctl/dump-conntrack,
      revalidator/wait, revalidator/purge
    - BANNED note: dpif-netdev/pmd-stats-show, pmd-rxq-show, pmd-rxq-rebalance,
      pmd-perf-show, netdev-dpdk/get-mempool-info

Phần II — OpenFlow keyword index
  0.3.II.1  Pipeline model (10 entry)
    - Pipeline architecture, table chaining via goto_table, instruction set order,
      action set vs action list, write_actions vs apply_actions, multi-table stages,
      ingress vs egress pipeline (1.5+), packet metadata preservation
  0.3.II.2  Match field catalog (60+ entry)
    - L2: in_port, in_phy_port, eth_src, eth_dst, eth_type, vlan_vid, vlan_pcp
    - L3: ip_dscp, ip_ecn, ip_proto, ipv4_src, ipv4_dst, ipv6_src, ipv6_dst,
      ipv6_flabel, ipv6_exthdr, nw_ttl
    - L4: tcp_src, tcp_dst, udp_src, udp_dst, sctp_src, sctp_dst, icmp_type, icmp_code,
      tcp_flags
    - ARP: arp_op, arp_spa, arp_tpa, arp_sha, arp_tha
    - MPLS: mpls_label, mpls_tc, mpls_bos
    - Pipeline state: tunnel_id (tun_id), pbb_isid, metadata, reg0-15, xreg0-7, xxreg0-3
    - NXM/OXM extension: ct_state, ct_zone, ct_mark, ct_label, ct_nw_src/dst, conj_id
  0.3.II.3  Action catalog (40+ entry)
    - Forwarding: output, group, drop (implicit), normal, flood, controller
    - Modification: set_field, copy_field (1.5+), set_queue
    - VLAN: push_vlan, pop_vlan
    - MPLS: push_mpls, pop_mpls, dec_mpls_ttl, set_mpls_ttl, copy_ttl_in/out
    - PBB: push_pbb, pop_pbb
    - L3: dec_ttl, set_nw_ttl
    - Recirculation: resubmit, conjunction, recirc, ct, ct_clear
    - Encapsulation: encap, decap (NSH)
    - Learning: learn
    - Annotation: note, sample
    - Meter: meter
  0.3.II.4  Instructions (6 entry)
    - Apply-Actions, Write-Actions, Clear-Actions, Write-Metadata, Goto-Table, Meter
  0.3.II.5  Messages & state machine (16 OFPT_* + state machine + AUX)
    - Symmetric: OFPT_HELLO, OFPT_ECHO_REQUEST/REPLY, OFPT_ERROR
    - Switch-to-Controller: OFPT_PACKET_IN, OFPT_FLOW_REMOVED, OFPT_PORT_STATUS, OFPT_TABLE_STATUS
    - Controller-to-Switch: OFPT_FEATURES_REQUEST/REPLY, OFPT_FLOW_MOD, OFPT_GROUP_MOD,
      OFPT_METER_MOD, OFPT_BARRIER_REQUEST/REPLY, OFPT_PACKET_OUT
    - Multipart: OFPT_MULTIPART_REQUEST/REPLY (14 type bên trong: FLOW, AGGREGATE, TABLE,
      PORT_STATS, GROUP, METER, METER_FEATURES, TABLE_FEATURES, ...)
    - Role: OFPT_ROLE_REQUEST/REPLY, OFPT_SET_ASYNC
    - Bundle (1.4+): OFPT_BUNDLE_OPEN, OFPT_BUNDLE_COMMIT, OFPT_BUNDLE_ADD_MESSAGE
    - Auxiliary (1.3+): OFPT_REQUESTFORWARD
    - State machine: HELLO → FEATURES → Steady (ECHO) → AUX
  0.3.II.6  Version differences (1.0 / 1.3 / 1.5)
    - Single-table vs Multi-table, NXM vs OXM, group tables 1.1+, meters 1.3+,
      bundles 1.4+, egress tables 1.5+, copy_field 1.5+, packet-type-aware 1.5+

Phần III — OVN keyword index
  0.3.III.1  Architecture & daemons (17 entry)
    - ovn-northd (active-standby + lock), ovn-controller (per-chassis),
      ovn-controller-vtep (HW gateway), ovn-ic, ovn-ic-northd,
      OVSDB Server roles, RAFT cluster, Relay mode, Inactivity probes,
      Northd probe interval, Leader election (active/standby/paused),
      Daemon threading (--n-threads)
  0.3.III.2  NB schema (25 entry)
    - NB_Global, Logical_Switch, Logical_Switch_Port (8 type), Port_Security,
      QoS, Requested Chassis, Reside-on-Redirect-Chassis, Logical_Router,
      Logical_Router_Port, Logical_Router_Static_Route, Logical_Router_Policy,
      NAT (snat/dnat/dnat_and_snat), Load_Balancer, Load_Balancer_Group,
      Load_Balancer_Health_Check, Address_Set, Port_Group, ACL, DHCP_Options,
      DNS, Forwarding_Group, HA_Chassis_Group, HA_Chassis, Meter, BFD
  0.3.III.3  SB schema (25 entry)
    - SB_Global, Chassis (with other_config), Datapath_Binding, Port_Binding (8 type),
      MAC_Binding, Logical_Flow, Multicast_Group, Service_Monitor, BFD, Encap,
      IGMP_Group, Connection, Address_Set, Port_Group, Meter, Meter_Band,
      MAC_Binding, Static_MAC_Binding, IP_Multicast, Load_Balancer, ACL, Chassis_Private,
      External_IDs, Controller_Event, FDB
  0.3.III.4  Pipeline table IDs (64 entry)
    - LS Ingress 28 stage (PORT_SEC_L2 → L2_UNKNOWN, table 0–27)
    - LS Egress 11 stage (PRE_ACL → APPLY_PORT_SEC, table 32–44)
    - LR Ingress 19 stage (ADMISSION → ARP_REQUEST)
    - LR Egress 6 stage (UNDNAT → DELIVERY)
  0.3.III.5  Register conventions + REGBIT + MLF (20 entry)
    - reg0-15 (32-bit), xreg0-7 (64-bit), xxreg0-3 (128-bit) OVN convention
    - REGBIT_PORT_SEC_DROP, REGBIT_ACL_HINT_*, REGBIT_CONNTRACK_COMMIT,
      REGBIT_LB_NAT_DEFRAG, REGBIT_DHCP_OPTS_RESULT, REGBIT_HAIRPIN_REPLY,
      REGBIT_SKIP_LOOKUP, REGBIT_FROM_RAMP, REGBIT_EGRESS_LOOPBACK,
      REGBIT_PKT_LARGER, REGBIT_OWN_REPLY, REGBIT_NOT_LOCALPORT
    - MLF_LOCAL_ONLY, MLF tunnel metadata encoding
    - Geneve TLV class 0x0102
  0.3.III.6  CLI tools
    - ovn-nbctl: ~100 command (12 group)
    - ovn-sbctl: ~15 command
    - ovn-trace: microflow expression syntax
    - ovn-detrace: cookie → logical flow mapping
    - ovn-ic-nbctl, ovn-ic-sbctl
    - ovn-appctl: 21 module command
  0.3.III.7  Observability
    - lflow-cache (show-stats, ovn-enable-lflow-cache, ovn-limit-lflow-cache,
      ovn-memlimit-lflow-cache-kb, ovn-trim-limit-lflow-cache, ovn-trim-wmark-perc),
      inc-engine/show-stats, connection-status, BFD table, Service_Monitor,
      MAC_Binding inspect, DNS table, Multicast_Group, ACL Logging (5 severity),
      HA_Chassis_Group failover

Phần IV — Out of curriculum scope (BANNED)
  - DPDK datapath, PMD thread, EMC (Exact-Match Cache), SMC (Signature Match Cache),
    mempool, hugepage NUMA tuning, dpif-netdev/pmd-* commands, netdev-dpdk/* commands
  - Lý do: PERMANENT BAN per CLAUDE.md North Star (verbatim user 2026-04-25)
  - Hành động: existing 9.3 + 16.x đã có baseline coverage, KHÔNG expand
  - Học viên muốn deep-dive: đọc REF Section 1.2, 1.5 hoặc upstream DPDK docs

Phần V — Cross-link map
  - Bảng "keyword → file → section anchor" cho 310 entry
  - Format: `<keyword> → <Part X.Y §Z> → <REF Section a.b>`
  - Sort theo bucket (OVS / OpenFlow / OVN) cho lookup nhanh
```

**Format mỗi entry:**

```markdown
### `<keyword name>`

**5-axis:**
- **Bucket:** <category>
- **Context:** <khi nào keyword xuất hiện>
- **Purpose:** <mục đích keyword giải quyết>
- **Activity:** <hành vi runtime / use case chính>
- **Mechanism:** <cách hoạt động dưới capot>

**Giải thích Vietnamese (5–10 dòng):** Đây là deep mode. Mở rộng từng axis bằng prose Vietnamese. Bao gồm: khi engineer đọc log/CLI gặp keyword này thì hiểu thế nào, edge case + caveat khi sử dụng, common misconception.

**Curriculum:** xem [Part X.Y §Z](X.Y - <name>.md#section)
**Upstream source:** <URL chính xác>
**Status:** DEEP / BREADTH / SHALLOW / MISSING (sau J.1 audit)
```

---

### 5.2. NEW `sdn-onboard/3.3 - openflow-protocol-messages-state-machine.md` (Phase J.4, ~600 dòng)

**Mục đích:**
Hiện 119 file curriculum không có file dedicated cho OpenFlow protocol messages. Học viên đọc log `ovs-vswitchd.log` thấy `OFPT_HELLO`, `OFPT_BARRIER_REQUEST` không hiểu nguồn gốc. File 3.3 fill gap: cover toàn bộ 16 OFPT_* messages + state machine 4-stage + auxiliary connection (OF 1.3+) + bundle (OF 1.4+) + role messages.

**Mục lục:**

```
3.3.0  Mục đích + cách đọc file
3.3.1  OpenFlow protocol overview
       - TCP/TLS over port 6633 (legacy) / 6653 (IANA assigned 2013)
       - Common 8-byte header: version + type + length + xid
       - Hex dump example từ tcpdump
3.3.2  Message classification
       - Symmetric (cả switch lẫn controller có thể khởi tạo)
       - Asymmetric (Switch → Controller hoặc Controller → Switch)
3.3.3  Symmetric messages
       3.3.3.1  OFPT_HELLO (Type 0)
                - Version negotiation bitmap
                - Anatomy hex dump
                - 5-axis treatment
       3.3.3.2  OFPT_ECHO_REQUEST/REPLY (Types 2/3)
                - Keep-alive heartbeat
                - Default 5-15 sec interval
                - 3 missed = reconnect
       3.3.3.3  OFPT_ERROR (Type 1)
                - Error code structure
                - Common errors (BAD_VERSION, BAD_TYPE, BAD_MULTIPART, etc.)
3.3.4  Switch-to-Controller messages
       3.3.4.1  OFPT_PACKET_IN (Type 10)
                - Reasons: no_match / action / invalid_ttl
                - Buffer ID + table_id + match (OXM)
                - Userdata Nicira extension (continuation-based)
       3.3.4.2  OFPT_FLOW_REMOVED (Type 11)
                - Reasons: IDLE_TIMEOUT / HARD_TIMEOUT / DELETE / GROUP_DELETE / METER_DELETE
                - Statistics carry-back (byte/packet count, duration, cookie)
       3.3.4.3  OFPT_PORT_STATUS (Type 12)
                - Reasons: ADD / DELETE / MODIFY
                - Topology awareness use case
       3.3.4.4  OFPT_TABLE_STATUS (Type 30, OF 1.3+)
                - VACANCY_DOWN / VACANCY_UP threshold crossing
                - Table pressure monitoring
3.3.5  Controller-to-Switch messages
       3.3.5.1  OFPT_FEATURES_REQUEST/REPLY (Types 5/6)
                - datapath_id, n_buffers, n_tables, capabilities
                - Port list with names + addresses + features
       3.3.5.2  OFPT_FLOW_MOD (Type 14)
                - Commands: ADD / MODIFY / MODIFY_STRICT / DELETE / DELETE_STRICT
                - Flags: NO_PKT_COUNTS, NO_BYT_COUNTS, SEND_FLOW_REMOVED, RESET_COUNTS
                - Idle vs hard timeout
       3.3.5.3  OFPT_GROUP_MOD (Type 15, OF 1.2+)
                - 4 group type: all / select / indirect / fast_failover
                - Bucket structure + watch_port/watch_group
       3.3.5.4  OFPT_METER_MOD (Type 29, OF 1.3+)
                - kbps vs pktps + burst
                - Band type drop / dscp_remark
       3.3.5.5  OFPT_BARRIER_REQUEST/REPLY (Types 20/21)
                - Strict ordering guarantee
                - When to use (post FLOW_MOD batch verify)
       3.3.5.6  OFPT_PACKET_OUT (Type 13)
                - in_port virtual + action list
                - Inject custom packet
3.3.6  Multipart messages (OF 1.3+)
       3.3.6.1  OFPT_MULTIPART_REQUEST (Type 18)
                - Type field 14 sub-type: FLOW, AGGREGATE, TABLE, PORT_STATS,
                  QUEUE_STATS, GROUP, GROUP_DESC, GROUP_FEATURES, METER, METER_CONFIG,
                  METER_FEATURES, TABLE_FEATURES, PORT_DESC, EXPERIMENTER
       3.3.6.2  OFPT_MULTIPART_REPLY (Type 19)
                - REPLY_MORE flag fragmentation
                - xid matching reassembly
3.3.7  Role + Async config (OF 1.3+)
       3.3.7.1  OFPT_ROLE_REQUEST/REPLY (Types 24/25)
                - 4 role: NOCHANGE / EQUAL / MASTER / SLAVE
                - generation_id stale prevention
                - Controller redundancy use case
       3.3.7.2  OFPT_SET_ASYNC (Type 28, OF 1.4+)
                - Per-role async notification mask
                - PACKET_IN / PORT_STATUS / FLOW_REMOVED / TABLE_STATUS
3.3.8  Bundle messages (OF 1.4+)
       3.3.8.1  OFPT_BUNDLE_OPEN (Type 34)
                - bundle_id + flags atomic / ordered
       3.3.8.2  OFPT_BUNDLE_ADD_MESSAGE (Type 36)
                - Encapsulate flow_mod / group_mod / meter_mod
       3.3.8.3  OFPT_BUNDLE_COMMIT (Type 35)
                - All-or-nothing semantics
                - Anti-pattern: split state during partial failure
3.3.9  Auxiliary connections (OF 1.3+)
       3.3.9.1  Concept (multiple TCP/TLS to same datapath_id)
       3.3.9.2  Use cases (parallel transmission, switch-to-switch forward,
                role assignment for redundant controllers)
       3.3.9.3  OFPT_REQUESTFORWARD (Type 32, OF 1.4+)
3.3.10 Connection state machine
       3.3.10.1  HELLO state (post TCP/TLS, version negotiation)
       3.3.10.2  FEATURES state (capability discovery)
       3.3.10.3  Steady state (ECHO keep-alive + flow ops + multipart query)
       3.3.10.4  AUX state (auxiliary connection)
       3.3.10.5  State transition diagram (ASCII)
       3.3.10.6  Error state + reconnect logic
3.3.11 Anatomy: capture + decode OF messages
       3.3.11.1  ovs-ofctl monitor watch:flow_mod,packet_in
       3.3.11.2  tcpdump on port 6653 + Wireshark dissector
       3.3.11.3  Decode hex dump example
3.3.12 Hands-on Guided Exercise
       3.3.12.1  Mininet 1-switch + ryu controller setup
       3.3.12.2  Trace HELLO + FEATURES exchange via tcpdump
       3.3.12.3  Trigger PACKET_IN bằng ARP
       3.3.12.4  Send BARRIER + verify reply
3.3.13 Capstone POE
       3.3.13.1  Bundle vs sequential FLOW_MOD: consistency under partial failure
       3.3.13.2  Sinh viên thiết kế experiment chứng minh atomic property
3.3.14 Cross-link
       3.3.14.1  Block III (3.0, 3.1, 3.2 OF spec evolution)
       3.3.14.2  Block IV (4.0–4.5 multi-table + group + meter + bundle)
       3.3.14.3  9.16 ovs-vswitchd connection manager
3.3.15 References
       3.3.15.1  ONF OpenFlow Switch Specification 1.3.5 + 1.5.1
       3.3.15.2  ovs-ofctl(8) man page
```

---

### 5.3. NEW `sdn-onboard/3.4 - openflow-version-differences-1.0-1.3-1.5.md` (Phase J.4, ~500 dòng)

**Mục đích:**
Học viên upgrade switch từ OF 1.0 lên 1.3 hoặc 1.5 không hiểu rule nào break, rule nào tự động compatible. File 3.4 cover 8 major version difference từ REF Section 2.4 + migration matrix + decision tree khi nào dùng version nào.

**Mục lục:**

```
3.4.0  Mục đích
3.4.1  OpenFlow version timeline
       - 1.0 (Dec 2009 wire 0x01) → 1.1 (Feb 2011) → 1.2 (Dec 2011) →
         1.3 (Apr 2012, wire 0x04, LTS) → 1.4 (Aug 2013) → 1.5 (Apr 2015 wire 0x06)
       - OVS support matrix per version
3.4.2  Single-table vs Multi-table pipeline (1.0 → 1.1+)
       - 1.0: 1 table only, no goto_table, simple match-action
       - 1.1+: 254-table pipeline, goto_table chain, metadata survives
       - Migration impact: rule rewrite required
       - Decision: when 1.0 sufficient (legacy testbed) vs need 1.3+ (OVN)
3.4.3  NXM vs OXM encoding (1.0-1.1 → 1.2+)
       - NXM: TLV format, 16-bit class (NXM_OF=0, NXM_NX=1) + 8-bit type
       - OXM: TLV with 32-bit class (OXM_OF=0x8000, OXM_NX=0x8001)
       - Wire format incompatible (OVS internal converts)
       - Practical impact: ovs-ofctl --protocols negotiation
3.4.4  Group tables (1.1+)
       - 4 type: all / select / indirect / fast_failover
       - Bucket structure
       - 1.0 workaround: duplicate flow per output port
       - fast_failover watch_port/watch_group health monitor
3.4.5  Meters (1.3+)
       - Meter table separate from flow table
       - Bands: drop / dscp_remark + rate (kbps/pktps) + burst
       - 1.0-1.2 workaround: external rate limit (tc qdisc)
3.4.6  Bundles (1.4+)
       - Atomic multi-message transaction
       - BUNDLE_OPEN → ADD_MESSAGE × N → COMMIT
       - Rollback semantics
       - Use case: OVN flow update during ovn-controller restart (avoid split-brain)
3.4.7  Egress tables (1.5+)
       - Optional pipeline after action set execution
       - Per-port output processing
       - Use case: VLAN tag removal only on specific ports
3.4.8  copy_field action (1.5+)
       - Standardized vs OVS extension move action (NXM)
       - Bit-offset support: copy_field(src_offset:src_field, dst_offset:dst_field, n_bits)
3.4.9  Packet-type-aware pipeline (1.5+)
       - packet_type field for non-Ethernet encapsulation
       - NSH / bare IP / Service Function Chaining
3.4.10 Anatomy: ovs-ofctl --protocols detection
       - Bridge.protocols column
       - HELLO bitmap exchange
       - Negotiation result
3.4.11 Migration matrix
       3.4.11.1  OF 1.0 → 1.3 rule rewrite walkthrough
       3.4.11.2  OF 1.3 → 1.5 add egress + copy_field migration
       3.4.11.3  Backward compat checklist (OVS forward-compat)
3.4.12 Decision tree: which version to use
       - OVN deployment: OF 1.3 minimum, recommend 1.5
       - Legacy SDN testbed: 1.0 acceptable
       - SFC/NSH research: 1.5 required
3.4.13 Capstone POE
       - Sinh viên đề xuất migration plan cho production switch từ 1.0 lên 1.3
       - Risk analysis + rollback strategy
3.4.14 Cross-link
       - 3.1 OF 1.0 spec, 4.0–4.5 1.1–1.5 deep dive
       - 4.7 OpenFlow programming with OVS
3.4.15 References
       - ONF spec 1.0.0, 1.3.5, 1.5.1
       - OVS NEWS file (https://www.openvswitch.org/releases/)
```

---

### 5.4. NEW `sdn-onboard/9.28 - ovs-pcap-tcpundump-utility.md` (Phase J.3, ~150 dòng)

**Mục đích:**
REF Section 1.4 entry `ovs-pcap` + `ovs-tcpundump` chỉ có 1 file curriculum mention. Helper này cực hữu dụng cho debugging: pipe pcap thật vào `ofproto/trace` để simulate "what would OVS pipeline do với packet này". Đây là missing tool trong CLI mastery.

**Mục lục:**

```
9.28.0  Mục đích (pure reformatter pipe vào ofproto/trace)
9.28.1  ovs-pcap: chuyển pcap → hex-encoded one-packet-per-line
        - Synopsis + options
        - Output format giải thích
9.28.2  ovs-tcpundump: reverse, từ tcpdump -xx output → pcap
        - Synopsis + options
        - Use case: revive old tcpdump dump
9.28.3  Workflow tích hợp với ofproto/trace
        - Pipeline: tcpdump → ovs-pcap → ovs-appctl ofproto/trace br-int "$(...)"
        - Hex format phải đúng cho ofproto/trace accept
9.28.4  Anatomy command output
        - ovs-pcap capture.pcap | head -1 → giải thích từng field hex
        - Cross-reference ovs-fields(7)
9.28.5  Hands-on Guided Exercise
        - Capture 5 packet TCP SYN trên br-int
        - Convert qua ovs-pcap → pipe vào ofproto/trace
        - So sánh với live traffic
9.28.6  Anti-pattern + caveat
        - Không dùng pcap đã bị truncated (snaplen ngắn)
        - Pipeline output không giống live nếu OVSDB state đã đổi
9.28.7  Cross-link
        - 9.4 ovs-vsctl, 9.11 ovs-appctl, 20.0 systematic debugging,
          20.7 packet flow tracing gradient (L4/L5)
9.28.8  References
        - ovs-pcap(1), ovs-tcpundump(1) man page
```

---

### 5.5. NEW `sdn-onboard/9.29 - vtep-ctl-vtep-schema.md` (Phase J.3, ~200 dòng)

**Mục đích:**
REF Section 1.4 đề cập `vtep-ctl` (same syntax như `ovs-vsctl` nhưng cho VTEP schema). 0 file curriculum mention. Hardware VXLAN gateway integration trong OVN deployment cần biết VTEP. File 9.29 fill gap: VTEP schema 7 table + vtep-ctl CLI + OVN integration.

**Mục lục:**

```
9.29.0  Mục đích (hardware VXLAN gateway integration)
9.29.1  VTEP schema overview
        - 7 table: Global, Manager, Logical_Switch, Logical_Binding_Stats,
          Physical_Switch, Physical_Port, Physical_Locator
        - JSON schema structure (cross-link 10.0 OVSDB schema)
9.29.2  vtep-ctl synopsis
        - Same syntax pattern như ovs-vsctl
        - Common subcommand: list-ps, add-ls, bind-ls, unbind-ls
9.29.3  Use case: HW VXLAN gateway in OVN
        - Logical_Switch_Port type=vtep (NB schema)
        - ovn-controller-vtep daemon cầu nối
        - Geneve vs VXLAN trade-off cho HW
9.29.4  Anatomy: vtep-ctl list-ps
        - 7-attribute table view
        - Healthy / Warning / Critical thresholds
9.29.5  Anatomy: vtep-ctl bind-ls
        - Binding logical switch to physical switch port
9.29.6  Hands-on Guided Exercise (synthetic)
        - Mock HW VTEP setup với ovs-vtep simulator
        - Add LS + bind to mock port
        - Verify binding via vtep-ctl + sbctl
9.29.7  Production caveat
        - HW vendor compat (Arista, Mellanox, Cumulus)
        - Tunnel MTU + checksum offload concerns
9.29.8  Cross-link
        - 13.5 OVN Port_Binding type=vtep
        - 11.0 VXLAN packet format
        - 13.0 OVN architecture
9.29.9  References
        - vtep-ctl(8) man page
        - OVN architecture VTEP section
```

---

### 5.6. NEW `sdn-onboard/9.30 - ovs-pki-pki-helper.md` (Phase J.3, ~180 dòng)

**Mục đích:**
REF Section 1.4 `ovs-pki` chỉ có 7 file curriculum mention. SSL/TLS cho Controller + Manager + OVSDB connection cần PKI. File 9.30 fill gap: certificate chain bootstrap workflow + 7 ovs-pki command.

**Mục lục:**

```
9.30.0  Mục đích (SSL/TLS cho Controller + Manager + OVSDB connection)
9.30.1  PKI overview
        - CA chain (root CA → intermediate → leaf cert)
        - Self-signed vs CA-signed trade-off
9.30.2  ovs-pki commands
        9.30.2.1  init: bootstrap PKI directory
        9.30.2.2  req: create cert request
        9.30.2.3  sign: CA signs cert request
        9.30.2.4  req+sign: combined
        9.30.2.5  fingerprint: print SHA-256 fingerprint
        9.30.2.6  self-sign: standalone cert
        9.30.2.7  set-default: pick default cert
9.30.3  Anatomy: ovs-pki req+sign workflow
        - Output structure giải thích
9.30.4  Hands-on Guided Exercise
        - Bootstrap CA + sign cert cho ovsdb-server
        - Configure ovsdb-server --remote=ssl:6640 với cert
        - Verify với ovs-vsctl --ssl-* options
9.30.5  Production caveat
        - Cert rotation workflow
        - CRL handling
        - Common mistake: file permission 600 cho privkey
9.30.6  Cross-link
        - 10.6 OVSDB SSL/RBAC advanced
        - 20.1 OVS+OVN security hardening
9.30.7  References
        - ovs-pki(8) man page
```

---

### 5.7. NEW `sdn-onboard/9.31 - ovsdb-tool-offline-utility.md` (Phase J.3, ~250 dòng)

**Mục đích:**
REF Section 1.4 `ovsdb-tool` 15 command, 0 file curriculum mention. Offline OVSDB file utility critical cho cluster bootstrap + db migration + show-log forensic. File 9.31 fill gap: 15 command với 5-axis + 3-node Raft cluster bootstrap walkthrough.

**Mục lục:**

```
9.31.0  Mục đích + warning ABSOLUTE (must NOT run against active server)
9.31.1  Synopsis + options
9.31.2  Database creation
        9.31.2.1  ovsdb-tool create DB SCHEMA
        9.31.2.2  ovsdb-tool create-cluster DB CONTENTS LOCAL
        9.31.2.3  ovsdb-tool join-cluster DB NAME LOCAL REMOTE...
        9.31.2.4  --cluster-name option
        9.31.2.5  --cid UUID option
        9.31.2.6  --election-timer MS option
9.31.3  Schema management
        9.31.3.1  ovsdb-tool convert DB SCHEMA
        9.31.3.2  ovsdb-tool needs-conversion DB SCHEMA
        9.31.3.3  ovsdb-tool db-version DB
        9.31.3.4  ovsdb-tool schema-version SCHEMA
        9.31.3.5  ovsdb-tool compare-versions A OP B
9.31.4  Integrity + compaction
        9.31.4.1  ovsdb-tool db-cksum DB
        9.31.4.2  ovsdb-tool schema-cksum SCHEMA
        9.31.4.3  ovsdb-tool compact DB
9.31.5  Inspection + query
        9.31.5.1  ovsdb-tool query DB QUERY
        9.31.5.2  ovsdb-tool transact DB TXN
        9.31.5.3  ovsdb-tool show-log DB
        9.31.5.4  ovsdb-tool show-log -m DB (with metadata)
        9.31.5.5  ovsdb-tool check-cluster DB...
9.31.6  Cluster lifecycle introspection
        9.31.6.1  ovsdb-tool db-name
        9.31.6.2  ovsdb-tool schema-name
        9.31.6.3  ovsdb-tool db-cid DB
        9.31.6.4  ovsdb-tool db-sid DB
        9.31.6.5  ovsdb-tool db-local-address DB
9.31.7  Anatomy: 3-node OVN_Southbound Raft cluster bootstrap
        - Step 1: ovsdb-tool create-cluster trên node-1
        - Step 2: ovsdb-tool join-cluster trên node-2 + node-3
        - Step 3: start ovsdb-server cluster mode
        - Step 4: ovsdb-client list-dbs verify
9.31.8  Anatomy: show-log forensic
        - Raft log entry parse
        - Term + index + command body
        - Use case: debug cluster split-brain
9.31.9  Hands-on Guided Exercise
        - Bootstrap 3-node OVN_Southbound từ scratch
        - Simulate node failure + check-cluster verify
        - Schema upgrade workflow (needs-conversion → convert)
9.31.10 Anti-pattern + caveat
        - KHÔNG dùng compact trên active cluster (offline only)
        - Backup trước khi convert
9.31.11 Cross-link
        - 10.0 OVSDB schema, 10.1 OVSDB Raft clustering, 10.2 backup-restore
9.31.12 References
        - ovsdb-tool(1) man page
```

---

### 5.8. NEW `sdn-onboard/13.15 - ovn-interconnect-multi-region.md` (Phase J.5, ~400 dòng)

**Mục đích:**
REF Section 3.1 đề cập `ovn-ic` + `ovn-ic-northd` + IC_NB + IC_SB DBs cho federated multi-region OVN deployment. 0 file curriculum mention. File 13.15 fill gap: OVN-IC architecture + Transit Switch + Transit Router + ovn-ic-nbctl/sbctl CLI + 2-region lab. KHÔNG đề cập BGP expansion (per BAN).

**Mục lục:**

```
13.15.0  Mục đích (federated multi-region OVN deployment)
13.15.1  Inter-Connect architecture
         13.15.1.1  Why federation: scale, geographic, regulatory boundary
         13.15.1.2  IC_NB + IC_SB DBs (separate from main NB/SB)
         13.15.1.3  Topology: per-region OVN cluster + central IC cluster
13.15.2  Daemons
         13.15.2.1  ovn-ic (per-region client)
         13.15.2.2  ovn-ic-northd (central IC compiler)
13.15.3  Transit Switch concept
         13.15.3.1  Cross-region L2 bridge
         13.15.3.2  TS_NAME convention
         13.15.3.3  Logical_Switch in IC_NB
13.15.4  Transit Router + AvailabilityZone
         13.15.4.1  Cross-region L3 routing
         13.15.4.2  AZ route synchronization
         13.15.4.3  Static route propagation (KHÔNG dùng BGP - banned)
13.15.5  ovn-ic-nbctl + ovn-ic-sbctl CLI
         13.15.5.1  ts-add, ts-list, ts-del
         13.15.5.2  list AvailabilityZone
         13.15.5.3  list Transit_Switch
         13.15.5.4  list Route
13.15.6  Geneve transit tunnel
         13.15.6.1  Per-region encap config
         13.15.6.2  Cross-link 11.0 Geneve packet format
13.15.7  Anatomy: ovn-ic-nbctl ts-add
         - 5-axis treatment + Healthy / Warning / Critical
13.15.8  Anatomy: ovn-ic-sbctl list AvailabilityZone
         - 7-attribute table view
13.15.9  Hands-on Guided Exercise: 2-region lab
         13.15.9.1  Region-A (HQ) setup: 3-node Raft + ovn-ic
         13.15.9.2  Region-B (Branch) setup
         13.15.9.3  Central IC cluster bootstrap
         13.15.9.4  Create Transit Switch + bind 2 regions
         13.15.9.5  Verify cross-region VM connectivity
13.15.10 Capstone POE
         - Sinh viên thiết kế federation cho 3-region (HQ + 2 branch)
         - Trade-off: Transit Switch L2 vs Transit Router L3
13.15.11 Production caveat
         - IC cluster latency tolerance
         - Inactivity probe tuning
         - KHÔNG dùng BGP expansion (banned, link 11.2 BGP EVPN cho học bộ riêng)
13.15.12 Cross-link
         - 13.0 OVN architecture
         - 11.0 Geneve
         - 9.31 ovsdb-tool create-cluster
         - 13.16 pipeline table IDs (cho IC datapath)
13.15.13 References
         - ovn-ic(8), ovn-ic-nbctl(8), ovn-ic-sbctl(8) man page
         - OVN Inter-Connect documentation
```

---

### 5.9. NEW `sdn-onboard/13.16 - ovn-logical-pipeline-table-id-map.md` (Phase J.5, ~700 dòng, **CRITICAL gap**)

**Mục đích:**
REF Section 3.3 enumerate 64 pipeline table IDs (28 LS_IN + 11 LS_OUT + 19 LR_IN + 6 LR_OUT). Sample audit cho thấy 0/64 file curriculum mention các stage names. Đây là CRITICAL gap nhất. Học viên đọc `ovs-ofctl dump-flows br-int table=N` không biết stage nào. File 13.16 = canonical reference table ID map cho OVN 22.03.8 baseline + version note callout.

**Mục lục:**

```
13.16.0  Mục đích (canonical table ID reference)
13.16.1  OVN pipeline overview
         13.16.1.1  Pipeline = sequence of logical "stages"
         13.16.1.2  Mỗi stage có fixed table_id trên br-int
         13.16.1.3  4 block: LS_IN, LS_OUT, LR_IN, LR_OUT
13.16.2  Table block layout (OVN 22.03.8 baseline)
         13.16.2.1  LS_IN tables 0–27 (28 stage)
         13.16.2.2  LS_OUT tables 32–44 (11 stage, có gap reserved)
         13.16.2.3  LR_IN tables 48+ (19 stage, offset depend on LS occupancy)
         13.16.2.4  LR_OUT tables ~70+ (6 stage)
         13.16.2.5  Version drift notes (22.03 → 24.03 + 24.09 changes)

13.16.3  LS Ingress pipeline 28 stage detail (Tables 0–27)
         Mỗi stage có: 5-axis | OpenFlow table_id | Source code anchor (northd/build_lflows.c) | Match field used | Action emitted | Next stage

         Table 0  - LS_IN_PORT_SEC_L2     (port-security L2 MAC check)
         Table 1  - LS_IN_PORT_SEC_IP     (port-security IP check)
         Table 2  - LS_IN_PORT_SEC_ND     (ND/ARP port-security)
         Table 3  - LS_IN_PRE_ACL         (pre-ACL stateful connector)
         Table 4  - LS_IN_PRE_LB          (pre-load-balancer conntrack entry)
         Table 5  - LS_IN_PRE_STATEFUL    (stateful pre-processing)
         Table 6  - LS_IN_ACL_HINT        (ACL hint allow/drop register)
         Table 7  - LS_IN_ACL_EVAL        (ACL evaluation match)
         Table 8  - LS_IN_ACL_ACTION     (ACL action drop/allow/reject)
         Table 9  - LS_IN_QOS_MARK       (QoS DSCP mark)
         Table 10 - LS_IN_QOS_METER      (QoS rate-limit metering)
         Table 11 - LS_IN_LB_AFF_CHECK   (LB affinity check)
         Table 12 - LS_IN_LB             (load balancer DNAT)
         Table 13 - LS_IN_LB_AFF_LEARN   (LB affinity learning)
         Table 14 - LS_IN_PRE_HAIRPIN    (pre-hairpin)
         Table 15 - LS_IN_NAT_HAIRPIN    (hairpin NAT)
         Table 16 - LS_IN_HAIRPIN        (hairpin delivery)
         Table 17 - LS_IN_ACL_AFTER_LB_EVAL  (post-LB ACL eval)
         Table 18 - LS_IN_ACL_AFTER_LB_ACTION (post-LB ACL action)
         Table 19 - LS_IN_STATEFUL       (stateful commit)
         Table 20 - LS_IN_ARP_ND_RSP     (ARP/ND responder)
         Table 21 - LS_IN_DHCP_OPTIONS   (DHCP option construction)
         Table 22 - LS_IN_DHCP_RESPONSE  (DHCP reply generation)
         Table 23 - LS_IN_DNS_LOOKUP     (DNS name lookup)
         Table 24 - LS_IN_DNS_RESPONSE   (DNS reply generation)
         Table 25 - LS_IN_EXTERNAL_PORT  (external port handling)
         Table 26 - LS_IN_L2_LKUP        (L2 unicast/multicast lookup)
         Table 27 - LS_IN_L2_UNKNOWN     (unknown unicast flooding)

13.16.4  LS Egress pipeline 11 stage detail (Tables 32–44)
         Mỗi stage có cùng template format

         Table 32 - LS_OUT_PRE_ACL
         Table 33 - LS_OUT_PRE_LB
         Table 34 - LS_OUT_PRE_STATEFUL
         Table 35 - LS_OUT_ACL_HINT
         Table 36 - LS_OUT_ACL_EVAL
         Table 37 - LS_OUT_ACL_ACTION
         Table 38 - LS_OUT_QOS_MARK
         Table 39 - LS_OUT_QOS_METER
         Table 40 - LS_OUT_STATEFUL
         Table 41 - LS_OUT_CHECK_PORT_SEC
         Table 42 - LS_OUT_APPLY_PORT_SEC

13.16.5  LR Ingress pipeline 19 stage detail
         LR_IN_ADMISSION
         LR_IN_LOOKUP_NEIGHBOR
         LR_IN_LEARN_NEIGHBOR
         LR_IN_IP_INPUT
         LR_IN_UNSNAT
         LR_IN_DNAT
         LR_IN_ECMP_STATEFUL
         LR_IN_ND_RA_OPTIONS
         LR_IN_ND_RA_RESPONSE
         LR_IN_IP_ROUTING_PRE
         LR_IN_IP_ROUTING
         LR_IN_IP_ROUTING_ECMP
         LR_IN_POLICY
         LR_IN_POLICY_ECMP
         LR_IN_ARP_RESOLVE
         LR_IN_CHK_PKT_LEN
         LR_IN_LARGER_PKTS
         LR_IN_GW_REDIRECT
         LR_IN_ARP_REQUEST

13.16.6  LR Egress pipeline 6 stage detail
         LR_OUT_UNDNAT
         LR_OUT_POST_UNDNAT
         LR_OUT_SNAT
         LR_OUT_POST_SNAT
         LR_OUT_EGR_LOOP
         LR_OUT_DELIVERY

13.16.7  Cross-pipeline metadata
         13.16.7.1  Packet jump LS → LR via patch port
         13.16.7.2  Packet jump LR → LR via patch port
         13.16.7.3  Tunnel encap (Geneve/VXLAN) cho cross-chassis
         13.16.7.4  reg14 + reg15 inport/outport tunnel key role

13.16.8  Anatomy: ovs-ofctl dump-flows br-int table=N
         - Mapping table N → stage name
         - Cookie field decode
         - Match register usage decode

13.16.9  Anatomy: ovn-sbctl lflow-list <ls> | <lr>
         - Pipeline column (ingress / egress)
         - Table column (table_id + stage name)
         - Match + Action column

13.16.10 Anatomy: ovn-detrace
         - Cookie → logical flow UUID mapping
         - Logical flow → NB schema source

13.16.11 Hands-on Guided Exercise
         13.16.11.1  Mininet 1-LS + 2-VM setup
         13.16.11.2  Trace TCP SYN packet qua ALL 28 LS_IN stages
         13.16.11.3  ovn-trace --detailed → identify mỗi stage output
         13.16.11.4  ovs-ofctl dump-flows table=N cho mỗi stage → verify

13.16.12 Hands-on Guided Exercise (LR)
         13.16.12.1  2-LS + 1-LR setup
         13.16.12.2  Cross-subnet ping
         13.16.12.3  Trace qua LR_IN 19 stage + LR_OUT 6 stage

13.16.13 Capstone POE
         13.16.13.1  Sinh viên dự đoán table_id cho given OVN feature
         13.16.13.2  Verify với ovn-sbctl lflow-list

13.16.14 Version drift note
         13.16.14.1  22.03 baseline (curriculum default)
         13.16.14.2  24.03 changes (LB_AFF reordered, ECMP stage merged)
         13.16.14.3  24.09 changes (mac-learning rewrite)
         13.16.14.4  Mỗi commit verified via Rule 14 source citation

13.16.15 Source code verify (Rule 14)
         - northd/northd.c enum ovn_stage
         - controller/lflow.c populate flow per stage
         - include/ovn/logical-fields.h register convention

13.16.16 Cross-link
         - 13.7 ovn-controller physical.c (translate logical → OF)
         - 13.8 northd build_lflows (compile NB → SB → logical flow)
         - 13.17 register conventions
         - 20.7 packet flow tracing gradient L1-L5

13.16.17 References
         - ovn-northd(8) section "Logical Switch Ingress Table"
         - OVN source branch-22.03 northd/northd.c
```

---

### 5.10. NEW `sdn-onboard/13.17 - ovn-register-conventions-regbit-mlf.md` (Phase J.5, ~400 dòng)

**Mục đích:**
REF Section 3.3 đề cập OVN register convention (reg13=ct_zone, reg14=inport, reg15=outport) + REGBIT bit-flag (REGBIT_PORT_SEC_DROP, REGBIT_CONNTRACK_COMMIT, etc.) + MLF flag (MLF_LOCAL_ONLY). 0 file curriculum mention. Đây là cốt lõi để decode `ovs-ofctl dump-flows | grep regN` output.

**Mục lục:**

```
13.17.0  Mục đích (decode dump-flows register state)
13.17.1  OpenFlow register inventory (background)
         13.17.1.1  reg0-15: 32-bit each (NXM extension OVS 1.1+)
         13.17.1.2  xreg0-7: 64-bit each (paired reg)
         13.17.1.3  xxreg0-3: 128-bit each
         13.17.1.4  Cross-link 4.8 match field catalog

13.17.2  OVN register convention
         13.17.2.1  reg0 - scratch / NAT match state / ECMP selection result
         13.17.2.2  reg1 - scratch / ECMP next-hop / IPv4 ARP resolve
         13.17.2.3  reg2-3 - reserved / occasional scratch
         13.17.2.4  reg4-5 - SNAT IPv4 source address scratch
         13.17.2.5  reg6-7 - reserved
         13.17.2.6  reg8-12 - destination IP scratch
         13.17.2.7  reg13 - ct_zone for ingress port (port-security stage write)
         13.17.2.8  reg14 - inport tunnel key (16-bit logical port)
         13.17.2.9  reg15 - outport tunnel key (16-bit logical port)
         13.17.2.10 xxreg0 - IPv6 ND/NA scratch (128-bit IPv6 address)

13.17.3  REGBIT bit-flag inventory (reg0 individual bits)
         13.17.3.1  REGBIT_PORT_SEC_DROP (bit 0) - port security drop indicator
         13.17.3.2  REGBIT_ACL_HINT_ALLOW_NEW (bit 1) - ACL allow-new hint cho ct
         13.17.3.3  REGBIT_CONNTRACK_COMMIT (bit 2) - instruct ct commit stage
         13.17.3.4  REGBIT_LB_NAT_DEFRAG - LB DNAT + defrag flag
         13.17.3.5  REGBIT_DHCP_OPTS_RESULT - DHCP option construction result
         13.17.3.6  REGBIT_HAIRPIN_REPLY - hairpin reply traffic flag
         13.17.3.7  REGBIT_SKIP_LOOKUP (bit 7) - skip L2 lookup (after ARP reply inject)
         13.17.3.8  REGBIT_FROM_RAMP - ramp switch traffic flag
         13.17.3.9  REGBIT_EGRESS_LOOPBACK - egress loop prevention
         13.17.3.10 REGBIT_PKT_LARGER - packet larger than MTU
         13.17.3.11 REGBIT_OWN_REPLY - reply to self (local traffic)
         13.17.3.12 REGBIT_NOT_LOCALPORT - traffic not for localport

13.17.4  MLF (Metadata Lookup Field) flags
         13.17.4.1  Concept: tunnel metadata bit flags
         13.17.4.2  MLF_LOCAL_ONLY - prevent inter-chassis tunneling
         13.17.4.3  MLF tunnel metadata encoding 24-bit datapath + 16-bit src port + flags

13.17.5  Geneve TLV class 0x0102 (OVN metadata carriage)
         13.17.5.1  TLV format: 4-byte header + variable payload
         13.17.5.2  Class 0x0102 reserved cho OVN
         13.17.5.3  Encoding: 24-bit logical datapath key + 32-bit (ingress + egress port) + flags
         13.17.5.4  Cross-link 11.0 Geneve packet format byte-by-byte

13.17.6  Anatomy: dump-flows + grep regN
         13.17.6.1  Identify register usage trong flow rule
         13.17.6.2  Map regN value back to OVN concept (LSP UUID, ct_zone, etc.)
         13.17.6.3  Bitmask notation: reg0=0x1/0x1 (REGBIT_PORT_SEC_DROP set)

13.17.7  Anatomy: ovn-trace --detailed register state
         13.17.7.1  Per-stage register snapshot
         13.17.7.2  Flag transition tracing

13.17.8  Hands-on Guided Exercise
         13.17.8.1  Setup 2-VM same LS with ACL deny rule
         13.17.8.2  ovn-trace --detailed → see REGBIT_ACL_HINT change
         13.17.8.3  ovs-ofctl dump-flows br-int | grep reg13 → see ct_zone assignment

13.17.9  Capstone POE
         13.17.9.1  Sinh viên thiết kế new pipeline stage using free reg/REGBIT
         13.17.9.2  Define semantics + safety analysis

13.17.10 Anti-pattern + caveat
         13.17.10.1  KHÔNG override reg13/14/15 trong custom flow (break OVN)
         13.17.10.2  REGBIT renumber giữa OVN minor version → version note

13.17.11 Source code verify (Rule 14)
         - lib/ovn-parallel-hdr.h
         - controller/lflow.c
         - include/ovn/logical-fields.h

13.17.12 Cross-link
         - 4.8 match field catalog (reg0-15)
         - 13.7 physical.c register usage
         - 13.16 pipeline table IDs (reg use per stage)
         - 9.24 conntrack ct_zone

13.17.13 References
         - OVN source branch-22.03
         - ovs-fields(7) man page
```

---

## 6. Files EXPAND (existing, ~10 file)

### 6.1. EXPAND `sdn-onboard/4.8 - openflow-match-field-catalog.md` (+150 dòng, Phase J.4)

**Mục đích thêm:** thêm Anatomy 9-attribute Template B cho 12 match field còn missing/shallow.

**Sections to add:**
```
4.8.X  Match field NEW Anatomy (mỗi field 1 block 9-attribute)
       4.8.X.1  in_phy_port (32 bits, OF 1.2+, OVS 1.7+)
       4.8.X.2  ipv6_flabel (20 bits, OF 1.2+, OVS 1.11+)
       4.8.X.3  ipv6_exthdr (16 bits, OF 1.2+, OVS 1.11+)
       4.8.X.4  pbb_isid (24 bits, PB/VB)
       4.8.X.5  mpls_tc (3 bits) — re-Anatomy nếu hiện shallow
       4.8.X.6  mpls_bos (1 bit) — re-Anatomy
       4.8.X.7  sctp_src/dst (16 bits, OF 1.2+, OVS 2.0+)
       4.8.X.8  tunnel_id / tun_id (64 bits) — re-Anatomy
       4.8.X.9  xreg0-7 (64-bit, OF 1.3+, OVS 2.4+)
       4.8.X.10 xxreg0-3 (128-bit, OVS 2.6+)
       4.8.X.11 nsh_spi, nsh_si, nsh_c1-c4 (NSH RFC 8300 fields, OVS 2.8+)
       4.8.X.12 packet_type (OF 1.5+)
```

### 6.2. EXPAND `sdn-onboard/4.9 - openflow-action-catalog.md` (+200 dòng, Phase J.4)

**Mục đích thêm:** thêm Anatomy 8-attribute Template C cho 10+ action còn missing.

**Sections to add:**
```
4.9.X  Action NEW Anatomy
       4.9.X.1  copy_field (OF 1.5+)
       4.9.X.2  push_pbb / pop_pbb
       4.9.X.3  set_mpls_ttl
       4.9.X.4  copy_ttl_in / copy_ttl_out
       4.9.X.5  dec_mpls_ttl
       4.9.X.6  set_nw_ttl
       4.9.X.7  decap (NSH chi tiết)
       4.9.X.8  encap (NSH chi tiết với md_type=1, tlv())
       4.9.X.9  conjunction (full Anatomy + decision tree)
       4.9.X.10 note (OVS 1.8+)
       4.9.X.11 sample (OVS 2.5+)
       4.9.X.12 controller (continuation-based program OVS 2.6+ với userdata)
```

### 6.3. EXPAND `sdn-onboard/9.4 - ovs-vsctl-mastery.md` (+180 dòng, Phase J.3)

**Sections to add:**
```
9.4.X  Every option Anatomy
       --bare, --dry-run, --retry, --id=@NAME, --if-exists/may-exist/if-not-exists,
       --columns=COLS, --no-headings, --pretty, --syslog-method, --log-file
9.4.Y  Subcommand group Anatomy (mỗi group 1 mini-Anatomy)
       Bridge group, Port group, Interface group, Controller group, Manager group,
       SSL group, Generic database group (list/find/get/set/add/remove/clear/create/destroy/wait-until)
9.4.Z  Anatomy: ovs-vsctl wait-until use case
       - Synchronization in scripts
       - Healthy / Warning / Critical timeout
```

### 6.4. EXPAND `sdn-onboard/9.11 - ovs-appctl-deep-playbook.md` (+100 dòng, Phase J.3)

**Sections to add:**
```
9.11.X Cross-daemon command
       vlog/list, vlog/list-pattern, vlog/set, vlog/close, vlog/reopen
9.11.Y Format option
       --format=text|json + --pretty
       Use case: pipe vào jq cho automation
9.11.Z Target option
       --target path vs pidfile basename
```

### 6.5. EXPAND `sdn-onboard/9.27 - cli-anatomy-template-A-curated.md` hoặc `20.4 - ovs-daily-operator-playbook.md` (+120 dòng, Phase J.3)

**Sections to add:** Anatomy 5-axis cho 13 observability commands còn missing/shallow:
- coverage/show, dpif/show, dpif/dump-flows BR, ofproto/trace, fdb/show,
- bond/show, lacp/show, vlog/list, memory/show, upcall/show,
- dpctl/dump-conntrack, revalidator/wait, revalidator/purge

Mỗi command có Healthy / Warning / Critical threshold + 5-axis.

### 6.6. EXPAND `sdn-onboard/13.0 - ovn-announcement-2015-rationale.md` (+80 dòng, Phase J.5)

**Sections to add:**
```
13.0.X Daemon roster post-2024
       - ovn-controller-vtep
       - ovn-ic + ovn-ic-northd
       - Relay mode ovsdb-server
13.0.Y OVSDB Server roles
       - 3 DBs: OVN_NB, OVN_SB, OVN_IC (optional)
       - Standalone vs replicated vs RAFT cluster
```

### 6.7. EXPAND `sdn-onboard/13.1 - ovn-nbdb-sbdb-architecture.md` (+100 dòng, Phase J.5)

**Sections to add:**
```
13.1.X Inactivity probe
       - external_ids:ovn-remote-probe-interval (ms)
       - Default value + min 1000ms
13.1.Y Northd probe interval
       - NB_Global.northd_probe_interval cho HA failover timing
13.1.Z Leader election state
       - STATUS: active / standby / paused
       - SB_Global lock acquisition
```

### 6.8. EXPAND `sdn-onboard/13.x` schema completeness (+200 dòng total, Phase J.5)

**Files touch:** 13.2 (Logical_Switch + Router), 13.3 (ACL), 13.5 (Port_Binding), 13.9 (Load_Balancer).

**Audit từng table column trong REF Section 3.2** (~50 entry). Mỗi column thiếu 5-axis → add Anatomy block ngắn (~5 dòng).

Cụ thể:
- Logical_Switch_Port: 8 type Anatomy compare matrix (router/localport/localnet/l2gateway/vtep/external/virtual/remote)
- Port_Security: REGBIT_PORT_SEC_DROP + check_in_port_sec() function
- QoS: qos_max_rate + qos_burst → set_queue() OF action
- Requested Chassis: options:requested-chassis hint vs constraint
- Reside-on-Redirect-Chassis: distributed gateway flag
- Logical_Router_Static_Route: ECMP same route_table behavior
- Logical_Router_Policy: priority + match + action + nexthop
- NAT options:stateless: bypass conntrack
- Load_Balancer options:hairpin_snat_ip
- Address_Set $set_name macro

### 6.9. EXPAND `sdn-onboard/13.14 - ovn-nbctl-sbctl-reference-playbook.md` (+200 dòng, Phase J.5)

**Sections to add:**
```
13.14.X All ovn-nbctl options Anatomy
        --db, --no-wait, --wait=hv|sb, --inactivity-probe, --leader-only,
        --no-leader-only, --shuffle-remotes, --ssl-*, --commit-retry,
        --unix-lock, --retry, --timeout, --dry-run, --oneline, --bare,
        --id=@NAME, --if-exists, --may-exist
13.14.Y ovn-trace microflow expression syntax
        - eth.src/dst, ip4.src/dst, tcp.dst, ct.new/est/inv, inport, outport
        - --detailed flag
        - --ovs flag (show OVS flows equivalent)
13.14.Z ovn-detrace deep
        - Cookie → logical flow UUID mapping
        - --ovnnb + --ovnsb option
13.14.W ovn-ic-nbctl + ovn-ic-sbctl
        - ts-add, ts-list, route propagation
```

### 6.10. EXPAND `sdn-onboard/20.2 - ovn-troubleshooting-deep-dive.md` (+300 dòng, Phase J.5 + J.6)

**Sections to add:**
- 20.2.X lflow-cache stats deep
  - lflow-cache/show-stats counter
  - external_ids:ovn-enable-lflow-cache
  - ovn-limit-lflow-cache + ovn-memlimit-lflow-cache-kb
  - ovn-trim-limit-lflow-cache + ovn-trim-wmark-perc

- 20.2.Y inc-engine recompute counter
  - inc-engine/show-stats compute / recompute / cancel
  - High recompute = instability indicator

- (Phase J.6) Distributed scenarios assigned to 20.2 (xem Section 7 dưới)

---

## 7. Distributed troubleshooting scenarios mapping (Phase J.6, NO bundling)

14 scenario REF Section 4 distributed vào file native technology. Mỗi scenario nhận FULL Forensic Anatomy depth (~80–100 dòng/scenario).

| # | Scenario | File native | Section assigned | Δ lines |
|---|----------|-------------|------------------|---------|
| 1 | East-west same-LS fail | `20.2 OVN troubleshoot` | new §20.2.S1 | +90 |
| 2 | North-south DGP blackhole | `20.2 OVN troubleshoot` | new §20.2.S2 | +90 |
| 3 | LB VIP drops new conn | `13.9 OVN Load_Balancer` | new §13.9.S3 | +100 |
| 4 | ovn-controller stuck recompute | `20.0 systematic debug` | new §20.0.S4 | +100 |
| 5 | SB DB connection flap | `10.1 OVSDB Raft` | new §10.1.S5 | +90 |
| 6 | Geneve tunnel down | `11.0 VXLAN/Geneve/STT` | new §11.0.S6 | +90 |
| 7 | Conntrack zone exhaustion | `9.24 OVS conntrack` | new §9.24.S7 | +90 |
| 8 | ovs-vswitchd 100% CPU revalidator | `9.26 revalidator-storm forensic` | EXISTING (verify depth) | +0 (already deep) |
| 9 | OF bundle commit fail | `4.3 OF 1.4 bundles+eviction` | new §4.3.S9 | +90 |
| 10 | Asymmetric ECMP | `13.11 OVN gateway router` | new §13.11.S10 | +100 |
| 11 | Stale MAC_Binding | `20.5 OVN forensic case studies` | new §20.5.S11 | +100 |
| 12 | ovn-northd standby no takeover | `13.0 OVN announcement` (HA section) | new §13.0.S12 | +90 |
| 13 | VM DNS dropped by OVN native | `13.10 OVN DHCP+DNS` | new §13.10.S13 | +90 |
| 14 | Geneve/VXLAN MTU fragmentation | `11.1 MTU/PMTUD/offload` | new §11.1.S14 | +100 |

**Tổng J.6:** ~13 file expand, +1300 dòng total. Mỗi scenario format chuẩn:

```markdown
### §X.Y.S<N> Forensic Anatomy: <scenario name>

**Problem statement.** <symptom + business impact>

**Layered checklist (top-down NB → SB → OF → datapath → tcpdump).**
1. NB topology check
2. SB binding check
3. Logical-flow inspection
4. End-to-end simulation (ovn-trace)
5. OpenFlow on br-int
6. Datapath megaflows
7. Counter + missed packet
8. Capture on br-int

**Likely root-cause categories.** 5–7 root cause với rationale.

**Anatomy: <key command> output interpretation.**
Healthy / Warning / Critical thresholds.

**Cross-link.** Related Part + REF Section 4 entry.
```

---

## 8. PERMANENT BAN handling (per Q1 confirm)

| REF Entry | BAN status | Curriculum action |
|-----------|------------|-------------------|
| DPDK datapath (general) | BAN | Existing 9.3 stays. KHÔNG expand. Mark trong 0.3 §IV. |
| PMD threads, pmd-cpu-mask | BAN | Same |
| EMC (Exact-Match Cache) | BAN | DPDK-specific, BAN. (Concept "exact match" giữ trong 9.7 megaflow context). |
| SMC (Signature Match Cache) | BAN | DPDK-specific, BAN |
| Mempool (rte_mempool, netdev-dpdk/get-mempool-info) | BAN | Same |
| dpif-netdev/pmd-stats-show, pmd-rxq-show, pmd-rxq-rebalance, pmd-perf-show | BAN | Skip Anatomy. Mark "Out of scope" trong 0.3 §I.5. |
| ovs-monitor-ipsec | NOT BAN | Add 5-axis trong 9.x (IPsec là OVS feature, không phải DPDK) |
| Conntrack family, megaflow, recirc, learn, UFID | NOT BAN | Cover deep |
| Microflow concept (general) | NOT BAN | Cover trong 9.7 (vs megaflow) |

Index 0.3 Phần IV liệt kê entry BANNED + rationale + redirect tới REF Section 1.2 + 1.5 cho học bộ riêng (offline study, không phải curriculum).

---

## 9. Sequencing + dependency (per Q5 confirm)

```
J.1 Audit ──┬─→ J.2 Master Index 0.3 ──┬─→ J.3 OVS backfill
            │                           ├─→ J.4 OpenFlow backfill
            │                           └─→ J.5 OVN backfill
            │                               ├─ J.5.c 13.16 + 13.17 LÀM TRƯỚC (foundation)
            │                               ├─ J.5.a 13.15 + 13.0 + 13.1 expand
            │                               ├─ J.5.b 13.x schema completeness
            │                               ├─ J.5.d 13.14 CLI mastery
            │                               └─ J.5.e 20.2 lflow-cache stats
            │                                              │
            │                                              ↓
            └─→ (gap matrix feeds all build phases)   J.6 Distributed troubleshoot
                                                           │
                                                           ↓
                                                      J.7 Validate + Release
```

**Dependency:**
- J.1 BLOCKS all (cần matrix trước build).
- J.2 PARALLELIZABLE với J.3/J.4/J.5 sau J.1. Đề xuất build J.2 skeleton đầu, fill detail iteratively song song với J.3-J.5.
- J.3 / J.4 / J.5 INDEPENDENT.
- J.5.c (13.16 pipeline IDs + 13.17 register) LÀM TRƯỚC trong J.5 vì underpins 13.x schema + observability.
- J.6 cần J.5 (troubleshoot reference OVN concept).
- J.7 cần tất cả phase trước.

**Execution order đề xuất:** J.1 → J.2 (skeleton) → J.3 OVS → J.4 OpenFlow → J.5.c (13.16 + 13.17) → J.5.a → J.5.b → J.5.d → J.5.e → J.6 distributed → J.7.

Lý do J.3 trước J.5: J.3 OVS familiar nhất, build vocabulary + Anatomy template muscle memory trước khi tackle pipeline IDs novel content.

---

## 10. Risk + mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Effort blow-out (>16 session) | MEDIUM | Slow delivery | Mỗi sub-phase độc lập commit, có thể pause sau J.4 nếu thấy đủ. |
| Touching foundation file (4.8, 4.9, 13.x) gây regression | MEDIUM | Curriculum quality | Rule 6 Checklist B trước Edit; Rule 14 source verify; spot check Rule 11 + 13 sau commit. |
| Pipeline table IDs version drift (22.03 vs 24.03) | HIGH | Stale info | Anchor 22.03.8 baseline; annotate version-specific stage names; cross-verify upstream `northd/northd.c` enum `ovn_stage`. |
| User thay đổi BAN giữa phase | LOW | Scope shift | Plan có flag rõ BAN keywords; nếu user lift BAN, add lại các BANNED entry như Tier B work item. |
| Index 0.3 trở thành bloat duplicate REF | MEDIUM | Maintenance burden | Index 0.3 có 5–10 dòng giải thích Vietnamese (deep mode), cross-link tới Part curriculum. KHÔNG copy verbatim REF (REF giữ làm offline source-of-truth English). |
| 13 file expand cho J.6 dễ vỡ Rule 11/13 quality | MEDIUM | Quality gate fail | Run Rule 11 §11.6 sweep + Rule 13 em-dash density sau MỖI scenario expand commit. |
| 14 scenario distributed gây fragmented user experience | LOW | Học viên khó tổng hợp | Index 0.3 có Section 4 cross-link map: scenario → file location. |

---

## 11. Success criteria (acceptance gate cho v3.5-KeywordBackbone)

1. **100% non-banned keyword coverage:** grep từng entry REF Section 1–3 (excl. BAN) trong curriculum → ≥ 1 hit có 5-axis treatment.
2. **64 pipeline table IDs covered:** dedicated file 13.16 với 5-axis cho LS_IN_* + LS_OUT_* + LR_IN_* + LR_OUT_*.
3. **CLI tool every option:** mọi option REF Section 1.4 + 3.4 có Anatomy hoặc 5-axis treatment.
4. **14 production scenarios distributed:** mỗi scenario nằm trong file native technology, có Forensic Anatomy depth.
5. **Master Index 0.3 functional:** mỗi entry có 5-axis 1-line + 5-10 dòng Vietnamese giải thích + working cross-link.
6. **Quality gates:** Rule 9 (null bytes 0), Rule 11 (~99% prose compliance), Rule 13 (em-dash density < 0.10/line per file), Rule 14 (source citation 100% verified).
7. **CLAUDE.md North Star updated:** REF làm backbone reference được mention.
8. **Tag v3.5-KeywordBackbone created + GitHub Release published.**

---

## 12. Effort estimate

| Phase | Session | Note |
|-------|---------|------|
| J.1 Inventory + matrix | 1–2 | Bash + Python scripted |
| J.2 Master Index 0.3 (DEEP ~3000 dòng) | 2 | Phần lớn write content |
| J.3 OVS backfill (4 NEW + 5 EXPAND) | 3 | |
| J.4 OpenFlow backfill (2 NEW + 2 EXPAND) | 3 | 4.8 + 4.9 expand quan trọng |
| J.5 OVN backfill (3 NEW + 4 EXPAND, 13.16 + 13.17 trước) | 4 | 13.16 ~700 dòng nặng nhất |
| J.6 Distributed troubleshoot (13 file expand) | 2 | ~100 dòng/scenario |
| J.7 Validate + Release | 1 | Audit + tag + release |
| **Tổng** | **16** | Mỗi session ~1.5–2 hours per past pace |

So sánh với v3.4: 24 commits trong ~1 working day. v3.5 dự kiến ~1.5–2 working day spread over multiple session.

---

## 13. Trigger để start

User confirm khung sườn này → start J.1 (Audit + matrix).

Sau J.1 xong, plan sẽ được updated với inventory exact (có thể phát hiện entry nhiều/ít hơn ước tính). Khung sườn Phase J.2-J.7 stays as-is unless audit phát hiện gap khác.

> **Ghi chú execution:** Plan này định nghĩa khung sườn (mục lục + mục đích) cho TỪNG file. Content writing (5-axis depth + Anatomy + GE + POE) sẽ thực hiện trong từng phase, mỗi commit độc lập. KHÔNG viết content tổng thể trong 1 commit.

---

## 14. Cross-link với CLAUDE.md rules

- **Rule 1 (Skill Activation):** mỗi session áp Core 4 (professor-style + document-design + fact-checker + web-fetcher). search-first khi viết content NEW. deep-research khi cần multi-source (J.5.c pipeline IDs).
- **Rule 2 (Cross-File Sync):** mỗi commit check `memory/file-dependency-map.md`; thêm file mới sẽ update map sau J.7.
- **Rule 6 Checklist B + C + E:** mỗi sub-phase chạy đầy đủ.
- **Rule 11:** §11.6 sweep cuối mỗi sub-phase. Dictionary `memory/rule-11-dictionary.md` updated nếu phát hiện new prose word.
- **Rule 13:** density check < 0.10/line cuối mỗi sub-phase.
- **Rule 14:** mọi source code citation từ upstream (OVN `branch-22.03`, OVS `v2.17.9`) verified qua MCP GitHub.
- **North Star (PERMANENT BAN):** DPDK/PMD/SMC/EMC/mempool skip 5-axis treatment.
- **Second North Star (Quality > Speed):** verify never estimate, real output only, explanation-heavy ratio ≥ 1.5.
