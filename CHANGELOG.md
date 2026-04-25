# Changelog — network-onboard

Training curriculum cho kỹ sư mạng: OpenvSwitch + OpenFlow + OVN. Focus sâu 5 trụ cột: nền tảng kiến thức, tools mastery, output interpretation, debug + troubleshoot, architecture + mechanism.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) adapted cho training series.

---

## v3.4-DeepFoundation (2026-04-25)

**Release type:** Foundation depth consolidation, tier 2 source-code internals across Block VIII (Linux primer), Block X (OVSDB), Block XI (Overlay), plus Block IX/XIII completion + critical bug fixes.

**Branch:** `docs/sdn-foundation-rev2`
**Base:** v3.3-ArchitectMaster + 23 commits.
**Effort:** Multiple working sessions.

### Mục tiêu

Đóng gap tier 2 source-code level depth cho mọi file foundation in-scope (excluding permanently-banned topics: DPDK/BPF/XDP/BGP/K8S). Curriculum đạt comprehensive coverage tier 2 cho 5 trụ cột mission core.

### Major directives

**2026-04-25 PERMANENT BAN directive:** DPDK, BPF/eBPF, XDP/AF_XDP, BGP, K8S excluded from active plan. Existing content stays as-is, no expansion. CLAUDE.md North Star + memory feedback files codify rule.

### Changes

**Critical bug fix (1 commit):**

- **`5944827` Part 0.2 truncation fix**: 56 → 460 dòng. Foundation anchor referenced từ 5+ Phần Phase G + I (9.25, 9.27, 13.7.8, 20.0, 20.7) trước đây kết thúc giữa câu "12 giai đoạn chi tiết:". Fixed bằng 12-stage packet journey complete + diagnostic workflow + GE + key takeaways.

**Block XI Overlay tier 2 (3 commits, +893 lines):**

- `7064d20` 11.0 VXLAN/Geneve/STT: 213 → 551 (+338). Geneve packet format byte-by-byte, IANA TLV class registry (OVN class 0x0102), header overhead math, NIC offload matrix.
- `673299b` 11.1 MTU/PMTUD/offload: 213 → 517 (+304). PMTUD packet flow IPv4+IPv6, PMTU black hole 5 root cause, TCP MSS clamping, OVN check_pkt_larger source.
- `5868137` 11.2 BGP EVPN: 157 → 408 (+251). Type 2 NLRI byte-by-byte, Type 3/4/5 deep, IRB modes, OVN integration use cases. **Note: BGP banned from future expansion per directive.**

**Block VIII Linux primer tier 2 (4 commits, +876 lines):**

- `47df050` 8.0 namespaces+cgroups: 194 → 382 (+188). clone/unshare/setns syscall internals, lifecycle ref counting, OVS daemon namespace pattern.
- `2d94b87` 8.1 bridge+veth+macvlan: 254 → 430 (+176). veth driver source (`net/core/veth.c`), bridge forwarding logic, OVS internal port comparison.
- `5dba35b` 8.2 VLAN+bonding+team: 182 → 426 (+244). bonding LACP 4-substate state machine, xmit_hash_policy, OVS bond comparison.
- `7279a3b` 8.3 tc+conntrack: 207 → 475 (+268). Kernel queueing path, HTB token bucket source, nf_conntrack hash table + zone implementation.

**Block X OVSDB tier 2 (1 commit, +429 lines):**

- `ddba050` 10.0 OVSDB schema RFC 7047: 196 → 625 (+429). Wire protocol byte-by-byte, 10 operations deep với JSON example, monitor + monitor_cond + monitor_cond_since evolution, IDL synchronization model, schema evolution flow.

**Block IX OVS internals tier 2 (3 commits, +671 lines):**

- `534e95a` 9.17 perf benchmark: 276 → 538 (+262). Hot path source mapping (kernel + userspace), coverage counter mapping, NUMA + cache locality methodology.
- `2352f3d` 9.19 flow table granularity: 278 → 521 (+243). Microflow vs Megaflow trade-off, wildcard mask design, match field cardinality.
- `16628df` 9.13 libvirt+docker: 202 → 561 (+359). libvirt-OVS protocol contract, Docker netns lifecycle, production security baseline expand.

**Sequence H, OVN core completion (3 commits, +550 lines):**

- `9677733` 13.9 OVN Load_Balancer: 218 → 451 (+233). `ct_lb` action source, Service_Monitor SBDB schema, distributed health check.
- `c553594` 13.10 OVN DHCP+DNS: 327 → 492 (+165). `put_dhcp_opts` + `dns_lookup` action source, NBDB→SBDB compile flow.
- `dffb24e` 13.12 OVN IPAM: 254 → 406 (+152). `ipam_get_unused_ip()` algorithm, MAC generation, IPv6 EUI-64 mode.

**Sequence O, OVS pure completion (3 commits, +533 lines):**

- `2c2e27c` 9.0 OVS history: 258 → 419 (+161). Timeline 17 năm version-by-version, NSDI 2015 + 2020 papers deep.
- `5e10344` 9.18 native L3 routing: 317 → 493 (+176). `dec_ttl` source, ECMP `multipath()`, 3-stage routing pattern.
- `e89a88c` 9.20 VLAN access+trunk: 337 → 533 (+196). `vlan_mode` 4 type source, push_vlan/pop_vlan action, QinQ 802.1ad deep.

**Meta (4 commits):**

- `0f04ed8` CLAUDE.md add BGP to out-of-scope (LOWEST priority).
- `4fa24a4` CLAUDE.md consolidate 5-tier priority hierarchy.
- `67090c8` CLAUDE.md elevate to PERMANENT BAN cho DPDK/BPF/XDP/BGP/K8S.
- `f62ab05`, `19aaad6` tracker updates.

### Statistics (v3.4 delta from v3.3)

- **20 files modified, 23 commits.**
- **+4,687 lines, -110 lines = +4,577 net.**
- Curriculum: 119 files unchanged, ~57,800 → **~61,826 lines** (+~4K).
- Block VIII Linux primer: ~837 → 1,713 lines (+105% growth).
- Block X OVSDB: ~2,996 → 3,425 lines.
- Block XI Overlay: ~2,196 → 3,089 lines.
- Block XIII OVN: ~6,028 → 6,838 lines.

### Curriculum state post-v3.4

- **HIGHEST tier (OVS+OpenFlow+OVN core internals):** All files DONE tier 2.
- **HIGH tier (Tools mastery + debug):** All DONE.
- **MEDIUM tier (Foundation prerequisites):** All DONE.
- **LOW tier (history + DC applied):** Stays at current depth (intentional, per North Star "foundation depth first" + relevance analysis).

5 pillars coverage:

- **#1 Foundational knowledge:** OVS + OpenFlow + OVN tier 2 source-code level. ~50+ Anatomy Template A.
- **#2 Tools mastery:** 9.4 + 9.11 + 13.14 + 10.7 + 20.x reference playbooks complete.
- **#3 Output interpretation:** 50+ Anatomy với Healthy/Warning/Critical thresholds.
- **#4 Debug + troubleshoot:** Decision tree (9.14, 20.0, 20.2), tracing gradient (20.7), forensic case studies (9.26, 20.5).
- **#5 Architecture + mechanism:** Source-code level cho xlate, classifier, revalidator, raft, northd, controller, encap, IPAM, LB, DHCP+DNS.

### Permanently banned (since 2026-04-25)

DPDK, BPF/eBPF, XDP/AF_XDP, BGP-related, K8S deep. Existing content (9.3, 11.2, 14.x, 15.x, 16.x, 17.0-19.0) stays as-is, no expansion.

### Quality gates maintained

- Rule 9 null bytes: 0 regressions.
- Rule 11 prose: ~99% compliance, 60+ fixes during expand.
- Rule 13 em-dash density: all expanded files < 0.10/line.
- Rule 14 source code citations: all verified upstream (`branch-22.03` OVN, `v2.17.9` OVS, Linux `v5.15`).

### Links

- v3.4 commits: `5944827` → `e89a88c` (23 commits sequential, plus meta + tracker).

---

## v3.3-ArchitectMaster (2026-04-25)

**Release type:** Minor release, Architecture Master tier 2 source-code internals + tools mastery + debug pedagogical gradient.
**Branch:** `docs/sdn-foundation-rev2`
**Base:** v3.2-FullDepth + Phase I 6-session execution (Sequence A 3 expand + Sequence B 3 NEW).
**Effort:** 1 working session (after audit-first recalibration, original 8 sessions reduced to 6).

### Mục tiêu

Đưa curriculum từ "Operator Master" + "Full Depth" tiến sang **Architect Master** với tier 2 = source-code level depth của OVN/OVS/OVSDB. Đầu tiên audit Phase I plan original (8 session) phát hiện 2 session redundant với Phase H/G work đã có; recalibrate xuống 6 session focused. Sau đó execute từng session với Rule 14 source-code citation verified upstream qua `gh api` cho mỗi function name + line number.

### Audit-first recalibration

| Original plan (Phụ lục J) | Audit verdict | Action |
|--------------------------|---------------|--------|
| S64 9.15 classifier expand | SKIP (đã tier 2 từ Phase H S45: cls_subtable + cmap + minimask + Patricia trie) | Loại |
| S65a 9.16 + revalidator URCU | SKIP (plan misaligned: revalidator nằm ở 9.2; 9.16 đã 433 dòng đủ) | Loại |
| S65b 10.1 OVSDB Raft expand | EXECUTE HIGH | Giữ (rename S66' Phase I.A3) |
| S66 13.8 northd build_lflows | EXECUTE HIGHEST | Giữ (S64' Phase I.A1) |
| S67 13.7 physical.c + Geneve TLV | EXECUTE HIGH | Giữ (S65' Phase I.A2) |
| S68 13.3 build_acls walkthrough | OPTIONAL minor | Defer (562 dòng đã dense) |
| S69 13.14 NEW ovn-nbctl/sbctl | EXECUTE HIGH | Giữ (S67' Phase I.B1) |
| S70 10.7 NEW ovsdb-client deep | EXECUTE HIGH | Giữ (S68' Phase I.B2) |
| S71 20.7 NEW tracing gradient | EXECUTE MEDIUM | Giữ (S69' Phase I.B3) |

Effort: 8 sessions → 6 sessions (25% reduction từ 2 SKIP với rationale).

### Changes

**Sequence A: OVN core source-code internals (3 commits, expand existing files)**

1. **S64' Part 13.8 ovn-northd build_lflows tier 2** (`05372ab`): 260 → 465 dòng (+205).
   - §13.8.5 source code: `main()` → `inc_proc_northd_run()` → `en_northd_run()` → `ovnnb_db_run()` → `build_lflows()` walkthrough.
   - §13.8.6 I-P engine cho northd (22.06+): DAG 2 node `en_northd` + `en_lflow`. Anatomy `inc-engine/show` 7-attribute.
   - §13.8.7 Parallel build internals: `build_lflows_thread()` worker, dp-groups merge.
   - §13.8.8 Capstone POE: `--n-threads=8` không luôn cải thiện latency.
   - Source verified `branch-22.03`: `northd/ovn-northd.c` (1022 dòng), `northd/inc-proc-northd.c` (296 dòng), `northd/northd.c` (15947 dòng).

2. **S65' Part 13.7 ovn-controller physical.c tier 2** (`16e2cdd`): 491 → 657 dòng (+166).
   - §13.7.8 source `controller/physical.c`: `physical_run()` → `consider_port_binding()` per type → `consider_mc_group()` + `put_encapsulation()` Geneve TLV class 0x0102.
   - Logic claim Port_Binding với race condition cross-chassis (eager claim 22.03 vs atomic `requested_chassis` 22.06+).
   - Geneve TLV encoding: `MFF_TUN_ID` 24-bit tunnel_key + `mff_ovn_geneve` 32-bit outport + 15-bit inport.
   - Anatomy `debug/dump-local-bindings` 7-attribute + 3 kịch bản bẻ gãy.
   - GE Geneve TLV trace 2-chassis với tcpdump + decode byte-by-byte.

3. **S66' Part 10.1 OVSDB Raft tier 2** (`69e4ad3`): 199 → 412 dòng (+213).
   - §10.6.1 Public API: lifecycle / state queries / write API / 3 role transitions.
   - §10.6.2 AppendEntries + heartbeat + election: `raft_send_append_request()`, `raft_handle_append_request()`, election timeout random hoá.
   - §10.6.3 Log compaction + snapshot: threshold tự động + `raft_save_snapshot()` + install snapshot RPC.
   - §10.6.4 Edge case bầu leader: split vote / network partition / asymmetric partition.
   - §10.6.5 Anatomy `cluster/status` 10-attribute.
   - Capstone POE: tăng `election_timer` không luôn cải thiện stability.
   - Source verified OVS `v2.17.9`: `ovsdb/raft.c` (5041 dòng), `ovsdb/raft.h` public API.

**Sequence B: Tools mastery + debug pedagogy (3 commits, new files)**

4. **S67' Part 13.14 NEW ovn-nbctl/sbctl reference playbook** (`6abf663`): 660 dòng.
   - Sister cho 9.11 `ovs-appctl` (1170 dòng).
   - 97 lệnh ovn-nbctl chia 12 nhóm: Generic / LS+LSP (28) / LR+LRP (28) / ACL / PG / LB / DHCP / QoS+Meter / HA Chassis / CoPP / Connection / SSL / OVSDB primitives.
   - 15 lệnh ovn-sbctl: chassis lifecycle / lsp-bind / lflow-list / connection.
   - 10 Anatomy Template A: show / list Chassis / Port_Binding / lflow-list / lr-route-list / acl-list / lb-list / ha-chassis-group-list / nb_cfg / find Port_Binding.
   - Decision matrix 11 row scenario → command.
   - GE multi-tier tenant T1 (web+db) + Capstone POE Rule 5 trụ cột (anti-pattern `ovsdb-client transact` cho ý đồ logical).
   - Source verified `branch-22.03`: `utilities/ovn-nbctl.c` (7244 dòng, 97 cmd), `utilities/ovn-sbctl.c` (1528 dòng, 15 cmd).

5. **S68' Part 10.7 NEW ovsdb-client deep playbook** (`6c175cf`): 589 dòng.
   - Companion cho 13.14, focus low-level RFC 7047 JSON-RPC tool.
   - 7 nhóm chức năng: schema introspection / query+dump / transaction / monitoring (3 variant) / coordination (wait+lock) / backup+restore / schema convert.
   - 5 Anatomy: monitor event stream với `--timestamp` / dump table / list-dbs / get-schema JSON / transact JSON-RPC response.
   - Decision matrix 9-row: ovsdb-client vs ovn-nbctl vs ovn-sbctl vs ovs-vsctl. Anti-pattern list.
   - GE forensic Port_Binding migration race với `monitor --timestamp` (cross-link Phase G.2.3 case study).
   - Capstone POE: `transact` không nhanh hơn `ovn-sbctl` cho 1 thao tác.
   - Source verified `v2.17.9`: `ovsdb/ovsdb-client.c` (2534 dòng).

6. **S69' Part 20.7 NEW packet flow tracing tutorial gradient L1-L5** (`a2cf3e1`): 691 dòng.
   - Sư phạm gradient từ hello-world tới production forensic.
   - L1 hello-world `ovn-trace` 1 LS đơn / L2 `--detailed` ACL stateful interplay ct_next 2-pass / L3 cross-subnet xuyên 3 datapath với routing+ARP / L4 multichassis Geneve combine `ovn-trace` + `ofproto/trace` / L5 production incident `ovn-detrace` chain với NBDB row UUID.
   - 5 Anatomy + 5 Exercise + 1 Capstone POE Phase I.B3.
   - ASCII decision tree workflow chọn level (3 câu hỏi).
   - Cross-link 9.25 / 9.27 / 13.7.8 / 13.8.5-8 / 20.0 / 20.2 / 20.3 / 20.5.

### Quality gates

| Rule | Result |
|------|--------|
| Rule 9 null bytes | 0/6 file |
| Rule 11 prose | 22 fix tổng (operator/Operator/engineer/Production engineer/verify/Verify/Inspect/inspect → người vận hành/kỹ sư/kiểm chứng/kiểm tra) |
| Rule 13 em-dash density | 0.0014-0.0320/line, all 6 files well below 0.10 target |
| Rule 14 source code citation | All function names + line numbers verified upstream via `gh api` at `branch-22.03` (OVN) + `v2.17.9` (OVS) |

**Source-code anchor density** (vs baseline 0):
- 13.8: 41 mention (`northd.c`, `build_lflows`, `inc-engine`, `ENGINE_NODE`, `ovnnb_db_run`)
- 13.7: 27 mention (`physical.c`, `physical_run`, `consider_port_binding`, `put_encapsulation`, `GENEVE`, `TLV`, `0x0102`)
- 10.1: 21 mention (`raft.c`, `raft_run`, `raft_become_*`, `raft_handle_*`, `raft_send_*`, `raft_install_*`, `raft_command_*`)
- 13.14: 105 mention (Anatomy / ovn-nbctl / ovn-sbctl / Port_Binding / Logical_Switch / Capstone)

### Statistics (v3.3 delta from v3.2)

- **6 files modified/created** (3 expand + 3 new)
- **+584 lines expand + +1940 lines new = +2524 net** (excluding minor doc/CHANGELOG/tracker updates)
- Block X: 7 → 8 files (added 10.7)
- Block XIII: 14 → 15 files (added 13.14)
- Block XX: 7 → 8 files (added 20.7)
- Curriculum: 116 → 119 files, ~55.7K → ~57.8K dòng

### Audit-first lessons

- Plan inaccuracies caught by `gh api` verification: `build_lswitch_and_lrouter_lflows` không tồn tại tại `branch-22.03`; actual function là `build_lflows`. Đã correct trong write.
- Plan scope mismatch: revalidator URCU thuộc Part 9.2, không phải 9.16 connmgr. Đã skip session sai location.
- Plan over-scope: 9.15 đã đạt tier 2 từ Phase H S45 với đầy đủ source-code anchor. Đã skip để tránh redundant work.
- Tổng tiết kiệm: 25% effort qua audit-first.

### Curriculum state post-v3.3

- **119 files** sdn-onboard/*.md
- **~57.8K lines**
- 5 trụ cột coverage maintained:
  - Pillar 1 (foundational knowledge): tier 2 source-code added
  - Pillar 2 (tools mastery): 3 reference playbook (9.11 ovs-appctl, 13.14 ovn-nbctl/sbctl, 10.7 ovsdb-client)
  - Pillar 3 (output interpretation): 41 Anatomy Template A across curriculum
  - Pillar 4 (debug + troubleshoot): packet tracing gradient L1-L5 + forensic case studies
  - Pillar 5 (architecture + mechanism): source-code level (xlate, classifier, revalidator, raft, northd, controller, encap)

### Links

- v3.3 commits: `05372ab` → `a2cf3e1` (6 commits sequential, plus tracker updates)
- Phase I plan: `plans/sdn-foundation-architecture.md` Phụ lục J
- Audit gate session log: `memory/session-log.md`

---

## v3.2-FullDepth (2026-04-25)

**Release type:** Minor release — audit residual content depth expansion.
**Branch:** `docs/sdn-foundation-rev2`
**Base:** v3.1.1-OperatorMaster-patch + 5 deferred audit findings resolved.
**Effort:** 1 working session (sequential P1→P5 priority execution).

### Mục tiêu

Đóng toàn bộ residual finding đã defer từ v3.1.1 patch — chuyển từ curriculum "operator mastery" sang "full depth mastery" với Block XIII Core đạt parity depth cùng Block IX + Block XX, tất cả CLI reference file có Anatomy Template A consistent, và narrative file Block II có Hiểu sai callout đạt professor-style 5/6 criteria.

### Changes

5 priority commits addressing all residual findings:

1. **P1 Block XIII Core expand** (7 commits `e3109ea` → `737980f`, audit P4.B13.1 CRITICAL + P4.B13.4 + P4.B13.5):
   - `13.0` OVN announcement 2015: 153 → 337 (+184) — author deep-dive Pfaff/Pettit/Shuhaa, 3 kỹ thuật + 2 thương mại motivation, 3-tier kiến trúc expanded, 4 alternative comparison, evolution timeline, GE 3-tier compilation.
   - `13.1` NBDB/SBDB schema: 505 → 624 (+119) — Anatomy Template A `ovn-nbctl show` + `list Datapath_Binding`, 2 Hiểu sai + Key Topic, GE NBDB→SBDB timing propagation.
   - `13.2` LS+LR pipeline: 399 → 546 (+147) — Anatomy `ls-list` + `lflow-list`, 2 Hiểu sai + Key Topic 27+10 stage, Capstone POE 3-tier ping trace.
   - `13.3` ACL + Port_Group: 411 → 563 (+152) — Anatomy `ovn-nbctl acl-list` 9-attr, 2 Hiểu sai + Key Topic scale, Capstone POE 1000-VM segmentation.
   - `13.4` br-int deep: 142 → 566 (+424) — CRITICAL expansion: 3-bridge pattern, patch port `ovs_vport_receive()` tail-call, 4 failure modes, 2 GE + Capstone POE TCAM utilization.
   - `13.5` Port_Binding 8 types: 182 → 455 (+273) — claim mechanism Raft propagation, Anatomy `list Port_Binding`, GE claim workflow, 5-step debug diagnostic.
   - `13.6` HA_Chassis + BFD: 184 → 469 (+285) — RFC 5880 packet format + state machine + timing math, Anatomy `ovs-appctl bfd/show` 11-attr, 13-step failover timeline, 4 failure modes, 11-step Capstone.
   - **Block XIII Core total: 1,976 → 3,560 (+1,584, +80% growth)**

2. **P2 Block IX Ops expand** (5 commits `5242de1` → `4cdb2ff`, audit P4.B9.2 MED):
   - `9.6` bonding+LACP: 162 → 297 (+135) — Anatomy `bond/show` 10-attr, 2 Hiểu sai, 4 failure modes, performance table.
   - `9.7` port mirroring: 154 → 275 (+121) — Anatomy `list Mirror` 9-attr, 2 Hiểu sai, 4 failure modes, retention planning table.
   - `9.8` flow monitoring sFlow/IPFIX: 152 → 252 (+100) — Anatomy `list sFlow` 9-attr, 2 Hiểu sai, capacity planning.
   - `9.10` TLS/PKI: 174 → 258 (+84) — Anatomy `list SSL` 9-attr, 2 Hiểu sai, 4 failure modes.
   - `9.12` upgrade/rolling restart: 172 → 248 (+76) — Anatomy pre-upgrade checklist 9-attr, 2 Hiểu sai "golden 3 rules", 4 failure modes.
   - **Block IX Ops total: 814 → 1,330 (+516, +63% growth)**

3. **P3 Block IV hands-on GE** (1 commit `1d192ef`, audit P4.B4.1 HIGH):
   - `4.0` multi-table pipeline GE (+59 dòng)
   - `4.1` OXM TLV ARP + TCP flags GE (+43)
   - `4.2` meter rate-limit GE (+42)
   - `4.3` bundle atomic GE (+50)
   - `4.4` egress simulation GE (+47)
   - `4.5` TTP capability discovery GE (+38)
   - **Block IV hands-on total: +279 dòng** (implement flow với OVS cho từng OF version feature).

4. **P4 CLI Anatomy standardize** (1 commit `9978e2e`, audit P5.C1 MED):
   - `20.0` §20.X `ovs-appctl coverage/show` debug entry 9-attr + 4 kịch bản (+27).
   - `20.1` §20.X ACL audit + port_security multi-command 9-attr + 4 kịch bản (+48).
   - `9.27` §9.27.7 `tnl/ports/show` + `bfd/show` cross-host tunnel 9-attr + 4 kịch bản (+38).
   - **Anatomy Template A standardize total: +112 dòng** — curriculum-wide pattern consistent.

5. **P5 Block II narrative enhance** (1 commit `0da3996`, audit P6.N1 MED):
   - `2.0` DCAN/OPENSIG/GSMP: 2 Hiểu sai (OpenFlow phát minh mới 2008 + idea sai vs technology sai).
   - `2.1` Ipsilon/Active Networking: 2 Hiểu sai (AN là tiền thân SDN + Ipsilon = GSMP lỗi).
   - `2.2` NAC/Orchestration/Virtualization: 2 Hiểu sai (NAC = SDN + vDS = SDN đầu tiên).
   - **Block II narrative total: +12 dòng** compact Hiểu sai callout. Đạt professor-style 5/6 criteria.

### Finding status (v3.2 closure)

| Severity | v3.1.1 deferred | v3.2 resolved | Residual |
|----------|----------------|---------------|----------|
| CRITICAL | 1 (P4.B13.1) | 1 | 0 |
| HIGH | 2 (P4.B4.1 + P4.B13.2) | 2 | 0 |
| MED | ~5 (P4.B9.2 + P5.C1 + P6.N1 + decision matrix) | 4 | 1 (stylistic, LOW-impact) |
| LOW | ~4 | 2 | 2 (Part X.Y.Z terminology cosmetic) |

**100% CRITICAL + HIGH closure.** Curriculum đạt verdict **A** post-audit (từ A- v3.1.1).

### Statistics (v3.2 delta from v3.1.1)

- **28 files modified** across 15 commits
- **+3,373 insertions, -321 deletions** = +3,052 net
- Block XIII Core: 7 file, 1,976 → 3,560 (+1,584, 80% growth)
- Block IX Ops: 5 file, 814 → 1,330 (+516, 63% growth)
- Block IV hands-on: 6 file +279 (GE sections)
- Anatomy standardize: 3 file +112
- Block II narrative: 3 file +12
- Anatomy Template A (9-attribute + "red flag" + diagnostic hint) applied to: 10 new locations
- Hiểu sai callout: 16 new (Block II 6 + Block XIII 10)
- Guided Exercise: 11 new (Block IV 6 + Block XIII 3 + Block IX 2)
- Capstone POE: 4 new (Block XIII 4)
- Rule 9 null byte: 0 regressions
- Rule 11 prose: maintained 99%+ compliance
- Rule 13 em-dash density: 0/28 files in warn zone (>0.10)

### Curriculum state post-v3.2

- **116 file** sdn-onboard/*.md (unchanged count, depth expansion only)
- **~55.7K dòng** (from ~52.6K baseline v3.1)
- Block XIII Core: 13 file, parity depth với Block IX + Block XX
- Anatomy Template A presence: Part 9.4/9.11/13.2/13.3/20.1/20.0/9.27 + all Block XIII Core (consistent pattern)
- Professor-style 5/6 criteria: 100% narrative file (Block I + II + III) có Hiểu sai + Key Topic callout

### Known residual (defer post-v3.2)

- **P7.R1 LOW**: Part X.Y.Z terminology normalization across ~8 legacy file headers. Cosmetic, non-blocking.
- **P4.B9.3 LOW**: 9.26 References section sub-heading format. Cosmetic.
- **Lab verification (C1b)**: 63 exercise pending lab host availability. External dependency.

### Links

- Audit master report: [`memory/audit-2026-04-25-master-report.md`](memory/audit-2026-04-25-master-report.md)
- v3.2 commits: `e3109ea` → `0da3996` (15 commits sequential)

---

## v3.1.1-OperatorMaster-patch (2026-04-25)

**Release type:** Patch release — audit compliance remediation.
**Branch:** `docs/sdn-foundation-rev2`
**Base:** v3.1-OperatorMaster + audit 2026-04-25 9-phase master report + 7 patch commits.
**Effort:** 1 working session post-audit.

### Audit 2026-04-25 context

Post-release comprehensive audit (9-phase) ngay sau tag v3.1. Tìm thấy 1 CRITICAL + 7 HIGH + 30 MED + 17 LOW + 13 STRONG positive finding. Verdict: curriculum production-ready GPA A-. v3.1.1 patch sprint address tất cả HIGH findings ngoại trừ những điểm content-level deferred sang v3.2.

### Changes

7 commits addressing findings từ audit Phase 1-8:

1. **P1.1 Dependency map backfill** (b542de5): 44 file content-phase (5 block VII/VIII/XII/XIV/XV từ 0% → 100% coverage). Rule 2 Cross-File Sync: 62% → ~95%. Line count + section count verified thực tế qua `wc -l` + grep.
2. **P1.2 Rule 11 prose Group A** (db49646): ~50 hit clear prose leak fixed across 40 file. Categories: approach → cách tiếp cận, flexibility → tính linh hoạt, motivation → động cơ, adoption → sự chấp nhận, paradigm → mô hình, convention → quy ước, postmortem → báo cáo hậu sự, troubleshoot → khắc phục sự cố, scalability → khả năng mở rộng, senior → kỳ cựu.
3. **P1.3 Rule 11 Group B manual triage** (cf93aa0): ~13 case-specific hit trong decision matrix + table labels. 16.2 Capstone decision matrix normalized Vietnamese labels. Table column headers 5.0/14.1/14.2 translated.
4. **P2.1 6 dead URL + README heading + S61b regression** (61f3000):
   - Dead URL fix: Network Heresy → wordpress.com, Stanford CS244 Ethane → yuba.stanford.edu, Princeton 4D → /ccr05-4d.pdf (Rexford reorganized), NVIDIA DOCA → /doca/sdk/, ONF press archive, p4.org/specs → p4lang/p4-spec.
   - README heading: Block IX 27→28, Block XX 6→7, total 20 block.
   - S61b regression restore: "Comprehensive Approach" book title (8 file), "OpenFlow Switch Specification Version" (12 instance), "High-Performance" (3 instance).
   - CLAUDE.md Rule 14 example clarify.
5. **P3.1 Memory + README + Mermaid** (26c4526):
   - `memory/sdn-series-state.md` (new 300 dòng, Rule 5 Session Handoff Protocol)
   - `memory/audit-index.md` (new, TOC of audit logs)
   - Parent `README.md` SDN section: +Block XX + Expert Extension summary + 12 new links (20.x + 9.26/9.27 + 14.x + 15.0 + 16.x).
   - `sdn-onboard/README.md`: 6 reading path → **7** (path 7 "Operator daily runbook" 30-50h). Mermaid graph: +P20 node (ops class green thick border) + 2 arrows.
6. **P4.1 Cosmetic cleanup** (b68dad5):
   - Paul Göransson diacritic fix (32 file) — "Goransson" → "Göransson".
   - CRLF → LF normalize (41 file regression from Task #6 Python script encoding).
   - Trailing whitespace strip.
   - Decimal separator "1,26 tỷ" (VN convention).
7. **P5.1 Man page backfill** (f08c8db):
   - 9.14 incident-response +11 man page (ovs-vswitchd, ovs-appctl, ovs-ofctl, ovs-dpctl, ovsdb-tool, conntrack, ethtool, ip-link, ovs-bugtool, ovs-pcap, ovs-testcontroller).
   - 20.1 security-hardening +7 man page (ovs-pki, ovsdb-server/client, openssl-s_client, ovn-nbctl/sbctl, ovn-trace, auditd) + RFC 5280 PKIX.
   - References section reorganized thành sub-heading (Documentation / Man pages / Standards).
   - inc-engine/show-stats verified upstream canonical naming.

### Finding status

| Severity | Count | v3.1.1 resolved | Deferred v3.2 |
|----------|-------|----------------|---------------|
| CRITICAL | 1 | 0 | 1 (P4.B13.1 Block XIII Core content expansion) |
| HIGH | 7 | 5 | 2 (P4.B4.1 Block IV hands-on + P4.B13.2 Block XIII 0 POE — content level) |
| MED | 30 | 25+ | ~5 (P4.B9.2 Block IX Ops expand + P4.B13.4 13.4 br-int expand + decision matrix stylistic) |
| LOW | 17 | 13+ | ~4 (P7.R1 Part X.Y.Z terminology + P4.B9.3 9.26 References heading) |

### Known residual (defer v3.2)

- **P4.B13.1 CRITICAL**: Block XIII Core (13.0-13.6) content expansion (+2000 dòng, 20-30h effort). Target v3.2-FullDepth.
- **P4.B4.1 HIGH**: Block IV 4.0-4.5 hands-on GE (6 file). Target v3.2.
- **P4.B9.2 MED**: Block IX Ops 9.6/9.7/9.8/9.10/9.12 expand (+1200 dòng). Target v3.2.
- **P5.C1 MED**: 20.0/20.1/9.27 Anatomy Template A standardize. Target v3.2.
- **P6.N1 MED**: Block II 2.0/2.1/2.2 phản biện + Hiểu sai callout. Target v3.2.

### Statistics (v3.1.1 delta)

- 47 file modified across 7 commits
- 570+ insertions, 540+ deletions (most cosmetic)
- 2 new memory files (sdn-series-state + audit-index)
- Rule 2 Cross-File Sync: 62% → ~100% (expected post backfill)
- Rule 11 Vietnamese prose: ~95% → ~99%
- Rule 9 null byte: 0 regressions maintained
- Rule 13 em-dash density: 0 warn zone introductions
- Dead URL: 6 → 0

### Links

- Audit master report: [`memory/audit-2026-04-25-master-report.md`](memory/audit-2026-04-25-master-report.md)
- Per-phase reports: `memory/audit-2026-04-25-phase1-8-*.md`
- v3.1.1 commits: `b542de5` → `f08c8db` (7 commits sequential)

---

## v3.1-OperatorMaster (2026-04-24)

**Release type:** Foundation + Operator Mastery complete.
**Branch:** `docs/sdn-foundation-rev2`
**Scope curriculum:** 116 file `sdn-onboard/*.md`, ~52.6K dòng content.
**Lab verification:** pending (C1b — chờ user cung cấp lab host).

### Highlights

- **Phase G Operator Master 5/5 area COMPLETE** (S37a-c + S51-S59):
  - G.1 Truy vết: Part 9.25 ofproto/trace expansion + Part 9.27 packet journey end-to-end + Part 13.7 ovn-controller run loop deep + Part 20.0 case study playback.
  - G.2 Xử lý sự cố: Part 9.14 20-symptom decision tree expansion + Part 20.5 OVN forensic 3 case study (Port_Binding migration race / northd bulk delete / MAC_Binding explosion).
  - G.3 Debug sâu: Part 9.26 OVS revalidator storm forensic 3 case study + Part 20.1 security hardening 4-layer audit trail + Part 20.2 OVN troubleshooting deep-dive.
  - G.4 Lịch sử: Part 20.6 reflective retrospective 2007-2024 (17 năm SDN, 10 meta-lesson universal).
  - G.5 Thao tác công cụ: Part 20.3 OVN daily operator playbook + Part 20.4 OVS daily operator playbook.
- **Phase H Foundation Depth 13 session COMPLETE** (S38-S50):
  - Template library A/B/C/D trong `sdn-onboard/_templates/`.
  - Full OpenFlow match field catalog (Part 4.8) + action catalog (Part 4.9) với 100% spec coverage.
  - Full OVN pipeline exhaustive (ls_in_*/ls_out_*/lr_in_*/lr_out_*) trong Part 13.2+13.11.
  - OVS internals tier 1 expand (Part 9.1 + 9.15 + 9.16) với classifier TSS + connection manager + ofproto-dpif deep.
  - Tools coverage closed: ovs-bugtool + ovs-pcap + ovs-testcontroller.
- **Phase E Fact-check audit 101 file** (S32-S33i): Rule 14 Source Code Citation Integrity codified.
- **Phase F Cloud Native partial** (S36a-g): Block XIV (P4), Block XVI (DPDK+AFXDP), Block XV partial (Service Mesh 15.0 only, 15.1+15.2 deferred per user directive).
- **Pre-release audit** (S60-S61):
  - Rule 9 null byte: PASS 0/116.
  - Rule 13 em-dash density < 0.10: PASS 0/116.
  - Rule 11 Vietnamese prose: 185/295 leak fixed (63% reduction). 110 residual trong spec/table/numbered step contexts, defer v3.1.1 patch release.
  - Rule 14 source code citation: spot-check PASS.

### Statistics

| Metric | Count |
|--------|-------|
| Total file | 116 |
| Total line | ~52.641 |
| Block (foundation 0-XIII + extension XIV-XVI + forensic XVII-XIX + operations XX) | 20 |
| Guided Exercises + Capstone POE | 60+ |
| Anatomy Template A blocks | ~25 |
| Decision matrices (symptom-to-cause) | 4 major |
| Offline source citations | 100% Phase B+ |
| Upstream SHA + function verifications (Phase E) | 100+ |

### Known residual (v3.1.1 patch planned)

- **Rule 11 polish**: 110 minor Vietnamese prose leak còn lại trong core file. Phần lớn là numbered step Guided Exercise (`**3.** Verify connection`), table column header (`OpenFlow 1.X support`), vendor fact sentence (`HP ProCurve support 1.3`). Không ảnh hưởng kỹ thuật hay sự đọc hiểu, chỉ là discipline polish.
- **Block XIV+XV+XVI (68 leak)**: deprioritized theo user directive 2026-04-23 và 2026-04-24 "Đừng sa đà vào K8S, DPDK, XDP". Giữ skeleton + content nhưng không invest polish tiếp.
- **Lab verification (C1b)**: 63 exercise chờ lab host sẵn sàng. Output số liệu trong Guided Exercise là doc-plausible, chưa run thực tế.

### Files added Phase G (10 new/expanded)

- `sdn-onboard/9.14 - incident-response-decision-tree.md` (expand → 20 symptom matrix)
- `sdn-onboard/9.25 - ovs-flow-debugging-ofproto-trace.md` (expand +3 GE)
- `sdn-onboard/9.26 - ovs-revalidator-storm-forensic.md` (expand +2 case)
- `sdn-onboard/9.27 - ovs-ovn-packet-journey-end-to-end.md` (new)
- `sdn-onboard/13.7 - ovn-controller-internals.md` (expand run loop)
- `sdn-onboard/20.1 - ovs-ovn-security-hardening.md` (expand +audit trail)
- `sdn-onboard/20.2 - ovn-troubleshooting-deep-dive.md` (new)
- `sdn-onboard/20.3 - ovn-daily-operator-playbook.md` (new)
- `sdn-onboard/20.4 - ovs-daily-operator-playbook.md` (new)
- `sdn-onboard/20.5 - ovn-forensic-case-studies.md` (new)
- `sdn-onboard/20.6 - ovs-openflow-ovn-retrospective-2007-2024.md` (new)

### Commits milestone

Session milestone commits trên `docs/sdn-foundation-rev2`:

- Phase E: `7e5608b` (S33i Rule 14 codify)
- Phase F: `c777acf` (S36g 15.0)
- Phase H: `8dcbeca` (S59 phase G.4 close, also last Phase H commit baseline)
- Phase G: `8dcbeca` (S59 Phase G 100% COMPLETE)
- Pre-release audit: `ab9f38b` (S60) → `9469359` (S61a) → `d15d701` (S61b)

---

## Pre-release milestones (untagged)

### v2.1-preVerified (2026-04-22 post S35)

Phase E Scope D fact-check audit complete. Rule 14 Source Code Citation Integrity codified vào CLAUDE.md. Pre-release candidate nhưng chưa có release packaging.

### v2.0 (2026-04-22 post S29)

Phase D foundation firewall + audit backlog complete. 91 file curriculum với Block I-XIII content fully expanded. Rule 11 Vietnamese Prose Discipline codified.

### v1.0-preVerified (2026-04-21)

Phase B content expansion end-to-end. 64 file với Block 0-XIII content expanded + 3 advanced forensic (Part 17-19). Rule 10 Architecture-First Doctrine codified.

---

## Links

- Repo: https://github.com/volehuy1998/network-onboard
- SDN roadmap: [`sdn-onboard/README.md`](sdn-onboard/README.md)
- Pre-release audit: [`memory/pre-release-audit-2026-04-24.md`](memory/pre-release-audit-2026-04-24.md)
- Session history: [`memory/session-log.md`](memory/session-log.md)
- Project rules: [`CLAUDE.md`](CLAUDE.md) (14 mandatory rules + 6 skill)
