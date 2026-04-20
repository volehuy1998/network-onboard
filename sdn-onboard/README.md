# SDN Onboard — OVN/OVS chuyên sâu

Chuỗi tài liệu nghiên cứu về Software Defined Networking trong môi trường OpenStack production, tập trung vào OVN (Open Virtual Network), OpenvSwitch, và OpenFlow. Mọi case study và log forensics đều lấy từ hệ thống thật chạy kolla-ansible trên hàng trăm node.

## Mục lục

### Part 1 — OVN L2 Forwarding và FDB Poisoning (1234 dòng)

[1.0 - ovn-l2-forwarding-and-fdb-poisoning.md](1.0%20-%20ovn-l2-forwarding-and-fdb-poisoning.md)

| Section | Nội dung |
|---------|---------|
| 1.1 | Tại sao OVN tồn tại: bài toán gốc và hành trình giải quyết |
| 1.2 | Localnet port: cầu nối giữa thế giới ảo và VLAN vật lý |
| 1.3 | MC_FLOOD và MC_UNKNOWN: broadcast và unknown destination trong distributed control plane |
| 1.4 | FDB table và dynamic MAC learning: từ bài toán flooding đến caching |
| 1.5 | MAC_Binding table: IP-to-MAC resolution trên logical router |
| 1.6 | **Case study: FDB poisoning trên provider network VLAN 3808** — forensic timeline từ 3 daemon logs (ovn-controller, ovs-vswitchd, nova-compute), phân tích bug FDP-620 |
| 1.7 | Bài học thiết kế: trade-off và tiến hóa incremental |

Exercises: GE1 (MC_UNKNOWN POE), GE2 (FDB 3-condition POE), Lab 3 (FDB poisoning diagnosis)

### Part 2 — OVN ARP Responder và BUM Suppression (496 dòng)

[2.0 - ovn-arp-responder-and-bum-suppression.md](2.0%20-%20ovn-arp-responder-and-bum-suppression.md)

| Section | Nội dung |
|---------|---------|
| 2.1 | Bối cảnh: ARP trên mạng vật lý và hiệu ứng khuếch đại trong overlay |
| 2.2 | Dòng chảy lịch sử: từ l2population đến ARP Responder tích hợp trong OVN |
| 2.3 | Cơ chế ARP Responder: Ingress Table 26 và hệ thống bốn tầng priority |
| 2.4 | Port_security: gate trung tâm quyết định ARP Responder có hoạt động hay không |
| 2.5 | ARP Responder và FDB: hai cơ chế độc lập cho hai bài toán |
| 2.6 | Khi ARP Responder vắng mặt: incidents thực tế và đánh giá triển khai |
| 2.7 | Bốn kiến trúc ARP suppression và arp_proxy |

Exercises: GE1 (ARP Responder POE), GE2 (BUM suppression POE), Lab 3 (troubleshooting)

### Part 3 — OVN Multichassis Binding, PMTUD và activation-strategy (1379 dòng)

[3.0 - ovn-multichassis-binding-and-pmtud.md](3.0%20-%20ovn-multichassis-binding-and-pmtud.md)

| Section | Nội dung |
|---------|---------|
| 3.1 | Lịch sử ba thời kỳ live migration trong OVN: pre-22.09 blackhole 13.25% loss → 22.09 multichassis duplicate → 24.03+ activation-strategy=rarp |
| 3.2 | Multichassis port binding lifecycle: CAN_BIND_AS_MAIN/ADDITIONAL/CANNOT_BIND, timeline, 6 scenarios matrix |
| 3.3 | `enforce_tunneling_for_multichassis_ports()`: priority 110 override localnet 100, 6 kịch bản packet path |
| 3.4 | Geneve 58-byte overhead, pipeline tables 41/42, **bug FDP-620 root cause** + patch Ales Musil 6-line |
| 3.5 | activation-strategy=rarp: ba "cửa khóa" flows (priority 1010/1000), pinctrl_activation_strategy_handler, 4 reasons RARP > GARP |
| 3.6 | Operational tuning: Jumbo frame MTU 9000→8942, mtu_expires kernel tuning |
| 3.7 | Design lessons: data-plane-as-signal pattern, Prometheus exporter, 3-phase deployment |

Labs: Lab 1 (verification playbook sáu lớp — POE framework), Lab 2 (FDP-620 reproduce với `ping -s 6000`), Lab 3 (Geneve overhead measurement bằng tcpdump+wireshark)

## Sơ đồ phụ thuộc kiến thức

```
Part 1 ──► Part 2
(L2, FDB)   (ARP, BUM)
   │
   └──────► Part 3
            (Multichassis, PMTUD, RARP)

Part 2 references từ Part 1:
  - Localnet port concept (1.2)
  - MC_UNKNOWN group (1.3)
  - FDB table (1.4)
  - MAC_Binding table (1.5)

Part 3 references từ Part 1:
  - Localnet port + chassisredirect (1.2)
  - Multichassis binding (1.2 — Chassis, Claim, Multichassis section)
  - Live migration trigger scenario (1.6 — section "Live migration")
  - FDB table interaction trong live migration (1.4 + 1.6)
```

Đọc Part 1 trước Part 2 và Part 3. Part 3 đào sâu cơ chế multichassis mà Part 1 đã giới thiệu ở mức conceptual; Part 2 độc lập với Part 3 (ARP responder ≠ multichassis binding).

## Log files sử dụng trong case study

Case study FDB poisoning (Part 1, section 1.6) sử dụng log thật từ destination host `vhhl1c2wc1tsn01` ngày 2026-04-08:

| Daemon | Timezone | Khoảng thời gian (UTC) |
|--------|----------|----------------------|
| ovn-controller | UTC | 15:39:40.455 — 15:39:47.392 |
| ovs-vswitchd | UTC | 15:39:37.947 — 15:39:40.623 |
| nova-compute | UTC+7 (container local) | 15:39:37.731 — 15:39:52.375 |

Mọi log entry trong tài liệu đã được đối chiếu verbatim với file log gốc (Rule 7a — System Log Absolute Integrity).
