# English Style Guide for the SDN Training Program

> **Status:** Active. Authoritative for all newly written or modified content in CLAUDE.md, `sdn-onboard/*.md`, and `haproxy-onboard/*.md` (per CLAUDE.md Rule 17).
> **Adopted:** 2026-04-28 (plan v3.9.1 Phase Q9, supersedes the Vietnamese-prose policy of retired Rule 11).
> **Audience for the curriculum:** Vietnamese network engineers with intermediate to upper-intermediate English reading proficiency (CEFR B2 to C1).
> **Authority:** Plan v3.9.1 §8 addendum (curriculum-wide English language migration).

This style guide defines how to write English prose in this repository so that a Vietnamese network engineer can read it without effort and without dictionary lookups, while still learning the canonical OVS, OVN, and OpenFlow terminology used by upstream documentation.

---

## 1. Audience and reading level

The reader is a Vietnamese network engineer who:

- Works on production OpenStack, OVS, OVN, or related infrastructure.
- Reads upstream OVS and OVN documentation in English regularly.
- Is comfortable with technical vocabulary (`packet`, `flow`, `controller`, `tunnel`, `conntrack`, `classifier`).
- Is less comfortable with idiomatic English, dense compound sentences, Latinate vocabulary, or culture-specific references.
- Wants to internalize concepts, not just memorize procedures.

The style aims for CEFR B2 to C1 reading level: clear, technical, no unnecessary complexity, no over-simplification.

---

## 2. Sentence structure

**Default to short declarative sentences.** Target 15 to 20 words per sentence. Split anything longer.

**One technical idea per sentence.** If a sentence introduces both a concept and a related warning, split into two sentences.

**Avoid stacked subordinate clauses.** A sentence with three nested "which" clauses is hard for a non-native reader.

**Examples:**

| Not recommended | Recommended |
|---|---|
| "The classifier, which uses Tuple Space Search, an algorithm originally proposed by Srinivasan et al. in 1998, partitions rules by mask, allowing constant-time lookup within each partition while remaining linear in the number of unique masks, a tradeoff that works well in practice." | "The classifier uses Tuple Space Search. This algorithm was first published by Srinivasan in 1998. It partitions the rules by their mask. Each partition supports constant-time lookup. The total cost is linear in the number of unique masks. The tradeoff works well in production traffic, where the number of distinct masks stays small." |
| "Upon receipt of an upcall, ovs-vswitchd, having dequeued the message, decodes the packet and, depending on the matched flow rule, installs the corresponding megaflow back into the kernel." | "When `ovs-vswitchd` receives an upcall, it dequeues the message. It then decodes the packet. Based on the matched flow rule, it installs the corresponding megaflow back into the kernel." |

---

## 3. Vocabulary policy

### 3.1. Plain words preferred

Choose the plain word over the Latinate or formal one. The reader will recognize the plain word faster.

| Avoid | Prefer |
|---|---|
| ascertain | check |
| necessitate | need |
| utilize | use |
| commence | start |
| terminate | stop |
| facilitate | make easier |
| remediate | fix |
| in the event that | if |
| with respect to | about |
| in order to | to |
| due to the fact that | because |

### 3.2. No abbreviations

Per user directive (2026-04-28), abbreviations are forbidden in prose. Always write the full form.

| Forbidden | Required |
|---|---|
| e.g. | for example |
| i.e. | that is |
| etc. | and so on, or list the items explicitly |
| vs. | versus |
| spec | specification (in prose; keep `spec` in code, CLI, identifier names) |
| config | configuration (in prose; keep `config` in code, CLI, identifier names) |
| docs | documentation (in prose; keep `docs/` for directory references) |
| info | information |
| repo | repository (in prose; keep `repo` in code, CLI, identifier names) |
| dev | development |

### 3.3. Keep-as-is identifier list (canonical names stay verbatim)

The following categories of words are used as named entities. They are kept verbatim, not translated, not expanded, not abbreviated. This preserves grep-ability and matches upstream documentation.

- **Product, project, organization names:** OpenFlow, OVS, OVN, Open vSwitch, NETCONF, NSX, Nicira, VMware, Linux, Ubuntu, Mininet, Cisco, Broadcom Trident, Stanford, ONF, GitHub, Spamhaus, Prometheus, Arbor Networks, Cloudflare, DigitalOcean, Red Hat, NVIDIA ConnectX-6, Intel E810, Anthropic.
- **International protocols and acronyms used as names:** TCP, UDP, IP, ICMP, SCTP, ARP, DNS, TLS, SSH, HTTP, HTTPS, VLAN, VXLAN, Geneve, BGP, OSPF, BFD, MPLS, NAT, SNAT, DNAT, DDoS, RPC, ECMP, FTP. (These are acronyms by industry consensus, not abbreviations of English words.)
- **CLI tools and flags:** `ovs-ofctl`, `ovs-vsctl`, `ovs-appctl`, `ovs-dpctl`, `ovn-nbctl`, `ovn-sbctl`, `ovn-northd`, `ovn-controller`, `conntrack`, `iptables`, `modprobe`, `sysctl`, `sudo`, `ping`, `iperf`, `tcpdump`, `--dpdk`. Man references such as `ovs-fields(7)`, `ovs-actions(7)`, `ovn-architecture(7)` keep their canonical form.
- **OpenFlow match field and identifier names:** `ct_state`, `ct_zone`, `ct_mark`, `ct_label`, `metadata`, `cookie`, `priority`, `in_port`, `nw_src`, `nw_dst`, `dl_src`, `dl_dst`, `dl_type`, `tp_dst`, `sport`, `dport`, `reg0` through `reg15`, `xreg0` through `xreg7`, OXM, NXM.
- **Action, instruction, and pipeline-stage names:** `goto_table`, `resubmit`, `output`, `normal`, `drop`, `mod_dl_src`, `mod_dl_dst`, `dec_ttl`, `ct()`, `ct(commit)`, `ct_next`, `ct_commit`, `ct_lb`, `ct_clear`, `apply_actions`, `write_actions`, `write_metadata`, `clear_actions`, `Apply-Actions`, `Write-Actions`, `Clear-Actions`, `Write-Metadata`, `Goto-Table`, `allow`, `allow-related`, `reject`, `set_queue`. Action values such as `ct_state=+trk+new` are also kept verbatim.
- **Pipeline stage and table names used as labels:** "Table 0 Classifier", "Table 1 L3 Forwarding", "Ingress ACL", "Egress ACL". These are pipeline stage names, not English prose.
- **Literal state, flag, or protocol values:** `NEW`, `ESTABLISHED`, `RELATED`, `INVALID`, `SYN_SENT`, `SYN_RECV`, `FIN_WAIT`, `TIME_WAIT`, `CLOSE`, `CLOSE_WAIT`, `LAST_ACK`, `UNREPLIED`, `ASSURED`, `[NEW]`, `[UPDATE]`, `[DESTROY]`.
- **Common international networking terms:** SDN, DC, WAN, LAN, DPU, ASIC, NOS, VM, RFC, MAC, VIP, NFV, SR-IOV, SmartNIC, FIB, BUM, DMZ, VPN, L2, L3, L4, five-tuple, three-way handshake, pseudo-state, bitfield, tuple, hairpin, subnet, broadcast, multicast, unicast, datapath, bridge, kernel, userspace, namespace, tenant, multi-tenant, chassis, overlay, underlay, east-west, north-south, fast path, slow path, line-rate, offload, DPDK.
- **OpenFlow and OVS specification concepts used as nouns:** flow, flow entry, flow table, flow rule, pipeline, multi-table pipeline, match field, action set, instruction, controller, stateful, stateless, conntrack, handshake.

When such a name appears in prose, it stays verbatim. Surround it with backticks if it is a literal CLI command or code identifier; leave it as plain text if it is a product or concept name.

This list is the spiritual successor to retired Rule 11 §11.1. It is referenced by Rule 17.

---

## 4. Em-dash forbidden

The em-dash character (Unicode U+2014, the long horizontal dash with the width of approximately one M) is forbidden in CLAUDE.md, in `sdn-onboard/*.md`, in `haproxy-onboard/*.md`, in `memory/*`, in `plans/*`, and in commit messages.

Per user directive (2026-04-28), this is a strict zero-count rule. There is no density target.

The pre-commit hook `scripts/em_dash_check.py` enforces this.

### 4.1. Replacements

| When the original used em-dash for | Use instead |
|---|---|
| A break in the middle of a sentence | A comma |
| A new related thought after a complete sentence | A period and a new sentence |
| Introducing a list or an explanation | A colon |
| An aside or parenthetical thought | Parentheses |
| Setting off three or more enumerated items | A new bulleted list |

### 4.2. Examples

In the table below, the "Original (forbidden)" column describes a sentence pattern in plain words. The forbidden character (U+2014) is not printed in this file because the pre-commit hook would reject it. Reading this guide, you should imagine the long horizontal dash that would appear between the words.

| Original pattern (forbidden) | Recommended replacement |
|---|---|
| Sentence break using a long dash, as in "The flow installs to the kernel `[U+2014]` but only after the userspace classifier matches." | "The flow installs to the kernel, but only after the userspace classifier matches." |
| Long dash before an enumerated list, as in "Three components participate `[U+2014]` kernel datapath, userspace `ovs-vswitchd`, and OVSDB." | "Three components participate: kernel datapath, userspace `ovs-vswitchd`, and OVSDB." |
| Two long dashes setting off a parenthetical phrase, as in "DPDK netdev `[U+2014]` a userspace packet I/O framework `[U+2014]` is out of scope." | "DPDK netdev (a userspace packet I/O framework) is out of scope." |
| Repeated long dashes used as separators between four items, as in "TSS handles wildcard matching `[U+2014]` exact match `[U+2014]` range match `[U+2014]` prefix match." | "TSS handles four kinds of matching: wildcard, exact, range, and prefix." |

### 4.3. Tooling note

The en-dash (U+2013, slightly shorter than em-dash) is allowed for numeric ranges in tables (`OVS 2.5–2.6`). The hyphen (U+002D) is allowed everywhere. Only U+2014 is forbidden.

---

## 5. Punctuation

- **Oxford comma always.** Write "a, b, and c", not "a, b and c".
- **One space after sentence-ending periods.** No double-space.
- **Straight quotes only.** Use `"` and `'`, not `"`, `"`, `'`, or `'`. The pre-commit hook will be extended in a future plan to flag curly quotes.
- **Inline code uses backticks.** `ovs-vsctl`, `MFF_CT_ZONE`, `lib/classifier.c`.
- **Block code uses fenced blocks** with an explicit language tag where the highlighter benefits from it: ```` ```bash ````, ```` ```c ````, ```` ```json ````, ```` ```diff ````.
- **Periods inside or outside quotes:** follow logical punctuation (the period is inside the quote only when it belongs to the quoted text). This matches British English convention and matches upstream OVS documentation style.

---

## 6. Voice and tone

- **Active voice preferred.** "The kernel forwards the packet" beats "The packet is forwarded by the kernel".
- **Second person ("you") when speaking to the engineer.** "You can verify with `ovs-appctl coverage/show`."
- **First person plural ("we") rarely.** Only when describing a shared design choice that the curriculum makes deliberately. "We choose to use TSS rather than a single hash table because production traffic has many distinct masks."
- **Never first person singular.** No "I" or "me" in the curriculum. The curriculum is a shared resource, not a personal voice.
- **Imperative for procedural steps.** "Run `ovs-vsctl show`. Verify that bridge `br-int` exists. If it is missing, see the troubleshooting section."
- **Past tense for incident anatomy.** When describing a real production incident, use past tense for the events ("The cluster lost quorum", "The operator ran"). Use present tense for the analysis ("The root cause is", "The fix is").

---

## 7. Pedagogy preserved (the why-before-what doctrine)

Per CLAUDE.md SECOND NORTH STAR, the curriculum is a teaching tool. English translation must not flatten dense Vietnamese reasoning into shallow English summaries.

**Lead with motivation.** Why does this concept exist? What problem did it solve? What was the world like before?

**Then explain mechanism.** How does it work? What are the moving parts?

**End with verification.** How does an operator confirm it is working? What CLI command shows the state?

**Concrete example for a section on `recirc_id`:**

| Approach | Description |
|---|---|
| Bad (mechanism only) | "`recirc_id` is a 32-bit field in the megaflow key. It is set by the `OVS_ACTION_ATTR_RECIRC` action. Use `ovs-dpctl dump-flows` to see it." |
| Good (why before what) | "Before OVS 2.2, the kernel datapath had no way to re-enter classification after running an action. This was a problem for `ct()`, because the conntrack result is only known after the packet hits netfilter, but a flow rule needs to match on that result. `recirc_id` was added to solve this. It is a 32-bit field in the megaflow key. The translator allocates a unique value, attaches it to a frozen state record in `ofproto/ofproto-dpif-rid.c`, and emits an `OVS_ACTION_ATTR_RECIRC` action. The datapath then re-runs classifier lookup with the new `recirc_id` set in the key. To verify, run `ovs-dpctl dump-flows`. Each megaflow that participates in recirculation shows `recirc_id(0x...)` as its first match field." |

The "Good" version is roughly 4 times longer, but it is the version a Vietnamese engineer can internalize.

---

## 8. Callout label conventions

Replace the existing Vietnamese callout labels with English ones. Locked in for grep-ability.

| Vietnamese (retired) | English (required from now on) |
|---|---|
| `**Hiểu sai:**` | `**Common misconception:**` |
| `**Điểm mấu chốt:**` | `**Key point:**` |
| `**Bối cảnh:**` | `**Context:**` |
| `**Quy tắc:**` | `**Rule:**` |
| `**Lưu ý:**` | `**Note:**` |
| `**Tuyên bố cần kiểm chứng:**` | `**Claim to verify:**` |
| `**Khái niệm:**` | `**Concept:**` |
| `**Lịch sử + bối cảnh:**` | `**History and background:**` |
| `**Vị trí trong kiến trúc:**` | `**Position in the architecture:**` |
| `**Vai trò:**` | `**Role:**` |
| `**Vì sao sinh ra:**` | `**Why it exists:**` |
| `**Vấn đề giải quyết:**` | `**Problems it solves:**` |
| `**Tầm quan trọng:**` | `**Importance:**` |
| `**Cơ chế hoạt động:**` | `**How it works:**` |
| `**Cách kỹ sư vận hành thành thạo:**` | `**How an operator masters this:**` |
| `**Phân loại:**` | `**Classification:**` |
| `**Quy trình sử dụng:**` | `**Usage workflow:**` |
| `**Khi xảy ra sự cố:**` | `**When something goes wrong:**` |
| `**Liên quan mật thiết:**` | `**Tightly related to:**` |
| `**Khác biệt giữa các phiên bản:**` | `**Version differences:**` |
| `**Cách quan sát + xác minh:**` | `**Observation and verification:**` |
| `**Source code tham chiếu:**` | `**Source code reference:**` |
| `**Trường hợp sự cố thực tế:**` | `**Real-world incident:**` |
| `**Bài tập synthetic:**` | `**Synthetic exercise:**` |
| `**Lỗi thường gặp + tín hiệu chẩn đoán:**` | `**Common failures and diagnostic signals:**` |
| `**So sánh với hệ khác:**` | `**Comparison with other systems:**` |
| `**Phiên bản:**` | `**Version note:**` |
| `**Triệu chứng:**` | `**Symptom:**` |
| `**Chẩn đoán:**` | `**Diagnosis:**` |
| `**Khắc phục:**` | `**Fix:**` |
| `**Bài học:**` | `**Lesson learned:**` |
| `**Mục tiêu:**` | `**Goal:**` |
| `**Chuẩn bị:**` | `**Setup:**` |
| `**Bước thực hiện:**` | `**Steps:**` |
| `**Hệ quả:**` | `**Consequence:**` |

If a label not in this table appears in legacy content, add the English mapping to this guide in the same commit that translates the section.

---

## 9. Technical-claim discipline preserved

CLAUDE.md Rule 14 (cross-source citation integrity) still applies in full to English prose. Every English explanation that touches an upstream OVS, OVN, or OpenFlow detail must cite the source per Rule 14:

- Function names: verified at the curriculum baseline tag (`v2.17.9` for OVS, `v22.03.8` for OVN).
- File paths: verified to exist at the baseline tag.
- Line numbers: optional per Rule 14.4 Option C, but if cited must be exact at the baseline.
- Commit SHAs: verified via `git log -1 <sha>` on the local repo.
- Schema claims: verified against the actual `*.ovsschema` JSON.

Translating a passage from Vietnamese to English does not relax accuracy requirements. If anything, the translation pass is a good opportunity to re-verify citations against the local OVS repo.

---

## 10. Side-by-side example: a full section translated

Below is a real curriculum section translated from Vietnamese to English per this style guide. The original is from `9.32 - ovs-classifier-internals-deep.md` §9.32.4 axis 1 ("Khái niệm").

### Original (Vietnamese, current curriculum text)

The Vietnamese source text is shown below in a fenced code block so that the language detector skips it. The block is verbatim from the file `9.32 - ovs-classifier-internals-deep.md` §9.32.4 axis 1.

```text
**Khái niệm.** `dpif` là tầng abstraction trong userspace OVS cho phép
`ofproto-dpif` (engine xlate OpenFlow tới datapath byte-code) thao tác
với một datapath backend bất kỳ qua một interface thống nhất. Cụ thể:
thay vì `ofproto-dpif` gọi trực tiếp Netlink syscall vào kernel
`openvswitch.ko`, hoặc gọi DPDK API vào userspace netdev, mọi thao
tác (port add/del, flow add/del/dump, packet send/recv, conntrack
execute) đi qua một virtual function table `struct dpif_class`. Mỗi
backend cụ thể (kernel, userspace, AF_XDP, DPDK) đăng ký một
implementation của `dpif_class` lúc khởi động.
```

### Translated (English, target style)

> **Concept.** `dpif` is an abstraction layer in OVS userspace. It lets `ofproto-dpif` (the OpenFlow-to-datapath translation engine) drive any datapath backend through one common interface. Without `dpif`, `ofproto-dpif` would have to call kernel Netlink syscalls directly for the kernel datapath, and DPDK APIs directly for userspace, and so on for each backend. With `dpif`, every operation goes through a virtual function table named `struct dpif_class`. The operations include adding and removing ports, adding, removing, and dumping flows, sending and receiving packets, and executing conntrack actions. Each concrete backend (kernel, userspace native, AF_XDP, DPDK) registers its own implementation of `dpif_class` at startup.

### What the translation preserves

- All canonical identifiers stay verbatim: `dpif`, `ofproto-dpif`, `openvswitch.ko`, `struct dpif_class`, AF_XDP, DPDK, Netlink.
- The "why before what" structure: first the role (lets `ofproto-dpif` drive any backend), then the mechanism (virtual function table), then the operations enumerated.
- Pedagogical depth: the "without `dpif`" sentence explicitly contrasts the layered design with what would happen without it.

### What the translation changes

- Vietnamese label `**Khái niệm.**` becomes English `**Concept.**`.
- Vietnamese arrow `→` is replaced by the English phrase "to" inside prose ("OpenFlow-to-datapath translation engine"). The arrow stays in code or in `ASCII art`.
- Em-dash that appeared in the original is gone (the translation uses a comma or a new sentence instead).
- The sentence count went up. The original has two sentences. The translation has five. This is intentional, per §2.

---

## 11. Maintenance

This style guide is itself subject to Rule 17 (English-only). It is also subject to Rule 14 (technical-claim discipline) for any code or upstream reference it contains.

When a new pattern emerges that the guide does not cover, append a sub-section in the same commit that introduces the pattern. Do not write a separate "guide v2" file; this file is the single source of truth.

When plan v3.12 is written, this guide is the canonical reference for legacy-section translations.

---

## 12. Cross-references

- CLAUDE.md Rule 17 (English as the mandatory explanation language).
- CLAUDE.md Rule 14 (Source code citation integrity), unchanged.
- Plan v3.9.1 §8 addendum (curriculum-wide English language migration).
- Plan v3.9.1 Phase Q9 (this guide's authoring phase).
- `memory/shared/rule-11-dictionary.md` (frozen historical reference for Vietnamese-to-English translation work in plan v3.12).
- Pre-commit hook `scripts/em_dash_check.py` (enforces §4 zero-em-dash rule).
