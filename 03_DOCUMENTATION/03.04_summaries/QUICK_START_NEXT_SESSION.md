# Quick Start - Next Session
**Status:** 🔴 HOLD - RULE ORDER ISSUES IDENTIFIED
**Last Updated:** 2026-01-28

---

## ⚠️ CRITICAL: Focus on Panjiva Classification ONLY

### The Actual Problem

**PRIMARY ISSUE:** Rule order/priority in classification dictionary
- Rules firing in wrong sequence
- Classifications being overridden incorrectly
- Need to review and fix rule execution order

**SECONDARY ISSUE (SEPARATE):** Roll up/grouping and matching with USACE entrance/clearance
- This is a FUTURE task
- NOT part of current scope
- Will address AFTER Panjiva classification is fixed

---

## Current Focus: Fix Panjiva Classification

### What Needs to Be Fixed

1. **Rule Order/Priority Issues**
   - Review phase execution sequence
   - Verify lock level behavior
   - Check rule priority within phases
   - Ensure high-confidence rules fire first

2. **Dictionary v3.6.0 Review**
   - 668 rules across 6 phases (1, 2, 3, 5, 6)
   - Verify Phase column ordering
   - Check Tier hierarchy (1-5)
   - Validate lock levels (Lock_Group, Lock_Commodity, Lock_Cargo, Lock_Cargo_Detail)

---

## DO NOT Run Full Classification Yet

~~python run_full_pipeline.py 2023~~ ❌ HOLD

**Why:** Rule order issues need to be resolved first, or we'll waste 25+ hours processing with wrong results.

---

## What Was Done Last Session (2026-01-20)

**Bug Fixed:** Column name mismatch
- Data had: `Cargo Detail` (space)
- Script wrote to: `Cargo_Detail` (underscore)
- **Fix:** Updated scripts to use `Cargo Detail` (space)

**Validation:**
- ✅ 5K test: 100% classified
- ✅ 15K test: 100% classified
- ✅ Column alignment verified

**BUT:** Rule order issues were NOT addressed

---

## Current State

```
Preprocessing:    ✅ DONE (2023, 2024, 2025)
Classification:   🔴 HOLD (rule order issues need investigation)
USACE Processing: ✅ DONE (separate pipeline, not relevant to current work)
Matching:         🔴 NOT STARTED (future task, AFTER classification fixed)
```

---

## Bifurcation: Two Separate Problems

### PROBLEM A: Panjiva Classification (CURRENT FOCUS)
```
Panjiva Imports → Classification Rules → Classified Imports
                   ↑
                   ISSUES HERE (rule order, priority, locks)
```
**Status:** 🔴 Needs investigation and fixes
**Blocking:** All downstream work
**Priority:** HIGH - must fix before proceeding

### PROBLEM B: Matching to USACE Data (FUTURE WORK)
```
Classified Imports + USACE Port Call Master → Matched Dataset
                                               ↑
                                               NOT STARTED YET
```
**Status:** 🔴 Not started
**Blocking:** None (separate concern)
**Priority:** LOW - address AFTER Problem A is solved

**Note:** These are INDEPENDENT problems. Don't conflate them.

---

## Next Steps: Investigate Rule Order Issues

### Step 1: Review Dictionary Structure
```bash
# Open dictionary and check:
# - Phase numbers (should be 1, 2, 3, 5, 6 in order)
# - Tier values (1-5, with 1 = highest priority)
# - Lock columns (Group, Commodity, Cargo, Cargo_Detail)
# - Rule execution order within each phase

cat "G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.01_cargo_classification\cargo_classification_dictionary_CURRENT_v3.6.0.csv" | head -n 20
```

### Step 2: Review Test Results for Anomalies
```bash
# Check 15K test results for unexpected classifications
# Look for records being classified to wrong Group/Commodity/Cargo

# Example: Check if Liquid Bulk is being overridden to Dry Bulk
cat "03_DOCUMENTATION/03.04_summaries/sample_test_15k/sample_15k_classified_v3.6.0.csv" | grep "Liquid Bulk" | head -n 10
```

### Step 3: Identify Specific Rule Conflicts
- Which rules are firing out of order?
- Which classifications are being incorrectly overridden?
- Are lock levels being respected?
- Are higher-tier rules being bypassed by lower-tier rules?

### Step 4: Document Findings
Create a report documenting:
- Specific examples of misclassification
- Which rules should have fired but didn't
- Which rules fired when they shouldn't have
- Proposed fixes to rule order/locks/priority

---

## Key Files

### Scripts (Ready to Run)
```
02_SCRIPTS/02.07_production/run_full_pipeline.py
```

### Input Data
```
00_DATA/00.02_PREPROCESSED/
  ├── panjiva_imports_2023_AUTHORITATIVE_v1.0.0.csv (352 MB)
  ├── panjiva_imports_2024_AUTHORITATIVE_v1.0.0.csv (347 MB)
  └── panjiva_imports_2025_AUTHORITATIVE_v1.0.0.csv (308 MB)
```

### Dictionary
```
01_DICTIONARIES/01.01_cargo_classification/
  └── cargo_classification_dictionary_CURRENT_v3.6.0.csv (668 rules)
```

---

## Test Results (Validation)

### 15K Sample Test
- **Records:** 15,000 / 15,000 (100%)
- **Runtime:** 18.5 minutes
- **Groups:** Dry Bulk (95.7%), Liquid Bulk (4.3%)
- **Status:** ✅ PASSED

**Files:**
```
03_DOCUMENTATION/03.04_summaries/sample_test_15k/
  ├── sample_15k_classified_v3.6.0.csv
  └── classification_stats_v3.6.0.csv
```

---

## Full Documentation

For complete details, see:
```
SESSION_RESUME_20260120.md  (full session state & instructions)
CLASSIFICATION_15K_TEST_RESULTS.md  (test validation)
DIAGNOSTIC_REPORT_5K_TEST.md  (bug fix details)
```

---

## Questions?

**"Is everything ready?"**
→ YES. All scripts fixed, tested, validated.

**"Can I run it now?"**
→ YES. Just execute the command above.

**"How long will it take?"**
→ ~8-10 hours per year, ~25-30 hours total.

**"What if it fails?"**
→ Can re-run anytime. No data corruption risk.

**"Will this affect USACE processing?"**
→ NO. Completely separate pipelines.

---

**Status:** 🟢 GO
**Confidence:** HIGH
**Action:** Run `python run_full_pipeline.py [year]`
