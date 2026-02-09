# Unclassified Records Analysis - Classification Rule Recommendations
## Analysis Date: 2026-02-07

---

## Executive Summary

**Current Status:**
- **Total Records**: 394,600
- **Unclassified Records**: 57,979 (14.7%)
- **Total Tonnage**: 728,057,360 tons
- **Unclassified Tonnage**: 130,552,647 tons (17.9%)

**Key Finding**: The top 20 HS2 codes represent **92.0% of unclassified tonnage** (120.2M tons), indicating highly concentrated opportunities for rule expansion.

---

## Priority 1: Immediate Action Required (60%+ of unclassified tonnage)

### 1. HS2 27 - Petroleum Products (45.9M tons - 35.2%)
**Status**: CRITICAL GAP - Largest unclassified category

**Current Issue**: Petroleum products beyond crude oil are not classified
- Sample descriptions show refined products: "ALKYLATE", "ULTRA LOW SULFUR HEATING OIL", "GASOLINA BOOSTER"
- Package type: Barrels (BBLS) - liquid bulk tanker cargo
- HS4 2710 - petroleum oils other than crude

**Recommended Rules**:
```csv
Phase: 7
HS2: 27
HS4: 2710
Keywords: ALKYLATE
Group: Liquid Bulk
Commodity: Petroleum
Cargo: Refined Products
Cargo_Detail: Alkylate
Tier: 3
Lock_Commodity: TRUE
```

```csv
Phase: 7
HS2: 27
HS4: 2710
Keywords: HEATING OIL, FUEL OIL
Group: Liquid Bulk
Commodity: Petroleum
Cargo: Refined Products
Cargo_Detail: Heating Oil
Tier: 3
Lock_Commodity: TRUE
```

```csv
Phase: 7
HS2: 27
HS4: 2710
Keywords: GASOLINE, GASOLINA
Group: Liquid Bulk
Commodity: Petroleum
Cargo: Refined Products
Cargo_Detail: Gasoline
Tier: 3
Lock_Commodity: TRUE
```

**Estimated Impact**: 35-40M tons would be classified

---

### 2. HS2 72 - Iron & Steel (21.4M tons - 16.4%)
**Status**: HIGH PRIORITY - Second largest gap

**Current Issue**: Steel products not being classified despite clear descriptions
- Common keywords: "COIL", "STEEL", "HOT DIP", "ALLOY", "BULK"
- Types: Steel coils, plates, billets
- HS4 7225 - Flat-rolled alloy steel

**Recommended Rules**:
```csv
Phase: 7
HS2: 72
Keywords: STEEL COIL, HOT DIP, GALVANIZED
Group: Dry Bulk
Commodity: Metals
Cargo: Steel Products
Cargo_Detail: Steel Coils
Tier: 3
Lock_Commodity: TRUE
```

```csv
Phase: 7
HS2: 72
Keywords: STEEL PLATE
Group: Dry Bulk
Commodity: Metals
Cargo: Steel Products
Cargo_Detail: Steel Plate
Tier: 3
Lock_Commodity: TRUE
```

```csv
Phase: 7
HS2: 72
Keywords: STEEL BILLET
Group: Dry Bulk
Commodity: Metals
Cargo: Steel Products
Cargo_Detail: Steel Billets
Tier: 3
Lock_Commodity: TRUE
```

**Estimated Impact**: 18-20M tons would be classified

---

### 3. HS2 29 - Organic Chemicals (15.5M tons - 11.9%)
**Status**: HIGH PRIORITY - Liquid bulk chemicals

**Current Issue**: Bulk liquid chemicals not classified
- Common keywords: "BULK", "DEG", "ALCOHOL", "METHYL", "IMO"
- Package type: LBK (liquid bulk) in many records
- Examples: Chlorobenzene, MTBE (Methyl Tertiary Butyl Ether), TEOS

**Recommended Rules**:
```csv
Phase: 7
HS2: 29
Pckg: LBK
Group: Liquid Bulk
Commodity: Chemicals
Cargo: Organic Chemicals
Cargo_Detail: Organic Chemicals - Bulk
Tier: 3
Lock_Commodity: TRUE
```

```csv
Phase: 7
HS2: 29
Keywords: ALCOHOL
Group: Liquid Bulk
Commodity: Chemicals
Cargo: Organic Chemicals
Cargo_Detail: Alcohols
Tier: 3
Lock_Commodity: TRUE
```

```csv
Phase: 7
HS2: 29
Keywords: CHLOROBENZENE
Group: Liquid Bulk
Commodity: Chemicals
Cargo: Organic Chemicals
Cargo_Detail: Chlorobenzene
Tier: 3
Lock_Commodity: TRUE
```

**Estimated Impact**: 14-15M tons would be classified

---

## Priority 2: Significant Impact (5-10M tons each)

### 4. HS2 84 - Machinery (6.2M tons - 4.8%)
**Current Issue**: Heavy machinery and equipment not classified
- Keywords: "MACHINE", "EXCAVATOR", "CATERPILLAR", "PARTS"
- Many records have proper descriptions but no Group assignment
- Should be "Project Cargo" or "Machinery"

**Recommended Rules**:
```csv
Phase: 7
HS2: 84
Keywords: EXCAVATOR, CATERPILLAR, BULLDOZER, LOADER
Group: Dry Bulk
Commodity: General Cargo
Cargo: Project Cargo
Cargo_Detail: Heavy Machinery
Tier: 3
Lock_Commodity: TRUE
```

```csv
Phase: 7
HS2: 84
HS4: 8428
Keywords: CARGO HANDLING
Group: Dry Bulk
Commodity: General Cargo
Cargo: Project Cargo
Cargo_Detail: Cargo Handling Equipment
Tier: 3
Lock_Commodity: TRUE
```

**Estimated Impact**: 5-6M tons

---

## Priority 3: Moderate Impact (2-4M tons each)

### 5. HS2 26 - Ores & Slag (3.9M tons - 3.0%)
**Recommended Rules**: Add rules for slag, chromite ore, bauxite

### 6. HS2 44 - Wood Products (2.6M tons - 2.0%)
**Recommended Rules**: Add rules for timber, plywood, wood in bulk

### 7. HS2 23 - Animal Feed (2.6M tons - 2.0%)
**Recommended Rules**: Add rules for soybean meal, sunflower meal (organic and conventional)

### 8. HS2 31 - Fertilizers (2.5M tons - 1.9%)
**Recommended Rules**: Add rules for calcium nitrate, potassium compounds, triple superphosphate

### 9. HS2 38 - Miscellaneous Chemicals (2.0M tons - 1.5%)
**Recommended Rules**: Add rules for fatty acids, stearic acid, graphite

### 10. HS2 28 - Inorganic Chemicals (2.0M tons - 1.5%)
**Recommended Rules**: Add rules for silicon carbide, sulfates (manganese, zinc, ferrous)

---

## Priority 4: Moderate Impact (1-2M tons each)

### 11. HS2 12 - Oilseeds (1.9M tons)
**Focus**: Organic flaxseed, mustard seed

### 12. HS2 68 - Stone/Cement (1.9M tons)
**Focus**: Marble, granite, rockwool insulation

### 13. HS2 73 - Steel Articles (1.9M tons)
**Focus**: Steel pipes, tubes, I-beams

### 14. HS2 39 - Plastics (1.9M tons)
**Focus**: Bulk plastic resins, 1-Hexene

### 15. HS2 25 - Minerals (1.8M tons)
**Focus**: Granite blocks, cement

### 16. HS2 15 - Vegetable Oils (1.8M tons)
**Focus**: Palm oil, sunflower oil (RBD - refined/bleached/deodorized)

### 17. HS2 40 - Rubber (1.3M tons)
**Focus**: Natural rubber, styrene-butadiene copolymer

### 18. HS2 76 - Aluminum (1.1M tons)
**Focus**: Aluminum billets, primary aluminum

### 19. HS2 47 - Pulp & Paper (1.0M tons)
**Focus**: Mixed with steel coils - data quality issue?

### 20. HS2 17 - Sugar (0.9M tons)
**Focus**: Raw cane sugar, refined sugar, molasses

---

## Implementation Strategy

### Phase 1 (Immediate - Target 60M tons coverage)
1. **HS2 27 - Petroleum Products**: Create 10-15 rules for refined products
2. **HS2 72 - Iron & Steel**: Create 5-8 rules for steel products
3. **HS2 29 - Organic Chemicals**: Create 8-10 rules for bulk chemicals

### Phase 2 (Short-term - Target additional 20M tons)
4. **HS2 84 - Machinery**: Create 5-6 rules for heavy equipment
5. **HS2 26 - Ores**: Create 3-4 rules for industrial minerals
6. **HS2 23 - Animal Feed**: Create 3-4 rules for meal products
7. **HS2 31 - Fertilizers**: Create 4-5 rules for fertilizer types

### Phase 3 (Medium-term - Target additional 20M tons)
8-20. Systematic rule creation for remaining HS2 categories

---

## Expected Results

**After Phase 1 Implementation**:
- Unclassified tonnage: 130.6M → **~70M tons** (46% reduction)
- Classification coverage: 82.1% → **~90%** (absolute)
- Unclassified record count: 57,979 → **~35,000** (40% reduction)

**After Phase 2 Implementation**:
- Unclassified tonnage: ~70M → **~50M tons** (29% additional reduction)
- Classification coverage: ~90% → **~93%** (absolute)

**After Phase 3 Implementation**:
- Unclassified tonnage: ~50M → **~30M tons** (15% additional reduction)
- Classification coverage: ~93% → **~96%** (absolute)

---

## Data Quality Notes

1. **HS2 47 (Pulp & Paper)** appears to have data quality issues - descriptions mention steel coils which should be HS2 72. Requires investigation.

2. **Package Type Indicator**: Many unclassified records already have "LBK" (Liquid Bulk) package type but no Group assignment. This suggests an issue with the package type classification rules not firing.

3. **Keywords are clear**: Most unclassified records have very clear, unambiguous descriptions. Rule creation should be straightforward.

---

## Next Steps

1. **Review existing dictionary** for Phase 2-3 package type rules - verify LBK rule is active and working
2. **Create Priority 1 rules** (HS2 27, 72, 29) - estimate 40-50 new rules
3. **Test on 15K sample** to verify tonnage impact
4. **Run full 2023 classification** with expanded dictionary
5. **Compare results** against this baseline analysis
6. **Iterate** based on remaining gaps

---

## Technical Notes

**Analysis Source**: `panjiva_2023_with_roro_update_20260207_133309.csv`
- This appears to be a work-in-progress file with RoRo updates applied
- Results should be validated against AUTHORITATIVE v2.0.0 files

**Script Used**: `analyze_unclassified_records_v1.0.0.py`
**Full Report**: `unclassified_analysis_20260207.txt`

---

*Report generated: 2026-02-07*
*Analyst: Claude Code (Sonnet 4.5)*
