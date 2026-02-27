# Image Analysis Guide - Distributor Inspector

## Team Photo Analysis

**Goal:** Estimate employee count from team photos

**Process:**
1. Count visible faces in team photos
2. Check for org chart images
3. Look for "X employees" text overlays
4. Cross-reference with text-based employee count claims

**Output format:**
```
Team photo analysis:
- Photo 1: ~8-12 people (group photo)
- Photo 2: ~5 people (leadership team)
- Estimated total: 15-25 employees
```

**Notes:**
- Count distinct faces, not repeated photos
- Consider org charts as structural info (not headcount)
- If multiple team photos exist, sum unique individuals
- Flag discrepancy if visual count differs significantly from claimed count

## Logo Detection

**Goal:** Identify competitor brand logos

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

**Process:**
1. Scan homepage footer for brand logos
2. Check "Our Partners" / "Partners" page images
3. Look for "Authorized Dealer" / "Certified Partner" badges
4. Examine product page hero images for brand mentions

**Output format:**
```
Logo detection:
- Footer: Pudu Robotics logo detected
- Partners page: Tennant, Nilfisk logos
- "Authorized Dealer" badge: Gausium
```

**Notes:**
- Distinguish between "partner" and "distributor" badges
- Note logo size/prominence (featured vs. small footer logo)
- Capture exact badge text when visible

## Certification Badges

**Goal:** Detect certifications and awards

**Target badges:**
- ISO 9001 (Quality Management)
- ISO 14001 (Environmental Management)
- "Authorized Dealer" / "Certified Partner" badges
- Industry awards (e.g., "Top Supplier 2024")
- Trade association memberships

**Process:**
1. Scan homepage footer for certification badges
2. Check "About Us" / "Company" page for certifications
3. Look for award logos or "Top Supplier" badges
4. Check for industry association logos

**Output format:**
```
Certification badges:
- ISO 9001 certified (badge in footer)
- "Top Supplier 2024" award
- "Authorized Dealer" badge: Gausium
```

**Notes:**
- Distinguish between actual certifications and marketing claims
- Note expiration dates if visible on badges
- Capture exact wording of awards

## Product Image Analysis

**Goal:** Visual confirmation of product types

**Target products:**
- Commercial cleaning robots (scrubbers, sweepers)
- Industrial cleaning equipment
- Facility management equipment
- Consumer robots (for 2C detection)

**Process:**
1. Examine product images on homepage
2. Check product category pages
3. Look for deployment photos (robots in use)

**Output format:**
```
Product images:
- Homepage hero: Commercial floor scrubbing robot
- Product page: Multiple autonomous cleaning robots
- Deployment photos: Robots in warehouse/retail settings
```

**Notes:**
- Distinguish between commercial and consumer products
- Note if images show actual deployment vs. stock photos
- Identify robot types (scrubber, sweeper, vacuum)
