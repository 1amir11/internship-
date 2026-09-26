# Internship — HVIA Data & AI Solutions

Main repo for internship work. First case: Olist Brazilian e-commerce business discovery (Tasks 1–7).

## How to read this repo (start here)

1. **Report first:** open `outputs/HVIA_Task7_Final_Business_Discovery_Report.pdf` (14 pages) — sections A (company), B (dataset), C (story), E (HVIA solutions), F (outreach draft to Head of Operations). This is the whole case in one file.
2. **Details:** `tasks/task-01-olist-business-discovery/hvia_task1_submission.md` — entry point with the same sections plus links to every artifact.
3. **Numbers you can quote:** `docs/definitions.md` — late rule, delivered base (96,470), AOV, freight formulas, retention wording. Every chart/table follows it.
4. **Charts:** `outputs/charts/` (23 PNGs) — the PDF tells you which figure to open for each finding (e.g. `06_delivery_vs_review_scores.png` for the 4.29 → 2.27 review drop).
5. **Reproduce (optional):** `notebooks/olist_eda.ipynb` or `notebooks/olist_full_eda.py` after downloading the data (one command below).

## Layout (only what's needed)

```
outputs/HVIA_Task7_Final_Business_Discovery_Report.pdf  # final report (read this)
tasks/task-01-olist-business-discovery/  # submission + research + solutions
docs/          # metric definitions + Tasks 2–6 deep dives
notebooks/     # EDA notebook + script (same logic)
scripts/       # PDF builders + locked-output guard
archive/       # data dictionary only — CSVs download on demand (see below)
references/    # upstream Kaggle notebook (attribution)
```

## Data (not in git)

Raw CSVs (~140MB, 9 tables, orders 2016-09-04 → 2018-10-17) are excluded from versioning. To reproduce:

```bash
pip install -r requirements.txt
python -c "import kagglehub; kagglehub.dataset_download('olistbr/brazilian-ecommerce')"
# copy the 9 CSVs into archive/ (see archive/README.md for the file table)
python scripts/locked_guard.py   # audit locked outputs before any rerun
```

Source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce (CC BY-NC-SA 4.0).

## Key findings (locked)

- Late: 6.8% of 96,470 delivered; reviews 4.29 (on-time) vs 2.27 (late)
- Retention: 96.9% buy once (93,099 / 96,096)
- Sellers: top 10% → ~67.5% of R$13.6M product revenue
- Freight: 14.2% of total paid; AOV ~R$138

## New tasks

```
tasks/task-NN-<slug>/README.md  # objective, inputs, outputs, status
```
