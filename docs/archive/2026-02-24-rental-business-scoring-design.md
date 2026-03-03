# Rental Business Scoring Design

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:writing-plans to create implementation plan.

**Date:** 2026-02-24
**Status:** Approved

## Problem Statement

The current scoring criteria penalizes rental businesses and lead-gen-style sites that are actually viable distributors. The autolaveuse.fr case revealed that:

1. Rental businesses are valid distributors - they've proven they "can survive" in the cleaning equipment market
2. Having rental services with pricing = active in market = Moderate cleaning equipment bonus
3. Multiple capability signals (rental, Devis, multiple categories) = strong channel capability

## Design Decision

### Cleaning Equipment Bonus (Revised)

| Level | Evidence | Points |
|-------|----------|--------|
| Light | Mentions cleaning equipment, informational only | +30 |
| Moderate | **Active in market: product catalog OR rental services OR Devis fulfillment** | +50 |
| Strong | Core business: multiple products/rentals with pricing, established operations | +70 |
| Dominant | Primary business: extensive catalog/inventory, major distributor | +90 |

**Key change:** "Active in market" now explicitly includes rental services and Devis fulfillment, not just product catalogs.

### Channel Capability Bonus (Clarification)

Rental services count as "Demo / trial" signal because:
- Rental = customers can try equipment before buying
- Demonstrates fulfillment capability
- Shows customer acquisition model

| Signal Type | Examples |
|------------|----------|
| After-sales support | "Service", "Repair", "Spare parts", "SAV" |
| Demo / trial | "Demo", "Test", "Pilot", **Rental services**, Location |
| Multiple brands | Brand pages, logos, "We distribute X, Y, Z" |
| Multiple categories | Separate product categories |
| SLA / response times | "SLA", "response within 24h" |

**Scoring:** +5 (1 signal), +10 (2 signals), +20 (3+ signals)

### Grade Thresholds (No change)

| Grade | Score | Action |
|-------|-------|--------|
| A | 90+ | prioritize |
| B | 70-89 | standard |
| C | 50-69 | explore |
| D/F | <50 | exclude |

## Example: autolaveuse.fr Re-scored

| Component | Points | Evidence |
|-----------|--------|----------|
| Required | PASS | Rents cleaning equipment |
| Cleaning equipment | +50 | Moderate: Active rental business with pricing |
| Competitor footprint | +0 | No competitor brands |
| Channel capability | +20 | 3+ signals: Rental, Devis, Multiple categories |
| **Total** | **70** | **B grade → standard** |

**Previous (incorrect) score:** 55 (C grade, explore)
**Corrected score:** 70 (B grade, standard)

## Implementation

Update `skills/distributor-inspector/SKILL.md`:
1. Revise Cleaning Equipment Bonus table to include rental services
2. Add rental to Channel Capability signals as demo/trial equivalent
3. Add note about "active in market" criteria

## Files to Modify

- `skills/distributor-inspector/SKILL.md` - Lines 156-164 (Cleaning Equipment Bonus)
- `skills/distributor-inspector/SKILL.md` - Lines 180-196 (Channel Capability Bonus)
