# Plans index

> **Convention:** plans tổ chức theo curriculum series. Khi làm việc với 1 series, đọc đúng directory của series đó.

## Cấu trúc

```
plans/
├── README.md           ← bạn đang đọc
├── sdn/                ← plans cho SDN training (OVS + OpenFlow + OVN)
│   ├── v3.5-keyword-backbone.md
│   ├── v3.6-content-depth.md
│   └── v3.7-reckoning-and-mastery.md   ← ACTIVE
└── haproxy/            ← plans cho HAProxy training
    └── (placeholder)
```

## SDN plans timeline

| File | Trạng thái | Tag | Verdict |
|------|-----------|-----|---------|
| [v3.5-keyword-backbone.md](sdn/v3.5-keyword-backbone.md) | Closed 2026-04-25 | `v3.5-KeywordBackbone` | Placement framework, không phải mastery (xem v3.7 reckoning) |
| [v3.6-content-depth.md](sdn/v3.6-content-depth.md) | Closed 2026-04-26 | `v3.6-AuditTooling` (rename per Phase A) | Audit tooling + 6 keyword closure, không phải content depth thực |
| [v3.7-reckoning-and-mastery.md](sdn/v3.7-reckoning-and-mastery.md) | Phase A-F done; Phase G PARTIAL (~22% reach tier target, gaming detected 2026-04-26) | (no tag) | 8 phase A→H plan; Phase G self-deception caught; superseded by v3.8 remediation |
| [v3.8-remediation.md](sdn/v3.8-remediation.md) | **APPROVED 2026-04-26, ACTIVE** | (TBD `v4.0-MasteryComplete` after Phase R6) | 7 phase R0-R6, anti-gaming infrastructure + per-keyword work + final audit, 352-577 giờ |

## HAProxy plans

Hiện chưa có plan active. Series HAProxy 1/29 Parts (xem `memory/haproxy/series-state.md`).

## Khi user nói "làm SDN"

Đọc `plans/sdn/*.md` + `memory/sdn/*` + `memory/shared/*`.

## Khi user nói "làm HAProxy"

Đọc `plans/haproxy/*.md` + `memory/haproxy/*` + `memory/shared/*`.
