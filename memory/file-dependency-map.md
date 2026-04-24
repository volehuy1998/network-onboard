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
