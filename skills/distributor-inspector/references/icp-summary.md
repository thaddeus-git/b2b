# ICP Summary: Quick Reference

> **For:** Sales team and AI skill implementation
> **Version:** 1.0
> **Updated:** 2026-02-27

---

## Hard Gates (All Required - Fail Any = Exclude or Downgrade)

| Gate | Requirement | AI Detection Method | Pass Threshold |
|------|-------------|---------------------|----------------|
| **Company Size** | 20-500 employees | About page, Impressum, LinkedIn, team list | 20 ≤ count ≤ 500 |
| **Financial Scale** | ~€10M annual revenue | Revenue mentions, "X million", turnover | ≥ €5M (soft), ≥ €10M (ideal) |
| **Sales/BD Team** | Dedicated sales function | "sales", "BD", "commercial", "Vertrieb" | Named sales contacts or team section |
| **Deployment Team** | Installation/delivery capability | "installation", "deployment", "implementation" | Service page with deployment offering |
| **After-sales Team** | Service/repair capability | "service", "repair", "maintenance", "SAV", "Kundendienst" | Dedicated service section |
| **SLA Capability** | Quantifiable response times | "24h", "48h", "SLA", "response time", "délai" | Specific time commitment mentioned |
| **PoC Capability** | Can support 1-week trials | "demo", "trial", "test", "showroom", "PoC" | Demo/trial policy or showroom |
| **Market Coverage** | 1-3 cities in economic zones | Multiple locations, service area mentions | Cross-city capability shown |
| **Price Discipline** | Willing to execute MSRP | "MSRP", "MAP", "authorized dealer", price policy | Brand partnership language |

**Gate Logic:**
- **ALL PASS** → Proceed to bonus scoring (eligible for A/B grade)
- **1-2 FAIL** → Cap max score at 50 (explore tier only)
- **3+ FAIL** → Route to `exclude` regardless of other signals

---

## Bonus Criteria (More = Higher Score, Capped at 100)

| Criterion | Max Points | Detection Signals |
|-----------|------------|-------------------|
| Cleaning equipment focus | +90 | Product catalog, multiple categories |
| Competitor footprint | +90 | Pudu/Gausium/LionsBot brand partnerships |
| Distribution network | +20 | "distributors", "resellers", "partners" page |
| System integration capability | +20 | "integration", "API", "customization", "solutions" |
| Existing FM/property customers | +15 | FM case studies, property management clients |
| After-sales maturity | +15 | SLA page, spare parts inventory, ticketing |
| Demo/showroom capability | +10 | Showroom, demo center, test drive mentions |
| Marketing investment | +10 | Budget mentions, exhibition participation |
| Customer overlap | +50 | Target end-user customers in portfolio |

---

## Target Industries (Priority Order)

1. **Commercial cleaning equipment distributors** - Highest priority, already have after-sales teams
2. **Property management / FM companies** - Direct access to end-user scenarios
3. **Cleaning service contractors** - Outsourced cleaning, may need delivery partners
4. **System integrators / commercial robot distributors** - Tech capability, existing robot knowledge
5. **Consumer electronics** - Must have B2B/wholesale division (check for commercial products)

---

## Customer Overlap Categories

| Category | Included Segments | Max Points |
|----------|-------------------|------------|
| Industrial | Warehouse, factory, logistics, manufacturing, distribution center | +15 |
| Commercial Real Estate | Office buildings, property management, parks, facilities | +15 |
| Retail | Supermarkets, retail chains, multi-site stores, drug stores | +15 |
| Hospitality | Hotels, restaurants, healthcare, senior living | +10 |
| Public/Institutional | Schools, government, airports, museums | +10 |

**Scoring:** +10 per category with evidence, capped at +50

### Named Enterprise Client Bonus

| Signal | Points | Max |
|--------|--------|-----|
| Named enterprise client in target segment (Fortune 500, DAX 40, etc.) | +10 per client | +30 |

**Examples:** DB Schenker, BMW, Siemens, Schneider Electric, Carrefour

---

## Manual Review Flag

**Rule:** If company routes to `exclude` BUT has named enterprise clients → Flag for human verification

**Output:** Add "⚠️ Manual Review Suggested" section with client names and potential value

---

## Exclude Criteria

- **Renovation/decoration companies** - Core business is construction, weak robotics relevance
- **Pure B2C retail** - No ToB channels, no commercial products (e.g., only robot vacuums for home)
- **Too small** - < 20 employees, no team structure ("shell companies")
- **No key decision-makers** - Cannot identify sales/technical leadership
- **Free sample seekers** - Unwilling to invest in demos/trials

---

## Country Strategies

| Country | Priority Focus | Scoring Adjustment |
|---------|----------------|-------------------|
| **France (FR)** | Competitor distributors, 3C/IT with China brand experience | Competitor footprint +10 bonus |
| **Spain (ES)** | Project-oriented partners, solution providers | After-sales maturity +10 bonus |
| **Germany (DE)** | Solution providers, technical evaluators | Expect 4-8 week testing, don't penalize |
| **Hungary (HU)** | Emerging market, growth potential | Standard scoring |
| **Switzerland (CH)** | High-value partners, quality focus | Standard scoring |
| **Greece (GR)** | Emerging market | Standard scoring |

---

## Action Routing

| Grade | Score Range | Gates Met | Action |
|-------|-------------|-----------|--------|
| A | 90-100 | All | prioritize |
| B | 70-89 | All | standard |
| C | 50-69 | Any | explore |
| D/F | < 50 | Any | exclude |
| — | Any | Competitor distributor | route-to-sales |
| — | Any | cleaning-services-provider | service-provider-prospect |
| — | Any | hospitality-service-provider | route-to-ka |

---

## Value Proposition by Prospect Type

| Prospect Type | Lead With | Secondary Message |
|---------------|-----------|-------------------|
| Competitor distributor | Supply chain diversification, margin improvement | Plug-and-play deployment advantage |
| Cleaning equipment distributor | Recurring revenue (RaaS), service contracts | Fast deployment vs. competitors |
| FM/Property company | Direct ROI, labor cost reduction | No infrastructure modification needed |
| System integrator | Customization capability, API access | Technical support, training |
| New to robotics | Turnkey solution, low-risk entry | Marketing support, lead generation |
