# Git Repository Setup Guide

**Date**: 2026-01-13
**Repository**: Panjiva Classification System
**Location**: `G:\My Drive\LLM\project_manifest`

---

## ✅ Repository Initialized

Your project is now under version control with the following configuration:

### 📊 Repository Statistics

- **Initial Commit**: `5a54f98`
- **Files Tracked**: 75 files
- **Repository Size**: 6.72 MB
- **Branch**: `master`

### 📁 What's Tracked (Committed)

**Documentation** (8 files):
- `INDEX.html` - Main landing page with dictionary links
- `classification_pipeline_dashboard.html` - Interactive charts
- `classification_technical_dataflow.html` - Technical diagrams
- `PIPELINE_MASTER_PLAN_UPDATED.md` - Complete system documentation
- `classification_phase10_final_summary.md` - Phase 10 results
- `classification_3year_comparison.md` - 3-year analysis
- `COLUMN_MAPPING_DICTIONARY.md` - Column reference
- `FOLDER_REORGANIZATION_SUMMARY.md` - Folder cleanup summary

**Reference Dictionaries** (65 files):
- **Cargo Classification**:
  - `01_cargo_dictionary_harmonized_v20260111_2313.csv` (latest)
  - `cargo_dictionary.csv`
  - Specialized dictionaries (pig iron, pulp & paper, steel, wind)

- **HS Code Lookups**:
  - `hs_code_lookup.json` (7.6 MB - complete hierarchy)
  - `hs2_lookup.csv`, `hs4_lookup.csv`, `hs6_lookup.csv`

- **Port & Location**:
  - `01_us_port_dictionary.csv`
  - ACE port codes, Schedule D
  - Country codes, waterway cross-references

- **Trade Codes**:
  - Schedule B export/import codes
  - SITC, NAICS, SIC, ATP codes

- **Carrier & Vessel**:
  - `01_ships_register.csv` (5.4 MB)
  - `01_carrier_scac_cargo.csv`

- **Party Harmonization**:
  - `parties_harmonization_master.json`
  - `parties_harmonization_rules.md`

- **Industry Standards**:
  - AISI steel product groups
  - Agency fee schedules
  - USACE references

**Configuration**:
- `.gitignore` - Exclusion rules

### 🚫 What's NOT Tracked (Excluded)

**Large Data Files** (~22 GB excluded):
- `00_raw_data/**` - All raw source files
- `01_step_one/**/*.csv` - Processed data files (1 GB)
- `build_documentation/classification_full_*/*.csv` - Classified outputs (1 GB+)
- `_archive/**` - Old versions (13 GB)

**Temporary Files**:
- Python cache (`__pycache__/`, `*.pyc`)
- IDE settings (`.vscode/`, `.idea/`)
- Logs and checkpoints
- Jupyter notebooks

---

## 🔧 Git Configuration

### Current Status
```bash
cd "G:/My Drive/LLM/project_manifest"
git status
# Output: On branch master, nothing to commit, working tree clean
```

### View Commit History
```bash
git log --oneline
# 5a54f98 Initial commit: Panjiva classification system
```

### Check Tracked Files
```bash
git ls-files | wc -l
# 75 files tracked
```

---

## 🌐 Next Steps: Remote Repository Setup

Your local git repository is ready. To enable cloud backup and collaboration, you need to push to a remote repository.

### Option 1: GitHub (Recommended)

**Steps**:

1. **Create GitHub Repository**:
   - Go to https://github.com/new
   - Repository name: `panjiva-classification-system`
   - Description: "Maritime cargo classification system for Panjiva import data (2023-2025)"
   - Privacy: **Private** (recommended for proprietary data)
   - Do NOT initialize with README (we have commits already)

2. **Add Remote**:
   ```bash
   cd "G:/My Drive/LLM/project_manifest"
   git remote add origin https://github.com/YOUR_USERNAME/panjiva-classification-system.git
   ```

3. **Push to GitHub**:
   ```bash
   git branch -M main  # Rename master to main
   git push -u origin main
   ```

4. **Verify**:
   - Visit your GitHub repository
   - Confirm 75 files uploaded
   - Check that large data files are NOT present

### Option 2: GitLab

**Steps**:

1. **Create GitLab Project**:
   - Go to https://gitlab.com/projects/new
   - Project name: `panjiva-classification-system`
   - Visibility: **Private**

2. **Add Remote**:
   ```bash
   cd "G:/My Drive/LLM/project_manifest"
   git remote add origin https://gitlab.com/YOUR_USERNAME/panjiva-classification-system.git
   ```

3. **Push to GitLab**:
   ```bash
   git branch -M main
   git push -u origin main
   ```

### Option 3: Bitbucket

Similar process to GitHub/GitLab.

---

## 📝 Daily Workflow

### Making Changes

1. **Check Status**:
   ```bash
   cd "G:/My Drive/LLM/project_manifest"
   git status
   ```

2. **Stage Changes**:
   ```bash
   # Stage specific files
   git add build_documentation/INDEX.html

   # Or stage all changes
   git add .
   ```

3. **Commit Changes**:
   ```bash
   git commit -m "Update INDEX.html: add new dictionary links"
   ```

4. **Push to Remote** (after setting up remote):
   ```bash
   git push
   ```

### Viewing History

```bash
# View commit log
git log --oneline --graph

# View changes in last commit
git show

# View changes to specific file
git log -p build_documentation/INDEX.html
```

### Undoing Changes

```bash
# Discard changes to file (before staging)
git restore build_documentation/INDEX.html

# Unstage file (after git add)
git restore --staged build_documentation/INDEX.html

# Revert to previous commit
git revert HEAD
```

---

## 🔄 Syncing Between Machines

If you work on multiple computers:

1. **Clone Repository** (on new machine):
   ```bash
   git clone https://github.com/YOUR_USERNAME/panjiva-classification-system.git
   cd panjiva-classification-system
   ```

2. **Pull Latest Changes**:
   ```bash
   git pull
   ```

3. **Make Changes and Push**:
   ```bash
   git add .
   git commit -m "Your changes"
   git push
   ```

---

## 📋 Commit Message Best Practices

**Good commit messages**:
```
✅ "Add dictionary section to INDEX.html"
✅ "Update cargo dictionary: add 15 crude oil variants"
✅ "Fix: correct HS code lookup for steel products"
✅ "Docs: update Phase 10 summary with final tonnage"
```

**Poor commit messages**:
```
❌ "update"
❌ "fixes"
❌ "changes"
❌ "wip"
```

**Format**:
- First line: Short summary (50 chars or less)
- Optional: Blank line + detailed description
- Use imperative mood ("Add" not "Added")
- Reference issue numbers if applicable

---

## 🔐 Security Notes

### What's Safe to Commit

✅ **Safe**:
- Documentation (HTML, Markdown)
- Reference dictionaries (public HS codes, port codes)
- Configuration files (`.gitignore`)
- Code/scripts

❌ **Never Commit**:
- API keys or passwords
- Personal identifiable information (PII)
- Proprietary raw data
- Large data files (>100 MB)
- Temporary files

### Already Protected

Your `.gitignore` already excludes:
- All raw data (`00_raw_data/**`)
- Processed CSV files
- Classified output files
- Archive folders

---

## 📊 Repository Size Management

### Current Size: 6.72 MB

**If repository grows too large**:

1. **Check large files**:
   ```bash
   git ls-files | xargs ls -lh | sort -k5 -hr | head -20
   ```

2. **Remove large file from history** (if committed by mistake):
   ```bash
   git filter-branch --tree-filter 'rm -f large_file.csv' HEAD
   ```

3. **Use Git LFS for large files**:
   ```bash
   git lfs install
   git lfs track "*.csv"
   git add .gitattributes
   ```

---

## 🛠️ Troubleshooting

### Problem: "Git not found"

**Solution**: Install Git for Windows
```
https://git-scm.com/download/win
```

### Problem: "Permission denied (publickey)"

**Solution**: Set up SSH keys for GitHub/GitLab
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Add public key to GitHub/GitLab settings
```

### Problem: "Large files rejected by remote"

**Solution**: Already handled! Your `.gitignore` excludes large files.
If you accidentally committed one:
```bash
git rm --cached large_file.csv
git commit -m "Remove large file from tracking"
```

### Problem: "Merge conflicts"

**Solution**: Pull before pushing
```bash
git pull --rebase
# Resolve conflicts in files
git add .
git rebase --continue
git push
```

---

## 🎯 Quick Reference

### Most Common Commands

```bash
# Check status
git status

# Stage all changes
git add .

# Commit with message
git commit -m "Your message"

# Push to remote
git push

# Pull from remote
git pull

# View history
git log --oneline

# Discard changes
git restore filename

# Create new branch
git checkout -b feature-branch

# Switch branches
git checkout main

# Merge branch
git merge feature-branch
```

---

## 📚 Additional Resources

- **Git Documentation**: https://git-scm.com/doc
- **GitHub Guides**: https://guides.github.com/
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
- **Interactive Git Tutorial**: https://learngitbranching.js.org/

---

## ✅ Summary

Your Panjiva classification system is now:
- ✅ Under version control (local repository)
- ✅ Protected with proper `.gitignore`
- ✅ Ready for remote backup (GitHub/GitLab)
- ✅ 75 files tracked (6.72 MB)
- ✅ 22 GB of data properly excluded

**Next Action**: Set up remote repository on GitHub/GitLab for cloud backup and collaboration.

---

**Last Updated**: 2026-01-13
**Git Commit**: `5a54f98`
