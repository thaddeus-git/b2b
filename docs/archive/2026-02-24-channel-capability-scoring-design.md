# Channel Capability Scoring Design

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:writing-plans to create the implementation plan.

**Goal:** Add Channel Capability bonus, cap total score at 100, strengthen Tier 2 competitor detection, and improve tagging guidance for cleaning robot distributors.

**Architecture:** Three focused updates to SKILL.md - add new bonus section, update scoring table with cap rule, enhance competitor detection with SKU canon reference, and add multi-tag guidance for cleaning robot distributors.

**Tech Stack:** Markdown, Agent Skills specification

---

## Decisions Made

1. **Channel Capability bonus**: +5/+10/+20 rubric based on signals from keywords.md
2. **Score cap**: Total score capped at 100
3. **Tier 2 detection**: Reference competing-brands.md for SKU/model detection (no inline list)
4. **Tagging**: Apply both `cleaning-equipment-distributor` and `robotics-distributor` for cleaning robot sellers

---

## Changes to SKILL.md

### 1. Update Scoring Section

**Current:**
```markdown
| Component | Points |
|-----------|--------|
| Required: Sells as expected | PASS/FAIL |
| Bonus: Cleaning equipment | +30 to +90 |
| Bonus: Competitor footprint | +0 to +20 |
```

**New:**
```markdown
| Component | Points |
|-----------|--------|
| Required: Sells as expected | PASS/FAIL |
| Bonus: Cleaning equipment | +30 to +90 |
| Bonus: Competitor footprint | +0 to +20 |
| Bonus: Channel capability | +0 to +20 |

> **Total score capped at 100.**
```

### 2. Add New Section: Channel Capability Bonus

After Competitor Footprint Bonus section, add:

```markdown
## Channel Capability Bonus

Use bonus signals from `references/keywords.md`:

| Points | Evidence |
|--------|----------|
| +5 | 1 capability signal (after-sales OR demo OR multiple brands OR multiple categories OR SLA) |
| +10 | 2 capability signals |
| +20 | 3+ signals OR explicit service/repair/spare parts/training page |

**Signals to detect:**
- After-sales: spare parts, maintenance, technical support, repair
- Showroom/Demo: showroom, demonstration, test drive, trial
- Multiple brands: "brands", "distributors of", "authorized dealer"
- Multiple categories: equipment + supplies + accessories
- Clear SLA: 24/48h response time, service guarantee, SLA
```

### 3. Update Competitor Footprint Bonus - Tier 2

**Current Tier 2:**
```markdown
| Tier 2 | Product pages / Sales evidence | +10 | Product listings, "we sell PUDU models", pricing pages |
```

**New:**
```markdown
| Tier 2 | Product pages / Sales evidence | +10 | Product listings, competitor SKU/model names from `references/competing-brands.md` |
```

### 4. Add Tagging Guidance

In Tag Format section, add after "Multiple tags allowed":

```markdown
**Multiple tags allowed:** If a distributor sells cleaning robots specifically (e.g., "Reinigungsroboter", "robot de nettoyage"), apply both `cleaning-equipment-distributor` AND `robotics-distributor`.
```

### 5. Update Output Format

Add Channel capability bonus line to Scoring Details:

```markdown
- Channel capability bonus: +{bonus} ({signals})
```

---

## Files to Modify

| File | Changes |
|------|---------|
| `skills/distributor-inspector/SKILL.md` | All 5 changes above |
| `~/.claude/skills/distributor-inspector/SKILL.md` | Re-copy after changes |

---

## Expected Impact

**Terra-Robotics example (before):**
- Score: 80 (cleaning +30, competitor +20, no channel bonus)
- Tags: robotics-distributor, competitor-robot-distributor

**Terra-Robotics example (after):**
- Score: 90 (cleaning +30, competitor +20, channel +10 for after-sales + demo + multiple brands)
- Tags: cleaning-equipment-distributor, robotics-distributor, competitor-robot-distributor
- Capped at 100 if exceeds

---

## Version

Bump to 1.3.0 after implementation.
