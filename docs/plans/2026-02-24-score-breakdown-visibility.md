# Score Breakdown Visibility Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update distributor-inspector output format to show detailed evidence for each score component, then run on 13 French distributor URLs.

**Architecture:** Modify Scoring Details section in SKILL.md to include explicit evidence for each bonus point. Then invoke distributor-inspector skill on each URL with facts-only enforcement.

**Tech Stack:** Markdown documentation, web inspection

---

### Task 1: Update Scoring Details Section

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md` (Output Format section)

**Step 1: Replace Scoring Details section**

Find:
```md
### Scoring Details
- Sells as expected: {pass/fail}
- Cleaning equipment bonus: +{bonus}
- Competitor footprint bonus: +{bonus} (Tier X: {evidence})
- Channel capability bonus: +{bonus} ({signals})
- **Total score: {total}** (capped at 100)
```

Replace with:
```md
### Scoring Breakdown

| Component | Points | Evidence |
|-----------|--------|----------|
| Required: Sells as expected | {PASS/FAIL} | {what they sell} |
| Cleaning equipment bonus | +{0-90} | {level}: {specific evidence from site} |
| Competitor footprint bonus | +{0-20} | {Tier X}: {competitor brand + evidence} |
| Channel capability bonus | +{0-20} | {count} signals: {specific signals found} |
| **Total** | **{score}** | (capped at 100) |

**Score calculation:**
- Base: {PASS = continue | FAIL = exclude}
- Cleaning equipment: {reasoning for level chosen}
- Competitor footprint: {reasoning for tier chosen}
- Channel capability: {list each signal with evidence}
```

**Step 2: Verify change**

Read: `skills/distributor-inspector/SKILL.md` Output Format section
Expected: Scoring Breakdown table with Evidence column

**Step 3: Commit**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "docs: add evidence column to Scoring Breakdown table

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 2-14: Run Distributor Inspector on Each URL

For each URL, invoke the distributor-inspector skill with facts-only enforcement.

**URLs to inspect:**
1. https://www.cleantec.fr/
2. https://www.comacfrance.com/
3. https://www.bernard.fr/
4. https://www.europe-service.com/
5. https://www.auto-laveuse.com/
6. https://www.nilfisk.com/
7. https://clean-equipements.com/
8. https://www.autolaveuse.fr/
9. https://www.delaisykargo.com/
10. https://www.autolaveuse-professionnelle-france.fr/
11. https://www.afidistribution.com/
12. https://www.dulevo.com/fr/
13. https://alcnett.com/

**Per-URL task template:**

**Task N: Inspect {domain}**

**Step 1: Invoke distributor-inspector skill**

Use the Skill tool with:
- skill: "distributor-inspector"
- args: "{url}"

**Step 2: Verify output includes**

- [ ] Company name and grade
- [ ] Tags applied
- [ ] Confidence level
- [ ] Action and Play (if applicable)
- [ ] Company Profile
- [ ] Verified Evidence with quotes
- [ ] Observations
- [ ] **Scoring Breakdown table with Evidence column**
- [ ] Sales Play (if applicable)

---

## Verification

After all tasks complete:

1. Compile results into batch summary table
2. Verify all 13 URLs have been inspected
3. Verify each report shows Scoring Breakdown with evidence column
