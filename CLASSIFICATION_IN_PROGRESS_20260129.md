# Classification Jobs In Progress
**Date:** 2026-01-29
**Status:** 🟢 ALL 3 YEARS RUNNING IN PARALLEL

---

## Background Jobs Running

| Year | Records | Task ID | Status | Estimated Time |
|------|---------|---------|--------|----------------|
| **2023** | 15,000 | bee292a | 🟢 RUNNING | ~30-60 min |
| **2024** | 449,233 | b4db121 | 🟢 RUNNING | ~8-10 hours |
| **2025** | 398,747 | bbeae2f | 🟢 RUNNING | ~7-9 hours |

**Total Estimated Time:** ~8-10 hours (running in parallel)

---

## What's Happening

All three years are being classified simultaneously using:
- **Input:** v2.0.0 preprocessed data (with 88-90% vessel enrichment)
- **Dictionary:** v3.6.0 (668 active rules)
- **Pipeline:** Phase 1 → 2 → 3 → 5 → 6
- **Expected Coverage:** 100% classification

---

## Monitoring Progress

### Option 1: Check Task Output Files

```bash
# View 2024 progress
type "C:\Users\wsd3\AppData\Local\Temp\claude\G--My-Drive-LLM-project-manifest\tasks\b4db121.output"

# View 2023 progress
type "C:\Users\wsd3\AppData\Local\Temp\claude\G--My-Drive-LLM-project-manifest\tasks\bee292a.output"

# View 2025 progress
type "C:\Users\wsd3\AppData\Local\Temp\claude\G--My-Drive-LLM-project-manifest\tasks\bbeae2f.output"
```

### Option 2: Check for Completed Files

```bash
cd "G:\My Drive\LLM\project_manifest\00_DATA\00.03_MATCHED"

# Check if output files exist
dir panjiva_imports_*_classified_v2.0.0.csv
dir classification_stats_*_v2.0.0.csv
```

### Option 3: Monitor Python Processes

```bash
# See all running Python processes
tasklist | findstr python
```

---

## Expected Output Files

When complete, you'll find these files in `00_DATA/00.03_MATCHED/`:

### Classified Data
```
panjiva_imports_2023_classified_v2.0.0.csv  (~13 MB)
panjiva_imports_2024_classified_v2.0.0.csv  (~1.2 GB)
panjiva_imports_2025_classified_v2.0.0.csv  (~1.0 GB)
```

### Statistics
```
classification_stats_2023_v2.0.0.csv
classification_stats_2024_v2.0.0.csv
classification_stats_2025_v2.0.0.csv
```

---

## What to Expect in Output

### Phase-by-Phase Progress

The classification script reports progress for each phase:

```
Processing Phase 1...
  Rules in phase: 65
  Progress: 22,461 / 449,233 (5.0%) - 8,253 matches so far
  Progress: 44,923 / 449,233 (10.0%) - 16,506 matches so far
  ...
  Matched: 247,178 records in 1853.2 seconds
```

### Expected Phase Distribution

Based on 15K validation test:
- **Phase 1:** ~55% (carrier locks - RoRo, Tanker, Reefer)
- **Phase 2:** ~0.6% (HS4 codes)
- **Phase 3:** ~1.5% (HS + keywords)
- **Phase 5:** ~30% (general cargo catch-all)
- **Phase 6:** ~13% (specific refinements)

### Expected Group Distribution

- **Dry Bulk:** ~95%
- **Liquid Bulk:** ~5%
- **Liquid Gas:** <1%

---

## Timeline

| Time | Event |
|------|-------|
| 12:47 PM | 2023 classification started |
| 12:52 PM | 2024 classification started |
| 12:52 PM | 2025 classification started |
| ~1:30 PM | 2023 expected to complete (estimated) |
| ~8:00 PM | 2024 expected to complete (estimated) |
| ~8:00 PM | 2025 expected to complete (estimated) |

**Note:** Times are estimates. Actual runtime depends on system performance and may vary by ±2 hours.

---

## What Happens After Completion

Once all three years complete, you'll need to:

1. **Validate Results**
   - Check 100% classification achieved
   - Verify group distribution is reasonable
   - Check no column errors
   - Confirm vessel enrichment rates

2. **Compare to Previous Results** (optional)
   - Compare v2.0.0 vs v1.0.0 results
   - Verify vessel rules improved classifications
   - Document accuracy improvements

3. **Next Steps**
   - Mark tasks complete
   - Update documentation
   - Consider USACE matching (separate pipeline)

---

## Troubleshooting

### If Jobs Fail

**Check logs:**
```bash
type "C:\Users\wsd3\AppData\Local\Temp\claude\G--My-Drive-LLM-project-manifest\tasks\[TASK_ID].output"
```

**Common issues:**
- Out of memory (close other applications)
- Disk space full (need ~5 GB free)
- File locked (close Excel if open)

**Recovery:**
Safe to re-run - jobs are idempotent.

### If Jobs Are Too Slow

**Normal behavior:**
- Phase 1 is slowest (most rules, most records matched)
- Progress may appear to stall during large batches
- CPU usage should be high (~80-100%)

**If truly stuck:**
- Check Task Manager for CPU usage
- If 0% CPU for >5 minutes, job may have crashed
- Check output file for errors

---

## Task IDs for Reference

```
2023: bee292a
2024: b4db121
2025: bbeae2f
```

Use these IDs with Claude's TaskOutput command to check status.

---

## Status Checks

### Quick Status Check

```bash
# See how many output files exist
cd "G:\My Drive\LLM\project_manifest\00_DATA\00.03_MATCHED"
dir panjiva_imports_*_classified_v2.0.0.csv | find /c ".csv"
```

When this shows "3", all jobs are complete.

### Check File Sizes (Growth)

```bash
cd "G:\My Drive\LLM\project_manifest\00_DATA\00.03_MATCHED"
dir panjiva_imports_*_classified_v2.0.0.csv
```

Files will grow as classification progresses. Final sizes:
- 2023: ~13 MB
- 2024: ~1.2 GB
- 2025: ~1.0 GB

---

## Success Criteria

✅ All three jobs complete without errors
✅ Output files created with correct sizes
✅ Statistics show 100% classification
✅ Group distribution matches expected (~95% Dry Bulk)
✅ Vessel enrichment reflected in Phase 1 matches (~55%)

---

**Current Status:** 🟢 ALL RUNNING
**Next Update:** When jobs complete or if errors occur
**Estimated Completion:** ~8:00-9:00 PM (2026-01-29)

---

**Document Version:** 1.0.0
**Created:** 2026-01-29 12:52 PM
**Status:** ACTIVE - JOBS RUNNING
