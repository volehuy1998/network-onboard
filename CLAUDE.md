# Project Memory, network-onboard

> **CRITICAL.** Read this entire file BEFORE doing anything. This file is the project's working memory, committed to git, and synchronised across machines.

> **Language convention (updated 2026-04-29 per Rule 17 below).** This file (CLAUDE.md), every working file under `memory/*`, every plan file under `plans/*`, and every curriculum file under `sdn-onboard/*.md` and `haproxy-onboard/*.md` must be written in plain technical English. The audience for the curriculum is Vietnamese network engineers reading at CEFR B2 to C1 level. Style policy is defined in `memory/shared/english-style-guide.md`. Plan v3.12 closed on 2026-04-29; all `sdn-onboard/*.md` files are full English (lang_check PASS across 136 files, 30,265 prose chunks, zero non-English). Cross-block surface (`sdn-onboard/_templates/*.md` and `haproxy-onboard/*.md`) remains legacy Vietnamese until the cross-block follow-on plan closes; the few sdn-onboard files in the prior mixed transition state carry a `**Language status:**` callout per plan v3.9.1 §8.3 retained as a future-proofing convention. Files under `linux-onboard/*.md` and `network-onboard/*.md` are out of the active migration scope and may stay as-is.

> **No em-dash anywhere in the repository (Rule 17).** The em-dash character (Unicode U+2014, the long horizontal dash) is forbidden. Use a comma, a period, a colon, parentheses, or a bulleted list instead. Pre-commit hook `scripts/em_dash_check.py` enforces this.

---

## North Star, Do Not Drift

> **Core mission.** Build a learning roadmap and curriculum that takes a learner from foundation to advanced **Open vSwitch + OpenFlow + OVN**. The learner outcome is a deep understanding of **structure, architecture, and hands-on operation** of these three technologies.
>
> **Top priority: foundational depth first.** The foundation must be rock-solid before any advanced topic is added. When choosing between "add a new advanced part" and "expand an existing foundation part for more depth", always choose the latter. The curriculum already has 116 files, 20 blocks, and roughly 55,700 lines; every future addition must justify itself as **strengthening the foundation**, not as breadth expansion.

**In scope (focus areas):**

- OVS internals: kernel and userspace datapath, megaflow cache, classifier (TSS), `ofproto-dpif` xlate, revalidator, upcall, OVSDB, `ovs-vswitchd` architecture.
- OpenFlow 1.0 to 1.5: full specification, match field catalog, action catalog, instruction set, group table, meter, bundle, OXM TLV, multi-table pipeline.
- OVN: NBDB schema, `ovn-northd` compile, SBDB intermediate, `ovn-controller` per chassis, `br-int` OpenFlow translation, `Logical_Switch` and `Logical_Router` pipeline, all 8 `Port_Binding` types, `Load_Balancer`, ACL, conntrack, NAT, BFD and `HA_Chassis_Group`.
- Overlay (Geneve, VXLAN, GRE) only insofar as OVS and OVN use them as tunnels.
- Tools mastery: `ovs-vsctl`, `ovs-ofctl`, `ovs-dpctl`, `ovs-appctl`, `ovn-nbctl`, `ovn-sbctl`, `ovn-trace`, `ofproto/trace`, `ovn-detrace`.
- Debug, troubleshoot, forensic, and daily operator playbook (incident decision tree, anatomy template, post-mortem of engagement).

**Permanently banned from the plan (since the consolidated owner directive of 2026-04-25):**

> **Owner directive (translated from Vietnamese original, 2026-04-25):** *"Permanently remember that anything related to advanced technologies such as DPDK, BPF, XDP, BGP, and Kubernetes will never appear in the plan unless I change my decision."*

This is **not** a low-priority topic classification. It is a **permanent ban from active planning**. The following topics are excluded from "next direction" options, sprint plans, audit upgrade priorities, and "future work" suggestions:

- **DPDK** (PMD threads, mempool, hugepage, NUMA tuning, fast-path internals).
- **BPF and eBPF** (datapath alternatives, classifier programs, libxdp, Cilium internals).
- **XDP and AF_XDP** (eXpress Data Plane, kernel bypass alternative to OVS datapath).
- **BGP-related content** (BGP EVPN, regular BGP routing, FRR BGP, OVN-BGP-Agent).
- **Kubernetes** (kube-proxy, OVN-Kubernetes specific, CNI plugin chain, service mesh control plane).

**Existing content stays as it is** (no revert): 9.3 DPDK and AF_XDP, 9.5 hardware offload, 11.2 BGP EVPN tier 2, 14.x P4 (less impacted), 15.x service mesh and Kubernetes, 16.x DPDK and AF_XDP, 17.0 / 18.0 / 19.0 OVN advanced. These were written before the ban and remain readable; they are not subject to further expansion.

**Rules for ongoing work:**

1. **Never propose** these topics in "next direction" options. Even if a topic is technically in scope per topic taxonomy, it is out per owner directive.
2. **Do not plan** sessions, sprints, or phases targeting these topics.
3. **Do not mention** them as "candidates" or "future work" or "deferred" in proposals. Just exclude them entirely.
4. If a part touches these topics tangentially (for example, 13.11 LR mentions FRR BGP), keep the mention to one or two sentences high-level and cross-link to the existing part. Do not deep-dive further.
5. When auditing shallow files for upgrade priority, exclude these from the candidate list (9.3 DPDK and AF_XDP, 15.x deferred files, 11.2 partial sections, and similar).

**Override condition:** only if the owner explicitly says "add DPDK" or an equivalent explicit reversal. Anything weaker means the ban remains.

**Active plan hierarchy (4 tiers, advanced topics not represented):**

1. **Highest** = OVS, OpenFlow, OVN core internals (datapath, classifier, conntrack, ofproto, OVN northd, controller, binding, NBDB, SBDB, Geneve as an OVN tunnel).
2. **High** = Tools mastery and debug pedagogy (CLI playbook, Anatomy Template A, troubleshooting decision tree).
3. **Medium** = Foundation prerequisites (Linux netns, bridge, veth, tc, conntrack), OVSDB foundation.
4. **Low** = History and narrative (Block II, Block III), data centre applied content (Block XII).

Block XV (Cloud Native) was officially deprioritised on 2026-04-23 and reaffirmed by the 2026-04-25 ban. Files 15.1 and 15.2 are deferred indefinitely. P4 and service mesh content remain in existing files but are not subject to expansion.

Memory pointer: [`memory/feedback_advanced_topics_permanent_ban.md`](memory) is auto-loaded each session.

**Self-check before writing a new part or expanding a section:**

> *"Does this topic make the engineer better at OVS, OpenFlow, or OVN? If it only makes them better at Kubernetes, DPDK, or XDP, it is out of scope."*

When in doubt, stop and ask the user before proceeding. Out-of-scope detours bloat the curriculum and dilute focus.

---

## Second North Star, Quality Over Speed

> **Owner directive (translated from Vietnamese original, 2026-04-25):** *"What I need is quality, meticulousness, care, and reasonableness. The amount of time or effort spent does not matter to me at all."*
>
> *"I value accuracy, clear explanation, meticulousness, and care over speed. For example, working at speed loses quality."*

**Translation of intent:** the owner values **accuracy, clear explanation, meticulousness, and caution** above all. Speed is explicitly not a goal. Working fast trades away quality, which is unacceptable.

**Operating principles:**

1. **Verify, never estimate.** When the user asks for a count, statistic, or status, run `wc -l`, `grep`, `git log`, or the relevant MCP API. Do not guess from memory or extrapolate from prior context. State the verified number.
2. **Explain why before what.** When introducing a concept or recommending an action, lead with the reasoning, then the conclusion. The reader needs the *why* to internalise, not just the procedure.
3. **Read the file before editing.** Always read the actual current state before Edit or Write. Do not rely on a cached mental model from earlier in the session. The file may have been modified by a linter, by the user, or by an earlier AI step.
4. **Check every URL before adding it.** Use `web-fetcher` or `curl -I`. Dead URLs are silent quality bugs that surface much later.
5. **Cross-reference upstream source.** For every commit SHA, function name, file path, line number, or schema claim, verify via the local upstream repository or via MCP GitHub (Rule 14). Do not cite from memory.
6. **Pre-flight checklist before commit.** Run Rule 6 Checklist B (before write) and Checklist C (before commit) every single time. Do not skip.
7. **When asked to be fast, refuse politely.** If a user request implies speed (for example, "quick fix" or "just commit it"), the response is to acknowledge but still do the careful version. Speed is not a valid trade-off.
8. **One commit per logical unit.** Do not bundle unrelated changes. Each commit should be reviewable in isolation, with a clear scope statement.

**Anti-pattern signals (you are slipping into speed mode if you are):**

- Skipping Read before Edit "because the file was just shown".
- Citing line numbers from memory instead of verifying.
- Writing a paragraph of conclusions before reading the source they are about.
- Batching three unrelated fixes into one commit "to save commits".
- Dropping pre-commit checklists "because nothing seems risky".
- Estimating instead of measuring.

When you catch yourself doing any of these, stop and restart the step the careful way.

---

## Owner

VO LE (volehuy1998@gmail.com), computer network engineer. Areas of work: OpenStack and kolla-ansible, SDN, OVN, OVS research.

---

## Repository Structure

```
network-onboard/                    (repo root, GitHub: volehuy1998/network-onboard)
|-- CLAUDE.md                       (this file, working memory)
|-- README.md                       (parent README, entry point for the repo)
|-- CHANGELOG.md                    (release notes, Keep a Changelog format)
|-- memory/                         (deep memory: state trackers, dictionaries, audit summaries)
|   |-- MEMORY.md                   (auto-memory index, hooks into Claude)
|   |-- session-log.md              (session by session log, append only)
|   |-- file-dependency-map.md      (Rule 2 cross-file sync map)
|   |-- sdn-series-state.md         (per-part status tracker, Rule 5 handoff)
|   |-- audit-index.md              (table of contents of audit reports)
|   |-- audit-2026-04-25-summary.md (consolidated audit findings, latest)
|   |-- english-style-guide.md      (English style policy, plan v3.9.1 Phase Q-1.A)
|   |-- rule-11-dictionary.md       (legacy Vietnamese-to-English translation reference, frozen 2026-04-28)
|   |-- lab-verification-pending.md (exercises pending lab host)
|   `-- haproxy-series-state.md
|-- sdn-onboard/                    (SDN onboard series, English with transitional Vietnamese sections per Rule 17)
|-- haproxy-onboard/                (HAProxy onboard series, English with transitional Vietnamese sections per Rule 17)
|-- linux-onboard/                  (Linux and RHCSA onboard series, out of active migration scope)
|-- network-onboard/                (Network and CCNA onboard series, out of active migration scope)
|-- references/                     (shared references)
`-- images/                         (shared images)
```

---

## Mandatory Rules

The repo has 6 skills installed at `~/.claude/skills/`. All 6 must be used; do not skip any when the activation condition holds.

### Rule 1: Skill Activation Sequence (mandatory)

**Group A, Core 4 (always active for any interaction with `.md` files):**

1. `professor-style`: tone control, conceptual structure (six criteria 2.1 to 2.6).
2. `document-design`: layout, headings, learning elements.
3. `fact-checker`: verify every technical claim before commit.
4. `web-fetcher`: verify every URL before adding to documentation.

**Group B, 2 conditional (consider before skipping):**

5. `search-first`: before writing new code, script, or utility. Adopt before extend before compose before build.
6. `deep-research`: when content needs multi-source citation beyond offline `doc/*` (firecrawl and exa MCP).

**Workflow.** When you open a `.md` file to write, edit, or audit, activate Core 4 immediately. Before writing helper code, activate `search-first`. Before writing content that needs multi-source research, activate `deep-research`. Record activated skills in the fact-forcing gate answer. Do not write content first and then review afterwards. Always: read skill, write, self-audit.

(Origin: 2026-03-30 audit miss; 2026-04-22 added Group B.)

### Rule 2: Cross-File Sync (mandatory)

Before commit, consult `memory/shared/file-dependency-map.md` to identify dependent files.

**Process:** identify the file being edited, look up the dependency map, check related files, update all related files in the same commit.

(Origin: parent `README.md` was left stale after `haproxy-onboard/README.md` version bump.)

### Rule 3: Version Annotation Convention

When writing content with HAProxy version differences, use the callout `> **Version note:** <difference>`. Also update `haproxy-onboard/references/haproxy-version-evolution.md` with a new entry.

### Rule 4: Git Workflow

- Protected branch: do not push directly to `main` or `master`.
- Commit convention: Conventional Commits (`feat()`, `fix()`, `docs()`).
- Branching: GitHub Flow (main plus feature branches).
- Read the `git-workflow` skill before any git operation.

### Rule 5: Session Handoff Protocol

**On session end (or when the user says "stop", "pause", or "end"):**

1. Update `memory/shared/session-log.md` with date and time, what was done (commits, files), what is pending, the current branch and state, and the commands the user must run locally (for example, `git push`).
2. Update `memory/sdn/series-state.md` if any part status has changed.
3. Commit memory changes.

**On session start:**

1. Read CLAUDE.md (this file).
2. Read `memory/shared/session-log.md` (last session context).
3. Read `memory/sdn/series-state.md` (curriculum status).
4. Run `git status`, `git branch`, `git log`.
5. Tell the user: "I have read context. Last session [summary]. Pending: [list]."

### Rule 6: Quality Gate, Pre-flight Checklist (mandatory)

**Checklist B, before writing, editing, or auditing `.md` or `.svg`:**

1. Activate `professor-style` skill (six criteria 2.1 to 2.6).
2. Activate `document-design` skill (chapter template, heading rules, English style guide).
3. Identify the file being edited.
4. Look up `memory/shared/file-dependency-map.md`, list related files (including Tier 5: SVG to markdown).
5. Read related files for current content.
6. If editing SVG: grep all `.md` referencing the SVG, read current captions, note entities.
7. Start writing or editing (not before steps 1 to 6).
8. If editing SVG: update the caption immediately after SVG completion, before any other task.

**Checklist C, before commit:**

1. Fact-check: list every technical claim, verify each.
2. URL check: list every URL, verify with `web-fetcher` or `curl`.
3. Cross-file sync: check the dependency map.
4. Version annotation: cross-version content gets a callout and a tracker entry.
5. SVG spacing and diacritics: run `svg-audit.py` and `diacritics-audit.py`. Zero violation.
6. SVG-to-caption consistency: run `svg-caption-consistency.py`. Zero mismatch.
7. File integrity: run the null byte check (Rule 9) on every modified text file. Zero null bytes.
8. English style lint: no abbreviations such as `e.g.`, `i.e.`, `etc.`, `vs.`, `spec`, `config`, `info`, `repo`, or `dev` in newly written prose. See `memory/shared/english-style-guide.md` rule 3.2 for the full list.
9. Language detection check: run `scripts/lang_check.py --staged`. The script must report PASS, meaning every prose chunk in every staged Markdown file is detected as English by the lingua-py binary classifier. Any chunk detected as Vietnamese with non-zero confidence rejects the commit. CLI commands inside fenced code blocks or backticks are skipped automatically. See `memory/shared/english-style-guide.md` rule 4 and Rule 17 below.
10. Language status callout: if the file is in mixed-language transition state, the `**Language status:**` callout immediately after the H1 heading lists the now-English sections. See plan v3.9.1 §8.3.
11. Em-dash count: zero. The pre-commit hook `scripts/em_dash_check.py` enforces this. Replace any em-dash with a comma, a period, a colon, parentheses, or a bulleted list.
12. Read the `git-workflow` skill before commit.
13. Self-audit `professor-style` six criteria on new content.
14. Lab verbatim check: if any staged file is under `sdn-onboard/labs/` or quotes lab output, run `python scripts/lab_verbatim_check.py --staged`. PASS required. See Rule 18.

**Checklist E, when adding a new part:**

1. Run Checklist B.
2. Create the file with the naming convention `X.0 - <name>.md`.
3. Header block and learning objectives per `document-design`.
4. Update `README.md` (table of contents, dependency graph).
5. Update `memory/sdn/series-state.md`.
6. Update `memory/shared/file-dependency-map.md`.
7. Run Checklist C.

Principle: this is pre-flight, not bureaucracy. Two to three minutes of overhead; the cost of a sync bug is much higher.

### Rule 7: Terminal Output Fidelity (mandatory)

When the user provides real terminal output to insert into documentation:

1. Do not trim, shorten, or omit any line.
2. Do not reorder lines.
3. Do not change spacing, indentation, or any character.
4. When comparing output: line by line diff, not just the value of interest.
5. To shorten output: ask the user first, naming which lines to drop and why.

This applies to: `fdinfo`, `lsof`, `ss`, `strace`, `tcpdump`, `haproxy -vv`, log files, and any user-provided output.

#### Rule 7a: System Log Absolute Integrity (no exceptions)

System logs (daemon and service logs, diagnostic tool output) follow stricter rules than Rule 7:

1. Absolutely no truncation, even of UUID, path, or IP.
2. Absolutely no merging of multiple log lines into one entry.
3. Absolutely no deletion of log lines, even if they look "repetitive" or "unimportant".
4. Absolutely no timestamp modification, not even by 1 millisecond.
5. No exceptions. System log is forensic evidence.
6. When presenting a log in another format (timeline, table, annotated block): the message body after the prefix must stay verbatim on its own line; annotations go on separate lines prefixed with `--`.
7. When showing a subset: include the line `[N other lines omitted, context: ...]`.

Scope: every daemon and service log (`ovn-controller`, `ovs-vswitchd`, `nova-compute`, `neutron-server`, `haproxy`, `nginx`, `journald`, `syslog`, `dmesg`) and every diagnostic tool output (`tcpdump`, `strace`, `lsof`, `ss`, `conntrack`, `ovs-ofctl`, `ovn-trace`, `ovn-detrace`).

(Origin: 2026-04-11. The SDN 1.0 timeline merged three separate log lines, truncated a UUID, deleted "Claiming unknown" lines, and modified a timestamp from `.947` to `.948`.)

### Rule 8: Sentence Completeness (mandatory)

Every clause must be complete on its own; do not lean on implicit context. This rule is the English equivalent of the previous Vietnamese-specific Rule 8 (retired 2026-04-28 per Rule 17).

1. Negation cannot dangle. "not", "never", "no longer" must come with a clear verb or object.
2. Demonstratives are unambiguous. "this", "that", "it" must have a clear antecedent in the same or adjacent sentence; otherwise repeat the noun.
3. Standalone-read test: after writing each sentence, read it isolated from context. If the meaning is unclear, rewrite.

(Origin of the original Vietnamese Rule 8: 2026-04-04, a dangling negation in Vietnamese prose at the end of a clause without an object. The English Rule 8 was adopted on 2026-04-28 per `memory/shared/english-style-guide.md` §2.)

### Rule 9: File Integrity, Null Byte Prevention (mandatory)

Before `git add`:

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

If null bytes are found, strip with:

```bash
python3 -c "d=open('FILE','rb').read(); open('FILE','wb').write(d.replace(b'\x00',b''))"
```

Verify: `grep -cP '\x00' FILE` must return 0.

Scope: every text file (`.md`, `.py`, `.sh`, `.yml`, `.html`, `.svg`, `.css`, `.js`). Null bytes in text files are always a bug. Binary files (`.png`, `.jpg`, `.pdf`) are exempt.

Warning signs: the `file` command says "with very long lines" on `.md`; abnormally large file size compared with line count; GitHub renders the file as binary.

(Origin: commit `9a17eec` had 3,612 trailing null bytes; GitHub refused to render the markdown.)

### Rule 10: Architecture-First Doctrine (historical)

This rule applied during the architecture phase (now complete; the project has been in the content phase since session 12). For historical record only. The skeleton-first discipline still applies when introducing brand-new blocks.

(Originally written 2026-04-21 to constrain over-eager content writing during the skeleton phase.)

### Rule 11: Vietnamese Prose Discipline (retired 2026-04-28)

This rule is retired per Rule 17. It defined how to choose between Vietnamese and English in curriculum prose, including a keep-as-is identifier list, a translation dictionary, and same-word-different-context guidance.

The keep-as-is identifier list is preserved verbatim in `memory/shared/english-style-guide.md` rule 3.3 and is still authoritative for naming conventions.

The dictionary at `memory/shared/rule-11-dictionary.md` is partially consumed by plan v3.12 (sdn-onboard slice closed 2026-04-29); it is preserved as a translation reference for the cross-block follow-on plan (`_templates/` plus `haproxy-onboard/`).

For new writing, follow the English style guide at `memory/shared/english-style-guide.md` instead of this rule.

(Origin: session 13, 2026-04-21, initial codification; sessions 22 to 23 broadened. Retired 2026-04-28 per plan v3.9.1 Phase Q-1.C.)

### Rule 12: Exhaustive Offline Source Exploration (mandatory)

Before writing any onboard content, inventory all offline sources via recursive Glob:

```
Glob "sdn-onboard/doc/**/*"
Glob "haproxy-onboard/doc/**/*"
Glob "linux-onboard/doc/**/*"
Glob "network-onboard/doc/**/*"
Glob "references/**/*"
```

**Process:**

1. At session start, run a recursive Glob, list files in `*/doc/**` and `references/**`. Build a mapping from offline file to the block or part using it.
2. Before each Write, list relevant `doc/*` files for the topic. Cite each one explicitly in the fact-forcing gate, the header block, and the References section.

**Violation signals:**

- The fact-forcing gate answer is missing the "Offline source providing content" line.
- The file header is missing `> **Primary offline source:**`.
- The References section is missing the offline source entry.
- The author is writing technical content without a `doc/*` citation when the topic is covered.

(Origin: session 14, 2026-04-22, missed `sdn-onboard/doc/ovs/` (eleven PDF and TXT files) when writing Block VII and Part 9.0.)

### Rule 13: Em-dash Discipline (retired 2026-04-28)

This rule is retired per Rule 17. It used to define a density target of fewer than 0.10 em-dashes per line for curriculum prose. The new rule is stricter: zero em-dash anywhere in the repository.

For the current rule, see Rule 17 below and `memory/shared/english-style-guide.md` rule 4. Pre-commit enforcement is `scripts/em_dash_check.py`.

(Origin: session 24, 2026-04-23, detected 361 em-dashes across four Phase D files at density 0.13 to 0.19 per line. Retired 2026-04-28 per plan v3.9.1 Phase Q-1.C.)

### Rule 14: Source Code Citation Integrity (mandatory)

Every reference to upstream source code (OVS, OVN, Linux kernel, HAProxy, Nginx, OpenStack, DPDK, FRR, strongSwan, P4, Cilium) must be verified via the local upstream repository or MCP GitHub before commit.

#### 14.1. Commit SHA reference

- Verify existence: `git log -1 <sha>` on the local repo, or `mcp__github__get_commit(owner, repo, sha)`.
- Verify claims match: author, date, message, files changed.
- Inline cite: 8 to 12 characters of the SHA prefix. The References section uses the 40-character full SHA.
- Inline SHA and References-section SHA must match (grep before commit).

#### 14.2. Function name reference

- Verify existence: in the local upstream repo with `git checkout <baseline-tag>` then `grep -nE "^<fn>" <path>`. The `^<fn>` anchor matches the function definition (column 0) per OVS coding style. Equivalent MCP form: `mcp__github__search_code(query="function_name repo:owner/repo")` with a fallback to `mcp__github__get_file_contents` plus a manual grep.
- Preserve the exact source spelling, even typos. Example: OVN source has `reply_imcp_error_if_pkt_too_big` (typo `imcp`). Do not "fix" it to `icmp` when citing. Annotate `(upstream typo imcp)` if it might confuse readers.
- If a function was renamed across versions, annotate the rename: `(named foo_bar in v22.03, renamed to bar_foo since v24.03 via commit abc1234)`.

#### 14.3. File path reference

- Verify existence at the version baseline: `git show <baseline>:<path> | head -1` on the local repo, or `mcp__github__get_file_contents(path, ref)` with `ref` set to the curriculum baseline tag (for example, `v22.03.8` for OVN, `v2.17.9` for OVS, `v5.15` for the Linux kernel matching Ubuntu 22.04).
- If a file migrated across versions, annotate per Rule 3. Example: `controller/mac-learn.c` (v22.03 to v24.03) or `controller/pinctrl.c` `MAX_FDB_ENTRIES` (v24.09 and later, commit `fb96ae3679`).

#### 14.4. Line number reference

Line numbers are version-sensitive. Mandatory annotation, choose one:

- **Option A** (branch-specific): `physical.c` lines 1939 to 1968 (OVN branch-24.03).
- **Option B** (commit permalink): `physical.c` link to the GitHub blob at the commit SHA (`https://github.com/ovn-org/ovn/blob/SHA/controller/physical.c#L1939-L1968`).
- **Option C** (function name anchor, recommended): instead of a line, use the function name as a stable anchor. Example: "In function `build_lswitch_arp_nd_responder_known_ips` in `northd/northd.c`, find the `op->lsp_has_port_sec || !op->has_unknown` check".

Line drift is common: from v22.03 to `main` typically shifts more than 2,000 lines. Option C is best practice.

#### 14.5. Verbatim commit body quote

- Copy and paste exactly from the API response or `git log` output. Do not translate, do not edit spacing, do not change bullet format.
- A block labelled `> "Verbatim commit body from GitHub API:"` must be 100 percent English if the commit body is English.
- Translate only with an explicit "paraphrase" label. Do not use the "verbatim" label on a paraphrase.
- Dash bullets (`-`) preserve exactly; do not convert to `(a) (b) (c)`.

#### 14.6. Database table and schema claim

- Verify schema existence via `mcp__github__get_file_contents` for `ovn-sb.ovsschema`, `ovn-nb.ovsschema`, `vswitchd/vswitch.ovsschema`.
- Parse the JSON to list the actual tables and columns.
- Do not fabricate table names. If a feature stores data in an `other_config` map instead of a dedicated table, say so.
- An internal C struct is not a database table. Distinguish clearly. Example: `struct chassis_features` in memory differs from a hypothetical `Chassis_features` OVSDB table.

#### 14.7. Pre-commit audit pass

- Grep every new claim in a section: SHA, function, path, line number, table name.
- If there are more than three references in a section, run a verification batch (verify all).
- Log evidence in `memory/fact-check-audit-YYYY-MM-DD.md`.
- Commit only when 100 percent pass; any failed reference must be fixed or removed.

(Origin: sessions 32 to 33i, 2026-04-22, found 32 issues across six categories on 43 files; codified Rule 14 in commit `7e5608b`.)

### Rule 15: No Self-Tag (mandatory)

> **Mirror governance principle GP-1.** Full text in [`memory/sdn/governance-principles.md`](memory/sdn/governance-principles.md) Section 1. CLAUDE.md summarises enforcement.

The SDN curriculum must not be tagged with any release version (v3.x, v4.x, vX.Y) until all four conditions below are met simultaneously:

1. **Scorecard committed:** every keyword in scope of REF has a 20-axis scorecard in the repository, version controlled.
2. **Threshold achieved:** every keyword meets the minimum threshold per Phase B rubric (Cornerstone DEEP-20, Medium DEEP-15, Peripheral PARTIAL-10).
3. **Audit script run and report committed:** `scripts/per_keyword_rubric_audit.py` ran successfully; the scorecard is fresh within 24 hours of the commit.
4. **User written sign-off:** explicit user confirmation (chat message, commit message, or plan tracker entry) approves the tag.

**Pre-tag checklist (mandatory):**

- [ ] Run the audit script; commit the scorecard.
- [ ] Verify threshold met (script exit 0).
- [ ] Verify scorecard timestamp is within 24 hours of HEAD.
- [ ] User sign-off captured in the commit message.
- [ ] Tag annotated message references the scorecard commit SHA.

**Exception (hotfix only):**

- Security CVE upstream affecting keyword treatment.
- Factual error correction (wrong commit SHA, typo in code citation).
- Typo or formatting fix in existing content.
- Must have user explicit approval, rubric impact assessment, and follow-up regression audit within seven days.

**No other exceptions.** "Quick win", "milestone", or "checkpoint" tags are not allowed.

(Origin: 2026-04-26 reckoning. The v3.6-ContentDepth tag was issued after one session with a "Tier A MISSING <= 50" acceptance gate that measured breadth, not depth. The user checked thirteen criteria and exposed the tag as misleading. Plan v3.7 codified governance to prevent recurrence. See [`memory/sdn/governance-principles.md`](memory/sdn/governance-principles.md) for the full GP-1 text and four sister principles.)

### Rule 16: Internal-vs-Reader-Facing Language Separation (mandatory)

> **Mirror governance principle GP-11.** Full text in [`memory/sdn/governance-principles.md`](memory/sdn/governance-principles.md) Section 16. CLAUDE.md summarises enforcement.

Curriculum content (`sdn-onboard/*.md`, `haproxy-onboard/*.md`, `linux-onboard/*.md`, `network-onboard/*.md` are reader-facing for the engineer learning SDN) must not contain internal terminology of the plan, rubric, or governance.

**Forbidden patterns inside curriculum files:**

- `**Axis N <category>.**` (rubric label). Use a natural English heading instead, for example `**Concept.**`, `**How it works.**`, `**Importance.**`.
- `Axis 1` through `Axis 20` (numbered reference). Use the natural English category name.
- `cohort C7`, `cohort M5`, `cohort P21` (triage label). Skip, or write "the group of <description>".
- `Phase G batch N`, `Phase R2`, `Phase R3`, `Phase R4` (plan reference). Skip, or write "expansion of 2026-04".
- `DEEP-20`, `DEEP-15`, `PARTIAL-10`, `REFERENCE-5`, `PLACEHOLDER` (tier label). Skip, or use prose such as "comprehensive coverage", "fairly comprehensive coverage".
- `rubric 20-axis`, `rubric 13-criteria` (meta term). Skip.
- `anti-gaming`, `gaming pattern`, `cosmetic stamp`, `cohort stamp` (governance term). Skip.
- `GP-1` through `GP-12` (governance reference). Skip.
- `Form A per GP-6`, `Form B per GP-6` (commit pattern reference). Skip.

**Replacement table for 20-axis treatment using natural English headings:**

| Internal axis label | Reader-facing English heading |
|---------------------|--------------------------------|
| Axis 1 Concept | Concept |
| Axis 2 History | History and background |
| Axis 3 Placement | Position in the architecture |
| Axis 4 Role | Role |
| Axis 5 Motivation | Why it exists |
| Axis 6 Problem | Problems it solves |
| Axis 7 Importance | Importance |
| Axis 8 Mechanism | How it works |
| Axis 9 Engineer-op | How an operator masters this |
| Axis 10 Taxonomy | Classification |
| Axis 11 Workflow | Usage workflow |
| Axis 12 Troubleshoot | When something goes wrong |
| Axis 13 Coupling | Tightly related to |
| Axis 14 Version drift | Version differences |
| Axis 15 Verification | Observation and verification |
| Axis 16 Source code | Source code reference |
| Axis 17 Incident | Real-world incident |
| Axis 18 Lab | Synthetic exercise |
| Axis 19 Failure mode | Common failures and diagnostic signals |
| Axis 20 Cross-domain | Comparison with other systems |

**Allowed exceptions:**

- `memory/*` and `plans/*` (working and meta audience).
- `CLAUDE.md` and `CHANGELOG.md` "Reckoning" sections (meta history).
- `0.3 - master-keyword-index.md` may use the status code `DEEP / BREADTH / SHALLOW / MISSING / PLACEHOLDER` per existing convention.
- Commit messages (internal audit log audience).

**Enforcement:**

- Pre-commit hook `scripts/rubric_leak_check.py` rejects violations.
- Phase R0.7 curriculum cleanup pass: replace existing leaks (about 25 files from Phase G v3.7).
- Self-check before each curriculum edit: read the replacement table above.

**Pre-commit enforcement:** [`scripts/rubric_leak_check.py`](scripts/rubric_leak_check.py) v2.1 (22 patterns total, 13 from v1, 7 from v2, 2 from the v2.1 amendment) detects six v2 pattern families after the audit of 2026-04-27: axis-numbered Vietnamese heading (an `### N. <axis label>` heading written in Vietnamese), cohort cornerstone phrase, tier cornerstone informal or bold prose, tier importance prose, Phase H session reference, cohort batch stamp leftover, stale Phase B compatibility note (em-dash variant). See plan v3.9-OVSBlockHotfix Phase S0 and S0.5 for the full pattern list and test suite.

(Origin: 2026-04-26. The user audit caught the agent team inserting `**Axis N**` labels into curriculum content, which confuses the engineer reader. Plan v3.8-Remediation Section 11 amendment plus GP-11 codified the rule. The 2026-04-27 master audit of the OVS block expanded the scope to seven additional patterns following the v2 to v2.1 amendment per plan v3.9.)

### Rule 17: English as the Mandatory Explanation Language (mandatory)

Every explanatory prose text written or modified in this repository, including curriculum files (`sdn-onboard/*.md`, `haproxy-onboard/*.md`), working files (CLAUDE.md, `memory/*`), plan files (`plans/*`), audit logs, and commit messages, must be written in plain technical English per the style guide at [`memory/shared/english-style-guide.md`](memory/shared/english-style-guide.md).

**No Vietnamese in newly written content.** Any Vietnamese passage that appears in a file modified after 2026-04-28 is replaced with English in the same commit. Verbatim quotes of an owner directive that was originally given in Vietnamese are translated to English with the attribution "Translated from Vietnamese original, dated YYYY-MM-DD". The Vietnamese source text is preserved in git history (the commit before the translation) for auditability.

**One narrow scoped allowance.** The historical dictionary at `memory/shared/rule-11-dictionary.md` (which lives outside the named scope, in `memory/`) keeps its bilingual body as a translation reference for the cross-block follow-on plan (5 `sdn-onboard/_templates/*.md` files plus 2 `haproxy-onboard/*.md` files). Its header is in English and now marks the file as `PARTIALLY CONSUMED by plan v3.12 (sdn-onboard slice closed 2026-04-29)`.

**Transition status for legacy files.** Plan v3.12 closed on 2026-04-29; all `sdn-onboard/*.md` files are full English. Cross-block surface (`sdn-onboard/_templates/`, `haproxy-onboard/`) remains legacy until the cross-block follow-on plan closes. The `**Language status:**` callout convention from plan v3.9.1 §8.3 is preserved as a future-proofing pattern for any future mixed-language transition state; no `sdn-onboard/*.md` file currently carries it after v3.12 closure.

**Em-dash discipline.** The em-dash character (Unicode U+2014, the long horizontal dash with the width of approximately one M) is forbidden anywhere in the repository, including curriculum, CLAUDE.md, memory files, plans, and commit messages. Use a comma, a period, a colon, parentheses, or a bulleted list instead. This supersedes the previous Rule 13 density-based discipline.

**Pre-commit enforcement.** Two scripts enforce Rule 17 at commit time:

1. `scripts/em_dash_check.py` (added by plan v3.9.1 Phase Q-1.B) rejects any staged file containing an em-dash in newly added or modified lines.
2. `scripts/lang_check.py` (added by plan v3.9.1 Phase Q-1.B follow-up) runs the lingua-py language detector on every prose chunk in every staged Markdown file. Strict mode: any chunk detected as Vietnamese with non-zero confidence rejects the commit. CLI commands inside fenced code blocks and backtick-wrapped inline code are skipped before detection, so labs and CLI examples do not trigger false positives. The pass criterion is "100 percent English, zero non-English" per the user directive of 2026-04-28.

**Plan-level enforcement.** Every plan file under `plans/*` must include a `lang_check.py` step in its acceptance gate. Specifically, the final-audit phase of any plan (for example, Phase Q8 of plan v3.9.1) runs `python scripts/lang_check.py --all` and the plan cannot close until the check returns PASS. New plans authored after 2026-04-28 must add this step explicitly when defining their acceptance criteria.

**Pedagogical requirement.** The English prose must remain accessible to Vietnamese network engineers reading at CEFR B2 to C1 level. Use short declarative sentences. Use plain vocabulary. Do not abbreviate (`for example`, not `e.g.`; `that is`, not `i.e.`; `and so on`, not `etc.`). Preserve the why-before-what pedagogy from the Second North Star. See `memory/shared/english-style-guide.md` for the full style policy.

(Origin: 2026-04-28, three consecutive owner directives. First, "every file modified by v3.9.1 must have its prose explanation rewritten in English". Second, "no em-dash allowed". Third, "CLAUDE.md and all training documents must be written in English without Vietnamese". Codified by plan v3.9.1 Phase Q-1.C.)

### Rule 18: Lab Output Verbatim Integrity (mandatory, extends Rule 7 and Rule 7a)

When the curriculum includes the output of a hands-on lab session run on a real lab host (for example, `lab-openvswitch` at `192.168.1.250`), every artifact captured from the lab host appears in the documentation exactly as it appeared on the host. Not a single character is modified, omitted, or rewritten.

Specific mandatory practices:

1. The shell prompt is preserved exactly. `root@lab-openvswitch:~#` is not shortened to `# `, not anonymised to `root@<HOST>:~#`, not coloured.
2. Lab IPs (`192.168.1.250` and so on), MAC addresses, hostnames, network device names (`ens33`, `ens36`, `br0`), UUIDs, and OVSDB row UUIDs are preserved character for character. Do not anonymise to `<LAB_IP>`, `<HOST>`, `<UUID>`. The lab is the lab; its identifiers are part of the historical record of the experiment.
3. Log timestamps are preserved to the millisecond.
4. Empty output is preserved as an empty line, with the explicit annotation `(no output)` only when the absence of output is itself the pedagogical point.
5. If the output is too long to embed inline (more than approximately 200 lines), the curriculum file references the full transcript at `sdn-onboard/labs/v3.13-XN-<topic>.typescript` and embeds an annotated extract per Rule 7 with the line `[N other lines omitted, context: full log preserved at <path>]`.
6. Transcripts are captured by `script -f -t` on the lab host and the typescript file is referenced from the curriculum. A diff between the human-readable rendering and the raw typescript must be empty.
7. The pre-commit hook `scripts/lab_verbatim_check.py` (added by plan v3.13 R0) compares the rendered transcript against the referenced typescript and rejects the commit on any divergence.
8. **No synthetic structure inside fenced code blocks.** A fenced code block in a lab transcript contains only real operator commands and the real host output those commands produce. The following are forbidden inside any fenced block under `sdn-onboard/labs/` and inside any curriculum quote of lab output:
   - `echo === ... ===` start-of-session and end-of-session banner markers.
   - `echo --- ... ---` mid-session section banner markers.
   - Any `echo` invocation whose only purpose is to print a section title or scene transition (regardless of the surrounding glyphs).
   - Shell-comment lines such as `# pre-build state on lab-openvswitch` or `# fetch tarball` whose only purpose is to label a section. Even though bash treats them as no-ops, they create visual noise inside the fenced block and force a reader to skip past them to find the next command.
   All structural and pedagogical commentary (section titles, scene-setting paragraphs, "what just happened" wrap-ups) lives outside the fenced block, in the surrounding `.md` prose: H2 / H3 headings introduce each phase, plain paragraphs explain the why and the what. The wall-clock window of the session is captured by `date -u` invocations at session start and end, both of which are real commands producing real host output. Orchestrator scripts that drive lab capture must not send any such banner or comment line; the COMMANDS list contains only real operator commands.
9. **R1.A grandfather clause.** The R1.A apt-distro-install transcript (`v3.13-R1A-apt-distro-install.{md,typescript,timing}`) was captured before this no-synthetic-structure rule was codified and uses both `echo === ... ===` start-end markers and `echo --- ... ---` section banners. Per Rule 18 the R1.A verbatim record is what was actually run; R1.A is left as-is and is the only transcript with this asymmetry. Every transcript from R1.B onward complies with the strict no-synthetic-structure form.

Scope: every lab transcript under `sdn-onboard/labs/`, every curriculum quote of lab output anywhere in `sdn-onboard/*.md`. The rule overrides any stylistic preference. Owner directives of 2026-04-29 and 2026-04-30 (translated from Vietnamese originals):

> 2026-04-29: "All operations, including commands, command outputs, hostnames, and logs, must be kept exactly as they are in the training documentation. No modifications, not even a single word, are allowed, in order to maintain integrity in the actual experiment."
>
> 2026-04-30 (first message): "Please also avoid this phrasing: `root@lab-openvswitch:~# echo --- post-uninstall state ---` ... Instead, use words to explain or comments within the block for easier understanding."
>
> 2026-04-30 (second message): "I no longer like #comments within the quote block; use words to explain it. Putting them there makes it really difficult to follow the command and its output."
>
> 2026-04-30 (third message): "claude.md needs to update its rules to prohibit explanations using comments or echo within the quote block to avoid information overload, as readers only want to see the actual command and output of command."

(Origin: 2026-04-29 owner directive, codified by plan v3.13 R0. Practice 8 and 9 added 2026-04-30 after R1.B's first capture surfaced the no-synthetic-structure rule.)

---

## Current State

| Key | Value |
|-----|-------|
| Branch | `docs/sdn-foundation-rev2`. Latest tag: `v4.1.0-OVNBlockHotfix` (2026-04-28 local, plan v3.10 full closure). Plans v3.11 and v3.12 closed without a tag pending user sign-off per Rule 15. Prior tags: `v4.0-MasteryComplete`, `v4.0.1-OVSHotfix`, `v4.0.3-OVSComprehensiveResolution`. **No remote push per system policy.** |
| Curriculum | 136 files in `sdn-onboard/*.md`, about 95,110 lines, 20 blocks. All v3.8 R0-R6, v3.9 OVS S0-S8, v3.9.1 to v3.9.4 OVS resolution chain, v3.10 OVN block hotfix, v3.11 OF block hotfix, and **v3.12 curriculum-wide English migration (sdn-onboard slice) complete**. lang_check PASS across 136 files (30,265 prose chunks, zero non-English). em_dash_check PASS (zero em-dash). rubric_leak_check inside sdn-onboard scope: zero leak (1 leak in `_templates/template-d-per-table.md` deferred to cross-block follow-on). |
| Active phase | **None. Plan v3.12 closed 2026-04-29 (R0 through R4 complete; R5 tag pending user sign-off per Rule 15).** Next planned: cross-block follow-on plan (`_templates/` plus `haproxy-onboard/`, ~5 to 10 hours). |
| Lab host | Pending (waiting on user). 63 exercises pending verification. |
| HAProxy series | One of 29 parts written. Linux FD doc 1,265 lines. |
| Trackers | [`memory/sdn/series-state.md`](memory/sdn/series-state.md), [`memory/shared/audit-index.md`](memory/shared/audit-index.md), [`memory/shared/session-log.md`](memory/shared/session-log.md), [`memory/sdn/phase-g-progress-tracker.md`](memory/sdn/phase-g-progress-tracker.md) (annotated PARTIAL after the honest audit). |
| Dependency map | [`memory/shared/file-dependency-map.md`](memory/shared/file-dependency-map.md) (Rule 2). |
| Lab pending | [`memory/sdn/lab-verification-pending.md`](memory/sdn/lab-verification-pending.md). |
| Governance | [`memory/sdn/governance-principles.md`](memory/sdn/governance-principles.md) v1.2 (after v3.9 S8.4), 12 governance principles (GP-1 to GP-5 from v3.7, GP-6 to GP-11 from v3.8, GP-12 from v3.9 Post-Tag Regression Audit Cadence). Mirrored in CLAUDE.md Rule 15 and Rule 16. GP-13 to be added by plan v3.9.1 Phase Q12. |
| Past plan v3.12 | [`plans/sdn/v3.12-curriculum-wide-english-migration.md`](plans/sdn/v3.12-curriculum-wide-english-migration.md), closed 2026-04-29 (no tag, pending user sign-off per Rule 15). 278 commits since baseline `1dbfe07`. R0 baseline plus R0.5 roster plus 14 R1 sub-batches (R1.A through R1.N) plus R2 final audit plus R3 CHANGELOG plus R4 dictionary deprecation. 14,523 Vietnamese chunks closed across 136 sdn-onboard files (30,265 prose chunks total scanned, lang_check PASS). Zero em-dash inside sdn-onboard scope. 2 of 3 GP-11 leaks closed (README L155, L156). CHANGELOG Reckoning #9. |
| Past plan v3.11 | [`plans/sdn/v3.11-of-block-source-verify-and-cleanup.md`](plans/sdn/v3.11-of-block-source-verify-and-cleanup.md), closed 2026-04-29 (no tag, pending user sign-off per Rule 15). 9 commits from `288c365` (R0) to `1dbfe07` (R4). 65 source-verify fixes plus 12 GP-11 leaks closed plus 6+ GP-13 rewrites = 77+ deliverables. Combined error rate 2.5 percent across 2,504 inventory candidates. CHANGELOG Reckoning #8. |
| Past plan v3.10 | [`plans/sdn/v3.10-ovn-block-source-verify-and-cleanup.md`](plans/sdn/v3.10-ovn-block-source-verify-and-cleanup.md), closed 2026-04-28 with tag `v4.1.0-OVNBlockHotfix`. 17 commits from `babd05b` (R0) to `62dbfc9` (R5). 126 fixes across 13 files. Combined error rate 3.1 percent across 4,038 inventory candidates. CHANGELOG Reckoning #7. |
| Past plan v3.9.1 | `plans/sdn/v3.9.1-ovs-block-source-verify-hotfix.md`, closed 2026-04-28. Future scheduled: v3.11 OF block hotfix, then cross-block README + templates plan, then v3.12 curriculum-wide English migration. |
| English style guide | [`memory/shared/english-style-guide.md`](memory/shared/english-style-guide.md). Authoring 2026-04-28 plan v3.9.1 Phase Q9. |
| Em-dash check | [`scripts/em_dash_check.py`](scripts/em_dash_check.py). Added 2026-04-28 plan v3.9.1 Phase Q-1.B. Pre-commit hook installed; nine pytest cases pass. |
| Language detection check | [`scripts/lang_check.py`](scripts/lang_check.py). Added 2026-04-28 plan v3.9.1 Phase Q-1.B follow-up. Uses the lingua-py binary classifier (English versus Vietnamese, strict mode). Pre-commit hook installed; eleven pytest cases pass. Library dependency: `pip install lingua-language-detector`. |
| Past plan v3.9 | [`plans/sdn/v3.9-ovs-block-hotfix.md`](plans/sdn/v3.9-ovs-block-hotfix.md), closed 2026-04-27. 24 commits from S0 to S7 plus 5 commits in S8. Actual effort about 27 to 39 hours versus the plan estimate of 60 to 84 hours. |
| Past plan v3.8 | [`plans/sdn/v3.8-remediation.md`](plans/sdn/v3.8-remediation.md), closed 2026-04-26 (R0 to R6 self-claimed complete; the subsequent v3.9 hotfix exposed six categories of issues per Reckoning #3). |
| Past plan v3.7 | [`plans/sdn/v3.7-reckoning-and-mastery.md`](plans/sdn/v3.7-reckoning-and-mastery.md). Phase A to F done. Phase G PARTIAL, about 22 percent (gaming detected). Phase H blocked. Superseded by v3.8-Remediation. |
| Past plan v3.6 | [`plans/sdn/v3.6-content-depth.md`](plans/sdn/v3.6-content-depth.md). Closed (audit tooling and six keyword closure, tag renamed). |
| Past plan v3.5 | [`plans/sdn/v3.5-keyword-backbone.md`](plans/sdn/v3.5-keyword-backbone.md). Closed (placement framework, not mastery). |
| Anti-gaming script | [`scripts/anti_gaming_check.py`](scripts/anti_gaming_check.py). GP-6 to GP-10 enforcement. Pre-commit hook installed. Detects cohort tier-stamp, cosmetic stamp, and min-lines violation. |
| Rubric leak check | [`scripts/rubric_leak_check.py`](scripts/rubric_leak_check.py) v2.1 (22 patterns after v3.9 S0 plus S0.5). GP-11 and Rule 16 enforcement. Pre-commit hook. OVS scope cleanup complete; Block 13, Block 3, Block 4 cleanup deferred to v3.10 and v3.11. |
| Test suite | [`scripts/tests/test_rubric_leak_check.py`](scripts/tests/test_rubric_leak_check.py) 18 tests, [`scripts/tests/test_em_dash_check.py`](scripts/tests/test_em_dash_check.py) 9 tests, [`scripts/tests/test_lang_check.py`](scripts/tests/test_lang_check.py) 11 tests. Total 38 pytest cases. |
| Pre-commit hook | [`scripts/pre-commit-install.sh`](scripts/pre-commit-install.sh) installs `.git/hooks/pre-commit` running four check scripts on staged Markdown: anti-gaming, rubric leak, em-dash, language detection. |
| Honest audit | [`memory/sdn/per-keyword-honest-audit.md`](memory/sdn/per-keyword-honest-audit.md). Manual stratified audit of 75 keywords on 2026-04-26 revealed a 4.5 times inflation in v3.7 Phase G. |
| Audit script v3 | [`scripts/refine_coverage_matrix_v2.py`](scripts/refine_coverage_matrix_v2.py). Coverage matrix breadth audit (legacy). Phase R5 will build `per_keyword_strict_audit.py` for depth verification. |
| Gap tracker | [`memory/sdn/keyword-true-gap-final.md`](memory/sdn/keyword-true-gap-final.md). v3.6 Phase 1 plus 2 deliverable. Superseded by Phase R5 strict audit. |
| REF source of truth | [`sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md`](sdn-onboard/doc/ovs-openflow-ovn-keyword-reference.md). REF, 2,617 lines, English authoritative, more than 320 keywords in scope. |
| Master index 0.3 | [`sdn-onboard/0.3 - master-keyword-index.md`](sdn-onboard/0.3%20-%20master-keyword-index.md). Vietnamese lookup spine of 1,153 lines, more than 320 keywords, five axis, one-line. **Note:** placement map, not mastery map. To be migrated to English in plan v3.12. |
| Plans index | [`plans/README.md`](plans/README.md) (per-series structure). |
| Memory index | [`memory/README.md`](memory/README.md) (per-series and shared structure). |

Session-by-session history (S1 to S63 and beyond) is in `memory/shared/session-log.md`. Audit history is in `memory/shared/audit-index.md`. The `git log` output is the source of truth for commit detail.

---

## Skill Quick Reference

**Installed at `~/.claude/skills/` (six skills, all must be used):**

| Group | Skill | When to use |
|-------|-------|-------------|
| Core A | `professor-style` | Every teaching content, every `.md` write, every technical explanation |
| Core A | `document-design` | Every `.md` in the onboard series |
| Core A | `fact-checker` | Every technical claim, every CLI command, every config directive |
| Core A | `web-fetcher` | Every URL to fetch or verify |
| Extra B | `search-first` | Before writing new code, script, or utility |
| Extra B | `deep-research` | Multi-source citation research (firecrawl and exa MCP) |

**Internal CLAUDE.md-triggered skills (outside global registry):**

| Skill | When to use |
|-------|-------------|
| `git-workflow` | Every git operation (commit, push, branch, PR) |
| `flow-graph` | Sequence diagram, protocol flow, handshake diagram |
| `quality-gate` | Every write, edit, or commit (pre-flight, see Rule 6 above) |

---

## Preferences

- Accuracy first. Double-check, cross-reference multiple sources.
- No AI writing patterns. Use a professor or PhD teaching style.
- No emoji in technical content.
- Real examples with verifiable output.
- Concise but deep. Analyst and engineer tone, not mechanical.
- English everywhere in working files, plan files, and curriculum (per Rule 17). Vietnamese remains only in legacy curriculum sections that plan v3.12 has not yet migrated, with the `**Language status:**` callout when present.
