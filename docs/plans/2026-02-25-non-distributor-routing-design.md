# Design: Non-Distributor Prospect Routing

**Date:** 2026-02-25
**Status:** Approved

## Problem

The distributor-inspector skill currently routes all non-distributors to `exclude`, but some non-distributors are still valuable prospects:

1. **Cleaning service providers** - They USE equipment (including competitor brands), may want robots for their own operations or become referral partners
2. **Hotel chains** - These are Key Accounts (end customers), not distributors, and should be evaluated differently

## Solution

Add two new routing actions for non-distributor prospects, triggered by tag detection.

## New Actions

| Action | Trigger Tag | Purpose |
|--------|-------------|---------|
| `service-provider-prospect` | `cleaning-services-provider` | Flag as potential service partner/customer |
| `route-to-ka` | `hospitality-service-provider` | Flag as Key Account, suggest KA-inspector |

## Routing Logic

**Updated flow:**

```
Required gate (Sells as expected?)
  ↓
  PASS → Score bonuses → Route by grade (prioritize/standard/explore/route-to-sales)
  ↓
  FAIL → Check for special tags:
    - cleaning-services-provider → service-provider-prospect
    - hospitality-service-provider → route-to-ka
    - Otherwise → exclude
```

## Step 5: Route (Updated)

```markdown
### Step 5: Route

Return action + play recommendation:

**For distributors (PASS required gate):**
- Grade A (90+): `prioritize`
- Grade B (70-89): `standard`
- Grade C (50-69): `explore`
- Tier 1-2 competitor footprint: `route-to-sales` + `competitive-conversion` play

**For non-distributors (FAIL required gate):**
- Tagged `cleaning-services-provider`: `service-provider-prospect`
- Tagged `hospitality-service-provider`: `route-to-ka` + note "Use KA-inspector for Key Account evaluation"
- All others: `exclude`
```

## Output Format

### service-provider-prospect

```markdown
## {company_name} - service-provider-prospect

**URL:** {url}
**Tags:** cleaning-services-provider
**Action:** service-provider-prospect

### Company Profile
- **Services:** {services}
- **Equipment used:** {equipment_brands_if_known}
- **Team:** {team_size}
- **Geography:** {geography}

### Note
This is a cleaning SERVICE provider, not an equipment distributor. They may be interested in:
- Purchasing robots for their own operations
- Becoming a referral partner
- Insights into local cleaning market
```

### route-to-ka

```markdown
## {company_name} - route-to-ka

**URL:** {url}
**Tags:** hospitality-service-provider
**Action:** route-to-ka

### Company Profile
- **Type:** Hotel chain / hospitality group
- **Locations:** {number_of_properties}
- **Geography:** {geography}

### Key Account Potential
This is a potential Key Account (end customer), not a distributor.

**Next step:** Use `KA-inspector` skill to evaluate as Key Account.
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
| route-to-ka | X | {list} |
| exclude | X | {list} |
```

## Files to Modify

| File | Changes |
|------|---------|
| `skills/distributor-inspector/SKILL.md` | Update Step 5 Route, add output formats, update batch results table |

## Summary

| Aspect | Decision |
|--------|----------|
| Cleaning service providers | `service-provider-prospect` action (any with tag) |
| Hotel chains | `route-to-ka` action + KA-inspector suggestion (tag-based) |
| Retail chains | NOT included - stays as `exclude` |
| Detection method | Tag-based (`cleaning-services-provider`, `hospitality-service-provider`) |
