# Rule 11 Historical Vietnamese Prose Dictionary (frozen reference)

> **Status: PARTIALLY CONSUMED by plan v3.12 (sdn-onboard slice closed 2026-04-29); awaiting cross-block follow-on for full retirement.** This file is no longer authoritative for new writing. It was consumed by plan v3.12 sdn-onboard scope; it is preserved for the cross-block follow-on plan (5 `sdn-onboard/_templates/*.md` files plus 2 `haproxy-onboard/*.md` files), where translators will still need to recognize the original Vietnamese phrasing in legacy template and HAProxy curriculum files and produce the canonical English rendering.
>
> **Why partially consumed.** CLAUDE.md Rule 17 (added by plan v3.9.1 Phase Q-1.C, 2026-04-28) makes English the mandatory explanation language across the SDN training program (`sdn-onboard/*.md` and `haproxy-onboard/*.md`), CLAUDE.md, all `memory/*` files, and all `plans/*` files. The Vietnamese prose policy that this dictionary supported (retired Rule 11) is no longer in force. Plan v3.12 (closed 2026-04-29) translated all 136 sdn-onboard curriculum files; the cross-block surface (`_templates/`, `haproxy-onboard/`) remains pending. New writing follows the English style guide at `memory/shared/english-style-guide.md` instead.
>
> **Scope of this file.** The body table below is preserved verbatim, in its original bilingual form, because the cross-block follow-on plan will need it. CLAUDE.md Rule 17 grants this file a narrow allowance to keep its Vietnamese content (the file lives in `memory/`, which is named in the allowance). The pre-commit `lang_check.py` allowlist exempts this exact path. Do not add new entries; do not rewrite existing entries. After the cross-block follow-on plan closes, this dictionary may be fully retired and either archived to a historical-record subdirectory or deleted.
>
> **For new writing, see:** `memory/shared/english-style-guide.md` rule 3.3 for the keep-as-is identifier list (the part of retired Rule 11 that survived the migration), and CLAUDE.md Rule 17 for the language policy.

## Historical context (preserved as it was written)

Rule 11 applies the "translate at the right place" principle. Named identifiers (OVS/OVN/OpenFlow concept, CLI verbatim, protocol acronym) KEEP English; descriptive prose words MUST translate to Vietnamese. This table lists common prose words with their canonical Vietnamese translation, so curriculum stays consistent.

Self-classification rule: see CLAUDE.md §11.1 (keep English) + §11.3 (same word, sometimes English sometimes Vietnamese, with examples). Both sections were retired on 2026-04-28; the keep-as-is list was preserved verbatim in the English style guide.

---

#### 11.2. TRANSLATE to Vietnamese when the word appears in descriptive prose

**Cognitive vocabulary, ALWAYS translate:**

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

