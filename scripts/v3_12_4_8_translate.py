#!/usr/bin/env python3
"""Plan v3.12 R1.N run 3b: §4.8.X.46-49 + §4.8.Y batch."""
from __future__ import annotations
import sys
from pathlib import Path

FILE = Path("sdn-onboard/4.8 - openflow-match-field-catalog.md")
REPLACEMENTS: list[tuple[str, str]] = []


def add(vi: str, en: str) -> None:
    REPLACEMENTS.append((vi, en))


# §4.8.Y reference table
add(
    "Khoảng 75 match field ngoại vi đã có treatment đầy đủ Anatomy 9-attribute trong §4.8.15 (12 field bổ khuyết v3.5 J.4.a), §4.8.16 (MPLS/PBB), và §4.8.17 (NSH). Bảng dưới là sơ đồ tra cứu nhanh để khi gặp keyword nào bạn biết phần nào trong file 4.8 chứa trình bày đầy đủ; bảng KHÔNG phải tier-stamp.",
    "About 75 peripheral match fields already have full 9-attribute anatomy treatment in §4.8.15 (the 12 fields backfilled by v3.5 J.4.a), §4.8.16 (MPLS and PBB), and §4.8.17 (NSH). The table below is a quick lookup map: given a keyword, it tells you which part of file 4.8 contains the full treatment. The table is not a tier stamp.",
)

add(
    "| Nhóm field | Số keyword | Vị trí trình bày native |\n|------------|------------|-------------------------|\n| Tunnel + IPv6 phụ | 8 | §4.8.15 (`in_phy_port`, `ipv6_flabel`, `ipv6_exthdr`, `sctp_src/dst`, `tunnel_id`, `pkt_mark`, `actset_output`) |\n| MPLS + PBB | 4 | §4.8.16 (`mpls_*`, `pbb_isid`) |\n| NSH service chain | 7 | §4.8.17 (NSH `spi/si/c1-c4`, `packet_type` v.v.) |\n| Internal control | 3 | §4.8 (`recirc_id` xem 9.2.14, `dp_hash`, `conj_id` xem catalog 4.8.4.4) |\n| Register catalog | 28 | §4.8 (16 `reg0..reg15` + 8 `xreg0..xreg7` + 4 `xxreg0..xxreg3` qua §4.8.15.9-10) |",
    "| Field group | Keyword count | Native location |\n|-------------|---------------|-----------------|\n| Tunnel and auxiliary IPv6 | 8 | §4.8.15 (`in_phy_port`, `ipv6_flabel`, `ipv6_exthdr`, `sctp_src/dst`, `tunnel_id`, `pkt_mark`, `actset_output`) |\n| MPLS and PBB | 4 | §4.8.16 (`mpls_*`, `pbb_isid`) |\n| NSH service chain | 7 | §4.8.17 (NSH `spi/si/c1-c4`, `packet_type`, and so on) |\n| Internal control | 3 | §4.8 (`recirc_id` see 9.2.14, `dp_hash`, `conj_id` see catalog 4.8.4.4) |\n| Register catalog | 28 | §4.8 (16 `reg0` through `reg15`, 8 `xreg0` through `xreg7`, 4 `xxreg0` through `xxreg3` through §4.8.15.9 and §4.8.15.10) |",
)

add(
    "Phiên bản OpenFlow nền: OF 1.2+ OXM TLV cho đa số field; NSH yêu cầu OF 1.5+. Production use case của các field này thường niche (tunnel metadata cho debug topology, IPv6 flow label cho QoS layer trên, NSH service chain cho NFV insertion, register manipulation cho pipeline OVN nội bộ). Lab pattern thực hành nằm trong các phần §4.8.15-17 đã liệt kê.",
    "Baseline OpenFlow versions: OXM TLV in OF 1.2 onward covers most fields; NSH requires OF 1.5 or later. Production use cases for these fields are often niche: tunnel metadata for topology debugging, the IPv6 Flow Label for an upper-layer QoS hint, the NSH service chain for NFV insertion, and register manipulation inside the OVN internal pipeline. Hands-on lab patterns live in §4.8.15 through §4.8.17 as listed.",
)

# §4.8.X.46 dp_hash
add(
    "**Khái niệm.** `dp_hash` là field 32-bit chứa hash do datapath tính trên một subset của packet header (5-tuple hoặc tuple được chỉ định qua action `hash`). Đây là **field nội bộ, read-only** từ controller — controller không thể \"set\" `dp_hash` qua flow rule, chỉ có thể yêu cầu datapath tính qua action `hash(...)` rồi match giá trị tính được. Spec ID: `NXM_NX_DP_HASH(35)` since OVS v2.2; OXM experimenter `NXOXM_ET_DP_HASH(0)` since v2.4. Comment block `meta-flow.h` ghi: \"Flow hash computed in the datapath. Internal use only, not programmable from controller.\" Loại field: **datapath-computed metadata** (như `recirc_id`), khác hẳn nhóm scratch register vốn write thoải mái.",
    "**Concept.** `dp_hash` is a 32-bit field that holds a hash computed by the datapath over a subset of the packet header (the 5-tuple, or a tuple specified through the `hash` action). This is an internal, read-only field from the controller's perspective. The controller cannot set `dp_hash` through a flow rule. It can only ask the datapath to compute it through the action `hash(...)` and then match on the resulting value. Spec ID: `NXM_NX_DP_HASH(35)` since OVS v2.2; OXM experimenter `NXOXM_ET_DP_HASH(0)` since v2.4. The block comment in `meta-flow.h` states: \"Flow hash computed in the datapath. Internal use only, not programmable from controller.\" Field type: **datapath-computed metadata** (like `recirc_id`), distinct from the scratch-register group, which can be written freely.",
)

add(
    "**OXM/NXM byte layout.**\n\n```\nNXM TLV:\n| nxm_class=0x0001 | nxm_field=35 | hasmask=0 | length=4 | value(4) |   Total 8 byte\n| 0x00 0x01        | (35<<1)=0x46 | 0         | 0x04     | be32      |\nMaskable bitwise → masked length=8 với 4-byte mask theo sau.\nOXM experimenter NXOXM_ET_DP_HASH(0): hiếm dùng, chỉ test OXM experimenter framework.\n```\n\n**Ví dụ match + use case ECMP/LB.**",
    "**OXM and NXM byte layout.**\n\n```\nNXM TLV:\n| nxm_class=0x0001 | nxm_field=35 | hasmask=0 | length=4 | value(4) |   Total 8 bytes\n| 0x00 0x01        | (35<<1)=0x46 | 0         | 0x04     | be32      |\nBitwise maskable: masked length=8, with a 4-byte mask following the value.\nOXM experimenter NXOXM_ET_DP_HASH(0): rarely used, only for testing the OXM experimenter framework.\n```\n\n**Match example and ECMP or load-balancer use case.**",
)

add(
    "# Bước 1: action hash() yêu cầu datapath tính dp_hash trên 5-tuple\ntable=20,priority=100,ip,actions=hash(symmetric_l4),resubmit(,21)\n\n# Bước 2: match dp_hash mod N để chọn member ECMP/LB\ntable=21,priority=100,dp_hash=0x0/0x3,actions=set_field:10.0.0.1->reg0,goto_table:30\ntable=21,priority=100,dp_hash=0x1/0x3,actions=set_field:10.0.0.2->reg0,goto_table:30\ntable=21,priority=100,dp_hash=0x2/0x3,actions=set_field:10.0.0.3->reg0,goto_table:30\ntable=21,priority=100,dp_hash=0x3/0x3,actions=set_field:10.0.0.4->reg0,goto_table:30",
    "# Step 1: the hash() action asks the datapath to compute dp_hash over the 5-tuple\ntable=20,priority=100,ip,actions=hash(symmetric_l4),resubmit(,21)\n\n# Step 2: match dp_hash mod N to choose an ECMP or load-balancer member\ntable=21,priority=100,dp_hash=0x0/0x3,actions=set_field:10.0.0.1->reg0,goto_table:30\ntable=21,priority=100,dp_hash=0x1/0x3,actions=set_field:10.0.0.2->reg0,goto_table:30\ntable=21,priority=100,dp_hash=0x2/0x3,actions=set_field:10.0.0.3->reg0,goto_table:30\ntable=21,priority=100,dp_hash=0x3/0x3,actions=set_field:10.0.0.4->reg0,goto_table:30",
)

add(
    "**OVN pipeline usage.** OVN dùng `dp_hash` trong stage **ECMP route selection** (`LR_IN_ECMP_STATEFUL`) và **Load_Balancer member selection** (`LS_IN_PRE_STATEFUL` → `ct_lb`). Khi LR có 2+ static route cùng prefix khác nexthop (ECMP), `ovn-northd` sinh flow tính `dp_hash` rồi match low bits để rẽ packet đều giữa nexthop. Khi Load_Balancer có 2+ backend, action `ct_lb()` nội bộ cũng dùng dp_hash để chọn member; OVN không expose action chọn member ra OF level mà bundle vào `ct_lb`. Engineer debug ECMP imbalance phải hiểu dp_hash là **5-tuple hash đối xứng** (`hash(symmetric_l4)`) — same flow cùng chiều đi cùng path, cần tính lại nếu muốn LAG/ECMP per-packet thay vì per-flow.",
    "**OVN pipeline usage.** OVN uses `dp_hash` in the ECMP route selection stage (`LR_IN_ECMP_STATEFUL`) and in Load_Balancer member selection (`LS_IN_PRE_STATEFUL` then `ct_lb`). When a Logical_Router has two or more static routes with the same prefix and different next hops (ECMP), `ovn-northd` emits a flow that computes `dp_hash` and then matches its low bits to distribute packets evenly across next hops. When a Load_Balancer has two or more backends, the `ct_lb()` action uses `dp_hash` internally to choose a member. OVN does not expose member selection at the OpenFlow level; it bundles the choice inside `ct_lb`. An operator debugging ECMP imbalance should know that `dp_hash` is a symmetric 5-tuple hash (`hash(symmetric_l4)`), so the same flow in both directions takes the same path. Recompute the hash if you need per-packet LAG or ECMP rather than per-flow distribution.",
)

add(
    "**Liên quan mật thiết tới.** Action `hash(fields)` (`lib/ofp-actions.c` `parse_HASH`), action `multipath()` (legacy ECMP với bucket-based selection), action `ct_lb(backends)` (OVN load-balancer wrapper), `recirc_id` (sister datapath-computed metadata, xem §9.2.14), stage `LR_IN_ECMP_STATEFUL` + `LS_IN_PRE_STATEFUL`, group table type `select` với `selection_method=hash` (alternative ECMP path không dùng dp_hash).",
    "**Tightly related to.** The `hash(fields)` action (`lib/ofp-actions.c`, `parse_HASH`), the `multipath()` action (legacy ECMP with bucket-based selection), the `ct_lb(backends)` action (the OVN load-balancer wrapper), `recirc_id` (the sister datapath-computed metadata, see §9.2.14), the stages `LR_IN_ECMP_STATEFUL` and `LS_IN_PRE_STATEFUL`, and the group table of type `select` with `selection_method=hash` (an alternative ECMP path that does not use `dp_hash`).",
)

add(
    "**Khác biệt giữa các phiên bản.** OVS v2.2 (2014) thêm `NXM_NX_DP_HASH(35)` cùng với action `hash()`. OVS v2.4 thêm OXM experimenter code point `NXOXM_ET_DP_HASH(0)`, chủ yếu để test framework experimenter; comment trong `meta-flow.h` nói rõ \"doesn't commit OVS to supporting this OXM experimenter code point in the future\". OVS v2.7+ thêm `selection_method=dp_hash` cho group `select` (bucket selection dùng dp_hash thay vì hash riêng của OVS classifier), giúp ECMP/LB scaling tốt hơn trên kernel datapath. Curriculum baseline OVS v2.17.9.",
    "**Version differences.** OVS v2.2 (2014) added `NXM_NX_DP_HASH(35)` together with the `hash()` action. OVS v2.4 added the OXM experimenter code point `NXOXM_ET_DP_HASH(0)`, mainly to exercise the experimenter framework. The `meta-flow.h` comment notes that this \"doesn't commit OVS to supporting this OXM experimenter code point in the future\". OVS v2.7 onward added `selection_method=dp_hash` for group `select` (bucket selection uses `dp_hash` instead of the OVS classifier hash), which scales ECMP and load balancing better on the kernel datapath. Curriculum baseline: OVS v2.17.9.",
)

add(
    "**Cách quan sát + xác minh.** `ovs-ofctl dump-flows br-int | grep dp_hash` show rule match dp_hash (thường thấy trong table ECMP/LB). `ovs-appctl ofproto/trace br-int '<flow>'` reveal giá trị dp_hash sau action `hash()`. OVN: `ovn-trace --detailed` show ECMP path selection step. Verify ECMP balance: `ovs-ofctl dump-flows br-int table=<ecmp> --rsort=packet_count` xem packet count phân bố đều giữa các bucket dp_hash mod N.",
    "**Observation and verification.** `ovs-ofctl dump-flows br-int | grep dp_hash` shows rules that match on `dp_hash` (typically in an ECMP or load-balancer table). `ovs-appctl ofproto/trace br-int '<flow>'` reveals the `dp_hash` value after the `hash()` action. In OVN, `ovn-trace --detailed` shows the ECMP path selection step. To verify ECMP balance, run `ovs-ofctl dump-flows br-int table=<ecmp> --rsort=packet_count` and confirm that packet counts are distributed evenly across the `dp_hash mod N` buckets.",
)

add(
    "**Source code.** `MFF_DP_HASH` trong `include/openvswitch/meta-flow.h` v2.17.9 (enum đầu của nhóm Metadata, line ~244). `NXM_NX_DP_HASH(35)` định nghĩa trong `include/openvswitch/nicira-ext.h`. Runtime tính trong `lib/dpif-netdev.c` (userspace datapath) và `datapath/flow.c` (kernel datapath) qua function `flow_hash_5tuple` hoặc `flow_hash_symmetric_l4`. Action `hash()` parse trong `lib/ofp-actions.c` `parse_HASH`. OVN ECMP build: `build_ecmp_routes_flows` trong `northd/northd.c`.",
    "**Source code reference.** `MFF_DP_HASH` is defined in `include/openvswitch/meta-flow.h` v2.17.9 (the first enum in the Metadata group, around line 244). `NXM_NX_DP_HASH(35)` is defined in `include/openvswitch/nicira-ext.h`. The runtime computation happens in `lib/dpif-netdev.c` (userspace datapath) and `datapath/flow.c` (kernel datapath) through the functions `flow_hash_5tuple` and `flow_hash_symmetric_l4`. The `hash()` action is parsed in `lib/ofp-actions.c` by `parse_HASH`. OVN ECMP build: `build_ecmp_routes_flows` in `northd/northd.c`.",
)

add(
    "**Lỗi thường gặp.** (a) Cố `set_field:0xN->dp_hash`: parser reject vì field read-only — phải dùng action `hash(...)` để datapath tính. (b) Kỳ vọng dp_hash giống nhau giữa kernel và userspace datapath: hash function khác, chỉ giống trong cùng datapath type. (c) Match `dp_hash=0x5` mà không có action `hash()` trước trong cùng flow: dp_hash giữ giá trị 0 (init), match thất bại trừ khi check exact 0. (d) Confuse `dp_hash` với group `select` weighted bucket: dp_hash là field, group select là cơ chế khác; có thể kết hợp qua `selection_method=dp_hash`.",
    "**Common failures.** (a) Trying `set_field:0xN->dp_hash`. The parser rejects it because the field is read-only. Use the `hash(...)` action so that the datapath computes the value. (b) Expecting the same `dp_hash` value between the kernel and userspace datapaths. The hash function differs, so values agree only within the same datapath type. (c) Matching `dp_hash=0x5` without a preceding `hash()` action in the same flow. The field stays at its initial value 0, so the match fails unless you check for exact 0. (d) Confusing `dp_hash` with the weighted bucket of group `select`. `dp_hash` is a field, while group `select` is a different mechanism. The two can be combined through `selection_method=dp_hash`.",
)

# §4.8.X.47 conj_id
add(
    "**Khái niệm.** `conj_id` là field 32-bit chứa ID của `conjunction()` action đã match trong cùng pipeline; cho phép flow rule tham chiếu chéo các \"thành phần\" của một match đa chiều mà không phải sinh đầy đủ N×M flow cross-product. Đây là **field read-only, exact-match-only** (no mask) từ controller. Spec ID: `NXM_NX_CONJ_ID(37)` since OVS v2.4; OXM none. Comment `meta-flow.h`: \"ID for 'conjunction' actions. Please refer to ovs-fields(7) documentation of 'conjunction' for details. Type: be32. Maskable: no. Access: read-only.\" Loại field: **internal control field** liên kết action `conjunction(id, k/n)` với rule final match `conj_id=id`. Nghĩa kỹ thuật: rule final chỉ trigger khi đủ `n` thành phần khác nhau đều match conjunction cùng `id`.",
    "**Concept.** `conj_id` is a 32-bit field that holds the ID of a `conjunction()` action that matched within the same pipeline. It lets a flow rule reference cross-cutting components of a multi-dimensional match without producing the full `N x M` cross-product of flows. This is a read-only, exact-match-only field (no mask) from the controller's perspective. Spec ID: `NXM_NX_CONJ_ID(37)` since OVS v2.4; no OXM equivalent. The `meta-flow.h` comment states: \"ID for 'conjunction' actions. Please refer to ovs-fields(7) documentation of 'conjunction' for details. Type: be32. Maskable: no. Access: read-only.\" Field type: **internal control field**, which links a `conjunction(id, k/n)` action to a final rule that matches `conj_id=id`. Semantically, the final rule triggers only when `n` distinct components all match a conjunction with the same `id`.",
)

add(
    "**OXM/NXM byte layout.**\n\n```\nNXM TLV:\n| nxm_class=0x0001 | nxm_field=37 | hasmask=0 | length=4 | value(4) |   Total 8 byte\n| 0x00 0x01        | (37<<1)=0x4a | 0         | 0x04     | be32      |\nMask: KHÔNG hỗ trợ (Maskable: no). Match phải exact 32-bit.\nOXM: none.\n```\n\n**Ví dụ cross-product compression (từ §4.8.4.4 mở rộng).**\n\nKhông dùng conjunction, ACL \"(src ∈ {A,B,C}) AND (dst ∈ {X,Y,Z})\" cần 3×3 = 9 rule. Dùng conjunction = 3+3+1 = 7 rule:",
    "**OXM and NXM byte layout.**\n\n```\nNXM TLV:\n| nxm_class=0x0001 | nxm_field=37 | hasmask=0 | length=4 | value(4) |   Total 8 bytes\n| 0x00 0x01        | (37<<1)=0x4a | 0         | 0x04     | be32      |\nMask: not supported (Maskable: no). The match must be an exact 32-bit value.\nOXM: none.\n```\n\n**Cross-product compression example (extending §4.8.4.4).**\n\nWithout conjunction, the ACL \"(src in {A, B, C}) AND (dst in {X, Y, Z})\" needs 3 x 3 = 9 rules. With conjunction it needs 3 + 3 + 1 = 7 rules:",
)

add(
    "# Component 1/2: 3 rule cho src\npriority=100,ip,nw_src=10.0.1.1,actions=conjunction(7,1/2)\npriority=100,ip,nw_src=10.0.1.2,actions=conjunction(7,1/2)\npriority=100,ip,nw_src=10.0.1.3,actions=conjunction(7,1/2)\n\n# Component 2/2: 3 rule cho dst\npriority=100,ip,nw_dst=10.0.2.1,actions=conjunction(7,2/2)\npriority=100,ip,nw_dst=10.0.2.2,actions=conjunction(7,2/2)\npriority=100,ip,nw_dst=10.0.2.3,actions=conjunction(7,2/2)\n\n# Final rule: chỉ trigger khi packet match 1 src + 1 dst với cùng conj_id=7\npriority=100,conj_id=7,actions=output:5",
    "# Component 1 of 2: three rules for the source\npriority=100,ip,nw_src=10.0.1.1,actions=conjunction(7,1/2)\npriority=100,ip,nw_src=10.0.1.2,actions=conjunction(7,1/2)\npriority=100,ip,nw_src=10.0.1.3,actions=conjunction(7,1/2)\n\n# Component 2 of 2: three rules for the destination\npriority=100,ip,nw_dst=10.0.2.1,actions=conjunction(7,2/2)\npriority=100,ip,nw_dst=10.0.2.2,actions=conjunction(7,2/2)\npriority=100,ip,nw_dst=10.0.2.3,actions=conjunction(7,2/2)\n\n# Final rule: triggers only when a packet matches one src and one dst with the same conj_id=7\npriority=100,conj_id=7,actions=output:5",
)

add(
    "Compression factor: N×M rule → N+M+1 rule. Nhân rộng cho ACL N chiều: `O(∑Ni)` thay `O(∏Ni)`. OVN ACL Port_Group cross-product dùng pattern này rất nhiều.",
    "Compression factor: `N x M` rules become `N + M + 1` rules. For an ACL with N dimensions, this is `O(sum of Ni)` instead of `O(product of Ni)`. OVN ACL Port_Group cross-products use this pattern extensively.",
)

add(
    "**OVN pipeline usage.** OVN dùng `conj_id` rộng rãi trong **ACL với Port_Group + Address_Set** cross-product. Khi user định nghĩa ACL `match=\"ip4.src == $set_A && ip4.dst == $set_B\"` với set_A 100 IP và set_B 50 IP, naive expansion = 5000 flow. `ovn-northd` sinh ACL với conjunction để giảm xuống 100+50+1 = 151 flow per ACL entry. Engineer audit OVN ACL phải đọc conj_id để hiểu quan hệ giữa các fragment ACL: `ovn-sbctl lflow-list | grep conj_id` show rule final, ngược lên các component conjunction(id, k/n).",
    "**OVN pipeline usage.** OVN uses `conj_id` extensively for ACL cross-products that combine Port_Group and Address_Set. When a user defines an ACL `match=\"ip4.src == $set_A && ip4.dst == $set_B\"` with `set_A` having 100 IPs and `set_B` having 50 IPs, the naive expansion would be 5,000 flows. `ovn-northd` emits the ACL with conjunction to bring the count down to 100 + 50 + 1 = 151 flows per ACL entry. An operator auditing OVN ACLs must read `conj_id` to understand the relationships among ACL fragments. `ovn-sbctl lflow-list | grep conj_id` shows the final rule, from which you can trace back to the `conjunction(id, k/n)` components.",
)

add(
    "**Liên quan mật thiết tới.** Action `conjunction(id, k/n)` (`lib/ofp-actions.c` `decode_NXAST_RAW_CONJUNCTION`), classifier conjunctive matching algorithm (`lib/classifier.c` `classifier_conjunction_lookup`), OVN macro generation cho ACL Port_Group + Address_Set, action `note` (debug breadcrumb), action `learn` (alternative dynamic rule generation, rất khác semantic).",
    "**Tightly related to.** The `conjunction(id, k/n)` action (`lib/ofp-actions.c`, `decode_NXAST_RAW_CONJUNCTION`), the classifier conjunctive matching algorithm (`lib/classifier.c`, `classifier_conjunction_lookup`), OVN macro generation for ACLs that combine Port_Group and Address_Set, the `note` action (a debug breadcrumb), and the `learn` action (an alternative dynamic rule generation method with very different semantics).",
)

add(
    "**Khác biệt giữa các phiên bản.** OVS v2.4 (2015) thêm `NXM_NX_CONJ_ID(37)` cùng action `conjunction()`, đề xuất bởi Pfaff để giải quyết flow explosion với ACL nhiều chiều mà OF spec không hỗ trợ native. OVS v2.6 cải thiện classifier internals để conjunction lookup hiệu quả hơn (TSS subtable handling). OF spec không bao giờ chuẩn hoá conjunction (vẫn là Nicira extension only). Curriculum baseline OVS v2.17.9. OVS v3.x giữ nguyên semantic.",
    "**Version differences.** OVS v2.4 (2015) added `NXM_NX_CONJ_ID(37)` together with the `conjunction()` action. The feature was proposed by Pfaff to address flow explosion in multi-dimensional ACLs, which the OF specification did not support natively. OVS v2.6 improved classifier internals so that conjunction lookups are more efficient (TSS subtable handling). The OpenFlow specification has never standardized conjunction; it remains a Nicira extension only. Curriculum baseline: OVS v2.17.9. OVS v3.x keeps the same semantics.",
)

add(
    "**Cách quan sát + xác minh.** `ovs-ofctl dump-flows br-int | grep -E 'conjunction|conj_id'` show cả component lẫn final rule. `ovs-appctl ofproto/trace br-int '<flow>'` reveal mỗi conjunction component trigger thế nào, conj_id final value match được gì. OVN: `ovn-sbctl lflow-list <datapath> | grep conj_id` show ACL biên dịch ra conjunction. Verify ACL compression: count rule trước (`grep -c conjunction`) so với cross-product naive expectation N×M.",
    "**Observation and verification.** `ovs-ofctl dump-flows br-int | grep -E 'conjunction|conj_id'` shows both component and final rules. `ovs-appctl ofproto/trace br-int '<flow>'` reveals how each conjunction component triggers and what the final `conj_id` value matches. In OVN, `ovn-sbctl lflow-list <datapath> | grep conj_id` shows ACLs compiled with conjunction. To verify ACL compression, count the conjunction rules (`grep -c conjunction`) and compare to the naive `N x M` cross-product expectation.",
)

add(
    "**Source code.** `MFF_CONJ_ID` trong `include/openvswitch/meta-flow.h` v2.17.9 (line ~287). `NXM_NX_CONJ_ID(37)` trong `include/openvswitch/nicira-ext.h`. Action implementation: `lib/ofp-actions.c` parse `parse_CONJUNCTION` + format `format_CONJUNCTION`. Classifier matching: `lib/classifier.c` function `find_match_wc` + `classifier_conjunctive_*`. OVN ACL build: `consider_acl` + `build_acls` trong `northd/northd.c` sinh conjunction rule khi Port_Group/Address_Set có nhiều phần tử. man page `ovs-fields(7)` mô tả semantic chi tiết.",
    "**Source code reference.** `MFF_CONJ_ID` is defined in `include/openvswitch/meta-flow.h` v2.17.9 (around line 287). `NXM_NX_CONJ_ID(37)` is defined in `include/openvswitch/nicira-ext.h`. Action implementation: `lib/ofp-actions.c` parses through `parse_CONJUNCTION` and formats through `format_CONJUNCTION`. Classifier matching: the function `find_match_wc` and the `classifier_conjunctive_*` family in `lib/classifier.c`. OVN ACL build: `consider_acl` and `build_acls` in `northd/northd.c` emit conjunction rules when a Port_Group or an Address_Set has multiple members. The man page `ovs-fields(7)` describes the semantics in detail.",
)

add(
    "**Lỗi thường gặp.** (a) Match `conj_id=N` mà không có rule với `actions=conjunction(N,k/n)`: rule final không bao giờ trigger (no source). (b) Inconsistent priority giữa conjunction component và rule final: classifier phải có cả N component cùng priority match thì mới `conj_id` thành công; sai priority → conjunction không complete. (c) Mỗi conjunction component ghi `actions=conjunction(...)` thôi, KHÔNG kèm action khác (nếu kèm sẽ bị reject) — final action chỉ nằm ở rule match `conj_id=N`. (d) Confuse `conj_id` với `recirc_id` hoặc `metadata`: cả ba đều internal control nhưng semantic khác hoàn toàn. (e) OF spec không chuẩn hoá conjunction → controller không-OVS không hiểu, portability thấp.",
    "**Common failures.** (a) Matching `conj_id=N` without any rule that has `actions=conjunction(N,k/n)`. The final rule never triggers because there is no source. (b) Inconsistent priorities between conjunction components and the final rule. The classifier requires that all N components match at the same priority for `conj_id` to succeed; mismatched priorities leave the conjunction incomplete. (c) Each conjunction component must specify only `actions=conjunction(...)`, with no additional action (additional actions are rejected). The final action lives only on the rule that matches `conj_id=N`. (d) Confusing `conj_id` with `recirc_id` or `metadata`. All three are internal-control fields, but their semantics differ. (e) The OpenFlow specification does not standardize conjunction, so non-OVS controllers do not recognize it, and portability is low.",
)

# §4.8.X.48 xreg0
add(
    "**Khái niệm.** `xreg0` là field 64-bit alias chồng lên cặp `reg0`+`reg1` (high 32-bit = `reg0`, low 32-bit = `reg1`); cho phép match/set giá trị 64-bit nguyên khối thay vì hai phép thao tác riêng cho từng register 32-bit. Đây là **OF 1.5 standard \"extended register\"** (`OXM_OF_PKT_REG0`), không phải Nicira extension như `reg0..reg15`. Spec ID: `OXM_OF_PKT_REG0(0) since OF1.3 and v2.4` (ban đầu là extension thử nghiệm OF 1.3, OF 1.5 chính thức chuẩn hoá là `pkt_reg`). Comment `meta-flow.h`: \"OpenFlow 1.5 'extended register'. Type: be64. Maskable: bitwise. Access: read/write. NXM: none. OXM: OXM_OF_PKT_REG<N>(<N>) since OF1.3 and v2.4.\" Loại field: **OF spec metadata register**, sub-loại \"64-bit extended register\" — khác `reg0` ở chỗ là OXM standard, có overlay relationship với cặp register 32-bit.",
    "**Concept.** `xreg0` is a 64-bit alias overlaid on the `reg0` and `reg1` pair (the high 32 bits map to `reg0` and the low 32 bits map to `reg1`). It lets you match or set a 64-bit value as a single unit, rather than performing two separate operations on the two 32-bit registers. This is the OF 1.5 standard \"extended register\" (`OXM_OF_PKT_REG0`), not a Nicira extension like `reg0` through `reg15`. Spec ID: `OXM_OF_PKT_REG0(0) since OF1.3 and v2.4` (originally an experimental extension in OF 1.3, then formally standardized in OF 1.5 as `pkt_reg`). The `meta-flow.h` comment states: \"OpenFlow 1.5 'extended register'. Type: be64. Maskable: bitwise. Access: read/write. NXM: none. OXM: OXM_OF_PKT_REG<N>(<N>) since OF1.3 and v2.4.\" Field type: **OF specification metadata register**, subtype \"64-bit extended register\". It differs from `reg0` in that it is an OXM standard and has an overlay relationship with the 32-bit register pair.",
)

add(
    "**OXM/NXM byte layout.**\n\n```\nOXM TLV (OF 1.5 standard):\n| oxm_class=0x8000 | oxm_field=0  | hasmask=0 | length=8 | value(8) |   Total 12 byte\n| 0x80 0x00        | (0<<1)=0x00  | 0         | 0x08     | be64      |\nMasked length=16 với 8-byte mask sau value.\nNXM: none (xreg là OF spec, không phải Nicira ext).\n\nOverlay relationship với reg0+reg1:\n+----------------------+----------------------+\n|       reg0 (32)      |       reg1 (32)      |\n| xreg0[63..32]        | xreg0[31..0]         |\n+----------------------+----------------------+\n```\n\n**Ví dụ match + load 64-bit nguyên khối.**",
    "**OXM and NXM byte layout.**\n\n```\nOXM TLV (OF 1.5 standard):\n| oxm_class=0x8000 | oxm_field=0  | hasmask=0 | length=8 | value(8) |   Total 12 bytes\n| 0x80 0x00        | (0<<1)=0x00  | 0         | 0x08     | be64      |\nMasked length=16, with an 8-byte mask following the value.\nNXM: none (xreg is OF spec, not a Nicira extension).\n\nOverlay relationship with reg0 and reg1:\n+----------------------+----------------------+\n|       reg0 (32)      |       reg1 (32)      |\n| xreg0[63..32]        | xreg0[31..0]         |\n+----------------------+----------------------+\n```\n\n**Match and load examples for the full 64-bit value.**",
)

add(
    "# Load 64-bit value vào xreg0 = đặt reg0=0xCAFEBABE, reg1=0x12345678 cùng lúc\ntable=0,priority=100,actions=load:0xCAFEBABE12345678->NXM_NX_XREG0[],goto_table:5\n\n# Match nguyên 64-bit\ntable=5,xreg0=0xCAFEBABE12345678,actions=output:2\n\n# Match một nửa qua reg0 (high half) hoặc reg1 (low half)\ntable=5,reg0=0xCAFEBABE,actions=output:3   # match high half xreg0\ntable=5,reg1=0x12345678,actions=output:4   # match low half xreg0\n\n# Bitwise mask phần giữa (cross 32-bit boundary)\ntable=5,xreg0=0x00000000ABCD0000/0x00000000FFFF0000,actions=output:5",
    "# Load a 64-bit value into xreg0, which sets reg0=0xCAFEBABE and reg1=0x12345678 at the same time\ntable=0,priority=100,actions=load:0xCAFEBABE12345678->NXM_NX_XREG0[],goto_table:5\n\n# Match the full 64-bit value\ntable=5,xreg0=0xCAFEBABE12345678,actions=output:2\n\n# Match one half through reg0 (high half) or reg1 (low half)\ntable=5,reg0=0xCAFEBABE,actions=output:3   # matches the high half of xreg0\ntable=5,reg1=0x12345678,actions=output:4   # matches the low half of xreg0\n\n# Bitwise mask spanning the 32-bit boundary\ntable=5,xreg0=0x00000000ABCD0000/0x00000000FFFF0000,actions=output:5",
)

add(
    "**OVN pipeline usage.** OVN dùng `xreg0` ít trực tiếp nhưng **cấp phát overlay tự động** khi engineer thao tác `reg0`+`reg1`. Vì `reg0` chứa **ACL flag bitmap** (xem §4.8.X.30) và `reg1` chứa **datapath/tunnel_key working copy**, ghi `xreg0` đồng nghĩa overwrite cả ACL flag lẫn working copy — pattern không nên dùng trong OVN-managed pipeline. Trong OVS standalone, `xreg0` hữu ích cho **store cặp giá trị 32-bit liên quan**: `reg0` = original IPv4 nexthop, `reg1` = original tp_dst → match cả hai cùng lúc bằng `xreg0=val`. OF 1.5 controller native (Faucet, Ryu) dùng `pkt_reg0` thay `xreg0` (cùng field, tên khác).",
    "**OVN pipeline usage.** OVN uses `xreg0` directly only rarely, but the overlay is allocated automatically whenever an operator works with `reg0` and `reg1`. Because `reg0` holds the ACL flag bitmap (see §4.8.X.30) and `reg1` holds the datapath or tunnel_key working copy, writing `xreg0` overwrites both the ACL flag and the working copy. This pattern is not recommended inside the OVN-managed pipeline. In standalone OVS, `xreg0` is useful for storing a related pair of 32-bit values: for example, `reg0` could hold an original IPv4 next hop and `reg1` could hold an original `tp_dst`, and you could match both at once with `xreg0=val`. Native OF 1.5 controllers (Faucet, Ryu) use the name `pkt_reg0` instead of `xreg0` (same field, different name).",
)

add(
    "**Liên quan mật thiết tới.** `reg0` (high 32-bit của `xreg0`, sister phần dưới của overlay), `reg1` (low 32-bit của `xreg0`, sister phần dưới của overlay), `xreg1..xreg7` (sister 64-bit register), `xxreg0` (128-bit alias `reg0..reg3`, phủ cả `xreg0`+`xreg1`), action `load`/`set_field`/`move`, OF 1.5 `pkt_reg` standard naming, OVN ACL flag (gián tiếp qua overlay với `reg0`).",
    "**Tightly related to.** `reg0` (the high 32 bits of `xreg0`, the sibling that occupies one half of the overlay), `reg1` (the low 32 bits of `xreg0`, the sibling that occupies the other half of the overlay), `xreg1` through `xreg7` (sibling 64-bit registers), `xxreg0` (the 128-bit alias of `reg0` through `reg3`, which covers both `xreg0` and `xreg1`), the actions `load`, `set_field`, and `move`, the OF 1.5 standard naming `pkt_reg`, and the OVN ACL flag (indirectly through the overlay with `reg0`).",
)

add(
    "**Khác biệt giữa các phiên bản.** OF 1.3 (2012) draft \"extended register\" như experimenter; OVS v2.4 (2015) thêm `OXM_OF_PKT_REG<N>(<N>) since OF1.3 and v2.4` cho 8 xreg. OF 1.5 (2014) chuẩn hoá `pkt_reg` (cùng field, tên `pkt_reg<N>`). OVS giữ tên `xreg<N>` để backward-compat với tooling cũ; `pkt_reg<N>` được nhận dạng song song qua `lib/meta-flow.c`. OVS v2.6 thêm `xxreg0` (128-bit alias `reg0..reg3`) phủ cả `xreg0`+`xreg1`. Curriculum baseline OVS v2.17.9.",
    "**Version differences.** OF 1.3 (2012) drafted the extended register as an experimenter feature. OVS v2.4 (2015) added `OXM_OF_PKT_REG<N>(<N>) since OF1.3 and v2.4` for the eight xregs. OF 1.5 (2014) standardized it as `pkt_reg` (same field, named `pkt_reg<N>`). OVS keeps the `xreg<N>` name for backward compatibility with older tooling; `pkt_reg<N>` is recognized in parallel through `lib/meta-flow.c`. OVS v2.6 added `xxreg0` (the 128-bit alias of `reg0` through `reg3`), which covers both `xreg0` and `xreg1`. Curriculum baseline: OVS v2.17.9.",
)

add(
    "**Cách quan sát + xác minh.** `ovs-ofctl dump-flows br-int | grep -E 'xreg0|pkt_reg0'` show rule. `ovs-appctl ofproto/trace br-int '<flow>'` reveal `xreg0` per stage; trace cũng show `reg0`+`reg1` riêng (cùng giá trị nhưng split). OVN: `ovn-trace --detailed` không reference `xreg0` trực tiếp (vì OVN dùng `reg0`+`reg1` riêng), nhưng nếu rule custom dùng xreg0 thì hiển thị. Verify overlay: load `xreg0=0x1122334455667788`, dump flow check `reg0=0x11223344` + `reg1=0x55667788` = đúng overlay.",
    "**Observation and verification.** `ovs-ofctl dump-flows br-int | grep -E 'xreg0|pkt_reg0'` shows rules. `ovs-appctl ofproto/trace br-int '<flow>'` reveals `xreg0` per stage; the trace also shows `reg0` and `reg1` separately (the same value, split). In OVN, `ovn-trace --detailed` does not reference `xreg0` directly because OVN uses `reg0` and `reg1` separately, but custom rules that use `xreg0` are displayed. To verify the overlay, load `xreg0=0x1122334455667788` and dump the flow; you should see `reg0=0x11223344` and `reg1=0x55667788`, confirming the overlay.",
)

add(
    "**Source code.** `MFF_XREG0` trong `include/openvswitch/meta-flow.h` v2.17.9 (line ~1046, comment block chung cho `MFF_XREG0..MFF_XREG7`). Implementation overlay: function `mf_get_value`/`mf_set_value` trong `lib/meta-flow.c` đọc `flow.regs[0]` ghép với `flow.regs[1]` thành 64-bit khi gọi với `MFF_XREG0`. Macro `FLOW_N_XREGS == 8` (compile-time) đảm bảo có đúng 8 xreg. Mapping logic: `id - MFF_XREG0` dùng làm index pair.",
    "**Source code reference.** `MFF_XREG0` is defined in `include/openvswitch/meta-flow.h` v2.17.9 (around line 1046, in the shared comment block for `MFF_XREG0` through `MFF_XREG7`). Overlay implementation: the functions `mf_get_value` and `mf_set_value` in `lib/meta-flow.c` read `flow.regs[0]` and combine it with `flow.regs[1]` into a 64-bit value when called with `MFF_XREG0`. The macro `FLOW_N_XREGS == 8` (compile time) guarantees exactly eight xregs. Mapping logic: `id - MFF_XREG0` is used as the pair index.",
)

add(
    "**Lỗi thường gặp.** (a) Ghi `xreg0` trong OVN pipeline vô tình overwrite `reg0` (ACL flag) + `reg1` (datapath working copy) → ACL semantic broken, packet drop hoặc mis-route. (b) Confuse byte order trong 64-bit value: `xreg0=0xAABBCCDDEEFF1122` thì `reg0=0xAABBCCDD` (high half), `reg1=0xEEFF1122` (low half) — engineer phải biết network byte order pattern. (c) OF 1.0/1.1/1.2 controller không hỗ trợ `xreg0` (cần OF 1.3+); rule reject với \"unknown OXM type\". (d) Match `xreg0=val` trong table dùng OF 1.0 protocol bridge → reject. (e) Quên mask khi chỉ care về một nửa: `xreg0=0x00000000ABCD0000/0x00000000FFFF0000` đúng, `xreg0=0xABCD0000` mặc định coi là exact 64-bit (high half + 0 low half).",
    "**Common failures.** (a) Writing `xreg0` inside the OVN pipeline accidentally overwrites `reg0` (the ACL flag) and `reg1` (the datapath working copy). The ACL semantics break, and packets drop or route incorrectly. (b) Confusing byte order in a 64-bit value: `xreg0=0xAABBCCDDEEFF1122` means `reg0=0xAABBCCDD` (high half) and `reg1=0xEEFF1122` (low half). An operator must know the network byte order pattern. (c) OF 1.0, 1.1, and 1.2 controllers do not support `xreg0` (it requires OF 1.3 or later). The rule is rejected with \"unknown OXM type\". (d) Matching `xreg0=val` on a table that uses an OF 1.0 protocol bridge is rejected. (e) Forgetting the mask when you care about only half of the value: `xreg0=0x00000000ABCD0000/0x00000000FFFF0000` is correct, while `xreg0=0xABCD0000` is treated as an exact 64-bit match (high half plus a zero low half).",
)

# §4.8.X.49 xreg1
add(
    "**Khái niệm.** `xreg1` là field 64-bit alias chồng lên cặp `reg2`+`reg3` (high 32-bit = `reg2`, low 32-bit = `reg3`); cấu trúc + semantics tương đương `xreg0` (xem §4.8.X.48): 64-bit OF 1.5 standard \"extended register\", read/write, maskable bitwise, no NXM (chỉ OXM). Spec ID: `OXM_OF_PKT_REG1(1) since OF1.3 and v2.4`. `meta-flow.h` v2.17.9: `MFF_XREG1` cùng comment block với `MFF_XREG0..MFF_XREG7`. Loại field: **OF spec metadata register**, sub-loại \"64-bit extended register\"; alias overlay cho cặp `reg2`+`reg3`.",
    "**Concept.** `xreg1` is a 64-bit alias overlaid on the `reg2` and `reg3` pair (the high 32 bits map to `reg2` and the low 32 bits map to `reg3`). Its structure and semantics are equivalent to `xreg0` (see §4.8.X.48): a 64-bit OF 1.5 standard \"extended register\", read/write, bitwise maskable, with no NXM (OXM only). Spec ID: `OXM_OF_PKT_REG1(1) since OF1.3 and v2.4`. In `meta-flow.h` v2.17.9, `MFF_XREG1` shares the comment block with `MFF_XREG0` through `MFF_XREG7`. Field type: **OF specification metadata register**, subtype \"64-bit extended register\"; an overlay alias for the `reg2` and `reg3` pair.",
)

add(
    "**OXM/NXM byte layout.**\n\n```\nOXM TLV (OF 1.5 standard):\n| oxm_class=0x8000 | oxm_field=1  | hasmask=0 | length=8 | value(8) |   Total 12 byte\n| 0x80 0x00        | (1<<1)=0x02  | 0         | 0x08     | be64      |\nMasked length=16. NXM: none.\n\nOverlay relationship với reg2+reg3:\n+----------------------+----------------------+\n|       reg2 (32)      |       reg3 (32)      |\n| xreg1[63..32]        | xreg1[31..0]         |\n+----------------------+----------------------+\n```\n\n**Ví dụ match + load 64-bit.**",
    "**OXM and NXM byte layout.**\n\n```\nOXM TLV (OF 1.5 standard):\n| oxm_class=0x8000 | oxm_field=1  | hasmask=0 | length=8 | value(8) |   Total 12 bytes\n| 0x80 0x00        | (1<<1)=0x02  | 0         | 0x08     | be64      |\nMasked length=16. NXM: none.\n\nOverlay relationship with reg2 and reg3:\n+----------------------+----------------------+\n|       reg2 (32)      |       reg3 (32)      |\n| xreg1[63..32]        | xreg1[31..0]         |\n+----------------------+----------------------+\n```\n\n**Match and load examples for the full 64-bit value.**",
)

add(
    "# Load 64-bit value vào xreg1 = đặt reg2 + reg3 cùng lúc\ntable=0,priority=100,actions=load:0xDEADBEEF87654321->NXM_NX_XREG1[],goto_table:5\n\n# Match nguyên 64-bit\ntable=5,xreg1=0xDEADBEEF87654321,actions=output:6\n\n# Match một nửa qua reg2 hoặc reg3\ntable=5,reg2=0xDEADBEEF,actions=output:7   # match high half xreg1\ntable=5,reg3=0x87654321,actions=output:8   # match low half xreg1\n\n# Move xreg0 vào xreg1 (copy 64-bit metadata pair)\ntable=5,priority=100,actions=move:NXM_NX_XREG0[]->NXM_NX_XREG1[],goto_table:6",
    "# Load a 64-bit value into xreg1, which sets reg2 and reg3 at the same time\ntable=0,priority=100,actions=load:0xDEADBEEF87654321->NXM_NX_XREG1[],goto_table:5\n\n# Match the full 64-bit value\ntable=5,xreg1=0xDEADBEEF87654321,actions=output:6\n\n# Match one half through reg2 or reg3\ntable=5,reg2=0xDEADBEEF,actions=output:7   # matches the high half of xreg1\ntable=5,reg3=0x87654321,actions=output:8   # matches the low half of xreg1\n\n# Move xreg0 into xreg1 (copy a 64-bit metadata pair)\ntable=5,priority=100,actions=move:NXM_NX_XREG0[]->NXM_NX_XREG1[],goto_table:6",
)

add(
    "**OVN pipeline usage.** OVN dùng cặp `reg2`+`reg3` cho **NAT working copy** trong stage `LR_IN_DNAT` + `LR_IN_UNSNAT` + `LR_OUT_SNAT` (lưu original src/dst IP trước khi NAT replace, để có thể restore khi reply traffic match `ct_state=+rpl`). Vì vậy `xreg1` là overlay 64-bit cho NAT scratch pad: ghi `xreg1` trong pipeline OVN sẽ overwrite cả `reg2` (NAT working IP slot 1) và `reg3` (NAT working IP slot 2). Pattern này không nên dùng trong rule custom thêm vào OVN-managed bridge. Trong OVS standalone, `xreg1` hữu ích cho **store IPv6 address half**: 64-bit fit nửa IPv6 address (high half hoặc low half), kết hợp với `xreg0` đủ chứa IPv6 128-bit (tuy nhiên `xxreg0` 128-bit gọn hơn).",
    "**OVN pipeline usage.** OVN uses the `reg2` and `reg3` pair as a NAT working copy in the stages `LR_IN_DNAT`, `LR_IN_UNSNAT`, and `LR_OUT_SNAT` (it stores the original source or destination IP before NAT replacement so that it can be restored when reply traffic matches `ct_state=+rpl`). Therefore `xreg1` is the 64-bit overlay for the NAT scratch pad: writing `xreg1` inside the OVN pipeline overwrites both `reg2` (NAT working IP slot 1) and `reg3` (NAT working IP slot 2). This pattern should not be used in custom rules added to an OVN-managed bridge. In standalone OVS, `xreg1` is useful for storing one half of an IPv6 address (the high or low half). Combined with `xreg0`, it can hold a full 128-bit IPv6 address, although `xxreg0` (128-bit) is more compact.",
)

add(
    "**Liên quan mật thiết tới.** `reg2` (high 32-bit của `xreg1`), `reg3` (low 32-bit của `xreg1`), `xreg0` (sister 64-bit register; cặp xreg0+xreg1 phủ trùm `reg0..reg3`, tương đương `xxreg0`), `xxreg0` (128-bit alias `reg0..reg3`, phủ cả `xreg0`+`xreg1` — ghi xxreg0 đè cả hai xreg), action `move`/`load`/`set_field`, OVN NAT stage (gián tiếp qua `reg2`+`reg3`), OF 1.5 `pkt_reg1` standard naming.",
    "**Tightly related to.** `reg2` (the high 32 bits of `xreg1`), `reg3` (the low 32 bits of `xreg1`), `xreg0` (the sibling 64-bit register; together `xreg0` plus `xreg1` cover `reg0` through `reg3`, equivalent to `xxreg0`), `xxreg0` (the 128-bit alias of `reg0` through `reg3`, which covers both `xreg0` and `xreg1`; writing `xxreg0` overwrites both xregs), the actions `move`, `load`, and `set_field`, the OVN NAT stages (indirectly through `reg2` and `reg3`), and the OF 1.5 standard naming `pkt_reg1`.",
)

add(
    "**Khác biệt giữa các phiên bản.** OVS v2.4 (2015) thêm `OXM_OF_PKT_REG1(1) since OF1.3 and v2.4` cùng đợt với 7 xreg khác. OF 1.5 chuẩn hoá `pkt_reg1`. OVS v2.6 thêm `xxreg0` (`reg0..reg3` 128-bit) phủ `xreg0`+`xreg1`. Hành vi 64-bit ổn định từ v2.4 đến v2.17.9. OVN binding: `reg2` + `reg3` reserve cho NAT working copy từ OVN 20.x trở đi (xem `northd/northd.c` `build_lrouter_in_dnat_flows`). Curriculum baseline OVS v2.17.9 + OVN v22.03.8.",
    "**Version differences.** OVS v2.4 (2015) added `OXM_OF_PKT_REG1(1) since OF1.3 and v2.4` together with the seven other xregs. OF 1.5 standardized it as `pkt_reg1`. OVS v2.6 added `xxreg0` (the 128-bit alias of `reg0` through `reg3`), which covers both `xreg0` and `xreg1`. The 64-bit behavior has been stable from v2.4 through v2.17.9. OVN binding: `reg2` and `reg3` are reserved for the NAT working copy from OVN 20.x onward (see `build_lrouter_in_dnat_flows` in `northd/northd.c`). Curriculum baseline: OVS v2.17.9 plus OVN v22.03.8.",
)

add(
    "**Cách quan sát + xác minh.** `ovs-ofctl dump-flows br-int | grep -E 'xreg1|pkt_reg1'` show rule (hiếm trong OVN pipeline mặc định, phổ biến hơn trong custom flow). `ovs-appctl ofproto/trace br-int '<flow>'` reveal `xreg1` cùng `reg2`+`reg3` per stage. OVN: `ovn-trace --detailed` không reference `xreg1` trực tiếp (vì OVN dùng `reg2`+`reg3` riêng cho NAT). Verify overlay: load `xreg1=0x1122334455667788`, dump flow xác nhận `reg2=0x11223344` + `reg3=0x55667788`.",
    "**Observation and verification.** `ovs-ofctl dump-flows br-int | grep -E 'xreg1|pkt_reg1'` shows rules (rare in the default OVN pipeline, more common in custom flows). `ovs-appctl ofproto/trace br-int '<flow>'` reveals `xreg1` together with `reg2` and `reg3` per stage. In OVN, `ovn-trace --detailed` does not reference `xreg1` directly because OVN uses `reg2` and `reg3` separately for NAT. To verify the overlay, load `xreg1=0x1122334455667788` and dump the flow; you should see `reg2=0x11223344` and `reg3=0x55667788`.",
)

add(
    "**Source code.** `MFF_XREG1` trong `include/openvswitch/meta-flow.h` v2.17.9 cùng enum với `MFF_XREG0..MFF_XREG7` (line ~1047). Implementation overlay: `mf_get_value`/`mf_set_value` trong `lib/meta-flow.c` index pair `(MFF_XREG1 - MFF_XREG0) * 2 = 2` → đọc `flow.regs[2]` + `flow.regs[3]`. Macro `FLOW_N_XREGS == 8`. OVN NAT working copy: function `build_lrouter_in_dnat_flows` + `build_lrouter_out_snat_flow` trong `northd/northd.c` sử dụng `reg2`+`reg3` (gián tiếp qua `xreg1` overlay khi engineer dump 64-bit).",
    "**Source code reference.** `MFF_XREG1` is in `include/openvswitch/meta-flow.h` v2.17.9, in the same enum as `MFF_XREG0` through `MFF_XREG7` (around line 1047). Overlay implementation: `mf_get_value` and `mf_set_value` in `lib/meta-flow.c` use the index pair `(MFF_XREG1 - MFF_XREG0) * 2 = 2`, so they read `flow.regs[2]` and `flow.regs[3]`. The macro `FLOW_N_XREGS == 8`. OVN NAT working copy: the functions `build_lrouter_in_dnat_flows` and `build_lrouter_out_snat_flow` in `northd/northd.c` use `reg2` and `reg3` (and indirectly `xreg1` through the overlay when an operator dumps the 64-bit value).",
)

add(
    "**Lỗi thường gặp.** (a) Ghi `xreg1` trong OVN pipeline overwrite `reg2`+`reg3` (NAT working copy) → reply traffic không restore nguyên IP gốc, packet đi sai route. (b) Confuse `xreg1` với `xreg0`: xreg0 phủ reg0+reg1 (ACL flag + datapath), xreg1 phủ reg2+reg3 (NAT working copy) — semantic khác hoàn toàn trong OVN. (c) Ghi `xxreg0` overwrite cả `xreg0`+`xreg1` (= `reg0..reg3`) đồng loạt, mất ACL flag + datapath copy + NAT working copy → pipeline collapse phía LR. (d) OF 1.0/1.1/1.2 controller không hỗ trợ `xreg1`. (e) Quên mask khi chỉ muốn match một nửa: `xreg1=0xABCD0000` mặc định exact 64-bit (low half = 0); cần `xreg1=0xABCD000000000000/0xFFFF000000000000` để chỉ match high 16 bit của reg2.",
    "**Common failures.** (a) Writing `xreg1` inside the OVN pipeline overwrites `reg2` and `reg3` (the NAT working copy). Reply traffic cannot restore the original IP, and packets take the wrong route. (b) Confusing `xreg1` with `xreg0`. `xreg0` covers `reg0` and `reg1` (the ACL flag and the datapath copy); `xreg1` covers `reg2` and `reg3` (the NAT working copy). The semantics in OVN differ completely. (c) Writing `xxreg0` overwrites both `xreg0` and `xreg1` (which is `reg0` through `reg3`) at once. The ACL flag, the datapath copy, and the NAT working copy are all lost, and the LR pipeline collapses. (d) OF 1.0, 1.1, and 1.2 controllers do not support `xreg1`. (e) Forgetting the mask when matching only half: `xreg1=0xABCD0000` is treated as an exact 64-bit match (with a low half of 0). Use `xreg1=0xABCD000000000000/0xFFFF000000000000` to match only the high 16 bits of `reg2`.",
)


def main() -> int:
    text = FILE.read_text(encoding="utf-8")
    not_found: list[str] = []
    applied = 0
    for vi, en in REPLACEMENTS:
        if vi not in text:
            not_found.append(vi[:80])
            continue
        if text.count(vi) > 1:
            not_found.append(f"AMBIGUOUS({text.count(vi)}x): " + vi[:80])
            continue
        text = text.replace(vi, en, 1)
        applied += 1
    FILE.write_text(text, encoding="utf-8")
    print(f"Applied {applied}/{len(REPLACEMENTS)} replacements.")
    if not_found:
        print(f"Skipped {len(not_found)} blocks (not found / ambiguous):", file=sys.stderr)
        for s in not_found:
            print("  -", s, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
