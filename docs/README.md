# Docs — metric definitions + Tasks 2–6 analysis notes

| File | Content |
|------|---------|
| `definitions.md` | Single source of truth: late rule, delivered base (96,470), AOV, freight formulas, retention wording, revenue base. Read first. |
| `delivery_decomposition.md` | Task 2 — stage timing (approval/handoff/transit) on the delivered base |
| `seller_risk.md` | Task 3 — seller concentration of risk (deciles, top-30, volume bands) |
| `category_risk.md` | Task 4 — category × risk (late/freight/review co-occurrence) |
| `cohort_retention.md` | Task 5 — fixed-window cohort retention on `customer_unique_id` |
| `financial_exposure.md` | Task 6 — late-GMV exposure as assumed commission scenarios (15/19/21%) |
| `locked_outputs_protection.md` | Rule: never overwrite locked tables/charts without explicit approval |

Locked numbers here must match `../outputs/tables/` and `../outputs/charts/19–23`. Wording stays descriptive/correlational — no causal or predictive claims beyond what each file states.
