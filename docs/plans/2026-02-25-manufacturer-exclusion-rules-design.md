# Manufacturer Exclusion Rules Design

**Date:** 2026-02-25
**Status:** Approved

## Problem

Traditional cleaning equipment manufacturers (Comac, Dulevo) were incorrectly excluded from distributor scoring. The skill was treating ALL manufacturers as competitors, but only manufacturers of autonomous cleaning robots are actual competitors.

## Root Cause

No explicit exclusion criteria in SKILL.md. The inspector was applying a blanket "manufacturer = exclude" rule.

## Solution

Add explicit "Exclusion Rules" section to SKILL.md that distinguishes between:
- **Competitor manufacturers** (in competing-brands.md) → EXCLUDE
- **Traditional equipment manufacturers** (NOT in competing-brands.md) → SCORE as potential distributor

## Design

### New Section Content

```markdown
## Exclusion Rules

**Exclude only:**

| Category | Criteria | Example |
|----------|----------|---------|
| Competitor manufacturer | Makes autonomous cleaning robots AND is in `references/competing-brands.md` | Nilfisk (Liberty SC50) |
| Wrong segment | Core business is outside cleaning equipment entirely | Europe Service (municipal road equipment) |

**Do NOT exclude:**

| Category | Why | Example |
|----------|-----|---------|
| Traditional equipment manufacturer | Could add robot distribution; has customers, service, market presence | Comac, Dulevo, Fimap |
| Any company NOT in competing-brands.md | Not a direct competitor | — |

**Key distinction:** A manufacturer of traditional scrubbers/sweepers is NOT a competitor. Only manufacturers of autonomous cleaning robots (listed in competing-brands.md) are competitors.
```

### Placement

Insert after the "Process" section (line 153), before "Cleaning Equipment Bonus" section.

### Impact on Previous Inspections

| Company | Previous | With Fix |
|---------|----------|----------|
| Comac France | Excluded (manufacturer) | Score as Strong (+70) - has catalog, service, market presence |
| Dulevo | Excluded (manufacturer) | Score as Moderate/Strong (+50-70) - street cleaning focus |
| Nilfisk | Excluded (competitor) | Still excluded (Liberty SC50 in competing-brands.md) |

## Success Criteria

1. Traditional manufacturers NOT in competing-brands.md are scored, not excluded
2. Competitor manufacturers (in competing-brands.md) are still excluded
3. Wrong segment companies (e.g., municipal equipment) are still excluded
