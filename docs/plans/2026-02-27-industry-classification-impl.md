# Industry Classification Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add industry classification from industries.json taxonomy to distributor-inspector and ka-inspector reports.

**Architecture:** Embed the industry taxonomy directly into both SKILL.md files, add a classification step to the process, and update the output format to include the Industry field in the header section.

**Tech Stack:** Markdown skill files, no code changes required

---

## Task 1: Update distributor-inspector SKILL.md

**Files:**
- Modify: `skills/distributor-inspector/SKILL.md`

**Step 1: Add Industry Classification section after Configuration Files**

Find the line `## Configuration Files` and add this new section BEFORE it:

```markdown
## Industry Classification

Classify each company into the most relevant industry and sub-industry from the taxonomy below.

**Classification criteria:**
- Primary business activity (products/services offered)
- Customer type (agent vs. end user)
- Business model (B2B, B2C, distribution)

**Format:** `{Industry Chinese} ({Industry English}) → {Sub-industry}`

**Example:** `清洁 (Cleaning) → 清洁代理商-机械类`

### Industry Taxonomy

| Industry (行业) | English | Sub-industries |
|-----------------|---------|----------------|
| 餐饮 | F&B | 餐饮代理商-供应链方向, 餐饮代理商-食品类方向, 餐饮终端方向-个体, 餐厅终端方向-KA |
| 医疗 | Healthcare | 医疗代理商-设备方向, 医疗终端方向-个体, 医疗终端方向-KA |
| 商超 | Retail | 商超终端方向-个体, 商超终端方向-KA |
| 酒店 | Hospitality | 酒店代理商-供应链方向, 酒店终端方向-个体, 酒店终端方向-KA |
| 机器人代理商 | Robot Distributor | 机器人业务代理商 |
| 工厂物流 | Factory/Logistics | 工厂代理商-自动化类, 工厂终端-小型物件, 工厂终端-大型物件, 工厂终端-物流方向 |
| IT信息技术 | IT | IT代理商-餐饮酒店方向, IT代理商-医疗方向, IT代理商-营销方向 |
| 贸易商/批发/零售 | Trading | 贸易代理商 |
| 金融 | Finance | 金融代理商 |
| 娱乐 | Entertainment | 娱乐终端方向-个体 |
| 服务行业 | Services | 服务代理商 |
| 其他行业 | Other | 其他行业代理商 |
| 弱相关 /不相关 | Unrelated | 无二级行业 |
| 清洁 | Cleaning | 清洁终端, 清洁代理商-能源类, 清洁代理商-其他相关类, 清洁代理商-清洁公司, 清洁代理商-建材类, 清洁代理商-机械类 |

---
```

**Step 2: Add classification step after Step 4 (Categorize)**

Find the section `### Step 4: Categorize` and add this new step AFTER it (before Step 4.5):

```markdown
### Step 4.1: Classify Industry

Using the Industry Taxonomy below, select the most appropriate industry and sub-industry:

1. **Identify primary business** - What products/services do they primarily offer?
2. **Determine customer type** - Are they an agent/distributor or end user?
3. **Match to taxonomy** - Find the closest match from the Industry Taxonomy table

**Format:** `{Industry Chinese} ({Industry English}) → {Sub-industry}`

**Examples:**
- Cleaning equipment distributor → `清洁 (Cleaning) → 清洁代理商-机械类`
- Hotel chain → `酒店 (Hospitality) → 酒店终端方向-KA`
- IT systems integrator → `IT信息技术 (IT) → IT代理商-餐饮酒店方向`
- Unrelated business → `弱相关 /不相关 (Unrelated) → 无二级行业`
```

**Step 3: Update Output Format header section**

Find the Output Format section and add the Industry field. Change:

```markdown
## {company_name} - {grade} ({score}/100)

**URL:** {url}
**Country:** {country} (detected from TLD/address/content)
**Language:** {language} (detected from content)
**Tags:** {tag1}, {tag2}
**Classification:** {SMB | MID-MARKET | KA}
```

To:

```markdown
## {company_name} - {grade} ({score}/100)

**URL:** {url}
**Country:** {country} (detected from TLD/address/content)
**Language:** {language} (detected from content)
**Tags:** {tag1}, {tag2}
**Industry:** {Industry Chinese} ({Industry English}) → {Sub-industry}
**Classification:** {SMB | MID-MARKET | KA}
```

**Step 4: Commit distributor-inspector changes**

```bash
git add skills/distributor-inspector/SKILL.md
git commit -m "feat(distributor-inspector): Add industry classification from taxonomy

- Add Industry Taxonomy table with Chinese + English labels
- Add Step 4.1 for classifying companies
- Update output format to include Industry field in header

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: Update ka-inspector SKILL.md

**Files:**
- Modify: `skills/ka-inspector/SKILL.md`

**Step 1: Add Industry Classification section before Configuration Files**

Find the line `## Configuration Files` and add this new section BEFORE it:

```markdown
## Industry Classification

Classify each company into the most relevant industry and sub-industry from the taxonomy below.

**Classification criteria:**
- Primary business activity (what facilities/properties do they operate?)
- End user type (retail, hospitality, healthcare, etc.)
- Scale indicator (individual vs. KA)

**Format:** `{Industry Chinese} ({Industry English}) → {Sub-industry}`

**Example:** `商超 (Retail) → 商超终端方向-KA`

### Industry Taxonomy

| Industry (行业) | English | Sub-industries |
|-----------------|---------|----------------|
| 餐饮 | F&B | 餐饮代理商-供应链方向, 餐饮代理商-食品类方向, 餐饮终端方向-个体, 餐厅终端方向-KA |
| 医疗 | Healthcare | 医疗代理商-设备方向, 医疗终端方向-个体, 医疗终端方向-KA |
| 商超 | Retail | 商超终端方向-个体, 商超终端方向-KA |
| 酒店 | Hospitality | 酒店代理商-供应链方向, 酒店终端方向-个体, 酒店终端方向-KA |
| 机器人代理商 | Robot Distributor | 机器人业务代理商 |
| 工厂物流 | Factory/Logistics | 工厂代理商-自动化类, 工厂终端-小型物件, 工厂终端-大型物件, 工厂终端-物流方向 |
| IT信息技术 | IT | IT代理商-餐饮酒店方向, IT代理商-医疗方向, IT代理商-营销方向 |
| 贸易商/批发/零售 | Trading | 贸易代理商 |
| 金融 | Finance | 金融代理商 |
| 娱乐 | Entertainment | 娱乐终端方向-个体 |
| 服务行业 | Services | 服务代理商 |
| 其他行业 | Other | 其他行业代理商 |
| 弱相关 /不相关 | Unrelated | 无二级行业 |
| 清洁 | Cleaning | 清洁终端, 清洁代理商-能源类, 清洁代理商-其他相关类, 清洁代理商-清洁公司, 清洁代理商-建材类, 清洁代理商-机械类 |

---
```

**Step 2: Add classification step after Step 2 (Extract Company Profile)**

Find the section `### Step 2: Extract Company Profile` and add this new step AFTER it (before Step 2.5):

```markdown
### Step 2.1: Classify Industry

Using the Industry Taxonomy below, select the most appropriate industry and sub-industry:

1. **Identify facility type** - What kind of facilities/properties do they operate?
2. **Determine scale** - Individual location or KA (chain/large enterprise)?
3. **Match to taxonomy** - Find the closest match from the Industry Taxonomy table

**For KA inspector, prefer "终端方向-KA" for chains and "终端方向-个体" for single locations.**

**Format:** `{Industry Chinese} ({Industry English}) → {Sub-industry}`

**Examples:**
- Retail chain (Metro, Carrefour) → `商超 (Retail) → 商超终端方向-KA`
- Single hotel → `酒店 (Hospitality) → 酒店终端方向-个体`
- Hospital network → `医疗 (Healthcare) → 医疗终端方向-KA`
- Unrelated business → `弱相关 /不相关 (Unrelated) → 无二级行业`
```

**Step 3: Update Output Format header section**

Find the Output Format section and add the Industry field. Change:

```markdown
---
{Company Name} - {Grade} ({score}/100)

URL: {url}
Country: {country}
Industry: {industry}
Action: {action}

---
```

To:

```markdown
---
{Company Name} - {Grade} ({score}/100)

URL: {url}
Country: {country}
Industry: {industry}
**Industry Classification:** {Industry Chinese} ({Industry English}) → {Sub-industry}
Action: {action}

---
```

**Step 4: Commit ka-inspector changes**

```bash
git add skills/ka-inspector/SKILL.md
git commit -m "feat(ka-inspector): Add industry classification from taxonomy

- Add Industry Taxonomy table with Chinese + English labels
- Add Step 2.1 for classifying KA end customers
- Update output format to include Industry Classification field

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: Verify and Release

**Files:**
- None (verification only)

**Step 1: Verify both SKILL.md files have consistent taxonomy**

```bash
# Check that both files contain the industry taxonomy
grep -c "Industry Taxonomy" skills/distributor-inspector/SKILL.md
grep -c "Industry Taxonomy" skills/ka-inspector/SKILL.md
```

Expected: Both return `1`

**Step 2: Verify output format includes Industry field**

```bash
grep "Industry:" skills/distributor-inspector/SKILL.md | head -2
grep "Industry Classification:" skills/ka-inspector/SKILL.md | head -2
```

Expected: Shows the new Industry fields in output format sections

**Step 3: Release new version**

```bash
./scripts/release.sh 1.21.0
```

---

## Summary

| Task | Description | Commits |
|------|-------------|---------|
| 1 | Update distributor-inspector SKILL.md | 1 |
| 2 | Update ka-inspector SKILL.md | 1 |
| 3 | Verify and release | 1 (via release script) |

**Total commits:** 3 (including release)
