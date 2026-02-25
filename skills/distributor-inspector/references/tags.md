# Niche Market Tag Taxonomy

> **Tag Format:** `{primary-product-category}-{business-model}`
> **Multiple tags allowed per company**

## Primary Product Categories

| Category | Description | Example Keywords |
|----------|-------------|------------------|
| cleaning-equipment | Floor cleaners, scrubbers, sweepers, vacuums | scrubber, sweeper, commercial cleaning, industrial cleaning |
| cleaning-supplies | Chemicals, consumables, janitorial supplies | detergents, consumables, janitorial, chemicals |
| facility-management | FM services, building management | facility management, IFM, building services |
| cleaning-services | Contract cleaning, janitorial services | cleaning services, contract cleaning, janitorial |
| robotics | Service robots, automation | service robot, cobot, automation |
| industrial-equipment | Industrial machinery and tools | industrial equipment, machinery |
| hospitality-supplies | Hotel/restaurant supplies | hospitality, HORECA, restaurant supplies |
| general-merchandise | General B2B wholesale/retail | wholesale, general trade |

## Business Models

| Model | Description | Detection Signals |
|-------|-------------|-------------------|
| distributor | Sells to B2B/resellers, has network | "distributor", "wholesale", B2B language |
| wholesaler | Bulk sales, volume focus | "wholesale", bulk, trade |
| retailer | Sells to end users | "shop", "store", "buy now" focus |
| service-provider | Offers services alongside products | "services", "maintenance", "support" |
| system-integrator | Integrates solutions | "integration", "solutions provider" |
| manufacturer | Makes products | "manufacturer", "we produce", OEM |

## Special Tags

| Tag | When to Apply | Action |
|-----|---------------|--------|
| competitor-robot-distributor | Sells Pudu/Gausium/LionsBot/etc. | Route to sales team (if not contacted) |
| pure-2c-retail | Only sells to consumers (B2C, no ToB channels) | **Exclude** if NO commercial products; **Score normally** if has commercial products |

## Example Tag Combinations

- `cleaning-equipment-distributor` (primary target)
- `cleaning-supplies-wholesaler`
- `facility-management-service-provider`
- `cleaning-services-provider`
- `robotics-distributor`
- `hospitality-supplies-distributor`
- `cleaning-equipment-service-provider` (sells equipment + provides service)
