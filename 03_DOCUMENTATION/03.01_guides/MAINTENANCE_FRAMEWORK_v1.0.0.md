# MAINTENANCE & SERVICE FRAMEWORK v1.0.0

**Date:** 2026-02-08
**Status:** Production Ready

---

## OVERVIEW

This framework supports ongoing operations with:
1. **Incremental data processing** - Add new raw files without full reprocess
2. **Targeted reclassification** - Surgical updates to specific records
3. **Full traceability** - RAW_REC_ID links back to original files
4. **Backup & recovery** - All changes are reversible

---

## PHASE SEPARATION

### CURRENT PHASE: Preprocessing & Classification
**Location:** `02_SCRIPTS/02.01_preprocessing/` through `02_SCRIPTS/02.07_production/`

**Characteristics:**
- Lock-based rules (once classified, locked)
- General-purpose classification
- High-volume, automated
- **Output:** Classified records ready for analytics

### FUTURE PHASE: Analytics & Targeting
**Location:** TBD (separate phase, not yet built)

**Characteristics:**
- **Has overwrite permission** (can override preprocessing)
- Very targeted, specific matches
- Low error risk (highly specific rules)
- **Input:** Preprocessing output
- **Output:** Refined, targeted classifications

---

## RAW FILE MANAGEMENT

### Archive Location
**Path:** `00_DATA/00.05_BACKUPS/processed_raw_files/`

### Policy
- **NEVER DELETE** raw files after processing
- Archive to `processed_raw_files/{year}_{filename}`
- Maintains full traceability via RAW_REC_ID
- Can always reprocess from raw if needed

### Example
```
00_DATA/
  00.01_RAW/
    new_file_001.xlsx  ← New file drops here

  00.05_BACKUPS/
    processed_raw_files/
      2025_file_001.xlsx  ← Archived after processing
      2025_file_002.xlsx
```

---

## INCREMENTAL PROCESSING

### When New Data Arrives

**Script:** `02_SCRIPTS/02.08_maintenance/incremental_add_new_data_v1.0.0.py`

**Usage:**
```bash
cd "G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.08_maintenance"

# Add new files to 2025 dataset
python incremental_add_new_data_v1.0.0.py --year 2025 --new_files "00_DATA/00.01_RAW/new_*.xlsx"
```

**What It Does:**
1. Loads existing `panjiva_imports_2025_AUTHORITATIVE_v2.0.0.csv`
2. Gets highest RAW_REC_ID (e.g., PANV_IMP_FILE170_R012345)
3. Processes new files starting from next ID (PANV_IMP_FILE171_R000001)
4. Appends new records to existing AUTHORITATIVE file
5. Archives processed raw files

**Output:**
- Updated: `panjiva_imports_2025_AUTHORITATIVE_v2.0.0.csv`
- Archived: `00_DATA/00.05_BACKUPS/processed_raw_files/2025_new_file_001.xlsx`

---

## TARGETED RECLASSIFICATION

### When You Need to Fix Something

**Script:** `02_SCRIPTS/02.08_maintenance/targeted_reclassify_v1.0.0.py`

**Common Scenarios:**

#### 1. Reclassify All Records with Specific HS4 Code
```bash
# All HS4 2709 → Crude Oil / Basrah Heavy
python targeted_reclassify_v1.0.0.py \
    --year 2023 \
    --hs4 2709 \
    --group "Liquid Bulk" \
    --commodity "Petroleum" \
    --cargo "Crude Oil" \
    --cargo_detail "Basrah Heavy"
```

#### 2. Reclassify Specific Carrier
```bash
# WALLENIUS carrier → RoRo Vehicles
python targeted_reclassify_v1.0.0.py \
    --year 2023 \
    --carrier WLWH \
    --group "Break Bulk" \
    --commodity "General Cargo" \
    --cargo "Vehicles" \
    --cargo_detail "RoRo Vehicles"
```

#### 3. Reclassify by Keyword
```bash
# All "BASRAH HEAVY" mentions → Basrah Heavy crude
python targeted_reclassify_v1.0.0.py \
    --year 2023 \
    --keyword "BASRAH HEAVY" \
    --group "Liquid Bulk" \
    --commodity "Petroleum" \
    --cargo "Crude Oil" \
    --cargo_detail "Basrah Heavy"
```

#### 4. Reclassify Specific Records (by RAW_REC_ID)
```bash
# Fix 3 specific records
python targeted_reclassify_v1.0.0.py \
    --year 2023 \
    --rec_id "PANV_IMP_FILE001_R000123,PANV_IMP_FILE001_R000456,PANV_IMP_FILE002_R000789" \
    --group "Liquid Bulk" \
    --commodity "Petroleum" \
    --cargo "Crude Oil" \
    --cargo_detail "Crude Oil"
```

#### 5. Preview Changes (Dry Run)
```bash
# See what WOULD be changed without actually changing it
python targeted_reclassify_v1.0.0.py \
    --year 2023 \
    --hs4 2709 \
    --group "Liquid Bulk" \
    --commodity "Petroleum" \
    --cargo "Crude Oil" \
    --cargo_detail "Crude Oil" \
    --dry_run
```

### What It Does

1. **Creates backup** - Before any changes, saves original to `00_DATA/00.05_BACKUPS/targeted_reclassifications/`
2. **Filters records** - Finds all records matching your criteria
3. **Shows preview** - Lists samples of what will change
4. **Applies changes** - Updates classification for matched records
5. **Saves new version** - Outputs new file with timestamp
6. **Logs changes** - Creates detailed change log for traceability

### Reverting Changes

If you made a mistake:
```bash
# Change log tells you which backup to restore
# Example: Restore from backup_2023_before_reclassify_20260208_165900.csv

cd "G:\My Drive\LLM\project_manifest\00_DATA\00.05_BACKUPS\targeted_reclassifications"

# Copy backup back to matched directory
cp backup_2023_before_reclassify_20260208_165900.csv ../../00.03_MATCHED/panjiva_2023_classified_final.csv
```

---

## TRACEABILITY

### RAW_REC_ID Format
```
PANV_IMP_FILE{FILE_NUM}_R{RECORD_NUM}

Examples:
  PANV_IMP_FILE001_R000123  ← Record 123 from file 001
  PANV_IMP_FILE170_R012345  ← Record 12,345 from file 170
```

### Trace Record to Raw Source
1. Get RAW_REC_ID from classified file
2. Extract file number (e.g., FILE001)
3. Look up in `00_DATA/00.05_BACKUPS/processed_raw_files/`
4. Original record preserved in archived raw file

---

## BACKUP STRATEGY

### Automatic Backups

**Created by:**
- Incremental processing (before appending new data)
- Targeted reclassification (before any changes)
- Major pipeline runs (lock down backups)

**Location:** `00_DATA/00.05_BACKUPS/`

**Structure:**
```
00_DATA/00.05_BACKUPS/
  LOCK_DOWN_20260208_165738/        ← Full system snapshot
    BACKUP_MANIFEST.txt
    CLASSIFICATION_DICTIONARY_REBUILD.csv
    carrier_exclusion_list.csv
    panjiva_2023_classified_complete.csv
    ...

  targeted_reclassifications/        ← Before surgical changes
    backup_2023_before_reclassify_20260208_165900.csv
    reclassify_log_20260208_165900.txt

  processed_raw_files/               ← Raw file archive
    2023_file_001.xlsx
    2024_file_045.xlsx
    2025_file_170.xlsx
```

---

## DICTIONARY MANAGEMENT

### Current Dictionaries

**Main Classification:**
- `CLASSIFICATION_DICTIONARY_REBUILD.csv` (133 rules)
- Keyword-based rules + final catchall

**HS4 Statistical Alignment:**
- `CLASSIFICATION_DICTIONARY_HS4_ALIGNMENT.csv` (89 rules)
- Regenerate when needed based on latest classifications

**Carrier Rules:**
- `01_DICTIONARIES/01.04_carriers/carrier_exclusion_list.csv` (39 carriers)
- `01_DICTIONARIES/01.04_carriers/carrier_classification_rules.csv` (66 carriers)

### Updating Dictionaries

**Always create backup first:**
```bash
cd "G:\My Drive\LLM\project_manifest"

# Backup before editing
cp CLASSIFICATION_DICTIONARY_REBUILD.csv CLASSIFICATION_DICTIONARY_REBUILD_BACKUP_$(date +%Y%m%d_%H%M%S).csv
```

**After editing, validate:**
```bash
# Check for empty keywords in rules 1-132
python -c "
import pandas as pd
df = pd.read_csv('CLASSIFICATION_DICTIONARY_REBUILD.csv', dtype=str)
problems = df[(df['Order'].astype(int) <= 132) & (df['Keywords'].isna())]
if len(problems) > 0:
    print(f'WARNING: {len(problems)} rules have empty keywords')
    print(problems[['Order', 'Cargo_Detail']])
else:
    print('OK: No problems found')
"
```

---

## COMPLETE PIPELINE EXECUTION ORDER

### Full Run (New Year or Major Update)

```bash
cd "G:\My Drive\LLM\project_manifest"

# Stage 1: Carrier Exclusions
python 02_SCRIPTS/02.07_production/apply_carrier_exclusions_v1.0.0.py

# Stage 2: White Noise Filter
python 02_SCRIPTS/02.07_production/exclude_tank_waste_v1.0.0.py

# Stage 3.5: RoRo/Reefer Carrier Classification
python 02_SCRIPTS/02.07_production/apply_carrier_classification_v1.0.0.py  # TO BE CREATED

# Stage 4: Main Classification (133 rules)
python 02_SCRIPTS/02.07_production/apply_all_remaining_rules_v1.0.0.py

# Stage 5: HS4 Statistical Alignment (89 rules)
python 02_SCRIPTS/02.07_production/apply_hs4_alignment_v1.0.0.py  # TO BE CREATED
```

---

## CONTACTS & SUPPORT

**User:** WSD3
**AI Assistant:** Claude Code (Anthropic)
**Version:** 1.0.0
**Last Updated:** 2026-02-08

---

## NEXT STEPS

### Remaining Work
1. Complete `apply_carrier_classification_v1.0.0.py` (Stage 3.5)
2. Complete `apply_hs4_alignment_v1.0.0.py` (Stage 5)
3. Test full pipeline on 2023 data
4. Validate 100% classification achieved
5. Document analytics/targeting phase (future)
