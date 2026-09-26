# Locked Outputs Protection

Tables in `outputs/tables/` and charts `outputs/charts/01–23` are **LOCKED** analytical results. Do not regenerate or overwrite them with a casual rerun of `notebooks/olist_full_eda.py` (its `to_csv`/`savefig` calls are unconditional).

Rule: before any rerun, back up `outputs/`. Overwrite a locked file only with an explicit, deliberate decision — never automatically.

Locked numbers live in `docs/01-definitions.md` plus `docs/02-delivery-decomposition.md`, `docs/03-seller-risk.md`, `docs/04-category-risk.md`, `docs/05-cohort-retention.md`, `docs/06-financial-exposure.md`.
