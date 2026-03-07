# Image Analysis Guide

Guidance for analyzing website screenshots to extract business intelligence.

## Overview

When `mode="deep"` is specified in inspector skills, additional image analysis is performed using Playwright screenshots. The LLM can directly view and analyze these images.

**This guide provides WHAT to look for, not HOW to implement (LLM vision capabilities are built-in).**

## Common Analysis Patterns

### Team Photo Analysis

**Used by:** distributor-inspector

**Goal:** Estimate employee count from team photos

**Detection:**
1. Navigate to /team, /about, /company pages
2. Capture full-page screenshot
3. Count visible faces in group photos
4. Check for org chart images
5. Look for "X employees" text overlays

**Analysis:**
```
Team photo analysis:
- Photo 1: ~8-12 people (group photo)
- Photo 2: ~5 people (leadership team)
- Estimated total: 15-25 employees
```

**Validation:**
- Count distinct faces, not repeated photos
- Consider org charts as structural info (not headcount)
- If multiple team photos exist, sum unique individuals
- Flag discrepancy if visual count differs significantly from claimed count

### Competitor Logo Detection

**Used by:** distributor-inspector

**Goal:** Identify competitor brand logos in footer/partners sections

**Target brands:**

**Tier 1 (Primary competitors):**
- Pudu Robotics
- Gausium (formerly SoftBank Robotics)
- LionsBot
- Tennant

**Tier 2 (Secondary competitors):**
- Nilfisk
- Karcher (Kärcher)
- Adlatus
- ICE Cobotics
- SoftBank Robotics
- Avidbots

**Detection:**
1. Scan homepage footer for brand logos
2. Check "Our Partners" / "Partners" page images
3. Look for "Authorized Dealer" / "Certified Partner" badges
4. Examine product page hero images for brand mentions

**Analysis:**
```
Logo detection:
- Footer: Pudu Robotics logo detected
- Partners page: Tennant, Nilfisk logos
- "Authorized Dealer" badge: Gausium
```

**Validation:**
- Distinguish between "partner" and "distributor" badges
- Note logo size/prominence (featured vs. small footer logo)
- Capture exact badge text when visible

### Facility Photo Analysis

**Used by:** ka-inspector

**Goal:** Verify facility type and scale for KA end customer qualification

**Target facility types (by priority):**
1. **Retail** - Supermarkets, department stores, retail chains
2. **Hospitality** - Hotels, resorts, restaurant chains
3. **Office/Commercial** - Office buildings, commercial real estate, business parks
4. **Healthcare** - Hospitals, clinics, medical centers
5. **Industrial** - Warehouses, distribution centers, manufacturing facilities
6. **Education** - Universities, schools, campus facilities
7. **Property Management** - Multi-property management companies

**Detection:**
1. Examine homepage hero images for facility type indicators
2. Look for interior photos showing cleanable spaces (floors, corridors, lobbies)
3. Check for facility scale indicators (large open spaces, multiple floors)
4. Identify cleaning-relevant environments (hard floors, high-traffic areas)

**Analysis:**
```
Facility photo analysis:
- Homepage hero: Large retail store interior (wide aisles, tile flooring)
- About page: Warehouse facility with high ceilings and concrete floors
- Estimated facility size: Large-scale (10,000+ sqm based on visual cues)
- Cleaning relevance: HIGH (extensive hard floor areas visible)
```

**Validation:**
- Prioritize facilities with large hard-floor areas (ideal for cleaning robots)
- Note if images show existing cleaning equipment or automation
- Distinguish between owned/managed facilities vs. project portfolio photos
- Look for multi-site indicators (chain store layouts, standardized interiors)

### Location Page Analysis

**Used by:** ka-inspector

**Goal:** Count and verify multi-site presence for KA qualification

**Detection:**
1. Navigate to /locations, /stores, /branches, or /about pages
2. Count visible location markers on maps
3. List location names/cities if displayed
4. Check for international vs. domestic presence
5. Note facility types per location (if differentiated)

**Analysis:**
```
Location analysis:
- Locations page: Found 15 store locations across Germany
- Key cities: Berlin, Munich, Hamburg, Frankfurt, Cologne
- Geographic spread: National coverage (5 states)
- Facility types: Retail stores (12), Distribution centers (3)
- Multi-site indicator: STRONG (15+ locations confirmed)
```

**Validation:**
- Screenshot the full locations page for later review
- If map-based, estimate count from visible markers
- Distinguish between HQ, branches, and partner locations
- Note if locations are owned vs. franchised (if indicated)
- Cross-reference with text-based location claims

### Certification Badge Detection

**Used by:** All inspectors

**Goal:** Detect certifications, awards, and industry affiliations

**Target badges:**

**Quality/Standards:**
- ISO 9001 (Quality Management)
- ISO 14001 (Environmental Management)
- ISO 45001 (Occupational Health & Safety)

**Industry-Specific:**
- HACCP (Food safety - for retail/hospitality)
- Hygiene certifications (for healthcare)
- "Authorized Dealer" / "Certified Partner" badges

**Technology/Digital:**
- IoT platforms (Microsoft Azure IoT, AWS IoT, Siemens MindSphere)
- Building Management Systems (Siemens, Schneider Electric, Honeywell)
- Smart Building certifications (LEED, BREEAM, DGNB)

**Associations:**
- Retail associations (HDE, BVMH for Germany)
- Hospitality associations (DEHOGA, IHA)
- Facility Management (IFMA, BIFM, GEFMA)
- Healthcare facilities (German Hospital Federation)
- Property Management (IVD, RICS)

**Detection:**
1. Scan homepage footer for certification badges
2. Check "About Us" / "Company" page for certifications
3. Look for award logos or "Top Supplier" badges
4. Check for industry association logos

**Analysis:**
```
Certification badges:
- ISO 9001 certified (badge in footer)
- "Top Supplier 2024" award
- "Authorized Dealer" badge: Gausium
```

**Validation:**
- Note expiration dates if visible on badges
- Capture exact wording of awards
- Distinguish between current and historical certifications

### Product Image Analysis

**Used by:** distributor-inspector

**Goal:** Visual confirmation of product types

**Target products:**
- Commercial cleaning robots (scrubbers, sweepers)
- Industrial cleaning equipment
- Facility management equipment
- Consumer robots (for 2C detection)

**Detection:**
1. Examine product images on homepage
2. Check product category pages
3. Look for deployment photos (robots in use)

**Analysis:**
```
Product images:
- Homepage hero: Commercial floor scrubbing robot
- Product page: Multiple autonomous cleaning robots
- Deployment photos: Robots in warehouse/retail settings
```

**Validation:**
- Distinguish between commercial and consumer products
- Note if images show actual deployment vs. stock photos
- Identify robot types (scrubber, sweeper, vacuum)

## Deep Mode Processing

**Standard Mode (text-only):**
- Processing time: ~30 seconds
- No screenshots captured
- No image analysis

**Deep Mode (with images):**
- Processing time: ~90 seconds
- Screenshots captured: home.png, locations.png/team.png
- Image analysis performed
- Additional "Deep Mode Analysis" section in report

## Screenshot Capture

**How image analysis works:**
1. Capture screenshot using browser tools (MCP or CLI)
2. Save to file (e.g., `home.png`, `team.png`)
3. The LLM reads the image file directly using built-in vision capabilities

**For deep mode:**
- Navigate to relevant pages (homepage, team, locations)
- Capture screenshots
- The multimodal LLM analyzes images automatically

**If no images captured:**
- Report "Not analyzed (image capture failed)" in Deep Mode Analysis section

## Error Handling

**If no images captured:**
```markdown
### Deep Mode Analysis

**Status:** Not analyzed (image capture failed)

**Possible reasons:**
- Screenshot command failed
- Page navigation timeout
- No team/about/locations pages found
```

**If analysis inconclusive:**
```markdown
### Deep Mode Analysis

**Team Photos:** No team photos found
**Logo Detection:** No competitor logos detected
**Certifications:** Unable to determine from available images
```

## Summary for Scoring

After image analysis, provide summary assessment for scoring:

```
Image Analysis Summary:
- Employee count: {estimated range}
- Competitor footprint: {tier with brands}
- Facility type: {type if applicable}
- Multi-site confirmation: {STRONG/MODERATE/WEAK}
- Cleaning relevance: {HIGH/MEDIUM/LOW}
- Digital maturity: {HIGH/MEDIUM/LOW}
- Certifications: {list key certs}
```

**Scoring implications:**
- HIGH employee count → Validates company size gate
- Competitor Tier 1-2 → Route to competitive-conversion play
- HIGH cleaning relevance + Multi-site STRONG → +30 multi-site bonus
- HIGH digital maturity → +20 digital maturity bonus
- Relevant certifications → Professional operations signal
