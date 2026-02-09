# HS Code Harmonization Coverage Analysis v1.1.0

**Analysis Date**: 2026-02-06
**Data Source**: panjiva_imports_2024_HARMONIZED_v1.1.0.csv
**Records Analyzed**: 449,233
**Total Tonnage**: 723.7 Million MT

---

## Executive Summary

### Overall Harmonization Performance

| Metric | Coverage |
|--------|----------|
| **Record Coverage** | 5.0% (22,446 / 449,233 records) |
| **Tonnage Coverage** | 54.0% (390.8M / 723.7M MT) |
| **Shipper Coverage** | 3.5% (15,742 records) |
| **Consignee Coverage** | 4.4% (19,791 records) |
| **Both Parties** | 2.9% (13,087 records) |

**Key Finding**: Despite low record coverage (5%), the harmonization dictionary captures **54% of total tonnage**, indicating successful targeting of high-volume commodity flows.

---

## Critical Commodity Assessment

### ✅ Meeting Targets

| HS2 | Commodity | Tonnage (MT) | Coverage | Status |
|-----|-----------|--------------|----------|--------|
| **27** | Crude Oil & Petroleum | 377.5M | 71.6% | **[OK]** Good coverage |
| **2709** | Crude Oil (specific) | 228.7M | 76.0% | **[!]** Below 80% target |

### ⚠️ Below Targets - Priority for v1.2.0

| HS2 | Commodity | Tonnage (MT) | Coverage | Gap (MT) |
|-----|-----------|--------------|----------|----------|
| **72** | Iron & Steel | 52.0M | 26.7% | 38.1M |
| **73** | Steel Articles | 12.0M | 32.9% | 8.0M |
| **Combined Steel** | HS 72-73 | 64.0M | **7.8%** | 56.1M |

**Critical Gap**: Steel harmonization is at 7.8% (record basis), far below the 60% target. Combined tonnage gap: **56.1 million MT**.

---

## Top 15 Highest Tonnage HS2 Chapters

| Rank | HS2 | Description | Tonnage (MT) | Coverage % | Gap (MT) | Priority |
|------|-----|-------------|--------------|------------|----------|----------|
| 1 | 27 | Crude Oil/Petroleum | 377.5M | 71.6% | 107.4M | Medium |
| 2 | **72** | Iron/Steel | 52.0M | **26.7%** | **38.1M** | **HIGH** |
| 3 | 68 | Stone/Plaster | 44.2M | 50.8% | 21.7M | HIGH |
| 4 | **25** | Salt/Cement | 38.9M | **46.9%** | **20.7M** | **HIGH** |
| 5 | 87 | Vehicles | 23.1M | 1.9% | 22.6M | HIGH |
| 6 | 44 | Wood | 17.2M | 62.5% | 6.4M | Medium |
| 7 | **29** | Organic Chemicals | 16.6M | **32.5%** | **11.2M** | **HIGH** |
| 8 | **31** | Fertilizers | 15.7M | **16.1%** | **13.1M** | **HIGH** |
| 9 | **26** | Ores, Slag, Ash | 15.3M | **38.8%** | **9.3M** | **HIGH** |
| 10 | 76 | Aluminum | 13.8M | 66.8% | 4.6M | Medium |
| 11 | 84 | Machinery | 13.1M | 26.7% | 9.6M | HIGH |
| 12 | **73** | Steel Articles | 12.0M | **32.9%** | **8.0M** | **HIGH** |
| 13 | 38 | Misc Chemicals | 11.6M | 64.7% | 4.1M | Medium |
| 14 | 28 | Inorganic Chemicals | 7.8M | 13.3% | 6.8M | HIGH |
| 15 | 15 | Animal/Veg Fats | 7.8M | 8.9% | 7.1M | HIGH |

---

## Gaps to Fill

### HS2 Chapters with ZERO Harmonization (44 chapters)

**Top 10 by tonnage:**

| HS2 | Description | Tonnage (MT) | Records |
|-----|-------------|--------------|---------|
| **10** | Cereals (Grain) | 1.56M | 359 |
| 30 | Pharmaceuticals | 0.68M | 242 |
| 99 | Special Provisions | 0.40M | 60 |
| 32 | Tanning/Dyeing | 0.32M | 588 |
| 34 | Soaps/Waxes | 0.23M | 545 |
| 53 | Veg Textile Fibers | 0.19M | 36 |
| 18 | Cocoa | 0.13M | 359 |
| 96 | Misc Manufactures | 0.11M | 95 |
| 2 | Meat | 0.11M | 218 |
| 41 | Hides/Skins | 0.10M | 27 |

**Recommendation**: Add basic grain shippers (HS 10) to dictionary - 1.56M MT with zero coverage is a significant gap.

### HS2 Chapters with <20% Coverage and >10K Tons (45 chapters)

**Top 10 by tonnage:**

| HS2 | Description | Tonnage (MT) | Coverage % |
|-----|-------------|--------------|------------|
| 87 | Vehicles | 23.1M | 1.9% |
| 31 | Fertilizers | 15.7M | 16.1% |
| 28 | Inorganic Chem | 7.8M | 13.3% |
| 15 | Animal/Veg Fats | 7.8M | 8.9% |
| 23 | Animal Feed Residues | 6.9M | 17.3% |
| 17 | Sugars | 5.2M | 1.5% |
| 22 | Beverages | 2.3M | 4.7% |
| 20 | Veg/Fruit Preps | 1.6M | 2.5% |
| 10 | Cereals | 1.6M | 0.0% |
| 8 | Fruits | 1.5M | 0.0% |

---

## Entity Specialization Insights

### Top 10 Entity-HS2 Combinations by Tonnage

| Entity | HS2 | Commodity | Tonnage (MT) |
|--------|-----|-----------|--------------|
| CHEVRON-001 | 27 | Crude Oil/Petroleum | 86.3M |
| VALERO-001 | 27 | Crude Oil/Petroleum | 53.8M |
| PMI-001 | 27 | Crude Oil/Petroleum | 47.8M |
| IRVING-001 | 27 | Crude Oil/Petroleum | 37.3M |
| PBF-001 | 27 | Crude Oil/Petroleum | 26.5M |
| ECOPETROL-001 | 27 | Crude Oil/Petroleum | 22.1M |
| EXXONMOBIL-001 | 27 | Crude Oil/Petroleum | 18.6M |
| MARATHON-001 | 27 | Crude Oil/Petroleum | 18.5M |
| SOMO-001 | 27 | Crude Oil/Petroleum | 15.7M |
| BOLANTER-001 | 27 | Crude Oil/Petroleum | 15.0M |

**Key Insight**: Top 10 entity-commodity combinations are ALL petroleum-related, demonstrating the dictionary's strong focus on energy commodities.

### Most Diversified Entities (Multiple HS2 Chapters)

| Entity | HS2 Count | Notes |
|--------|-----------|-------|
| EMIRATES-001 | 35 | Operates across most commodity categories |
| CHEVRON-001 | 22 | Petroleum-focused but diversified |
| ARCELORMITTAL-001 | 19 | Steel + diversified industrial |
| VALE-001 | 16 | Mining conglomerate |
| CEMEX-001 | 15 | Cement + construction materials |
| EXXONMOBIL-001 | 14 | Energy + petrochemicals |
| MORTON-001 | 12 | Salt + industrial chemicals |

**Specialized Entities** (appearing in <=2 HS2 codes): 26 entities

---

## Recommendations for v1.2.0 Dictionary Expansion

### Tier 1 Priority (High Tonnage + Low Coverage)

1. **Steel Sector (HS 72-73)** - 56.1M MT gap (7.8% coverage)
   - Add major steel producers: ArcelorMittal, Nucor, US Steel, Ternium
   - Add steel importers: automotive OEMs, construction companies
   - Target gap: Increase to 60% coverage

2. **Cement & Building Materials (HS 25)** - 20.7M MT gap (46.9% coverage)
   - Add cement importers beyond current coverage
   - Focus on high-volume ports (Gulf Coast, Great Lakes)

3. **Fertilizers (HS 31)** - 13.1M MT gap (16.1% coverage)
   - Add agricultural commodity traders (Cargill, ADM, Bunge)
   - Add fertilizer producers/importers (Mosaic, CF Industries, Yara)

4. **Organic Chemicals (HS 29)** - 11.2M MT gap (32.5% coverage)
   - Add petrochemical companies beyond current coverage
   - Focus on Gulf Coast chemical corridor

5. **Ores & Minerals (HS 26)** - 9.3M MT gap (38.8% coverage)
   - Add mining companies and metal traders
   - Target iron ore, bauxite, copper concentrate flows

### Tier 2 Priority (Medium Tonnage Gaps)

6. **Machinery (HS 84)** - 9.6M MT gap
7. **Inorganic Chemicals (HS 28)** - 6.8M MT gap
8. **Animal/Veg Fats (HS 15)** - 7.1M MT gap
9. **Wood Products (HS 44)** - 6.4M MT gap (already at 62.5%, optimize further)

### Tier 3 Priority (Fill Zero-Coverage Gaps)

10. **Grain (HS 10)** - 1.6M MT, 0% coverage
    - Add major grain traders: Cargill, ADM, Bunge, Louis Dreyfus
    - Should be easy wins with existing agricultural entities

### Quick Wins (High ROI)

Based on the analysis, focus v1.2.0 efforts on:

1. **Steel entities** - Massive tonnage gap (56M MT) with concentrated shipper base
2. **Agricultural traders** - Already have some entities; expand to grain/fertilizers
3. **Chemical companies** - Expand beyond petroleum to cover organic/inorganic chemicals
4. **Mining companies** - Add major miners for ores/minerals coverage

---

## Coverage Distribution Summary

| Coverage Level | HS2 Chapters | % of Total |
|----------------|--------------|------------|
| **High (>=70%)** | 5 | 5.2% |
| **Medium (40-70%)** | 9 | 9.3% |
| **Low (<40%)** | 83 | 85.6% |

**Total HS2 chapters**: 97

---

## HS 27 (Petroleum) Deep Dive

### HS4 Breakdown for Crude Oil & Petroleum

| HS4 | Description | Tonnage (MT) | Coverage % |
|-----|-------------|--------------|------------|
| **2709** | Crude Oil | 228.7M | 76.0% |
| 2710 | Refined Petroleum | 140.8M | 34.3% |
| 2707 | Oils from Coal | 4.2M | 29.5% |
| 2711 | Petroleum Gas (LPG) | 1.4M | 4.7% |
| 2713 | Petroleum Coke | 0.8M | 23.0% |
| 2715 | Bituminous Mixtures | 0.7M | 76.5% |

**Finding**: Crude oil (HS 2709) has 76.0% coverage, slightly below the 80% target. Refined petroleum (HS 2710) has only 34.3% coverage despite being the second-largest petroleum product by tonnage.

**Recommendation**: Add petroleum product traders and distributors to improve HS 2710 coverage.

---

## Next Steps

### For v1.2.0 Dictionary Development

1. **Extract unmatched shippers/consignees** from priority HS codes:
   - HS 72-73 (Steel)
   - HS 31 (Fertilizers)
   - HS 25 (Cement)
   - HS 29 (Organic Chemicals)
   - HS 26 (Ores)

2. **Analyze top unmatched parties** by tonnage in each category

3. **Research corporate structures** for identified high-volume shippers

4. **Add harmonization rules** targeting 100K+ MT unmatched entities

5. **Validate** against known commodity flows and industry knowledge

### Analysis Scripts to Run

1. `extract_unmatched_parties_by_hs.py` - Get top unmatched shippers/consignees for each priority HS2
2. `analyze_steel_importers_v1.0.0.py` - Deep dive into HS 72-73 unmatched parties
3. `analyze_fertilizer_flows_v1.0.0.py` - Map fertilizer importers and distributors
4. `analyze_cement_importers_v1.0.0.py` - Identify cement and building material entities

---

## Files Generated

1. **Analysis Script**: `02_SCRIPTS/02.04_analysis/analyze_hs_coverage_by_harmonization_v1.0.0.py`
2. **CSV Output**: `03_DOCUMENTATION/03.04_summaries/hs_code_harmonization_coverage_v1.1.0.csv`
3. **This Summary**: `03_DOCUMENTATION/03.04_summaries/HS_CODE_HARMONIZATION_ANALYSIS_v1.1.0.md`

---

**Analysis Complete**: 2026-02-06 01:03:29
**Script Version**: v1.0.0
**Dictionary Version**: v1.1.0
