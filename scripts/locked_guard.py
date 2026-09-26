"""Locked-output guard for HVIA Olist Tasks 1-6 analytical outputs.

Read-only by default. Import or run this module BEFORE any future rerun of
notebooks/olist_full_eda.py so locked files can never be silently overwritten.

Rule: locked files are NEVER overwritten unless overwrite=True is passed
explicitly by a human (deliberate action). The analysis notebook was
intentionally NOT modified to add these guards inline (to avoid changing
Sections 1-18 execution behavior); wire writes through guard_write() if the
pipeline is ever re-enabled.
"""

from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

LOCKED_TABLES = [
    "outputs/tables/delivery_decomposition.csv",
    "outputs/tables/seller_level.csv",
    "outputs/tables/seller_decile_summary.csv",
    "outputs/tables/category_risk.csv",
    "outputs/tables/cohort_monthly.csv",
    "outputs/tables/cohort_customers.csv",
    "outputs/tables/financial_exposure.csv",
]

LOCKED_CHARTS = [f"outputs/charts/{i:02d}_" for i in range(1, 24)]  # prefix match


def locked_files():
    """Return the list of locked table paths that currently exist."""
    return [BASE / p for p in LOCKED_TABLES if (BASE / p).exists()]


def check_locked():
    """Read-only audit: report presence of every locked table."""
    rows = []
    for rel in LOCKED_TABLES:
        p = BASE / rel
        rows.append((rel, p.exists(), p.stat().st_mtime if p.exists() else None))
    return rows


def guard_write(path, overwrite=False):
    """Return True if writing to path is allowed, False if blocked.

    Locked Task 1-6 outputs (outputs/tables/*.csv from the analysis sections
    and outputs/charts/*.png) require overwrite=True explicitly.
    """
    p = Path(str(path))
    name = p.name
    is_locked = (
        (BASE / "outputs" / "tables" in p.parents or "outputs\\tables" in str(p) or "outputs/tables" in str(p))
        and p.suffix == ".csv"
    ) or (
        ("outputs\\charts" in str(p) or "outputs/charts" in str(p))
        and p.suffix == ".png"
    )
    _ = name  # name kept for future per-file allow-list extensions
    if is_locked and p.exists() and not overwrite:
        return False
    return True


if __name__ == "__main__":
    for rel, exists, mtime in check_locked():
        print(f"{'OK ' if exists else 'MISSING'}  {rel}")
