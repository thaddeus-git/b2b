# Migrate distributor-inspector to Playwright MCP

**Date:** 2026-02-26
**Status:** Approved
**Author:** Claude + User collaboration

## Problem Statement

The `distributor-inspector` skill currently requires crawl4ai Docker server, which adds complexity:
- External Docker dependency
- Server startup/shutdown management
- Not native to Claude Code tooling

## Goal

Replace crawl4ai with Playwright MCP as the single, unified way to inspect websites. Keep all scoring logic, only change the tooling.

## Architecture

### Current Flow
```
URL → crawl4ai Docker (localhost:11235) → fit_markdown → LLM extracts → Score
```

### New Flow
```
URL → Playwright MCP (browser_navigate) → browser_snapshot → LLM extracts → Score
```

## What Stays (No Changes)

All scoring, routing, and output logic remains:

- Customer overlap bonus (+0 to +50)
- Grade conditions (PASS gate for A/B)
- Special routing (service-provider-prospect, route-to-ka, pure-2c-retail)
- Commercial product exception
- All output format variants
- All reference files (keywords.md, tags.md, competing-brands.md)

## What Changes

### Process Section Only

| Current | New |
|---------|-----|
| crawl4ai Docker prerequisite | Playwright MCP prerequisite |
| `POST /crawl` JSON payload | `browser_navigate` + `browser_snapshot` |
| fit_markdown response | accessibility tree |
| Server status checks | Direct MCP tool calls |

### Tool Mapping

| Action | Old | New |
|--------|-----|-----|
| Load URL | `POST localhost:11235/crawl` | `mcp__plugin_playwright_playwright__browser_navigate` |
| Get content | `fit_markdown` from JSON | `mcp__plugin_playwright_playwright__browser_snapshot` |
| Error handling | Server not running | Navigation failed / timeout |

## New Process Section

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

### Step 3: Categorize

Apply niche market tags from `references/tags.md` (multiple tags allowed).

### Step 4: Score

Check for commercial products first:
- If tagged `pure-2c-retail` AND NO commercial products → Skip scoring, route to `exclude`
- If tagged `pure-2c-retail` BUT has commercial products → Continue scoring

Apply all bonuses:
- Required: Sells as expected (PASS/FAIL - informational)
- Bonus: Customer overlap (+0 to +50)
- Bonus: Cleaning equipment level (+30 to +90)
- Bonus: Competitor footprint tier (+30 to +90)
- Bonus: Channel capability signals (+0 to +20)

Total score capped at 100.

### Step 5: Route

Return action + play recommendation based on score and special routing rules.
```

## File Changes

| File | Action |
|------|--------|
| `skills/distributor-inspector/SKILL.md` | Replace Prerequisites + Process sections |
| `CLAUDE.md` | Remove crawl4ai references |
| `scripts/crawl4ai-server.sh` | Delete |
| `docs/plans/2026-02-25-crawl4ai-*.md` | Delete |
| `docs/plans/2026-02-26-migrate-to-playwright-mcp.md` | This file |

## Expected Outcome

The distributor-inspector skill will:
1. Use Playwright MCP exclusively for website navigation and content extraction
2. No longer require crawl4ai Docker server
3. No longer reference Chrome DevTools MCP
4. Have clear, simplified setup instructions (just install Playwright MCP)
5. Keep all current scoring logic intact

## Prerequisites for Users

- Claude Code with Playwright MCP installed
- No additional Docker containers or servers required