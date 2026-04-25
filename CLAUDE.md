# Project Memory, network-onboard

> **CRITICAL.** Read this entire file BEFORE doing anything. This file is the project's working memory, committed to git, synced across machines.

> **Language convention.** This file (CLAUDE.md) and `memory/*` are written in English (working/meta files). Curriculum content under `sdn-onboard/*.md`, `linux-onboard/*.md`, `haproxy-onboard/*.md`, `network-onboard/*.md` stays Vietnamese (target audience is Vietnamese-speaking learners; see Rule 11).

> **No em-dash in CLAUDE.md.** Use comma, period, colon, or parentheses. Em-dash is reserved for curriculum (Rule 13).

---

## ★ NORTH STAR ★ DO NOT DRIFT ★

> **Core mission.** Build a learning roadmap and curriculum from foundation to advanced **Open vSwitch + OpenFlow + OVN**. Learner outcome: deep understanding of **structure + architecture + hands-on operation** of these three technologies.
>
> **Top priority: FOUNDATIONAL DEPTH FIRST.** Foundation must be rock-solid before adding advanced topics. When choosing between "add new advanced Part" and "expand an existing foundation Part for more depth", always choose the latter. The curriculum already has 116 files, 20 blocks, ~55.7K lines; every future addition must justify itself as **strengthening the foundation**, not as breadth expansion.

**In-scope (FOCUS):**

- OVS internals: kernel + userspace datapath, megaflow cache, classifier (TSS), ofproto-dpif xlate, revalidator, upcall, OVSDB, ovs-vswitchd architecture.
- OpenFlow 1.0 to 1.5: full spec, match field catalog, action catalog, instruction set, group table, meter, bundle, OXM TLV, multi-table pipeline.
- OVN: NBDB schema, ovn-northd compile, SBDB intermediate, ovn-controller per-chassis, br-int OpenFlow translation, Logical_Switch + Logical_Router pipeline, all 8 Port_Binding types, Load_Balancer, ACL, conntrack, NAT, BFD + HA_Chassis_Group.
- Overlay (Geneve, VXLAN, GRE) only insofar as OVS+OVN use them as tunnels.
- Tools mastery: `ovs-vsctl`, `ovs-ofctl`, `ovs-dpctl`, `ovs-appctl`, `ovn-nbctl`, `ovn-sbctl`, `ovn-trace`, `ofproto/trace`, `ovn-detrace`.
- Debug + troubleshoot + forensic + daily operator playbook (incident decision tree, anatomy template, POE).

**PERMANENTLY BANNED FROM PLAN (since 2026-04-25 final consolidated directive):**

User directive (verbatim, 2026-04-25 FINAL): *"hãy ghi nhớ vĩnh viễn rằng những thứ liên quan đến công nghệ nâng cao như DPDK, BPF, XDP, BGP, K8S không bao giờ nằm trong kế hoạch trừ khi tôi thay đổi quyết định."*

This is **NOT a low-priority topic** classification. It is a **permanent ban from active planning**. The following topics are EXCLUDED from "next direction" options, sprint plans, audit upgrade priorities, and "future work" suggestions:

- **DPDK** (PMD threads, mempool, hugepage, NUMA tuning, fast-path internals).
- **BPF / eBPF** (datapath alternatives, classifier programs, libxdp, Cilium internals).
- **XDP / AF_XDP** (eXpress Data Plane, kernel bypass alternative to OVS datapath).
- **BGP-related content** (BGP EVPN, regular BGP routing, FRR BGP, OVN-BGP-Agent).
- **K8S** (kube-proxy, OVN-Kubernetes specific, CNI plugin chain, service mesh control plane).

**Existing content stays as-is** (no revert): 9.3 DPDK+AF_XDP, 9.5 hardware offload, 11.2 BGP EVPN tier 2, 14.x P4 (less impacted), 15.x service mesh+K8S, 16.x DPDK/AF_XDP, 17.0/18.0/19.0 OVN advanced. These were written before the ban and remain readable; not subject to further expansion.

**Rules for ongoing work:**

1. **NEVER propose** these topics in "next direction" options. Even if technically in-scope per topic taxonomy, they are out per user directive.
2. **DO NOT plan** sessions, sprints, or phases targeting these topics.
3. **DO NOT mention** them as "candidates" or "future work" or "deferred" in proposals — just exclude entirely.
4. If a Part touches these topics tangentially (ví dụ: 13.11 LR mentions FRR BGP), keep mention 1-2 sentence high-level + cross-link existing Part. Do not deep-dive further.
5. When auditing SHALLOW files for upgrade priority, EXCLUDE these from candidate list (9.3 DPDK+AF_XDP, 15.x deferred files, 11.2 partial sections, etc.).

**Override condition:** ONLY if user explicitly says "hãy thêm DPDK..." or equivalent explicit reversal. Anything weaker = ban remains.

**Active plan hierarchy (4 tiers, advanced topics not represented):**

1. **HIGHEST** = OVS/OpenFlow/OVN core internals (datapath, classifier, conntrack, ofproto, OVN northd/controller/binding, NBDB/SBDB, Geneve as OVN tunnel).
2. **HIGH** = Tools mastery + debug pedagogy (CLI playbook, Anatomy Template A, troubleshooting decision tree).
3. **MEDIUM** = Foundation prerequisites (Linux netns/bridge/veth/tc/conntrack), OVSDB foundation.
4. **LOW** = History/narrative (Block II/III), DC applied (Block XII).

Block XV (Cloud Native) was officially deprioritized 2026-04-23 + reaffirmed by 2026-04-25 ban. 15.1 + 15.2 deferred indefinitely. P4 + service mesh remain in existing files but not subject to expansion.

Memory pointer: [`memory/feedback_advanced_topics_permanent_ban.md`](memory) auto-loaded each session.

**Self-check before writing a new Part or expanding a section:**

> *"Does this topic make the engineer better at OVS, OpenFlow, or OVN? If it only makes them better at K8S, DPDK, or XDP, it is OUT OF SCOPE."*

When in doubt, stop and ask the user before proceeding. Out-of-scope detours bloat the curriculum and dilute focus.

---

## ★ SECOND NORTH STAR ★ QUALITY OVER SPEED ★

> **Owner directive (verbatim, 2026-04-25):** *"cái tôi cần là chất lượng, tỉ mỉ, cẩn thận và hợp lý. Tốn bao nhiêu thời gian hay bao nhiêu effort hoàn toàn không quan trọng với tôi."*
>
> *"Tôi đề cao tính chính xác, giải thích dễ hiểu, sự tỉ mỉ và cẩn thận hơn là tốc độ. Ví dụ làm việc tốc độ thì kết quả sẽ mất đi tính chất lượng."*

**Translation:** the user values **accuracy + clear explanation + meticulousness + caution** above all. Speed is explicitly NOT a goal. Working fast trades away quality, which is unacceptable.

**Operating principles:**

1. **Verify, never estimate.** When the user asks for a count, statistic, or status, run `wc -l`, `grep`, `git log`, or MCP API. Do NOT guess from memory or extrapolate from prior context. State the verified number.
2. **Explain why before what.** When introducing a concept or recommending an action, lead with the reasoning, then the conclusion. Vietnamese learners reading the curriculum need the *why* to internalize, not just the procedure.
3. **Read the file before editing.** Always Read the actual current state before Edit/Write. Do NOT rely on cached mental models from earlier in the session. The file may have been modified by a linter, by the user, or by an earlier AI step.
4. **Check every URL before adding it.** Use `web-fetcher` or `curl -I`. Dead URLs are silent quality bugs that surface much later.
5. **Cross-reference upstream source.** For every commit SHA, function name, file path, line number, or schema claim, verify via MCP GitHub (Rule 14). Do not cite from memory.
6. **Pre-flight checklist before commit.** Run Rule 6 Checklist B (before write) and Checklist C (before commit) every single time. Do not skip.
7. **When asked to be fast, refuse politely.** If a user request implies speed (e.g., "quick fix", "just commit it"), the response is to acknowledge but still do the careful version. Speed is not a valid trade-off.
8. **One commit per logical unit.** Do not bundle unrelated changes. Each commit should be reviewable in isolation, with a clear scope statement.

**Anti-pattern signals (you are slipping into speed mode if):**

- Skipping Read before Edit "because the file was just shown".
- Citing line numbers from memory instead of verifying.
- Writing a paragraph of conclusions before reading the source they are about.
- Batching 3 unrelated fixes into one commit "to save commits".
- Dropping pre-commit checklists "because nothing seems risky".
- Estimating instead of measuring.

When you catch yourself doing any of these, STOP, restart that step the careful way.

---

## Owner

VO LE (volehuy1998@gmail.com), Computer Network Engineer, OpenStack/kolla-ansible, SDN/OVN/OVS researcher.

---

## Repository Structure

```
network-onboard/                    (repo root, GitHub: volehuy1998/network-onboard)
├── CLAUDE.md                       (THIS FILE, working memory)
├── README.md                       (parent README, entry point for the repo)
├── CHANGELOG.md                    (release notes, Keep a Changelog format)
├── memory/                         (deep memory: state trackers, dictionaries, audit summaries)
│   ├── MEMORY.md                   (auto-memory index, hooks into Claude)
│   ├── session-log.md              (session-by-session log, append-only)
│   ├── file-dependency-map.md      (Rule 2 cross-file sync map)
│   ├── sdn-series-state.md         (per-Part status tracker, Rule 5 handoff)
│   ├── audit-index.md              (TOC of audit reports)
│   ├── audit-2026-04-25-summary.md (consolidated audit findings, latest)
│   ├── rule-11-dictionary.md       (Vietnamese prose translation dictionary)
│   ├── lab-verification-pending.md (exercises pending lab host)
│   └── haproxy-series-state.md
├── sdn-onboard/                    (SDN onboard series, Vietnamese)
├── haproxy-onboard/                (HAProxy onboard series, Vietnamese)
├── linux-onboard/                  (Linux/RHCSA onboard series, Vietnamese)
├── network-onboard/                (Network/CCNA onboard series, Vietnamese)
├── references/                     (shared references)
└── images/                         (shared images)
```

---

## Mandatory Rules

The repo has 6 skills installed at `~/.claude/skills/`. All 6 must be used; do not skip any when the activation condition holds.

### Rule 1: Skill Activation Sequence (MANDATORY)

**Group A, Core 4 (ALWAYS active for ANY interaction with `.md` files):**

1. `professor-style`: tone control, conceptual structure (6 criteria 2.1 to 2.6).
2. `document-design`: layout, headings, learning elements.
3. `fact-checker`: verify EVERY technical claim before commit.
4. `web-fetcher`: verify EVERY URL before adding to documentation.

**Group B, 2 conditional (consider before skipping):**

5. `search-first`: before writing new code/script/utility. Adopt > Extend > Compose > Build.
6. `deep-research`: when content needs multi-source citation beyond offline `doc/*` (firecrawl + exa MCP).

**Workflow.** Open `.md` to write/edit/audit, activate Core 4 immediately. Before writing helper code, activate `search-first`. Before writing content needing multi-source research, activate `deep-research`. Record activated skills in the fact-forcing gate answer. Do not write content first then review afterwards. Always: read skill, write, self-audit.

(Origin: 2026-03-30 audit miss; 2026-04-22 added Group B.)

### Rule 2: Cross-File Sync (MANDATORY)

Before commit, consult `memory/shared/file-dependency-map.md` to identify dependent files.

**Process:** identify file being edited, look up dependency map, check related files, update ALL related files in the SAME commit.

(Origin: parent `README.md` left stale after `haproxy-onboard/README.md` version bump.)

### Rule 3: Version Annotation Convention

When writing content with HAProxy version differences, use the callout `> **Version note:** <difference>`. Also update `haproxy-onboard/references/haproxy-version-evolution.md` with a new entry.

### Rule 4: Git Workflow

- Protected branch: do NOT push directly to `main`/`master`.
- Commit convention: Conventional Commits (`feat()`, `fix()`, `docs()`).
- Branching: GitHub Flow (main + feature branches).
- Read the `git-workflow` skill before any git operation.

### Rule 5: Session Handoff Protocol

**On session END (or when user says "stop", "pause", "end"):**

1. Update `memory/shared/session-log.md` with date/time, what was done (commits, files), what is PENDING, current branch + state, commands the user must run locally (e.g., `git push`).
2. Update `memory/sdn/series-state.md` if any Part status changed.
3. Commit memory changes.

**On session START:**

1. Read CLAUDE.md (this file).
2. Read `memory/shared/session-log.md` (last session context).
3. Read `memory/sdn/series-state.md` (curriculum status).
4. Run `git status`, `git branch`, `git log`.
5. Tell the user: "I have read context. Last session [summary]. Pending: [list]."

### Rule 6: Quality Gate, Pre-flight Checklist (MANDATORY)

**Checklist B, BEFORE writing/editing/auditing `.md` or `.svg`:**

1. Activate `professor-style` skill (6 criteria 2.1 to 2.6).
2. Activate `document-design` skill (chapter template, heading rules, Rule 8).
3. Identify the file being edited.
4. Look up `memory/shared/file-dependency-map.md`, list related files (including Tier 5: SVG to markdown).
5. Read related files for current content.
6. If editing SVG: grep all `.md` referencing the SVG, read current captions, note entities.
7. START writing/editing (NOT before steps 1 to 6).
8. If editing SVG: update caption IMMEDIATELY after SVG completion, before any other task.

**Checklist C, BEFORE commit:**

1. Fact-check: list EVERY technical claim, verify each.
2. URL check: list EVERY URL, verify with `web-fetcher` or `curl`.
3. Cross-file sync: check dependency map.
4. Version annotation: cross-version content gets a callout + tracker entry.
5. SVG spacing + diacritics: run `svg-audit.py` + `diacritics-audit.py`. Zero violation.
6. SVG-caption consistency: run `svg-caption-consistency.py`. Zero mismatch.
7. File integrity: null byte check (Rule 9) on EVERY modified text file. Zero null bytes.
8. Rule 11 Vietnamese Prose scan (full regex `§11.6`, not just `inspect|support`). Classify each hit per §11.3, fix prose hits, add new dictionary entries.
9. Rule 11 spot-check bold label + section heading: `grep '^##' <file>`, `grep -E '^\*\*[A-Z][a-z]+' <file>`, `grep -E '^> \*\*(Key Topic|Hiểu sai|Điểm mấu chốt)' <file>`.
10. Rule 13 em-dash density: target < 0.10/line. Audit every em-dash if > 0.10, fix prose overuse.
11. Read `git-workflow` skill before commit.
12. Self-audit `professor-style` 6 criteria on new content.

**Checklist E, when adding a new Part:**

1. Run Checklist B.
2. Create file with naming convention `X.0 - <name>.md`.
3. Header block + learning objectives per `document-design`.
4. Update `README.md` (TOC, dependency graph).
5. Update `memory/sdn/series-state.md`.
6. Update `memory/shared/file-dependency-map.md`.
7. Run Checklist C.

Principle: this is pre-flight, not bureaucracy. 2 to 3 minutes overhead; cost of a sync bug is much higher.

### Rule 7: Terminal Output Fidelity (MANDATORY)

When the user provides real terminal output to insert into documentation:

1. Do NOT trim, shorten, or omit any line.
2. Do NOT reorder lines.
3. Do NOT change spacing, indentation, or any character.
4. When comparing output: line-by-line diff, not just the value of interest.
5. To shorten output: ASK the user first, naming which lines to drop and why.

Applies to: `fdinfo`, `lsof`, `ss`, `strace`, `tcpdump`, `haproxy -vv`, log files, any user-provided output.

#### Rule 7a: System Log Absolute Integrity (NO EXCEPTIONS)

System logs (daemon/service logs, diagnostic tool output) follow stricter rules than Rule 7:

1. ABSOLUTELY NO truncation, even of UUID, path, IP.
2. ABSOLUTELY NO merging multiple log lines into one entry.
3. ABSOLUTELY NO deletion of log lines, even if "repetitive" or "unimportant".
4. ABSOLUTELY NO timestamp modification, not even by 1 ms.
5. NO EXCEPTIONS. System log is forensic evidence.
6. When presenting log in another format (timeline, table, annotated block): message body after the prefix MUST stay verbatim on its own line; annotations on separate lines prefixed with `--`.
7. When showing a subset: include `[N other lines omitted, context: ...]`.

Scope: every daemon/service log (ovn-controller, ovs-vswitchd, nova-compute, neutron-server, haproxy, nginx, journald, syslog, dmesg) and every diagnostic tool output (tcpdump, strace, lsof, ss, conntrack, ovs-ofctl, ovn-trace, ovn-detrace).

(Origin: 2026-04-11 SDN 1.0 timeline merged 3 separate log lines, truncated UUID, deleted "Claiming unknown" lines, modified timestamp `.947` to `.948`.)

### Rule 8: Vietnamese Sentence Completeness (MANDATORY)

Documentation written for Vietnamese readers. Every clause must be complete on its own; do not lean on implicit context.

1. Negation cannot dangle: `không`, `chưa`, `chẳng` MUST come with a clear verb or object.
2. Demonstratives are unambiguous: `điều đó`, `việc này`, `nó` MUST have a clear antecedent within the same or adjacent sentence; otherwise repeat the noun.
3. Standalone-read test: after writing each sentence, read it isolated from context. If meaning is unclear, rewrite.

(Origin: 2026-04-04 dangling `không` at clause end with no object.)

### Rule 9: File Integrity, Null Byte Prevention (MANDATORY)

BEFORE `git add`:

```bash
for f in $(git diff --name-only --cached 2>/dev/null; git diff --name-only); do
  if [ -f "$f" ]; then
    nullcount=$(python3 -c "print(open('$f','rb').read().count(b'\x00'))")
    if [ "$nullcount" -gt 0 ]; then
      echo "BLOCKED: $f has $nullcount null bytes"
    fi
  fi
done
```

If null bytes found, strip with:

```bash
python3 -c "d=open('FILE','rb').read(); open('FILE','wb').write(d.replace(b'\x00',b''))"
```

Verify: `grep -cP '\x00' FILE` must return 0.

Scope: every text file (`.md`, `.py`, `.sh`, `.yml`, `.html`, `.svg`, `.css`, `.js`). Null bytes in text files are ALWAYS a bug. Binary files (`.png`, `.jpg`, `.pdf`) are exempt.

Warning signs: `file` command says "with very long lines" on `.md`; abnormally large file size vs line count; GitHub renders the file as binary.

(Origin: commit `9a17eec` had 3612 trailing null bytes; GitHub refused to render markdown.)

### Rule 10: Architecture-First Doctrine (HISTORICAL)

This rule applied during the architecture phase (now complete; project is in content phase since session 12). For historical record only. Skeleton-first discipline still applies when introducing brand-new blocks.

(Originally written 2026-04-21 to constrain over-eager content writing during the skeleton phase.)

### Rule 11: Vietnamese Prose Discipline (MANDATORY)

This is a training program for Vietnamese readers. Prefer natural Vietnamese; keep English only for named entities, syntax, and identifiers. Core principle: **translate at the right place**.

#### 11.1. KEEP English when the word appears as one of:

- **Product / project / organization name**: OpenFlow, OVS, OVN, Open vSwitch, NETCONF, NSX, Nicira, VMware, Linux, Ubuntu, Mininet, Cisco, Broadcom Trident, Stanford, ONF, GitHub, Spamhaus, Prometheus, Arbor Networks, Cloudflare, DigitalOcean, Red Hat, NVIDIA ConnectX-6, Intel E810, Anthropic.
- **International protocol / acronym**: TCP, UDP, IP, ICMP, SCTP, ARP, DNS, TLS, SSH, HTTP, HTTPS, VLAN, VXLAN, Geneve, BGP, OSPF, BFD, MPLS, NAT, SNAT, DNAT, DDoS, RPC, ECMP, FTP.
- **CLI verbatim + flag**: `ovs-ofctl`, `ovs-vsctl`, `ovs-appctl`, `ovs-dpctl`, `ovn-nbctl`, `ovn-sbctl`, `ovn-northd`, `ovn-controller`, `conntrack`, `iptables`, `modprobe`, `sysctl`, `sudo`, `ping`, `iperf`, `tcpdump`, `--dpdk`, man references like `ovs-fields(7)`, `ovs-actions(7)`, `ovn-architecture(7)`.
- **Spec field name / match field / OpenFlow identifier**: `ct_state`, `ct_zone`, `ct_mark`, `ct_label`, `metadata`, `cookie`, `priority`, `in_port`, `nw_src`, `nw_dst`, `dl_src`, `dl_dst`, `dl_type`, `tp_dst`, `sport`, `dport`, `reg0..reg15`, `xreg0..xreg7`, OXM, NXM.
- **Action / instruction / pipeline stage name**: `goto_table`, `resubmit`, `output`, `normal`, `drop`, `mod_dl_src`, `mod_dl_dst`, `dec_ttl`, `ct()`, `ct(commit)`, `ct_next`, `ct_commit`, `ct_lb`, `ct_clear`, `apply_actions`, `write_actions`, `write_metadata`, `clear_actions`, `Apply-Actions`, `Write-Actions`, `Clear-Actions`, `Write-Metadata`, `Goto-Table`, `allow`, `allow-related`, `reject`, `set_queue`, action values like `ct_state=+trk+new`.
- **Pipeline stage / table name as label**: "Table 0 Classifier", "Table 1 L3 Forwarding", "Ingress ACL", "Egress ACL", "(ACL, routing, output)". These are pipeline stage names in OVS/OVN architecture.
- **Literal state / flag / protocol value**: `NEW`, `ESTABLISHED`, `RELATED`, `INVALID`, `SYN_SENT`, `SYN_RECV`, `FIN_WAIT`, `TIME_WAIT`, `CLOSE`, `CLOSE_WAIT`, `LAST_ACK`, `UNREPLIED`, `ASSURED`, `[NEW]`, `[UPDATE]`, `[DESTROY]`.
- **Common international networking term**: SDN, DC, WAN, LAN, DPU, ASIC, NOS, VM, RFC, MAC, VIP, NFV, SR-IOV, SmartNIC, FIB, BUM, DMZ, VPN, L2, L3, L4, five-tuple, three-way handshake, pseudo-state, bitfield, tuple, hairpin, subnet, broadcast, multicast, unicast, datapath, bridge, kernel, userspace, namespace, tenant, multi-tenant, chassis, overlay, underlay, east-west, north-south, fast path, slow path, line-rate, offload, DPDK.
- **OpenFlow / OVS spec concept used as noun**: flow, flow entry, flow table, flow rule, pipeline, multi-table pipeline, match field, action set, instruction, controller, stateful, stateless, conntrack, handshake.

#### 11.2. TRANSLATE to Vietnamese when the word appears in prose

Full dictionary (~60 entries) is in [`memory/shared/rule-11-dictionary.md`](memory/shared/rule-11-dictionary.md). Common examples: paradigm to mô hình, approach to cách tiếp cận, deployment to triển khai, performance to hiệu năng, verify to kiểm chứng, operator to người vận hành, motivation to động cơ, scalability to khả năng mở rộng, flexibility to tính linh hoạt, post-mortem to báo cáo hậu sự, troubleshoot to khắc phục sự cố, version to phiên bản.

When you encounter a word not in the dictionary: ADD it to `memory/shared/rule-11-dictionary.md` in the same fix commit (Rule 11 §11.7).

#### 11.3. Same word, sometimes English sometimes Vietnamese

| Word | KEEP English when | TRANSLATE when |
|------|------------------|---------------|
| `routing` | Stage name: `(ACL, routing, output)`, `L3 Forwarding`, `distributed routing` (OVN noun phrase) | Prose verb: "gói tin được định tuyến sang subnet khác" |
| `output` | Action: `action=output:3`; stage in tuple `(ACL, routing, output)` | Prose: "kết quả của toàn bộ pipeline", "đầu ra của trace" |
| `table` | OpenFlow concept: `table=0`, "multi-table pipeline" | Prose: "bảng FIB L3", "bảng MAC", "bảng trạng thái conntrack" |
| `forwarding` | Table name: "Table 2 L2 Forwarding" | Prose: "chuyển tiếp gói tin sang h3" |
| `state` | Field name: `ct_state`; literal: `state=ESTABLISHED` | Prose: "theo dõi trạng thái", "máy trạng thái" |
| `flow` | OpenFlow concept: "flow entry", "flow table", "flow rule" | Generic: "luồng dữ liệu" (rare) |
| `traffic` | Rare | Prose: "lưu lượng đông-tây", "lưu lượng reply" |
| `connection` | Conntrack literal: `connection ESTABLISHED` | Prose: "kết nối hai chiều", "kết nối h1 to h3" |
| `switch` | Device name: switch `s1`, OVS switch | Verb "chuyển đổi" translates |
| `monitoring` | Component name: "Monitoring tool" | Prose: "giám sát bảng trạng thái" |
| `pattern` | Code/config pattern name | Prose: "mẫu 7-flow Lab 8" |
| `commit` | CLI/action: `ct(commit)`, `commit entry` | Prose: "tạo entry tồn tại vượt quá vòng đời gói tin" |

**Self-classification question:** Is this word a **named entity** that OVS/OpenFlow/OVN docs use for an entity, syntax, or stage? If YES, keep English. If NO (descriptive/explanatory prose), translate.

#### 11.4. Bold label and section heading

Cannot leave English in:
- Prose section heading (Vietnamese curriculum).
- Paragraph-leading bold label: `**Sequential evaluation.**` becomes `**Đánh giá tuần tự.**`.
- Internal callout label: `> **Key Topic:**` becomes `> **Điểm mấu chốt:**`.

Can keep English when label is a concept/stage name: `## 9.24.3 Action ct(), full semantics`, `**NEW**`, `**ESTABLISHED**`.

#### 11.5. Standalone-read test + hybrid acceptable + misconception callout

- After each sentence, read it isolated. If it has > 3 non-standard English words, rewrite.
- Hybrid acceptable: "tích hợp với vSphere" (technical term + Vietnamese connector). Not "integrate với vSphere".
- Quotes inside `> **Hiểu sai:** *"..."*` must be full Vietnamese; only product/action/field names stay English.

#### 11.6. Pre-commit scan checklist (MANDATORY)

Run `grep -niE` for the dictionary regex (see `memory/shared/rule-11-dictionary.md` for the full list). Most hits are false positive (URL, code block, product name). Classify each hit:

1. Inside URL/code block/CLI sample, skip.
2. OVS/OVN/OpenFlow product/concept name, skip.
3. Bold label/section heading/cognitive prose, FIX to Vietnamese.

When uncertain: §11.3 self-classification question.

#### 11.7. Adding new dictionary entries

When you discover a new prose word not in `memory/shared/rule-11-dictionary.md`, ADD it in the same fix commit with example context. Dictionary is a living document.

(Origin: session 13 (2026-04-21) initial codification; sessions 22-23 broadened.)

### Rule 12: Exhaustive Offline Source Exploration (MANDATORY)

Before writing any onboard content, inventory all offline sources via recursive Glob:

```
Glob "sdn-onboard/doc/**/*"
Glob "haproxy-onboard/doc/**/*"
Glob "linux-onboard/doc/**/*"
Glob "network-onboard/doc/**/*"
Glob "references/**/*"
```

**Process:**

1. Session start: recursive Glob, list files in `*/doc/**` and `references/**`. Build a mapping: offline file to Block/Part using it.
2. Before each Write: list relevant `doc/*` for the topic. Cite explicitly in fact-forcing gate, header block, and References section.

**Violation signals:**

- Fact-forcing gate answer missing "Offline source providing content" line.
- File header missing `> **Primary offline source:**`.
- References section missing offline source entry.
- Writing technical content without `doc/*` citation when topic is covered.

(Origin: session 14 (2026-04-22) missed `sdn-onboard/doc/ovs/` (11 PDF + TXT) when writing Block VII + Part 9.0.)

### Rule 13: Em-dash Discipline (MANDATORY for curriculum)

> **Note:** CLAUDE.md and `memory/*` are zero em-dash zone (top of file directive). Rule 13 below applies to curriculum (`*-onboard/*.md`).

Em-dash is the exception, not the default. Vietnamese prose default to:

- **Comma (,)** for clause continuation.
- **Period (.) + capital** for new sentence.
- **Colon (:)** for list introduction or explanation.
- **Parentheses (...)** for aside.
- **Newline + bullet** for 3+ enumerated items.

#### 13.1. Em-dash IS allowed when

1. Heading-subtitle separator: `# 9.22. OVS multi-table pipeline, goto_table, resubmit`. One em-dash max in heading levels 1 to 3.
2. Bold mini-label separator in structured rule/flow: `**Rule 1, Always start at table 0.**`.
3. Bold noun + inline code list intro.
4. Attribution separator (organization, date).
5. Table row visual label inside ASCII diagram code block.

#### 13.2. Em-dash is NOT allowed when

1. Replacing comma in continuous prose.
2. Replacing period when starting a new sentence.
3. Replacing relative pronoun "là, nghĩa là, tức là".
4. Inside bullet definition `- X, explanation`.
5. Inside header block metadata `> **Label:** X, Y`.

#### 13.3. Density threshold

| Level | Em-dash/line | Verdict |
|-------|--------------|---------|
| < 0.05 | 1 per 20 lines | Natural |
| 0.05 to 0.10 | 1 per 10 to 20 lines | Acceptable |
| 0.10 to 0.15 | 1 per 7 to 10 lines | Warn, audit |
| > 0.15 | > 1 per 7 lines | Overuse, must fix |

Curriculum target: **< 0.10 em-dash/line**. Files exceeding 0.10 require audit before commit.

#### 13.4. Pre-commit em-dash audit (MANDATORY)

```bash
for f in $(git diff --name-only --cached | grep .md); do
  count=$(grep -c $'\xe2\x80\x94' "$f")  # U+2014 em-dash literal
  lines=$(wc -l < "$f")
  ratio=$(python -c "print(f'{$count/$lines:.3f}')")
  echo "$f: $count em-dash / $lines lines ($ratio/line)"
done
```

If ratio > 0.10, audit each hit. Fix priority: bullet definition (a) > inline prose lowercase (b) > inline prose capital (c) > header block metadata (d).

#### 13.5. New writing minimizes em-dash

Place em-dash last, not first. Write sentences with normal punctuation; convert to em-dash only if strong emphasis is required. When in doubt, do not use em-dash. Check density every 50 to 100 lines; rewrite if > 0.15.

(Origin: session 24 (2026-04-23) detected 361 em-dash across 4 Phase D files at density 0.13 to 0.19/line; reduced to 155 (57%) via 3-pass scripts + manual.)

### Rule 14: Source Code Citation Integrity (MANDATORY)

Every reference to upstream source code (OVS, OVN, Linux kernel, HAProxy, Nginx, OpenStack, DPDK, FRR, strongSwan, P4, Cilium) MUST be verified via MCP GitHub (or equivalent) BEFORE commit.

#### 14.1. Commit SHA reference

- Verify existence: `mcp__github__get_commit(owner, repo, sha)`.
- Verify claims match: author + date + message + files changed.
- Inline cite: 8 to 12 chars (SHA prefix). References section: 40-char full SHA.
- Inline SHA and Reference section MUST match (grep pre-commit).

#### 14.2. Function name reference

- Verify existence: `mcp__github__search_code(query="function_name repo:owner/repo")`.
- `search_code` has false negatives. Mandatory fallback: `mcp__github__get_file_contents`, then grep file content.
- Preserve exact source spelling, even typos. Example: OVN source has `reply_imcp_error_if_pkt_too_big` (typo `imcp`), do not "fix" to `icmp` when citing. Annotate `(upstream typo imcp)` if it might confuse readers.
- If function renamed across versions, annotate: `(named foo_bar in v22.03, renamed to bar_foo since v24.03 via commit abc1234)`.

#### 14.3. File path reference

- Verify existence at version baseline: `mcp__github__get_file_contents(path, ref)` with `ref` = curriculum baseline tag (e.g., `v22.03.8` for OVN, `v2.17.9` for OVS, `v5.15` for Linux Ubuntu 22.04).
- If file migrated across versions, annotate per Rule 3. Example: `controller/mac-learn.c` (v22.03 to v24.03) or `controller/pinctrl.c` §MAX_FDB_ENTRIES (v24.09+, commit `fb96ae3679`).

#### 14.4. Line number reference

Line numbers are version-sensitive. Mandatory annotation, choose one:

- **Option A** (branch-specific): `physical.c` lines 1939 to 1968 (OVN branch-24.03).
- **Option B** (commit permalink): `physical.c` link to GitHub blob at commit SHA (`https://github.com/ovn-org/ovn/blob/SHA/controller/physical.c#L1939-L1968`).
- **Option C** (function name anchor, RECOMMENDED): instead of line, use function name as stable anchor. Example: "In function `build_lswitch_arp_nd_responder_known_ips` in `northd/northd.c`, find the `op->lsp_has_port_sec || !op->has_unknown` check".

Line drift is common: v22.03 to main typically shifts 2000+ lines. Option C is best practice.

#### 14.5. Verbatim commit body quote

- Copy-paste EXACT from MCP API response. No translate, no edit spacing, no bullet format change.
- A block `> "Verbatim commit body from GitHub API:"` must be 100% English if the commit body is English.
- Translate only with explicit "paraphrase" label. Do NOT use "verbatim" label on a paraphrase.
- Dash bullets (`-`) preserve exact, do NOT convert to `(a)(b)(c)`.

#### 14.6. Database table + schema claim

- Verify schema existence via `mcp__github__get_file_contents` for `ovn-sb.ovsschema`, `ovn-nb.ovsschema`, `vswitchd/vswitch.ovsschema`.
- Parse JSON to list actual tables + columns.
- Do not fabricate table names. If a feature stores in `other_config` map instead of a dedicated table, say so.
- Internal C struct is NOT a database table. Distinguish clearly. Example: `struct chassis_features` in-memory differs from a hypothetical `Chassis_features` OVSDB table.

#### 14.7. Pre-commit audit pass

- Grep every new claim in section: SHA, function, path, line number, table name.
- If > 3 references in a section, run MCP audit batch (verify all).
- Log evidence in `memory/fact-check-audit-YYYY-MM-DD.md`.
- Commit only when 100% pass; any failed reference must be fixed or removed.

(Origin: session 32-33i (2026-04-22) found 32 issues across 6 categories on 43 files; codified Rule 14 in commit `7e5608b`.)

### Rule 15: No Self-Tag (MANDATORY)

> **Mirror governance principle GP-1.** Full text trong [`memory/sdn/governance-principles.md`](memory/sdn/governance-principles.md) Section 1. CLAUDE.md tóm tắt enforcement.

Curriculum SDN không được tag bất kỳ release version nào (v3.x, v4.x, vX.Y) cho đến khi đồng thời thỏa 4 điều kiện:

1. **Scorecard committed:** Mỗi keyword in-scope của REF có scorecard 20-axis trong repo, version-controlled.
2. **Threshold achieved:** Tất cả keyword đạt minimum threshold per Phase B rubric (Cornerstone DEEP-20, Medium DEEP-15, Peripheral PARTIAL-10).
3. **Audit script run + report committed:** `scripts/per_keyword_rubric_audit.py` chạy thành công, scorecard fresh trong 24 giờ trước commit.
4. **User written sign-off:** User confirmation explicit (chat message hoặc commit message hoặc plan tracker entry) approve tag.

**Pre-tag checklist (mandatory):**

- [ ] Run audit script, scorecard committed
- [ ] Verify threshold met (script exit 0)
- [ ] Verify scorecard timestamp ≤ 24 giờ vs HEAD
- [ ] User sign-off captured trong commit message
- [ ] Tag annotated message reference scorecard commit SHA

**Exception (hotfix only):**

- Security CVE upstream affecting keyword treatment
- Factual error correction (wrong commit SHA, typo in code citation)
- Typo/formatting trong existing content
- MUST có user explicit approval + rubric impact assessment + follow-up regression audit ≤ 7 ngày

**No other exceptions.** "Quick win", "milestone", "checkpoint" tag NOT allowed.

(Origin: 2026-04-26 reckoning. V3.6-ContentDepth tagged sau 1 session với "Tier A MISSING ≤ 50" acceptance gate measure breadth không depth. User check 13-tiêu-chí expose tag misleading. Plan v3.7 codify governance để prevent recurrence. See [governance-principles.md](memory/sdn/governance-principles.md) for full GP-1 text + 4 sister principles.)

### Rule 16: Internal-vs-Reader-Facing Language Separation (MANDATORY)

> **Mirror governance principle GP-11.** Full text trong [`memory/sdn/governance-principles.md`](memory/sdn/governance-principles.md) Section 16. CLAUDE.md tóm tắt enforcement.

Curriculum content (file `sdn-onboard/*.md`, `haproxy-onboard/*.md`, `linux-onboard/*.md`, `network-onboard/*.md` là reader-facing cho engineer học SDN) MUST KHÔNG chứa internal terminology của plan/rubric/governance.

**Forbidden patterns trong curriculum file:**

- `**Axis N <category>.**` (rubric label) → dùng natural VN heading: `**Khái niệm.**`, `**Cơ chế hoạt động.**`, `**Tầm quan trọng.**`, etc.
- `Axis 1` đến `Axis 20` (numbered reference) → category name VN
- `cohort C7`, `cohort M5`, `cohort P21` (triage label) → skip hoặc "nhóm <description>"
- `Phase G batch N`, `Phase R2/R3/R4` (plan reference) → skip hoặc "expansion 2026-04"
- `DEEP-20`, `DEEP-15`, `PARTIAL-10`, `REFERENCE-5`, `PLACEHOLDER` (tier label) → skip hoặc prose "đầy đủ", "khá đầy đủ"
- `rubric 20-axis`, `rubric 13-tiêu-chí` (meta term) → skip
- `anti-gaming`, `gaming pattern`, `cosmetic stamp`, `cohort stamp` (governance) → skip
- `GP-1` đến `GP-11` (governance reference) → skip
- `Form A per GP-6`, `Form B per GP-6` (commit pattern reference) → skip

**Replacement table cho 20-axis treatment** dùng natural VN heading:

| Internal axis label | Reader-facing VN heading |
|---------------------|-------------------------|
| Axis 1 Concept | Khái niệm |
| Axis 2 History | Lịch sử + bối cảnh |
| Axis 3 Placement | Vị trí trong kiến trúc |
| Axis 4 Role | Vai trò |
| Axis 5 Motivation | Vì sao sinh ra |
| Axis 6 Problem | Vấn đề giải quyết |
| Axis 7 Importance | Tầm quan trọng |
| Axis 8 Mechanism | Cơ chế hoạt động |
| Axis 9 Engineer-op | Cách kỹ sư vận hành thành thạo |
| Axis 10 Taxonomy | Phân loại |
| Axis 11 Workflow | Quy trình sử dụng |
| Axis 12 Troubleshoot | Khi xảy ra sự cố |
| Axis 13 Coupling | Liên quan mật thiết |
| Axis 14 Version drift | Khác biệt giữa các phiên bản |
| Axis 15 Verification | Cách quan sát + xác minh |
| Axis 16 Source code | Source code tham chiếu |
| Axis 17 Incident | Trường hợp sự cố thực tế |
| Axis 18 Lab | Bài tập synthetic |
| Axis 19 Failure mode | Lỗi thường gặp + tín hiệu chẩn đoán |
| Axis 20 Cross-domain | So sánh với hệ khác |

**Allowed exceptions:**

- `memory/*`, `plans/*` (working/meta audience)
- `CLAUDE.md`, `CHANGELOG.md` "Reckoning" sections (meta history)
- `0.3 - master-keyword-index.md` MAY use status code `DEEP/BREADTH/SHALLOW/MISSING/PLACEHOLDER` per existing convention
- Commit messages (internal audit log audience)

**Enforcement:**

- Pre-commit hook `scripts/rubric_leak_check.py` reject violation
- Phase R0.7 curriculum cleanup pass: replace existing leak (~25 file from Phase G v3.7)
- Self-check before each curriculum edit: read replacement table above

(Origin: 2026-04-26 user audit catch agent team chèn `**Axis N**` labels vào curriculum content gây confuse engineer reader. Plan v3.8-Remediation Section 11 amendment + GP-11 codify.)

---

## Current State

| Key | Value |
|-----|-------|
| Branch | `docs/sdn-foundation-rev2`. Latest tag: `v3.6-AuditTooling` (2026-04-26, renamed from v3.6-ContentDepth per Phase A v3.7 reckoning). **No newer tag.** v3.7 Phase G claim "COMPLETE" was self-deception, not honored. |
| Curriculum | **~128 files** in `sdn-onboard/*.md`, **~70K lines**, 20 blocks. **Honest depth ~22% reach tier target per 20-axis rubric** (manual audit 75 keyword sample 2026-04-26). Cornerstone 14/50 (28%) DEEP-20, medium ~27/112 (24%) DEEP-15, peripheral ~46/228 (20%) PARTIAL-10. Phase G v3.7 claim 100% inflate 4.5x. |
| Active phase | **v3.8-Remediation Phase R0/R1 in progress** (anti-gaming infrastructure + reckoning correction). Phase R2-R4 (~301 keyword real per-keyword work) + Phase R5 (user audit + sign-off) + Phase R6 (tag v4.0) thuộc multi-month effort. |
| Lab host | PENDING (waiting on user). 63 exercises pending verification. |
| HAProxy series | 1/29 Parts. Linux FD doc 1265 lines. |
| Trackers | [memory/sdn/series-state.md](memory/sdn/series-state.md), [memory/shared/audit-index.md](memory/shared/audit-index.md), [memory/shared/session-log.md](memory/shared/session-log.md), [memory/sdn/phase-g-progress-tracker.md](memory/sdn/phase-g-progress-tracker.md) (annotated PARTIAL post-honest-audit). |
| Dependency map | [memory/shared/file-dependency-map.md](memory/shared/file-dependency-map.md) (Rule 2). |
| Lab pending | [memory/sdn/lab-verification-pending.md](memory/sdn/lab-verification-pending.md). |
| **Governance** | [memory/sdn/governance-principles.md](memory/sdn/governance-principles.md) v1.1, **11 GP** (GP-1 đến GP-5 v3.7 + GP-6 đến GP-11 v3.8). Mirror trong CLAUDE.md Rule 15 (no self-tag) + Rule 16 (internal-vs-reader language separation). |
| **Active plan** | [plans/sdn/v3.8-remediation.md](plans/sdn/v3.8-remediation.md), APPROVED 2026-04-26, 7 phase R0→R6, target tag v4.0-MasteryComplete sau R6 (post-R5 user sign-off). Realistic effort 350-600 giờ multi-month. |
| Past plan v3.7 | [plans/sdn/v3.7-reckoning-and-mastery.md](plans/sdn/v3.7-reckoning-and-mastery.md), Phase A-F done, **Phase G PARTIAL ~22% (gaming detected)**, Phase H blocked. Superseded by v3.8-Remediation. |
| Past plan v3.6 | [plans/sdn/v3.6-content-depth.md](plans/sdn/v3.6-content-depth.md), Closed (audit tooling + 6 keyword closure, tag renamed). |
| Past plan v3.5 | [plans/sdn/v3.5-keyword-backbone.md](plans/sdn/v3.5-keyword-backbone.md), Closed (placement framework, không phải mastery). |
| **Anti-gaming script** | [scripts/anti_gaming_check.py](scripts/anti_gaming_check.py) GP-6 đến GP-10 enforcement. Pre-commit hook installed. Detect cohort tier-stamp + cosmetic stamp + min-lines violation. |
| **Rubric leak check** | [scripts/rubric_leak_check.py](scripts/rubric_leak_check.py) GP-11 / Rule 16 enforcement. Pre-commit hook. Phase R0.7 cleanup ~25 file pending. |
| Pre-commit hook | [scripts/pre-commit-install.sh](scripts/pre-commit-install.sh) installs `.git/hooks/pre-commit` running both check scripts on staged .md. |
| Honest audit | [memory/sdn/per-keyword-honest-audit.md](memory/sdn/per-keyword-honest-audit.md) manual 75-keyword stratified audit 2026-04-26 reveal v3.7 Phase G 4.5x inflate. |
| Audit script v3 | [scripts/refine_coverage_matrix_v2.py](scripts/refine_coverage_matrix_v2.py), coverage matrix breadth audit (legacy). Phase R5 sẽ build per_keyword_strict_audit.py cho depth verification. |
| Gap tracker | [memory/sdn/keyword-true-gap-final.md](memory/sdn/keyword-true-gap-final.md), v3.6 Phase 1+2 deliverable. Superseded by Phase R5 strict audit. |
| REF source-of-truth | [sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md](sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md), REF 2617 dòng English authoritative, 320+ keyword in-scope. |
| Master index 0.3 | [sdn-onboard/0.3 - master-keyword-index.md](sdn-onboard/0.3%20-%20master-keyword-index.md), Vietnamese lookup spine 1153 dòng, 320+ keyword 5-axis 1-line. **Note:** placement map, không phải mastery map. |
| Plans index | [plans/README.md](plans/README.md) (per-series structure) |
| Memory index | [memory/README.md](memory/README.md) (per-series + shared structure) |

Session-by-session history (S1 to S63+) is in `memory/shared/session-log.md`. Audit history is in `memory/shared/audit-index.md`. `git log` is the source of truth for commit detail.

---

## Skill Quick Reference

**Installed at `~/.claude/skills/` (6 skills, all must be used):**

| Group | Skill | When to use |
|-------|-------|-------------|
| Core A | `professor-style` | EVERY teaching content, `.md` write, technical explanation |
| Core A | `document-design` | EVERY `.md` in onboard series |
| Core A | `fact-checker` | EVERY technical claim, CLI command, config directive |
| Core A | `web-fetcher` | EVERY URL to fetch or verify |
| Extra B | `search-first` | Before writing new code/script/utility |
| Extra B | `deep-research` | Multi-source citation research (firecrawl + exa MCP) |

**Internal CLAUDE.md-triggered skills (outside global registry):**

| Skill | When to use |
|-------|-------------|
| `git-workflow` | EVERY git operation (commit, push, branch, PR) |
| `flow-graph` | Sequence diagram, protocol flow, handshake diagram |
| `quality-gate` | EVERY write/edit/commit (pre-flight, see Rule 6 above) |

---

## Preferences

- Accuracy first. Double-check, cross-reference multiple sources.
- No AI writing patterns. Professor/PhD teaching style.
- No emoji in technical content.
- Real examples with verifiable output.
- Concise but deep. Analyst/engineer tone, not mechanical.
- Vietnamese for documentation content (curriculum); English for CLAUDE.md and `memory/*` (working files).
