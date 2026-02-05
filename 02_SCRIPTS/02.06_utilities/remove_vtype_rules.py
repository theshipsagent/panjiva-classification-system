"""
Remove VTYPE rules from Phase 1 to allow cargo-based classification

VTYPE rules lock Group based on vessel type, blocking Phase 2 cargo classification.
Result: 31.8% of tonnage stuck with TBN (7.6M tons).

Solution: Remove VTYPE rules, let cargo HS codes determine Group.

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
INPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v3.1.0_20260114_0230.csv")
OUTPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v3.2.0_20260114_0300.csv")

stamp("=== Removing VTYPE Rules from Phase 1 ===")
stamp("")

# Load current dictionary
df = pd.read_csv(INPUT_DICT, dtype=str)
stamp(f"Loaded v3.1.0: {len(df)} rules")

# Count VTYPE rules
vtype_rules = df[df['Rule_ID'].str.contains('VTYPE', na=False)]
stamp(f"Found {len(vtype_rules)} VTYPE rules:")
for _, rule in vtype_rules.iterrows():
    stamp(f"  - {rule['Rule_ID']}: Group={rule.get('Group', '')}")

stamp("")

# Remove VTYPE rules
df_clean = df[~df['Rule_ID'].str.contains('VTYPE', na=False)]
stamp(f"After removal: {len(df_clean)} rules")
stamp(f"Removed: {len(df) - len(df_clean)} VTYPE rules")

stamp("")

# Save v3.2.0
stamp(f"Saving v3.2.0: {OUTPUT_DICT}")
df_clean.to_csv(OUTPUT_DICT, index=False)

stamp("")
stamp("=== v3.2.0 Complete ===")
stamp("VTYPE rules removed - Phase 2 can now classify cargo by HS codes")
