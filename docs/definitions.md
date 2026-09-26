# HVIA Olist — Locked Analysis Definitions

Single source of truth for metric grain, denominator, and formula.  
Code: `notebooks/olist_full_eda.py`, `notebooks/olist_eda.ipynb`.  
**Do not change these definitions without updating this file and all citing docs.**

Raw CSVs: `archive/` (9 Olist tables; Kaggle source documented in `archive/README.md`).

---

## Truncation / window notes

| Grain | Min purchase | Max purchase | Notes |
|-------|--------------|--------------|-------|
| `orders` table | 2016-09-04 | 2018-10-17 | Full orders window |
| `master` / items-joined | 2016-09-04 | **2018-09-03** | **775** orders have **no items** → drop out of item joins; max date truncates |
| Payments | — | — | **1** order has no payment row |

---

## 1. Late delivery (primary)

| Field | Definition |
|-------|------------|
| **Formula** | `delivery_delta_days = (delivered_customer_date − estimated_delivery_date).dt.days`; **late** iff `delivery_delta_days > 0` |
| **Grain** | Order-level |
| **Denominator** | Delivered base (def. 4): **96,470** |
| **Numerator** | **6,534** late orders |
| **Primary rate** | **6.77%** (docs often round to **6.8%**) |
| **Code** | `orders_delivered['is_late'] = orders_delivered['delivery_delta'] > 0` |

### Late-definition sensitivity (do not swap primary)

| Rule | Count | Rate |
|------|-------|------|
| **Primary:** `delta_days > 0` (calendar-day truncate) | 6,534 | **6.77%** |
| **Sensitivity:** strict timestamp `delivered > estimated` | 7,826 | **8.11%** |
| Gap | 1,292 | Same-calendar-day cases: day-diff = 0 but timestamp still after ETA |

Primary remains **6.77% / 6.8%**. Cite 8.11% only as sensitivity.

---

## 2. Average order value (AOV)

| Field | Definition |
|-------|------------|
| **Primary formula** | Mean of per-order product totals: `items.groupby('order_id')['price'].sum().mean()` |
| **Grain** | Order (orders that appear in `order_items`) |
| **Primary value** | **R$ 137.75** (docs may round ~R$138) |
| **Alternate (not primary)** | `SUM(price) / n_orders_with_items` ≈ **R$ 136.68** — label explicitly if used |

---

## 3. Freight share (three formulas)

| Label | Formula | Value | Use |
|-------|---------|-------|-----|
| **PRIMARY** | `SUM(freight) / (SUM(price) + SUM(freight))` | **14.21%** (~**14.2%**) of total paid | Headline freight burden |
| **SECONDARY** | `SUM(freight) / SUM(price)` | **16.57%** (~**16.6%** / docs ~**17%** of product revenue) | Freight vs product GMV only |
| **SECONDARY (mean item)** | Mean of `freight / (price + freight)` per item row | **21.34%** (~**21.3%**) | Category charts / item experience |

Always state which of the three when quoting a freight %.

---

## 4. Delivered denominator

| Field | Definition |
|-------|------------|
| **Formula** | `order_status == 'delivered'` **and** both `order_delivered_customer_date` and `order_estimated_delivery_date` non-null |
| **Grain** | Order-level |
| **Value** | **96,470** |
| **Use** | Late rate, delivery deltas, delivery↔review joins (after review dedupe) |

---

## 5. Retention wording

| Field | Definition |
|-------|------------|
| **Grain** | `customer_unique_id` over the **full orders window** (not cohort / not time-bounded) |
| **Unique customers** | **96,096** |
| **One-time** | **93,099** → **96.88%** (docs **96.9%**) |
| **Repeat 2+** | **2,997** → **3.1%** |
| **Wording** | Always **“crude full-window one-time rate”** (not retention curve / not survival) |

---

## 6. Revenue base

| Field | Definition |
|-------|------------|
| **Formula** | `SUM(order_items.price)` — product GMV only (**excludes freight**) |
| **Value** | **R$ 13,591,643.70** (docs ~R$13.6M) |
| **Seller Pareto** | Same base, grouped by `seller_id` on item/master grain → top 10% ~**67.5%**, bottom 50% ~**3.2%** |

---

## Quick citation cheat-sheet

- Late: **6.8% of 96,470 delivered (`delta_days > 0`)**; reviews on-time/late **4.29 / 2.27** on that late flag  
- AOV: **~R$138 per-order mean of Σprice**  
- Freight: **14.2% of total paid (primary)**; **~17% of product (secondary)**; **mean item ratio 21.3%**  
- Retention: **96.9% crude full-window one-time rate** (93,099 / 96,096)  
- Revenue: **R$13.6M = SUM(price)**
