# Template D — Per-table pipeline stage block cho OVN / OVS pipeline

> **Mục đích:** định nghĩa một stage trong pipeline (ovn ingress ls_in_*, egress ls_out_*, router lr_in_*/lr_out_*, hoặc OpenFlow table cụ thể của OVS br-int).
> **Upstream baseline:** man `ovn-architecture(7)` — 30+ logical flow table được itemize, mỗi table có match criteria + action + stage name.
> **Tối thiểu:** 50 dòng per stage.

## Skeleton

```markdown
### Pipeline stage `<stage_name>` (OVN table T<N>)

| Attribute | Giá trị |
|---|---|
| **Table number** | `T<N>` |
| **Pipeline direction** | ingress logical switch / egress logical switch / ingress logical router / egress logical router |
| **Stage name trong source** | `<stage>`, ví dụ `ls_in_port_sec_l2` (northd/northd.h: enum ovn_stage) |
| **Purpose** | <1-2 dòng trả lời: stage này đảm bảo property gì cho packet?> |
| **Match criteria** | <condition nào match vào stage — prefix của `ovn-sbctl lflow-list`> |
| **Typical actions** | <action phổ biến: next; stages với advance; drop; reg load; ...> |
| **Produced by** | `ovn-northd` dịch từ NBDB table `<X>` (ví dụ ACL → pre_acl; LB → lb; NAT → nat) |
| **State input** | <metadata/register từ stage trước set gì làm input> |
| **State output** | <metadata/register stage này set gì cho stage sau> |
| **Subsequent stage** | `T<N+1>` tên `<next_stage>`, hoặc `next;` dùng macro resubmit |

**Purpose chi tiết:**

<4-8 dòng giải thích stage này bảo vệ / enforce / translate gì. Tại sao OVN designer put stage này vào vị trí này của pipeline (before vs after stage Y).>.

**Ví dụ logical flow output** (`ovn-sbctl lflow-list` filtered by stage):

\`\`\`shell
$ ovn-sbctl lflow-list <datapath_name> | grep "ls_in_<stage>"
  table=<N>(<stage>), priority=<P>, match=<match_expr>, action=<action_expr>
  table=<N>(<stage>), priority=<P>, match=<match_expr>, action=<action_expr>
  <... 5-10 sample flow>
\`\`\`

**Ví dụ OpenFlow translation** (`ovs-ofctl dump-flows br-int` filtered):

\`\`\`shell
$ ovs-ofctl -O OpenFlow15 dump-flows br-int | grep "table=<N_ofport>"
 cookie=<...>, duration=<...>, table=<N_ofport>, n_packets=<P>, n_bytes=<B>,
  priority=<P>,<match>,<action>
 <... 5-10 OpenFlow entries sinh ra từ logical flow>
\`\`\`

**Anatomy của logical flow line:**

| Token | Ý nghĩa |
|---|---|
| `table=<N>` | Logical table number, không phải OpenFlow table |
| `(<stage_name>)` | Tên stage, tra trong `northd.h` enum ovn_stage |
| `priority=<P>` | Priority match, highest wins |
| `match=<expr>` | Logical flow expression (BNF ở `ovn-sb.xml` §Logical_Flow) |
| `action=<expr>` | Action list, semicolon-separated, compile thành OpenFlow apply_actions |

**Ví dụ `ovn-trace` annotated:**

\`\`\`shell
$ ovn-trace --ovs --detailed <datapath> "<flow>"
  ...
ingress(dp="<dp>", inport="<in>")
---------------------------------
 <N>. ls_in_<stage> (priority <P>): <match> -> <action>
  <action_annotated_breakdown>
\`\`\`

**Kịch bản bẻ gãy:**

- **Misconfig ACL dẫn đến drop tại stage này:** `ovn-trace` thấy `ls_in_<stage>` fire với `action=drop;` → fix bằng `ovn-nbctl acl-del ...`.
- **Quên state input:** nếu stage trước không set reg/metadata expected → stage này sẽ không match rule priority cao → fall through default → <symptom>.
- **Hardware offload không support:** stage X có action Y mà HW offload chưa implement → flow fallback slow path → CPU spike.

**Liên hệ với concept/cơ chế:**

<4-6 dòng nối stage này với kiến trúc OVN: logical flow → ovn-controller I-P translation → OpenFlow → br-int → datapath>.

**Upstream:**
- man `ovn-architecture(7)` §Logical Switch Datapath / Logical Router Datapath
- OVN source `northd/northd.c` function `build_<feature>_flows()`
- `ovn-sb.xml` §Logical_Flow schema
```

## Inventory stage foundation OVN

### Logical Switch Ingress Pipeline (25+ stage)

Per `northd.h` enum ovn_stage (OVN 22.03):

```
PIPELINE_INGRESS  (Pipeline direction: host → NBDB port)

T0  ls_in_check_port_sec        Port security validation (incoming)
T1  ls_in_lookup_fdb            Consult FDB for known source MAC
T2  ls_in_put_fdb               Insert new MAC into FDB
T3  ls_in_pre_acl               Pre-ACL connection tracker commit
T4  ls_in_pre_lb                Pre-load-balancer CT commit
T5  ls_in_pre_stateful          Commit into conntrack zone
T6  ls_in_acl_hint              Hint generation for ACL (reduce redundant CT)
T7  ls_in_acl                   Apply ACL rules (allow/allow-related/drop/reject)
T8  ls_in_qos_mark              DSCP / IP marking via QoS
T9  ls_in_qos_meter             Rate limiting via meters
T10 ls_in_stateful              Final commit and action
T11 ls_in_pre_hairpin           Detect hairpin traffic (VIP→backend same LS)
T12 ls_in_nat_hairpin           NAT hairpin (reverse SNAT)
T13 ls_in_hairpin               Redirect hairpin to originator
T14 ls_in_lb                    Load balancer VIP→backend selection
T15 ls_in_lb_aff_check          LB affinity check (pinned session)
T16 ls_in_lb_aff_learn          Learn affinity entry
T17 ls_in_pre_stateful          (re-used after LB)
T18 ls_in_stateful              (re-used after LB)
T19 ls_in_arp_rsp               ARP responder (stays in host)
T20 ls_in_dhcp_options          DHCPv4/v6 option lookup
T21 ls_in_dhcp_response         DHCP response packet generation
T22 ls_in_dns_lookup            DNS query processing
T23 ls_in_dns_response          DNS response generation
T24 ls_in_external_port         Bridging to external port
T25 ls_in_l2_lkup               Destination MAC lookup
```

### Logical Switch Egress Pipeline (8 stage)

```
T0 ls_out_pre_lb
T1 ls_out_pre_acl
T2 ls_out_pre_stateful
T3 ls_out_acl_hint
T4 ls_out_acl
T5 ls_out_qos_mark
T6 ls_out_qos_meter
T7 ls_out_stateful
T8 ls_out_port_sec_ip
T9 ls_out_port_sec_l2
```

### Logical Router Ingress Pipeline (20+ stage)

```
T0  lr_in_admission                 MAC + L3 validation
T1  lr_in_lookup_neighbor           Neighbor cache lookup
T2  lr_in_learn_neighbor            Populate neighbor cache
T3  lr_in_ip_input                  IP-layer input (redirects, ICMP reply)
T4  lr_in_unsnat                    Reverse SNAT
T5  lr_in_defrag                    IP fragment reassembly
T6  lr_in_dnat                      DNAT
T7  lr_in_ecmp_stateful             ECMP state tracking
T8  lr_in_nat_hairpin               NAT hairpin
T9  lr_in_ip_routing_pre            Pre-routing hook
T10 lr_in_ip_routing                FIB lookup
T11 lr_in_ip_routing_ecmp           ECMP path selection
T12 lr_in_policy                    Logical Router Policy
T13 lr_in_policy_ecmp               Policy ECMP
T14 lr_in_arp_resolve               ARP resolution
T15 lr_in_chk_pkt_len               Packet length check for ICMP-too-big
T16 lr_in_larger_pkts               Generate ICMP-too-big reply
T17 lr_in_gw_redirect               Gateway chassis redirect (distributed GR)
T18 lr_in_arp_request               ARP request emission
```

### Logical Router Egress Pipeline (8 stage)

```
T0 lr_out_chk_dnat_local
T1 lr_out_undnat
T2 lr_out_post_undnat
T3 lr_out_snat
T4 lr_out_post_snat
T5 lr_out_egr_loop
T6 lr_out_delivery
```

Tổng: ~61 stage để cover theo pattern exhaustive per-table breakdown. Priority Phase H session S46 (LS ingress+egress), S47 (LR ingress+egress), S48 (schema backup/complement).

## OVS physical table mapping (br-int)

Khi translate logical flow → OpenFlow, `ovn-controller` assign physical OpenFlow table number khác logical. Xem `ovn-architecture(7)` §Physical Pipeline hoặc `ovn-controller` source `controller/physical.c` để map T logical → T physical.

Physical tables của br-int (OpenFlow numbering):

```
T0  Physical-to-logical ingress (từ Geneve tunnel / NIC)
T8  Ingress pipeline table 0 (logical mapping)
... (ingress stages)
T32 Egress lookup
T33 Egress pipeline
...
T38 Output port selection
T64 Loopback for hairpin
T65 Logical-to-physical (Geneve encap / NIC output)
```

Numbering có thay đổi giữa OVN version; luôn tham chiếu `ovn-architecture(7)` cho phiên bản đang dùng.
