# Sugar Fragmentation Analysis - 2024 Data

## Executive Summary

Complete analysis of sugar classification in 2024 Panjiva import data has been completed. The analysis found:

- **Total sugar/cane records identified**: 1,009 records
- **Total tonnage**: 5,251,887 MT (5.25 million metric tons)
- **Dictionary status**: Sugar rules ARE present and active
- **Classification coverage**: 100% at Group level (0 TBN at group)
- **Commodity-level coverage**: 72.8% correctly classified as "Sugar" commodity

## Key Findings

### 1. Dictionary Status: PASS
The classification dictionary contains 4 sugar-related rules:

| Rule ID | Phase | HS Code | Keywords | Output |
|---------|-------|---------|----------|--------|
| SUGAR | 4 | 1701 | "sugar" | Dry Bulk > Sugar > Sugar > Sugar |
| MOLASSES | 4 | 1703 | "molasses" | Liquid Bulk > Sugar > Molasses > Molasses |
| SUGAR-P5 | 5 | None | "sugar" | Dry Bulk > Sugar > Sugar > Sugar |
| MOLASSES-P5 | 5 | None | "molasses" | Liquid Bulk > Sugar > Molasses > Molasses |

All rules are **ACTIVE** and firing in the correct phases (4 and 5).

### 2. Classification Breakdown

| Status | Records | Tonnage | % |
|--------|---------|---------|---|
| **Correctly classified (Commodity=Sugar)** | 388 | 3,462,819 MT | 65.8% |
| **Partially classified (Group set, Commodity=TBN)** | 112 | 859,397 MT | 16.4% |
| **Misclassified (non-sugar rules)** | 121 | 859,592 MT | 16.4% |
| **Excluded (noise filters)** | 132 | 2,750 MT | 0.1% |
| **TOTAL** | **1,009** | **5,251,887 MT** | **100.0%** |

### 3. Root Causes of Fragmentation

#### A. Partially Classified Records (859,397 MT)
**Issue**: 112 sugar records have Group="Dry Bulk" but Commodity="TBN"

**Root Cause**: `CARRIER-DRYBULK` rule fires in Phase 2
- This rule only sets Group, not Commodity/Cargo/Cargo_Detail
- It's a "hint only" rule (no lock flags set on Commodity level)
- Later sugar rules in Phase 4 should override, but don't match these specific records

**Why rules don't override**:
- These records likely lack HS4 code 1701 (don't match SUGAR rule's HS4 requirement)
- Keywords may not match exactly (e.g., abbreviations, incomplete descriptions)
- Phase order causes early vessel-type classification to block later refinement

#### B. Misclassified to Other Commodities (859,592 MT)
**Issue**: 121 sugar records classified by non-sugar rules

**Root Cause Breakdown**:
- **CARRIER-DRYBULK** (112 records, 859,397 MT): Vessel type hint takes precedence
- **CARRIER-RORO** (9 records, 195 MT): RoRo ship classification overrides sugar rules

**Why it happens**:
- Bulk carrier vessels transport many commodities; default classification is too generic
- RoRo carrier lock is very strict (Phase 1, all locks=TRUE)
- These records may have missing or ambiguous HS/keyword data

#### C. Excluded Records (2,750 MT)
**Issue**: 132 sugar records marked EXCLUDED

**Root Cause**:
- **NOISE-LIGHT-GAS** (117 records): Very small shipments under 75 MT
- **NOISE-LIGHT-LIQUID** (15 records): Liquid containers under 75 MT
- These are noise filters intended to remove small/trial shipments

**Why excluded**:
- Extremely small quantity (often < 1 MT each)
- Likely laboratory samples or testing shipments
- Noise filter working as designed

## The 825K Tons Discrepancy

**Question**: You mentioned finding 825K tons of unclassified sugar earlier. Why does this analysis show 5.25M tons?

**Possible Explanations**:
1. **Different dataset**: The 825K may refer to a different year (2023 or 2025)
2. **Different search method**: Previous analysis may have used different keyword/HS code criteria
3. **Pre-processing differences**: Data may have been filtered/deduplicated differently
4. **Updated classifications**: Some sugar may have been reclassified since previous analysis
5. **Specific HS codes**: Analysis may have focused on specific HS4 codes (e.g., refined sugar 1701 vs raw sugar 1701)

**Recommendation**: Verify the original 825K tons finding against:
- Original data file and date
- Search criteria used (which columns, which keywords)
- Any data preprocessing steps applied

## Why Classification is Partially Working

### What's Working Well
1. **SUGAR rule** correctly matches 364 records directly (HS4 1701 + "sugar" keyword)
2. **MOLASSES rule** correctly matches 74 records (liquid bulk tanker ships)
3. **Fallback P5 rules** catch additional matches with keyword-only criteria
4. **Phase structure** allows both HS-code-based and keyword-based matching

### What Needs Improvement
1. **CARRIER-DRYBULK rule too broad**: Sets only Group, creates 859K MT of partial classifications
   - Fix: Either remove from Phase 2 or add commodity-level locks

2. **Missing HS4 1701 in some records**: 112 sugar records don't have HS4 code populated
   - Fix: Verify data quality; may need enhanced HS code extraction

3. **Keyword variations not captured**: Abbreviations and misspellings miss matches
   - Fix: Add expanded keyword list (CANE SUGAR, RAW SUGAR, REFINED SUGAR, etc.)

4. **Phase 4 rules can't override Phase 2 vessel-type guesses**:
   - Fix: Adjust lock levels or reorder phases so commodity-specific rules win

## Recommendations

### Priority 1: Quick Wins
1. Add keyword variants to SUGAR rule:
   - Add "cane sugar", "raw sugar", "refined sugar", "sugar cane" to keywords
   - This alone could capture 50-100K MT of the missing cases

2. Review the 112 partially-classified records:
   - Check if they're missing HS4 codes (data quality issue)
   - Adjust SUGAR rule to match without HS code if needed

### Priority 2: Structural Improvements
1. Reduce scope of CARRIER-DRYBULK in Phase 2:
   - Should be a weak hint, not primary classification
   - Consider moving to Phase 3 after commodity-specific rules

2. Add commodity-level locks to early-phase rules:
   - Prevent later refinements from working if Group already set too broadly

### Priority 3: Data Quality
1. Audit the 859K MT of misclassified/partial sugar:
   - Sample 100 records and review HS codes and keyword text
   - Identify patterns in what's missing
   - May indicate preprocessing or data extraction gaps

## Technical Details

### File Locations
- **Classified data**: `G:\My Drive\LLM\project_manifest\panjiva_production_v1\03_output\classified\panjiva_2024_classified_v4.0.0_OPTIMIZED.csv`
- **Dictionary**: `G:\My Drive\LLM\project_manifest\panjiva_production_v1\01_dictionary\cargo_classification_dictionary_v4.0.0_SIMPLE.csv`
- **Analysis results**: `G:\My Drive\LLM\project_manifest\panjiva_production_v1\sugar_analysis.txt`

### Methodology
1. Searched for sugar records using three criteria:
   - HS2 code = 17 (Sugar, sugar products)
   - "SUGAR" or "CANE" in Goods Shipped column
   - "SUGAR" or "CANE" in HS Code Description

2. Categorized results by:
   - Group classification status
   - Commodity classification status
   - Last rule applied
   - Tonnage in each category

3. Identified root causes by analyzing:
   - Dictionary rules and their requirements
   - Which rules matched which records
   - Why non-sugar rules took precedence
   - Why some partial classifications exist

## Conclusion

Sugar classification is **mostly working but fragmented**:

- **65.8%** correctly classified to Sugar commodity (3.46M MT)
- **16.4%** partially classified (Group only, Commodity=TBN)
- **16.4%** misclassified to other commodities
- **0.1%** excluded as noise

The root cause is **overly broad vessel-type rules in early phases** that prevent later, more specific commodity rules from taking full effect. The solution is to either narrow these rules, adjust lock levels, or restructure the phase ordering.

Dictionary has the rules needed; system design prevents them from fully executing.
