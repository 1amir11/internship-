# HVIA Data Analysis Training Task — Submission

**HVIA – Data & AI Solutions** | **Case:** Olist Business Discovery  
**Language:** English | **Dataset:** Olist Store orders, 2016–2018 (aggregator / shared storefront)

> Research → Understand → Analyze → Propose → Communicate.  
> Framing: analyze under the **2016–2018 marketplace aggregator** model; company research may mention today’s ecosystem without forcing 2025–2026 products into every KPI.

---

## Checklist

| # | Requirement | Status | Section |
|---|-------------|--------|---------|
| 1 | Company Research Summary | Done | A |
| 2 | Dataset Understanding & Key Findings | Done | B |
| 3 | Analysis & Business Story | Done | C |
| 4 | Solution Proposal (HVIA) | Done | E |
| 5 | Outreach Message Draft | Todo | F |
| — | Supporting Work | Ready | G |
| — | LinkedIn Milestone Post | Todo | H |

---

# A. Company Research

**Source (full):** `company_research_summary.md`

### Snapshot

| Field | Detail |
|-------|--------|
| Legal name | Olist Serviços Digitais Ltda. (CNPJ 18.552.346/0001-68) |
| Founded | 2014 (commercially active from 2015) |
| Founder & CEO | Tiago Dalvi |
| HQ | Curitiba, Paraná, Brazil (+ São Paulo, Bento Gonçalves) |
| Team | ~790–850 |
| Valuation / funding | $1.5B unicorn (Dec 2021) · $320M+ |
| Merchants / scale | 50,000+ · ~R$60–70B ecosystem invoicing (company-reported) |
| Primary customer | SMB retailers / brands (sellers) |

### Timeline — what was added when

| When | Change |
|------|--------|
| 2007 | Solidarium (pre-Olist) |
| 2014–15 | Olist founded as marketplace bridge for SMBs |
| **2016–18** | **Dataset window:** Olist Store / shared storefront; ~19–21% commission + fees |
| 2019–20 | Clickspace + PAX Logtech (later Olist Pax) |
| 2021 | Tiny ERP + Vnda; unicorn $1.5B |
| 2022–24 | SaaS discipline / higher-margin focus |
| Aug 2025 | Flip → Flip by Olist (credit; FIDC ~R$90M) |
| 2026 | Breakeven path; wind-down of shared marketplace storefront |

### Business model

**Dataset era (2016–2018):** Seller joins Olist → listed under Olist’s verified storefront → customer buys from “Olist” → seller fulfills. Monetization: ~19–21% blended commission + fees.

**Structural risks then:** thin intermediary margins; **reputation contagion** on the shared account; merchant churn as sellers scale; easier direct marketplace onboarding.

**Later / today (context):** Tiny, Vnda, Pax, Flip, PDV, Lis — recurring SaaS-led mix. Competitors (examples): Bling, Nuvemshop, VTEX, Melhor Envio, Magazord.

**Takeaway:** For this task’s data, interpret operations as the **2016–2018 aggregator**. For company research, acknowledge today’s ecosystem without forcing it into every finding.

---

# B. Dataset Understanding & Key Findings

Numbers from `../../archive/` via `../../notebooks/olist_eda.ipynb` / `../../notebooks/olist_full_eda.py`.

### What it is

Public Brazilian e-commerce orders from **Olist Store**, ~**2016-09-04 → 2018-10-17**. Relational extract of ~**99.4k** orders under the aggregator model. **Not included:** ad spend, seller subscription invoices, post-2018 SaaS telemetry.

### Nine tables

| Table | Rows | Role |
|-------|------|------|
| orders | 99,441 | Hub — status + purchase / approval / carrier / delivery / ETA |
| order_items | 112,650 | Line items — product, seller, price, freight (~1.14 / order) |
| customers | 99,441 | Location; `customer_unique_id` = true person (96,096) |
| sellers | 3,095 | Merchant location |
| products | 32,951 | Category, photos, weight/dims |
| payments | 103,886 | Type, installments, value |
| reviews | 99,224 | Score 1–5 + optional text |
| geolocation | 1,000,163 | Lat/lng (many rows per ZIP → mean before distance) |
| category_translation | 71 | Portuguese → English |

```
customers ──< orders >── payments
               ├──< order_items >── products ── category_translation
               │              └── sellers
               └── reviews
ZIP (customer/seller) → geolocation (mean lat/lng per prefix)
```

### Cardinality & quality (must-know)

- Aggregate **item → order** before revenue/SLA/review joins.
- Reviews: nearly 1:1; **551** duplicate `order_id` rows → aggregate score.
- Retention only via **`customer_unique_id`**, not `customer_id`.
- Delivery KPIs: `delivered` + non-null delivery & estimated dates → **96,470** orders (delivered denominator; see `../../docs/definitions.md`).
- Review text sparse (~59% no message) → text themes are a biased subsample.
- Status: ~97% delivered; cancel + unavailable ~1.2% (secondary).

### Exploration snapshot

| KPI | Value |
|-----|-------|
| Product revenue / AOV / freight | R$13.6M (`SUM(price)`) · ~R$138 (per-order mean of Σprice) · ~R$2.3M freight (**14.2%** of total paid; ~**17%** of product; mean item **21.3%**) |
| Late vs ETA | **6.8%** of **96,470** delivered (`delta_days > 0`) |
| Review on-time vs late | **4.29 vs 2.27** (order-level; same late flag / delivered base) |
| One-time buyers | **96.9%** crude full-window one-time rate |
| Top 10% sellers → revenue | ~**67.5%** of `SUM(price)` |
| SP customers / sellers | ~42% / ~60% |
| Payments | Credit card ~74% · boleto ~19% · voucher ~6% |

**Takeaway:** Order-centric ops data. Early story = fulfillment risk + seller concentration on a one-shot customer base → Section C.

---

# C. Analysis & Business Story

**Framing:** 2016–2018 shared storefront — commission (~19–21%) + reputation contagion.  
**Charts (PDF):** selected from `../../outputs/charts/` (story-first, not all 18).  
**Working notes:** `problems_from_analysis.md`

### Story (one paragraph)

The platform **grew fast**, kept **almost no repeat buyers**, and concentrated GMV in a **thin seller elite**, while a minority of **late deliveries** crushed reviews on the **shared marketplace account**. Geography and freight drive fulfillment stress; 1★ comments point to **delivery**, not product. The story is **reputation and unit economics**, not “more charts.”

### C.1 Late delivery destroys satisfaction — critical

| Metric | Value |
|--------|-------|
| Delivered analyzed | **96,470** (status=delivered + both dates non-null) |
| Late vs ETA | **6.8%** of 96,470 delivered (`delta_days > 0`) |
| Review on-time / late | **4.29 / 2.27** (−2.02 stars; order-level, same late flag) |
| Actual vs ETA (mean) | 12.1 vs 23.4 days |
| Corr. days ↔ score | r ≈ −0.33 |

**Meaning:** Small late rate, outsized damage. Shared storefront → reputation contagion. Buffer-heavy ETAs still miss painfully (e.g. high late rates in distant states).  
**Lever:** Treat lateness as **reputation risk**, not a volume footnote.

### C.2 Retention crisis — critical

| Metric | Value |
|--------|-------|
| Unique customers | 96,096 |
| One-time | **96.9%** crude full-window one-time rate |
| 2+ / 3+ | 3.1% / 0.3% |

**Meaning:** Acquisition-led growth; commission LTV barely compounds. One bad first delivery (C.1) can erase order #2.  
**Lever:** Protect the first experience ruthlessly.

### C.3 Seller Pareto + long-tail risk — high

| Metric | Value |
|--------|-------|
| Sellers | 3,095 |
| Top 10% → revenue | **~67.5%** of `SUM(price)` |
| Bottom 50% → revenue | **~3.2%** of `SUM(price)` |

**Meaning:** Elite churn shocks GMV; long-tail shares the same Olist face (low GMV ≠ low reputation risk); support spread across low-yield sellers is inefficient.  
**Lever:** Segment by revenue **and** SLA/review risk.

### C.4 Geo / distance gap — high

| Metric | Value |
|--------|-------|
| SP customers / sellers | ~42% / ~60% |
| Same-state / cross-state delivery | ~7.5 / ~14.7 days (+~7.2) |
| Median / mean distance | ~434 / ~601 km |
| distance ↔ days | r ≈ 0.39 |

**Meaning:** National promise, uneven Brazil; distance feeds lateness (C.1).  
**Lever:** Geo-aware ETA / routing.

### C.5 Freight pressure — medium–high

| Metric | Value |
|--------|-------|
| Freight | R$2.25M — **14.2%** of total paid (primary); ~**17%** of product (secondary) |
| Item freight share of (price+freight) | ~**21.3%** mean item ratio |
| weight ↔ freight | r ≈ 0.61 |

**Meaning:** Shipping is a large slice of what customers pay; freight + late = double hit.  
**Lever:** Freight is strategic (assortment, display, carriers).

### C.6 Review text — supports C.1

Among 1★ comments (keyword scan): delivery/delay **~41%** vs product **~13%**. Median response ~40 hours. Confirms operational root cause; text is underused as an ops signal.

### C.7 Growth & seasonality — context

Peak **2017-11: 7,544** orders; YoY look huge partly from early-base effect. Peaks amplify C.1–C.4. Cancel + unavailable ~1.2% is secondary.

### Priority map → solutions

| # | Problem | Stake (2016–18 model) |
|---|---------|------------------------|
| 1 | Late delivery → review collapse | Shared account reputation |
| 2 | Near-zero repeat | Weak commission LTV |
| 3 | Seller Pareto + long tail | GMV fragility + contagion |
| 4 | Geo / distance SLA | Uneven promise |
| 5 | Freight burden | Price perception + delay sensitivity |

**Bridge:** Fulfillment reliability and seller heterogeneity on a one-shot base → Section E.

---

# E. HVIA Solution Proposal

**Full write-up:** `hvia_task1_section_e_solutions.md`  
**Principle:** *Don’t sell a tool. Find a problem worth solving.*

| # | Problem | Solution | Type |
|---|---------|----------|------|
| 1 | P1 Late / reviews | Predictive Late-Delivery Risk & Response | Core |
| 2 | P2 No repeat | First-Order Retention Risk Flag | Core |
| 3 | P3 Seller Pareto | Seller Health Score | Core |
| 4 | P4 Geo | Geo-aware Dynamic ETA | Supporting → #1 |
| 5 | P5 Freight | Freight-Ratio Catalog Alert | Side |
| 6 | P6 Review text | Review-Text Triage | Supporting → #1, #2 |
| 7 | P7 Seasonality | Seasonal Demand Signal | Supporting → #1 |

**Build order:** #3 with or before #1 → Geo ETA + Seasonal → Review triage → Freight alert.

**Pitch:** Protect shared reputation and commission economics by predicting late risk before reviews collapse, focusing retention on damaged first orders, and ranking sellers by health — not GMV alone.

---

# F. Outreach Draft

*Recipient: Head of Operations / Marketplace at Olist. Channel: LinkedIn message or short email. Language: English.*

> Hi [Name] — I'm an intern with HVIA – Data & AI Solutions. I spent the last weeks on Olist's public 2016–2018 store orders (~99k) and three patterns stood out: (1) only 6.8% of delivered orders arrive after the ETA, yet average reviews drop from 4.29 to 2.27 when they do; (2) 96.9% of customers buy exactly once; (3) the top 10% of sellers drive ~67.5% of product revenue. I sketched three focused responses — late-delivery risk scoring before the ETA is missed, a seller health score beyond GMV, and first-order retention flags. Would you be open to a 20-minute call next week to sense-check whether these match the operational reality you saw? Happy to share the one-page summary. Best, [Your Name]

---

# G. Supporting Work

| Asset | Path |
|-------|------|
| EDA notebook | `../../notebooks/olist_eda.ipynb` |
| EDA script (same logic) | `../../notebooks/olist_full_eda.py` |
| Charts (01–18) | `../../outputs/charts/` |
| Solutions detail | `hvia_task1_section_e_solutions.md` |
| Company research | `company_research_summary.md` |
| Problem notes (AR) | `problems_from_analysis.md` |
| Arabic understanding copy | `hvia_task1_arabic_understanding.md` |
| PDF preview (EN) | `../../outputs/HVIA_Task1_Olist_Preview_A_B_C_E.pdf` |
| Raw CSVs | `../../archive/` |

---

# H. LinkedIn Post

*Todo — milestone post: HVIA task, Olist case, 1–2 discoveries, tools, data↔business, mention **HVIA – Data & AI Solutions** (do not paste the brief).*
