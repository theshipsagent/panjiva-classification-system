"""
Fix VTYPE-RORO to only lock Group (not all 4 columns)

Issue: VTYPE-RORO locks all 4, preventing Phase 2 carrier rules from refining
Fix: Change locks to Group=TRUE, Commodity/Cargo/Cargo_Detail=FALSE
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# Paths
INPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.3.1_20260113_2030.csv")
OUTPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.3.2_20260113_2300.csv")

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

stamp("=== Fixing VTYPE-RORO Lock Levels ===")

# Load dictionary
df = pd.read_csv(INPUT_DICT, dtype=str)

# Find VTYPE-RORO rule
vtype_roro = df[df['Rule_ID'] == 'VTYPE-RORO']

if len(vtype_roro) > 0:
    idx = vtype_roro.index[0]

    stamp(f"\nCurrent VTYPE-RORO locks:")
    stamp(f"  Group: {df.at[idx, 'Lock_Group']}")
    stamp(f"  Commodity: {df.at[idx, 'Lock_Commodity']}")
    stamp(f"  Cargo: {df.at[idx, 'Lock_Cargo']}")
    stamp(f"  Cargo_Detail: {df.at[idx, 'Lock_Cargo_Detail']}")

    # Fix lock levels - only lock Group
    df.at[idx, 'Lock_Group'] = 'TRUE'
    df.at[idx, 'Lock_Commodity'] = 'FALSE'
    df.at[idx, 'Lock_Cargo'] = 'FALSE'
    df.at[idx, 'Lock_Cargo_Detail'] = 'FALSE'

    # Set taxonomy to TBN (will be refined by carrier rules)
    df.at[idx, 'Commodity'] = 'TBN'
    df.at[idx, 'Cargo'] = 'TBN'
    df.at[idx, 'Cargo_Detail'] = 'TBN'

    df.at[idx, 'Last_Modified'] = '2026-01-13'

    stamp(f"\nFixed VTYPE-RORO locks:")
    stamp(f"  Group: {df.at[idx, 'Lock_Group']} (lock Ro/Ro)")
    stamp(f"  Commodity: {df.at[idx, 'Lock_Commodity']} (allow refinement)")
    stamp(f"  Cargo: {df.at[idx, 'Lock_Cargo']} (allow refinement)")
    stamp(f"  Cargo_Detail: {df.at[idx, 'Lock_Cargo_Detail']} (allow refinement)")

    stamp(f"\nClassification: Ro/Ro > TBN > TBN > TBN")
    stamp(f"(Carrier rules in Phase 2 will refine to full classification)")

# Save v2.3.2
stamp(f"\nSaving v2.3.2: {OUTPUT_DICT}")
df.to_csv(OUTPUT_DICT, index=False)

stamp("\n=== Dictionary v2.3.2 Complete ===")
stamp("VTYPE-RORO now locks Group only")
stamp("Phase 2 carrier rules can now fully classify RoRo records")
