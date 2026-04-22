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

> Nguồn gốc: session 13, 2026-04-21. User chỉ ra 9 ví dụ điển hình về English abuse
> trong Phase B content Block I-VI (~890 English hit trên 24 file, mật độ 5-26%).
> Ví dụ: "hypervisor overlay paradigm" thay vì "mô hình hypervisor overlay",
> "VMware announce acquisition Nicira" thay vì "VMware thông báo mua lại Nicira",
> "troubleshoot tunnel issue cần inspect 2 layer" thay vì "khắc phục sự cố tunnel
> cần kiểm tra 2 lớp". Root cause: mental model khái niệm trừu tượng hình thành
> trong tiếng Anh, không translate khi viết Việt → câu lai bad.

**Khi viết content tiếng Việt cho onboard series, tuân thủ:**

1. **Giữ tiếng Anh chỉ cho**:
   - Tên sản phẩm/dự án (OpenFlow, NETCONF, OVS, OVN, NSX, Nicira, VMware, Linux, Kubernetes, Docker).
   - Protocol/acronym (TCP, UDP, VLAN, VXLAN, Geneve, BGP, OSPF, MPLS, TLS).
   - CLI verbatim (`ovs-ofctl`, `ovs-vsctl`, `ovn-nbctl`).
   - Spec field name (match fields, flow entry, OXM, NXM).
   - Acronym ngành (SDN, DC, WAN, LAN, DPU, ASIC, NOS, VM, RFC).

2. **Dịch sang tiếng Việt cho vocabulary tư duy**:
   - paradigm → mô hình
   - architecture → kiến trúc
   - approach → cách tiếp cận
   - deployment → triển khai
   - support → hỗ trợ
   - adoption → sự chấp nhận / việc áp dụng
   - trade-off → sự đánh đổi
   - backward compat → tương thích ngược
   - lock-in → bị phụ thuộc vào
   - production (IT context) → **môi trường production** (GIỮ "production", KHÔNG dịch "sản xuất")
   - production (manufacturing) → sản xuất (ODM sản xuất hardware)
   - rebrand → đổi tên thương hiệu
   - announce → thông báo / công bố
   - troubleshoot → khắc phục sự cố
   - inspect → kiểm tra
   - integration → tích hợp
   - exclusive → độc quyền
   - steep learning curve → quá trình học hỏi rất khó khăn

3. **Test đọc đơn lập**: sau khi viết xong một câu, đọc tách biệt khỏi context.
   Nếu câu có > 3 từ tiếng Anh không phải technical term chuẩn → rewrite bằng
   từ nối tiếng Việt.

4. **Hybrid acceptable**: "tích hợp với vSphere" (không phải "integrate với
   vSphere"). Technical term tiếng Anh + từ nối thuần Việt.

5. **Misconception callout**: câu quote trong "Hiểu sai:" phải đầy đủ tiếng
   Việt, không phải shortform tiếng Anh.

Từ điển dịch đầy đủ tham khảo: `.claude/plans/tender-scribbling-comet.md`
Phần 1 (plan session 13).

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

## Current State

| Key | Value |
|-----|-------|
| Active branch | `docs/sdn-foundation-rev2` @ `7b22823` (session 16 final — **22 commits total**; 10 pushed up to `73856a4`, 12 pending push, về ready push khi user confirm) |
| Current phase (session 16 end) | **🎉 Phase C Master Quality Plan — active phases COMPLETE** (2026-04-22). C1/C2/C3/C4/C1a/C5/C6a all committed. Deferred: C1b (chờ lab host — user notify) → C6b (sau C1b). |
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
