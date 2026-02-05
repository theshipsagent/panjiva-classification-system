# Panjiva Classification System - Naming Conventions v1.0.0

**Author:** WSD3 / Claude Code
**Date:** 2026-01-13
**Status:** Production Standard

---

## Overview

This document defines the naming conventions and organizational structure for the entire Panjiva Classification System project. All folders, files, dictionaries, and scripts follow these conventions to ensure:

- **Traceability:** Clear version history and timestamps
- **Maintainability:** Easy to find and update components
- **Scalability:** Support for future phases and stages
- **Automation:** Dictionary-driven, not code-driven

---

## Hierarchy Levels

```
STAGE → PHASE → VERSION → TIMESTAMP
 └─ 00, 01, 02...
     └─ 00.01, 00.02... (sub-stages)
          └─ v1.0.0, v2.0.0 (major.minor.patch)
               └─ YYYYMMDD_HHMM
```

### Stage

Top-level pipeline stages (numbered 00-99):

- **STAGE 00:** Raw data acquisition and storage
- **STAGE 01:** Preprocessing (extraction, cleaning, year splits)
- **STAGE 02:** Classification pipeline (Phases 1-10)
- **STAGE 03:** (Future) Analysis and reporting
- **STAGE 04:** (Future) ML pattern discovery

### Phase

Sub-divisions within stages (numbered XX.01-XX.99):

**STAGE 00 Phases:**
- 00.01: Raw imports
- 00.02: Raw exports (future)
- 00.05: Master archive

**STAGE 02 Phases (Classification):**
- Phase 01: Filters (SHIP_SPARES, FROB)
- Phase 02-03: Carrier locks
- Phase 04: HS2 matching
- Phase 05: HS4 matching
- Phase 06: HS6 matching
- Phase 07: Keyword matching
- Phase 08: Combinatorial rules
- Phase 09: Refinements
- Phase 10: High-value specific grades

### Version

Semantic versioning: `vMAJOR.MINOR.PATCH`

- **MAJOR (2.0.0):** Breaking changes
  - Schema changes (new/removed columns)
  - Logic overhaul
  - Incompatible with previous version

- **MINOR (1.1.0):** New features, backwards compatible
  - New rules added
  - New phases added
  - Enhanced functionality

- **PATCH (1.0.1):** Bug fixes, corrections
  - Fix typos
  - Correct rule errors
  - Documentation updates

**Examples:**
```
v1.0.0 → v2.0.0  # Added Phase/Tier columns (breaking change)
v2.0.0 → v2.1.0  # Added 10 new crude oil rules
v2.1.0 → v2.1.1  # Fixed typo in BASRAH keyword
```

### Timestamp

Format: `YYYYMMDD_HHMM`

Examples:
- `20260113_1430` = January 13, 2026 at 2:30 PM
- `20260201_0900` = February 1, 2026 at 9:00 AM

---

## Folder Structure

```
G:\My Drive\LLM\project_manifest\
│
├── 00_STAGE00_RAW_DATA\                    # Raw source data
│   ├── 00.01_panjiva_imports_raw\          # 170 ZIPs + CSVs
│   ├── 00.02_panjiva_exports_raw\          # (Future)
│   └── 00.05_master_archive\               # Consolidated masters
│
├── 01_STAGE01_PREPROCESSING\               # Preprocessing outputs
│   ├── 01.01_annual_files\                 # Year splits (2023-2025)
│   └── 01.02_validation_reports\           # Quality checks
│
├── 02_STAGE02_CLASSIFICATION\              # Classification pipeline
│   ├── 02.01_phase01_filters\              # Phase 1 checkpoints
│   ├── 02.02_phase02_carriers\             # Phase 2-3 checkpoints
│   ├── 02.03_phase04_hs2\                  # Phase 4 checkpoints
│   ├── 02.04_phase05_hs4\                  # Phase 5 checkpoints
│   ├── 02.05_phase06_hs6\                  # Phase 6 checkpoints
│   ├── 02.06_phase07_keywords\             # Phase 7 checkpoints
│   ├── 02.07_phase08_combinatorial\        # Phase 8 checkpoints
│   ├── 02.08_phase09_refinements\          # Phase 9 checkpoints
│   ├── 02.09_phase10_highvalue\            # Phase 10 checkpoints
│   └── 02.10_final_output\                 # Final classified files
│
├── 03_DICTIONARIES\                        # Reference data
│   ├── 03.01_cargo_classification\         # Main classification dict
│   ├── 03.02_hs_codes\                     # HS code hierarchy
│   ├── 03.03_ports\                        # Port dictionaries
│   └── 03.04_ships\                        # Ship registry
│
├── 04_SCRIPTS\                             # Python code
│   ├── stage00_preprocessing_v1.0.0.py
│   ├── stage01_classification_v2.0.0.py
│   └── utilities\                          # Helper functions
│
├── 05_DOCUMENTATION\                       # Documentation
│   ├── 05.01_pipeline_docs\                # Master plans, guides
│   ├── 05.02_dashboards\                   # HTML dashboards
│   ├── 05.03_phase_summaries\              # Phase results
│   └── 05.04_logs\                         # Execution logs
│
├── 06_CHECKPOINTS\                         # Resume capability
│   └── {stage}_checkpoint_{phase}_{timestamp}.parquet
│
└── _ARCHIVE\                               # Old versions
    ├── user_notes\
    └── old_archive\
```

---

## File Naming Patterns

### 1. Dictionaries

```
{name}_dictionary_v{MAJOR}.{MINOR}.{PATCH}_{YYYYMMDD_HHMM}.csv
```

**Examples:**
```
cargo_classification_dictionary_v2.0.0_20260113_1430.csv
us_port_dictionary_v1.0.0_20260101_0900.csv
hs_codes_hierarchy_v1.2.0_20260110_1500.csv
ships_register_v1.0.1_20260105_1000.csv
```

**Schema Versions:**
- v1.x.x: Original schema (pre-Phase/Tier columns)
- v2.x.x: Current schema with Phase, Tier, control columns

### 2. Data Files

```
{source}_{year}_classified_v{VERSION}_{YYYYMMDD_HHMM}.csv
```

**Examples:**
```
panjiva_imports_master_v1.0.0_20260113_1430.csv          # Consolidated master
panjiva_imports_2023_v1.0.0_20260113_1430.csv            # Preprocessing output
panjiva_2023_classified_v1.0.0_20260113_1545.csv         # Classification output
pivot_summary_all_years_v1.0.0_20260113_1600.csv        # Analytics
```

### 3. Scripts

```
stage{NN}_{purpose}_v{VERSION}.py
```

**Examples:**
```
stage00_preprocessing_v1.0.0.py
stage01_classification_v2.0.0.py
transform_dictionary_to_v2.py
reorganize_folders_v1.0.0.py
```

**Utilities:**
```
utilities/dict_loader_v1.0.0.py
utilities/validation_v1.0.0.py
utilities/stamp_v1.0.0.py
```

### 4. Documentation

```
{name}_v{VERSION}.{ext}
```

**Examples:**
```
PIPELINE_MASTER_PLAN_v2.0.0.md
NAMING_CONVENTIONS_v1.0.0.md
classification_pipeline_dashboard_v1.0.0.html
classification_technical_dataflow_v1.0.0.html
classification_phase10_final_summary_v1.0.0.md
```

### 5. Logs

```
{stage_name}_log_{YYYYMMDD_HHMM}.{ext}
```

**Examples:**
```
preprocessing_log_20260113_1430.txt
classification_log_20260113_1545.txt
validation_report_20260113_1430.json
row_count_audit_20260113_1430.csv
```

### 6. Checkpoints

```
{stage_name}_checkpoint_{phase}_{YYYYMMDD_HHMM}.parquet
```

**Examples:**
```
stage00_checkpoint_03_csv_loading_20260113_1430.parquet
stage01_checkpoint_phase04_hs2_20260113_1545.parquet
stage01_checkpoint_phase10_highvalue_20260113_1600.parquet
```

---

## Dictionary Schema Reference

**File:** `03.01_cargo_classification/cargo_classification_dictionary_v2.0.0_20260113_1430.csv`

### Column Groups

**Control Columns:**
- `Rule_ID` - Unique identifier (RULE-0001-CARGO-NAME)
- `Phase` - Execution phase (1-10)
- `Tier` - Priority tier (1-5)
- `Active` - Enable/disable (TRUE/FALSE)
- `Lock_Classification` - Never override (TRUE for carriers)
- `Override_HS` - Can override HS classification (TRUE/FALSE)

**Matching Criteria:**
- `Carrier_Name` - Exact carrier match
- `Package_Type` - LBK, BLK, DBK, etc.
- `HS2`, `HS4`, `HS6` - HS code levels
- `Keywords` - Semicolon-separated terms
- `Exclude_Keywords` - Exclusion terms
- `Min_Tons`, `Max_Tons` - Tonnage thresholds
- `Port_Filter`, `Country_Filter` - Geographic filters

**Classification Output:**
- `Group` - Level 1 (Dry Bulk, Liquid Bulk, etc.)
- `Commodity` - Level 2 (Metals & Minerals, Petroleum, etc.)
- `Cargo` - Level 3 (Iron Products, Crude Oil, etc.)
- `Cargo_Detail` - Level 4 (Iron Ore, Basrah Heavy, etc.)
- `Filter` - Special handling (SHIP_SPARES, FROB, EXCLUDE)

**Metadata:**
- `Note` - Documentation
- `Accuracy_Est` - Estimated accuracy (100%, 98%, etc.)
- `Tonnage_Impact` - Expected impact (Very High, High, etc.)
- `Date_Added`, `Last_Modified` - Timestamps

---

## Phase-Tier Matrix

| Phase | Tier | Description | Example Rules | Accuracy | Override |
|-------|------|-------------|---------------|----------|----------|
| **1** | - | Filters | SHIP_SPARES, FROB | 100% | No |
| **2-3** | 1 | Carrier Locks | WALLENIUS → RoRo | 100% | Never |
| **3** | 2 | Package Types | LBK → Liquid Bulk | 98% | Yes |
| **4** | 3 | HS2 + Keywords | HS2 26 + "iron" | 90% | No |
| **5** | 3 | HS4 + Keywords | HS4 2601 + "ore" | 90% | No |
| **6** | 3 | HS6 + Keywords | HS6 260111 + details | 90% | No |
| **7** | 3 | Keyword-only | "limestone", "salt" | 85% | No |
| **8** | 4 | Combinatorial | HS + tonnage threshold | 80% | Yes |
| **9** | 4 | Refinements | Edge cases | 80% | Yes |
| **10** | 5 | Specific Grades | BASRAH HEAVY | 95% | Yes |

---

## Best Practices

### 1. Version Incrementing

**When to increment MAJOR:**
- Adding/removing dictionary columns
- Changing schema structure
- Breaking backward compatibility

**When to increment MINOR:**
- Adding new rules
- Adding new phases
- New features (backward compatible)

**When to increment PATCH:**
- Fixing typos
- Correcting errors
- Documentation updates

### 2. Timestamps

- Always use 24-hour format
- Use local time (document timezone if distributing)
- Include in filename for traceability

### 3. Folder Organization

- Keep phases separate for debugging
- Use numbered prefixes for sort order
- Archive old versions, don't delete

### 4. Dictionary Edits

1. Open current version
2. Make changes
3. Increment version appropriately
4. Add timestamp to filename
5. Update `Last_Modified` column
6. Test classification with new version
7. Archive old version

### 5. Git Commits

When committing dictionary changes:
```bash
git add 03_DICTIONARIES/03.01_cargo_classification/cargo_classification_dictionary_v2.1.0_*.csv
git commit -m "Dictionary v2.1.0: Add 15 crude oil variants for Phase 10"
git push
```

---

## Quick Reference

### Current Versions (as of 2026-01-13)

| Component | Version | Location |
|-----------|---------|----------|
| Cargo Dictionary | v2.0.0 | 03_DICTIONARIES/03.01_cargo_classification/ |
| Classification Script | v2.0.0 | 04_SCRIPTS/stage01_classification_v2.0.0.py |
| Preprocessing Script | v1.0.0 | 04_SCRIPTS/stage00_preprocessing_v1.0.0.py |
| Pipeline Docs | v2.0.0 | 05_DOCUMENTATION/05.01_pipeline_docs/ |
| Dashboards | v1.0.0 | 05_DOCUMENTATION/05.02_dashboards/ |

### File Suffixes Quick Guide

```
.csv    - Data files, dictionaries
.py     - Python scripts
.md     - Markdown documentation
.html   - Interactive dashboards
.json   - Structured validation reports
.txt    - Plain text logs
.parquet - Binary checkpoints (fast resume)
```

---

## Migration from Old Structure

Old → New mappings:

```
00_raw_data/                → 00_STAGE00_RAW_DATA/
01_step_one/                → 01_STAGE01_PREPROCESSING/
build_documentation/        → 05_DOCUMENTATION/
01.01_dictionary/           → 03_DICTIONARIES/
user_notes/                 → _ARCHIVE/user_notes/
```

---

## Future Enhancements

Planned additions to naming convention:

1. **Stage 03:** Analysis and reporting
2. **Stage 04:** ML pattern discovery
3. **Carrier dictionary:** Separate from cargo (v1.0.0)
4. **Port enrichment:** Geo-coordinates, facilities
5. **Vessel tracking:** Historical voyages integration

---

**End of Naming Conventions v1.0.0**

*For questions or clarifications, see PIPELINE_MASTER_PLAN_v2.0.0.md*
