# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

This is a **maritime cargo classification system** for U.S. import data. It processes 1.3M+ Panjiva shipment records (2023-2025) through a multi-phase classification pipeline that assigns cargo to a 4-level taxonomy using rule-based pattern matching.

**Key Achievement**: 786,674 records classified (62.9%) capturing 1.47 billion tons (71.3% of total tonnage).

**Working Directory**: `G:\My Drive\LLM\project_manifest\` (Google Drive File Stream on Windows)

---

## Python Environment

**Requirements**:
- Python 3.8 or higher
- Required packages: `pandas`, `numpy`

**Setup**:
```bash
pip install pandas numpy
```

**Note**: All scripts use standard pandas/numpy operations. No special ML libraries required for classification.

---

## Core Architecture

### Data Pipeline Flow

```
Raw Panjiva Data (170 files)
    ↓
STAGE 00: Preprocessing
    - Deduplication
    - Column standardization
    - HS code extraction
    - Year splitting (2023/2024/2025)
    ↓
STAGE 02: Classification (Phases 1-10)
    - Phase 1: Filters (SHIP_SPARES, FROB)
    - Phase 2-3: Carrier locks (RoRo, Reefer, Chemical Tankers)
    - Phase 4-7: HS code + keyword matching
    - Phase 8-9: Combinatorial rules & refinements
    - Phase 10: High-value specific grades
    ↓
Output: Classified CSVs + Pivot Summaries
```

### Dictionary-Driven Classification

**Critical Concept**: This is NOT a code-driven system. All classification rules live in CSV dictionaries, not Python code. The classification scripts are generic engines that execute rules from the dictionary.

**Main Dictionary**: `03_DICTIONARIES/03.01_cargo_classification/cargo_classification_dictionary_v*.csv`

**Dictionary Schema** (38 columns):
- **Control**: `Rule_ID`, `Phase`, `Tier`, `Active`, `Lock_Group`, `Lock_Commodity`, `Lock_Cargo`, `Lock_Cargo_Detail`
- **Matching Criteria**: `Carrier_SCAC`, `Vessel_Type`, `HS2/HS4/HS6`, `Keywords`, `Exclude_Keywords`, `Min_Tons`, `Max_Tons`, `Exclude_Groups`
- **Classification Output**: `Group`, `Commodity`, `Cargo`, `Cargo_Detail`
- **Metadata**: `Note`, `Accuracy_Est`, `Tonnage_Impact`, `Date_Added`, `Last_Modified`

⚠️ **Column Name Note**: Dictionary uses `Cargo_Detail` (underscore), but some scripts output `Cargo Detail` (space). Be aware of this inconsistency when reading/writing data.

### 5-Tier Rule Hierarchy

Classification rules execute in order of priority:

| Tier | Type | Accuracy | Override Behavior |
|------|------|----------|-------------------|
| **1** | Carrier Locks | 100% | NEVER override (WALLENIUS → RoRo) |
| **2** | Package Types | 98% | Can refine (LBK → Liquid Bulk → Petroleum → Crude Oil) |
| **3** | HS Code + Keywords | 85-95% | Standard matching |
| **4** | Tonnage Overrides | 80-90% | Correct misclassifications based on weight |
| **5** | User Refinements | 75-90% | Edge cases and specific grades |

### Lock Level System

**Critical for understanding classification behavior**:

The dictionary uses 4 lock columns to control which taxonomy levels can be overridden by later phases:

- `Lock_Group`: TRUE → Group cannot be changed by subsequent rules
- `Lock_Commodity`: TRUE → Group + Commodity locked
- `Lock_Cargo`: TRUE → Group + Commodity + Cargo locked
- `Lock_Cargo_Detail`: TRUE → All 4 levels locked (final classification)

**Pattern Example**:
```
Phase 2 (Carrier): Lock_Group=TRUE, others=FALSE
  → Sets "Ro/Ro" group, allows later phases to refine to specific cargo types

Phase 10 (Crude Variants): All locks=TRUE
  → Sets "Liquid Bulk → Petroleum → Crude Oil → Basrah Heavy" permanently
```

---

## File Organization

### ⚠️ Folder Migration Status - READ THIS FIRST

The repository contains **BOTH old and new folder structures** as a migration is in progress. Many scripts still reference old paths.

**Old Structure (currently active - scripts use these)**:
- `00_raw_data/` - Raw data files
- `01_step_one/` - Preprocessed data (contains the actual year files)
- `01.01_dictionary/` - Reference dictionaries (actively used)
- `build_documentation/` - Output files

**New Structure (documented, being migrated to)**:
- `00_STAGE00_RAW_DATA/` - Raw data files (new location)
- `01_STAGE01_PREPROCESSING/` - Preprocessed data (new location)
- `03_DICTIONARIES/` - Reference dictionaries (new location)
- Other numbered STAGE folders

**Critical for Claude Code**: When a script path doesn't work, try the alternate naming convention. Check both `01_step_one/` and `01_STAGE01_PREPROCESSING/` for data files. Check both `01.01_dictionary/` and `03_DICTIONARIES/` for reference files.

See `FOLDER_REORGANIZATION_SUMMARY.md` for complete migration details.

### Directory Structure (Target State)

```
G:\My Drive\LLM\project_manifest\
├── 00_STAGE00_RAW_DATA\          # Raw source files (170 Panjiva files)
├── 01_STAGE01_PREPROCESSING\     # Year-split preprocessed files
├── 02_STAGE02_CLASSIFICATION\    # Phase outputs and checkpoints
├── 03_DICTIONARIES\              # All reference dictionaries
│   ├── 03.01_cargo_classification\  # Main classification dictionary
│   ├── 03.02_hs_codes\              # HS code hierarchies
│   ├── 03.03_ports\                 # Port dictionaries
│   └── 03.04_ships\                 # Ship registry, carrier codes
├── 04_SCRIPTS\                   # Classification scripts (development)
├── 05_DOCUMENTATION\             # Master plans, guides, dashboards
├── 06_CHECKPOINTS\               # Processing checkpoints (.parquet)
├── build_documentation\          # Final classified outputs
└── [Old folders: 00_raw_data, 01_step_one, 01.01_dictionary - still active]
```

### Naming Conventions

**Dictionary Files**:
```
cargo_classification_dictionary_v{MAJOR}.{MINOR}.{PATCH}_{YYYYMMDD_HHMM}.csv
```

**Data Files**:
```
panjiva_{year}_classified_v{VERSION}_{YYYYMMDD_HHMM}.csv
pivot_summary_{year}_v{VERSION}_{YYYYMMDD_HHMM}.csv
```

**Scripts**:
```
classify_15k_sample_v{VERSION}.py
stage{NN}_{purpose}_v{VERSION}.py
```

**Versioning**:
- **MAJOR** (3.0.0): Breaking changes (schema changes, incompatible logic)
- **MINOR** (3.1.0): New features, backwards compatible (new rules/phases)
- **PATCH** (3.1.1): Bug fixes, corrections (typos, rule errors)

---

## Common Development Tasks

### Running Classification

**Test on 15K sample** (recommended for development):
```bash
cd "G:\My Drive\LLM\project_manifest\04_SCRIPTS"

# Find the latest version
dir classify_15k_sample_v*.py

# Run the latest version (e.g., v3.4.0 or newer)
python classify_15k_sample_v3.4.0.py
```
**Output**: `build_documentation/sample_test_15k/sample_15k_classified_v*.csv`
**Runtime**: ~1-2 minutes

**Full year classification** (use for production):

⚠️ **Note**: Production scripts are located in `C:\Users\wsd3\` (separate from development scripts in `04_SCRIPTS\`). These are the mature, optimized versions used for full data processing.

```bash
cd C:\Users\wsd3

# Run full year classification
python classification_phase10_high_value.py 2024
```
**Output**: `build_documentation/classification_full_2024/panjiva_2024_classified_*.csv`
**Runtime**: ~40 minutes for full year

### Editing Classification Rules

**NEVER edit rules in Python code**. Always edit the CSV dictionary.

**Finding the latest dictionary**:
```bash
# Check both old and new locations
dir "G:\My Drive\LLM\project_manifest\03_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v*.csv" /O-D
dir "G:\My Drive\LLM\project_manifest\01.01_dictionary\cargo_classification_dictionary_v*.csv" /O-D

# The highest version number with most recent timestamp is the latest
```

**Workflow**:
1. Open latest dictionary (e.g., `cargo_classification_dictionary_v3.4.0_20260114_0400.csv`)
2. Add/modify rules following the schema (see "Dictionary Schema" section)
3. Save with incremented version:
   - New rules: `v3.4.0` → `v3.5.0` (minor bump)
   - Bug fixes: `v3.4.0` → `v3.4.1` (patch bump)
   - Schema changes: `v3.4.0` → `v4.0.0` (major bump)
4. Update script's `DICTIONARY` path variable to point to new version
5. Test on 15K sample before running full classification

**Example: Adding a new crude oil variant**:
```csv
Rule_ID: CRUDE-LIZA-CRUDE
Phase: 10
Tier: 5
Active: TRUE
Lock_Group: TRUE
Lock_Commodity: TRUE
Lock_Cargo: TRUE
Lock_Cargo_Detail: TRUE
Vessel_Type: Tanker
HS2: 27
HS4: 2709
Keywords: LIZA CRUDE
Group: Liquid Bulk
Commodity: Petroleum
Cargo: Crude Oil
Cargo_Detail: Crude Oil - Liza Crude
Note: Guyanese crude oil grade
Accuracy_Est: 99%
Tonnage_Impact: Medium
```

### Analyzing Classification Results

**Quick tonnage report** (check tonnage distribution by commodity):
```bash
cd "G:\My Drive\LLM\project_manifest\04_SCRIPTS"

# Use latest version
python quick_tonnage_report_v*.py  # Find latest with: dir quick_tonnage_report_v*.py
```

**Check specific phase impact** (see what a phase classified):
```bash
python analyze_phase5_v*.py
```

**Identify unclassified records** (analyze TBN remaining):
```bash
python analyze_tbn_remaining_v*.py
```

**Compare versions** (tonnage differences between dictionary versions):
```bash
python compare_v31_v32_tonnage.py  # Adjust version numbers as needed
```

### Checking Dictionary Integrity

**Verify dictionary structure**:
```bash
python verify_v3_dictionary.py
```

**Check phase 1 lock conflicts**:
```bash
python check_phase1_locks.py
```

---

## Classification Script Structure

All classification scripts follow the same pattern:

### Core Functions

**`map_vessel_type(detailed_type)`**: Maps detailed vessel types to simplified categories (Bulk Carrier, Tanker, RoRo, etc.)

**`add_vessel_types(df)`**: Enriches data with vessel type from ship registry

**`load_dictionary()`**: Loads and filters active rules from CSV dictionary

**`check_match(record, rule)`**: Tests if a record matches rule criteria (carrier, vessel type, HS codes, keywords, tonnage)

**`can_apply_rule(record, rule)`**: Checks lock levels and exclusions to determine if rule can be applied

**`apply_rule(record, rule)`**: Applies classification taxonomy and sets lock flags

**`classify_in_phases(df, df_dict)`**: Main orchestrator - iterates through phases 1-10, applying matching rules

### Processing Flow in Scripts

1. Load 15K sample or full year file
2. Add vessel types from ship registry
3. Load dictionary and filter active rules
4. Initialize classification columns (Group, Commodity, Cargo, Cargo_Detail, lock flags)
5. For each phase (1-10):
   - Filter rules for current phase
   - For each record:
     - Check if any rule matches AND can be applied (lock check)
     - Apply first matching rule (priority matters!)
6. Generate statistics and output classified CSV

---

## Key Discoveries & Patterns

### Most Impactful Rules (by tonnage)

1. **LBK Package Rule** (501M tons): Package type "LBK" → Liquid Bulk
2. **Crude Oil Variants** (79M tons): Specific grades (BASRAH, KIRKUK, LIZA, TUPI)
3. **Simplified Salt** (32.9M tons): "SALT" keyword → Salt (no HS code required)

### Common Pitfalls

**Issue**: Rules firing out of order
- **Cause**: Phase/Tier numbering incorrect in dictionary
- **Fix**: Verify Phase column is sequential, Tier reflects priority

**Issue**: Carrier rules not matching
- **Cause**: Carrier column has format "SCAC - Name", need to search for SCAC code
- **Fix**: Use `carrier_scac.upper() in record_carrier` (substring match)

**Issue**: Rules not refining existing classifications
- **Cause**: Lock levels set too aggressively in earlier phases
- **Fix**: Use `Lock_Group=TRUE` only for initial classification, allow later refinement

**Issue**: "TBN" appearing in Commodity/Cargo/Cargo_Detail
- **Cause**: Rules only classifying Group level, leaving others as "To Be Named"
- **Fix**: This is intentional for partial classification; later phases will refine

**Issue**: Dictionary version doesn't match script version
- **Cause**: Dictionary evolves faster than scripts; versions don't need to align
- **Fix**: Script version (e.g., v1.2.0) is about script features. Dictionary version (e.g., v3.4.0) is about rules. They're independent. Just update the `DICTIONARY` path in script to use latest dictionary.

---

## Testing & Validation

### Before Committing Dictionary Changes

1. Run 15K sample classification: `python classify_15k_sample_v*.py` (use latest version)
2. Check tonnage statistics: `python quick_tonnage_report_v*.py` (use latest version)
3. Compare with previous version: `python compare_v*_v*_tonnage.py` (adjust version numbers)
4. Verify no regressions in key commodities (crude oil, grain, steel)
5. Update script to reference new dictionary version in `DICTIONARY` path variable

### Validation Metrics

- **Record Coverage**: % of records classified (target: >60%)
- **Tonnage Coverage**: % of tonnage classified (target: >70%)
- **TBN Remaining**: Tonnage still showing "To Be Named" (minimize)
- **Phase Distribution**: Ensure phases firing as expected

---

## Important Data Paths

⚠️ **Note**: Due to folder migration, check both old and new paths. Scripts may reference either location.

**Preprocessed Annual Files** (check both locations):
```
# Old location (actively used by scripts)
G:\My Drive\LLM\project_manifest\01_step_one\01_01_panjiva_imports_step_one\
  - panjiva_imports_2023_20260112_STAGE00_v20260112_2052.csv (352 MB)
  - panjiva_imports_2024_20260112_STAGE00_v20260112_2052.csv (347 MB)
  - panjiva_imports_2025_20260112_STAGE00_v20260112_2052.csv (308 MB)

# New location (target)
G:\My Drive\LLM\project_manifest\01_STAGE01_PREPROCESSING\01.01_annual_files\
```

**Ship Registry** (for vessel type enrichment, check both):
```
# Old location
G:\My Drive\LLM\project_manifest\01.01_dictionary\01_ships_register.csv

# New location
G:\My Drive\LLM\project_manifest\03_DICTIONARIES\03.04_ships\
```

**Main Classification Dictionary** (check both locations):
```
# Old location (actively used)
G:\My Drive\LLM\project_manifest\01.01_dictionary\
  - cargo_classification_dictionary_v*.csv

# New location (target)
G:\My Drive\LLM\project_manifest\03_DICTIONARIES\03.01_cargo_classification\
  - cargo_classification_dictionary_v3.4.0_20260114_0400.csv (LATEST as of 2026-01-14)
```

**Classified Outputs**:
```
G:\My Drive\LLM\project_manifest\build_documentation\
  - classification_full_2023\
  - classification_full_2024\
  - classification_full_2025\
  - sample_test_15k\  (development testing)
```

---

## Reference Documentation

**Essential Reading**:
- `README.md` - Project overview and results
- `05_DOCUMENTATION/05.01_pipeline_docs/PIPELINE_MASTER_PLAN_UPDATED.md` - Complete system reference
- `05_DOCUMENTATION/05.01_pipeline_docs/NAMING_CONVENTIONS_v1.0.0.md` - Versioning and naming standards
- `05_DOCUMENTATION/05.01_pipeline_docs/RULE_EDITING_GUIDE_v1.0.0.md` - How to edit dictionary rules
- `GIT_SETUP_GUIDE.md` - Version control workflow

**Interactive Dashboards** (open in browser):
- `build_documentation/INDEX.html` - Main landing page
- `build_documentation/classification_pipeline_dashboard.html` - Charts & metrics
- `build_documentation/classification_technical_dataflow.html` - Architecture diagrams

**Analysis Reports**:
- `build_documentation/classification_phase10_final_summary.md` - Latest phase results
- `build_documentation/classification_3year_comparison.md` - Cross-year analysis
- `build_documentation/classification_victory_summary.md` - Success metrics

---

## Git Workflow

**Large files are excluded** via `.gitignore`:
- Raw data files (`00_raw_data/`, `00_STAGE00_RAW_DATA/`)
- Preprocessed CSVs (`01_step_one/`, `01_STAGE01_PREPROCESSING/`)
- Classified outputs (`build_documentation/classification_full_*/`)
- Archive folder (`_archive/`)
- Checkpoints (`*.parquet`, `06_CHECKPOINTS/`)

**What IS tracked**:
- Python scripts (04_SCRIPTS/)
- Dictionaries (03_DICTIONARIES/)
- Documentation (05_DOCUMENTATION/, build_documentation/*.md, *.html)
- README, guides, summaries

**Commit Pattern**:
```bash
git add 03_DICTIONARIES/03.01_cargo_classification/cargo_classification_dictionary_v3.5.0_*.csv
git commit -m "Dictionary v3.5.0: Add 10 new petroleum product rules"
git push
```

---

## Troubleshooting Common Issues

### Path Not Found Errors

**Problem**: Script can't find file at specified path
```
FileNotFoundError: [Errno 2] No such file or directory: 'G:\My Drive\LLM\project_manifest\03_DICTIONARIES\...'
```

**Solutions**:
1. Check alternate folder location (old vs new structure):
   - Try `01.01_dictionary/` instead of `03_DICTIONARIES/`
   - Try `01_step_one/` instead of `01_STAGE01_PREPROCESSING/`
2. Verify Google Drive File Stream is mounted at `G:\`
3. Use `dir` or `ls` to find actual file location
4. Update script's path constants to match actual location

### Dictionary Version Mismatch

**Problem**: Script references old dictionary version that doesn't exist

**Solution**:
```python
# In script, update the DICTIONARY path to latest version
DICTIONARY = Path(r"G:\My Drive\LLM\project_manifest\03_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v3.5.0_20260114_1200.csv")
```

### Ship Registry Not Found

**Problem**: Vessel type enrichment fails

**Solution**: Check both locations:
```bash
# Old location
dir "G:\My Drive\LLM\project_manifest\01.01_dictionary\01_ships_register.csv"

# New location
dir "G:\My Drive\LLM\project_manifest\03_DICTIONARIES\03.04_ships\*ships*.csv"
```

### Classification Results Don't Match Expected

**Problem**: Rules firing out of order or not matching

**Solutions**:
1. Verify `Phase` column is set correctly (1-10)
2. Check `Active` column is `TRUE`
3. Verify lock levels allow refinement (see Lock Level System section)
4. Check `Exclude_Groups` isn't blocking matches
5. Test with 15K sample to isolate issue

### Column Name Errors

**Problem**: KeyError for 'Cargo_Detail' or similar

**Solution**: Some contexts use `Cargo Detail` (with space), others use `Cargo_Detail` (underscore). Check script output column names and adjust references accordingly.

---

## Notes for Future Claude Instances

1. **Folder migration in progress** - check both old (`01_step_one/`, `01.01_dictionary/`) and new (`01_STAGE01_PREPROCESSING/`, `03_DICTIONARIES/`) paths when files not found
2. **Never edit rules in Python code** - always edit the CSV dictionary and increment version
3. **Test on 15K sample first** - takes ~1-2 minutes vs ~40 minutes for full year
4. **Lock levels control refinement** - understand Lock_Group vs Lock_Commodity vs Lock_Cargo vs Lock_Cargo_Detail
5. **Phase order matters** - Phase 2 carrier locks must fire before Phase 10 refinements
6. **Carrier matching is substring** - "SCAC - Name" format requires `SCAC in record_carrier`
7. **TBN is normal** - "To Be Named" indicates partial classification awaiting refinement
8. **Package type is powerful** - "LBK" alone classified 501M tons
9. **Dictionary is authoritative** - script versions lag dictionary versions (dictionary drives everything)
10. **Timestamps in filenames** - helps track execution order and debugging
11. **Large files stay on Google Drive** - never commit CSVs >10 MB to git
12. **Production scripts separate** - mature scripts in `C:\Users\wsd3\`, development in `04_SCRIPTS\`

---

## Current System Status (as of 2026-01-14)

- **Dictionary Version**: v3.4.0 (Fixed vehicle carrier Group classification)
- **Latest Classification Run**: Phase 10 complete for all years
- **Record Coverage**: 786,674 / 1,302,246 (60.4%)
- **Tonnage Coverage**: 1.47B / 2.07B tons (71.3%)
- **Production Status**: Ready for ML training set use

---

**For detailed architecture and rule mechanics, see**:
- `build_documentation/PIPELINE_MASTER_PLAN_UPDATED.md` (comprehensive technical reference)
- `build_documentation/classification_technical_dataflow.html` (visual architecture diagrams)
