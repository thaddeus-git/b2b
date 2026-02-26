# Implementation Plan: Playwright CLI Distributor Inspector

**Date:** 2026-02-27
**Goal:** Create CLI-based inspector that produces same full reports as MCP version

---

## Overview

Replace the batch-processing script approach with a simpler inline approach where:
1. Claude uses `playwright-cli` commands directly
2. Snapshot YAML output goes to Claude's context (stdout)
3. Claude applies extraction/scoring rules inline
4. Full report generated in same session

---

## Task 1: Update distributor-inspector-cli/SKILL.md

**File:** `skills/distributor-inspector-cli/SKILL.md`

**Change:** Rewrite as a simple instruction that tells Claude to:
- Use `playwright-cli` for navigation
- Read snapshot YAML from command output
- Apply same reference files as MCP version
- Output same report format

**Before:** Complex batch processing with file-based snapshots
**After:** Simple inline extraction, same as MCP flow

---

## Task 2: Test on Single URL

**Command:**
```bash
cd /Users/thaddeus/skills/playwright-cli-test

# Navigate
playwright-cli open https://lan-security.de --persistent -s=test1

# Capture (YAML appears in stdout)
playwright-cli snapshot -s=test1
```

Then Claude reads the YAML output and applies extraction rules.

**Expected:** Full report like Alpeffect Hotels example

---

## Task 3: Compare Output Quality

Run both MCP and CLI on same URL, compare:
- Company profile extraction
- Contact info completeness
- Tags applied
- Score calculation
- Action recommendation

**Acceptance:** Reports match in quality and format

---

## Task 4: Document Batch Workflow (Optional)

For 50 URLs, document two options:
1. Sequential Claude calls (one per URL)
2. Script capture + batch Claude processing

---

## Files to Modify

| File | Action | Reason |
|------|--------|--------|
| `skills/distributor-inspector-cli/SKILL.md` | Rewrite | Simplify to inline extraction |
| `scripts/batch-inspect.js` | Keep (optional) | Batch capture only |
| `scripts/post-process.js` | Delete | Not needed |
| `scripts/extract-prompt.md` | Delete | Not needed |

---

## Success Criteria

- [ ] Single URL inspection works end-to-end
- [ ] Full report format matches MCP version
- [ ] Same extraction quality
- [ ] Same scoring accuracy
- [ ] Session persistence optional (for batch)

---

## Rollback Plan

If CLI approach doesn't work:
```bash
# Delete worktree
cd /Users/thaddeus/skills/b2b
git worktree remove ../playwright-cli-test

# Continue using MCP version
```
