# Docs — read in file order (01 → 07)

| File | Content |
|------|---------|
| `01-definitions.md` | Single source of truth — read first. Late rule, delivered base (96,470), AOV, freight formulas, retention wording, revenue base |
| `02-delivery-decomposition.md` | Stage timing (approval / handoff / transit) on the delivered base |
| `03-seller-risk.md` | Seller concentration of risk (deciles, top-30, volume bands) |
| `04-category-risk.md` | Category × risk (late / freight / review co-occurrence) |
| `05-cohort-retention.md` | Fixed-window cohort retention on `customer_unique_id` |
| `06-financial-exposure.md` | Late-GMV exposure as assumed commission scenarios (15/19/21%) |
| `07-locked-outputs-protection.md` | Rule: never overwrite locked tables/charts without explicit approval |

Locked numbers here must match `../outputs/tables/` and `../outputs/charts/19–23`. Wording stays descriptive/correlational — no causal or predictive claims beyond what each file states.
