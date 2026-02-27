# Target Industries - KA End Customer

> **Priority Order:** Highest priority first
> **Updated:** 2026-02-27

---

## Overview

This document defines the **target industry hierarchy** for KA end customer qualification. Industries are ordered by:
1. Cleaning frequency and labor intensity
2. Multi-site replication potential
3. Budget availability for automation

---

## Priority 1: Large Retail Chains / Supermarkets

### Why Highest Priority
- High cleaning frequency (daily)
- Large floor space
- Labor cost pressure
- Can replicate across stores quickly

### Detection Keywords

**German:**
- "Supermarkt", "Einzelhandel", "Filialen"
- "Handelskette", "Warenumsatz"

**English:**
- "Supermarket", "retail chain", "department store"
- "Multi-location retail", "stores"

**French:**
- "Supermarché", "grande distribution"
- "Chaîne de magasins", "enseignes"

### Examples
- Metro, Edeka, Rewe (Germany)
- Carrefour, Auchan (France)
- Tesco, Sainsbury's (UK)

---

## Priority 2: Hospitals / Healthcare Facilities

### Why High Priority
- Strict hygiene requirements
- 24/7 operations
- High labor costs
- Budget for compliance

### Detection Keywords

**German:**
- "Krankenhaus", "Klinik", "Gesundheitswesen"
- "Pflegeeinrichtung", "Seniorenheim"

**English:**
- "Hospital", "healthcare", "medical center"
- "Senior care", "nursing home"

**French:**
- "Hôpital", "clinique", "établissement de santé"
- "Maison de retraite", "EHPAD"

---

## Priority 3: Commercial Real Estate / Office Buildings

### Why Medium-High Priority
- Large common areas
- Professional image requirements
- Facility management budgets

### Detection Keywords

**German:**
- "Bürogebäude", "Immobilien", "Gewerbeimmobilien"
- "Objektverwaltung", "Gebäudemanagement"

**English:**
- "Office building", "commercial property"
- "Property management", "real estate"

**French:**
- "Immeuble de bureaux", "immobilier commercial"
- "Gestion immobilière", "facility management"

---

## Priority 4: Property Management / FM Companies

### Why Medium Priority
- Manage multiple properties
- Can deploy across portfolio
- May need distributor partners for service

### Detection Keywords

**German:**
- "Facility Management", "Gebäudereinigung"
- "Hausverwaltung", "Objektbetreuung"

**English:**
- "Facility management", "FM", "IFM"
- "Property management", "building services"

**French:**
- "Facility Management", "FM"
- "Gestion de propriétés", "services immobiliers"

---

## Priority 5: Hotels / Convention Centers / Transport Hubs

### Why Medium Priority
- High foot traffic
- Image-critical environments
- Budget for quality

### Detection Keywords

**German:**
- "Hotel", "Tagungszentrum", "Konzerthalle"
- "Flughafen", "Bahnhof", "Verkehrsknotenpunkt"

**English:**
- "Hotel", "convention center", "exhibition hall"
- "Airport", "train station", "transport hub"

**French:**
- "Hôtel", "centre de congrès", "palais des congrès"
- "Aéroport", "gare", "plateforme de transport"

---

## Priority 6: Manufacturing / Warehousing / Logistics Parks

### Why Lower Priority (but still viable)
- Large spaces
- Labor shortage in cleaning
- May prioritize production over facilities

### Detection Keywords

**German:**
- "Fabrik", "Produktion", "Lager"
- "Logistikzentrum", "Industriepark"

**English:**
- "Factory", "manufacturing", "warehouse"
- "Distribution center", "logistics park"

**French:**
- "Usine", "fabrication", "entrepôt"
- "Centre logistique", "parc industriel"

---

## Industry Decision Tree

```
Is company a retail chain with multiple stores?
├─ YES → Priority 1 (large-retail-chain)
└─ NO → Continue

Is company a hospital or healthcare facility?
├─ YES → Priority 2 (hospital-healthcare)
└─ NO → Continue

Is company managing commercial real estate / offices?
├─ YES → Priority 3 (commercial-real-estate)
└─ NO → Continue

Is company a property management / FM provider?
├─ YES → Priority 4 (property-management-fm)
└─ NO → Continue

Is company a hotel / convention center / transport hub?
├─ YES → Priority 5 (hospitality-venue)
└─ NO → Continue

Is company a manufacturer / warehouse / logistics operator?
├─ YES → Priority 6 (manufacturing-warehousing)
└─ NO → May not be a good KA prospect
```
