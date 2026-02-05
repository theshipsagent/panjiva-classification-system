# Dictionary v3.6.0 Analysis
**Date:** 2026-01-28
**Dictionary File:** `00_REFERENCE/dictionary_v3.6.0.csv`

---

## 📊 Overview Statistics

| Metric | Value |
|--------|-------|
| **Total Rules** | 668 |
| **Active Rules** | 668 (100%) |
| **Columns** | 43 |
| **Phases Used** | 5 (1, 2, 3, 5, 6) |
| **Groups** | 3 (Dry Bulk, Liquid Bulk, Liquid Gas) |
| **Commodities** | 20+ |

---

## 📋 Dictionary Schema (43 Columns)

### Control Columns (10)
```
1. Rule_ID                  Unique identifier (e.g., HS4-1001, CARRIER-ACLU)
2. Phase                    Execution phase (1, 2, 3, 5, 6)
3. Tier                     Priority tier (1 = highest)
4. Active                   TRUE/FALSE (all TRUE in v3.6.0)
5. Lock_Classification      (legacy, not used)
6. Override_HS              (legacy, not used)
7. Priority                 Numeric priority (1 = highest)
8. Public                   Visibility flag
9. Private                  Visibility flag
10. Source                  Rule origin/author
```

### Matching Criteria (14)
```
11. Carrier_SCAC            Shipping line code (e.g., ACLU, AETK)
12. Carrier_Name            Carrier name
13. Package_Type            Package code (e.g., LBK, BLK)
14. Vessel_Type             Vessel category (not used in v3.6.0)
15. Exclude_Groups          Groups to exclude from match
16. HS2                     2-digit HS code
17. HS4                     4-digit HS code
18. HS6                     6-digit HS code
19. Keywords                Legacy keyword list (semicolon separated)
20. Key_Phrases             Multi-word phrases (comma separated)
21. Primary_Keywords        Main product terms (comma separated)
22. Descriptor_Keywords     Modifiers (comma separated)
23. Match_Strategy          PHRASE_REQUIRED or PRIMARY_SUFFICIENT
24. Exclude_Keywords        Exclusion terms (semicolon separated)
```

### Tonnage Filters (4)
```
25. Min_Tons                Minimum tonnage threshold
26. Max_Tons                Maximum tonnage threshold
27. Port_Filter             Port filter (not widely used)
28. Country_Filter          Country filter (not widely used)
```

### Lock Levels (4)
```
29. Lock_Group              TRUE = Group cannot be changed
30. Lock_Commodity          TRUE = Group + Commodity locked
31. Lock_Cargo              TRUE = Group + Commodity + Cargo locked
32. Lock_Cargo_Detail       TRUE = All 4 levels locked (final)
```

### Classification Output (4)
```
33. Group                   Level 1 (Dry Bulk, Liquid Bulk, Liquid Gas)
34. Commodity               Level 2 (Agricultural Products, Chemicals, etc.)
35. Cargo                   Level 3 (Grain, Crude Oil, Steel, etc.)
36. Cargo_Detail            Level 4 (Wheat, Basrah Heavy, Hot Rolled Coils, etc.)
```

### Metadata (7)
```
37. Filter                  Custom filter flag
38. Note                    Rule description/source
39. Accuracy_Est            Estimated accuracy (not used in v3.6.0)
40. Tonnage_Impact          Expected tonnage impact (not used in v3.6.0)
41. Date_Added              Rule creation date
42. Last_Modified           Last update date
43. HS4_Description         Human-readable HS4 description
```

---

## 🔢 Phase Distribution

| Phase | Rules | Description | Purpose |
|-------|-------|-------------|---------|
| **1** | 65 | Carrier Locks | Lock Group based on shipping line (RoRo, Tanker, etc.) |
| **2** | 51 | HS4 Broad Strokes | HS4 codes without tonnage filters (grain, agricultural) |
| **3** | 263 | HS + Keywords | HS codes with keyword matching (most specific) |
| **5** | 1 | Default Catch-All | Classify everything remaining as "General Cargo" |
| **6** | 288 | Refinements | Refine classifications, specific products |

**Note:** Phase 4 is missing - likely reserved for future use.

---

## 🎯 Matching Criteria Usage

### Criteria Frequency
```
HS4 codes:          602 rules (90.1%)  ← Most common
HS2 codes:          602 rules (90.1%)
Primary_Keywords:   422 rules (63.2%)
Key_Phrases:        311 rules (46.6%)
Min_Tons:           307 rules (46.0%)
Max_Tons:           307 rules (46.0%)
Package_Type:       218 rules (32.6%)
Carrier_SCAC:       65 rules (9.7%)   ← Phase 1 only
HS6 codes:          44 rules (6.6%)
Keywords (legacy):  45 rules (6.7%)
Vessel_Type:        0 rules (0%)      ← Not used
```

**Insight:** Most rules rely on HS4 codes + keywords + tonnage filters. Carrier and package type are used for specific classifications.

---

## 🔒 Lock Level Strategy

### Lock Distribution
```
Lock_Group = TRUE:          667 rules (99.9%)  ← Almost always locked
Lock_Commodity = TRUE:      623 rules (93.3%)
Lock_Cargo = TRUE:          623 rules (93.3%)
Lock_Cargo_Detail = TRUE:   623 rules (93.3%)
```

**Pattern:**
- **Phase 1 (Carrier):** Lock Group only, allow refinement
- **Phase 2 (HS4 Broad):** Lock Group + Commodity
- **Phase 3+ (Specific):** Lock all 4 levels (final classification)

**Why:** Early phases set high-level classification, later phases refine details without overriding fundamentals.

---

## 📦 Group Distribution

| Group | Rules | % | Description |
|-------|-------|---|-------------|
| **Dry Bulk** | 554 | 82.9% | Grain, coal, ore, minerals, steel, chemicals (dry form) |
| **Liquid Bulk** | 111 | 16.6% | Petroleum, chemicals (liquid), vegetable oils |
| **Liquid Gas** | 3 | 0.4% | LNG, LPG |

**Insight:** Heavily skewed toward Dry Bulk (83%), reflecting import composition.

---

## 🏭 Commodity Distribution (Top 15)

| Rank | Commodity | Rules | % |
|------|-----------|-------|---|
| 1 | General Cargo | 299 | 44.8% |
| 2 | Chemicals | 74 | 11.1% |
| 3 | Agricultural Products | 37 | 5.5% |
| 4 | Forestry | 36 | 5.4% |
| 5 | Metals | 31 | 4.6% |
| 6 | Finished Steel | 29 | 4.3% |
| 7 | Minerals & Ores | 23 | 3.4% |
| 8 | Construction Materials | 22 | 3.3% |
| 9 | Ferrous Raw Materials | 21 | 3.1% |
| 10 | Ro/Ro | 17 | 2.5% |
| 11 | Non Ferrous Raw Materials | 7 | 1.0% |
| 12 | Petroleum Products | 7 | 1.0% |
| 13 | Fertilizer | 6 | 0.9% |
| 14 | Solid Fuels | 5 | 0.7% |
| 15 | Misc Bulk | 5 | 0.7% |

**Insight:** "General Cargo" is catch-all (45%), then specialized commodities.

---

## 🔍 Rule Examples by Phase

### Phase 1: Carrier Lock (65 rules)
**Purpose:** Lock Group based on shipping line

**Example 1: RoRo Carrier**
```csv
Rule_ID: CARRIER-ACLU
Phase: 1
Carrier_SCAC: ACLU
Lock_Group: TRUE
Lock_Commodity: FALSE
Lock_Cargo: FALSE
Lock_Cargo_Detail: FALSE
Group: Dry Bulk
Commodity: Ro/Ro
Cargo: Vehicles
Cargo_Detail: (empty)
Note: Auto carrier - RoRo vessels
```

**Logic:** If shipper is ACLU (Atlantic Container Line) → Classify as Ro/Ro. Later phases can refine Cargo/Cargo_Detail.

---

### Phase 2: HS4 Broad (51 rules)
**Purpose:** HS4 codes without tonnage filters (high confidence)

**Example 2: Wheat**
```csv
Rule_ID: HS4-1001
Phase: 2
HS2: 10
HS4: 1001
Key_Phrases: PULP, WHEAT
Primary_Keywords: BULK, PACKED, GRADE
Match_Strategy: PRIMARY_SUFFICIENT
Lock_Group: TRUE
Lock_Commodity: TRUE
Lock_Cargo: TRUE
Lock_Cargo_Detail: TRUE
Group: Dry Bulk
Commodity: Agricultural Products
Cargo: Grain
Cargo_Detail: Wheat
Note: AUTHORITATIVE - Phase 2 HS4 Broad (no tonnage filters)
```

**Logic:** If HS4=1001 + keywords match → Classify as Wheat. Locks all levels (final classification).

---

### Phase 3: HS + Keywords (263 rules)
**Purpose:** Specific products with HS codes + keyword matching

**Example 3: Crude Oil (specific grade)**
```csv
Rule_ID: HS6-270900-BASRAH
Phase: 3
HS2: 27
HS4: 2709
HS6: 270900
Key_Phrases: BASRAH HEAVY, BASRAH CRUDE
Primary_Keywords: CRUDE, OIL
Match_Strategy: PHRASE_REQUIRED
Min_Tons: 1000
Lock_Group: TRUE
Lock_Commodity: TRUE
Lock_Cargo: TRUE
Lock_Cargo_Detail: TRUE
Group: Liquid Bulk
Commodity: Petroleum
Cargo: Crude Oil
Cargo_Detail: Crude Oil - Basrah Heavy
Note: Specific crude oil grade from Iraq
```

**Logic:** If HS6=270900 + "BASRAH" in description + tonnage > 1000 → Classify as Basrah Heavy crude. Very specific.

---

### Phase 5: Default Catch-All (1 rule)
**Purpose:** Ensure 100% classification rate

**Example 4: General Cargo Default**
```csv
Rule_ID: DEFAULT-GENERAL
Phase: 5
(no matching criteria)
Lock_Group: TRUE
Lock_Commodity: TRUE
Lock_Cargo: TRUE
Lock_Cargo_Detail: TRUE
Group: Dry Bulk
Commodity: General Cargo
Cargo: Misc Dry Bulk
Cargo_Detail: General Cargo NOS
Note: Default classification for anything not matched
```

**Logic:** If no other rule matched → Classify as General Cargo. Guarantees 100% classification.

---

### Phase 6: Refinements (288 rules)
**Purpose:** Refine existing classifications, specific products

**Example 5: Hot Rolled Coils**
```csv
Rule_ID: HS6-720851-HRC
Phase: 6
HS2: 72
HS4: 7208
HS6: 720851
Key_Phrases: HOT ROLLED, HRC
Primary_Keywords: COIL, STEEL, SHEET
Descriptor_Keywords: PRIME, GRADE
Match_Strategy: PRIMARY_SUFFICIENT
Min_Tons: 100
Lock_Group: TRUE
Lock_Commodity: TRUE
Lock_Cargo: TRUE
Lock_Cargo_Detail: TRUE
Group: Dry Bulk
Commodity: Finished Steel
Cargo: Steel Coils
Cargo_Detail: Hot Rolled Coils
Note: Specific steel product
```

**Logic:** If HS6=720851 + "HOT ROLLED" or "HRC" + tonnage > 100 → Hot Rolled Coils.

---

## 🎲 Match Strategy Patterns

### PRIMARY_SUFFICIENT (Default)
- Match if ANY Primary_Keyword found
- OR if ANY Key_Phrase found
- Descriptor_Keywords not required

**Use case:** Broad matching (wheat, steel, chemicals)

### PHRASE_REQUIRED
- Must match at least one Key_Phrase
- Primary_Keywords ignored
- More restrictive

**Use case:** Specific grades (Basrah Heavy, Liza Crude)

---

## 🔢 Tonnage Filters

**Distribution:**
- 307 rules use Min_Tons
- 307 rules use Max_Tons
- Typical thresholds: 100, 500, 1000, 5000 tons

**Purpose:** Distinguish bulk cargo from containerized:
- Crude oil: Min 1000 tons (bulk tanker)
- Steel coils: Min 100 tons (break bulk)
- Containers: Max 50 tons (not bulk)

---

## ⚠️ Potential Issues & Considerations

### 1. **Tier Column Not Used**
- All active rules have Tier = 1 (or blank)
- Tier system not implemented in v3.6.0
- May need to add tier priority later

### 2. **Phase 4 Missing**
- Phases: 1, 2, 3, 5, 6 (no Phase 4)
- Gap intentional or oversight?
- Reserved for future use?

### 3. **Vessel_Type Not Used**
- 0 rules use Vessel_Type matching
- Column exists but empty
- May add vessel-based rules later

### 4. **High Lock Rate**
- 99.9% of rules lock Group
- 93.3% lock all 4 levels
- Little room for refinement after match
- Is this intentional?

### 5. **General Cargo Dominance**
- 45% of rules classify as "General Cargo"
- May be too vague for analysis
- Consider breaking down further

### 6. **Keyword Strategy Complexity**
- 3 keyword fields: Keywords, Key_Phrases, Primary_Keywords
- 2 match strategies: PRIMARY_SUFFICIENT, PHRASE_REQUIRED
- Complex logic - easy to misconfigure

### 7. **Package_Type Not Standardized**
- 218 rules use Package_Type
- But column not in preprocessed data schema!
- Need to add Package_Type column to preprocessing

---

## 📈 Rule Effectiveness (Estimated)

**Cannot measure without running classification, but based on structure:**

**High Confidence (Phases 1-2):**
- 116 rules (17%)
- Carrier locks + broad HS4
- Expected coverage: 50-60%

**Medium Confidence (Phase 3):**
- 263 rules (39%)
- HS codes + keywords + tonnage
- Expected coverage: 30-40%

**Catch-All (Phase 5):**
- 1 rule (0.1%)
- Ensures 100% classification
- Expected coverage: 10-20% (everything else)

**Refinements (Phase 6):**
- 288 rules (43%)
- Specific products
- Expected coverage: 5-10% (overlap with Phase 3)

---

## 🔧 Recommendations

### Before Running Classification

1. **Add Package_Type to preprocessing**
   - 218 rules depend on it
   - Currently not in preprocessed schema
   - Extract from raw data "Quantity" field?

2. **Verify Phase 4 gap**
   - Is Phase 4 intentionally skipped?
   - Or should rules be renumbered?

3. **Test lock level strategy**
   - Are locks too aggressive?
   - Should later phases be able to refine more?

4. **Review Tier implementation**
   - Tier column exists but not used
   - Add priority logic?

### After Running Classification

5. **Analyze General Cargo breakdown**
   - 45% of rules = "General Cargo"
   - Too vague?
   - Break down further?

6. **Measure rule effectiveness**
   - Which rules match most records?
   - Which match most tonnage?
   - Optimize rule order

7. **Check for rule conflicts**
   - Do multiple rules match same records?
   - Which wins?
   - Priority logic correct?

---

## 📝 Summary

**Dictionary v3.6.0 is:**
- ✅ Well-structured (43 columns, clear schema)
- ✅ Comprehensive (668 active rules)
- ✅ Multi-phase (5 phases with different purposes)
- ✅ Flexible (multiple matching criteria)
- ⚠️ Complex (3 keyword fields, 2 match strategies)
- ⚠️ Potentially over-locked (99.9% lock Group)
- ⚠️ Missing Package_Type in preprocessing
- ⚠️ Tier system not implemented

**Ready for classification?**
- ✅ Schema is valid
- ✅ Rules are active
- ✅ Phases are sequential
- ⚠️ Need to add Package_Type to preprocessing
- ⚠️ Need to verify lock level behavior

**Next steps:**
1. Add Package_Type column to preprocessing
2. Test classification on 5K sample
3. Review results
4. Adjust rules if needed

---

**Document Version:** 1.0.0
**Created:** 2026-01-28
**Dictionary Version:** v3.6.0 (668 rules)
