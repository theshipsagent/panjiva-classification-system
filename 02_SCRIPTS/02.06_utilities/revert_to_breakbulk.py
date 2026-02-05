"""
REVERT vehicle carriers back to Break Bulk (original authoritative classification)

ERROR: Changed Break Bulk -> Ro/Ro in v2.5.1
FIX: Restore original Break Bulk classification from 01_carrier_scac_cargo.csv

Priority is TONS classified, not record count
Vehicle carriers are Break Bulk, not Ro/Ro

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
INPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.5.1_20260114_0030.csv")
ORIGINAL_DICT = Path(r"G:\My Drive\LLM\project_manifest\01.01_dictionary\01_carrier_scac_cargo.csv")
OUTPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.5.2_20260114_0100.csv")

stamp("=== REVERTING to Original Break Bulk Classification ===")
stamp("ERROR: Incorrectly changed vehicle carriers from Break Bulk to Ro/Ro")
stamp("FIX: Restoring authoritative classification from 01_carrier_scac_cargo.csv")
stamp("")

# Load dictionaries
df = pd.read_csv(INPUT_DICT, dtype=str)
df_orig = pd.read_csv(ORIGINAL_DICT, dtype=str)

# Get original authoritative classifications
original_classifications = {}
for _, row in df_orig.iterrows():
    scac = str(row['Carrier']).strip()
    if scac and scac != 'nan':
        action = str(row.get('action', '')).lower()
        if 'lock from further processing' in action or 'enter values' in action:
            original_classifications[scac] = {
                'Group': str(row.get('Group', '')).strip(),
                'Commodity': str(row.get('Commodity', '')).strip(),
                'Cargo': str(row.get('Cargo', '')).strip(),
                'Cargo_Detail': str(row.get('CargoDetail', '')).strip()
            }

stamp(f"Loaded {len(original_classifications)} authoritative carrier classifications")
stamp("")

# Revert any changes back to original
reverted_count = 0
for scac, orig_class in original_classifications.items():
    mask = df['Carrier_SCAC'] == scac
    if mask.sum() > 0:
        idx = df[mask].index[0]
        current_group = df.at[idx, 'Group']

        # Check if we changed it
        if current_group != orig_class['Group']:
            stamp(f"  REVERT {scac:6s}: {current_group:15s} -> {orig_class['Group']:15s} (ORIGINAL)")

            # Restore original authoritative values
            df.at[idx, 'Group'] = orig_class['Group']
            df.at[idx, 'Commodity'] = orig_class['Commodity']
            df.at[idx, 'Cargo'] = orig_class['Cargo']
            df.at[idx, 'Cargo_Detail'] = orig_class['Cargo_Detail']
            df.at[idx, 'Last_Modified'] = '2026-01-14'
            df.at[idx, 'Note'] = 'AUTHORITATIVE - from 01_carrier_scac_cargo.csv - DO NOT EDIT'

            reverted_count += 1

stamp("")
stamp(f"Reverted {reverted_count} carriers to original authoritative classification")

# Save v2.5.2
stamp(f"\nSaving v2.5.2: {OUTPUT_DICT}")
df.to_csv(OUTPUT_DICT, index=False)

stamp("\n=== Dictionary v2.5.2 Complete ===")
stamp("All carrier classifications restored to AUTHORITATIVE original values")
stamp("Future edits: ADD rules only, NEVER edit authoritative classifications")
