# Rubric 20-axis Per-Keyword Depth (SDN Curriculum)

> **Trạng thái:** Phase B v3.7 deliverable, draft 2026-04-26 chờ user sign-off (gate 2 per plan Section 14 + GP-4).
> **Phạm vi áp dụng:** Mỗi keyword in-scope của REF (`sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md`, ~320 entry).
> **Authority:** Rubric structure approved trong /plan v3.7 2026-04-26. Section formalization Phase B output này.
> **Mục đích:** Đo DEPTH (am hiểu cơ bản đến chuyên sâu) per-keyword theo 20 tiêu chí, không đo BREADTH (mention count). Cấm metric gaming per GP-5.

---

## 0. Lịch sử + Mục đích

### 0.1. Origin của 20 axis

13 axis đầu (axis 1-13) do user định trong message 2026-04-26 sau khi check 320+ keyword chưa thoả mãn nội dung depth. 7 axis sau (axis 14-20) Claude đề xuất dựa trên kinh nghiệm Vietnamese learner cần và pattern từ curriculum hiện tại (e.g., version drift, source code anchor là pattern từ Rule 14, lab exercise pattern từ Anatomy template).

### 0.2. Vì sao 20 axis (không phải 5 hay 13 hay 30)

5-axis (Bucket | Context | Purpose | Activity | Mechanism) hiện tại trong curriculum quá ít → keyword treatment thiếu lịch sử + sự cố + verification + cross-domain. 13-axis user định cover nhiều phương diện nhưng còn thiếu source verification (Rule 14 critical) + observability + lab + comparison. 30+ axis sẽ overlap nặng.

20 axis là sweet spot: covered fundamentals + practical operational + verifiability + comparable, không overlap excessive.

### 0.3. Threshold philosophy

Không phải mọi keyword cần đạt 20/20. Cornerstone (cốt lõi) cần 18-20/20 để sinh viên am hiểu thấu đáo. Peripheral (tool option niche) chỉ cần 10/20 đủ để engineer biết tồn tại + dùng được khi cần.

---

## 1. Cấu trúc tổng quát: 20 axis

| # | Axis (VN) | Axis (EN) | Loại | Tác giả | Auto-detect difficulty |
|---|-----------|-----------|------|---------|----------------------|
| 1 | Khái niệm + định nghĩa | Concept + definition | Definition | User | Easy |
| 2 | Lịch sử + bối cảnh ra đời | History + birth context | Historical | User | Medium |
| 3 | Vị trí trong kiến trúc | Architectural placement | Architectural | User | Easy |
| 4 | Vai trò + nhiệm vụ trong kiến trúc | Architectural role | Architectural | User | Medium |
| 5 | Vì sao được sinh ra | Motivation | Why | User | Hard |
| 6 | Vấn đề mà nó giải quyết | Problem solved | Why | User | Medium |
| 7 | Sự quan trọng + xếp hạng cốt lõi | Importance + criticality | Why | User | Hard |
| 8 | Cơ chế + nguyên lý hoạt động | Mechanism + operating principle | Mechanism | User | Medium |
| 9 | Cách kỹ sư vận hành thành thạo | Engineer master-operation | Operations | User | Medium |
| 10 | Phân loại taxonomy | Classification | Taxonomy | User | Easy |
| 11 | Cách dùng thành thạo + workflow | Proficient usage workflow | Operations | User | Medium |
| 12 | Khi xảy ra sự cố cần nhớ keyword này | Troubleshooting context | Troubleshooting | User | Hard |
| 13 | Liên quan mật thiết tới thành phần nào | Tight coupling cross-link | Cross-link | User | Medium |
| 14 | Sự khác biệt phiên bản | Version drift | Version | Claude | Easy |
| 15 | Verification: làm sao quan sát keyword đang hoạt động | Observability verification | Observability | Claude | Easy |
| 16 | Source code anchor | Source code reference | Source | Claude | Easy |
| 17 | Real-world incident anatomy | Production case study | Forensic | Claude | Hard |
| 18 | Lab exercise | Synthetic hands-on | Hands-on | Claude | Medium |
| 19 | Failure mode + diagnostic signal | Failure + diagnostic | Troubleshooting | Claude | Medium |
| 20 | So sánh cross-domain | Cross-domain analogue | Comparison | Claude | Medium |

### 1.1. Auto-detect difficulty levels

- **Easy:** regex pattern + position heuristic ≥ 90% accuracy
- **Medium:** mixed regex + content semantic check, manual override expected ~20-30%
- **Hard:** primarily manual judgement, regex pattern is signal not proof

---

## 2. Axis 1, Khái niệm + định nghĩa (Concept + definition)

### 2.1. Definition

Keyword được định nghĩa rõ ràng là gì + thuộc category nào trong taxonomy OVS/OF/OVN. Đây là axis nền tảng nhất; nếu fail axis 1, mọi axis sau đều rỗng.

### 2.2. Pass criteria

- 1+ câu định nghĩa explicit trong curriculum (không chỉ tên keyword)
- Category placement rõ ràng (e.g., "match field", "action", "subcommand", "OVSDB table column", "daemon")
- Định nghĩa không phải tautology ("X là X")
- Định nghĩa cho phép reader phân biệt keyword với concept lân cận

### 2.3. Fail example

```
ovs-monitor-ipsec
  Helper for IPsec monitoring.
```

**Fail vì:** "IPsec monitoring" tautology, không nói component nào, không phân biệt với `ipsec-tools`, `strongSwan`.

### 2.4. Pass example

```
ovs-monitor-ipsec là daemon helper Python (utility script trong OVS distribution)
chạy alongside ovsdb-server để watch OVSDB Open_vSwitch.other_config:ipsec_*
configuration. Khi config đổi, daemon trigger strongSwan reload swanctl.conf
mới. Loại: helper daemon, không phải core OVS component, không phải cli tool;
chỉ active khi OVS deployed với IPsec tunnel mode (Geneve over IPsec, VXLAN
over IPsec).
```

**Pass vì:** category rõ (helper daemon Python), function rõ (watch OVSDB → trigger strongSwan), boundary rõ (không phải core, chỉ active với IPsec mode).

### 2.5. Auto-detect signal

- Regex: keyword name xuất hiện trong 1-line định nghĩa của master index 0.3 (Bucket axis fill)
- Regex: keyword + " là " + descriptor (Vietnamese definition pattern)
- Regex: keyword + " is " + descriptor (English fallback nếu nhiều)
- Position: trong 5-axis Anatomy template Bucket field

### 2.6. Manual review when

- Definition exists nhưng circular ("X là cái dùng X")
- Multiple definitions across files conflict → reconcile manually
- Keyword là alias of multiple concepts (e.g., `ct` có thể là action `ct()`, prefix family `ct_state/ct_zone`, hoặc daemon `conntrack`)

### 2.7. Score

- **1.0:** Pass criteria all met
- **0.5:** Definition present nhưng category placement vague hoặc không phân biệt với concept lân cận
- **0:** Tautology hoặc absent
- **N/A:** Không applicable (không có case nào N/A cho axis 1)

---

## 3. Axis 2, Lịch sử + bối cảnh ra đời (History + birth context)

### 3.1. Definition

Keyword được introduce khi nào (version + năm + commit nếu có), trong bối cảnh kỹ thuật/tổ chức/người propose nào. Lịch sử per-keyword không phải lịch sử OVS/OF/OVN tổng quát.

### 3.2. Pass criteria

- Mention version/year specific (e.g., "OVS 1.11 (2013)", "OF 1.5 (2014)")
- 1+ trong 3:
  - (a) Lý do introduce (gap nào fill, alternative trước đó)
  - (b) Tổ chức/người propose (Nicira, ONF, Stanford, specific author)
  - (c) Vấn đề trước đó keyword address

### 3.3. Fail example

```
ct_state
  OF match field cho conntrack state.
```

**Fail vì:** không version, không bối cảnh.

### 3.4. Pass example

```
ct_state được Nicira giới thiệu OVS 2.5 (2016) cùng với action ct() như là
extension Nicira NXM_NX_CT_STATE. Trước đó OVS chỉ có stateless flow rule,
phải bypass vì conntrack functionality nằm trong Linux netfilter (iptables).
Pfaff propose ct_state để OVS có thể consume conntrack state trực tiếp trong
OF pipeline mà không cần upcall. OF 1.6 chuẩn hoá ct_state thành OXM_OF_CT_STATE
2018 sau ONF approve. Code: lib/ofp-actions.c commit 8e53fe8e22 2015-08-04.
```

**Pass vì:** version (OVS 2.5), năm (2016), người propose (Pfaff), lý do (stateless OVS không tận dụng được netfilter conntrack), evolution (Nicira ext → OF chuẩn).

### 3.5. Auto-detect signal

- Regex: `(OVS|OpenFlow|OVN|OF)\s+\d+\.\d+\+?` near keyword
- Regex: 4-digit year `(20\d{2})` near keyword
- Regex: people name "Pfaff", "Casado", "McKeown", "Pettit", "Shenker"
- Regex: organization "Nicira", "Stanford", "ONF", "VMware"

### 3.6. Manual review when

- Year/version mentioned nhưng cho concept lân cận không phải keyword cụ thể
- "Original" hoặc "ban đầu" without specific anchor
- Lịch sử OVS/OF/OVN tổng quát mention near keyword nhưng không link

### 3.7. Score

- **1.0:** Version/year + (lý do hoặc người hoặc problem-before)
- **0.5:** Chỉ có version, không có context
- **0:** Không version, không context
- **N/A:** Hiếm; có thể N/A cho concept không có "introduce" event (e.g., generic concept like "flow")

---

## 4. Axis 3, Vị trí trong kiến trúc (Architectural placement)

### 4.1. Definition

Keyword nằm ở component/layer nào trong stack OVS/OF/OVN. Architecture diagram: kernel datapath / userspace ofproto-dpif / OVSDB / control plane (controller, ovn-northd, ovn-controller).

### 4.2. Pass criteria

- Identify layer (kernel / userspace / OVSDB / control)
- Identify component within layer (e.g., "userspace classifier in ofproto-dpif")
- Identify scope (per-bridge / per-flow / per-packet / global)

### 4.3. Fail example

```
ct_state
  Trong OVS.
```

### 4.4. Pass example

```
ct_state nằm ở OpenFlow match field abstraction trong userspace ofproto-dpif
xlate layer, populated bởi ct() action invoke. Concretely: khi xlate gặp ct()
action, nó upcall xuống kernel netfilter conntrack, retrieve state, populate
flow's ct_state register. Downstream match rule trong cùng pipeline hoặc table
hạ nguồn (qua resubmit hoặc goto_table) có thể read ct_state. Scope: per-packet
(ct_state available trong context xử lý 1 packet, không persist between packet).
Khác với conntrack table entry chính (per-connection, kernel-side). Cross-link
9.2 §kernel datapath, 9.24 §ct() action, 9.1 §3-component architecture.
```

### 4.5. Auto-detect signal

- Regex: layer keywords "kernel datapath", "userspace", "ovsdb-server", "ofproto-dpif", "control plane", "br-int"
- Regex: scope keywords "per-bridge", "per-port", "per-flow", "per-packet", "global"

### 4.6. Manual review when

- Layer mentioned nhưng vague
- Multiple layer involved (e.g., ct_state spans kernel + userspace) cần manual reconcile

### 4.7. Score

- **1.0:** Layer + component + scope clear
- **0.5:** Layer clear nhưng scope mơ hồ
- **0:** Vague placement
- **N/A:** Hiếm

---

## 5. Axis 4, Vai trò + nhiệm vụ trong kiến trúc (Architectural role)

### 5.1. Definition

Function gì keyword đóng góp vào pipeline/system overall. "Role" khác "placement" ở chỗ role mô tả contribution function, placement mô tả location.

### 5.2. Pass criteria

- Statement "X đóng vai trò Y trong Z"
- Function rõ ràng (enable, gate, transform, observe, control)
- Scope of effect (single packet, flow lifetime, control state)

### 5.3. Pass example

```
ct_state đóng vai trò bridge giữa OVS stateless OF abstraction và Linux kernel
netfilter stateful conntrack. Cụ thể: ct_state cho phép flow rule downstream
phân biệt 4 transition state của 1 connection (NEW = first packet, EST = reply
seen, REL = related connection, INV = invalid). Without ct_state, OVS không
thể implement stateful firewall semantics; phải bypass external iptables.
Scope effect: flow lifetime (NEW → EST transition persist trong conntrack
table cho đến entry timeout).
```

### 5.4. Auto-detect signal

- Regex: "vai trò" / "role" / "function"
- Purpose axis fill trong 5-axis Anatomy

### 5.5. Manual review when

- Vai trò described chung chung ("quan trọng", "useful")
- Vai trò keyword overlap heavily với keyword khác → reconcile

### 5.6. Score

- **1.0:** Role explicit + scope effect clear
- **0.5:** Role mentioned nhưng scope mờ
- **0:** Vague hoặc absent
- **N/A:** Hiếm

---

## 6. Axis 5, Vì sao được sinh ra (Motivation)

### 6.1. Definition

Lý do thiết kế keyword tồn tại, gap nào nó fill, alternative trước đó là gì.

### 6.2. Pass criteria

- 1+ câu mô tả pre-existence pain (vấn đề OVS/OF/OVN hadn't have keyword)
- Hoặc design intent (mục tiêu cụ thể của đề xuất)
- Alternative trước (nếu có): cách giải quyết cũ tốn kém ra sao

### 6.3. Pass example

```
Megaflow ra đời 2014 vì microflow gốc của OVS có pain point production: mỗi
unique 5-tuple tạo 1 entry trong kernel datapath. Production traffic 100K+
new flow/sec (e.g., DC web server) gây flow explosion: kernel datapath giữ
hàng triệu entry, classifier traverse cost O(N), upcall rate cao gây
ovs-vswitchd CPU 100%. Megaflow fix: classifier output 1 wildcarded entry
generalize cho cluster microflow tương đồng, reduce entry count 100-1000x,
classifier load drop tương ứng. Trade-off: wildcarding mask consolidation
overhead ở revalidator, nhưng net win lớn.
```

### 6.4. Auto-detect signal

- Regex: "vì sao", "lý do", "motivation", "pain point", "before X", "trước đó"
- Position: gần keyword name + temporal phrase

### 6.5. Manual review when

- "Để improve performance" generic không cụ thể
- Motivation present nhưng không link tới keyword cụ thể

### 6.6. Score

- **1.0:** Pre-existence pain + design intent + alternative-before clear
- **0.5:** 1 trong 3 element
- **0:** Tautology hoặc absent
- **N/A:** Hiếm

---

## 7. Axis 6, Vấn đề mà nó giải quyết (Problem solved)

### 7.1. Definition

Cụ thể vấn đề kỹ thuật hoặc operational keyword address. Khác axis 5 ở chỗ axis 5 mô tả gap historic, axis 6 mô tả problem statement engineering.

### 7.2. Pass criteria

- Problem statement explicit (1+ câu)
- Solution mechanism (keyword X solves by Y)
- Scope of solution (full solve, partial solve, workaround)

### 7.3. Pass example

```
Conntrack zone giải quyết vấn đề shared conntrack table giữa nhiều logical
context có thể overlap 5-tuple. Ví dụ: tenant A có VM 10.0.0.5:80 → 8.8.8.8:443,
tenant B cũng có VM 10.0.0.5:80 → 8.8.8.8:443 (cùng IP overlap). Without zone,
cả 2 tenant share 1 conntrack entry, NAT collision, security violation. Zone
solve qua partition: zone=42 cho tenant A, zone=84 cho tenant B, mỗi zone độc
lập 5-tuple hashing. Scope solution: full solve cho conntrack-level isolation,
nhưng không solve address space overlap (cần namespace/VRF cho cái đó).
```

### 7.4. Auto-detect signal

- Regex: "vấn đề" / "problem" / "giải quyết" / "solves" / "address" near keyword
- Pattern: problem statement + "fix"/"solve"/"solution"

### 7.5. Manual review when

- "Giải quyết các vấn đề" mơ hồ không liệt kê specific
- Solution-without-problem (claim solve nhưng không nêu problem)

### 7.6. Score

- **1.0:** Problem + mechanism + scope
- **0.5:** Problem hoặc mechanism only
- **0:** Vague
- **N/A:** Hiếm

---

## 8. Axis 7, Sự quan trọng + xếp hạng cốt lõi (Importance + criticality)

### 8.1. Definition

Importance ranking của keyword trong architecture. Không phải mọi keyword equal; engineer cần biết "hiểu cái này là tier 1 mandatory, hay tier 3 niche optional".

### 8.2. Pass criteria

- Statement explicit về tier importance (foundational / important / specialized / niche)
- Justification (vì sao tier đó)

### 8.3. Pass example

```
Logical_Flow là cốt lõi tuyệt đối tier 1 của OVN. Justification: là intermediate
representation duy nhất giữa NBDB (declarative intent) và OF flow trên br-int
(physical execution). Mọi feature OVN cuối cùng đều compile xuống Logical_Flow:
ACL, LB, NAT, routing, DHCP, DNS, ARP. Nếu engineer không hiểu Logical_Flow,
không debug được bất kỳ vấn đề OVN compile pipeline nào. Tương đương "must
know" với megaflow trong OVS.
```

### 8.4. Auto-detect signal

- Regex: "trụ cột" / "cốt lõi" / "central" / "foundation" / "tier 1" / "must know"
- Position: explicit ranking statement near keyword

### 8.5. Manual review when

- "Quan trọng" generic không justify
- Implicit importance (covered extensively but never stated as tier)

### 8.6. Score

- **1.0:** Tier explicit + justification
- **0.5:** Tier implicit (extensive coverage tự nó là implicit "important")
- **0:** Absent
- **N/A:** Hiếm

---

## 9. Axis 8, Cơ chế + nguyên lý hoạt động (Mechanism + operating principle)

### 9.1. Definition

How it works internally: data flow, transitions, invariants, data structure changes. Đây là axis "mechanism" trong 5-axis Anatomy hiện tại.

### 9.2. Pass criteria

- Input/output description (gì vào, gì ra)
- State transitions hoặc data structure changes
- Invariants (gì luôn đúng)
- Algorithm hoặc strategy (TSS, hash, prefix match, etc.)

### 9.3. Pass example

```
Megaflow build qua TSS (Tuple Space Search) classifier algorithm: mỗi unique
mask pattern tạo 1 subtable, classifier traverse các subtable theo priority
order, return first match. Mask consolidation: 2 microflow có cùng wildcard
pattern (e.g., wildcard tp_src) share 1 megaflow entry. Invariant: mỗi packet
match exactly 1 megaflow (priority + uniqueness). Revalidator goroutine
validate megaflow mỗi 0.5-1 giây, evict nếu underlying flow rule changed
trong OVSDB. Data: subtable list trong struct cls_classifier; megaflow entry
trong struct dp_netdev_flow (kernel) hoặc struct ofproto_flow (userspace).
Transition: megaflow new → installed → revalidated → evicted → replaced.
```

### 9.4. Auto-detect signal

- Regex: data structure name pattern (struct X, table Y)
- Regex: algorithm name pattern (TSS, hash, prefix, longest-match)
- Regex: state transition pattern "X → Y", "transition", "state machine"

### 9.5. Manual review when

- Mechanism described cho concept lân cận không phải keyword cụ thể
- Surface-level "X works by Y" without internal detail

### 9.6. Score

- **1.0:** Input/output + transitions + invariants + algorithm
- **0.5:** 2/4 element
- **0:** Surface-level
- **N/A:** Hiếm; có thể N/A cho keyword không có "mechanism" (e.g., naming convention)

---

## 10. Axis 9, Cách kỹ sư vận hành thành thạo (Engineer master-operation)

### 10.1. Definition

Operational skill engineer cần để work với keyword: read it, modify it, observe it. Khác axis 11 ở chỗ axis 9 là "skill profile" (gì cần biết), axis 11 là "step-by-step workflow" (làm theo thứ tự).

### 10.2. Pass criteria

- Skill list (read / modify / observe / debug)
- CLI command tied to skill
- Decision tree khi nào dùng skill nào

### 10.3. Pass example

```
Vận hành thành thạo ct_state cần 4 skill:

(1) Read: hiểu ct_state flag combination trong flow rule (`ct_state=+trk+new`,
    `ct_state=+trk+est+rpl`, etc.). Reference table 9.24 §ct_state flag matrix.
(2) Modify: viết flow rule có ct_state match (`ovs-ofctl add-flow br0
    'priority=200,ct_state=+trk+est,actions=NORMAL'`).
(3) Observe: 3 cách:
    - `ovs-appctl dpif/dump-flows | grep ct_state` xem flow rule đã install
    - `ovs-appctl dpctl/dump-conntrack zone=N` xem conntrack table state
    - `ofproto/trace 'in_port=1,tcp,ct_state=...'` simulate packet
(4) Debug: khi suspect stateful drop, diagnostic flow:
    Step 1: check conntrack zone → có collision không
    Step 2: check ct_state flag matching → rule có catch packet không
    Step 3: check NAT collision → nat() commit có conflict không

Decision: nếu drop happens trên packet đầu tiên, suspect axis 1 (zone). Nếu
drop happens trên packet phản hồi, suspect axis 2 (ct_state +est rule missing).
```

### 10.4. Auto-detect signal

- Regex: skill verb "read"/"modify"/"observe"/"debug" trong context keyword
- Anatomy template / GE pointer

### 10.5. Manual review when

- Command list without context
- Skill mentioned nhưng decision tree absent

### 10.6. Score

- **1.0:** Skill list + CLI + decision tree
- **0.5:** Skill list nhưng không decision tree
- **0:** Command dump only
- **N/A:** Hiếm; có thể N/A cho concept không vận hành (e.g., abstract architectural concept)

---

## 11. Axis 10, Phân loại taxonomy (Classification)

### 11.1. Definition

What category keyword belongs trong taxonomy structured.

### 11.2. Categories

- **CLI tool:** standalone command (e.g., `ovs-vsctl`, `ovn-trace`)
- **CLI subcommand:** subcommand của tool (e.g., `set-controller`, `lflow-list`)
- **CLI option/flag:** flag của tool/subcommand (e.g., `--no-wait`, `-u`)
- **OVSDB table:** schema table (e.g., `Bridge`, `Port`, `SSL`)
- **OVSDB column:** column within table (e.g., `Bridge.protocols`)
- **OF match field:** OXM/NXM field (e.g., `ct_state`, `tp_dst`)
- **OF action:** OF action (e.g., `output`, `ct()`)
- **OF instruction:** OF instruction (e.g., `Apply-Actions`, `Goto-Table`)
- **OF message:** OFPT_* message type (e.g., `OFPT_FLOW_MOD`)
- **Daemon/process:** background daemon (e.g., `ovs-vswitchd`, `ovn-northd`)
- **Concept:** abstract concept (e.g., `multi-table pipeline`, `Geneve TLV`)
- **Pipeline stage:** OVN logical pipeline stage (e.g., `LS_IN_ACL`)
- **Register/flag:** reg, REGBIT, MLF (e.g., `REGBIT_PORT_SEC_DROP`)
- **Schema convention:** naming convention (e.g., `OFTABLE_LOG_INGRESS`)

### 11.3. Pass criteria

- Explicit category label

### 11.4. Pass example

```
ovs-vsctl set-controller — Loại: CLI subcommand. Parent tool: ovs-vsctl. Type
of operation: state-changing (write OVSDB Bridge.controller column).
Idempotency: yes (set same URL multiple times = no effect). Atomicity: single
OVSDB transaction.
```

### 11.5. Auto-detect signal

- Header tag "Loại:"/"Type:"/"Category:" near keyword
- Section heading taxonomy

### 11.6. Manual review when

- Category implicit không stated
- Multi-category keyword (e.g., `ct` là action + match field family)

### 11.7. Score

- **1.0:** Category explicit
- **0.5:** Category implicit (placement suggests but not stated)
- **0:** Absent
- **N/A:** Hiếm

---

## 12. Axis 11, Cách dùng thành thạo + workflow (Proficient usage workflow)

### 12.1. Definition

Step-by-step workflow + best practice + idiom cho dùng keyword in production.

### 12.2. Pass criteria

- Numbered workflow steps (1, 2, 3, ...)
- Verification step at each phase
- Best practice notes
- Common idiom OR anti-pattern

### 12.3. Pass example

```
Workflow chuẩn cho `ovs-vsctl set-controller`:

Step 1. Verify connectivity: `nc -zv controller-host 6653` confirm reachable
Step 2. Set controller: `ovs-vsctl set-controller br0 tcp:host:6653`
Step 3. Verify config write: `ovs-vsctl get-controller br0` should return URL
Step 4. Verify connection up: `ovs-vsctl get Controller br0 is_connected` = "true"
Step 5. Verify flows pushed: `ovs-ofctl dump-flows br0` see initial rules

Best practice:
- Always TLS in production: use `ssl:` not `tcp:` URL prefix
- Set `ovs-vsctl set Controller br0 connection-mode=secure` để tránh fail-mode
  fallback chuyển sang standalone (gây security violation)
- Set inactivity probe phù hợp với network latency: `ovs-vsctl set Controller
  br0 inactivity_probe=10000` cho cross-region (default 5000 quá nhạy)

Anti-pattern:
- KHÔNG set `tcp:` controller trên production exposing OF socket public
- KHÔNG để fail_mode=standalone trong fleet multi-bridge sản xuất
```

### 12.4. Auto-detect signal

- Numbered list pattern
- "Step 1/2/3" trong context keyword
- "Best practice" / "anti-pattern" / "idiom"

### 12.5. Manual review when

- Workflow exists nhưng incomplete (no verification step)
- Workflow described cho concept lân cận

### 12.6. Score

- **1.0:** Steps + verification + best practice + idiom/anti-pattern
- **0.5:** Steps only
- **0:** Command syntax only
- **N/A:** Có thể N/A cho concept không có "workflow" (abstract concept)

---

## 13. Axis 12, Khi xảy ra sự cố cần nhớ keyword này (Troubleshooting context)

### 13.1. Definition

Symptom → keyword mapping; reverse lookup cho operator on-call: nhìn signal → biết keyword nào relevant.

### 13.2. Pass criteria

- Symptom list (1+) trỏ tới keyword
- Diagnostic flow để confirm keyword involvement
- Cross-link tới incident response Phần (20.x family)

### 13.3. Pass example

```
Khi nào on-call engineer phải nhớ ct_state:

Symptom A: Stateful firewall drop traffic mà rule allow rõ ràng
  → Suspect ct_state matching mismatch
  → Diagnostic: `ofproto/trace 'in_port=N,tcp,...'` xem ct_state value sau ct()
  → Confirm: nếu trace shows `ct_state=+trk+inv` thay vì `+trk+est`, có conntrack
    state corruption (zone collision hoặc table overflow)

Symptom B: Connection only 1 direction passes, reply dropped
  → Suspect missing `+est` rule path
  → Diagnostic: `ovs-ofctl dump-flows br0 | grep ct_state` count rule per state
  → Confirm: nếu chỉ có rule cho `+new` không có `+est`, reply path drop

Symptom C: New connection blocked intermittent
  → Suspect conntrack table near max
  → Diagnostic: `cat /proc/sys/net/netfilter/nf_conntrack_count`
    `cat /proc/sys/net/netfilter/nf_conntrack_max` ratio > 90% = exhaustion
  → Confirm: increase nf_conntrack_max OR tune timeout

Cross-link: 9.24 §troubleshooting, 20.0 §incident response decision tree, 20.2
§ovn-trace ct_state debug.
```

### 13.4. Auto-detect signal

- Regex: "Khi nào" / "When does" / "Symptom" / "sự cố" / "failure mode" near keyword
- Cross-link to 20.x file

### 13.5. Manual review when

- Keyword mentioned trong troubleshoot file but not as primary
- Generic troubleshoot không tied to keyword

### 13.6. Score

- **1.0:** Symptom + diagnostic + confirm step + cross-link
- **0.5:** Symptom only
- **0:** Absent
- **N/A:** Có thể N/A cho concept không có troubleshoot context (pure architectural concept)

---

## 14. Axis 13, Liên quan mật thiết tới thành phần nào (Tight coupling cross-link)

### 14.1. Definition

Identify keyword tightly coupled, nghĩa là changes propagate hoặc semantic dependence. Khác cross-link bình thường ở chỗ "tightly coupled" implies "đổi 1 ảnh hưởng cái kia"; loose cross-link chỉ là "related topic".

### 14.2. Pass criteria

- 3+ tightly coupled keyword/Phần listed
- Coupling rationale stated (vì sao tight)

### 14.3. Pass example

```
Tightly coupled với ct_state:

- ct_zone: zone partition affects ct_state semantics (per-zone state machine)
- ct_mark / ct_label: downstream tagging populated when ct() commits, ct_state
  match condition often combined với ct_mark
- nat() action: NAT shares conntrack entry với ct(); ct_state +est for NAT'd
  flow requires nat() awareness
- nf_conntrack_max sysctl: conntrack table size limit; exhaustion → ct_state
  cho new connection trở thành +inv
- Upcall: first packet through ct() triggers conntrack lookup userspace → upcall
  cost; high-rate ct() = high upcall load

Loose related (cross-link, not tightly coupled):
- iptables: separate stack, Linux native
- VXLAN/Geneve: tunnel encap, not directly conntrack
```

### 14.4. Auto-detect signal

- Cross-reference section pattern
- "Tightly coupled" / "depends on" / "phụ thuộc" terminology

### 14.5. Manual review when

- Cross-link list exists nhưng không phân biệt tight vs loose
- All cross-link as same level

### 14.6. Score

- **1.0:** 3+ coupled + rationale + tight-vs-loose distinction
- **0.5:** 3+ coupled but no rationale
- **0:** Random cross-link
- **N/A:** Hiếm

---

## 15. Axis 14, Sự khác biệt phiên bản (Version drift)

### 15.1. Definition

Behavior or syntax differences across OF/OVS/OVN versions cho keyword.

### 15.2. Pass criteria

- 1+ version note callout liệt kê pre/post diff
- Affected version specific
- Behavior change OR syntax change OR removal

### 15.3. Pass example

```
> **Version drift ct_state:**
> - OVS 2.4: bit field expanded, added `+rpl` flag (reply seen)
> - OVS 2.6: zone partition for inter-bridge ct (cùng zone share state across
>   br1, br-int)
> - OVS 2.8: added `ct_nw_proto`, `ct_tp_src/dst` extension match
> - OF 1.6 standardize NXM_NX_CT_STATE → OXM_OF_CT_STATE
> - OVN 22.03: deprecated `+rel` in favor of `+est` (rel becoming subset of est)
>
> Curriculum baseline: OVS v2.17.9 + OVN v22.03.8. Production có thể chạy
> OVS 3.3 hoặc OVN 24.03; check version trước khi áp flag mới.
```

### 15.4. Auto-detect signal

- Regex: "version note" / "OVS X.Y" / "OF X.Y+" pattern
- Callout block `> **Version note:**`

### 15.5. Manual review when

- Version mentioned nhưng only single version
- Version drift across OVS only, OF/OVN missing

### 15.6. Score

- **1.0:** Multi-version drift documented
- **0.5:** Single version mention
- **0:** No version awareness
- **N/A:** Có thể N/A cho keyword không có version drift (e.g., concept stable across versions)

---

## 16. Axis 15, Verification: làm sao quan sát keyword đang hoạt động (Observability verification)

### 16.1. Definition

Specific CLI/log/file/table that exposes keyword runtime state.

### 16.2. Pass criteria

- Specific command (not generic "check logs")
- Output sample (1-3 dòng)
- What output reveals about keyword

### 16.3. Pass example

```
Verify ct_state runtime:

Method 1, dpctl/dump-flows
  $ ovs-appctl dpctl/dump-flows | head -3
  ufid:abc..., recirc_id(0),in_port(2),...,actions:ct(zone=42),...
  Reveals: flow rule có ct() action; check actions field

Method 2, dpctl/dump-conntrack
  $ ovs-appctl dpctl/dump-conntrack zone=42
  tcp,orig=(src=10.0.0.5,dst=10.0.0.10,sport=4001,dport=80),
       reply=(src=10.0.0.10,dst=10.0.0.5,sport=80,dport=4001),
       protoinfo=(state=ESTABLISHED)
  Reveals: live conntrack entry với state ESTABLISHED, zone=42 partition

Method 3, ofproto/trace
  $ ovs-appctl ofproto/trace br0 'in_port=2,tcp,ct_state=+trk+est,...'
  Final flow: ...,ct_state=0x21,...
  Reveals: simulated ct_state value sau khi pipeline xử lý
```

### 16.4. Auto-detect signal

- Specific CLI command + grep pattern + sample output
- Command output block với keyword visible

### 16.5. Manual review when

- Command exists nhưng không verify keyword
- "Check logs" generic

### 16.6. Score

- **1.0:** Specific command + sample output + interpretation
- **0.5:** Command only without sample
- **0:** Generic/absent
- **N/A:** Có thể N/A cho concept không có observability surface (abstract design pattern)

---

## 17. Axis 16, Source code anchor (Source code reference)

### 17.1. Definition

file:function:commit pointer to upstream OVS/OVN/Linux source code, verified per Rule 14.

### 17.2. Pass criteria

- 1+ verified file path
- Function name within file
- Optional: commit SHA cho recent changes
- Annotation cho version drift nếu file moved/renamed

### 17.3. Pass example

```
Source code anchor ct_state (OVS v2.17.9):

- `lib/ofp-actions.c` `parse_ct()` parser của ct() action; populate
  ofpact_conntrack struct
- `lib/conntrack.c` `conntrack_execute()` runtime execution sau ct() invoke
- `include/openvswitch/ofp-actions.h` ofpact_conntrack struct definition
  (zone, mark, labels, alg fields)
- `lib/odp-execute.c` `odp_execute_actions()` calls into conntrack_execute
  for kernel datapath path

Linux kernel side (5.15):
- `net/netfilter/nf_conntrack_core.c` `nf_conntrack_in()` table lookup
- `include/uapi/linux/netfilter/nf_conntrack_common.h` IPS_* state flags

Cross-link Rule 14: source citation table trong 9.24 §source code citation.
```

### 17.4. Auto-detect signal

- Regex: `[a-z_/-]+\.[ch]\b` filename pattern
- Function name pattern: `[a-z_]+\(`
- Cross-link to upstream commit URL

### 17.5. Manual review when

- File path mentioned but unverified (Rule 14.3 requires version baseline)
- Generic "in OVS source"

### 17.6. Score

- **1.0:** Verified file + function + version annotation
- **0.5:** File only without function
- **0:** Vague mention
- **N/A:** Có thể N/A cho concept (e.g., "multi-table pipeline" abstract concept; no specific file)

---

## 18. Axis 17, Real-world incident anatomy (Production case study)

### 18.1. Definition

At least 1 production case study where keyword was root cause OR key debug step.

### 18.2. Pass criteria

- Specific incident (date, system, identifier)
- Symptom description
- Investigation flow
- Root cause analysis
- Fix applied

### 18.3. Pass example

```
Production case (FDP-620, 2024-Q3, OVN multi-tenant cluster):

Symptom: East-west traffic between VMs trên cùng Logical_Switch intermittent
drop ~5% rate. Service A → Service B request timeout 5%.

Investigation:
  Step 1: ovn-trace `inport==lsp-A,outport==lsp-B,...` shows pipeline pass OK
  Step 2: ofproto/trace br-int packet → trace stuck ở ct() table 12
  Step 3: dpctl/dump-conntrack zone=N shows entry với state INVALID

Root cause: ct_zone collision. Northd compile chose zone=42 cho both LS-A
internal traffic AND LR-transit-12 forwarding, resulting in shared conntrack
table có entries từ 2 contexts khác. Một số packet match wrong entry → state
=INVALID.

Fix: OVN 24.03 introduced zone-id externally configurable per LS. Set
LS-A.options:zone-id=100, LR-transit-12.options:zone-id=200. Cluster upgrade
+ config reapply. Drop rate 0% sau fix.

Reference: ovn issue tracker FDP-620, fix commit ovn 24.03 abc1234.
Cross-link: Phần 19.0 (forensic case study).
```

### 18.4. Auto-detect signal

- Case study terminology + specific identifier (incident ID, date, system)
- "Production case" / "real incident" / "FDP-XXX" / case study heading

### 18.5. Manual review when

- Hypothetical scenario disguised as case
- Incident exists nhưng không tied to specific keyword

### 18.6. Score

- **1.0:** Full anatomy (symptom + investigation + root cause + fix)
- **0.5:** Symptom + root cause only
- **0:** Hypothetical
- **N/A:** Có thể N/A cho keyword chưa có known incident (rare in OVS family but possible cho niche option)

---

## 19. Axis 18, Lab exercise (Synthetic hands-on)

### 19.1. Definition

Reproducible lab setup engineer có thể run để play với keyword.

### 19.2. Pass criteria

- Lab setup steps (Mininet topology, OVS config)
- Verification commands
- Expected output
- Variations (try different params)

### 19.3. Pass example

```
Lab synthetic ct_state stateful firewall:

Setup:
  $ sudo mn --topo single,3 --switch ovsk --controller=remote,ip=127.0.0.1
  $ ovs-ofctl add-flow s1 'priority=100,ip,ct_state=-trk,actions=ct(table=0)'
  $ ovs-ofctl add-flow s1 'priority=200,ip,ct_state=+trk+new,in_port=1,
                                   actions=ct(commit),NORMAL'
  $ ovs-ofctl add-flow s1 'priority=200,ip,ct_state=+trk+est,actions=NORMAL'
  $ ovs-ofctl add-flow s1 'priority=10,actions=drop'

Verify:
  Step 1: h1 ping h2 first packet
    > h1 ping -c 1 h2
    1 packet transmitted, 1 received  (PASS)
  
  Step 2: dump conntrack
    $ ovs-appctl dpctl/dump-conntrack
    icmp,orig=(src=10.0.0.1,dst=10.0.0.2,id=...),reply=(...),
         protoinfo=(state=ESTABLISHED)
  
  Step 3: dump-flows shows usage
    $ ovs-ofctl dump-flows s1 | grep ct_state
    cookie=0x0, duration=10s, n_packets=2, ct_state=+trk+est, actions=NORMAL

Variations to try:
  (a) Change priority để test order matter
  (b) Add zone partition: `ct(zone=42)` xem dpctl shows zone=42 entry
  (c) Try invalid packet (e.g., TCP SYN-ACK without prior SYN) xem +inv flag
  (d) Saturate conntrack table (1000 short-lived ping rapid) xem +new transition
```

### 19.4. Auto-detect signal

- GE / Lab pattern
- Mininet / lab synthetic terminology
- Step-by-step + verification + expected output

### 19.5. Manual review when

- GE exists nhưng không exercise keyword này
- Setup incomplete (missing controller, topology)

### 19.6. Score

- **1.0:** Setup + verify + expected output + variations
- **0.5:** Setup + verify only
- **0:** "Try it" generic
- **N/A:** Có thể N/A cho keyword không có lab setup tự nhiên (e.g., specific OVSDB column rarely exercised standalone)

---

## 20. Axis 19, Failure mode + diagnostic signal (Failure + diagnostic)

### 20.1. Definition

How keyword fails OR appears broken; diagnostic signal để confirm.

### 20.2. Pass criteria

- 2+ failure modes listed
- Diagnostic signal cho mỗi mode (log line, metric, command output)
- Recovery action

### 20.3. Pass example

```
Failure modes ct_state:

Mode A, Zone exhaustion
  Diagnostic: ovs-vswitchd.log "ct_zone limit reached" hoặc sysctl
              `nf_conntrack_count > nf_conntrack_max` ratio > 95%
  Recovery: increase nf_conntrack_max (`sysctl -w net.netfilter.nf_conntrack_max=1048576`)
            hoặc tune tcp_timeout_established (default 432000s = 5 days, quá lâu)

Mode B, State stuck at +trk-... (no positive flag set)
  Diagnostic: revalidator log "ct rule mismatch" hoặc dpctl/dump-flows shows
              entry với ct_state value mismatch flow rule expectation
  Recovery: ovs-appctl revalidator/wait sleep until revalidator catch up;
            nếu persistent → ovs-vswitchd restart (last resort)

Mode C, NAT collision causing +inv state
  Diagnostic: conntrack -L shows duplicate orig+reply tuple với cùng zone
  Recovery: identify NAT source, disable conflict, OR partition zone properly

Mode D, ALG (Application Layer Gateway) mismatch
  Diagnostic: TCP three-way handshake passes nhưng FTP data connection drop;
              `dpctl/dump-conntrack | grep helper` shows expected vs actual
  Recovery: adjust ct() helper option (`ct(commit, helper=ftp)`) hoặc disable
            ALG nếu không cần
```

### 20.4. Auto-detect signal

- "Failure mode" / "Hiểu sai" / "Anti-pattern" near keyword
- "Recovery" / "Fix" / "Resolve" terminology

### 20.5. Manual review when

- Failure mentioned nhưng signal absent
- Generic troubleshooting không tied to specific failure mode

### 20.6. Score

- **1.0:** 2+ modes + diagnostic + recovery
- **0.5:** 1 mode only
- **0:** Generic
- **N/A:** Có thể N/A cho keyword không có failure mode (e.g., naming convention)

---

## 21. Axis 20, So sánh cross-domain (Cross-domain analogue)

### 21.1. Definition

Compare to equivalent in Linux native / iptables / Cisco / NSX / other vendor.

### 21.2. Pass criteria

- 1+ cross-domain comparison
- Similarity statement
- Difference statement (what makes OVS/OF/OVN unique)

### 21.3. Pass example

```
Cross-domain ct_state ≈ iptables `-m state --state` extension:

Similarity:
- Cả hai consume nf_conntrack table state
- Cả hai expose 4 state cơ bản: NEW, ESTABLISHED, RELATED, INVALID

Difference:
- iptables: state expression bound to single chain hook (filter/nat/mangle);
  cannot reuse state value across chains without re-evaluation
- ct_state: OF match field, accessible bất cứ table nào trong pipeline qua
  read register; có thể be combined với arbitrary other field trong same match
- iptables: state populated implicit khi packet hit -m state rule
- ct_state: state populated explicit via ct() action call; pipeline có control
  over when conntrack lookup happens

Cisco ASA equivalent: `inspect tcp` stateful inspection, similar state machine
nhưng integrated với inspect engine. Khác OVS ct_state ở chỗ ASA không expose
state machine cho rule mở rộng (closed semantic).

NSX-T equivalent: distributed firewall stateful rule, internally cũng dùng
conntrack-style table per host, expose state qua NSX policy API thay vì OF
match field directly.
```

### 21.4. Auto-detect signal

- Comparison terminology "iptables" / "Cisco" / "NSX" / "≈" / "tương tự"
- Section heading "So sánh" / "Cross-domain" / "Compare"

### 21.5. Manual review when

- Comparison mentioned but only superficial
- Comparison cho concept không phải keyword cụ thể

### 21.6. Score

- **1.0:** Comparison + similarity + difference
- **0.5:** Comparison statement only without difference
- **0:** OVS-only treatment
- **N/A:** Có thể N/A cho keyword không có cross-domain analogue (e.g., OVN-specific concept như Logical_Flow không có direct analogue)

---

## 22. Threshold + Scoring Rules

### 22.1. Score per axis

| Score | Meaning |
|-------|---------|
| 1.0 | Pass clearly, all criteria met |
| 0.5 | Partial pass, some criteria met |
| 0 | Fail, criteria absent |
| N/A | Not applicable (keyword không có axis này naturally) |

### 22.2. Threshold tier

| Tier | Score range | Target keyword count | Application |
|------|-------------|----------------------|-------------|
| **DEEP-20** | 18.0 to 20.0 | ~50 cornerstone | Bắt buộc 100% trong Phase H |
| **DEEP-15** | 15.0 to 17.5 | ~100 medium | Target 95% trong Phase H |
| **PARTIAL-10** | 10.0 to 14.5 | ~170 peripheral | Target 90% trong Phase H |
| **REFERENCE-5** | 5.0 to 9.5 | (work in progress) | Phase G tackle these |
| **PLACEHOLDER** | < 5.0 | (mostly unaddressed) | Phase G priority focus |

### 22.3. Tier classification rule

- **Cornerstone:** keyword với architectural importance "tier 1" (axis 7 score = 1.0 với "trụ cột" / "must know" justification). Examples: megaflow, ct_state, ovn-controller, Logical_Flow, OFPT_FLOW_MOD.
- **Medium:** keyword với importance "tier 2" (axis 7 score ≥ 0.5 with explicit medium ranking). Examples: xreg, learn action, OVN ACL, Service_Monitor.
- **Peripheral:** keyword importance "tier 3" hoặc niche. Examples: ovs-monitor-ipsec, OFPMP_QUEUE_STATS, ovn-nbctl --shuffle-remotes.

Tier classification done qua manual review trong Phase E triage, document trong scorecard.

---

## 23. N/A Handling

### 23.1. When axis is N/A

Một số axis có thể naturally N/A cho keyword:

- Axis 17 (incident anatomy): keyword chưa có known production incident (rare cho OVS family core, common cho niche options)
- Axis 18 (lab exercise): keyword không có natural standalone lab setup (e.g., schema convention)
- Axis 20 (cross-domain): keyword OVN-specific không có analogue (Logical_Flow, REGBIT_*)
- Axis 9 (engineer master-operation): pure abstract concept không vận hành (generic concept)

### 23.2. Normalization

Score normalize qua denominator effective:

```
effective_denominator = 20 - count_NA
normalized_score = sum_score / effective_denominator
```

### 23.3. Tier with N/A

Threshold adjusted proportionally:

- DEEP-20 effective: ≥ 90% (e.g., 16.2/18 nếu 2 N/A)
- DEEP-15 effective: ≥ 75% (e.g., 13.5/18 nếu 2 N/A)
- PARTIAL-10 effective: ≥ 50%

### 23.4. N/A justification

Mỗi N/A MUST có justification trong scorecard. Auto-classify N/A NOT allowed; manual review.

---

## 24. Auto-detection Signal Summary

| Axis | Difficulty | Primary signal | Confidence threshold |
|------|------------|---------------|---------------------|
| 1 Concept | Easy | Definition pattern + Bucket axis | 90% |
| 2 History | Medium | Year + version + people | 70% |
| 3 Placement | Easy | Layer keywords | 90% |
| 4 Role | Medium | Purpose axis + role verb | 75% |
| 5 Motivation | Hard | "vì sao"/"motivation" near keyword | 60% |
| 6 Problem | Medium | Problem-solution pattern | 75% |
| 7 Importance | Hard | "trụ cột"/"must know" | 50% |
| 8 Mechanism | Medium | Data structure + algorithm | 70% |
| 9 Engineer-op | Medium | Skill verb + decision tree | 75% |
| 10 Taxonomy | Easy | Header tag | 90% |
| 11 Workflow | Medium | Numbered steps | 80% |
| 12 Troubleshoot | Hard | Symptom mapping | 60% |
| 13 Coupling | Medium | Cross-ref + tight terminology | 70% |
| 14 Version drift | Easy | Version note callout | 90% |
| 15 Verification | Easy | CLI command + sample output | 85% |
| 16 Source code | Easy | File path pattern | 90% |
| 17 Incident | Hard | Case study identifier | 50% |
| 18 Lab | Medium | GE pattern | 75% |
| 19 Failure | Medium | Failure mode + recovery | 75% |
| 20 Cross-domain | Medium | Comparison terminology | 70% |

Average confidence: ~75%. Manual review expected for ~25% of axis-keyword cells.

---

## 25. Manual Review Process

### 25.1. When manual review triggered

- Auto-detect confidence < threshold per axis
- N/A determination (mandatory manual)
- Tier classification (mandatory manual)
- Conflict between auto-detect signals (e.g., axis 8 mechanism present in 3 file but contradict)
- New keyword addition (REF expand)

### 25.2. Manual review workflow

```
1. Read scorecard auto-detect output
2. For each axis flagged manual:
   a. Read relevant curriculum file(s) per evidence pointer
   b. Apply pass criteria from rubric Section corresponding axis
   c. Score 0/0.5/1/N/A
   d. Document evidence: file:line citation OR justification
3. Update scorecard with manual override
4. Recompute total + tier
5. Commit scorecard update
```

### 25.3. Reviewer

Phase D: Claude does initial manual review, Phase D acceptance gate = user approve script accuracy ≥ 85%.

Phase G: Claude does manual review per cohort, user spot-check sample 5-10% per cohort batch.

Phase H: User personally spot-check 30+ keyword across all tier để verify final scorecard.

---

## 26. Application Workflow

### 26.1. Phase D (initial scorecard build)

```
For each keyword in REF (320+):
  1. Run audit script per_keyword_rubric_audit.py
  2. Get auto-detect scorecard
  3. Manual review flagged axis
  4. Tier classify (cornerstone/medium/peripheral)
  5. Commit scorecard entry
End for
Output: memory/sdn/keyword-rubric-scorecard.md
```

### 26.2. Phase G (cohort batch fill)

```
For each cohort (Phase E priority order):
  For each keyword in cohort:
    1. Read scorecard, identify axes < 1.0
    2. For each axis < 1.0:
       a. Research (REF + upstream + curriculum)
       b. Write content fill axis
       c. Cross-link
    3. Re-run audit script
    4. Verify scorecard score increased
  End for
  Cohort acceptance: all keyword reach minimum tier threshold
  Commit cohort batch + scorecard update
End for
```

### 26.3. Phase H (final validation)

```
1. Re-run audit script full
2. Confirm:
   - Cornerstone (50): 100% at DEEP-20
   - Medium (100): ≥ 95% at DEEP-15
   - Peripheral (170): ≥ 90% at PARTIAL-10
3. User spot-check 30+ random keyword
4. User written sign-off
5. Tag v4.0-MasteryComplete
```

---

## 27. Worked Example: megaflow Scoring

> Demonstrate rubric application với 1 cornerstone keyword đại diện. Score dựa trên curriculum hiện tại 9.2 + 9.26 (estimate, sẽ verify Phase D).

| Axis | Score | Evidence | Notes |
|------|-------|----------|-------|
| 1 Concept | 1.0 | 9.2:line 30+ "Megaflow là wildcarded flow entry trong kernel datapath, tương đương 1 cluster microflow" | Pass |
| 2 History | 1.0 | 9.2:line 50+ "OVS 2.4 (2014) introduce megaflow để address flow explosion" | Pass |
| 3 Placement | 1.0 | 9.2:line 30+ "Kernel datapath classifier" | Pass |
| 4 Role | 1.0 | 9.2 §megaflow purpose: scaling fast-path | Pass |
| 5 Motivation | 1.0 | 9.2:line 50+ pre-megaflow pain explicit | Pass |
| 6 Problem | 1.0 | 9.2 problem-solution pattern | Pass |
| 7 Importance | 0.5 | 9.2 implies tier 1 nhưng không state explicit | Partial; cần tier 1 justification |
| 8 Mechanism | 1.0 | 9.2:line 100-300 TSS + mask consolidation deep | Pass |
| 9 Engineer-op | 0.5 | 9.4 + 9.11 có command nhưng decision tree mơ hồ cho megaflow specifically | Partial |
| 10 Taxonomy | 0.5 | "kernel datapath concept" implied, không header tag | Partial; cần add taxonomy tag |
| 11 Workflow | 0.5 | 9.4 có workflow read megaflow nhưng không "modify" / "tune" workflow | Partial |
| 12 Troubleshoot | 1.0 | 9.26 §revalidator storm extensive, axis 12 explicit | Pass |
| 13 Coupling | 1.0 | 9.2 cross-link revalidator/upcall/UFID/microflow | Pass |
| 14 Version drift | 0.5 | OVS 2.4 introduce mention, nhưng không document evolution since | Partial |
| 15 Verification | 1.0 | 9.4 dpctl/dump-flows + ofproto/trace pattern | Pass |
| 16 Source code | 1.0 | 9.2 §source code citation lib/dpif-netdev.c | Pass |
| 17 Incident | 1.0 | 9.26 production case study (revalidator storm) extensively | Pass |
| 18 Lab | 1.0 | 9.21 Mininet lab + 9.4 GE | Pass |
| 19 Failure | 1.0 | 9.26 §failure modes 4 modes + signal | Pass |
| 20 Cross-domain | 0 | Không có comparison với Linux bridge / Cisco classifier | Fail |
| **Total** | **15.5/20** | | |
| **Tier** | DEEP-15 | | Cornerstone target DEEP-20 (≥ 18) → cần fill axis 7 + 9 + 10 + 11 + 14 + 20 để đạt |

**Phase G action cho megaflow:**

1. Axis 7: add explicit tier 1 importance statement với justification
2. Axis 9: add decision tree khi nào tune megaflow vs investigate revalidator
3. Axis 10: add taxonomy tag header "Loại: kernel datapath flow entry abstraction"
4. Axis 11: add modify/tune workflow (e.g., disable wildcard via OF rule, force microflow installation)
5. Axis 14: document version drift OVS 2.4 → 3.3 (e.g., SMC addition 2.6, depthwise lookup optimization 2.9)
6. Axis 20: cross-domain comparison with Linux bridge MAC learning (similar wildcard concept) hoặc Cisco TCAM (different storage but similar generalization)

Estimated effort fill: 2-3 giờ research + write.

---

## 28. References

- **Plan v3.7:** `plans/sdn/v3.7-reckoning-and-mastery.md`
- **Governance principles:** `memory/sdn/governance-principles.md` (GP-1 đến GP-5 binding)
- **REF source-of-truth:** `sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md`
- **CHANGELOG reckoning:** `CHANGELOG.md` section "Reckoning 2026-04-26"
- **Future scorecard (Phase D):** `memory/sdn/keyword-rubric-scorecard.md`
- **Future audit script (Phase D):** `scripts/per_keyword_rubric_audit.py`
- **5-axis Anatomy precedent:** Bucket | Context | Purpose | Activity | Mechanism (used in 0.3 master index, ~100 keyword Anatomy template)

---

## 29. Amendment Log

| Version | Date | Change | Approval |
|---------|------|--------|----------|
| v1.0 | 2026-04-26 | Initial Phase B v3.7 deliverable. 20 axis (13 user + 7 Claude) + threshold tier + scoring rule + worked example megaflow | Pending Phase B end gate, user sign-off needed |

---

> **Đơn giản hoá rubric:** 20 axis (đa diện depth), 4 tier threshold (DEEP-20 / DEEP-15 / PARTIAL-10 / REFERENCE-5), 3 score level (0 / 0.5 / 1) + N/A normalization. Mục tiêu phục vụ Phase D auto-audit + Phase G content writing + Phase H final validation. Rubric measures depth không breadth (per GP-5).
