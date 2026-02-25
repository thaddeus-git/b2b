# Channel Partner Prospect Routing Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add `channel-partner-prospect` routing action for cross-industry equipment distributors (industrial/logistics) with strong distributor capabilities.

**Architecture:** Documentation-only change to SKILL.md. Update routing logic, add output format, update tables.

**Tech Stack:** Markdown skill file

---

## Task 1: Update Step 5 Route Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (lines 228-241)

**Step 1: Replace Step 5: Route section**

Find the current section (lines 228-241):
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

Replace with:
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
- Tagged `industrial-equipment-distributor` OR `logistics-equipment-distributor` + 2+ distributor capability signals: `channel-partner-prospect`
- All others: `exclude`

**Distributor capability signals for channel-partner-prospect:**
- Multi-brand distribution
- Service/technical support (SAT)
- Spare parts inventory
- Training offering
- Multi-location presence
```

**Step 2: Verify the edit**

Run: `grep -A 25 "### Step 5: Route" skills/distributor-inspector/SKILL.md`
Expected: New routing logic with channel-partner-prospect visible

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs(skill): add channel-partner-prospect routing for cross-industry distributors"
```

---

## Task 2: Update Scoring Table

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (lines 69-77)

**Step 1: Update the Scoring table**

Find the current table (lines 69-77):
```markdown
| Grade | Score | Action |
|-------|-------|--------|
| A | 90+ | prioritize |
| B | 70-89 | standard |
| C | 50-69 | explore |
| D/F | <50 | exclude (or non-distributor routing) |
| Tier 1-2 competitor footprint | — | route-to-sales + play |
| cleaning-services-provider tag | — | service-provider-prospect |
| hospitality-service-provider tag | — | route-to-ka |
```

Replace with:
```markdown
| Grade | Score | Action |
|-------|-------|--------|
| A | 90+ | prioritize |
| B | 70-89 | standard |
| C | 50-69 | explore |
| D/F | <50 | exclude (or non-distributor routing) |
| Tier 1-2 competitor footprint | — | route-to-sales + play |
| cleaning-services-provider tag | — | service-provider-prospect |
| hospitality-service-provider tag | — | route-to-ka |
| industrial/logistics-equipment-distributor + 2+ signals | — | channel-partner-prospect |
```

**Step 2: Verify the edit**

Run: `grep -A 10 "| Grade | Score" skills/distributor-inspector/SKILL.md`
Expected: Table includes channel-partner-prospect row

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs(skill): add channel-partner-prospect to scoring table"
```

---

## Task 3: Add Output Format for channel-partner-prospect

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (after route-to-ka output format)

**Step 1: Add new output format after route-to-ka format**

Find the route-to-ka format that ends with:
```markdown
**Next step:** Use `KA-inspector` skill to evaluate as Key Account.
```
```

Insert AFTER that closing triple backtick:

```markdown

**For channel-partner-prospect (cross-industry distributors):**

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
```

**Step 2: Verify the edit**

Run: `grep -A 30 "channel-partner-prospect" skills/distributor-inspector/SKILL.md`
Expected: New output format visible

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs(skill): add output format for channel-partner-prospect"
```

---

## Task 4: Update Batch Results Table

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (lines 169-177)

**Step 1: Update the batch results table**

Find the current table (lines 169-177):
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

Replace with:
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

**Step 2: Verify the edit**

Run: `grep -A 10 "| Action | Count" skills/distributor-inspector/SKILL.md`
Expected: Table includes channel-partner-prospect row

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs(skill): add channel-partner-prospect to batch results table"
```

---

## Task 5: Final Verification and Release

**Step 1: Verify complete SKILL.md**

Run: `cat skills/distributor-inspector/SKILL.md`
Expected: All changes present - updated routing logic, new output format, updated tables

**Step 2: Push changes**

```bash
git push origin main
```

**Step 3: Create release**

```bash
./scripts/release.sh 1.4.7
```

Expected: Version bumped, committed, tagged, pushed, and GitHub release created.

---

## Summary

| Task | Description |
|------|-------------|
| 1 | Update Step 5 Route with channel-partner-prospect routing |
| 2 | Add channel-partner-prospect to scoring table |
| 3 | Add output format for channel-partner-prospect |
| 4 | Add channel-partner-prospect to batch results table |
| 5 | Verify and release v1.4.7 |
