# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This project is for inspecting and evaluating websites as potential distributors for **OrientStar Robotics**, which sells cleaning robots. The goal is to qualify distributors based on specific criteria before sales outreach.

## Project Structure

```
possible_distributor_inspection/
├── config/
│   ├── keywords.md       # Product/service keywords by target industry (editable)
│   └── tags.md            # Niche market tag taxonomy (editable)
├── skills/
│   └── distributor-inspector.md  # Main skill for inspecting and scoring websites
├── human_input/
│   ├── competing brands & SKUs.md  # Competitor brands to detect
│   ├── competitor distributors.csv  # Known competitor distributors (skip)
│   ├── serp_results.csv     # Search engine results to process
│   └── possible distributors(consider to merge into the current one).md  # Examples
└── CLAUDE.md                # This file
```

## How to Use

**Inspect a single website:**
```
Use the skill: skills/distributor-inspector.md
Input: URL to inspect
Output: JSON with digest, tags, score, and action recommendation
```

**Key Design:**
1. **Criterion Digest**: LLM extracts key info from website
2. **Categorization**: Applies niche market tags from `config/tags.md`
3. **Scoring**: Required gates + cleaning equipment bonus
4. **Action**: prioritized / standard / explore / exclude / route-to-sales

## Ideal Customer Profile (ICP) - Distributor

### Must-Have Qualification Criteria (Hard Thresholds)

1. **Company Size & Financials**: 20-500 employees, ~€10M annual revenue, strong industry investment commitment
2. **Complete Team Capability**: Must have Sales/BD, Deployment/Delivery, and After-sales/Repair teams
3. **Quantifiable Service SLA**: Can commit to response times and processes (remote support, on-site arrival, spare parts)
4. **Trial/PoC Capability**: Can support 1-week proof-of-concept with on-site training and acceptance
5. **Market Coverage**: Covers at least 1-3 cities in top 10 GDP cities/core economic zones with cross-city service capability
6. **Price Discipline**: Willing to execute MSRP, avoid price dumping as primary means

###加分条件 (Bonus Criteria - Higher Priority)

- Complete distribution network (downstream resellers/tier-2 distributors)
- Secondary development/system integration capability (API/customization/integration)
- Existing customers in property management/FM sector (verifiable cases)
- Local industry resources/influence (property, cleaning services, commercial channels, government/park relations)
- Mature after-sales system: SLA/ticketing/spare parts inventory
- Fixed marketing investment and customer acquisition capability
- Showroom/demo machine management (mobile exhibitions), or clear terminal trial policy
- Competitor channel background (e.g., already representing Pudu/Gaussin) but willing to invest resources

### Target Industries (Priority Order)

1. **Commercial cleaning equipment distributors/agents** (highest priority, those with after-sales teams preferred)
2. **Property management companies** (Facility Management / IFM)
3. **Cleaning service contractors** (outsourced cleaning companies)
4. **System integrators / commercial robot distributors**
5. **Home appliance/consumer electronics distributors** (must have ToB distribution network and B2B delivery capability)

### High-Potential End-User Scenarios

- National retail chains/supermarkets/drug stores (single customer can scale quickly)
- Office buildings/commercial real estate/parks (centralized procurement + multi-point reuse)
 - Hotels/medical/chain stores (high cleaning frequency, easier ROI calculation)

### Exclusion Criteria

- **Renovation/decoration companies**: Core business is renovation, weak relevance to robotics business
- **Pure 2C retail-oriented**: No ToB channels or B2B delivery capability
- **Too small or no team**: <20 employees, no delivery/after-sales teams ("shell companies")
- **Learning-oriented individuals/sole operators**: Cannot commit to delivery and after-sales short-term
- **Free sample seekers**: Unwilling to invest in demos/trials
- Companies without clear path to key decision-makers

### Value Proposition Messaging

When reaching out to distributors, lead with:

1. **Profitable (Flexible Business Model)**: Support distributors in promoting leasing (RaaS) model to avoid price wars and gain recurring revenue; guaranteed margin + multiple profit points (maintenance/operations/consumables/additional equipment/secondary development services)
2. **Easy Delivery (Solve Deployment Challenges)**: Address competitors' slow deployment and difficult environment modifications - highlight "plug-and-play, no complex plumbing modifications, deployment completed within 1 day"
3. **Fast Service (Eliminate After-sales Concerns)**: Address European market sensitivity to after-sales/SAV - emphasize clear SLA, remote technical support mechanism, spare parts and consumables support, and building local service capability with distributors
4. **Controlled Delivery & Inventory**: European warehouse/fast replenishment + actionable forecast/stocking collaboration mechanism to reduce inventory risk and delivery anxiety for project-oriented distributors
5. **Market Support (Build Brand Together)**: For high-quality exhibitions/online customer acquisition, can provide joint exhibition, market fund/subsidy policies (subject to contract signing and performance)
6. **Product Strength Directly Addresses Pain Points**: Prioritize promoting "fully automated" high-end configurations (e.g., automatic water station/manual water dumping reduction) to reduce "doesn't seem intelligent" resistance

### Key Qualification Questions (10-Minute Screen)

1. What cleaning robot/cleaning equipment brands do you currently primarily promote? Are you representing Pudu/Gaussin?
2. What is your local deployment/after-sales team configuration? Which cities do you cover? Can on-site arrival be achieved within 2-3 business days?
3. Do you have spare parts/consumables inventory and ticketing mechanisms? Are you willing to establish a minimum spare parts package?
4. What is your customer acquisition method (exhibitions/advertising/channels/key accounts)? Do you have a fixed marketing budget?
5. Do you require exclusivity? If so: What annual commitment, market investment, demo machines/stock are you willing to commit to?
6. How long does terminal advancement usually require for trial? Can you provide 1-week PoC and be responsible for training/acceptance?
7. What are your expectations for inventory/delivery? Are you accepting European warehouse replenishment + rolling forecast collaboration?

### Country Strategic Priority

- **France (FR)**: Prioritize "competitor distributors (especially Pudu) → 3C/IT channels (China brand cooperation experience)"
- **Spain (ES)**: Many project/solution-oriented partners, generally concerned about inventory risk; high requirements for after-sales technical support response
- **Germany (DE)**: Head channels lean toward "solutions + service providers", usually require 4-8 weeks of rigorous testing before listing
- Also prioritize: **Hungary, Switzerland, Greece**

### Exclusive Negotiation Rules

**Exclusivity is an exchange, not a give.** Exclusive = distributor's annual commitment + market investment + service investment + price discipline.

- Prefer `scope exclusivity` (by industry/channel/product line/region) or `phased exclusivity` (pilot 90-180 days → meet target → convert to exclusive)
- Hard conditions for exclusivity: annual/quarterly KPI + first order demo/stock requirements, marketing plan and investment amount, after-sales SLA, price discipline (MSRP/MAP), review rhythm
- Demo strategy: firmly avoid "unconstrained free demo machines"; use `demo special price` or `paid trial deductible`

## Qualification Framework

When evaluating a website as a potential distributor:

1. **Hard Threshold Check**: Verify company size (20-500 employees), team completeness (sales + deployment + after-sales), and SLA capability
2. **Target Industry Match**: Check if they operate in commercial cleaning equipment, property management, cleaning services, or system integration
3. **Exclusion Screening**: Ensure they are not renovation-focused, pure retail, or too small
4. **Value Proposition Fit**: Assess if they can benefit from RaaS model, fast deployment, and after-sales support
5. **Country Context**: Consider strategic priorities and local market conditions (France/Spain/Germany/Hungary/Switzerland/Greece)
