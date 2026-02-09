# UNCLASSIFIED RECORDS GAP ANALYSIS
# 2023 Data - Classification Dictionary Expansion Opportunities

**Analysis Date**: February 7, 2026
**Data Source**: `panjiva_2023_with_roro_update_20260207_133309.csv`
**Total Records**: 394,600
**Unclassified Records**: 57,979 (14.7%)
**Unclassified Tonnage**: 130,552,646.83 tons

---

## EXECUTIVE SUMMARY

This analysis identifies the **top 30 HS4 codes** in unclassified 2023 records, representing significant gaps in classification dictionary coverage. The **top 10 HS4 codes alone account for 71.2M tons (54.6% of unclassified tonnage)**, making them high-priority targets for dictionary expansion.

### Major Product Categories Missing from Classification:

1. **Petroleum Products** (HS 2710, 2707) - 35.1M tons (26.9%)
2. **Steel Products** (HS 7219, 7210, 7221, 7208, 7204) - 18.8M tons (14.4%)
3. **Chemicals & Alcohols** (HS 2905, 2914, 2915, 2922, 3824) - 17.7M tons (13.6%)
4. **Coal & Coke** (HS 2701, 2713) - 5.3M tons (4.1%)
5. **Crude Oil variants** (HS 2709) - 5.1M tons (3.9%)

---

## TOP 10 PRIORITY HS4 CODES FOR DICTIONARY EXPANSION

### 1. HS 2710 - Petroleum Oils (excluding crude)
**Tonnage**: 28,564,079 tons (21.9% of unclassified)
**Records**: 4,373
**Package Types**: LBK (2,483), PCS (958), BLK (606)

**Product Categories Identified**:
- **Ultra-low sulfur diesel (ULSD)** - "ULTRA" (625), "SULFUR" (549), "LOW" (717)
- **Diesel fuel / Gas oil** - "OIL" (873)
- **Petroleum product shipments** - "BBLS" (2,188), "CARGO" (792)
- **Vehicle/trailer shipments** (mixed cargo) - "TRLRS" (1,974), "SEMI" (1,028), "CAR" (564)

**Recommended Dictionary Rules**:
```
Phase 4 | HS4=2710 | Keywords: ULTRA LOW SULFUR | Exclude: CRUDE
→ Liquid Bulk → Petroleum → Diesel Fuel → Ultra-Low Sulfur Diesel (ULSD)

Phase 4 | HS4=2710 | Keywords: DIESEL | Exclude: CRUDE
→ Liquid Bulk → Petroleum → Diesel Fuel → Diesel Fuel

Phase 4 | HS4=2710 | Keywords: GAS OIL | Exclude: CRUDE
→ Liquid Bulk → Petroleum → Diesel Fuel → Gas Oil

Phase 4 | HS4=2710 | Pckg=LBK | Exclude: CRUDE
→ Liquid Bulk → Petroleum → Petroleum Products → Refined Products (TBN)
```

**Accuracy Estimate**: 90-95%
**Tonnage Impact**: Very High (28.6M tons)

---

### 2. HS 7219 - Hot-rolled stainless steel
**Tonnage**: 7,034,210 tons (5.4% of unclassified)
**Records**: 647
**Package Types**: COL (323), PCS (253)

**Product Categories Identified**:
- **Hot-rolled steel coils** - "HOT" (505), "ROLLED" (432), "COIL" (417), "COILS" (238)
- **Stainless steel** - "STEEL" (234), "ALLOY" (165)
- **Prime quality** - "PRIME" (290), "QUALITY" (282)

**Recommended Dictionary Rules**:
```
Phase 4 | HS4=7219 | Keywords: HOT ROLLED | Pckg=COL
→ Dry Bulk → Steel → Steel Coils → Hot-Rolled Stainless Steel Coils

Phase 4 | HS4=7219 | Keywords: STAINLESS STEEL
→ Dry Bulk → Steel → Steel Products → Stainless Steel (TBN)

Phase 4 | HS4=7219 | Pckg=COL
→ Dry Bulk → Steel → Steel Coils → Steel Coils (TBN)
```

**Accuracy Estimate**: 95%
**Tonnage Impact**: Very High (7.0M tons)

---

### 3. HS 2707 - Oils from coal tar distillation (Naphtha)
**Tonnage**: 6,516,368 tons (5.0% of unclassified)
**Records**: 626
**Package Types**: LBK (536), BLK (78)

**Product Categories Identified**:
- **Naphtha** - "NAPHTHA" (457), "NAPTHA" (32)
- **Heavy virgin naphtha** - "HVN" (68), "VIRGIN" (50)
- **Reformate** - "REFORMATE" (47)

**Recommended Dictionary Rules**:
```
Phase 4 | HS4=2707 | Keywords: NAPHTHA | Pckg=LBK
→ Liquid Bulk → Petroleum → Naphtha → Naphtha

Phase 4 | HS4=2707 | Keywords: HVN | VIRGIN | NAPHTHA
→ Liquid Bulk → Petroleum → Naphtha → Heavy Virgin Naphtha (HVN)

Phase 4 | HS4=2707 | Keywords: REFORMATE
→ Liquid Bulk → Petroleum → Naphtha → Reformate

Phase 4 | HS4=2707 | Pckg=LBK
→ Liquid Bulk → Petroleum → Petroleum Products → Coal Tar Distillates (TBN)
```

**Accuracy Estimate**: 92-97%
**Tonnage Impact**: Very High (6.5M tons)

---

### 4. HS 2905 - Acyclic alcohols (Glycerine, MEG, DEG)
**Tonnage**: 5,534,181 tons (4.2% of unclassified)
**Records**: 348
**Package Types**: LBK (280), BLK (44), TNK (17)

**Product Categories Identified**:
- **Glycerine** - "GLYCERINE" (110), "REFINED" (54)
- **Monoethylene Glycol (MEG)** / **Diethylene Glycol (DEG)** - "DEG" (115)
- **Butyl alcohol** - "BUTYL" (53)
- **Methyl alcohol** - "METHYL" (37), "CARBINOL" (39)

**Recommended Dictionary Rules**:
```
Phase 4 | HS4=2905 | Keywords: GLYCERINE | Pckg=LBK
→ Liquid Bulk → Chemicals → Alcohols → Glycerine

Phase 4 | HS4=2905 | Keywords: DIETHYLENE GLYCOL | DEG
→ Liquid Bulk → Chemicals → Alcohols → Diethylene Glycol (DEG)

Phase 4 | HS4=2905 | Keywords: MONOETHYLENE GLYCOL | MEG
→ Liquid Bulk → Chemicals → Alcohols → Monoethylene Glycol (MEG)

Phase 4 | HS4=2905 | Keywords: BUTYL ALCOHOL
→ Liquid Bulk → Chemicals → Alcohols → Butyl Alcohol

Phase 4 | HS4=2905 | Pckg=LBK
→ Liquid Bulk → Chemicals → Alcohols → Acyclic Alcohols (TBN)
```

**Accuracy Estimate**: 88-92%
**Tonnage Impact**: Very High (5.5M tons)

---

### 5. HS 2709 - Crude Oil (unclassified variants)
**Tonnage**: 5,083,590 tons (3.9% of unclassified)
**Records**: 339
**Package Types**: LBK (215), BLK (124)

**Product Categories Identified**:
- **Crude oil (generic)** - "CRUDE" (148), "OIL" (100), "API" (85)
- **Low sulfur vacuum gas oil** - "LSVGO" (46)
- **Foreign crude (retained onboard)** - "FOREIGN" (46), "RETAINED" (46), "ONBOARD" (133)

**Recommended Dictionary Rules**:
```
Phase 4 | HS4=2709 | HS6=270900 | Keywords: LSVGO | VACUUM GAS OIL
→ Liquid Bulk → Petroleum → Gas Oil → Low Sulfur Vacuum Gas Oil (LSVGO)

Phase 4 | HS4=2709 | HS6=270900 | Keywords: CRUDE OIL | Pckg=LBK
→ Liquid Bulk → Petroleum → Crude Oil → Crude Oil (generic)

Phase 4 | HS4=2709 | HS6=270900 | Pckg=LBK
→ Liquid Bulk → Petroleum → Crude Oil → Crude Oil (TBN)
```

**Note**: Many existing crude oil rules may need **Lock_Cargo_Detail=FALSE** to allow these to refine further.

**Accuracy Estimate**: 90%
**Tonnage Impact**: Very High (5.1M tons)

---

### 6. HS 7210 - Flat-rolled steel, clad/plated/coated
**Tonnage**: 4,763,239 tons (3.6% of unclassified)
**Records**: 2,479
**Package Types**: COL (2,086), PCS (348)

**Product Categories Identified**:
- **Hot-dip galvanized coils** - "HOT" (1,705), "DIP" (1,472), "ZINC" (827)
- **Pre-painted steel coils** - "PREPAINTED" (918), "COATED" (886)
- **Aluminum-zinc coated** - "ALUMINUM" (396), "ZINC" (827)

**Recommended Dictionary Rules**:
```
Phase 4 | HS4=7210 | Keywords: HOT DIP | GALVANIZED | ZINC | Pckg=COL
→ Dry Bulk → Steel → Steel Coils → Hot-Dip Galvanized Steel Coils

Phase 4 | HS4=7210 | Keywords: PREPAINTED | COATED | Pckg=COL
→ Dry Bulk → Steel → Steel Coils → Pre-Painted Steel Coils

Phase 4 | HS4=7210 | Keywords: ALUMINUM ZINC | ALUZINC | Pckg=COL
→ Dry Bulk → Steel → Steel Coils → Aluminum-Zinc Coated Steel Coils

Phase 4 | HS4=7210 | Pckg=COL
→ Dry Bulk → Steel → Steel Coils → Coated Steel Coils (TBN)
```

**Accuracy Estimate**: 93-96%
**Tonnage Impact**: Very High (4.8M tons)

---

### 7. HS 2701 - Coal (Steam coal, Anthracite)
**Tonnage**: 4,397,365 tons (3.4% of unclassified)
**Records**: 98
**Package Types**: BLK (88), BAG (6)

**Product Categories Identified**:
- **Steam coal** - "STEAM" (79), "COAL" (90)
- **Colombian coal** - "COLUMBIAN" (60), "COLOMBIAN" (19)
- **Anthracite coal** - "ANTHRACITE" (15)
- **Calcined/recarburizer coal** - "RECARBURIZER" (4), "CALCINED" (4)

**Recommended Dictionary Rules**:
```
Phase 4 | HS4=2701 | Keywords: STEAM COAL | Pckg=BLK
→ Dry Bulk → Coal & Coke → Coal → Steam Coal

Phase 4 | HS4=2701 | Keywords: ANTHRACITE | Pckg=BLK
→ Dry Bulk → Coal & Coke → Coal → Anthracite Coal

Phase 4 | HS4=2701 | Keywords: RECARBURIZER | CALCINED | Pckg=BLK|BAG
→ Dry Bulk → Coal & Coke → Coal → Calcined Coal / Recarburizer

Phase 4 | HS4=2701 | Pckg=BLK
→ Dry Bulk → Coal & Coke → Coal → Coal (TBN)
```

**Accuracy Estimate**: 95%
**Tonnage Impact**: Very High (4.4M tons)

---

### 8. HS 2915 - Saturated acyclic monocarboxylic acids
**Tonnage**: 3,460,275 tons (2.7% of unclassified)
**Records**: 233
**Package Types**: LBK (181), BLK (25)

**Product Categories Identified**:
- **Acetic acid** - "ACID" (117), "ACETIC" (41)
- **Ethyl acetate** - "ETHYL" (35), "ACETATE" (40)

**Recommended Dictionary Rules**:
```
Phase 4 | HS4=2915 | Keywords: ACETIC ACID | Pckg=LBK
→ Liquid Bulk → Chemicals → Acids → Acetic Acid

Phase 4 | HS4=2915 | Keywords: ETHYL ACETATE
→ Liquid Bulk → Chemicals → Esters → Ethyl Acetate

Phase 4 | HS4=2915 | Pckg=LBK
→ Liquid Bulk → Chemicals → Acids → Acyclic Acids (TBN)
```

**Accuracy Estimate**: 88%
**Tonnage Impact**: High (3.5M tons)

---

### 9. HS 7221 - Hot-rolled bars/rods of stainless steel
**Tonnage**: 3,070,596 tons (2.4% of unclassified)
**Records**: 289
**Package Types**: PCS (233), BDL (48)

**Product Categories Identified**:
- **Steel wire rod** - "WIRE" (271), "ROD" (270), "STEEL" (270)

**Recommended Dictionary Rules**:
```
Phase 4 | HS4=7221 | Keywords: WIRE ROD | STEEL | Pckg=PCS|BDL
→ Dry Bulk → Steel → Steel Products → Steel Wire Rod

Phase 4 | HS4=7221 | Keywords: HOT ROLLED | BARS | RODS
→ Dry Bulk → Steel → Steel Products → Hot-Rolled Steel Bars/Rods

Phase 4 | HS4=7221 | Pckg=PCS|BDL
→ Dry Bulk → Steel → Steel Products → Steel Bars/Rods (TBN)
```

**Accuracy Estimate**: 94%
**Tonnage Impact**: High (3.1M tons)

---

### 10. HS 2914 - Ketones (MEK, MIBK, Acetone)
**Tonnage**: 2,798,585 tons (2.1% of unclassified)
**Records**: 176
**Package Types**: LBK (155), BLK (10)

**Product Categories Identified**:
- **Methyl ethyl ketone (MEK)** - "MEK" (40), "KETONE" (142), "METHYL" (128), "ETHYL" (80)
- **Methyl isobutyl ketone (MIBK)** - "MIBK" (50), "ISOBUTYL" (46)
- **Acetone** - "ACETONE" (34)

**Recommended Dictionary Rules**:
```
Phase 4 | HS4=2914 | Keywords: METHYL ETHYL KETONE | MEK | Pckg=LBK
→ Liquid Bulk → Chemicals → Ketones → Methyl Ethyl Ketone (MEK)

Phase 4 | HS4=2914 | Keywords: METHYL ISOBUTYL KETONE | MIBK | Pckg=LBK
→ Liquid Bulk → Chemicals → Ketones → Methyl Isobutyl Ketone (MIBK)

Phase 4 | HS4=2914 | Keywords: ACETONE | Pckg=LBK
→ Liquid Bulk → Chemicals → Ketones → Acetone

Phase 4 | HS4=2914 | Pckg=LBK
→ Liquid Bulk → Chemicals → Ketones → Ketones (TBN)
```

**Accuracy Estimate**: 90%
**Tonnage Impact**: High (2.8M tons)

---

## ADDITIONAL HIGH-VALUE HS4 CODES (11-20)

### 11. HS 7204 - Ferrous waste & scrap
**Tonnage**: 2,347,931 tons (1.8%)
**Records**: 312
**Products**: Steel scrap, busheling scrap, metal scrap

```
Phase 4 | HS4=7204 | Keywords: SCRAP | STEEL | BUSHELING | Pckg=BLK
→ Dry Bulk → Steel → Scrap Metal → Steel Scrap
```

---

### 12. HS 2619 - Slag (blast furnace slag, GGBFS)
**Tonnage**: 1,698,968 tons (1.3%)
**Records**: 63
**Products**: Granulated blast furnace slag, ground granulated slag

```
Phase 4 | HS4=2619 | Keywords: GRANULATED BLAST FURNACE SLAG | GGBFS | Pckg=BLK
→ Dry Bulk → Industrial Minerals → Slag → Granulated Blast Furnace Slag (GGBFS)

Phase 4 | HS4=2619 | Keywords: SLAG | Pckg=BLK
→ Dry Bulk → Industrial Minerals → Slag → Slag (TBN)
```

---

### 13. HS 7208 - Hot-rolled flat steel
**Tonnage**: 1,532,481 tons (1.2%)
**Records**: 48
**Products**: Hot-rolled coils, pickled & oiled steel

```
Phase 4 | HS4=7208 | Keywords: HOT ROLLED | PICKLED | OILED | Pckg=COL
→ Dry Bulk → Steel → Steel Coils → Hot-Rolled Pickled & Oiled Steel Coils

Phase 4 | HS4=7208 | Keywords: HOT ROLLED | COIL | Pckg=COL
→ Dry Bulk → Steel → Steel Coils → Hot-Rolled Steel Coils
```

---

### 14. HS 8428 - Lifting/handling machinery
**Tonnage**: 1,387,498 tons (1.1%)
**Records**: 327
**Products**: Handling equipment, cranes, conveyors, aggregates (mixed cargo)

```
Phase 4 | HS4=8428 | Keywords: CONVEYOR | HANDLING | MACHINE | Exclude: AGGREGATES | Pckg=PKG|CAS
→ Dry Bulk → General Cargo → Project Cargo → Handling Machinery

Phase 4 | HS4=8428 | Keywords: CRANE | SENNEBOGEN
→ Dry Bulk → General Cargo → Project Cargo → Cranes & Lifting Equipment
```

**Note**: Many records show "AGGREGATES" mixed with machinery parts (possible ship spares).

---

### 15. HS 3105 - Mineral/chemical fertilizers (nitrogen)
**Tonnage**: 1,370,950 tons (1.1%)
**Records**: 156
**Products**: Calcium nitrate solution, liquid fertilizers (CN9)

```
Phase 4 | HS4=3105 | Keywords: CALCIUM NITRATE | NOXIOUS | CN9 | Pckg=LBK
→ Liquid Bulk → Fertilizer → Liquid Fertilizers → Calcium Nitrate Solution

Phase 4 | HS4=3105 | Keywords: AMMONIUM NITRATE | Pckg=LBK|BLK
→ Liquid Bulk → Fertilizer → Liquid Fertilizers → Ammonium Nitrate Solution

Phase 4 | HS4=3105 | Pckg=LBK
→ Liquid Bulk → Fertilizer → Liquid Fertilizers → Liquid Fertilizers (TBN)
```

---

### 16. HS 1201 - Soybeans
**Tonnage**: 1,282,397 tons (1.0%)
**Records**: 197
**Products**: Organic soybeans, bulk soybeans

```
Phase 4 | HS4=1201 | Keywords: SOYBEANS | ORGANIC | Pckg=BLK
→ Dry Bulk → Agricultural Products → Grains & Seeds → Organic Soybeans

Phase 4 | HS4=1201 | Keywords: SOYBEANS | Pckg=BLK
→ Dry Bulk → Agricultural Products → Grains & Seeds → Soybeans
```

---

### 17. HS 8479 - Machines with individual functions
**Tonnage**: 1,208,678 tons (0.9%)
**Records**: 488
**Products**: Mixed cargo (machinery, furnace equipment, slag handling)

```
Phase 4 | HS4=8479 | Keywords: FURNACE | SLAG | BULK | Exclude: BOX | Pckg=BLK
→ Dry Bulk → Industrial Minerals → Slag → Blast Furnace Equipment (mixed)

Phase 4 | HS4=8479 | Keywords: MACHINE | Pckg=PKG|CAS|PCS
→ Dry Bulk → General Cargo → Project Cargo → Industrial Machinery
```

**Note**: High variability - many ship spares or container misclassifications.

---

### 18. HS 2922 - Oxygen-function amino compounds
**Tonnage**: 1,124,080 tons (0.9%)
**Records**: 97
**Products**: Diethanolamine (DEA), lysine

```
Phase 4 | HS4=2922 | Keywords: DIETHANOLAMINE | DEA | Pckg=LBK
→ Liquid Bulk → Chemicals → Amines → Diethanolamine (DEA)

Phase 4 | HS4=2922 | Keywords: LYSINE | Pckg=BAG|PKG
→ Dry Bulk → Chemicals → Amino Acids → Lysine
```

---

### 19. HS 6806 - Slag wool, rock wool, mineral wool
**Tonnage**: 1,062,422 tons (0.8%)
**Records**: 51
**Products**: Rock wool, slag wool, expanded perlite

```
Phase 4 | HS4=6806 | Keywords: ROCK WOOL | SLAG WOOL | Pckg=BAG|PKG
→ Dry Bulk → Industrial Minerals → Insulation Materials → Mineral Wool

Phase 4 | HS4=6806 | Keywords: PERLITE | EXPANDED | Pckg=BAG
→ Dry Bulk → Industrial Minerals → Perlite → Expanded Perlite
```

---

### 20. HS 8474 - Machinery for sorting/screening/crushing
**Tonnage**: 1,053,910 tons (0.8%)
**Records**: 268
**Products**: Crushers, screens, mobile plants, aggregates (mixed)

```
Phase 4 | HS4=8474 | Keywords: CRUSHER | SCREEN | MOBILE PLANT | Pckg=PKG|UNT
→ Dry Bulk → General Cargo → Project Cargo → Crushing & Screening Equipment

Phase 4 | HS4=8474 | Keywords: MILL | GRINDING | Pckg=PKG
→ Dry Bulk → General Cargo → Project Cargo → Grinding Mills
```

---

## REMAINING HIGH-IMPACT HS4 CODES (21-30)

### 21. HS 3824 - Chemical products & preparations
**Tonnage**: 1,004,726 tons (0.8%)
**Products**: Linear esters, additives, carbon black

### 22. HS 4411 - Fibreboard (hardboard)
**Tonnage**: 985,290 tons (0.8%)
**Products**: Hardboard sheets

### 23. HS 2713 - Petroleum coke (petcoke)
**Tonnage**: 925,272 tons (0.7%)
**Products**: Calcined petcoke, green petcoke, graphitized petcoke

### 24. HS 1701 - Cane/beet sugar
**Tonnage**: 903,331 tons (0.7%)
**Products**: Raw cane sugar, Colombian sugar, Brazilian sugar

### 25. HS 4703 - Chemical wood pulp
**Tonnage**: 890,372 tons (0.7%)
**Products**: ECF pulp bales

### 26. HS 3102 - Mineral/chemical fertilizers (nitrogen)
**Tonnage**: 840,618 tons (0.6%)
**Products**: Urea, ammonium nitrate, sodium nitrate

### 27. HS 2303 - Residues from starch/brewing/distilling
**Tonnage**: 834,278 tons (0.6%)
**Products**: Corn DDGS, distillers grains, animal feed

### 28. HS 7202 - Ferro-alloys
**Tonnage**: 834,082 tons (0.6%)
**Products**: Ferro-silicon, ferro-nickel, ferro-chrome

### 29. HS 6802 - Worked monumental/building stone
**Tonnage**: 801,988 tons (0.6%)
**Products**: Stone products, granite, marble

### 30. HS 2908 - Halogenated derivatives (molasses)
**Tonnage**: 750,069 tons (0.6%)
**Products**: Molasses

---

## IMPLEMENTATION PRIORITY MATRIX

### TIER 1 - IMMEDIATE PRIORITY (Top 5 HS4 codes)
**Target Coverage**: 52.8M tons (40.4% of unclassified)

| HS4 | Product Type | Tonnage | Complexity | Est. Rules |
|-----|--------------|---------|------------|------------|
| 2710 | Petroleum Products | 28.6M | Medium | 4-6 |
| 7219 | Stainless Steel Coils | 7.0M | Low | 3-4 |
| 2707 | Naphtha | 6.5M | Low | 4-5 |
| 2905 | Alcohols (Glycerine, MEG) | 5.5M | Medium | 5-6 |
| 2709 | Crude Oil variants | 5.1M | Low | 3-4 |

**Estimated Time**: 2-3 hours
**Expected Classification Gain**: +40% unclassified tonnage

---

### TIER 2 - HIGH PRIORITY (HS4 codes 6-10)
**Target Coverage**: 18.4M tons (14.1% of unclassified)

| HS4 | Product Type | Tonnage | Complexity | Est. Rules |
|-----|--------------|---------|------------|------------|
| 7210 | Coated Steel Coils | 4.8M | Medium | 4-5 |
| 2701 | Coal (Steam, Anthracite) | 4.4M | Low | 3-4 |
| 2915 | Acetic Acid, Acetates | 3.5M | Medium | 3-4 |
| 7221 | Steel Wire Rod | 3.1M | Low | 3 |
| 2914 | Ketones (MEK, MIBK) | 2.8M | Medium | 4-5 |

**Estimated Time**: 2 hours
**Expected Classification Gain**: +14% unclassified tonnage

---

### TIER 3 - MEDIUM PRIORITY (HS4 codes 11-20)
**Target Coverage**: 13.9M tons (10.6% of unclassified)

**Estimated Time**: 3-4 hours
**Expected Classification Gain**: +11% unclassified tonnage

---

### TIER 4 - LOWER PRIORITY (HS4 codes 21-30)
**Target Coverage**: 8.5M tons (6.5% of unclassified)

**Estimated Time**: 2-3 hours
**Expected Classification Gain**: +7% unclassified tonnage

---

## CUMULATIVE IMPACT PROJECTION

| Phase | HS4 Codes | Tonnage Classified | Coverage Gain | Remaining Unclassified |
|-------|-----------|-------------------|---------------|------------------------|
| Baseline | - | - | - | 130.6M (100%) |
| Tier 1 | 1-5 | 52.8M | +40.4% | 77.8M (59.6%) |
| Tier 2 | 6-10 | 18.4M | +14.1% | 59.4M (45.5%) |
| Tier 3 | 11-20 | 13.9M | +10.6% | 45.5M (34.9%) |
| Tier 4 | 21-30 | 8.5M | +6.5% | 37.0M (28.4%) |
| **TOTAL** | **1-30** | **93.6M** | **71.6%** | **37.0M (28.4%)** |

**Estimated Total Time**: 9-12 hours of dictionary expansion work
**Expected Result**: Reduce unclassified tonnage from 130.6M to 37.0M tons
**Classification Coverage Improvement**: From 85.3% to 96.3% (overall dataset)

---

## TECHNICAL NOTES

### Mixed Cargo Challenges

Several HS4 codes show **mixed cargo patterns** that complicate classification:

1. **HS 8428 / 8479** - Mix of machinery and bulk aggregates (possible ship spares or container misclassifications)
2. **HS 2710** - Mix of petroleum products and vehicle shipments (trailers, semi-trucks)
3. **HS 8474** - Mix of crushing equipment and bulk aggregates

**Recommendation**: Use **Exclude_Keywords** to filter out anomalous records, or accept lower accuracy estimates.

---

### Lock Level Strategy

For all new rules:

- **Lock_Group**: TRUE (set Group level)
- **Lock_Commodity**: TRUE (set Commodity level)
- **Lock_Cargo**: FALSE (allow Phase 10 refinements)
- **Lock_Cargo_Detail**: FALSE (allow future grade-specific rules)

This allows **hierarchical refinement** without requiring rule rewrites.

---

### Package Type Patterns

| Package Code | Typical Cargo Type | HS4 Examples |
|--------------|-------------------|--------------|
| **LBK** | Liquid Bulk | 2710, 2707, 2905, 2914, 2915, 3824 |
| **BLK** | Dry Bulk | 2701, 7204, 2619, 1201, 3102 |
| **COL** | Steel Coils | 7219, 7210, 7208 |
| **PCS/BDL** | Steel Products | 7221, 7210 |
| **BAG** | Bagged Solids | 2713, 1701, 6806, 3102 |
| **PKG/CAS** | General Cargo | 8428, 8474, 8479 |

---

## NEXT STEPS

### Phase 1: Immediate Action (Tier 1)
1. Expand petroleum product rules (HS 2710, 2707)
2. Add steel coil rules (HS 7219, 7210)
3. Create alcohol/glycerine rules (HS 2905)
4. Test on 2023 data

**Goal**: Achieve 60% reduction in unclassified tonnage

---

### Phase 2: Consolidation (Tier 2)
1. Add remaining steel rules (HS 7221, 7208)
2. Expand chemical rules (HS 2914, 2915)
3. Add coal rules (HS 2701)
4. Test across 2023-2025 data

**Goal**: Achieve 75% reduction in unclassified tonnage

---

### Phase 3: Long-tail coverage (Tiers 3-4)
1. Add specialty products (slag, fertilizers, sugar)
2. Handle edge cases (mixed cargo)
3. Final validation

**Goal**: Achieve 90%+ classification coverage

---

## FILES GENERATED

1. **Text Report**: `unclassified_2023_analysis_20260207.txt` (detailed keyword analysis)
2. **CSV Summary**: `unclassified_2023_by_hs4_20260207.csv` (top 30 HS4 codes)
3. **This Document**: `UNCLASSIFIED_GAP_ANALYSIS_20260207.md` (strategic recommendations)

---

**Analysis Complete**: February 7, 2026
**Next Review**: After Tier 1 dictionary expansion
