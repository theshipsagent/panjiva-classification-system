# Complete Panjiva Classification Workflow v1.0.0

## 📋 Overview

This is a **3-step pipeline** for classifying Panjiva import data:

1. **Step 01b: Enhance AUTHORITATIVE** - Add missing columns (REC_ID, Package_Type, Vessel_Type_Simple)
2. **Step 02: Classify Cargo** - Assign Group → Commodity → Cargo → Cargo Detail
3. **Step 03: Enrich Ports** - Add Port_Consolidated, Port_Coast, Port_Region, Port_Code

---

## 🔄 Complete Workflow

### For Each Year (2023, 2024, 2025):

```bash
# Step 1: Enhance AUTHORITATIVE file (adds 5 columns)
cd "G:\My Drive\LLM\project_manifest\panjiva_classification_v2\02_SCRIPTS"
python step01b_enhance_authoritative_v1.0.0.py 2024

# Output: 03_DATA/01_preprocessed/panjiva_imports_2024_preprocessed_v1.0.0_*.csv
# Time: ~1-2 minutes for 449K records

# Step 2: Classify cargo (5 phases)
python step02_classify_v1.0.0.py --input "../03_DATA/01_preprocessed/panjiva_imports_2024_preprocessed_v1.0.0_*.csv" --year 2024

# Output: 03_DATA/02_classified/panjiva_imports_2024_classified_v1.0.0_*.csv
# Time: ~40-60 minutes for 449K records

# Step 3: Enrich ports (add 4 columns)
python step03_enrich_ports_v1.0.0.py 2024

# Output: 03_DATA/03_enriched/panjiva_imports_2024_enriched_v1.0.0_*.csv
# Time: ~2-3 minutes for 449K records
```

---

## 📊 Data Flow

```
AUTHORITATIVE (51 cols)
    ↓
Step 01b: Enhance
    - Add REC_ID (audit trail)
    - Add Package_Type (for LBK rules)
    - Add Vessel_Type_Simple (from ship registry)
    - Add Carrier Name (extracted from Carrier)
    - Add Count (always 1)
    ↓
PREPROCESSED (60 cols)
    - Classification columns initialized (empty)
    - Lock flags initialized (FALSE)
    ↓
Step 02: Classify
    Phase 1: Carrier locks (65 rules)
    Phase 2: HS4 broad (51 rules)
    Phase 3: HS + Keywords (263 rules)
    Phase 5: Default catch-all (1 rule)
    Phase 6: Refinements (288 rules)
    ↓
CLASSIFIED (60 cols)
    - Classification filled: Group, Commodity, Cargo, Cargo Detail
    - Locks set: Group_Locked, Commodity_Locked, etc.
    - Phase/Rule tracked: Classified_Phase, Last_Rule_ID
    - Ports still empty: Port_Consolidated, Port_Coast, Port_Region, Port_Code
    ↓
Step 03: Enrich Ports
    - Match "Port of Discharge (D)" → us_port_dictionary.csv
    - Fill: Port_Consolidated, Port_Coast, Port_Region, Port_Code
    ↓
ENRICHED (60 cols) ✅ FINAL
    - All classification complete
    - All port data complete
    - Ready for analysis/export
```

---

## 📂 File Locations

### Input Files (Parent Project)
```
G:\My Drive\LLM\project_manifest\00_DATA\00.02_PREPROCESSED\
├── panjiva_imports_2023_AUTHORITATIVE_v1.0.0.csv  (11.8 MB, 98K records)
├── panjiva_imports_2024_AUTHORITATIVE_v1.0.0.csv  (346 MB, 449K records)
└── panjiva_imports_2025_AUTHORITATIVE_v1.0.0.csv  (308 MB, ~380K records)
```

### Reference Files
```
panjiva_classification_v2\00_REFERENCE\
├── dictionary_v3.6.0.csv          (668 classification rules)
└── ship_registry.csv              (vessel type lookup)

Parent Project\01_DICTIONARIES\01.02_ports\
└── us_port_dictionary.csv         (777 port mappings)
```

### Output Files (This Project)
```
panjiva_classification_v2\03_DATA\
├── 01_preprocessed\               Step 01b output (60 cols)
├── 02_classified\                 Step 02 output (60 cols)
└── 03_enriched\                   Step 03 output (60 cols) ⭐ FINAL
```

---

## ⏱️ Timing Estimates

### 2024 (449,233 records)
- **Step 01b:** ~1-2 minutes
- **Step 02:** ~40-60 minutes
  - Phase 1: ~10 minutes
  - Phase 2: ~5 minutes
  - Phase 3: ~15-20 minutes
  - Phase 5: ~1-2 minutes
  - Phase 6: ~10-15 minutes
- **Step 03:** ~2-3 minutes
- **Total:** ~45-65 minutes

### 2023 (98,000 records)
- **Step 01b:** ~1 minute
- **Step 02:** ~10-15 minutes
- **Step 03:** ~1 minute
- **Total:** ~12-17 minutes

### 2025 (~380,000 records)
- **Step 01b:** ~1-2 minutes
- **Step 02:** ~30-45 minutes
- **Step 03:** ~2-3 minutes
- **Total:** ~35-50 minutes

---

## 📋 Column Counts Through Pipeline

| Stage | Columns | Description |
|-------|---------|-------------|
| AUTHORITATIVE | 51 | Input from parent project |
| After Step 01b | 60 | +5 columns (REC_ID, Package_Type, etc.) +4 classification columns |
| After Step 02 | 60 | Same columns, classification filled |
| After Step 03 | 60 | Same columns, ports filled |

---

## 🎯 Success Metrics

### Step 01b (Enhancement)
- ✅ REC_ID format correct: `PANV_IMP_FILE###_R######`
- ✅ REC_ID unique: 100%
- ✅ Package_Type present: Column exists
- ✅ Vessel enrichment: 40-50% (expected)

### Step 02 (Classification)
- ✅ 100% classification rate: All records assigned Group/Commodity/Cargo
- ✅ Phase distribution: Phase 1 ~60%, Phase 5 ~30%, others ~10%
- ✅ Lock levels set: Group locked ~65%, Commodity locked ~50%
- ✅ No errors in log

### Step 03 (Port Enrichment)
- ✅ Port enrichment rate: 80-95% (expected)
- ✅ Top ports identified: Houston, New York, Savannah, etc.
- ✅ Coast/Region assigned

---

## 🚨 Current Status (2026-01-28 10:30)

### ✅ Completed:
- 2024 Step 01b: ✅ Enhanced (449K records)
- 2024 Step 02: 🔄 IN PROGRESS
  - Phase 1: ✅ Complete (290,392 classified)
  - Phase 2: 🔄 Running (51 rules)
  - Estimated completion: ~11:00 AM

### ⏳ Pending:
- 2024 Step 03: Port enrichment (~2-3 minutes)
- 2023 Full pipeline: Steps 01b → 02 → 03 (~12-17 minutes)
- 2025 Full pipeline: Steps 01b → 02 → 03 (~35-50 minutes)

---

## 🔍 Verification Commands

### Check if Step 02 (Classification) completed:
```bash
tail -n 50 "C:\Users\wsd3\AppData\Local\Temp\claude\G--My-Drive-LLM-project-manifest\tasks\b154255.output"
```
Look for: "CLASSIFICATION COMPLETE"

### Quick stats on classified file:
```bash
cd "G:\My Drive\LLM\project_manifest\panjiva_classification_v2"
python -c "
import pandas as pd
from pathlib import Path

files = list(Path('03_DATA/02_classified').glob('panjiva_imports_2024_classified*.csv'))
if files:
    latest = sorted(files)[-1]
    df = pd.read_csv(latest, nrows=5000, dtype=str)
    print(f'File: {latest.name}')
    print(f'Size: {latest.stat().st_size / (1024*1024):.1f} MB')
    print(f'\nPhase distribution:')
    for phase, count in df['Classified_Phase'].value_counts().sort_index().items():
        print(f'  Phase {phase}: {count:,} ({count/len(df)*100:.1f}%)')
"
```

### Quick stats on enriched file (after Step 03):
```bash
cd "G:\My Drive\LLM\project_manifest\panjiva_classification_v2"
python -c "
import pandas as pd
from pathlib import Path

files = list(Path('03_DATA/03_enriched').glob('panjiva_imports_2024_enriched*.csv'))
if files:
    latest = sorted(files)[-1]
    df = pd.read_csv(latest, nrows=5000, dtype=str)
    print(f'File: {latest.name}')
    print(f'Size: {latest.stat().st_size / (1024*1024):.1f} MB')
    enriched = (df['Port_Code'] != '').sum()
    print(f'\nPort enrichment: {enriched:,} / {len(df):,} ({enriched/len(df)*100:.1f}%)')
    print(f'\nTop 10 ports:')
    for port, count in df['Port_Consolidated'].value_counts().head(10).items():
        print(f'  {port}: {count:,}')
"
```

---

## 📝 Important Notes

### REC_ID Format
- Format: `PANV_IMP_FILE###_R######`
- Example: `PANV_IMP_FILE001_R000000` (first record of file 001)
- Purpose: Permanent audit trail, never changes

### Package_Type
- Critical for 218 rules (33% of dictionary)
- Values: LBK (Liquid Bulk), BLK (Dry Bulk), CON (Container), etc.
- Missing this column = many classification failures

### Lock Levels
- Phase 1 (Carrier): Lock Group only → allows later refinement
- Phase 2-3 (HS4/Keywords): Lock all 4 levels → final classification
- Phase 5 (Default): No locks → fully open for Phase 6 refinement
- Phase 6 (Refinements): Lock all 4 levels → final classification

### Port Matching
- Handles complex port names: "Port of Brunswick, Brunswick, Georgia"
- Strips prefixes: "Port of", "Port Authority of", etc.
- Normalizes states: "Texas" → "TX"
- Fallback: Partial match on city name

---

## 🔜 Next Actions (After 2024 Step 02 Completes)

1. **Run 2024 Step 03** (Port Enrichment)
   ```bash
   python step03_enrich_ports_v1.0.0.py 2024
   ```

2. **Run Full 2023 Pipeline**
   ```bash
   python step01b_enhance_authoritative_v1.0.0.py 2023
   # Wait for completion
   python step02_classify_v1.0.0.py --input "../03_DATA/01_preprocessed/panjiva_imports_2023_preprocessed_v1.0.0_*.csv" --year 2023
   # Wait for completion
   python step03_enrich_ports_v1.0.0.py 2023
   ```

3. **Run Full 2025 Pipeline**
   ```bash
   python step01b_enhance_authoritative_v1.0.0.py 2025
   # Wait for completion
   python step02_classify_v1.0.0.py --input "../03_DATA/01_preprocessed/panjiva_imports_2025_preprocessed_v1.0.0_*.csv" --year 2025
   # Wait for completion
   python step03_enrich_ports_v1.0.0.py 2025
   ```

4. **Compare Results Across Years**
   - Tonnage by commodity
   - Classification rates
   - Port distribution
   - Year-over-year changes

---

## 📚 Documentation Files

- `SESSION_STATUS_20260128_1020.md` - Session summary with test results
- `QUICK_CHECK_PROGRESS.md` - Progress checking commands
- `06_DOCUMENTATION/DICTIONARY_ANALYSIS_v3.6.0.md` - Complete dictionary analysis
- `04_TESTS/classification_quality_check.txt` - 5K sample QA report
- `PIPELINE_RULES.md` - 15 strict rules to prevent drift

---

**Document Version:** 1.0.0
**Created:** 2026-01-28
**Updated:** 2026-01-28 10:30
**Status:** 2024 Step 02 in progress (Phase 2/5)
