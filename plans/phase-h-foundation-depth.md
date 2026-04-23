# Plan Phase H — Foundation Depth Pass (OVS + OpenFlow + OVN)

> **Trạng thái:** Draft 2026-04-24, chờ user confirm.
> **Tạo:** 2026-04-24 sau audit pass 2 (max-effort) — xem `memory/sdn-onboard-audit-2026-04-24.md`.
> **Owner:** VO LE.
> **Mandate user 2026-04-24:** *"tỉ mỉ, chi tiết, thành thạo công cụ, đọc hiểu tất cả output của command, cơ chế + kiến trúc, troubleshoot + debug"* — KHÔNG K8S/DPDK/XDP.
> **Baseline:** curriculum hiện có 109 file, 37.522 dòng; 65/110 concept foundation ở mức shallow; 18/110 concept hoàn toàn vắng mặt; 71% code block ≤ 5 dòng (median 3).
> **Mục tiêu Phase H:** đưa curriculum từ v2.1-preVerified lên v3.0-FoundationDepth với tất cả concept foundation được cover đủ depth theo upstream authoritative baseline (ovs-fields / ovs-actions / ovn-architecture / OVS Advanced Tutorial / OVN OpenStack Tutorial).

---

## 0. Nguyên tắc chỉ đạo

1. **Foundation-first tuyệt đối.** KHÔNG mở rộng Block XIV/XV/XVI. Block 0 + I–XIII + XVII–XX là toàn bộ scope. Nếu có khái niệm K8s/DPDK/XDP xuất hiện trong foundation (ví dụ DPDK khi nhắc userspace datapath ở 9.3), chỉ note tối thiểu + redirect sang Block XVI, không đi sâu.

2. **Template-driven.** Thiết kế 4 template chuẩn TRƯỚC S38. Mọi session sau áp dụng template đồng nhất — không ad-hoc.

3. **Upstream-lift first.** Mỗi concept phải có **upstream source** cụ thể (man page section / spec section / tutorial section / paper section). Content được *adapt* từ upstream, KHÔNG tự chế. Rule 1 skill `search-first` enforce nghiêm.

4. **Real output only.** Mỗi output sample phải là raw capture thật từ Ubuntu 22.04 + OVS 2.17.9 + OVN 22.03.8 (hoặc reproduce lại). Nếu không có lab host, dùng output từ upstream man page / paper / GitHub issue. Mark rõ nguồn. Rule 7 + 7a enforce.

5. **Explanation-heavy.** Ratio explanation : (command + output) phải **≥ 1.5** per OVN OpenStack Tutorial baseline. Hiện tại curriculum nghịch đảo (prose dày, output thưa).

6. **14 Rule + 6 skill CLAUDE.md** enforce toàn bộ session Phase H:
   - Mở file .md → kích hoạt Core-4 (professor-style, document-design, fact-checker, web-fetcher).
   - Trước viết content mới → kích hoạt search-first; trước viết section cần multi-source → kích hoạt deep-research.
   - Rule 6 Quality Gate Checklist B + C + E chạy mỗi session.
   - Rule 11 §11.6 full sweep + Rule 13 em-dash density + Rule 14 source citation integrity per session.

---

## 1. Phạm vi mở rộng per Block

### 1.1. Block IV, OpenFlow evolution (8 file hiện có)

**Gap:** Instructions (Apply-Actions / Write-Actions / Clear-Actions / Write-Metadata / Goto-Table / Meter) nhắc ở 4.0 nhưng không structured; action_set execution order (12 priority) không có; group types 4 (all / select / indirect / fast_failover) chỉ 9 file; meter_band (5 band type) 0 mention.

**Expansion:**

| File | Thêm section (≥ 50 dòng) |
|---|---|
| 4.0 | §4.0.X Instructions catalog (6 instruction, mỗi cái anatomy 40-60 dòng theo 8-attribute template) + §4.0.Y Action Set execution order (12 priority level) |
| 4.2 | §4.2.X Meter bands (5 type: drop, dscp_remark, experimenter, yieldtoband, simple_rate_limiter) + lab OF 1.3 meter config |
| 4.4 | §4.4.X OF 1.5 L4 match fields + TCP flags matching + IPv6 extension headers |
| 4.7 | Expand existing với per-action anatomy (output / drop / set_field / push_pop / ct / learn / note / conjunction / normal / flood / controller / dec_ttl / enqueue / multipath / bundle / set_queue / resubmit — 17 action) |

### 1.2. Block VIII, Linux networking primer (4 file)

**Gap:** Netlink / genl không cover (42 mention trong 9.1 nhưng chưa có primer).

**Expansion:**

| File | Thêm section |
|---|---|
| 8.0 | §8.0.X Netlink + Generic Netlink (nl_socket, nlmsghdr, attribute TLV, OVS genl family) — 60-80 dòng |

### 1.3. Block IX, OVS internals + operations (28 file) — TRỌNG ĐIỂM

Đây là Block lớn nhất + user trọng điểm. Gap lớn nhất.

| File | Hiện tại (dòng) | Target (dòng) | Thêm |
|---|---:|---:|---|
| 9.1 | - | +150 | Classifier internals (staged lookup, prefix tree, subtable, TSS); connmgr (multi-controller, OF negotiation) |
| 9.2 | - | +200 | SMC cache (Signature Match Cache, OVS 2.15+); EMC anatomy; upcall netlink anatomy; revalidator RCU |
| 9.3 | - | +100 | PMD thread model; rxq scheduling; pmd-stats-show output anatomy; EMC/SMC trong netdev-dpdk |
| **9.4** | **267** | **~1.200** | **(priority #1)** expand toàn bộ 5 tool với Setup→Command→Output→Anatomy→Scenario cho mỗi tool |
| 9.7 | - | +100 | `ovs-tcpdump` deep-dive; `ovs-pcap` (vắng mặt); port mirror span-destination; RSPAN |
| 9.8 | - | +80 | sFlow datagram field anatomy; NetFlow v9 template; IPFIX IE |
| 9.9 | - | +100 | Meter bands catalog (kết nối với 4.2); queue anatomy per class |
| 9.10 | - | +100 | `ovs-pki` workflow CA init → sign → rotate; mTLS handshake trace |
| **9.11** | **215** | **~800** | **(priority #2)** 20 target ovs-appctl × 30-40 dòng anatomy = 600-800 dòng |
| 9.13 | - | +80 | `ovs-testcontroller` trong lab; libvirt XML → OVS binding deep |
| 9.14 | - | +100 | `ovs-bugtool` bundle collection; tar structure; triage playbook |
| 9.15 | - | +150 | Classifier deep: tuple space search thuật toán; subtable/staged lookup; prefix tree + prefix_lookup với ví dụ trace |
| 9.16 | - | +100 | Connection manager anatomy (inactivity probe, role MASTER/SLAVE/EQUAL negotiation, multi-controller fallback) |
| 9.17 | - | +100 | Coverage counter classes catalog; cache hit rate metrics anatomy |
| 9.19 | - | +80 | idle_timeout/hard_timeout semantics; flow_removed message; cookie pattern |
| 9.22 | - | +80 | Instructions catalog kết nối 4.0; action set 12-priority order; group_select/fast_failover lab |
| 9.24 | - | +150 | Expand ct anatomy: ct_nat / ct_commit / ct_alg (FTP ALG); conntrack_table structure; ct_mark / ct_label deep |
| 9.25 | - | +100 | Reserved port: flood / all / controller / local / in_port / table; packet_in/out anatomy |

**Tổng Block IX expansion:** +~2.000 dòng content mới.

### 1.4. Block X, OVSDB management (7 file)

| File | Thêm |
|---|---|
| 10.0 | §10.0.X OVSDB transaction deep (ACID chain, commit, rollback) — 80 dòng |
| 10.1 | §10.1.X Raft message catalog (AppendEntries, RequestVote, InstallSnapshot); cluster/status output anatomy |
| 10.2 | §10.2.X `ovsdb-tool` catalog (create, compact, convert, check-cluster, cluster-join/kick/leave) |
| 10.4 | §10.4.X Monitor Condition deep (columns, where clause, notification flow); `ovsdb-client monitor --where` |

### 1.5. Block XI, Overlay encapsulation (5 file)

| File | Thêm |
|---|---|
| 11.0 | §11.0.X VXLAN VNI format; Geneve option_class 0x0102; tun_metadata fields |
| 11.1 | §11.1.X Tun_fields catalog (tun_id, tun_src, tun_dst, tun_flags, tun_metadata[0-63]) |

### 1.6. Block XIII, OVN foundation (14 file) — TRỌNG ĐIỂM

**Gap lớn nhất của toàn curriculum:** OVN egress pipeline + logical router pipeline hoàn toàn không có table breakdown.

| File | Hiện tại | Thêm |
|---|---|---|
| 13.0 | - | OVN SB/NB schema version history; ovn-ic (interconnect) primer |
| **13.1** | - | +200 OVN NB schema catalog 13 table (Logical_Switch, LR, LSP, LRP, ACL, LB, NAT, Port_Group, DHCP_Options, **Static_Route** (vắng mặt), **Copp** (vắng mặt), QoS, Meter) với per-table anatomy 20-30 dòng |
| 13.1 | - | +150 OVN SB schema catalog 10 table (Datapath_Binding, Port_Binding, Chassis, Encap, HA_Chassis_Group, Logical_Flow, MAC_Binding, Multicast_Group, Service_Monitor, Controller_Event) |
| **13.2** | - | +300 OVN logical switch ingress pipeline **exhaustive table breakdown** (24 stage: port_sec_l2 / port_sec_ip / port_sec_nd / lookup_fdb / put_fdb / pre_acl / pre_lb / pre_stateful / acl_hint / acl / qos_mark / qos_meter / stateful / pre_hairpin / nat_hairpin / hairpin / lb / lb_aff_check / lb_aff_commit / stateful / arp_rsp / dhcp_opt / dhcp_resp / dns_lookup / dns_resp / external_port / l2_lkup) |
| **13.2** | - | +200 OVN logical switch egress pipeline (ls_out_*) exhaustive — **hiện vắng mặt hoàn toàn** |
| **13.11** | - | +400 OVN logical router ingress pipeline lr_in_* exhaustive (admission, lookup_neighbor, learn_neighbor, nd_rs / ip_input, dhcp_relay_req, unsnat, defrag, lb, lb_aff_check/commit, dnat, ecmp_stateful, nat, ip_routing, ip_routing_ecmp, policy, policy_ecmp, arp_resolve, chk_pkt_len, larger_pkts, gw_redirect, arp_request) — **hiện vắng mặt** |
| **13.11** | - | +200 OVN logical router egress pipeline lr_out_* exhaustive — **hiện vắng mặt** |
| 13.3 | - | ACL stage anatomy (pre_acl, acl_hint, acl, acl_after_lb); conjunctive match compression với conj_id |
| 13.6 | - | HA_Chassis_Group + Chassis priority + BFD; `ha_chassis` protocol walkthrough |
| 13.7 | - | §13.7.X I-P engine node catalog; recompute trigger; `ovn-appctl inc-engine/show-stats` output anatomy |
| 13.8 | - | northd per-logical-object translation catalog (LS → N flow, LR → M flow, ACL → K flow) với count example |
| 13.9 | - | Service_Monitor table deep (endpoints health check, BFD integration) |
| 13.10 | - | DHCP options catalog (all options OVN supports); DNS zone lookup flow |
| 13.11 | - | Distributed vs centralized gateway; chassisredirect (crp) deep |
| 13.12 | - | IPAM algorithm (allocation, exclude, pool exhaustion) |

**Tổng Block XIII expansion:** +~1.500 dòng.

### 1.7. Block XX, Operational Excellence (2 file)

| File | Thêm |
|---|---|
| 20.0 | §20.0.X Troubleshooting matrix 30-pattern (logical, physical, OVSDB, control plane) |
| 20.1 | §20.1.X Copp (Control Plane Protection) config; rate limiting catalog |

### 1.8. Block 0 + 0.2 (packet journey)

| File | Thêm |
|---|---|
| 0.2 | §0.2.X End-to-end annotated trace walk-through (reproduce `ofproto/trace` + `ovn-trace` + `dpif/dump-flows` cho 1 ICMP cross-host, annotate từng output token) |

---

## 2. Template library (thiết kế TRƯỚC S38)

Tạo `sdn-onboard/_templates/` chứa 4 markdown template. Mọi session Phase H phải import template khi viết content mới.

### 2.1. Template A — Anatomy block

```markdown
#### Đọc hiểu output `<tool> <subcommand>`

**Bối cảnh:** <khi nào chạy lệnh này, tình huống gì>.

```shell
$ <command>
<raw output 20-50 dòng reproduce từ Ubuntu 22.04 + OVS 2.17.9>
```

**Anatomy từng field:**

| Cột / Field | Giá trị mẫu | Ý nghĩa | Dấu hiệu đáng báo động |
|---|---|---|---|
| `<field1>` | <value> | <meaning> | <red flag> |
| ... | ... | ... | ... |

**Kịch bản bẻ gãy:**

- Nếu `<field>` = `<value>` thì symptom là <X>, root cause <Y>, fix <Z>.
- Nếu `<field>` vượt quá `<threshold>` thì <...>.

**Upstream nguồn:** [man <tool>(8)](URL) + [OVS tutorial](URL).
```

### 2.2. Template B — Per-field structured block (ovs-fields pattern)

```markdown
#### Match field `<name>`

| Attribute | Giá trị |
|---|---|
| **Name** | `<name>` |
| **Width** | `<N>` bits |
| **Format** | `<format>` (hex / decimal / MAC / IP / ...) |
| **Masking** | bitwise / CIDR / exact match / không hỗ trợ |
| **Prerequisites** | `<match prerequisites>` (e.g., `eth_type=0x0800` cho IP) |
| **Access** | read-only / read-write |
| **OpenFlow 1.0** | có/không, via `OFPFW_<...>` |
| **OpenFlow 1.1+** | OXM_OF_<...> |
| **NXM** | NXM_OF_<...> / NXM_NX_<...> |

**Semantics:** <mô tả field ý nghĩa trong packet format + pipeline use case>.

**Ví dụ match:**
```
priority=100,<field>=<value>,actions=...
```

**Kết hợp với action:** <action nào dùng field này>.

**Upstream:** man `ovs-fields(7)` §<section>.
```

### 2.3. Template C — Per-action structured block (ovs-actions pattern)

```markdown
#### Action `<name>`

| Attribute | Giá trị |
|---|---|
| **Syntax** | `<name>(<args>)` hoặc `<name>:<value>` |
| **Category** | Output / Encap/Decap / Field-Modification / Metadata / Firewall/CT / Control / Other |
| **Semantics** | <mô tả action làm gì, side effect, state change> |
| **Prerequisites** | <field prerequisites> |
| **Parameters** | <list arguments với range + default> |
| **OpenFlow version** | 1.0 / 1.1 / 1.3 / 1.5 / NXM extension |
| **Extensions** | Nicira extension? OVS-specific? |
| **Examples** | 3-5 dòng actions= cụ thể |
| **Conformance** | có spec conformant + ràng buộc pipeline |
| **Errors** | lỗi có thể xảy ra (ví dụ `OFPET_BAD_ACTION`) |

**Ví dụ use case:**
```
<flow với action>
```

**Trace output có action này:**
```
<ofproto/trace output show action execute>
```

**Kịch bản bẻ gãy:** <khi nào action fail hoặc side effect không mong>.

**Upstream:** man `ovs-actions(7)` §<section>.
```

### 2.4. Template D — Per-table pipeline stage block (ovn-architecture pattern)

```markdown
#### Pipeline stage `<stage_name>` (OVN table T<N>)

| Attribute | Giá trị |
|---|---|
| **Table number** | T`<N>` (ingress / egress / router ingress / router egress) |
| **Stage name** | `<stage>` (e.g., `ls_in_pre_acl`) |
| **Purpose** | <mô tả stage làm gì trong pipeline> |
| **Match criteria** | <common match field + condition> |
| **Actions** | <typical action sequence> |
| **Produced by** | `ovn-northd` từ NBDB table nào (ACL, Port_Security, LB, NAT, ...) |
| **Prerequisites** | Pipeline stage trước nào phải set metadata/register |
| **Subsequent stage** | Table T<N+1> hoặc resubmit target |

**Ví dụ logical flow:**
```
<ovn-sbctl lflow-list output sample cho stage này>
```

**Ví dụ OpenFlow translation (ovn-controller sinh):**
```
<ovs-ofctl dump-flows sample cho stage này tại br-int>
```

**Trace annotated:**
```
<ovn-trace output annotate stage này>
```

**Upstream:** `ovn-architecture(7)` §<section> + `ovn-northd.c` §<function>.
```

---

## 3. Cấu trúc session Phase H

### 3.1. Template session (áp dụng cho mọi H.2.X → H.7.X)

```
1. (5 min) Kích hoạt Core-4 skill + read CLAUDE.md Rule 1-14
2. (10 min) Read memory/session-log.md + read target file hiện tại + file dependency map
3. (15 min) search-first: identify upstream source section phù hợp
   - Fetch man page relevant section nếu cần
   - Fetch OVS/OVN Documentation/tutorials/*.rst relevant
   - Identify existing lab capture trong doc/ovs/ nếu phù hợp
4. (5 min) Declare session scope + target line count + template áp dụng
5. (60-90 min) Write content áp dụng template A/B/C/D
   - Mỗi concept 1 Anatomy block hoặc per-field/per-action/per-table block
   - Mỗi section 50-150 dòng (không dưới 50)
   - Real output reproduce hoặc lift từ upstream với attribution
6. (15 min) Rule 11 §11.6 regex scan + Rule 13 em-dash density check
7. (15 min) Rule 14 source citation verify qua MCP GitHub nếu cite source code
8. (10 min) Update memory/session-log.md + memory/file-dependency-map.md
9. (5 min) Commit với message `docs(sdn): session H.X.Y Phase H — <brief>`
```

### 3.2. Pilot session S38 (bắt buộc) — Part 9.4 CLI tools playbook

S38 là pilot để validate template A + B + C + D trước khi roll out. Scope:

- Part 9.4 (267 → ~1.200 dòng)
- Tool: `ovs-vsctl` + `ovs-ofctl` + `ovs-appctl` + `ovs-dpctl` + `ovsdb-client`
- Per tool: 3-5 common scenario × 30-50 dòng (command + output + Anatomy block + kịch bản bẻ gãy)
- Upstream source: `ovs-vsctl(8)`, `ovs-ofctl(8)`, `ovs-appctl(8)`, `ovs-dpctl(8)`, USC Lab 3 + Lab 4
- Target: median code block 20-30 dòng, explanation ratio ≥ 1.5

Sau S38, user review → approve template + depth pattern → roll out S39 trở đi.

---

## 4. Session roadmap (12 session)

| S# | Scope | Target file | Concept cover | Dòng thêm | Est effort |
|---|---|---|---|---:|---:|
| **S38** | H.0 Template + H.2.1 Pilot | `_templates/`, 9.4 | ovs-vsctl/ovs-ofctl/ovs-appctl/ovs-dpctl/ovsdb-client anatomy | +950 | 6-8h |
| S39 | H.2.2 | 9.11 expand | 20 ovs-appctl target anatomy | +600 | 5-6h |
| S40 | H.2.3 | 9.2 expand | Microflow/EMC/SMC/megaflow/upcall/revalidator/ukey deep | +200 | 4-5h |
| S41 | H.3 Match Fields | 4.1 + new 4.x | IPv6/ARP/ICMP/MPLS/tun/conj_id/pkt_mark fields | +300 | 5-6h |
| S42 | H.4.1 Actions output+control | 4.7 + 9.22 | output/drop/flood/all/controller/local/in_port/table reserved ports | +250 | 4-5h |
| S43 | H.4.2 Actions field+encap | 4.7 + 9.18 | set_field/dec_ttl/push_pop VLAN+MPLS/mod_* | +300 | 5-6h |
| S44 | H.4.3 Actions advanced | 4.7 + 9.22 + 9.24 | ct/learn/note/conjunction/multipath/bundle/resubmit/group | +400 | 6-7h |
| S45 | H.5 OVS internals | 9.1 + 9.15 + 9.16 | classifier/subtable/staged/TSS/connmgr/bridge-controller | +350 | 5-6h |
| **S46** | **H.6.1 OVN LS pipeline** | 13.2 | **ls_in_* 27 stage + ls_out_* 15 stage exhaustive** | +500 | 8-10h |
| **S47** | **H.6.2 OVN LR pipeline** | 13.11 | **lr_in_* 20 stage + lr_out_* 8 stage exhaustive** | +600 | 8-10h |
| S48 | H.6.3 OVN schema | 13.1 + 13.10 | NB 13 table + SB 10 table + DHCP options catalog | +350 | 6-7h |
| S49 | H.7 Conntrack completeness | 9.24 + 13.3 | ct_nat/ct_commit/ct_alg/ct_mark/ct_label/tcp_flags/ip_frag | +200 | 4-5h |
| S50 | H.8 Missing tools + Quality gate | 9.14 + 9.4 + 9.11 + sweep | ovs-bugtool/ovs-pcap/ovs-testcontroller; Rule 11/13/14 full sweep | +250 | 6-7h |

**Total:** +~5.250 dòng content mới, 12 session, estimate 72-88h.

---

## 5. Quality gate trước release v3.0-FoundationDepth

Mỗi session chạy local gate. Sau S50 chạy full sweep:

```bash
# Rule 9 null byte
python -c "
import glob
for f in glob.glob('sdn-onboard/*.md'):
  n=open(f,'rb').read().count(b'\x00')
  if n>0: print(f'NULL {n}: {f}')
"

# Rule 13 em-dash density (target < 0.10/line)
python -c "
import glob
for f in sorted(glob.glob('sdn-onboard/*.md')):
  t=open(f,encoding='utf8').read()
  L=t.count(chr(10)); e=t.count(chr(8212))
  if L>0 and e/L>0.10: print(f'DENSE {e/L:.3f}: {f}')
"

# Rule 11 prose scan §11.6 regex — targeted
grep -nIE '\b(paradigm|approach|deployment|adoption|motivation|performance|overhead|verify|experiment|pattern|behavior|monitor(ing)?|tracking|operator|engineer|subtle|significant|criteria|flexibility|bidirectional|symmetric|asymmetric)\b' sdn-onboard/*.md | grep -v '`' | grep -v 'http'

# Code block depth — target median ≥ 15
python - <<'EOF'
import glob,re
all_blocks=[]
for f in glob.glob('sdn-onboard/*.md'):
  bs=re.findall(r'```[a-zA-Z]*\n(.*?)\n```',open(f,encoding='utf8').read(),re.DOTALL)
  all_blocks.extend(b.count('\n')+1 for b in bs)
all_blocks.sort()
print(f'total={len(all_blocks)} median={all_blocks[len(all_blocks)//2]} mean={sum(all_blocks)/len(all_blocks):.1f}')
print(f'le5={sum(1 for l in all_blocks if l<=5)*100/len(all_blocks):.1f}%')
EOF

# Concept coverage — re-run tmp-concept-audit.py
# Target: Shallow ≤ 20 / 110 (was 65); Medium ≥ 50; Rich ≥ 40
python tmp-concept-audit.py

# Rule 12 offline source citation — target all Block IX + XIII parts có citation
grep -c 'compass_artifact\|USC Lab\|Day 4\|Day 5 -Lab\|Day 5-lab\|ovs-fields(7)\|ovs-actions(7)\|ovn-architecture(7)\|NSDI\|tutorial.rst\|man7.org' sdn-onboard/*.md

# Rule 14 source code citation — MCP GitHub verify cho mọi SHA/function/file/line new
# Log vào memory/fact-check-audit-2026-04-<X>.md
```

**Release gate v3.0:**
- Code block median ≥ 15 dòng
- ≤ 40% block ≤ 5 dòng (từ 71%)
- Concept shallow ≤ 20/110 (từ 65/110)
- Concept 0-mention = 0 (từ 18)
- Rule 11/13/14 all PASS
- Lab verification 63 item: C1b pending → resolve theo user notify lab host

---

## 6. Risk & mitigation

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Scope creep sang K8s/DPDK | Medium | Phá mandate user | Block XIV/XV/XVI không touch. Nếu Block IX/XIII nhắc khái niệm K8s/DPDK, link → không sâu |
| Output reproduce thiếu lab host | High | Content dùng fake output | Lift từ upstream tutorial + attribution rõ; mark `[reproduced from OVS tutorial]` vs `[real capture]` |
| Session kéo dài > 8h làm mệt | Medium | Quality giảm | Chia S38 pilot xong review, sau đó mỗi session tối đa 1 scope H.X.Y |
| Rule 11 retrofit tốn thời gian | High | Chậm v3.0 | Mỗi session làm local sweep file mình touch; batch full sweep cuối ở S50 |
| Upstream source URL thay đổi | Low | Link rot | Cite với commit SHA hoặc archive.org snapshot; version tag cho man page |
| Template A/B/C/D không fit mọi case | Medium | Consistency drop | S38 pilot reveal gap → refine template trước roll out S39+ |

---

## 7. Handoff & working memory

Phase H workflow refine `memory/file-dependency-map.md` (thêm tầng cho template import); cập nhật `memory/session-log.md` mỗi session; tạo `memory/phase-h-progress.md` tracker:

```markdown
# Phase H Progress Tracker

## Template library
- [ ] Template A Anatomy block
- [ ] Template B Per-field block (ovs-fields pattern)
- [ ] Template C Per-action block (ovs-actions pattern)
- [ ] Template D Per-table pipeline block (ovn-architecture pattern)

## Pilot S38
- [ ] Part 9.4 expanded to ~1200 lines
- [ ] User review + approve pattern

## Rollout
- [ ] S39 Part 9.11 (20 ovs-appctl target anatomy)
- [ ] S40 Part 9.2 (kernel datapath deep)
...
- [ ] S50 Missing tools + Quality gate

## Quality gate v3.0
- [ ] Code block median ≥ 15
- [ ] Concept shallow ≤ 20
- [ ] Rule 11/13/14 sweep PASS
```

---

## 8. Decision points cần user confirm

1. **Phê duyệt Phase H plan này?** (yes / modify / reject)
2. **S38 pilot scope:** Part 9.4 có phải file đúng để pilot, hay priority khác (9.11 trước, hoặc 9.2 kernel internals trước)?
3. **Lab host timeline:** khi nào có lab host để reproduce real output? Trong lúc chờ, có OK dùng upstream tutorial output với attribution không?
4. **Session cadence:** 1 session/ngày hay gộp weekend? Ảnh hưởng timeline 12 session (12 ngày vs 6 tuần).
5. **Version tag chiến lược:** sau Phase H mark v3.0-FoundationDepth; sau Lab C1b mark v3.1-LabVerified; sau user final review mark v3.2-Published — có OK không?
6. **Template library location:** `sdn-onboard/_templates/` (underscore prefix) hay `plans/templates/`?

---

**End of Phase H plan draft, 2026-04-24. Chờ user confirm.**
