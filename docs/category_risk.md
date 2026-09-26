# Category × Risk Analysis (Task 4)

Category-level late delivery, freight burden, and review co-occurrence on the **locked** bases (`docs/definitions.md`). Late rule is **not** redefined: `is_late = delivery_delta_days > 0` on the delivered base (**n = 96,470**; **6,534** late orders). Revenue ranking uses **`SUM(order_items.price)`** (product GMV = **R$13,591,643.70**). Freight item ratio uses locked mean-item denominator: **`MEAN(freight / (price + freight))`**.

Code: `notebooks/olist_full_eda.py` → **SECTION 16: CATEGORY × RISK** (lines **1337–1755**); mirrored in `notebooks/olist_eda.ipynb` (**cells 36–37**, after SECTION 15 cells 34–35).  
Table: `outputs/tables/category_risk.csv` · Chart: `outputs/charts/21_category_risk.png`.

---

## Methods and grains

| Object | Grain | Definition |
|--------|-------|------------|
| Category join | Item | `order_items` → **inner** `orders_delivered` (`order_id`, locked `is_late`, `delivery_delta`, `actual_delivery_days`) → left `products[product_id, product_category_name, product_weight_g]` → left `product_category_name_translation` → `product_category_name_english` |
| `is_late` / review | Item (broadcast) | Each item inherits its order’s locked `is_late` and deduped `review_score` (`reviews[['order_id','review_score']].drop_duplicates('order_id')`) |
| `n_items`, `n_orders` | Delivered item / distinct delivered `order_id` | Primary risk denominators |
| `late_items`, `late_rate_items` | Delivered item | `late_items / n_items` within category (items in delivered orders) |
| `avg_review_items`, `reviewed_items_n` | Delivered item | Mean score on reviewed items only |
| `revenue_sum`, `freight_sum`, `mean_freight_ratio`, `avg_weight_g` | **All items** (same category label) | Locked revenue base / chart-03 & chart-13 alignment; `mean_freight_ratio = MEAN(freight/(price+freight))` |
| `single_cat_orders`, `single_cat_late_rate` | Order | Delivered orders with exactly one category; late rate at **order** grain |

**Do not** treat item-grain late rates and order-grain single-category rates as interchangeable — both are reported; captions state which.

---

## Missing category & translation handling

| Issue | Distinct count | Affected items | Affected orders | Affected revenue (`SUM(price)`) |
|-------|---------------:|---------------:|----------------:|--------------------------------:|
| Null `product_category_name` on products | **610** (1.9% of 32,951) | **1,603** | **1,451** | **R$179,535.28** |
| PT category with no English mapping | **2** (`pc_gamer`, `portateis_cozinha_e_preparadores_de_alimentos`) | **24** | **22** | **R$5,514.48** |

Both are bucketed as **`Unknown / untranslated`** (pooled). That bucket is **quantified and kept in totals reconciliation**, but **excluded from ranked headlines**.

| Unknown / untranslated (pooled) | Value |
|---------------------------------|------:|
| Delivered items / orders | 1,559 / 1,412 |
| Revenue (all-items) | R$185,049.76 |
| Item late rate | 7.44% |

---

## Thresholds and coverage

| Rule | Use |
|------|-----|
| **`n_orders` (delivered, distinct) ≥ 100** | Headline ranked tables & chart-21 |
| **`≥ 50`** | Sensitivity appendix (matches chart-13 cutoff) |
| **Below threshold** | “Other / thin” aggregate only — never ranked individually |
| **Unknown / untranslated** | Totals only — never ranked |

### Headline coverage (`≥ 100`, named categories only)

| Metric | Value |
|--------|------:|
| Named categories ≥100 | **51 / 71** (**71.8%** of named) |
| % delivered items retained | **97.77%** |
| % category–order-sum share | **97.71%** |
| % platform revenue retained | **97.63%** |

### Other / thin aggregate (`n_orders < 100`, excl. Unknown)

| Metric | Value |
|--------|------:|
| n categories | **20** |
| Delivered items / order-sum | 902 / 817 |
| Revenue | R$137,180.35 |
| Pooled item late rate | **5.43%** |

---

## Reconciliation

| Check | Result |
|-------|--------|
| Category `SUM(price)` vs locked platform | **13,591,643.70 − 13,591,643.70 = delta 0.0000** |
| Late items (broadcast) vs locked late orders | **7,264** item flags vs **6,534** late orders (ratio ≈ **1.112**) — inflation from **multi-item** late orders inheriting the same order-level `is_late` |
| Reviewed items vs reviewed delivered orders | **109,362** reviewed items vs **95,824** reviewed delivered orders — same broadcast pattern (~1.14 items/order) |

---

## Top-15 by revenue (`≥ 100` delivered orders)

Grain note: **revenue** = all-items `SUM(price)`; **late rate** = delivered **item** grain. Every row shows `n_items` + `n_orders`.

Cross-check vs chart-03 leaders: **15/15 exact name-set match**.

| Rank | Category | Revenue (R$) | Rev share | n_items | n_orders | Late rate (items) |
|-----:|----------|-------------:|----------:|--------:|---------:|------------------:|
| 1 | health_beauty | 1,258,681.34 | 9.26% | 9,465 | 8,647 | 7.56% |
| 2 | watches_gifts | 1,205,005.68 | 8.87% | 5,857 | 5,493 | 7.21% |
| 3 | bed_bath_table | 1,036,988.68 | 7.63% | 10,953 | 9,272 | 7.03% |
| 4 | sports_leisure | 988,048.97 | 7.27% | 8,430 | 7,529 | 6.31% |
| 5 | computers_accessories | 911,954.32 | 6.71% | 7,643 | 6,529 | 6.49% |
| 6 | furniture_decor | 729,762.49 | 5.37% | 8,160 | 6,307 | 7.03% |
| 7 | cool_stuff | 635,290.85 | 4.67% | 3,718 | 3,559 | 5.84% |
| 8 | housewares | 632,248.66 | 4.65% | 6,795 | 5,743 | 5.00% |
| 9 | auto | 592,720.11 | 4.36% | 4,139 | 3,809 | 7.03% |
| 10 | garden_tools | 485,256.46 | 3.57% | 4,268 | 3,448 | 6.56% |
| 11 | toys | 483,946.60 | 3.56% | 4,029 | 3,803 | 6.35% |
| 12 | baby | 411,764.89 | 3.03% | 2,982 | 2,809 | 7.68% |
| 13 | perfumery | 399,124.87 | 2.94% | 3,340 | 3,086 | 6.50% |
| 14 | telephony | 323,667.53 | 2.38% | 4,430 | 4,093 | 6.95% |
| 15 | office_furniture | 273,960.70 | 2.02% | 1,668 | 1,254 | 7.97% |

---

## Top-15 by late rate (`≥ 100`; item grain)

| Rank | Category | Late rate | n_items | n_orders | Avg review (reviewed items) | Reviewed n |
|-----:|----------|----------:|--------:|---------:|----------------------------:|-----------:|
| 1 | audio | **11.60%** | 362 | 348 | 3.84 | 358 |
| 2 | christmas_supplies | 10.00% | 150 | 125 | 4.07 | 143 |
| 3 | fashion_underwear_beach | 9.45% | 127 | 117 | 4.05 | 126 |
| 4 | home_confort | 9.32% | 429 | 392 | 3.86 | 427 |
| 5 | books_technical | 7.98% | 263 | 256 | 4.39 | 262 |
| 6 | office_furniture | 7.97% | 1,668 | 1,254 | 3.52 | 1,654 |
| 7 | baby | 7.68% | 2,982 | 2,809 | 4.08 | 2,959 |
| 8 | electronics | 7.59% | 2,729 | 2,517 | 4.07 | 2,710 |
| 9 | health_beauty | 7.56% | 9,465 | 8,647 | 4.19 | 9,402 |
| 10 | musical_instruments | 7.37% | 651 | 611 | 4.22 | 645 |
| 11 | construction_tools_lights | 7.31% | 301 | 242 | 4.08 | 292 |
| 12 | watches_gifts | 7.21% | 5,857 | 5,493 | 4.07 | 5,813 |
| 13 | furniture_living_room | 7.07% | 495 | 414 | 3.93 | 490 |
| 14 | furniture_decor | 7.03% | 8,160 | 6,307 | 3.96 | 8,080 |
| 15 | auto | 7.03% | 4,139 | 3,809 | 4.12 | 4,098 |

Descriptive read: category **audio** shows **11.60%** late (**n = 362 items / 348 orders**), above the platform order-level late rate (6.77%). High-revenue categories such as health_beauty and watches_gifts also sit slightly above that order-level benchmark on the **item** grain.

---

## Top-15 by mean freight ratio (`≥ 100`)

Denominator label: **mean-item** `MEAN(freight / (price + freight))` (locked FREIGHT_MEAN_ITEM family; not the primary platform 14.21% sum formula).

| Rank | Category | Mean freight ratio | n_items | n_orders |
|-----:|----------|-------------------:|--------:|---------:|
| 1 | electronics | **35.81%** | 2,729 | 2,517 |
| 2 | christmas_supplies | 33.80% | 150 | 125 |
| 3 | food_drink | 30.36% | 269 | 221 |
| 4 | telephony | 30.00% | 4,430 | 4,093 |
| 5 | signaling_and_security | 28.50% | 197 | 138 |
| 6 | drinks | 26.91% | 361 | 287 |
| 7 | costruction_tools_garden | 26.77% | 232 | 190 |
| 8 | home_appliances | 25.27% | 754 | 747 |
| 9 | housewares | 25.16% | 6,795 | 5,743 |
| 10 | fashion_underwear_beach | 24.30% | 127 | 117 |
| 11 | kitchen_dining_laundry_garden_furniture | 24.30% | 274 | 241 |
| 12 | food | 23.81% | 499 | 441 |
| 13 | books_general_interest | 23.77% | 536 | 495 |
| 14 | books_technical | 23.61% | 263 | 256 |
| 15 | furniture_decor | 23.27% | 8,160 | 6,307 |

### Freight cross-check (`dvds_blu_ray`)

Prior chart-13 leader **`dvds_blu_ray`** still shows mean-item freight ratio **40.37%**, matching the ~40% prior label under the same `MEAN(freight/(price+freight))` denominator. Delivered **n_orders = 56** → **below the ≥100 headline filter**; it remains the top freight category under the **≥50** sensitivity cutoff (same as chart-13).

---

## Order-grain sensitivity (top-15 revenue; single-category delivered orders)

| Category | Single-cat orders | Single-cat late rate | Item late rate |
|----------|------------------:|---------------------:|---------------:|
| health_beauty | 8,576 | 7.56% | 7.56% |
| watches_gifts | 5,453 | 7.45% | 7.21% |
| bed_bath_table | 9,069 | 7.54% | 7.03% |
| sports_leisure | 7,457 | 6.61% | 6.31% |
| computers_accessories | 6,478 | 6.44% | 6.49% |
| furniture_decor | 6,103 | 7.31% | 7.03% |
| cool_stuff | 3,492 | 5.96% | 5.84% |
| housewares | 5,627 | 5.46% | 5.00% |
| auto | 3,773 | 7.37% | 7.03% |
| garden_tools | 3,377 | 6.66% | 6.56% |
| toys | 3,752 | 6.42% | 6.35% |
| baby | 2,716 | 8.25% | 7.68% |
| perfumery | 3,059 | 6.60% | 6.50% |
| telephony | 4,066 | 7.16% | 6.95% |
| office_furniture | 1,239 | 8.15% | 7.97% |

---

## Scatter correlations (descriptive only)

Among named categories with **`n_orders ≥ 100`** (**n = 51**):

| Pair | Pearson r | Framing |
|------|----------:|---------|
| Mean freight ratio vs late rate (items) | **0.120** | Descriptive co-occurrence only |
| Mean freight ratio vs avg review (items) | **0.030** | Descriptive co-occurrence only |

No causal test; high-freight categories **co-occur** weakly with higher item late rates in this cross-section.

---

## Link to P1 (one paragraph)

P1 is the locked association between late delivery and lower reviews at **order** grain. At **category** grain, late flags are **broadcast** to items (7,264 late items vs 6,534 late orders), so category late rates describe assortment co-occurrence with the same locked `is_late`, not a new late definition. Some categories show elevated item late rates (e.g. audio at 11.60%, n=362/348) and high mean-item freight ratios (electronics 35.81% at ≥100; `dvds_blu_ray` 40.37% at n_orders=56). Freight ratio and late rate **co-occur** only weakly (r≈0.12). This section does **not** claim that category causes lateness or review loss, does not prescribe delisting, and does not blame carriers.

---

## Figure

`outputs/charts/21_category_risk.png` — two panels:

- **(a)** Top-15 revenue categories: revenue bars (all-items `SUM(price)`) + late-rate dots (delivered **item** grain); dual axis; **n_orders** labeled; filter **`≥ 100`**; Unknown excluded.
- **(b)** Mean freight ratio vs late rate scatter; bubble size = `n_orders`; **`≥ 100`** named categories; extremes labeled; trend / Pearson **r = 0.120** noted as **descriptive only — no causality**.

Captions state item grain, threshold, n’s, and no causality.

---

## Limits / caveats

- **Item vs order grain:** late item counts exceed order-level late (**6,534**) when multi-item orders are late; do not equate the two rates.
- **Revenue vs risk grain:** `revenue_sum` uses **all items** (platform reconcile / chart-03); late/review use **delivered** items.
- **Unknown / untranslated** is excluded from ranks but included in revenue totals.
- **Thin categories (<100 orders)** are pooled, not ranked — small-n late rates are noisy.
- **`dvds_blu_ray` ~40% freight** is real under mean-item labeling but fails the ≥100 headline filter.
- **Pearson r** is descriptive only; not a causal or predictive claim.
- Wording stays correlational: categories **account for** revenue shares and **show** late/freight rates; no assortment prescriptions stated as proven.
- Tasks 1–3 outputs and `docs/definitions.md` remain locked and unchanged in substance.
