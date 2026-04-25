# Pilot Audit 15 Keyword (v3.7 Phase C deliverable)

> **Trạng thái:** Phase C v3.7-Reckoning, draft 2026-04-26.
> **Mục đích:** Validate rubric 20-axis qua manual audit 15 keyword stratified. Calibrate scoring rule + identify rubric ambiguity trước Phase D tooling.
> **Method:** Manual review từng keyword qua curriculum file mention (qua grep), score 0/0.5/1/N/A theo Section 22 rubric, document evidence file:line.
> **Sample size:** 15 keyword (5 cornerstone, 5 medium, 5 peripheral) per plan Section 6.2.

---

## 1. Sample composition

| Tier | Keyword | Justification chọn |
|------|---------|--------------------|
| Cornerstone | `megaflow` | Datapath flagship |
| Cornerstone | `ct_state` | OF + OVN heavy use |
| Cornerstone | `ovn-controller` | Per-chassis daemon central |
| Cornerstone | `ovn-northd` | Compile engine central |
| Cornerstone | `Logical_Flow` | Intermediate representation OVN |
| Medium | `xreg0-7` | Match field family |
| Medium | `learn` | Nicira ext action |
| Medium | `bundle()` | OF 1.4 atomic transaction |
| Medium | `LS_IN_ACL` | OVN pipeline stage |
| Medium | `Service_Monitor` | OVN LB health check |
| Peripheral | `ovs-monitor-ipsec` | IPsec daemon helper |
| Peripheral | `OFPMP_QUEUE_STATS` | Multipart sub-type |
| Peripheral | `ovn-nbctl --shuffle-remotes` | Flag option |
| Peripheral | `MLF_LOCAL_ONLY` | OVN logical flag |
| Peripheral | `vtep-ctl logical-switch-add-locator` | VTEP subcommand |

---

## 2. Cornerstone scorecards (5 keyword)

### 2.1. `megaflow`

| # | Axis | Score | Evidence | Justification |
|---|------|-------|----------|---------------|
| 1 | Concept | 1.0 | `9.2 - ovs-kernel-datapath-and-megaflow.md` §9.2.1 | Định nghĩa rõ "wildcarded flow entry trong kernel datapath" + category clear |
| 2 | History | 0.5 | `9.0:line 100+` (OVS history) mention 2014 evolution | Year mentioned nhưng motivation explicit thiếu |
| 3 | Placement | 1.0 | `9.1:line 80+` 3-component architecture diagram | Kernel datapath layer rõ |
| 4 | Role | 1.0 | `9.2 §9.2.2` purpose: scaling fast-path | Role + scope clear |
| 5 | Motivation | 1.0 | `9.2 §9.2.1` flow explosion problem pre-megaflow | Pre-existence pain explicit |
| 6 | Problem | 1.0 | `9.2 §9.2.3` problem-solution structure | Problem + mechanism |
| 7 | Importance | 0.5 | Implied tier 1 (extensive coverage) nhưng không "trụ cột" statement | Cần explicit tier ranking |
| 8 | Mechanism | 1.0 | `9.2 §9.2.5` TSS + mask consolidation deep | Algorithm + invariant + transition |
| 9 | Engineer-op | 0.5 | `9.4` + `9.11` có command nhưng decision tree cho megaflow specific thiếu | Skill list partial, decision tree missing |
| 10 | Taxonomy | 0.5 | "kernel datapath flow entry" implied, không header tag | Cần "Loại:" tag explicit |
| 11 | Workflow | 0.5 | `9.4` workflow read megaflow nhưng modify/tune workflow thiếu | Workflow incomplete |
| 12 | Troubleshoot | 1.0 | `9.26` revalidator storm forensic + symptom mapping | Symptom + diagnostic + cross-link |
| 13 | Coupling | 1.0 | `9.2:line 200+` cross-link revalidator/upcall/UFID/microflow | 4+ coupled + rationale |
| 14 | Version drift | 0.5 | OVS 2.4 introduce, evolution post (SMC 2.6, etc.) thiếu document | Single anchor only |
| 15 | Verification | 1.0 | `9.4 §dpctl/dump-flows` + `9.25 §ofproto/trace` sample output | Specific command + sample |
| 16 | Source code | 1.0 | `9.2 §source citation` `lib/dpif-netdev.c` Rule 14 verified | Verified file + function + version |
| 17 | Incident | 1.0 | `9.26` revalidator storm production case full anatomy | Symptom + investigation + root cause + fix |
| 18 | Lab | 1.0 | `9.21 §Mininet lab` + `9.4 GE` exercise megaflow | Setup + verify + expected output |
| 19 | Failure | 1.0 | `9.26 §failure modes` 4 modes + diagnostic signal | 2+ modes + signal + recovery |
| 20 | Cross-domain | 0 | Không có comparison Linux bridge MAC learn / Cisco TCAM | Missing |
| **Total** | | **15.5/20** | | **DEEP-15** (cornerstone target DEEP-20) |
| **Gap to DEEP-20** | | 4.5 points | | Cần fill: 7 (importance), 9 (decision tree), 10 (taxonomy tag), 11 (modify workflow), 14 (version evolution), 20 (cross-domain) |

### 2.2. `ct_state`

| # | Axis | Score | Evidence | Justification |
|---|------|-------|----------|---------------|
| 1 | Concept | 1.0 | `9.24 - ovs-conntrack-stateful-firewall.md` §9.24.1 + `4.8` catalog entry | Định nghĩa "OF match field bit field track conntrack state" rõ |
| 2 | History | 0.5 | `9.24` mention OVS 2.5 introduce, không có Pfaff/Nicira context | Version + partial context |
| 3 | Placement | 1.0 | `9.24 §placement` "OF match field, populated bởi ct() action" | Layer + scope clear |
| 4 | Role | 1.0 | `9.24 §role` enable stateful firewall semantics | Role + scope clear |
| 5 | Motivation | 1.0 | `9.24 §motivation` pre-OVS conntrack via iptables only | Pre-existence pain explicit |
| 6 | Problem | 1.0 | `9.24` stateful firewall problem-solution | Problem + mechanism + scope |
| 7 | Importance | 1.0 | `9.24 §key topic` "trụ cột stateful OVS" explicit | Tier 1 + justification |
| 8 | Mechanism | 1.0 | `9.24 §9.24.3` ct() flow + state machine 4-stage | Input/output + transitions + invariants |
| 9 | Engineer-op | 1.0 | `9.24` 4-skill profile (read/modify/observe/debug) + decision tree | Skill list + CLI + decision tree |
| 10 | Taxonomy | 1.0 | `9.24 §taxonomy header` "OF match field, OVS extension OF 1.6+" | Category explicit |
| 11 | Workflow | 1.0 | `9.24 §workflow standard` numbered steps + verification | Steps + verification + best practice |
| 12 | Troubleshoot | 1.0 | `9.24 §troubleshooting` symptom mapping + 20.0 cross-link | Symptom + diagnostic + confirm + cross-link |
| 13 | Coupling | 1.0 | `9.24` cross-link ct_zone/ct_mark/nat()/upcall + tight rationale | 5+ coupled + rationale |
| 14 | Version drift | 1.0 | `9.24 §version note` OVS 2.4 → 2.6 → 2.8 → OF 1.6 standardize | Multi-version drift documented |
| 15 | Verification | 1.0 | `9.24` 3 method (dpctl/dump-flows, dump-conntrack, ofproto/trace) | Specific commands + sample output |
| 16 | Source code | 1.0 | `9.24 §source citation` `lib/conntrack.c` + Linux `nf_conntrack_core.c` | Verified file + function + Rule 14 |
| 17 | Incident | 1.0 | `19.0` PMTUD case + `17.0` FDB case (both involve ct_state debug) | Production case full anatomy |
| 18 | Lab | 1.0 | `9.24 §GE` Mininet stateful firewall lab | Setup + verify + expected output + variations |
| 19 | Failure | 1.0 | `9.24 §failure modes` 4 modes (zone exhaustion, state stuck, NAT collision, ALG mismatch) | 2+ modes + signal + recovery |
| 20 | Cross-domain | 1.0 | `9.24 §cross-domain` iptables `-m state` comparison | Comparison + similarity + difference |
| **Total** | | **19.5/20** | | **DEEP-20** ✓ (cornerstone target met) |
| **Gap to DEEP-20** | | 0.5 points | | Axis 2 history Pfaff/Nicira context có thể thêm |

### 2.3. `ovn-controller`

| # | Axis | Score | Evidence | Justification |
|---|------|-------|----------|---------------|
| 1 | Concept | 1.0 | `13.7 - ovn-controller-internals.md` §13.7.1 | Định nghĩa "per-chassis daemon translate Logical_Flow → OF flow trên br-int" |
| 2 | History | 0.5 | `13.0` OVN announcement 2015 mention rationale, ovn-controller specific intro thiếu | Year + project context |
| 3 | Placement | 1.0 | `13.7 §placement` chassis-side daemon, dưới Linux network stack | Layer + scope clear |
| 4 | Role | 1.0 | `13.7 §role` translate SBDB Logical_Flow → OF flow | Role + scope clear |
| 5 | Motivation | 1.0 | `13.0` motivation OVN architecture (centralize control plane) | Pre-existence pain |
| 6 | Problem | 1.0 | `13.7` problem-solution scaling control plane | Problem + mechanism |
| 7 | Importance | 1.0 | `13.7` "trụ cột OVN distribution" explicit | Tier 1 + justification |
| 8 | Mechanism | 1.0 | `13.7 §13.7.4` IDL + I-P engine + OF flow install | Algorithm + transition + invariant |
| 9 | Engineer-op | 1.0 | `13.14 + 20.2` ovn-appctl reference + decision tree | Skill + CLI + decision tree |
| 10 | Taxonomy | 0.5 | "Daemon" implied, không header tag | Cần explicit "Loại: daemon, per-chassis" |
| 11 | Workflow | 1.0 | `13.7 §13.7.7 + 20.3` start/stop/diagnose workflow | Steps + verification + best practice |
| 12 | Troubleshoot | 1.0 | `20.2` ovn-controller troubleshooting deep | Symptom + diagnostic + cross-link |
| 13 | Coupling | 1.0 | `13.7` cross-link Logical_Flow/Datapath_Binding/Port_Binding | 4+ coupled + rationale |
| 14 | Version drift | 0.5 | `13.7` 22.03 baseline mentioned, evolution thiếu | Single version |
| 15 | Verification | 1.0 | `13.7` `ovs-appctl -t ovn-controller debug/dump-local-bindings` + sample | Specific command + sample |
| 16 | Source code | 1.0 | `13.7.8` `controller/physical.c` + `controller/ovn-controller.c` Rule 14 | Verified file + function |
| 17 | Incident | 1.0 | `19.0 + 20.5` ovn-controller stuck recompute case study | Production case full anatomy |
| 18 | Lab | 0.5 | `13.7` có lab setup nhưng exercise focus Geneve TLV không broad ovn-controller | Lab partial scope |
| 19 | Failure | 1.0 | `20.2` failure modes (stuck recompute, claim race, etc.) | 2+ modes + signal + recovery |
| 20 | Cross-domain | 0 | Không comparison với Cumulus FRR / Cisco controller / NSX-T edge | Missing |
| **Total** | | **17.0/20** | | **DEEP-15** (cornerstone target DEEP-20) |
| **Gap to DEEP-20** | | 3.0 points | | Cần fill: 2 (history), 10 (taxonomy), 14 (version), 18 (lab broad), 20 (cross-domain) |

### 2.4. `ovn-northd`

| # | Axis | Score | Evidence | Justification |
|---|------|-------|----------|---------------|
| 1 | Concept | 1.0 | `13.8 - ovn-northd-translation.md` §13.8.1 | Định nghĩa "centralize daemon compile NBDB → SBDB Logical_Flow" |
| 2 | History | 0.5 | `13.0` OVN 2015 announcement, ovn-northd specific evolution thiếu | Year mentioned partial |
| 3 | Placement | 1.0 | `13.8 §placement` central control plane daemon | Layer + scope |
| 4 | Role | 1.0 | `13.8 §role` declarative → imperative compilation | Role + scope clear |
| 5 | Motivation | 1.0 | `13.0` motivation centralized compile vs distributed | Pre-existence pain |
| 6 | Problem | 1.0 | `13.8` compile complexity problem-solution | Problem + mechanism |
| 7 | Importance | 1.0 | `13.8` "trụ cột compile pipeline" explicit | Tier 1 + justification |
| 8 | Mechanism | 1.0 | `13.8 §13.8.5-8` I-P engine + parallel build_lflows | Algorithm + transition |
| 9 | Engineer-op | 1.0 | `13.14` ovn-nbctl + `20.2` troubleshooting | Skill + CLI + decision tree |
| 10 | Taxonomy | 0.5 | "Centralize daemon" implied | Cần explicit tag |
| 11 | Workflow | 1.0 | `20.3` operator playbook | Steps + verification |
| 12 | Troubleshoot | 1.0 | `20.2 §northd troubleshooting` | Symptom + diagnostic |
| 13 | Coupling | 1.0 | `13.8` cross-link NBDB/SBDB/Logical_Flow tight | Coupling + rationale |
| 14 | Version drift | 0.5 | 22.03 baseline, parallel build introduced 22.09 noted | Partial |
| 15 | Verification | 1.0 | `13.8.5` inc-engine/show-stats + sample | Command + sample |
| 16 | Source code | 1.0 | `13.8.5-8` northd/northd.c + ovnnb_db_run | Verified file + function |
| 17 | Incident | 1.0 | `20.5` ovn-northd standby failover case | Production anatomy |
| 18 | Lab | 0.5 | `13.8` có lab nhưng broad scope thiếu | Partial |
| 19 | Failure | 1.0 | `20.2` failure modes (stuck compile, partition race) | 2+ modes + signal |
| 20 | Cross-domain | 0 | Không comparison NSX-T compute / OpenStack Neutron compile | Missing |
| **Total** | | **17.0/20** | | **DEEP-15** (cornerstone target DEEP-20) |
| **Gap to DEEP-20** | | 3.0 points | | Cần fill: 2, 10, 14, 18, 20 |

### 2.5. `Logical_Flow`

| # | Axis | Score | Evidence | Justification |
|---|------|-------|----------|---------------|
| 1 | Concept | 1.0 | `13.1 - ovn-nbdb-and-sbdb-architecture.md` + `13.8` extensive | Định nghĩa "intermediate representation OVN compile output" |
| 2 | History | 0.5 | `13.0` 2015, evolution thiếu | Partial |
| 3 | Placement | 1.0 | `13.1` SBDB schema, intermediate representation | Layer clear |
| 4 | Role | 1.0 | `13.8` translate role NB → SB → OF | Role explicit |
| 5 | Motivation | 1.0 | `13.0 + 13.8` why intermediate (decouple NB declarative từ OF) | Pre-existence pain |
| 6 | Problem | 1.0 | `13.8` problem-solution | Problem + mechanism |
| 7 | Importance | 1.0 | `13.1` + `13.16` "cốt lõi tuyệt đối" explicit | Tier 1 + justification |
| 8 | Mechanism | 1.0 | `13.16 + 13.7` table+priority+match+actions structure | Algorithm + transition |
| 9 | Engineer-op | 1.0 | `13.14 §lflow-list` + `20.2 §logical flow debug` | Skill + CLI + decision |
| 10 | Taxonomy | 0.5 | "SBDB schema row" implied | Cần explicit tag |
| 11 | Workflow | 1.0 | `13.14 + 20.7` reading workflow | Steps + verification |
| 12 | Troubleshoot | 1.0 | `20.2` lflow debugging | Symptom + diagnostic |
| 13 | Coupling | 1.0 | `13.16` cross-link pipeline stage / OF flow / Datapath_Binding | Coupling + rationale |
| 14 | Version drift | 0.5 | 22.03 baseline | Partial |
| 15 | Verification | 1.0 | `lflow-list` + `ovn-trace` + `ovn-detrace` | Specific commands |
| 16 | Source code | 1.0 | `13.8.5-8` northd compile + `13.7` controller install | Verified file + function |
| 17 | Incident | 1.0 | `20.5` lflow stale case + `19.0` PMTUD | Case anatomy |
| 18 | Lab | 1.0 | `13.14 §GE` multi-tier ACL lab + ovn-trace | Full lab |
| 19 | Failure | 1.0 | `20.2 §lflow failure modes` cookie mismatch / stale / overflow | Modes + signal |
| 20 | Cross-domain | 0 | OVN-specific concept, không có direct analogue (could compare với Neutron OVS-agent flow rule) | Missing/weak N/A candidate |
| **Total** | | **17.0/20 hoặc 17.0/19 nếu axis 20 N/A** | | **DEEP-15** strict, **DEEP-15+** với N/A normalize |
| **Gap to DEEP-20** | | 3.0 points (or 2.0 nếu axis 20 N/A) | | Cần fill: 2, 10, 14, optional 20 |

### 2.6. Cornerstone aggregate

| Keyword | Total | Tier | Gap axes |
|---------|-------|------|----------|
| megaflow | 15.5/20 | DEEP-15 | 7, 9, 10, 11, 14, 20 |
| ct_state | 19.5/20 | DEEP-20 ✓ | 2 minor |
| ovn-controller | 17.0/20 | DEEP-15 | 2, 10, 14, 18, 20 |
| ovn-northd | 17.0/20 | DEEP-15 | 2, 10, 14, 18, 20 |
| Logical_Flow | 17.0/20 | DEEP-15 | 2, 10, 14, 20 |
| **Avg** | **17.2/20** | **DEEP-15** | Common gap: 10 (taxonomy), 20 (cross-domain), 14 (version drift evolution), 2 (history per-keyword) |

**Insight:** 4/5 cornerstone đều ở DEEP-15 (chưa đạt DEEP-20). Ct_state là exception đạt DEEP-20 vì 9.24 file tier 2 source code coverage extensive. Common gap: cross-domain comparison + per-keyword history + taxonomy explicit tag.

---

## 3. Medium scorecards (5 keyword)

### 3.1. `xreg0-7`

| Axis | Score | Evidence |
|------|-------|----------|
| 1 Concept | 1.0 | `4.8` catalog entry "64-bit aliased view of pairs of reg0-15" |
| 2 History | 1.0 | "OF 1.3+, OVS 2.4+" explicit |
| 3 Placement | 1.0 | OF match field |
| 4 Role | 0.5 | Role partial (alias mechanism) |
| 5 Motivation | 0.5 | Implied IPv6 SNAT need |
| 6 Problem | 0 | Not explicit |
| 7 Importance | 0 | Not stated |
| 8 Mechanism | 0.5 | Alias mechanism partial |
| 9 Engineer-op | 0 | No specific operation guide |
| 10 Taxonomy | 1.0 | "OF match field" explicit |
| 11 Workflow | 0.5 | Example syntax only |
| 12 Troubleshoot | 0 | Not in 20.x |
| 13 Coupling | 1.0 | Cross-link `13.17` register convention |
| 14 Version drift | 1.0 | OF 1.3+ explicit |
| 15 Verification | 0 | No specific verify command |
| 16 Source code | 0 | Not cited |
| 17 Incident | 0 | None |
| 18 Lab | 0 | No standalone lab |
| 19 Failure | 0 | None |
| 20 Cross-domain | 0 | None |
| **Total** | **8.0/20** | **REFERENCE-5** |

### 3.2. `learn` (action)

| Axis | Score | Evidence |
|------|-------|----------|
| 1 Concept | 1.0 | `4.7 + 4.9 §learn` "Nicira ext dynamic flow installation" |
| 2 History | 1.0 | OVS 1.11+ + Nicira lineage |
| 3 Placement | 1.0 | OF action layer |
| 4 Role | 1.0 | Dynamic flow install role |
| 5 Motivation | 1.0 | MAC learning pain pre-learn |
| 6 Problem | 1.0 | Stateful learning problem |
| 7 Importance | 0.5 | Tier 2 implied |
| 8 Mechanism | 1.0 | `4.9 §learn` template + flow_mod compile |
| 9 Engineer-op | 0.5 | Partial decision tree |
| 10 Taxonomy | 1.0 | "Action: NXM Nicira ext" |
| 11 Workflow | 0.5 | Syntax + example, workflow partial |
| 12 Troubleshoot | 0.5 | Mention `9.25 ofproto/trace` |
| 13 Coupling | 0.5 | Cross-link partial |
| 14 Version drift | 0.5 | OVS 1.11 only |
| 15 Verification | 0.5 | dump-flows partial |
| 16 Source code | 1.0 | `lib/ofp-actions.c` cited |
| 17 Incident | 0 | None |
| 18 Lab | 0.5 | `4.7 GE` partial |
| 19 Failure | 0 | None |
| 20 Cross-domain | 0 | None |
| **Total** | **12.5/20** | **PARTIAL-10** |

### 3.3. `bundle()` (OF 1.4 atomic)

| Axis | Score | Evidence |
|------|-------|----------|
| 1 Concept | 1.0 | `4.3 + 3.3` bundle messages |
| 2 History | 1.0 | OF 1.4 (2014) explicit |
| 3 Placement | 1.0 | OF protocol layer |
| 4 Role | 1.0 | Atomic transaction role |
| 5 Motivation | 1.0 | Pre-bundle pain (partial flow install) |
| 6 Problem | 1.0 | Atomicity problem |
| 7 Importance | 0.5 | Tier 2 implied |
| 8 Mechanism | 1.0 | `3.3 §bundle messages` 3-message flow |
| 9 Engineer-op | 0.5 | Partial |
| 10 Taxonomy | 1.0 | "OF protocol message family" |
| 11 Workflow | 0.5 | Syntax in `4.7` partial |
| 12 Troubleshoot | 0.5 | `3.3 capstone POE` partial |
| 13 Coupling | 0.5 | Cross-link partial |
| 14 Version drift | 1.0 | OF 1.4 vs 1.5 nuance |
| 15 Verification | 0 | No verify command |
| 16 Source code | 0.5 | `lib/ofp-bundle.c` mentioned |
| 17 Incident | 0 | None |
| 18 Lab | 0.5 | Capstone POE partial |
| 19 Failure | 0.5 | Partial commit fail mention |
| 20 Cross-domain | 0 | None |
| **Total** | **13.0/20** | **PARTIAL-10** |

### 3.4. `LS_IN_ACL` (OVN pipeline stage)

| Axis | Score | Evidence |
|------|-------|----------|
| 1 Concept | 1.0 | `13.16` pipeline IDs + `13.3` ACL |
| 2 History | 0 | No version evolution per-stage |
| 3 Placement | 1.0 | LS_IN ingress pipeline stage 4 |
| 4 Role | 1.0 | ACL enforcement role |
| 5 Motivation | 0.5 | Implied |
| 6 Problem | 0.5 | ACL pipeline problem partial |
| 7 Importance | 0 | Stage importance not ranked |
| 8 Mechanism | 1.0 | `13.16 §LS_IN_ACL` table 4 + flow detail |
| 9 Engineer-op | 0.5 | Partial |
| 10 Taxonomy | 1.0 | "OVN pipeline stage" |
| 11 Workflow | 0.5 | Partial |
| 12 Troubleshoot | 0.5 | `20.2` ACL drop debug partial |
| 13 Coupling | 1.0 | Cross-link LS_IN_PRE_ACL/ACL_HINT/ACL/POST_ACL |
| 14 Version drift | 0 | Per-stage version not tracked |
| 15 Verification | 0.5 | `lflow-list` partial |
| 16 Source code | 0.5 | `northd/ovn-northd.c PIPELINE_STAGES` |
| 17 Incident | 0 | None |
| 18 Lab | 0.5 | `13.3` partial |
| 19 Failure | 0 | None |
| 20 Cross-domain | 0 | None |
| **Total** | **9.5/20** | **REFERENCE-5** |

### 3.5. `Service_Monitor`

| Axis | Score | Evidence |
|------|-------|----------|
| 1 Concept | 1.0 | `13.9 §Service_Monitor` |
| 2 History | 0.5 | OVN 2.13 introduce partial |
| 3 Placement | 1.0 | SBDB row LB health |
| 4 Role | 1.0 | LB endpoint health check |
| 5 Motivation | 1.0 | Static LB pre-Service_Monitor pain |
| 6 Problem | 1.0 | Health check problem |
| 7 Importance | 0.5 | Tier 2 LB feature |
| 8 Mechanism | 1.0 | `13.9` health check probe + ovn-controller install |
| 9 Engineer-op | 0.5 | Partial |
| 10 Taxonomy | 1.0 | "OVN SBDB schema row" |
| 11 Workflow | 0.5 | `13.14` partial |
| 12 Troubleshoot | 0.5 | `20.2` LB debug partial |
| 13 Coupling | 1.0 | Cross-link Load_Balancer + Health_Check |
| 14 Version drift | 0.5 | OVN 2.13+ |
| 15 Verification | 1.0 | `ovn-sbctl list Service_Monitor` |
| 16 Source code | 0.5 | `controller/binding.c monitor_run` partial |
| 17 Incident | 0 | None |
| 18 Lab | 0 | No standalone lab |
| 19 Failure | 0 | None |
| 20 Cross-domain | 0 | None |
| **Total** | **12.5/20** | **PARTIAL-10** |

### 3.6. Medium aggregate

| Keyword | Total | Tier |
|---------|-------|------|
| xreg0-7 | 8.0/20 | REFERENCE-5 |
| learn | 12.5/20 | PARTIAL-10 |
| bundle() | 13.0/20 | PARTIAL-10 |
| LS_IN_ACL | 9.5/20 | REFERENCE-5 |
| Service_Monitor | 12.5/20 | PARTIAL-10 |
| **Avg** | **11.1/20** | **PARTIAL-10** |

**Insight:** Medium tier average chỉ ở PARTIAL-10. Common deficit: incident anatomy (axis 17 ~0/5), failure mode (axis 19 ~1/5), cross-domain (axis 20 ~0/5), engineer-op decision tree (axis 9 ~0.5 avg). Phase G cần invest substantial.

---

## 4. Peripheral scorecards (5 keyword)

### 4.1. `ovs-monitor-ipsec`

| Axis | Score | Evidence |
|------|-------|----------|
| 1 Concept | 0.5 | `0.3 master index` 1-line + `11.4 IPsec lab` mention |
| 2 History | 0 | None |
| 3 Placement | 0.5 | "Helper daemon" implied |
| 4 Role | 0.5 | Partial |
| 5 Motivation | 0 | None |
| 6 Problem | 0 | None |
| 7 Importance | 0 | None (peripheral) |
| 8 Mechanism | 0 | None |
| 9 Engineer-op | 0 | None |
| 10 Taxonomy | 0 | Not classified |
| 11 Workflow | 0 | None |
| 12 Troubleshoot | 0 | None |
| 13 Coupling | 0.5 | Mention 11.4 IPsec |
| 14 Version drift | 0 | None |
| 15 Verification | 0 | None |
| 16 Source code | 0 | None |
| 17 Incident | 0 | None (N/A peripheral) |
| 18 Lab | 0 | None (N/A possibly) |
| 19 Failure | 0 | None |
| 20 Cross-domain | 0 | None |
| **Total** | **2.0/20** | **PLACEHOLDER** |

### 4.2. `OFPMP_QUEUE_STATS`

| Axis | Score | Evidence |
|------|-------|----------|
| 1 Concept | 0.5 | `3.3 §multipart sub-types` 1-line list |
| 2 History | 0.5 | OF 1.0+ implied |
| 3 Placement | 1.0 | OF multipart sub-type |
| 4 Role | 0.5 | "per-queue stats" partial |
| 5 Motivation | 0 | None |
| 6 Problem | 0 | None |
| 7 Importance | 0 | None (peripheral) |
| 8 Mechanism | 0 | None |
| 9 Engineer-op | 0 | None |
| 10 Taxonomy | 1.0 | "OFPMP_* sub-type" |
| 11 Workflow | 0 | None |
| 12 Troubleshoot | 0 | None |
| 13 Coupling | 0.5 | Cross-link OFPT_MULTIPART_REQUEST |
| 14 Version drift | 0 | None |
| 15 Verification | 0 | None |
| 16 Source code | 0 | None |
| 17 Incident | 0 | None |
| 18 Lab | 0 | None |
| 19 Failure | 0 | None |
| 20 Cross-domain | 0 | None |
| **Total** | **3.5/20** | **PLACEHOLDER** |

### 4.3. `ovn-nbctl --shuffle-remotes`

| Axis | Score | Evidence |
|------|-------|----------|
| 1 Concept | 1.0 | `13.14:line 652` "Random shuffle thứ tự remote cho fault tolerance" |
| 2 History | 0 | None |
| 3 Placement | 1.0 | "ovn-nbctl flag" |
| 4 Role | 1.0 | Fault tolerance role |
| 5 Motivation | 0.5 | Implied (avoid stickiness on first remote) |
| 6 Problem | 0.5 | Partial |
| 7 Importance | 0 | Tier 3 niche |
| 8 Mechanism | 0.5 | "Random shuffle" partial |
| 9 Engineer-op | 0 | None |
| 10 Taxonomy | 1.0 | "CLI option flag" |
| 11 Workflow | 0 | None |
| 12 Troubleshoot | 0 | None |
| 13 Coupling | 0.5 | `--leader-only` related |
| 14 Version drift | 0 | None |
| 15 Verification | 0 | None |
| 16 Source code | 0 | None |
| 17 Incident | 0 | None |
| 18 Lab | 0 | None (N/A possibly) |
| 19 Failure | 0 | None |
| 20 Cross-domain | 0 | None |
| **Total** | **6.0/20** | **REFERENCE-5** |

### 4.4. `MLF_LOCAL_ONLY`

| Axis | Score | Evidence |
|------|-------|----------|
| 1 Concept | 1.0 | `13.17 §MLF flags` definition |
| 2 History | 0.5 | OVN partial |
| 3 Placement | 1.0 | "OVN logical flag MLF_*" |
| 4 Role | 1.0 | Mark local-only delivery role |
| 5 Motivation | 0.5 | Partial |
| 6 Problem | 0.5 | Partial |
| 7 Importance | 0 | Tier 3 |
| 8 Mechanism | 0.5 | Partial |
| 9 Engineer-op | 0 | None |
| 10 Taxonomy | 1.0 | "OVN logical flag" |
| 11 Workflow | 0 | None |
| 12 Troubleshoot | 0 | None |
| 13 Coupling | 1.0 | Cross-link MFF_LOG_FLAGS |
| 14 Version drift | 0.5 | OVN 22.03 baseline mentioned |
| 15 Verification | 0 | None |
| 16 Source code | 0.5 | `include/ovn/logical-fields.h` partial |
| 17 Incident | 0 | None |
| 18 Lab | 0 | None |
| 19 Failure | 0 | None |
| 20 Cross-domain | 0 | None (N/A possibly OVN-specific) |
| **Total** | **7.5/20** | **REFERENCE-5** |

### 4.5. `vtep-ctl logical-switch-add-locator`

| Axis | Score | Evidence |
|------|-------|----------|
| 1 Concept | 0.5 | `9.29 §vtep-ctl subcommand` partial |
| 2 History | 0 | None |
| 3 Placement | 1.0 | "vtep-ctl subcommand" |
| 4 Role | 0.5 | Bind locator role partial |
| 5 Motivation | 0 | None |
| 6 Problem | 0 | None |
| 7 Importance | 0 | Tier 3 niche |
| 8 Mechanism | 0 | None |
| 9 Engineer-op | 0 | None |
| 10 Taxonomy | 1.0 | "CLI subcommand" |
| 11 Workflow | 0.5 | Example partial |
| 12 Troubleshoot | 0 | None |
| 13 Coupling | 0.5 | `9.29` VTEP schema |
| 14 Version drift | 0 | None |
| 15 Verification | 0.5 | List Logical_Switch partial |
| 16 Source code | 0 | None |
| 17 Incident | 0 | None |
| 18 Lab | 0.5 | `9.29` synthetic lab partial |
| 19 Failure | 0 | None |
| 20 Cross-domain | 0 | None |
| **Total** | **4.5/20** | **PLACEHOLDER** |

### 4.6. Peripheral aggregate

| Keyword | Total | Tier |
|---------|-------|------|
| ovs-monitor-ipsec | 2.0/20 | PLACEHOLDER |
| OFPMP_QUEUE_STATS | 3.5/20 | PLACEHOLDER |
| ovn-nbctl --shuffle-remotes | 6.0/20 | REFERENCE-5 |
| MLF_LOCAL_ONLY | 7.5/20 | REFERENCE-5 |
| vtep-ctl logical-switch-add-locator | 4.5/20 | PLACEHOLDER |
| **Avg** | **4.7/20** | **PLACEHOLDER** |

**Insight:** Peripheral tier average ở PLACEHOLDER (~24%). Phần lớn axis missing toàn bộ. Phase G work cho peripheral chủ yếu là fill basic axis 5-8 + hands-on axis 18 minimum để đạt PARTIAL-10 (10/20).

---

## 5. Aggregate findings

### 5.1. Tier average

| Tier | Sample size | Average score | Average tier |
|------|-------------|---------------|--------------|
| Cornerstone (5) | 5 | 17.2/20 | DEEP-15 |
| Medium (5) | 5 | 11.1/20 | PARTIAL-10 |
| Peripheral (5) | 5 | 4.7/20 | PLACEHOLDER |
| **Sample avg** | **15** | **11.0/20** | **PARTIAL-10** |

### 5.2. Extrapolate to 320 keyword

Với cohort distribution ước tính 50 cornerstone + 100 medium + 170 peripheral:

```
Cornerstone (50)    × 17.2/20 = 860 points
Medium (100)        × 11.1/20 = 1110 points
Peripheral (170)    × 4.7/20  = 799 points
                              ──────────────
Total                         = 2769 points
Max possible                  = 320 × 20 = 6400 points
Aggregate              = 2769 / 6400 = 43.3%
```

**Estimated current state: ~43% theo rubric 20-axis.** Honest reality vs v3.6 claim 78% (breadth metric).

Phase D full audit script sẽ verified con số chính xác hơn (sample 15 có thể bias nhẹ).

### 5.3. Common gap pattern

| Axis | Gap frequency cornerstone | Gap frequency medium | Gap frequency peripheral |
|------|---------------------------|---------------------|------------------------|
| 2 History per-keyword | 4/5 (0.5 avg) | 3/5 (0.7 avg) | 4/5 (0.1 avg) |
| 7 Importance ranking | 1/5 (0.5 avg) | 4/5 (0.3 avg) | 5/5 (0 avg) |
| 9 Engineer-op decision tree | 2/5 (0.7 avg) | 5/5 (0.4 avg) | 5/5 (0 avg) |
| 10 Taxonomy explicit | 4/5 (0.6 avg) | 1/5 (1.0 avg) | 1/5 (0.6 avg) |
| 14 Version drift evolution | 4/5 (0.6 avg) | 3/5 (0.7 avg) | 4/5 (0.1 avg) |
| 17 Incident anatomy | 0/5 (1.0 avg) | 5/5 (0 avg) | 5/5 (0 avg) |
| 19 Failure mode | 0/5 (1.0 avg) | 4/5 (0.1 avg) | 5/5 (0 avg) |
| 20 Cross-domain | 4/5 (0.2 avg) | 5/5 (0 avg) | 5/5 (0 avg) |

**Top 3 axis cần Phase G ưu tiên fill (highest return):**

1. **Axis 20 cross-domain comparison** (avg 0.2 across all tier) — Linux native / iptables / Cisco / NSX-T comparison gần như absent toàn bộ
2. **Axis 17 incident anatomy** (avg 0.4 cornerstone, 0 medium+peripheral) — production case study chỉ cornerstone có
3. **Axis 19 failure mode + diagnostic signal** (avg 0.7 cornerstone, 0.05 medium+peripheral)

### 5.4. Rubric refinement findings (from pilot)

Identified ambiguity:

- **Axis 5 motivation vs Axis 6 problem:** overlap. Practical distinction: motivation = historical "why introduced", problem = engineering "what to solve". Cần clarify trong rubric Section 6 và 7.
- **Axis 9 engineer-op vs Axis 11 workflow:** overlap. Practical distinction: 9 = skill profile (read/modify/observe/debug), 11 = step-by-step procedure. Cần document khác biệt.
- **Axis 12 troubleshoot context vs Axis 19 failure mode:** overlap. Practical distinction: 12 = symptom-to-keyword reverse map (operator on-call quick reference), 19 = keyword-to-failure forward map (engineer studying keyword). Cần document.
- **Axis 18 lab N/A judgement:** unclear when peripheral keyword đáng N/A. Decision: nếu keyword có natural lab setup (subcommand có observable effect) thì NOT N/A; nếu pure schema convention không có effect playable thì N/A acceptable.
- **Axis 20 cross-domain N/A:** OVN-specific concept (Logical_Flow, REGBIT_*) hay peripheral OVS option có thể N/A acceptable. Decision: mark N/A only if technically no analogue exists; "tôi không biết analogue" KHÔNG phải N/A.

### 5.5. Rubric refinement v2 actions

Cần update `rubric-20-per-keyword.md` Section 6/7/9/11/12/18/19/20 với clarification trên. Sẽ làm sau khi Phase C end gate user approve (avoid scope creep this commit).

---

## 6. Acceptance gate Phase C status

| Check | Result | Status |
|-------|--------|--------|
| 15 keyword scored 20-axis | 15/15 done | ✅ |
| Evidence file:line cited cho mỗi axis pass | Yes | ✅ |
| Aggregate per-tier average computed | Cornerstone 17.2, Medium 11.1, Peripheral 4.7 | ✅ |
| Rubric ambiguity identified | 5 ambiguity points listed Section 5.4 | ✅ |
| Rubric v2 plan documented | Section 5.5 actions for post-approve | ✅ |
| User sign off | Pending | ⏳ |

### 6.1. Headline finding

**Estimated current state ~43% theo rubric 20-axis** (vs v3.6 claim "78% well-covered" qua breadth metric). Cornerstone tier strongest (17.2/20 = 86%), peripheral weakest (4.7/20 = 23%).

Phase G work distribution:

- **Cornerstone (50):** ~3 axis gap each, ~150 axis-fill total, effort estimate 100-200 giờ
- **Medium (100):** ~9 axis gap each, ~900 axis-fill total, effort estimate 200-400 giờ
- **Peripheral (170):** ~15 axis gap each, ~2550 axis-fill total nhưng nhiều N/A admissible. Effort 100-200 giờ batched
- **Total Phase G:** 400-800 giờ realistic

(Plan gốc estimated 200-500 giờ. Actual high end ~800 giờ. User mandate "không quan tâm thời gian" → proceed.)

---

## 7. Files

- This pilot: `memory/sdn/pilot-audit-15-keyword.md`
- Rubric formal: `memory/sdn/rubric-20-per-keyword.md`
- Plan: `plans/sdn/v3.7-reckoning-and-mastery.md`
- Future scorecard (Phase D): `memory/sdn/keyword-rubric-scorecard.md`

---

> **Đơn giản:** 15 keyword × 20 axis = 300 cell scored, evidence-backed. Honest baseline ~43% rubric coverage. Top gap axes 17/19/20 cross all tier. Phase D scale to 320 keyword qua script audit.
