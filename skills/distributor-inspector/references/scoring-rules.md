# Scoring Rules for Distributor Inspector

## Scoring Components

| Component | Points |
|-----------|--------|
| Required: Sells as expected | PASS/FAIL |
| Bonus: Customer overlap | +0 to +50 |
| Bonus: Cleaning equipment | +30 to +90 |
| Bonus: Competitor footprint | +30 to +90 |
| Bonus: Channel capability | +0 to +20 |

> **Total score capped at 100.**

## Grade & Action Mapping

| Grade | Score | Condition | Action |
|-------|-------|-----------|--------|
| A | 90+ | PASS gate | prioritize |
| B | 70-89 | PASS gate | standard |
| C | 50-69 | Any | explore |
| D/F | <50 | Any | exclude |
| — | — | Tier 1-2 competitor | route-to-sales |
| — | — | cleaning-services-provider | service-provider-prospect |
| — | — | hospitality-service-provider | route-to-ka |
| — | — | pure-2c-retail ONLY | exclude |

**Special routing (overrides score):**
- Tagged `pure-2c-retail` with NO commercial products: `exclude` - B2C only, no ToB channels
- Tier 1-2 competitor footprint: `route-to-sales` + `competitive-conversion` play
- Tagged `cleaning-services-provider`: `service-provider-prospect`
- Tagged `hospitality-service-provider`: `route-to-ka`

**Note:**
- Companies tagged `pure-2c-retail` that ALSO sell commercial/industrial products should be scored normally
- Companies that FAIL the gate but score 50+ via customer overlap + channel capability route to `explore`

---

## Commercial Products Check (Pre-Scoring)

Before applying scores, check for commercial products:

**If tagged `pure-2c-retail` AND NO commercial products → Skip scoring, route to `exclude`**

**If tagged `pure-2c-retail` BUT has commercial products → Continue scoring (valid prospect)**

**Commercial product signals:**
- Cleaning equipment (commercial scrubbers, sweepers, industrial vacuums)
- Facility management products
- Janitorial supplies
- Robotics/automation equipment
- Any B2B/wholesale product lines

---

## Cleaning Equipment Bonus

| Level | Evidence | Points |
|-------|----------|--------|
| Light | Mentions cleaning equipment | +30 |
| Moderate | Has product category | +50 |
| Strong | Core offering, multiple products | +70 |
| Dominant | Primary business, extensive catalog | +90 |

**Detection signals:**
- Product pages with commercial cleaning machines
- Multiple equipment categories (scrubbers, sweepers, vacuums)
- Brand portfolio of cleaning equipment
- "Professional" or "industrial" cleaning focus

---

## Competitor Footprint Bonus

| Tier | Evidence | Points | Example |
|------|----------|--------|---------|
| Tier 1 | Official distributor / Authorized partner language | +90 | "Official distributor of PUDU", "Authorized Gausium partner" |
| Tier 2 | Product pages / Sales evidence | +60 | Product listings, competitor SKU/model names |
| Tier 3 | Mentions only | +30 | Blog posts, comparisons, "compatible with..." |

**Why competitor footprint is a TOP signal:**

Competitor distributors are the BEST prospects because they already have:
- Customer base in cleaning robotics
- Sales and deployment teams trained on robots
- After-sales service capability
- Market knowledge and relationships
- Proven willingness to invest in robot inventory

**This is MORE valuable than generic cleaning equipment sales** because the jump from cleaning equipment to robots is harder than switching robot brands.

---

## Channel Capability Bonus

| Points | Evidence |
|--------|----------|
| +5 | 1 capability signal |
| +10 | 2 capability signals |
| +20 | 3+ signals OR explicit service/repair/spare parts/training page |

**Signals to detect:**
- **After-sales**: spare parts, maintenance, technical support, repair
- **Showroom/Demo**: showroom, demonstration, test drive, trial
- **Multiple brands**: "brands", "distributors of", "authorized dealer"
- **Multiple categories**: equipment + supplies + accessories
- **Clear SLA**: 24/48h response time, service guarantee

---

## Customer Overlap Bonus

Award points for serving target customers that OrientStar robots would clean.

| Level | Evidence | Points |
|-------|----------|--------|
| None | No target customer mentions | +0 |
| Light | One target customer type mentioned | +20 |
| Moderate | 2+ types OR recurring focus | +35 |
| Strong | Core customer base is target sectors | +50 |

**Target customer categories:**
- **Warehouses/Logistics:** warehouse, logistics, distribution center, fulfillment, storage, depot
- **Factories/Industrial:** factory, manufacturing, industrial, production, plant
- **Property/FM:** property management, facility management, building services, real estate
- **Retail chains:** supermarket, retail chain, stores, multi-site

**Detection approach:**
- Look for customer testimonials, case studies, "our clients" sections
- Check service descriptions for target industries
- Identify mentions of warehouse/logistics/factory/retail customers

**Important:** This bonus applies regardless of whether "sells as expected" passes or fails. A forklift distributor serving warehouses can score 50+ through customer overlap + channel capability alone.

---

## Competitor Detection

Check `references/competing-brands.md` for brands to detect:
- Pudu, Gausium, LionsBot, Tennant, Nilfisk, Kärcher, Adlatus, ICE Cobotics, SoftBank, Avidbots

**When competitor products found:**
1. Apply `competitor-robot-distributor` tag
2. Score competitor footprint tier (+30 to +90 bonus)
3. Route to sales with play label:

| Tier | Bonus | Action | Play | Sales Approach |
|------|-------|--------|------|----------------|
| Tier 1 | +90 | route-to-sales | `competitive-conversion` | "You're already a robot distributor. Here's why adding OrientStar grows your margin and de-risks your supply chain..." |
| Tier 2 | +60 | route-to-sales | `competitive-conversion` | "You're selling [competitor]. Here's what OrientStar does better for [specific use case]..." |
| Tier 3 | +30 | route-to-sales or prioritize | `competitive-conversion` | "You mentioned [competitor]. Let's discuss how OrientStar complements or replaces that..." |
