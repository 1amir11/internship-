"""
HVIA Task 7 - Final Integrated Business Discovery PDF (A + B + C + E).
Implements Part A decisions exactly. Reuses Doc helpers from preview builder.
"""
from pathlib import Path

from fpdf import FPDF, XPos, YPos

OUT = Path(__file__).resolve().parent.parent / "outputs" / "HVIA_Task7_Final_Business_Discovery_Report.pdf"
CHARTS = Path(__file__).resolve().parent.parent / "outputs" / "charts"
OUT.parent.mkdir(parents=True, exist_ok=True)


class Doc(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(110, 110, 110)
        self.cell(
            0,
            5,
            "HVIA | Olist Business Discovery | Final - Integrated Tasks 1-6",
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )
        self.set_draw_color(200, 200, 200)
        self.line(self.l_margin, 10, self.w - self.r_margin, 10)
        self.ln(2)

    def footer(self):
        self.set_y(-11)
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(120, 120, 120)
        self.cell(0, 7, f"{self.page_no()}/{{nb}}", align="C")

    def h1(self, text):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(20, 40, 70)
        self.multi_cell(0, 6.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def h2(self, text):
        self.ln(1.2)
        self.set_font("Helvetica", "B", 10.5)
        self.set_text_color(30, 60, 100)
        self.multi_cell(0, 5.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(0.4)

    def body(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(35, 35, 35)
        self.multi_cell(0, 4.6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(0.5)

    def bullet(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(35, 35, 35)
        self.cell(4, 4.6, "-")
        self.multi_cell(0, 4.6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def step(self, n, title, text):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(30, 60, 100)
        self.multi_cell(
            0, 4.8, f"Step {n}  |  {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )
        self.set_font("Helvetica", "", 9)
        self.set_text_color(35, 35, 35)
        self.multi_cell(0, 4.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(0.8)

    def timeline_row(self, when, what):
        w_when, w_what = 34, self.epw - 34
        h = 4.5
        lines = self.multi_cell(w_what - 3, h, what, dry_run=True, output="LINES")
        max_h = max(h + 1, len(lines) * h + 2)
        if self.get_y() + max_h > self.page_break_trigger:
            self.add_page()
        y0 = self.get_y()
        x0 = self.l_margin
        self.set_fill_color(30, 60, 100)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 8.5)
        self.set_xy(x0, y0)
        self.cell(w_when - 2, max_h, f"  {when}", fill=True)
        self.set_fill_color(248, 249, 251)
        self.set_text_color(35, 35, 35)
        self.set_font("Helvetica", "", 8.5)
        self.set_xy(x0 + w_when, y0)
        self.rect(x0 + w_when, y0, w_what, max_h, style="F")
        self.set_xy(x0 + w_when + 1.5, y0 + 1)
        self.multi_cell(w_what - 3, h, what, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_y(y0 + max_h + 1.5)

    def figure(self, filename, caption, width=150):
        path = CHARTS / filename
        if not path.exists():
            self.body(f"[Missing: {filename}]")
            return
        need = width * 0.52 + 10
        if self.get_y() + need > self.page_break_trigger:
            self.add_page()
        x = self.l_margin + (self.epw - width) / 2
        self.image(str(path), x=x, w=width)
        self.ln(0.5)
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(80, 80, 80)
        self.multi_cell(
            0, 3.8, caption, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )
        self.ln(1.5)

    def figures_pair(self, left, right, cap_left, cap_right, width=88):
        p1, p2 = CHARTS / left, CHARTS / right
        if not p1.exists() or not p2.exists():
            if p1.exists():
                self.figure(left, cap_left)
            else:
                self.body(f"[Missing: {left}]")
            if p2.exists():
                self.figure(right, cap_right)
            else:
                self.body(f"[Missing: {right}]")
            return
        need = width * 0.55 + 16
        if self.get_y() + need > self.page_break_trigger:
            self.add_page()
        y0 = self.get_y()
        gap = max(4, self.epw - 2 * width)
        x1 = self.l_margin
        x2 = self.l_margin + width + gap
        self.image(str(p1), x=x1, y=y0, w=width)
        self.image(str(p2), x=x2, y=y0, w=width)
        img_h = width * 0.52
        self.set_y(y0 + img_h + 1)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(80, 80, 80)
        y_cap = self.get_y()
        self.set_xy(x1, y_cap)
        self.multi_cell(width, 3.5, cap_left, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        y_after_left = self.get_y()
        self.set_xy(x2, y_cap)
        self.multi_cell(
            width, 3.5, cap_right, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )
        self.set_y(max(y_after_left, self.get_y()) + 2)

    def kv_compact(self, rows, col_widths=None):
        if col_widths is None:
            col_widths = [48, self.epw - 48]
        for i, row in enumerate(rows):
            h = 4.2
            max_h = h
            for j, cell in enumerate(row):
                lines = self.multi_cell(
                    col_widths[j], h, str(cell), dry_run=True, output="LINES"
                )
                max_h = max(max_h, len(lines) * h)
            if self.get_y() + max_h > self.page_break_trigger:
                self.add_page()
            y0, x0 = self.get_y(), self.l_margin
            for j, cell in enumerate(row):
                if i == 0:
                    self.set_fill_color(30, 60, 100)
                    self.set_text_color(255, 255, 255)
                    self.set_font("Helvetica", "B", 7.5)
                else:
                    fill = (246, 248, 250) if i % 2 == 0 else (255, 255, 255)
                    self.set_fill_color(*fill)
                    self.set_text_color(35, 35, 35)
                    self.set_font("Helvetica", "B" if j == 0 else "", 7.5)
                self.set_xy(x0 + sum(col_widths[:j]), y0)
                self.rect(
                    x0 + sum(col_widths[:j]), y0, col_widths[j], max_h, style="FD"
                )
                self.set_xy(x0 + sum(col_widths[:j]) + 1, y0 + 0.3)
                self.multi_cell(
                    col_widths[j] - 2, h, str(cell), new_x=XPos.RIGHT, new_y=YPos.TOP
                )
            self.set_xy(x0, y0 + max_h)
        self.ln(2)

    def grain_box(self):
        """Late-grain reconciliation - defined once in C.2; later pages reference it."""
        text = (
            "LATE GRAINS (same locked is_late = delivery delta_days > 0): "
            "order 6,534 / 96,470  |  item-broadcast 7,264 (x1.112)  |  "
            "seller-pair 6,547 (97,811 pairs; 1,278 multi-seller orders with items, "
            "of which 1,275 delivered).  "
            "Different grains, not an error."
        )
        h = 4.0
        lines = self.multi_cell(self.epw - 4, h, text, dry_run=True, output="LINES")
        max_h = len(lines) * h + 3
        if self.get_y() + max_h > self.page_break_trigger:
            self.add_page()
        y0, x0 = self.get_y(), self.l_margin
        self.set_fill_color(255, 248, 230)
        self.set_draw_color(200, 160, 60)
        self.rect(x0, y0, self.epw, max_h, style="FD")
        self.set_xy(x0 + 2, y0 + 1.2)
        self.set_font("Helvetica", "", 7.2)
        self.set_text_color(90, 60, 10)
        self.multi_cell(self.epw - 4, h, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_y(y0 + max_h + 1.5)

    def grain_ref(self):
        """Short reference after first full definition."""
        self.set_font("Helvetica", "I", 7.2)
        self.set_text_color(90, 60, 10)
        self.multi_cell(
            0, 4.0,
            "Late-grain note: see definition in C.2 (order 6,534 / item 7,264 / pair 6,547).",
            new_x=XPos.LMARGIN, new_y=YPos.NEXT,
        )
        self.ln(1)

    def callout(self, title, text):
        h = 4.0
        body = f"{title}: {text}"
        lines = self.multi_cell(self.epw - 4, h, body, dry_run=True, output="LINES")
        max_h = len(lines) * h + 3
        if self.get_y() + max_h > self.page_break_trigger:
            self.add_page()
        y0, x0 = self.get_y(), self.l_margin
        self.set_fill_color(240, 245, 252)
        self.set_draw_color(30, 60, 100)
        self.rect(x0, y0, self.epw, max_h, style="FD")
        self.set_xy(x0 + 2, y0 + 1.2)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(30, 50, 80)
        self.multi_cell(self.epw - 4, h, body, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_y(y0 + max_h + 1.5)

    def assumption_banner(self, text):
        h = 4.0
        lines = self.multi_cell(self.epw - 4, h, text, dry_run=True, output="LINES")
        max_h = len(lines) * h + 3
        if self.get_y() + max_h > self.page_break_trigger:
            self.add_page()
        y0, x0 = self.get_y(), self.l_margin
        self.set_fill_color(255, 235, 235)
        self.set_draw_color(160, 50, 50)
        self.rect(x0, y0, self.epw, max_h, style="FD")
        self.set_xy(x0 + 2, y0 + 1.2)
        self.set_font("Helvetica", "B", 7.5)
        self.set_text_color(120, 30, 30)
        self.multi_cell(self.epw - 4, h, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_y(y0 + max_h + 1.5)


def build():
    pdf = Doc(format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.set_margins(16, 14, 16)

    # -- PAGE 1: banner + snapshot + both models --
    pdf.add_page()
    pdf.set_fill_color(20, 40, 70)
    pdf.rect(0, 0, pdf.w, 24, style="F")
    pdf.set_y(6)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(
        0, 5.5, "HVIA Data Analysis Training Task", align="C",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.set_font("Helvetica", "", 8.5)
    pdf.multi_cell(
        0, 4.5,
        "Olist Business Discovery  |  Final Integrated Report (Tasks 1-6)  |  A + B + C + E",
        align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.set_y(28)

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(90, 90, 90)
    pdf.multi_cell(
        0, 4.2,
        "Reading path: A Company  ->  B Dataset  ->  C Analysis (evolved with Tasks 2-6)  ->  "
        "E HVIA Solutions (+ E.8 extensions). Descriptive evidence only - no causal claims.",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.ln(1)

    pdf.h1("A. Company Research")
    pdf.body(
        "Olist helps Brazilian SMB retailers sell more through technology. Below: who they are, "
        "how money worked in the dataset era, what was added later, then a dated timeline. "
        "The public order extract (Kaggle ~2018) reflects the marketplace aggregator / Olist Store "
        "model - not today's full SaaS + fintech stack. Keep that split while reading B and C."
    )

    pdf.h2("Executive Summary")
    pdf.body(
        "Olist's 2016-2018 marketplace-aggregator story, as the data shows it: fast order growth "
        "on a shared storefront where a small share of late deliveries coincides with much lower "
        "review scores, customers rarely return, and revenue is concentrated in a thin seller elite. "
        "The public order extract (roughly 2016-09-04 to 2018-10-17) describes that aggregator model - "
        "not today's SaaS + fintech stack."
    )
    pdf.body(
        "Strongest descriptive signals: only 6.8% of delivered orders arrive after the ETA, yet average "
        "review scores show 4.29 (on-time/early) vs 2.27 when late; crude one-time buying is 96.88% "
        "(fixed-window H1-2017 12m repeat is 4.68% on eligible customers); the top 10% of sellers account "
        "for ~67.5% of product revenue; and late product GMV is R$985,924.34 (7.25% of GMV), concentrated "
        "in the top revenue decile - with any commission math shown as ASSUMED scenarios only."
    )
    pdf.body(
        "Tasks 2-6 add: delivery-stage timing (handoff and transit gaps between late and on-time orders), "
        "seller exposure tiers, a category-risk lens restricted to categories with >=100 delivered orders, "
        "fixed-window cohort retention with censoring labeled, and late-GMV exposure sizing by seller and "
        "category. Integrated direction: predict late risk before the ETA is missed, rank sellers by health "
        "rather than GMV alone, protect the first-order experience, and size late-GMV exposure as labeled "
        "scenarios for investigation."
    )

    pdf.h2("A.1 Snapshot")
    pdf.kv_compact(
        [
            ("Field", "Detail"),
            ("Legal name", "Olist Servi\u00e7os Digitais Ltda. (CNPJ 18.552.346/0001-68)"),
            ("Founded", "2014 (commercially active from 2015; reported; sources differ on 2014 vs 2015)"),
            ("Founder & CEO", "Tiago Dalvi"),
            ("HQ", "Curitiba, Paran\u00e1, Brazil (+ S\u00e3o Paulo, Bento Gon\u00e7alves)"),
            ("Team size", "~790-850 (approximate; after SaaS-oriented restructuring)"),
            ("Valuation / funding", "$1.5B unicorn (Dec 2021, reported)  |  ~$300M+ funding (approximate; unverified)"),
            ("Merchants / scale", "50,000+ merchants (reported)  |  R$60B+ ecosystem invoicing (company-reported)"),
            ("Primary customer", "SMB retailers / brands (sellers); end consumers are demand-side in the CSVs"),
        ]
    )

    pdf.h2("A.2 Dataset-era model (2016-2018) - what the data describes")
    pdf.body(
        "Flow: small seller joins Olist -> products listed under Olist's verified storefront on "
        "major marketplaces -> customer buys from \"Olist\" -> seller fulfills. Monetization: "
        "roughly 19-21% blended commission (reported/unverified; C.6 take-rates are ASSUMED scenarios) plus "
        "modest seller subscription / membership fees."
    )
    pdf.bullet(
        "Thin intermediary margins: historically gross margins in a mid-30s percent range were "
        "hard to expand while operating the aggregator layer."
    )
    pdf.bullet(
        "Reputation contagion: a few late or poor sellers could damage the shared Olist account "
        "rating on Mercado Livre, Amazon, etc., hurting thousands of good sellers at once."
    )
    pdf.bullet(
        "Merchant churn at scale: as seller GMV grew, a ~20% take-rate pushed sellers to open "
        "direct marketplace accounts; platforms also made direct onboarding easier over time."
    )

    pdf.h2("A.3 Later model (context only) - what was added after the dataset")
    pdf.body(
        "Olist evolved into a retail technology ecosystem often framed as a \"Commerce OS\": "
        "Tiny ERP, Vnda (D2C), Olist Pax (logistics), Flip (credit), PDV, and Lis (embedded AI). "
        "Indicative later mix (unverified estimate): ~65% recurring SaaS, ~20% fintech/credit, ~10% logistics spread. "
        "Use this for company research; do not force 2025-2026 products into every 2016-2018 KPI."
    )
    pdf.bullet(
        "Competitors (examples): Bling, Nuvemshop, VTEX, Melhor Envio, Magazord - different "
        "ERP / storefront / shipping mixes."
    )
    pdf.bullet(
        "Stack (high level): Python/Go/React; Kafka; PostgreSQL/Redis/Elasticsearch; "
        "AWS + Spark/Databricks-style analytics."
    )

    # -- PAGE 2: Timeline + bridge KPIs --
    pdf.add_page()
    pdf.h1("A.4 Sequential timeline - what was added when")
    pdf.body(
        "Read top to bottom. The 2016-18 band is locked to the public CSV extract. Later rows "
        "explain strategic evolution; they are not additional columns in the order tables."
    )
    pdf.timeline_row(
        "2007",
        "Solidarium (reported): physical retail network supporting artisans and small producers "
        "(founder Tiago Dalvi's pre-Olist chapter - same SMB DNA).",
    )
    pdf.timeline_row(
        "2014-15",
        "Olist founded. Insight: SMBs struggle to reach customers on major marketplaces, not "
        "only to open a store. Olist launches as a tech + logistics bridge / aggregator.",
    )
    pdf.timeline_row(
        "2016-18",
        "DATASET WINDOW (this task). Olist Store / shared storefront: sellers fulfill under one "
        "Olist face; commission ~19-21% (reported/unverified) + fees; ~99k public orders. Shared reputation is the "
        "structural risk. All Sections B-C interpret operations in this window.",
    )
    pdf.timeline_row(
        "2019-20",
        "Ecosystem build: Clickspace (marketplace / social commerce infrastructure) and "
        "PAX Logtech (later Olist Pax - carrier aggregation, rate shopping, discounted labels).",
    )
    pdf.timeline_row(
        "2021",
        "Adds Tiny ERP (catalog, inventory, Brazilian tax invoicing) and Vnda (D2C / headless "
        "storefront). Unicorn at $1.5B (Dec 2021). Software becomes a clearer growth path.",
    )
    pdf.timeline_row(
        "2022-24",
        "Tech-winter discipline: cost control, focus on higher-margin SaaS recurring revenue, "
        "and operating leverage versus pure marketplace take-rate economics.",
    )
    pdf.timeline_row(
        "Aug 2025",
        "Adds fintech Flip -> Flip by Olist for merchant working capital, supported by an "
        "FIDC credit structure (~R$90M, reported). Underwriting edge (hypothesis): ERP sales/invoice signals.",
    )
    pdf.timeline_row(
        "2026",
        "Aug: reported operational breakeven path. Sep: CEO announces wind-down of the shared "
        "marketplace storefront model and a full shift toward SaaS + fintech - closing the "
        "chapter that the 2016-2018 dataset documents.",
    )

    pdf.h2("A.5 Takeaway - how to use this in B and C")
    pdf.body(
        "Acknowledge today's Commerce OS in company research. For dataset understanding and "
        "analysis, stay inside 2016-2018: shared reputation, commission on orders, "
        "seller-fulfilled shipping, freight and ETA as customer-visible promises. "
        "Early dataset signals already point to late delivery associated with lower reviews, near-zero "
        "repeat purchase, and seller revenue concentration - expanded next."
    )
    pdf.kv_compact(
        [
            ("Bridge KPI (from CSVs)", "Signal"),
            ("~99.4k orders / ~96k unique buyers", "Scale of the public extract"),
            ("Late vs ETA 6.8% with reviews 4.29 vs 2.27 (descriptive)", "Reputation risk > volume risk"),
            ("Crude one-time 96.88% (H1-2017 12m repeat 4.68%)", "Acquisition-led growth, weak LTV"),
            ("Top 10% sellers -> ~67.5% product revenue", "GMV + quality concentration"),
        ]
    )

    # -- PAGE 3: Dataset B dense --
    pdf.add_page()
    pdf.h1("B. Dataset Understanding")
    pdf.body(
        "Public Brazilian E-Commerce extract (Olist Store). Purchase timestamps span roughly "
        "2016-09-04 to 2018-10-17. Nine related CSVs. Not in scope: marketplace ad spend, "
        "seller subscription invoices, or post-2018 SaaS / Flip product telemetry."
    )

    pdf.h2("B.1 Nine tables (structure)")
    pdf.kv_compact(
        [
            ("Table", "Rows / role"),
            ("orders", "99,441 | Hub: status + purchase/approval/carrier/delivery/ETA"),
            ("order_items", "112,650 | Line items: product, seller, price, freight (~1.14/order)"),
            ("customers", "99,441 | Location; customer_unique_id = true person (96,096)"),
            ("sellers", "3,095 | Merchant location"),
            ("products", "32,951 | Category, photos, weight/dims"),
            ("payments", "103,886 | Type, installments, value (some split payments)"),
            ("reviews", "99,224 | Score 1-5 + optional text (~1 per order)"),
            ("geolocation", "1,000,163 | Lat/lng; many rows per ZIP -> mean before distance"),
            ("category_translation", "71 | Portuguese category -> English"),
        ],
        col_widths=[48, pdf.epw - 48],
    )

    pdf.h2("B.2 How to join (sequential)")
    pdf.step(
        1,
        "Start at orders",
        "Filter/status first. ~97% delivered. Delivery KPIs need delivered + non-null "
        "delivered_customer_date (96,470 orders in the SLA cut).",
    )
    pdf.step(
        2,
        "Attach items -> products -> sellers",
        "Revenue and freight live on items; aggregate to order before AOV or late-rate. "
        "Category via products + translation: 610 null category + 2 unmapped PT names -> "
        "Unknown bucket (1,559 delivered items / R$185k revenue); quantified for totals "
        "reconciliation, excluded from ranked headlines.",
    )
    pdf.step(
        3,
        "Attach customers + payments",
        "Retention only via customer_unique_id. Payments: ~74% credit card, ~19% boleto, "
        "~6% voucher; ~3k orders have multiple payment rows.",
    )
    pdf.step(
        4,
        "Attach reviews + geo",
        "Aggregate review_score if duplicate order_id (551 duplicate rows). ZIP geo is not "
        "unique - mean lat/lng per prefix before seller-customer distance.",
    )

    pdf.h2("B.3 Data quality + exploration snapshot")
    pdf.body(
        "Main traps are grain mismatches (item vs order) and geo duplication - not corrupt CSVs. "
        "Review titles missing ~88% and messages ~59%: scores scale; text themes are biased "
        "toward customers who wrote comments."
    )
    pdf.kv_compact(
        [
            ("KPI", "Value"),
            ("Product revenue / freight / AOV", "R$13.6M  |  R$2.3M  |  ~R$138"),
            ("Late vs ETA (delivered)", "6.8% of 96,470"),
            ("Review on-time vs late", "4.29 vs 2.27 stars (descriptive)"),
            ("One-time buyers", "96.88% crude (H1-2017 12m repeat 4.68%)"),
            ("Top 10% sellers -> revenue", "~67.5%"),
            ("SP share (customers / sellers)", "~42% / ~60%"),
            ("Cancel + unavailable", "~1.24% (secondary vs late & loyalty)"),
        ]
    )
    pdf.body(
        "Takeaway: order-centric marketplace ops data. Fulfillment reliability and seller "
        "heterogeneity sit on a one-shot customer base - the chain of associations in Section C."
    )

    # -- C --
    pdf.add_page()
    pdf.h1("C. Analysis & Business Story  |  Chain of associations")
    pdf.body(
        "Read as a sequence of associations: growth stress -> logistics and geography -> late deliveries -> "
        "review collapse and written complaints -> weak repeat purchase - amplified by a "
        "concentrated seller base under one shared Olist face. Tasks 2-6 add stage timing, "
        "seller/category concentration, cohort windows, and late-GMV exposure sizing. "
        "Note: Task D is folded into C (no separate D section)."
    )

    pdf.h2("C.1 Growth co-occurred with operational pressure")
    pdf.body(
        "Orders scaled fast (Jan 2017 -> Jan 2018 YoY ~+809%, with an early-base caveat: "
        "Jan 2017 had only ~800 orders). Peak month Nov 2017: 7,544 orders (Black Friday "
        "context). Cancel + unavailable together ~1.2% - secondary versus lateness and "
        "loyalty. Peaks coincide with wider SLA gaps (descriptive; not proof peaks cause lateness)."
    )
    pdf.body(
        "New evidence (late-GMV seasonality, see E.8): within-month late product GMV share spikes at "
        "Nov-2017 12.49%, Feb-2018 15.05%, and Mar-2018 19.03% (item grain; locked is_late "
        "broadcast) - peaks co-occur with volume stress and warrant investigation as "
        "seasonal exposure, not proof of a single root cause."
    )
    pdf.figure(
        "01_monthly_order_volume.png",
        "Fig C.1 (Chart 01)  Monthly order volume - growth and seasonal spike.",
        width=148,
    )

    pdf.h2("C.2 Distance and freight coincide with an uneven promise")
    pdf.grain_box()
    pdf.body(
        "S\u00e3o Paulo holds ~42% of customers and ~60% of sellers. Same-state delivery averages "
        "~7.5 days versus cross-state ~14.7 (+~7.2 days). Median seller-to-customer distance "
        "~434 km (distance <-> delivery days r ~ 0.39). Freight totals ~R$2.3M (~17% of "
        "product revenue); at item level, freight is ~21% of (price + freight)."
    )
    pdf.callout(
        "Glossary (first use)",
        "New evidence in this report: delivery stages; seller exposure tiers; category-risk lens; "
        "late-GMV view (detail in E.8). "
        "D1 = top revenue decile (310 sellers; a ranking label, not a problem ID). Broadcast=order late flag copied to each item. "
        "Locked is_late=delivery delta_days > 0 on 96,470 delivered. Grain=unit of counting "
        "(order / item / seller-pair / customer).",
    )
    pdf.figure(
        "16_distance_vs_delivery.png",
        "Fig C.2a (Chart 16)  Distance vs delivery - farther pairs show longer times and higher late shares (descriptive).",
        width=140,
    )

    pdf.callout(
        "New evidence - Delivery stages (see E.8)",
        "Full-chain n=96,455. Medians (>=0): approval 0.34h / handoff 44.38h / transit 7.10d / "
        "total 10d. Late vs on-time gaps: +0.07h / +30.57h / +19.25d / +22d. p90 handoff "
        "~144.55h. DQ negatives flagged (not dropped): handoff 1,350 (1.40%), transit 23. "
        "Shows where time sits; cannot establish which stage causes lateness.",
    )
    pdf.figure(
        "19_delivery_stage_breakdown.png",
        "Fig C.2b (Chart 19a)  Most delivery time sits in transit; late orders show far longer transit "
        "and handoff tails. Technical detail: full-chain n=96,455; medians on >=0 subsets; panel (b) "
        "transit density late vs on-time; correlational; see grain definitions in C.2.",
        width=148,
    )
    pdf.body(
        "New evidence - Category freight lens (see E.8; >=100 delivered orders only; 51/71 cats = 97.77% items / "
        "97.63% revenue): electronics mean item freight ratio 35.81%; audio late rate 11.60% "
        "(362 items / 348 orders). dvds_blu_ray 40.37% freight at n=56 is sensitivity-only "
        "(below >=100 headline). Freight ratio vs late rate r=0.12 (descriptive); vs review "
        "r=0.03 - co-occurrence is weak, not causal."
    )
    pdf.figure(
        "21_category_risk.png",
        "Fig C.2c (Chart 21b)  Freight cost does not show a strong relationship with lateness "
        "in this descriptive cut. Technical detail: item grain; >=100 delivered orders; n labeled; "
        "Unknown excluded; r=0.12; descriptive only. Panel (a) top-15 revenue + late dots.",
        width=145,
    )

    # -- C.3 --
    pdf.add_page()
    pdf.h2("C.3 Late delivery is associated with lower shared-account scores")
    pdf.body(
        "Note on seller counts: the floor-based top-10% count (309 sellers, 67.49%) differs slightly "
        "from the qcut-based D1 decile (310 sellers, 67.56%) used in Task 3-6 seller tables - both round "
        "to ~67.5%; D1 is the primary reference from here on."
    )
    pdf.body(
        "Only 6.8% of delivered orders arrive after the ETA, but average review score is "
        "lower when late: 4.29 (on-time/early) vs 2.27 when late (-2.02 stars, descriptive). "
        "Mean actual delivery ~12.1 days versus mean ETA ~23.4 - a large buffer exists, yet late "
        "cases still show lower scores. Under aggregator logic this pattern is consistent with "
        "reputation contagion on the shared marketplace account, not a CX footnote. Among 1-star "
        "comments, delivery/delay keyword hit-rate (unvalidated) ~41% versus product/quality ~13% "
        "(commented 1-stars only; n=8,744)."
    )
    pdf.figures_pair(
        "06_delivery_vs_review_scores.png",
        "18_review_text_signals.png",
        "Fig C.3a (Chart 06)  Late vs on-time reviews",
        "Fig C.3b (Chart 18)  1-star text themes (keyword hit-rate)",
        width=92,
    )

    pdf.callout(
        "New evidence - Seller + stage concentration (see E.8)",
        "D1 (top revenue decile, 310 sellers): 67.56% of product revenue (R$9,183,174.76) and "
        "63.14% of seller-pair late flags. Top-30 sellers by late count hold ~30.1% of "
        "pair-late. Operational coverage sellers >=10 delivered: 1,237 = 93.9% volume / "
        "90.2% revenue. Stage gaps (handoff +30.57h, transit +19.25d) co-occur with the "
        "locked late flag - warrants investigation, cannot establish causality.",
    )
    pdf.body(
        "Stage detail: see Fig C.2b (Chart 19) - transit density for late vs on-time orders."
    )
    pdf.figure(
        "20_seller_risk.png",
        "Fig C.3c (Chart 20a)  Revenue and late flags are concentrated in the top decile, while "
        "late rates stay flat across deciles. Technical detail: n=3,095 sellers; seller-pair grain; "
        "locked is_late; descriptive only.",
        width=148,
    )

    pdf.h2("C.4 Almost no loyalty + a thin seller elite")
    pdf.body(
        "Of 96,096 unique customers, crude one-time 93,099/96,096 = 96.88% (~96.9%) buy once "
        "and only ~3.1% return (2+ orders) in the full window. Fixed-window counterpart: H1-2017 "
        "12m repeat 666/14,239 = 4.68% (i.e. ~95.3% did not repeat within 12m; eligible 29,087; "
        "censored 67,009). Commission LTV would barely compound if repeat stays low "
        "(hypothesis; no CAC or customer-value data in scope); a weak first delivery experience "
        "coincides with lower likelihood of order #2 (hypothesis, not proven). "
        "Among 3,095 sellers, the top 10% drive ~67.5% of product revenue while the bottom "
        "50% contribute ~3.2% - GMV dependence and long-tail reputation risk share the "
        "same Olist storefront."
    )
    pdf.callout(
        "Cohort window (Task 5)",
        "Crude full-window one-time 93,099/96,096 = 96.88% remains locked alongside "
        "H1-2017 12m repeat 666/14,239 = 4.68% (71 with 3+; median days to second 60.5d). "
        "Eligible denominator 29,087; right-censored 67,009 (first_date after 2017-10-17). "
        "Different windows/denominators - not a contradiction.",
    )
    pdf.figures_pair(
        "08_customer_retention_crisis.png",
        "10_seller_pareto_curve.png",
        "Fig C.4a (Chart 08)  One-time vs repeat buyers",
        "Fig C.4b (Chart 10)  Seller revenue Pareto",
        width=92,
    )
    pdf.figure(
        "22_cohort_retention.png",
        "Fig C.4c (Chart 22)  Fixed-window repeat stays low even with full observation time. "
        "Technical detail: customer grain; eligible n labeled; censored 67,009 annotated; no causality.",
        width=148,
    )
    pdf.callout(
        "Descriptive: first-order lateness vs 12m repeat (eligible cohort, no causality)",
        "Eligible 29,087 (first_date <= 2017-10-17): on-time first 1,226/26,860 = 4.56%; "
        "late first 35/1,010 = 3.47% (-1.10 pp gap, descriptive); non-delivered/unclassifiable "
        "first 57/1,217 = 4.68%. Total eligible repeat 1,318/29,087 = 4.53%. Cross-foots H1 "
        "666/14,239 = 4.68%. Delivered-first only; same locked is_late; fixed 365d window.",
    )
    pdf.body(
        "New evidence (exposure concentration, see E.8): D1 holds 67.56% revenue and 63.14% of seller-pair late "
        "flags; top-30 late sellers ~30.1% of pair-late - creates exposure at the elite and "
        "warrants tiered investigation, not a claim that sellers cause lateness."
    )

    # -- C.5 + problem table --
    pdf.add_page()
    pdf.h2("C.5 Priority spine (what to solve next)")
    pdf.body(
        "Priority order using the same P1-P7 labels as the register below "
        "(* = new evidence from Tasks 2-6 attached; detail in E.8). "
        "P6 feeds P1. Language remains correlational (shows / co-occurs / creates exposure)."
    )
    pdf.kv_compact(
        [
            ("P#", "Problem -> business stake (2016-18 model)"),
            ("P1*", "Late delivery associated with review drop  |  shared marketplace reputation"),
            ("P2*", "Near-zero repeat purchase  |  acquisition-cost hypothesis, weak LTV (no CAC data)"),
            ("P3*", "Seller Pareto + long tail  |  GMV fragility + contagion"),
            ("P4", "Geo / distance SLA gap  |  uneven national promise"),
            ("P5*", "Freight burden  |  price perception + delay sensitivity"),
            ("P7*", "Growth/seasonality pressure + late-GMV exposure  |  seasonal volume stress on SLA (scenario commission)"),
        ],
        col_widths=[10, pdf.epw - 10],
    )

    pdf.h2("Problem register P1-P7 (Scale + New evidence)")
    w = pdf.epw
    pdf.kv_compact(
        [
            ("P#", "Problem", "Scale", "New evidence / Limitation"),
            (
                "P1",
                "Late delivery <-> review collapse",
                "6,534/96,470=6.77%; reviews 4.29/2.27",
                "Stages: handoff +30.57h, transit +19.25d (full-chain 96,455). "
                "Limitation: correlational; 8.11% sensitivity only.",
            ),
            (
                "P2",
                "Near-zero repeat / loyalty",
                "Crude one-time 96.88% (93,099/96,096)",
                "H1 12m 4.68% (666/14,239); median 60.5d; censored 67,009. "
                "Limitation: windows differ; no LTV proof.",
            ),
            (
                "P3",
                "Seller Pareto + quality mix",
                "Top 10% ~67.5% rev; n=3,095",
                "D1 67.56% rev + 63.14% pair-late; top-30 ~30.1%; >=10: 1,237 "
                "(93.9% vol / 90.2% rev). Limitation: not inefficiency proof.",
            ),
            (
                "P4",
                "Geo / distance SLA gap",
                "Same-state ~7.5d vs cross ~14.7d; r~0.39",
                "Unchanged primary; stage/geo still descriptive. "
                "Limitation: distance is a proxy, not carrier ID.",
            ),
            (
                "P5",
                "Freight burden",
                "~14.2% of paid; ~17% of product; mean-item ~21%",
                "electronics 35.81% (>=100); dvds 40.37% n=56 sensitivity-only; "
                "freight-late r=0.12. Limitation: weak co-occurrence.",
            ),
            (
                "P6",
                "Review-text delivery anger",
                "~41% delivery keyword hit-rate (unvalidated) in commented 1-stars",
                "Unchanged primary text scan. Limitation: commented subset + unvalidated stems.",
            ),
            (
                "P7",
                "Growth / seasonality pressure",
                "Nov-17 peak 7,544 orders",
                "Late-GMV monthly spikes Nov-17 12.49%, Feb-18 15.05%, Mar-18 19.03%. "
                "Limitation: seasonality context, not causal.",
            ),
        ],
        col_widths=[10, 42, 48, w - 10 - 42 - 48],
    )
    pdf.body(
        "Bridge to HVIA solutions (next section): start from problems 1-3 - predictive delay / ETA, "
        "seller SLA risk scoring, and first-order experience protection - not from a tool list. "
        "E.8 extends cores with delivery-stage, exposure-tier, category-risk and late-GMV extensions "
        "plus a P2 60d refinement."
    )

    # -- C.6 Financial Exposure --
    pdf.add_page()
    pdf.h2("C.6 Financial Exposure (Task 6)")
    pdf.assumption_banner(
        "ASSUMPTION BANNER: Take-rates 15% / 19% / 21% are ASSUMED scenarios only - "
        "NOT loss, NOT verified take-rate, NOT recoverable revenue."
    )
    pdf.body(
        "Product GMV = SUM(price) = R$13,591,643.70. Late product GMV (is_late broadcast to "
        "items) = R$985,924.34 = 7.25% of GMV. D1 late GMV R$680,097.81 = 68.98% of late GMV; "
        "top-30 late sellers R$224,401.75 = 22.76%; top-10 categories (>=100) R$637,375.28 = "
        "64.65%. Under a 19% ASSUMED take-rate, implied commission on late GMV = R$187,325.62. "
        "Creates exposure for investigation; cannot establish causality or recoverable amounts."
    )
    pdf.kv_compact(
        [
            ("Slice", "Product GMV (R$)", "Share", "Comm @19% (ASSUMED)"),
            ("Total product GMV", "13,591,643.70", "100%", "2,582,412.30"),
            ("Late product GMV", "985,924.34", "7.25% of GMV", "187,325.62"),
            ("D1 late GMV", "680,097.81", "68.98% of late", "129,218.58"),
            ("Top-30 late sellers", "224,401.75", "22.76% of late", "42,636.33"),
            ("Top-10 cats late GMV", "637,375.28", "64.65% of late", "121,101.30"),
        ],
        col_widths=[42, 38, 38, pdf.epw - 42 - 38 - 38],
    )
    pdf.figure(
        "23_financial_exposure.png",
        "Fig C.6 (Chart 23)  Late GMV concentrates in peak months and in the top decile; commission "
        "shown is a scenario, not a loss. Technical detail: item grain; comm@19% ASSUMED; no causality.",
        width=148,
    )

    # -- E: Solutions --
    pdf.add_page()
    pdf.h1("E. HVIA Solution Proposal")
    pdf.body(
        "Principle from the brief: \"Don't sell a tool. Find a problem worth solving.\" "
        "Every solution below starts from a Section C problem. Build priority follows C.5: "
        "core Solutions 1-3 first (strongest evidence, highest reputation stakes), then "
        "supporting layers that feed them, then one lighter side solution. "
        "E.8 adds Task 2-6 extensions without replacing cores."
    )

    pdf.h2("E.1 Solution map")
    pdf.kv_compact(
        [
            ("#", "Problem -> Solution  |  Type  |  HVIA domain"),
            (
                "1",
                "P1 Late delivery / reviews -> Predictive Late-Delivery Risk & Response  |  "
                "Core  |  Forecasting + Logistics Intelligence",
            ),
            (
                "2",
                "P2 Near-zero repeat -> First-Order Retention Risk Flag  |  Core  |  "
                "Customer Intelligence",
            ),
            (
                "3",
                "P3 Seller Pareto -> Seller Health Score  |  Core  |  Analytics & Decision "
                "+ AI-Assisted Ops",
            ),
            (
                "4",
                "P4 Geo/distance SLA -> Geo-aware Dynamic ETA  |  Supporting (feeds #1)  |  "
                "Logistics Intelligence",
            ),
            (
                "5",
                "P5 Freight pressure -> Freight-Ratio Catalog Alert  |  Side  |  "
                "Analytics & Decision Systems",
            ),
            (
                "6",
                "P6 Review-text delivery anger -> Review-Text Triage  |  Supporting "
                "(feeds #1,#2)  |  Customer Intelligence + AI Ops",
            ),
            (
                "7",
                "P7 Growth/seasonality -> Seasonal Demand Signal  |  Supporting (feeds #1)  |  "
                "Forecasting & Predictive + Automation & Data Pipelines (scheduled refresh)",
            ),
        ],
        col_widths=[8, pdf.epw - 8],
    )
    pdf.body(
        "Automation & Data Pipelines layer (feeds all alerts): scheduled ingest of orders/items/reviews, "
        "grain-aware late-flag broadcast, and automated risk-list refresh for Solutions 1-3. "
        "No new numbers; labeling only."
    )
    pdf.callout(
        "Lead idea for outreach (one headline)",
        "Predictive late-risk early warning with Seller Health as a feature (Solution 1 + 3). "
        "The rest below are supporting/side layers. No model was trained or validated in this task.",
    )

    pdf.h2("E.2 Core 1 - Predictive Late-Delivery Risk & Response (P1)")
    pdf.body(
        "Problem: only 6.8% of delivered orders are late vs ETA, yet average review is lower when late: "
        "4.29 (on-time/early) vs 2.27 (-2.02 stars, descriptive). Under the shared storefront this pattern "
        "is consistent with reputation contagion on one Olist marketplace account - not an isolated CX issue."
    )
    pdf.body(
        "What it does: at ship-prep time, score each order for probability of missing the "
        "*promised* ETA (catch cases where the generous buffer still will not be enough). "
        "Limitation: no model was trained or validated in this task."
    )
    pdf.bullet(
        "Inputs: seller-customer distance (r~0.39 with days); same-state vs cross-state; "
        "weight/category as freight-cost and handling proxy (weight-freight r~0.61 describes cost only, "
        "not lateness; freight-late co-occurrence is weak r~0.12); seller historical on-time (from Seller "
        "Health); current volume load (Seasonal Demand). No carrier ID exists in this extract "
        "(orders has only carrier timestamp; items has shipping_limit_date); use freight-per-km proxy "
        "or drop; no carrier attribution."
    )
    pdf.bullet(
        "Actions: Low = standard flow. Medium = proactive customer notice with a revised "
        "realistic window before the ETA is missed. High (+ poor Seller Health) = escalate "
        "to seller to expedite; flag for priority support if delay still occurs."
    )
    pdf.bullet(
        "KPI: shrink the on-time vs late review gap (baseline -2.02) for medium-risk notified "
        "vs control; secondary: % of high-risk orders still late after escalation (should fall)."
    )
    pdf.body("Evidence: Charts 04, 05, 06, 15, 19.")

    pdf.h2("E.3 Core 2 - First-Order Retention Risk Flag (P2)")
    pdf.body(
        "Problem: crude one-time 96.88% buy once; only ~3.1% return in the full window. Growth is acquisition-led; "
        "commission LTV would barely compound if repeat stays low (hypothesis; no CAC or customer-value data). "
        "Cohort view (eligible H1) shows 4.68% 12m repeat - still low, but a fairer fixed-window KPI than crude alone."
    )
    pdf.body(
        "What it does: when a first order completes (delivered + reviewed, or delivered + no "
        "review after N days), score repeat-buy probability from that single experience - "
        "turning blanket \"come back\" campaigns into a targeted list worth a proactive touch."
    )
    pdf.bullet(
        "Inputs: late/high-risk flag from Solution 1; fulfilling seller Health Score; "
        "order value/category; review score if given."
    )
    pdf.bullet(
        "Action: high-value + high-churn-risk customers get a lightweight retention action "
        "(support check-in or small proactive gesture) - cost proportional to likely worth."
    )
    pdf.bullet(
        "KPI: repeat-purchase rate in the flagged high-risk/high-value cohort vs eligible 12m baseline "
        "(H1-2017 4.68% on eligible denominator) with a control group from the same cohort; do not use "
        "the 3.1% crude full-window rate as the comparator."
    )
    pdf.body("Evidence: Charts 08, 22.")

    pdf.add_page()
    pdf.h2("E.4 Core 3 - Seller Health Score (P3)")
    pdf.body(
        "Problem: top 10% of sellers -> ~67.5% product revenue; bottom 50% -> ~3.2%. Under a "
        "shared storefront, low GMV does not mean low reputation risk."
    )
    pdf.body(
        "What it does: composite per-seller score (late rate, avg review, GMV contribution, "
        "growth trend). Tiers e.g. Protect and Grow / Monitor / At-Risk - any size seller whose "
        "delivery/review pattern threatens the shared account. Minimum-volume rule: apply "
        "the >=10 delivered filter (1,237 sellers) for rate headlines; order-weighted late rates are "
        "flat ~5-7% across deciles. Tier thresholds are TBD (not defined here)."
    )
    pdf.bullet(
        "Action: tier feeds Solution 1 as a delay-model feature; account/support attention "
        "prioritizes At-Risk sellers instead of spreading evenly across 3,095 merchants."
    )
    pdf.bullet(
        "KPI: earlier detection of reputation-risk sellers; falling share of GMV from At-Risk "
        "sellers over time as intervention works."
    )
    pdf.body("Evidence: Charts 10, 20. Build note: ship #3 first or alongside #1 (#1 needs the score).")

    # Supporting + side + build order
    pdf.add_page()
    pdf.h2("E.5 Supporting components (not standalone pitches)")
    pdf.body(
        "Scoped as accuracy layers inside Solutions 1-3 - not separate products to sell first."
    )

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(30, 60, 100)
    pdf.multi_cell(
        0, 4.8, "E.5.1 Geo-aware Dynamic ETA (P4 -> feeds Solution 1)",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.body(
        "Replace a flat, buffer-heavy national ETA with a per-route estimate from historical "
        "same-state vs cross-state and distance-bucket times (distance<->days r~0.39). This is "
        "how Solution 1 knows what a realistic promise looks like for a seller-customer pair. "
        "Success must be measured by ETA calibration/accuracy and review score, not late rate alone "
        "(tightening ETA mechanically raises late rate under late = delivered > ETA). Who sets the ETA "
        "(Olist vs marketplace) is not visible in the data. "
        "Evidence: Charts 05, 11, 12, 16."
    )

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(30, 60, 100)
    pdf.multi_cell(
        0, 4.8, "E.5.2 Review-Text Triage (P6 -> feeds Solutions 1 & 2)",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.body(
        "Among commented 1-stars (n=8,744), delivery/delay keyword hit-rate (unvalidated) ~41% exceeds "
        "product/quality ~13%, yet median review response is ~40 hours. A lightweight classifier routes new "
        "delivery-related negatives to a priority support queue and feeds which features "
        "Solution 1 should weight. Evidence: Charts 07, 18. Keyword stems are unvalidated; precision unknown."
    )

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(30, 60, 100)
    pdf.multi_cell(
        0, 4.8, "E.5.3 Seasonal Demand Signal (P7 -> feeds Solution 1)",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.body(
        "Volume is highly seasonal (e.g. Nov 2017 peak 7,544 orders). During peaks, baseline "
        "late risk is higher independent of one seller or route (descriptive). Feed Solution 1 as a risk "
        "multiplier in forecasted high-volume windows. Evidence: Charts 01, 02, 14, 23a."
    )

    pdf.h2("E.6 Side - Freight-Ratio Catalog Alert (P5)")
    pdf.body(
        "Freight ~17% of product revenue; item-level freight share of (price+freight) ~21%, "
        "some categories ~40% (e.g. DVDs/Blu-ray). At catalog add/reprice, flag items above a "
        "freight-to-price threshold so merchandising can intervene (bundle, min order, carrier "
        "negotiation) before weak conversion. Domain: Analytics & Decision Systems. "
        "Evidence: Charts 12, 13, 17, 21. Rank headlines only for cats >=100 delivered orders."
    )

    pdf.h2("E.7 Suggested build order")
    pdf.kv_compact(
        [
            ("Order", "What to ship"),
            ("1", "Solutions 1-3 (core). Prefer Seller Health (#3) first or parallel with #1."),
            ("2", "E.5.1 Geo ETA + E.5.3 Seasonal signal - upgrade Solution 1 accuracy."),
            ("3", "E.5.2 Review-text triage - strengthens Solutions 1 and 2."),
            ("4", "E.6 Freight catalog alert - light dependency on the rest."),
            ("5", "E.8 extensions (delivery-stage, exposure-tier, category-risk, late-GMV + P2 60d) - layer onto cores after baselines."),
        ],
        col_widths=[14, pdf.epw - 14],
    )

    # -- E.8 Extensions --
    pdf.add_page()
    pdf.h2("E.8 Extensions from Tasks 2-6 (same style as E.2-E.6)")
    pdf.body(
        "These extend existing cores/supports. They do not replace P1-P7 or Solutions 1-3. "
        "Wording stays descriptive (shows / indicates / co-occurs / creates exposure / warrants "
        "investigation). This report does not establish causality, loss, recoverable amounts, "
        "or carrier attribution."
    )
    pdf.grain_ref()

    # E.8.1 delivery-stage extension
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(30, 60, 100)
    pdf.multi_cell(
        0, 4.8, "E.8.1 Handoff-timer + quarantine (extends E.2 / E.5.1)",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.body(
        "What: Monitor seller->carrier handoff clock after approval; quarantine / escalate "
        "orders whose handoff age crosses a threshold before transit even starts."
    )
    pdf.body(
        "Evidence: see C.2 / Chart 19 (Fig C.2b)."
    )
    pdf.body(
        "Mechanism: early timer on the stage that shows the widest upper tail, feeding "
        "Solution 1 risk and Dynamic ETA realism."
    )
    pdf.body(
        "Needs: reliable approved_at + carrier timestamps; DQ handling for negatives; "
        "seller contact path."
    )
    pdf.body(
        "KPI: share of late orders with handoff > p90 among notified vs control; "
        "secondary: review gap on timer-touched orders."
    )
    pdf.body(
        "Limitation: co-occurrence only - cannot establish that handoff causes lateness "
        "or review collapse; no carrier attribution."
    )

    # E.8.2 exposure-tier extension
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(30, 60, 100)
    pdf.multi_cell(
        0, 4.8, "E.8.2 Exposure tier playbook (extends E.4)",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.body(
        "What: Playbook that tiers sellers by exposure - D1 / top-30 late-count / thin-volume "
        "volatility - instead of GMV-only attention."
    )
    pdf.body(
        "Evidence: see C.3-C.4 / Chart 20 (Fig C.3c)."
    )
    pdf.body(
        "Mechanism: maps Seller Health tiers to ops actions proportional to concentrated "
        "late flags and thin-n rate volatility."
    )
    pdf.body("Needs: seller-pair late grain labeled; >=10 filter for rate headlines.")
    pdf.body(
        "KPI: share of pair-late flags under Monitor/At-Risk tiers over time; "
        "coverage of late GMV under tiered outreach."
    )
    pdf.body(
        "Limitation: concentration indicates exposure, not inefficiency or causal seller blame."
    )

    # E.8.3 category-risk extension
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(30, 60, 100)
    pdf.multi_cell(
        0, 4.8, "E.8.3 Category-risk lens >=100 only (extends E.6 / E.5.1)",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.body(
        "What: Assortment risk view restricted to categories with >=100 delivered orders "
        "(51/71 = 97.77% items / 97.63% rev); Unknown excluded from ranks."
    )
    pdf.body(
        "Evidence: see C.2 / Chart 21 (Fig C.2c)."
    )
    pdf.body(
        "Mechanism: feeds Freight Alert + ETA features with n-safe category priors."
    )
    pdf.body("Needs: item-grain late broadcast labeled; dual n_items + n_orders on every row.")
    pdf.body("KPI: % of late items in >=100 ranked cats under review; catalog flags fired.")
    pdf.body(
        "Limitation: category co-occurs with late flags; cannot establish causality or "
        "justify delisting from this evidence alone."
    )

    # N4
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(30, 60, 100)
    pdf.multi_cell(
        0, 4.8, "E.8.4 Late-GMV view + peak guardrail (extends E.5.3)",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.body(
        "What: Ops dashboard of late product GMV (not order-count alone) with peak-month "
        "guardrails when within-month late-GMV share spikes."
    )
    pdf.body(
        "Evidence: see C.1 and C.6 / Chart 23 (Fig C.6)."
    )
    pdf.body(
        "Mechanism: Seasonal Demand multiplier keyed to late-GMV share, not volume only."
    )
    pdf.body(
        "Needs: item-broadcast late GMV pipeline; explicit ASSUMED take-rate labels."
    )
    pdf.body(
        "KPI: peak-month late-GMV share vs baseline 7.25%; scenario commission on late GMV "
        "under stated assumption."
    )
    pdf.body(
        "Limitation: scenarios are NOT loss / NOT verified take-rate / NOT recoverable; "
        "spikes warrant investigation only."
    )

    # P2 refined
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(30, 60, 100)
    pdf.multi_cell(
        0, 4.8, "P2-refined - 60d retention window with 4.68% KPI (extends E.3)",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.body(
        "What: Keep crude 96.88% for full-window honesty, and add a fixed-horizon playbook "
        "anchored on H1-2017 12m repeat 4.68% with a ~60d median-to-second outreach window "
        "(median days to second among 12m repeaters = 60.5d)."
    )
    pdf.body(
        "Evidence: see C.4 / Chart 22 (Fig C.4c)."
    )
    pdf.body(
        "Mechanism: Solution 2 timing and success metric use eligible 12m (and ~60d touch) "
        "instead of only crude lifetime repeat."
    )
    pdf.body(
        "Needs: eligibility cutoff (2017-10-17 style) in production; censoring labeled."
    )
    pdf.body(
        "KPI: 12m repeat in treated first-order cohort vs 4.68% H1 baseline "
        "(eligible denominator only)."
    )
    pdf.body(
        "Limitation: cohort rate is not a replacement for crude 96.88%; no claim that "
        "fixing delivery raises retention to a target."
    )

    pdf.ln(2)
    pdf.body(
        "One-line pitch (2016-2018 lens): HVIA helps Olist protect the shared marketplace reputation and "
        "commission economics by predicting late risk before reviews show lower scores, focusing "
        "retention on weak first orders, ranking sellers by health - not by GMV alone - "
        "and sizing late-GMV exposure as labeled scenarios."
    )
    pdf.callout(
        "Bridge to today (hypothesis, not a finding)",
        "If mapped to today's Olist, the same ideas would translate to: late-risk scoring for merchant "
        "shipments via Pax; merchant health as a possible input to Flip underwriting; ETA calibration "
        "inside ERP/Vnda flows. The 2016-2018 evidence does not prove these transfers; they are hypotheses."
    )

    pdf.h2("References (sources actually opened and checked)")
    pdf.body(
        "1) Local Olist order/customer/item/review tables (9 CSVs). 2) Analysis script and generated "
        "tables/charts (all numbers recomputed locally). "
        "3) Locked definitions appendix (grains/denominators). 4) Public Kaggle dataset page for the Olist extract "
        "(dataset identity only). Company facts above are company-reported / approximate / unverified unless labeled; "
        "no web company source was opened for this pass."
    )

    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(
        0, 4,
        "End of Final Integrated Report (A-B-C-E + Tasks 2-6 evidence; D folded into C). "
        "Charts 01-23 with locked definitions appendix. Outreach draft (F) and LinkedIn post remain pending.",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )

    pdf.output(str(OUT))
    print(f"Wrote: {OUT}")
    print(f"Pages: {pdf.page_no()}")


if __name__ == "__main__":
    build()
