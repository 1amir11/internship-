# E. HVIA Solution Proposal

> Framing: per the case brief ("Don't sell a tool. Find a problem worth solving."), every solution below starts from a specific problem in Section C — not from a technology looking for a use case. Build priority follows Section C.5's bridge: start from problems 1-3 (strongest evidence, highest reputation stakes), then layer in the supporting components that feed them.

## E.1 Solution Map

| # | Problem (from Section C) | Solution | Type | HVIA Domain(s) |
|---|---------------------------|----------|------|-----------------|
| 1 | P1 — Late delivery destroys reviews | Predictive Late-Delivery Risk & Response System | Core | Forecasting & Predictive Solutions, Logistics Intelligence |
| 2 | P2 — Near-zero repeat purchase | First-Order Retention Risk Flag | Core | Customer Intelligence |
| 3 | P3 — Seller concentration (Pareto) | Seller Health Score | Core | Analytics & Decision Systems, AI-Assisted Operations |
| 4 | P4 — Geo / distance SLA gap | Geo-aware Dynamic ETA | Supporting (feeds #1) | Logistics Intelligence |
| 5 | P5 — Freight cost pressure | Freight-Ratio Catalog Alert | Side | Analytics & Decision Systems |
| 6 | P6 — Review text: delivery is the anger theme | Review-Text Triage | Supporting (feeds #1, #2) | Customer Intelligence, AI-Assisted Operations |
| 7 | P7 — Fast growth & seasonality | Seasonal Demand Signal | Supporting (feeds #1) | Forecasting & Predictive Solutions |

---

## E.2 Core Solution 1 — Predictive Late-Delivery Risk & Response System

**Problem it addresses (P1):** Only 6.8% of delivered orders arrive after the ETA, yet the average review score collapses from 4.29 to 2.27 (-2.02 stars) when they do. Under the shared-storefront model, this is reputation contagion on the single Olist account across marketplaces — not an isolated CX issue.

**What it does:** Scores each order, at the point the seller is preparing to ship, for probability of arriving late relative to the *promised* ETA (not just relative to typical transit time — the goal is to catch cases where the generous buffer still won't be enough).

**Inputs:**
- Seller-to-customer distance (r ≈ 0.39 with actual delivery days)
- Customer state / seller state (same-state ≈7.5 days vs cross-state ≈14.7 days)
- Product weight/category (proxy via weight↔freight correlation, r ≈ 0.61)
- Seller's historical on-time rate (see Solution 3 — Seller Health Score)
- Current order-volume load (see E.5.3 — Seasonal Demand Signal)
- *To verify:* whether the dataset includes an explicit shipping-carrier field; if not, drop this feature or approximate via freight-cost-per-km as a proxy.

**Triggered action (tiered by risk score):**
- **Low risk:** no action — standard flow.
- **Medium risk:** proactive notification to the customer with a realistic, revised delivery window, before the standard ETA is missed.
- **High risk** (compounded with a poor Seller Health tier): automatic escalation to the seller to expedite handling, and the order is flagged for priority customer-support follow-up if a delay does occur.

**Expected impact / KPI to track:** Reduction in the review-score gap between on-time and late orders (baseline: -2.02 stars) for the "medium risk, notified" cohort vs. an unnotified control group; secondary KPI: % of high-risk orders that still arrive late despite escalation (should trend down over time as seller behavior adjusts).

**Evidence:** Charts 04, 05, 06, 15.

---

## E.3 Core Solution 2 — First-Order Retention Risk Flag

**Problem it addresses (P2):** 96.9% of customers buy exactly once; only 3.1% return. Growth in the dataset window is acquisition-led — commission is paid once per customer, but lifetime value barely compounds.

**What it does:** At the point a first order completes (delivered + reviewed, or delivered + no review after N days), scores that customer for probability of becoming a repeat buyer, using signals already known about their single order experience. This turns a blanket "please come back" campaign into a targeted list of customers whose experience suggests they are worth a proactive retention touch.

**Inputs:**
- Whether the order was flagged late/high-risk by Solution 1
- The fulfilling seller's Health Score (Solution 3)
- Order value and category
- Review score, if given

**Triggered action:** Customers flagged as high-value + high-churn-risk are routed to a lightweight retention action (e.g., a support check-in or a small proactive gesture) rather than a broad, undifferentiated campaign — keeping the cost of retention proportional to the customer's likely worth.

**Expected impact / KPI to track:** Repeat-purchase rate within the flagged high-risk-but-high-value cohort vs. the 3.1% baseline repeat rate.

**Evidence:** Chart 08.

---

## E.4 Core Solution 3 — Seller Health Score

**Problem it addresses (P3):** The top 10% of sellers generate ~67.5% of product revenue; the bottom 50% generate ~3.2%. Under a shared storefront, a low-revenue seller is not necessarily low-risk — a poor-performing long-tail seller can damage the same account rating as a top seller.

**What it does:** A composite score per seller combining: late-delivery rate, average review score, revenue/GMV contribution, and growth trend. Segments sellers into tiers, e.g.: **Protect & Grow** (elite, low risk), **Monitor** (mid-tier), **At-Risk / Needs Intervention** (any seller — regardless of size — whose delivery/review pattern threatens the shared account).

**Inputs:** Seller-level aggregates of order lateness, review scores, order volume/revenue trend over time.

**Triggered action:** Feeds directly into Solution 1 (a seller's tier becomes a risk feature in the delay model) and into seller relationship management — support and account-management attention is prioritized toward "At-Risk" sellers rather than spread evenly across all 3,095 sellers.

**Expected impact / KPI to track:** Reduction in the revenue share coming from sellers flagged "At-Risk" over time; earlier detection of reputation-risk sellers before damage accumulates in reviews.

**Evidence:** Chart 10.

---

## E.5 Supporting Components

These are not standalone deliverables — they are technical layers that make the three core solutions more accurate. They should be scoped as part of Solutions 1/2/3, not pitched separately.

### E.5.1 Geo-aware Dynamic ETA (feeds Solution 1 — addresses P4)
Replaces a single flat, buffer-heavy national ETA with a per-route estimate built from historical same-state vs. cross-state and distance-bucket delivery times (r ≈ 0.39, distance↔delivery days). This is the mechanism Solution 1 uses to know *what a realistic promise looks like* for a given seller-customer pair, rather than a single company-wide average.
*Evidence: Charts 05, 11, 12, 16.*

### E.5.2 Review-Text Triage (feeds Solutions 1 & 2 — addresses P6)
Among 1-star comments, delivery/delay themes (~41%) far outweigh product/quality themes (~13%), but the median review-response time is ~40 hours. A lightweight text classifier routes newly arriving delivery-related negative reviews to a priority support queue immediately, and doubles as an ongoing feedback loop confirming (or challenging) which features Solution 1 should weight most heavily.
*Evidence: Charts 07, 18.*

### E.5.3 Seasonal Demand Signal (feeds Solution 1 — addresses P7)
Order volume is highly seasonal (e.g., November 2017 peak: 7,544 orders, Black Friday context). During high-volume windows, baseline late-delivery risk rises independent of any single seller or route. This is fed into Solution 1 as an additional risk multiplier during forecasted peak periods, rather than treated as its own deliverable.
*Evidence: Charts 01, 02, 14.*

---

## E.6 Side Solution — Freight-Ratio Catalog Alert (P5)

**Problem it addresses:** Freight totals ~17% of product revenue; at the item level, freight averages ~21% of (price + freight), with some categories (e.g., DVDs/Blu-ray) reaching ~40%.

**What it does:** At the point a product is added or re-priced in the catalog, flags items where the projected freight-to-price ratio exceeds a set threshold, so the merchandising/pricing team can intervene proactively (bundling, minimum order size, alternate carrier negotiation) rather than discovering the problem later through weak conversion or complaints.

**HVIA Domain:** Analytics & Decision Systems.

*Evidence: Charts 12, 13, 17.*

---

## E.7 Suggested Build Order

1. **Solutions 1-3** (core) — build in parallel where possible; Solution 1 depends on Solution 3's Seller Health Score as an input feature, so Solution 3 should ship first or alongside it.
2. **E.5.1 and E.5.3** — technical upgrades to Solution 1's accuracy.
3. **E.5.2** — can ship independently once Solutions 1/2 exist, as it strengthens both.
4. **E.6** — lighter-weight, catalog-level addition; lowest dependency on the others.
