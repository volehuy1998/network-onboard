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
| `sdn-onboard/README.md` | **Rev 2 (2026-04-20 session 4, 33937 bytes):** TOC 20 Parts / 17 Blocks + Block XVII advanced; baseline OVS 2.17.9/OVN 22.03.8/Ubuntu 22.04 + upgrade path OVS 3.3/OVN 24.03/Ubuntu 24.04; Mermaid dependency graph P0-P19; 7 reading paths; Phụ lục A Version Evolution Tracker (với Part 9.5 DOCA row); Phụ lục B RFC references; Phụ lục C Bibliography (Goransson, NSDI 2015, NVIDIA DOCA, upstream) | `README.md` (root — SDN section), TẤT CẢ 60 file skeleton Block 0-XVI (60 markdown links cần verify tồn tại), 3 file OVN advanced `17.0/18.0/19.0` (S3 đã rename 2026-04-20; TOC entries Part 17/18/19 đã sync), `plans/sdn-foundation-architecture.md` §3.1/§3.4/§3.5 (TOC/graph/reading paths phải khớp) |
| `sdn-onboard/17.0 - ovn-l2-forwarding-and-fdb-poisoning.md` | OVN L2 Forwarding, FDB Poisoning case study VLAN 3808, multichassis/claim high-level, FDP-620 trigger conditions (1178 lines sau khi trim §17.6 deep-dive sang Part 19 ngày 2026-04-20, production log forensics) | `README.md` (root — SDN section), `sdn-onboard/README.md` (TOC), `sdn-onboard/18.0` nếu 18.0 cross-reference 17.0, `sdn-onboard/19.0` (cross-refs bidirectional: Part 17 §17.6 liên kết tới Part 19 §19.2/19.4/19.5/19.6) |
| `sdn-onboard/18.0 - ovn-arp-responder-and-bum-suppression.md` | OVN ARP Responder, BUM suppression (496 lines, rewritten 2026-04-10) | `sdn-onboard/README.md` (TOC), `sdn-onboard/17.0` (cross-references đến tunnel key, localnet port, MC_FLOOD từ Part 17) |
| `sdn-onboard/19.0 - ovn-multichassis-binding-and-pmtud.md` | OVN multichassis binding lifecycle + Geneve PMTUD bug FDP-620 root cause + RARP activation-strategy + 3 Labs (1379 lines) | `sdn-onboard/README.md` (TOC), `sdn-onboard/17.0` (live migration trigger, localnet, Chassis/Claim baseline), `README.md` (root — SDN section) |

> **Quy tắc:** Khi sửa SDN 17.0, kiểm tra SDN 18.0 có references đến localnet/MC_UNKNOWN không, và SDN 19.0 có cross-ref đến live migration/multichassis của Part 17 không. Khi sửa SDN 18.0, kiểm tra SDN 17.0 có concepts nào được tái sử dụng không. Khi sửa SDN 19.0, kiểm tra consistency với Part 17 section 17.2 (Chassis/Claim) và section 17.6 (live migration trigger).

### Tầng 2c: SDN foundation skeletons rev 2 (Block IX — OpenvSwitch internals)

> **Scope:** Block IX sau khi thêm 9.5 (session 2026-04-20 session 4). 6 file skeleton,
> dependency chain tuyến tính 9.0 → 9.1 → 9.2 → 9.3 → 9.4 → 9.5.
> Các Block khác (0, I-VIII, X-XVI) cũng có skeleton tồn tại nhưng chưa nhập vào bảng này
> — sẽ được ghi nhận khi S5-S19 bắt đầu viết content từng Block.

| File | Nội dung chính | Related Files — PHẢI kiểm tra khi sửa |
|------|---------------|---------------------------------------|
| `sdn-onboard/9.0 - ovs-history-2007-present.md` | Skeleton: OVS 2007 Nicira → NSDI 2015 → Linux Foundation 2016, version timeline, so sánh Linux bridge | `plans/sdn-foundation-architecture.md` §3.3 Block IX (sections phải khớp), `sdn-onboard/README.md` TOC (khi rewrite S2) |
| `sdn-onboard/9.1 - ovs-3-component-architecture.md` | Skeleton: ovs-vswitchd + ovsdb-server + openvswitch.ko, netlink genl family upcall | §3.3 Block IX, Part 8.1 (linux-onboard bridge reference), cross-ref tới Part 10 (OVSDB details) |
| `sdn-onboard/9.2 - ovs-kernel-datapath-megaflow.md` | Skeleton: microflow → megaflow → ukeys, handler/revalidator threads, NSDI 2015 numbers | §3.3 Block IX, 9.1 (prerequisite), cross-ref Part 13 (OVN sử dụng megaflow installation path) |
| `sdn-onboard/9.3 - ovs-userspace-dpdk-afxdp.md` | Skeleton: DPDK PMD + hugepages + NUMA, AF_XDP alternative, trade-off matrix | §3.3 Block IX, 9.2 (prerequisite), **9.5 (complement: DPDK vs DOCA so sánh)** |
| `sdn-onboard/9.4 - ovs-cli-tools-playbook.md` | Skeleton: ovs-vsctl/ofctl/appctl/dpctl, 6-layer troubleshooting playbook, Capstone Block IX Lab 2 | §3.3 Block IX, 9.3 (prerequisite), 9.5 (CLI là tool verify DOCA offload counters) |
| `sdn-onboard/9.5 - hw-offload-switchdev-asap2-doca.md` | Skeleton mới 2026-04-20: switchdev, ASAP² eSwitch, 3 DPIFs comparison, OVS-DOCA internals, vDPA, BlueField DPU, megaflow scaling 200k-2M | §3.3 Block IX (entry 9.5 mới), 9.3 (trade-off bridge → DOCA), 9.4 (CLI cho `ovs-appctl coverage/show` read DOCA counters), Part 8.1 (Linux bridge/veth tiên quyết) |

> **Capstone positioning trong Block IX:** "Capstone Block IX Lab 2" giữ tại 9.4 (CLI) —
> baseline cho mọi user (không yêu cầu NIC đặc biệt). Lab của 9.5 là **capstone mở rộng**
> cho user có NIC ConnectX-5+ hoặc BlueField (so sánh throughput 3 DPIFs). Quyết định này
> xuất phát từ nguyên tắc accessibility: Block capstone không được đòi hỏi hardware mà
> phần lớn học viên không có.

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

### Tầng 2e: SDN foundation skeletons rev 2 (các Block khác — placeholder)

> Khi bắt đầu S5-S19 cho một Block mới, di chuyển skeleton entries sang Tầng 2c/2d/2f-tương đương
> và liệt kê cross-ref. Hiện tại track Block IX (đã thay đổi 5→6 file), Block 0 (S4 đã viết content),
> Block I (S5.1 bắt đầu Part 1.0, còn 1.1/1.2 pending).

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
