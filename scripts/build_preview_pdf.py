"""
HVIA Task 1 — sequential PDF preview (A + B + C).
Denser first pages; selected charts in Section C.
"""
from pathlib import Path

from fpdf import FPDF, XPos, YPos

OUT = Path(__file__).resolve().parent.parent / "outputs" / "HVIA_Task1_Olist_Preview_A_B_C_E.pdf"
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
            "HVIA  |  Olist Business Discovery  |  Preview A-B-C-E",
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
            # Always surface missing files; never skip silently
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


def build():
    pdf = Doc(format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.set_margins(16, 14, 16)

    # ── PAGE 1: banner + snapshot + both models ──
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
        0, 4.5, "Olist Business Discovery  |  Sections A + B + C + E  |  Preview",
        align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.set_y(28)

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(90, 90, 90)
    pdf.multi_cell(
        0, 4.2,
        "Reading path: A Company  ->  B Dataset  ->  C Analysis  ->  E HVIA Solutions. "
        "Still to come: Outreach (F), LinkedIn (H).",
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

    pdf.h2("A.1 Snapshot")
    pdf.kv_compact(
        [
            ("Field", "Detail"),
            ("Legal name", "Olist Servicos Digitais Ltda. (CNPJ 18.552.346/0001-68)"),
            ("Founded", "2014 (commercially active from 2015)"),
            ("Founder & CEO", "Tiago Dalvi"),
            ("HQ", "Curitiba, Parana, Brazil (+ Sao Paulo, Bento Goncalves)"),
            ("Team size", "~790-850 (after SaaS-oriented restructuring)"),
            ("Valuation / funding", "$1.5B unicorn (Dec 2021)  |  $320M+ (Goldman, SoftBank, Wellington, etc.)"),
            ("Merchants / scale", "50,000+ merchants  |  ~R$60-70B ecosystem invoicing (company-reported)"),
            ("Primary customer", "SMB retailers / brands (sellers); end consumers are demand-side in the CSVs"),
        ]
    )

    pdf.h2("A.2 Dataset-era model (2016-2018) - what the data describes")
    pdf.body(
        "Flow: small seller joins Olist -> products listed under Olist's verified storefront on "
        "major marketplaces -> customer buys from \"Olist\" -> seller fulfills. Monetization: "
        "roughly 19-21% blended commission (marketplace + Olist + payment-related costs) plus "
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
        "Indicative later mix: ~65% recurring SaaS, ~20% fintech/credit, ~10% logistics spread. "
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

    # ── PAGE 2: Timeline + bridge KPIs ──
    pdf.add_page()
    pdf.h1("A.4 Sequential timeline - what was added when")
    pdf.body(
        "Read top to bottom. The 2016-18 band is locked to the public CSV extract. Later rows "
        "explain strategic evolution; they are not additional columns in the order tables."
    )
    pdf.timeline_row(
        "2007",
        "Solidarium: physical retail network supporting artisans and small producers "
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
        "Olist face; commission ~19-21% + fees; ~99k public orders. Shared reputation is the "
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
        "FIDC credit structure (~R$90M). Underwriting edge: ERP sales/invoice signals.",
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
        "Early dataset signals already point to late-delivery review collapse, near-zero "
        "repeat purchase, and seller revenue concentration - expanded next."
    )
    pdf.kv_compact(
        [
            ("Bridge KPI (from CSVs)", "Signal"),
            ("~99.4k orders / ~96k unique buyers", "Scale of the public extract"),
            ("Late vs ETA 6.8% but reviews 4.29 -> 2.27", "Reputation risk > volume risk"),
            ("96.9% one-time buyers", "Acquisition-led growth, weak LTV"),
            ("Top 10% sellers -> ~67.5% product revenue", "GMV + quality concentration"),
        ]
    )

    # ── PAGE 3: Dataset B dense ──
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
        "Category via products + translation (610 products lack category; 13 untranslated).",
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
            ("Review on-time vs late", "4.29 vs 2.27 stars"),
            ("One-time buyers", "96.9%"),
            ("Top 10% sellers -> revenue", "~67.5%"),
            ("SP share (customers / sellers)", "~42% / ~60%"),
            ("Cancel + unavailable", "~1.24% (secondary vs late & loyalty)"),
        ]
    )
    pdf.body(
        "Takeaway: order-centric marketplace ops data. Fulfillment reliability and seller "
        "heterogeneity sit on a one-shot customer base - the cause chain in Section C."
    )

    # ── C ──
    pdf.add_page()
    pdf.h1("C. Analysis & Business Story  |  Cause chain")
    pdf.body(
        "Read as a sequence: growth stress -> logistics and geography -> late deliveries -> "
        "review collapse and written complaints -> weak repeat purchase - amplified by a "
        "concentrated seller base under one shared Olist face."
    )

    pdf.h2("C.1 Growth created operational pressure")
    pdf.body(
        "Orders scaled fast (Jan 2017 -> Jan 2018 YoY ~+809%, with an early-base caveat: "
        "Jan 2017 had only ~800 orders). Peak month Nov 2017: 7,544 orders (Black Friday "
        "context). Cancel + unavailable together ~1.2% - secondary versus lateness and "
        "loyalty. Peaks expose SLA gaps faster than quiet days."
    )
    pdf.figure(
        "01_monthly_order_volume.png",
        "Fig C.1  Monthly order volume - growth and seasonal spike.",
        width=155,
    )

    pdf.h2("C.2 Distance and freight make the promise uneven")
    pdf.body(
        "Sao Paulo holds ~42% of customers and ~60% of sellers. Same-state delivery averages "
        "~7.5 days versus cross-state ~14.7 (+~7.2 days). Median seller-to-customer distance "
        "~434 km (distance <-> delivery days r ~ 0.39). Freight totals ~R$2.3M (~17% of "
        "product revenue); at item level, freight is ~21% of (price + freight)."
    )
    pdf.figure(
        "16_distance_vs_delivery.png",
        "Fig C.2  Distance vs delivery - farther pairs take longer and late more often.",
        width=155,
    )

    pdf.h2("C.3 Late delivery destroys the shared-account score")
    pdf.body(
        "Only 6.8% of delivered orders arrive after the ETA, but average review score falls "
        "from 4.29 (on-time/early) to 2.27 when late (-2.02 stars). Mean actual delivery "
        "~12.1 days versus mean ETA ~23.4 - a large buffer exists, yet misses still hurt. "
        "Under aggregator logic this is reputation contagion on the shared marketplace "
        "account, not a CX footnote. Among 1-star comments (keyword scan), delivery/delay "
        "themes ~41% versus product/quality ~13%."
    )
    pdf.figures_pair(
        "06_delivery_vs_review_scores.png",
        "18_review_text_signals.png",
        "Fig C.3a  Late vs on-time reviews",
        "Fig C.3b  1-star text themes",
    )

    pdf.h2("C.4 Almost no loyalty + a thin seller elite")
    pdf.body(
        "Of 96,096 unique customers, 96.9% buy once and only 3.1% return (2+ orders). "
        "Commission LTV barely compounds; one bad first delivery can erase order #2. "
        "Among 3,095 sellers, the top 10% drive ~67.5% of product revenue while the bottom "
        "50% contribute ~3.2% - GMV dependence and long-tail reputation risk share the "
        "same Olist storefront."
    )
    pdf.figures_pair(
        "08_customer_retention_crisis.png",
        "10_seller_pareto_curve.png",
        "Fig C.4a  One-time vs repeat buyers",
        "Fig C.4b  Seller revenue Pareto",
    )

    pdf.h2("C.5 Priority spine (what to solve next)")
    pdf.kv_compact(
        [
            ("#", "Problem -> business stake (2016-18 model)"),
            ("1", "Late delivery -> review collapse  |  shared marketplace reputation"),
            ("2", "Near-zero repeat purchase  |  CAC paid once, weak LTV"),
            ("3", "Seller Pareto + long tail  |  GMV fragility + contagion"),
            ("4", "Geo / distance SLA gap  |  uneven national promise"),
            ("5", "Freight burden  |  price perception + delay sensitivity"),
        ],
        col_widths=[10, pdf.epw - 10],
    )
    pdf.body(
        "Bridge to HVIA solutions (next section): start from problems 1-3 - predictive delay / ETA, "
        "seller SLA risk scoring, and first-order experience protection - not from a tool list."
    )

    # ── E: Solutions ──
    pdf.add_page()
    pdf.h1("E. HVIA Solution Proposal")
    pdf.body(
        "Principle from the brief: \"Don't sell a tool. Find a problem worth solving.\" "
        "Every solution below starts from a Section C problem. Build priority follows C.5: "
        "core Solutions 1-3 first (strongest evidence, highest reputation stakes), then "
        "supporting layers that feed them, then one lighter side solution."
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
                "Forecasting & Predictive",
            ),
        ],
        col_widths=[8, pdf.epw - 8],
    )

    pdf.h2("E.2 Core 1 - Predictive Late-Delivery Risk & Response (P1)")
    pdf.body(
        "Problem: only 6.8% of delivered orders are late vs ETA, yet reviews fall 4.29 -> 2.27 "
        "(-2.02 stars). Under the shared storefront this is reputation contagion on one Olist "
        "marketplace account - not an isolated CX issue."
    )
    pdf.body(
        "What it does: at ship-prep time, score each order for probability of missing the "
        "*promised* ETA (catch cases where the generous buffer still will not be enough)."
    )
    pdf.bullet(
        "Inputs: seller-customer distance (r~0.39 with days); same-state vs cross-state; "
        "weight/category (weight<->freight r~0.61); seller historical on-time (from Seller "
        "Health); current volume load (Seasonal Demand). Carrier field: verify in data; else "
        "proxy via freight-per-km or drop."
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
    pdf.body("Evidence: charts 04, 05, 06, 15.")

    pdf.h2("E.3 Core 2 - First-Order Retention Risk Flag (P2)")
    pdf.body(
        "Problem: 96.9% of customers buy once; only 3.1% return. Growth is acquisition-led; "
        "commission LTV barely compounds."
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
        "KPI: repeat-purchase rate in the flagged high-risk/high-value cohort vs 3.1% baseline."
    )
    pdf.body("Evidence: chart 08.")

    pdf.h2("E.4 Core 3 - Seller Health Score (P3)")
    pdf.body(
        "Problem: top 10% of sellers -> ~67.5% product revenue; bottom 50% -> ~3.2%. Under a "
        "shared storefront, low GMV does not mean low reputation risk."
    )
    pdf.body(
        "What it does: composite per-seller score (late rate, avg review, GMV contribution, "
        "growth trend). Tiers e.g. Protect & Grow / Monitor / At-Risk - any size seller whose "
        "delivery/review pattern threatens the shared account."
    )
    pdf.bullet(
        "Action: tier feeds Solution 1 as a delay-model feature; account/support attention "
        "prioritizes At-Risk sellers instead of spreading evenly across 3,095 merchants."
    )
    pdf.bullet(
        "KPI: earlier detection of reputation-risk sellers; falling share of GMV from At-Risk "
        "sellers over time as intervention works."
    )
    pdf.body("Evidence: chart 10. Build note: ship #3 first or alongside #1 (#1 needs the score).")

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
        "Evidence: charts 05, 11, 12, 16."
    )

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(30, 60, 100)
    pdf.multi_cell(
        0, 4.8, "E.5.2 Review-Text Triage (P6 -> feeds Solutions 1 & 2)",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.body(
        "Among 1-star comments, delivery/delay themes (~41%) beat product/quality (~13%), yet "
        "median review response is ~40 hours. A lightweight classifier routes new "
        "delivery-related negatives to a priority support queue and feeds which features "
        "Solution 1 should weight. Evidence: charts 07, 18."
    )

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(30, 60, 100)
    pdf.multi_cell(
        0, 4.8, "E.5.3 Seasonal Demand Signal (P7 -> feeds Solution 1)",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.body(
        "Volume is highly seasonal (e.g. Nov 2017 peak 7,544 orders). During peaks, baseline "
        "late risk rises independent of one seller or route. Feed Solution 1 as a risk "
        "multiplier in forecasted high-volume windows. Evidence: charts 01, 02, 14."
    )

    pdf.h2("E.6 Side - Freight-Ratio Catalog Alert (P5)")
    pdf.body(
        "Freight ~17% of product revenue; item-level freight share of (price+freight) ~21%, "
        "some categories ~40% (e.g. DVDs/Blu-ray). At catalog add/reprice, flag items above a "
        "freight-to-price threshold so merchandising can intervene (bundle, min order, carrier "
        "negotiation) before weak conversion. Domain: Analytics & Decision Systems. "
        "Evidence: charts 12, 13, 17."
    )

    pdf.h2("E.7 Suggested build order")
    pdf.kv_compact(
        [
            ("Order", "What to ship"),
            ("1", "Solutions 1-3 (core). Prefer Seller Health (#3) first or parallel with #1."),
            ("2", "E.5.1 Geo ETA + E.5.3 Seasonal signal - upgrade Solution 1 accuracy."),
            ("3", "E.5.2 Review-text triage - strengthens Solutions 1 and 2."),
            ("4", "E.6 Freight catalog alert - light dependency on the rest."),
        ],
        col_widths=[14, pdf.epw - 14],
    )

    pdf.body(
        "One-line pitch: HVIA helps Olist protect the shared marketplace reputation and "
        "commission economics by predicting late risk before reviews collapse, focusing "
        "retention on damaged first orders, and ranking sellers by health - not by GMV alone."
    )

    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(
        0, 4,
        "End of preview (A-B-C-E). Next: Outreach draft (F), LinkedIn post (H). "
        "Full chart set (18) in outputs/charts/. Solution source: hvia_task1_section_e_solutions.md.",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )

    pdf.output(str(OUT))
    print(f"Wrote: {OUT}")


if __name__ == "__main__":
    build()
