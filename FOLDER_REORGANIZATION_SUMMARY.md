# Panjiva Project Folder Reorganization Summary

**Date**: 2026-01-13
**Action**: Complete folder structure cleanup and reorganization

## Overview

Reorganized the entire project manifest folder structure to eliminate redundancy, archive old versions, and create a clean hierarchy with only final work products in active folders.

---

## Final Folder Structure

### 📁 00_raw_data
**Purpose**: All raw, unprocessed source data files

**Contents**:
```
00_raw_data/
├── 00_01_panjiva_imports_raw/          # 170 original Panjiva import files (ZIPs + CSVs)
├── 00_02_panjiva_exports_raw/          # Panjiva export data
├── 00_03_usace_entrance_clearance_raw/ # USACE clearance data
├── 00_04_fgis_raw/                     # FGIS grain inspection data
├── 00_05_all_raw_archive/              # Consolidated master archive
└── 00_99_user_notes_raw_data/          # Miscellaneous raw data collections
```

**Status**: ✅ Clean - Properly organized numbered structure

---

### 📁 01_step_one
**Purpose**: Preprocessed data files ready for classification

**Contents**:
```
01_step_one/
└── 01_01_panjiva_imports_step_one/
    ├── panjiva_imports_2023_20260112_STAGE00_v20260112_2052.csv  (352 MB)
    ├── panjiva_imports_2024_20260112_STAGE00_v20260112_2052.csv  (347 MB)
    └── panjiva_imports_2025_20260112_STAGE00_v20260112_2052.csv  (308 MB)
```

**Changes**:
- ❌ Removed 45 old version files (8 GB freed)
- ✅ Kept only the 3 final STAGE00 files (one per year)

---

### 📁 01.01_dictionary
**Purpose**: All reference dictionaries and lookup tables

**Contents**:

**Cargo Classification**:
- `01_cargo_dictionary.csv` (401 KB) - Original cargo dictionary
- `01_cargo_dictionary_harmonized_v20260111_2313.csv` (184 KB) - **Latest harmonized version**
- `cargo_dictionary.csv` (243 KB) - Legacy cargo dictionary
- `pigiron_dictionary.csv` (22 KB)
- `pulp_paper_dictionary.csv` (151 KB)
- `slabs_dictionary.csv` (4 KB)
- `steel_coil_dictionary (2).csv` (82 KB)
- `wind_dictionary.csv` (16 KB)

**HS Code Lookups**:
- `hs_code_lookup.json` (7.6 MB) - Complete HS code hierarchy
- `hs2_lookup.csv` (3 KB)
- `hs4_lookup.csv` (52 KB)
- `hs6_lookup.csv` (524 KB)

**Port & Location**:
- `01_us_port_dictionary.csv` (68 KB) - US port codes
- `01.05.ACE_Port_Codes_Merged_v20260111_1527.csv` (67 KB)
- `01.06.sked_d_usports.csv` (11 KB)
- `01.07.sked_d_e.csv` (63 KB)
- `sked_c_countries.csv` (5 KB)
- `sked_d_usports.csv` (11 KB)

**Trade Codes**:
- `sked_b_export_codes.csv` (1.6 MB)
- `sked_b_import_codes.csv` (3.5 MB)
- `atp_export_codes.csv` (47 KB)
- `atp_import_codes.csv` (65 KB)
- `enduse_export_codes.csv` (5 KB)
- `enduse_import_codes.csv` (4 KB)
- `sic_export_codes.csv` (21 KB)
- `sic_import_codes.csv` (20 KB)
- `sitc_codes.csv` (244 KB)
- `naics_codes.csv` (242 bytes)

**Reference Text Files**:
- `country.txt`, `country2.txt`, `country3.txt`, `country4.txt`
- `dist.txt`, `dist2.txt`, `dist3.txt`
- `esic.txt`, `isic.txt`
- `exeumstr.txt`, `imeumstr.txt`
- `expatp22.txt`, `impatp22.txt`
- `naicsmst.txt`, `sitcmstr.txt`
- `sked_b_exp_code.txt`, `sked_b_exp_stru.txt`
- `sked_b_imp_code.txt`, `sked_b_imp_stru.txt`

**Carrier & Vessel**:
- `01_carrier_scac_cargo.csv` (43 KB) - Carrier SCAC codes
- `01_ships_register.csv` (5.4 MB) - Ship registry with IMO numbers

**Party Harmonization**:
- `parties_harmonization_master.json` (25 KB)
- `parties_harmonization_rules.md` (17 KB)

**Industry Standards**:
- `aisi_steel_product_groups.csv` (46 KB)
- `aisi2022hts.xlsx` (32 KB)
- `aisi2022hts201.xlsx` (21 KB)
- `agency_fee_schedule.csv` (2.4 KB)

**USACE References**:
- `Schedule K 4th Quarter 2024.csv` (217 KB)
- `Schedule K 4th Quarter 2024.xlsx` (175 KB)
- `usace_sked_k_geotrade.pdf` (414 KB)
- `usace_sked_k_geotrade.xls` (355 KB)
- `usace_waterway_code_wcus_cross.txt` (107 KB)
- `usace_waterwaycode_wcus_cross.xlsx` (95 KB)

**ACE References**:
- `ACE Appendix E Schedule D 4_17_2024 (1)_508c_0.pdf` (551 KB)
- `ACE Appendix E Schedule D January 2020 (1).xlsx` (40 KB)

**Changes**:
- ❌ Removed 11 old dictionary versions
- ✅ Consolidated all dictionaries from user_notes
- ✅ Added specialized cargo dictionaries
- ✅ Added all reference lookup tables

---

### 📁 build_documentation
**Purpose**: Final documentation, dashboards, and classified output data

**Contents**:

**Interactive Dashboards**:
- `INDEX.html` (11 KB) - **Main landing page**
- `classification_pipeline_dashboard.html` (17 KB) - Interactive charts & metrics
- `classification_technical_dataflow.html` (19 KB) - Technical architecture diagrams

**Documentation**:
- `PIPELINE_MASTER_PLAN_UPDATED.md` (20 KB) - **Complete system documentation**
- `classification_phase10_final_summary.md` (15 KB) - Phase 10 results
- `classification_3year_comparison.md` (16 KB) - 3-year analysis
- `COLUMN_MAPPING_DICTIONARY.md` (18 KB) - Column transformation reference

**Classified Data Folders**:
```
classification_full_2023/
├── panjiva_2023_classified_phase10_20260113_1219.csv  (454,266 records)
└── pivot_summary_2023_phase10_20260113_1219.csv       (95 commodity groups)

classification_full_2024/
├── panjiva_2024_classified_phase10_20260113_1223.csv  (449,233 records)
└── pivot_summary_2024_phase10_20260113_1223.csv       (41 commodity groups)

classification_full_2025/
├── panjiva_2025_classified_phase10_20260113_1226.csv  (398,747 records)
└── pivot_summary_2025_phase10_20260113_1226.csv       (41 commodity groups)
```

**Changes**:
- ❌ Removed: analysis reports, old dashboards, correction summaries, stage00 files
- ❌ Archived: checkpoints (4.7 GB), classification_tests (180 MB), logs (649 KB)
- ❌ Removed: empty data_quality folder
- ✅ Kept only final dashboards and documentation

---

### 📁 user_notes
**Purpose**: User reference materials and temporary workspace

**Status**: 🗑️ **Emptied** - All contents redistributed

**Changes**:
- ✅ Moved all dictionaries → `01.01_dictionary/`
- ✅ Moved raw_data subfolder → `00_raw_data/00_99_user_notes_raw_data/`
- ✅ Archived 60+ old files (cargo classification versions, HS mappings, prompts, analysis files)

---

### 📁 _archive
**Purpose**: Old versions and intermediate work products

**Structure**:
```
_archive/
├── user_notes_old/             # 60+ files, ~62 MB
├── step_one_old_versions/      # 45 files, ~8 GB
├── dictionary_old_versions/    # 11 files, ~11 MB
└── build_documentation_old/    # Multiple folders + files, ~5 GB
```

**Archived Items**:
- 45 old Panjiva data versions (2023-2025 processing iterations)
- 11 cargo dictionary versions
- Stage00 checkpoints (4.7 GB)
- Classification test runs (180 MB)
- Pipeline logs (649 KB)
- Analysis reports and synthesis documents
- Old dashboards and execution logs
- HS code mapping files
- Cargo classification iterations
- Prompts and temporary work files

---

## Summary Statistics

### Space Recovered
- **01_step_one**: ~8 GB freed (45 files → 3 files)
- **01.01_dictionary**: ~11 MB freed (11 old versions removed)
- **build_documentation**: ~5 GB freed (archived checkpoints, tests, logs)
- **user_notes**: ~62 MB redistributed

**Total Archived**: ~13 GB

### File Count Reduction
- **Before**: 200+ files across main folders
- **After**: ~60 essential files in active folders
- **Archived**: 140+ old versions and intermediate files

---

## Key Improvements

### 1. Clear Hierarchy
- Each folder has single, well-defined purpose
- Numbered structure for processing stages (00, 01, 01.01)
- Final products separated from work-in-progress

### 2. Dictionary Consolidation
- All reference dictionaries in one location (`01.01_dictionary/`)
- Eliminated duplicates (carrier_dictionary, cargo_dictionary)
- Added specialized cargo dictionaries from user_notes
- Added all trade code lookups

### 3. Version Control
- Only latest STAGE00 files in active folders
- All old versions preserved in `_archive/`
- Easy to restore if needed

### 4. Documentation Clarity
- `build_documentation/` contains only final deliverables
- Interactive dashboards accessible from INDEX.html
- Classified data organized by year in subfolders

### 5. Eliminated Redundancy
- Removed duplicate ships_master file
- Consolidated cargo classification files
- Removed intermediate HS code mapping iterations

---

## Quick Reference

### Start Here
📄 **Main Landing Page**: `G:\My Drive\LLM\project_manifest\build_documentation\INDEX.html`

### Key Data Files
📊 **2023 Classified**: `build_documentation/classification_full_2023/panjiva_2023_classified_phase10_20260113_1219.csv`
📊 **2024 Classified**: `build_documentation/classification_full_2024/panjiva_2024_classified_phase10_20260113_1223.csv`
📊 **2025 Classified**: `build_documentation/classification_full_2025/panjiva_2025_classified_phase10_20260113_1226.csv`

### Key Dictionaries
📚 **Cargo**: `01.01_dictionary/01_cargo_dictionary_harmonized_v20260111_2313.csv`
📚 **HS Codes**: `01.01_dictionary/hs_code_lookup.json`
📚 **Ports**: `01.01_dictionary/01_us_port_dictionary.csv`
📚 **Ships**: `01.01_dictionary/01_ships_register.csv`

### Documentation
📖 **Master Plan**: `build_documentation/PIPELINE_MASTER_PLAN_UPDATED.md`
📖 **Phase 10 Summary**: `build_documentation/classification_phase10_final_summary.md`
📖 **3-Year Comparison**: `build_documentation/classification_3year_comparison.md`

---

## Restore Instructions

If you need to restore archived files:

1. **Old data versions**: `_archive/step_one_old_versions/`
2. **Old dictionaries**: `_archive/dictionary_old_versions/`
3. **Checkpoints**: `_archive/build_documentation_old/checkpoints/`
4. **Test runs**: `_archive/build_documentation_old/classification_tests/`
5. **Logs**: `_archive/build_documentation_old/logs/`
6. **User notes**: `_archive/user_notes_old/`

Simply copy files back to their original location if needed.

---

## Next Steps

### Immediate
- ✅ All active folders contain only essential, final work products
- ✅ All dictionaries consolidated in single location
- ✅ All old versions safely archived

### Future Enhancements
- Consider compressing `_archive/` folder to save space
- Periodically review archive for files that can be permanently deleted
- Document any new dictionary additions to maintain organization

---

**Reorganization Status**: ✅ **COMPLETE**

The project manifest now has a clean, logical structure optimized for ongoing work and future reference.
