# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This project is for inspecting and evaluating websites as potential distributors for **OrionStar Robotics**, which sells cleaning robots. The goal is to qualify distributors based on specific criteria before sales outreach.

## Project Structure

```
skills/
├── lead-classifier/              # Classifies industry + routes to inspector (ENHANCED)
├── shared-references/            # All shared markdown docs (NEW)
│   ├── icp/                      # ICP files (hard-gates, scoring, etc.)
│   ├── country-strategies.md
│   ├── target-segments.md
│   ├── cross-routing.md
│   ├── image-analysis-guide.md
│   └── industry-taxonomy.md      # Fixed industry dictionary (NEW)
├── shared-scripts/               # Python utilities (RENAMED)
│   ├── serp_search.py           # Unified SERP search
│   └── brightdata_utils.py
├── distributor-inspector/        # Evaluates resellers/distributors
├── ka-inspector/                 # Evaluates key account end customers
├── channel-partner-inspector/    # Evaluates channel partners
└── lead-enricher/                # Enriches CSV leads with website data
```

## How to Use

### Full Pipeline: CSV Leads → CRM (Recommended)

**Use this when you have leads WITHOUT websites** (names, companies, emails only):

```
# Step 1: Enrich CSV with website data (2-5 min)
cd skills/lead-enricher
python3 scripts/enrich.py /path/to/leads.csv

# Input CSV format (tab-delimited):
# full_name	company_name	work_phone_number	work_email
# Sven Haubert	Reha360	+4951418879605	Office@reha360.de

# Output: leads_enriched.csv with website URLs, LinkedIn profiles

# Step 2: Classify each URL for industry + routing (30s per URL)
Use the Skill tool with: lead-classifier
Input: Each website URL from enriched CSV
Output:
  - primary_industry: e.g., 商超 (Retail)
  - secondary_industry: e.g., 商超终端方向-KA
  - lead_type: distributor/ka-end-user/channel-partner
  - route_to: recommended inspector skill

# Step 3: Run recommended inspector on qualified leads (60s per URL)
Use the Skill tool with: {recommended-inspector}
Input: URL to inspect
Output: Full scored report with action recommendation

# Step 4: Manual CRM insertion
Copy classification output (primary_industry, secondary_industry, lead_type) to CRM
```

### Single URL Workflow

**If you already have a website URL:**
```
# Step 1: Classify (30s)
Use the Skill tool with: lead-classifier
Input: URL to classify
Output: Industry classification + routing recommendation

# Step 2: Inspect (60s)
Use the Skill tool with: {recommended-inspector}
Input: URL to inspect
Output: Full scored report
```

**If you DON'T have a website URL (only company name, email, or person info):**
```
# Step 1: Enrich the lead first
Use the Skill tool with: lead-enricher
Input: CSV with company_name, work_email, full_name
Output: CSV with website URL found

# Step 2: Classify (30s)
Use the Skill tool with: lead-classifier
Input: URL from enriched output
Output: Industry classification + routing recommendation

# Step 3: Inspect (60s)
Use the Skill tool with: {recommended-inspector}
Input: URL to inspect
Output: Full scored report
```

**Direct inspection (if you already know lead type):**
```
Use the Skill tool with: distributor-inspector / ka-inspector / channel-partner-inspector
Input: URL to inspect
Output: Full scored report
```

---

## Workflow Decision Tree

```
What input do you have?
│
├─ Website URL
│   └─→ Run: lead-classifier → inspector → CRM
│
├─ Company name only
│   └─→ Run: lead-enricher (finds website) → lead-classifier → inspector → CRM
│
├─ Email address
│   └─→ Run: lead-enricher (finds website) → lead-classifier → inspector → CRM
│
├─ Person name + company name
│   └─→ Run: lead-enricher (finds website + LinkedIn) → lead-classifier → inspector → CRM
│
└─ CSV with multiple leads (names, companies, emails)
    └─→ Run: lead-enricher (batch) → lead-classifier (each URL) → inspector → CRM
```

**Key point:** `lead-classifier` requires a URL. If you don't have one, run `lead-enricher` first.

---

**Prerequisites:**
```bash
# Install shared utilities
cd skills/shared-scripts
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Configure API key (shared across all skills)
# Create: ~/.claude/config.json
{
  "brightdata_api_key": "your-api-key-here"
}
```

## Routing Workflow

**Recommended:**
1. Run `lead-classifier` (30s) → Get industry classification + routing recommendation
2. Run recommended inspector skill (60s) → Get scored report
3. Copy industry fields to CRM

**Efficiency:** 50% faster than sequential trial

**Output fields from lead-classifier:**
| Field | Example | Purpose |
|-------|---------|---------|
| `primary_industry` | 商超 (Retail) | CRM industry category |
| `secondary_industry` | 商超终端方向-KA | CRM sub-industry |
| `lead_type` | ka-end-user | Business model type |
| `route_to` | ka-inspector | Next action |

**Manual routing (if classifier unavailable):**
- Sells products → distributor-inspector
- Operates facilities → ka-inspector
- Has client relationships → channel-partner-inspector

---

## Use Case: 商超 (Supermarket/Retail) Classification

**Scenario:** You have a lead list of supermarket chains and need to classify them for CRM.

**Example 1: Retail Chain (KA End-User)**
```
Input URL: real-supermarkt.de

Step 1: Run lead-classifier
Output:
  - Primary Industry: 商超 (Retail)
  - Secondary Industry: 商超终端方向-KA
  - Lead Type: ka-end-user
  - Route To: ka-inspector

Step 2: Run ka-inspector (because route_to = ka-inspector)
Output: Full scored report with pilot-readiness assessment

CRM Fields:
  primary_industry = "商超"
  secondary_industry = "商超终端方向-KA"
  lead_type = "ka-end-user"
```

**Example 2: Single Retail Store (Individual)**
```
Input URL: kleine-laden-berlin.de

Step 1: Run lead-classifier
Output:
  - Primary Industry: 商超 (Retail)
  - Secondary Industry: 商超终端方向 - 个体
  - Lead Type: ka-end-user
  - Route To: ka-inspector (or exclude if too small)

CRM Fields:
  primary_industry = "商超"
  secondary_industry = "商超终端方向 - 个体"
```

**Example 3: Cleaning Equipment Distributor (sells to supermarkets)**
```
Input URL: cleaning-equipment-de.de

Step 1: Run lead-classifier
Output:
  - Primary Industry: 清洁 (Cleaning)
  - Secondary Industry: 清洁代理商 - 机械类
  - Lead Type: distributor
  - Route To: distributor-inspector

CRM Fields:
  primary_industry = "清洁"
  secondary_industry = "清洁代理商 - 机械类"
  lead_type = "distributor"
```

**Decision Logic:**
| Company Type | Primary | Secondary | Route To |
|--------------|---------|-----------|----------|
| Supermarket chain (50+ locations) | 商超 | 商超终端方向-KA | ka-inspector |
| Single supermarket | 商超 | 商超终端方向 - 个体 | ka-inspector |
| Retail chain (non-supermarket) | 商超 | 商超终端方向-KA | ka-inspector |
| Cleaning equipment seller | 清洁 | 清洁代理商 - 机械类 | distributor-inspector |
| FM service provider | 服务行业 | 服务代理商 | channel-partner-inspector |

**Manual Inspection:**
```bash
# Navigate to URL
playwright-cli open {url} --persistent -s=inspector

# Capture snapshot (YAML appears in stdout)
playwright-cli snapshot -s=inspector

# Claude extracts, scores, and outputs full report
```

**Batch Inspection (50 URLs):**
```bash
# Initialize persistent session
playwright-cli open about:blank --persistent -s=inspector

# For each URL:
playwright-cli goto {url} -s=inspector
playwright-cli snapshot -s=inspector
# Claude processes each snapshot inline

# Cleanup (optional)
playwright-cli close-all -s=inspector
```

**Installation (Marketplace):**
```bash
/plugin marketplace add thaddeus-git/b2b
/plugin install b2b@b2b
```

**Manual Installation:**
```bash
# Copy to project
cp -r skills/distributor-inspector /path/to/project/.claude/skills/

# Or copy globally
cp -r skills/distributor-inspector ~/.claude/skills/
```

**Key Design:**
1. **Criterion Digest**: LLM extracts key info from website
2. **Categorization**: Applies niche market tags from `references/tags.md`
3. **Scoring**: Required gate + bonuses (cleaning equipment + competitor footprint + channel capability, capped at 100)
4. **Action + Play**: prioritize / standard / explore / exclude / route-to-sales (with competitive-conversion play when applicable)

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
  - **Exception:** If they ALSO sell commercial/industrial products → NOT excluded, score normally
  - Example: A shop selling home robot vacuums AND warehouse scrubbers is a valid prospect
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

**IMPORTANT (Tier 1):** DE, FR, IT, UK, HU

**OTHERS (Tier 2):**
- Europe: AT, NL, BE, ES, SE, PL, IE
- APAC: SG, TH, MY, ID, PH, VN, TW, AU, NZ
- MENA: AE, SA, QA, KW, OM, BH, TR, IR, IQ, EG
- Americas: US, CA, MX, CO, CL, PE, BR, AR
- Africa: ZA

See `skills/distributor-inspector/references/icp-sales/country-strategies.md` for detailed strategies.

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
5. **Country Context**: Consider strategic priorities and local market conditions (see country-strategies.md for all 35+ markets)

## Multi-Skill Workflows

### Full Pipeline: Search + Inspect

```
# Step 1: Search for distributors (using your preferred method)
# e.g., manual search, or use the Bright Data SERP API script directly:
python3 skills/distributor-inspector/scripts/search.py "cleaning robot distributor France" "FR" "fr" "20"

# Step 2: Batch inspect
Use distributor-inspector skill on each URL

# Step 3: Validate top prospects (optional)
python3 skills/distributor-inspector/scripts/search.py "{company} news 2024" "FR" "fr" "5"
```

### API Cost Awareness
- Search script uses paid Bright Data API
- Each search consumes quota
- Use distributor-inspector first (free), then enrich selectively

## Release Process

Use the release script to create new versions. This ensures `plugin.json` version stays synced with git tags.

```bash
./scripts/release.sh 1.4.5
```

The script will:
1. Update `.claude-plugin/plugin.json` version
2. Commit the change
3. Create an annotated git tag
4. Push to origin (commit + tag)
5. Create a GitHub release with auto-generated notes

**Prerequisites:**
- Clean working directory (no uncommitted changes)
- `gh` CLI authenticated with GitHub

## Release Workflow (Correct Order)

**Important:** Stage your feature changes but do NOT commit them before releasing.

```bash
# 1. Make your changes and stage them (DO NOT COMMIT)
git add skills/distributor-inspector/SKILL.md

# 2. Create release (script bundles staged changes + version bump)
./scripts/release.sh 1.8.0

# 3. Script auto-pushes (main + tag) - done!
```

**Why this order matters:**

The release script bundles your staged changes into the version bump commit, keeping history clean and satisfying the pre-push hook.

**Common Issues:**

| Error | Cause | Fix |
|-------|-------|-----|
| "Uncommitted changes" | Unstaged modifications | `git add .` to stage, then run release |
| "Unstaged changes" | Files modified but not staged | `git add .` or `git stash` |
| Version already released | Tag exists for current version | Bump version: `./scripts/release.sh 1.4.9` |
| `.DS_Store` blocking | macOS system file tracked | Run once: `git rm --cached .DS_Store && git commit -m "chore: untrack DS_Store"` |

**If you already committed features (wrong order):**

```bash
git reset --soft HEAD~1             # Uncommit, keep changes staged
./scripts/release.sh 1.8.0          # Now works correctly
# Script auto-pushes
```

**To untrack `.DS_Store` permanently (run once):**

```bash
git rm --cached .DS_Store
git commit -m "chore: stop tracking .DS_Store"
git push origin main
```
