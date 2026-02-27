# Image Analysis Guide - KA Inspector

## Facility Photo Analysis

**Goal:** Verify facility type and scale for KA end customer qualification

**Target facility types (by priority):**

1. **Retail** - Supermarkets, department stores, retail chains
2. **Hospitality** - Hotels, resorts, restaurant chains
3. **Office/Commercial** - Office buildings, commercial real estate, business parks
4. **Healthcare** - Hospitals, clinics, medical centers
5. **Industrial** - Warehouses, distribution centers, manufacturing facilities
6. **Education** - Universities, schools, campus facilities
7. **Property Management** - Multi-property management companies

**Process:**
1. Examine homepage hero images for facility type indicators
2. Look for interior photos showing cleanable spaces (floors, corridors, lobbies)
3. Check for facility scale indicators (large open spaces, multiple floors)
4. Identify cleaning-relevant environments (hard floors, high-traffic areas)

**Output format:**
```
Facility photo analysis:
- Homepage hero: Large retail store interior (wide aisles, tile flooring)
- About page: Warehouse facility with high ceilings and concrete floors
- Estimated facility size: Large-scale (10,000+ sqm based on visual cues)
- Cleaning relevance: High (extensive hard floor areas visible)
```

**Notes:**
- Prioritize facilities with large hard-floor areas (ideal for cleaning robots)
- Note if images show existing cleaning equipment or automation
- Distinguish between owned/managed facilities vs. project portfolio photos
- Look for multi-site indicators (chain store layouts, standardized interiors)

## Location Page Analysis

**Goal:** Count and verify multi-site presence for KA qualification

**Process:**
1. Navigate to /locations, /stores, /branches, or /about pages
2. Count visible location markers on maps
3. List location names/cities if displayed
4. Check for international vs. domestic presence
5. Note facility types per location (if differentiated)

**Output format:**
```
Location analysis:
- Locations page: Found 15 store locations across Germany
- Key cities: Berlin, Munich, Hamburg, Frankfurt, Cologne
- Geographic spread: National coverage (5 states)
- Facility types: Retail stores (12), Distribution centers (3)
- Multi-site indicator: STRONG (15+ locations confirmed)
```

**Notes:**
- Screenshot the full locations page for later review
- If map-based, estimate count from visible markers
- Distinguish between HQ, branches, and partner locations
- Note if locations are owned vs. franchised (if indicated)
- Cross-reference with text-based location claims

## Partnership/Certification Detection

**Goal:** Identify technology partners, certifications, and industry affiliations

**Target badges/logos:**

**Technology Partners:**
- IoT platforms (Microsoft Azure IoT, AWS IoT, Siemens MindSphere)
- Building Management Systems (Siemens, Schneider Electric, Honeywell)
- Facility Management Software (IBM TRIRIGA, Archibus)
- Smart Building certifications (LEED, BREEAM, DGNB)

**Industry Associations:**
- Retail associations (HDE, BVMH for Germany)
- Hospitality associations (DEHOGA, IHA)
- Facility Management (IFMA, BIFM, GEFMA)
- Healthcare facilities (German Hospital Federation)
- Property Management (IVD, RICS)

**Certifications:**
- ISO 9001 (Quality Management)
- ISO 14001 (Environmental Management)
- ISO 45001 (Occupational Health & Safety)
- HACCP (Food safety - for retail/hospitality)
- Hygiene certifications (for healthcare)

**Process:**
1. Scan homepage footer for certification badges
2. Check "About Us" / "Company" page for partnerships
3. Look for "Our Partners" or "Technology" sections
4. Examine investor relations pages for affiliations
5. Check sustainability/ESG pages for green building certs

**Output format:**
```
Partnership/Certification detection:
- Footer: ISO 9001 certified badge
- Technology partners: Microsoft Azure IoT, Siemens Building Technologies
- Industry associations: IFMA member, LEED certified buildings
- Notable: "Smart Building Award 2024" winner
```

**Notes:**
- Distinguish between actual certifications and marketing claims
- Note logo prominence (featured partner vs. small footer logo)
- Capture exact badge text when visible
- Technology partnerships signal digital maturity (scoring bonus)

## Digital Systems Detection

**Goal:** Identify IoT, automation, and building management system mentions

**Signals to look for:**
- "Smart building" / "Intelligent building" mentions
- IoT sensor imagery or dashboards
- Building management system screenshots
- Automation/robotics mentions (existing deployments)
- Digital twin or facility monitoring systems

**Process:**
1. Scan homepage for "smart" or "digital" language
2. Check technology/innovation pages
3. Look for facility management dashboards
4. Examine sustainability pages (often mention smart systems)

**Output format:**
```
Digital systems detection:
- Homepage: "Smart Building Initiative" feature
- Technology page: IoT sensor network across all locations
- Existing automation: Automated guided vehicles (AGVs) in warehouse
- Digital maturity: HIGH (dedicated innovation team, IoT infrastructure)
```

**Notes:**
- Existing automation suggests openness to robotic solutions
- IoT infrastructure indicates technical capability for robot integration
- Note if facility already uses cleaning automation (competitor or complementary)

## Summary for KA Scoring

After image analysis, provide a summary assessment:

```
Image Analysis Summary:
- Facility type: {retail/hospitality/office/healthcare/industrial}
- Cleaning relevance: {HIGH/MEDIUM/LOW}
- Multi-site confirmation: {STRONG/MODERATE/WEAK} - {count} locations
- Digital maturity: {HIGH/MEDIUM/LOW}
- Existing automation: {yes/no} - {details}
- Certifications: {list key certs}
```

**Scoring implications:**
- HIGH cleaning relevance + Multi-site STRONG → +30 multi-site bonus
- HIGH digital maturity → +20 digital maturity bonus
- Existing automation → Positive signal for pilot readiness
- Relevant certifications → Professional operations signal
