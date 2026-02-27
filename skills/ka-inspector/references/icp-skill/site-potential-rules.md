# Site Potential Rules - KA End Customer

> **Purpose:** Rules for evaluating multi-site potential
> **Updated:** 2026-02-27

---

## Overview

Site potential measures: **"How many locations could deploy our robots?"**

This is the **most important bonus criterion** for KA evaluation because:
- Single site = one sale
- Multi-site = recurring revenue, faster ROI

---

## Location Count Scoring

| Count | Level | Points |
|-------|-------|--------|
| 1 | Single site | +0 |
| 2-5 | Small multi-site | +10 |
| 6-20 | Medium chain | +20 |
| 20+ | Large chain | +30 |

---

## Detection Methods

### Method 1: Explicit Location Count

**Patterns to detect:**
- "X locations", "X stores", "X branches"
- "X sites", "X properties", "X facilities"
- "Over X", "More than X", "X+"

**Examples:**
- "50 stores across Germany" → 50 locations → +30
- "Over 200 sites" → 200+ locations → +30
- "3 locations in Berlin" → 3 locations → +10

---

### Method 2: Location Page Analysis

**If company has a "Locations" or "Stores" page:**

1. Count listed locations
2. Check for grouping (regions, districts)
3. Look for expansion mentions ("opening soon")

**Examples:**
- Locations page with 15 stores listed → +20
- Locations page with 5 stores + "expanding" → +15

---

### Method 3: Chain Language Detection

**Keywords indicating chain/multi-site:**

| Language | Strength |
|----------|----------|
| "Chain", "group", "network" | Strong |
| "Nationwide", "countrywide" | Strong |
| "Multi-location", "multiple sites" | Strong |
| "Regional", "area" | Medium |
| "Expanding", "growing" | Weak |

---

## Segment-Specific Rules

### Retail Chains

**Detection:**
- "Our stores", "our locations"
- Store locator page
- Regional structure (North, South, East, West)

**Scoring:**
- Store count from locator → Direct count
- No count but "nationwide" → +20 (assume 20+)

---

### Hotel Chains

**Detection:**
- "Our hotels", "properties"
- Hotel list page
- Booking platform integration

**Scoring:**
- Hotel count from list → Direct count
- "Boutique hotel group" → +10 (assume 2-5)

---

### Property Management

**Detection:**
- "Property portfolio", "managed properties"
- Client list
- Service area

**Scoring:**
- Property count mentioned → Direct count
- "Large portfolio" → +20 (assume 20+)

---

### Office Buildings / Commercial Real Estate

**Detection:**
- "Office park", "business center"
- Building list
- Tenant information

**Scoring:**
- Building count → Direct count
- "Business park" (single) → +0
- "Multiple properties" → +10

---

## Special Cases

### Franchise Models

**Scenario:** Company operates franchise model (franchisee owns locations)

**Decision:** Still count all franchise locations - they influence standards.

**Scoring:** Use total location count (including franchises)

---

### Managed Properties

**Scenario:** Property management company manages properties for others

**Decision:** Count managed properties - they make purchasing decisions.

**Scoring:** Use managed property count

---

### Partnership/Alliance Networks

**Scenario:** Company has partnership network (not owned locations)

**Decision:** Do NOT count partner locations unless they control standards.

**Scoring:** Only count owned/managed properties

---

## Examples

### Example A: Supermarket Chain

**Evidence:**
- "52 stores across Bavaria"
- Store locator with 52 entries
- "Opening 10 more stores in 2026"

**Scoring:**
- Location count: 52 → +30

---

### Example B: Hotel Group

**Evidence:**
- "Boutique hotel group"
- 4 hotels listed on website
- "Expanding to 6 by end of year"

**Scoring:**
- Location count: 4 → +10

---

### Example C: Property Manager

**Evidence:**
- "Managing 200+ properties"
- "Portfolio includes office and retail"
- No specific count

**Scoring:**
- "200+" mentioned → +30

---

### Example D: Single Restaurant

**Evidence:**
- "Family-owned restaurant"
- Single address
- No expansion mentions

**Scoring:**
- Single location → +0

---

## Summary Table

| Component | Points |
|-----------|--------|
| 1 location | +0 |
| 2-5 locations | +10 |
| 6-20 locations | +20 |
| 20+ locations | +30 |
| "Chain" language without count | +10 |
| "Nationwide" without count | +20 |

---

## Notes for AI Implementation

1. **Look for explicit counts first** - "X locations", "X stores"
2. **Check location pages** - Count listed locations
3. **Use chain language as fallback** - If no count, use language strength
4. **Show evidence** - Report: "Multi-site: 52 stores mentioned"
