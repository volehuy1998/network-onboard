# Project Memory — network-onboard

> **CRITICAL**: Đọc toàn bộ file này TRƯỚC KHI thực hiện bất kỳ thao tác nào.
> File này là working memory của project, được commit vào git và sync qua mọi thiết bị.

## Owner

VO LE (volehuy1998@gmail.com) — Computer Network Engineer, OpenStack/kolla-ansible, SDN/OVN/OVS researcher.

## Repository Structure

```
network-onboard/                    ← Repo root (GitHub: volehuy1998/network-onboard)
├── CLAUDE.md                       ← FILE NÀY — working memory
├── README.md                       ← Parent README (entry point cho toàn bộ repo)
├── memory/                         ← Deep memory — session log, state tracking
│   ├── session-log.md              ← Log của session gần nhất
│   ├── file-dependency-map.md      ← Bản đồ phụ thuộc giữa các file
│   └── haproxy-series-state.md     ← Trạng thái từng Part trong series
├── haproxy-onboard/                ← HAProxy onboard series (29 Parts, 6 Blocks)
│   ├── README.md                   ← TOC + Knowledge Dependency Map + Version Tracker link
│   ├── 1.0 - haproxy-history-and-architecture.md  ← Part 1 (DONE)
│   ├── references/
│   │   └── haproxy-version-evolution.md  ← Version Evolution Tracker (52 entries)
│   └── images/
├── linux-onboard/                  ← Linux/RHCSA onboard series
├── network-onboard/                ← Network/CCNA onboard series
├── references/                     ← Shared references (The Linux Programming Interface, etc.)
└── images/                         ← Shared images
```

## Mandatory Rules — Đọc trước khi làm bất kỳ điều gì

### Rule 1: Skill Activation Sequence (BẮT BUỘC)

Khi **viết, sửa, hoặc audit/review** file `.md` trong bất kỳ onboard series nào, PHẢI kích hoạt skills theo thứ tự:

> **Bài học từ lỗi thực tế (session 2026-03-30):** Audit Part 1 + cấu trúc series nhưng chỉ
> kích hoạt 2/4 skills (professor-style, document-design), bỏ qua fact-checker và web-fetcher.
> Kết quả: phát hiện lỗi cấu trúc nhưng bỏ sót lỗi factual và dead links.
> Nguyên nhân: diễn giải sai "viết hoặc sửa" → coi audit là "chỉ đọc" → bỏ qua verification.
> **Quy tắc: 4 skills LUÔN kích hoạt cho MỌI tương tác với file .md — không có ngoại lệ.**

```
1. professor-style    → Kiểm soát giọng văn, cấu trúc khái niệm (6 mục: 2.1-2.6)
2. document-design    → Kiểm soát bố cục, heading, learning elements
3. fact-checker       → Xác minh MỌI technical claim trước khi commit
4. web-fetcher        → Xác minh MỌI URL trước khi đưa vào tài liệu
```

**KHÔNG được viết content trước rồi review sau.** Phải đọc skill TRƯỚC → viết → self-audit.

### Rule 2: Cross-File Sync (BẮT BUỘC)

Trước khi commit, kiểm tra `memory/file-dependency-map.md` để xác định file nào bị ảnh hưởng.

Ví dụ thực tế đã xảy ra: sửa `haproxy-onboard/README.md` (version 3.2 → 2.0) nhưng QUÊN sửa `README.md` (parent) — vẫn còn references đến HAProxy 3.2. Nguyên nhân: không có dependency map.

**Quy trình bắt buộc:**
```
1. Xác định file đang sửa
2. Tra dependency map → liệt kê related files
3. Kiểm tra related files có cần cập nhật không
4. Sửa TẤT CẢ related files trong CÙNG commit
```

### Rule 3: Version Annotation Convention

Khi viết nội dung có sự khác biệt giữa các phiên bản HAProxy:

```markdown
> **Lưu ý phiên bản:** <nội dung khác biệt>
```

Đồng thời cập nhật `haproxy-onboard/references/haproxy-version-evolution.md` với entry mới.

### Rule 4: Git Workflow

- **Protected branch**: KHÔNG push trực tiếp lên main/master
- **Commit convention**: Conventional Commits (`feat()`, `fix()`, `docs()`)
- **Branching**: GitHub Flow (main + feature branches)
- Đọc `git-workflow` skill trước mọi thao tác git

### Rule 5: Session Handoff Protocol

Khi KẾT THÚC session (hoặc khi user nói "dừng", "tạm dừng", "kết thúc"):

```
1. Cập nhật memory/session-log.md với:
   - Ngày, thời gian
   - Những gì đã làm (commits, files changed)
   - Những gì CHƯA làm (pending tasks)
   - Branch hiện tại và trạng thái (clean/dirty)
   - Lệnh cần chạy trên local (nếu có, ví dụ: git push)
2. Cập nhật memory/haproxy-series-state.md nếu Part nào thay đổi status
3. Commit memory changes
```

Khi BẮT ĐẦU session mới:
```
1. Đọc CLAUDE.md (file này)
2. Đọc memory/session-log.md → biết context từ session trước
3. Đọc memory/haproxy-series-state.md → biết trạng thái series
4. Kiểm tra git status, git branch, git log
5. Thông báo cho user: "Tôi đã đọc context. Session trước [tóm tắt]. Pending: [danh sách]."
```

### Rule 6: Quality Gate — Pre-flight Checklist (BẮT BUỘC)

> Nguồn gốc: `.claude-skills/quality-gate/SKILL.md` — tích hợp trực tiếp vào đây để enforcement.
> Lý do: skill nằm trong repo nhưng ngoài danh sách registered skills → không bao giờ được trigger tự động.
> Bài học: session trước đã viết section 1.10 (close-on-exec) mà bỏ qua quality-gate hoàn toàn.

**Checklist B — TRƯỚC KHI viết/sửa/audit file .md HOẶC .svg (BẮT BUỘC):**
```
□ 1. Kích hoạt professor-style SKILL → nắm 6 criteria (2.1-2.6)
□ 2. Kích hoạt document-design SKILL → nắm chapter template, heading rules, Rule 8
□ 3. Xác định file đang sửa
□ 4. Tra memory/file-dependency-map.md → liệt kê related files (kể cả Tầng 5: SVG↔markdown)
□ 5. Đọc related files để biết content hiện tại
□ 5b. NẾU sửa SVG: grep tất cả .md tham chiếu SVG → đọc caption hiện tại → ghi nhận entity
□ 6. BẮT ĐẦU viết/sửa (KHÔNG viết trước bước 1-5b)
□ 6b. NẾU sửa SVG: update caption NGAY SAU khi hoàn thành SVG — trước bất kỳ task khác
```

**Checklist C — TRƯỚC KHI commit (BẮT BUỘC):**
```
□ 1. Fact-check: liệt kê MỌI technical claims → verify từng claim
□ 2. URL check: liệt kê MỌI URLs → verify bằng web-fetcher hoặc curl
□ 3. Cross-file sync: tra dependency map → kiểm tra related files
□ 4. Version annotation: nếu có cross-version content → thêm callout + update tracker
□ 5a. SVG spacing+diacritics: nếu có SVG mới/sửa → chạy svg-audit.py + diacritics-audit.py (Rule 6). 0 violation.
□ 5b. SVG-caption consistency: chạy svg-caption-consistency.py cho mỗi SVG đã sửa (Rule 8). 0 mismatch.
□ 6. File integrity: chạy null byte check (Rule 9) trên MỌI file text đã modified. 0 null bytes.
□ 7. Git workflow skill: đọc trước khi commit
□ 8. Self-audit professor-style: chạy 6 criteria (2.1-2.6) lên content vừa viết
```

**Checklist E — Khi thêm Part mới (BẮT BUỘC):**
```
□ 1. Chạy Checklist B
□ 2. Tạo file theo convention: X.0 - <name>.md
□ 3. Include header block + learning objectives theo document-design
□ 4. Cập nhật README.md (TOC, dependency graph)
□ 5. Cập nhật memory/haproxy-series-state.md
□ 6. Cập nhật memory/file-dependency-map.md
□ 7. Chạy Checklist C
```

**Nguyên tắc:** Checklist không phải bureaucracy — giống pre-flight check phi công. Overhead 2-3 phút. Chi phí lỗi đồng bộ: phải sửa lại session sau, tốn thêm commit, có thể bỏ sót.

### Rule 7: Terminal Output Fidelity (BẮT BUỘC)

> Nguồn gốc: session 2026-04-04. Viết unified FD exercise, tự ý cắt output `fdinfo` chỉ giữ `pos:`,
> bỏ `flags:` và `mnt_id:`. User đưa output thật đầy đủ 3 dòng và yêu cầu "không được cắt bớt một
> chữ nào" — nhưng Claude vẫn tuyên bố "khớp hoàn hảo" vì chỉ so giá trị `pos` mà không đếm số dòng.
> Nguyên nhân gốc: không có quy tắc nào trong CLAUDE.md hoặc skills bắt buộc giữ nguyên output.

**Quy tắc:**

Khi user cung cấp terminal output thực để thay thế vào tài liệu:

```
1. KHÔNG được cắt bớt, rút gọn, hoặc lược bỏ bất kỳ dòng nào
2. KHÔNG được sắp xếp lại thứ tự các dòng
3. KHÔNG được thay đổi spacing, indentation, hoặc ký tự nào trong output
4. Khi đối chiếu output: so sánh TỪNG DÒNG (line-by-line diff), không chỉ so giá trị quan tâm
5. Nếu cần rút gọn output vì quá dài: PHẢI hỏi user trước, nêu rõ dòng nào muốn bỏ và lý do
```

Quy tắc này áp dụng cho mọi loại output: `fdinfo`, `lsof`, `ss`, `strace`, `tcpdump`, `haproxy -vv`, log files, và bất kỳ terminal output nào user cung cấp. Output thực là bằng chứng thực nghiệm — cắt bớt bằng chứng là phá hỏng tính xác minh được (reproducibility) của tài liệu.

#### Rule 7a: System Log Absolute Integrity (KHÔNG CÓ NGOẠI LỆ)

> Nguồn gốc: session 2026-04-11. Viết timeline trong SDN 1.0 (FDB poisoning case study)
> nhưng tự ý: (a) merge 3 dòng log riêng biệt thành 1 block, (b) truncate UUID từ đầy đủ
> `0a17b4f8-736d-4bf5-ba1e-335d17cb5973` thành `0a17b4f8`, (c) xóa hoàn toàn 3 dòng
> "Claiming unknown" trong final claim, (d) sửa timestamp `.947` thành `.948`.
> Rationalization sai: "đây là formatted timeline, không phải raw log."
> Log hệ thống là forensic evidence — chỉnh sửa bằng chứng dù dưới dạng nào
> cũng phá hỏng tính toàn vẹn. Rule 7 mục 5 ("hỏi trước") KHÔNG áp dụng cho system log.

Log hệ thống (daemon/service logs, diagnostic tool output) tuân theo nguyên tắc
**toàn vẹn tuyệt đối** — nghiêm ngặt hơn Rule 7 thông thường:

```
1. TUYỆT ĐỐI KHÔNG cắt ngắn, rút gọn, truncate — kể cả UUID, path, IP address
2. TUYỆT ĐỐI KHÔNG merge nhiều dòng log thành 1 entry — mỗi dòng log gốc = 1 visual line
3. TUYỆT ĐỐI KHÔNG xóa dòng log — dù nội dung "lặp lại" hoặc "không quan trọng"
4. TUYỆT ĐỐI KHÔNG thay đổi timestamp — dù chỉ 1 millisecond
5. KHÔNG có ngoại lệ — system log KHÔNG BAO GIỜ được cắt ngắn dưới bất kỳ lý do nào
6. Khi trình bày log trong format khác (timeline, table, annotated block):
   - Message body sau log prefix PHẢI giữ nguyên verbatim trên cùng 1 dòng
   - Mỗi dòng log gốc PHẢI là 1 visual line riêng biệt trong code block
   - Annotation → dòng riêng với prefix "──", KHÔNG chèn vào giữa message body
7. Khi timeline chỉ hiển thị subset: PHẢI ghi "[N dòng khác omitted — context: ...]"
```

Phạm vi: mọi log từ daemon/service (ovn-controller, ovs-vswitchd, nova-compute,
neutron-server, haproxy, nginx, journald, syslog, dmesg) và mọi output từ diagnostic
tools (tcpdump, strace, lsof, ss, conntrack, ovs-ofctl, ovn-trace, ovn-detrace).
Áp dụng KHÔNG PHÂN BIỆT format trình bày — raw, timeline, table, annotated, hay diagram.

### Rule 8: Vietnamese Sentence Completeness (BẮT BUỘC)

> Nguồn gốc: session 2026-04-04. Viết câu bridging "nhưng thực tế không" — từ phủ định "không" bị
> bỏ lửng, thiếu tân ngữ. Người đọc phải tự suy "không" cái gì. User chỉ ra lỗi: "bạn cần giải
> thích rõ nghĩa hơn 4 từ này". Nguyên nhân gốc: professor-style skill (read-only) không có rule
> nào yêu cầu mệnh đề tiếng Việt phải đủ thành phần câu. Bổ sung professor-style 5.4 tại đây.

**Quy tắc:**

Tài liệu viết cho người Việt đọc — mọi mệnh đề phải đủ nghĩa khi đọc đơn lập, không dựa vào
context ngầm. Ba lỗi cụ thể phải tránh:

```
1. Từ phủ định bỏ lửng: "không", "chưa", "chẳng" PHẢI đi kèm động từ hoặc tân ngữ rõ ràng
   Sai:  "...nhưng thực tế không."
   Đúng: "...nhưng kết quả thực tế luôn khớp với dự đoán của mô hình."

2. Đại từ chỉ định mơ hồ: "điều đó", "việc này", "nó" PHẢI có tiền ngữ rõ ràng
   trong cùng câu hoặc câu liền trước. Nếu xa hơn → lặp lại danh từ.
   Sai:  "Fork tạo bản sao. Dup chỉ nhân bản một FD. Điều này giải thích..."
   Đúng: "...Sự khác biệt selective vs wholesale này giải thích..."

3. Phép đọc đơn lập: sau khi viết xong một câu, đọc lại câu đó TÁCH BIỆT khỏi context.
   Nếu nghĩa không rõ khi đứng một mình → viết lại. Tài liệu kỹ thuật không phải
   tin nhắn chat — người đọc có thể mở đúng mục đó mà không đọc từ đầu.
```

### Rule 9: File Integrity — Null Byte Prevention (BẮT BUỘC)

> Nguồn gốc: session 2026-04-04. Commit `9a17eec` chứa file `file-descriptor-deep-dive.md` có
> 3612 trailing null bytes (0x00) ở cuối. GitHub renderer phát hiện null bytes → phân loại file
> là binary → từ chối render markdown. VS Code preview bỏ qua trailing nulls → hiển thị bình
> thường → user không phát hiện cho đến khi merge PR #35 lên master và mở trên GitHub.
> Nguyên nhân gốc: Write tool đôi khi padding null bytes vào cuối file (sparse file behavior
> hoặc buffer không flush sạch). Không có bước kiểm tra nào trong Checklist C phát hiện lỗi này.

**Quy tắc:**

TRƯỚC KHI `git add` bất kỳ file nào, chạy kiểm tra file integrity:

```bash
# Bước 1: Kiểm tra null bytes trong mọi file đã modified/staged
for f in $(git diff --name-only --cached 2>/dev/null; git diff --name-only); do
  if [ -f "$f" ]; then
    nullcount=$(python3 -c "print(open('$f','rb').read().count(b'\x00'))")
    if [ "$nullcount" -gt 0 ]; then
      echo "BLOCKED: $f chứa $nullcount null bytes"
    fi
  fi
done

# Bước 2: Nếu phát hiện null bytes → loại bỏ trước khi commit
python3 -c "
d = open('FILE','rb').read()
clean = d.replace(b'\x00', b'')
open('FILE','wb').write(clean)
print(f'Removed {len(d)-len(clean)} null bytes')
"

# Bước 3: Verify lại — kết quả PHẢI là 0
grep -cP '\x00' FILE
```

**Phạm vi áp dụng:** Mọi file text (.md, .py, .sh, .yml, .html, .svg, .css, .js). Null bytes
trong file text là LUÔN LUÔN lỗi — không có trường hợp hợp lệ nào. File binary (.png, .jpg,
.pdf) được miễn kiểm tra này.

**Dấu hiệu cảnh báo sớm:**
- `file` command báo "with very long lines" trên file .md → kiểm tra ngay
- File size bất thường lớn so với số dòng (ví dụ: 93KB cho 1169 dòng text thuần)
- GitHub hiển thị file như binary hoặc wall of text không format

## Current State

| Key | Value |
|-----|-------|
| Active branch | `docs/sdn-foundation-rev2` (S3 rename + renumber completed, 2026-04-20) |
| Master HEAD | `a416dcf` — chore(memory): update session log and dependency map for session 4 |
| HAProxy baseline | HAProxy 2.0 on Ubuntu 20.04 (Canonical repo) |
| HAProxy Parts | 1/29 completed (Part 1 only, fact-checked, Quiz added) |
| Linux FD doc | `linux-onboard/file-descriptor-deep-dive.md` — **1265 lines, 14 SVG figures** |
| FD exercises | 7/9 verified. Exercise 7 (strace) + Exercise 8 (FD limit) cần lab |
| SDN 17.0 doc | `sdn-onboard/17.0 - ovn-l2-forwarding-and-fdb-poisoning.md` — **1178 lines** (renamed từ `1.0 - ovn-l2-...` ở S3; renumbered Phần 1 → Phần 17, mục 1.X → 17.X; forward refs tới Part 19 §19.2/§19.4/§19.5-19.6) |
| SDN 18.0 doc | `sdn-onboard/18.0 - ovn-arp-responder-and-bum-suppression.md` — **496 lines** (renamed từ `2.0 - ovn-arp-...` ở S3; renumbered Phần 2 → Phần 18, mục 2.X → 18.X; cross-refs sang Part 17 mục 17.4/17.6 đã cập nhật) |
| SDN 19.0 doc | `sdn-onboard/19.0 - ovn-multichassis-binding-and-pmtud.md` — **1379 lines, 127,903 bytes** (renamed từ `3.0 - ovn-multichassis-...` ở S3; renumbered Phần 3 → Phần 19, §3.X → §19.X; RFC refs RFC 791 §3.1 / RFC 8926 §3.4/§3.5 preserved intact) |
| S3 status | S3.1-S3.5 completed 2026-04-20. Working tree pending: commit S3 rename+renumber + metadata sync. S3.6 = null byte check + commit. Legacy artifact `sdn-onboard/.fuse_hidden...` là sandbox fuse lock, sẽ tự động giải phóng khi file bị `git rm` local. |
| Experiment plan | `memory/experiment-plan.md` — Phases A-E, priority-ordered |

## Skill Quick Reference

| Skill | Khi nào dùng |
|-------|-------------|
| professor-style | MỌI nội dung giảng dạy, viết .md, giải thích kỹ thuật |
| document-design | MỌI file .md trong onboard series |
| fact-checker | MỌI technical claim, CLI command, config directive |
| web-fetcher | MỌI URL cần fetch hoặc verify |
| git-workflow | MỌI thao tác git: commit, push, branch, PR |
| flow-graph | Sequence diagram, protocol flow, handshake diagram |
| quality-gate | MỌI thao tác viết/sửa/commit — pre-flight checklist (Rule 6 ở trên) |

## Preferences

- Accuracy first — double-check everything, cross-reference multiple sources
- No AI writing patterns — professor/PhD teaching style
- No emoji in technical content
- Real examples with verifiable output
- Concise but deep — analyst/engineer tone, not mechanical
- Vietnamese language for documentation content
