# Facts-Only Scoring Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Enforce facts-only outputs in distributor-inspector skill and fix Channel Capability scoring to use only defined signals.

**Architecture:** Single-file edit to SKILL.md — add Evidence Policy section, update Output Format, replace Channel Capability section with strict table, fix language in Competitor Footprint section.

**Tech Stack:** Markdown documentation

---

### Task 1: Add Evidence Policy Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (insert after line 12, before "## When to Use")

**Step 1: Add Evidence Policy section**

Insert after the Overview section (line 12):

```md
## Evidence Policy (Facts-Only)

**Hard rule:** Only include claims and scoring evidence that are explicitly supported by website content.

- If a capability is not explicitly stated, mark it as **Unknown** — do not infer.
- Do not write implied statements like "trained teams", "after-sales established", "customer base" unless the site explicitly states it.
- Indirect hints go in **Observations**, not capability claims or scoring.

```

**Step 2: Verify insertion**

Read: `skills/distributor-inspector/SKILL.md` lines 1-30
Expected: Evidence Policy section appears after Overview, before "## When to Use"

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs: add Evidence Policy (facts-only) section to distributor-inspector

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 2: Update Output Format - Add Confidence Field

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (Output Format section)

**Step 1: Add Confidence field after Tags**

Find line with `**Tags:** {tag1}, {tag2}` and add after it:

```md
**Confidence:** {high|medium|low}
```

**Step 2: Verify change**

Read: `skills/distributor-inspector/SKILL.md` Output Format section
Expected: Confidence field appears after Tags line

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs: add Confidence field to distributor-inspector output format

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 3: Update Output Format - Replace Key Signals

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (Output Format section)

**Step 1: Replace Key Signals section**

Find:
```md
### Key Signals
{signals_list}
```

Replace with:
```md
### Verified Evidence (quotes/snippets)
- {verbatim or close paraphrase + page context}

### Observations (non-interpretive)
- {objective observation without capability inference}
```

**Step 2: Verify change**

Read: `skills/distributor-inspector/SKILL.md` Output Format section
Expected: Verified Evidence and Observations sections replace Key Signals

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs: replace Key Signals with Verified Evidence + Observations

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 4: Fix Competitor Footprint Language

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (Competitor Footprint Bonus section)

**Step 1: Replace inference-prone language**

Find:
```md
**Why this is a bonus, not a blocker:** Competitor distributors already have:
- Customer base in cleaning robotics
- Sales and deployment teams trained on robots
- After-sales service capability
- Market knowledge and relationships

These are high-value prospects for competitive conversion.
```

Replace with:
```md
**Why this is a bonus, not a blocker:** Competitor distributors are often high-value because they:
- Are already selling comparable products in the category (explicit competitor evidence)
- May already have channel motion for robots (distribution language, partner programs, pricing pages)
- Are typically open to multi-brand portfolios (if the site explicitly mentions multiple brands)

> Note: These are general patterns — do not claim capabilities about a specific company unless explicitly stated.
```

**Step 2: Verify change**

Read: `skills/distributor-inspector/SKILL.md` Competitor Footprint section
Expected: Facts-safe language without inferred claims

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs: use facts-safe language in Competitor Footprint section

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 5: Replace Channel Capability Bonus Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (Channel Capability Bonus section)

**Step 1: Replace entire Channel Capability Bonus section**

Find the entire section starting with `## Channel Capability Bonus` and ending before `## Competitor Detection`.

Replace with:
```md
## Channel Capability Bonus (Facts-Only)

Award points **only** when the website explicitly shows these signals:

| Signal Type | Examples of Explicit Evidence |
|------------|-------------------------------|
| After-sales support | "Service", "Repair", "Spare parts", "Wartung", "Support center", "ticket system" |
| Demo / trial | "Demo", "Vorführung", "Teststellung", "Pilot", "free trial" |
| Multiple brands | Brand pages, logos, "We distribute X, Y, Z" |
| Multiple categories | Separate product categories (e.g., cleaning robots + reception robots + industrial robots) |
| SLA / response times | "SLA", "response within 24h", "Supportzeiten", "Service Level" |

**Scoring:**
- +5 = 1 explicit signal
- +10 = 2 explicit signals
- +20 = 3+ explicit signals **OR** explicit service/repair/training infrastructure page

**Not scored (record as Observation only):**
- Partner portal, warehouse/logistics, quiz — useful signals but not counted for points
```

**Step 2: Verify change**

Read: `skills/distributor-inspector/SKILL.md` Channel Capability section
Expected: New facts-only table with explicit evidence examples

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs: replace Channel Capability with facts-only scoring table

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 6: Add Sales Play Facts-Only Rule

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (Output Format section)

**Step 1: Add facts-only rule to Sales Play section**

Find:
```md
### Sales Play (if applicable)
{play_name}: {play_description}
```

Replace with:
```md
### Sales Play (if applicable)
- Cite only explicitly verified evidence.
- Do not include assumptions like "trained teams" or "after-sales capability" unless the site explicitly states training/service/repair.

{play_name}: {play_description}
```

**Step 2: Verify change**

Read: `skills/distributor-inspector/SKILL.md` Output Format section
Expected: Sales Play includes facts-only bullet points

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs: add facts-only rule to Sales Play section

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 7: Add Routing Precedence

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (Process section)

**Step 1: Add routing precedence to Route step**

Find:
```md
4. **Route**: Return action + play recommendation (if competitor footprint)
```

Replace with:
```md
4. **Route**: Return action + play recommendation (if competitor footprint)

**Routing precedence:** Competitor footprint Tier 1–2 overrides score-based action.
```

**Step 2: Verify change**

Read: `skills/distributor-inspector/SKILL.md` Process section
Expected: Routing precedence documented after Route step

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs: add routing precedence documentation

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 8: Bump Version

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (frontmatter)

**Step 1: Update description to reflect facts-only**

Find frontmatter description and update if needed to indicate facts-only enforcement.

**Step 2: Commit version bump**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "chore: bump version for facts-only scoring feature

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Verification

After all tasks complete:

1. Read full `skills/distributor-inspector/SKILL.md`
2. Verify all acceptance criteria met:
   - [ ] Evidence Policy section exists
   - [ ] Confidence field in output format
   - [ ] Verified Evidence + Observations sections
   - [ ] Competitor footprint language is facts-safe
   - [ ] Channel Capability has explicit table
   - [ ] Sales Play has facts-only rule
   - [ ] Routing precedence documented

3. Test with Terra-Robotics or similar competitor distributor URL to verify facts-only output
