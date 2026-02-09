# Preprocessing Consolidation Plan
**Date:** 2026-01-28
**Goal:** Move ALL column transformations to preprocessing, leave classification to ONLY fill Group/Commodity/Cargo/Cargo Detail

---

## Problem Statement

**Currently:** Column transformations are scattered across multiple stages
- Stage 01: Preprocessing (drops, renames, adds some columns)
- Stage 02: Vessel enrichment (adds Type, DWT, Vessel_Type_Simple)
- Stage 03: Classification (adds lock columns, tracking columns)

**This causes:**
- Hard to track column evolution
- Hard to audit what happened when
- Classification script doing more than classification
- Confusing when debugging

---

## Solution: Consolidate Everything into Preprocessing

### New Structure

**Stage 01: Preprocessing (ALL TRANSFORMATIONS)**
1. Drop junk columns (84 columns)
2. Rename columns (9 columns)
3. Split Quantity → Qty + Pckg
4. Extract HS2, HS4, HS6 from HS Code
5. Add port rollups (Port_Consolidated, Port_Coast, Port_Region, Port_Code)
6. Add vessel enrichment (Type, DWT, Vessel_Type_Simple from ship registry)
7. Add classification columns (Group, Commodity, Cargo, Cargo Detail) - EMPTY
8. Add lock columns (Group_Locked, Commodity_Locked, Cargo_Locked, Cargo_Detail_Locked) - FALSE
9. Add tracking columns (Classified_Phase, Last_Rule_ID, Report_One/Two/Three/Four, Filter, Note) - EMPTY
10. Add metadata (RAW_REC_ID, Count, Carrier Name)

**Output:** Complete schema with all columns, ready for classification

**Stage 02: Classification (FILL ONLY)**
- Input: Preprocessed data with empty classification columns
- Process: Match rules, fill Group/Commodity/Cargo/Cargo Detail, update locks
- Output: Same schema, classification columns now populated

**Stage 03: USACE Matching (FUTURE)**
- Match classified Panjiva to USACE port call master
- Roll up, aggregate, join

---

## Current State vs. Target State

### Current State (Scattered)

| Stage | Columns In | Operations | Columns Out |
|-------|------------|------------|-------------|
| **Raw** | 135 | - | 135 |
| **Stage 01: Preprocess** | 135 | Drop 84, Rename 9, Split 1→2, Extract HS codes, Add 12 tracking | 51 |
| **Stage 02: Vessel Enrich** | 51 | Add Type, DWT, Vessel_Type_Simple from registry | 54 |
| **Stage 03: Classify** | 54 | Add 6 lock/tracking columns, fill Group/Commodity/Cargo/Cargo Detail | 60 |
| **Final** | 60 | - | 60 |

**Problem:** Vessel enrichment and lock initialization happen OUTSIDE preprocessing

---

### Target State (Consolidated)

| Stage | Columns In | Operations | Columns Out |
|-------|------------|------------|-------------|
| **Raw** | 135 | - | 135 |
| **Stage 01: Preprocess (ALL)** | 135 | Drop, Rename, Split, Extract, Add ALL columns (vessel, classification, locks, tracking) | 60 |
| **Stage 02: Classify (FILL ONLY)** | 60 | Fill Group/Commodity/Cargo/Cargo Detail, update locks/tracking | 60 |
| **Stage 03: USACE Match** | 60 | Match to USACE, roll up | TBD |

**Benefit:** Clear separation - preprocessing creates schema, classification fills values

---

## Columns to MOVE into Preprocessing

### Currently Added in Classification Script (MOVE to Preprocessing)

| Column | Current Stage | Target Stage | Initialize As | Notes |
|--------|--------------|--------------|---------------|-------|
| Type | Vessel Enrich (Stage 02) | Preprocessing (Stage 01) | From ship registry | Vessel type (detailed) |
| DWT | Vessel Enrich (Stage 02) | Preprocessing (Stage 01) | From ship registry | Deadweight tonnage |
| Vessel_Type_Simple | Vessel Enrich (Stage 02) | Preprocessing (Stage 01) | Map from Type | Simplified category |
| Group | Classification (Stage 03) | Preprocessing (Stage 01) | Empty string '' | Classification Level 1 |
| Commodity | Classification (Stage 03) | Preprocessing (Stage 01) | Empty string '' | Classification Level 2 |
| Cargo | Classification (Stage 03) | Preprocessing (Stage 01) | Empty string '' | Classification Level 3 |
| Cargo Detail | Classification (Stage 03) | Preprocessing (Stage 01) | Empty string '' | Classification Level 4 |
| Group_Locked | Classification (Stage 03) | Preprocessing (Stage 01) | 'FALSE' | Lock flag |
| Commodity_Locked | Classification (Stage 03) | Preprocessing (Stage 01) | 'FALSE' | Lock flag |
| Cargo_Locked | Classification (Stage 03) | Preprocessing (Stage 01) | 'FALSE' | Lock flag |
| Cargo_Detail_Locked | Classification (Stage 03) | Preprocessing (Stage 01) | 'FALSE' | Lock flag |
| Classified_Phase | Classification (Stage 03) | Preprocessing (Stage 01) | Empty string '' | Tracking field |
| Last_Rule_ID | Classification (Stage 03) | Preprocessing (Stage 01) | Empty string '' | Tracking field |

**Total:** 13 columns to move

---

## Final Schema (After Preprocessing) - 60 columns

### Core Shipment Data (31 columns)
1. Bill of Lading Number
2. Arrival Date
3. Consignee
4. Consignee (Original Format)
5. Consignee SIC Codes
6. Shipper
7. Shipper (Original Format)
8. Shipper SIC Codes
9. Notify Party
10. Carrier
11. Carrier Name (extracted)
12. Origin (F)
13. Destination (D)
14. Port of Discharge (D)
15. Port of Loading (F)
16. Country of Origin (F)
17. Place of Receipt (F)
18. Port_Consolidated
19. Port_Coast
20. Port_Region
21. Port_Code
22. Vessel
23. Voyage
24. IMO
25. Is Containerized
26. Measurement
27. Kilos
28. Tons
29. Weight (Original Format)
30. Value
31. HS Code Desc.

### Product Data (7 columns)
32. Goods Shipped
33. Qty
34. Pckg
35. HS2
36. HS4
37. HS6
38. RAW_REC_ID

### Aggregation (1 column)
39. Count

### Classification Columns (4 columns - EMPTY after preprocessing)
40. Group
41. Commodity
42. Cargo
43. Cargo Detail

### Lock Flags (4 columns - FALSE after preprocessing)
44. Group_Locked
45. Commodity_Locked
46. Cargo_Locked
47. Cargo_Detail_Locked

### Tracking (2 columns - EMPTY after preprocessing)
48. Classified_Phase
49. Last_Rule_ID

### Reporting (4 columns - EMPTY after preprocessing)
50. Report_One
51. Report_Two
52. Report_Three
53. Report_Four

### User Fields (2 columns - EMPTY after preprocessing)
54. Filter
55. Note

### Vessel Enrichment (3 columns - FROM REGISTRY)
56. Type (vessel type detailed)
57. DWT (deadweight tonnage)
58. Vessel_Type_Simple (mapped from Type)

### Totals (2 columns - RESERVED)
59. [RESERVED for future use]
60. [RESERVED for future use]

---

## Implementation Steps

### Step 1: Update Preprocessing Script

**File:** Create new `stage01_preprocess_imports_CONSOLIDATED_v2.0.0.py`

**Add these operations:**
```python
# SECTION 1: Existing operations (keep)
- Drop 84 columns
- Rename 9 columns
- Split Quantity → Qty + Pckg
- Extract HS2, HS4, HS6
- Add RAW_REC_ID, Count
- Add port rollups

# SECTION 2: NEW - Add vessel enrichment
- Load ship registry (01_ships_register.csv)
- Match on Vessel name
- Add Type, DWT from registry
- Map Type → Vessel_Type_Simple

# SECTION 3: NEW - Initialize classification columns
df['Group'] = ''
df['Commodity'] = ''
df['Cargo'] = ''
df['Cargo Detail'] = ''

# SECTION 4: NEW - Initialize lock flags
df['Group_Locked'] = 'FALSE'
df['Commodity_Locked'] = 'FALSE'
df['Cargo_Locked'] = 'FALSE'
df['Cargo_Detail_Locked'] = 'FALSE'

# SECTION 5: NEW - Initialize tracking columns
df['Classified_Phase'] = ''
df['Last_Rule_ID'] = ''

# SECTION 6: Existing - Add reporting columns
df['Report_One'] = ''
df['Report_Two'] = ''
df['Report_Three'] = ''
df['Report_Four'] = ''
df['Filter'] = ''
df['Note'] = ''
```

**Output:** 60-column CSV ready for classification

---

### Step 2: Simplify Classification Script

**File:** Update `classify_15k_sample.py` and `run_full_pipeline.py`

**Remove these operations:**
- ~~add_vessel_types()~~ (already in preprocessing)
- ~~Initialize classification columns~~ (already in preprocessing)
- ~~Initialize lock columns~~ (already in preprocessing)
- ~~Initialize tracking columns~~ (already in preprocessing)

**Keep only:**
- load_dictionary()
- classify_in_phases() (match rules, fill values)
- save_results()

**Result:** Classification script becomes pure classification logic

---

### Step 3: Update AUTHORITATIVE Files

**Current:** `panjiva_imports_2023/2024/2025_AUTHORITATIVE_v1.0.0.csv` (51 columns)

**Action:** Re-run consolidated preprocessing on raw files

**New:** `panjiva_imports_2023/2024/2025_AUTHORITATIVE_v2.0.0.csv` (60 columns)

**Changes:**
- +3 columns: Type, DWT, Vessel_Type_Simple
- +4 columns: Group, Commodity, Cargo, Cargo Detail (empty)
- +4 columns: Group_Locked, Commodity_Locked, Cargo_Locked, Cargo_Detail_Locked (FALSE)
- +2 columns: Classified_Phase, Last_Rule_ID (empty)

---

### Step 4: Update Column Mapping Documentation

**Files to update:**
- `COLUMN_EVOLUTION_TRACKER.csv` (already created ✅)
- `PREPROCESSING_COLUMN_MAP.md` (update with new operations)
- `CLAUDE.md` (update preprocessing section)

---

## Benefits of Consolidation

### 1. Clear Separation of Concerns
- **Preprocessing:** ALL schema transformations, vessel enrichment, initialization
- **Classification:** ONLY fill Group/Commodity/Cargo/Cargo Detail using rules
- **Matching:** ONLY join Panjiva to USACE

### 2. Easier Debugging
- Column missing? Check preprocessing
- Wrong classification? Check classification rules
- Match failed? Check matching logic

### 3. Auditable
- Single CSV tracker shows evolution at each stage
- Can trace any column back to source
- Can see what transformation created it

### 4. Reusable
- Preprocessing output is classification-agnostic
- Can run different classification strategies on same preprocessed data
- Can test new dictionaries without reprocessing

### 5. Performant
- Vessel enrichment done once during preprocessing
- Classification doesn't waste time on lookups
- Can parallelize classification runs

---

## Testing Plan

### Test 1: Preprocessing v2.0.0
```bash
# Run consolidated preprocessing on 2024 data
python stage01_preprocess_imports_CONSOLIDATED_v2.0.0.py 2024

# Verify output has 60 columns
# Verify Type/DWT/Vessel_Type_Simple populated
# Verify classification columns are empty
# Verify lock columns are FALSE
```

### Test 2: Classification on v2.0.0 Input
```bash
# Run classification on new preprocessed file
python classify_15k_sample_v2.0.0.py

# Verify classification columns filled
# Verify locks updated
# Verify tracking columns populated
# Verify same results as before
```

### Test 3: Full Pipeline
```bash
# Run end-to-end on 5K sample
python stage01_preprocess → 5k_preprocessed_v2.0.0.csv
python classify_5k → 5k_classified_v2.0.0.csv

# Compare to old pipeline results
# Should match exactly
```

---

## Migration Checklist

- [ ] Create `stage01_preprocess_imports_CONSOLIDATED_v2.0.0.py`
- [ ] Test preprocessing on 5K sample
- [ ] Verify 60-column output schema
- [ ] Update classification scripts to use v2.0.0 input
- [ ] Test classification on 5K sample
- [ ] Compare old vs. new results (should match)
- [ ] Re-run preprocessing on all 3 years (2023, 2024, 2025)
- [ ] Create new AUTHORITATIVE v2.0.0 files
- [ ] Update documentation (CLAUDE.md, PREPROCESSING_COLUMN_MAP.md)
- [ ] Archive old v1.0.0 files
- [ ] Update paths in all classification scripts

---

## Timeline Estimate

| Task | Time | Status |
|------|------|--------|
| Create consolidated preprocessing script | 1-2 hours | 🔴 Not started |
| Test on 5K sample | 10 minutes | 🔴 Not started |
| Update classification scripts | 30 minutes | 🔴 Not started |
| Test classification on 5K | 10 minutes | 🔴 Not started |
| Re-run preprocessing (2023, 2024, 2025) | 30 minutes | 🔴 Not started |
| Update documentation | 30 minutes | 🔴 Not started |
| **TOTAL** | **3-4 hours** | 🔴 Ready to start |

---

## Questions & Decisions

### Q1: Should we keep v1.0.0 files?
**A:** Yes, archive them for rollback. Keep in `_archive/preprocessing_v1.0.0/`

### Q2: What if classification results differ?
**A:** They shouldn't. If they do, it's a bug in consolidation. Must match exactly.

### Q3: What about USACE data?
**A:** Separate pipeline. Will address later after Panjiva is fixed.

### Q4: Update dictionary version?
**A:** No. Dictionary v3.6.0 stays the same. Only preprocessing changes.

### Q5: What about exports?
**A:** Same consolidation approach. Do imports first, then replicate for exports.

---

**Status:** 🟡 Plan complete, ready for implementation
**Next Step:** Create consolidated preprocessing script v2.0.0
**Priority:** HIGH (blocks all classification work)
