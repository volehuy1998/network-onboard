# Template B — Per-field block cho OpenFlow / OVN match field

> **Mục tiêu:** định nghĩa một match field (eth_src, nw_src, tun_id, ct_state, reg0, metadata, v.v.) theo pattern chuẩn của `ovs-fields(7)`.
> **Upstream baseline:** man `ovs-fields(7)`, 100+ field, mỗi field 15-25 dòng, 9-10 attribute anatomy.
> **Tối thiểu:** 30 dòng per field.

## Skeleton

```markdown
### Match field `<field_name>`

| Attribute | Giá trị |
|---|---|
| **Name** | `<field>` (hoặc aliases: `<alt1>`, `<alt2>`) |
| **Width** | `<N>` bits (ví dụ 32 bit cho IPv4) |
| **Format** | `<format>` (hex / decimal / MAC 6-byte / IPv4 dotted / IPv6 colon / string) |
| **Masking** | bitwise / CIDR prefix / exact match only / không hỗ trợ masking |
| **Prerequisites** | `<match prerequisites>`, ví dụ `eth_type=0x0800` cho IP layer field |
| **Access** | read-only trong match + write qua `<action tương ứng>` / read-only-in-flows |
| **OpenFlow 1.0** | có / không. Nếu có thì tên cụ thể `OFPFW_<name>` |
| **OpenFlow 1.1+ OXM** | `OXM_OF_<name>` code `<N>` type `<class>.<field>` |
| **NXM** | `NXM_OF_<name>` hoặc `NXM_NX_<name>` code `<N>` |
| **Semantics trong packet** | <mô tả 2-4 dòng> |

**Vị trí trong packet header** (nếu field thuộc wire protocol):

<ASCII diagram hoặc RFC reference, ví dụ `eth_src` là byte 0-5 của Ethernet frame theo IEEE 802.3>.

**Ví dụ match syntax** (trong flow spec của `ovs-ofctl`):

\`\`\`
priority=100,<field>=<value>,actions=<...>
priority=100,<field>=<value>/<mask>,actions=<...>    # nếu support mask
\`\`\`

**Action liên quan** (field có thể modify bằng action nào):

- `<action1>`: modify field này
- `<action2>`: read field này làm parameter

**Use case pipeline**:

<2-4 dòng: field này thường được match ở stage nào của pipeline OVN/OVS, dùng làm key cho ACL / LB / routing / metadata passing>.

**Kịch bản bẻ gãy khi quên prerequisites**:

- Nếu dùng `<field>=<value>` mà thiếu `eth_type=0x0800` → flow spec báo lỗi "`field not in normal form`" vì OVS không biết field này là L3 nên không set L2 prerequisite.

**Upstream:**
- man `ovs-fields(7)` §`<section>`
- RFC nếu là wire field: ví dụ RFC 791 §3.1 cho IPv4 header
```

## Nhóm match field foundation cần cover

OpenFlow 1.5 + OVS extensions gồm **~100 field**. Cần cover theo nhóm (xem ovs-fields(7) structure):

**Nhóm A, Metadata (6 field):** `in_port`, `in_port_oxm`, `actset_output`, `skb_priority`, `pkt_mark`, `metadata`.

**Nhóm B, Register (19 field):** `reg0`-`reg15`, `xreg0`-`xreg7`, `xxreg0`-`xxreg3`, `OXM_OF_METADATA`.

**Nhóm C, Tunnel (~30 field):** `tun_id`, `tun_src`, `tun_dst`, `tun_ipv6_src`, `tun_ipv6_dst`, `tun_flags`, `tun_ttl`, `tun_tos`, `tun_metadata0`-`tun_metadata63`, `tun_gbp_id`, `tun_gbp_flags`, `tun_erspan_ver`.

**Nhóm D, L2 (9 field):** `eth_src`, `eth_dst`, `eth_type`, `vlan_tci`, `vlan_vid`, `vlan_pcp`, `dl_vlan_present`, `packet_type`, `conj_id`.

**Nhóm E, ARP (5 field):** `arp_op`, `arp_spa`, `arp_tpa`, `arp_sha`, `arp_tha`.

**Nhóm F, L3 IPv4 (6 field):** `ipv4_src`, `ipv4_dst`, `nw_proto`, `nw_tos`, `nw_ecn`, `nw_ttl`.

**Nhóm G, L3 IPv6 (7 field):** `ipv6_src`, `ipv6_dst`, `ipv6_label`, `ipv6_exthdr`, `nd_target`, `nd_sll`, `nd_tll`.

**Nhóm H, L4 (8 field):** `tcp_src`, `tcp_dst`, `tcp_flags`, `udp_src`, `udp_dst`, `sctp_src`, `sctp_dst`, `icmp_type`, `icmp_code`.

**Nhóm I, MPLS (4 field):** `mpls_label`, `mpls_tc`, `mpls_bos`, `mpls_ttl`.

**Nhóm J, Conntrack (9 field):** `ct_state`, `ct_zone`, `ct_mark`, `ct_label`, `ct_nw_src`, `ct_nw_dst`, `ct_nw_proto`, `ct_tp_src`, `ct_tp_dst`.

**Nhóm K, IP frag (1 field):** `ip_frag`.

Tổng 104 field. Priority Phase H: nhóm A, B, D, F, G, J (foundation core, ~40 field) phải được cover. Nhóm C (tunnel), H, I xếp tier 2.
