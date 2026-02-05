# Project Reorganization Plan
**Date:** 2026-01-16
**Status:** PROPOSED - NEEDS REVIEW BEFORE EXECUTION

---

## Problem Statement

The project has accumulated multiple versions of the same files with inconsistent naming:
- Duplicate files with timestamps (v20260115_1242, v20260115_1245, v20260115_1246)
- Inconsistent suffixes (_FILTERED, _PORTCALL, _PREPROCESSED)
- Files scattered across old and new folder structures
- No clear "authoritative" vs "working" vs "archive" designation

**Result:** Confusion about which file is the source of truth.

---

## Proposed File Structure

### ✅ KEEP - Authoritative Source Files

#### 01_STAGE01_PREPROCESSING/01.01_AUTHORITATIVE/ (NEW FOLDER)
```
panjiva_imports_2023_AUTHORITATIVE_v1.0.0.csv
  └─ Source: 01_step_one/01_01_panjiva_imports_step_one/panjiva_imports_2023_20260112_STAGE00_v20260112_2052.csv
  └─ Size: 351.6 MB
  └─ Description: Raw imports data, preprocessed and deduplicated
  └─ Columns: All original Panjiva columns + standardized fields

panjiva_exports_2023_AUTHORITATIVE_v1.0.0.csv
  └─ Source: 01_step_one/01_02_panjiva_exports_step_one/[NEED TO FIND]
  └─ Size: TBD
  └─ Description: Raw exports data, preprocessed and deduplicated

usace_2023_entrance_AUTHORITATIVE_v1.0.0.csv
  └─ Source: 02_STAGE02_CLASSIFICATION/usace_2023_inbound_entrance_transformed_v2.2.0.csv
  └─ Size: 28.1 MB
  └─ Description: USACE entrance records, transformed with vessel registry and port stats

usace_2023_clearance_AUTHORITATIVE_v1.0.0.csv
  └─ Source: 02_STAGE02_CLASSIFICATION/usace_2023_outbound_clearance_transformed_v2.2.0.csv
  └─ Size: 28.3 MB
  └─ Description: USACE clearance records, transformed with vessel registry and port stats
```

#### 02_STAGE02_CLASSIFICATION/02.01_PANJIVA_MATCHED/ (NEW FOLDER)
```
panjiva_imports_2023_with_portcall_AUTHORITATIVE_v1.0.0.csv
  └─ Source: 01_STAGE01_PREPROCESSING/01.01_annual_files/panjiva_imports_2023_PORTCALL_v20260115_1530.csv
  └─ Size: 301.9 MB
  └─ Description: Imports matched to USACE entrance port calls

panjiva_exports_2023_with_portcall_AUTHORITATIVE_v1.0.0.csv
  └─ Source: 01_STAGE01_PREPROCESSING/01.01_annual_files/panjiva_exports_2023_PORTCALL_v20260115_1246.csv (LATEST)
  └─ Size: 2.5 MB
  └─ Description: Exports matched to USACE clearance port calls

usace_2023_entrance_with_panjiva_AUTHORITATIVE_v1.0.0.csv
  └─ Source: 02_STAGE02_CLASSIFICATION/usace_2023_entrance_with_panjiva_match_v1.3.1.csv
  └─ Size: 30.0 MB
  └─ Description: Entrance records with Panjiva import manifest matches

usace_2023_clearance_with_panjiva_AUTHORITATIVE_v1.0.0.csv
  └─ Source: 02_STAGE02_CLASSIFICATION/usace_2023_clearance_with_panjiva_match_v1.0.1.csv
  └─ Size: 29.5 MB
  └─ Description: Clearance records with Panjiva export manifest matches
```

#### 02_STAGE02_CLASSIFICATION/02.02_PORT_CALL_MASTER/ (NEW FOLDER)
```
usace_2023_portcall_master_AUTHORITATIVE_v1.5.0.csv
  └─ Source: 02_STAGE02_CLASSIFICATION/usace_2023_portcall_master_v1.5.0_AUTHORITATIVE.csv
  └─ Size: 48.5 MB
  └─ Columns: 85 (complete technical dataset)
  └─ Description: Complete port call master with all metadata, US Flag registry, grain exports

usace_2023_portcall_master_ABRIDGED_v1.5.0.csv
  └─ Source: 02_STAGE02_CLASSIFICATION/usace_2023_portcall_master_v1.5.0_ABRIDGED.csv
  └─ Size: 34.6 MB
  └─ Columns: 46 (analytics-focused)
  └─ Description: Streamlined port call master for dashboards and analysis
```

---

### 🗄️ ARCHIVE - Old Versions (Move to _archive/)

#### Files to Archive:
```
02_STAGE02_CLASSIFICATION/_archive/port_call_master/
  ├── usace_2023_portcall_master_v1.0.0.csv
  ├── usace_2023_portcall_master_v1.1.0.csv
  ├── usace_2023_portcall_master_v1.2.0.csv
  ├── usace_2023_portcall_master_v1.3.0_restructured.csv
  ├── usace_2023_portcall_master_v1.4.0_usflag.csv
  └── usace_2023_portcall_master_v1.5.0_fuzzy.csv

02_STAGE02_CLASSIFICATION/_archive/entrance/
  ├── usace_2023_entrance_with_panjiva_match_v1.1.0.csv
  ├── usace_2023_entrance_with_panjiva_match_v1.2.0.csv
  ├── usace_2023_entrance_with_panjiva_match_v1.3.0.csv
  ├── usace_2023_inbound_entrance_transformed_v2.0.0.csv
  └── usace_2023_inbound_entrance_transformed_v2.1.0.csv

02_STAGE02_CLASSIFICATION/_archive/clearance/
  ├── usace_2023_clearance_with_panjiva_match_v1.0.0.csv
  ├── usace_2023_outbound_clearance_transformed_v2.0.0.csv
  └── usace_2023_outbound_clearance_transformed_v2.1.0.csv

01_STAGE01_PREPROCESSING/_archive/duplicates/
  ├── panjiva_exports_2023_PORTCALL_v20260115_1242.csv
  ├── panjiva_exports_2023_PORTCALL_v20260115_1245.csv
  ├── panjiva_exports_2023_PREPROCESSED_v20260115_1239.csv
  ├── panjiva_exports_2023_PREPROCESSED_v20260115_1241.csv
  ├── panjiva_imports_2023_FILTERED_v20260114_1236.csv
  ├── panjiva_imports_2024_FILTERED_v20260114_1237.csv
  └── panjiva_imports_2025_FILTERED_v20260114_1238.csv
```

---

## Proposed Naming Convention

### Format:
```
{dataset}_{year}_{type}_{version}.csv

Where:
  dataset = panjiva_imports | panjiva_exports | usace_entrance | usace_clearance | portcall_master
  year = 2023 | 2024 | 2025
  type = AUTHORITATIVE | ABRIDGED | WORKING | DRAFT
  version = v{MAJOR}.{MINOR}.{PATCH}
```

### Examples:
```
✅ panjiva_imports_2023_AUTHORITATIVE_v1.0.0.csv
✅ usace_2023_portcall_master_AUTHORITATIVE_v1.5.0.csv
✅ usace_2023_portcall_master_ABRIDGED_v1.5.0.csv
❌ panjiva_exports_2023_PORTCALL_v20260115_1246.csv (confusing timestamp)
```

---

## Data Lineage Map

### Stage 0: Raw Data (00_STAGE00_RAW_DATA/)
```
170 Panjiva import files
  └─ Combine & deduplicate
     └─ panjiva_imports_2023_AUTHORITATIVE_v1.0.0.csv

N Panjiva export files
  └─ Combine & deduplicate
     └─ panjiva_exports_2023_AUTHORITATIVE_v1.0.0.csv

USACE Entrance raw
  └─ Transform & enrich
     └─ usace_2023_entrance_AUTHORITATIVE_v1.0.0.csv

USACE Clearance raw
  └─ Transform & enrich
     └─ usace_2023_clearance_AUTHORITATIVE_v1.0.0.csv
```

### Stage 1: Preprocessing (01_STAGE01_PREPROCESSING/)
```
panjiva_imports_2023_AUTHORITATIVE_v1.0.0.csv
  └─ Match to USACE entrance
     └─ panjiva_imports_2023_with_portcall_AUTHORITATIVE_v1.0.0.csv

panjiva_exports_2023_AUTHORITATIVE_v1.0.0.csv
  └─ Match to USACE clearance
     └─ panjiva_exports_2023_with_portcall_AUTHORITATIVE_v1.0.0.csv

usace_2023_entrance_AUTHORITATIVE_v1.0.0.csv
  └─ Match to Panjiva imports
     └─ usace_2023_entrance_with_panjiva_AUTHORITATIVE_v1.0.0.csv

usace_2023_clearance_AUTHORITATIVE_v1.0.0.csv
  └─ Match to Panjiva exports
     └─ usace_2023_clearance_with_panjiva_AUTHORITATIVE_v1.0.0.csv
```

### Stage 2: Classification (02_STAGE02_CLASSIFICATION/)
```
usace_2023_entrance_with_panjiva_AUTHORITATIVE_v1.0.0.csv
  +
usace_2023_clearance_with_panjiva_AUTHORITATIVE_v1.0.0.csv
  └─ Marry entrance → clearance (sequential matching)
     └─ Add FGIS grain export data
        └─ Add US Flag registry data (exact + fuzzy matching)
           └─ Calculate agency fees
              └─ usace_2023_portcall_master_AUTHORITATIVE_v1.5.0.csv (85 columns)
                 └─ Remove technical metadata
                    └─ usace_2023_portcall_master_ABRIDGED_v1.5.0.csv (46 columns)
```

---

## Action Items

### Phase 1: Identify Authoritative Sources ✅ COMPLETE
- [x] Audit all files in project
- [x] Identify latest/best version of each dataset
- [x] Document data lineage

### Phase 2: Create Reorganization Script (NEXT)
- [ ] Write Python script to copy authoritative files to new structure
- [ ] Rename files according to new convention
- [ ] Move old versions to _archive/ folders
- [ ] Create README.md in each folder explaining contents

### Phase 3: Update Documentation
- [ ] Update CLAUDE.md with new file paths
- [ ] Update INDEX.html with new structure
- [ ] Create data dictionary index
- [ ] Update all references in scripts

### Phase 4: Clean Up Old Folders
- [ ] Move 01_step_one/ contents to _archive/
- [ ] Consolidate 01_STAGE01_PREPROCESSING/ and 01_step_one/
- [ ] Delete duplicate files after archiving

---

## Questions for User

1. **Should we execute this reorganization now or continue as-is?**
   - Pros: Clean structure, clear source of truth, easier to maintain
   - Cons: Need to update all script paths, takes time

2. **Do you want to keep all intermediate versions or just final?**
   - Option A: Keep only AUTHORITATIVE versions (saves space)
   - Option B: Archive all versions for auditing (safe but cluttered)

3. **Should we consolidate 01_step_one/ into 01_STAGE01_PREPROCESSING/?**
   - They're currently duplicates serving the same purpose

4. **What's your priority?**
   - Clean up now and organize properly
   - OR continue working and organize later
   - OR just document current state and leave as-is

---

## Current Authoritative Files (IDENTIFIED)

| Dataset | Current Location | Size | Use This For |
|---------|-----------------|------|--------------|
| **Panjiva Imports Raw** | `01_step_one/01_01_panjiva_imports_step_one/panjiva_imports_2023_20260112_STAGE00_v20260112_2052.csv` | 351.6 MB | Source data |
| **Panjiva Exports Raw** | `[NEED TO FIND IN 01_step_one/01_02_panjiva_exports_step_one/]` | TBD | Source data |
| **USACE Entrance** | `02_STAGE02_CLASSIFICATION/usace_2023_inbound_entrance_transformed_v2.2.0.csv` | 28.1 MB | Source data |
| **USACE Clearance** | `02_STAGE02_CLASSIFICATION/usace_2023_outbound_clearance_transformed_v2.2.0.csv` | 28.3 MB | Source data |
| **Entrance + Panjiva** | `02_STAGE02_CLASSIFICATION/usace_2023_entrance_with_panjiva_match_v1.3.1.csv` | 30.0 MB | Matched data |
| **Clearance + Panjiva** | `02_STAGE02_CLASSIFICATION/usace_2023_clearance_with_panjiva_match_v1.0.1.csv` | 29.5 MB | Matched data |
| **Port Call Master** | `02_STAGE02_CLASSIFICATION/usace_2023_portcall_master_v1.5.0_AUTHORITATIVE.csv` | 48.5 MB | **FINAL OUTPUT** |
| **Port Call Abridged** | `02_STAGE02_CLASSIFICATION/usace_2023_portcall_master_v1.5.0_ABRIDGED.csv` | 34.6 MB | **FINAL OUTPUT** |

---

**Status:** PROPOSED - Awaiting user decision on whether to execute reorganization.
