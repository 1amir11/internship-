# Notebooks — reproducible EDA

| File | Content |
|------|---------|
| `olist_full_eda.py` | Full pipeline, sections 1–18. Generates `../outputs/charts/` + prints business insights; sections 14–18 also write `../outputs/tables/` |
| `olist_eda.ipynb` | Same logic in notebook form (run-all from repo root) |

Both resolve data via `ROOT / 'archive'` (project root = parent of `notebooks/`). Formulas/grains follow `../docs/definitions.md`.

WARNING: sections 14–18 write locked Task 2–6 tables/charts. Before any rerun, read `../docs/locked_outputs_protection.md` and run `python ../scripts/locked_guard.py`.
