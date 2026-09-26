# Internship — HVIA Data & AI Solutions

Olist Brazilian e-commerce business discovery: research, data analysis, and HVIA solution proposal.

## Main file

**`outputs/HVIA_Olist_Business_Discovery_Report.pdf`** (14 pages) — the whole case in one file.

## How to read the PDF (in order)

Read it top to bottom — each section feeds the next: company → data → story → solutions → outreach.

**A. Company Research** — who Olist was during the data window. Start with the Executive Summary box, then Snapshot (A.1), the 2016–2018 aggregator model (A.2), what came later for context only (A.3), the timeline (A.4), and the takeaway on how to use this in B and C (A.5).

**B. Dataset Understanding** — what the data is. Nine tables and row counts (B.1), how they join (B.2: aggregate item → order before revenue/SLA/review joins; retention only via `customer_unique_id`), then quality caveats + the KPI snapshot (B.3).

**C. Analysis & Business Story** — read as one chain: growth stress → geography/freight → late deliveries → review collapse → no repeat, amplified by seller concentration.
- C.1 growth + seasonal pressure → Fig C.1 (Chart 01)
- C.2 distance/freight uneven promise → Figs C.2a–c (Charts 16, 19, 21); the yellow grain box defines the late-counting grains used everywhere
- C.3 late delivery ↔ lower scores (4.29 vs 2.27) → Figs C.3a–c (Charts 06, 18, 20)
- C.4 loyalty + seller elite → Figs C.4a–c (Charts 08, 10, 22)
- C.5 priority spine + the P1–P7 problem register table — the 2-minute summary of the whole story
- C.6 financial exposure → Fig C.6 (Chart 23); read the red banner first: commissions are ASSUMED scenarios (15/19/21%), not losses

**E. Solution Proposal** — every solution starts from a Section C problem ("don't sell a tool"). Read the solution map (E.1), the three cores (E.2 late-risk, E.3 retention flag, E.4 seller health), the supporting layers (E.5), the side alert (E.6), build order (E.7), then the Tasks 2–6 extensions (E.8).

**F. Outreach Draft** (last page) — English message to Head of Operations requesting a 20-minute sense-check.

Short on time? Read only: Executive Summary → C.5 register table → E.1 map → E.7 build order → F.

Words you'll see everywhere: `is_late` = delivered after ETA (`delta_days > 0`, n = 6,534 / 96,470); grain = unit of counting (order / item / seller-pair / customer); broadcast = order late flag copied to its items; D1 = top revenue decile (310 sellers). Claims stay descriptive ("associated", "co-occurs") — nothing here proves causation.

## How to read the repo

Follow the same order as the PDF:

1. `outputs/HVIA_Olist_Business_Discovery_Report.pdf` — read first (above)
2. `docs/definitions.md` — the numbers you can quote (late rule, bases, formulas); single source of truth
3. `docs/` deep dives — one file per analysis: delivery stages, seller risk, category risk, cohorts, financial exposure (+ protection note)
4. `outputs/charts/` + `outputs/tables/` — figures and CSVs behind the report; `outputs/README.md` maps each chart to its report section
5. `notebooks/` — EDA notebook + script (same logic) if you want to reproduce or audit a number
6. `scripts/build_report.py` — builds the PDF from the charts (one script)
7. `archive/` — data dictionary only; raw CSVs download on demand (below)
8. `references/` — upstream Kaggle notebook, attribution only

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
