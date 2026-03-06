# Target Industries - Distributor Qualification

> **Priority Order:** Highest priority first
> **Updated:** 2026-02-27

---

## Overview

This document defines the **target industry hierarchy** for distributor qualification. Industries are ordered by:
1. Existing after-sales capability
2. Customer base overlap with cleaning robots
3. Speed to revenue (shortest sales cycle)

---

## Priority 1: Commercial Cleaning Equipment Distributors

### Why Highest Priority
- Already sell what we sell (floor care equipment)
- Have after-sales teams and spare parts infrastructure
- Customer relationships in facility management, janitorial, property
- Natural product line extension (manual → robotic cleaning)

### Detection Keywords

**German:**
- "Gewerbliche Reinigungstechnik"
- "Gebäudereinigung Geräte"
- "Scheuersaugmaschinen", "Kehrmaschinen"
- "Reinigungstechnik Großhandel"

**English:**
- "Commercial cleaning equipment"
- "Floor care machinery"
- "Janitorial supplies and equipment"
- "Facility management equipment"

**French:**
- "Matériel de nettoyage professionnel"
- "Équipements pour l'entretien"
- "Autolaveuses", "Balayeuses"

### Tags
`cleaning-equipment-distributor`, `cleaning-equipment-wholesaler`

---

## Priority 2: Property Management / FM Companies

### Why High Priority
- Direct access to end-user facilities
- Control purchasing decisions for cleaning across portfolios
- Can deploy robots across multiple properties
- May have in-house maintenance teams

### Detection Keywords

**German:**
- "Gebäudemanagement", "Immobilienverwaltung"
- "Facility Management", "FM-Dienstleister"
- "Objektverwaltung"

**English:**
- "Property management"
- "Facility management", "FM"
- "Building services"
- "Real estate management"

**French:**
- "Gestion immobilière"
- "Facility Management", "FM"
- "Services immobiliers"

### Tags
`facility-management-service-provider`, `property-management`

---

## Priority 3: Cleaning Service Contractors

### Why Medium-High Priority
- Direct end-users (they clean buildings themselves)
- ROI calculation is straightforward (labor cost savings)
- May need financing/leasing partners for robot purchases

### Caveats
- May lack technical service capability → need service partner
- Often smaller companies (< 50 employees)
- May prefer RaaS/leasing model over purchase

### Detection Keywords

**German:**
- "Gebäudereinigung", "Reinigungsdienst"
- "Unterhaltsreinigung", "Grundreinigung"
- "Facility Services"

**English:**
- "Cleaning services"
- "Contract cleaning"
- "Janitorial services"
- "Commercial cleaning"

**French:**
- "Services de nettoyage"
- "Entreprise de nettoyage"
- "Nettoyage industriel"

### Tags
`cleaning-services-provider`

---

## Priority 4: System Integrators / Commercial Robot Distributors

### Why Medium Priority
- Technical capability for complex deployments
- May already sell other commercial robots (AGVs, etc.)
- Can handle custom integration requirements

### Caveats
- May lack cleaning-specific customer base
- Need to verify they can sell (not just integrate)
- Longer sales cycles (technical evaluation)

### Detection Keywords

**German:**
- "Systemintegration", "Systemhaus"
- "Roboterlösungen", "Automatisierung"
- "Lösungsanbieter"

**English:**
- "System integrator"
- "Robotics solutions"
- "Automation solutions"
- "Commercial robots"

**French:**
- "Intégrateur système"
- "Solutions robotiques"
- "Automatisation"

### Tags
`robotics-system-integrator`, `robotics-distributor`

---

## Priority 5: Consumer Electronics with B2B Division

### Why Conditional Priority
- May have capital and infrastructure
- Can leverage existing distribution networks

### Hard Requirements (Must Verify)
- **Must have B2B/wholesale division** - Not just retail stores
- **Must have commercial products** - Not only consumer vacuums
- **Must have business customer team** - Not just walk-in sales

### Detection Keywords (B2B signals)

**German:**
- "Gewerbekunden", "B2B-Bereich"
- "Großhandel", "Fachhandel"
- "Geschäftskunden"

**English:**
- "Business customers"
- "B2B division"
- "Wholesale"
- "Trade counter"

**French:**
- "Clients professionnels"
- "Division B2B"
- "Grossiste"
- "Professionnels"

### Tags
`general-merchandise-retailer` + `pure-2c-retail` (if B2B not verified → EXCLUDE)

---

## Industry Decision Tree

```
Does company sell commercial cleaning equipment?
├─ YES → Priority 1 (cleaning-equipment-distributor)
└─ NO → Continue

Does company manage properties/facilities?
├─ YES → Priority 2 (facility-management-service-provider)
└─ NO → Continue

Does company provide cleaning services?
├─ YES → Priority 3 (cleaning-services-provider)
└─ NO → Continue

Does company sell/integrate robots or automation?
├─ YES → Priority 4 (robotics-system-integrator)
└─ NO → Continue

Does company have B2B/wholesale division with commercial products?
├─ YES → Priority 5 (tag appropriately)
└─ NO → EXCLUDE (pure B2C retail)
```

---

## High-Potential End-User Scenarios

Use these to evaluate **customer overlap bonus** (see `icp-sales/bonus-criteria.md`).

| Scenario | Why High Potential | Detection Keywords |
|----------|-------------------|-------------------|
| National retail chains | Single customer → multi-location rollout | "Supermarket", "retail chain", "multi-site" |
| Office buildings / commercial real estate | Centralized procurement, recurring need | "Office tower", "business park", "commercial property" |
| Hotels / Hospitality | High cleaning frequency, ROI easy to calculate | "Hotel chain", "hospitality group", "resort" |
| Medical / Healthcare | Strict hygiene requirements, budget available | "Hospital", "clinic", "healthcare facility" |
| Logistics / Warehouses | Labor shortage acute, large floorspaces | "Distribution center", "fulfillment", "warehouse" |

---

## Non-Target Industries (Exclude)

| Industry | Reason for Exclusion |
|----------|---------------------|
| Renovation/decoration | Core business is construction, not cleaning equipment |
| Pure B2C retail | No ToB channels, no commercial capability |
| Residential real estate agents | Transaction-focused, not facility management |
| Security services | Different buyer, different procurement cycle |
| Waste management | Different industry vertical, no cleaning equipment overlap |
