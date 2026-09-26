# Cohort Retention Analysis (Task 5)

Fixed-window cohort retention on **`customer_unique_id`** (customer grain). Does **not** redefine or replace the locked crude full-window one-time rate (**93,099 / 96,096 = 96.88%** — `docs/01-definitions.md`). Late / delivery / category / seller definitions remain locked.

Code: `notebooks/olist_full_eda.py` → **SECTION 17: COHORT RETENTION** (lines **1757–2073**); mirrored in `notebooks/olist_eda.ipynb` (cells **38–39**, after SECTION 16 cells 36–37).  
Tables: `outputs/tables/cohort_monthly.csv`, `outputs/tables/cohort_customers.csv` · Chart: `outputs/charts/22_cohort_retention.png`.

---

## Methods and identity

| Field | Definition |
|-------|------------|
| **Customer** | `customer_unique_id` — a person may map to multiple `customer_id`; **never** use `customer_id` for retention rates |
| **First purchase** | `MIN(order_purchase_timestamp)` per `customer_unique_id` over **all** rows in `olist_orders_dataset.csv` |
| **Repeat** | Distinct `order_id` count (`nunique`) — same-day multi-rows never inflate |
| **Primary status rule** | **All** `order_status` values count as purchases (behavioral loyalty) |
| **Delivered-only sensitivity** | Restrict to `order_status == 'delivered'` (first + subsequent among delivered only) |
| **Grain for rates** | **Customer** (`customer_unique_id`); order grain only for supporting context (orders per repeater) |

Purchase timestamps: **0 nulls** (asserted). Orders purchase window: **2016-09-04 → 2018-10-17**.

### Fan-out / sanity

| Check | Value |
|-------|------:|
| Unique `customer_unique_id` | **96,096** |
| `unique_id` with >1 `customer_id` | **2,997** |
| Max distinct orders per `customer_unique_id` | **17** |
| Primary first-purchase `delivered` | **93,253** |
| Primary first-purchase non-delivered statuses | **2,843** |

---

## Eligibility cutoff (date math)

Dataset max purchase date used for observability: **2018-10-17**.

\[
\text{eligibility cutoff} = 2018\text{-}10\text{-}17 - 365\text{ days} = \mathbf{2017\text{-}10\text{-}17}
\]

| Group | Rule | n |
|-------|------|--:|
| **Eligible (12m denominator)** | `first_date ≤ 2017-10-17` | **29,087** |
| **Censored / incomplete-window** | `first_date` in **2017-10-18 → 2018-10-17** | **67,009** |
| **Sum** | Must equal unique customers | **96,096** |

Boundary: **2017-10-17** included (≤ cutoff); **2017-10-18** censored.  
**Every 12m rate uses eligible customers as denominator — not all 96,096.**

---

## H1-2017 headline (primary, 365-day window)

Pooled first-purchasers **Jan–Jun 2017** (all eligible by construction).

| Metric | Value | Grain |
|--------|------:|-------|
| `n_customers` (eligible) | **14,239** | Customer |
| `n_repeat_12m` (≥2 distinct orders with second ≤ first + 365d) | **666** | Customer |
| `repeat_12m_rate` | **666 / 14,239 = 4.68%** | Customer |
| `n_3plus_12m` | **71** | Customer |
| `median_days_to_second` (among 12m repeaters) | **60.5** | Customer |
| Mean / median orders in 12m among repeaters | **2.14 / 2.0** | Order count per repeater (supporting) |

Feasibility anchor matched exactly: **n = 14,239**.

---

## Monthly cohorts Jan–Oct 2017 (12m, eligible denominator)

| cohort_month | n_customers | n_eligible_12m | n_repeat_12m | repeat_12m_rate | n_3plus_12m | median_days_to_second | note |
|--------------|------------:|---------------:|-------------:|----------------:|------------:|----------------------:|------|
| 2017-01 | 764 | 764 | 48 | **6.28%** (48/764) | 9 | 1.0 | |
| 2017-02 | 1,752 | 1,752 | 62 | **3.54%** (62/1,752) | 4 | 88.0 | |
| 2017-03 | 2,636 | 2,636 | 113 | **4.29%** (113/2,636) | 14 | 65.0 | |
| 2017-04 | 2,352 | 2,352 | 99 | **4.21%** (99/2,352) | 8 | 84.0 | |
| 2017-05 | 3,596 | 3,596 | 182 | **5.06%** (182/3,596) | 25 | 50.5 | |
| 2017-06 | 3,139 | 3,139 | 162 | **5.16%** (162/3,139) | 11 | 63.0 | |
| 2017-07 | 3,894 | 3,894 | 178 | **4.57%** (178/3,894) | 18 | 37.5 | |
| 2017-08 | 4,184 | 4,184 | 197 | **4.71%** (197/4,184) | 25 | 45.0 | |
| 2017-09 | 4,130 | 4,130 | 190 | **4.60%** (190/4,130) | 19 | 47.0 | |
| 2017-10 | 4,470 | 2,314 | 80 | **3.46%** (80/2,314) | 10 | 36.5 | Oct truncated to ≤2017-10-17; **2,156** post-cutoff censored |

**Monthly eligible 12m repeat range: 3.46% – 6.28%.**  
Cross-foot: Jan–Oct `n_eligible_12m` sum = **28,761**; `n_repeat_12m` sum = **1,311** — both match the eligible customer file filtered to first_date in [2017-01-01, 2017-10-17].

---

## Sensitivities

### 6m window (fixed **182** days ≈ 6 months; same eligibility)

| Cohort | Rate |
|--------|------|
| H1-2017 | **483 / 14,239 = 3.39%** |

### Delivered-only (`order_status == 'delivered'`)

| Scope | n | 12m repeat |
|-------|--:|-----------|
| Delivered-first customers (any) | 93,358 | — |
| Delivered-first eligible ≤ cutoff | 27,911 | — |
| H1-2017 delivered-first | **13,592** (primary H1 **14,239**; Δn = **647**) | **616 / 13,592 = 4.53%** |
| Delta vs primary H1 rate | — | **+0.15 pp** (primary higher) |

Canceled / unavailable / invoiced / etc. first purchases are **included in primary**, **excluded from delivered-only** (or shifted if a later delivered order exists).

---

## Reconciliation vs crude 96.88% (mandatory)

| Metric | Numerator / denominator | Rate | Window | Denominator |
|--------|-------------------------|-----:|--------|-------------|
| **Crude one-time (locked)** | **93,099 / 96,096** | **96.88%** | Full orders window (variable observability) | **All** unique customers |
| **Crude repeat (locked complement)** | **2,997 / 96,096** | **3.12%** | Full window | All 96,096 |
| **H1-2017 cohort 12m repeat** | **666 / 14,239** | **4.68%** | Fixed 365 days from first purchase | **Eligible** H1 first-purchasers only |

The crude **96.88% one-time / 3.12% repeat** figures remain the locked full-window facts (`docs/01-definitions.md`); they are **not** replaced. H1-2017 eligible customers show a **higher** 12m repeat rate (**4.68%**) than the crude full-window repeat (**3.12%**) — less alarming than reading “only 3.1% ever return” as a fixed-horizon loyalty rate — because (1) the cohort denominator is **eligible** first-purchasers with a full 365-day observation window (**14,239**), not all **96,096** (of whom **67,009** are right-censored with &lt;12m observability), and (2) the window is a **fixed 365 days** from first purchase rather than a variable span ending at 2018-10-17. Both numbers are valid for their stated grains; they answer different questions.

**Deltas (descriptive):** cohort 12m repeat − crude repeat ≈ **+1.56 pp**; crude one-time remains **96.88%** on the full-window denominator.

---

## Link to P2 (one paragraph)

P2 is the loyalty / near-zero-repeat problem framed from the locked crude full-window one-time rate (**96.88%**). Cohort analysis **co-occurs** with that fact: H1-2017 eligible customers show **4.68%** repeat within 12m (**666 / 14,239**), and monthly cohorts range **3.46%–6.28%** on eligible denominators. This section does **not** claim that lateness causes non-repeat, that fixing delivery will raise retention to a target, or that loyalty has “recovered”; it does not quantify LTV/CAC as fact, name carriers, or make predictive claims. Crude **96.88%** stays alongside cohort rates.

---

## Figure

`outputs/charts/22_cohort_retention.png` — two panels:

- **(a)** Monthly-cohort 12m repeat bars (Jan–Oct 2017) with **eligible-n** labels; customer grain; 365-day rule; cutoff **2017-10-17**; no causality.
- **(b)** H1-2017 12m eligible vs crude full-window repeat (two bars; denominators explicitly labeled **“12m eligible”** vs **“full-window crude”**) + censored-count annotation (**67,009**); no causality.

---

## Limits / caveats

- **Right-censoring:** post-2017-10-17 first-purchasers are incomplete-window; never in the 12m denominator.
- **Oct-2017 cohort** is truncated to ≤2017-10-17 (**2,314** eligible of **4,470** calendar-month first-purchasers).
- **Primary includes non-delivered** first purchases; delivered-only is sensitivity only.
- **No imputation** of missing timestamps (purchase nulls = 0).
- **Customer vs order grain:** do not divide orders by customers across grains without labeling.
- Tasks 1–4 outputs and `docs/01-definitions.md` remain locked; crude **96.88%** is never overwritten.
