# Distributor Inspector - Evaluation Workflow

> **Purpose:** Complete flow from URL input to final action recommendation
> **Last Updated:** 2026-02-27

---

## Quick Reference: The Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│  INPUT: URL (e.g., "https://hotel-pendl.at")                            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 1: Navigate & Capture                                             │
│  - playwright-cli open {url}                                            │
│  - playwright-cli snapshot → YAML context                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 2: Extract Company Profile                                        │
│  - Delegate to: references/company-profiler.md                          │
│  - Output: {company, products, services, team, geography, SLA}          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 3: SMB vs. KA CLASSIFICATION (NEW - CRITICAL)                     │
│  - Delegate to: references/smb-classifier.md                            │
│  - Decision: Is this a Key Account or Small Business?                   │
│  - Output: {classification: "SMB" | "KA" | "MID-MARKET"}                │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  IF SMB → AUTO-ROUTE TO nurture/exclude (CAP AT 50)             │   │
│  │  - Single location + <20 employees = SMB                        │   │
│  │  - No procurement function = SMB                                │   │
│  │  - Family operation without departments = SMB                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 4: Hard Gates Evaluation (6 gates)                                │
│  - Delegate to: references/icp-sales/hard-gates.md                      │
│  - Output: {ALL_PASS | SOME_FAIL (1-2) | MOST_FAIL (3+)}                │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  IF MOST_FAIL → ROUTE TO exclude (regardless of bonuses)        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 5: Bonus Scoring                                                  │
│  - Delegate to: references/icp-skill/scoring-matrix.md                  │
│  - Apply bonuses: cleaning equipment, competitor footprint, etc.        │
│  - Output: Raw score (0-270+)                                           │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  APPLY CAPS:                                                    │   │
│  │  - SMB classification → max 50                                  │   │
│  │  - SOME_FAIL gates → max 50                                     │   │
│  │  - ALL_PASS + KA → full 100                                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 6: Route to Action                                                │
│  - Score + Gates → Grade (A/B/C/D/F)                                    │
│  - Special tags → Override action                                       │
│  - Output: {prioritize | standard | explore | nurture | exclude}        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  OUTPUT: Markdown Report                                                │
│  - Company profile                                                      │
│  - Hard gates table (with evidence)                                     │
│  - Scoring breakdown                                                    │
│  - Action recommendation                                                │
│  - Play (if competitor footprint detected)                              │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Who Triggers What?

### Trigger Chain

| Step | Triggered By | Triggers |
|------|--------------|----------|
| 1. Navigate | **User** calls skill with URL | Snapshot YAML |
| 2. Extract | **AI** reads snapshot | Company profile data |
| 3. SMB Classifier | **AI** (after extraction) | Classification result |
| 4. Hard Gates | **AI** (after classification) | Gate pass/fail |
| 5. Scoring | **AI** (after gates) | Raw score |
| 6. Routing | **AI** (after scoring) | Final action |

### Key Insight: SMB Classifier is NOT a Separate Skill Call

The **SMB classifier** (`references/smb-classifier.md`) is a **reference document** - it contains rules/logic that the AI applies **during** the main skill execution. It is NOT called separately.

```
┌─────────────────────────────────────────────────────────────────┐
│                    MAIN SKILL (SKILL.md)                        │
│  Orchestrates the entire workflow                               │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  references/smb-classifier.md                           │   │
│  │  - Contains classification rules                        │   │
│  │  - Applied inline during extraction                     │   │
│  │  - Decision affects scoring caps downstream             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  references/icp-sales/hard-gates.md                     │   │
│  │  - Contains gate evaluation rules                       │   │
│  │  - Applied after classification                         │   │
│  │  - Result affects max eligible grade                    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## SMB vs. KA Classification Logic

### Classification Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLASSIFICATION START                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Employees < 20?   │
                    └─────────┬─────────┘
                              │
              ┌───────────────┴───────────────┐
              │ YES                           │ NO
              ▼                               ▼
    ┌───────────────────┐           ┌───────────────────┐
    │ Single location?  │           │ 2-5 locations?    │
    └─────────┬─────────┘           └─────────┬─────────┘
              │                               │
    ┌─────────┴─────────┐           ┌─────────┴─────────┐
    │ YES               │ NO          │ YES             │ NO
    ▼                   │             ▼                 │
┌───────────┐           │         ┌───────────┐         │
│   SMB     │◄──────────┴────────►│ MID-MARKET│◄────────┤
│ (cap 50)  │                     │ (std评)   │         │
└───────────┘                     └───────────┘         │
      ▲                                                 │
      │                                                 │
      │                              ┌──────────────────┘
      │                              │
      │                    ┌─────────┴─────────┐
      │                    │ 6+ locations?     │
      │                    └─────────┬─────────┘
      │                              │
      │                    ┌─────────┴─────────┐
      │                    │ YES               │ NO
      │                    ▼                   │
      │              ┌───────────┐             │
      │              │    KA     │─────────────┘
      │              │ (full 100)│
      │              └───────────┘
      │
      └─────────────────────────────────────────┐
                                                │
┌────────────────────────────────────────────────┘
│
▼
Also check: No procurement function → SMB
            No department structure → SMB
            Family-only operation → SMB
```

### Classification Rules (from `references/smb-classifier.md`)

| Criterion | SMB Signal | KA Signal |
|-----------|------------|-----------|
| **Employees** | <20 | 20-500 |
| **Locations** | Single property | 2+ branches |
| **Team Structure** | "Family team", no departments | Named departments (Sales, Service) |
| **Revenue** | Not mentioned, <€5M | €10M+ or explicit mentions |
| **Procurement** | No purchasing function visible | "Procurement", "Einkauf" page |
| **Web Presence** | Basic info, booking only | Case studies, resources, careers |

### Classification Outcomes

| Classification | Score Cap | Max Grade | Typical Action |
|----------------|-----------|-----------|----------------|
| **SMB** | 50 | C | nurture or explore |
| **MID-MARKET** | 75 | B | standard |
| **KA** | 100 | A | prioritize |

---

## Hard Gates vs. SMB Classifier: What's the Difference?

### SMB Classifier (Step 3)
- **Purpose:** Classify company scale and sophistication
- **Focus:** Size, structure, procurement maturity
- **Output:** SMB / MID-MARKET / KA
- **Effect:** Applies score CAP

### Hard Gates (Step 4)
- **Purpose:** Verify minimum capability thresholds
- **Focus:** Specific capabilities (SLA, PoC, team functions)
- **Output:** ALL_PASS / SOME_FAIL / MOST_FAIL
- **Effect:** Determines ELIGIBILITY for A/B grade

### Why Both?

```
┌─────────────────────────────────────────────────────────────────┐
│  Example: Large Company with Poor Processes                     │
│                                                                 │
│  Classification: KA (500 employees, 10 locations)               │
│  Hard Gates: SOME_FAIL (no SLA, no PoC capability)              │
│                                                                 │
│  Result: Score cap at 50 (due to gates)                         │
│  Even though it's a KA, it can't be A/B grade                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Example: Small but Specialized Company                         │
│                                                                 │
│  Classification: SMB (15 employees, 1 location)                 │
│  Hard Gates: ALL_PASS (has SLA, PoC, all 3 functions)           │
│                                                                 │
│  Result: Score cap at 50 (due to SMB classification)            │
│  Even with all gates passing, limited scale = limited priority │
└─────────────────────────────────────────────────────────────────┘
```

---

## The Gasthof Pendl Example (Why This Matters)

### What Went Wrong

```
┌─────────────────────────────────────────────────────────────────┐
│  Gasthof Pendl - Original Assessment                            │
│                                                                 │
│  Classification: NOT APPLIED (missing step)                     │
│  Hard Gates: SOME_FAIL (Budget UNCLEAR, PoC UNCLEAR)            │
│  Bonuses Applied:                                               │
│    - Digital maturity: +10 (has website) ← WRONG                │
│    - Cross-team: +10 (family operation) ← WRONG                 │
│  Final Score: 45/100 (Grade C)                                  │
│                                                                 │
│  Problem: Should have been capped at 50 AND routed to nurture   │
│           Bonuses were incorrectly applied for SMB              │
└─────────────────────────────────────────────────────────────────┘
```

### Correct Assessment (With SMB Classifier)

```
┌─────────────────────────────────────────────────────────────────┐
│  Gasthof Pendl - Correct Assessment                             │
│                                                                 │
│  STEP 3 - SMB Classifier:                                       │
│    - Employees: Not stated (family business, likely <20)        │
│    - Locations: Single property (27 rooms, Kalsdorf only)       │
│    - Team: "Family-operated", no departments visible            │
│    - Procurement: No function visible                           │
│    → Classification: SMB                                        │
│                                                                 │
│  STEP 4 - Hard Gates:                                           │
│    - Company Size: FAIL (<20, no revenue data)                  │
│    - Team Capability: FAIL (no dept structure)                  │
│    - SLA: UNCLEAR (no explicit commitments)                     │
│    - PoC: UNCLEAR (no demo policy)                              │
│    - Market Coverage: FAIL (single location)                    │
│    - Price Discipline: UNCLEAR (no signals)                     │
│    → Result: MOST_FAIL (3+ fails)                               │
│                                                                 │
│  STEP 5 - Scoring:                                              │
│    - Base: 0 (MOST_FAIL → exclude tier)                         │
│    - SMB Cap: 50 (irrelevant since base = 0)                    │
│    - Bonuses: None eligible (exclude tier)                      │
│    → Final Score: 0/100                                         │
│                                                                 │
│  STEP 6 - Routing:                                              │
│    → Action: exclude (or nurture if soft approach preferred)    │
└─────────────────────────────────────────────────────────────────┘
```

---

## File Structure & Responsibilities

```
skills/distributor-inspector/
├── SKILL.md                          # ORCHESTRATOR - main workflow
│   └── Calls reference docs in order │
│                                     │
├── references/                       # RULES & REFERENCE DATA
│   ├── smb-classifier.md             # Classification rules (NEW)
│   ├── icp-sales/
│   │   └── hard-gates.md             # Gate evaluation rules
│   ├── icp-skill/
│   │   ├── gate-translation.md       # How to interpret gates
│   │   └── scoring-matrix.md         # Bonus scoring rules
│   ├── tags.md                       # Industry tag taxonomy
│   ├── company-profiler.md           # Extraction rules
│   └── contact-extractor.md          # Contact extraction rules
│
└── docs/
    └── evaluation-workflow.md        # THIS FILE - workflow overview
```

### Document Responsibilities

| Document | Role | When Used |
|----------|------|-----------|
| `SKILL.md` | Orchestrator | Always - entry point |
| `smb-classifier.md` | Classification rules | Step 3 - after extraction |
| `hard-gates.md` | Gate requirements | Step 4 - after classification |
| `gate-translation.md` | Gate interpretation | Step 4 - helps evaluate |
| `scoring-matrix.md` | Bonus points | Step 5 - after gates |

---

## Example: Running the Skill

### User Input
```
Use distributor-inspector skill on https://hotel-pendl.at
```

### Skill Execution Flow (Behind the Scenes)

```
1. AI reads SKILL.md
2. AI navigates to URL, captures snapshot
3. AI extracts company profile using company-profiler.md rules
4. AI applies smb-classifier.md rules:
   → "Single property, family-operated, no departments"
   → Classification: SMB
5. AI evaluates hard gates using hard-gates.md:
   → 3+ FAILs detected
   → Result: MOST_FAIL
6. AI calculates score using scoring-matrix.md:
   → Base = 0 (MOST_FAIL)
   → SMB cap = 50 (not relevant)
   → Final = 0
7. AI routes based on score + gates:
   → Action: exclude
8. AI outputs markdown report
```

---

## Future Improvements

### 1. Pre-Flight URL Check
Before navigation, check domain signals:
- TLD (.de, .fr, .at) → country detection
- Domain age (if API available)
- Known SMB patterns (hotel, gasthof, pension in domain)

### 2. Parallel Enrichment
While snapshot is loading, run:
- LinkedIn company search
- Company register lookup (Impressum/API)
- News mentions

### 3. Confidence Scoring
Each classification/gate result includes confidence level:
- HIGH: Explicit data (e.g., "50 employees")
- MEDIUM: Inferred (e.g., 3+ departments)
- LOW: Weak signals (e.g., team photo only)

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `README.md` | User-facing documentation |
| `docs/design.md` | Architecture decisions |
| `docs/plans/` | Implementation plans |
| `CLAUDE.md` | Project-level instructions |
