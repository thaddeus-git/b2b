# Tool-Authoritative Distributor Inspector Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update distributor-inspector skill to explicitly require Chrome DevTools MCP and google-search skill with specific tool calls.

**Architecture:** Documentation-only change to SKILL.md. Add Prerequisites section, rewrite Process with explicit MCP tool names, update Enrichment Workflow to require Skill tool invocation.

**Tech Stack:** Markdown skill file, Chrome DevTools MCP, google-search skill

---

## Task 1: Add Prerequisites Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (after line 13, after Overview section)

**Step 1: Add Prerequisites section after Overview**

Insert after the Overview section (after line 13):

```markdown
## Prerequisites

This skill requires **Chrome DevTools MCP** for website inspection.

Install it first:
```bash
claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest
```

Then restart Claude Code.

For enrichment searches, this skill uses the **google-search** skill (Bright Data SERP API). Ensure it's configured with valid API credentials.

```

**Step 2: Verify the edit**

Run: `head -30 skills/distributor-inspector/SKILL.md`
Expected: Prerequisites section visible between Overview and When to Use sections

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs(skill): add Prerequisites section requiring Chrome DevTools MCP"
```

---

## Task 2: Replace Process Section with Explicit Tool Calls

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (lines 127-132, Process section)

**Step 1: Replace the Process section**

Replace the existing Process section (lines 127-132):

**Old:**
```markdown
## Process

1. **Digest**: Fetch website, extract key info (company, products, services, brands, team, SLA)
2. **Categorize**: Apply niche market tags (multiple allowed)
3. **Score**: Run required checks + apply bonuses (cleaning equipment + competitor footprint + channel capability)
4. **Route**: Return action + play recommendation (if competitor footprint)
```

**New:**
```markdown
## Process

### Step 1: Navigate to Website

Use Chrome DevTools MCP:
```
mcp__chrome_devtools__navigate_page(url)
```

If navigation fails, return error with URL for manual review.

### Step 2: Extract Content

Use Chrome DevTools MCP:
```
mcp__chrome_devtools__take_snapshot()
```

Parse the accessibility tree output for:
- Company name
- Products and services
- Brands carried
- Team/employee indicators
- SLA/service mentions
- Geographic coverage

If `take_snapshot` returns empty, try `mcp__chrome_devtools__take_screenshot()` as fallback for visual inspection.

### Step 3: Categorize

Apply niche market tags from `references/tags.md` (multiple tags allowed).

### Step 4: Score

Run required gate check + apply bonuses:
- Required: Sells as expected (PASS/FAIL)
- Bonus: Cleaning equipment level (+30 to +90)
- Bonus: Competitor footprint tier (+30 to +90)
- Bonus: Channel capability signals (+0 to +20)

Total score capped at 100.

### Step 5: Route

Return action + play recommendation:
- Grade A (90+): `prioritize`
- Grade B (70-89): `standard`
- Grade C (50-69): `explore`
- Grade D/F (<50): `exclude`
- Tier 1-2 competitor footprint: `route-to-sales` + `competitive-conversion` play
```

**Step 2: Verify the edit**

Run: `grep -A 30 "## Process" skills/distributor-inspector/SKILL.md`
Expected: New process with 5 steps and explicit MCP tool names visible

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs(skill): update Process with explicit Chrome DevTools MCP tool calls"
```

---

## Task 3: Update Enrichment Workflow Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (lines 201-218, Enrichment Workflow section)

**Step 1: Replace the Enrichment Workflow section**

Replace the existing Enrichment Workflow section (lines 201-218):

**Old:**
```markdown
## Enrichment Workflow (Optional)

For deeper due diligence, combine with google-search skill:

### When to Enrich
- High-value prospects (Grade A)
- Competitor distributors (route-to-sales)
- Unclear company information on website

### How to Enrich
1. **Claim Validation:** Search "{company} employees LinkedIn" to verify team size
2. **Market Coverage:** Search "{company} locations" to verify geographic coverage
3. **Competitor Relationship:** Search "{company} {competitor} partnership" to verify claims

### Example Pipeline
Search → Filter URLs → Inspect → (optional) Validate claims

See CLAUDE.md for full multi-skill workflow examples.
```

**New:**
```markdown
## Enrichment Workflow (Optional)

For deeper due diligence, use the **google-search** skill via the Skill tool.

### When to Enrich
- High-value prospects (Grade A)
- Competitor distributors (route-to-sales)
- Unclear company information on website

### How to Enrich

Use the Skill tool to invoke google-search:

```
Skill: google-search
Args: "{company} employees LinkedIn" + locale
```

**Enrichment searches:**
1. **Claim Validation:** `Skill: google-search "{company} employees LinkedIn"`
2. **Market Coverage:** `Skill: google-search "{company} locations"`
3. **Competitor Relationship:** `Skill: google-search "{company} {competitor} partnership"`

**Important:** Use the Skill tool, NOT built-in web search. The google-search skill uses Bright Data SERP API for localized, reliable results.

### Example Pipeline
Search (google-search skill) → Filter URLs → Inspect (this skill) → (optional) Enrich (google-search skill)

See CLAUDE.md for full multi-skill workflow examples.
```

**Step 2: Verify the edit**

Run: `grep -A 25 "## Enrichment" skills/distributor-inspector/SKILL.md`
Expected: New section with explicit "Skill: google-search" syntax visible

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs(skill): update Enrichment Workflow to require Skill tool for google-search"
```

---

## Task 4: Add Error Handling Documentation

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (add new section after Process)

**Step 1: Add Error Handling section after Process section**

Insert after the Process section:

```markdown
## Error Handling

### Chrome DevTools MCP Not Available

If Chrome DevTools MCP tools are not available, fail with:

```
Error: Chrome DevTools MCP required for website inspection.

Install with:
claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest

Then restart Claude Code.
```

### Navigation Failure

If `navigate_page` fails:
1. Return error with the URL
2. Suggest manual review
3. Do NOT fall back to WebFetch

### Empty Snapshot

If `take_snapshot` returns empty content:
1. Try `take_screenshot` for visual inspection
2. Note in output that content extraction was limited
```

**Step 2: Verify the edit**

Run: `grep -A 20 "## Error Handling" skills/distributor-inspector/SKILL.md`
Expected: Error handling section with MCP installation instructions visible

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs(skill): add Error Handling section with MCP dependency instructions"
```

---

## Task 5: Update Skill Description

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (line 3, description field)

**Step 1: Update frontmatter description**

Update line 3 to mention Chrome DevTools MCP:

**Old:**
```yaml
description: Use when evaluating websites as potential distributors for OrionStar Robotics (cleaning robots). Use when needing to score companies against ICP criteria, categorize by niche market, or identify competitor distributors for sales outreach.
```

**New:**
```yaml
description: Use when evaluating websites as potential distributors for OrionStar Robotics (cleaning robots). Requires Chrome DevTools MCP. Use when needing to score companies against ICP criteria, categorize by niche market, or identify competitor distributors for sales outreach.
```

**Step 2: Verify the edit**

Run: `head -5 skills/distributor-inspector/SKILL.md`
Expected: Description mentions "Requires Chrome DevTools MCP"

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs(skill): update description to mention Chrome DevTools MCP requirement"
```

---

## Task 6: Final Verification and Release

**Step 1: Verify complete SKILL.md**

Run: `cat skills/distributor-inspector/SKILL.md`
Expected: All changes present - Prerequisites, updated Process, Error Handling, updated Enrichment Workflow

**Step 2: Push changes**

```bash
git push origin main
```

**Step 3: Create release**

```bash
./scripts/release.sh 1.4.5
```

Expected: Version bumped, committed, tagged, pushed, and GitHub release created.

---

## Summary

| Task | Description |
|------|-------------|
| 1 | Add Prerequisites section |
| 2 | Replace Process with explicit MCP tool calls |
| 3 | Update Enrichment Workflow for Skill tool |
| 4 | Add Error Handling section |
| 5 | Update frontmatter description |
| 6 | Verify and release v1.4.5 |
