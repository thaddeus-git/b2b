# B2C-Only Retailer No-Scoring Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Skip scoring ONLY for companies that are pure-2c-retail AND have no commercial/B2B products. Companies selling both consumer and commercial products should still be scored.

**Architecture:**
- Detect `pure-2c-retail` tag AND check for any commercial product signals
- If ONLY B2C products → no score, exclude with explanation
- If B2C + B2B products → score normally (they may be valid prospects)

**Key insight:** A retailer selling home robot vacuums AND warehouse cleaning equipment could be a valid distributor for OrionStar's commercial robots.

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

**Step 1: Add pure-2c-retail routing rule with commercial check**

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
| — | — | pure-2c-retail ONLY | exclude |

**Special routing (overrides score):**
- Tagged `pure-2c-retail` with NO commercial products: `exclude` - B2C only, no ToB channels
- Tier 1-2 competitor footprint: `route-to-sales` + `competitive-conversion` play
- Tagged `cleaning-services-provider`: `service-provider-prospect`
- Tagged `hospitality-service-provider`: `route-to-ka`

**Note:**
- Companies tagged `pure-2c-retail` that ALSO sell commercial/industrial products should be scored normally
- Companies that FAIL the gate but score 50+ via customer overlap + channel capability route to `explore`
```

**Step 2: Verify the change**

Run: `grep -A 18 "| Grade | Score |" skills/distributor-inspector/SKILL.md`
Expected: Shows `pure-2c-retail ONLY | exclude` with clarification

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: add pure-2c-retail routing with commercial check

B2C-only retailers without commercial products route to exclude.
Retailers with both B2C and B2B products are scored normally.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: Add Pure-2C-Retail Output Format Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md:121-163` (after service-provider-prospect and route-to-ka examples)

**Step 1: Add output format for B2C-only retailers**

Insert after line 162 (after the route-to-ka example, before the batch results section):

```markdown
**For pure-2c-retail ONLY (no commercial products):**

```markdown
## {company_name} - exclude

**URL:** {url}
**Tags:** pure-2c-retail
**Action:** exclude

### Note
This is a B2C retailer selling only to consumers with no B2B distribution channels.

**Products observed:** {consumer_products}

**Exclusion reason:** No commercial/industrial products or B2B channels detected.

**Next step:** Do not pursue as distributor prospect.
```

**For pure-2c-retail WITH commercial products:**

Score and route normally based on commercial product lines. The `pure-2c-retail` tag is informational only.
```

**Step 2: Verify the change**

Run: `grep -A 25 "For pure-2c-retail ONLY" skills/distributor-inspector/SKILL.md`
Expected: Shows new output format section with both cases

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: add output format for B2C-only and mixed retailers

B2C-only: exclusion report with explanation
B2C+B2B: normal scoring and routing

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 4: Update Scoring Section with Commercial Check Logic

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md:302-312` (Step 5: Score)

**Step 1: Add commercial check before skipping score**

Replace lines 302-312 (entire Step 5: Score section) with:

```markdown
### Step 5: Score

**Check for commercial products:**
- If tagged `pure-2c-retail` AND NO commercial/industrial products detected → Skip scoring, route to `exclude`
- If tagged `pure-2c-retail` BUT has commercial products → Continue scoring (valid prospect)

**Commercial product signals:**
- Cleaning equipment (commercial scrubbers, sweepers, industrial vacuums)
- Facility management products
- Janitorial supplies
- Robotics/automation equipment
- Any B2B/wholesale product lines

Otherwise, apply all bonuses (even if "sells as expected" fails):
- Required: Sells as expected (PASS/FAIL - informational)
- Bonus: Customer overlap (+0 to +50)
- Bonus: Cleaning equipment level (+30 to +90)
- Bonus: Competitor footprint tier (+30 to +90)
- Bonus: Channel capability signals (+0 to +20)

Total score capped at 100.
```

**Step 2: Verify the change**

Run: `grep -A 20 "### Step 5: Score" skills/distributor-inspector/SKILL.md`
Expected: Shows commercial check logic before scoring

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: add commercial product check before skipping score

pure-2c-retail alone doesn't skip scoring.
Only skip if pure-2c-retail AND no commercial products.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5: Update Exclusion Criteria in CLAUDE.md

**Files:**
- Modify: `CLAUDE.md:112-120` (Exclusion Criteria section)

**Step 1: Clarify exclusion criteria with commercial product exception**

Replace lines 114-115:
```markdown
- **Pure 2C retail-oriented**: No ToB channels or B2B delivery capability
```

With:
```markdown
- **Pure 2C retail-oriented**: No ToB channels or B2B delivery capability
  - **Exception:** If they ALSO sell commercial/industrial products → NOT excluded, score normally
  - Example: A shop selling home robot vacuums AND warehouse scrubbers is a valid prospect
```

**Step 2: Verify the change**

Run: `grep -A 8 "### Exclusion Criteria" CLAUDE.md`
Expected: Shows updated exclusion criteria with exception

**Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add commercial product exception to exclusion criteria

Pure B2C retailers are excluded ONLY if they have no commercial products.
Retailers with both B2C and B2B lines are valid prospects.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 6: Add Detection Signals for Commercial Products

**Files:**
- Modify: `skills/distributor-inspector/references/tags.md` (add new section)

**Step 1: Add commercial product detection section**

Insert after line 36 (after Special Tags table):

```markdown
## Pure-2C-Retail vs Mixed Retailer Detection

**B2C-only signals (exclude if ALL present):**
| Signal | Description |
|--------|-------------|
| Shopping cart | "Add to cart", checkout flow for consumers |
| Consumer pricing | Single-unit pricing, no volume/tier pricing |
| No B2B section | No "Become a dealer", "Wholesale", or "Trade" pages |
| Product focus | Home/consumer products only (e.g., robot vacuums for home) |
| No business info | No company registration, tax ID, or trade account options |

**Commercial product signals (score normally if ANY present):**
| Signal | Description |
|--------|-------------|
| Commercial equipment | Floor scrubbers, sweepers, industrial cleaning machines |
| B2B language | "Professional", "Commercial", "Industrial", "B2B" |
| Volume pricing | Tier pricing, bulk discounts, quote requests |
| Trade accounts | Business registration, tax ID required for purchase |
| Facility management | Products for property management, janitorial supplies |
| Warehouse/industrial | Products for warehouses, factories, commercial spaces |

**Decision:**
- ALL B2C signals + NO commercial signals → `pure-2c-retail ONLY` → exclude
- B2C signals + ANY commercial signal → `pure-2c-retail` + relevant commercial tag → score normally
```

**Step 2: Verify the change**

Run: `grep -A 30 "Pure-2C-Retail vs Mixed" skills/distributor-inspector/references/tags.md`
Expected: Shows new detection section with both B2C and commercial signals

**Step 3: Commit**

```bash
git add skills/distributor-inspector/references/tags.md
git commit -m "feat: add commercial product detection signals

Distinguishes between B2C-only retailers (exclude) and
mixed retailers with commercial products (score normally).

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | Update tags.md with exclusion action | `skills/distributor-inspector/references/tags.md:35` |
| 2 | Add pure-2c-retail routing with commercial check | `skills/distributor-inspector/SKILL.md:83-96` |
| 3 | Add output format for B2C-only and mixed retailers | `skills/distributor-inspector/SKILL.md:162` |
| 4 | Add commercial product check before skipping score | `skills/distributor-inspector/SKILL.md:302` |
| 5 | Clarify exclusion in CLAUDE.md with exception | `CLAUDE.md:115` |
| 6 | Add commercial product detection signals | `skills/distributor-inspector/references/tags.md:36+` |

**Expected behavior after implementation:**

| Company Type | Tags | Action |
|--------------|------|--------|
| robotspecialist.com.au (home vacuums only) | `pure-2c-retail` | exclude (no score) |
| Retailer with home + warehouse equipment | `pure-2c-retail`, `cleaning-equipment-distributor` | score normally |
| Retailer with home + FM products | `pure-2c-retail`, `facility-management-distributor` | score normally |

**Decision flow:**
```
pure-2c-retail detected?
  ├─ YES + NO commercial products → exclude (no score)
  └─ YES + HAS commercial products → score normally (valid prospect)
```