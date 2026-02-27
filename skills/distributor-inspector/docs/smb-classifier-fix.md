# SMB Classifier Fix - Implementation Summary

> **Problem:** Single-property businesses (like Gasthof Pendl) were receiving inflated scores due to incorrect bonus awards for SMB-typical signals.
> **Solution:** Added SMB classification step + tightened bonus criteria to prevent SMB signal inflation.
> **Date:** 2026-02-27

---

## Problem Analysis

### What Went Wrong with Gasthof Pendl

**Original Assessment:**
- Classification: **NOT APPLIED** (missing step)
- Gates: SOME_FAIL (Budget UNCLEAR, PoC UNCLEAR)
- Bonuses Applied:
  - Digital maturity: **+10** (had website + Facebook) ← **WRONG**
  - Cross-team: **+10** ("family operation") ← **WRONG**
- Final Score: **45/100** (Grade C)

**Why This Is Wrong:**
1. A single-property Gasthof is clearly an SMB (<20 employees, family-run, one location)
2. SMBs should be capped at 50 points maximum
3. "Has website" is not digital maturity - it's table stakes
4. "Family operation" is not cross-team coordination - it's the absence of department structure

---

## Solution: Two-Layer Cap System

### Layer 1: SMB Classification (NEW - Step 3)

**New document:** `references/smb-classifier.md`

**Classification Criteria:**

| Classification | Employees | Locations | Structure | Score Cap |
|----------------|-----------|-----------|-----------|-----------|
| **SMB** | <20 or unknown | Single property | No departments | 50 |
| **MID-MARKET** | 20-500 | 2-5 branches | Some departments | 75 |
| **KA** | 500+ | 6+ branches | Full structure | 100 |

**SMB Detection Signals:**
- Single property/location (one hotel, one shop)
- "Family business", "Familienbetrieb", no department structure
- Employee count not stated or <20
- No procurement function visible
- Hospitality single-property pattern (Gasthof, Pension)

### Layer 2: Hard Gates (Existing - Step 4)

**Gate Result + Classification determines final cap:**

| Classification | ALL_PASS | SOME_FAIL (1-2) | MOST_FAIL (3+) |
|----------------|----------|-----------------|----------------|
| **SMB** | 50 | 50 | 0 (exclude) |
| **MID-MARKET** | 75 | 50 | 0 (exclude) |
| **KA** | 100 | 50 | 0 (exclude) |

---

## Key Changes Made

### 1. New Files Created

| File | Purpose |
|------|---------|
| `docs/evaluation-workflow.md` | Complete workflow documentation with flowcharts |
| `references/smb-classifier.md` | SMB vs. KA classification rules |

### 2. Updated Files

| File | Changes |
|------|---------|
| `SKILL.md` | Added Step 3 (classification), updated scoring/routing logic, added Classification output section |
| `references/icp-skill/scoring-matrix.md` | Added classification caps, added "Invalid Bonus Signals" section, updated pseudocode |

### 3. Bonus Criteria Tightened

**INVALID Signals (DO NOT SCORE):**

| Bonus | Was Scored For | Now Requires |
|-------|----------------|--------------|
| Digital maturity | Website, Facebook | B2B portal, RFP/tender page |
| Cross-team coordination | "Family operation" | Org chart, 3+ departments |
| Marketing investment | Social media activity | Trade fairs, marketing budget |
| After-sales | "We provide service" | Specific SLA, spare parts, ticketing |

---

## Correct Assessment for Gasthof Pendl

**With the fix applied:**

```
STEP 3 - Classification:
  - Employees: Not stated (family business, likely <20)
  - Locations: 1 (single property in Kalsdorf)
  - Structure: "Family-operated Gasthof", no departments
  → Classification: SMB (HIGH confidence)
  → Score Cap: 50

STEP 4 - Hard Gates:
  - Company Size: FAIL (<20, no revenue data)
  - Team Capability: FAIL (no dept structure)
  - SLA: UNCLEAR (no explicit commitments)
  - PoC: UNCLEAR (no demo policy)
  - Market Coverage: FAIL (single location)
  - Price Discipline: UNCLEAR (no signals)
  → Result: MOST_FAIL (3+ fails)

STEP 5 - Scoring:
  - Base: 0 (MOST_FAIL → exclude tier)
  - SMB Cap: 50 (irrelevant since base = 0)
  - Bonuses: None eligible (exclude tier)
  → Final Score: 0/100

STEP 6 - Routing:
  → Action: exclude (or nurture if soft approach preferred)
```

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  INPUT: URL                                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Navigate & Capture                                     │
│  - playwright-cli snapshot → YAML                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Extract Company Profile                                │
│  - Delegate to: references/company-profiler.md                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: SMB Classifier (NEW)                                   │
│  - Delegate to: references/smb-classifier.md                    │
│  - Output: {SMB | MID-MARKET | KA}                              │
│  - Effect: Applies score cap (50/75/100)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: Hard Gates                                             │
│  - Delegate to: references/icp-sales/hard-gates.md              │
│  - Output: {ALL_PASS | SOME_FAIL | MOST_FAIL}                   │
│  - Effect: Determines base score + additional caps              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: Bonus Scoring                                          │
│  - Delegate to: references/icp-skill/scoring-matrix.md          │
│  - CRITICAL: Do NOT score SMB trap signals                      │
│  - Apply lower of: classification cap or gate cap               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 6: Route to Action                                        │
│  - Classification + Gates + Score → Final action                │
│  - Output: {prioritize | standard | explore | nurture | exclude}│
└─────────────────────────────────────────────────────────────────┘
```

---

## Who Triggers What?

| Step | Triggered By | Triggers |
|------|--------------|----------|
| 1. Navigate | **User** calls skill | Snapshot YAML |
| 2. Extract | **AI** reads snapshot | Company profile |
| 3. Classifier | **AI** (inline, after extraction) | Classification result |
| 4. Gates | **AI** (after classification) | Gate pass/fail |
| 5. Scoring | **AI** (after gates) | Raw score + cap |
| 6. Routing | **AI** (after scoring) | Final action |

**Key Point:** The SMB classifier is **NOT a separate skill call**. It's a reference document (`references/smb-classifier.md`) that contains rules the AI applies **during** the main skill execution.

---

## Testing the Fix

### Test Case 1: Single-Property Hotel (Gasthof Pendl Pattern)

```
Input: https://hotel-pendl.at
Expected:
  - Classification: SMB
  - Gates: MOST_FAIL (3+ fails)
  - Score: 0/100
  - Action: exclude or nurture
```

### Test Case 2: Multi-Location Cleaning Distributor

```
Input: https://frigosystem.de (假设)
Expected:
  - Classification: MID-MARKET (35 emp, 3 locations)
  - Gates: ALL_PASS
  - Score: Up to 75
  - Action: standard or prioritize (if score >= 70)
```

### Test Case 3: Enterprise Distributor

```
Input: Large competitor distributor (e.g., 600 emp, 12 locations)
Expected:
  - Classification: KA
  - Gates: ALL_PASS
  - Score: Up to 100
  - Action: prioritize (if score >= 90)
```

---

## Files to Review

| File | Purpose |
|------|---------|
| `docs/evaluation-workflow.md` | Full workflow with decision trees |
| `references/smb-classifier.md` | Classification rules and examples |
| `SKILL.md` | Main skill with integrated workflow |
| `references/icp-skill/scoring-matrix.md` | Updated scoring with SMB trap warnings |

---

## Next Steps

1. **Test with Gasthof Pendl** - Verify it now scores 0-25 and routes to exclude/nurture
2. **Test with known KAs** - Verify high-scoring distributors still get A grades
3. **Edge cases** - Test mid-market companies to ensure 75 cap applies correctly
