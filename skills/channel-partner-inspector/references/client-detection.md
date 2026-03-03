# Client Detection Guide

> **Purpose:** How to extract and categorize client lists from websites
> **Related:** `hard-gates.md`, `../_shared/target-segments.md`

---

## Detection Sources

### Primary Sources (High Confidence)

1. **Client Logos Section**
   - Location: Usually in footer, homepage, or dedicated "Clients" page
   - Detection: Look for logo grids with company names in alt text
   - Signal: "Our clients", "Trusted by", "Who we serve"

2. **Case Studies / Success Stories**
   - Location: `/case-studies`, `/success-stories`, `/customers`
   - Detection: Named company with story details
   - Signal: "Read how [Company] achieved [result]"

3. **Testimonials with Attribution**
   - Location: Homepage, product pages, about page
   - Detection: Quote + person name + company name
   - Signal: "– [Name], [Title], [Company]"

### Secondary Sources (Medium Confidence)

4. **"Who We Serve" Pages**
   - Location: `/who-we-serve`, `/industries`, `/solutions`
   - Detection: Industry pages with named examples
   - Signal: "Serving [industry] leaders like..."

5. **Press Releases / News**
   - Location: `/news`, `/press`, `/blog`
   - Detection: Announcements of client wins
   - Signal: "[Company] selects [Vendor] for..."

6. **Partner/Integration Pages**
   - Location: `/partners`, `/integrations`
   - Detection: Mutual customers mentioned
   - Signal: "Together with [Partner], serving [Client]"

---

## Extraction Process

### Step 1: Scan Homepage

Look for:
- Logo sections (footer, mid-page)
- Testimonial carousels
- "Trusted by N companies" claims
- Client count claims ("Serving 500+ organizations")

### Step 2: Check Common Pages

Navigate to:
- `/clients` or `/customers`
- `/case-studies` or `/success-stories`
- `/who-we-serve` or `/industries`
- `/about` (may list notable clients)

### Step 3: Extract Client Names

For each detected client:
1. Record company name
2. Note detection source (logo, case study, testimonial)
3. Categorize by segment (Healthcare, Retail, etc.)
4. Note if KA (recognizable enterprise brand)

---

## Segment Categorization

### Healthcare

**Keywords:** Hospital, medical center, clinic, health system, healthcare, patient, clinical

**Examples:**
- OHSU (Oregon Health & Sciences University)
- Keck Medicine USC
- Kaiser Permanente
- HCA Healthcare
- Cleveland Clinic

### Retail

**Keywords:** Retail, store, chain, supermarket, pharmacy, grocery, mall

**Examples:**
- Walmart
- Target
- CVS Health
- Walgreens
- Kroger
- Albertsons

### Hospitality

**Keywords:** Hotel, resort, casino, hospitality, guest, lodging, accommodation

**Examples:**
- Marriott International
- Hilton
- MGM Resorts
- Caesars Entertainment
- IHG

### Property / Facility Management

**Keywords:** Property management, facility management, FM, building services, real estate, CRE

**Examples:**
- JLL
- CBRE
- Cushman & Wakefield
- Colliers
- Prologis

### Logistics

**Keywords:** Warehouse, distribution, fulfillment, logistics, supply chain, DC

**Examples:**
- Amazon
- FedEx
- UPS
- DHL
- XPO Logistics

### Education

**Keywords:** University, college, school, campus, education, academic

**Examples:**
- State University systems
- Community college districts
- Private universities

### Government

**Keywords:** Government, municipal, city, state, federal, public sector, agency

**Examples:**
- City of [Name]
- State of [Name]
- GSA
- Department of [X]

---

## Output Format

Extract clients in this format:

```markdown
**Named Clients:**
- OHSU (Healthcare) - KA
- Keck Medicine USC (Healthcare) - KA
- Kern Medical (Healthcare)
- Golden Valley Health Centers (Healthcare)
- Omni Family Health (Healthcare)
```

---

## Client Count Estimation

When exact count unavailable:

| Signal | Estimated Count |
|--------|-----------------|
| "Serving 500+ organizations" | 500+ |
| Logo grid with 20+ logos | 20+ |
| "Fortune 500 clients" | Assume 5-10 |
| "Trusted by industry leaders" | Assume 5-10 |
| No signals | Count extracted names |
