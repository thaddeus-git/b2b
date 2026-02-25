# Non-Distributor Prospect Routing Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add two new routing actions (`service-provider-prospect`, `route-to-ka`) for non-distributor prospects based on tag detection.

**Architecture:** Documentation-only change to SKILL.md. Update routing logic, add output format examples, update batch results table.

**Tech Stack:** Markdown skill file

---

## Task 1: Update Step 5 Route Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (lines 182-189)

**Step 1: Replace Step 5: Route section**

Find the current section (lines 182-189):
```markdown
### Step 5: Route

Return action + play recommendation:
- Grade A (90+): `prioritize`
- Grade B (70-89): `standard`
- Grade C (50-69): `explore`
- Grade D/F (<50): `exclude`
- Tier 1-2 competitor footprint: `route-to-sales` + `competitive-conversion` play
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
- All others: `exclude`
```

**Step 2: Verify the edit**

Run: `grep -A 20 "### Step 5: Route" skills/distributor-inspector/SKILL.md`
Expected: New routing logic with distributor/non-distributor sections visible

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs(skill): add non-distributor routing logic (service-provider-prospect, route-to-ka)"
```

---

## Task 2: Update Scoring Table

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (lines 69-75)

**Step 1: Update the Scoring table**

Find the current table (lines 69-75):
```markdown
| Grade | Score | Action |
|-------|-------|--------|
| A | 90+ | prioritize |
| B | 70-89 | standard |
| C | 50-69 | explore |
| D/F | <50 | exclude |
| Tier 1-2 competitor footprint | — | route-to-sales + play |
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
```

**Step 2: Verify the edit**

Run: `grep -A 10 "| Grade | Score" skills/distributor-inspector/SKILL.md`
Expected: Table now includes non-distributor routing rows

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs(skill): add non-distributor actions to scoring table"
```

---

## Task 3: Add Output Format for service-provider-prospect

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (after Output Format section)

**Step 1: Add new output format after existing Output Format section**

Insert after line 116 (after the existing output format code block):

```markdown

**For service-provider-prospect (cleaning services):**

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
```

**Step 2: Verify the edit**

Run: `grep -A 20 "service-provider-prospect" skills/distributor-inspector/SKILL.md`
Expected: New output format visible

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs(skill): add output format for service-provider-prospect"
```

---

## Task 4: Add Output Format for route-to-ka

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (after service-provider-prospect format)

**Step 1: Add new output format after service-provider-prospect format**

Insert after the service-provider-prospect format:

```markdown

**For route-to-ka (hotel chains / Key Accounts):**

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
```

**Step 2: Verify the edit**

Run: `grep -A 20 "route-to-ka" skills/distributor-inspector/SKILL.md`
Expected: New output format visible

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs(skill): add output format for route-to-ka (Key Accounts)"
```

---

## Task 5: Update Batch Results Table

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (lines 125-131)

**Step 1: Update the batch results table**

Find the current table (lines 125-131):
```markdown
| Action | Count | Companies |
|--------|-------|-----------|
| prioritize | X | {list} |
| standard | X | {list} |
| explore | X | {list} |
| route-to-sales | X | {list} |
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
| route-to-ka | X | {list} |
| exclude | X | {list} |
```

**Step 2: Verify the edit**

Run: `grep -A 10 "| Action | Count" skills/distributor-inspector/SKILL.md`
Expected: Table now includes service-provider-prospect and route-to-ka rows

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs(skill): add non-distributor actions to batch results table"
```

---

## Task 6: Final Verification and Release

**Step 1: Verify complete SKILL.md**

Run: `cat skills/distributor-inspector/SKILL.md`
Expected: All changes present - updated routing logic, new output formats, updated tables

**Step 2: Push changes**

```bash
git push origin main
```

**Step 3: Create release**

```bash
./scripts/release.sh 1.4.6
```

Expected: Version bumped, committed, tagged, pushed, and GitHub release created.

---

## Summary

| Task | Description |
|------|-------------|
| 1 | Update Step 5 Route with non-distributor routing logic |
| 2 | Update Scoring table with new actions |
| 3 | Add output format for service-provider-prospect |
| 4 | Add output format for route-to-ka |
| 5 | Update batch results table |
| 6 | Verify and release v1.4.6 |
