# Panjiva Classification Pipeline v2
**Created:** 2026-01-28
**Status:** 🟢 ACTIVE - Fresh Start

---

## 🎯 Project Overview

Clean rebuild of Panjiva import classification system with strict rules to prevent drift.

**What this does:**
1. Preprocess raw Panjiva data (135 cols → 61 cols)
2. Classify cargo into 4-level taxonomy (Group → Commodity → Cargo → Cargo Detail)
3. Match to USACE port call data (future)

**Key Principle:** Every row traceable to original raw data via `REC_ID`

---

## 📁 Project Structure

```
panjiva_classification_v2/
│
├── 00_REFERENCE/              # Reference data (READ-ONLY)
│   ├── ship_registry.csv      # Vessel specs (52K vessels)
│   ├── dictionary_v3.6.0.csv  # Classification rules (668 rules)
│   └── port_dictionary.csv    # Port mappings (future)
│
├── 01_RAW_DATA/               # Raw source data (READ-ONLY)
│   ├── panjiva_imports/       # 170 raw Panjiva import files
│   ├── panjiva_exports/       # Export data (future)
│   └── usace_entrance_clearance/  # USACE data (future)
│
├── 02_SCRIPTS/                # Processing scripts (VERSIONED)
│   ├── step01_preprocess_v1.0.0.py   # Preprocessing ONLY
│   ├── step02_classify_v1.0.0.py     # Classification ONLY
│   ├── step03_match_v1.0.0.py        # Matching ONLY (future)
│   └── _archive/              # Old script versions
│
├── 03_DATA/                   # Output data pipeline
│   ├── 00_excluded/           # Excluded records (saved, not deleted)
│   ├── 01_preprocessed/       # After step01 (61 columns)
│   ├── 02_classified/         # After step02 (61 columns, filled)
│   ├── 03_matched/            # After step03 (future)
│   └── 99_checkpoints/        # Emergency checkpoints
│
├── 04_TESTS/                  # Testing files
│   ├── sample_5k/             # 5K test samples
│   └── test_results/          # Test outputs
│
├── 05_LOGS/                   # Execution logs
│   └── step01_preprocess_YYYYMMDD_HHMM.log
│
├── 06_DOCUMENTATION/          # Project documentation
│   ├── COLUMN_EVOLUTION_TRACKER.csv
│   └── HARMONIZATION_DECISIONS.md
│
├── PIPELINE_RULES.md          # ⚠️ MUST FOLLOW - 15 rules
├── README.md                  # This file
└── .gitignore                 # Git exclusions
```

---

## 🚀 Current Status (2026-01-28)

### Completed
✅ Fresh project structure created
✅ Reference data copied (ship registry, dictionary v3.6.0)
✅ PIPELINE_RULES.md written (15 rules)
✅ Documentation copied (column tracker, harmonization decisions)
✅ Folder structure created (7 top-level folders)

### Next Steps
🔴 Create step01_preprocess_v1.0.0.py
🔴 Create symlinks to raw data (avoid duplicating 1GB+ files)
🔴 Test preprocessing on 5K sample
🔴 Run preprocessing on 2024 full year
🔴 Create step02_classify_v1.0.0.py
🔴 Test classification on 5K sample

---

## 📊 Data Pipeline Flow

```
Raw Panjiva (135 columns)
    ↓
[Step 01: Preprocessing]
    → 03_DATA/01_preprocessed/ (61 columns, all initialized)
    → 03_DATA/00_excluded/ (excluded records saved)
    ↓
[Step 02: Classification]
    → 03_DATA/02_classified/ (61 columns, classification filled)
    ↓
[Step 03: Matching] (FUTURE)
    → 03_DATA/03_matched/ (matched to USACE)
```

**Key:** Each step reads from previous step's output folder

---

## 🎯 Key Features (v2 Improvements)

### 1. Complete Audit Trail
- Every row has permanent `REC_ID` (format: `PANV_IMP_FILE001_R000123`)
- Can trace any record back to original raw file + row number
- Excluded records saved, not deleted

### 2. Strict Rules
- **PIPELINE_RULES.md** enforces discipline
- One script per step (no ad-hoc drift)
- Test on 5K before full run (ALWAYS)
- Version everything (scripts, data, reference)

### 3. Clean Separation
- Preprocessing: ALL column transformations (drop, rename, add, enrich)
- Classification: ONLY fill Group/Commodity/Cargo/Cargo Detail
- Matching: ONLY join tables

### 4. Harmonization
- Shipper/Consignee overwritten with harmonized values
- "(Original Format)" columns preserve originals
- Can always roll back to original values

### 5. Simple Structure
- 7 folders (not 20+)
- 3 scripts (not scattered everywhere)
- Linear flow (can't get confused)

---

## 🔢 Schema Evolution

| Stage | Columns | Key Changes |
|-------|---------|-------------|
| **Raw** | 135 | Original Panjiva data |
| **Preprocessed** | 61 | Dropped 84, renamed 9, split Quantity, extract HS codes, add vessel enrichment, add empty classification columns |
| **Classified** | 61 | Same schema, Group/Commodity/Cargo/Cargo Detail now filled |
| **Matched** | TBD | Join to USACE port call master |

**Final Column (61):** `REC_ID` - Permanent unique identifier ⭐

---

## ⚠️ Critical Rules

**From PIPELINE_RULES.md:**

1. **Test on 5K first** - NEVER run full without testing small (Rule 7)
2. **Every row traceable** - REC_ID enables audit trail (Rule 1)
3. **Save excluded records** - Nothing truly deleted (Rule 2)
4. **Column changes = preprocessing only** - Don't add columns in classification (Rule 6)
5. **Version everything** - Scripts, data, reference files (Rule 8)
6. **Archive before changes** - Can always roll back (Rule 5)
7. **One script per step** - No ad-hoc scripts (Rule 2)

**See PIPELINE_RULES.md for complete list (15 rules)**

---

## 🚦 How to Use This Project

### Quick Start (5K Test)
```bash
cd "G:\My Drive\LLM\project_manifest\panjiva_classification_v2"

# 1. Preprocessing (5K sample)
python 02_SCRIPTS/step01_preprocess_v1.0.0.py --sample 5000 --year 2024

# 2. Verify output
# Check: 03_DATA/01_preprocessed/sample_5k/
# Verify: 61 columns, ~5000 rows, REC_ID unique

# 3. Classification (5K sample)
python 02_SCRIPTS/step02_classify_v1.0.0.py --sample 5000 --year 2024

# 4. Verify results
# Check: 03_DATA/02_classified/sample_5k/
# Verify: Group/Commodity/Cargo/Cargo Detail filled
```

### Full Year Processing
```bash
# ONLY after 5K test passes

# 1. Preprocess full 2024
python 02_SCRIPTS/step01_preprocess_v1.0.0.py --year 2024

# 2. Classify full 2024
python 02_SCRIPTS/step02_classify_v1.0.0.py --year 2024

# Outputs:
# 03_DATA/01_preprocessed/panjiva_2024_preprocessed_v1.0.0_YYYYMMDD_HHMM.csv
# 03_DATA/02_classified/panjiva_2024_classified_v1.0.0_YYYYMMDD_HHMM.csv
```

---

## 📈 Performance Expectations

| Operation | Records | Time | Output Size |
|-----------|---------|------|-------------|
| Preprocess 5K | 5,000 | ~2 min | 2 MB |
| Classify 5K | 5,000 | ~2 min | 2 MB |
| Preprocess 2024 | ~430K | ~30 min | ~350 MB |
| Classify 2024 | ~430K | ~8-10 hrs | ~350 MB |

---

## 🔍 Troubleshooting

### Script can't find raw data
→ Create symlinks to old project raw data folder (see below)

### REC_ID not unique
→ Bug in preprocessing, check file numbering logic

### Vessel enrichment low match rate (<70%)
→ Check ship_registry.csv has correct vessel names

### Classification columns still empty
→ Check dictionary_v3.6.0.csv is loaded, rules are Active=TRUE

### Excluded records file missing
→ Check 03_DATA/00_excluded/ folder exists, script has write permission

---

## 🔗 Linking Raw Data (Avoid Duplication)

**Don't copy 1GB+ of raw files. Create symlinks instead:**

```bash
# Windows (run as administrator)
mklink /D "G:\My Drive\LLM\project_manifest\panjiva_classification_v2\01_RAW_DATA\panjiva_imports" "G:\My Drive\LLM\project_manifest\00_raw_data\00_01_panjiva_imports_raw"

# Linux/Mac
ln -s "G:\My Drive\LLM\project_manifest\00_raw_data\00_01_panjiva_imports_raw" "G:\My Drive\LLM\project_manifest\panjiva_classification_v2\01_RAW_DATA\panjiva_imports"
```

---

## 📝 Git Setup

```bash
cd "G:\My Drive\LLM\project_manifest\panjiva_classification_v2"
git init
git add .
git commit -m "[INIT] Fresh project structure v2 with PIPELINE_RULES"
```

**What's committed:**
- ✅ Scripts (02_SCRIPTS/)
- ✅ Reference data (00_REFERENCE/)
- ✅ Documentation (06_DOCUMENTATION/)
- ✅ Rules (PIPELINE_RULES.md, README.md)
- ❌ Data files (too large, excluded via .gitignore)
- ❌ Logs (temporary)

---

## 📚 Documentation

**Essential Reading:**
- `PIPELINE_RULES.md` - 15 rules to prevent drift ⚠️ MUST FOLLOW
- `06_DOCUMENTATION/COLUMN_EVOLUTION_TRACKER.csv` - Track columns through pipeline
- `06_DOCUMENTATION/HARMONIZATION_DECISIONS.md` - Data transformation decisions

**Quick References:**
- Rule 1: Every row gets permanent REC_ID
- Rule 2: Save excluded records (never delete)
- Rule 3: Overwrite Shipper/Consignee (keep Original Format)
- Rule 4: Quantity split is only destructive transform
- Rule 7: Test on 5K before full run

---

## 🎉 Success Criteria

**Before declaring "done":**

✅ Preprocessing
- [ ] 5K test passes (61 columns, REC_ID unique, vessel enrichment >70%)
- [ ] Full 2024 completes without errors
- [ ] Excluded records saved to 00_excluded/
- [ ] Output files created in 01_preprocessed/

✅ Classification
- [ ] 5K test passes (Group/Commodity/Cargo/Cargo Detail filled)
- [ ] Full 2024 completes (8-10 hours)
- [ ] Classification rate >60% (780K+ records)
- [ ] Tonnage capture >70% (1.4B+ tons)

✅ Documentation
- [ ] README.md updated with current status
- [ ] Git commits after each milestone
- [ ] Logs archived to 05_LOGS/

---

## 🤝 Contributing

**Making Changes:**

1. Follow PIPELINE_RULES.md strictly
2. Test on 5K before full run
3. Version scripts when changing
4. Archive before major changes
5. Update README.md after changes
6. Commit to git

**Adding New Features:**

1. Update preprocessing script (if schema changes)
2. Update dictionary (if new classification rules)
3. Increment version number
4. Test on 5K
5. Document in README.md

---

## 📞 Contact

**Project Owner:** WSD3
**Created:** 2026-01-28
**Version:** 2.0.0 (Fresh Start)

---

**Status:** 🟢 Ready for development
**Next Action:** Create step01_preprocess_v1.0.0.py
