# Review Brief — what this repo is and what was done
*(Written for an AI/human reviewer. Author: Amir, intern @ HVIA – Data & AI Solutions.)*

## 1. Context

This repo is my internship workspace. Its first (and so far only) case is a **business-discovery task on Olist**, a Brazilian retail-tech company, using Olist's public 2016–2018 store-order extract (~99k orders). The brief's guiding principle: *"Don't sell a tool. Find a problem worth solving."* — i.e. every proposed solution must start from a problem found in the data, not from a pre-chosen technique.

Time frame in the data (2016-09-04 → 2018-10-17) reflects Olist's **marketplace-aggregator model** (sellers listed under one shared Olist storefront, ~19–21% commission). Later SaaS/fintech evolution is context only.

## 2. Tasks and where each lives

| Task | Objective | Output (path) | Status |
|------|-----------|---------------|--------|
| 1A — Company research | Who Olist is, model then vs now | Report §A + `docs/` background | Done |
| 1B — Dataset understanding | 9 tables, joins, quality, KPIs | Report §B | Done |
| 1C — Analysis & business story | Problems P1–P7 as one causal-style chain (kept correlational) | Report §C + Figs C.1–C.6 | Done |
| 1E — HVIA solution proposal | 3 core + supporting + side solutions mapped to P1–P7 | Report §E | Done |
| 1F — Outreach draft | Short email to Head of Operations, signed Amir | Report §F (last page) | Done |
| 2 — Delivery decomposition | Stage timing (approval/handoff/transit) | `docs/02-delivery-decomposition.md` + `outputs/tables/delivery_decomposition.csv` + Chart 19 | Done, locked |
| 3 — Seller risk | Revenue concentration + late concentration (D1, top-30) | `docs/03-seller-risk.md` + `seller_level.csv`, `seller_decile_summary.csv` + Chart 20 | Done, locked |
| 4 — Category risk | Late/freight/review by category (≥100-order filter) | `docs/04-category-risk.md` + `category_risk.csv` + Chart 21 | Done, locked |
| 5 — Cohort retention | Fixed-window 12m repeat vs crude rate | `docs/05-cohort-retention.md` + `cohort_monthly.csv`, `cohort_customers.csv` + Chart 22 | Done, locked |
| 6 — Financial exposure | Late-GMV sizing under ASSUMED take-rates (scenarios, not losses) | `docs/06-financial-exposure.md` + `financial_exposure.csv` + Chart 23 | Done, locked |
| 7 — Final report | Integrated A–C, E–F, 13 pages | `outputs/HVIA_Olist_Business_Discovery_Report.pdf` | Done (main deliverable) |

Dropped by owner decision: LinkedIn milestone post (no LinkedIn account). Its section was removed from the report.

## 3. Locked facts (verify everything against these)

From `docs/01-definitions.md` (single source of truth):

- Late = `delivery_delta_days > 0` on delivered base **96,470** → **6,534** late (**6.8%**); reviews on-time/late **4.29 / 2.27**
- Retention: **93,099 / 96,096 = 96.88%** one-time (`customer_unique_id`, full window); H1-2017 12m repeat **666/14,239 = 4.68%**
- Revenue: `SUM(price)` = **R$13,591,643.70**; top 10% sellers → **~67.5%**
- Freight primary **14.21%** of total paid; secondary ~17% of product; mean item ratio ~21.3%
- AOV **R$137.75** (per-order mean of Σprice)
- Wording rule: descriptive/correlational only ("associated", "co-occurs"); commission figures are ASSUMED scenarios

## 4. Data

Source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce (CC BY-NC-SA 4.0). 9 CSVs (~140MB) are **not versioned**; `archive/README.md` has the file table and this recovery command:

```bash
pip install -r requirements.txt
python -c "import kagglehub; kagglehub.dataset_download('olistbr/brazilian-ecommerce')"
```

Code: `notebooks/olist_eda.ipynb` + `notebooks/olist_full_eda.py` (same logic, sections 1–18).

## 5. Repo map

```
outputs/HVIA_Olist_Business_Discovery_Report.pdf  # main deliverable (13pp, 11 figures)
docs/01-definitions.md .. 07-*.md                 # analysis notes in reading order
notebooks/                                        # reproducible EDA
outputs/charts/ (23) + outputs/tables/ (7)        # locked artifacts
archive/README.md                                 # data dictionary (CSVs on demand)
references/                                       # upstream Kaggle notebook (attribution)
```

Deliberately removed (all in git history if needed): `tasks/` working notes, extra PDF builders/preview PDFs, `scripts/` (report builder last at `e53da8c:scripts/build_report.py`), raw CSVs. No analysis number was ever altered — check `git log`.

## 6. Reviewer verification checklist

1. `docs/01-definitions.md` values == §3 table above
2. CSV row counts after download: orders 99,441; items 112,650; customers 99,441
3. PDF: 13 pages, 11 embedded figures, sections A–C/E–F, outreach opening "Hi there" and signed "Amir", no bracket placeholders, TODOs, or LinkedIn section
4. `outputs/charts/01–23` + `outputs/tables/` (7 files) present; chart→section map in `outputs/README.md`
5. No stale references in code, docs, charts, or READMEs (retired names are documented only in §5 of this brief for recoverability)
6. `notebooks/olist_eda.ipynb` is valid JSON; `notebooks/olist_full_eda.py` compiles; both resolve data via repo-relative `archive/` path
