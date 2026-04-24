# Template A — Anatomy block cho output của command

> **Mục tiêu:** giải thích output thực của một command OVS/OVN để kỹ sư đọc hiểu được từng field, từng counter, từng cột.
> **Upstream baseline:** OVS Advanced Tutorial field annotation pattern (github.com/openvswitch/ovs/Documentation/tutorials/ovs-advanced.rst).
> **Tối thiểu:** 50 dòng.

## Skeleton

```markdown
### N.N.N Đọc hiểu output `<tool> <subcommand>`

**Bối cảnh khi chạy:**

<2-5 dòng mô tả khi nào engineer dùng command này, vấn đề gì trigger mở terminal gõ lệnh này, từ playbook nào (L1-L6 của Part 9.4), expected state của hệ thống lúc này>.

**Command và output thật** (reproduce từ `<môi trường lab>` hoặc lift từ `<upstream source>`):

\`\`\`shell
$ <command đầy đủ bao gồm option và argument>
<raw output 20-50 dòng, KHÔNG cắt bớt theo Rule 7a, copy verbatim từ terminal>
\`\`\`

**Anatomy từng field (table đọc hiểu):**

| Cột / Field | Giá trị mẫu | Ý nghĩa kỹ thuật | Dấu hiệu bất thường |
|---|---|---|---|
| `<field1>` | `<mẫu>` | <2-3 dòng giải thích bản chất field này — nó lưu gì, tính theo công thức nào, update bởi thread nào> | <giá trị nào phải cảnh báo> |
| `<field2>` | `<mẫu>` | <...> | <...> |
| `<field3>` | `<mẫu>` | <...> | <...> |
| ... | ... | ... | ... |

**Kịch bản bẻ gãy (troubleshooting cues):**

- **Nếu `<field>` = `<value abnormal>`** → symptom quan sát được là <A>, root cause có khả năng nhất là <B>, bước verify tiếp theo là <command C>, fix bằng <action D>.
- **Nếu ratio `<fieldA>` / `<fieldB>` > `<threshold>`** → <...>.
- **Nếu `<counter>` tăng với tốc độ > `<X>/sec`** → <...>.

**Liên hệ với concept/cơ chế:**

<2-4 dòng nối output này với cơ chế OVS/OpenFlow/OVN đã học ở Part X.Y — field này phản ánh state nào trong datapath/pipeline, counter này cập nhật từ code path nào của ovs-vswitchd>.

**Upstream nguồn đọc thêm:**

- [man <tool>(<section>)](https://man7.org/linux/man-pages/man<section>/<tool>.<section>.html) section `<SECTION_NAME>`
- `<path>` trong upstream source, ví dụ `lib/<file>.c` function `<name>()`
- <tutorial link hoặc NSDI paper section>
```

## Yêu cầu chi tiết

**1. Bối cảnh khi chạy.** Không phải "lệnh này dùng để ...". Phải là "khi engineer oncall được page 2h sáng về triệu chứng X, step đầu tiên trong playbook là chạy lệnh này vì ...". Bối cảnh phải operational, không academic.

**2. Raw output.** PHẢI là real capture. Mark rõ một trong ba state:

- `[real capture — Ubuntu 22.04 + OVS 2.17.9 + OVN 22.03.8]`
- `[reproduced from <upstream source>]`
- `[synthetic example illustrating <pattern>]`

Synthetic chỉ được dùng khi output real quá phụ thuộc cấu hình cục bộ, và phải note rõ.

**3. Anatomy table.** Minimum 3-5 cột (Cột / Giá trị mẫu / Ý nghĩa / Dấu hiệu bất thường). Mỗi field explain 2-3 dòng ý nghĩa kỹ thuật (không 1 dòng). Nếu output có > 10 field, chia thành nhiều table theo nhóm (ví dụ "nhóm counter", "nhóm timestamp", "nhóm config").

**4. Kịch bản bẻ gãy.** Minimum 3 kịch bản. Format:
- `Nếu <condition>` → `symptom` → `root cause` → `verify command` → `fix action`.

Đây là phần operational value cao nhất — engineer đọc anatomy 1 lần rồi nhớ; kịch bản bẻ gãy đọc nhiều lần khi debug.

**5. Liên hệ concept.** Nối output với cơ chế đã học. Ví dụ: `packets`/`bytes` counter trong `ofproto/trace` không tăng cho đến khi có `-generate`, vì đây là simulation không gửi gói tin thật — kết nối với Phần 9.2 §9.2.X fast/slow path.

**6. Upstream link.** Ít nhất 2 nguồn. Man page cụ thể (không phải home page), hoặc source file + function name, hoặc tutorial .rst cụ thể.

## Ví dụ đầy đủ (mẫu reference)

Xem Phần 9.4 session S38 expansion — section §9.4.X "Đọc hiểu output `ovs-ofctl dump-flows`" là ví dụ hoàn chỉnh áp dụng template này.
