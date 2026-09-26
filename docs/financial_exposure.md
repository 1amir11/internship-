# Financial Exposure Scenarios (Task 6)

Implied commission exposure under **unsourced** take-rate assumptions applied to locked product GMV bases (`docs/definitions.md`). Late rule is **not** redefined: `is_late = delivery_delta_days > 0` on the delivered base (**n = 96,470**; **6,534** late orders). Product GMV = **`SUM(order_items.price)`** = **R$13,591,643.70**.

**True 2016–18 marketplace take-rate is unverified.** Rates **15% / 19% / 21%** are scenario assumptions only — not facts. There is **no** “recoverable revenue” column.

Code: `notebooks/olist_full_eda.py` → **SECTION 18: FINANCIAL EXPOSURE SCENARIOS** (lines **2074–2393**); mirrored in `notebooks/olist_eda.ipynb` (cells **40–41**, after SECTION 17 cells 38–39).  
Table: `outputs/tables/financial_exposure.csv` · Chart: `outputs/charts/23_financial_exposure.png`.

---

## Methods and bases

| Object | Grain | Definition |
|--------|-------|------------|
| **Product GMV** | Item (all items) | `SUM(items.price)` — locked revenue base; **excludes freight** |
| **Late GMV** | Item (delivered) | `SUM(price)` on items whose order has locked `is_late` (**order-level flag broadcast** to every item in that order) |
| **Customer-paid base** | Item | `SUM(price) + SUM(freight)` = **R$15,843,553.24** — **context only**; not the primary commissionable base |
| **`payment_value`** | Payment row | `SUM(payments.payment_value)` = **R$16,008,872.12** — **reconciliation footnote only** |
| **Implied commission** | Scenario | `commission = GMV × take_rate` for rates in {0.15, 0.19, 0.21} |

Freight is **never** presented as commissionable without labeling it a scenario variant (none used as primary here).

### Late-item / GMV broadcast

| Check | Value |
|-------|------:|
| Late orders (locked) | **6,534** |
| Late items (broadcast) | **7,264** |
| Ratio items/orders | **≈ 1.112** |
| Late GMV | **R$985,924.34** |

Multi-item late orders inherit the same order-level `is_late` on every item row — item counts and late GMV exceed a naïve one-row-per-late-order view.

---

## Scenario table (implied commission under X% assumption)

| Slice | Grain | n_items | n_orders | Product GMV (R$) | Share of total GMV | Comm @15% | Comm @19% | Comm @21% |
|-------|-------|--------:|---------:|-----------------:|-------------------:|----------:|----------:|----------:|
| Total product GMV | item (all) | 112,650 | 98,666 | **13,591,643.70** | 100% | 2,038,746.55 | 2,582,412.30 | 2,854,245.18 |
| Late product GMV | item (is_late broadcast) | 7,264 | 6,534 | **985,924.34** | **7.25%** | 147,888.65 | **187,325.62** | 207,044.11 |
| D1 late GMV | item (D1 sellers × late) | 4,508 | 4,127 | 680,097.81 | 5.00% | 102,014.67 | 129,218.58 | 142,820.54 |
| Top-30 late-seller GMV | item (Task-3 IDs × late) | 2,177 | 1,964 | 224,401.75 | 1.65% | 33,660.26 | 42,636.33 | 47,124.37 |
| Top-10 category late GMV | item (≥100 cats) | 4,587 | 4,122 | 637,375.28 | 4.69% | 95,606.29 | 121,101.30 | 133,848.81 |

Reading guide (allowed wording): **late GMV represents 7.25% of product GMV; under a 19% assumption, implied commission on late GMV is R$187,325.62.** True take-rate unverified.

Machine-readable: `outputs/tables/financial_exposure.csv` (columns: `slice`, `grain`, `n_items`, `n_orders`, `gmv_product`, `gmv_share`, `commission_15`, `commission_19`, `commission_21`).

---

## Late-GMV concentration cuts

| Cut | Formula | Late GMV (R$) | Share of **late** GMV |
|-----|---------|--------------:|----------------------:|
| D1 late GMV | Late items from Task-3 revenue decile **D1** (310 sellers) | 680,097.81 | **68.98%** |
| Top-30 late sellers | Late items from Task-3 top-30 by `seller_late_orders` | 224,401.75 | **22.76%** |
| Top-10 categories | Late GMV among named cats with **≥100** delivered orders, ranked by late GMV | 637,375.28 | **64.65%** |

Coverage vs Task 3: top-30 seller ID set overlap **30/30**; D1 seller count **310**.

### Category late-GMV top-10 (≥100 filter, item grain)

| Rank | Category | Late GMV (R$) | n_items | n_orders | Comm @19% (assumed) |
|-----:|----------|--------------:|--------:|---------:|--------------------:|
| 1 | health_beauty | 94,273.39 | 716 | 649 | 17,911.94 |
| 2 | watches_gifts | 91,298.05 | 422 | 406 | 17,346.63 |
| 3 | bed_bath_table | 79,235.10 | 770 | 689 | 15,054.67 |
| 4 | sports_leisure | 70,453.26 | 532 | 495 | 13,386.12 |
| 5 | auto | 66,549.23 | 291 | 278 | 12,644.35 |
| 6 | computers_accessories | 61,459.32 | 496 | 417 | 11,677.27 |
| 7 | furniture_decor | 58,515.94 | 574 | 449 | 11,118.03 |
| 8 | cool_stuff | 39,269.48 | 217 | 210 | 7,461.20 |
| 9 | housewares | 38,465.31 | 340 | 308 | 7,308.41 |
| 10 | baby | 37,856.20 | 229 | 226 | 7,192.68 |

---

## Monthly late-GMV rate (purchase month, Jan-2017–Aug-2018)

Within-month rate = late product GMV / product GMV that purchase month (all-items `SUM(price)`). Seasonality context only — no causality.

| Month | Month GMV (R$) | Late GMV (R$) | Late-GMV rate | n_items late | n_orders late |
|-------|---------------:|--------------:|--------------:|-------------:|--------------:|
| 2017-01 | 120,311.60 | 3,115.95 | 2.59% | 24 | 22 |
| 2017-02 | 247,302.59 | 6,263.68 | 2.53% | 58 | 49 |
| 2017-03 | 374,341.15 | 16,070.84 | 4.29% | 136 | 116 |
| 2017-04 | 359,925.26 | 28,172.07 | 7.83% | 160 | 151 |
| 2017-05 | 506,065.94 | 14,764.98 | 2.92% | 128 | 106 |
| 2017-06 | 433,038.34 | 26,442.62 | 6.11% | 103 | 95 |
| 2017-07 | 498,027.23 | 18,691.46 | 3.75% | 133 | 108 |
| 2017-08 | 573,968.82 | 16,639.93 | 2.90% | 133 | 122 |
| 2017-09 | 624,396.18 | 26,710.42 | 4.28% | 208 | 182 |
| 2017-10 | 664,218.49 | 25,773.67 | 3.88% | 204 | 187 |
| 2017-11 | 1,010,270.06 | 126,218.09 | **12.49%** | 1,009 | 904 |
| 2017-12 | 743,911.15 | 77,499.92 | 10.42% | 452 | 411 |
| 2018-01 | 950,024.72 | 68,787.49 | 7.24% | 463 | 403 |
| 2018-02 | 844,181.10 | 127,034.06 | **15.05%** | 1,046 | 926 |
| 2018-03 | 983,212.16 | 187,137.72 | **19.03%** | 1,447 | 1,328 |
| 2018-04 | 996,638.57 | 48,351.92 | 4.85% | 319 | 306 |
| 2018-05 | 996,511.72 | 66,307.89 | 6.65% | 495 | 443 |
| 2018-06 | 865,102.72 | 12,801.79 | 1.48% | 81 | 71 |
| 2018-07 | 895,512.09 | 36,531.52 | 4.08% | 228 | 208 |
| 2018-08 | 854,685.02 | 52,302.45 | 6.12% | 432 | 393 |

CSV monthly rows store late GMV in `gmv_product` and the within-month late rate in `gmv_share`.

### Methodological note — monthly GMV derivation

Reproducible recipe (SECTION 18 / `olist_full_eda.py`):

1. **Month assignment:** `orders.order_purchase_timestamp` → `pd.to_datetime(...).dt.to_period('M')` (calendar purchase month).
2. **Join:** `items[['order_id', 'price']].merge(orders[['order_id', 'order_purchase_timestamp']], on='order_id', how='left')` — item grain; all items (not delivered-only).
3. **GMV field:** month product GMV = `SUM(price)` over item rows in that purchase month (locked product base; freight excluded).
4. **Rate / rounding:** `late_gmv_rate = late_gmv / month_gmv` on full-precision floats; CSV then stores late GMV as `gmv_product` rounded to **2** decimals and the rate as `gmv_share` rounded to **6** decimals.

The **Month GMV** column in the table above is a **display reconstruction** `round(late_gmv / gmv_share, 2)` from those already-rounded CSV fields. That back-calculation can differ by about **R$1–3** (<0.0003%) from an independent raw-CSV `SUM(price)` by month (e.g. Nov-2017, Feb-2018, Mar-2018). **Late GMV and monthly late-GMV rates are authoritative and match** a direct recomputation; do not treat the display Month GMV cents as a second locked base.

---

## Chart 23

`outputs/charts/23_financial_exposure.png` — two panels:

| Panel | Content |
|-------|---------|
| **(a)** | Monthly product GMV vs late-GMV share of month GMV (Jan-2017–Aug-2018); item grain; locked `is_late` broadcast |
| **(b)** | Late-GMV concentration bars (D1 / top-30 late sellers / top-10 categories ≥100) with **implied commission @19% labeled “assumed”** |

Captions state **scenario + grain + no causality**.

---

## Reconciliation

| Check | Result |
|-------|--------|
| Product GMV vs locked R$13,591,643.70 | **delta = 0.0000** |
| Late-order count | **6,534** (locked order-level `is_late`) |
| Late items vs late orders | **7,264** / **6,534** (broadcast inflation) |
| Take-rate math | `commission_r = gmv_product × r` for r ∈ {0.15, 0.19, 0.21} |
| Top-30 / D1 ID coverage | **30/30** top-30; **310** D1 sellers (Task 3) |
| Customer-paid (context) | R$15,843,553.24 |
| `payment_value` (footnote) | R$16,008,872.12 |

---

## Limits

- Take-rates **15 / 19 / 21%** are **unsourced assumptions**; the true 2016–18 Olist take-rate is **unverified**.
- Figures are **implied commission exposure under an assumption**, not observed commission, not margin, not cash recovered.
- Late GMV uses **order-level** lateness broadcast to items — not an independent item-level lateness measure.
- Concentration cuts reuse Task 3 seller IDs / D1 membership and Task 4 ≥100 category filter; they do **not** prove that sellers or categories “cause” commission loss.
- Descriptive / scenario wording only. **Forbidden** framings (not used here): “fixing lateness saves R$…”, “sellers cause R$… loss”, LTV/CAC as fact, carrier blame, predictive claims, presenting 19–21% as verified.
