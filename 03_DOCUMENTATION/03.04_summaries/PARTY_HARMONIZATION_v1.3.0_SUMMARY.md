# Party Harmonization Dictionary v1.3.0 - Summary

**Date**: 2026-02-06
**Status**: Ready for Testing
**Location**: `01_DICTIONARIES/01.06_parties/party_harmonization_master_v1.3.0.csv`

---

## Executive Summary

Successfully expanded party harmonization dictionary from **120 entities** (v1.2.0) to **163 entities** (v1.3.0), adding **43 new entities** (+35.8%) targeting high-tonnage unmatched parties. The expansion focuses on closing the gap from 57.3% to 68-72% consignee coverage.

### Version Progression
- **v1.0.0**: 80 entities (initial release)
- **v1.1.0**: 100 entities (+20)
- **v1.2.0**: 120 entities (+20) → **57.3% consignee coverage**
- **v1.3.0**: 163 entities (+43) → **target: 68-72% consignee coverage**

---

## Coverage Metrics

### V1.2.0 Baseline (from 2024 data)
- **Consignee**: 57.3% coverage (308M tons matched, 409K records)
- **Shipper**: 50.2% coverage (362M tons matched, 411K records)
- **Notify**: 43.2% coverage (411M tons matched, 427K records)

### V1.3.0 Targets
- **Consignee**: 68-72% (+10-15 points)
- **Shipper**: 60-64% (+10-12 points)
- **Notify**: 52-56% (+9-13 points)

### Estimated Impact
- **Total tonnage from new entities**: 68.5M tons
- **Average per entity**: 1.6M tons
- **Top 10 entities**: 22.7M tons (33% of new coverage)

---

## Strategic Additions by Industry

### Automotive (4 entities, 6.8M tons)
- **Volkswagen Group of America** (VW-001): 1.5M tons - VW, Audi, Porsche brands
- **Subaru of America** (SUBARU-001): 2.0M tons - Japanese automaker
- **Hyundai Motor America** (HYUNDAI-MOTOR-001): 1.9M tons - distinct from Kia
- **Hyundai Mobis** (HYUNDAI-MOBIS-001): 1.2M tons - parts supplier

**Coverage**: Now includes Toyota, GM, Mazda, Mercedes, Kia, VW, Subaru, Hyundai

### Cement (8 entities, 13.7M tons)
- **Vissai Ninh Binh** (VISSAI-001): 2.6M tons - Vietnam
- **Nuh Cimento** (NUH-CIMENTO-001): 2.6M tons - Turkey
- **Zona Franca Argos** (ZONA-FRANCA-ARGOS-001): 1.2M tons - Colombia
- **Cemtech Global** (CEMTECH-001): 1.4M tons - Turkey
- **McInnis USA** (MCINNIS-001): 1.8M tons - Canada
- **Lafarge Emirates** (LAFARGE-EMIRATES-001): 1.3M tons - UAE
- **Saudi Cement** (SAUDI-CEMENT-001): 1.2M tons - Saudi Arabia
- **Akcansa Cimento** (AKCANSA-001): 1.1M tons - Turkey

**Focus**: Middle East and Asia cement imports to US

### Oil & Gas (7 entities, 10.5M tons)
- **EP Petroecuador** (EP-PETROECUADOR-001): 2.1M tons - Ecuador state oil
- **Hunt Crude Oil Supply** (HUNT-CRUDE-001): 1.9M tons - Hunt family trading
- **Cenovus Energy** (CENOVUS-001): 1.2M tons - Canada oil sands
- **Shell Brasil Petroleo** (SHELL-BRASIL-001): 1.1M tons - Shell Brazil
- **Galaxy Oil** (GALAXY-OIL-001): 1.1M tons - UAE trader
- **National Oil Corp** (NATIONAL-OIL-LIBYA-001): 1.0M tons - Libya
- **North American Fuel** (NAF-CORP-001): 937K tons - US distributor

### Chemicals (4 entities, 5.4M tons)
- **Total Specialties USA** (TOTAL-SPEC-001): 1.8M tons - TotalEnergies specialty chemicals
- **Wilmar Oleo Quimico** (WILMAR-001): 1.8M tons - oleochemicals Mexico
- **Natural Oleochemicals** (NATURAL-OLEO-001): 1.8M tons - Malaysia
- **Dow Europe** (DOW-EUROPE-001): 926K tons - Dow European operations
- **TotalEnergies Petrochemicals** (TOTALENERGIES-PETRO-001): 912K tons

### Steel (2 entities, 3.2M tons)
- **California Steel Industries** (CSI-001): 1.6M tons - Fontana CA, west coast
- **Nippon Steel Trading** (NIPPON-STEEL-TRADING-001): 1.6M tons - Japanese imports

### Trading & Logistics (3 entities, 7.2M tons)
- **Freepoint Commodities** (FREEPOINT-001): 2.7M tons - physical commodity trader
- **CSC Sugar** (CSC-SUGAR-001): 2.3M tons - sugar trader
- **Mitsui & Co USA** (MITSUI-USA-001): 2.2M tons - Japanese trading house

### Finance (3 entities, 3.6M tons)
- **IIG Capital** (IIG-CAPITAL-001): 1.3M tons - financial services
- **UBS Switzerland** (UBS-001): 1.3M tons - commodity financing
- **ING Bank** (ING-001): 978K tons - commodity financing

### Other Categories
- **Mining**: Grupo Minero Del Mar De Cortes (2.1M tons)
- **Oil Refining**: Neste (2.3M tons) - Finnish renewable diesel
- **Fertilizer**: ECO Fertilizers (1.5M tons)
- **Salt**: Morton Bahamas (1.2M tons)
- **Construction Materials**: On Site Concrete (1.7M tons), Saint Gobain (1.1M tons)
- **Utilities**: PREPA Puerto Rico (1.3M tons), Naturgy Spain (1.8M tons)
- **Aggregates**: Carver Sand & Gravel (1.6M tons)

---

## Top 10 New Entities by Tonnage

| Rank | Entity | Tonnage | Category | Industry |
|------|--------|---------|----------|----------|
| 1 | Freepoint Commodities | 2.7M | All | Trader |
| 2 | Vissai Ninh Binh | 2.6M | Shipper | Cement |
| 3 | Nuh Cimento | 2.6M | Shipper | Cement |
| 4 | CSC Sugar | 2.3M | Consignee | Trader |
| 5 | Neste | 2.3M | All | Oil Refining |
| 6 | Mitsui & Co USA | 2.2M | All | Trading Company |
| 7 | Grupo Minero Del Mar | 2.1M | Shipper | Mining |
| 8 | EP Petroecuador | 2.1M | Shipper | Oil & Gas |
| 9 | Subaru of America | 2.0M | All | Automotive |
| 10 | Hyundai Motor America | 1.9M | All | Automotive |

---

## Technical Implementation

### Match Strategy Distribution
- **Contains**: 32 entities (74.4%)
  - Used for unique company names or multi-word patterns
  - Examples: "SHELL BRASIL PETROLEO", "CARVER SAND"

- **Contains_All**: 11 entities (25.6%)
  - Used for common terms requiring all tokens present
  - Examples: "CSC SUGAR", "HYUNDAI MOBIS", "SAUDI CEMENT CO"
  - Prevents false matches on single generic words

### Safe Matching Patterns
✅ **Good Patterns**:
- "VOLKSWAGEN GROUP OF AMERICA" (specific brand + geography)
- "VISSAI NINH BINH" (unique company name)
- "CALIFORNIA STEEL INDUSTRIES" (full company name)
- "EUROCHEM NORTH AMERICA" (specific subsidiary)

⚠️ **Potential Conflicts Avoided**:
- NOT "CARVER" alone → use "CARVER SAND;CARVER MATERIALS"
- NOT "MORTON" alone → use "MORTON BAHAMAS"
- NOT "NATIONAL OIL" alone → use "NATIONAL OIL CORP"
- NOT "HYUNDAI" alone → use "HYUNDAI MOTOR AMERICA"

### Category Distribution
- **All** (applies to Shipper, Consignee, Notify): 7 entities
- **Consignee**: 18 entities
- **Shipper**: 18 entities

---

## Validation & Testing Plan

### Phase 1: Apply to 2024 Data
```bash
python harmonize_parties_v1.3.0.py --input panjiva_imports_2024_AUTHORITATIVE_v2.0.0.csv
```

**Expected Output**:
- New file: `panjiva_imports_2024_HARMONIZED_v1.3.0.csv`
- Coverage statistics by party type
- Match distribution report

### Phase 2: Validation Checks
1. **Coverage Metrics**: Confirm 68-72% consignee coverage reached
2. **False Positive Check**: Review sample of matches for accuracy
3. **Collision Detection**: Ensure no entity ID conflicts
4. **Pattern Validation**: Test for unexpected matches

### Phase 3: Gap Analysis
1. Identify remaining high-tonnage unmatched parties
2. Calculate distance to 75% target
3. Plan v1.4.0 if needed

---

## Files Created

### Dictionary
- **Main**: `01_DICTIONARIES/01.06_parties/party_harmonization_master_v1.3.0.csv`
- **Previous**: `party_harmonization_master_v1.2.0.csv` (archived)

### Documentation
- **Summary**: `03_DOCUMENTATION/03.04_summaries/v1.3.0_expansion_summary.txt`
- **Entity List**: `03_DOCUMENTATION/03.04_summaries/v1.3.0_complete_entity_list.txt`
- **This File**: `03_DOCUMENTATION/03.04_summaries/PARTY_HARMONIZATION_v1.3.0_SUMMARY.md`

### Analysis Files
- **Unmatched Consignees**: `unmatched_consignee_v1.2.0_analysis.csv`
- **Unmatched Shippers**: `unmatched_shipper_v1.2.0_analysis.csv`
- **Unmatched Notify**: `unmatched_notify_party_v1.2.0_analysis.csv`

---

## Next Session Priorities

### Immediate Actions
1. ✅ **COMPLETE**: v1.3.0 dictionary created (163 entities)
2. ⏭️ **NEXT**: Test v1.3.0 on 2024 data
3. ⏭️ **NEXT**: Validate coverage improvement
4. ⏭️ **NEXT**: Generate updated gap analysis

### If Coverage Target Not Met
- **Plan v1.4.0**: Add 30-40 more entities from remaining gaps
- **Focus Areas**:
  - More automotive (Nissan, Honda, BMW)
  - More steel (USS, Cleveland-Cliffs, Gerdau)
  - More chemicals (BASF, LyondellBasell, Eastman)
  - More grain (Viterra, Richardson, General Mills)

### Long-term Goals
- **v1.5.0**: Target 75% coverage (benchmark goal)
- **v2.0.0**: Expand to notify party coverage (currently 43%)
- **Future**: Investigate address-based matching for complex cases

---

## Success Criteria

### Minimum Viable (v1.3.0)
- ✅ 163 entities (target: 160-170)
- ⏳ 68-72% consignee coverage (pending validation)
- ⏳ 60-64% shipper coverage (pending validation)

### Target (v1.5.0)
- 200+ entities
- 75% consignee coverage
- 70% shipper coverage
- 60% notify coverage

### Stretch Goals
- 85% consignee coverage (requires aggressive expansion)
- Address-based matching for logistics companies
- Automated pattern suggestion from unmatched parties

---

## Dictionary Schema Reference

### Required Columns
1. **Entity_ID**: Unique identifier (e.g., "VW-001")
2. **Canonical_Name**: Official company name
3. **Entity_Type**: Industry classification
4. **Parent_Company**: Ultimate parent (blank if independent)
5. **Match_Keywords**: Semicolon-separated patterns
6. **Match_Strategy**: "Contains" or "Contains_All"
7. **Category**: "Shipper", "Consignee", "Notify Party", or "All"
8. **Active**: "True" or "False"
9. **Notes**: Description and context
10. **Estimated_Tons**: Approximate annual tonnage impact

---

## Contact & Support

For questions about this expansion or harmonization methodology:
- See: `01_DICTIONARIES/01.06_parties/party_harmonization_rules.md`
- Review: `03_DOCUMENTATION/03.04_summaries/` for gap analyses
- Reference: Original party naming patterns in raw Panjiva data

---

**End of Summary**
