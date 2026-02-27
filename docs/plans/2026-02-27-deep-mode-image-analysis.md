# Deep Mode (Image Analysis) Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add optional deep mode with image analysis to distributor-inspector and ka-inspector skills.

**Architecture:** Text-only by default (fast), image analysis when `mode="deep"` requested.

**Tech Stack:** Playwright CLI for screenshots, Claude's vision capabilities for image analysis.

---

## Design Overview

### User Interface

```bash
# Standard mode (fast, text-only) - DEFAULT
distributor-inspector url="example.de"

# Deep mode (slower, includes images)
distributor-inspector url="example.de" mode="deep"
ka-inspector url="example.com" mode="deep"
```

### What Deep Mode Adds

| Analysis | Standard Mode | Deep Mode |
|----------|---------------|-----------|
| Employee count | Text mentions only | + Team photo face count |
| Competitor brands | Text mentions only | + Logo detection in footer |
| Certifications | Text mentions only | + Badge/award image detection |
| Processing time | ~30 seconds | ~90 seconds |

### Screenshots in Deep Mode

| Page | Purpose | Analysis |
|------|---------|----------|
| Home page | Overview, hero images | Brand logos, product images |
| About/Team | Team photos | Employee count verification |
| Products | Product catalog | Product type confirmation |
| Footer (close-up) | Partner logos | Competitor brand detection |

---

## Implementation Tasks

### Task 1: Update distributor-inspector SKILL.md

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md`

**Changes:**
1. Add `mode` argument to skill definition
2. Add "Deep Mode" section explaining image analysis
3. Add screenshot capture step (conditional on mode)
4. Add image analysis prompts for team photos and logos

**Step 1: Add mode argument to skill header**

```yaml
arguments:
  url:
    description: The URL of the website to inspect
    required: true
    type: string
  mode:
    description: Analysis mode: "standard" (text-only, fast) or "deep" (includes image analysis)
    required: false
    type: string
    default: "standard"
```

**Step 2: Add deep mode section**

```markdown
## Deep Mode (Image Analysis)

When `mode="deep"` is specified:

1. **Team Photo Analysis** - Count faces to verify employee count
2. **Logo Detection** - Identify brand logos in footer/partners sections
3. **Certification Badges** - Detect ISO, authorized dealer badges
4. **Product Images** - Visual confirmation of product types

**Processing time:** ~90 seconds (vs ~30 seconds standard)
```

**Step 3: Add screenshot capture step**

```bash
# Deep mode: Capture screenshots
if mode == "deep":
  playwright-cli screenshot -s=inspector --full-page home.png
  playwright-cli goto {url}/about -s=inspector
  playwright-cli screenshot -s=inspector --full-page about.png
  playwright-cli goto {url}/team -s=inspector
  playwright-cli screenshot -s=inspector --full-page team.png
```

---

### Task 2: Update ka-inspector SKILL.md

**Files:**
- Modify: `skills/ka-inspector/SKILL.md`

**Changes:**
- Same as Task 1, but for ka-inspector

---

### Task 3: Create Image Analysis Prompts

**Files:**
- Create: `skills/distributor-inspector/references/image-analyzer.md`
- Create: `skills/ka-inspector/references/image-analyzer.md`

**Content:**

```markdown
# Image Analysis Guide

## Team Photo Analysis

**Goal:** Estimate employee count from team photos

**Process:**
1. Count visible faces in team photos
2. Check for org chart images
3. Look for "X employees" text overlays

**Output format:**
```
Team photo analysis:
- Photo 1: ~8-12 people (group photo)
- Photo 2: ~5 people (leadership team)
- Estimated total: 15-25 employees
```

## Logo Detection

**Goal:** Identify competitor brand logos

**Target brands:** Pudu, Gausium, LionsBot, Tennant, Nilfisk, Kärcher, etc.

**Process:**
1. Scan footer for brand logos
2. Check "Our Partners" page images
3. Look for "Authorized Dealer" badges

**Output format:**
```
Logo detection:
- Footer: Pudu Robotics logo detected
- Partners page: Tennant, Nilfisk logos
- "Authorized Dealer" badge: Gausium
```

## Certification Badges

**Goal:** Detect certifications and awards

**Target badges:**
- ISO 9001, ISO 14001
- "Authorized Dealer", "Certified Partner"
- Industry awards

**Output format:**
```
Certification badges:
- ISO 9001 certified (badge in footer)
- "Top Supplier 2024" award
```
```

---

### Task 4: Update Output Format

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (output format section)
- Modify: `skills/ka-inspector/SKILL.md` (output format section)

**Changes:**

Add "Deep Mode Analysis" section to output (only when mode="deep"):

```markdown
### Deep Mode Analysis

**Team Photos:**
- {analysis results}

**Logo Detection:**
- {analysis results}

**Certifications:**
- {analysis results}
```

---

### Task 5: Test Both Modes

**Files:**
- Test files: N/A (manual testing)

**Step 1: Test standard mode**

```bash
playwright-cli open https://example.de --persistent -s=inspector
playwright-cli snapshot -s=inspector
# Verify: Fast response, text-only extraction
```

**Step 2: Test deep mode**

```bash
playwright-cli open https://example.de --persistent -s=inspector
playwright-cli snapshot -s=inspector
# Request: mode="deep"
# Verify: Screenshots captured, image analysis included
```

**Step 3: Compare results**

- Standard mode should be ~30 seconds
- Deep mode should be ~90 seconds
- Deep mode should have additional image-based findings

---

### Task 6: Update Documentation

**Files:**
- Modify: `README.md`

**Changes:**

Add deep mode documentation:

```markdown
## Deep Mode (Image Analysis)

Both skills support an optional `mode="deep"` argument for enhanced analysis:

```bash
# Standard mode (default) - text-only, fast
distributor-inspector url="example.de"

# Deep mode - includes image analysis
distributor-inspector url="example.de" mode="deep"
ka-inspector url="example.com" mode="deep"
```

**Deep mode adds:**
- Team photo analysis (employee count verification)
- Logo detection (competitor brand identification)
- Certification badge detection

**Processing time:** ~90 seconds (vs ~30 seconds standard)
```

---

## Testing Checklist

| Test | Mode | Expected Result |
|------|------|-----------------|
| distributor-inspector (standard) | text-only | Fast, no image analysis |
| distributor-inspector (deep) | with images | Slower, includes team photos, logos |
| ka-inspector (standard) | text-only | Fast, no image analysis |
| ka-inspector (deep) | with images | Slower, includes facility photos |
| Edge case: No team photos | deep | "No team photos detected" message |
| Edge case: Logo unclear | deep | "Possible [brand] logo (low confidence)" |

---

## Success Criteria

1. ✅ Both skills accept `mode` argument
2. ✅ Standard mode works unchanged (backward compatible)
3. ✅ Deep mode captures screenshots and analyzes images
4. ✅ Image analysis findings are merged into report
5. ✅ Processing time is acceptable (~90 seconds for deep)
6. ✅ Documentation updated with deep mode usage
