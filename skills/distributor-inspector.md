# Distributor Inspector Skill

Inspect a potential distributor website and evaluate it against OrientStar Robotics' ICP criteria.

## Inputs

- `url`: The website URL to inspect

## Outputs

```json
{
  "url": "https://example.com",
  "digest": {
    "company_name": "Company name",
    "description": "Brief description",
    "products_sold": ["product1", "product2"],
    "services_offered": ["service1", "service2"],
    "brands_carried": ["brand1", "brand2"],
    "geographic_focus": "Country/Region",
    "team_presence": "Evidence of sales/service team",
    "sla_mentions": "Any SLA or service guarantees mentioned"
  },
  "tags": ["tag1", "tag2", "tag3"],
  "scoring": {
    "required_checks": {
      "sells_as_expected": true/false,
      "no_competitor_focus": true/false
    },
    "cleaning_equipment_bonus": 0,
    "total_score": 0,
    "grade": "A/B/C/D/F"
  },
  "key_signals": [
    "Positive signal 1",
    "Positive signal 2",
    "Concern signal (if any)"
  ],
  "action": "prioritize / standard / explore / exclude / route-to-sales"
}
```

## Evaluation Process

### Step 1: Fetch and Extract (Digest)

1. Navigate to the URL
2. If obvious from homepage, extract info from there
3. If not obvious, browse to product catalog/about pages
4. Extract: company name, products, services, brands, geography, team, SLA mentions

### Step 2: Categorization (Tags)

Apply tags from `config/tags.md`:
- Match product category based on what they sell
- Match business model based on how they operate
- Apply special tags if applicable
- Multiple tags allowed

### Step 3: Scoring

**Required Checks (Pass/Fail):**
- `sells_as_expected`: Sells products/services in target categories
- `no_competitor_focus`: Does NOT prominently feature competitor robots

**Cleaning Equipment Bonus:**
- +30: Light presence (mentions cleaning equipment)
- +50: Moderate (has a product category)
- +70: Strong (core offering, multiple products)
- +90: Dominant (primary business, extensive catalog)

**Grade Calculation:**
- If any required check fails → D or F
- Otherwise: grade = bonus + base assessment (0-10 for general quality)

### Step 4: Action Recommendation

| Grade | Action |
|-------|--------|
| A (90+) | prioritize - High priority outreach |
| B (70-89) | standard - Standard outreach queue |
| C (50-69) | explore - Worth investigating |
| D/F (<50) | exclude - Not a fit |
| competitor-robot-distributor tag | route-to-sales - Send to competitor outreach team |

## Configuration Files

- `config/keywords.md` - Product/service keywords by target industry
- `config/tags.md` - Niche market tag taxonomy
- `human_input/competing brands & SKUs.md` - Competitor brands to detect

## Example Execution

**Input:** `https://www.decapulire.com/`

**Output:**
```json
{
  "url": "https://www.decapulire.com/",
  "digest": {
    "company_name": "Deca Srl",
    "description": "Commercial cleaning equipment distributor in Italy, selling professional cleaning machines and products",
    "products_sold": ["Floor scrubbers", "Sweepers", "Vacuum cleaners", "Cleaning accessories"],
    "services_offered": ["Technical assistance", "Spare parts", "Mobile workshop (24-48h)"],
    "brands_carried": ["Lavor Pro", "Du-Puy", "Eureka", "IPC", "TSM"],
    "geographic_focus": "Italy",
    "team_presence": "Has technical team and mobile workshop",
    "sla_mentions": "Assistenza Tecnica presso la vostra sede con Officina Mobile entro 24/48 ore"
  },
  "tags": [
    "cleaning-equipment-distributor",
    "cleaning-supplies-distributor"
  ],
  "scoring": {
    "required_checks": {
      "sells_as_expected": true,
      "no_competitor_focus": true
    },
    "cleaning_equipment_bonus": 70,
    "total_score": 78,
    "grade": "B"
  },
  "key_signals": [
    "✓ Sells commercial cleaning equipment (primary business)",
    "✓ Has after-sales service with 24-48h mobile workshop",
    "✓ Carries multiple established brands",
    "✓ Offers consumables and spare parts",
    "? Team size unknown (requires LinkedIn verification)"
  ],
  "action": "standard"
}
```
