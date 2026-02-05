"""
Create v3.3.0: Remove tonnage filters from Phase 2 broad stroke rules

User's Min/Max Tons filters are blocking legitimate high-tonnage shipments.
Phase 2 = Broad strokes (HS4 match only, no tonnage filters)
Phase 3 = Refinement (HS6 + keywords + tonnage filters)

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
INPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v3.2.0_20260114_0300.csv")
OUTPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v3.3.0_20260114_0330.csv")

stamp("=== Creating v3.3.0: Remove Tonnage Filters from Phase 2 ===")
stamp("")

# Load current dictionary
df = pd.read_csv(INPUT_DICT, dtype=str)
stamp(f"Loaded v3.2.0: {len(df)} rules")

# Count Phase 2 rules with tonnage filters
phase2 = df[df['Phase'] == '2']
phase2_with_tons = phase2[
    ((phase2['Min_Tons'].notna()) & (phase2['Min_Tons'] != '')) |
    ((phase2['Max_Tons'].notna()) & (phase2['Max_Tons'] != ''))
]

stamp(f"Phase 2 rules: {len(phase2)}")
stamp(f"Phase 2 with tonnage filters: {len(phase2_with_tons)}")
stamp("")

# Remove tonnage filters from Phase 2
for idx in phase2.index:
    df.at[idx, 'Min_Tons'] = ''
    df.at[idx, 'Max_Tons'] = ''
    # Update note
    old_note = str(df.at[idx, 'Note'])
    if 'AUTHORITATIVE' in old_note:
        df.at[idx, 'Note'] = old_note.replace('Phase 2 HS4 Broad', 'Phase 2 HS4 Broad (no tonnage filters)')

stamp(f"Removed Min/Max Tons from all {len(phase2)} Phase 2 rules")
stamp("")

# Save v3.3.0
stamp(f"Saving v3.3.0: {OUTPUT_DICT}")
df.to_csv(OUTPUT_DICT, index=False)

stamp("")
stamp("=== v3.3.0 Complete ===")
stamp("Phase 2 rules now match on HS4 only (broad strokes)")
stamp("Tonnage filters moved to Phase 3 for refinement (future)")
