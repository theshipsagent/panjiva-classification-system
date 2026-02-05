"""
Fix Phase 1 carrier lock problem - v3.4.0

Problem: 42 Phase 1 carrier rules lock Commodity but don't set it,
blocking Phase 2 from refining based on HS codes.

Solution:
- Phase 1 carriers: Lock only Group (vessel-based classification)
- Leave Commodity/Cargo/Detail unlocked for Phase 2 HS refinement

Exception: Carriers with full taxonomy (all 4 values set) can lock all 4

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
INPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v3.3.0_20260114_0330.csv")
OUTPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v3.4.0_20260114_0400.csv")

stamp("=== Fixing Phase 1 Carrier Locks (v3.4.0) ===")
stamp("")

# Load current dictionary
df = pd.read_csv(INPUT_DICT, dtype=str)
stamp(f"Loaded v3.3.0: {len(df)} rules")

# Get Phase 1 carrier rules
phase1 = df[df['Phase'] == '1']
stamp(f"Phase 1 rules: {len(phase1)}")
stamp("")

# Fix rules that lock Commodity without setting it
fixed_count = 0

for idx in phase1.index:
    commodity = str(df.at[idx, 'Commodity']).strip()
    cargo = str(df.at[idx, 'Cargo']).strip()
    cargo_detail = str(df.at[idx, 'Cargo_Detail']).strip()

    # Check if taxonomy values are empty
    commodity_empty = not commodity or commodity == 'nan'
    cargo_empty = not cargo or cargo == 'nan'
    detail_empty = not cargo_detail or cargo_detail == 'nan'

    # If any taxonomy value is empty, unlock it
    if commodity_empty:
        df.at[idx, 'Lock_Commodity'] = 'FALSE'
        fixed_count += 1

    if cargo_empty:
        df.at[idx, 'Lock_Cargo'] = 'FALSE'

    if detail_empty:
        df.at[idx, 'Lock_Cargo_Detail'] = 'FALSE'

stamp(f"Fixed {fixed_count} Phase 1 rules:")
stamp("  - Carriers now lock only Group (vessel-based)")
stamp("  - Commodity/Cargo/Detail unlocked for Phase 2 HS refinement")
stamp("")

# Save v3.4.0
stamp(f"Saving v3.4.0: {OUTPUT_DICT}")
df.to_csv(OUTPUT_DICT, index=False)

stamp("")
stamp("=== v3.4.0 Complete ===")
stamp("Phase 1 carriers set Group, Phase 2 refines Commodity based on cargo HS codes")
