# Internship — HVIA Data & AI Solutions

Olist Brazilian e-commerce business discovery: research, data analysis, and HVIA solution proposal.

## Main file (start here)

**`outputs/HVIA_Olist_Business_Discovery_Report.pdf`** (14 pages) — the whole case in one file:

| Section | Content |
|---------|---------|
| A | Company research (Olist model 2016–2018 + later context) |
| B | Dataset understanding (9 tables, joins, quality) |
| C | Analysis & business story (growth, geo, late delivery, loyalty, sellers, exposure) |
| E | HVIA solution proposal (late-risk scoring, seller health, retention flags) |
| F | Outreach draft (English message to Head of Operations) |

## How to read the rest

- **Numbers you can quote:** `docs/definitions.md` — late rule, delivered base (96,470), AOV, freight formulas, retention wording. Every chart follows it.
- **Charts:** `outputs/charts/` (23 PNGs) — the report names the figure for each finding (e.g. `06_delivery_vs_review_scores.png` for the 4.29 → 2.27 review drop).
- **Deep dives:** `docs/` — delivery stages, seller risk, category risk, cohorts, financial exposure.
- **Reproduce (optional):** `notebooks/olist_eda.ipynb` or `notebooks/olist_full_eda.py` after downloading the data (below). Rebuild the PDF with `python scripts/build_report.py`.

## Layout

```
outputs/HVIA_Olist_Business_Discovery_Report.pdf  # <-- main deliverable
docs/          # definitions + analysis notes
notebooks/     # EDA notebook + script (same logic)
scripts/       # report builder (one script)
archive/       # data dictionary only — CSVs download on demand
references/    # upstream Kaggle notebook (attribution)
```

## Data (not in git)

Raw CSVs (~140MB, orders 2016-09-04 → 2018-10-17) are excluded from versioning:

```bash
pip install -r requirements.txt
python -c "import kagglehub; kagglehub.dataset_download('olistbr/brazilian-ecommerce')"
# copy the 9 CSVs into archive/ (file table in archive/README.md)
```

Source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce (CC BY-NC-SA 4.0).

## Key findings

- Late: 6.8% of 96,470 delivered; reviews 4.29 (on-time) vs 2.27 (late)
- Retention: 96.9% buy once (93,099 / 96,096)
- Sellers: top 10% → ~67.5% of R$13.6M product revenue
- Freight: 14.2% of total paid; AOV ~R$138
