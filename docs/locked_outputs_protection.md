# Locked Outputs Protection (Tasks 1–6)

Tasks 1–6 analytical outputs are **LOCKED**. They must never be regenerated or
overwritten by an accidental full-pipeline rerun.

## Locked set (do not overwrite)

Tables (`outputs/tables/`):

- `delivery_decomposition.csv` (Task 2)
- `seller_level.csv`, `seller_decile_summary.csv` (Task 3)
- `category_risk.csv` (Task 4)
- `cohort_monthly.csv`, `cohort_customers.csv` (Task 5)
- `financial_exposure.csv` (Task 6)

Charts (`outputs/charts/`): `01`–`23` PNGs, especially `19`–`23` (Tasks 2–6).

Locked numbers live in `docs/definitions.md` plus `docs/delivery_decomposition.md`,
`docs/seller_risk.md`, `docs/category_risk.md`, `docs/cohort_retention.md`,
`docs/financial_exposure.md`.

## Rule

1. Before any future run of `notebooks/olist_full_eda.py`, back up `outputs/`.
2. Before writing any locked output, check whether the file already exists.
3. If it exists, **do NOT overwrite automatically** — stop and ask a human.
4. Overwrite only with an explicit, deliberate flag (see `scripts/locked_guard.py`
   → `guard_write(path, overwrite=True)`; default is `overwrite=False`).
5. `notebooks/olist_full_eda.py` was intentionally **not modified** in the
   Part 2 pass (its `to_csv`/`savefig` calls remain unconditional) to avoid
   changing Sections 1–18 execution behavior. Until its writes are routed
   through the guard, **do not execute it**.

## Audit

Run `python scripts/locked_guard.py` for a read-only presence check. It writes
nothing to the locked set.
