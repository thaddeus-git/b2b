# Industry Classification in Inspection Reports

**Date:** 2026-02-27
**Status:** Approved

## Overview

Add industry classification from `industries.json` taxonomy to both `distributor-inspector` and `ka-inspector` reports.

## Requirements

1. Classify each inspected company into the industries.json taxonomy
2. Display in header section of report (with URL, Country, Tags)
3. Informational only - does NOT affect scoring or routing
4. Format: Chinese + English (e.g., "清洁 (Cleaning) → 清洁代理商-机械类")

## Industry Taxonomy

| Industry (行业) | Sub-industries |
|-----------------|----------------|
| 餐饮 (F&B) | 餐饮代理商-供应链方向, 餐饮代理商-食品类方向, 餐饮终端方向-个体, 餐厅终端方向-KA |
| 医疗 (Healthcare) | 医疗代理商-设备方向, 医疗终端方向-个体, 医疗终端方向-KA |
| 商超 (Retail) | 商超终端方向-个体, 商超终端方向-KA |
| 酒店 (Hospitality) | 酒店代理商-供应链方向, 酒店终端方向-个体, 酒店终端方向-KA |
| 机器人代理商 (Robot Distributor) | 机器人业务代理商 |
| 工厂物流 (Factory/Logistics) | 工厂代理商-自动化类, 工厂终端-小型物件, 工厂终端-大型物件, 工厂终端-物流方向 |
| IT信息技术 (IT) | IT代理商-餐饮酒店方向, IT代理商-医疗方向, IT代理商-营销方向 |
| 贸易商/批发/零售 (Trading) | 贸易代理商 |
| 金融 (Finance) | 金融代理商 |
| 娱乐 (Entertainment) | 娱乐终端方向-个体 |
| 服务行业 (Services) | 服务代理商 |
| 其他行业 (Other) | 其他行业代理商 |
| 弱相关 /不相关 (Unrelated) | 无二级行业 |
| 清洁 (Cleaning) | 清洁终端, 清洁代理商-能源类, 清洁代理商-其他相关类, 清洁代理商-清洁公司, 清洁代理商-建材类, 清洁代理商-机械类 |

## Implementation

### Files to Modify

| File | Changes |
|------|---------|
| `skills/distributor-inspector/SKILL.md` | Add taxonomy section, add classification step, update output format |
| `skills/ka-inspector/SKILL.md` | Add taxonomy section, add classification step, update output format |

### SKILL.md Changes

#### 1. Add Industry Taxonomy Section

Add after existing reference tables, before Example Usage:

```markdown
### Industry Classification

Classify each company into the most relevant industry and sub-industry:

| Industry (行业) | English | Sub-industries |
|-----------------|---------|----------------|
| 餐饮 | F&B | 餐饮代理商-供应链方向, 餐饮代理商-食品类方向, 餐饮终端方向-个体, 餐厅终端方向-KA |
| ... | ... | ... |
```

#### 2. Add Classification Step

Add new step after categorization:

```markdown
### Step X: Classify Industry

Select the most appropriate industry and sub-industry based on:
- Primary business activity (products/services)
- Customer type (agent vs. end user)
- Business model (B2B, B2C, distribution)

Format: `{Industry Chinese} ({Industry English}) → {Sub-industry}`
Example: `清洁 (Cleaning) → 清洁代理商-机械类`
```

#### 3. Update Output Format

Add `Industry` field to header section after Tags:

```markdown
**Industry:** {Industry Chinese} ({Industry English}) → {Sub-industry}
```

### Example Output

```markdown
## Example Cleaning Corp - B (72/100)

**URL:** https://example.de
**Country:** Germany
**Language:** German
**Tags:** commercial-equipment-distributor, cleaning-focused
**Industry:** 清洁 (Cleaning) → 清洁代理商-机械类
**Classification:** MID-MARKET
**Action:** standard
```

## Out of Scope

- No changes to scoring matrices
- No changes to routing logic
- No changes to hard gates
- No changes to reference files (taxonomy embedded in SKILL.md)
