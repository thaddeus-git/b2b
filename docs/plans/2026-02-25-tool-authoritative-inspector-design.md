# Design: Tool-Authoritative Distributor Inspector

**Date:** 2026-02-25
**Status:** Approved

## Problem

The `distributor-inspector` skill doesn't prescribe specific tools, causing the LLM to default to built-in web search and WebFetch instead of:
1. Chrome DevTools MCP for website inspection
2. google-search skill (Bright Data API) for enrichment

## Solution

Update the skill to explicitly require and prescribe specific tools.

## Tool Requirements

| Tool | Purpose | Invoked via |
|------|---------|-------------|
| **Chrome DevTools MCP** | Website inspection (navigate + extract content) | MCP tools |
| **google-search skill** | Enrichment searches | Skill tool |

### Chrome DevTools MCP Tools

| Tool | When to use |
|------|-------------|
| `navigate_page` | Open distributor website |
| `take_snapshot` | Extract accessibility tree (products, services, brands, team info) |
| `take_screenshot` | Optional visual context for ambiguous cases |
| `list_console_messages` | Check for site errors (broken pages) |

### google-search Skill Usage

- Invoke via `Skill` tool with query + locale
- Use for enrichment: company validation, employee count, competitor partnerships

## Process Flow

```
1. NAVIGATE
   → mcp__chrome_devtools__navigate_page(url)

2. EXTRACT CONTENT
   → mcp__chrome_devtools__take_snapshot()
   → Parse accessibility tree for: products, services, brands, team, SLA mentions

3. ENRICH (optional, for high-value prospects)
   → Skill tool: google-search "{company} employees LinkedIn"
   → Skill tool: google-search "{company} {competitor} partnership"

4. CATEGORIZE & SCORE
   → Apply tags from references/tags.md
   → Score: required gate + bonuses (cleaning equipment + competitor footprint + channel capability)

5. ROUTE
   → Return action + play recommendation
```

## Error Handling

- If Chrome DevTools MCP not available → Fail with installation instructions
- If `navigate_page` fails → Return error with URL for manual check
- If `take_snapshot` returns empty → Try `take_screenshot` as fallback

## Dependency Type

**Hard dependency** - Skill requires Chrome DevTools MCP and fails clearly if not installed.

Error message:
```
Chrome DevTools MCP required. Install with:
claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest
```

## Files to Modify

| File | Changes |
|------|---------|
| `skills/distributor-inspector/SKILL.md` | Add Prerequisites section, update Process with explicit tool calls, update Enrichment Workflow |

## SKILL.md Changes

### Add Prerequisites Section

```markdown
## Prerequisites

This skill requires **Chrome DevTools MCP** for website inspection.

Install it first:
claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest

Then restart Claude Code.
```

### Update Process Section

```markdown
## Process

### Step 1: Navigate to Website
Use Chrome DevTools MCP:
- mcp__chrome_devtools__navigate_page(url)

### Step 2: Extract Content
Use Chrome DevTools MCP:
- mcp__chrome_devtools__take_snapshot() → Parse for products, services, brands, team, SLA

### Step 3: Enrich (Optional)
For high-value prospects, use google-search skill via Skill tool:
- Skill: google-search "{company} employees LinkedIn"
- Skill: google-search "{company} {competitor} partnership"

### Step 4: Categorize & Score
Apply tags and scoring rules from references/

### Step 5: Route
Return action + play recommendation
```

### Update Enrichment Workflow Section

Replace generic "combine with google-search skill" with explicit Skill tool invocation.

## Summary

| Aspect | Decision |
|--------|----------|
| Website inspection | Chrome DevTools MCP (`navigate_page`, `take_snapshot`) |
| Enrichment search | google-search skill via Skill tool |
| Dependency type | Hard - fails if MCP not installed |
| Fallback | None - requires Chrome DevTools MCP |
