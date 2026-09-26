# Locked Outputs Protection

Tables in `outputs/tables/` and charts `outputs/charts/01–23` are **LOCKED** analytical results. Do not regenerate or overwrite them with a casual rerun of `notebooks/olist_full_eda.py` (its `to_csv`/`savefig` calls are unconditional).

Rule: before any rerun, back up `outputs/`. Overwrite a locked file only with an explicit, deliberate decision — never automatically.

Locked numbers live in `docs/definitions.md` plus `docs/delivery_decomposition.md`, `docs/seller_risk.md`, `docs/category_risk.md`, `docs/cohort_retention.md`, `docs/financial_exposure.md`.
