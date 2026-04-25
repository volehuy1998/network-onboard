# Plans index

> **Convention:** plans tổ chức theo curriculum series. Khi làm việc với 1 series, đọc đúng directory của series đó.

## Cấu trúc

```
plans/
├── README.md           ← bạn đang đọc
├── sdn/                ← plans cho SDN training (OVS + OpenFlow + OVN)
│   ├── v3.5-keyword-backbone.md
│   └── v3.6-content-depth.md
└── haproxy/            ← plans cho HAProxy training
    └── (placeholder)
```

## SDN plans active

| File | Trạng thái | Tag |
|------|-----------|-----|
| [v3.5-keyword-backbone.md](sdn/v3.5-keyword-backbone.md) | RELEASED 2026-04-25 (14/14 phase done) | `v3.5-KeywordBackbone` |
| [v3.6-content-depth.md](sdn/v3.6-content-depth.md) | DRAFT 2026-04-26, chờ user confirm | (chưa tag) |

## HAProxy plans

Hiện chưa có plan active. Series HAProxy 1/29 Parts (xem `memory/haproxy/series-state.md`).

## Khi user nói "làm SDN"

Đọc `plans/sdn/*.md` + `memory/sdn/*` + `memory/shared/*`.

## Khi user nói "làm HAProxy"

Đọc `plans/haproxy/*.md` + `memory/haproxy/*` + `memory/shared/*`.
