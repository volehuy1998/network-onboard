# Ebook Coverage Map — Goransson/Black/Culver (2nd Ed, 2017) → sdn-onboard

> **Trạng thái:** Draft rev 1 — 2026-04-20
> **Ebook:** Paul Göransson, Chuck Black, Timothy Culver. *Software Defined Networks: A Comprehensive Approach*, 2nd Edition. Morgan Kaufmann / Elsevier, 2017. ISBN 978-0-12-804555-8, 438 pages.
> **Mục đích:** Map mọi chương/mục của ebook sang quyết định coverage trong series `sdn-onboard`, với scope gate KEEP / PARTIAL / SKIP + rationale + Block đích.
> **Nguyên tắc lọc (user directive 2026-04-20):** "những cái nào quá sa đà, rối rắm, hoặc hiểu sai của tác giả, ... bạn có thể bỏ qua nó" — bỏ nội dung lỗi thời, suy đoán thị trường đã không còn đúng, và các đoạn tiếp thị vendor.

---

## 1. Triết lý lọc

Ebook xuất bản 2017, viết trong thời điểm OpenFlow còn được xem là tương lai chủ đạo và NSX/Contrail/OpenDaylight đang cạnh tranh quyết liệt. Chín năm sau (2026), một số nhận định của tác giả đã bị lịch sử chứng minh sai hoặc lỗi thời. Bốn nhóm nội dung cần lọc:

Thứ nhất, *số liệu thị trường* (market sizing, acquisitions, VC funding, startup valuations) — Chương 14 là điển hình. Những số liệu năm 2014-2016 không còn phản ánh thực tế kỹ sư vận hành OpenStack/kolla-ansible năm 2026, và nếu trích dẫn sẽ dẫn đến misinformation.

Thứ hai, *dự đoán tương lai chưa thành hiện thực hoặc đã đổi hướng* — Chương 15 dự đoán SD-WAN sẽ "đẩy OpenFlow lên biên mạng"; thực tế SD-WAN overlay (Cisco Viptela, VMware VeloCloud) đi theo hướng IPsec + BGP EVPN, không phải OpenFlow. Giữ phần concept SD-WAN, bỏ dự đoán cụ thể.

Thứ ba, *ví dụ code legacy với Floodlight* — Chương 12 demo SDN application bằng Java + Floodlight. Năm 2026, ecosystem đã dịch chuyển sang Ryu (Python), ONOS (Java enterprise), Faucet (Python, focus campus), và hầu hết người vận hành OpenStack dùng OVN chứ không viết app trực tiếp. Giữ concept (reactive vs proactive, internal vs external), bỏ code Floodlight chi tiết.

Thứ tư, *marketing tone của tác giả về một số vendor* — vài đoạn về Nicira/VMware, Cisco ACI, Juniper Contrail có tính ca ngợi hơn phân tích kỹ thuật. Extract kỹ thuật, bỏ marketing tone.

---

## 2. Bảng coverage map

Ký hiệu: **KEEP** = đưa vào trực tiếp làm source chính cho Part tương ứng. **PARTIAL** = trích một phần (chỉ lấy concept/framework, bỏ ví dụ lỗi thời). **SKIP** = không dùng, ghi nhận để tránh quay lại. **REF** = reference ngắn trong appendix hoặc callout "Lịch sử", không phải nội dung chính.

### 2.1 Phần một — Foundations (Ch1-5)

| Ebook chapter/section | Pages | Decision | Rationale | Target Block |
|---|---|---|---|---|
| **Ch1 Introduction** | 1-21 | **KEEP** | Foundation trực tiếp: packet switching terms, three-plane model, protocol soup — giáo trình chuẩn. | Block I |
| Ch1.1 Basic Packet Switching Terminology | 2-4 | KEEP | Định nghĩa cốt lõi: switch, router, bridge, forwarding vs routing | 1.0 |
| Ch1.2 Historical Background | 4-5 | KEEP | Mainframe → LAN → bridged → routed lineage | 1.1 |
| Ch1.3 The Modern Data Center | 5-7 | KEEP | East-west traffic, ToR/spine-leaf | 1.2 |
| Ch1.4 Traditional Switch Architecture | 7-11 | KEEP | Three planes (data/control/management), software vs hardware forwarding | 1.3 |
| Ch1.5 Autonomous and Dynamic Forwarding Tables | 11-17 | KEEP | L2 control (STP, RSTP, MSTP), L3 control (OSPF, BGP), protocol soup critique | 1.4 |
| Ch1.6 Can We Increase the Packet Forwarding IQ? | 17-19 | KEEP | Motivation for programmable forwarding | 1.5 |
| Ch1.7 Open Source and Technological Shifts | 19-20 | PARTIAL | Concept KEEP, ignore specific OpenFlow predictions | 1.5 |
| Ch1.8 Organization of the Book | 20-21 | SKIP | Meta — về ebook itself, không liên quan series ta | — |
| **Ch2 Why SDN?** | 23-37 | **KEEP** | Core motivation chapter. Cost, vendor lock-in, innovation. | Block I |
| Ch2.1 Evolution of Switches and Control Planes | 23-28 | KEEP | Timeline hardware forwarding evolution | 1.3 |
| Ch2.2 Cost | 28-30 | PARTIAL | Concept cost breakdown KEEP; specific vendor cost numbers SKIP (lỗi thời) | 1.6 |
| Ch2.3 SDN Implications for Research and Innovation | 30-32 | KEEP | Tại sao SDN thúc đẩy nghiên cứu (Stanford/Berkeley) | 1.6 |
| Ch2.4 Data Center Innovation | 32-35 | KEEP | Compute + storage virtualization driving network virtualization | 1.7 |
| Ch2.5 Data Center Needs | 35-37 | KEEP | Automation, scalability, multipathing, multitenancy, NV | 1.7 |
| **Ch3 Genesis of SDN** | 39-59 | **KEEP** | Critical chapter — all forerunners. | Block II |
| Ch3.1 Evolution of Networking Technology | 39-42 | KEEP | Mainframe → LAN → bridged → routed | 2.0 (brief recap) |
| Ch3.2.1 Early Efforts (DCAN, GSMP, Active Networking) | 43 | KEEP | IEEE P1520, RFC 3292 (GSMP v3), DARPA Active Networking | 2.1 |
| Ch3.2.2 Network Access Control (NAC) | 43-44 | KEEP | RADIUS + COPS as early "control protocol" | 2.2 |
| Ch3.2.3 Orchestration (SNMP/CLI plug-ins) | 44-46 | KEEP | HP OpenView, IBM Tivoli historical lineage | 2.3 |
| Ch3.2.4 Virtualization Manager Plug-ins (vCenter/vMotion) | 46-48 | KEEP | VMware ESX/vCenter era — ra đời từ virtualization | 2.4 |
| Ch3.2.5 ForCES | 48-49 | KEEP | IETF 2003, FE/CE/NE, RFC 3654/3746, lý do ForCES không thắng | 2.5 |
| Ch3.2.6 4D Project | 49-51 | KEEP | Princeton/CMU 2004-2005, Decision/Dissemination/Discovery/Data | 2.6 |
| Ch3.2.7 Ethane | 51-52 | KEEP | Stanford 2007, Casado, direct ancestor của OpenFlow | 2.7 |
| Ch3.3 Legacy Mechanisms Evolve Toward SDN | 52 | SKIP | Rất ngắn, không thêm giá trị | — |
| Ch3.4 Software Defined Networking is Born | 52-54 | KEEP | OpenFlow birth 2008, ONF 21/03/2011, 6 operators | 2.8 |
| Ch3.5 Sustaining SDN Interoperability | 54-56 | PARTIAL | Concept KEEP; tổ chức liên quan nay đã đổi (ONF sáp nhập, MEF…) | 2.9 |
| Ch3.6 Open Source Contributions | 56-58 | PARTIAL | Framework KEEP (power/danger of collective); examples đã outdated | 2.9 |
| Ch3.7 Network Virtualization | 58 | KEEP | Khái niệm NV — tiền đề cho Block XI (Overlay), XIII (OVN) | 2.9 |
| Ch3.8 May I Please Call My Network SDN? | 58-59 | KEEP | Marketing vs technical SDN — cần cho kỹ sư phân biệt | 2.9 |
| **Ch4 How SDN Works** | 61-87 | **KEEP** | Canonical architecture chapter. | Block III |
| Ch4.1 Fundamental Characteristics of SDN | 61-63 | KEEP | Plane separation, centralized control, automation, openness | 3.0 |
| Ch4.2 SDN Operation | 64-66 | KEEP | Packet journey through SDN system | 3.1 |
| Ch4.3 SDN Devices | 66-71 | KEEP | Flow tables, software switches, hardware switches, scaling flows | 3.2 |
| Ch4.4 SDN Controller | 71-76 | KEEP | Core modules, northbound/southbound, issues (scale, failure, consistency) | 3.3 |
| Ch4.5 SDN Applications | 76-77 | KEEP | App responsibilities, reactive vs proactive preview | 3.4 |
| Ch4.6 Alternate SDN Methods (intro) | 77-87 | PARTIAL | Chỉ intro; deep dive ở Ch6/7 | 3.5 (brief) |
| **Ch5 The OpenFlow Specification** | 89-135 | **KEEP** | Canonical reference — full chapter. | Block IV |
| Ch5.1 Chapter-Specific Terminology | 89-90 | KEEP | Terms reference | 4.0 appendix |
| Ch5.2 OpenFlow Overview | 90-95 | KEEP | Switch, controller, protocol, secure channel (TLS optional!) | 4.0 |
| Ch5.3 OpenFlow 1.0 and OpenFlow Basics | 95-107 | KEEP | Foundation version — ports, flow table, 12-tuple match, actions, messaging | 4.1 |
| Ch5.4 OpenFlow 1.1 Additions | 107-113 | KEEP | Multi-table, groups, MPLS/VLAN, virtual ports, CC failure | 4.2 |
| Ch5.5 OpenFlow 1.2 Additions | 113-118 | KEEP | Extensible match (OXM), SET_FIELD, multi-controllers | 4.3 |
| Ch5.6 OpenFlow 1.3 Additions | 118-125 | KEEP | Per-flow meters (QoS), auxiliary connections, PBB, cookies | 4.4 |
| Ch5.7 OpenFlow 1.4 Additions | 125-127 | KEEP | Bundles, eviction/vacancy, optical port | 4.5 |
| Ch5.8 OpenFlow 1.5 Additions | 127-130 | KEEP | L4-L7, egress tables, carrier fitness | 4.6 |
| Ch5.9 Improving OpenFlow Interoperability | 130-131 | KEEP | TTP (ONF TS-017), Flow Objectives — critical for ODL users | 4.7 |
| Ch5.10 Optical Transport Protocol Extensions | 131-134 | PARTIAL | Concept KEEP (for awareness); deep dive SKIP (not relevant to OVS/OVN) | 4.7 appendix |
| Ch5.11 OpenFlow Limitations | 134 | KEEP | No DPI, silicon gap, processing delay, DDoS — critical criticism | 4.8 |

### 2.2 Phần hai — Alternatives, Ecosystems, Deployment (Ch6-13)

| Ebook chapter/section | Pages | Decision | Rationale | Target Block |
|---|---|---|---|---|
| **Ch6 Alternative Definitions of SDN** | 137-164 | **KEEP** | Essential balance chapter. | Block V |
| Ch6.1 Potential Drawbacks of Open SDN | 137-149 | KEEP | Change pace, SPOF, scale, DPI, stateful awareness | 5.0 |
| Ch6.2 SDN via APIs | 149-155 | KEEP | NETCONF/YANG, BGP-LS/PCE-P, REST + ranking | 5.1 |
| Ch6.3 SDN via Hypervisor-Based Overlays | 155-160 | KEEP | NVP/NSX, Contrail — direct ancestor of OVN | 5.2 |
| Ch6.4 SDN via Opening Up the Device | 160-162 | KEEP | Whitebox + merchant silicon | 5.3 |
| Ch6.5 Network Functions Virtualization (intro) | 162-163 | PARTIAL | Intro only; deep dive ở Block XVI | 5.4 |
| Ch6.6 Alternatives Overlap and Ranking | 163-164 | KEEP | Comparison matrix | 5.5 |
| **Ch7 Emerging Protocol/Controller/App Models** | 167-189 | **KEEP** | Evolution beyond OpenFlow. | Block VI |
| Ch7.1 Expanded Definitions of SDN | 167-170 | PARTIAL | Concept KEEP; NEM impact section đã lỗi thời | 6.0 |
| Ch7.2 Additional SDN Protocol Models | 170-177 | KEEP | NETCONF deep dive, BGP/BGP-LS/PCE-P, MPLS | 6.1 |
| Ch7.3 Additional SDN Controller Models | 177-183 | KEEP | Multi-southbound, model-driven, SP-targeted, scalable, intents | 6.2 |
| Ch7.4 Additional Application Models | 183-186 | KEEP | Proactive, declarative, external app focus | 6.3 |
| Ch7.5 New Approaches to SDN Security | 186-188 | PARTIAL | Framework KEEP; specific products lỗi thời | 6.4 |
| Ch7.6 The P4 Programming Language | 188 | KEEP | Brief intro — expand from other sources (P4.org spec) | 6.5 |
| **Ch8 SDN in the Data Center** | 191-215 | **KEEP** | Most practically relevant chapter for our audience. | Block XII |
| Ch8.1 Data Center Definition | 191-193 | KEEP | DC scope definition | 12.0 |
| Ch8.2 Data Center Demands | 193-198 | KEEP | Overcoming limits, add/move/delete, failure recovery, multitenancy, TE | 12.0 |
| Ch8.3 Tunneling Technologies for the Data Center | 198-202 | KEEP | VXLAN, NVGRE, STT — foundation for Block XI | 11.1/11.2/11.3 |
| Ch8.4 Path Technologies in the Data Center | 202-205 | KEEP | MSTP, SPB (IEEE 802.1aq), ECMP, SDN + SPF | 12.1 |
| Ch8.5 Ethernet Fabrics in the Data Center | 205-206 | PARTIAL | Concept KEEP; vendor fabric specifics (Brocade VCS, Cisco FabricPath) SKIP | 12.2 |
| Ch8.6 SDN Use Cases in the Data Center | 206-212 | KEEP | Five canonical use cases | 12.3 |
| Ch8.7 Comparison of Open SDN, Overlays, and APIs | 212 | KEEP | Decision matrix | 12.4 |
| Ch8.8 Real-World Data Center Implementations | 214 | SKIP | Outdated case studies (Google B4 moved on, AWS uses own stack) | — |
| **Ch9 SDN in Other Environments** | 217-239 | **PARTIAL** | Selectively relevant. | Block XV |
| Ch9.1 Wide Area Networks + Google B4 | 220-223 | KEEP | Google B4 is canonical — include historical context, note that Orion replaced B4 internally | 15.0 |
| Ch9.2 Service Provider and Carrier Networks | 223-227 | KEEP | MPLS-TE, MPLS-VPN with SDN | 15.1 |
| Ch9.3 Campus Networks | 227-233 | PARTIAL | Concept KEEP; specific campus examples lỗi thời | 15.2 |
| Ch9.4 Hospitality Networks | 233 | **SKIP** | Niche, one paragraph, not relevant for OpenStack engineers | — |
| Ch9.5 Mobile Networks | 233-235 | PARTIAL | SDN for mobile RAN concept KEEP; 4G-era specifics SKIP (5G/O-RAN now canonical) | 15.3 |
| Ch9.6 Optical Networks + Fujitsu example | 235-237 | PARTIAL | Concept KEEP; Fujitsu-specific SKIP | 15.4 |
| Ch9.7 SDN vs P2P/Overlay Networks | 238 | **SKIP** | Tangential, muddles the abstraction (P2P overlays like Tor are unrelated to DC overlays) | — |
| **Ch10 Network Functions Virtualization** | 241-252 | **KEEP** | Key adjacent topic. | Block XVI |
| Ch10.1 Definition of NFV | 241-243 | KEEP | ETSI NFV architecture | 16.0 |
| Ch10.2 What Can We Virtualize? | 243-244 | KEEP | VNF catalog (firewall, LB, IDS/IPS, CPE, router, WAF) | 16.0 |
| Ch10.3 Standards | 244 | KEEP | ETSI NFV working groups | 16.1 |
| Ch10.4 OPNFV | 244-246 | PARTIAL | Concept KEEP; note: OPNFV merged into Anuket in 2020 | 16.1 |
| Ch10.5 Leading NFV Vendors | 246 | SKIP | Vendor list lỗi thời | — |
| Ch10.6 SDN vs NFV | 246-247 | KEEP | Crucial distinction — kỹ sư thường nhầm | 16.2 |
| Ch10.7 In-Line Network Functions (SLB, Firewall, IDS) | 247-251 | KEEP | SDN-driven SLB/FW/IDS — relevant cho Octavia + OVN LB | 16.3 |
| **Ch11 Players in the SDN Ecosystem** | 253-268 | **PARTIAL** | Ecosystem map still useful; vendor specifics need 2026 refresh. | Block VII + appendix |
| Ch11.1 Academic Research Institutions | 253-255 | KEEP | Stanford, Berkeley, Princeton, CMU, ICSI | 7.0 appendix |
| Ch11.1.1 Key Contributors to SDN From Academia | 255-256 | KEEP | Casado, McKeown, Shenker, Parulkar, Appenzeller, Erickson, Sherwood | 7.0 |
| Ch11.2 Industry Research Labs | 256 | SKIP | Very short, no depth | — |
| Ch11.3 Network Equipment Manufacturers | 256-258 | PARTIAL | NEM list KEEP as historical; specific vendor "strategy" outdated | 7.4 |
| Ch11.4 Software Vendors | 258-260 | PARTIAL | Vendor names KEEP; product lines outdated | 7.4 |
| Ch11.5 White-Box Switches | 260-261 | KEEP | Whitebox category definition — still relevant (Arista, Accton, SONiC era) | 5.3 |
| Ch11.6 Merchant Silicon Vendors | 261-262 | KEEP | Broadcom Trident/Tomahawk, Mellanox (now NVIDIA), Intel Tofino | 5.3 |
| Ch11.7 Original Device Manufacturers (ODMs) | 262 | KEEP | Quanta, Accton, Delta — whitebox supply chain | 5.3 |
| Ch11.8 Cloud Services and Service Providers | 262-263 | PARTIAL | Concept KEEP; specific deployments (Rackspace SoftLayer…) outdated | 14.0 |
| Ch11.9.1 Open Networking Foundation | 265 | KEEP | ONF founding + role | 2.8, 7.0 |
| Ch11.9.2 OpenDaylight | 265 | KEEP | ODL governance + roles | 7.1 |
| Ch11.9.3 ONOS | 265-266 | KEEP | ONOS origin ON.Lab 2014 | 7.2 |
| Ch11.9.4 OpenStack | 266 | KEEP | OpenStack founding 2010, Foundation 2012, Neutron (formerly Quantum) | 14.0 |
| Ch11.9.5 OpenSwitch | 267 | PARTIAL | OpenSwitch has been superseded by SONiC (Microsoft) — note as historical | 18.x |
| Ch11.9.6 The Open Source SDN Community | 267 | SKIP | Very brief, no unique content | — |
| Ch11.9.7 IETF | 268 | KEEP | IETF role + BGP/NETCONF working groups | 2.5, 6.1 |
| **Ch12 SDN Applications** | 271-301 | **PARTIAL** | Concept framework KEEP; Floodlight code example SKIP (deprecated). | Block XVII (optional) |
| Ch12.1-12.3 Terminology, App Types | 271-281 | KEEP | Reactive/proactive/internal/external taxonomy | 17.0 |
| Ch12.4 A Brief History of SDN Controllers | 281 | KEEP | NOX → POX → Beacon → Floodlight lineage | 7.0 |
| Ch12.5-12.6 Floodlight Training + Blacklist App Java Code | 281-291 | **SKIP** | Floodlight deprecated; Java code not useful to kolla-ansible operator. Link to Appendix B only for historical reference. | — |
| Ch12.7 Controller Considerations (ODL, ONOS) | 291-292 | KEEP | API design impact | 17.1 |
| Ch12.8 Network Device Considerations | 292-295 | KEEP | OF + non-OF device considerations | 17.2 |
| Ch12.9 Creating Network Virtualization Tunnels | 295-296 | KEEP | App pattern for NV | 17.3 |
| Ch12.10 Offloading Flows in the Data Center | 296-297 | KEEP | Elephant flow offload pattern | 17.3 |
| Ch12.11 Access Control for the Campus | 297-299 | KEEP | Canonical SDN app | 17.4 |
| Ch12.12 Traffic Engineering for SPs | 299-300 | KEEP | TE app pattern | 17.4 |
| **Ch13 SDN Open Source** | 303-325 | **PARTIAL** | Landscape KEEP; specific package tutorials SKIP. | Block XVIII |
| Ch13.1 SDN Open Source Landscape | 303 | KEEP | Ecosystem map | 18.0 |
| Ch13.4 Open Source Licensing Issues | 305-307 | KEEP | GPL vs Apache vs MIT — critical for ops | 18.1 |
| Ch13.5 Profiles of SDN Open Source Users | 307-309 | SKIP | Generic, no unique value | — |
| Ch13.6 OpenFlow Source Code | 309-310 | PARTIAL | OF ref implementation history KEEP; specific source walk SKIP | 18.2 |
| Ch13.7 Switch Implementations | 310-312 | KEEP | OVS, ofsoftswitch13, OfDPA, Indigo | 18.2, 9.0 |
| Ch13.8 Controller Implementations | 312-316 | KEEP | NOX/POX/Ryu/Beacon/Floodlight/ODL/ONOS | 7.0-7.3 |
| Ch13.9 SDN Applications (open source) | 316-318 | PARTIAL | Concept KEEP; specific projects 2016-era | 18.3 |
| Ch13.10 Orchestration and NV | 318-319 | KEEP | OpenStack Neutron as NV orchestrator | 14.0 |
| Ch13.11 Simulation, Testing, and Tools | 319-320 | KEEP | Mininet, Containernet, ofsoftswitch13 | 18.4 |
| Ch13.12 Open Source Cloud Software (OpenStack, CloudStack) | 320-322 | KEEP (OpenStack) / SKIP (CloudStack) | CloudStack marginal in 2026 | 14.0 |
| Ch13.13 Example: Applying SDN Open Source | 322-325 | SKIP | Generic how-to, no new concept | — |

### 2.3 Phần ba — Business + Futures (Ch14-15) — Phần lớn SKIP

| Ebook chapter/section | Pages | Decision | Rationale |
|---|---|---|---|
| **Ch14 Business Ramifications** | 327-350 | **SKIP với ngoại lệ** | Market sizing, VC, acquisitions 2014-2016 đã lỗi thời. Career predictions speculative. |
| Ch14.1 Everything as a Service | 327-328 | SKIP | Concept đã phổ biến; không cần introduction |
| Ch14.2-14.3 Market Sizing + Vendor Classification | 328-330 | SKIP | Số liệu 2016 không còn đúng |
| Ch14.4 Impact on Incumbent NEMs | 330-332 | SKIP | Tiên đoán không chính xác — Cisco/Juniper vẫn thịnh vượng 2026 |
| Ch14.5 Impact on Enterprise Consumers | 332-333 | SKIP | Generic |
| Ch14.6 Turmoil in the Networking Industry | 333-334 | SKIP | Speculation đã không đúng |
| Ch14.7 Venture Capital | 335 | SKIP | VC data lỗi thời |
| Ch14.8 Major SDN Acquisitions | 335-340 | **REF only** | Nicira→VMware 2012, 1.26B KEEP as một câu reference trong Block II (lịch sử); phần còn lại SKIP |
| Ch14.9 SDN Startups | 340-347 | SKIP | Danh sách startup 2016 — nhiều đã phá sản hoặc pivot |
| Ch14.10 Career Disruptions | 347-349 | SKIP | Dự đoán sự nghiệp — không phải kỹ thuật |
| **Ch15 SDN Futures** | 353-372 | **PARTIAL** | Một số concept vẫn hợp lệ; dự đoán cụ thể đã outdated. |
| Ch15.1 Current State of Affairs | 353-355 | SKIP | "Current" 2016 ≠ 2026 |
| Ch15.2 SD-WAN | 355-360 | KEEP (core concept) | SD-WAN đã trở thành ngành công nghiệp riêng; concept overlay + central policy vẫn đúng. Bỏ dự đoán OpenFlow-based. | 15.5 |
| Ch15.3.1 Managing Nontraditional Physical Layers | 360-361 | SKIP | Quá speculative |
| Ch15.3.2 Applying Programming Techniques to Networks | 361-364 | PARTIAL | Concept NetKAT/P4 linking KEEP ngắn | 6.5 |
| Ch15.3.3 Security Applications | 364-366 | SKIP | Generic |
| Ch15.3.4 Roaming in Mobile Networks | 366-367 | SKIP | 5G/O-RAN đã thay thế |
| Ch15.3.5 Traffic Engineering in Mobile Networks | 367-369 | SKIP | Outdated |
| Ch15.3.6 Energy Savings | 369 | SKIP | Thực tế không hiện thực hoá |
| Ch15.3.7 SDN-Enabled Switching Chips | 370-371 | PARTIAL | Tofino + PISA vẫn relevant (Intel acquired, then shutdown 2023) — KEEP as historical callout | 4.9 |

### 2.4 Phụ lục

| Ebook appendix | Pages | Decision | Rationale |
|---|---|---|---|
| Appendix A Acronyms | 375-380 | **REF** | Đối chiếu khi viết acronym ở series ta; không include trực tiếp |
| Appendix B Blacklist Application (Java source) | 381-393 | **SKIP** | Floodlight Java code, không cần trong series kolla-ansible |

---

## 3. Thống kê coverage

| Decision | Số mục | Percentage |
|---|---|---|
| KEEP (nguồn chính cho Block tương ứng) | 62 mục | ~58% |
| PARTIAL (trích một phần) | 17 mục | ~16% |
| SKIP (không dùng) | 24 mục | ~22% |
| REF (chỉ nhắc trong appendix) | 4 mục | ~4% |

**Tổng lượng nội dung ebook được leverage:** ~74% (KEEP + PARTIAL). 22% SKIP là các đoạn lỗi thời, speculative, hoặc không liên quan OpenStack/kolla-ansible.

---

## 4. Khoảng trống ebook cần bổ sung từ nguồn khác

Ebook 2017 có những khoảng trống với thực tế 2026 — cần bổ sung từ nguồn chính thống:

Thứ nhất, *OVN* chỉ được nhắc một lần trong Ch6.3 dưới tên cũ. Deep dive OVN (Block XIII-XIV) phải lấy từ: [ovn.org](https://www.ovn.org/), [Network Heresy blog 13/01/2015](https://networkheresy.com/), [OVN patch history](https://github.com/ovn-org/ovn), [ovn-architecture(7) manpage](https://www.ovn.org/support/dist-docs/ovn-architecture.7.html).

Thứ hai, *OVSDB Raft clustering* không có trong ebook (chỉ active-standby). Raft support added in OVS 2.9 (Feb 2018). Nguồn: [ovsdb-server(5) manpage](https://docs.openvswitch.org/en/latest/ref/ovsdb-server.5/), [Raft paper Ongaro+Ousterhout 2014](https://raft.github.io/).

Thứ ba, *Geneve* chỉ brief mention. RFC 8926 (Nov 2020) không có trong ebook. Phải dựa trực tiếp [RFC 8926](https://datatracker.ietf.org/doc/html/rfc8926).

Thứ tư, *OpenStack Neutron ML2/OVN driver evolution*: ebook chỉ nhắc networking-ovn (early). ML2/OVN trở thành in-tree từ Rocky (Aug 2018). Nguồn: [OpenStack Neutron docs](https://docs.openstack.org/neutron/latest/admin/ovn/), [kolla-ansible neutron/ovn reference](https://docs.openstack.org/kolla-ansible/latest/reference/networking/neutron.html).

Thứ năm, *P4* chỉ một đoạn intro trong ebook. Deep dive Block VI.5 lấy từ [P4.org language specification](https://p4.org/specs/).

Thứ sáu, *SD-WAN* trong ebook dự đoán OpenFlow-based; thực tế đi theo IPsec+BGP. Lấy từ [MEF SD-WAN specifications](https://www.mef.net/resources/standards/), [Viptela/VMware SASE documentation](https://www.vmware.com/topics/glossary/content/sase.html).

Thứ bảy, *Linux bridge + netns + tc + conntrack* không có trong ebook. Block VIII hoàn toàn dựa [The Linux Programming Interface (Kerrisk)](https://man7.org/tlpi/), [man7.org manpages](https://man7.org/linux/man-pages/), [LWN.net articles](https://lwn.net/).

Thứ tám, *OVS kernel datapath architecture, megaflow, upcall*: NSDI 2015 paper "The Design and Implementation of Open vSwitch" của Pfaff et al. (không có trong ebook ngoại trừ một câu reference). [NSDI 2015 paper](https://www.usenix.org/conference/nsdi15/technical-sessions/presentation/pfaff).

---

## 5. Thứ tự ưu tiên nội dung từ ebook khi viết series

Khi một Part cần nội dung từ ebook, độ ưu tiên lấy theo thứ tự:

1. **Primary source:** ebook chapter được đánh KEEP trong table §2 — đây là nguồn chính, trích dẫn trực tiếp với số trang.
2. **Cross-reference:** các section PARTIAL — trích khung/framework, không copy example code/số liệu lỗi thời.
3. **Authoritative primary source bên ngoài:** khi ebook outdated hoặc thiếu, lấy từ nguồn §4 (ovn.org, datatracker.ietf.org, opennetworking.org, openvswitch.org, docs.openstack.org).
4. **Secondary recognized source:** Vincent Bernat blog, Scott Lowe, Russ White — chỉ khi primary thiếu.
5. **Never:** blog cá nhân không rõ tác giả, Stack Overflow không cross-referenced, medium.com bài trending.

---

## 6. Ghi chú thẩm định (fact-checker)

Các claim sau của ebook cần double-check trước khi đưa vào series:

| Ebook claim | Location | Status verification | Ghi chú |
|---|---|---|---|
| OpenFlow 1.0 spec 31/12/2009 | Ch5 + Ch3.4 | VERIFIED | [opennetworking.org wp-content 2013/04/openflow-spec-v1.0.0.pdf](https://opennetworking.org/wp-content/uploads/2013/04/openflow-spec-v1.0.0.pdf) |
| Nicira thành lập 2007 | Ch3.4.1 + Ch14.8 | VERIFIED | [Network Heresy archives](https://networkheresy.com/), Martin Casado Stanford PhD 2007 |
| VMware acquired Nicira 23/07/2012 $1.26B | Ch14.8 | VERIFIED | [VMware press release 23/07/2012](https://news.vmware.com/) |
| ONF founded 21/03/2011 bởi 6 operators (DT, FB, Google, Microsoft, Verizon, Yahoo!) | Ch3.4.2 | VERIFIED | [ONF About page](https://opennetworking.org/about/) |
| OpenStack founded 2010 Rackspace+NASA | Ch11.9.4 | VERIFIED | [OpenStack history](https://www.openstack.org/foundation/) |
| OVS moved to Linux Foundation | Ch13.7 | VERIFIED 2016 | [Linux Foundation OVS announcement](https://www.linuxfoundation.org/press/press-release/open-vswitch-moves-to-the-linux-foundation) |
| 4D Project at Princeton/CMU | Ch3.2.6 | NEEDS VERIFY | Check paper Greenberg/Hjalmtysson/Maltz "A Clean Slate 4D Approach" 2005 |
| Ethane SIGCOMM 2007 | Ch3.2.7 | VERIFIED | Casado et al., [dl.acm.org/doi/10.1145/1282380.1282382](https://dl.acm.org/doi/10.1145/1282380.1282382) |
| ForCES RFC 3654/3746 | Ch3.2.5 | VERIFIED | [RFC 3654](https://datatracker.ietf.org/doc/html/rfc3654), [RFC 3746](https://datatracker.ietf.org/doc/html/rfc3746) |

Tất cả fact-check pass sẽ được ghi lại trong file `memory/fact-check-log.md` khi viết content thực tế.

---

## 7. Quy trình cập nhật coverage map

Khi phát hiện một section ebook cần reclassify trong quá trình viết:

1. Update bảng §2 với decision mới + rationale
2. Ghi vào `memory/session-log.md` entry reclassification
3. Nếu decision thay đổi từ KEEP → SKIP: kiểm tra file `X.Y - *.md` nào đã reference section đó → update

Coverage map này là living document — tiến hoá cùng quá trình viết.

---

**Hết rev 1.** File này là tiên quyết cho `plans/sdn-foundation-architecture.md` rev 2.
