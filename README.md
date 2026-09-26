# Internship — HVIA Data & AI Solutions

Main repository for internship work. Started with the Olist Brazilian e-commerce business-discovery case (Tasks 1–7). Future internship tasks go under `tasks/` following the same convention.

Remote: https://github.com/1amir11/internship-.git

## Tasks

| Task | Folder | Status |
|------|--------|--------|
| Task 01 — Olist business discovery (research + EDA + story + HVIA solutions) | `tasks/task-01-olist-business-discovery/` | Done (sections A–C, E; F/H TODO) |
| Tasks 02–06 — Delivery, seller, category, cohort, financial exposure (locked analysis) | `docs/` + `outputs/` | Done, locked |
| Task 07 — Final integrated business discovery report | `outputs/HVIA_Task7_Final_Business_Discovery_Report.pdf` | Done |
| Next tasks | `tasks/task-NN-<slug>/` | Template below |

`tasks/task-01-olist-business-discovery/hvia_task1_submission.md` is the Task 1 entry point.

## Repository layout

```
archive/        # 9 raw Olist CSVs (see archive/README.md)
docs/           # Locked metric definitions + Tasks 2–6 analysis notes
tasks/          # One folder per internship task (handwritten deliverables)
notebooks/      # Reproducible EDA (notebook + script, same logic)
scripts/        # PDF builders + locked-output guard
outputs/        # Charts (01–23), tables, final PDFs (locked)
references/     # Upstream Kaggle notebook (attribution only)
```

## Quickstart

```bash
pip install -r requirements.txt

# Full EDA (WARNING: locked outputs — read docs/locked_outputs_protection.md first)
python scripts/locked_guard.py
jupyter notebook notebooks/olist_eda.ipynb
# or
python notebooks/olist_full_eda.py

# Rebuild PDFs
python scripts/build_preview_pdf.py
python scripts/build_arabic_pdf.py
python scripts/build_task7_final.py
```

Paths in `notebooks/` and `scripts/` resolve relative to the repo root, so any clone location works.

## Data

Source: Olist Brazilian E-Commerce public dataset (Kaggle: `olistbr/brazilian-ecommerce`), orders ~2016-09-04 → 2018-10-17. Details and table dictionary in `archive/README.md`. Upstream notebook preserved for attribution in `references/upstream-brazilian-ecommerce-analysis/`.

## Locked outputs (do not regenerate casually)

Tasks 1–6 tables in `outputs/tables/` and charts `outputs/charts/01–23` are locked. Metric grain/denominators live in `docs/definitions.md` (single source of truth). Before any rerun: back up `outputs/`, run `python scripts/locked_guard.py`, and never overwrite locked files without explicit approval. Full rule: `docs/locked_outputs_protection.md`.

## Key numbers (locked)

- Late: 6.8% of 96,470 delivered (`delivery_delta_days > 0`); reviews on-time/late 4.29 / 2.27
- Retention: 96.9% crude full-window one-time rate (93,099 / 96,096 `customer_unique_id`)
- Revenue: R$13.6M `SUM(price)`; top 10% sellers → ~67.5%
- Freight: 14.2% of total paid (primary); ~17% of product; mean item ratio 21.3%
- AOV: ~R$138 per-order mean of Σprice

## Adding a new task

```
tasks/task-NN-<slug>/
  README.md        # objective, inputs, outputs, status
  <deliverables>.md
```

Use zero-padded numbers (`task-02-...`), keep raw data in `archive/` or a task-local `data/` with a README, write reproducible code in `notebooks/` or `scripts/`, and put final artifacts in `outputs/` (prefix with task number if needed).
