# Archive Plan - Redundant Draft Files (2026-01-15)

## Purpose
Clean up repository by moving old development/test files to `_archive/redundant_drafts_20260115/`

## Archive Folder Structure
```
_archive/redundant_drafts_20260115/
├── 04_SCRIPTS/          # Old script versions and dev tools
└── 03_DICTIONARIES/     # Old dictionary versions (v2.x)
```

## Files to Archive

### 04_SCRIPTS/ (49 files)

#### Old Classify Versions (8 files - keep only v3.x)
- `classify_15k_sample_v1.0.0.py`
- `classify_15k_sample_v1.0.1.py`
- `classify_15k_sample_v1.0.2.py`
- `classify_15k_sample_v1.0.3.py`
- `classify_15k_sample_v1.1.0.py`
- `classify_15k_sample_v1.1.1.py`
- `classify_15k_sample_v1.2.0.py`
- `classify_15k_sample_v1.2.1.py`

#### Debug Scripts (5 files)
- `debug_carrier_matching.py`
- `debug_phase2_matching.py`
- `debug_vessel_port_matching.py`
- `debug_port_normalization.py`
- `debug_entrance_clearance_matching_v1.0.0.py`

#### Analysis Scripts (14 files)
- `analyze_what_was_lost.py`
- `analyze_v2.5.2_by_tons.py`
- `analyze_missing_hs4_by_tonnage.py`
- `analyze_tbn_remaining_v3.1.py`
- `analyze_vtype_impact.py`
- `analyze_phase5_v32.py`
- `analyze_tonnage_filter_blocks.py`
- `analyze_tbn_remaining_v3.3.py`
- `analyze_phase1_lock_problem.py`
- `analyze_tbn_remaining_v3.4.py`
- `analyze_chemicals_bulk.py`
- `analyze_v3.6.0_results.py`
- `analyze_clearance_by_region.py`
- `analyze_unmatched_records_v1.0.0.py` (keep - recent analysis)

#### Check Scripts (9 files)
- `check_carrier_rules.py`
- `check_wlwh_classification.py`
- `check_results_v2.py`
- `check_results_FINAL.py`
- `check_phase1_locks.py`
- `check_pipeline_progress.py`
- `check_all_pipelines_progress.py`
- `check_panjiva_structure.py`
- `check_portcall_master.py` (keep - recent utility)

#### Compare Scripts (2 files)
- `compare_v31_v32_tonnage.py`
- `compare_import_export_columns.py`

#### Fix Scripts (8 files)
- `fix_carrier_scac_v1.0.0.py`
- `fix_carrier_rules_scac_only.py`
- `fix_vtype_roro_locks.py`
- `fix_carrier_rules_remove_hs.py`
- `fix_vehicle_carrier_groups.py`
- `fix_phase1_locks_v3.4.0.py`
- `fix_and_convert_hs28-29.py`
- `fix_and_convert_2mil_tons.py`

### 03_DICTIONARIES/03.01_cargo_classification/ (11 files - keep only v3.4.0+)

#### Dictionary v2.x (11 files to archive)
- `cargo_classification_dictionary_v2.0.0_20260113_1430.csv`
- `cargo_classification_dictionary_v2.1.0_20260113_1445.csv`
- `cargo_classification_dictionary_v2.2.0_20260113_1500.csv`
- `cargo_classification_dictionary_v2.2.1_20260113_1530.csv`
- `cargo_classification_dictionary_v2.3.0_20260113_1545.csv`
- `cargo_classification_dictionary_v2.3.1_20260113_2030.csv`
- `cargo_classification_dictionary_v2.3.2_20260113_2300.csv`
- `cargo_classification_dictionary_v2.4.0_20260113_2330.csv`
- `cargo_classification_dictionary_v2.5.0_20260114_0000.csv`
- `cargo_classification_dictionary_v2.5.1_20260114_0030.csv`
- `cargo_classification_dictionary_v2.5.2_20260114_0100.csv`

## Total Files to Archive
- **Scripts**: 46 files
- **Dictionaries**: 11 files
- **Total**: 57 files

## Execution

Run the PowerShell script to perform the move:
```powershell
cd "G:\My Drive\LLM\project_manifest"
powershell -ExecutionPolicy Bypass -File archive_redundant_files.ps1
```

Or manually move using File Explorer to:
```
G:\My Drive\LLM\project_manifest\_archive\redundant_drafts_20260115\
```

## Retention Policy
These files are being archived (not deleted) for:
1. **Historical reference** - understanding development progression
2. **Recovery** - ability to restore if needed
3. **Audit trail** - documenting methodology evolution

Files should be retained for at least 1 year, then reviewed for permanent deletion.
