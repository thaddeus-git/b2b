# Migrate distributor-inspector to Playwright MCP

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace crawl4ai with Playwright MCP as the single, unified way to inspect websites in the distributor-inspector skill. Keep all scoring logic intact.

**Architecture:** Remove crawl4ai Docker dependency. Use Playwright MCP for all website navigation and content extraction. Update SKILL.md to reflect the simpler approach.

**Tech Stack:** Playwright MCP (replaces crawl4ai)

---

## Task 1: Update SKILL.md Prerequisites Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (Prerequisites section, lines 14-38)

**Step 1: Replace the Prerequisites section**

Find the current Prerequisites section (starts with `## Prerequisites`) and replace it with:

```markdown
## Prerequisites

This skill uses **Playwright MCP** for website content extraction.

### Setup

Playwright MCP comes pre-installed with Claude Code. No additional setup required.

If you need to install it manually:

```bash
claude mcp add playwright npx @anthropic-ai/playwright-mcp
```

Then restart Claude Code.
```

**Step 2: Verify the change**

Run: `grep -A 10 "## Prerequisites" skills/distributor-inspector/SKILL.md`
Expected: Shows Playwright MCP prerequisites (not crawl4ai)

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: replace crawl4ai with Playwright MCP in prerequisites

Remove crawl4ai Docker setup, add Playwright MCP (pre-installed).

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: Update SKILL.md Process Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (Process section, lines ~232-400)

**Step 1: Replace the Process section**

Find the current Process section (starts with `## Process`) and replace everything through the end of Step 3 with:

```markdown
## Process

Use Playwright MCP for website content extraction.

### Step 1: Navigate and Capture

Use Playwright MCP tools:
1. `browser_navigate` - load the website URL
2. `browser_snapshot` - capture accessibility tree content

### Step 2: Extract Company Profile

Parse the accessibility snapshot for:
- Company name
- Products and services
- Brands carried
- Team/employee indicators
- SLA/service mentions
- Geographic coverage

If navigation fails or snapshot is empty, return error with URL for manual review.

### Step 3: Categorize

Apply niche market tags from `references/tags.md` (multiple tags allowed).

### Step 4: Score

Check for commercial products first:
- If tagged `pure-2c-retail` AND NO commercial products detected → Skip scoring, route to `exclude`
- If tagged `pure-2c-retail` BUT has commercial products → Continue scoring (valid prospect)

Commercial product signals:
- Cleaning equipment (commercial scrubbers, sweepers, industrial vacuums)
- Facility management products
- Janitorial supplies
- Robotics/automation equipment
- Any B2B/wholesale product lines

Apply all bonuses (even if "sells as expected" fails):
- Required: Sells as expected (PASS/FAIL - informational)
- Bonus: Customer overlap (+0 to +50)
- Bonus: Cleaning equipment level (+30 to +90)
- Bonus: Competitor footprint tier (+30 to +90)
- Bonus: Channel capability signals (+0 to +20)

Total score capped at 100.

### Step 5: Route

Return action + play recommendation based on score:

| Score | Gate | Action |
|-------|------|--------|
| 90+ | PASS | `prioritize` |
| 70-89 | PASS | `standard` |
| 50-69 | Any | `explore` |
| <50 | Any | `exclude` |

**Special routing (overrides score):**
- Tier 1-2 competitor footprint: `route-to-sales` + `competitive-conversion` play
- Tagged `cleaning-services-provider`: `service-provider-prospect`
- Tagged `hospitality-service-provider`: `route-to-ka`

**Note:** Companies that FAIL the gate but score 50+ via customer overlap + channel capability route to `explore`.
```

**Step 2: Verify the change**

Run: `grep -A 20 "## Process" skills/distributor-inspector/SKILL.md`
Expected: Shows Playwright MCP process steps (not crawl4ai)

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: replace crawl4ai with Playwright MCP in process

Simplify to browser_navigate + browser_snapshot, keep all scoring logic.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: Update SKILL.md Error Handling Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (Error Handling section)

**Step 1: Replace the Error Handling section**

Find the Error Handling section and replace with:

```markdown
## Error Handling

### Navigation Failure

If the website cannot be accessed:
1. Check the URL is correct and accessible
2. Verify the website is not blocking automated access
3. Return error with the URL for manual review

### Empty Content

If the accessibility snapshot is empty or missing key information:
1. Try scrolling the page with `browser_press_key` to load lazy content
2. Check if the page requires JavaScript interaction
3. Return error with URL for manual review
```

**Step 2: Verify the change**

Run: `grep -A 15 "## Error Handling" skills/distributor-inspector/SKILL.md`
Expected: Shows Playwright MCP error handling (not crawl4ai server errors)

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat: replace crawl4ai with Playwright MCP in error handling

Remove crawl4ai server errors, add Playwright navigation guidance.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 4: Remove crawl4ai Files and References

**Files:**
- Check: `scripts/crawl4ai-server.sh`
- Check: `CLAUDE.md`
- Check: `docs/plans/`

**Step 1: Check for crawl4ai-server.sh**

Run: `ls -la scripts/crawl4ai-server.sh 2>/dev/null || echo "File not found"`

If it exists:
```bash
git rm scripts/crawl4ai-server.sh
```

**Step 2: Update CLAUDE.md**

Run: `grep -n "crawl4ai" CLAUDE.md`

If any references exist, update them to mention Playwright MCP instead, or remove them.

**Step 3: Remove obsolete design docs**

Run: `ls docs/plans/*crawl4ai* 2>/dev/null`

If any crawl4ai-related plan files exist:
```bash
git rm docs/plans/*crawl4ai*
```

**Step 4: Remove obsolete migration plan**

```bash
git rm docs/plans/2026-02-26-migrate-to-playwright-mcp.md 2>/dev/null || echo "Already removed or not found"
```

**Step 5: Commit (if changes made)**

```bash
git add -A
git commit -m "chore: remove crawl4ai files and references

Clean up obsolete Docker setup and design docs.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5: Update SKILL.md Description

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (frontmatter description)

**Step 1: Update the description**

Find the frontmatter description (line 2-3) and update it to remove crawl4ai reference:

```markdown
---
name: distributor-inspector
description: Use when evaluating websites as potential distributors for OrientStar Robotics (cleaning robots). Use when needing to score companies against ICP criteria, categorize by niche market, or identify competitor distributors for sales outreach.
---
```

Remove any mention of "Requires crawl4ai Docker server" if present.

**Step 2: Verify the change**

Run: `head -5 skills/distributor-inspector/SKILL.md`
Expected: Shows updated description without crawl4ai

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs: remove crawl4ai from skill description

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | Update Prerequisites to Playwright MCP | `skills/distributor-inspector/SKILL.md:14-38` |
| 2 | Update Process to Playwright MCP | `skills/distributor-inspector/SKILL.md:232+` |
| 3 | Update Error Handling to Playwright MCP | `skills/distributor-inspector/SKILL.md` |
| 4 | Remove crawl4ai files and references | `scripts/`, `CLAUDE.md`, `docs/plans/` |
| 5 | Update skill description | `skills/distributor-inspector/SKILL.md` |

**Expected outcome:**

The distributor-inspector skill will:
1. Use Playwright MCP exclusively for website navigation and content extraction
2. No longer require crawl4ai Docker server
3. No longer reference Chrome DevTools MCP
4. Have clear, simplified setup instructions
5. Keep all current scoring logic intact

Users will only need:
1. Claude Code with Playwright MCP (pre-installed)
2. No additional Docker containers or servers