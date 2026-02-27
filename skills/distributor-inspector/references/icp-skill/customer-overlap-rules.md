# Customer Overlap Scoring Rules

> **Purpose:** Explicit rules for scoring customer overlap between prospect's clients and OrientStar's target end-users
> **Updated:** 2026-02-27

---

## Overview

Customer overlap measures: **"Does this company already serve the customers who would buy our cleaning robots?"**

This is a **bonus criterion** - it adds points but cannot rescue a company that fails hard gates.

---

## Scoring Logic

| Evidence Type | Points Per Category | Max |
|---------------|--------------------|-----|
| End-user customer in case study | +10 | +50 |
| Channel partner serving customers | +15 | +50 |
| Multiple customers in same segment | +5 additional | +50 |

---

## Customer Categories (Non-Overlapping)

Categories are designed so that multiple sub-types within a category count as **ONE category**, not multiple.

### Category 1: Industrial (+15 max)

**Sub-types (all count as "Industrial"):**
- Warehouses
- Factories / Manufacturing plants
- Logistics centers
- Distribution centers
- Fulfillment centers
- Industrial depots

**Detection Keywords:**
- "Warehouse", "Lager", "entrepôt"
- "Factory", "Fabrik", "usine"
- "Logistics", "Logistik", "logistique"
- "Distribution center", "Verteilzentrum"
- "Manufacturing", "Fertigung", "fabrication"

**Example Evidence:**
- Case study: "DB Schenker warehouse automation"
- Customer testimonial: "Kuehne + Nagel logistics center"
- Reference: "BMW factory cleaning"

---

### Category 2: Commercial Real Estate (+15 max)

**Sub-types (all count as "Commercial Real Estate"):**
- Office buildings
- Property management companies
- Business parks
- Commercial facilities
- Real estate portfolios

**Detection Keywords:**
- "Property management", "Gebäudemanagement", "gestion immobilière"
- "Facility management", "FM"
- "Office building", "Bürogebäude", "bureaux"
- "Business park", "Gewerbepark", "parc d'activités"
- "Real estate", "Immobilien", "immobilier"

**Example Evidence:**
- Case study: "CBRE facility cleaning"
- Customer: "JLL property portfolio"
- Reference: "Office tower Frankfurt cleaning"

---

### Category 3: Retail (+15 max)

**Sub-types (all count as "Retail"):**
- Supermarkets
- Retail chains
- Multi-site stores
- Department stores
- Drug stores

**Detection Keywords:**
- "Supermarket", "Supermarkt", "supermarché"
- "Retail chain", "Einzelhandelskette"
- "Multi-site retail", "Filialen"
- "Department store", "Kaufhaus"
- "Drug store", "Drogerie"

**Example Evidence:**
- Case study: "Edeka supermarket cleaning"
- Customer: "Carrefour retail portfolio"
- Reference: "DM drug store chain"

---

### Category 4: Hospitality (+10 max)

**Sub-types (all count as "Hospitality"):**
- Hotels / Hotel chains
- Restaurants (commercial chains)
- Healthcare facilities
- Senior living facilities
- Resorts

**Detection Keywords:**
- "Hotel", "Hôtel"
- "Hospitality", "Gastgewerbe", "hôtellerie"
- "Healthcare", "Gesundheitswesen", "santé"
- "Hospital", "Krankenhaus"
- "Senior living", "Seniorenheim"

**Example Evidence:**
- Case study: "Marriott hotel cleaning"
- Customer: "Hospital group"
- Reference: "Senior living facility"

---

### Category 5: Public/Institutional (+10 max)

**Sub-types (all count as "Public/Institutional"):**
- Schools / Universities
- Government buildings
- Airports
- Museums / Cultural venues
- Convention centers

**Detection Keywords:**
- "School", "Schule", "école"
- "University", "Universität", "université"
- "Government", "Regierung", "gouvernement"
- "Airport", "Flughafen", "aéroport"
- "Museum", "Konzerthalle"

**Example Evidence:**
- Case study: "Frankfurt Airport cleaning"
- Customer: "City government"
- Reference: "University campus"

---

## Scoring Examples

### Example A: Industrial Specialist

**Company:** Serves warehouses + factories + logistics centers

**Evidence:**
- Case study: "DHL warehouse"
- Testimonial: "BMW factory"
- Reference: "Amazon fulfillment center"

**Scoring:**
- Customer types: 1 (all Industrial)
- Base: +10 (end-user evidence)
- Multiple in same segment: +5
- **Total: +15**

---

### Example B: Cross-Sector Distributor

**Company:** Sells to supermarkets + office buildings + hotels

**Evidence:**
- Product page: "Retail cleaning solutions"
- Case study: "Office tower Frankfurt"
- Reference: "Hotel chain partnership"

**Scoring:**
- Customer types: 3 (Retail + Commercial Real Estate + Hospitality)
- Base: +10 × 3 = +30 (end-user evidence)
- **Total: +30**

---

### Example C: Channel Partner (Strongest Signal)

**Company:** Has resellers serving factories + warehouses + retail + offices

**Evidence:**
- Partner page: "Our partners serve manufacturing, retail, and office sectors"
- Case study: "Partner deployed to 50 retail locations"
- Multiple sector testimonials

**Scoring:**
- Customer types: 3 (Industrial + Retail + Commercial Real Estate)
- Channel rate: +15 × 3 = +45
- Multiple in Industrial segment: +5
- **Total: +50 (capped)**

---

### Example D: Single Customer Type

**Company:** Only serves breweries

**Evidence:**
- Multiple brewery case studies
- "Beverage industry" focus

**Scoring:**
- Customer types: 1 (Industrial - beverage manufacturing)
- Base: +10 (end-user evidence)
- Multiple in same segment: +5
- **Total: +15**

---

## Evidence Strength Hierarchy

| Evidence Type | Reliability | Points |
|---------------|-------------|--------|
| Named customer case study | High | +10 per category |
| Customer testimonial with logo | High | +10 per category |
| Reference list with names | Medium | +8 per category |
| Sector mentions (no names) | Low | +5 per category |
| Generic "we serve X" claims | Very Low | +3 per category |

---

## Detection Algorithm

```python
def score_customer_overlap(extracted_customers):
    """
    extracted_customers: list of customer mentions with context
    Returns: (score, breakdown)
    """
    categories_found = {
        'industrial': [],
        'commercial_real_estate': [],
        'retail': [],
        'hospitality': [],
        'public_institutional': []
    }

    evidence_strength = {
        'case_study': 10,
        'testimonial': 10,
        'reference_named': 8,
        'sector_mention': 5,
        'generic_claim': 3
    }

    # Categorize each customer mention
    for customer in extracted_customers:
        category = categorize_customer(customer.name, customer.context)
        if category:
            strength = determine_evidence_strength(customer.type)
            categories_found[category].append(strength)

    # Score: best evidence per category
    score = 0
    for category, evidences in categories_found.items():
        if evidences:
            best_evidence = max(evidences)
            score += best_evidence

            # Bonus for multiple in same category
            if len(evidences) >= 2:
                score += 5

    return min(score, 50)  # Cap at 50
```

---

## Customer Categorization Reference

| Customer Name/Type | Category |
|-------------------|----------|
| DHL, DB Schenker, Kuehne+Nagel, Amazon Logistics | Industrial |
| BMW, Mercedes, Siemens, Bosch factories | Industrial |
| CBRE, JLL, Cushman & Wakefield | Commercial Real Estate |
| Edeka, Carrefour, Tesco, Aldi, Lidl | Retail |
| Marriott, Hilton, Accor | Hospitality |
| HCA (UK hospitals), Charité Berlin | Hospitality |
| Frankfurt Airport, CDG Paris | Public/Institutional |
| Government buildings, city halls | Public/Institutional |
| Universities, schools | Public/Institutional |

---

## Special Cases

### Renovation Companies with Facility Clients

**Scenario:** Renovation company serves office buildings and warehouses.

**Decision:** This is NOT customer overlap - they're doing construction, not cleaning.

**Action:** Do NOT award points unless they ALSO sell cleaning equipment.

---

### Cleaning Service Companies

**Scenario:** Cleaning contractor serves offices, hotels, and retail.

**Decision:** This IS customer overlap - they have direct end-user relationships.

**Action:** Award points, but also tag as `cleaning-services-provider` for special routing.

---

### System Integrators

**Scenario:** Integrator serves factories and warehouses with automation.

**Decision:** This IS customer overlap - they have industrial customer access.

**Action:** Award points + consider for `robotics-system-integrator` tag.

---

## Summary Table

| Component | Points |
|-----------|--------|
| Per customer category (best evidence) | +10 to +15 |
| Multiple customers in same segment | +5 additional |
| Maximum total | +50 (capped) |

---

## Notes for AI Implementation

1. **Extract named customers** when possible - they're stronger evidence
2. **Categorize conservatively** - if unclear, use lower category
3. **Show evidence** in report: "Customer overlap: Industrial (DB Schenker warehouse case study)"
4. **Don't double-count** - supermarket + retail chain = 1 category (Retail)
5. **Channel partners score higher** - they SELL to customers vs. serving them directly
