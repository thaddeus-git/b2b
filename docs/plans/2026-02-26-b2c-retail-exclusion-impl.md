# B2C Retail Exclusion Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add explicit handling for pure-2c-retail companies to skip scoring and route directly to `exclude` action.

**Architecture:** Add a new routing rule that intercepts `pure-2c-retail` tagged companies before scoring, outputs a minimal report without score, and recommends exclusion.

**Tech Stack:** SKILL.md (distributor-inspector skill), tags.md (reference file)

---

## Task 1: Update Tags.md with Pure-2C-Retail Action

**Files:**
- Modify: `skills/distributor-inspector/references/tags.md:30-36` (Special Tags table)

**Step 1: Add action column to pure-2c-retail row**

Replace line 35:
```markdown
| pure-2c-retail | Only sells to consumers | Exclude/downgrade |
```

With:
```markdown
| pure-2c-retail | Only sells to consumers (B2C, no ToB channels) | **Exclude** - Do not score, route to `exclude` action |
```

**Step 2: Verify the change**

Run: `grep "pure-2c-retail" skills/distributor-inspector/references/tags.md`
Expected: Shows updated action text

**Step 3: Commit**

```bash
git add skills/distributor-inspector/references/tags.md
git commit -m "docs: clarify pure-2c-retail exclusion action

Explicitly state that pure B2C retailers should be excluded without scoring.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: Update SKILL.md Routing Logic

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md:83-96` (Scoring table and routing)

**Step 1: Add pure-2c-retail routing rule**

Replace lines 83-96 (the routing table and special routing section) with:

```markdown
| Grade | Score | Condition | Action |
|-------|-------|-----------|--------|
| A | 90+ | PASS gate | prioritize |
| B | 70-89 | PASS gate | standard |
| C | 50-69 | Any | explore |
| D/F | <50 | Any | exclude |
| — | — | Tier 1-2 competitor | route-to-sales |
| — | — | cleaning-services-provider | service-provider-prospect |
| — | — | hospitality-service-provider | route-to-ka |
| — | — | pure-2c-retail | exclude |

**Special routing (overrides score):**
- Tagged `pure-2c-retail`: `exclude` - Do not score, B2C only
- Tier 1-2 competitor footprint: `route-to-sales` + `competitive-conversion` play
- Tagged `cleaning-services-provider`: `service-provider-prospect`
- Tagged `hospitality-service-provider`: `route-to-ka`

**Note:** Companies that FAIL the gate but score 50+ via customer overlap + channel capability route to `explore`.
```

**Step 2: Verify the change**

Run: `grep -A 15 "| Grade | Score |" skills/distributor-inspector/SKILL.md`
Expected: Shows `pure-2c-retail | exclude` in the table

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: add pure-2c-retail to routing table

B2C-only retailers now route directly to exclude without scoring.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: Add Pure-2C-Retail Output Format Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md:121-163` (after service-provider-prospect and route-to-ka examples)

**Step 1: Add output format for excluded B2C retailers**

Insert after line 162 (after the route-to-ka example, before the batch results section):

```markdown
**For pure-2c-retail (excluded):**

```markdown
## {company_name} - exclude

**URL:** {url}
**Tags:** pure-2c-retail
**Action:** exclude

### Note
This is a B2C retailer selling directly to consumers with no B2B distribution channels.

**Exclusion reason:** No ToB channels or B2B delivery capability.

**Next step:** Do not pursue as distributor prospect.
```
```

**Step 2: Verify the change**

Run: `grep -A 15 "For pure-2c-retail" skills/distributor-inspector/SKILL.md`
Expected: Shows new output format section

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: add output format for pure-2c-retail exclusion

Provides clear explanation when excluding B2C-only retailers.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 4: Update Scoring Section with Early Exit Logic

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md:302-312` (Step 5: Score)

**Step 1: Add early exit for pure-2c-retail**

Replace lines 302-312 (entire Step 5: Score section) with:

```markdown
### Step 5: Score

**Early exit:** If tagged `pure-2c-retail`, skip scoring and route to `exclude`.

Otherwise, apply all bonuses (even if "sells as expected" fails):
- Required: Sells as expected (PASS/FAIL - informational)
- Bonus: Customer overlap (+0 to +50)
- Bonus: Cleaning equipment level (+30 to +90)
- Bonus: Competitor footprint tier (+30 to +90)
- Bonus: Channel capability signals (+0 to +20)

Total score capped at 100.
```

**Step 2: Verify the change**

Run: `grep -A 12 "### Step 5: Score" skills/distributor-inspector/SKILL.md`
Expected: Shows early exit instruction at top of scoring section

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: add early exit in scoring for pure-2c-retail

Skip scoring entirely for B2C-only retailers.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5: Update Exclusion Criteria in CLAUDE.md

**Files:**
- Modify: `CLAUDE.md:112-120` (Exclusion Criteria section)

**Step 1: Clarify exclusion criteria**

Replace line 115:
```markdown
- **Pure 2C retail-oriented**: No ToB channels or B2B delivery capability
```

With:
```markdown
- **Pure 2C retail-oriented**: No ToB channels or B2B delivery capability (e.g., home robot vacuum shops, consumer electronics retailers)
```

**Step 2: Verify the change**

Run: `grep -A 5 "### Exclusion Criteria" CLAUDE.md`
Expected: Shows updated exclusion criteria with examples

**Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add examples to pure-2c-retail exclusion

Clarifies that home robot vacuum shops are B2C, not distributors.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 6: Add Detection Signals to Tags.md

**Files:**
- Modify: `skills/distributor-inspector/references/tags.md:20-29` (Business Models table)

**Step 1: Add detection signals for retailer model**

Replace line 25:
```markdown
| retailer | Sells to end users | "shop", "store", "buy now" focus |
```

With:
```markdown
| retailer | Sells to end users | "shop", "store", "buy now", shopping cart, consumer pricing, no B2B/wholesale section |
```

**Step 2: Add pure-2c-retail detection section**

Insert after line 36 (after Special Tags table):

```markdown
## Pure-2C-Retail Detection

**Signals to detect B2C-only retailers:**

| Signal | Description |
|--------|-------------|
| Shopping cart | "Add to cart", checkout flow for consumers |
| Consumer pricing | Single-unit pricing, no volume/tier pricing |
| No B2B section | No "Become a dealer", "Wholesale", or "Trade" pages |
| Product focus | Home/consumer products only (e.g., robot vacuums for home) |
| No business info | No company registration, tax ID, or trade account options |

**When all signals present:** Apply `pure-2c-retail` tag and exclude.
```

**Step 3: Verify the change**

Run: `grep -A 15 "Pure-2C-Retail Detection" skills/distributor-inspector/references/tags.md`
Expected: Shows new detection section

**Step 4: Commit**

```bash
git add skills/distributor-inspector/references/tags.md
git commit -m "feat: add pure-2c-retail detection signals

Helps identify B2C-only retailers for automatic exclusion.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | Update tags.md with exclusion action | `skills/distributor-inspector/references/tags.md:35` |
| 2 | Add pure-2c-retail to routing table | `skills/distributor-inspector/SKILL.md:83-96` |
| 3 | Add output format for exclusions | `skills/distributor-inspector/SKILL.md:162` |
| 4 | Add early exit in scoring | `skills/distributor-inspector/SKILL.md:302` |
| 5 | Clarify exclusion in CLAUDE.md | `CLAUDE.md:115` |
| 6 | Add detection signals | `skills/distributor-inspector/references/tags.md:25, 36+` |

**Expected behavior after implementation:**

When inspecting `robotspecialist.com.au`:
1. Detect B2C retail signals (shopping cart, consumer pricing, no B2B section)
2. Apply `pure-2c-retail` tag
3. Skip scoring entirely (early exit)
4. Output minimal report with exclusion reason
5. Action: `exclude`