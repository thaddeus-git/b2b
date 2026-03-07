# Industry Taxonomy

Classification system for categorizing companies during inspection.

## Classification Criteria

- **Primary business activity** - What products/services do they primarily offer?
- **Customer type** - Are they an agent/distributor or end user?
- **Business model** - B2B, B2C, distribution

## Format

`{Industry Chinese} ({Industry English}) → {Sub-industry}`

**Example:** `清洁 (Cleaning) → 清洁代理商-机械类`

---

## Taxonomy Table

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

## Examples

| Company Type | Classification |
|--------------|----------------|
| Cleaning equipment distributor | `清洁 (Cleaning) → 清洁代理商-机械类` |
| Hotel chain | `酒店 (Hospitality) → 酒店终端方向-KA` |
| IT systems integrator | `IT信息技术 (IT) → IT代理商-餐饮酒店方向` |
| Unrelated business | `弱相关 /不相关 (Unrelated) → 无二级行业` |