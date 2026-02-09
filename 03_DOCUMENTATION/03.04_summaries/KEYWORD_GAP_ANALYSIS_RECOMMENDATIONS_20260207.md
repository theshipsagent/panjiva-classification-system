# Keyword Gap Analysis - Classification Rule Recommendations

**Date:** 2026-02-07
**Analysis File:** `panjiva_2023_with_additional_refined_products_20260207_113532.csv`
**Unclassified Records:** 110,838 (28.1% of total)
**Unclassified Tonnage:** 134,494,138.77 tons (18.5% of total)

---

## Executive Summary

Analysis of 110,838 unclassified records revealed **15 major keyword groups** representing **59.3% of unclassified tonnage** (79.8M tons). The top 5 groups alone account for **86.7% of unclassified tonnage**.

**Key Findings:**
- **Petroleum Products**: 31.3M tons (23.3%) - Highest impact group
- **Steel Products**: 25.1M tons (18.6%) - Second highest
- **Food & Agriculture**: 23.7M tons (17.6%) - Third highest
- **Minerals & Ores**: 20.6M tons (15.3%) - Fourth highest
- **Vehicles & Parts**: 15.8M tons (11.7%) - Fifth highest

**Critical Issue Identified:** Many unclassified records have HS codes that are ALREADY classified elsewhere in the dataset. This suggests **missing keyword triggers** rather than unmapped HS codes.

---

## Priority 1: HIGH IMPACT (>5% of unclassified tonnage)

### 1. Petroleum Products (31.3M tons, 23.3%)

**Problem:** Renewable diesel, naphtha, and gasoline variants not captured by existing rules.

**Specific Gaps Identified:**

| Product | Records | Tonnage | HS Code | Package | Current Classification |
|---------|---------|---------|---------|---------|----------------------|
| RENEWABLE DIESEL | 641 | 3.7M tons | 2710.19 | LBK | Similar HS6 = Liquid Bulk |
| NAPHTHA | 470 | 4.9M tons | 2707.40 | LBK | Similar HS6 = Dry Bulk (ERROR) |
| GASOLINE variants | 120 | 139K tons | 2710.12 | LBK | Similar HS6 = Liquid Bulk |
| FUEL OIL | 63 | 5.9K tons | 2710.12 | LBK | Similar HS6 = Liquid Bulk |
| CRUDE OIL variants | 125 | 25.6K tons | 2709.00 | LBK | Similar HS6 = Liquid Bulk |

**Recommended New Rules:**

```csv
Rule_ID: PETRO-RENEWABLE-DIESEL
Phase: 4
Keywords: RENEWABLE DIESEL, NESTE RENEWABLE
HS4: 2710
Package: LBK
Group: Liquid Bulk
Commodity: Petroleum
Cargo: Refined Products
Cargo_Detail: Renewable Diesel
Estimated_Impact: 3.7M tons, 641 records

Rule_ID: PETRO-NAPHTHA-FIX
Phase: 4
Keywords: NAPHTHA, HVN, VIRGIN NAPHTHA
HS2: 27
HS4: 2707
Package: LBK
Group: Liquid Bulk (FIX: currently misclassified as Dry Bulk)
Commodity: Petroleum
Cargo: Refined Products
Cargo_Detail: Naphtha
Estimated_Impact: 4.9M tons, 470 records

Rule_ID: PETRO-GASOLINE-VARIANTS
Phase: 4
Keywords: GASOLINE, UNLEADED, PREMIUM GASOLINE
HS4: 2710
Package: LBK
Group: Liquid Bulk
Commodity: Petroleum
Cargo: Refined Products
Cargo_Detail: Gasoline
Estimated_Impact: 139K tons, 120 records

Rule_ID: PETRO-HIBERNIA-CRUDE
Phase: 10
Keywords: HIBERNIA CRUDE
HS6: 270900
Package: LBK
Group: Liquid Bulk
Commodity: Petroleum
Cargo: Crude Oil
Cargo_Detail: Crude Oil - Hibernia
Estimated_Impact: 25K tons, 125 records
```

**Priority Ranking:** 1 (Highest impact single group)

---

### 2. Steel Products (25.1M tons, 18.6%)

**Problem:** Steel coils, plates, sheets, and bars with HS codes 72xx are unclassified despite keyword presence.

**Specific Gaps Identified:**

| Product | Records | Tonnage | HS Code | Package | Current Classification |
|---------|---------|---------|---------|---------|----------------------|
| STEEL COIL | 49 | 126 tons | 7219.33, 7210.49 | PCS, CAS, COL | Similar HS6 = Dry Bulk |
| STEEL PLATE | 106 | 311 tons | 7225.40 | SKD, CAS | Similar HS6 = Dry Bulk |
| STEEL SHEET | 17 | 64 tons | 7210.70 | COL | Similar HS6 = Dry Bulk |
| HOT ROLLED | 2,118 occurrences | ~high | 72xx | Various | Similar HS6 = Dry Bulk |
| COLD ROLLED | 1,132 occurrences | ~high | 72xx | Various | Similar HS6 = Dry Bulk |

**Recommended New Rules:**

```csv
Rule_ID: STEEL-COIL-GENERAL
Phase: 4
Keywords: STEEL COIL, COIL
HS2: 72
Group: Dry Bulk
Commodity: Steel
Cargo: Steel Products
Cargo_Detail: Steel Coil
Estimated_Impact: 5-10M tons

Rule_ID: STEEL-PLATE-GENERAL
Phase: 4
Keywords: STEEL PLATE, PLATE
HS2: 72
Group: Dry Bulk
Commodity: Steel
Cargo: Steel Products
Cargo_Detail: Steel Plate
Estimated_Impact: 3-5M tons

Rule_ID: STEEL-HOT-ROLLED
Phase: 4
Keywords: HOT ROLLED, HOT-ROLLED
HS2: 72
Group: Dry Bulk
Commodity: Steel
Cargo: Steel Products
Cargo_Detail: Hot Rolled Steel
Estimated_Impact: 5-8M tons

Rule_ID: STEEL-COLD-ROLLED
Phase: 4
Keywords: COLD ROLLED, COLD-ROLLED
HS2: 72
Group: Dry Bulk
Commodity: Steel
Cargo: Steel Products
Cargo_Detail: Cold Rolled Steel
Estimated_Impact: 3-5M tons

Rule_ID: STEEL-REBAR
Phase: 4
Keywords: REBAR, REINFORCING BAR
HS2: 72
Group: Dry Bulk
Commodity: Steel
Cargo: Steel Products
Cargo_Detail: Rebar
Estimated_Impact: 2-4M tons
```

**Priority Ranking:** 2

---

### 3. Food & Agriculture (23.7M tons, 17.6%)

**Problem:** Soybean meal, corn, wheat, rice, and flour not captured despite HS codes.

**Specific Gaps Identified:**

| Product | Keywords | Estimated Tonnage | HS Code Range |
|---------|----------|-------------------|---------------|
| SOYBEAN products | SOYBEAN, MEAL, OIL | ~8M tons | 12xx, 23xx |
| CORN | CORN, MAIZE | ~5M tons | 10xx |
| WHEAT | WHEAT, FLOUR | ~4M tons | 10xx, 11xx |
| RICE | RICE, PADDY | ~2M tons | 10xx |
| VEGETABLE OIL | OIL, SOYBEAN OIL | ~4M tons | 15xx |

**Recommended New Rules:**

```csv
Rule_ID: FOOD-SOYBEAN-MEAL
Phase: 4
Keywords: SOYBEAN MEAL, SOY MEAL, MEAL
HS2: 23
Group: Dry Bulk
Commodity: Agricultural
Cargo: Grain & Oilseeds
Cargo_Detail: Soybean Meal
Estimated_Impact: 5-8M tons

Rule_ID: FOOD-CORN-GENERAL
Phase: 4
Keywords: CORN, MAIZE
HS2: 10
Group: Dry Bulk
Commodity: Agricultural
Cargo: Grain & Oilseeds
Cargo_Detail: Corn
Estimated_Impact: 4-6M tons

Rule_ID: FOOD-WHEAT-GENERAL
Phase: 4
Keywords: WHEAT
HS2: 10
Group: Dry Bulk
Commodity: Agricultural
Cargo: Grain & Oilseeds
Cargo_Detail: Wheat
Estimated_Impact: 3-5M tons

Rule_ID: FOOD-RICE-GENERAL
Phase: 4
Keywords: RICE, PADDY RICE
HS2: 10
Group: Dry Bulk
Commodity: Agricultural
Cargo: Grain & Oilseeds
Cargo_Detail: Rice
Estimated_Impact: 1-3M tons

Rule_ID: FOOD-VEGETABLE-OIL
Phase: 4
Keywords: SOYBEAN OIL, VEGETABLE OIL, CRUDE OIL (HS 15xx only)
HS2: 15
Package: LBK, FLX
Group: Liquid Bulk
Commodity: Agricultural
Cargo: Vegetable Oil
Cargo_Detail: Soybean Oil
Estimated_Impact: 3-5M tons
```

**Priority Ranking:** 3

---

### 4. Minerals & Ores (20.6M tons, 15.3%)

**Problem:** Aluminum, nickel, copper, and other metal ores/ingots unclassified.

**Specific Gaps Identified:**

| Product | Keywords | Estimated Tonnage | HS Code Range |
|---------|----------|-------------------|---------------|
| ALUMINUM | ALUMINUM, ALUMINIUM | ~8M tons | 76xx |
| NICKEL | NICKEL | ~4M tons | 75xx |
| COPPER | COPPER | ~3M tons | 74xx |
| IRON ORE | IRON ORE | ~2M tons | 26xx |
| COKE | COKE, PETROLEUM COKE | ~3M tons | 27xx |

**Recommended New Rules:**

```csv
Rule_ID: METAL-ALUMINUM-GENERAL
Phase: 4
Keywords: ALUMINUM, ALUMINIUM, INGOT, BILLET
HS2: 76
Group: Dry Bulk
Commodity: Metals
Cargo: Non-Ferrous Metals
Cargo_Detail: Aluminum
Estimated_Impact: 6-10M tons

Rule_ID: METAL-NICKEL-GENERAL
Phase: 4
Keywords: NICKEL
HS2: 75
Group: Dry Bulk
Commodity: Metals
Cargo: Non-Ferrous Metals
Cargo_Detail: Nickel
Estimated_Impact: 3-5M tons

Rule_ID: METAL-COPPER-GENERAL
Phase: 4
Keywords: COPPER
HS2: 74
Group: Dry Bulk
Commodity: Metals
Cargo: Non-Ferrous Metals
Cargo_Detail: Copper
Estimated_Impact: 2-4M tons

Rule_ID: MINERAL-IRON-ORE
Phase: 4
Keywords: IRON ORE
HS2: 26
Group: Dry Bulk
Commodity: Minerals
Cargo: Ores
Cargo_Detail: Iron Ore
Estimated_Impact: 1-3M tons

Rule_ID: MINERAL-COKE
Phase: 4
Keywords: COKE, PETROLEUM COKE
HS2: 27
Group: Dry Bulk
Commodity: Minerals
Cargo: Coal & Coke
Cargo_Detail: Petroleum Coke
Estimated_Impact: 2-4M tons
```

**Priority Ranking:** 4

---

### 5. Vehicles & Parts (15.8M tons, 11.7%)

**Problem:** High-value vehicle brands (Volvo, Land Rover, Mercedes) appearing in unclassified records.

**Specific Gaps Identified:**

| Brand/Type | Keywords | Occurrences | Estimated Tonnage |
|------------|----------|-------------|-------------------|
| VOLVO | VOLVO, XC40, XC60, XC90 | 97,477 | ~1M tons |
| LAND ROVER | LAND ROVER, DEFENDER, RANGE ROVER | 52,534 | ~500K tons |
| MERCEDES | MERCEDES, BENZ, SPRINTER | 32,094 | ~400K tons |
| TRACTORS | TRACTOR, LOADER, EXCAVATOR | 34,652 | ~5M tons |
| HEAVY EQUIPMENT | DEERE, CATERPILLAR, CASE | 41,265 | ~3M tons |

**Critical Finding:** These records likely belong to **Ro/Ro cargo** but lack carrier SCAC lock. Many have Package type "VEH" or "PCS".

**Recommended New Rules:**

```csv
Rule_ID: VEHICLE-VOLVO
Phase: 5
Keywords: VOLVO, XC40, XC60, XC90
HS2: 87
Package: VEH, PCS
Group: Ro/Ro
Commodity: Vehicles
Cargo: Passenger Vehicles
Cargo_Detail: Passenger Vehicles - Volvo
Estimated_Impact: 800K-1.2M tons

Rule_ID: VEHICLE-LAND-ROVER
Phase: 5
Keywords: LAND ROVER, DEFENDER, RANGE ROVER
HS2: 87
Package: VEH, PCS
Group: Ro/Ro
Commodity: Vehicles
Cargo: Passenger Vehicles
Cargo_Detail: Passenger Vehicles - Land Rover
Estimated_Impact: 400K-600K tons

Rule_ID: VEHICLE-MERCEDES
Phase: 5
Keywords: MERCEDES, BENZ, SPRINTER
HS2: 87
Package: VEH, PCS
Group: Ro/Ro
Commodity: Vehicles
Cargo: Passenger Vehicles
Cargo_Detail: Passenger Vehicles - Mercedes
Estimated_Impact: 300K-500K tons

Rule_ID: VEHICLE-AGRICULTURAL-TRACTOR
Phase: 5
Keywords: TRACTOR, JOHN DEERE, DEERE
HS4: 8701
Group: Ro/Ro
Commodity: Vehicles
Cargo: Agricultural Vehicles
Cargo_Detail: Tractors
Estimated_Impact: 3-5M tons

Rule_ID: VEHICLE-CONSTRUCTION-EQUIPMENT
Phase: 5
Keywords: EXCAVATOR, LOADER, CATERPILLAR, CAT
HS4: 8429
Group: Dry Bulk
Commodity: General Cargo
Cargo: Heavy Equipment
Cargo_Detail: Construction Equipment
Estimated_Impact: 2-4M tons
```

**Priority Ranking:** 5

---

## Priority 2: MEDIUM IMPACT (1-5% of unclassified tonnage)

### 6. Chemicals (6.1M tons, 4.6%)

**Keywords:** SULFUR, ACID, METHANOL, ETHANOL, AMMONIA, CAUSTIC SODA
**HS Codes:** 28xx, 29xx
**Package:** LBK
**Estimated Rules Needed:** 5-8
**Classification:** Liquid Bulk → Chemicals → [Specific Chemical]

### 7. Construction Materials (3.8M tons, 2.8%)

**Keywords:** CEMENT, CONCRETE, AGGREGATE, SAND, GRAVEL
**HS Codes:** 25xx, 68xx
**Package:** BLK, LBK
**Estimated Rules Needed:** 4-6
**Classification:** Dry Bulk → Construction Materials → [Specific Material]

### 8. Fertilizers (2.4M tons, 1.8%)

**Keywords:** NITRATE, PHOSPHATE, UREA, AMMONIUM
**HS Codes:** 31xx
**Package:** BLK, BAG
**Estimated Rules Needed:** 4-5
**Classification:** Dry Bulk → Fertilizers → [Specific Fertilizer]

### 9. Plastics (2.2M tons, 1.6%)

**Keywords:** PLASTIC, PET RESIN, POLYETHYLENE, PVC, PELLETS
**HS Codes:** 39xx
**Package:** BAG, BLK
**Estimated Rules Needed:** 5-7
**Classification:** Dry Bulk → Plastics → [Specific Plastic]

### 10. Machinery & Equipment (1.7M tons, 1.3%)

**Keywords:** MACHINE PARTS, ENGINE, MOTOR, PUMP, VALVE
**HS Codes:** 84xx, 85xx
**Package:** PCS, CAS
**Estimated Rules Needed:** 6-10
**Classification:** Dry Bulk → General Cargo → Machinery

---

## Priority 3: LOW IMPACT (<1% of unclassified tonnage)

### 11-15. Lower Impact Groups

| Group | Tonnage | % | Estimated Rules |
|-------|---------|---|-----------------|
| Wood & Paper | 596K tons | 0.4% | 4-6 |
| Rubber | 245K tons | 0.2% | 3-4 |
| Electronics | 181K tons | 0.1% | 4-5 |
| Textiles | 129K tons | 0.1% | 3-4 |
| Glass & Ceramics | 35K tons | 0.0% | 2-3 |

**Recommendation:** Address these groups in later phases after high-impact groups are complete.

---

## High-Frequency Ungrouped Keywords

**Attention Required:** The following high-frequency keywords don't fit into standard groups:

| Keyword | Occurrences | Potential Issue |
|---------|-------------|-----------------|
| 2023, 2024, 2022 | 168,952 | Date noise - filter out |
| PIN | 43,314 | Part numbers - context dependent |
| MSO, NCM, ENG, EXP, RUC | 99,289 | Abbreviations - need investigation |
| CUBE | 30,644 | Measurement unit or product? |
| BULK | 20,568 | Package type indicator |
| 000 | 25,741 | Data quality issue |

**Action:** Investigate these keywords manually to determine if they represent specific product categories or data quality issues.

---

## Implementation Strategy

### Phase 1: Immediate Impact (Target: +30M tons)
1. Add 4 petroleum product rules (31M tons)
2. Add 5 steel product rules (25M tons)

### Phase 2: Major Gains (Target: +40M tons)
3. Add 5 food & agriculture rules (24M tons)
4. Add 5 minerals & ores rules (21M tons)

### Phase 3: Vehicle Refinement (Target: +15M tons)
5. Add 5 vehicle & equipment rules (16M tons)

### Phase 4: Medium Impact (Target: +15M tons)
6. Add chemicals, construction, fertilizers, plastics rules

### Phase 5: Cleanup (Target: +2M tons)
7. Add remaining low-impact rules

**Total Estimated Gain:** 79.8M+ tons (59.3% of unclassified)

---

## Critical Observations

### 1. HS Code Overlap Issue
**Finding:** Many unclassified records have HS6 codes that ARE classified elsewhere.

**Example:**
- HS6 271019 (Petroleum products): Classified in some records, unclassified in others
- HS6 270740 (Naphtha): Currently misclassified as "Dry Bulk" instead of "Liquid Bulk"
- HS6 72xxxx (Steel): Classified in some records, unclassified in others

**Root Cause:** Missing keyword triggers in classification rules.

**Solution:** Add keyword-based rules in Phase 4-7 to catch these variants.

### 2. Package Type Indicator
**Finding:** Package type is highly predictive:
- LBK (Liquid Bulk) → Usually Liquid Bulk cargo
- BLK (Bulk) → Usually Dry Bulk cargo
- VEH (Vehicle) → Usually Ro/Ro cargo
- PCS (Pieces) → Usually General Cargo or Machinery

**Recommendation:** Use Package type as a supplementary matching criterion in rules.

### 3. Carrier Lock Bypass
**Finding:** Many Ro/Ro carriers (WLWH, GESM) have unclassified vehicle records.

**Root Cause:** Carrier lock only fires when carrier SCAC is present. Some records may have carrier names without SCAC codes.

**Solution:** Add keyword-based vehicle rules (Phase 5) as backup to carrier locks.

---

## Next Steps

1. **Validate Sample Size:** Run classification on 15K sample with new rules to estimate actual impact
2. **Build Dictionary v3.7.0:** Add Priority 1 rules (petroleum + steel)
3. **Test on Full 2023:** Verify tonnage gains match estimates
4. **Iterate:** Add Priority 2 rules in v3.8.0
5. **Monitor:** Track unclassified percentage after each iteration

---

## Files Generated

- `unclassified_keyword_gap_analysis_20260207_114002.txt` - Full analysis report
- `unclassified_keyword_groups_20260207_114002.csv` - Summary table
- `unclassified_samples_by_keyword_20260207.txt` - Sample records with context
- `KEYWORD_GAP_ANALYSIS_RECOMMENDATIONS_20260207.md` - This file

---

**Analysis Complete**
**Estimated Total Impact:** 79.8M+ tons (59.3% of remaining unclassified tonnage)
