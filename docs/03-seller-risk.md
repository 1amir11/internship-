# Seller Concentration of Risk (Task 3)

Seller-grain revenue concentration and late/review co-occurrence on the **locked** bases (`docs/01-definitions.md`). Late rule is **not** redefined: `is_late = delivery_delta_days > 0` on the delivered base (**n = 96,470**). Revenue ranking uses **`SUM(order_items.price)`** (product GMV ≈ **R$13.59M**).

Code: `notebooks/olist_full_eda.py` → **SECTION 15: SELLER CONCENTRATION OF RISK**; mirrored in `notebooks/olist_eda.ipynb`.  
Tables: `outputs/tables/seller_level.csv`, `outputs/tables/seller_decile_summary.csv` · Chart: `outputs/charts/20_seller_risk.png`.

---

## Methods and grains

| Object | Grain | Definition |
|--------|-------|------------|
| `seller_revenue` | Seller | `SUM(price)` over **all** item rows for `seller_id` (locked revenue base; used for ranking & deciles) |
| `seller_items` | Seller | Item-row count |
| Delivered seller–order pair | Seller × order | Items → locked delivered orders; **multi-seller order counts once per involved seller** |
| `seller_delivered_orders` | Seller | Distinct delivered `order_id` in that seller’s pairs |
| `seller_late_orders` / `seller_late_rate` | Seller | Count / rate of pairs with locked `is_late` |
| `seller_avg_review`, `seller_review_n`, `seller_1star_rate` | Seller | Deduped `order_id`→review join on delivered pairs; **reviewed-only** denominator (~**95,824** delivered orders with a review; ~**97,151** seller–order–review rows) |

Multi-seller orders: **1,278 / 98,666** orders with items (**1.3%**; of which **1,275** are in the delivered base of 96,470 — 3 are non-delivered). Seller–order delivered pairs = **97,811** vs order-level delivered **96,470** (pair sum exceeds order count when an order has >1 seller).

---

## Thresholds and coverage

| Rule | Use |
|------|-----|
| **All 3,095 sellers** | Concentration / revenue deciles |
| **`seller_delivered_orders >= 10`** | Operational headlines |
| **`>= 5` and `>= 1`** | Appendix sensitivity only (median / IQR late rate) |
| **Zero-delivered sellers** | Isolated **count only** (still in revenue ranking) |

### Operational coverage (`>= 10`)

| Metric | Value | Grain |
|--------|------:|-------|
| n sellers | **1,237** | Seller |
| % sellers | **40.0%** | / 3,095 |
| % delivered orders | **93.9%** | Share of **seller–order** delivered volume (97,811) |
| % revenue | **90.2%** | / `SUM(price)` |

Zero-delivered sellers (items exist but no delivered-base order): **125**.

### Appendix — median / IQR late rate by threshold

| Threshold | n sellers | Median late rate | IQR (pp) |
|-----------|----------:|-----------------:|---------:|
| `>= 10` (headline) | 1,237 | **5.43%** | 7.58 |
| `>= 5` | 1,766 | 4.47% | 10.00 |
| `>= 1` | 2,970 | 0.00% | 7.69 |

---

## Locked Pareto check

Equal to `docs/01-definitions.md` / SECTION 8:

| Slice | Revenue share |
|-------|--------------:|
| Top **10%** sellers (by `seller_revenue`) | **~67.5%** |
| Bottom **50%** sellers | **~3.2%** |

Note: the floor-based top-10% count (309 sellers, 67.49%) differs slightly from the
qcut-based D1 decile below (310 sellers, 67.56%); both round to ~67.5%.
D1 is the primary reference for all Task 3–6 seller tables.

This describes **pooled GMV concentration**. It is **not** an efficiency proof, and the long tail’s small revenue share is **not** framed here as operational “inefficiency.”

---

## Revenue deciles (equal-count; D1 = top)

Ten equal-count groups by `seller_revenue` descending (`rank` method `first` for ties). **n ≈ 309–310** per decile.

**Column grains**

| Column | Grain / formula |
|--------|-----------------|
| `n_sellers` | Seller count in decile |
| `revenue_sum` / `revenue_share` | Seller `SUM(price)` / platform total |
| `delivered_orders` / share | Sum of `seller_delivered_orders` (seller–order pairs) |
| `late_orders` / share | Sum of `seller_late_orders` |
| `order_weighted_late_rate` | `sum(late) / sum(delivered)` in decile |
| `median_seller_late_rate` | Median of seller rates among sellers with `delivered > 0` |
| `order_weighted_review_mean` | Review-n–weighted mean of `seller_avg_review` |
| `median_seller_review` | Median of seller averages among sellers with `review_n > 0` |

| Decile | n | Revenue (R$) | Rev % | Deliv. orders | Deliv % | Late orders | Late % | OW late rate | Med. seller late | OW review | Med. seller review |
|--------|--:|-------------:|------:|--------------:|--------:|------------:|-------:|-------------:|-----------------:|----------:|-------------------:|
| D1 | 310 | 9,183,174.76 | **67.56** | 59,817 | 61.16 | 4,134 | **63.14** | 6.91% | 6.10% | 4.11 | 4.18 |
| D2 | 309 | 2,055,983.47 | 15.13 | 16,022 | 16.38 | 974 | 14.88 | 6.08% | 4.76% | 4.16 | 4.19 |
| D3 | 310 | 1,035,757.79 | 7.62 | 9,120 | 9.32 | 651 | 9.94 | 7.14% | 4.82% | 4.13 | 4.19 |
| D4 | 309 | 549,917.43 | 4.05 | 4,589 | 4.69 | 309 | 4.72 | 6.73% | 4.00% | 4.22 | 4.27 |
| D5 | 310 | 329,944.18 | 2.43 | 3,024 | 3.09 | 178 | 2.72 | 5.89% | 0.00% | 4.23 | 4.33 |
| D6 | 309 | 202,961.64 | 1.49 | 1,978 | 2.02 | 110 | 1.68 | 5.56% | 0.00% | 4.21 | 4.26 |
| D7 | 309 | 116,884.68 | 0.86 | 1,513 | 1.55 | 79 | 1.21 | 5.22% | 0.00% | 4.28 | 4.44 |
| D8 | 310 | 67,209.73 | 0.49 | 839 | 0.86 | 54 | 0.82 | 6.44% | 0.00% | 4.22 | 4.50 |
| D9 | 309 | 36,112.91 | 0.27 | 573 | 0.59 | 41 | 0.63 | 7.16% | 0.00% | 4.21 | 4.67 |
| D10 | 310 | 13,697.11 | 0.10 | 336 | 0.34 | 17 | 0.26 | 5.06% | 0.00% | 4.19 | 5.00 |

Machine-readable: `outputs/tables/seller_decile_summary.csv`.

**Read descriptively:** D1 holds ~**68%** of revenue and ~**63%** of seller-grain late flags; order-weighted late rates stay in a similar band across deciles (~5–7%). Median seller late rate falls to **0** in lower-revenue deciles because many low-volume sellers have zero late orders (small denominators), not because the tail is “risk-free.”

---

## Top-30 sellers by `seller_late_orders`

Sorted by late seller–order count (then revenue). Together: **1,968** late seller–orders → **~30.1%** of all seller-grain late flags (**6,547**; order-level late count remains **6,534**).

| Rank | seller_id (abbrev.) | Delivered n | Late n | Late rate | Rev. decile | Avg review |
|-----:|---------------------|------------:|-------:|----------:|:-----------:|-----------:|
| 1 | `4a3ca931…` | 1,772 | 172 | 9.7% | D1 | 3.86 |
| 2 | `1f50f920…` | 1,399 | 124 | 8.9% | D1 | 4.14 |
| 3 | `4869f7a5…` | 1,124 | 118 | 10.5% | D1 | 4.15 |
| 4 | `6560211a…` | 1,819 | 96 | 5.3% | D1 | 3.98 |
| 5 | `ea8482cd…` | 1,132 | 96 | 8.5% | D1 | 4.03 |
| 6 | `7c67e144…` | 973 | 89 | 9.1% | D1 | 3.50 |
| 7 | `da8622b1…` | 1,311 | 87 | 6.6% | D1 | 4.18 |
| 8 | `cc419e06…` | 1,651 | 87 | 5.3% | D1 | 4.15 |
| 9 | `8b321bb6…` | 930 | 81 | 8.7% | D1 | 4.10 |
| 10 | `955fee92…` | 1,261 | 77 | 6.1% | D1 | 4.20 |
| 11 | `06a2c3af…` | 389 | 74 | 19.0% | D1 | 4.01 |
| 12 | `1025f0e2…` | 910 | 72 | 7.9% | D1 | 4.01 |
| 13 | `7d13fca1…` | 558 | 64 | 11.5% | D1 | 4.04 |
| 14 | `620c87c1…` | 722 | 63 | 8.7% | D1 | 4.31 |
| 15 | `7a67c85e…` | 1,145 | 60 | 5.2% | D1 | 4.28 |
| 16 | `3d871de0…` | 1,064 | 58 | 5.5% | D1 | 4.19 |
| 17 | `fa1c13f2…` | 578 | 53 | 9.2% | D1 | 4.37 |
| 18 | `81602554…` | 380 | 52 | 13.7% | D1 | 3.95 |
| 19 | `391fc663…` | 521 | 45 | 8.6% | D1 | 4.04 |
| 20 | `1835b56c…` | 417 | 43 | 10.3% | D1 | 3.67 |
| 21 | `88460e8e…` | 246 | 42 | 17.1% | D1 | 3.45 |
| 22 | `e9779976…` | 645 | 39 | 6.0% | D1 | 4.26 |
| 23 | `855668e0…` | 300 | 38 | 12.7% | D1 | 3.85 |
| 24 | `4e922959…` | 412 | 37 | 9.0% | D1 | 3.96 |
| 25 | `a1043baf…` | 702 | 35 | 5.0% | D1 | 4.28 |
| 26 | `cca3071e…` | 699 | 34 | 4.9% | D1 | 3.88 |
| 27 | `e5a34388…` | 216 | 34 | 15.7% | D2 | 4.00 |
| 28 | `218d46b8…` | 382 | 33 | 8.6% | D1 | 4.19 |
| 29 | `1900267e…` | 406 | 33 | 8.1% | D1 | 3.86 |
| 30 | `16090f2c…` | 398 | 32 | 8.0% | D1 | 4.09 |

Full IDs and metrics: filter `seller_level.csv` by the same sort.

---

## Late-rate distribution by volume band

Sellers with ≥1 delivered order (**n = 2,970**). Bands on `seller_delivered_orders`.

| Volume band | n sellers | Median late rate | P90 late rate |
|-------------|----------:|-----------------:|--------------:|
| 1 | 536 | 0.0% | 0.0% |
| 2–4 | 668 | 0.0% | 33.3% |
| 5–9 | 529 | 0.0% | 20.0% |
| 10–29 | 610 | 5.3% | 16.7% |
| 30+ | 627 | 5.5% | 12.6% |

Low-volume medians of 0% and high p90s reflect **binary / thin denominators**, not a claim that small sellers are uniformly better or worse.

---

## Link to P1 (one paragraph)

P1 is the locked association between late delivery and lower reviews at **order** grain. At **seller** grain, late seller–order flags are **concentrated** with revenue (D1 ≈ 63% of late flags and ≈ 68% of GMV), while order-weighted late rates remain in a narrow band across deciles; separately, low delivered-volume bands show wide **seller-level** late-rate spread (high p90). Descriptively, fulfillment risk co-occurs with both elite GMV sellers (via volume of late flags) and thin-denominator sellers (via rate volatility). This section does **not** claim that sellers cause lateness or review loss, does not name carriers, and does not assert predictive improvement from any intervention.

---

## Figure

`outputs/charts/20_seller_risk.png` — two panels:

- **(a)** Revenue share vs late-orders share by revenue decile; seller grain; **n = 3,095**; ranking on all-items `SUM(price)`; locked `is_late`.
- **(b)** Median and p90 seller late rate by delivered-order volume band; sellers with ≥1 delivered (**n = 2,970**); operational headline threshold ≥10 (**n = 1,237**).

Captions state grain, n, and correlational framing (no causality).

---

## Limits / caveats

- **Pair vs order grain:** seller–order late sums (**6,547**) can exceed order-level late (**6,534**) when multi-seller orders are late.
- **Zero-delivered sellers (125)** enter revenue deciles but have undefined late rates.
- **Review metrics** use reviewed-only denominators; sellers/orders without reviews are excluded from review means.
- **Median late rate = 0** in lower deciles / low-volume bands is often a small-n artifact.
- **Concentration ≠ efficiency:** top-decile GMV share does not prove elite sellers are more efficient, and the bottom half’s ~3.2% revenue share is not labeled “inefficient.”
- **No causal / predictive claims** about sellers, carriers, or interventions; wording stays descriptive/correlational.
- Task 2 delivery decomposition and `docs/01-definitions.md` remain locked and unchanged.
