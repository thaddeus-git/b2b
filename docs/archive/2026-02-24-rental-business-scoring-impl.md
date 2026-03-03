# Rental Business Scoring Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update distributor-inspector SKILL.md to properly score rental businesses as viable distributors.

**Architecture:** Modify two sections of SKILL.md: (1) Cleaning Equipment Bonus to include rental services as "active in market" evidence, (2) Channel Capability Bonus to count rental as demo/trial signal.

**Tech Stack:** Markdown documentation

---

## Task 1: Update Cleaning Equipment Bonus Table

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md:156-164`

**Step 1: Edit the Cleaning Equipment Bonus table**

Change lines 156-164 from:

```markdown
## Cleaning Equipment Bonus

| Level | Evidence | Points |
|-------|----------|--------|
| Light | Mentions cleaning equipment | +30 |
| Moderate | Has product category | +50 |
| Strong | Core offering, multiple products | +70 |
| Dominant | Primary business, extensive catalog | +90 |
```

To:

```markdown
## Cleaning Equipment Bonus

| Level | Evidence | Points |
|-------|----------|--------|
| Light | Mentions cleaning equipment, informational only | +30 |
| Moderate | Active in market: product catalog OR rental services OR Devis fulfillment | +50 |
| Strong | Core business: multiple products/rentals with pricing, established operations | +70 |
| Dominant | Primary business: extensive catalog/inventory, major distributor | +90 |

**Key insight:** Rental businesses are valid distributors. If they can survive renting/selling cleaning equipment, they can survive with cleaning robots.
```

**Step 2: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs: add rental services to cleaning equipment bonus criteria

- Rental services = active in market = Moderate (+50)
- Devis fulfillment also counts as active in market
- Rental businesses are viable robot distribution partners"
```

---

## Task 2: Update Channel Capability Bonus Table

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md:184-187`

**Step 1: Add rental to Demo / trial signal**

Change lines 184-187 from:

```markdown
| Signal Type | Examples of Explicit Evidence |
|------------|-------------------------------|
| After-sales support | "Service", "Repair", "Spare parts", "Wartung", "Support center", "ticket system" |
| Demo / trial | "Demo", "Vorführung", "Teststellung", "Pilot", "free trial" |
```

To:

```markdown
| Signal Type | Examples of Explicit Evidence |
|------------|-------------------------------|
| After-sales support | "Service", "Repair", "Spare parts", "Wartung", "Support center", "ticket system" |
| Demo / trial / rental | "Demo", "Vorführung", "Teststellung", "Pilot", "free trial", "Location", "rental", "leasing" |
```

**Step 2: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs: add rental to channel capability demo/trial signal

- Rental services count as demo/trial capability
- Customers can try equipment before committing
- Adds Location/rental/leasing keywords"
```

---

## Task 3: Bump Version

**Files:**
- Modify: `.claude-plugin/plugin.json`

**Step 1: Update version**

Change line 3 from:
```json
  "version": "1.3.0",
```

To:
```json
  "version": "1.3.1",
```

**Step 2: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "chore: bump version to 1.3.1 for rental business scoring"
```

---

## Task 4: Push to Remote

**Step 1: Push all commits**

```bash
git push origin inspection
```

---

## Verification

After all tasks complete:
1. [ ] SKILL.md Cleaning Equipment Bonus includes rental services
2. [ ] SKILL.md Channel Capability includes rental in demo/trial
3. [ ] Version bumped to 1.3.1
4. [ ] All commits pushed to remote

## Example: autolaveuse.fr Re-scored

| Component | Points | Evidence |
|-----------|--------|----------|
| Required | PASS | Rents cleaning equipment |
| Cleaning equipment | +50 | Moderate: Active rental business with pricing |
| Competitor footprint | +0 | No competitor brands |
| Channel capability | +20 | 3+ signals: Rental, Devis, Multiple categories |
| **Total** | **70** | **B grade → standard** |
