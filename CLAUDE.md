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

**Main Dictionary**: `01_DICTIONARIES/01.01_cargo_classification/cargo_classification_dictionary_CURRENT_v*.csv`

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

### ✅ Reorganization Completed (2026-01-16)

**Status**: Project reorganization is **COMPLETE**. The repository has been cleaned from 20+ scattered folders into a professional 7-folder hierarchy.

**What Changed**:
- 108 scripts organized by purpose (60+ scripts updated with new paths)
- 12 AUTHORITATIVE data files standardized
- 5 dictionary categories centralized
- Complete historical snapshot preserved in `_archive/2026-01-16_pre_reorganization/`

**Old Structure (archived)**:
- Old folders preserved in `_archive/` for rollback capability
- Exception: `00_raw_data/` and `user_notes/` remain at root per user request

See `REORGANIZATION_COMPLETE.md` for complete details.

### Directory Structure (Current)

```
G:\My Drive\LLM\project_manifest\
├── README.md                     # Project overview
├── CLAUDE.md                     # AI assistant instructions
│
├── 00_DATA/                      # All data files (4 stages)
│   ├── 00.01_RAW/               # Raw sources - DO NOT TOUCH
│   ├── 00.02_PREPROCESSED/      # 6 AUTHORITATIVE files
│   ├── 00.03_MATCHED/           # 4 matched datasets
│   └── 00.04_FINAL/             # 2 Port Call Master files ⭐ FINAL OUTPUTS
│
├── 01_DICTIONARIES/              # All reference data
│   ├── 01.01_cargo_classification/  # CURRENT v3.6.0
│   ├── 01.02_ports/             # 3 port dictionaries
│   ├── 01.03_vessels/           # ships_register + US Flag inventory
│   ├── 01.04_carriers/          # carrier SCAC mappings
│   └── 01.05_hs_codes/          # HS2/4/6 lookups
│
├── 02_SCRIPTS/                   # Organized by purpose (108 scripts)
│   ├── 02.01_preprocessing/     # 10 scripts
│   ├── 02.02_matching/          # 14 scripts
│   ├── 02.03_enrichment/        # 10 scripts
│   ├── 02.04_analysis/          # 26 scripts
│   ├── 02.05_validation/        # 11 scripts
│   ├── 02.06_utilities/         # 35 scripts
│   └── 02.07_production/        # 2 scripts
│
├── 03_DOCUMENTATION/             # Centralized documentation
│   ├── 03.01_guides/            # 2 guides
│   ├── 03.02_technical/         # 5 technical docs
│   ├── 03.03_dashboards/        # 5 HTML dashboards + assets
│   ├── 03.04_summaries/         # 21 summary reports
│   └── 03.05_data_dictionaries/ # 4 CSV column lists
│
├── 04_DEVELOPMENT/               # Development files (hidden from production)
│   ├── 04.01_experiments/       # 3 helper scripts
│   ├── 04.02_tests/             # Test files
│   └── 04.03_deprecated/        # 19 old script versions
│
├── 05_USER_NOTES/                # User working folder
│
├── 00_raw_data/                  # Preserved at root per user request
├── user_notes/                   # Preserved at root (user actively working)
│
└── _archive/                     # Complete historical snapshot
    └── 2026-01-16_pre_reorganization/
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

**IMPORTANT: Always use v2.0.0 scripts and data (as of 2026-01-29)**

**Test on 15K sample** (recommended for development):
```bash
cd "G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.07_production"

# Run 15K validation test
python classify_15k_test_v2.0.0.py
```
**Input**: `00_DATA/00.02_PREPROCESSED/panjiva_imports_2024_AUTHORITATIVE_v2.0.0.csv` (first 15K)
**Output**: `00_DATA/00.03_MATCHED/sample_15k_classified_v2.0.0_validation.csv`
**Runtime**: ~20 minutes
**Expected**: 100% classification, ~55% Phase 1 (carrier locks)

**Full year classification** (use for production):

```bash
cd "G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.07_production"

# Run full year classification (v2.0.0)
python classify_full_year_v2.0.0.py --year 2023
python classify_full_year_v2.0.0.py --year 2024
python classify_full_year_v2.0.0.py --year 2025
```
**Input**: v2.0.0 AUTHORITATIVE files from `00_DATA/00.02_PREPROCESSED/`
**Output**: `00_DATA/00.03_MATCHED/panjiva_imports_{year}_classified_v2.0.0.csv`
**Runtime**:
- 2023: ~20 minutes (15K records)
- 2024: ~9 hours (449K records)
- 2025: ~8 hours (398K records)
**Expected**: 100% classification with vessel enrichment

### Editing Classification Rules

**NEVER edit rules in Python code**. Always edit the CSV dictionary.

**Finding the latest dictionary**:
```bash
# Check the cargo classification dictionary folder
dir "G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.01_cargo_classification\cargo_classification_dictionary_*.csv" /O-D

# Look for the file with "CURRENT" in the name for the active version
# Example: cargo_classification_dictionary_CURRENT_v3.6.0.csv
```

**Workflow**:
1. Open latest dictionary (e.g., `cargo_classification_dictionary_CURRENT_v3.6.0.csv`)
2. Add/modify rules following the schema (see "Dictionary Schema" section)
3. Save with incremented version:
   - New rules: `v3.6.0` → `v3.7.0` (minor bump)
   - Bug fixes: `v3.6.0` → `v3.6.1` (patch bump)
   - Schema changes: `v3.6.0` → `v4.0.0` (major bump)
4. Update the filename to include "CURRENT" prefix and update script's `DICTIONARY` path variable
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
cd "G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.04_analysis"

# Use latest version
python quick_tonnage_report_v*.py  # Find latest with: dir quick_tonnage_report_v*.py
```

**Check specific phase impact** (see what a phase classified):
```bash
cd "G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.04_analysis"
python analyze_phase5_v*.py
```

**Identify unclassified records** (analyze TBN remaining):
```bash
cd "G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.04_analysis"
python analyze_tbn_remaining_v*.py
```

**Compare versions** (tonnage differences between dictionary versions):
```bash
cd "G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.04_analysis"
python compare_v31_v32_tonnage.py  # Adjust version numbers as needed
```

### Checking Dictionary Integrity

**Verify dictionary structure**:
```bash
cd "G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.05_validation"
python verify_v3_dictionary.py
```

**Check phase 1 lock conflicts**:
```bash
cd "G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.05_validation"
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

**Preprocessed Annual Files** (AUTHORITATIVE versions - v2.0.0):
```
G:\My Drive\LLM\project_manifest\00_DATA\00.02_PREPROCESSED\
  - panjiva_imports_2023_AUTHORITATIVE_v2.0.0.csv (13 MB, 59 columns)
  - panjiva_imports_2024_AUTHORITATIVE_v2.0.0.csv (373 MB, 59 columns)
  - panjiva_imports_2025_AUTHORITATIVE_v2.0.0.csv (332 MB, 59 columns)
  - panjiva_exports_2023_AUTHORITATIVE_v1.0.0.csv (76 MB)
  - usace_2023_entrance_AUTHORITATIVE_v1.0.0.csv (29 MB)
  - usace_2023_clearance_AUTHORITATIVE_v1.0.0.csv (29 MB)

Note: v2.0.0 includes vessel enrichment (88-90% match rate) and lock columns
```

**Final Output Files** (Port Call Master):
```
G:\My Drive\LLM\project_manifest\00_DATA\00.04_FINAL\
  - usace_2023_portcall_master_v1.5.0_AUTHORITATIVE.csv (49 MB, 85 columns)
  - usace_2023_portcall_master_v1.5.0_ABRIDGED.csv (35 MB, 46 columns) ⭐
```

**Ship Registry** (for vessel type enrichment):
```
G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.03_vessels\
  - 01_ships_register.csv (5.4 MB)
  - US Flag vessel inventory (9 Excel files)
```

**Main Classification Dictionary**:
```
G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.01_cargo_classification\
  - cargo_classification_dictionary_CURRENT_v3.6.0.csv (LATEST as of 2026-01-16)
```

**Analysis Reports and Summaries**:
```
G:\My Drive\LLM\project_manifest\03_DOCUMENTATION\03.04_summaries\
  - classification_full_2023\
  - classification_full_2024\
  - classification_full_2025\
  - sample_test_15k\ (development testing)
```

---

## Reference Documentation

**Essential Reading**:
- `README.md` - Project overview and results
- `CLASSIFICATION_3YEAR_COMPARISON_v2.0.0.md` - **Complete v2.0.0 results and analysis** ⭐
- `CLASSIFICATION_COMPLETE_20260130.md` - Final classification completion summary
- `V2.0.0_PIPELINE_SUMMARY.md` - v2.0.0 technical details and improvements
- `03_DOCUMENTATION/03.02_technical/ARCHITECTURE.md` - Complete system reference
- `03_DOCUMENTATION/03.01_guides/` - Naming conventions and editing guides
- `REORGANIZATION_COMPLETE.md` - Details of 2026-01-16 reorganization

**Interactive Dashboards** (open in browser):
- `03_DOCUMENTATION/03.03_dashboards/index.html` - Main landing page
- `03_DOCUMENTATION/03.03_dashboards/classification_pipeline_dashboard.html` - Charts & metrics
- `03_DOCUMENTATION/03.03_dashboards/classification_technical_dataflow.html` - Architecture diagrams

**Analysis Reports**:
- `03_DOCUMENTATION/03.04_summaries/classification_phase10_final_summary.md` - Latest phase results
- `03_DOCUMENTATION/03.04_summaries/classification_3year_comparison.md` - Cross-year analysis
- `03_DOCUMENTATION/03.04_summaries/classification_victory_summary.md` - Success metrics

---

## Git Workflow

**Large files are excluded** via `.gitignore`:
- All data files (`00_DATA/`, `00_raw_data/`)
- Archive folder (`_archive/`)
- Deprecated scripts (`04_DEVELOPMENT/04.03_deprecated/`)
- User working files (`user_notes/`, `05_USER_NOTES/`)

**What IS tracked**:
- Python scripts (`02_SCRIPTS/`)
- Dictionaries (`01_DICTIONARIES/`)
- Documentation (`03_DOCUMENTATION/`)
- README, CLAUDE.md, REORGANIZATION_COMPLETE.md

**Commit Pattern**:
```bash
git add 01_DICTIONARIES/01.01_cargo_classification/cargo_classification_dictionary_CURRENT_v3.7.0.csv
git commit -m "Dictionary v3.7.0: Add 10 new petroleum product rules"
git push
```

---

## Troubleshooting Common Issues

### Path Not Found Errors

**Problem**: Script can't find file at specified path
```
FileNotFoundError: [Errno 2] No such file or directory: 'G:\My Drive\LLM\project_manifest\01_DICTIONARIES\...'
```

**Solutions**:
1. Verify Google Drive File Stream is mounted at `G:\`
2. Use current folder structure (reorganization completed 2026-01-16):
   - Data files: `00_DATA/00.02_PREPROCESSED/`
   - Dictionaries: `01_DICTIONARIES/01.0X_[category]/`
   - Scripts: `02_SCRIPTS/02.0X_[purpose]/`
3. Use `dir` to verify actual file location
4. If using an old script from archive, update paths to new structure

### Dictionary Version Mismatch

**Problem**: Script references old dictionary version that doesn't exist

**Solution**:
```python
# In script, update the DICTIONARY path to use CURRENT version
DICTIONARY = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.01_cargo_classification\cargo_classification_dictionary_CURRENT_v3.6.0.csv")
```

### Ship Registry Not Found

**Problem**: Vessel type enrichment fails

**Solution**: Use standardized location:
```bash
dir "G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.03_vessels\01_ships_register.csv"
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

1. **Reorganization completed 2026-01-16** - folder structure is final; old paths archived in `_archive/`
2. **Never edit rules in Python code** - always edit the CSV dictionary and increment version
3. **Use "CURRENT" dictionary** - look for `cargo_classification_dictionary_CURRENT_v*.csv` in `01_DICTIONARIES/01.01_cargo_classification/`
4. **Test on 15K sample first** - takes ~1-2 minutes vs ~40 minutes for full year
5. **Lock levels control refinement** - understand Lock_Group vs Lock_Commodity vs Lock_Cargo vs Lock_Cargo_Detail
6. **Phase order matters** - Phase 2 carrier locks must fire before Phase 10 refinements
7. **Carrier matching is substring** - "SCAC - Name" format requires `SCAC in record_carrier`
8. **TBN is normal** - "To Be Named" indicates partial classification awaiting refinement
9. **Package type is powerful** - "LBK" alone classified 501M tons
10. **Dictionary is authoritative** - script versions lag dictionary versions (dictionary drives everything)
11. **Timestamps in filenames** - helps track execution order and debugging
12. **Large files stay on Google Drive** - never commit CSVs >10 MB to git
13. **Scripts organized by purpose** - 108 scripts in 7 categories under `02_SCRIPTS/`
14. **AUTHORITATIVE data files** - use files with "AUTHORITATIVE" tag in `00_DATA/00.02_PREPROCESSED/` and `00_DATA/00.04_FINAL/`

---

## Current System Status (as of 2026-02-09)

### Classification Pipeline

- **Pipeline Version**: v2.1.0 (PRODUCTION READY - added automatic BOL deduplication)
- **Dictionary Version**: v3.6.0 (668 active rules)
- **Dataset**: 854,870 records, 1.35 billion tons (deduplicated from 1,302,246 raw records)
- **Classification Status**: ✅ **100% COMPLETE**
  - **Classified**: 560,091 records (65.5%), 1.34B tons (99.3%)
  - **Excluded**: 294,779 records (34.5%), 9.0M tons (0.7%)
  - **Unclassified**: 0 records (0%)
- **Port Enrichment**: 100% match rate (all records enriched)
- **Schema**: 69 columns in final output (includes vessel & port data)
- **Production Status**: ✅ v2.1.0 pipeline VALIDATED and PRODUCTION READY
- **Major Fix**: Deduplication removes 447,376 duplicate BOLs (34.4% of raw data)

### Party Harmonization System (NEW - 2026-02-09)

- **Status**: ✅ **TESTED AND READY FOR PRODUCTION**
- **Dictionary**: party_harmonization_master_v1.3.0.csv (163 entities)
- **Coverage**: 11 sectors (Cement, Steel, Petroleum, Chemicals, Aggregates, etc.)
- **Test Results** (January 2024 sample, 25,399 records):
  - Shipper: 5.9% records matched, **32.5% tonnage captured**
  - Consignee: 6.7% records matched, **53.3% tonnage captured**
  - Notify Party: 3.5% records matched, 43.3% tonnage captured
- **Key Insight**: Low record match but HIGH tonnage capture (big players harmonized)
- **Location**: `05_TASKS/05.01_party_harmonization/`
- **Scripts**: 4 harmonization scripts + controlled refinement system
- **Integration**: NOT yet integrated with cargo classification pipeline
- **Projected Coverage**: 68-72% consignee tonnage when deployed on full data

### Controlled Refinement System (NEW - 2026-02-09)

- **Architecture**: Two-tier classification (stable high-level + progressive detail refinement)
- **Task Registry**: Explicit overwrite permissions per refinement task
- **Active Tasks**: 4 construction material tasks (cement, SCM, aggregates, trade lanes)
- **Pending Tasks**: Steel product forms, wind/solar component detection
- **Philosophy**: "No drift" - all changes tracked, audited, controlled
- **Example**: "Cement NOS" → "Cement - Turkish Import (Nuh Cimento)"
- **Location**: `05_TASKS/05.01_party_harmonization/refinement_tasks/`

---

**For detailed architecture and rule mechanics, see**:
- `03_DOCUMENTATION/03.02_technical/ARCHITECTURE.md` (comprehensive technical reference)
- `03_DOCUMENTATION/03.03_dashboards/classification_technical_dataflow.html` (visual architecture diagrams)
- `REORGANIZATION_COMPLETE.md` (folder structure details)
