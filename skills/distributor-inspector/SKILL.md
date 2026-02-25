---
name: distributor-inspector
description: Use when evaluating websites as potential distributors for OrientStar Robotics (cleaning robots). Requires crawl4ai Docker server. Use when needing to score companies against ICP criteria, categorize by niche market, or identify competitor distributors for sales outreach. Supports batch processing.
---

# Distributor Inspector

Inspect and score potential distributor websites for OrientStar Robotics (cleaning robot sales).

## Overview

Evaluates websites against ICP criteria, categorizes by niche market using standardized tags, and routes to appropriate action (prioritize/standard/explore/exclude/route-to-sales).

## Prerequisites

This skill requires **crawl4ai** for website content extraction.

### Quick Start

1. Ensure Docker is installed and running
2. Start the crawl4ai server:
   ```bash
   ./scripts/crawl4ai-server.sh start
   ```
3. Verify the server is running:
   ```bash
   ./scripts/crawl4ai-server.sh status
   ```

### Manual Setup (Alternative)

```bash
docker run -d --name crawl4ai -p 11235:11235 unclecode/crawl4ai:latest
```

The server runs on `http://localhost:11235` with the `/crawl` endpoint.

For enrichment searches, this skill uses the **google-search** skill (Bright Data SERP API). Ensure it's configured with valid API credentials.

## When to Use

```dot
digraph use_flowchart {
    "Need to evaluate distributor website?" [shape=diamond];
    "Use distributor-inspector" [shape=box];

    "Need to evaluate distributor website?" -> "Use distributor-inspector" [label="yes"];
}
```

**When to use:**
- Evaluating potential distributors from search results
- Qualifying websites for sales outreach
- Identifying competitor distributors (Pudu, Gausium, LionsBot, etc.)
- Categorizing companies by niche market

## Tag Format

`{primary-product-category}-{business-model}`

**Multiple tags allowed:** If a distributor sells cleaning robots specifically (e.g., "Reinigungsroboter", "robot de nettoyage", "robot pulitore"), apply both `cleaning-equipment-distributor` AND `robotics-distributor`.

**Product categories:** cleaning-equipment, cleaning-supplies, facility-management, cleaning-services, robotics, industrial-equipment, hospitality-supplies, general-merchandise

**Business models:** distributor, wholesaler, retailer, service-provider, system-integrator, manufacturer

**Special tags:** competitor-robot-distributor, pure-2c-retail

See `references/tags.md` for complete taxonomy.

## Scoring

| Component | Points |
|-----------|--------|
| Required: Sells as expected | PASS/FAIL |
| Bonus: Customer overlap | +0 to +50 |
| Bonus: Cleaning equipment | +30 to +90 |
| Bonus: Competitor footprint | +30 to +90 |
| Bonus: Channel capability | +0 to +20 |

> **Total score capped at 100.**

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

## Output Format

**Markdown format** for human and AI readability:

```markdown
## {company_name} - {grade} ({score}/100)

**URL:** {url}
**Tags:** {tag1}, {tag2}
**Action:** {action}
**Play:** {play} (optional - only if competitor footprint detected)

### Company Profile
- **Products:** {products}
- **Services:** {services}
- **Brands:** {brands}
- **Geography:** {geography}
- **Team:** {team_presence}
- **SLA:** {sla_mentions}

### Key Signals
{signals_list}

### Scoring Details

| Component | Result | Points |
|-----------|--------|--------|
| Sells as expected | {pass/fail with reason} | — |
| Customer overlap bonus | {level with evidence} | +{bonus} |
| Cleaning equipment bonus | {level with evidence} | +{bonus} |
| Competitor footprint bonus | {tier with evidence} | +{bonus} |
| Channel capability bonus | {signals detected} | +{bonus} |
| **Total** | (capped at 100) | **{total}** |

### Sales Play (if applicable)
{play_name}: {play_description}
```

**For service-provider-prospect (cleaning services):**

```markdown
## {company_name} - service-provider-prospect

**URL:** {url}
**Tags:** cleaning-services-provider
**Action:** service-provider-prospect

### Company Profile
- **Services:** {services}
- **Equipment used:** {equipment_brands_if_known}
- **Team:** {team_size}
- **Geography:** {geography}

### Note
This is a cleaning SERVICE provider, not an equipment distributor. They may be interested in:
- Purchasing robots for their own operations
- Becoming a referral partner
- Insights into local cleaning market
```

**For route-to-ka (hotel chains / Key Accounts):**

```markdown
## {company_name} - route-to-ka

**URL:** {url}
**Tags:** hospitality-service-provider
**Action:** route-to-ka

### Company Profile
- **Type:** Hotel chain / hospitality group
- **Locations:** {number_of_properties}
- **Geography:** {geography}

### Key Account Potential
This is a potential Key Account (end customer), not a distributor.

**Next step:** Use `KA-inspector` skill to evaluate as Key Account.
```

**For batch results**, compile into summary table:

```markdown
# Distributor Inspection Results

## Action Summary

| Action | Count | Companies |
|--------|-------|-----------|
| prioritize | X | {list} |
| standard | X | {list} |
| explore | X | {list} |
| route-to-sales | X | {list} |
| service-provider-prospect | X | {list} |
| route-to-ka | X | {list} |
| exclude | X | {list} |

## Top Prospects
{ranked_list_with_details}

## Competitor Distributors
{table_with_competitor_brands}
```

## Process

### Step 1: Ensure crawl4ai Server Running

Check if the crawl4ai server is running:

```bash
./scripts/crawl4ai-server.sh status
```

If not running, start it:

```bash
./scripts/crawl4ai-server.sh start
```

If the server is unavailable, fail with:

```
Error: crawl4ai server not running.

Start with: ./scripts/crawl4ai-server.sh start

Or manually: docker run -d --name crawl4ai -p 11235:11235 unclecode/crawl4ai:latest
```

### Step 2: Crawl URL(s)

**Single URL:**

POST to `http://localhost:11235/crawl` with this payload:

```json
{
  "urls": ["https://example.com"],
  "browser_config": {
    "type": "BrowserConfig",
    "params": {
      "headless": true,
      "viewport": {"width": 1200, "height": 800}
    }
  },
  "crawler_config": {
    "type": "CrawlerRunConfig",
    "params": {
      "markdown_generator": {
        "type": "DefaultMarkdownGenerator",
        "params": {
          "content_filter": {
            "type": "PruningContentFilter",
            "params": {"threshold": 0.6}
          }
        }
      },
      "page_timeout": 60000,
      "delay_before_return_html": 2.0
    }
  }
}
```

**Batch URLs (5-10 concurrent):**

```json
{
  "urls": ["https://url1.com", "https://url2.com", "https://url3.com"],
  "browser_config": { ... },
  "crawler_config": { ... }
}
```

**Response format:**

```json
[
  {
    "url": "https://example.com",
    "success": true,
    "markdown": {
      "fit_markdown": "Company Name\n\nProducts and services..."
    }
  }
]
```

### Step 3: Extract Structured Data from Markdown

Parse the `fit_markdown` content for:
- Company name
- Products and services
- Brands carried
- Team/employee indicators
- SLA/service mentions
- Geographic coverage

If `success: false` or empty markdown, return error with URL for manual review.

### Step 4: Categorize

Apply niche market tags from `references/tags.md` (multiple tags allowed).

### Step 5: Score

Apply all bonuses (even if "sells as expected" fails):
- Required: Sells as expected (PASS/FAIL - informational)
- Bonus: Customer overlap (+0 to +50)
- Bonus: Cleaning equipment level (+30 to +90)
- Bonus: Competitor footprint tier (+30 to +90)
- Bonus: Channel capability signals (+0 to +20)

Total score capped at 100.

### Step 6: Route

Return action + play recommendation based on score:

| Score | Gate | Action |
|-------|------|--------|
| 90+ | PASS | `prioritize` |
| 70-89 | PASS | `standard` |
| 50-69 | Any | `explore` |
| <50 | Any | `exclude` |

**Special routing (overrides score):**
- Tier 1-2 competitor footprint: `route-to-sales` + `competitive-conversion` play
- Tagged `cleaning-services-provider`: `service-provider-prospect`
- Tagged `hospitality-service-provider`: `route-to-ka`

**Note:** Companies that FAIL the gate but score 50+ via customer overlap + channel capability route to `explore`.

## Error Handling

### crawl4ai Server Not Running

If the crawl4ai server is not running:

```
Error: crawl4ai server not running.

Start with: ./scripts/crawl4ai-server.sh start

Or manually: docker run -d --name crawl4ai -p 11235:11235 unclecode/crawl4ai:latest
```

### Crawl Failure

If the crawl request fails:
1. Return error with the URL
2. Suggest manual review
3. Do NOT fall back to WebFetch

### Empty Markdown

If `fit_markdown` is empty or `success: false`:
1. Check the URL manually
2. Note in output that content extraction failed
3. Include URL in error for manual review

## Cleaning Equipment Bonus

| Level | Evidence | Points |
|-------|----------|--------|
| Light | Mentions cleaning equipment | +30 |
| Moderate | Has product category | +50 |
| Strong | Core offering, multiple products | +70 |
| Dominant | Primary business, extensive catalog | +90 |

## Competitor Footprint Bonus

| Tier | Evidence | Points | Example |
|------|----------|--------|---------|
| Tier 1 | Official distributor / Authorized partner language | +90 | "Official distributor of PUDU", "Authorized Gausium partner" |
| Tier 2 | Product pages / Sales evidence | +60 | Product listings, competitor SKU/model names from `references/competing-brands.md` |
| Tier 3 | Mentions only | +30 | Blog posts, comparisons, "compatible with..." |

**Why competitor footprint is a TOP signal:** Competitor distributors are the BEST prospects because they already have:
- Customer base in cleaning robotics
- Sales and deployment teams trained on robots
- After-sales service capability
- Market knowledge and relationships
- Proven willingness to invest in robot inventory

**This is MORE valuable than generic cleaning equipment sales** because the jump from cleaning equipment to robots is harder than switching robot brands.

## Channel Capability Bonus

Use bonus signals from `references/keywords.md`:

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

## Customer Overlap Bonus

Award points for serving target customers that OrientStar robots would clean. This bonus recognizes that distributors in adjacent industries (e.g., forklifts, material handling) may have valuable customer relationships and channel capabilities.

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

## Configuration Files

| File | Purpose |
|------|---------|
| `references/keywords.md` | Product/service keywords by industry |
| `references/tags.md` | Niche market tag taxonomy |
| `references/competing-brands.md` | Competitor brands to detect |

## Enrichment Workflow (Optional)

For deeper due diligence, use the **google-search** skill via the Skill tool.

### When to Enrich
- High-value prospects (Grade A)
- Competitor distributors (route-to-sales)
- Unclear company information on website

### How to Enrich

Use the Skill tool to invoke google-search:

```
Skill: google-search
Args: "{company} employees LinkedIn" + locale
```

**Enrichment searches:**
1. **Claim Validation:** `Skill: google-search "{company} employees LinkedIn"`
2. **Market Coverage:** `Skill: google-search "{company} locations"`
3. **Competitor Relationship:** `Skill: google-search "{company} {competitor} partnership"`

**Important:** Use the Skill tool, NOT built-in web search. The google-search skill uses Bright Data SERP API for localized, reliable results.

### Example Pipeline
Search (google-search skill) → Filter URLs → Inspect (this skill) → (optional) Enrich (google-search skill)

See CLAUDE.md for full multi-skill workflow examples.
