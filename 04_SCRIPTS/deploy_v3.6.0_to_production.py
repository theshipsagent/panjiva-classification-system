"""
Deploy Dictionary v3.6.0 to Production
- Move dictionary to authoritative location
- Update project documentation
- Create version history
- Prepare git commit

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
import shutil
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
SOURCE_DICT = Path(r"G:\My Drive\LLM\project_manifest\user_notes\cargo_classification_dictionary_v3.6.0_DRAFT_20260114.csv")
PRODUCTION_DIR = Path(r"G:\My Drive\LLM\project_manifest\03_DICTIONARIES\03.01_cargo_classification")
PRODUCTION_FILE = PRODUCTION_DIR / "cargo_classification_dictionary_v3.6.0_20260114_1830.csv"

# Documentation paths
DOCS_DIR = Path(r"G:\My Drive\LLM\project_manifest\05_DOCUMENTATION")
VERSION_HISTORY = DOCS_DIR / "DICTIONARY_VERSION_HISTORY.md"
README = Path(r"G:\My Drive\LLM\project_manifest\README.md")

stamp("=" * 80)
stamp("Deploy Dictionary v3.6.0 to Production")
stamp("=" * 80)
stamp("")

# Step 1: Copy dictionary to production
stamp("Step 1: Deploying dictionary to production location...")
shutil.copy2(SOURCE_DICT, PRODUCTION_FILE)
stamp(f"  [OK] Copied to: {PRODUCTION_FILE.name}")

# Verify file
df = pd.read_csv(PRODUCTION_FILE, dtype=str)
stamp(f"  [OK] Verified: {len(df)} rules loaded successfully")

# Step 2: Create version history entry
stamp("")
stamp("Step 2: Updating version history...")

version_entry = f"""
## Version 3.6.0 - 2026-01-14 18:30

**Major Release: Refined Keywords & Comprehensive Commodity Coverage**

### Summary
- **668 total rules** (+95 from v3.4.0, +16.6%)
- **218 new user-edited rules** across 31 HS2 chapters
- **100% test classification rate** on 15K sample
- **Break-Bulk group eliminated** - replaced with reliable Dry Bulk/Liquid Bulk/Liquid Gas

### New Features

#### 1. Refined Keyword Strategy
- **Key_Phrases**: Multi-word phrases requiring exact matches (e.g., "CRUDE OIL", "PIG IRON")
- **Primary_Keywords**: Standalone product terms (e.g., "CEMENT", "STEEL")
- **Descriptor_Keywords**: Modifiers and qualifiers (e.g., "HOT", "ROLLED", "PRIME")
- **Match_Strategy**: PHRASE_REQUIRED vs PRIMARY_SUFFICIENT

#### 2. Comprehensive Coverage (218 New Rules)
- **HS27 Mineral Fuels** (13): Crude Oil, Petroleum Products, Coal, LNG
- **HS28 Inorganic Chemicals** (42): Caustic Soda, Ammonia, Fertilizers, Alumina
- **HS29 Organic Chemicals** (40): Alcohols, Ketones, Benzene, Acids
- **HS72-73 Iron & Steel** (40): Pig Iron, Flat Rolled, Long Products, Semi-Finished
- **HS76 Aluminum** (16): Unwrought, Plates, Bars, Wire, Foil
- **HS74 Copper** (2): Cathodes, Mattes
- **HS78-79 Lead & Zinc** (8): Unwrought, Concentrates
- **HS25 Stone/Earth** (9): Salt, Cement, Aggregates, Gypsum
- **HS31 Fertilizers** (3): Nitrogen, Potash, Compounds
- **HS26 Ores** (5): Bauxite, Iron Ore, Titanium Ore
- **Agricultural Products** (14): Grain, Oils, Coffee, Sugar, Rubber
- **Forestry** (6): Lumber, Paper, Wood Pulp
- **Construction** (17): Cement, Aggregates, Gypsum, Slag
- **General Cargo** (7): Vehicles, Machinery

### Test Results (15K Sample)

| Metric | v3.4.0 | v3.6.0 | Change |
|--------|--------|--------|--------|
| Total Rules | 573 | 668 | +95 (+16.6%) |
| Phase 3 Rules | 0 | 218 | +218 |
| Phase 3 Classifications | 0 | 1,443 | +1,443 (9.6%) |
| Dry Bulk % | 11.4% | 95.7% | +84.3 points |
| Break-Bulk % | 82.0% | 0.0% | -82.0 points |
| Classification Rate | 100% | 100% | Maintained |

### Breaking Changes
- **Break-Bulk group eliminated**: All records reclassified to Dry Bulk, Liquid Bulk, or Liquid Gas
- **Keyword columns changed**: Added Key_Phrases, Primary_Keywords, Descriptor_Keywords, Match_Strategy
- **Old Keywords column**: Still present but deprecated, will be removed in v4.0

### Files Changed
- `03_DICTIONARIES/03.01_cargo_classification/cargo_classification_dictionary_v3.6.0_20260114_1830.csv`
- `05_DOCUMENTATION/DICTIONARY_V3.6.0_SUMMARY.md`
- `05_DOCUMENTATION/DICTIONARY_V3.6.0_TEST_RESULTS.md`

### Classification Scripts
- Updated keyword matching logic in `classify_15k_sample_v3.6.0.py`
- Added `check_keyword_match()` function supporting refined strategy

### Contributors
- WSD3 (User) - Manual classification of 218 specialized rules
- Claude Code - Script development, testing, documentation

---

"""

# Check if version history exists, create or append
if VERSION_HISTORY.exists():
    with open(VERSION_HISTORY, 'r', encoding='utf-8') as f:
        existing = f.read()

    # Insert new version at top (after header)
    if '# Dictionary Version History' in existing:
        parts = existing.split('# Dictionary Version History\n', 1)
        new_content = parts[0] + '# Dictionary Version History\n' + version_entry + parts[1]
    else:
        new_content = '# Dictionary Version History\n\n' + version_entry + existing
else:
    new_content = '# Dictionary Version History\n\n' + version_entry

with open(VERSION_HISTORY, 'w', encoding='utf-8') as f:
    f.write(new_content)

stamp(f"  [OK] Updated: {VERSION_HISTORY.name}")

# Step 3: Update README
stamp("")
stamp("Step 3: Updating README...")

readme_update = f"""
## Latest Version: v3.6.0 (2026-01-14)

**Major Release: 218 new user-edited rules with refined keyword strategy**

- [OK] 668 total rules (+95 from v3.4.0)
- [OK] 100% classification rate on 15K test sample
- [OK] Break-Bulk group eliminated (improved from 82% vague to 95.7% Dry Bulk)
- [OK] Comprehensive coverage: Crude Oil, Steel, Chemicals, Metals, Fertilizers
- [OK] Refined keyword strategy: Key_Phrases, Primary_Keywords, Match_Strategy

**Quick Links:**
- [Version History](05_DOCUMENTATION/DICTIONARY_VERSION_HISTORY.md)
- [v3.6.0 Summary](user_notes/DICTIONARY_V3.6.0_SUMMARY.md)
- [v3.6.0 Test Results](user_notes/DICTIONARY_V3.6.0_TEST_RESULTS.md)
- [Dictionary File](03_DICTIONARIES/03.01_cargo_classification/cargo_classification_dictionary_v3.6.0_20260114_1830.csv)

"""

if README.exists():
    with open(README, 'r', encoding='utf-8') as f:
        readme = f.read()

    # Replace or add version section
    if '## Latest Version:' in readme:
        # Find and replace the version section
        lines = readme.split('\n')
        new_lines = []
        skip = False
        for line in lines:
            if line.startswith('## Latest Version:'):
                new_lines.extend(readme_update.strip().split('\n'))
                skip = True
            elif skip and line.startswith('##'):
                skip = False
                new_lines.append(line)
            elif not skip:
                new_lines.append(line)
        readme = '\n'.join(new_lines)
    else:
        # Add version section at top
        readme = readme_update + '\n' + readme

    with open(README, 'w', encoding='utf-8') as f:
        f.write(readme)

    stamp(f"  [OK] Updated: README.md")
else:
    stamp("  [WARNING] README.md not found, skipping")

# Step 4: Summary statistics
stamp("")
stamp("=" * 80)
stamp("Deployment Summary")
stamp("=" * 80)
stamp("")
stamp(f"Dictionary v3.6.0 deployed successfully!")
stamp(f"  Location: {PRODUCTION_FILE}")
stamp(f"  Rules: {len(df)}")
stamp(f"  Active: {len(df[df['Active'] == 'TRUE'])}")
stamp("")
stamp("Phase breakdown:")
for phase in sorted(df['Phase'].unique()):
    count = len(df[df['Phase'] == phase])
    stamp(f"  Phase {phase}: {count} rules")
stamp("")
stamp("Group breakdown:")
for group in df.groupby('Group').size().sort_values(ascending=False).head(5).items():
    stamp(f"  {group[0]}: {group[1]} rules")
stamp("")
stamp("Documentation updated:")
stamp(f"  [OK] {VERSION_HISTORY.name}")
stamp(f"  [OK] {README.name}")
stamp("")
stamp("Next steps:")
stamp("  1. Update HTML dashboard and graphs")
stamp("  2. Git add and commit changes")
stamp("  3. Deploy to production systems")
stamp("")
stamp("=" * 80)
