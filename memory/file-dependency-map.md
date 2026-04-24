# File Dependency Map

> Bản đồ phụ thuộc giữa các file trong repo. Khi sửa file A, PHẢI kiểm tra tất cả
> file mà A tham chiếu hoặc được tham chiếu bởi — để tránh lỗi đồng bộ.
>
> **Cách dùng:** Trước khi commit, tra bảng dưới → tìm file đang sửa → kiểm tra cột "Related Files".

---

## Bảng phụ thuộc chính

### Tầng 1: README files (TOC và navigation)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `README.md` (root) | Entry point repo, liệt kê tất cả series (Linux, Cisco, SDN, HAProxy) | `haproxy-onboard/README.md`, `sdn-onboard/README.md`, `linux-onboard/`, `network-onboard/` |
| `haproxy-onboard/README.md` | TOC 29 Parts, Knowledge Dependency Map, Phụ lục A (Version Evolution Tracker — 52 entries, 12 categories) | `README.md` (root — version refs), MỌI file Part `*.md` (tên Part phải khớp TOC), `memory/haproxy-series-state.md` (tên Part phải khớp) |
| `sdn-onboard/README.md` | TOC 20 Parts (17 foundation + 3 advanced), dependency graph, log file metadata | `README.md` (root — SDN section), `sdn-onboard/17.0`, `sdn-onboard/18.0`, `sdn-onboard/19.0` (section titles phải khớp TOC) |

### Tầng 2: Content files (Parts)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `haproxy-onboard/1.0 - haproxy-history-and-architecture.md` | Part 1: history, architecture, process model | `haproxy-onboard/README.md` (TOC entry, dependency graph, Phụ lục A nếu có version-specific content), `README.md` (root — summary) |
| `linux-onboard/file-descriptor-deep-dive.md` | FD deep-dive: TLPI 3-table, epoll, CLOEXEC (1261 lines, 14 figures) | 14 SVGs trong `images/fd-*.svg` (Tầng 5), `README.md` (root — nếu có link) |

> **Template cho Parts mới:** Copy dòng trên và điều chỉnh. Mỗi Part mới phải được thêm vào bảng này.

### Tầng 3: Reference files

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| _(Không còn file riêng — Version Evolution Tracker đã tích hợp vào `haproxy-onboard/README.md` Phụ lục A)_ | — | — |

> **Lưu ý:** `haproxy-onboard/references/haproxy-version-evolution.md` đã được migrate vào Phụ lục A của `haproxy-onboard/README.md` (session 2026-03-30). File gốc cần xóa trên local (`git rm`).

### Tầng 4: Memory và config files

| File | Nội dung chính | Related Files |
|------|---------------|---------------|
| `CLAUDE.md` | Working memory, rules, current state | `memory/session-log.md`, `memory/haproxy-series-state.md`, `memory/experiment-plan.md` |
| `memory/session-log.md` | Log session gần nhất | `CLAUDE.md` (Current State section) |
| `memory/haproxy-series-state.md` | Trạng thái từng Part | `haproxy-onboard/README.md` (TOC) |
| `memory/experiment-plan.md` | Kế hoạch thí nghiệm 5 phases (A→E) | `CLAUDE.md`, `linux-onboard/file-descriptor-deep-dive.md` (exercise inventory) |

### Tầng 2b: SDN onboard series

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/README.md` | **Rev 3 (2026-04-21 session 9, scope tightening):** TOC 13 Block foundation + 3 Block advanced (17/18/19); baseline OVS 2.17.9/OVN 22.03.8/Ubuntu 22.04 + upgrade path OVS 3.3/OVN 24.03/Ubuntu 24.04; Mermaid dependency graph P0-P13 + P17-19 (gap XIV-XVI for numbering stability); 5 reading paths; Phụ lục A Version Evolution Tracker (với Part 9.5 DOCA row); Phụ lục B RFC references; Phụ lục C Bibliography (Goransson + UofSC NSF Award 1829698 + Compass Anthropic + NSDI 2015 + upstream). **Rev 3 scope:** OVS + OpenFlow + OVN standalone, NO OpenStack/Neutron/kolla. | `README.md` (root — SDN section), TẤT CẢ file skeleton Block 0-XIII + 17/18/19 (60 cũ - 9 xóa + 15 thêm ≈ ~66 markdown links cần verify tồn tại), 3 file OVN advanced `17.0/18.0/19.0` (S3 đã rename 2026-04-20; TOC entries Part 17/18/19 đã sync), `plans/sdn-foundation-architecture.md` §3.1/§3.4/§3.5 (TOC/graph/reading paths phải khớp), `.claude/plans/flickering-baking-fern.md` (rev 3 plan file) |
| `sdn-onboard/17.0 - ovn-l2-forwarding-and-fdb-poisoning.md` | OVN L2 Forwarding, FDB Poisoning case study VLAN 3808, multichassis/claim high-level, FDP-620 trigger conditions (1178 lines sau khi trim §17.6 deep-dive sang Part 19 ngày 2026-04-20, production log forensics) | `README.md` (root — SDN section), `sdn-onboard/README.md` (TOC), `sdn-onboard/18.0` nếu 18.0 cross-reference 17.0, `sdn-onboard/19.0` (cross-refs bidirectional: Part 17 §17.6 liên kết tới Part 19 §19.2/19.4/19.5/19.6) |
| `sdn-onboard/18.0 - ovn-arp-responder-and-bum-suppression.md` | OVN ARP Responder, BUM suppression (496 lines, rewritten 2026-04-10) | `sdn-onboard/README.md` (TOC), `sdn-onboard/17.0` (cross-references đến tunnel key, localnet port, MC_FLOOD từ Part 17) |
| `sdn-onboard/19.0 - ovn-multichassis-binding-and-pmtud.md` | OVN multichassis binding lifecycle + Geneve PMTUD bug FDP-620 root cause + RARP activation-strategy + 3 Labs (1379 lines) | `sdn-onboard/README.md` (TOC), `sdn-onboard/17.0` (live migration trigger, localnet, Chassis/Claim baseline), `README.md` (root — SDN section) |

> **Quy tắc:** Khi sửa SDN 17.0, kiểm tra SDN 18.0 có references đến localnet/MC_UNKNOWN không, và SDN 19.0 có cross-ref đến live migration/multichassis của Part 17 không. Khi sửa SDN 18.0, kiểm tra SDN 17.0 có concepts nào được tái sử dụng không. Khi sửa SDN 19.0, kiểm tra consistency với Part 17 section 17.2 (Chassis/Claim) và section 17.6 (live migration trigger).

### Tầng 2c: SDN foundation Block IX — OpenvSwitch internals + operations (rev 3 expansion, P2 2026-04-21)

> **Scope:** Block IX sau rev 3 P2 expansion. **15 file** skeleton (6 cũ + 9 mới absorbing
> Compass Part II chapters). Dependency chain: 9.0 history → 9.1 architecture → 9.2 kernel
> datapath → 9.3 userspace datapath → 9.4 CLI playbook → 9.5 HW offload → 9.6 bonding →
> 9.7 mirror → 9.8 sFlow/NetFlow/IPFIX → 9.9 QoS → 9.10 TLS → 9.11 appctl reference →
> 9.12 upgrade → 9.13 libvirt/docker → 9.14 incident response (Capstone mở rộng).

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/9.0 - ovs-history-2007-present.md` | Skeleton: OVS 2007 Nicira → NSDI 2015 → Linux Foundation 2016, version timeline, so sánh Linux bridge | `plans/sdn-foundation-architecture.md` §3.3 Block IX (sections phải khớp), `sdn-onboard/README.md` TOC (khi rewrite S2) |
| `sdn-onboard/9.1 - ovs-3-component-architecture.md` | Skeleton: ovs-vswitchd + ovsdb-server + openvswitch.ko, netlink genl family upcall | §3.3 Block IX, Part 8.1 (linux-onboard bridge reference), cross-ref tới Part 10 (OVSDB details) |
| `sdn-onboard/9.2 - ovs-kernel-datapath-megaflow.md` | Skeleton: microflow → megaflow → ukeys, handler/revalidator threads, NSDI 2015 numbers | §3.3 Block IX, 9.1 (prerequisite), cross-ref Part 13 (OVN sử dụng megaflow installation path) |
| `sdn-onboard/9.3 - ovs-userspace-dpdk-afxdp.md` | Skeleton: DPDK PMD + hugepages + NUMA, AF_XDP alternative, trade-off matrix | §3.3 Block IX, 9.2 (prerequisite), **9.5 (complement: DPDK vs DOCA so sánh)** |
| `sdn-onboard/9.4 - ovs-cli-tools-playbook.md` | Skeleton: ovs-vsctl/ofctl/appctl/dpctl, 6-layer troubleshooting playbook, Capstone Block IX Lab 2 | §3.3 Block IX, 9.3 (prerequisite), 9.5 (CLI là tool verify DOCA offload counters) |
| `sdn-onboard/9.5 - hw-offload-switchdev-asap2-doca.md` | Skeleton mới 2026-04-20: switchdev, ASAP² eSwitch, 3 DPIFs comparison, OVS-DOCA internals, vDPA, BlueField DPU, megaflow scaling 200k-2M | §3.3 Block IX (entry 9.5 mới), 9.3 (trade-off bridge → DOCA), 9.4 (CLI cho `ovs-appctl coverage/show` read DOCA counters), Part 8.1 (Linux bridge/veth tiên quyết) |
| `sdn-onboard/9.6 - bonding-and-lacp.md` | Skeleton 5 section (P2 rev 3): 3 bond mode (active-backup/balance-slb/balance-tcp) + LACP active/passive/off + fast-timer + fallback-ab + bond/show + lacp/show letter salad ACEGIKNP | 9.1 prerequisite, Part 8.2 (Linux VLAN bonding), Compass Ch E |
| `sdn-onboard/9.7 - port-mirroring-and-packet-capture.md` | Skeleton 5 section: Mirror table OVSDB schema + canonical `--id=@` atomic idiom + local SPAN (output_port) + RSPAN (output_vlan) + cleanup auto-GC | 9.1 prerequisite, 9.6 OVSDB idiom, Compass Ch G |
| `sdn-onboard/9.8 - flow-monitoring-sflow-netflow-ipfix.md` | Skeleton 6 section: sFlow (RFC 3176 sampling) + NetFlow v5/v9 (RFC 3954) + IPFIX (RFC 7011 template negotiation) + atomic idiom cho cả 3 + collector stack (goflow2/nfdump/ntopng) | 9.1, 9.7, Compass Ch H |
| `sdn-onboard/9.9 - qos-policing-shaping-metering.md` | Skeleton 5 section: OVS configure via tc/rte_sched + ingress policing + egress shaping linux-htb recipe verbatim + OF 1.3+ meter-based policing + CIR/PIR 2-color marking + explicit destroy QoS/Queue (no auto-GC) | 9.1, Part 8.3 (tc/qdisc), Part 4.2 (OF 1.3 meters), Compass Ch I + UofSC Lab 9 |
| `sdn-onboard/9.10 - tls-pki-hardening.md` | Skeleton 5 section: ptcp vs ssl (production chỉ ssl) + ovs-pki workflow (init + req+sign switch/controller) + openssl s_client verification + CA rotation add-then-switch + cipher suite restriction | 9.1, Part 10.0 (Manager/Controller URIs), Compass Ch K |
| `sdn-onboard/9.11 - ovs-appctl-reference-playbook.md` | Skeleton 8 section (reference playbook): Unix-socket RPC architecture + vlog control + coverage/show + memory/show + ofproto/trace + dpctl/dpif/upcall introspection + DPDK PMD telemetry + tunnel neighbor tables | 9.4 prerequisite (6-layer playbook), Compass Ch L + R |
| `sdn-onboard/9.12 - upgrade-and-rolling-restart.md` | Skeleton 5 section: 3 golden rules (schema trước binary, 1 daemon một lúc, không kernel+OVS đồng thời) + 5-step choreography + --bundle atomic + failure mode schema convert + in-place vs cordon-and-replace | 9.1, 10.0 (OVSDB schema), Compass Ch P + 19 |
| `sdn-onboard/9.13 - libvirt-docker-integration.md` | Skeleton 6 section: libvirt virtualport=openvswitch + external_ids:iface-id contract + libvirt troubleshoot + ovs-docker helper + manual veth attach production-grade + CNI plugin pattern (OVN-Kubernetes context) | 9.1, Part 8.1, Compass Ch S + T compressed |
| `sdn-onboard/9.14 - incident-response-decision-tree.md` | Skeleton 7 section (Capstone mở rộng): 4-layer mental model (OVSDB/OpenFlow/datapath/wire) + 5-branch decision tree (packet loss/drops/tunnel/bond/OVSDB) + Appendix C compressed reconciliation | 9.4, 9.6, 9.11, Part 13.6 (HA Chassis Group), Compass Ch 20 + Appendix C |

> **Capstone positioning Block IX (rev 3):**
> - Baseline Capstone (accessible mọi user): 9.4 CLI playbook Lab 2 — giữ nguyên.
> - Hardware-specific mở rộng: 9.5 DOCA/switchdev (cần ConnectX-5+/BlueField).
> - Advanced operational: **9.14 Incident Response Capstone** (drill 5 scenario với 4-layer reconciliation) — mới thêm rev 3. Không yêu cầu hardware đặc biệt, chỉ cần 2-node lab thông thường.
> - Depth gradient: 9.9 QoS (UofSC Lab 9 deep absorb) + 9.12 Upgrade choreography (production drill) đều có Guided Exercise riêng trong Phase B.

### Tầng 2d: SDN foundation Block 0 (content written — S4 hoàn tất 2026-04-20)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/0.0 - how-to-read-this-series.md` | Meta orientation: định vị series trong bộ onboard, 4 reading paths (linear/OVS-only/OVN-focused/incident-responder), convention markers (Key Topic, Guided Exercise, Lab, Trouble Ticket, version annotation), mapping CCNA/RHCSA/CKA (148 dòng) | `sdn-onboard/README.md` (TOC), `sdn-onboard/0.1` (tham chiếu lab mode A/B/C) |
| `sdn-onboard/0.1 - lab-environment-setup.md` | Lab setup: 3 mode (single-node / two-node chassis pair / multi-node kolla), Ubuntu 22.04 baseline (kernel 5.15, OVS 2.17.9, OVN 22.03.8 jammy-updates), Mininet 2.3.0 từ source, kolla-ansible version matrix (16.x=Antelope → 20.x=Epoxy verified từ releases.openstack.org), health check playbook, teardown/reset, Guided Exercise 1 (426 dòng) | `sdn-onboard/README.md` (baseline OVS/OVN/Ubuntu phải khớp), `plans/sdn-foundation-architecture.md` §3.3 Block 0 |

> **Quy tắc version sync:** Khi sửa baseline OVS/OVN/Ubuntu version trong `sdn-onboard/README.md`,
> PHẢI cập nhật song song `0.1` mục 0.1.2 và 0.1.3 (package version block + version annotation).
> Ngược lại khi phát hiện version mismatch ở `0.1`, kiểm tra `README.md` Phụ lục A Version
> Evolution Tracker có khớp không.

### Tầng 2f: SDN foundation Block I (content written — S5.1 bắt đầu 2026-04-21)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/1.0 - networking-industry-before-sdn.md` | Block I Part 1.0: mô hình control/data/management hợp nhất vendor-proprietary (1984-2008); vendor lock-in 3 layer; East-West traffic explosion (Jupiter SIGCOMM 2015, Facebook Fabric 2014, Roy SIGCOMM 2015); 3 giới hạn kỹ thuật (STP 40-50% block, VLAN 4096, chassis oversubscription 8.7:1 Cat 6513); 3 giới hạn vận hành (CLI/expect, config drift, change velocity); Guided Exercise 1 POE (174 CLI commands, 20-switch VLAN 100); 10 refs (Ethane, RFC 7348/5556, IEEE 802.1Q/802.1D, Jupiter, Roy, FB Fabric, EC2 launch, Cat 6500) (198 dòng) | `sdn-onboard/README.md` (TOC Block I), `plans/sdn-foundation-architecture.md` §3.3 Block I, `sdn-onboard/1.1` (forward ref: DC pain points phát triển từ 3 giới hạn kỹ thuật), `sdn-onboard/1.2` (forward ref: 5 drivers vì sao SDN) |

> **Quy tắc dependency Block I:** Khi sửa `1.0`, PHẢI kiểm tra forward references trong `1.1`
> và `1.2` (khi viết): historical claims (năm Ethane, IEEE, kolla-ansible versions) phải consistent.
> Ngược lại khi viết `1.1`/`1.2`, không được nhắc lại nội dung `1.0` (Rule non-repetition) —
> chỉ reference section number (ví dụ: "như 1.0.4 đã trình bày").

### Tầng 2g: SDN foundation Block II (skeleton refined — S6a hoàn tất 2026-04-21)

> **Scope:** Block II sau S6a refinement (Rule 10 architecture phase). 5 file skeleton, mỗi file
> 30-80 dòng với title + summary 1-3 câu cho mỗi section. Dependency chain tuyến tính:
> 2.0 → 2.1 → 2.2 → 2.3 → 2.4 (2.4 phụ thuộc 2.3 cho 4D Project lineage vào Ethane).

| File | Nội dung chính (skeleton) | Related Files — PHẢI kiểm tra khi sửa |
|------|--------------------------|---------------------------------------|
| `sdn-onboard/2.0 - dcan-open-signaling-gsmp.md` | Skeleton 5 section: DCAN (Cambridge 1995) / OPENSIG (Aurel Lazar Columbia) / GSMP RFC 3292 (06/2002 từ Ipsilon) / GSMP message structure vs OF 1.0 12-tuple / di sản switch controlled by external entity | `sdn-onboard/README.md` (TOC Block II), `plans/sdn-foundation-architecture.md` §3.3 Block II Phase A, `sdn-onboard/2.1` (GSMP biến thể Ipsilon), `sdn-onboard/1.2` (forward ref từ Part 1) |
| `sdn-onboard/2.1 - ipsilon-and-active-networking.md` | Skeleton 6 section: Ipsilon IP Switching (Peter Newman 1996, RFC 1953/1987) / Ipsilon → MPLS lineage / DARPA Active Networking 1996-2001 / capsules vs programmable switches / tại sao AN không commercialize / di sản đến P4 | `sdn-onboard/README.md` TOC, §3.3 Block II, `sdn-onboard/2.0` (GSMP prerequisite), Block VI Part 6.x P4 (forward ref) |
| `sdn-onboard/2.2 - nac-orchestration-virtualization.md` | Skeleton 4 section: NAC (RADIUS RFC 2865 + COPS RFC 2748 + 802.1X) / HP OpenView/IBM Tivoli orchestration / VMware vDS 2009 + XenServer OVS 2009 / di sản modular plugin architecture (rev 3 — scrubbed Neutron ML2 forward ref) | `sdn-onboard/README.md` TOC, §3.3 Block II, `sdn-onboard/2.0` (prerequisite controller motif), `sdn-onboard/4.1` + Block XIII 13.5 (forward ref modular match/plugin abstractions) |
| `sdn-onboard/2.3 - forces-and-4d-project.md` | Skeleton 6 section: ForCES WG (RFC 3654/3746/5810) / ForCES CE/FE vs OpenFlow split / tại sao ForCES không commercialize / 4D Project authors (Rexford/Greenberg/Hjalmtýsson/Maltz/Myers/Zhang) / 4 planes Decision/Dissemination/Discovery/Data / di sản 4D → Ethane | `sdn-onboard/README.md` TOC, §3.3 Block II, `sdn-onboard/2.0` (prerequisite), `sdn-onboard/2.4` (4D → Ethane lineage) |
| `sdn-onboard/2.4 - ethane-the-direct-ancestor.md` | Skeleton 5 section: Ethane SIGCOMM 2007 authors (Casado/Freedman/Pettit/Luo/McKeown/Shenker) / architecture centralized policy + flow-based forwarding / NOX controller (CCR 07/2008) / Casado PhD thesis 2007 + Nicira founding / Ethane → OpenFlow 1.0 (CCR 04/2008 + spec 31/12/2009) + Capstone Block II Lab | `sdn-onboard/README.md` TOC, §3.3 Block II, `sdn-onboard/2.3` (prerequisite 4D), Block IV OpenFlow (forward ref), Block XIV Commercial SDN (Nicira NVP → NSX) |

> **Quy tắc dependency Block II (Phase A):** Các claim lịch sử (năm paper, tên tác giả, số RFC)
> phải consistent xuyên 5 file. Khi Phase B viết content, PHẢI fact-check mọi entry trong reference
> placeholder (RFC 3292/1953/1987/2865/2748/3654/3746/5810/3031, SIGCOMM 2007/2008, CCR 1996/1999/2005/2008).
> Rule non-repetition: 2.0 đặt nền GSMP → 2.1 chỉ nhắc GSMP variant Ipsilon, không giải lại message format.

### Tầng 2h: SDN foundation Block III (skeleton refined — S7a hoàn tất 2026-04-21)

> **Scope:** Block III "Khai sinh OpenFlow" sau S7a refinement (Rule 10 architecture phase). 3 file skeleton,
> mỗi file 40-60 dòng với title + summary 1-3 câu cho mỗi section. Dependency chain tuyến tính:
> 3.0 → 3.1 → 3.2 (3.2 phụ thuộc 3.1 cho spec ownership transition Stanford → ONF).

| File | Nội dung chính (skeleton) | Related Files — PHẢI kiểm tra khi sửa |
|------|--------------------------|---------------------------------------|
| `sdn-onboard/3.0 - stanford-clean-slate-program.md` | Skeleton 5 section: Clean Slate funded 2006-2012 (NSF FIND + DARPA + industry consortium) / key researchers (McKeown/Shenker/Casado/Parulkar) / Stanford Gates Building deployment 2008-2009 (8-10 HP ProCurve 5400 + NOX) / CCR 04/2008 foundational paper 7 authors / Nicira founding 08/2007 → VMware acquisition 07/2012 $1.26B | `sdn-onboard/README.md` (TOC Block III), `plans/sdn-foundation-architecture.md` §3.3 Block III Phase A, `sdn-onboard/2.4` (prerequisite: Casado PhD thesis + Ethane lineage), `sdn-onboard/3.1` (forward ref: Stanford shepherd spec 1.0 trước ONF), Block XIV Commercial SDN (forward ref NVP → NSX) |
| `sdn-onboard/3.1 - openflow-1.0-specification.md` | Skeleton 7 section: spec 1.0.0 (31/12/2009, 42 trang, Stanford shepherd) / TCP 6633 plain + TCP 6653 TLS (IANA 09/2013) / message types 3 nhóm (symmetric/controller-to-switch/async) / 12-tuple match fields (ofp_match §A.2.3) / 8 actions (§A.2.6) / flow entry anatomy (match+priority+counters+timeouts+cookie+actions) / single-table cross-product explosion + OVS resubmit NXM workaround | `sdn-onboard/README.md` TOC, §3.3 Block III, `sdn-onboard/3.0` (prerequisite: Stanford history + CCR 04/2008), `sdn-onboard/3.2` (forward ref: ONF take over spec 1.1+), `sdn-onboard/2.0` (cross-ref GSMP 12-tuple mapping §2.0.4), Part 4.x OpenFlow evolution (forward ref multi-table 1.1, group table 1.3) |
| `sdn-onboard/3.2 - onf-formation-and-governance.md` | Skeleton 6 section + Capstone Lab: ONF press release 21/03/2011 / 6 founding operators (Deutsche Telekom/Facebook/Google/Microsoft/Verizon/Yahoo) + 17 early adopters (Cisco/Juniper/HP/NEC/VMware...) / working groups (Config/FAWG/NBI/Optical/Security/Testing) / Stanford → ONF spec ownership transition / ONF vs IETF/IEEE/OCP 4-dimension comparison / 2018 merger với ON.Lab → ONOS+CORD+SD-RAN + OpenFlow 1.5.1 last revision (03/2015) | `sdn-onboard/README.md` TOC, §3.3 Block III, `sdn-onboard/3.1` (prerequisite: spec 1.0 transition), Block IV OpenFlow evolution (forward ref: ONF shepherd 1.1 → 1.5.1), Block XIV Commercial SDN (forward ref: ONOS governance history) |

> **Quy tắc dependency Block III (Phase A):** Claim lịch sử phải consistent — đặc biệt các timestamp
> quan trọng: OpenFlow 1.0 spec (31/12/2009), CCR paper (04/2008), ONF formation (21/03/2011),
> IANA TCP 6653 assignment (09/2013), ONF-ON.Lab merger (10/2018), OpenFlow 1.5.1 (03/2015).
> Khi Phase B viết content, PHẢI fact-check cross-source: ACM CCR 38(2), ONF bylaws
> (opennetworking.org/legal), Stanford Clean Slate archive (cloud.stanford.edu/cleanslate),
> VMware-Nicira press release 07/2012. Rule non-repetition: 3.0 đặt nền Stanford +
> Nicira lineage → 3.1 không lặp lại Stanford history, chỉ nhắc "Stanford shepherd spec 1.0";
> 3.2 không lặp lại Ethane → OF transition (đã ở 2.4.5), chỉ tập trung governance process.

### Tầng 2j: SDN foundation Block XIII expansion (P1 rev 3 — 2026-04-21)

> **Scope:** Block XIII mở rộng từ 4 → 7 file sau khi absorb concept OVN-native từ Block XIV (đã bị xóa ở P0).
> 3 file mới: 13.4 br-int architecture, 13.5 Port_Binding types upstream taxonomy, 13.6 HA_Chassis_Group + BFD.
> Dependency chain: 13.0 → 13.1 → 13.2 → 13.3 → 13.4 → 13.5 → 13.6.

| File | Nội dung chính (skeleton) | Related Files — PHẢI kiểm tra khi sửa |
|------|--------------------------|---------------------------------------|
| `sdn-onboard/13.4 - br-int-architecture-and-patch-ports.md` | Skeleton 6 section: br-int role + ownership ovn-controller + external bridge pattern (br-ex/br-provider qua ovn-bridge-mappings) + patch port zero-copy cross-bridge + DPDK patch port caveat + cross-ref Block IX/XI. | `sdn-onboard/README.md` TOC Block XIII, `plans/sdn-foundation-architecture.md` §3.3 Block XIII, `sdn-onboard/9.1` (OVS 3-component prerequisite), `sdn-onboard/9.4` (CLI baseline), `sdn-onboard/13.5` (localnet triggers patch port), `sdn-onboard/13.3` prerequisite |
| `sdn-onboard/13.5 - port-binding-types-ovn-native.md` | Skeleton 9 section: Port_Binding SBDB schema + 8 types (vif/localnet/l2gateway/l3gateway/chassisredirect/patch/localport/virtual) + diagnosis workflow `ovn-sbctl list Port_Binding`. **KHÔNG dùng Neutron terminology (Nova/libvirt/iface-id từ orchestrator được mô tả neutral).** | `sdn-onboard/README.md` TOC, §3.3 Block XIII, `sdn-onboard/13.1` prerequisite (NBDB/SBDB architecture), `sdn-onboard/13.4` (br-int + patch port auto-creation), `sdn-onboard/13.6` (chassisredirect lifecycle) |
| `sdn-onboard/13.6 - ha-chassis-group-and-bfd.md` | Skeleton 6 section: HA_Chassis_Group NBDB schema + HA_Chassis priority + BFD session RFC 5880 + failover 3-5s sequence + tuning sub-second + relation với Part 19 live migration | `sdn-onboard/README.md` TOC, §3.3 Block XIII, `sdn-onboard/13.5` prerequisite (chassisredirect Port_Binding), `sdn-onboard/19.0` (live migration case study uses HA_Chassis_Group), `sdn-onboard/11.1` (MTU/PMTUD liên quan multichassis) |

> **Quy tắc dependency Block XIII expansion:** Ba file mới 13.4/13.5/13.6 absorb concept OVN-native từ Block XIV (đã xóa). KHÔNG được dùng OpenStack/Neutron/kolla/Nova/libvirt terminology — tất cả concept phải portable với bất kỳ orchestrator (OVN standalone, OVN-Kubernetes, bare-metal). Forward reference tới Part 19 (live migration case study) phải chính xác — Part 19 là production forensic content đã fact-checked.

### Tầng 2k: SDN foundation P3 additions (4.7 + 10.2 + 11.3 + 11.4) — rev 3 2026-04-21

> **Scope:** Phase P3 thêm 4 file skeleton cross-Block: 4.7 OF programming (Block IV),
> 10.2 OVSDB ops (Block X), 11.3 GRE lab + 11.4 IPsec lab (Block XI). Mỗi file absorb
> từ source: UofSC Lab 4/5/6/8 + Compass Ch 5-10 cho 4.7; Compass Ch M+O cho 10.2;
> UofSC Lab 14 cho 11.3; UofSC Lab 15 cho 11.4.

| File | Nội dung chính (skeleton) | Related Files |
|------|--------------------------|---------------|
| `sdn-onboard/4.7 - openflow-programming-with-ovs.md` | Skeleton 8 section (132 dòng — reference playbook): flow grammar + -O flag / 12-tuple match + NXM/OXM extensions / 8+ actions / multi-table 3-stage L3 routing recipe (UofSC Lab 6 verbatim) / conntrack 5-flow stateful firewall recipe (Compass Ch 9 + UofSC Lab 8) / groups + meters / flow hygiene monitor/replace-flows/diff-flows / 5-table MAC learning advanced tutorial placeholder. | Block IV 4.0-4.6 prerequisite, Part 9.1 (OVS architecture), Part 9.9 (QoS meter), 9.11 (ofproto/trace), Part 13.x (OVN uses OF under-the-hood) |
| `sdn-onboard/10.2 - ovsdb-backup-restore-compact-rbac.md` | Skeleton 7 section (95 dòng): append-only log + compact rationale / offline ovsdb-tool compact vs live ovsdb-server/compact / backup+restore workflow / schema conversion needs-conversion/convert / transaction log inspection show-log + db-cksum / RBAC Manager.role / cluster fresh member after leave | Part 10.0 (OVSDB schema), Part 10.1 (Raft), Part 9.12 (upgrade choreography), Compass Ch M + O |
| `sdn-onboard/11.3 - gre-tunnel-lab.md` | Skeleton 7 section (119 dòng — hands-on lab): GRE header RFC 2784 + vì sao còn relevant / OVS gre port config / UofSC Lab 14 topology 3 ISP router + 2 Docker-nested Mininet container / OSPF FRR/Quagga config / GRE tunnel giữa 2 site / Wireshark inspection outer + inner / MTU math pitfall | Part 11.0 (VXLAN/Geneve), Part 8.0 (netns), Part 4.7 (OF rules), UofSC Lab 14 |
| `sdn-onboard/11.4 - ipsec-tunnel-lab.md` | Skeleton 7 section (108 dòng — hands-on lab): IPsec AH vs ESP, tunnel vs transport mode / IKE Phase 1 ISAKMP SA + DH + identity auth / IKE Phase 2 Child SA cho ESP / OVS option psk auto-program strongSwan / strongSwan daemon + ovs-monitor-ipsec / IPsec-over-GRE topology / PSK rotation procedure | Part 11.3 (GRE prerequisite), Part 9.10 (TLS/PKI cross-ref), UofSC Lab 15 |

> **Skeleton length note:** 4 file rev 3 P3 (95-132 dòng) vượt Rule 10 soft target 30-60 dòng
> do bản chất reference playbook — cần liệt kê đầy đủ match fields, actions, recipes verbatim.
> Content vẫn là section headers + 1-3 câu summary + code block placeholder, không paragraph
> giải thích dài, không fact-check deep. Phase B sẽ expand lên 600-1200 dòng/file.

### Tầng 2i: SDN foundation Block IV (skeleton refined — S8a hoàn tất 2026-04-21)

> **Scope:** Block IV "OpenFlow evolution" sau S8a refinement (Rule 10 architecture phase). 7 file skeleton,
> mỗi file 40-70 dòng với title + summary 1-3 câu cho mỗi section. Dependency chain tuyến tính:
> 4.0 (OF 1.1) → 4.1 (OF 1.2) → 4.2 (OF 1.3 LTS) → 4.3 (OF 1.4) → 4.4 (OF 1.5) → 4.5 (TTP) → 4.6
> (limitations + Capstone Lab). 4.6 tổng kết và kết nối sang Block V (API-based SDN) + Block VI (P4).

| File | Nội dung chính (skeleton) | Related Files — PHẢI kiểm tra khi sửa |
|------|--------------------------|---------------------------------------|
| `sdn-onboard/4.0 - openflow-1.1-multi-table-groups.md` | Skeleton 6 section: OF 1.1 release 28/02/2011 (pre-ONF, Stanford shepherd) / multi-table pipeline semantics + GOTO_TABLE / instructions vs actions distinction / 4 group types (ALL/SELECT/INDIRECT/FAST_FAILOVER sub-10ms reroute) / MPLS native (PUSH/POP/SET_TTL) / use case multi-tenant classifier → tunnel giảm O(N·M) → O(N+M) | `sdn-onboard/README.md` (TOC Block IV), `plans/sdn-foundation-architecture.md` §3.3 Block IV Phase A, `sdn-onboard/3.1` (prerequisite: single-table cross-product explosion §3.1.7), `sdn-onboard/4.1` (forward ref: OXM identify field) |
| `sdn-onboard/4.1 - openflow-1.2-oxm-tlv-match.md` | Skeleton 5 section: OF 1.2 release 05/12/2011 (spec đầu tiên do ONF công bố) / OXM TLV format (class+field+HM+length, origin NXM) / IPv6 match fields / controller roles EQUAL/MASTER/SLAVE + generation_id / migration 1.0→1.2 không backward compat wire | `sdn-onboard/README.md` TOC, §3.3 Block IV, `sdn-onboard/4.0` (prerequisite), `sdn-onboard/4.2` (forward ref IPv6 extension header), Block VII (forward ref controllers) |
| `sdn-onboard/4.2 - openflow-1.3-meters-pbb-ipv6.md` | Skeleton 6 section: OF 1.3 release timeline 1.3.0-1.3.5 (2012-2015, errata chain backward compat) / meter table per-flow QoS (DROP/DSCP_REMARK bands + token bucket) / per-connection auxiliary channels / PBB 802.1ah match (PBB_ISID 24-bit) / IPv6 extension headers bitmask / tại sao 1.3 = LTS (OVS 2.0+, Ryu/ODL baseline, Pica8/HP/NEC commit silicon) | `sdn-onboard/README.md` TOC, §3.3 Block IV, `sdn-onboard/4.1` (prerequisite OXM), `sdn-onboard/4.3` (forward ref 1.4 adoption mismatch), Block XVI (forward ref WAN QoS) |
| `sdn-onboard/4.3 - openflow-1.4-bundles-eviction.md` | Skeleton 5 section: OF 1.4 release 14/10/2013 / bundles atomic transaction (OPEN/CLOSE/COMMIT/DISCARD + ATOMIC/ORDERED flags, analogy SQL) / flow entry eviction với importance field vs timeout / optical port extensions (ITU-T G.694.1 wavelength grid) / adoption reality OVS 2.5 partial + vendor skip | `sdn-onboard/README.md` TOC, §3.3 Block IV, `sdn-onboard/4.2` (prerequisite 1.3), `sdn-onboard/4.4` (continuity 1.5 adoption narrative), `sdn-onboard/16.1` (forward ref optical SDN) |
| `sdn-onboard/4.4 - openflow-1.5-egress-l4l7.md` | Skeleton 5 section: OF 1.5 release 1.5.0 (19/12/2014) + 1.5.1 (26/03/2015) cuối cùng / egress tables per-output-port processing / TCP flags matching (URG/ACK/PSH/RST/SYN/FIN) / packet type aware (OXM PACKET_TYPE) / current state 2026 OVS 2.10+ partial, vendor zero, Tofino/P4 thay chỗ | `sdn-onboard/README.md` TOC, §3.3 Block IV, `sdn-onboard/4.3` (prerequisite 1.4), `sdn-onboard/4.6` (forward ref lesson learned), Block VI Part 6.0 (forward ref P4) |
| `sdn-onboard/4.5 - ttp-table-type-patterns.md` | Skeleton 4 section: vấn đề silicon subset OF spec (Broadcom Trident2, Intel FM6000) / TTP pre-agreed pattern analogy HTTP Accept / ONF TS-017 spec (15/08/2014, YANG-based) / alternative Flow Objectives của ONOS (forward ref Block VI) | `sdn-onboard/README.md` TOC, §3.3 Block IV, `sdn-onboard/4.4` (prerequisite), `sdn-onboard/6.1` (forward ref Flow Objectives abstraction) |
| `sdn-onboard/4.6 - openflow-limitations-lessons.md` | Skeleton 7 section + Capstone Block IV Lab POE: 5 limitations (flow-table explosion Broadcom Trident2 4K ACL / controller latency 1-5ms DevoFlow SIGCOMM 2011 / distribution scale Atomix Raft / silicon mismatch TCAM vs SRAM ingress vs egress / L4-L7 gap HTTP/SSL/DPI) / Google B4 SIGCOMM 2013 fork / lesson → P4 + API-based SDN — Capstone: multi-table pipeline + FAST_FAILOVER sub-10ms reroute POE verification | `sdn-onboard/README.md` TOC, §3.3 Block IV, TẤT CẢ 4.0-4.5 (tổng kết), `sdn-onboard/5.0` (forward ref API SDN), `sdn-onboard/6.0` (forward ref P4), `sdn-onboard/9.2` (cross-ref OVS megaflow), `sdn-onboard/10.1` (cross-ref OVSDB Raft), Block VIII/XVI (forward ref Linux L7/SDN WAN) |

> **Quy tắc dependency Block IV (Phase A):** Các timestamp và số version phải consistent xuyên 7 file.
> Khi Phase B viết content, PHẢI fact-check mọi release date: 1.1.0 (28/02/2011), 1.2 (05/12/2011),
> 1.3.0 (25/04/2012) → 1.3.5 (26/03/2015), 1.4 (14/10/2013), 1.5.0 (19/12/2014) → 1.5.1 (26/03/2015),
> ONF TS-017 (15/08/2014). Rule non-repetition: 4.0 đặt nền multi-table + group → các Part sau chỉ
> nhắc additions/changes, không giải lại pipeline semantic; 4.6 là tổng kết — không lặp lại chi tiết
> 4.0-4.5, chỉ extract limitations theo chiều ngang. Fact-check cross-source: SIGCOMM 2011 (DevoFlow),
> SIGCOMM 2013 (B4), NSDI 2015 (OVS), CCR 2014 (P4), Broadcom Trident2 architecture brief.

### Tầng 2e: SDN foundation skeletons rev 2 (các Block khác — placeholder)

> Khi bắt đầu S5-S19 cho một Block mới, di chuyển skeleton entries sang Tầng 2c/2d/2f/2g/2h/2i-tương đương
> và liệt kê cross-ref. Hiện tại track Block IX (đã thay đổi 5→6 file), Block 0 (S4 đã viết content),
> Block I (S5.1 Part 1.0 content, 1.1/1.2 skeleton refined), Block II (S6a skeleton refined 2026-04-21),
> Block III (S7a skeleton refined 2026-04-21), Block IV (S8a skeleton refined 2026-04-21).

**Conflict numbering — đã giải quyết (S3 hoàn tất 2026-04-20):**

```
sdn-onboard/1.0 - networking-industry-before-sdn.md        ← skeleton rev 2 Block I (giữ nguyên)
sdn-onboard/17.0 - ovn-l2-forwarding-and-fdb-poisoning.md  ← OVN advanced (renamed từ 1.0)

sdn-onboard/2.0 - dcan-open-signaling-gsmp.md              ← skeleton rev 2 Block II (giữ nguyên)
sdn-onboard/18.0 - ovn-arp-responder-and-bum-suppression.md ← OVN advanced (renamed từ 2.0)

sdn-onboard/3.0 - stanford-clean-slate-program.md          ← skeleton rev 2 Block III (giữ nguyên)
sdn-onboard/19.0 - ovn-multichassis-binding-and-pmtud.md   ← OVN advanced (renamed từ 3.0)
```

S3 đã thực thi ngày 2026-04-20: `git mv` 3 file OVN sang 17.0/18.0/19.0, renumber internal
headings (Phần 1/2/3 → Phần 17/18/19; mục X.Y → tương ứng), update cross-references giữa
3 file. Legacy artifact `1.0 - sdn-history-and-openflow-protocol.md` đã được đánh dấu để
`git rm` trên local (sandbox không delete được do fuse lock). Không còn conflict tên —
skeleton Block I/II/III (1.0/2.0/3.0) và advanced Part (17.0/18.0/19.0) ở hai dải số tách biệt.

### Tầng 2l: SDN foundation Block XX — Operational Excellence (Part 20, 3 file)

> **Scope:** Block XX Operational Excellence, cover kỹ năng vận hành chẩn đoán thực chiến. Dependency chain: Part 20.0 (systematic debugging philosophy + 5-layer) → Part 20.1 (security hardening + port_security/ACL/audit) → Part 20.2 (OVN troubleshooting deep-dive với ovn-trace/ovn-detrace/Port_Binding forensic).

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/20.0 - ovs-ovn-systematic-debugging.md` | Content 788 dòng (với §20.7 3-case-study playback Phase G.1.4): isolation-first philosophy + 5-layer model + 8 common scenarios + 3 production case study (VM no network race / upgrade schema drift / partition thundering herd) | `sdn-onboard/README.md` TOC Block XX, `sdn-onboard/9.14` (incident decision tree OVS-specific, đối xứng), `sdn-onboard/9.25` (`ofproto/trace` grammar), `sdn-onboard/0.2` (packet journey anchor), `sdn-onboard/13.7` (ovn-controller internals) |
| `sdn-onboard/20.1 - ovs-ovn-security-hardening.md` | Content 475 dòng: 3-layer defense-in-depth (control/management/data plane) + port_security + ACL default-deny + audit logging + 10-point checklist | `sdn-onboard/README.md` TOC Block XX, `sdn-onboard/13.3` (ACL foundation), `sdn-onboard/9.10` (TLS hardening), `sdn-onboard/18.0` (ARP poisoning threat model) |
| `sdn-onboard/20.2 - ovn-troubleshooting-deep-dive.md` | Content 1627 dòng (Session S51 Phase G.3.1): 3-layer OVN debug + `ovn-trace` 11 option 9 subsection + `ovn-detrace` chain + Port_Binding 8 type × 22 failure mode + ovn-appctl 21 command (7 Anatomy) + MAC_Binding/FDB/Service_Monitor triage + 16-symptom matrix + 3 GE + Capstone POE | `sdn-onboard/README.md` TOC Block XX, `sdn-onboard/13.1` (NBDB/SBDB schema prerequisite), `sdn-onboard/13.2` (LS pipeline 27+10 stage), `sdn-onboard/13.5` (Port_Binding 8 type taxonomy — 20.2 đi sâu forensic angle), `sdn-onboard/13.7` (ovn-controller main_loop + I-P engine — 20.2 reference cho inc-engine stats interpretation), `sdn-onboard/13.8` (ovn-northd compile NB→SB — 20.2 reference cho northd status/pause/resume), `sdn-onboard/13.11` (LR pipeline 19+7 stage), `sdn-onboard/9.25` (`ofproto/trace` grammar — 20.2 reference cho chain với ovn-detrace), `sdn-onboard/9.27` (3-tier parallel diagnostic — 20.2 complement OVN-specific angle), `sdn-onboard/20.0` (systematic debugging framework — 20.2 deep-dive cho OVN tool) |
| `sdn-onboard/20.3 - ovn-daily-operator-playbook.md` | Content 1554 dòng (Session S53 Phase G.5.1): 10 task category daily workflow (health/inventory/port-lifecycle/ACL/LB+NAT/DHCP+DNS/gateway/conntrack/performance/backup) + 2 end-to-end workflow script (new-tenant/tenant-teardown) + 3 GE + Capstone POE (refute "500 ACL raw" với Port_Group consolidation) + Anatomy Template A cho 10+ command output | `sdn-onboard/README.md` TOC Block XX, `sdn-onboard/13.1` (NBDB/SBDB schema — 20.3 reference `get NB_Global nb_cfg`), `sdn-onboard/13.2` (LS/LR concept — 20.3 apply), `sdn-onboard/13.3` (ACL/LB/NAT/Port_Group concept — 20.3 scale practice), `sdn-onboard/13.5` (Port_Binding type — 20.3 chassis bind workflow), `sdn-onboard/13.6` (HA_Chassis+BFD — 20.3 gateway failover), `sdn-onboard/13.7` + `sdn-onboard/13.8` (ovn-controller + ovn-northd health monitoring), `sdn-onboard/13.10` (DHCP/DNS concept — 20.3 operational CRUD), `sdn-onboard/13.11` (LR gateway — 20.3 LRP external creation), `sdn-onboard/13.12` (IPAM — 20.3 dynamic/static address), `sdn-onboard/20.0` (systematic debugging — 20.3 complement với daily routine), `sdn-onboard/20.1` (security hardening — 20.3 reference port_security workflow), `sdn-onboard/20.2` (troubleshooting tools — 20.3 reference ovn-trace dry-run + inc-engine/stopwatch metrics), `sdn-onboard/9.26` (forensic case study — 20.3 reference prevention pattern) |
| `sdn-onboard/20.4 - ovs-daily-operator-playbook.md` | Content 1422 dòng (Session S55 Phase G.5.2, sister cho 20.3 nhưng OVS pure-datapath): 10 task category daily OVS workflow (health/inventory/bridge-port/flow/tunnel/QoS+mirror/conntrack/performance/OVSDB/backup) + 2 workflow end-to-end (new-bridge.sh + bridge-decommission.sh) + 3 GE + Capstone POE (refute "DPDK migrate live" với parallel-bridge option) + Anatomy Template A cho 8 command output + phân biệt 4 CLI layer (vsctl/ofctl/dpctl/appctl) | `sdn-onboard/README.md` TOC Block XX, `sdn-onboard/9.1` (OVS 3-component arch prerequisite), `sdn-onboard/9.2` (kernel DP + megaflow — 20.4 reference dpctl show lookups/masks), `sdn-onboard/9.3` (DPDK userspace — 20.4 reference pmd-stats-show + datapath_type=netdev), `sdn-onboard/9.4` (CLI 6-layer playbook — 20.4 consolidate scenario-driven), `sdn-onboard/9.11` (ovs-appctl reference — 20.4 apply daily workflow), `sdn-onboard/9.15` (classifier — 20.4 reference subtable lookup count), `sdn-onboard/9.22` (multi-table pipeline — 20.4 apply add-flow goto_table), `sdn-onboard/9.24` (conntrack concept — 20.4 operational CRUD), `sdn-onboard/9.25` (flow debug ofproto/trace — 20.4 reference), `sdn-onboard/9.26` (forensic incident class — 20.4 prevent via operational hygiene), `sdn-onboard/20.0` (systematic debug — 20.4 complement morning routine), `sdn-onboard/20.3` (OVN sister playbook — 20.4 parallel structure cho OVS pure) |

> **Quy tắc dependency Block XX:** Part 20.x các file bổ sung chiều sâu cho Block IX (OVS) + Block XIII (OVN). Khi sửa 20.0/20.1/20.2, KHÔNG được lặp lại nội dung foundation từ 13.x/9.x — chỉ reference section cross-link. Part 20.2 cụ thể prerequisite 8 Part, phải verify mọi forward-ref còn valid khi thêm section mới.

### Tầng 5: Image files (SVG → Markdown captions)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `images/fd-kernel-3-table-model.svg` | Figure 1-1: TLPI Three-Table Model (pure, no fork/exec) | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~141) |
| `images/fd-exercise1-initial-open-read.svg` | Figure 1-2: Guided Exercise 2 baseline — 1 FD, 1 OFD, pos=5 | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~195) |
| `images/fd-exercise1-after-dup.svg` | Figure 1-3: Guided Exercise 2 sau dup() — FD 3,4 → OFD "A" | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~228) |
| `images/fd-exercise1-after-open-independent.svg` | Figure 1-4: Guided Exercise 2 sau open() độc lập — 2 OFDs | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~250) |
| `images/fd-exercise1-read-offset-sharing.svg` | Figure 1-5: Guided Exercise 2 final — open()+dup()+fork() | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~346) |
| `images/fd-exercise2-dup-write.svg` | Figure 1-6: Guided Exercise 3 Phần E — dup write nối tiếp | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~402) |
| `images/fd-exercise2-open-write.svg` | Figure 1-7: Guided Exercise 3 Phần F — open write đè dữ liệu | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~427) |
| `images/fd-exercise2-fork-write.svg` | Figure 1-8: Guided Exercise 3 Phần G — fork write xuyên process | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~457) |
| `images/fd-exercise3-status-flags-sharing.svg` | Figure 1-9: Guided Exercise 4 — Status flags sharing qua OFD | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~545) |
| `images/fd-exercise4-lseek-cross-process.svg` | Figure 1-10: Guided Exercise 5 — lseek xuyên process | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~623) |
| `images/fd-epoll-architecture.svg` | Figure 1-11: Kiến trúc epoll — Interest List, Ready List, Kernel Callback | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~823) |
| `images/fd-select-poll-vs-epoll.svg` | Figure 1-12: So sánh select(), poll() và epoll | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~839) |
| `images/fd-fork-exec-cloexec.svg` | Figure 1-13: fork()+exec() trên FD table, CLOEXEC | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~1017) |
| `images/fd-leak-and-cloexec.svg` | Figure 1-14: FD leak comparison (with/without CLOEXEC) | `linux-onboard/file-descriptor-deep-dive.md` (caption tại line ~1023) |

> **Quy tắc Tầng 5 (document-design Rule 8):** Khi sửa SVG, PHẢI đọc và update caption trong CÙNG batch thao tác. KHÔNG được giao SVG mà chưa verify caption. Chạy `svg-caption-consistency.py` trước commit.

> **Bài học từ lỗi thực tế:** Session 2026-03-30, `fd-kernel-3-table-model.svg` được rewrite từ combined diagram (fork+exec+socket) sang pure TLPI model, nhưng caption vẫn mô tả fork() và socket:443. Nguyên nhân: Tầng 5 chưa tồn tại → cross-file sync check bỏ sót hoàn toàn.

### Tầng 2m: Dependency map backfill v3.1.1 (2026-04-25 post-audit)

> **Scope:** 44 file content-phase đã viết (Phase B-H) chưa được backfill vào map. Audit 2026-04-25 phát hiện P1.D1 (37,9% file thiếu map) + P7.D1 (5 block 0% coverage: VII/VIII/XII/XIV/XV). Backfill đồng loạt theo group block để trả Rule 2 Cross-File Sync về 100% coverage.
>
> **Phương pháp verify:** Mỗi entry line count được đọc thực tế qua `wc -l` + section heading qua grep `^## [0-9]`. Không estimate, không guess.

#### Block IV OpenFlow evolution — 4.8/4.9 catalog reference (S41-S44)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/4.8 - openflow-match-field-catalog.md` | Content 926 dòng (S41 Phase H.3): catalog ~60 match field Template B 9-attribute anatomy. 12 nhóm: Metadata (6 field) + Register (16+8+4) + L2 (9) + ARP (5) + IPv4 (6) + IPv6 (7) + L4 TCP/UDP/SCTP (8) + ICMP (4) + Tunnel (6) + Conntrack (9) + MPLS (4) + misc (ip_frag + packet_type). Prerequisite chain table 12 rows. Lazy wildcarding thực nghiệm. | `sdn-onboard/README.md` TOC Block IV, `sdn-onboard/4.0`-`4.5` (OF spec evolution), `sdn-onboard/4.9` (action catalog sibling), `sdn-onboard/9.2` (megaflow wildcard mechanism), `sdn-onboard/9.15` (classifier TSS consume field), ovs-fields(7) man page |
| `sdn-onboard/4.9 - openflow-action-catalog.md` | Content 1544 dòng (S42-S44 Phase H.4): catalog ~40 action Template C 8-attribute anatomy tier 1+2+3. Tier 1: Output/drop/normal/flood/group/resubmit/clone/note. Tier 2: VLAN push/pop/MPLS/PBB/encap/decap/set_field generic/legacy mod_*/move-load register/write_metadata/set_tunnel/QoS set_queue+enqueue+meter. Tier 3: ct(commit/zone/nat/force/alg)/learn/conjunction/multipath/bundle/check_pkt_larger. Action Set vs Apply-Actions execution order 12-priority. | `sdn-onboard/README.md` TOC Block IV, `sdn-onboard/4.8` (match catalog sibling), `sdn-onboard/9.24` (ct action deep-dive), `sdn-onboard/13.3` (OVN ACL conjunction pattern), `sdn-onboard/13.11` (check_pkt_larger PMTUD), ovs-actions(7) |

#### Block V Mô hình SDN thay thế — 5.1/5.2 (Phase B)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/5.1 - hypervisor-overlays-nvp-nsx.md` | Content 305 dòng, 6 section: Nicira NVP sản phẩm thương mại 2011 / Kiến trúc hypervisor-edge OVS + controller tập trung / VMware acquisition 23/07/2012 (1,26 tỷ USD) / NSX-V (vSphere) vs NSX-T (đa hypervisor) / Juniper Contrail dòng dõi tương tự nhưng BGP EVPN control plane / Di sản: OVN là kẻ kế thừa tinh thần NVP. | `sdn-onboard/README.md` TOC Block V, `sdn-onboard/3.0` (Nicira founding), `sdn-onboard/5.0` (API-based sibling), `sdn-onboard/5.2` (whitebox complementary), `sdn-onboard/7.3` (NSX-T vendor context), `sdn-onboard/11.0` (VXLAN/Geneve overlay), `sdn-onboard/13.0` (OVN announcement lineage), `sdn-onboard/11.2` (BGP EVPN comparison) |
| `sdn-onboard/5.2 - opening-device-whitebox.md` | Content 313 dòng, 6 section: OCP Network project (2013+) / Whitebox hardware Celestica/Edgecore/Delta / Merchant silicon Broadcom Tomahawk+Trident / NOS options Cumulus Linux/SONiC/OpenSwitch/Stratum / ONIE Open Network Install Environment / Current state 2026: SONiC thắng thị phần hyperscale. | `sdn-onboard/README.md` TOC Block V, `sdn-onboard/5.0` (API-based sibling), `sdn-onboard/5.1` (hypervisor sibling), `sdn-onboard/16.0` (DPDK accelerate whitebox), `sdn-onboard/14.1` (Tofino PISA silicon alternative) |

#### Block VII Controller ecosystem — 7.0-7.5 (full block, Phase B)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/7.0 - nox-pox-ryu-faucet.md` | Content 258 dòng, 5 section: NOX 2008 (Ethane runtime open-source) / POX 2011 (Python port dạy học) / Ryu 2012 NTT (OpenFlow full 1.0-1.5) / Faucet 2015 REANNZ (production focus) / So sánh 4 controller + lựa chọn phù hợp. | `sdn-onboard/README.md` TOC Block VII, `sdn-onboard/2.4` (NOX origin Ethane), `sdn-onboard/3.1` (OF 1.0 target), `sdn-onboard/4.2` (OF 1.3 LTS cho Faucet), `sdn-onboard/7.4` (Faucet deep), `sdn-onboard/7.5` (Ryu deep) |
| `sdn-onboard/7.1 - opendaylight-architecture.md` | Content 180 dòng, 6 section: Thành lập Linux Foundation 08/04/2013 / Release train Hydrogen 2014 → Argon 2023 / MD-SAL trái tim kiến trúc (YANG data store) / Southbound plugins OpenFlow+NETCONF+BGP-LS+OVSDB / Triển khai thực tế Telefonica/Comcast/AT&T / Trạng thái hiện tại 2026: maintenance-only. | `sdn-onboard/README.md` TOC Block VII, `sdn-onboard/3.2` (ONF/LF governance), `sdn-onboard/5.0` (NETCONF/YANG model), `sdn-onboard/7.2` (ONOS sibling comparison) |
| `sdn-onboard/7.2 - onos-service-provider-scale.md` | Content 158 dòng, 6 section: ON.Lab + AT&T 2012-2014 origin / Kiến trúc phân tán Atomix multi-master / Mục tiêu hiệu năng 1M flow + 100ms control loop / Trellis SD-Fabric stack đầy đủ DC / ON.Lab hợp nhất với ONF 10/2018 / So sánh trực tiếp ONOS vs ODL. | `sdn-onboard/README.md` TOC Block VII, `sdn-onboard/3.2` (ONF-ONLab merger 10/2018), `sdn-onboard/7.1` (ODL comparison), `sdn-onboard/10.1` (Atomix Raft cluster), `sdn-onboard/4.6` (Google B4 lineage) |
| `sdn-onboard/7.3 - vendor-controllers-aci-contrail.md` | Content 191 dòng, 5 section: Cisco ACI và APIC / Juniper Contrail và Tungsten Fabric / VMware NSX-T từ NVP đến hiện tại / Arista CloudVision cách tiếp cận khác biệt / Đánh đổi mô hình mở vs vendor. | `sdn-onboard/README.md` TOC Block VII, `sdn-onboard/5.1` (NSX-T hypervisor overlay), `sdn-onboard/7.1` + `7.2` (open controller sibling), `sdn-onboard/13.0` (OVN là open alternative) |
| `sdn-onboard/7.4 - faucet-pipeline-and-operations.md` | Content 272 dòng, 4 section: Tại sao Faucet chọn pipeline cố định / Bốn bảng cốt lõi trong pipeline Faucet / ACL nâng cao trong Faucet / Gauge giám sát với Prometheus. | `sdn-onboard/README.md` TOC Block VII, `sdn-onboard/7.0` (Faucet origin), `sdn-onboard/4.2` (OF 1.3 LTS target), `sdn-onboard/9.8` (flow monitoring context Prometheus) |
| `sdn-onboard/7.5 - ryu-flow-management.md` | Content 419 dòng, 4 section: Kiến trúc event system của Ryu / OFPFlowMod cài đặt và xóa flow entry / REST API pattern trong Ryu / Thu thập traffic statistics. | `sdn-onboard/README.md` TOC Block VII, `sdn-onboard/7.0` (Ryu origin), `sdn-onboard/4.1`-`4.4` (OF 1.2-1.5 support), `sdn-onboard/9.4` (OVS CLI alternative path), `sdn-onboard/4.9` (action catalog OFPFlowMod consume) |

#### Block VIII Linux networking primer — 8.0-8.3 (full block, Phase B)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/8.0 - linux-namespaces-cgroups.md` | Content 194 dòng, 4 section: Linux namespaces 7 loại (net/mnt/pid/ipc/uts/user/cgroup) / Network namespace: `ip netns`, `/var/run/netns` / `unshare` và `nsenter` syscall + command / cgroups v1 vs v2. | `sdn-onboard/README.md` TOC Block VIII, `sdn-onboard/8.1` (bridge/veth trong netns), `sdn-onboard/9.13` (libvirt/docker integration), `sdn-onboard/11.3` (GRE lab dùng netns), `linux-onboard/file-descriptor-deep-dive.md` (TLPI process model) |
| `sdn-onboard/8.1 - linux-bridge-veth-macvlan.md` | Content 254 dòng, 7 section: brctl legacy vs `ip link` modern / Bridge datapath trong kernel / veth pair `net/core/veth.c` / macvlan 4 modes (private/vepa/bridge/passthru) / ipvlan L2 vs L3 / Pattern br-int/br-ex/br-tun (compass Ch F) / Tại sao OVS thay thế Linux bridge cho SDN. | `sdn-onboard/README.md` TOC Block VIII, `sdn-onboard/8.0` (netns prerequisite), `sdn-onboard/9.1` (OVS 3-component architecture), `sdn-onboard/9.13` (libvirt/docker), `sdn-onboard/13.4` (br-int NOT Linux bridge) |
| `sdn-onboard/8.2 - linux-vlan-bonding-team.md` | Content 182 dòng, 4 section: VLAN stacking (single-tagged / QinQ / triple-tagged) / Bonding 7 modes / LACP specifics / Team daemon (deprecate trong RHEL 9). | `sdn-onboard/README.md` TOC Block VIII, `sdn-onboard/8.1` (bridge prerequisite), `sdn-onboard/9.6` (OVS bonding sibling comparison), `sdn-onboard/9.20` (OVS VLAN access/trunk), IEEE 802.1Q + 802.1ad |
| `sdn-onboard/8.3 - tc-qdisc-and-conntrack.md` | Content 207 dòng, 5 section: tc qdisc taxonomy / HTB + HFSC + fq_codel / conntrack zones + marks + states / iptables-nft vs nftables native / OVS `ct()` action tích hợp conntrack. | `sdn-onboard/README.md` TOC Block VIII, `sdn-onboard/9.9` (OVS QoS policing via tc), `sdn-onboard/9.24` (OVS conntrack stateful firewall), `sdn-onboard/4.9` (OF meter vs tc comparison) |

#### Block IX OVS internals — 9.15-9.21/9.23 (Phase B-H tier 2+)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/9.15 - ofproto-classifier-tuple-space-search.md` | Content 407 dòng (S45 Phase H.5): struct classifier + cls_subtable + minimask bit-packing; TSS algorithm Srinivasan-Varghese SIGCOMM 1999; Patricia trie prefix optimization; cmap RCU-safe read; performance pathology (subtable explosion + priority sort churn). §9.15.7-9 subtable internals + `dpctl/dump-flows` masked output anatomy. | `sdn-onboard/README.md` TOC Block IX, `sdn-onboard/9.1` (ofproto prerequisite), `sdn-onboard/9.2` (megaflow relationship), `sdn-onboard/4.8` (match field consume), `sdn-onboard/9.19` (flow table granularity related), `lib/classifier.c` upstream |
| `sdn-onboard/9.16 - ovs-connection-manager-controller-failover.md` | Content 433 dòng (S45 Phase H.5): multi-controller 3-node setup + `ofproto/show-connection` anatomy + role election timeline. §9.16.7-10: OFPT_ROLE_REQUEST wire format + OFPT_SET_ASYNC + connmgr coverage counter + 6-symptom troubleshooting matrix. | `sdn-onboard/README.md` TOC Block IX, `sdn-onboard/9.1` (OVS architecture), `sdn-onboard/4.1` (OF 1.2 controller role EQUAL/MASTER/SLAVE origin), `sdn-onboard/7.1`-`7.2` (controller architecture consumer), `ofproto/connmgr.c` upstream |
| `sdn-onboard/9.17 - ovs-performance-benchmark-methodology.md` | Content 276 dòng: iperf + netperf + pktgen; DPDK testpmd; scaling megaflow entry count 200K-2M; line-rate validation; revalidator throughput measurement. | `sdn-onboard/README.md` TOC Block IX, `sdn-onboard/9.2` (megaflow metric baseline), `sdn-onboard/9.3` (DPDK benchmark context), `sdn-onboard/9.5` (hardware offload benchmark) |
| `sdn-onboard/9.18 - ovs-native-l3-routing.md` | Content 317 dòng: OVS native L3 với `dec_ttl` action; multi-table recipe router; static routing mô phỏng với flow rule (không dùng Linux kernel routing). | `sdn-onboard/README.md` TOC Block IX, `sdn-onboard/4.9` (dec_ttl action catalog), `sdn-onboard/13.11` (OVN distributed router comparison), `sdn-onboard/9.22` (multi-table pipeline foundation) |
| `sdn-onboard/9.19 - ovs-flow-table-granularity.md` | Content 278 dòng: flow table = megaflow granularity choice; microflow vs megaflow trade-off; wildcarded mask design; rule count vs lookup time. | `sdn-onboard/README.md` TOC Block IX, `sdn-onboard/9.2` (megaflow internal), `sdn-onboard/9.15` (TSS subtable mechanism), `sdn-onboard/4.8` (match field wildcard context) |
| `sdn-onboard/9.20 - ovs-vlan-access-trunk.md` | Content 337 dòng: OVS port VLAN mode 4 type (access/trunk/native-tagged/native-untagged); vlan_mode + trunks + tag field in Port table; push_vlan/pop_vlan action trong flow. | `sdn-onboard/README.md` TOC Block IX, `sdn-onboard/8.2` (Linux VLAN comparison), `sdn-onboard/4.9` (push_vlan/pop_vlan action), `sdn-onboard/9.1` (ovs-vsctl prerequisite) |
| `sdn-onboard/9.21 - mininet-for-ovs-labs.md` | Content 571 dòng: Mininet 2.3.0 Python topology API; `mn` CLI; custom topology class; OVS integration default; use case giáo dục + lab reproducible. | `sdn-onboard/README.md` TOC Block IX, `sdn-onboard/0.1` (lab environment setup), `sdn-onboard/9.1` (OVS prerequisite), `sdn-onboard/9.25` (trace lab consumer), `sdn-onboard/9.27` (packet journey lab consumer) |
| `sdn-onboard/9.23 - ovs-stateless-acl-firewall.md` | Content 346 dòng (Phase D): stateless ACL recipe với single-table 5-tuple match; priority ordering; default-deny pattern; comparison với OVN ACL + iptables stateless. | `sdn-onboard/README.md` TOC Block IX, `sdn-onboard/9.22` (multi-table prerequisite), `sdn-onboard/9.24` (stateful sibling), `sdn-onboard/13.3` (OVN ACL apply concept), `sdn-onboard/8.3` (iptables comparison) |

#### Block X OVSDB management — 10.0/10.3-10.6 (Phase B-F)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/10.0 - ovsdb-rfc7047-schema-transactions.md` | Content 196 dòng, 6 section: OVSDB ordered + transactional + schema-bound / Schema vswitchd tables / Column types / 10 operations RFC 7047 (insert/select/update/mutate/delete/wait/commit/abort/comment/assert) / monitor_cond protocol / Client tools (ovsdb-client, ovs-vsctl). | `sdn-onboard/README.md` TOC Block X, `sdn-onboard/9.1` (ovsdb-server in OVS arch), `sdn-onboard/10.1` (Raft build on top), `sdn-onboard/10.2` (backup/restore), `sdn-onboard/10.3` (ACID semantics detail), `sdn-onboard/13.1` (OVN NBDB/SBDB use RFC 7047) |
| `sdn-onboard/10.3 - ovsdb-transaction-acid-semantics.md` | Content 321 dòng, 6 section: Bốn tính chất ACID của OVSDB transaction / Cấu trúc transaction trong protocol RFC 7047 / Prerequisites check (wait + assert + nb_cfg) / Xử lý xung đột của mutate / Transaction failure + cơ chế retry của client / Hạn chế so với SQL database transaction. | `sdn-onboard/README.md` TOC Block X, `sdn-onboard/10.0` (transaction basics), `sdn-onboard/10.4` (IDL monitor consumer), `sdn-onboard/10.5` (performance benchmark) |
| `sdn-onboard/10.4 - ovsdb-idl-monitor-cond-client.md` | Content 386 dòng, 6 section: Tại sao cần IDL thay vì JSON-RPC trực tiếp / Protocol monitor so với monitor_cond / Kiến trúc thư viện IDL client / Sao chép có điều kiện — thay đổi condition thời gian chạy / Xử lý mất kết nối + đồng bộ lại / Cân nhắc hiệu năng cho IDL client ở quy mô lớn. | `sdn-onboard/README.md` TOC Block X, `sdn-onboard/10.0` (RFC 7047 monitor), `sdn-onboard/13.7` (ovn-controller IDL consumer), `sdn-onboard/13.8` (ovn-northd IDL consumer) |
| `sdn-onboard/10.5 - ovsdb-performance-benchmarking.md` | Content 297 dòng, 5 section: Đặc tính hiệu năng cơ bản / Các yếu tố ảnh hưởng hiệu năng ở quy mô lớn / Phương pháp benchmark / Các kỹ thuật tinh chỉnh chính / Điểm nghẽn điển hình và cách phát hiện. | `sdn-onboard/README.md` TOC Block X, `sdn-onboard/10.1` (Raft cluster context), `sdn-onboard/10.3` (transaction semantics baseline), `sdn-onboard/13.1` (OVN scale target), `sdn-onboard/9.17` (OVS benchmark methodology sibling) |
| `sdn-onboard/10.6 - ovsdb-security-mtls-rbac-advanced.md` | Content 365 dòng, 6 section: Mô hình bảo mật OVSDB server-side / Thiết lập mTLS cho cluster OVSDB / Xoay cert không downtime / RBAC advanced multi-tenant + condition-based / Ghi log audit và tuân thủ / Mô hình threat + giải pháp. | `sdn-onboard/README.md` TOC Block X, `sdn-onboard/10.2` (RBAC basic), `sdn-onboard/9.10` (TLS/PKI foundation), `sdn-onboard/20.1` (security hardening apply) |

#### Block XI Overlay — 11.0/11.2 (Phase B)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/11.0 - vxlan-geneve-stt.md` | Content 213 dòng, 6 section: Tại sao cần overlay encapsulation / VXLAN (RFC 7348, 08/2014, UDP 4789 + 24-bit VNI) / Geneve (RFC 8926, 11/2020, variable TLV + class 0x0102) / STT deprecated (TCP-like header, removed) / So sánh 3 protocol / Multipoint tunneling với `options:key=flow`. | `sdn-onboard/README.md` TOC Block XI, `sdn-onboard/11.1` (MTU/PMTUD consumer), `sdn-onboard/11.2` (BGP EVPN control plane), `sdn-onboard/11.3` (GRE sibling), `sdn-onboard/11.4` (IPsec overlay), `sdn-onboard/13.0` (OVN Geneve default), RFC 7348 + RFC 8926 |
| `sdn-onboard/11.2 - bgp-evpn-control-plane-overlay.md` | Content 157 dòng, 6 section: Flood-and-learn — vấn đề của VXLAN gốc / BGP EVPN (RFC 7432, 02/2015) / 5 EVPN route types / VXLAN + EVPN workflow / Leaf-spine DC fabric với EVPN / OVN vs BGP EVPN. | `sdn-onboard/README.md` TOC Block XI, `sdn-onboard/11.0` (VXLAN prerequisite), `sdn-onboard/12.1` (DC EVPN integration consumer), `sdn-onboard/5.1` (Juniper Contrail BGP EVPN), RFC 7432 + RFC 8365 |

#### Block XII SDN trong Data Center — 12.0-12.2 (full block, Phase B)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/12.0 - dc-network-topologies-clos-leaf-spine.md` | Content 143 dòng: Clos network 1953; fat-tree Al-Fares SIGCOMM 2008; leaf-spine 2-tier; oversubscription ratio; Jupiter 5-stage; Facebook Fabric 4-post. | `sdn-onboard/README.md` TOC Block XII, `sdn-onboard/1.0` (pre-SDN DC pain context), `sdn-onboard/12.1` (overlay integrate topology), `sdn-onboard/11.0` (VXLAN over leaf-spine) |
| `sdn-onboard/12.1 - dc-overlay-integration-vxlan-evpn.md` | Content 178 dòng: VXLAN + EVPN integration DC; leaf-spine underlay + overlay separate; anycast gateway; symmetric vs asymmetric IRB. | `sdn-onboard/README.md` TOC Block XII, `sdn-onboard/11.0` (VXLAN), `sdn-onboard/11.2` (EVPN control plane), `sdn-onboard/12.0` (leaf-spine topology), `sdn-onboard/12.2` (micro-seg apply) |
| `sdn-onboard/12.2 - micro-segmentation-service-chaining.md` | Content 162 dòng: Zero Trust micro-segmentation; east-west firewall; NSH SFC RFC 8300; comparison NSX DFW + OVN ACL + Cilium. | `sdn-onboard/README.md` TOC Block XII, `sdn-onboard/12.1` (DC overlay context), `sdn-onboard/13.3` (OVN ACL implementation), `sdn-onboard/15.0` (service mesh sibling), RFC 8300 |

#### Block XIII OVN foundation — 13.0/13.9/13.13 (Phase B-H)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/13.0 - ovn-announcement-2015-rationale.md` | Content 153 dòng: OVN announcement 01/2015 (Pfaff/Pettit); tại sao 8 năm sau OVS; scope "shifting to OVN" rationale; comparison NSX proprietary + OVS pure; 3-pillar NBDB + northd + SBDB + controller. | `sdn-onboard/README.md` TOC Block XIII, `sdn-onboard/3.0` (Nicira/Stanford lineage), `sdn-onboard/5.1` (ngữ cảnh mô hình NSX hypervisor overlay), `sdn-onboard/9.0` (OVS pure ngữ cảnh hạn chế tạo động cơ cho OVN), `sdn-onboard/13.1` (architecture detail consumer) |
| `sdn-onboard/13.9 - ovn-load-balancer-internals.md` | Content 218 dòng: Load_Balancer NBDB schema; `ct_lb` action; VIP → pool member hash distribution; Service_Monitor health check; relationship với kube-proxy comparison. | `sdn-onboard/README.md` TOC Block XIII, `sdn-onboard/13.1` (NBDB schema), `sdn-onboard/13.3` (ACL+LB+NAT sibling), `sdn-onboard/13.11` (gateway router LB), `sdn-onboard/4.9` (ct_lb action catalog) |
| `sdn-onboard/13.13 - ovs-to-ovn-migration-guide.md` | Content 403 dòng: migration từ pure OVS setup sang OVN; NB schema mapping; phase rollout; rollback strategy; production checklist. | `sdn-onboard/README.md` TOC Block XIII, `sdn-onboard/9.0` (OVS baseline), `sdn-onboard/9.12` (rolling restart), `sdn-onboard/13.0` (OVN rationale), `sdn-onboard/13.1`-`13.12` (all OVN foundation reference) |

#### Block XIV P4 Programmable (Expert) — 14.0-14.2 (full block, Phase F)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/14.0 - p4-language-fundamentals.md` | Content 507 dòng, 7 section (S36a Phase F): Drama mở đầu "tại sao OpenFlow match field cứng?" / Cấu trúc chương trình P4_16 / PSA (Portable Switch Architecture) / PISA (Protocol Independent Switch Architecture) / BMv2 compiler + behavioral model / So sánh P4 với OpenFlow + OVS + OVN / Điểm cốt lõi. | `sdn-onboard/README.md` TOC Block XIV, `sdn-onboard/2.1` (Active Networking ancestor), `sdn-onboard/4.6` (OpenFlow hạn chế tạo động cơ P4), `sdn-onboard/14.1` (Tofino silicon target), `sdn-onboard/14.2` (P4Runtime API consumer) |
| `sdn-onboard/14.1 - tofino-pisa-silicon.md` | Content 356 dòng, 7 section (S36b Phase F): Drama "fixed-function ASIC → Tofino 2016" / Kiến trúc tham chiếu PISA / Các thế hệ Tofino 1 → 2 → 3 / Tài nguyên stage và ràng buộc compile / Intel mua lại + lộ trình EOL / So sánh Tofino PISA vs fixed-function ASIC Broadcom vs DPDK CPU / Điểm cốt lõi. | `sdn-onboard/README.md` TOC Block XIV, `sdn-onboard/14.0` (P4 language), `sdn-onboard/5.2` (whitebox silicon context), `sdn-onboard/4.6` (silicon mismatch lesson), p4.org/p4-spec |
| `sdn-onboard/14.2 - p4runtime-gnmi-integration.md` | Content 491 dòng, 7 section (S36c Phase F): Drama "OpenFlow spec-driven → P4Runtime schema-driven" / Kiến trúc giao thức P4Runtime / API dựa trên schema / gNMI cho trạng thái vận hành / Tích hợp ONOS + Stratum / So sánh P4Runtime+gNMI với OpenFlow+NETCONF+SONiC / Điểm cốt lõi. | `sdn-onboard/README.md` TOC Block XIV, `sdn-onboard/14.0` (P4 language), `sdn-onboard/14.1` (Tofino target), `sdn-onboard/7.2` (ONOS + Stratum driver), p4.org/p4runtime |

#### Block XV Service Mesh + K8s (Expert) — 15.0-15.2 (full block, Phase F)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/15.0 - service-mesh-integration.md` | Content 474 dòng, 7 section (S36g Phase F): Drama "Hystrix+Finagle library → Envoy sidecar 2016-2017" / Mô hình kiến trúc service mesh / Istio với Envoy sidecar + xDS / Linkerd với linkerd2-proxy / Cilium service mesh dựa trên eBPF / OVN-Kubernetes CNI / Điểm cốt lõi. | `sdn-onboard/README.md` TOC Block XV, `sdn-onboard/12.2` (micro-segmentation sibling), `sdn-onboard/15.1` (OVN-K8s CNI deep), `sdn-onboard/15.2` (Cilium eBPF deep), `sdn-onboard/16.2` (eBPF XDP prerequisite) |
| `sdn-onboard/15.1 - ovn-kubernetes-cni-deep-dive.md` | Content 368 dòng, 5 section (K8S priority thấp theo user directive 2026-04-23): Các thành phần OVN-Kubernetes (nbctl-daemon master + ovnkube-node) / Dịch NetworkPolicy → OVN ACL / Service + thay thế kube-proxy / Mạng đa cluster OVN-IC / Di trú OpenShift-SDN → OVN-K8s. | `sdn-onboard/README.md` TOC Block XV, `sdn-onboard/13.1`-`13.12` (OVN foundation full), `sdn-onboard/9.13` (container integration pattern), `sdn-onboard/15.0` (service mesh sibling) |
| `sdn-onboard/15.2 - cilium-ebpf-internals.md` | Content 248 dòng, 5 section (K8S priority thấp): Kiến trúc datapath eBPF / Cilium CNI so với OVN-K8s / Thay thế kube-proxy / Cilium Service Mesh không có sidecar / Hubble nền tảng quan sát. | `sdn-onboard/README.md` TOC Block XV, `sdn-onboard/15.0` (service mesh comparison), `sdn-onboard/15.1` (OVN-K8s sibling), `sdn-onboard/16.2` (AF_XDP prerequisite), `sdn-onboard/9.24` (conntrack comparison) |

#### Block XVI Kernel + DPDK (Expert) — 16.0/16.2 (Phase F)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/16.0 - dpdk-afxdp-kernel-tuning.md` | Content 636 dòng, 9 section (S36d Phase F): Drama "kernel stack đủ → bypass Tbps" / So sánh data path kernel vs DPDK vs AF_XDP / DPDK EAL + PMD internals / AF_XDP zero-copy + XDP programs / Các nút điều chỉnh kernel / Ghim CPU + nhận biết cấu trúc NUMA / Profiling với perf + bpftrace / So sánh DPDK/AF_XDP/kernel với OVS + OVN + Cilium / Điểm cốt lõi. | `sdn-onboard/README.md` TOC Block XVI, `sdn-onboard/9.3` (OVS DPDK/AF_XDP), `sdn-onboard/16.1` (DPDK advanced sibling), `sdn-onboard/16.2` (AF_XDP eBPF program deep), `sdn-onboard/9.5` (hardware offload comparison) |
| `sdn-onboard/16.2 - afxdp-xdp-programs.md` | Content 560 dòng, 8 section (S36f Phase F): Drama "DPDK hoặc nothing → AF_XDP compromise kernel 4.18 (2018)" / Kiến trúc AF_XDP (4 ring) / Chế độ driver so với SKB / Loại + hành động của chương trình XDP / libbpf + libxdp userspace / Đặc tính hiệu năng / So sánh XDP/AF_XDP với DPDK + OVS + Cilium production / Điểm cốt lõi. | `sdn-onboard/README.md` TOC Block XVI, `sdn-onboard/16.0` (AF_XDP overview), `sdn-onboard/15.2` (Cilium apply XDP), `sdn-onboard/9.3` (OVS AF_XDP integration) |

#### Block XX Operational Excellence — 20.5/20.6 (Phase G.2.3 + G.4)

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/20.5 - ovn-forensic-case-studies.md` | Content 842 dòng (S58 Phase G.2.3): 3 case study distributed control plane: (1) Port_Binding migration race dual-bind 3-18s + SBDB Raft propagation; (2) northd bulk tenant deletion memory cascade 5000 LSP + I-P engine recompute fallback; (3) MAC_Binding ARP scan exploit table explosion. 3 design lesson + 2 GE + Capstone POE. | `sdn-onboard/README.md` TOC Block XX, `sdn-onboard/13.1` (SBDB Raft), `sdn-onboard/13.5` (Port_Binding 8 type), `sdn-onboard/13.7` (ovn-controller I-P engine), `sdn-onboard/13.8` (northd build_lflows), `sdn-onboard/20.2` (troubleshooting tool), `sdn-onboard/9.26` (OVS sister forensic) |
| `sdn-onboard/20.6 - ovs-openflow-ovn-retrospective-2007-2024.md` | Content 432 dòng (S59 Phase G.4): retrospective narrative 5 thời kỳ 2007-2024: (1) sơ khai Clean Slate/Nicira/OF 1.0/ONF; (2) reality đối mặt 1.1-1.5 evolution + Google B4 lesson; (3) hypervisor overlays thắng NSX/OpenStack; (4) OVN era 2015-2020; (5) production hardening 2020-2024. 10 meta-lesson + 6 frontier 2024-2030. | `sdn-onboard/README.md` TOC Block XX, `sdn-onboard/1.0`-`1.2` (pre-SDN context), `sdn-onboard/2.4` (Ethane predecessor), `sdn-onboard/3.0`-`3.2` (OpenFlow birth), `sdn-onboard/4.0`-`4.6` (OF evolution), `sdn-onboard/5.1` (NSX lineage), `sdn-onboard/9.0` (OVS history sibling), `sdn-onboard/13.0` (OVN announcement) |

> **Quy tắc dependency Tầng 2m:** Đây là mass backfill post-audit 2026-04-25 để đóng gap Rule 2. Line count + section count + content summary đã verify thực tế qua `wc -l` và grep section heading. Khi sửa các file này, verify related files trong cùng block + cross-block prerequisite. Pattern tổng quát: file nào cần prerequisite phải cite Block foundation (9.x cho OVS, 13.x cho OVN, 10.x cho OVSDB). Forward ref đến file advanced phải đúng số Part hiện tại.

---

## Quy tắc đồng bộ cụ thể

### Khi thay đổi version references (HAProxy version, Ubuntu version)

Phải kiểm tra TẤT CẢ file sau:
1. `README.md` (root) — section HAProxy
2. `haproxy-onboard/README.md` — TOC descriptions + Phụ lục A (Version Evolution Tracker)
3. MỌI Part file đã viết — inline version annotations (`> **Lưu ý phiên bản:**`)

**Bài học từ lỗi thực tế:** Session ngày 2026-03-29, sửa `haproxy-onboard/README.md` từ HAProxy 3.2 → 2.0 nhưng QUÊN `README.md` (root) vẫn còn "HAProxy 3.2". Phát hiện nhờ professor-style review, sửa trong commit `3535f14`.

### Khi thêm Part mới

1. Tạo file Part: `haproxy-onboard/X.0 - <name>.md`
2. Cập nhật `haproxy-onboard/README.md` — TOC entry + Mermaid dependency graph + reading path
3. Cập nhật `memory/haproxy-series-state.md` — thêm dòng mới
4. Cập nhật `memory/file-dependency-map.md` (file này) — thêm entry Part mới
5. Nếu có version-specific content: cập nhật Phụ lục A trong `haproxy-onboard/README.md`

### Khi sửa Mermaid dependency graph

1. Sửa graph trong `haproxy-onboard/README.md`
2. Cập nhật reading path description (cùng file, ngay dưới graph)
3. Kiểm tra `memory/haproxy-series-state.md` — prerequisites column có consistent không
