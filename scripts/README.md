# Scripts

| File | Content |
|------|---------|
| `build_preview_pdf.py` | Builds `../outputs/HVIA_Task1_Olist_Preview_A_B_C_E.pdf` (Task 1 preview A+B+C+E) |
| `build_arabic_pdf.py` | Builds `../outputs/HVIA_Task1_Arabic_Understanding.pdf` (Arabic understanding copy; needs Windows Arial fonts + `arabic-reshaper`, `python-bidi`) |
| `build_task7_final.py` | Builds `../outputs/HVIA_Task7_Final_Business_Discovery_Report.pdf` (final integrated report, Tasks 1–6) |
| `locked_guard.py` | Read-only audit + write guard for locked outputs. Run `python scripts/locked_guard.py` before any EDA rerun |

All paths resolve relative to the repo root (`Path(__file__).resolve().parent.parent`), so any clone location works.
