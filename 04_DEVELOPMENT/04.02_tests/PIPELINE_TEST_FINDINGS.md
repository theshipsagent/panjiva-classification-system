# Pipeline Test Findings - 15K Sample Test
**Date:** 2026-01-16
**Test Size:** 15,000 records per source
**Status:** TESTING COMPLETE

---

## Summary

Ran complete pipeline test on 15K randomized samples to validate new folder structure after reorganization. Found both successes and critical issues.

---

## ✅ SUCCESSES

### 1. Folder Structure Works
- All paths updated correctly
- Scripts can find data in new locations:
  - `00_DATA/00.02_PREPROCESSED/` ✓
  - `01_DICTIONARIES/01.03_vessels/` ✓
  - `04_DEVELOPMENT/04.02_tests/` ✓

### 2. Data Loading Success
- Panjiva imports: 15,000 records (51 columns) ✓
- Panjiva exports: 15,000 records (80 columns) ✓
- USACE entrance: 15,000 records (44 columns) ✓
- USACE clearance: 15,000 records (40 columns) ✓
- Ship registry: 52,034 vessels ✓

### 3. Matching Potential Confirmed
- IMO overlap (Panjiva-USACE): 1,080 vessels (18.9% of USACE IMOs)
- Vessel name overlap: 1,766 vessels
- **Ship registry match rate: 91.9%** (5,258 of 5,720 USACE IMOs)

---

## 🔴 ISSUES FOUND

### Issue #1: Column Name Inconsistency
**Problem:** Script referenced `'Vessel Name'` but Panjiva imports uses `'Vessel'`

**Location:** `run_test_pipeline.py` line 134, 172

**Impact:** Script crashed when trying to access non-existent column

**Fix Applied:** Changed all references from `'Vessel Name'` to `'Vessel'`

**Status:** ✅ FIXED

---

### Issue #2: Unicode Encoding Error
**Problem:** Python console can't display emoji characters (✅ ❌) in print statements

**Error:**
```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705'
```

**Location:** Multiple log() calls throughout test scripts

**Impact:** Script crashed when trying to print status messages

**Fix Applied:** Replaced all emoji with text:
- `✅` → `[OK]`
- `❌` → `[ERROR]`

**Status:** ✅ FIXED

---

### Issue #3: IMO Data Type Mismatch (FALSE ALARM)
**Problem:** Initial test showed 0% ship registry match rate

**Root Cause:** Improper data type conversion in comparison:
- USACE IMO: `float64` (9837444.0)
- Ship registry IMO: `int64` (1004156)
- String comparison failed without proper float→int→string conversion

**Actual Match Rate:** 91.9% (5,258 of 5,720)

**Fix Required:** Ensure all IMO comparisons use proper conversion:
```python
# WRONG (shows 0% match):
usace_imos = set(df['IMO'].astype(str))

# RIGHT (shows 91.9% match):
usace_imos = set(df['IMO'].dropna().astype(int).astype(str))
```

**Status:** ⚠️ DOCUMENTED - Scripts need review for proper IMO handling

---

### Issue #4: IMO Number Range Differences
**Observation:**
- USACE IMOs start with 8-9 (modern vessels)
- Ship registry has many IMOs starting with 1 (older vessels)

**Distribution:**
- USACE: Mostly 9xxxxxx (90%+) - modern commercial vessels
- Ship registry: Mixed 1xxxxxx through 9xxxxxx

**Impact:** None - this is expected (registry includes older vessels)

**Status:** ℹ️ INFORMATIONAL ONLY

---

## 📊 Test Statistics

### Data Completeness

| Dataset | Total | IMO Present | IMO % | Vessel Name % |
|---------|-------|-------------|-------|---------------|
| USACE Entrance | 15,000 | 14,156 | 94.4% | 100% |
| USACE Clearance | 15,000 | 14,272 | 95.1% | 100% |
| Panjiva Imports | 15,000 | 10,333 | 68.9% | 100% |
| Panjiva Exports | 15,000 | ? | ? | 100% |

### Matching Feasibility

| Match Type | Overlap | Total | Rate |
|------------|---------|-------|------|
| Panjiva→USACE (IMO) | 1,080 | 5,720 | 18.9% |
| Panjiva→USACE (Name) | 1,766 | 5,836 | 30.3% |
| USACE→Registry (IMO) | 5,258 | 5,720 | 91.9% |

---

## 🔧 Fixes Applied

1. ✅ **Column name correction** - Updated `'Vessel Name'` → `'Vessel'`
2. ✅ **Unicode fix** - Removed emoji characters from all output
3. ⚠️ **IMO conversion** - Documented proper conversion pattern

---

## ⏭️ Next Steps

### Immediate
1. ✅ Document findings in this file
2. ⚠️ Review all matching scripts for IMO conversion patterns
3. ⚠️ Test actual matching algorithms with 15K samples
4. ⚠️ Test port call master generation

### Follow-up
- Run marry_entrance_clearance.py on test samples
- Test US Flag registry matching
- Test FGIS grain export matching
- Generate test port call master file
- Compare results with full pipeline

---

## 📁 Test Files Generated

```
04_DEVELOPMENT/04.02_tests/
├── test_samples_15k/
│   ├── panjiva_imports_2023_sample_15k.csv (11.8 MB)
│   ├── panjiva_exports_2023_sample_15k.csv (11.2 MB)
│   ├── usace_entrance_2023_sample_15k.csv (4.9 MB)
│   └── usace_clearance_2023_sample_15k.csv (4.9 MB)
│
├── test_output/
│   └── pipeline_test_log_20260116_1621.txt
│
├── create_test_samples.py
├── run_test_pipeline.py
├── diagnose_imo_mismatch.py
└── PIPELINE_TEST_FINDINGS.md (this file)
```

---

## 🎯 Overall Assessment

**Reorganization Status:** ✅ SUCCESS
- New folder structure working correctly
- Path updates applied successfully
- Scripts can locate all required files

**Pipeline Status:** ⚠️ NEEDS REVIEW
- Core data loading works
- Matching potential confirmed
- IMO handling needs standardization across scripts

**Recommended Action:**
1. Audit all matching scripts for IMO conversion patterns
2. Create helper function for IMO normalization
3. Continue testing with actual matching algorithms

---

**Test Duration:** ~7 minutes
**Test Execution:** 2026-01-16 16:15 - 16:22
**Findings:** 4 issues (2 fixed, 1 documented, 1 informational)
