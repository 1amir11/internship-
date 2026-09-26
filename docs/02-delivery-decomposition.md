# Delivery Decomposition (Task 2)

Order-level stage timing on the **locked delivered base** (`docs/01-definitions.md`: `order_status == 'delivered'` + both customer delivery and ETA non-null; **n = 96,470**). Late rule is **not** redefined: `is_late = delivery_delta_days > 0` (primary; calendar-day truncate).

Code: `notebooks/olist_full_eda.py` → **SECTION 14: DELIVERY DECOMPOSITION**; mirrored in `notebooks/olist_eda.ipynb`.  
Table: `outputs/tables/delivery_decomposition.csv` · Chart: `outputs/charts/19_delivery_stage_breakdown.png`.

---

## Stage definitions

| Stage | Symbol | Formula | Units |
|-------|--------|---------|-------|
| Approval | `t_approval_h` | `order_approved_at − order_purchase_timestamp` | hours |
| Handoff (seller→carrier) | `t_handoff_h` | `order_delivered_carrier_date − order_approved_at` | hours |
| Transit (carrier→customer) | `t_transit_d` | `order_delivered_customer_date − order_delivered_carrier_date` | days (hours kept as `t_transit_h`) |
| Total | `t_total_d` | `order_delivered_customer_date − order_purchase_timestamp` | **days** — set equal to existing `actual_delivery_days` (`.dt.days` calendar truncate) |

Locked late fields reused as-is: `delivery_delta` / `delivery_delta_days` and `is_late`.

---

## Bases and denominators

| Base | Rule | n |
|------|------|--:|
| Delivered (locked) | status delivered + customer date + ETA non-null | **96,470** |
| **Full-chain (primary table)** | delivered base **and** `order_approved_at`, `order_delivered_carrier_date` non-null (ETA already required) | **96,455** |
| Stage-wise usable — approval | `order_approved_at` non-null on delivered base | **96,456** |
| Stage-wise usable — handoff | approved + carrier non-null | **96,455** |
| Stage-wise usable — transit | carrier + customer non-null | **96,469** |

Primary decomposition stats and the CSV use the **full-chain** base. Stage-wise n’s are reported separately; any order missing a stage timestamp is excluded from that stage’s usable count only.

---

## Negative-duration data-quality cases

Negatives are **flagged, not silently dropped**. Counts below are vs **full-chain n = 96,455**.

| Flag | Meaning | Count | % of full-chain |
|------|---------|------:|----------------:|
| `t_handoff_h < 0` | Carrier timestamp before approval | **1,350** | **1.40%** |
| `t_transit_d < 0` | Customer delivery before carrier | **23** | **0.024%** |
| `t_approval_h < 0` | Approval before purchase | **0** | 0% |
| `t_total_d < 0` | Delivery before purchase | **0** | 0% |

**Headline median / mean / p90 / SD** are computed on the **≥ 0** subset within full-chain. **Full-sample median** (including negatives) is also reported for transparency. Both n’s appear in the table below and in figure captions.

---

## Stage statistics (full-chain; headline on ≥ 0)

Outlier rule: report median (= p50), p90, mean, SD on unclipped ≥ 0 data. **Do not winsorize.** Plots may clip display ranges only (labeled).

| Stage | Units | n_stage (usable) | n_negative | n (≥0 stats) | Median (≥0) | Full-sample median | Mean (≥0) | p90 (≥0) | SD (≥0) |
|-------|-------|-----------------:|----------:|-------------:|------------:|-------------------:|----------:|---------:|--------:|
| Approval | hours | 96,456 | 0 | 96,455 | **0.34** | 0.34 | 10.28 | 34.60 | 20.54 |
| Handoff | hours | 96,455 | 1,350 | 95,105 | **44.38** | 43.58 | 68.48 | 144.55 | 83.65 |
| Transit | days | 96,469 | 23 | 96,432 | **7.10** | 7.10 | 9.33 | 18.90 | 8.76 |
| Transit (hours) | hours | 96,469 | 23 | 96,432 | **170.40** | 170.39 | 224.00 | 453.65 | 210.22 |
| Total | days | 96,470 | 0 | 96,455 | **10** | 10 | 12.09 | 23 | 9.55 |

**Reconciliation:** `t_total_d` is identical to `actual_delivery_days` on the full-chain set (same `.dt.days` definition). Continuous elapsed days (seconds/86400) have median ≈ 10.22 d on the same orders — calendar truncate vs continuous, not a logic conflict.

Machine-readable copy (units column states hours vs days for median/mean/p90/sd): `outputs/tables/delivery_decomposition.csv`.

---

## Late vs on-time split (correlational)

Full-chain late share ≈ **6.77%** (6,533 / 96,455; one locked late order lacks a full stage chain). Medians on ≥ 0 subset:

| Stage | On-time median | Late median | Late − on-time | Late share in ≥0 stage rows |
|-------|---------------:|------------:|---------------:|----------------------------:|
| Approval (h) | 0.34 | 0.41 | +0.07 h | 6.77% |
| Handoff (h) | 43.02 | 73.60 | **+30.57 h** | 6.84% |
| Transit (d) | 6.95 | 26.20 | **+19.25 d** | 6.77% |
| Total (d) | 9 | 31 | +22 d | 6.77% |

Wording is **descriptive / correlational only**: late orders **show** longer median handoff and especially longer median transit; this does **not** establish that handoff or any named carrier **causes** late outcomes or review drops.

---

## Link to P1 (one paragraph)

Among full-chain stages, **transit** has the largest median duration (~7.1 d) and accounts for most of the median total (~10 calendar days), while **handoff** shows the widest upper-tail spread (p90 ≈ 145 h on the ≥ 0 subset) and a large late-vs-on-time median gap (~+31 h). Late orders also show a much higher transit median (~26 d vs ~7 d on-time). Descriptively, stage-time variation — especially transit length and handoff tail — co-occurs with the locked late flag that underpins **P1** (late delivery ↔ lower reviews); this decomposition does **not** claim which stage causes lateness or review loss, and it does not name or blame carriers.

---

## Figure

`outputs/charts/19_delivery_stage_breakdown.png` — two panels:

- **(a)** Stacked median stage times (approval/handoff converted to days + transit days) vs median total; full-chain **n = 96,455**; stats on ≥ 0 subsets; medians across stages do not sum to median total.
- **(b)** Transit density, late vs on-time overlay; **display clip 0–30 d** (stats unclipped on ≥ 0; **n = 96,432**); negatives flagged (n = 23), not dropped. Caption also notes handoff display convention 0–300 h / approval 0–72 h where those axes appear in companion views.

---

## Limits

- Timestamp quality: ~1.4% of full-chain orders have carrier-before-approval; 23 have delivery-before-carrier — treated as data-quality flags.
- Full-chain drops 15 delivered orders missing approval and/or carrier timestamps (96,470 → 96,455).
- Calendar-day `t_total_d` / `actual_delivery_days` vs continuous hours/days: same interval, different grain; stack of stage medians ≠ median total.
- No causal attribution to sellers, carriers, or interventions; review links remain correlational and out of scope for causal claims here.
