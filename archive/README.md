# Raw data — Olist Brazilian E-Commerce (9 tables)

Source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce (public release, 2018).
Window in this extract: orders ~2016-09-04 → 2018-10-17. See `../docs/01-definitions.md` for window/truncation notes.

Recoverable: if `archive/` is empty, run `python -c "import kagglehub; kagglehub.dataset_download('olistbr/brazilian-ecommerce')"` and copy the 9 CSVs here (requires `pip install kagglehub`).

## Files

| File | Rows (approx) | Role |
|------|---------------|------|
| `olist_orders_dataset.csv` | 99,441 | Hub — status + purchase/approval/carrier/delivery/ETA timestamps |
| `olist_order_items_dataset.csv` | 112,650 | Line items — product, seller, price, freight |
| `olist_customers_dataset.csv` | 99,441 | Customer location; `customer_unique_id` = true person (96,096) |
| `olist_sellers_dataset.csv` | 3,095 | Seller location |
| `olist_products_dataset.csv` | 32,951 | Category, photos, weight/dimensions |
| `olist_order_payments_dataset.csv` | 103,886 | Payment type, installments, value |
| `olist_order_reviews_dataset.csv` | 99,224 | Score 1–5 + optional text |
| `olist_geolocation_dataset.csv` | 1,000,163 | ZIP → lat/lng (many rows per prefix; average before distance) |
| `product_category_name_translation.csv` | 71 | PT → EN category names |

Primary consumer: `../notebooks/olist_full_eda.py` (`DATA_PATH = ROOT / 'archive'`). Do not rename files without updating the notebook and `../docs/01-definitions.md`.

Dataset license: CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/).
