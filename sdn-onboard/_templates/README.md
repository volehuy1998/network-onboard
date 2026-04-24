# Phase H Template Library

> **Mục tiêu:** đảm bảo mọi Phần trong Phase H (Foundation Depth Pass) viết content theo 4 template chuẩn thay vì ad-hoc.
> **Áp dụng:** session S38 trở đi.
> **Nguồn gốc:** `plans/phase-h-foundation-depth.md` §2.

## Bốn template

| ID | Tên | Khi nào dùng | Baseline upstream |
|---|---|---|---|
| A | [Anatomy block](template-a-anatomy-block.md) | Giải thích output của một command (dump-flow, show, trace, stats) | OVS Advanced Tutorial field annotation |
| B | [Per-field block](template-b-per-field.md) | Định nghĩa khớp với field OpenFlow hoặc OVN | `ovs-fields(7)` 9-attribute anatomy |
| C | [Per-action block](template-c-per-action.md) | Định nghĩa OpenFlow action hoặc instruction | `ovs-actions(7)` 8-attribute anatomy |
| D | [Per-table pipeline block](template-d-per-table.md) | Định nghĩa stage trong OVN ingress/egress pipeline hoặc OpenFlow table của OVS | `ovn-architecture(7)` table map |

## Quy ước chung

1. Mỗi block phải có **upstream source** cụ thể (man page section, RFC, spec, tutorial .rst), cite ở cuối.
2. Raw output mẫu phải **reproduce thật** trên Ubuntu 22.04 LTS + OVS 2.17.9 + OVN 22.03.8; nếu không có lab host, lift từ upstream doc + mark rõ `[reproduced from <source>]`. Rule 7 + Rule 7a CLAUDE.md.
3. Tiếng Việt cho prose, English cho named identifier. Rule 11 CLAUDE.md.
4. Không overuse em-dash. Rule 13 CLAUDE.md, density target < 0.10/line.
5. Mỗi block tối thiểu **50 dòng** (prose + raw output + table anatomy + scenario bẻ gãy). Dưới mức này không đạt.
6. Code block target **20-50 dòng** cho output sample; tránh one-liner trừ khi là ví dụ syntax.

## Kiểm tra trước commit

Checklist Phase H mỗi file mới/sửa:

```
[ ] Áp dụng đúng template A/B/C/D theo loại content
[ ] Mọi code block output 20-50 dòng (không 2-5 dòng)
[ ] Mọi output có Anatomy table giải thích từng field
[ ] Có ít nhất 1 scenario bẻ gãy (nếu field X = Y thì symptom Z)
[ ] Có link upstream source (man page / RFC / tutorial)
[ ] Rule 11 §11.6 scan PASS trên file
[ ] Rule 13 em-dash density < 0.10/line
[ ] Rule 14 source code citation verified nếu có SHA/function/file
[ ] Rule 9 null byte check PASS
[ ] Median code block length ≥ 15 dòng (per Phase H quality gate)
```
