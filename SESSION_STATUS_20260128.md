# Session Status - 2026-01-28
**Status:** 🔴 INVESTIGATING RULE ORDER ISSUES
**Current Focus:** Panjiva Classification Fixes ONLY

---

## Problem Statement (Clarified)

### The Real Issues

**PRIMARY PROBLEM: Rule Order/Priority in Classification**
- Rules executing in wrong sequence
- Classifications being overridden incorrectly
- Lock levels not working as expected
- Need to diagnose and fix rule execution logic

**SECONDARY PROBLEM: USACE Matching (FUTURE - SEPARATE)**
- Matching classified Panjiva imports to USACE port call master
- Roll up/grouping of matched data
- **This is NOT the current focus**
- Will address AFTER classification is fixed

---

## Bifurcation Strategy

### Two Independent Pipelines

```
PIPELINE A: Panjiva Classification
├── Input:  Panjiva imports (preprocessed)
├── Process: Classification rules (dictionary v3.6.0)
├── Output: Classified imports
└── STATUS: 🔴 BROKEN (rule order issues)

PIPELINE B: USACE Matching (Future)
├── Input:  Classified imports + USACE port call master
├── Process: Match on vessel/port/date, roll up/aggregate
├── Output: Matched dataset
└── STATUS: 🔴 NOT STARTED (waiting for Pipeline A to be fixed)
```

**Current Work:** Fix Pipeline A ONLY. Ignore Pipeline B for now.

---

## What Needs to Be Done

### Immediate Actions (This Session)

1. **Diagnose rule order problem**
   - Review 15K test results for specific misclassifications
   - Identify which rules are firing incorrectly
   - Trace execution order for problem records
   - Document specific examples

2. **Review dictionary v3.6.0 structure**
   - Check phase ordering (1, 2, 3, 5, 6)
   - Check tier values (1-5) within each phase
   - Check lock level settings
   - Identify conflicting rules

3. **Identify root cause**
   - Are phases executing out of order?
   - Are locks being ignored?
   - Are high-tier rules being overridden by low-tier rules?
   - Are there logic errors in the classification script?

4. **Propose fixes**
   - Dictionary changes (phase/tier/lock adjustments)
   - OR script logic changes (execution order, lock checks)
   - OR both

---

## What NOT to Do

❌ **Do NOT run full year classification yet**
- Reason: Will waste 25+ hours with wrong results

❌ **Do NOT work on USACE matching**
- Reason: Not relevant until classification is fixed
- Separate problem for later

❌ **Do NOT assume column fix solved everything**
- Reason: Column fix was minor, rule order is the major issue

---

## Key Questions to Answer

1. **What specific classifications are wrong?**
   - Need examples from 15K test
   - Expected vs. actual Group/Commodity/Cargo/Cargo_Detail

2. **Which rules are involved?**
   - Rule IDs from dictionary
   - Phase and tier numbers
   - Lock levels set

3. **What's the execution sequence?**
   - Which rule fires first?
   - Which rule overrides it?
   - Should the lock have prevented override?

4. **What's the root cause?**
   - Dictionary configuration error?
   - Script logic error?
   - Both?

---

## Files to Review

### Test Results (15K sample)
```
03_DOCUMENTATION/03.04_summaries/sample_test_15k/
  ├── sample_15k_classified_v3.6.0.csv        (classification output)
  └── classification_stats_v3.6.0.csv         (phase breakdown)
```

### Dictionary (Current version)
```
01_DICTIONARIES/01.01_cargo_classification/
  └── cargo_classification_dictionary_CURRENT_v3.6.0.csv  (668 rules)
```

### Classification Scripts
```
02_SCRIPTS/02.07_production/
  ├── classify_15k_sample.py                  (test script)
  └── run_full_pipeline.py                    (production script)
```

---

## Success Criteria

Before proceeding to full year classification:

✅ **Understand the problem**
- Specific examples of misclassification documented
- Root cause identified

✅ **Fix implemented**
- Dictionary updated OR script updated OR both
- Version incremented (e.g., v3.6.0 → v3.7.0)

✅ **Fix validated**
- Re-run 15K test
- Verify misclassifications are corrected
- Check no regressions in other classifications

✅ **Ready for production**
- Confidence level HIGH
- No known issues remaining

---

## Timeline

**Current Phase:** Investigation & Diagnosis
**Estimated Time:** 2-4 hours (review data, identify issues)

**Next Phase:** Fix Implementation
**Estimated Time:** 1-2 hours (update dictionary/script)

**Validation Phase:** Re-test
**Estimated Time:** ~20 minutes (15K test run)

**Production Phase:** Full Year Classification
**Estimated Time:** 24-30 hours (ONLY AFTER above complete)

---

## Status Summary

```
Investigation:  🟡 READY TO START
Diagnosis:      🔴 NOT STARTED
Fix:            🔴 BLOCKED (waiting for diagnosis)
Validation:     🔴 BLOCKED (waiting for fix)
Production:     🔴 BLOCKED (waiting for validation)

USACE Matching: 🔴 OUT OF SCOPE (future work)
```

---

## Next Command

**DO NOT run classification yet. Instead:**

```bash
# Review test results to find misclassification examples
cat "G:\My Drive\LLM\project_manifest\03_DOCUMENTATION\03.04_summaries\sample_test_15k\sample_15k_classified_v3.6.0.csv" | head -n 100
```

Or ask Claude to:
- "Analyze the 15K test results and identify misclassifications"
- "Review dictionary v3.6.0 for rule order conflicts"
- "Explain how lock levels should work and check if they're correct"

---

**Session Focus:** Panjiva classification fixes ONLY
**Out of Scope:** USACE matching, roll up, aggregation
**Status:** Investigation phase - do not run production yet
