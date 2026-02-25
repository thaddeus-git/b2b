# Design: Channel Partner Prospect Routing

**Date:** 2026-02-25
**Status:** Approved

## Problem

Cross-industry equipment distributors (e.g., forklifts, warehouse equipment) are being excluded even though they:
- Have strong distributor capabilities (multi-brand, service, parts, training)
- Serve target industries that need cleaning robots (warehouses, logistics, manufacturing)
- Could become potential distributors through channel partnership

Example: Tomi Maquinaria - forklift distributor with strong capabilities and network to warehouses.

## Solution

Add new routing action `channel-partner-prospect` for cross-industry equipment distributors.

## New Action

| Action | Trigger | Purpose |
|--------|---------|---------|
| `channel-partner-prospect` | Tagged `industrial-equipment-distributor` OR `logistics-equipment-distributor` + 2+ distributor capability signals | Flag as potential channel partner/distributor |

## Trigger Conditions

**Required tags (one of):**
- `industrial-equipment-distributor`
- `logistics-equipment-distributor`

**Required capability signals (2+):**
- Multi-brand distribution
- Service/technical support (SAT)
- Spare parts inventory
- Training offering
- Multi-location presence

## Routing Logic

**Updated flow:**

```
Required gate (Sells as expected?)
  ↓
  PASS → Score bonuses → Route by grade
  ↓
  FAIL → Check for special tags:
    - cleaning-services-provider → service-provider-prospect
    - hospitality-service-provider → route-to-ka
    - industrial-equipment-distributor + 2+ signals → channel-partner-prospect
    - logistics-equipment-distributor + 2+ signals → channel-partner-prospect
    - Otherwise → exclude
```

## Output Format

```markdown
## {company_name} - channel-partner-prospect

**URL:** {url}
**Tags:** industrial-equipment-distributor (or logistics-equipment-distributor)
**Action:** channel-partner-prospect

### Company Profile
- **Products:** {products}
- **Services:** {services}
- **Brands:** {brands}
- **Geography:** {geography}
- **Team:** {team_size}

### Key Signals
- ✓ {positive_signal_1}
- ✓ {positive_signal_2}
- ❌ Wrong industry - {their_industry}, not cleaning equipment

### Scoring Details

| Component | Result | Points |
|-----------|--------|--------|
| Sells as expected | FAIL - {their_industry}, NOT cleaning equipment | — |
| Cleaning equipment bonus | None | +0 |
| Competitor footprint bonus | None | +0 |
| Channel capability bonus | {signals detected} | +0 (wrong industry) |

### Channel Partner Potential
Cross-industry distributor with strong capabilities serving target industries (warehouses, logistics).

**Action:** Forward to sales team for channel partnership outreach.
```

## Batch Results Table (Updated)

```markdown
| Action | Count | Companies |
|--------|-------|-----------|
| prioritize | X | {list} |
| standard | X | {list} |
| explore | X | {list} |
| route-to-sales | X | {list} |
| service-provider-prospect | X | {list} |
| channel-partner-prospect | X | {list} |
| route-to-ka | X | {list} |
| exclude | X | {list} |
```

## Files to Modify

| File | Changes |
|------|---------|
| `skills/distributor-inspector/SKILL.md` | Update Step 5 Route, add output format, update scoring table, update batch results table |

## Summary

| Aspect | Decision |
|--------|----------|
| New action | `channel-partner-prospect` |
| Trigger tags | `industrial-equipment-distributor`, `logistics-equipment-distributor` |
| Trigger condition | Tag + 2+ distributor capability signals |
| Action item | Forward to sales team for channel partnership outreach |
