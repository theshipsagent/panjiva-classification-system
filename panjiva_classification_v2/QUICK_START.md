# Quick Start Guide
**For when you return to this project**

---

## 📍 Where Am I?

**Project:** `panjiva_classification_v2/`
**Status:** Fresh start with strict rules
**Created:** 2026-01-28

---

## 🚀 Quick Commands

### Check Current Status
```bash
# Read README.md for latest status
cat README.md

# Check what scripts exist
ls -l 02_SCRIPTS/

# Check latest outputs
ls -lh 03_DATA/01_preprocessed/
ls -lh 03_DATA/02_classified/
```

### Run 5K Test (ALWAYS DO THIS FIRST)
```bash
cd "G:\My Drive\LLM\project_manifest\panjiva_classification_v2"

# Step 1: Preprocess
python 02_SCRIPTS/step01_preprocess_v1.0.0.py --sample 5000 --year 2024

# Step 2: Classify
python 02_SCRIPTS/step02_classify_v1.0.0.py --sample 5000 --year 2024
```

### Run Full Year
```bash
# ONLY after 5K test passes!

# Preprocess 2024
python 02_SCRIPTS/step01_preprocess_v1.0.0.py --year 2024

# Classify 2024
python 02_SCRIPTS/step02_classify_v1.0.0.py --year 2024
```

---

## 📋 Essential Files

| File | Purpose |
|------|---------|
| `PIPELINE_RULES.md` | ⚠️ MUST FOLLOW - 15 rules to prevent drift |
| `README.md` | Current project status and overview |
| `06_DOCUMENTATION/COLUMN_EVOLUTION_TRACKER.csv` | Track columns through pipeline |
| `06_DOCUMENTATION/HARMONIZATION_DECISIONS.md` | Data transformation decisions |

---

## 🎯 Current Workflow

```
1. Read README.md → Know current status
2. Check PIPELINE_RULES.md → Remind yourself of rules
3. Test on 5K → Verify everything works
4. Run full year → Process actual data
5. Update README.md → Document what you did
6. Git commit → Save progress
```

---

## ⚠️ Critical Rules (Top 5)

1. **Test on 5K first** (Rule 7) - NEVER run full without testing
2. **Every row traceable** (Rule 1) - REC_ID enables audit
3. **Column changes = preprocessing only** (Rule 6) - Don't modify schema elsewhere
4. **Version everything** (Rule 8) - Scripts, data, reference files
5. **Save excluded records** (Rule 2) - Never truly delete

**See PIPELINE_RULES.md for all 15 rules**

---

## 🆘 Troubleshooting

**Problem:** Script can't find raw data
**Solution:** Create symlink to old project's raw data folder

**Problem:** REC_ID not unique
**Solution:** Bug in preprocessing file numbering logic

**Problem:** Vessel match rate low (<70%)
**Solution:** Check ship_registry.csv has correct data

**Problem:** Classification columns empty
**Solution:** Check dictionary v3.6.0 loaded, rules Active=TRUE

**Problem:** Can't remember what to do next
**Solution:** Read README.md "Next Steps" section

---

## 📂 Folder Purposes

| Folder | Purpose | Size |
|--------|---------|------|
| `00_REFERENCE/` | Ship registry, dictionary (READ-ONLY) | 6 MB |
| `01_RAW_DATA/` | Original Panjiva files (symlink, READ-ONLY) | 1 GB |
| `02_SCRIPTS/` | 3 scripts only (versioned) | <1 MB |
| `03_DATA/` | Pipeline outputs (preprocessing, classification) | ~3 GB |
| `04_TESTS/` | 5K test samples and results | <50 MB |
| `05_LOGS/` | Execution logs | <10 MB |
| `06_DOCUMENTATION/` | Column tracker, decisions | <5 MB |

---

## 🔄 Common Operations

### Adding New Classification Rules
1. Edit `00_REFERENCE/dictionary_v3.6.0.csv`
2. Increment version → `dictionary_v3.7.0.csv`
3. Update script to use new version
4. Test on 5K
5. Update README.md

### Fixing Preprocessing Bug
1. Copy `step01_preprocess_v1.0.0.py` → `step01_preprocess_v1.0.1.py`
2. Fix bug
3. Test on 5K
4. Run full year if test passes
5. Archive old version to `02_SCRIPTS/_archive/`

### Adding New Column
1. Update `step01_preprocess_v1.0.0.py` (ONLY place to add columns)
2. Increment MAJOR version → `step01_preprocess_v2.0.0.py`
3. Update `COLUMN_EVOLUTION_TRACKER.csv`
4. Test on 5K
5. Re-run preprocessing on all years

---

## 💡 Remember

- **One script per step** - No ad-hoc scripts
- **Linear flow** - Raw → Preprocess → Classify → Match
- **Test small first** - 5K before full
- **Document as you go** - Update README.md
- **Commit often** - Save progress to git

---

**When in doubt, check PIPELINE_RULES.md**
