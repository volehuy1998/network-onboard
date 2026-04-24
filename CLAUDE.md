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

Repo onboard đã cài đặt **6 skill** tại `~/.claude/skills/`. Tất cả 6 skill đều phải được sử dụng — không skip bất kỳ skill nào khi điều kiện kích hoạt thoả mãn.

> **Bài học từ lỗi thực tế (session 2026-03-30):** Audit Part 1 + cấu trúc series nhưng chỉ
> kích hoạt 2/4 skills (professor-style, document-design), bỏ qua fact-checker và web-fetcher.
> Kết quả: phát hiện lỗi cấu trúc nhưng bỏ sót lỗi factual và dead links.
> Nguyên nhân: diễn giải sai "viết hoặc sửa" → coi audit là "chỉ đọc" → bỏ qua verification.
> **Quy tắc: 4 core skill LUÔN kích hoạt cho MỌI tương tác với file .md — không có ngoại lệ.**
> **Bổ sung session 2026-04-22:** sau khi cài đặt thêm `deep-research` + `search-first`,
> repo có đủ 6 skill. Hai skill bổ sung kích hoạt theo điều kiện (xem bảng 2) — không mặc định
> LUÔN kích hoạt như 4 core, nhưng phải được cân nhắc trước khi bỏ qua.

**Nhóm A — Core 4 skill (LUÔN kích hoạt cho MỌI tương tác với file .md):**

```
1. professor-style    → Kiểm soát giọng văn, cấu trúc khái niệm (6 mục: 2.1-2.6)
2. document-design    → Kiểm soát bố cục, heading, learning elements
3. fact-checker       → Xác minh MỌI technical claim trước khi commit
4. web-fetcher        → Xác minh MỌI URL trước khi đưa vào tài liệu
```

**Nhóm B — 2 skill bổ sung (kích hoạt theo điều kiện — PHẢI cân nhắc trước khi bỏ qua):**

```
5. search-first       → Trước khi viết code/script/utility mới. Tìm tool/library/MCP/skill
                         đã tồn tại trước khi tự viết. Áp dụng cho mọi tác vụ coding trong
                         repo (scripts/, lab tooling, Python audit script, SVG tooling).
                         Nguyên tắc: "Adopt > Extend > Compose > Build" — chỉ build custom
                         khi 3 lựa chọn trên đã loại trừ.

6. deep-research      → Khi cần research multi-source có citation cho nội dung onboard
                         (technology evaluation, protocol history, vendor comparison,
                         market/adoption data). Dùng firecrawl + exa MCP để lấy 15-30 nguồn,
                         synthesize thành cited report. BẮT BUỘC khi viết content Phase B
                         mà topic vượt quá phạm vi offline sources (doc/*) + bản năng LLM.
```

**Quy trình áp dụng toàn bộ 6 skill:**

```
1. Mở file .md để viết/sửa/audit → kích hoạt Core 4 (Nhóm A) ngay lập tức
2. Trước khi viết code/script hỗ trợ (bash/Python/SVG tooling) → kích hoạt search-first
3. Trước khi viết content section cần multi-source research → kích hoạt deep-research
4. Ghi rõ trong fact-forcing gate answer những skill nào đã kích hoạt cho task này
5. Nếu bỏ qua skill nào trong Nhóm B → PHẢI giải thích lý do (vd: topic đã có đủ doc/*
   offline source; hoặc script < 10 dòng một lần dùng; hoặc coding task chỉ là edit
   nhẹ file có sẵn)
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
□ 7a. Rule 11 Vietnamese Prose scan (BẮT BUỘC — không skip):
     - Chạy regex `§11.6` full trên MỌI file .md đã modified — KHÔNG chỉ `inspect|support`
     - Phân loại từng hit theo §11.3 (named identifier vs prose)
     - Fix mọi prose hit bold label + section heading + câu văn tư duy
     - Nếu gặp từ mới chưa có trong §11.2 dictionary → bổ sung vào CLAUDE.md cùng commit
□ 7b. Rule 11 spot-check bold label + section heading:
     - grep '^##' <file> — mọi heading prose phải Việt (trừ tên concept/stage)
     - grep -E '^\*\*[A-Z][a-z]+' <file> — mọi bold label đầu câu phải Việt (trừ tên concept)
     - grep -E '^> \*\*(Key Topic|Hiểu sai|Điểm mấu chốt)' <file> — callout label phải Việt
□ 7c. Rule 13 Em-dash density (BẮT BUỘC):
     - Đếm em-dash/dòng mỗi file modified. Target < 0.10
     - Nếu > 0.10: audit từng em-dash theo §13.2, fix prose overuse
     - Final density phải < 0.10 sau fix
□ 8. Git workflow skill: đọc trước khi commit
□ 9. Self-audit professor-style: chạy 6 criteria (2.1-2.6) lên content vừa viết
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

### Rule 10: Architecture-First Doctrine (BẮT BUỘC)

> Nguồn gốc: session 2026-04-21 (session 7). Khi bắt đầu S5.1, Claude đã viết full content 198
> dòng cho Part 1.0 (networking-industry-before-sdn) thay vì chỉ skeleton (title + summary).
> User correction: "chúng ta đang kiến trúc bài giảng chứ chưa hề đi sâu vào nội dung... bạn có
> quyền kiến trúc thư mục, file, ghi trước tựa đề và tóm tắt nội dung của tựa đề đó nhưng đừng
> sa đà vào nội dung". Nguyên nhân gốc: plan `sdn-foundation-architecture.md` ghi "S5 = Block I
> content (~1200 dòng)" khiến Claude hiểu nhầm đây là content phase. Thực tế project đang ở
> **architecture phase** — xây khung toàn bộ 17 blocks trước, viết content sau khi khung xong.

**Quy tắc:**

Trong phase hiện tại (**Architecture Phase**), Claude CHỈ được phép:

```
1. Tạo cấu trúc thư mục (mkdir)
2. Tạo file skeleton theo naming convention X.Y - <name>.md
3. Viết trong mỗi skeleton:
   - Header block (trạng thái, block, part, prerequisites, ebook mapping)
   - Mục tiêu bài học (3-5 Bloom objectives)
   - Section headings (## X.Y.Z) với tên đầy đủ
   - Tóm tắt ngắn dưới mỗi heading (1-3 câu mô tả nội dung SẼ viết — không phải nội dung)
   - Placeholder cho exercises/labs (tên + mục đích, không chi tiết)
   - Tài liệu tham khảo placeholder
```

**Claude KHÔNG được viết trong phase này:**

```
1. Đoạn văn giải thích khái niệm chi tiết (>3 câu liên tục)
2. Ví dụ cụ thể (config snippet, CLI output, log lines)
3. Bảng so sánh đầy đủ dữ liệu
4. Guided Exercise có nội dung step-by-step
5. References với URL đầy đủ và annotation
6. Analysis/reasoning content
```

**Dấu hiệu cảnh báo over-scope:**
- File skeleton > 80 dòng (skeleton target: 30-60 dòng)
- Đang gọi curl/WebFetch để verify technical claims → DỪNG, claim đó là content
- Đang viết `### ▶ Guided Exercise N: ...` có bullet steps → DỪNG, chỉ ghi title + 1-2 câu mục đích
- Đang viết code block với output cụ thể → DỪNG, placeholder `*Code example sẽ được thêm khi viết content phase*`

**Khi nào chuyển sang Content Phase:**

Chỉ khi (a) toàn bộ skeleton Block 0-XVI completed (~60 file), (b) user review architecture end-to-end, (c) user explicitly nói "chuyển sang viết content" hoặc "bắt đầu content phase". Không tự ý chuyển.

**Di sản over-scope đã xảy ra:**

```
sdn-onboard/0.0 - how-to-read-this-series.md     148 dòng content (S4, session 6)
sdn-onboard/0.1 - lab-environment-setup.md       426 dòng content (S4, session 6)
sdn-onboard/1.0 - networking-industry-before-sdn.md  198 dòng content (S5.1, session 7)
```

Các file này KHÔNG revert (commit đã push lên remote). Nhưng từ Part 1.1 trở đi + mọi Block mới
PHẢI tuân Rule 10. Khi chuyển sang Content Phase, xem 3 file trên là reference implementation
(style, cấu trúc heading, reference format) và viết lại các Part còn lại theo cùng chuẩn.

### Rule 11: Vietnamese Prose Discipline (BẮT BUỘC)

> Nguồn gốc ban đầu: session 13, 2026-04-21. User chỉ ra 9 ví dụ điển hình về English abuse
> trong Phase B content Block I-VI (~890 English hit trên 24 file, mật độ 5-26%).
> Ví dụ: "hypervisor overlay paradigm" thay vì "mô hình hypervisor overlay",
> "VMware announce acquisition Nicira" thay vì "VMware thông báo mua lại Nicira",
> "troubleshoot tunnel issue cần inspect 2 layer" thay vì "khắc phục sự cố tunnel
> cần kiểm tra 2 lớp". Root cause: mental model khái niệm trừu tượng hình thành
> trong tiếng Anh, không translate khi viết Việt → câu lai bad.
>
> Mở rộng session 22+23, 2026-04-22. User phát hiện Part 9.22+9.23+9.24 tái phạm
> Rule 11 có hệ thống (60+ hit trên 1464 dòng): "Sequential evaluation" bold label,
> "Abstraction level / Auto zone assignment / Distributed commit" bold label,
> "operator manage thứ tự", "experiment để verify", "fail" lặp 4 lần, "motivation
> cho Part 9.24", "performance cho traffic symmetric", v.v. Session log tự báo
> cáo "Rule 11 OK" vì chỉ chạy regex catch `inspect|support` — bỏ sót toàn bộ
> nhóm vocabulary mới. User làm rõ nguyên tắc **dịch đúng nơi đúng chỗ**: cùng
> một từ (routing, output, table, state, flow, forwarding), nếu xuất hiện như
> named identifier / syntax / tên stage của OVS-OpenFlow-OVN thì GIỮ English;
> nếu xuất hiện trong prose mô tả thì DỊCH Việt.

**Đây là chương trình đào tạo cho người Việt Nam đọc** — ưu tiên tiếng Việt tự nhiên, chỉ giữ tiếng Anh cho named entity/cú pháp/identifier. Nguyên tắc cốt lõi: **dịch đúng nơi đúng chỗ**.

#### 11.1. Giữ English khi từ xuất hiện như một trong các vai trò sau

- **Tên sản phẩm / dự án / tổ chức**: OpenFlow, OVS, OVN, Open vSwitch, NETCONF, NSX, Nicira, VMware, Linux, Ubuntu, Mininet, Cisco, Broadcom Trident, Stanford, ONF, GitHub, Spamhaus, Prometheus, Arbor Networks, Cloudflare, DigitalOcean, Red Hat, NVIDIA ConnectX-6, Intel E810, Anthropic.
- **Protocol / acronym chuẩn quốc tế**: TCP, UDP, IP, ICMP, SCTP, ARP, DNS, TLS, SSH, HTTP, HTTPS, VLAN, VXLAN, Geneve, BGP, OSPF, BFD, MPLS, NAT, SNAT, DNAT, DDoS, RPC, ECMP, FTP.
- **CLI verbatim & flag**: `ovs-ofctl`, `ovs-vsctl`, `ovs-appctl`, `ovs-dpctl`, `ovn-nbctl`, `ovn-sbctl`, `ovn-northd`, `ovn-controller`, `conntrack`, `iptables`, `modprobe`, `sysctl`, `sudo`, `ping`, `iperf`, `tcpdump`, `--dpdk`, man page reference `ovs-fields(7)`, `ovs-actions(7)`, `ovn-architecture(7)`.
- **Spec field name / match field / OpenFlow identifier**: `ct_state`, `ct_zone`, `ct_mark`, `ct_label`, `metadata`, `cookie`, `priority`, `in_port`, `nw_src`, `nw_dst`, `dl_src`, `dl_dst`, `dl_type`, `tp_dst`, `sport`, `dport`, `reg0..reg15`, `xreg0..xreg7`, OXM, NXM.
- **Action name / instruction name / stage name của OpenFlow-OVS-OVN**: `goto_table`, `resubmit`, `output`, `normal`, `drop`, `mod_dl_src`, `mod_dl_dst`, `dec_ttl`, `ct()`, `ct(commit)`, `ct_next`, `ct_commit`, `ct_lb`, `ct_clear`, `apply_actions`, `write_actions`, `write_metadata`, `clear_actions`, `Apply-Actions`, `Write-Actions`, `Clear-Actions`, `Write-Metadata`, `Goto-Table`, `allow`, `allow-related`, `reject`, `set_queue`, action value như `ct_state=+trk+new`.
- **Pipeline stage / table name khi dùng như nhãn**: "Table 0 Classifier", "Table 1 L3 Forwarding", "Ingress ACL", "Egress ACL", "(ACL, routing, output)", "(ingress ACL → LB → routing → egress ACL)". Các từ này là **tên stage** trong kiến trúc pipeline OVS/OVN, KHÔNG dịch dù thoạt nhìn giống vocabulary thường.
- **Literal value của state / flag / protocol**: `NEW`, `ESTABLISHED`, `RELATED`, `INVALID`, `SYN_SENT`, `SYN_RECV`, `FIN_WAIT`, `TIME_WAIT`, `CLOSE`, `CLOSE_WAIT`, `LAST_ACK`, `UNREPLIED`, `ASSURED`, `[NEW]`, `[UPDATE]`, `[DESTROY]`.
- **Thuật ngữ ngành mạng quốc tế phổ biến**: SDN, DC, WAN, LAN, DPU, ASIC, NOS, VM, RFC, MAC, VIP, NFV, SR-IOV, SmartNIC, FIB, BUM, DMZ, VPN, L2, L3, L4, five-tuple (5-tuple), three-way handshake, pseudo-state, bitfield, tuple, hairpin, subnet, broadcast, multicast, unicast, datapath, bridge, kernel, userspace, namespace, tenant, multi-tenant, chassis, overlay, underlay, east-west, north-south, fast path, slow path, line-rate, offload, DPDK.
- **Concept từ OpenFlow / OVS spec dùng như noun**: flow, flow entry, flow table, flow rule, pipeline, multi-table pipeline, match field, action set, instruction, controller, stateful, stateless, conntrack, handshake.

#### 11.2. Dịch Việt khi từ xuất hiện trong prose mô tả / giải thích

**Vocabulary tư duy — LUÔN dịch:**

| English | Vietnamese | English | Vietnamese |
|---|---|---|---|
| paradigm | mô hình | architecture | kiến trúc |
| approach | cách tiếp cận | deployment | triển khai |
| support | hỗ trợ | adoption | sự chấp nhận / việc áp dụng |
| trade-off | sự đánh đổi | backward compat | tương thích ngược |
| lock-in | bị phụ thuộc vào | rebrand | đổi tên thương hiệu |
| announce | thông báo / công bố | troubleshoot | khắc phục sự cố |
| inspect | kiểm tra | integration | tích hợp |
| exclusive | độc quyền | steep learning curve | quá trình học hỏi rất khó khăn |
| operator | người vận hành | engineer | kỹ sư |
| developer / dev team | nhóm phát triển | performance | hiệu năng |
| optimization | tối ưu hoá | overhead | chi phí phụ |
| compile (verb) | biên dịch | compiler (noun) | compiler (giữ) / trình biên dịch |
| deploy (verb) | triển khai | deployment (noun) | việc triển khai |
| experiment (noun) | thử nghiệm / thí nghiệm | verify | kiểm chứng |
| fail / failure | thất bại | behavior | hành vi |
| motivation | động cơ | criteria | tiêu chí |
| subtle | tinh tế | pedagogical | sư phạm |
| explicit | tường minh | implicit | ngầm định |
| version | phiên bản | strict | nghiêm ngặt |
| tolerate | chấp nhận | undefined | không xác định |
| guideline | hướng dẫn | convention | quy ước |
| bypass (verb) | né / vượt qua | modify | sửa |
| rewrite | sửa / viết lại | report (verb) | báo / báo cáo |
| input / output (noun, prose) | đầu vào / kết quả | control (noun, prose) | điều khiển / kiểm soát |
| tracking mechanism | cơ chế theo dõi | state tracking | theo dõi trạng thái |
| track (verb, prose) | theo dõi | monitoring | giám sát |
| monitor event | theo dõi sự kiện | event stream | luồng sự kiện |
| symmetric | đối xứng | asymmetric | không đối xứng / một chiều |
| bidirectional | hai chiều | unidirectional / one-way | một chiều |
| communication | giao tiếp | connection (prose) | kết nối |
| session (prose) | phiên | lookup (prose) | tra cứu |
| pattern (prose) | mẫu | template (prose) | khuôn mẫu |
| namespace isolation | cô lập namespace | multi-tenant isolation | cô lập multi-tenant |
| overlap | chồng lấn | multiplex | ghép kênh |
| modularization | module hoá | modular | module hoá |
| flexibility | tính linh hoạt | concern | nhiệm vụ / mối quan tâm |
| transfer control | chuyển giao điều khiển | recirculate (trong prose) | đưa về pipeline |
| expression (prose) | biểu thức | assignment (prose) | việc gán |
| read-only (prose) | chỉ đọc | read / write (prose) | đọc / ghi |
| junior / senior | mới vào nghề / kỳ cựu | production (IT) | **môi trường production** (giữ "production") |
| production (manufacturing) | sản xuất | incident | sự cố |
| post-mortem | báo cáo hậu sự | beyond lifetime | vượt quá vòng đời |
| debug (verb, prose) | gỡ lỗi | debugging (noun) | việc gỡ lỗi |
| scale (noun, prose) | quy mô | scalability | khả năng mở rộng |
| flow explosion | bùng nổ flow | table explosion | bùng nổ bảng |
| cross-product | tích chéo | termination | tính kết thúc |
| traffic (prose) | lưu lượng | packet (prose) | gói tin |
| forwarding (prose, verb nghĩa "chuyển tiếp") | chuyển tiếp | routing (prose, verb nghĩa "định tuyến") | định tuyến |
| rule ordering | thứ tự rule | first-match wins | ai match trước thì thắng |
| consumer (prose IT) | người tiêu thụ / consumer | buy-in | sự ủng hộ |
| shepherd (verb) | dẫn dắt | worry (verb) | lo ngại / lo lắng |
| favor (verb) | ưu ái | bent (verb) | bẻ cong |
| workaround | biện pháp tạm thời | unusual | bất thường |
| significant (adj prose) | đáng kể / có ý nghĩa lớn | industry dynamics | động lực ngành |
| promote adoption | thúc đẩy sự chấp nhận | advocate for | vận động cho |

#### 11.3. Cùng một từ, lúc dịch lúc không — minh hoạ

| Từ | Giữ English khi | Dịch Việt khi |
|---|---|---|
| `routing` | Tên stage: `(ACL, routing, output)`, `L3 Forwarding`, `distributed routing` (cụm danh từ OVN) | Prose động từ: "gói tin được định tuyến sang subnet khác" |
| `output` | Action: `action=output:3`; tên stage trong tuple `(ACL, routing, output)` | Prose: "kết quả của toàn bộ pipeline", "đầu ra của trace" |
| `table` | OpenFlow concept: `table=0`, "multi-table pipeline", "table lookup trong OpenFlow" | Prose: "bảng FIB L3", "bảng MAC", "bảng trạng thái conntrack" |
| `forwarding` | Tên table: "Table 2 L2 Forwarding" | Prose: "chuyển tiếp gói tin sang h3" |
| `state` | Field name: `ct_state`; literal: `state=ESTABLISHED` | Prose: "theo dõi trạng thái", "máy trạng thái" |
| `flow` | OpenFlow concept: "flow entry", "flow table", "flow rule" | Generic (hiếm dùng): "luồng dữ liệu" |
| `traffic` | Hiếm khi giữ | Prose: "lưu lượng đông-tây", "lưu lượng reply" |
| `connection` | Conntrack literal: `connection ESTABLISHED` | Prose: "kết nối hai chiều", "kết nối h1 → h3" |
| `switch` | Tên thiết bị: switch `s1`, OVS switch | Động từ "chuyển đổi" thì dịch |
| `monitoring` | Tên công cụ/component: "Monitoring tool" | Prose: "giám sát bảng trạng thái" |
| `pattern` | Code/config pattern name | Prose: "mẫu 7-flow Lab 8" |
| `commit` | CLI/action: `ct(commit)`, `commit entry` | Prose: "tạo entry tồn tại vượt quá vòng đời gói tin" |

**Câu hỏi để tự phân loại:** từ này có phải là *tên riêng* mà tài liệu OVS/OpenFlow/OVN dùng để gọi một entity, syntax, hoặc stage không? Nếu CÓ → giữ English. Nếu KHÔNG (từ dùng để mô tả, giải thích, kể chuyện) → dịch Việt.

#### 11.4. Bold label và section heading

**KHÔNG được để English cho:**
- Section heading prose: `## Guided Exercise 2 — State table inspection và TCP lifecycle` → `## Guided Exercise 2 — Kiểm tra state table và vòng đời TCP` (giữ `Guided Exercise` + `state table` là concept; dịch `inspection` → `Kiểm tra`, `TCP lifecycle` → `vòng đời TCP`).
- Bold label mở đầu đoạn: `**Sequential evaluation.**` → `**Đánh giá tuần tự.**`; `**Abstraction level.**` → `**Mức trừu tượng.**`; `**Auto zone assignment.**` → `**Tự động gán zone.**`; `**Distributed commit.**` → `**Commit phân tán.**`.
- Callout label nội bộ: `> **Key Topic:**` → `> **Điểm mấu chốt:**`.

**Được giữ English cho:**
- Section heading là tên concept/stage: `## 9.24.3 Action ct() — ngữ nghĩa đầy đủ`, `## 9.24.7 ct_zone — cô lập multi-tenant`.
- Bold label là tên concept: `**NEW**`, `**ESTABLISHED**`, `**commit**`, `**zone=N**`.

#### 11.5. Test đọc đơn lập + Hybrid acceptable + Misconception callout

- Sau khi viết xong một câu, đọc tách biệt khỏi context. Nếu câu có > 3 từ tiếng Anh không phải technical term chuẩn → rewrite.
- Hybrid acceptable: "tích hợp với vSphere" (technical term + từ nối thuần Việt). Không viết "integrate với vSphere".
- Câu quote trong `> **Hiểu sai:** *"..."*` phải đầy đủ tiếng Việt — chỉ giữ tên sản phẩm / action / field / literal.

#### 11.6. Checklist scan trước khi commit (BẮT BUỘC)

Không được tin tưởng vào regex lẻ `inspect|support`. BẮT BUỘC chạy lần lượt:

```bash
# Scan nhóm vocabulary tư duy — dùng ripgrep case-insensitive
grep -niE '\b(paradigm|architecture|approach|deployment|adoption|trade-?off|lock-?in|rebrand|announce|troubleshoot|inspect|integration|exclusive|operator|engineer|performance|optimization|overhead|compile[rd]?|deploy(ment)?|experiment|verify|fail(ure)?|behavior|motivation|criteria|subtle|pedagogical|explicit|implicit|version|strict|tolerate|undefined|guideline|convention|bypass|modify|rewrite|report(ing)?|input|output|control|tracking|symmetric|bidirectional|communication|session|lookup|pattern|template|namespace|overlap|multiplex|modular|flexibility|concern|expression|assignment|junior|senior|incident|post-?mortem|lifetime|debug(ging)?|scale|scalability|rule|first-?match|track(ing)?|monitor(ing)?|event)\b' <file.md>
```

Kết quả không nên trống — phần lớn hit là false positive (trong URL, code block, product name). Phân loại từng hit:
1. **Inside URL, code block, CLI sample** → skip.
2. **Tên sản phẩm/tổ chức/concept OpenFlow-OVS-OVN** → skip.
3. **Bold label / section heading / prose tư duy** → FIX Việt hóa.

Nếu nghi ngờ, áp dụng câu hỏi §11.3: "đây có phải tên riêng trong thế giới OVS không?"

#### 11.7. Khi thêm từ mới vào dictionary

Nếu trong quá trình review gặp một từ chưa có trong §11.2, BỔ SUNG vào bảng ngay lập tức trong cùng commit fix, kèm ví dụ ngữ cảnh. Dictionary là tài liệu sống — không đông cứng ở phiên bản session 22+23.

Từ điển mở rộng chi tiết: `.claude/plans/tender-scribbling-comet.md` Phần 1 (plan session 13) + retrofit session 22+23 trong cùng file này.

### Rule 12: Exhaustive Offline Source Exploration (BẮT BUỘC)

> Nguồn gốc: session 14, 2026-04-22. Khi bắt đầu Phase B cho Block VII, Claude dùng Glob
> pattern `**/*.skill` + `.claude-skills/**/*` mà không recursive explore `sdn-onboard/doc/`.
> Kết quả: bỏ sót toàn bộ kho offline USC/Crichigno trong `sdn-onboard/doc/ovs/` (11 PDF + TXT),
> viết 4 file Block VII + Part 9.0 mà không cite offline sources. User chỉ ra: "tôi đã bảo
> sdn-onboard/doc/* là tài liệu offline quý giá nhưng vì sao không nằm trong danh sách file/line
> tham chiếu?" và "sdn-onboard/doc/ovs/* không nằm trong context của bạn à?"

**Quy tắc:**

Khi bắt đầu session làm việc với onboard series, TRƯỚC KHI viết bất kỳ content nào, BẮT BUỘC
inventory đầy đủ kho offline bằng recursive Glob:

```
Glob "sdn-onboard/doc/**/*"        (không phải chỉ "sdn-onboard/doc/*")
Glob "haproxy-onboard/doc/**/*"    (tương tự cho series khác)
Glob "linux-onboard/doc/**/*"
Glob "network-onboard/doc/**/*"
Glob "references/**/*"
```

**Quy trình bắt buộc:**

```
1. Session start:
   - Chạy recursive Glob liệt kê mọi file trong */doc/** và references/**
   - Lập bảng mapping: file offline nào → Block/Part nào sử dụng
   - Ghi nhớ bảng này trong memory nếu session dài

2. Trước mỗi Write file .md content:
   - Kiểm tra mapping: doc file nào phù hợp với topic này
   - LIỆT KÊ đầy đủ trong fact-forcing gate answer:
     "Nguồn offline cung cấp content: <đường dẫn cụ thể> — <chapter/section>"
   - Include trong header block của file: "> **Nguồn offline chính:** ..."
   - Include trong References section cuối file

3. Nếu user cung cấp nhắc nhở về offline sources:
   - Stop ngay lập tức
   - Re-run recursive Glob
   - Identify gap
   - Propose remediation (backfill existing files + apply prospectively)
```

**Dấu hiệu vi phạm Rule 12:**

- Fact-forcing gate answer thiếu dòng "Nguồn offline cung cấp content"
- File content header không có "> **Nguồn offline chính:**"
- References section không có mục cho offline source
- Viết content technical mà không có doc/* citation dù topic có sẵn trong compass/USC labs

**Phạm vi áp dụng:** Mọi session onboard series. Không có ngoại lệ — dù topic có vẻ "quá đơn giản"
hay "không cần source", vẫn phải verify offline mapping trước khi kết luận.

**Di sản khắc phục đã làm (session 14):**

- Backfill `doc/*` references vào `9.0 - ovs-history-2007-present.md` và `9.1 - ovs-3-component-architecture.md`
- Viết 13 file content Block IX (9.0-9.14 + backfill) với đầy đủ doc/* citation
- 4 file Block VII (7.0-7.3) không có doc/* vì controller ecosystem không được cover bởi compass/USC labs
- Part 9.0-9.14 citation pattern: compass_artifact Chapter X + USC Lab Y (nếu có) + online upstream URL

### Rule 13: Em-dash Discipline (BẮT BUỘC)

> Nguồn gốc: session 24, 2026-04-23. User phát hiện em-dash (—) bị lạm dụng xuyên suốt Phase D Part 9.22/9.23/9.24/9.25 — mật độ 0.13-0.19 em-dash/dòng. Tổng 361 em-dash trên 4 file ~2.100 dòng. Đa phần dùng em-dash thay vì diễn đạt tự nhiên tiếng Việt (comma, period, colon, parentheses). Chữ Việt không cần nhiều em-dash như tiếng Anh — mỗi em-dash người đọc phải dừng lại suy nghĩ ngắt câu. Quá nhiều em-dash làm văn bản đứt gãy, khó đọc. User: *"Hãy audit toàn bộ em-dash, tôi thấy ký hiệu đang bị lạm dùng quá nhiều thay vì sử dụng ngôn ngữ tự nhiên để diễn đạt."*

**Nguyên tắc cốt lõi: em-dash là ngoại lệ, không phải mặc định.**

Khi viết prose tiếng Việt, KHÔNG dùng em-dash thay cho dấu câu thông thường. Mặc định ưu tiên:
- **Dấu phẩy (,)** khi continuation cùng mệnh đề
- **Dấu chấm (.) + viết hoa** khi sang câu mới
- **Dấu hai chấm (:)** khi giới thiệu danh sách hoặc giải thích
- **Ngoặc đơn (...)** khi aside / parenthetical
- **Xuống dòng + bullet list** khi enumerate 3+ mục

#### 13.1. Em-dash được phép dùng khi

1. **Heading-subtitle separator**: `# 9.22. OVS multi-table pipeline — \`goto_table\`, \`resubmit\``. Em-dash tách tiêu đề chính và mô tả phụ trong heading level 1-3. Mỗi heading 0-1 em-dash tối đa.

2. **Bold mini-label separator trong mô tả rule/flow có cấu trúc**: `**Quy tắc 1 — Luôn bắt đầu ở table 0.**`, `**Flow 1 — default normal processing**`. Em-dash ngăn cách ID và label text của rule/flow có cấu trúc đồng đều.

3. **Bold noun + inline code list**: `**Instruction** là lệnh ở cấp *table entry* — \`Apply-Actions\`, \`Write-Actions\`, ...`. Em-dash introduce danh sách inline code sau câu mô tả (colon `:` cũng OK).

4. **Attribution tách tổ chức/ngày**: `(Crichigno, Sharif, Kfoury — University of South Carolina, NSF Award 1829698)`. Hoặc có thể dùng ngoặc đơn / comma tuỳ ngữ cảnh.

5. **Table row visual label trong code block**: `Table 0 — Port security + VLAN decap`. Khi dùng ASCII diagram trong ```` ``` ```` block để mô tả pipeline layout.

#### 13.2. Em-dash KHÔNG được dùng khi

1. **Thay dấu phẩy trong câu prose liền mạch**: SAI `OVS-based OVN 22.03 có optimization — `allow` bỏ qua luôn lệnh `ct()`` → ĐÚNG `OVS-based OVN 22.03 có tối ưu hoá: `allow` bỏ qua luôn lệnh `ct()`.`.

2. **Thay dấu chấm khi sang câu mới**: SAI `Không có gói tin nào được gửi thật — đây là simulation thuần tuý` → ĐÚNG `Không có gói tin nào được gửi thật. Đây là simulation thuần tuý`.

3. **Thay đại từ quan hệ "là, nghĩa là, tức là"**: SAI `OpenFlow 1.0.0 — bản đặc tả đầu tiên` → ĐÚNG `OpenFlow 1.0.0, bản đặc tả đầu tiên`.

4. **Trong bullet definition "- X — giải thích"**: SAI `- \`cookie=0xN\` — nhãn nhóm flow (Part 9.19 §19.4).` → ĐÚNG `- \`cookie=0xN\`: nhãn nhóm flow (Part 9.19 §19.4).`.

5. **Trong header block metadata (> **Label:** ...)**: SAI `> **Plan:** §F.4.5 — Phase D flow debugging toolbox.` → ĐÚNG `> **Plan:** §F.4.5, Phase D flow debugging toolbox.`.

#### 13.3. Ngưỡng mật độ (density threshold)

| Mức | Em-dash/dòng | Đánh giá |
|-----|-------------|----------|
| < 0.05 | 1 em-dash mỗi 20 dòng | Tự nhiên, đúng mức |
| 0.05 - 0.10 | 1 em-dash mỗi 10-20 dòng | Chấp nhận được |
| 0.10 - 0.15 | 1 em-dash mỗi 7-10 dòng | Cảnh báo, cần audit |
| > 0.15 | > 1 em-dash mỗi 7 dòng | Lạm dụng, phải fix |

Target cho onboard series: **< 0.10 em-dash/dòng**. Mọi file vi phạm ngưỡng 0.10 bắt buộc audit trước commit.

#### 13.4. Checklist Em-dash Audit (BẮT BUỘC trước commit)

```bash
# 1. Đếm mật độ mỗi file modified
for f in $(git diff --name-only --cached | grep .md); do
  count=$(grep -c '—' "$f")
  lines=$(wc -l < "$f")
  ratio=$(python -c "print(f'{$count/$lines:.3f}')")
  echo "$f: $count em-dash / $lines lines ($ratio/line)"
done

# 2. Nếu ratio > 0.10, audit từng hit:
grep -n '—' "<file.md>" | while read line; do
  echo "$line"
  # Phân loại: heading / bold label / attribution / code table / prose
  # Nếu prose → FIX theo §13.2
done

# 3. Fix theo priority:
#    (a) Bullet definition "- X — Y" → "- X: Y"
#    (b) Inline prose "X — Y" (Y lowercase) → "X, Y"
#    (c) Inline prose "X — Y" (Y capital Vietnamese) → "X. Y"
#    (d) Header block metadata "Label: X — Y" → "Label: X, Y"

# 4. Final check: density phải < 0.10 sau fix
```

#### 13.5. Khi viết Part mới — dùng em-dash tối thiểu

Từ session 24 trở đi, viết content mới theo nguyên tắc:
- Đặt em-dash cuối cùng, không phải đầu tiên. Viết câu xong bằng dấu câu thông thường trước, rồi mới chuyển sang em-dash nếu thực sự cần nhấn mạnh ngắt mạnh.
- Nếu không chắc, không dùng em-dash.
- Check density sau khi viết 50-100 dòng. Nếu > 0.15, rewrite.

#### 13.6. Di sản retrofit (session 24)

Part 9.22/9.23/9.24/9.25 giảm em-dash từ 361 → 155 (57% reduction) bằng 3 script pass + manual edits:
- `tmp-emdash-audit.py` — phân loại theo category
- `tmp-emdash-reduce.py` — pattern replacement conservative
- `tmp-emdash-aggressive.py` — bullet definition + Vietnamese sentence split + comma split
- Manual edits cho dangling markup + spacing bugs

Dictionary và Checklist C cập nhật với §13.4 Em-dash scan.

### Rule 14: Source Code Citation Integrity (BẮT BUỘC)

> Nguồn gốc: session 32+33a+33b, 2026-04-22. User flag `MAX_FDB_ENTRIES`
> nằm trong `controller/mac-learn.c` cho OVN v22.03-v24.03 nhưng v24.09+
> đã migrate sang `controller/pinctrl.c`. Audit sweep Phase E Scope D
> phát hiện 32 issue qua 6 category trên 43 file: wrong commit SHA
> (`ee20c48c2f5c` 404 mà Reference 27 cùng file có SHA đúng
> `949b098626b7`), broken cross-ref (`./3.0` → `./19.0`, 4 instances),
> function name fabricated (`reply_icmp_error_if_pkt_too_big` không
> tồn tại — actual upstream có typo `reply_imcp_error_if_pkt_too_big`),
> fabricated OVSDB table (`Chassis_features` — thực tế feature flags
> ở `Chassis.other_config` map), wrong version attribution
> (`MAC_Binding.timestamp` claim v22.03 — actual v22.09 qua commit
> `1a947dd3`), wrong default (`mac_binding_age_threshold=600s` claim
> — actual default 0 disabled), line numbers không annotation version,
> verbatim quote có leak Vietnamese. Nguyên nhân gốc: Rule 1-13 không
> có quy tắc bắt buộc verify source code reference qua upstream trước
> khi cite.

**Quy tắc:**

Mọi reference tới mã nguồn upstream (OVS, OVN, Linux kernel, HAProxy,
Nginx, OpenStack, DPDK, FRR, strongSwan, P4, Cilium, v.v.) PHẢI được
verify qua MCP GitHub (hoặc tương đương) TRƯỚC khi được commit vào
curriculum. Sáu loại reference và cách verify:

**14.1. Commit SHA reference**

- Verify existence: `mcp__github__get_commit(owner, repo, sha)`
- Verify claims match: author + date + message + files changed
- Inline cite dùng 8-12 ký tự (SHA prefix); Reference section dùng
  40-ký tự đầy đủ
- **Inline SHA và Reference section phải match** — grep pre-commit
  để catch mismatch trong cùng file

**14.2. Function name reference**

- Verify existence: `mcp__github__search_code(query="function_name repo:owner/repo")`
- **Lưu ý search_code false negative**: một số function có thật nhưng
  search không index. Fallback mandatory: `mcp__github__get_file_contents`
  đọc thực file rồi grep nội dung.
- **Preserve exact source spelling** kể cả typo (ví dụ OVN source có
  hàm `reply_imcp_error_if_pkt_too_big` với typo `imcp` — không sửa
  thành `icmp` khi cite). Nếu typo gây nhầm, thêm note `(tên gốc
  upstream có typo imcp)`.
- Nếu function đã rename giữa versions, annotate: "(tên cũ `foo_bar`
  trong v22.03, rename thành `bar_foo` từ v24.03 qua commit `abc1234`)"

**14.3. File path reference**

- Verify tồn tại tại version baseline: `mcp__github__get_file_contents(path, ref)`
  với `ref` là tag curriculum baseline (vd `v22.03.8` cho OVN,
  `v2.17.9` cho OVS, `v5.15` cho Linux kernel Ubuntu 22.04)
- Nếu file di trú giữa versions: annotate per Rule 3
  - Ví dụ: "`controller/mac-learn.c` (v22.03 → v24.03) hoặc
    `controller/pinctrl.c` §MAX_FDB_ENTRIES (v24.09+, commit
    `fb96ae3679` merge)"

**14.4. Line number reference**

- Line number LUÔN version-sensitive. Bắt buộc annotate:
  - Option A — branch-specific: "`physical.c` dòng 1939-1968 (OVN
    branch-24.03)"
  - Option B — commit permalink: "`physical.c`
    [link tới GitHub blob tại commit SHA](https://github.com/ovn-org/ovn/blob/SHA/controller/physical.c#L1939-L1968)"
  - Option C — function name anchor: thay vì dòng, dùng function
    name làm anchor stable (ví dụ "Trong function
    `build_lswitch_arp_nd_responder_known_ips` ở `northd/northd.c`,
    tìm `op->lsp_has_port_sec || !op->has_unknown` check")
- **Line number drift phổ biến**: v22.03 → main thường shift 2000+
  dòng. Option C (function name) là recommended best practice.

**14.5. Verbatim quote commit body**

- Copy-paste EXACT từ MCP API response, không dịch, không edit
  spacing, không đổi bullet format
- Block `> "Trích nguyên văn commit body từ GitHub API:"` phải 100%
  English nếu commit body là English
- Chỉ dịch sang Vietnamese nếu chọn format "paraphrase" explicit,
  KHÔNG dùng label "nguyên văn" trên paraphrase
- **Dash bullets (`-`) preserve exact** — không chuyển sang `(a)(b)(c)`

**14.6. Database table + schema claims**

- Verify schema existence via `mcp__github__get_file_contents` cho
  `ovn-sb.ovsschema`, `ovn-nb.ovsschema`, `vswitchd/vswitch.ovsschema`
- Parse JSON để liệt kê tables + columns actual
- **Không fabricate table names** — nếu feature lưu ở `other_config`
  map thay vì dedicated table, nói rõ
- **Internal C struct ≠ database table** — phân biệt rõ (ví dụ
  `struct chassis_features` in-memory khác với giả thiết bảng
  `Chassis_features` trên OVSDB)

**14.7. Audit pass TRƯỚC khi commit**

- Grep mọi claim mới trong section: SHA, function, path, line number,
  table name
- Nếu > 3 references trong section, chạy MCP audit batch (verify
  tất cả)
- Ghi log evidence vào `memory/fact-check-audit-YYYY-MM-DD.md`
- Commit chỉ khi 100% pass; bất kỳ ref nào fail → fix hoặc xóa claim

**Phạm vi áp dụng:** Mọi onboard series (SDN, HAProxy, Linux, Network),
mọi Part mới hoặc audit lại file cũ. Rule 14 áp dụng tiếp nối
(prospectively) + retrofit (cho file đã viết khi phát hiện drift).

**Dấu hiệu vi phạm Rule 14:**

- Inline cite commit SHA nhưng không có matching entry trong References
  section (hoặc SHA khác nhau giữa inline và References)
- Function name không có trong upstream khi search MCP + không có
  trong file khi grep direct
- File path không tồn tại tại version baseline (404)
- Line number không annotate version trong cùng sentence/paragraph
- Block "Trích nguyên văn" có Vietnamese trong English quote
- Database table claim mà không verify schema (vd claim "Chassis_features"
  mà không kiểm ovn-sb.ovsschema)
- Commit Session X chứa source code ref mới mà `memory/fact-check-audit`
  không có entry ngày X

**Quy trình khi viết Part mới (prospective enforcement):**

1. Pre-write phase: research topic trên upstream, note mọi SHA +
   function + file path + line number + table name định cite
2. Batch verify qua MCP trước khi draft content
3. Draft content chỉ dùng ref đã verify
4. Post-write audit: re-grep section, verify lần 2 bằng MCP
5. Commit chỉ khi Step 2 + Step 4 đều pass

**Quy trình khi retrofit file cũ (reactive enforcement):**

1. Grep file cho pattern trong §14.1-§14.6
2. Batch verify MCP
3. Fix từng issue theo category
4. Log findings vào `memory/fact-check-audit-YYYY-MM-DD.md`
5. Re-verify post-fix
6. Commit với message "docs(...): Rule 14 retrofit — N issues fixed"

**Bài học Phase E (session 32-33i):**

- MCP `search_code` có false negative (ví dụ `build_lswitch_learn_fdb_op`
  search return 0 dù function tồn tại ở `northd/northd.c` line 6299
  v22.03.8). Fallback `get_file_contents` bắt buộc.
- Source code có typo intentional (ví dụ `imcp` thay vì `icmp` trong
  OVN `reply_imcp_error_if_pkt_too_big`). Preserve spelling.
- Version attribution phổ biến bị lệch 1 LTS (vd v22.03 vs v22.09).
  Luôn verify commit date + release tag gần nhất.
- Foundation/conceptual blocks (Block I-VIII + X-XII + XIV-XVI + XX)
  density source code ref thấp — ít fact-check risk. Forensic case
  study blocks (XVII-XIX) + internals blocks (XIII OVN + IX OVS) là
  nơi chứa phần lớn risk.

## Current State

| Key | Value |
|-----|-------|
| Active branch | `docs/sdn-foundation-rev2` @ `7e5608b` (session 34 post — Phase E Scope D audit full + Rule 14 codify + Part 9.26 OVS forensic). Release-ready v2.1-preVerified. |
| Phase E status | **🎉 COMPLETE** — Scope A (audit rev2 residual cleanup, 14 fixes), Scope D (fact-check audit 101 file, 32 issues fixed), Scope B (Part 9.26 OVS forensic 464 dòng), Rule 14 codified. Session 32+33a-33i+34+35. |
| Session 32 status | **DONE** Audit rev2 residual (Rule 11 + header backfill) + Phụ lục G + MAX_FDB_ENTRIES version drift fix (`076ef87`+`b243207`). |
| Session 33a status | **DONE** Scope D.1 3 Advanced OVN fact-check (17.0/18.0/19.0, 26 issues 6 category) commit `acc58a2`. |
| Session 33b status | **DONE** Scope D.2 Block XIII OVN foundation (5 issues Chassis_features fabricated + stage count + timestamp version) commit `e06bf63`. |
| Session 33c status | **DONE** Scope D.3 Block IX OVS internals (1 date drift OVS 2.0) commit `93442cc`. |
| Session 33d-h status | **DONE** Block 0-VIII+X-XII+XIV-XVI+XX (0 issues, low density) batch audit. |
| Session 33i status | **DONE** Rule 14 Source Code Citation Integrity codify vào CLAUDE.md (7 subsection 14.1-14.7) commit `7e5608b`. |
| Session 34 status | **DONE** Part 9.26 OVS Revalidator Storm Forensic (464 dòng, 6 điểm cốt lõi, 2 Guided Exercise + 1 Capstone POE) với Rule 14 pre-write verify — commit `180ab2fd635e` + `464bc6f9` + `0d9dc8e9` all verified real. |
| Session 35 status | **DONE** README TOC Block IX 27 file + memory/session-log.md + CLAUDE.md Current State sync. |
| Phase F status | **🔶 PARTIAL COMPLETE (7/9 sessions, 78%) — K8S DEPRIORITIZED** — Block XIV (3/3: 14.0/14.1/14.2) + Block XVI (3/3: 16.0/16.1/16.2) + Block XV 1/3 (15.0 only). **15.1 + 15.2 DEFERRED** theo user directive 2026-04-23 "xếp độ ưu tiên K8S xuống thấp". Plan adjustment: `plans/sdn-foundation-architecture.md` **Phụ lục I** (new). Delta Phase F: +1165 dòng across 7 files. |
| Phase F audit status | **✅ PASSED** — Audit 2026-04-23 across 14 Rules + 6 SKILL. Log: `memory/phase-f-audit-2026-04-23.md`. Rule 9 null bytes 0, Rule 13 em-dash 0.038-0.078/line, Rule 14 MCP verify all repos. |
| Phase F commits | 8 commits pushed: `524773e` (36a 14.0) → `bbc331f` (36b 14.1) → `9a8e2ea` (36c 14.2) → `2fead39` (36d 16.0) → `ef1963d` (36e 16.1) → `1483cfd` (36f 16.2) → `19d8092` (audit) → `c777acf` (36g 15.0). |
| Phase F priority reprioritized | User directive 2026-04-23 post-36g: mission core = **lịch sử + hiểu biết + kiến thức + thao tác công cụ + truy vết + xử lý sự cố + debug với OVS/OpenFlow/OVN**. Block XV Cloud Native (Istio/Linkerd/Cilium/OVN-K8s) thuộc Expert Extension priority thấp. 15.1 deferred (medium priority, OVN lens), 15.2 deferred (low priority, không OVS/OVN). |
| Phase G status | **🟢 IN PROGRESS 5/12 sessions (42%) — G.1 TRUY VẾT COMPLETE + G.3 Debug sâu 2/3** | Plan approved 2026-04-23 (Option C). Scope: OVS/OVN Core Deepening 5 areas (G.1 Truy vết ✅ + G.3 Debug sâu 🟢 2/3 + G.2 Xử lý sự cố ⏳ + G.5 Thao tác công cụ ⏳ + G.4 Lịch sử optional). Plan `plans/sdn-foundation-architecture.md` Phụ lục I §I.4. |
| Session 51 status | **DONE** (2026-04-24) G.3.1 new Part 20.2 OVN troubleshooting deep-dive (1627 dòng). 14 section cover 3-layer debug OVN (NB/SB/OpenFlow), `ovn-trace` 11 option + 4 output mode + 9 subsection deep-dive, `ovn-detrace` chain `ofproto/trace | ovn-detrace` với Anatomy Template A, Port_Binding 8 type forensic × 22 failure mode consolidated, `ovn-appctl -t ovn-controller` 11 command + `ovn-appctl -t ovn-northd` 10 command (7 Anatomy key), MAC_Binding + FDB + Service_Monitor stateful triage, 16-symptom diagnostic matrix, 3 GE + 1 Capstone POE refute "restart cures all". Rule 9 null 0, Rule 11 8 fix (Engineer→Kỹ sư, Verify→Kiểm chứng), Rule 13 em-dash density 0.0535/line, Rule 14 no new SHA claim. Block XX 2→3 file. Curriculum 111→112 file, 44.084→45.711 dòng. Commit `bd2ae48`. |
| Session 52 status | **DONE** (2026-04-24) G.3.2 expand Part 9.26 OVS Revalidator Storm Forensic từ 464 → 1185 dòng (+721). Append 2 case study mới + 2 Guided Exercise + 1 cross-case takeaway: **Case 2** §9.26.11 LACP bond flap cascade (ToR firmware trigger LACPDU timeout → 200 chassis đồng loạt mark slave DOWN → megaflow mask invalidation storm → upcall rate 50 pps → 250K pps → VM latency cascade) với Anatomy Template A cho `bond/show` 10 field + `lacp/show` state bits + `dump-ports drop counter` + 4 coverage counter bond-specific, mechanism deep-dive `bond_update_post_recirc_rules()` + remediation 4 tầng (lacp-time slow maintenance window / upgrade 3.1+ single-slave optimization). **Case 3** §9.26.12 Conntrack zone collision cross-chassis migration (tenant T2 migrate chassis-A→B race với T1 zone 1012 → state cross-talk → "random connection reset" dual-tenant) với Anatomy `ct-zone-list` + `dpctl/dump-conntrack zone=N` detect duplicate, mechanism `alloc_ct_zone()` bitmap refresh race + remediation (restart ovn-controller + sequential migration + upgrade 24.03+ transactional alloc + daily audit cron). **§9.26.13** cross-case takeaway: 3 incident class "eventually consistent distributed cache" + 4 design lesson (convergence test adversarial / observability per-cycle metric / symptom cascading / latency phân tách). **GE3** reproduce bond_reconfigure spike với veth slave flap (balance-slb sandbox). **GE4** zone audit script `sort | uniq -d` O(n log n) verify 10K LSP < 0.1s. Rule 9 null 0, Rule 11 1 fix (Verify→Kiểm chứng), Rule 13 em-dash density 0.0802/line (< 0.10). Curriculum 112 file, 45.711 → 46.432 dòng. Phase G 4/12 → 5/12 (42%), G.3 Debug sâu 1/3 → 2/3. Commit `262f768`. |
| Session 53 status | **DONE** (2026-04-24) G.5.1 new Part 20.3 OVN daily operator playbook (1554 dòng). 18 section cover 10 task category scenario-driven cho operator daily workflow: (1) health check morning routine 5 lệnh < 10 giây với Anatomy Template A `ovn-nbctl show` + chassis liveness + northd/ovn-controller status + nb_cfg sync + lflow count; (2) inventory listing 5 cách đếm LS/LSP/LR/ACL/LB/NAT/DHCP/Chassis; (3) port lifecycle 6 scenario (add/bind/remove/rename/migrate/disable); (4) ACL management 6 scenario với Port_Group consolidation 5-10x; (5) Load_Balancer + NAT 6 scenario (create/modify/health-check/SNAT/DNAT/remove); (6) DHCP + DNS native 5 scenario; (7) Gateway + HA_Chassis 5 scenario (LRP external/HA group/active check/failover/BFD); (8) Conntrack 5 scenario (dump/count/flush/zone check/timeout); (9) Performance 5 metric (stopwatch/inc-engine/lflow-cache/datapath/Prometheus export); (10) Backup + maintenance 5 scenario (NBDB+SBDB backup/restore/chassis cordon 7-step/rolling upgrade/audit). **2 workflow end-to-end**: §20.3.11 new-tenant.sh + §20.3.12 tenant-teardown.sh script complete bash. **3 Guided Exercise**: health check walkthrough + new tenant provisioning + chassis maintenance procedure. **Capstone POE** "Add 500 ACL safe for prod?" refute với Port_Group consolidation + priority block recommendation. 8 hiểu sai phổ biến + 8 điểm cốt lõi. Rule 9 null 0, Rule 11 0 prose leak (đã apply Kiểm chứng từ đầu), Rule 13 em-dash density 0.0257/line (rất thấp), Rule 14 no new SHA. Block XX 3→4 file. Curriculum 112→113 file, 46.432 → 47.986 dòng. Phase G 5/12 → 6/12 (50%), G.5 Thao tác công cụ 0/2 → 1/2. |
| Session 37a status | **DONE** (2026-04-23) G.1.1 expand Part 9.25 — +3 Guided Exercise (multi-bridge patch port / reg-metadata state / ct+tunnel recirculation) +3 objective +3 key point. 636 → 1046 dòng (+410). Commit `fad6631` pushed. |
| Session 37b status | **DONE** (2026-04-23) G.1.2 new Part 9.27 OVS+OVN Debug playbook end-to-end (659 dòng). Complement Part 0.2 tour với focus: 3-tier parallel diagnostic framework (`ovn-trace` + `ofproto/trace` + `dpif/dump-flows`), Geneve TLV deep-dive (class 0x0102), MTU forensic (overhead 66 byte), fault catalog 10 pattern, 2 GE + 1 Capstone POE. Rule 13 density 0.074/line. Block IX 26 → 27 file. Commit `2e139c8` pushed. |
| Session 37c status | **DONE** (2026-04-23) G.1.3+G.1.4: expand Part 13.7 +§13.7.7 ovn-controller run loop deep-dive (main_loop anatomy + I-P engine graph + recompute events + diagnostic recipes sync lag), 334 → 491 dòng (+157). Expand Part 20.0 +§20.7 case study playback 3 production scenario (VM no network race, upgrade schema drift, partition thundering herd), 582 → 788 dòng (+206). Rule 13 density 0.039/0.070 per file. G.1 TRUY VẾT area COMPLETE. Commit `3793139` pushed. |
| Phase H status | **🎉 COMPLETE 13/13 session (100%) — v3.0-FoundationDepth** — S38-S50 DONE 2026-04-24. Curriculum 111 file, 44.084 dòng (+6.562 từ baseline 37.522). Template library (A/B/C/D). Full match field + action catalog. Full OVN LS+LR pipeline exhaustive. Full NBDB+SBDB schema. Gaps closed: ls_out_*/lr_in_*/lr_out_*/ovs-bugtool. Rule 9+13 PASS trên 111 file. Plan `plans/phase-h-foundation-depth.md`. Tracker `memory/phase-h-progress.md`. |
| Audit 2026-04-24 status | **DONE refreshed+severity-upgraded** — `memory/sdn-onboard-audit-2026-04-24.md`. 110 concept audit: 22 rich / 24 medium / 65 shallow / 18 zero-mention. Code block stats: median 3 dòng, 71% ≤5 dòng (CRITICAL gap xác nhận user feedback). Upstream baseline research via Agent Explore: OVS Advanced Tutorial 1.250 dòng, OVN Tutorial 3.500-4.000 dòng, ovs-fields(7) 100+ field 9-attribute anatomy. |
| Session 38 status | **DONE** (2026-04-24) H.0 + H.2.1 pilot: (a) Template library `sdn-onboard/_templates/` với 4 template A/B/C/D + README (500 dòng); (b) Pilot Part 9.4 OVS CLI tools playbook expansion 267→1406 dòng (+1139). Rule 9 null byte 0; Rule 13 em-dash 0.041/line; Rule 11 12 prose fix. 38 code block median 12 mean 15.4 ≤5 blocks 13.2%. Upstream lift từ man ovs-vsctl/ovs-ofctl/ovs-dpctl + openvswitch.org/support/dist-docs. |
| Session 39 status | **DONE** (2026-04-24) H.2.2: Part 9.11 ovs-appctl reference playbook expansion 215→1170 dòng (+955, vượt target 46%). 18 nhóm target × Anatomy block: introspection (vlog/memory/coverage) + bridge+FDB+mdb + bond+LACP + STP+RSTP + BFD+CFM + ofproto + dpctl/dpif + dpif-netdev + tunnel + upcall/revalidator + OVSDB cluster. Decision matrix 10-symptom + Guided Exercise coverage delta. Rule 9 null byte 0; Rule 13 em-dash 0.044/line; Rule 11 4 prose fix. 50 code block median 5 (reference doc pattern), key Anatomy ≥15 dòng. Upstream ovs-appctl(8)+ovs-vswitchd(8)+ovsdb-server(1)+RFC 5880. |
| Session 40 status | **DONE** (2026-04-24) H.2.3: Part 9.2 kernel datapath deep-dive expansion 529→878 dòng (+349, vượt target 75%). 5 section mới: §9.2.8 EMC (8K entry/PMD hash exact-match) + §9.2.9 SMC (OVS 2.15+ 16K entry signature tier) + §9.2.10 Upcall Netlink genl wire format (nlmsghdr+genlmsghdr+OVS_PACKET_ATTR TLV) + §9.2.11 Ukey 6-state lifecycle + revalidator RCU read-side + §9.2.12 3-tier cache summary table + 10-item production health checklist. Legacy cleanup: rename §9.2.6 dup → §9.2.13. Rule 9 null byte 0; Rule 13 em-dash 0.058/line; Rule 11 4 prose fix (overhead→chi phí phụ, pattern→mẫu). Upstream NSDI 2015+2020+OVS source ofproto-dpif-upcall.c+Linux genl man+USC Lab 9. |
| Session 41 status | **DONE** (2026-04-24) H.3 Match Fields: tạo mới Part 4.8 `openflow-match-field-catalog.md` (926 dòng). 12 nhóm × Template B 9-attribute anatomy: Metadata (6 field) + Register (16+8+4) + L2 (9) + ARP (5) + IPv4 (6) + IPv6 (7) + L4 TCP/UDP/SCTP (8) + ICMP (4) + Tunnel (6) + Conntrack (9) + MPLS (4) + ip_frag + packet_type. Prerequisite chain table 12 rows + lazy wildcarding thực nghiệm nối Part 9.2. Curriculum 109→110 file (Block IV 8→9). Rule 9 null byte 0; Rule 13 em-dash 0.045/line; Rule 11 5 prose fix. Upstream ovs-fields(7)+OpenFlow 1.3/1.5 spec+RFC 4861/6437/7348/8926+OVS meta-flow.h. |
| Session 42 status | **DONE** (2026-04-24) H.4.1 Actions tier 1: tạo mới Part 4.9 `openflow-action-catalog.md` (762 dòng tier 1). Template C 8-attribute anatomy applied first time. 14 section: §4.9.1 action vs instruction (6 instruction OF 1.1+) + §4.9.2-10 Category 1 Output (output, drop, normal, flood, all, controller, local, in_port, table, group với 4 types all/select/indirect/fast_failover) + §4.9.11-13 control actions (resubmit, clone, note) + §4.9.14 Action Set 12-priority execution order vs Apply-Actions sequential. Tier 2+3 sẽ expand S43+S44. Curriculum 110→111 file (Block IV 9→10). Rule 9 null byte 0; Rule 13 em-dash 0.051/line; Rule 11 4 prose fix. Upstream ovs-actions(7)+OpenFlow 1.3/1.5 spec §5.10-5.11+OVS ofp-actions.h+ofproto-dpif-xlate.c. |
| Session 43 status | **DONE** (2026-04-24) H.4.2 Actions tier 2: append Part 4.9 tier 2 (762→1124 dòng, +362). 8 section mới: §4.9.15 VLAN encap (push/pop 0x8100+0x88a8 Q-in-Q) + §4.9.16 MPLS + PBB + encap/decap generic OF 1.5 + §4.9.17 set_field generic với mask + §4.9.18 legacy mod_* family (11 action) + dec_ttl router function + copy_ttl MPLS stacking + §4.9.19 move/load register bit-range + ARP responder 7-action pattern + §4.9.20 write_metadata + set_tunnel + §4.9.21 QoS (set_queue + enqueue + meter OF 1.3+ với band type drop/dscp_remark) + §4.9.22 bảng tổng hợp tier 1+2. Coverage ~35/40 action. Rule 9 null byte 0; Rule 13 em-dash 0.046/line; Rule 11 2 prose fix. Upstream ovs-actions(7) Category 2-4+7 + OpenFlow 1.3 §5.10 + OVS ofp-actions.h. |
| Session 44 status | **DONE** (2026-04-24) H.4.3 Actions tier 3 advanced — Part 4.9 FINAL: append tier 3 (1124→1544 dòng, +420). 8 section: §4.9.23 ct() full (commit/zone/nat/force/alg/exec/table + ct_clear + typical stateful firewall pattern) + §4.9.24 learn() MAC learning self-programming + fin_idle_timeout + §4.9.25 conjunction() cross-product ACL compression (OVN Port_Group context) + §4.9.26 multipath() ECMP với 4 hash algorithm + §4.9.27 bundle/bundle_load + §4.9.28 check_pkt_larger() PMTUD (OVN lr_in_chk_pkt_len) + §4.9.29 full catalog summary 40+ action + §4.9.30 Guided Exercise full-pipeline (rate limit → stateful CT → SNAT → output 4-table chain). Part 4.9 TOTAL 1544 dòng 30 section 40+ action 100% foundation coverage. Rule 9 null byte 0; Rule 13 em-dash 0.050/line; 50 code blocks median 5 mean 7.6. Upstream ovs-actions(7) Cat 5+6+OVS ofproto-dpif-xlate.c+cross-ref Part 9.24+13.3+13.11. |
| Session 45 status | **DONE** (2026-04-24) H.5 OVS internals expand 3 file: 9.1 (341→430 +89) + 9.15 (254→407 +153) + 9.16 (240→433 +193) = +435 dòng (vượt target +350 là 24%). 9.1 §9.1.X: ofproto-dpif 5-layer architecture + dpif/show anatomy + thread model (main/handler/revalidator/PMD/URCU). 9.15 §9.15.7: subtable internals (struct cls_subtable cmap + minimask) + `dpctl/dump-flows` masked output anatomy; §9.15.8: Patricia trie prefix optimization; §9.15.9: performance pathology (subtable explosion + priority sort churn). 9.16 §9.16.7: multi-controller 3-node setup + ofproto/show-connection anatomy + role election timeline; §9.16.8: OFPT_ROLE_REQUEST wire format + OFPT_SET_ASYNC; §9.16.9: connmgr coverage counter; §9.16.10: troubleshooting matrix 6-symptom. Rule 9 0, Rule 13 0.023-0.047/line, Rule 11 0 new leak. Upstream OVS `lib/classifier.c`+`ofproto/connmgr.c`+OpenFlow 1.3 §7.3.9+§7.5.4+SIGCOMM 1999 TSS. |
| Session 46-50 batch status | **DONE** (2026-04-24) Phase H COMPLETE — 5 session batch cover OVN foundation + tools + final QG. S46 H.6.1 LS pipeline (13.2 201→399 +198): ingress 27 stage + egress 10 stage Template D. S47 H.6.2 LR pipeline (13.11 268→516 +248): ingress 19-23 stage + egress 7 stage Template D. S48 H.6.3 schema (13.1 191→446 +255 + 13.10 272→319 +47): NBDB 17 table + SBDB 15 table deep + DHCP options catalog. S49 H.7 conntrack (13.3 189→454 +265): OVN ACL expression syntax + allow-related + conjunction + LB deep + Service_Monitor + NAT patterns. S50 H.8 tools+QG (9.14 218→370 +152): ovs-bugtool + ovs-pcap + ovs-testcontroller + final QG v3.0-FoundationDepth checklist. Gap foundation fix: ls_out_*/lr_in_*/lr_out_*/ovs-bugtool/ovs-pcap (từ 0-mention → full coverage). Curriculum 111 file, 44.084 dòng, 1572 code block median 3 mean 6.2 ≤5 blocks 66.3% (từ baseline 71%). Rule 9 null 0, Rule 13 em-dash 0 dense, Rule 11+14 pass. Upstream ovn-architecture(7)+ovn-nb(5)+ovn-sb(5)+northd source+ovs-bugtool(8). |
| Lab host status | **⏳ PENDING — chờ user** — 2026-04-23 user confirm "chưa có môi trường để thực hành, khi nào có sẽ thông báo". 63 exercise pending C1b. |
| Tools state | Node v24.15.0 LTS installed (winget, 2026-04-23). MCP GitHub full access confirmed working. Restart Claude Code to activate node for hooks. |
| Session 22+23 status | **🎉 Phase D firewall foundation COMPLETE** (2026-04-22). Part 9.22 multi-table + 9.23 stateless ACL + 9.24 conntrack stateful. |
| Session 24 status | **🎉 Phase D new-Part phase COMPLETE** (2026-04-23). Part 9.25 + Part 9.21 + Rule 13 ra đời + Rule 11 retrofit session 22+23. |
| Session 25 status | **DONE** Audit P0.1 (README TOC 14 orphans) + P0.2 (2 dead URL) + P1.4 (Rule 13 top 10, 508→156) + P3.8 (CLAUDE.md state) + Part 9.9 QoS expansion (+458 dòng). |
| Session 26 status | **DONE** Part 11.3 GRE expansion (+547 dòng, Lab 14 full). |
| Session 27 status | **DONE** Part 11.4 IPsec expansion (+662 dòng, Lab 15 full) + Part 9.2 kernel datapath lab steps (+251 dòng, Lab 11). **🎉 Phase D expansion COMPLETE 4/4.** |
| Session 28 status | **DONE** Audit P2.6 (Rule 13 remaining 20 files, 689→196) + P2.7 (Dictionary expansion 12 entries) + P2.5-safe (5 Critical files, 36 replacements). |
| Session 29 status | **DONE** Audit P2.5 context-review 3 pre-existing Critical (19.0 + 17.0 + 18.0 = 123 replacements + 10 URL restorations). |
| Session 30 status | **DONE** Audit P2.5 context-review 2 Phase B Critical (3.2 + 4.6 = 132 changes). URL protection improved. Manual syntax cleanup 6 lines. |
| Session 31 status | **🎉 COMPLETE** Audit P2.5 context-review 6 residual Critical (3.1 + 3.0 + 2.1 + 2.4 + 5.0 + 6.0 = 171 replacements). **P2.5 TOTAL 11/11 Critical DONE**, 426 replacements. |
| Phase D final status | **9/9 deliverable DONE**: 5 Part mới (9.21/9.22/9.23/9.24/9.25) + 4 expansion (9.9/11.3/11.4/9.2). Còn C1b Lab Verification + C6b Final Publish chờ lab host. |
| Audit 2026-04-23 state | **🎉 FULL COMPLETE** — tất cả P0/P1/P2/P3 items. Only C1b Lab Verification + C6b Final Publish v2.0 deferred (bên ngoài audit scope). |
| Audit 2026-04-23 P2.5 summary | 11 Critical files cleaned, 426 prose replacements total. Patterns: operator/engineer/version/deployment/verify/incident/fail/support/performance/approach/pattern/expose/scalability/dynamics/adoption/shepherd/consumer/workaround/trade-off/worry/bent/favor/significant/unusual/overlap/troubleshoot/subtle/pedagogical/motivation/criteria/flexibility/bidirectional/symmetric/asymmetric/experiment/tolerate/undefined (~37 patterns). 0 URL corruption, 0 null bytes. |
| Commits session 24-31 pushed | **15 commits**: `ce2c13b` → `41f6533` → `24bb66b` → `edbba24` → `cab7ea5` → `b225c1d` → `b1200c9` → `497d9e7` → `434890f` → `2a11a53` → `2f152f6` → `d883751` → `02edad8` → `22a8616` → `f868d8e`. |
| Session 17 status | **🎉 COMPLETE — C5.4 + C5.5 + C7 + C8 + C9 + C10 all DONE + pushed** (2026-04-22). Core OVS/OpenFlow/OVN đạt bề rộng + bề sâu + cross-cutting view. |
| Session 17 deliverables | 17 file mới (9 core blocks + 3 cross-cutting + 5 Rule 11 retrofit) + expand 14 file Block XIV/XV/XVI cũ. Tổng +8315 dòng content. README TOC updated 3 lần (Block X + XIII + Block 0). |
| Curriculum state (end session 31) | **93 file, ~40.5K dòng** content OVS/OpenFlow/OVN. Block IX 26 file (cao nhất curriculum), Block XI 5 file (GRE + IPsec full expansion). Rule 9 null bytes 0 trên 93 file. Rule 11 prose 100% safe + 11/11 Critical context-cleaned. Rule 12 offline source 100%. Rule 13 em-dash 100% compliance (< 0.10/line). |
| Curriculum state (end session 23) | **91 file, ~34.8K dòng** content OVS/OpenFlow/OVN. Block IX (24 file — cao nhất curriculum, 4 tier + Firewall foundation 9.22-9.24), các block khác unchanged vs session 17. |
| Curriculum state (end session 17) | **85+ file, ~32K+ dòng** content OVS/OpenFlow/OVN. Block IX (18 file), Block X (7 file), Block XIII (14 file), Block XVII-XIX (3 file), Expert Extension (9 file), Block 0 intro (3 file), các block khác unchanged. |
| Next session deferred | C1b Lab Verification (chờ lab host) → C6b Final Publish v2.0 (chờ C1b) |
| Session 17 deltas (final) | **C5.4** (pushed): 9 file Block XIV/XV/XVI section body expanded 2523→2917 (+394). **C5.5** (pushed): 5 file Exercise Rule 11 retrofit. **C7** (committed 3 batches, ready push): 6 file mới 13.7-13.12 OVN ovn-controller/northd/LB/DHCP-DNS/GR/IPAM (+1606 dòng). |
| Block XIII final state | 7 core (13.0-13.6) + 6 extended (13.7-13.12) = 13 file 2847 dòng. Scope OVS/OpenFlow/OVN core per user directive. README TOC updated. |
| C2 audit result | 70/70 file audited. 4 fixes applied: HIGH (Part 1.2 Capstone Predict step), MEDIUM (5 heading type cleanups), LOW (Part 1.1 numbering). Cross-ref integrity validated. Commit `d821e65` + `10fe2e5`. |
| C3 prose passes (3 rounds + 2 reverts) | **R1** `3a92e27`: paradigm/rebrand/troubleshoot (45). **R2** `c78cb39`: scalability/bottleneck/real-time/backward-compat (32). **R3** `739db7f`: adoption/deprecation (53). **Reverts**: `63a0506` (3.2 English quote + URL), `7b22823` (1.1 RFC 7348 quote). **Net 127 replacements** across 50+ files. Remaining (approach/deployment/trade-off/announce) deferred. |
| C4 URL audit | 384 unique URLs, 98.7% OK. 3 dead URLs fixed (Netflix + YouTube press moved, archive.openflow.org timeout → ONF spec archive). 2 placeholder URLs kept as-is (10.0.0.3, odl-controller:8181). Commit `e6d7a8b`. |
| C1a lab inventory | 54 Exercise/Lab/Capstone headings inventoried in `memory/lab-verification-pending.md`. Priority matrix: HIGH (8 Capstones với numeric output), MEDIUM (14 Block IX OVS exercises), LOW (historical Block II-III). Ready for C1b when lab host available. |
| C5 expert extension | **Arch + Exercise content COMPLETE** — 9 files Block XIV/XV/XVI với 18 exercises fully specified (Mục đích/Chuẩn bị/Mô hình/Bước/Output/Bài học/Cleanup). Section X.Y.Z skeleton giữ nguyên cho future content phase. 2523 lines total. Lab outputs doc-plausible pending C1b. Commits `2c6d052` + `dc8634e` + `562bee9`. |
| C6a publish pipeline | `scripts/build-sdn-pdf.sh` + `scripts/README.md` — Pandoc XeLaTeX Vietnamese PDF + EPUB3 builder. Targets v1.0-preVerified (current state) → v2.0-Verified (post C1b) → v2.1+ (future content expansion). Commit `ce13e49`. |
| Lab verification tracker | `memory/lab-verification-pending.md` — fully populated C1a pass. Resume point for C1b (chờ user notify lab host available). |
| Push state (session 16 final) | **10 commits pushed** (→ `73856a4`). **12 commits pending push**: `562bee9` C5.3 exercises (+2006 lines) → `8a0b8fb` handoff-2 → `03e6c0b/b452388/1fe4ac5` README updates → `c78cb39` C3 R2 → `a0bf84c` root README → `76a4418` CLAUDE.md sync → `c0fbccc` foundation forward-refs → `739db7f` C3 R3 → `63a0506/7b22823` sed reverts. |
| README updates (session 16 ext-2) | `sdn-onboard/README.md`: TOC Block XIV/XV/XVI entries, mermaid graph với dashed Expert track arrows, 6th reading path (Expert Extension sub-tracks). Root `README.md`: SDN structure overview note (rev 4). |
| Last 8 commits trên branch | `6ad6b8f` em-dash scripts archive → `6009320` Block VI content → `ced93e0` Block V content → `4da6a98` Part 4.7 content → `2eef2e6` Block IV 4.2-4.6 content → `b3de38c` Part 4.1 content → `6aef52b` IPv6 scope cut → `6bae8f4` Block III content |
| Master HEAD | `e7864d3` chore(plans) — local master ahead origin/master by 1 commit (chưa push, ngoài scope SDN rev 2) |
| HAProxy baseline | HAProxy 2.0 on Ubuntu 20.04 (Canonical repo) |
| HAProxy Parts | 1/29 completed (Part 1 only, fact-checked, Quiz added) |
| Linux FD doc | `linux-onboard/file-descriptor-deep-dive.md` — **1265 lines, 14 SVG figures** |
| FD exercises | 7/9 verified. Exercise 7 (strace) + Exercise 8 (FD limit) cần lab |
| SDN 17.0 doc | `sdn-onboard/17.0 - ovn-l2-forwarding-and-fdb-poisoning.md` — **1178 lines** (renamed từ `1.0 - ovn-l2-...` ở S3; renumbered Phần 1 → Phần 17, mục 1.X → 17.X; forward refs tới Part 19 §19.2/§19.4/§19.5-19.6) |
| SDN 18.0 doc | `sdn-onboard/18.0 - ovn-arp-responder-and-bum-suppression.md` — **496 lines** (renamed từ `2.0 - ovn-arp-...` ở S3; renumbered Phần 2 → Phần 18, mục 2.X → 18.X; cross-refs sang Part 17 mục 17.4/17.6 đã cập nhật) |
| SDN 19.0 doc | `sdn-onboard/19.0 - ovn-multichassis-binding-and-pmtud.md` — **1379 lines, 127,903 bytes** (renamed từ `3.0 - ovn-multichassis-...` ở S3; renumbered Phần 3 → Phần 19, §3.X → §19.X; RFC refs RFC 791 §3.1 / RFC 8926 §3.4/§3.5 preserved intact) |
| SDN Block 0 | `sdn-onboard/0.0 - how-to-read-this-series.md` (148 lines) + `0.1 - lab-environment-setup.md` (426 lines) = 574 dòng content. S4 DONE. |
| S3 status | S3.1-S3.6 completed 2026-04-20. User đã push commit remote ở session 6. Legacy artifacts đã cleanup. |
| S4 status | **DONE** (2026-04-21). S4.1-S4.3 content Block 0, S4.4 quality gate (null byte 0, URL 6/7 → 7/7 sau fix Vanderbilt, cross-file sync, version annotation). Commit `c38c3c9` + handoff `76173cd` đã push lên remote. Index stale do plumbing path đã được refresh ở session 7. |
| Current phase | **Content Phase (Phase B) — in progress**. Block I (1.0/1.1/1.2), Block II (2.0-2.4), Block III (3.0-3.2), Block IV (4.0-4.7), Block V (5.0-5.2), Block VI (6.0-6.1) DONE = 20/~66 foundation file content-expanded. Remaining skeleton: Block VII-XIII + 4.x leftovers. |
| S5 status | Block I content + skeleton DONE. Part 1.0 = 198 dòng content (over-scope, commit `9cd8041`). Part 1.1 + Part 1.2 skeleton refined Rule 10 (~70 dòng/file) ở S5a, commit `10ab5cb`. |
| S6a status | **DONE** (session 8, 2026-04-21). Block II skeleton refined Rule 10: Part 2.0 (DCAN/Open Signaling/GSMP RFC 3292), 2.1 (Ipsilon RFC 1953/Active Networking DARPA), 2.2 (NAC/orchestration/virtualization), 2.3 (ForCES RFC 3654/3746 + 4D Project Princeton/CMU 2005), 2.4 (Ethane SIGCOMM 2007 — direct OpenFlow predecessor). Tầng 2g thêm vào dependency map. Commit `dc1b0b9`. |
| S7a status | **DONE** (session 8b, 2026-04-21). Block III skeleton refined Rule 10: Part 3.0 (Stanford Clean Slate 2006-2012 + Nicira founding 08/2007 + VMware $1.26B 07/2012), 3.1 (OpenFlow 1.0 spec 31/12/2009 + 12-tuple match + 8 actions), 3.2 (ONF formation 21/03/2011 + 6 founding operators + 2018 ON.Lab merger). Tầng 2h thêm vào dependency map với non-repetition rules + Phase B fact-check list. Commit `ff0dd14`. |
| S8a status | **DONE** (session 8c, 2026-04-21). Block IV skeleton refined Rule 10: Part 4.0 (OF 1.1 multi-table + 4 group types FAST_FAILOVER), 4.1 (OF 1.2 OXM TLV + controller roles MASTER/SLAVE), 4.2 (OF 1.3 LTS — meter table + PBB + IPv6 ext headers), 4.3 (OF 1.4 bundles + eviction + optical), 4.4 (OF 1.5 egress + TCP flags + packet type), 4.5 (TTP ONF TS-017 + Flow Objectives ONOS), 4.6 (5 limitations + Google B4 SIGCOMM 2013 + lessons → P4). Tầng 2i thêm vào dependency map. Commit `908279d`. |
| Architecture backlog (rev 3) | P0-P5 COMPLETE 2026-04-21. Total 70 markdown files. |
| Phase B content progress (session 15 end) | **🎉 COMPLETE — 61/~61 file foundation content-expanded + 3 advanced production = 64 file toàn curriculum**. Sessions 12-13: Block 0-VI 20 file. Session 14: Block VII 4 + Block IX 15 + Block VIII 1 = 20 file. Session 15: Block VIII 3 + Block X 3 + Block XI 5 + Block XII 3 + Block XIII 7 = 21 file. Tổng ~20.000 dòng content Phase B. |
| Phase B status | **DONE end-to-end**. Toàn bộ Block 0-XIII content-expanded với Rule 11 (Vietnamese Prose Discipline) + Rule 12 (Exhaustive Offline Source Exploration) compliance. Advanced XVII-XIX đã production trước đó (sessions 1-9). |
| Offline sources inventory (session 14) | `sdn-onboard/doc/compass_artifact_wf-*.md` (Anthropic OVS curriculum, 682 dòng) + `sdn-onboard/doc/ovs/` (USC/Crichigno NSF 1829698: OVS.pdf, OpenVSwitch.pdf, 7 lab PDF+TXT). Rule 12 codified exhaustive exploration. |
| Experiment plan | `memory/experiment-plan.md` — Phases A-E, priority-ordered |
| Push state on next machine | Branch `docs/sdn-foundation-rev2` ahead origin bởi ~30+ commit (session 12+13+14). Khi resume trên máy mới: `git fetch origin && git checkout docs/sdn-foundation-rev2 && git pull --ff-only origin docs/sdn-foundation-rev2` + `git push origin docs/sdn-foundation-rev2` nếu chưa push. |

## Skill Quick Reference

**Skill đã cài đặt tại `~/.claude/skills/` (6 skill — tất cả phải được dùng):**

| Nhóm | Skill | Khi nào dùng |
|------|-------|-------------|
| Core A | professor-style | MỌI nội dung giảng dạy, viết .md, giải thích kỹ thuật |
| Core A | document-design | MỌI file .md trong onboard series |
| Core A | fact-checker | MỌI technical claim, CLI command, config directive |
| Core A | web-fetcher | MỌI URL cần fetch hoặc verify |
| Extra B | search-first | Trước khi viết code/script/utility mới — tìm tool/library/MCP/skill đã tồn tại |
| Extra B | deep-research | Research multi-source có citation (firecrawl + exa MCP) khi offline doc/* không đủ |

**Skill tham chiếu nội bộ (ngoài registry global, trigger qua CLAUDE.md):**

| Skill | Khi nào dùng |
|-------|-------------|
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
