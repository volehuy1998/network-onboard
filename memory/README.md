# Memory index

> **Convention:** memory chia 3 nhóm — per-series + shared cross-series.

## Cấu trúc

```
memory/
├── README.md           ← bạn đang đọc
├── sdn/                ← state + audit + tracker cho SDN training
│   ├── series-state.md          ← Per-Part status tracker (Rule 5 handoff)
│   ├── audit-2026-04-25-summary.md  ← consolidated audit
│   ├── keyword-inventory.md     ← REF parsed (~395 entry)
│   ├── keyword-coverage-matrix.md   ← per-entry depth + tier classification
│   ├── keyword-gap-priority.md  ← ranked work list (250 work item)
│   └── lab-verification-pending.md  ← 63 exercise pending lab host
├── haproxy/            ← state cho HAProxy training
│   └── series-state.md
└── shared/             ← cross-series, dùng cho cả 2
    ├── audit-index.md           ← TOC of all audit reports
    ├── file-dependency-map.md   ← Rule 2 cross-file sync map (cả 2 series)
    ├── rule-11-dictionary.md    ← Vietnamese prose translation dict (Rule 11)
    └── session-log.md           ← session-by-session log (cả 2 series)
```

## Khi user nói "làm SDN"

Đọc bắt buộc:
- `memory/sdn/series-state.md` (Per-Part status)
- `memory/shared/file-dependency-map.md` (Rule 2 sync)
- `memory/shared/session-log.md` (last session context)

Đọc khi cần:
- `memory/sdn/keyword-*.md` cho v3.5/v3.6 work
- `memory/sdn/audit-*.md` cho audit findings
- `memory/sdn/lab-verification-pending.md` cho lab tracking

## Khi user nói "làm HAProxy"

Đọc bắt buộc:
- `memory/haproxy/series-state.md`
- `memory/shared/file-dependency-map.md`
- `memory/shared/session-log.md`

## Khi user nói "audit toàn hệ thống"

Đọc:
- `memory/shared/audit-index.md` (TOC)
- Specific audit từ `memory/sdn/audit-*.md` hoặc `memory/haproxy/audit-*.md`
