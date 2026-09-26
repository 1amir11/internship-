# Outputs

| Path | Content |
|------|---------|
| `HVIA_Olist_Business_Discovery_Report.pdf` | **Main deliverable** — final integrated report (A–C, E–F). Rebuild: `python scripts/build_report.py`. Reading guide in root `README.md` |
| `charts/` | 23 PNGs backing the report (map to report figures below) |
| `tables/` | 7 CSVs from the analysis (delivery, seller, category, cohort, exposure) |

## Chart → report figure map

| Chart | Report figure | Section |
|-------|---------------|---------|
| 01 monthly volume | Fig C.1 | C.1 growth |
| 16 distance vs delivery | Fig C.2a | C.2 geo/freight |
| 19 stage breakdown | Fig C.2b | C.2 stages |
| 21 category risk | Fig C.2c | C.2 categories |
| 06 delivery vs reviews | Fig C.3a | C.3 late ↔ scores |
| 18 review text signals | Fig C.3b | C.3 written complaints |
| 20 seller risk | Fig C.3c | C.3 concentration |
| 08 retention crisis | Fig C.4a | C.4 loyalty |
| 10 seller pareto | Fig C.4b | C.4 sellers |
| 22 cohort retention | Fig C.4c | C.4 cohorts |
| 23 financial exposure | Fig C.6 | C.6 late GMV |
| 02–05, 07, 09, 11–15, 17 | supporting Task-1 story charts, kept for completeness |

Locked: do not regenerate tables/charts casually — see `../docs/locked_outputs_protection.md`. Definitions: `../docs/definitions.md`.
