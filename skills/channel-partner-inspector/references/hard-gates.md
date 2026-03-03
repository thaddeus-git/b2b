# Hard Gates - Channel Partner Inspector

> **Purpose:** Define the primary qualification gate for channel partners
> **Related:** `../_shared/target-segments.md`

---

## Primary Gate: Client Overlap

A company qualifies as a channel partner prospect if they have **named clients in target segments**.

### Gate Definition

| Gate | Requirement | Weight |
|------|-------------|--------|
| **Client Overlap** | Has named clients in target segments | PASS/FAIL (blocking) |

### What Counts as Client Evidence

**Strong Evidence (definite client):**
- Client logo with link to case study
- Named testimonial with person's name and company
- Case study / success story with named company
- "Our clients include: [Company A, Company B, ...]"
- Press release mentioning client relationship

**Moderate Evidence (likely client):**
- Client logos without case study links
- "Trusted by [industry] leaders" with logos
- "Who we serve" page with company types

**Weak Evidence (possible client):**
- Industry mentions without specific companies
- "Serving Fortune 500 companies" (no names)

**Minimum for PASS:** At least ONE named client in a target segment

### Target Segments (from _shared/target-segments.md)

| Segment | Priority | Client Types |
|---------|----------|--------------|
| Healthcare | HIGH | Hospitals, medical centers, clinics, health systems |
| Retail | HIGH | Retail chains, supermarkets, drug stores, malls |
| Hospitality | HIGH | Hotels, resorts, casinos, event venues |
| Property/FM | HIGH | Property management, facility management, IFM |
| Logistics | MEDIUM | Warehouses, distribution centers, fulfillment |
| Education | MEDIUM | Universities, colleges, school districts |
| Government | MEDIUM | Municipal, state, federal agencies |

### Gate Evaluation Process

1. **Scan for client evidence:**
   - Check homepage for client logos
   - Look for "Clients", "Case Studies", "Success Stories" pages
   - Check testimonials for company names
   - Search for "our clients", "who we serve", "trusted by"

2. **Categorize each client:**
   - Map client to target segment (Healthcare, Retail, etc.)
   - Note if client is KA (enterprise/recognizable brand)

3. **Determine gate result:**
   - If ANY client in target segment → PASS
   - If NO clients in target segments → FAIL

### Gate Result Impact

| Result | Action |
|--------|--------|
| **PASS** | Continue to scoring (base score: 60) |
| **FAIL** | Route to `exclude` or cross-route to appropriate skill |

---

## Cross-Routing on Gate Fail

If client overlap gate FAILS, check for alternative fits:

| Condition | Route To |
|-----------|----------|
| Sells physical products | `distributor-inspector` |
| Operates facilities | `ka-inspector` |
| Neither | `exclude` (not a prospect) |
