# Quick Start Guide: Dictionary v5.0.0

**Date**: 2026-02-04
**Status**: Testing in progress

---

## What Changed in v5.0.0

### TL;DR
- **217 rules → 71 rules** (67% reduction)
- **Phase 5 deleted** (100% duplicate of Phase 4)
- **Phase 4 consolidated** (101 → 56 rules)
- **Expected**: 67% faster classification (12 hours → 3-4 hours)

---

## Using v5.0.0

### File Location
```
G:\My Drive\LLM\project_manifest\panjiva_production_v1\01_dictionary\
cargo_classification_dictionary_v5.0.0_CONSOLIDATED.csv
```

### In Your Classification Script
Update the `DICT_PATH` variable:

```python
# OLD v4.1.0
DICT_PATH = Path(__file__).parent / "01_dictionary" / "cargo_classification_dictionary_v4.1.0_SIMPLE.csv"

# NEW v5.0.0
DICT_PATH = Path(__file__).parent / "01_dictionary" / "cargo_classification_dictionary_v5.0.0_CONSOLIDATED.csv"
```

### Phase Loop Update
Remove Phase 5 from your loop:

```python
# OLD (with Phase 5)
for phase_str in ['1', '2', '3', '4', '5']:
    ...

# NEW (no Phase 5)
for phase_str in ['1', '2', '3', '4']:
    ...
```

---

## Key Consolidations

### Steel (9 → 4)
- **OLD**: STEEL-COILS, STEEL-PIPE, STEEL-REBAR, STEEL-BEAMS, STEEL-BARS, STEEL-TINPLATE (6 separate)
- **NEW**: STEEL-FINISHED (merged all 6 into 1 rule)
- **Keywords preserved**: Can still differentiate coil vs pipe post-classification

### Petroleum (14 → 5)
- **PETROLEUM-CRUDE**: Kept as-is (209M tons)
- **PETROLEUM-LIGHT-PRODUCTS**: Merged diesel+jet+gasoline+reformate+alkylate+LSSR
- **PETROLEUM-HEAVY-FUEL**: Merged fuel oil+VLSFO+HSFO+base oil
- **PETROLEUM-SPECIALTY**: Merged naphtha+condensate
- **PETROLEUM-ASPHALT**: Kept separate

### Chemicals (13 → 5)
- **CHEMICALS-ALCOHOLS**: methanol+MIBC+paraffin
- **CHEMICALS-AROMATICS**: benzene+LAB
- **CHEMICALS-ACIDS-CAUSTICS**: caustic+sulfuric+fatty acids+ethylhexanoic
- **CHEMICALS-ESTERS-KETONES**: acetone+methacrylate+ethyl acetate
- **CHEMICALS-SPECIALTY**: isocyanate

### Fertilizers (7 → 3)
- **FERTILIZERS-LIQUID**: UAN+CAN
- **FERTILIZERS-NPK**: urea+DAP+MAP+potash
- **PHOSPHATE-ROCK**: Kept separate

### Construction (7 → 3)
- **CONSTRUCTION-CEMENT**: Kept separate (32M tons)
- **CONSTRUCTION-AGGREGATES**: aggregates+stone+gypsum
- **CONSTRUCTION-BYPRODUCTS**: slag+fly ash+pozzolan

---

## What Was NOT Changed

### High-Impact Commodities (kept distinct)
✅ PETROLEUM-CRUDE (209M tons, 29% of all tonnage)
✅ GRAIN-WHEAT, GRAIN-CORN, GRAIN-SOYBEANS (different HS codes)
✅ CONSTRUCTION-CEMENT (32M tons)
✅ SUGAR, COAL, LNG, LPG, AMMONIA

### Carrier Locks (preserved)
✅ STEEL-CLIPPER (Clipper Line carrier-specific)

### Phases 1-3 (unchanged)
✅ Carrier locks (CARRIER-RORO, CARRIER-REEFER, CARRIER-EXCLUDE)
✅ Vessel type hints (CARRIER-DRYBULK, CARRIER-TANKER, CARRIER-LNG)
✅ Exclusions (NOISE-*, MACHINERY-EXCLUDE, RAILWAY-EXCLUDE, VEHICLES-EXCLUDE)

---

## Testing Checklist

Before deploying v5.0.0 to production:

1. ✅ Run on 10% sample (130K records)
   - Expected runtime: ~1 hour (vs 3 hours with v4.1.0)
   - Expected classification: 86%+ records

2. ⏭️ Validate tonnage distribution
   - Compare vs v4.1.0 results
   - Check top 10 commodities (crude, cement, fuel oil, etc.)
   - Ensure 91%+ tonnage coverage

3. ⏭️ Check for regressions
   - Steel products still classified?
   - Petroleum variants captured?
   - Chemicals properly grouped?

4. ⏭️ Run on full 2023 (1.3M records)
   - Expected runtime: 3-4 hours (vs 12 hours with v4.1.0)
   - Measure actual speedup

---

## Rollback Instructions

If v5.0.0 shows issues, revert to v4.1.0:

```python
# Revert to v4.1.0
DICT_PATH = Path(__file__).parent / "01_dictionary" / "cargo_classification_dictionary_v4.1.0_SIMPLE.csv"

# Restore Phase 5 loop
for phase_str in ['1', '2', '3', '4', '5']:
    ...
```

**v4.1.0 location**:
```
G:\My Drive\LLM\project_manifest\panjiva_production_v1\01_dictionary\
cargo_classification_dictionary_v4.1.0_SIMPLE.csv
```

---

## Expected Results

### Classification Rate
- **v4.1.0**: 86% records, 91% tonnage
- **v5.0.0**: 86% records, 91% tonnage (same)
- **Why**: HS codes and keywords preserved, only grouping changed

### Runtime (Full 2023 - 1.3M records)
- **v4.1.0**: ~12 hours
- **v5.0.0**: ~3-4 hours (67% faster)
- **With vectorization**: ~30-60 minutes (potential future optimization)

### Comparison Iterations
- **v4.1.0**: 217 rules × 1.3M records = 282M comparisons
- **v5.0.0**: 71 rules × 1.3M records = 92M comparisons
- **Reduction**: 67% fewer iterations

---

## Troubleshooting

### Issue: Classification rate drops below 86%
**Diagnosis**: Some consolidation lost coverage
**Fix**: Check which commodity groups dropped, selectively un-consolidate those rules

### Issue: Runtime not improved
**Diagnosis**: Script bottleneck not in rule iteration
**Fix**: Profile script to find actual bottleneck (likely df.loc[idx] access)

### Issue: Top commodities missing
**Diagnosis**: Keyword matching failed due to consolidation
**Fix**: Split consolidated rule back to original separate rules

---

## Next Optimizations (After v5.0.0 Validates)

### 1. Vectorize HS Code Filtering
Pre-filter dataframe by HS code before keyword matching:

```python
# Instead of checking each record
for idx in df.index:
    if check_match(record, rule):
        classify(record, rule)

# Do this
hs27_mask = df['HS2'] == '27'
hs27_df = df[hs27_mask]
for rule in petroleum_rules:
    apply_to_subset(hs27_df, rule)
```

**Expected speedup**: 4-8x faster (3-4 hours → 30-60 minutes)

### 2. Batch Keyword Matching
Use pandas `.str.contains()` instead of record-by-record iteration:

```python
# Instead of
for idx in df.index:
    if 'crude oil' in df.loc[idx, 'Goods Shipped']:
        ...

# Do this
crude_mask = df['Goods Shipped'].str.contains('crude oil', case=False, na=False)
df.loc[crude_mask, 'Commodity'] = 'Crude Oil'
```

**Expected speedup**: 10-20x faster for keyword matching

### 3. Early Exit for Locked Records
Already implemented in test script - skip locked records early:

```python
unlocked_mask = df['Cargo_Detail_Locked'] != 'TRUE'
unlocked_indices = df[unlocked_mask].index.tolist()

for idx in unlocked_indices:  # Only process unlocked
    ...
```

---

## Files

**Dictionary**:
- v5.0.0: `cargo_classification_dictionary_v5.0.0_CONSOLIDATED.csv` (71 rules)
- v4.1.0: `cargo_classification_dictionary_v4.1.0_SIMPLE.csv` (217 rules)

**Test Script**:
- `test_v5.0.0_on_10pct_sample.py`

**Documentation**:
- Summary: `CONSOLIDATION_v5.0.0_SUMMARY.md`
- Complete: `DICTIONARY_CONSOLIDATION_COMPLETE.md`
- Quick Start: `QUICK_START_v5.0.0.md` (this file)

---

## Support

**If test passes**: Deploy to full 2023, measure runtime
**If test fails**: Check output, identify regressions, selectively revert consolidations
**Questions**: Review `CONSOLIDATION_v5.0.0_SUMMARY.md` for detailed consolidation rationale

---

**Current Status**: ⏳ Testing in progress on 10% sample (130K records)
**Expected**: Results in ~1 hour from start (started 2026-02-04 19:58:50)

---

END OF QUICK START GUIDE
