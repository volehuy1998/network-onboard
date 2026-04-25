# Keyword Rubric Scorecard (v3.7 Phase D output)

> **Auto-generated** by `scripts/per_keyword_rubric_audit.py`.
> **Total keyword:** 383
> **Rubric:** `memory/sdn/rubric-20-per-keyword.md` v1.0
> **Confidence:** auto-detect heuristic ~75%, manual override ~25% via `manual-overrides.csv` (Phase D2 manual review).

## Tier distribution

| Tier | Count | % | Threshold |
|------|-------|---|-----------|
| DEEP-20 | 26 | 6.8% | ≥ 18/20 |
| DEEP-15 | 30 | 7.8% | 15-17.5/20 |
| PARTIAL-10 | 41 | 10.7% | 10-14.5/20 |
| REFERENCE-5 | 133 | 34.7% | 5-9.5/20 |
| PLACEHOLDER | 153 | 39.9% | < 5/20 |

**Aggregate average:** 6.56/20 (32.8%)

---

## REF Section 1.1.1 (4 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| `ovsdb-server` | 18.0/20 | DEEP-20 | 32 | 2,3,4 |  |
| `ovs-monitor-ipsec` | 8.5/20 | REFERENCE-5 | 2 | 6,9,11 | 5,12,13 |
| `ovs-tcpdump` | 9.5/20 | REFERENCE-5 | 2 | 6,7,9 | 2,5,12 |
| `Control socket / pidfile convention` | 5.0/20 | REFERENCE-5 | 2 | 15,1,3 | 2,5,6 |

## REF Section 1.1.2 (20 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| `openvswitch.ko (kernel datapath)` | 15.0/20 | DEEP-15 | 15 | 1,3,4 | 5,6,14 |
| `Megaflow` | 14.5/20 | PARTIAL-10 | 23 | 2,3,4 | 5,18,20 |
| `Upcall` | 12.0/20 | PARTIAL-10 | 13 | 3,4,8 | 2,5,6 |
| `Handler thread` | 6.5/20 | REFERENCE-5 | 4 | 3,8,1 | 2,5,6 |
| `Revalidator thread` | 6.0/20 | REFERENCE-5 | 6 | 1,3,4 | 2,5,6 |
| `Recirculation (`recirc_id`)` | 8.0/20 | REFERENCE-5 | 6 | 1,8,9 | 2,5,6 |
| `Connection tracking (`ct`)` | 6.5/20 | REFERENCE-5 | 3 | 7,11,1 | 2,5,6 |
| ``ct_state`` | 15.5/20 | DEEP-15 | 14 | 2,3,4 | 6,19 |
| ``ct_zone`` | 12.5/20 | PARTIAL-10 | 7 | 2,4,5 | 6,12,17 |
| ``ct_mark`` | 7.5/20 | REFERENCE-5 | 4 | 11,13,1 | 5,6,12 |
| ``ct_label`` | 7.5/20 | REFERENCE-5 | 5 | 11,13,1 | 5,6,12 |
| `ALG (FTP/TFTP/SIP)` | 8.0/20 | REFERENCE-5 | 3 | 3,7,9 | 5,6,12 |
| `NAT` | 18.5/20 | DEEP-20 | 52 | 2,3,4 |  |
| ``learn` action` | 5.5/20 | REFERENCE-5 | 3 | 1,9,3 | 2,5,6 |
| `Megaflow wildcarding` | 2.5/20 | PLACEHOLDER | 1 | 1,3,4 | 2,5,6 |
| `UFID (Unique Flow ID)` | 11.0/20 | PARTIAL-10 | 5 | 2,6,9 | 5,13,18 |
| `Interface type: `internal`` | 3.5/20 | PLACEHOLDER | 1 | 10,1,3 | 2,5,6 |
| `Interface type: `patch`` | 3.5/20 | PLACEHOLDER | 1 | 10,1,3 | 2,5,6 |
| `VLAN bridge modes (`Port.vlan_mode`)` | 3.5/20 | PLACEHOLDER | 1 | 9,1,3 | 2,5,6 |
| `Bond mode (`Port.bond_mode`)` | 7.0/20 | REFERENCE-5 | 2 | 1,15,3 | 2,5,6 |

## REF Section 1.1.3 (16 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| `OVSDB schema` | 9.5/20 | REFERENCE-5 | 13 | 1,4,7 | 5,6,14 |
| `Transactional model` | 2.5/20 | PLACEHOLDER | 1 | 1,3,4 | 2,5,6 |
| `RAFT clustering` | 2.5/20 | PLACEHOLDER | 1 | 1,3,4 | 2,5,6 |
| `Active-backup replication` | 2.5/20 | PLACEHOLDER | 1 | 1,3,4 | 2,5,6 |
| `JSON-RPC monitor` | 2.5/20 | PLACEHOLDER | 1 | 1,3,4 | 2,5,6 |
| ``Open_vSwitch` table (root)` | 6.0/20 | REFERENCE-5 | 4 | 20,1,3 | 2,5,6 |
| ``Bridge` table` | 6.5/20 | REFERENCE-5 | 4 | 3,9,11 | 2,5,6 |
| ``Port` table` | 6.5/20 | REFERENCE-5 | 5 | 3,9,11 | 2,5,6 |
| ``Interface` table` | 9.0/20 | REFERENCE-5 | 8 | 3,8,9 | 2,5,6 |
| ``Controller` table` | 6.0/20 | REFERENCE-5 | 4 | 3,9,1 | 2,5,6 |
| ``Manager` table` | 5.5/20 | REFERENCE-5 | 4 | 9,1,3 | 2,5,6 |
| ``Mirror` table` | 7.0/20 | REFERENCE-5 | 3 | 1,8,9 | 2,5,6 |
| ``NetFlow` / `sFlow` / `IPFIX`` | 4.5/20 | PLACEHOLDER | 1 | 1,3,4 | 2,5,6 |
| ``SSL` table` | 4.5/20 | PLACEHOLDER | 1 | 1,3,4 | 2,5,6 |
| ``Flow_Table` table` | 5.5/20 | REFERENCE-5 | 2 | 3,9,1 | 2,5,6 |
| ``CT_Zone` / `CT_Timeout_Policy`` | 5.0/20 | REFERENCE-5 | 2 | 1,3,4 | 2,5,6 |

## REF Section 1.1.4 (17 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| `ovs-vsctl` | 19.0/20 | DEEP-20 | 79 | 2,3,4 |  |
| `Bridge subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Port subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Interface subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Controller subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Manager subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `SSL subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Generic database subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovs-ofctl` | 18.5/20 | DEEP-20 | 65 | 2,3,4 |  |
| `ovs-appctl` | 19.0/20 | DEEP-20 | 65 | 2,3,4 |  |
| `ovs-dpctl` | 17.5/20 | DEEP-15 | 18 | 2,3,4 |  |
| `ovsdb-tool` | 15.5/20 | DEEP-15 | 19 | 2,3,4 | 6,20 |
| `ovsdb-client` | 15.0/20 | DEEP-15 | 19 | 3,4,5 | 14,20 |
| `Other utilities` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| ``ovs-pki`` | 12.0/20 | PARTIAL-10 | 9 | 1,3,4 | 6,14,18 |
| ``ovs-testcontroller`` | 5.0/20 | REFERENCE-5 | 3 | 1,3,4 | 2,5,6 |
| ``vtep-ctl`` | 8.5/20 | REFERENCE-5 | 5 | 1,4,9 | 2,5,6 |

## REF Section 1.1.5 (12 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| ``ovs-appctl coverage/show`` | 19.0/20 | DEEP-20 | 47 | 2,3,5 |  |
| ``ovs-appctl dpif/show`` | 19.0/20 | DEEP-20 | 48 | 2,3,5 |  |
| ``ovs-appctl dpif/dump-flows BR`` | 8.0/20 | REFERENCE-5 | 11 | 3,9,11 | 2,5,6 |
| ``ovs-appctl ofproto/trace`` | 19.0/20 | DEEP-20 | 45 | 2,3,4 |  |
| ``ovs-appctl fdb/show BR`` | 5.5/20 | REFERENCE-5 | 3 | 15,1,3 | 2,5,6 |
| ``ovs-appctl bond/show` / `lacp/show`` | 19.0/20 | DEEP-20 | 48 | 2,3,5 |  |
| ``ovs-appctl vlog/list` / `vlog/set`` | 15.0/20 | DEEP-15 | 33 | 3,4,6 | 5,18 |
| ``ovs-appctl memory/show`` | 19.0/20 | DEEP-20 | 47 | 2,3,5 |  |
| ``ovs-appctl upcall/show`` | 19.0/20 | DEEP-20 | 47 | 2,3,5 |  |
| ``ovs-appctl dpctl/dump-conntrack`` | 8.0/20 | REFERENCE-5 | 9 | 3,6,15 | 2,5,13 |
| ``ovs-appctl revalidator/wait` / `revalidator/purge`` | 11.0/20 | PARTIAL-10 | 15 | 3,9,11 | 2,5,6 |
| `OpenFlow protocol version negotiation` | 2.5/20 | PLACEHOLDER | 1 | 1,3,4 | 2,5,6 |

## REF Section 2.2.1 (11 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| `Pipeline Architecture` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Table Chaining via goto_table` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Packet Metadata Fields` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Action Set vs Action List` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `write_metadata Instruction` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Group Tables (all/select/indirect/fast_failover)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Meter Table` | 13.0/20 | PARTIAL-10 | 15 | 2,6,7 | 5,17,19 |
| `Instructions vs Actions Distinction` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Multipart Messages (OFPT_MULTIPART_REQUEST/REPLY)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `OpenFlow Reserved Port Numbers` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Table 0 Ingress Pipeline` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |

## REF Section 2.2.2 (83 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| `in_port (16 bits, OpenFlow 1.0+)` | 15.5/20 | DEEP-15 | 48 | 2,3,5 | 19,20 |
| `in_phy_port (32 bits, OpenFlow 1.2+ / OVS 1.7+)` | 7.5/20 | REFERENCE-5 | 2 | 9,1,2 | 5,6,12 |
| `eth_src / eth_dst (48 bits, OF 1.2+ / OVS 1.1+)` | 10.0/20 | PARTIAL-10 | 14 | 2,8,9 | 5,6,17 |
| `eth_type (16 bits, OF 1.2+ / OVS 1.1+)` | 10.5/20 | PARTIAL-10 | 15 | 2,9,10 | 5,6,17 |
| `vlan_vid (12 bits, OF 1.2+ / OVS 1.7+)` | 8.0/20 | REFERENCE-5 | 9 | 2,9,14 | 5,6,12 |
| `vlan_pcp (3 bits, OF 1.2+ / OVS 1.7+)` | 7.0/20 | REFERENCE-5 | 7 | 2,1,3 | 5,6,12 |
| `ip_dscp (6 bits, OF 1.2+ / OVS 1.7+)` | 6.5/20 | REFERENCE-5 | 3 | 1,2,3 | 5,6,12 |
| `ip_ecn (2 bits, OF 1.2+ / OVS 1.7+)` | 6.0/20 | REFERENCE-5 | 2 | 1,2,3 | 5,6,7 |
| `ip_proto (8 bits, OF 1.2+ / OVS 1.1+)` | 7.5/20 | REFERENCE-5 | 6 | 2,8,1 | 5,6,12 |
| `ipv4_src / ipv4_dst (32 bits, OF 1.2+ / OVS 1.1+)` | 8.0/20 | REFERENCE-5 | 7 | 2,13,14 | 5,6,12 |
| `ipv6_src / ipv6_dst (128 bits, OF 1.2+ / OVS 1.1+)` | 7.5/20 | REFERENCE-5 | 2 | 2,13,1 | 5,6,12 |
| `ipv6_flabel (20 bits, OF 1.2+ / OVS 1.11+)` | 8.5/20 | REFERENCE-5 | 2 | 1,5,8 | 6,12,17 |
| `ipv6_exthdr (16 bits, OF 1.2+ / OVS 1.11+)` | 7.0/20 | REFERENCE-5 | 2 | 9,1,2 | 5,6,12 |
| `tcp_src / tcp_dst (16 bits, OF 1.2+ / OVS 1.1+)` | 9.0/20 | REFERENCE-5 | 7 | 2,9,13 | 5,6,17 |
| `udp_src / udp_dst (16 bits, OF 1.2+ / OVS 1.1+)` | 8.0/20 | REFERENCE-5 | 6 | 2,13,14 | 5,6,12 |
| `sctp_src / sctp_dst (16 bits, OF 1.2+ / OVS 2.0+)` | 7.5/20 | REFERENCE-5 | 2 | 2,13,1 | 5,6,12 |
| `icmp_type / icmp_code (8 bits, OF 1.2+ / OVS 1.1+)` | 8.0/20 | REFERENCE-5 | 3 | 2,9,13 | 5,6,12 |
| `arp_op (16 bits, OF 1.2+ / OVS 1.1+)` | 10.0/20 | PARTIAL-10 | 7 | 2,5,9 | 6,18,19 |
| `arp_spa / arp_tpa (32 bits, OF 1.2+ / OVS 1.1+)` | 13.5/20 | PARTIAL-10 | 9 | 2,3,5 | 18,19 |
| `arp_sha / arp_tha (48 bits, OF 1.2+ / OVS 1.1+)` | 9.5/20 | REFERENCE-5 | 4 | 2,6,9 | 5,17,18 |
| `mpls_label (20 bits, OF 1.2+ / OVS 1.11+)` | 7.0/20 | REFERENCE-5 | 5 | 11,1,2 | 5,6,12 |
| `mpls_tc (3 bits, OF 1.2+ / OVS 1.11+)` | 7.5/20 | REFERENCE-5 | 3 | 9,11,1 | 5,6,12 |
| `mpls_bos (1 bit, OF 1.3+ / OVS 1.11+)` | 8.0/20 | REFERENCE-5 | 4 | 9,11,1 | 5,6,17 |
| `tunnel_id / tun_id (64 bits, OF 1.3+ / OVS 1.1+)` | 13.5/20 | PARTIAL-10 | 15 | 1,2,3 | 5,6,18 |
| `pbb_isid (24 bits, PB/VB)` | 9.0/20 | REFERENCE-5 | 3 | 6,9,13 | 5,12,17 |
| `metadata (64 bits, OF 1.2+ / OVS 1.8+)` | 20.0/20 | DEEP-20 | 61 | 1,2,3 |  |
| `reg0-reg15 (32 bits each, OVS 1.1+)` | 6.0/20 | REFERENCE-5 | 2 | 1,2,3 | 5,6,12 |
| `xreg0-xreg7 (64 bits each, OF 1.3+ / OVS 2.4+)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `xxreg0-xxreg3 (128 bits each, OVS 2.6+)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ct_state (32 bits, OVS 2.5+)` | 16.0/20 | DEEP-15 | 20 | 2,3,4 | 6 |
| `ct_zone (16 bits, OVS 2.5+)` | 15.5/20 | DEEP-15 | 17 | 2,4,5 | 6,19 |
| `ct_mark (32 bits, OVS 2.5+)` | 9.0/20 | REFERENCE-5 | 12 | 3,9,11 | 5,6,12 |
| `ct_label (128 bits, OVS 2.5+)` | 12.0/20 | PARTIAL-10 | 15 | 6,7,8 | 5,18,19 |
| `ct_nw_proto (8 bits, OVS 2.8+)` | 5.5/20 | REFERENCE-5 | 2 | 1,2,3 | 5,6,7 |
| `ct_tp_src / ct_tp_dst (16 bits, OVS 2.8+)` | 7.5/20 | REFERENCE-5 | 3 | 2,11,1 | 5,6,12 |
| `conj_id (32 bits, OVS 2.4+)` | 7.0/20 | REFERENCE-5 | 5 | 9,1,2 | 5,6,12 |
| `pkt_mark (32 bits, OVS 2.0+)` | 5.5/20 | REFERENCE-5 | 2 | 1,2,3 | 5,6,12 |
| `tcp_flags (16 bits, OVS 2.1+ / NXM_NX_TCP_FLAGS)` | 9.0/20 | REFERENCE-5 | 9 | 2,14,15 | 5,6,17 |
| `dp_hash (32 bits, OVS 2.2+ / NXM_NX_DP_HASH)` | 7.0/20 | REFERENCE-5 | 4 | 3,8,9 | 2,5,6 |
| `actset_output (32 bits, OVS 2.4+ / OF 1.5+)` | 6.5/20 | REFERENCE-5 | 1 | 2,14,1 | 5,6,7 |
| `NSH fields (OVS 2.8+ / Network Service Header — RFC 8300)` | 4.5/20 | PLACEHOLDER | 1 | 1,3,4 | 2,5,6 |
| `Instruction: meter` | 19.0/20 | DEEP-20 | 41 | 2,3,4 |  |
| `Instruction: apply_actions` | 7.0/20 | REFERENCE-5 | 5 | 9,11,1 | 5,6,12 |
| `Instruction: clear_actions` | 2.5/20 | PLACEHOLDER | 1 | 1,3,4 | 2,5,6 |
| `Instruction: write_actions` | 7.0/20 | REFERENCE-5 | 4 | 9,11,1 | 5,6,12 |
| `Instruction: write_metadata` | 6.5/20 | REFERENCE-5 | 7 | 7,9,1 | 2,5,6 |
| `Instruction: goto_table` | 16.0/20 | DEEP-15 | 18 | 2,3,4 | 19 |
| `Action: output` | 20.0/20 | DEEP-20 | 89 | 1,2,3 |  |
| `Action: group` | 19.5/20 | DEEP-20 | 72 | 1,2,3 |  |
| `Action: drop (implicit)` | 20.0/20 | DEEP-20 | 91 | 1,2,3 |  |
| `Action: set_field` | 15.0/20 | DEEP-15 | 21 | 2,3,4 | 5,6,19 |
| `Action: copy_field (OpenFlow 1.5+)` | 10.5/20 | PARTIAL-10 | 4 | 2,5,9 | 6,12,17 |
| `Action: push_vlan` | 8.5/20 | REFERENCE-5 | 8 | 3,4,9 | 5,6,12 |
| `Action: pop_vlan` | 8.5/20 | REFERENCE-5 | 6 | 3,4,13 | 5,6,12 |
| `Action: push_mpls` | 6.5/20 | REFERENCE-5 | 3 | 1,2,3 | 5,6,12 |
| `Action: pop_mpls` | 8.5/20 | REFERENCE-5 | 3 | 1,9,13 | 5,6,17 |
| `Action: push_pbb` | 8.0/20 | REFERENCE-5 | 3 | 2,9,14 | 5,6,12 |
| `Action: pop_pbb` | 8.5/20 | REFERENCE-5 | 3 | 2,9,13 | 5,6,12 |
| `Action: set_queue` | 11.5/20 | PARTIAL-10 | 10 | 2,6,7 | 5,17,19 |
| `Action: dec_ttl` | 12.0/20 | PARTIAL-10 | 11 | 2,3,4 | 5,6,19 |
| `Action: dec_mpls_ttl` | 7.0/20 | REFERENCE-5 | 2 | 9,1,2 | 5,6,12 |
| `Action: set_mpls_ttl` | 7.0/20 | REFERENCE-5 | 3 | 9,1,2 | 5,6,12 |
| `Action: copy_ttl_in` | 7.5/20 | REFERENCE-5 | 3 | 9,13,1 | 5,6,12 |
| `Action: copy_ttl_out` | 5.5/20 | REFERENCE-5 | 2 | 1,3,4 | 2,5,6 |
| `Action: set_nw_ttl` | 7.0/20 | REFERENCE-5 | 2 | 9,1,2 | 5,6,12 |
| `Action: resubmit (Nicira extension, OVS 1.1+)` | 17.0/20 | DEEP-15 | 30 | 2,3,4 | 19 |
| `Action: learn (Nicira extension, OVS 1.11+)` | 19.0/20 | DEEP-20 | 64 | 2,3,5 |  |
| `Action: conjunction (Nicira extension, OVS 2.4+)` | 12.5/20 | PARTIAL-10 | 15 | 2,6,7 | 5,17,19 |
| `Action: ct (Nicira extension, OVS 2.5+)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Action: ct_clear (Nicira extension, OVS 2.5+)` | 7.5/20 | REFERENCE-5 | 6 | 7,9,1 | 5,6,12 |
| `Action: decap (Nicira extension, OVS 2.1+)` | 15.0/20 | DEEP-15 | 24 | 2,3,4 | 5,6,19 |
| `Action: encap (Nicira extension, OVS 2.1+)` | 17.5/20 | DEEP-15 | 54 | 2,3,4 | 19 |
| `Action: controller (Nicira extension)` | 19.5/20 | DEEP-20 | 112 | 1,2,3 |  |
| `Action: note (Nicira extension)` | 13.5/20 | PARTIAL-10 | 19 | 2,3,4 | 6,19,20 |
| `Action: sample (Nicira extension, OVS 2.5+)` | 14.5/20 | PARTIAL-10 | 21 | 2,3,7 | 5,6,19 |
| `Action: exit (Nicira extension)` | 17.0/20 | DEEP-15 | 55 | 2,3,4 | 20 |
| `Action: multipath (Nicira extension, OVS 1.11+)` | 11.0/20 | PARTIAL-10 | 7 | 2,7,8 | 5,6,17 |
| `Action: bundle / bundle_load (Nicira extension, OVS 1.11+)` | 17.5/20 | DEEP-15 | 27 | 2,3,4 |  |
| `Action: fin_timeout (Nicira extension, OVS 1.11+)` | 11.0/20 | PARTIAL-10 | 1 | 1,2,5 | 6,12,17 |
| `Action: move (Nicira extension)` | 19.5/20 | DEEP-20 | 58 | 2,3,4 |  |
| `Action: output:NXM (dynamic port)` | 4.5/20 | PLACEHOLDER | 2 | 1,3,4 | 2,5,6 |
| `Action: push:src (Nicira extension)` | 7.0/20 | REFERENCE-5 | 1 | 2,9,1 | 5,6,7 |
| `Action: pop:dst (Nicira extension)` | 7.0/20 | REFERENCE-5 | 1 | 2,9,1 | 5,6,7 |

## REF Section 2.2.3 (23 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| `OFPT_HELLO (Type 0, OpenFlow 1.0+)` | 10.0/20 | PARTIAL-10 | 7 | 2,8,9 | 5,6,12 |
| `OFPT_FEATURES_REQUEST (Type 5, OpenFlow 1.0+)` | 8.5/20 | REFERENCE-5 | 6 | 2,9,11 | 5,6,12 |
| `OFPT_FEATURES_REPLY (Type 6, OpenFlow 1.0+)` | 8.5/20 | REFERENCE-5 | 7 | 2,8,9 | 5,6,12 |
| `OFPT_PACKET_IN (Type 10, OpenFlow 1.0+)` | 7.5/20 | REFERENCE-5 | 7 | 9,13,1 | 5,6,12 |
| `OFPT_PACKET_OUT (Type 13, OpenFlow 1.0+)` | 8.0/20 | REFERENCE-5 | 4 | 5,9,1 | 6,12,17 |
| `OFPT_FLOW_MOD (Type 14, OpenFlow 1.0+)` | 9.5/20 | REFERENCE-5 | 5 | 2,9,11 | 5,6,17 |
| `OFPT_BARRIER_REQUEST / OFPT_BARRIER_REPLY (Types 20/21, Open` | 8.5/20 | REFERENCE-5 | 4 | 5,9,13 | 6,12,17 |
| `OFPT_ECHO_REQUEST / OFPT_ECHO_REPLY (Types 2/3, OpenFlow 1.0` | 7.0/20 | REFERENCE-5 | 3 | 9,1,2 | 5,6,12 |
| `OFPT_MULTIPART_REQUEST (Type 18, OpenFlow 1.3+)` | 7.0/20 | REFERENCE-5 | 2 | 9,13,1 | 5,6,7 |
| `OFPT_MULTIPART_REPLY (Type 19, OpenFlow 1.3+)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `OFPT_PORT_STATUS (Type 12, OpenFlow 1.0+)` | 6.5/20 | REFERENCE-5 | 4 | 9,1,2 | 5,6,7 |
| `OFPT_FLOW_REMOVED (Type 11, OpenFlow 1.0+)` | 7.0/20 | REFERENCE-5 | 5 | 9,1,2 | 5,6,12 |
| `OFPT_ROLE_REQUEST / OFPT_ROLE_REPLY (Types 24/25, OpenFlow 1` | 8.5/20 | REFERENCE-5 | 4 | 2,4,9 | 5,6,12 |
| `OFPT_GROUP_MOD (Type 15, OpenFlow 1.2+)` | 7.0/20 | REFERENCE-5 | 2 | 2,9,1 | 5,6,7 |
| `OFPT_METER_MOD (Type 29, OpenFlow 1.3+)` | 8.0/20 | REFERENCE-5 | 2 | 2,9,13 | 5,6,7 |
| `OFPT_BUNDLE_OPEN / OFPT_BUNDLE_COMMIT / OFPT_BUNDLE_ADD_MESS` | 8.0/20 | REFERENCE-5 | 5 | 2,9,13 | 5,6,12 |
| `OFPT_REQUESTFORWARD (Type 32, OpenFlow 1.4+)` | 8.0/20 | REFERENCE-5 | 3 | 2,9,11 | 5,6,7 |
| `OFPT_TABLE_STATUS (Type 30, OpenFlow 1.3+)` | 7.5/20 | REFERENCE-5 | 3 | 2,9,13 | 5,6,7 |
| `Connection State Machine: HELLO` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Connection State Machine: FEATURES_REQUEST/REPLY` | 13.5/20 | PARTIAL-10 | 17 | 2,4,5 | 17,19,20 |
| `Connection State Machine: Steady State (ECHO keep-alive)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Auxiliary Connections (OpenFlow 1.3+)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `OFPT_SET_ASYNC (Type 28, OpenFlow 1.4+)` | 9.0/20 | REFERENCE-5 | 4 | 2,9,11 | 5,6,12 |

## REF Section 2.2.4 (9 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| `Single-Table vs Multi-Table Pipeline` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `NXM vs OXM (Match Field Encoding)` | 6.0/20 | REFERENCE-5 | 2 | 1,2,3 | 5,6,7 |
| `Group Tables (OF 1.1+)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Meters (OF 1.3+)` | 7.5/20 | REFERENCE-5 | 3 | 2,14,1 | 5,6,12 |
| `Bundles (OF 1.4+)` | 8.0/20 | REFERENCE-5 | 5 | 2,9,14 | 5,6,12 |
| `Egress Tables (OF 1.5+)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `copy_field (OF 1.5+)` | 10.5/20 | PARTIAL-10 | 4 | 2,5,9 | 6,12,17 |
| `Packet Type Aware Pipeline (OF 1.5+)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Version Support Summary` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |

## REF Section 3.3.1 (16 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| `Daemon: ovn-northd` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Northbound DB Management` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Southbound DB Management` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Daemon: ovn-controller` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Chassis Configuration` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Integration Bridge` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Daemon: ovn-controller-vtep` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Daemon: ovn-ic` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Daemon: ovn-ic-northd` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `OVSDB Server Roles` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `RAFT Clustering` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Relay Mode (ovsdb-server)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Inactivity Probes` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Northd Probe Interval` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Leader Election` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Daemon Threading` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |

## REF Section 3.3.2 (48 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| `NB_Global Table` | 11.0/20 | PARTIAL-10 | 19 | 5,6,9 | 13,14,19 |
| `Logical_Switch Table (NB)` | 18.0/20 | DEEP-20 | 39 | 1,2,3 | 20 |
| `Logical_Switch_Port Table (NB)` | 17.0/20 | DEEP-15 | 30 | 2,3,4 | 20 |
| `Port Security (NB)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `QoS Configuration (NB)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Requested Chassis (NB)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Reside-on-Redirect-Chassis (NB)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Logical_Router Table (NB)` | 17.0/20 | DEEP-15 | 28 | 2,3,4 |  |
| `Logical_Router_Port Table (NB)` | 11.5/20 | PARTIAL-10 | 16 | 3,4,6 | 5,18,19 |
| `Logical_Router_Static_Route (NB)` | 6.5/20 | REFERENCE-5 | 5 | 9,13,1 | 2,5,6 |
| `Logical_Router_Policy (NB)` | 7.0/20 | REFERENCE-5 | 5 | 9,13,1 | 2,5,6 |
| `NAT Table (NB)` | 18.5/20 | DEEP-20 | 52 | 2,3,4 |  |
| `Load_Balancer Table (NB)` | 13.5/20 | PARTIAL-10 | 18 | 3,4,6 | 2,5,14 |
| `Load_Balancer_Group (NB)` | 6.5/20 | REFERENCE-5 | 3 | 9,13,1 | 2,5,6 |
| `Load_Balancer_Health_Check (NB)` | 8.0/20 | REFERENCE-5 | 4 | 8,9,11 | 2,5,6 |
| `Address_Set Table (NB)` | 9.0/20 | REFERENCE-5 | 8 | 6,9,13 | 5,14,18 |
| `Port_Group Table (NB)` | 15.0/20 | DEEP-15 | 22 | 3,4,5 | 14,19 |
| `ACL Table (NB)` | 19.0/20 | DEEP-20 | 80 | 2,3,4 |  |
| `Meter Table (NB)` | 13.0/20 | PARTIAL-10 | 15 | 2,6,7 | 5,17,19 |
| `QoS Table (NB)` | 18.0/20 | DEEP-20 | 49 | 2,3,4 |  |
| `DHCP_Options Table (NB)` | 12.5/20 | PARTIAL-10 | 13 | 4,6,8 | 2,5,14 |
| `Mirror Table (NB)` | 14.0/20 | PARTIAL-10 | 12 | 3,5,7 | 6,14,20 |
| `Mirror_Rule (NB)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Forwarding_Group (NB)` | 4.5/20 | PLACEHOLDER | 3 | 1,3,4 | 2,5,6 |
| `BFD Table (NB)` | 17.0/20 | DEEP-15 | 24 | 1,2,3 | 5,14 |
| `HA_Chassis Table (NB)` | 16.0/20 | DEEP-15 | 16 | 3,4,5 | 2,14,18 |
| `HA_Chassis_Group (NB)` | 16.0/20 | DEEP-15 | 16 | 3,4,5 | 2,14,18 |
| `SB_Global Table` | 10.0/20 | PARTIAL-10 | 13 | 4,7,9 | 5,6,13 |
| `Chassis Table (SB)` | 18.0/20 | DEEP-20 | 45 | 1,2,3 | 14 |
| `Chassis_Private Table (SB)` | 9.0/20 | REFERENCE-5 | 6 | 3,4,9 | 2,5,6 |
| `Encap Table (SB)` | 11.5/20 | PARTIAL-10 | 23 | 2,4,5 | 6,13,14 |
| `Datapath_Binding Table (SB)` | 13.0/20 | PARTIAL-10 | 16 | 3,4,6 | 2,5,14 |
| `Port_Binding Table (SB)` | 18.5/20 | DEEP-20 | 49 | 2,3,4 |  |
| `Port Binding Types (SB)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Logical_Flow Table (SB)` | 17.5/20 | DEEP-15 | 36 | 2,3,4 | 14 |
| `Logical Flow Pipeline` | 5.5/20 | REFERENCE-5 | 1 | 11,16,1 | 2,5,6 |
| `Multicast_Group Table (SB)` | 11.5/20 | PARTIAL-10 | 8 | 3,4,6 | 2,5,13 |
| `MAC_Binding Table (SB)` | 16.5/20 | DEEP-15 | 23 | 2,3,4 | 14 |
| `DNS Table (SB)` | 16.0/20 | DEEP-15 | 24 | 2,3,4 | 5 |
| `RBAC_Role & RBAC_Permission (SB)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `IGMP_Group Table (SB)` | 4.5/20 | PLACEHOLDER | 1 | 1,3,4 | 2,5,6 |
| `Controller_Event Table (SB)` | 6.5/20 | REFERENCE-5 | 4 | 4,9,11 | 2,5,6 |
| `Service_Monitor Table (SB)` | 13.0/20 | PARTIAL-10 | 10 | 3,4,5 | 2,6,14 |
| `Load_Balancer (SB)` | 13.5/20 | PARTIAL-10 | 18 | 3,4,6 | 2,5,14 |
| `Static_MAC_Binding (SB)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `FDB Table (SB)` | 18.5/20 | DEEP-20 | 22 | 1,2,3 | 14 |
| `Logical_DP_Group (SB)` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `IP_Multicast (SB)` | 6.5/20 | REFERENCE-5 | 2 | 4,9,11 | 2,5,6 |

## REF Section 3.3.3 (19 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| `Ingress vs Egress Pipeline` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Logical Datapath Binding` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Tunnel Key Allocation` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Logical Port Tunnel Key` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Standard Switch Table Sequence` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Standard Router Table Sequence` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `VTEP Gateway Integration` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Geneve TLV Encapsulation` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Encapsulation Precedence` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Distributed Gateway Routing` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Distributed NAT` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `DVR-style Logical Patches` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `MLF Local-Only Flag` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `MLF Tunnel Metadata Encoding` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `OVN internal OVS register conventions` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `OVN logical port pipeline table IDs` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `OVN logical port pipeline table IDs — LS_OUT stages` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `OVN logical port pipeline table IDs — LR ingress stages` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `OVN logical port pipeline table IDs — LR egress stages` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |

## REF Section 3.3.4 (66 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| `ovn-nbctl: Northbound DB CLI` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-nbctl --db` | 9.0/20 | REFERENCE-5 | 13 | 3,7,9 | 2,5,6 |
| `ovn-nbctl --wait / --no-wait` | 8.0/20 | REFERENCE-5 | 7 | 9,11,15 | 2,5,6 |
| `ovn-nbctl --print-wait-time` | 6.5/20 | REFERENCE-5 | 1 | 9,11,1 | 2,5,6 |
| `ovn-nbctl --leader-only / --no-leader-only` | 5.0/20 | REFERENCE-5 | 3 | 1,3,4 | 2,5,6 |
| `ovn-nbctl --shuffle-remotes / --no-shuffle-remotes` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-nbctl --bare` | 9.5/20 | REFERENCE-5 | 11 | 6,7,9 | 2,5,13 |
| `ovn-nbctl --no-headings` | 6.5/20 | REFERENCE-5 | 4 | 15,1,3 | 2,5,6 |
| `ovn-nbctl --columns` | 9.0/20 | REFERENCE-5 | 23 | 6,7,9 | 2,5,13 |
| `ovn-nbctl --if-exists` | 6.5/20 | REFERENCE-5 | 7 | 3,9,1 | 2,5,6 |
| `ovn-nbctl --may-exist` | 6.0/20 | REFERENCE-5 | 5 | 3,1,4 | 2,5,6 |
| `ovn-nbctl --dry-run` | 5.0/20 | REFERENCE-5 | 4 | 1,3,4 | 2,5,6 |
| `ovn-nbctl --oneline` | 4.5/20 | PLACEHOLDER | 2 | 1,3,4 | 2,5,6 |
| `ovn-nbctl --timeout` | 5.5/20 | REFERENCE-5 | 5 | 3,1,4 | 2,5,6 |
| `ovn-nbctl --detach` | 6.5/20 | REFERENCE-5 | 9 | 8,1,3 | 2,5,6 |
| `ovn-nbctl -u` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-nbctl logical switch subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-nbctl logical switch port subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-nbctl logical router subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-nbctl ACL subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-nbctl load balancer subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-nbctl static route subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-nbctl NAT subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-nbctl address set / port group subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-nbctl DHCP options subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-nbctl DNS subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-nbctl BFD subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-nbctl load-balancer health-check subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-nbctl generic DB subcommands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-sbctl: Southbound DB CLI` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-sbctl --db` | 9.0/20 | REFERENCE-5 | 13 | 3,7,9 | 2,5,6 |
| `ovn-sbctl --leader-only` | 4.5/20 | PLACEHOLDER | 2 | 1,3,4 | 2,5,6 |
| `ovn-sbctl lflow-list` | 13.0/20 | PARTIAL-10 | 21 | 1,3,6 | 2,5,14 |
| `ovn-sbctl lflow-list --uuid` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-sbctl lflow-list --ovs` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-sbctl lflow-list --vflows` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-sbctl dump-flows` | 17.5/20 | DEEP-15 | 54 | 2,3,5 | 14 |
| `ovn-sbctl chassis-add` | 7.5/20 | REFERENCE-5 | 3 | 4,9,11 | 2,5,6 |
| `ovn-sbctl chassis-del` | 10.5/20 | PARTIAL-10 | 4 | 6,7,9 | 2,5,14 |
| `ovn-sbctl lsp-bind` | 4.5/20 | PLACEHOLDER | 2 | 1,3,4 | 2,5,6 |
| `ovn-sbctl lsp-unbind` | 4.5/20 | PLACEHOLDER | 1 | 1,3,4 | 2,5,6 |
| `ovn-trace: Packet Tracing Tool` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-trace --minimal` | 5.5/20 | REFERENCE-5 | 2 | 15,1,3 | 2,5,6 |
| `ovn-trace --detailed` | 8.5/20 | REFERENCE-5 | 9 | 8,9,11 | 2,5,6 |
| `ovn-trace --ovs` | 5.5/20 | REFERENCE-5 | 2 | 15,1,3 | 2,5,6 |
| `ovn-detrace: OpenFlow-to-OVN Translation` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-appctl: Runtime Control` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-appctl exit` | 17.0/20 | DEEP-15 | 55 | 2,3,4 | 20 |
| `ovn-appctl pause / resume` | 15.0/20 | DEEP-15 | 14 | 2,3,5 | 18,20 |
| `ovn-appctl is-paused / status` | 17.5/20 | DEEP-15 | 52 | 2,3,4 | 14 |
| `ovn-appctl set-n-threads / get-n-threads` | 7.0/20 | REFERENCE-5 | 1 | 9,11,15 | 2,5,6 |
| `ovn-appctl inc-engine/show-stats` | 11.5/20 | PARTIAL-10 | 8 | 3,9,11 | 5,6,14 |
| `ovn-appctl sb-cluster-state-reset / nb-cluster-state-reset` | 5.0/20 | REFERENCE-5 | 1 | 1,3,4 | 2,5,6 |
| `ovn-appctl ct-zone-list` | 9.5/20 | REFERENCE-5 | 6 | 9,11,12 | 2,5,6 |
| `ovn-appctl meter-table-list` | 5.0/20 | REFERENCE-5 | 1 | 1,3,4 | 2,5,6 |
| `ovn-appctl group-table-list` | 5.0/20 | REFERENCE-5 | 1 | 1,3,4 | 2,5,6 |
| `ovn-appctl inject-pkt` | 9.0/20 | REFERENCE-5 | 2 | 6,9,11 | 2,5,13 |
| `ovn-appctl connection-status` | 9.5/20 | REFERENCE-5 | 10 | 3,9,11 | 2,5,6 |
| `ovn-appctl recompute` | 17.0/20 | DEEP-15 | 20 | 2,3,4 | 14,18 |
| `ovn-appctl lflow-cache/flush` | 11.0/20 | PARTIAL-10 | 14 | 3,7,9 | 5,6,13 |
| `ovn-appctl lflow-cache/show-stats` | 12.0/20 | PARTIAL-10 | 8 | 2,3,9 | 5,6,14 |
| `ovn-ic-nbctl` | 9.5/20 | REFERENCE-5 | 3 | 7,9,11 | 5,6,12 |
| ``ovn-ic-nbctl`` | 8.0/20 | REFERENCE-5 | 2 | 7,9,13 | 2,5,6 |
| `ovn-ic-sbctl` | 9.5/20 | REFERENCE-5 | 3 | 7,9,12 | 5,6,14 |
| ``ovn-ic-sbctl`` | 6.0/20 | REFERENCE-5 | 2 | 9,13,1 | 2,5,6 |
| ``ovn-ic` appctl commands` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |

## REF Section 3.3.5 (25 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| `ovn-trace Simulation` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-trace Output Format` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-detrace Reverse Lookup` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-controller Flow Installation Tracing` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Connection Tracking Zone Limits` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `SB Cluster State Monitoring` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `OVN Bug Tools` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ovn-controller Flow Installation Metrics` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `OVN Logical Flow Cache` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Lflow Cache Size Limits` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `OVN Database Monitoring` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Southbound Connection State` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Datapath Binding Verification` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Port Binding Status Inspection` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Logical Flow Debugging` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `OpenFlow Flow Correlation` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Multicast Group Debugging` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `MAC Binding Inspection` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `DNS Resolution Debugging` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Meter and Rate Limiting` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `ACL Logging` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Load Balancer Health Monitoring` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `BFD Health Detection` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `HA Chassis Failover Verification` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Connector Inspection` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |

## REF Section 4 (12 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| `Scenario 1: East-west traffic between two VMs on the same OV` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Scenario 2: North-south egress through OVN distributed gatew` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Scenario 3: OVN load balancer VIP drops new connections afte` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Scenario 4: `ovn-controller` stuck in re-compute / high CPU` | 7.0/20 | REFERENCE-5 | 2 | 9,12,1 | 2,5,6 |
| `Scenario 5: SB DB connection flaps between `ovn-controller` ` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Scenario 6: Geneve tunnel down between two chassis (`br-int`` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Scenario 7: Conntrack zone exhaustion / "ct_zone in use" err` | 5.5/20 | REFERENCE-5 | 2 | 1,3,4 | 2,5,6 |
| `Scenario 8: `ovs-vswitchd` 100 % CPU with revalidator thread` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Scenario 9: OpenFlow bundle commit fails / partial flow inst` | 6.5/20 | REFERENCE-5 | 1 | 9,11,1 | 2,5,6 |
| `Scenario 10: Asymmetric routing in OVN ECMP (return path tak` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Scenario 11: Stale or missing MAC_Binding causes routing bla` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Scenario 12: `ovn-northd` standby does not take over after a` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |

## REF Section 5 (2 keyword)

| Keyword | Total | Tier | Files | Top axes pass | Top axes fail |
|---------|-------|------|-------|---------------|---------------|
| `Scenario 13: VM DNS queries dropped by OVN native DNS` | 0.0/20 | PLACEHOLDER | 0 |  | 1,2,3 |
| `Scenario 14: Geneve/VXLAN MTU fragmentation causing intermit` | 6.5/20 | REFERENCE-5 | 2 | 9,1,3 | 2,5,6 |
