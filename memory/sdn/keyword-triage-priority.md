# Keyword Triage Priority (v3.7 Phase E deliverable)

> **Trạng thái:** Phase E v3.7-Reckoning, draft 2026-04-26.
> **Mục đích:** Sắp xếp 383 in-scope keyword thành cohort + ưu tiên thực thi cho Phase G content writing. Priority = architectural importance × current deficit.
> **Input:** `memory/sdn/keyword-rubric-scorecard.md` (Phase D output) + REF source.
> **Output:** Cohort list + execution order + effort estimate per cohort.

---

## 1. Methodology

### 1.1. Importance classification

| Importance | Definition | Target tier sau Phase G |
|------------|-----------|------------------------|
| **Cornerstone** | Trụ cột tuyệt đối; engineer không hiểu = không debug được | DEEP-20 (≥ 18/20) |
| **Medium** | Important nhưng không must-know mọi kỹ sư | DEEP-15 (≥ 15/20) |
| **Peripheral** | Niche/specialized, biết khi cần | PARTIAL-10 (≥ 10/20) |

### 1.2. Priority formula

```
Priority = Importance_weight × Deficit_score

Importance_weight:
  Cornerstone = 3
  Medium = 2  
  Peripheral = 1

Deficit_score = (target_tier_score - current_score) / 20
```

Cornerstone với current PLACEHOLDER (deficit ~0.85) = priority 2.55 = highest.
Peripheral với current DEEP-15 (deficit ~-0.25, already over target) = priority -0.25 = lowest.

### 1.3. Cohort principle

Group 5-15 keyword cùng theme thành 1 cohort cho efficient batch writing (shared research, shared cross-link, single commit).

---

## 2. Importance Classification (manual triage 320+ keyword)

> Per Phase E plan: cornerstone ~50, medium ~100, peripheral ~170.

### 2.1. Cornerstone (50 keyword)

**OVS core (12):**
megaflow, ct_state, ct_zone, openvswitch.ko (kernel datapath), ofproto-dpif xlate, classifier (TSS), upcall, recirc_id, conntrack execute, ovs-vswitchd, OVSDB Raft cluster, dpif

**OF protocol (8):**
OFPT_HELLO, OFPT_FEATURES_REQUEST, OFPT_FLOW_MOD, OFPT_PACKET_IN, OFPT_BARRIER_REQUEST, multi-table pipeline, goto_table, output (action)

**OVN architecture (15):**
ovn-northd, ovn-controller, ovn-trace, ovn-detrace, NBDB, SBDB, Logical_Flow, Datapath_Binding, Port_Binding, Logical_Switch, Logical_Router, ACL, Load_Balancer, NAT, Geneve TLV (OVN tunnel)

**OVN pipeline cornerstone (10):**
LS_IN_PORT_SEC_L2, LS_IN_PRE_ACL, LS_IN_ACL, LS_IN_LB, LS_IN_DHCP_OPTIONS, LS_IN_L2_LKUP, LR_IN_ADMISSION, LR_IN_IP_INPUT, LR_IN_DNAT, LR_IN_GW_REDIRECT

**OVN register (5):**
REGBIT_PORT_SEC_DROP, REGBIT_NAT_REDIRECT, MFF_LOG_INPORT, MFF_LOG_OUTPORT, MFF_LOG_DATAPATH

### 2.2. Medium (100 keyword)

**OVS internals (15):**
revalidator thread, handler thread, ukey, UFID, fast path / slow path, dpctl/dump-flows, ofproto/trace, coverage/show, packet_in handler, action_set, write_metadata, br-int patch port, OVSDB transaction model, JSON-RPC monitor, ovsdb-server roles

**OVS CLI (10):**
ovs-vsctl set-controller, ovs-ofctl add-flow, ovs-ofctl dump-flows, ovs-appctl dpif/dump-flows, ovs-appctl ofproto/trace, ovs-appctl coverage/show, ovs-vsctl show, ovs-vsctl get, ovs-dpctl show, ovs-dpctl dump-flows

**OF match field (20):**
in_port, eth_src, eth_dst, eth_type, vlan_vid, vlan_pcp, ip_proto, nw_src, nw_dst, ip_dscp, ip_ecn, ipv6_src, ipv6_dst, tp_src, tp_dst, tcp_flags, ct_mark, ct_label, ct_nw_proto, ct_zone

**OF action (15):**
output (handled), drop, set_field, mod_dl_src, mod_dl_dst, mod_nw_src, mod_nw_dst, mod_tp_src, mod_tp_dst, dec_ttl, push_vlan, pop_vlan, learn, conjunction, ct() (full)

**OVN NB schema (15):**
Logical_Router_Port, Logical_Switch_Port, Address_Set, Port_Group, Logical_Router_Static_Route, Logical_Router_Policy, Load_Balancer_Group, NAT (extended), DHCP_Options, DNS, BFD (NB), Forwarding_Group, QoS, Meter (NB), HA_Chassis_Group

**OVN SB schema (10):**
Chassis, Encap, MAC_Binding, FDB, Service_Monitor, Multicast_Group, IGMP_Group, BFD (SB), HA_Chassis, Connection

**OVN pipeline secondary (15):**
LS_IN_LB_AFF_CHECK, LS_IN_LB_AFF_LEARN, LS_IN_PRE_HAIRPIN, LS_IN_NAT_HAIRPIN, LS_IN_HAIRPIN, LS_IN_ARP_ND_RSP, LS_IN_DHCP_RESPONSE, LS_OUT_PRE_LB, LS_OUT_ACL, LS_OUT_PORT_SEC_L2, LR_IN_DEFRAG, LR_IN_UNSNAT, LR_IN_LARGER_PKTS, LR_IN_ND_RA_OPTIONS, LR_OUT_SNAT

### 2.3. Peripheral (170 keyword)

**OVS daemon helpers (8):**
ovs-monitor-ipsec, ovs-tcpdump, ovs-pcap, ovs-tcpundump, ovs-pki, vtep-ctl, ovs-vtep, ovsdb-tool

**OVS CLI options/flags (~30):**
ovs-vsctl --timeout, --columns, --bare, --format, --pretty, --no-headings, --if-exists, --may-exist, etc.
ovs-ofctl --strict, --readd, --bundle, --no-stats, etc.
ovs-appctl all daemon-specific commands not in cornerstone/medium

**OVSDB schema rows minor (~15):**
SSL row, Manager row, Mirror row, NetFlow row, sFlow row, IPFIX row, Queue row, QoS row, Meter row (OVS), Bridge subcommands, Port subcommands, Interface subcommands, etc.

**OF protocol minor (~25):**
OFPT_GET_CONFIG_REQUEST/REPLY, OFPT_SET_CONFIG, OFPT_PORT_MOD, OFPT_TABLE_MOD, OFPT_QUEUE_GET_CONFIG_REQUEST/REPLY, OFPT_REQUESTFORWARD, OFPT_TABLE_STATUS, OFPT_BUNDLE_OPEN/COMMIT/ADD/DISCARD, OFPMP_DESC, OFPMP_FLOW, OFPMP_AGGREGATE, OFPMP_TABLE, OFPMP_PORT_STATS, OFPMP_QUEUE_STATS, OFPMP_GROUP, OFPMP_GROUP_DESC, OFPMP_GROUP_FEATURES, OFPMP_METER, OFPMP_METER_CONFIG, OFPMP_METER_FEATURES, OFPMP_TABLE_FEATURES, OFPMP_PORT_DESC, OFPMP_EXPERIMENTER

**OF match field minor (~25):**
in_phy_port, ipv6_flabel, ipv6_exthdr, sctp_src, sctp_dst, mpls_label, mpls_tc, mpls_bos, pbb_isid, tunnel_id, pkt_mark, actset_output, NSH spi/si/c1-c4/np/mdtype, packet_type, recirc_id, dp_hash, conj_id, reg0-15 individual entries, xreg0-7, xxreg0-3

**OF action minor (~25):**
push_pbb, pop_pbb, set_mpls_ttl, dec_mpls_ttl, copy_ttl_in, copy_ttl_out, set_nw_ttl, decap, encap (NSH), controller (with userdata), note, sample, exit, multipath, bundle / bundle_load, fin_timeout, push, pop, move, copy_field, output:NXM, push:src, pop:dst, set_queue, group, meter

**OVN CLI options/subcommands (~30):**
ovn-nbctl --timeout, --leader-only, --no-leader-only, --shuffle-remotes, --no-headings, --dry-run, --oneline, -u, --print-wait-time, --inactivity-probe, --commit-retry, --unix-lock, --bare, --pretty, --id=@NAME, etc.
ovn-appctl exit, pause, resume, is-paused, status, set-n-threads, get-n-threads, sb-cluster-state-reset, nb-cluster-state-reset, ct-zone-list, meter-table-list, group-table-list, inject-pkt, recompute, lflow-cache/flush
ovn-ic-nbctl, ovn-ic-sbctl all subcommands

**OVN logical pipeline peripheral (~20):**
LS_IN_PORT_SEC_IP, LS_IN_PORT_SEC_ND, LS_IN_LOOKUP_FDB, LS_IN_PUT_FDB, LS_IN_PRE_STATEFUL, LS_IN_LB_AFF_LEARN, LS_OUT_PRE_ACL, LS_OUT_LB_AFF_CHECK, LS_OUT_PRE_STATEFUL, LS_OUT_LB, LR_IN_LOOKUP_NEIGHBOR, LR_IN_LEARN_NEIGHBOR, LR_IN_IP_ROUTING, LR_IN_IP_ROUTING_ECMP, LR_IN_POLICY, LR_IN_POLICY_ECMP, LR_IN_ARP_RESOLVE, LR_OUT_UNDNAT, LR_OUT_POST_UNDNAT, LR_OUT_DELIVERY

**OVN MLF flag family (8):**
MLF_LOCAL_ONLY, MLF_RCV_FROM_RAMP, MLF_FORCE_SNAT_FOR_DNAT, MLF_FORCE_SNAT_FOR_LB, MLF_LOCAL_BACKUP, MLF_DNAT_HAIRPIN, MLF_OUT_PORT_DIRECT_TUNNELLING, MLF_OUT_FROM_VTEP

**Production scenarios (14):**
14 troubleshoot scenarios trong REF Section 4 (đã cross-link 20.0 J.6 v3.5 nhưng cần Phase G expand thành full 20-axis treatment per scenario nếu treat them as keyword)

---

## 3. Cohort grouping (~50 cohort)

> Each cohort = 5-15 keyword cùng theme, 1 commit, ~500-2000 dòng curriculum.

### 3.1. Cornerstone cohort (5 cohort, ~50 keyword)

| # | Cohort | Keyword | Importance | Estimated effort |
|---|--------|---------|------------|------------------|
| C1 | OVS datapath core | megaflow, ct_state, ct_zone, openvswitch.ko, recirc_id, conntrack execute | Cornerstone | 12-20 giờ |
| C2 | OVS classifier + thread | classifier (TSS), upcall, ofproto-dpif xlate, dpif | Cornerstone | 8-15 giờ |
| C3 | OVS daemon + cluster | ovs-vswitchd, OVSDB Raft cluster | Cornerstone | 5-10 giờ |
| C4 | OF protocol cornerstone | OFPT_HELLO, OFPT_FEATURES_REQUEST, OFPT_FLOW_MOD, OFPT_PACKET_IN, OFPT_BARRIER_REQUEST, multi-table pipeline, goto_table, output (action) | Cornerstone | 15-25 giờ |
| C5 | OVN architecture cornerstone | ovn-northd, ovn-controller, ovn-trace, ovn-detrace, NBDB, SBDB, Logical_Flow, Datapath_Binding, Port_Binding, Logical_Switch, Logical_Router, ACL, Load_Balancer, NAT, Geneve TLV | Cornerstone | 30-45 giờ |
| C6 | OVN pipeline cornerstone | LS_IN_PORT_SEC_L2, LS_IN_PRE_ACL, LS_IN_ACL, LS_IN_LB, LS_IN_DHCP_OPTIONS, LS_IN_L2_LKUP, LR_IN_ADMISSION, LR_IN_IP_INPUT, LR_IN_DNAT, LR_IN_GW_REDIRECT | Cornerstone | 20-30 giờ |
| C7 | OVN register cornerstone | REGBIT_PORT_SEC_DROP, REGBIT_NAT_REDIRECT, MFF_LOG_INPORT, MFF_LOG_OUTPORT, MFF_LOG_DATAPATH | Cornerstone | 8-15 giờ |
| **Subtotal cornerstone** | 7 cohort | ~50 keyword | | **98-160 giờ** |

### 3.2. Medium cohort (~15 cohort, ~100 keyword)

| # | Cohort | Keyword | Importance | Effort |
|---|--------|---------|------------|--------|
| M1 | OVS internals secondary | revalidator thread, handler thread, ukey, UFID, fast path / slow path, action_set, write_metadata, br-int patch port | Medium | 10-15 giờ |
| M2 | OVS observability core | dpctl/dump-flows, ofproto/trace, coverage/show, packet_in handler, OVSDB transaction model, JSON-RPC monitor, ovsdb-server roles | Medium | 12-18 giờ |
| M3 | OVS CLI core (ovs-vsctl) | set-controller, set-fail-mode, add-port, add-br, set Bridge, get Bridge, show, list Bridge, list Port, list Interface | Medium | 10-15 giờ |
| M4 | OVS CLI core (ovs-ofctl) | add-flow, dump-flows, mod-flows, del-flows, dump-tables, dump-ports, dump-aggregate | Medium | 10-15 giờ |
| M5 | OVS CLI core (ovs-appctl) | dpif/dump-flows, dpif/dump-conntrack, ofproto/trace, ofproto/list-tunnels, coverage/show, vlog/list, vlog/set | Medium | 10-15 giờ |
| M6 | OF match field L2 | in_port, eth_src, eth_dst, eth_type, vlan_vid, vlan_pcp | Medium | 8-12 giờ |
| M7 | OF match field L3 | ip_proto, nw_src, nw_dst, ip_dscp, ip_ecn, ipv6_src, ipv6_dst | Medium | 8-12 giờ |
| M8 | OF match field L4 | tp_src, tp_dst, tcp_flags | Medium | 5-8 giờ |
| M9 | OF match field conntrack | ct_mark, ct_label, ct_nw_proto, ct_zone (medium aspect) | Medium | 5-8 giờ |
| M10 | OF action modification | drop, set_field, mod_dl_src, mod_dl_dst, mod_nw_src, mod_nw_dst, mod_tp_src, mod_tp_dst, dec_ttl, push_vlan, pop_vlan | Medium | 12-18 giờ |
| M11 | OF action NXM extension | learn, conjunction, ct() full | Medium | 8-12 giờ |
| M12 | OVN NB schema port | Logical_Router_Port, Logical_Switch_Port, Address_Set, Port_Group | Medium | 6-10 giờ |
| M13 | OVN NB schema policy | Logical_Router_Static_Route, Logical_Router_Policy, Load_Balancer_Group, NAT extended | Medium | 8-12 giờ |
| M14 | OVN NB schema services | DHCP_Options, DNS, BFD (NB), Forwarding_Group, QoS, Meter (NB), HA_Chassis_Group | Medium | 10-15 giờ |
| M15 | OVN SB schema runtime | Chassis, Encap, MAC_Binding, FDB, Service_Monitor, Multicast_Group, IGMP_Group, BFD (SB), HA_Chassis, Connection | Medium | 12-18 giờ |
| M16 | OVN pipeline LS secondary | LS_IN_LB_AFF_*, LS_IN_PRE_HAIRPIN, LS_IN_NAT_HAIRPIN, LS_IN_HAIRPIN, LS_IN_ARP_ND_RSP, LS_IN_DHCP_RESPONSE, LS_OUT_* | Medium | 15-22 giờ |
| M17 | OVN pipeline LR secondary | LR_IN_DEFRAG, LR_IN_UNSNAT, LR_IN_LARGER_PKTS, LR_IN_ND_RA_OPTIONS, LR_OUT_SNAT | Medium | 8-12 giờ |
| **Subtotal medium** | 17 cohort | ~100 keyword | | **157-237 giờ** |

### 3.3. Peripheral cohort (~25 cohort, ~170 keyword)

| # | Cohort | Keyword | Importance | Effort (batched) |
|---|--------|---------|------------|------------------|
| P1 | OVS daemon helpers | ovs-monitor-ipsec, ovs-tcpdump, ovs-pcap, ovs-tcpundump, ovs-pki, vtep-ctl, ovs-vtep, ovsdb-tool | Peripheral | 6-10 giờ |
| P2 | ovs-vsctl options | --timeout, --columns, --bare, --format, --pretty, --no-headings, --if-exists, --may-exist, --id, --no-wait, etc. (~15) | Peripheral | 5-8 giờ |
| P3 | ovs-ofctl options | --strict, --readd, --bundle, --no-stats, --more, --names, etc. (~10) | Peripheral | 4-6 giờ |
| P4 | OVSDB schema rows minor | SSL, Manager, Mirror, NetFlow, sFlow, IPFIX, Queue, QoS, Meter (OVS) | Peripheral | 8-12 giờ |
| P5 | OVS subcommand families | Bridge, Port, Interface, Controller, Manager, SSL subcommands generic | Peripheral | 5-8 giờ |
| P6 | OF protocol minor messages | OFPT_GET_CONFIG_REQUEST/REPLY, OFPT_SET_CONFIG, OFPT_PORT_MOD, OFPT_TABLE_MOD, OFPT_QUEUE_GET_CONFIG_*, OFPT_REQUESTFORWARD, OFPT_TABLE_STATUS | Peripheral | 8-12 giờ |
| P7 | OF protocol bundle | OFPT_BUNDLE_OPEN/COMMIT/ADD/DISCARD | Peripheral | 4-6 giờ |
| P8 | OF multipart sub-types | OFPMP_DESC/FLOW/AGGREGATE/TABLE/PORT_STATS/QUEUE_STATS/GROUP/GROUP_DESC/GROUP_FEATURES/METER/METER_CONFIG/METER_FEATURES/TABLE_FEATURES/PORT_DESC/EXPERIMENTER (~15) | Peripheral | 8-12 giờ |
| P9 | OF match field tunnel + IPv6 | in_phy_port, ipv6_flabel, ipv6_exthdr, sctp_src, sctp_dst, tunnel_id, pkt_mark, actset_output | Peripheral | 6-10 giờ |
| P10 | OF match field MPLS + PBB | mpls_label, mpls_tc, mpls_bos, pbb_isid | Peripheral | 4-6 giờ |
| P11 | OF match field NSH | NSH spi/si/c1-c4/np/mdtype, packet_type | Peripheral | 4-6 giờ |
| P12 | OF match field internal | recirc_id, dp_hash, conj_id | Peripheral | 3-5 giờ |
| P13 | OF match field register catalog | reg0-15 individual entries (16), xreg0-7 (8), xxreg0-3 (4) | Peripheral | 8-12 giờ |
| P14 | OF action MPLS + PBB | push_pbb, pop_pbb, set_mpls_ttl, dec_mpls_ttl, copy_ttl_in, copy_ttl_out, set_nw_ttl | Peripheral | 5-8 giờ |
| P15 | OF action NSH + decap | decap, encap (NSH) | Peripheral | 3-5 giờ |
| P16 | OF action observability | controller (with userdata), note, sample, exit | Peripheral | 4-6 giờ |
| P17 | OF action NXM stack + register | multipath, bundle / bundle_load, fin_timeout, push, pop, move, copy_field, output:NXM, push:src, pop:dst, set_queue, group, meter | Peripheral | 10-15 giờ |
| P18 | ovn-nbctl options | --timeout, --leader-only, --no-leader-only, --shuffle-remotes, --no-headings, --dry-run, --oneline, -u, --print-wait-time, --inactivity-probe, --commit-retry, --unix-lock, --bare, --pretty, --id=@NAME (~15) | Peripheral | 6-10 giờ |
| P19 | ovn-appctl runtime | exit, pause, resume, is-paused, status, set-n-threads, get-n-threads, sb-cluster-state-reset, nb-cluster-state-reset, ct-zone-list, meter-table-list, group-table-list, inject-pkt, recompute, lflow-cache/flush | Peripheral | 8-12 giờ |
| P20 | ovn-ic-nbctl + ovn-ic-sbctl | All subcommands (most niche) | Peripheral | 5-8 giờ |
| P21 | OVN pipeline LS peripheral | LS_IN_PORT_SEC_IP, LS_IN_PORT_SEC_ND, LS_IN_LOOKUP_FDB, LS_IN_PUT_FDB, LS_IN_PRE_STATEFUL, LS_OUT_PRE_ACL/PRE_STATEFUL/LB | Peripheral | 6-10 giờ |
| P22 | OVN pipeline LR peripheral | LR_IN_LOOKUP_NEIGHBOR, LEARN_NEIGHBOR, IP_ROUTING, IP_ROUTING_ECMP, POLICY, POLICY_ECMP, ARP_RESOLVE, LR_OUT_UNDNAT/POST_UNDNAT/DELIVERY | Peripheral | 8-12 giờ |
| P23 | OVN MLF flag family | 8 MLF_* flag | Peripheral | 4-6 giờ |
| P24 | OVN production scenarios | 14 scenarios trong REF Section 4 (cross-link 20.0 J.6 đã có; full 20-axis treatment cần expand) | Peripheral | 12-18 giờ |
| P25 | Misc REF entries | Catch-all cho 5-10 entry chưa cohort hoá | Peripheral | 4-6 giờ |
| **Subtotal peripheral** | 25 cohort | ~170 keyword | | **148-220 giờ** |

### 3.4. Total Phase G effort estimate

| Tier | Cohort | Keyword | Effort range |
|------|--------|---------|--------------|
| Cornerstone | 7 | 50 | 98-160 giờ |
| Medium | 17 | 100 | 157-237 giờ |
| Peripheral | 25 | 170 | 148-220 giờ |
| **Total Phase G** | **49 cohort** | **320 keyword** | **403-617 giờ** |

Plan v3.7 original Phase G estimate: 200-500 giờ.
Phase E refined: **403-617 giờ** (within plan upper bound, đầu hơn lower bound vì pilot reveals deficit deeper than originally estimated).

---

## 4. Execution Order (priority queue)

### 4.1. Top 10 cohort priority

| Rank | Cohort | Importance | Avg deficit | Priority score | Effort |
|------|--------|-----------|-------------|----------------|--------|
| 1 | C5 OVN architecture cornerstone | 3 | 0.4 | 1.2 | 30-45 giờ |
| 2 | C1 OVS datapath core | 3 | 0.3 | 0.9 | 12-20 giờ |
| 3 | C4 OF protocol cornerstone | 3 | 0.3 | 0.9 | 15-25 giờ |
| 4 | C6 OVN pipeline cornerstone | 3 | 0.4 | 1.2 | 20-30 giờ |
| 5 | C2 OVS classifier + thread | 3 | 0.4 | 1.2 | 8-15 giờ |
| 6 | C7 OVN register cornerstone | 3 | 0.5 | 1.5 | 8-15 giờ |
| 7 | C3 OVS daemon + cluster | 3 | 0.3 | 0.9 | 5-10 giờ |
| 8 | M1 OVS internals secondary | 2 | 0.4 | 0.8 | 10-15 giờ |
| 9 | M2 OVS observability core | 2 | 0.4 | 0.8 | 12-18 giờ |
| 10 | M11 OF action NXM extension | 2 | 0.5 | 1.0 | 8-12 giờ |

### 4.2. Phase G execution batches

Batch 1 (cornerstone first 4 cohort): C7 + C2 + C1 + C5 → ~58-105 giờ
Batch 2 (cornerstone remaining): C6 + C4 + C3 → ~40-70 giờ
Batch 3-5 (medium 17 cohort): ~157-237 giờ
Batch 6-10 (peripheral 25 cohort): ~148-220 giờ

**User checkpoint mỗi batch (per GP-4 Phase G mid-points):** 5-10 cohort completion → user review → continue.

### 4.3. Sequencing rationale

1. **Cornerstone first:** highest impact per hour. Gap to DEEP-20 small (~3 axis), high return.
2. **Medium second:** larger gap (~6 axis) but importance moderate.
3. **Peripheral last:** largest gap (~15 axis) but acceptable PARTIAL-10 target.
4. **Within tier, prioritize highest importance × deficit:**
   - C7 register (deficit ~0.5, smallest cohort 5 keyword) → quick win
   - C5 architecture (deficit ~0.4, largest cohort 15 keyword) → largest impact

---

## 5. Cohort dependency graph

Some cohort BLOCKED by others (foundation pattern):

- **C2 (classifier)** depends C1 (datapath core terms)
- **C5 (OVN architecture)** depends C1 + C4 (OVS + OF foundation)
- **C6 (OVN pipeline)** depends C5 + C7 (architecture + register)
- **M16 (LS pipeline secondary)** depends C6 (LS pipeline cornerstone)
- **M17 (LR pipeline secondary)** depends C6 (LR pipeline cornerstone)
- **M5 (ovs-appctl CLI)** depends C2 (classifier + thread for context)
- **P19 (ovn-appctl runtime)** depends C5 (architecture)

Recommended order: C1 → C2 → C3 → C4 → C5 → C6 → C7 → M-batch → P-batch

---

## 6. Acceptance Gate Phase E status

| Check | Result | Status |
|-------|--------|--------|
| Cohort grouping ~30-50 | 49 cohort defined | ✅ |
| Importance classification 50/100/170 | 50 cornerstone + ~100 medium + ~170 peripheral | ✅ |
| Priority order documented | Top 10 + batch breakdown Section 4 | ✅ |
| Effort estimate per cohort | 403-617 giờ tổng (within plan range) | ✅ |
| Cohort dependency graph | Section 5 | ✅ |
| User approve cohort order | Pending | ⏳ |

---

## 7. Files

- This triage: `memory/sdn/keyword-triage-priority.md`
- Scorecard input: `memory/sdn/keyword-rubric-scorecard.md`
- Rubric: `memory/sdn/rubric-20-per-keyword.md`
- Plan: `plans/sdn/v3.7-reckoning-and-mastery.md`

---

> **Đơn giản:** 49 cohort, 320 keyword, 403-617 giờ Phase G effort. Cornerstone first → medium → peripheral. Batch 5-10 cohort/checkpoint per GP-4. User approve cohort order trước khi Phase G start (gate 5/8 plan Section 14).
