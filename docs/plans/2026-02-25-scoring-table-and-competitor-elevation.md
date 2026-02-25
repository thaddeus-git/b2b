# Scoring Table Format & Competitor Footprint Elevation

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Convert scoring details to table format and elevate competitor footprint bonus to match cleaning equipment bonus levels (+30 to +90).

**Architecture:** Modify SKILL.md to update scoring rules and output format template. The competitor footprint bonus becomes as valuable as cleaning equipment bonus because competitor distributors are the best prospects - they already have the infrastructure, training, and customer base.

**Tech Stack:** Markdown skill file modification

---

### Task 1: Update Scoring Structure in SKILL.md

**Files:**
- Modify: `/Users/thaddeus/.claude/skills/distributor-inspector/SKILL.md:46-66`

**Step 1: Update the Scoring table section**

Replace lines 46-66 with:

```markdown
## Scoring

| Component | Points |
|-----------|--------|
| Required: Sells as expected | PASS/FAIL |
| Bonus: Cleaning equipment | +30 to +90 |
| Bonus: Competitor footprint | +30 to +90 |
| Bonus: Channel capability | +0 to +20 |

> **Total score capped at 100.**

| Grade | Score | Action |
|-------|-------|--------|
| A | 90+ | prioritize |
| B | 70-89 | standard |
| C | 50-69 | explore |
| D/F | <50 | exclude |
| Tier 1-2 competitor footprint | — | route-to-sales + play |

**Competitor footprint triggers special routing:**
- If Tier 1-2 competitor evidence → Action: `route-to-sales`, Play: `competitive-conversion`
- If no/minimal competitor footprint → Action based on score above
```

**Step 2: Verify the change**

Run: Read the file and confirm the scoring table shows competitor footprint as +30 to +90

---

### Task 2: Update Competitor Footprint Bonus Table

**Files:**
- Modify: `/Users/thaddeus/.claude/skills/distributor-inspector/SKILL.md:140-154`

**Step 1: Update the Competitor Footprint Bonus table**

Replace lines 140-154 with:

```markdown
## Competitor Footprint Bonus

| Tier | Evidence | Points | Example |
|------|----------|--------|---------|
| Tier 1 | Official distributor / Authorized partner language | +90 | "Official distributor of PUDU", "Authorized Gausium partner" |
| Tier 2 | Product pages / Sales evidence / Multiple competitor products | +60 | Product listings, competitor SKU/model names from `references/competing-brands.md` |
| Tier 3 | Single product mention / Comparison mentions | +30 | Blog posts, comparisons, "compatible with..." |

**Why competitor footprint is a TOP signal:** Competitor distributors are the BEST prospects because they already have:
- Customer base in cleaning robotics
- Sales and deployment teams trained on robots
- After-sales service capability
- Market knowledge and relationships
- Proven willingness to invest in robot inventory

**This is MORE valuable than generic cleaning equipment sales** because the jump from cleaning equipment to robots is harder than switching robot brands.
```

**Step 2: Verify the change**

Run: Read the file and confirm the competitor footprint bonus table shows +30/+60/+90 tiers

---

### Task 3: Update Output Format Template

**Files:**
- Modify: `/Users/thaddeus/.claude/skills/distributor-inspector/SKILL.md:91-96`

**Step 1: Convert Scoring Details to table format**

Replace lines 91-96 with:

```markdown
### Scoring Details

| Component | Result | Points |
|-----------|--------|--------|
| Sells as expected | {pass/fail with reason} | — |
| Cleaning equipment bonus | {level with evidence} | +{bonus} |
| Competitor footprint bonus | {tier with evidence} | +{bonus} |
| Channel capability bonus | {signals detected} | +{bonus} |
| **Total** | (capped at 100) | **{total}** |
```

**Step 2: Verify the change**

Run: Read the file and confirm the output format shows a table for scoring details

---

### Task 4: Update Competitor Detection Section

**Files:**
- Modify: `/Users/thaddeus/.claude/skills/distributor-inspector/SKILL.md:178-187`

**Step 1: Update the competitor detection routing table**

Replace lines 178-187 with:

```markdown
**When competitor products found:**
1. Apply `competitor-robot-distributor` tag
2. Score competitor footprint tier (+30 to +90 bonus)
3. Route to sales with play label:

| Tier | Bonus | Action | Play | Sales Approach |
|------|-------|--------|------|----------------|
| Tier 1 | +90 | route-to-sales | `competitive-conversion` | "You're already a robot distributor. Here's why adding OrientStar grows your margin and de-risks your supply chain..." |
| Tier 2 | +60 | route-to-sales | `competitive-conversion` | "You're selling [competitor]. Here's what OrientStar does better for [specific use case]..." |
| Tier 3 | +30 | route-to-sales or prioritize | `competitive-conversion` | "You mentioned [competitor]. Let's discuss how OrientStar complements or replaces that..." |
```

**Step 2: Verify the change**

Run: Read the file and confirm the routing table shows the new bonus levels

---

### Task 5: Update the Project Copy of SKILL.md

**Files:**
- Modify: `/Users/thaddeus/projects/possible_distributor_inspection/skills/distributor-inspector/SKILL.md`

**Step 1: Apply the same changes to the project copy**

The project has its own copy at `skills/distributor-inspector/SKILL.md`. Apply all the same changes from Tasks 1-4.

**Step 2: Verify both files are in sync**

Run: `diff /Users/thaddeus/.claude/skills/distributor-inspector/SKILL.md /Users/thaddeus/projects/possible_distributor_inspection/skills/distributor-inspector/SKILL.md`

Expected: No differences (or only version-specific differences)

---

### Task 6: Update Example Report

**Files:**
- Modify: `/Users/thaddeus/projects/possible_distributor_inspection/workspace/batch-2026-02-25/14-jobotto-fr.md:24-29`

**Step 1: Update the Scoring Details section to table format**

Replace lines 24-29 with:

```markdown
### Scoring Details

| Component | Result | Points |
|-----------|--------|--------|
| Sells as expected | PASS - robotics distributor with service and cleaning robots | — |
| Cleaning equipment bonus | Moderate - sells cleaning robots but service robots are primary | +60 |
| Competitor footprint bonus | Tier 1 - Official PUDU distributor language | +90 |
| Channel capability bonus | Configuration, training, maintenance, rental/leasing, accessories | +20 |
| **Total** | (capped at 100) | **100** |
```

**Step 2: Update the grade to reflect new scoring**

With the new scoring, Jobotto would be:
- Cleaning equipment: +60
- Competitor footprint: +90 (Tier 1)
- Channel capability: +20
- Total: 170 → capped at 100

The grade stays A+ but the reasoning is clearer.

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md workspace/batch-2026-02-25/14-jobotto-fr.md docs/plans/2026-02-25-scoring-table-and-competitor-elevation.md
git commit -m "feat: elevate competitor footprint scoring and add table format

- Competitor footprint bonus now +30/+60/+90 (was +0/+10/+20)
- Scoring details now displayed as table in reports
- Competitor distributors are BEST prospects, scoring reflects this"
```

---

## Summary of Changes

| Change | Before | After |
|--------|--------|-------|
| Competitor footprint Tier 1 | +20 | +90 |
| Competitor footprint Tier 2 | +10 | +60 |
| Competitor footprint Tier 3 | +0 | +30 |
| Scoring Details format | Bullet list | Table |
| Rationale | Competitor = bonus | Competitor = BEST signal |

**Why this matters:** A company selling Pudu robots is more valuable than a company selling floor scrubbers. The robot distributor already knows how to sell, deploy, and service autonomous cleaning equipment. The jump from "knows Pudu" to "knows OrientStar" is much smaller than from "knows cleaning supplies" to "knows robots".
