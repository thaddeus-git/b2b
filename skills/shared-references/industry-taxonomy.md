# Industry Taxonomy (Fixed Dictionary)

Classification system for categorizing companies. This is a **fixed dictionary** - do not create new industry values.

**Used by:** lead-classifier, distributor-inspector, ka-inspector, channel-partner-inspector

---

## Format

`{Industry Chinese} ({Industry English}) → {Sub-industry}`

**Example:** `商超 (Retail) → 商超终端方向 - 个体`

---

## Taxonomy Table

| Industry (行业) | English | Sub-industries | Detection Criteria |
|-----------------|---------|----------------|-------------------|
| 餐饮 | F&B | 餐饮代理商 - 供应链方向，餐饮代理商 - 食品类方向，餐饮终端方向 - 个体，餐厅终端方向-KA | Restaurants, food service, F&B distribution |
| 医疗 | Healthcare | 医疗代理商 - 设备方向，医疗终端方向 - 个体，医疗终端方向-KA | Hospitals, clinics, medical equipment distributors |
| 商超 | Retail | 商超终端方向 - 个体，商超终端方向-KA | Supermarkets, retail chains, department stores |
| 酒店 | Hospitality | 酒店代理商 - 供应链方向，酒店终端方向 - 个体，酒店终端方向-KA | Hotels, resorts, hospitality groups |
| 机器人代理商 | Robot Distributor | 机器人业务代理商 | Robot distributors, automation equipment |
| 工厂物流 | Factory/Logistics | 工厂代理商 - 自动化类，工厂终端 - 小型物件，工厂终端 - 大型物件，工厂终端 - 物流方向 | Factories, warehouses, logistics centers |
| IT 信息技术 | IT | IT 代理商 - 餐饮酒店方向，IT 代理商 - 医疗方向，IT 代理商 - 营销方向 | IT services, software, systems integrators |
| 贸易商/批发/零售 | Trading | 贸易代理商 | General trading, wholesale, import/export |
| 金融 | Finance | 金融代理商 | Financial services, banking, insurance |
| 娱乐 | Entertainment | 娱乐终端方向 - 个体 | Entertainment venues, casinos, recreation |
| 服务行业 | Services | 服务代理商 | Business services, consulting, facility services |
| 其他行业 | Other | 其他行业代理商 | Other industries not listed above |
| 弱相关 /不相关 | Unrelated | 无二级行业 | Industry not relevant to cleaning robots |
| 清洁 | Cleaning | 清洁终端，清洁代理商 - 能源类，清洁代理商 - 其他相关类，清洁代理商 - 清洁公司，清洁代理商 - 建材类，清洁代理商 - 机械类 | Cleaning equipment, cleaning services, facility management |

---

## Sub-industry Selection Rules

### For Distributors (cleaning equipment, supplies, etc.)

| Products/Services | Sub-industry |
|-------------------|--------------|
| Floor scrubbers, sweepers, commercial cleaning machines | 清洁代理商 - 机械类 |
| Cleaning chemicals, detergents, consumables | 清洁代理商 - 其他相关类 |
| Cleaning company with equipment | 清洁代理商 - 清洁公司 |
| HVAC/technical building equipment | 清洁代理商 - 建材类 |
| Energy systems related to cleaning | 清洁代理商 - 能源类 |

### For KA End-Users (facilities)

| Facility Type | Sub-industry |
|---------------|--------------|
| Retail chain (multiple locations) | 商超终端方向-KA |
| Single retail store | 商超终端方向 - 个体 |
| Hotel chain | 酒店终端方向-KA |
| Single hotel | 酒店终端方向 - 个体 |
| Hospital/clinic network | 医疗终端方向-KA |
| Single hospital/clinic | 医疗终端方向 - 个体 |
| Restaurant chain | 餐厅终端方向-KA |
| Single restaurant | 餐饮终端方向 - 个体 |
| Warehouse/logistics | 工厂终端 - 物流方向 |
| Factory (small items) | 工厂终端 - 小型物件 |
| Factory (large items) | 工厂终端 - 大型物件 |
| Entertainment venue | 娱乐终端方向 - 个体 |

### For Channel Partners

| Client Industry | Sub-industry |
|-----------------|--------------|
| IT serving F&B/hospitality | IT 代理商 - 餐饮酒店方向 |
| IT serving healthcare | IT 代理商 - 医疗方向 |
| IT serving retail/marketing | IT 代理商 - 营销方向 |
| F&B distribution/supply chain | 餐饮代理商 - 供应链方向 |
| F&B products/food | 餐饮代理商 - 食品类方向 |
| Robot/automation distribution | 机器人业务代理商 |
| General business services | 服务代理商 |
| Medical equipment distribution | 医疗代理商 - 设备方向 |
| Hotel supply chain | 酒店代理商 - 供应链方向 |
| Factory automation | 工厂代理商 - 自动化类 |
| General trading | 贸易代理商 |
| Finance-related services | 金融代理商 |
| Other industries | 其他行业代理商 |

### For Excluded/Unrelated

| Situation | Classification |
|-----------|----------------|
| Industry not relevant to cleaning robots | 弱相关 /不相关 (Unrelated) → 无二级行业 |
| Website under construction / insufficient info | 弱相关 /不相关 (Unrelated) → 无二级行业 |
| Pure B2C with no commercial products | 弱相关 /不相关 (Unrelated) → 无二级行业 |

---

## Individual vs KA Distinction

| Indicator | 个体 (Individual/SMB) | KA (Key Account/Enterprise) |
|-----------|----------------------|----------------------------|
| Locations | 1-2 locations | 3+ locations / chain |
| Employees | <50 employees | 50+ employees |
| Revenue | Local/regional | National/international |
| Procurement | Owner-managed | Centralized procurement function |
| Decision making | Quick, informal | Formal processes, longer cycles |

---

## Related References

- `../distributor-inspector/references/industry-taxonomy.md` - Detailed distributor-focused taxonomy
- `tags.md` - Tag taxonomy for niche market categorization
- `target-segments.md` - Target end-user segments
