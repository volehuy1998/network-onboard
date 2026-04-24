# Changelog — network-onboard

Training curriculum cho kỹ sư mạng: OpenvSwitch + OpenFlow + OVN. Focus sâu 5 trụ cột: nền tảng kiến thức, tools mastery, output interpretation, debug + troubleshoot, architecture + mechanism.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) adapted cho training series.

---

## v3.1-OperatorMaster (2026-04-24)

**Release type:** Foundation + Operator Mastery complete.
**Branch:** `docs/sdn-foundation-rev2`
**Scope curriculum:** 116 file `sdn-onboard/*.md`, ~52.6K dòng content.
**Lab verification:** pending (C1b — chờ user cung cấp lab host).

### Highlights

- **Phase G Operator Master 5/5 area COMPLETE** (S37a-c + S51-S59):
  - G.1 Truy vết: Part 9.25 ofproto/trace expansion + Part 9.27 packet journey end-to-end + Part 13.7 ovn-controller run loop deep + Part 20.0 case study playback.
  - G.2 Xử lý sự cố: Part 9.14 20-symptom decision tree expansion + Part 20.5 OVN forensic 3 case study (Port_Binding migration race / northd bulk delete / MAC_Binding explosion).
  - G.3 Debug sâu: Part 9.26 OVS revalidator storm forensic 3 case study + Part 20.1 security hardening 4-layer audit trail + Part 20.2 OVN troubleshooting deep-dive.
  - G.4 Lịch sử: Part 20.6 reflective retrospective 2007-2024 (17 năm SDN, 10 meta-lesson universal).
  - G.5 Thao tác công cụ: Part 20.3 OVN daily operator playbook + Part 20.4 OVS daily operator playbook.
- **Phase H Foundation Depth 13 session COMPLETE** (S38-S50):
  - Template library A/B/C/D trong `sdn-onboard/_templates/`.
  - Full OpenFlow match field catalog (Part 4.8) + action catalog (Part 4.9) với 100% spec coverage.
  - Full OVN pipeline exhaustive (ls_in_*/ls_out_*/lr_in_*/lr_out_*) trong Part 13.2+13.11.
  - OVS internals tier 1 expand (Part 9.1 + 9.15 + 9.16) với classifier TSS + connection manager + ofproto-dpif deep.
  - Tools coverage closed: ovs-bugtool + ovs-pcap + ovs-testcontroller.
- **Phase E Fact-check audit 101 file** (S32-S33i): Rule 14 Source Code Citation Integrity codified.
- **Phase F Cloud Native partial** (S36a-g): Block XIV (P4), Block XVI (DPDK+AFXDP), Block XV partial (Service Mesh 15.0 only, 15.1+15.2 deferred per user directive).
- **Pre-release audit** (S60-S61):
  - Rule 9 null byte: PASS 0/116.
  - Rule 13 em-dash density < 0.10: PASS 0/116.
  - Rule 11 Vietnamese prose: 185/295 leak fixed (63% reduction). 110 residual trong spec/table/numbered step contexts, defer v3.1.1 patch release.
  - Rule 14 source code citation: spot-check PASS.

### Statistics

| Metric | Count |
|--------|-------|
| Total file | 116 |
| Total line | ~52.641 |
| Block (foundation 0-XIII + extension XIV-XVI + forensic XVII-XIX + operations XX) | 20 |
| Guided Exercises + Capstone POE | 60+ |
| Anatomy Template A blocks | ~25 |
| Decision matrices (symptom-to-cause) | 4 major |
| Offline source citations | 100% Phase B+ |
| Upstream SHA + function verifications (Phase E) | 100+ |

### Known residual (v3.1.1 patch planned)

- **Rule 11 polish**: 110 minor Vietnamese prose leak còn lại trong core file. Phần lớn là numbered step Guided Exercise (`**3.** Verify connection`), table column header (`OpenFlow 1.X support`), vendor fact sentence (`HP ProCurve support 1.3`). Không ảnh hưởng kỹ thuật hay sự đọc hiểu, chỉ là discipline polish.
- **Block XIV+XV+XVI (68 leak)**: deprioritized theo user directive 2026-04-23 và 2026-04-24 "Đừng sa đà vào K8S, DPDK, XDP". Giữ skeleton + content nhưng không invest polish tiếp.
- **Lab verification (C1b)**: 63 exercise chờ lab host sẵn sàng. Output số liệu trong Guided Exercise là doc-plausible, chưa run thực tế.

### Files added Phase G (10 new/expanded)

- `sdn-onboard/9.14 - incident-response-decision-tree.md` (expand → 20 symptom matrix)
- `sdn-onboard/9.25 - ovs-flow-debugging-ofproto-trace.md` (expand +3 GE)
- `sdn-onboard/9.26 - ovs-revalidator-storm-forensic.md` (expand +2 case)
- `sdn-onboard/9.27 - ovs-ovn-packet-journey-end-to-end.md` (new)
- `sdn-onboard/13.7 - ovn-controller-internals.md` (expand run loop)
- `sdn-onboard/20.1 - ovs-ovn-security-hardening.md` (expand +audit trail)
- `sdn-onboard/20.2 - ovn-troubleshooting-deep-dive.md` (new)
- `sdn-onboard/20.3 - ovn-daily-operator-playbook.md` (new)
- `sdn-onboard/20.4 - ovs-daily-operator-playbook.md` (new)
- `sdn-onboard/20.5 - ovn-forensic-case-studies.md` (new)
- `sdn-onboard/20.6 - ovs-openflow-ovn-retrospective-2007-2024.md` (new)

### Commits milestone

Session milestone commits trên `docs/sdn-foundation-rev2`:

- Phase E: `7e5608b` (S33i Rule 14 codify)
- Phase F: `c777acf` (S36g 15.0)
- Phase H: `8dcbeca` (S59 phase G.4 close, also last Phase H commit baseline)
- Phase G: `8dcbeca` (S59 Phase G 100% COMPLETE)
- Pre-release audit: `ab9f38b` (S60) → `9469359` (S61a) → `d15d701` (S61b)

---

## Pre-release milestones (untagged)

### v2.1-preVerified (2026-04-22 post S35)

Phase E Scope D fact-check audit complete. Rule 14 Source Code Citation Integrity codified vào CLAUDE.md. Pre-release candidate nhưng chưa có release packaging.

### v2.0 (2026-04-22 post S29)

Phase D foundation firewall + audit backlog complete. 91 file curriculum với Block I-XIII content fully expanded. Rule 11 Vietnamese Prose Discipline codified.

### v1.0-preVerified (2026-04-21)

Phase B content expansion end-to-end. 64 file với Block 0-XIII content expanded + 3 advanced forensic (Part 17-19). Rule 10 Architecture-First Doctrine codified.

---

## Links

- Repo: https://github.com/volehuy1998/network-onboard
- SDN roadmap: [`sdn-onboard/README.md`](sdn-onboard/README.md)
- Pre-release audit: [`memory/pre-release-audit-2026-04-24.md`](memory/pre-release-audit-2026-04-24.md)
- Session history: [`memory/session-log.md`](memory/session-log.md)
- Project rules: [`CLAUDE.md`](CLAUDE.md) (14 mandatory rules + 6 skill)
