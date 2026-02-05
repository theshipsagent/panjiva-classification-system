"""
Fix vehicle carrier rules - change Group from "Break Bulk" to "Ro/Ro"

Vehicle carriers (PCTCs) should be classified as Ro/Ro, not Break Bulk

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
INPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.5.0_20260114_0000.csv")
OUTPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.5.1_20260114_0030.csv")

stamp("=== Fixing Vehicle Carrier Group Classifications ===")

# Load dictionary
df = pd.read_csv(INPUT_DICT, dtype=str)

# Vehicle carriers that need fixing
vehicle_carriers = [
    'KKLU', 'MOLU', 'AROF', 'ACLU', 'NMCC', 'HDGL',
    'VWTG', 'GESM', 'NMTE', 'PSGP', 'MCGQ', 'TGBS', 'GDSL'
]

stamp(f"Fixing {len(vehicle_carriers)} vehicle carrier rules")

fixed_count = 0
for scac in vehicle_carriers:
    mask = df['Carrier_SCAC'] == scac
    if mask.sum() > 0:
        idx = df[mask].index[0]
        old_group = df.at[idx, 'Group']
        old_commodity = df.at[idx, 'Commodity']

        # Update to Ro/Ro > Vehicles > Motor Vehicles > Vehicles
        df.at[idx, 'Group'] = 'Ro/Ro'
        df.at[idx, 'Commodity'] = 'Vehicles'
        df.at[idx, 'Cargo'] = 'Motor Vehicles'
        df.at[idx, 'Cargo_Detail'] = 'Vehicles'
        df.at[idx, 'Last_Modified'] = '2026-01-14'

        stamp(f"  {scac:6s}: {old_group:15s} -> Ro/Ro")
        fixed_count += 1

stamp(f"\nFixed {fixed_count} vehicle carrier rules")

# Save v2.5.1
stamp(f"Saving v2.5.1: {OUTPUT_DICT}")
df.to_csv(OUTPUT_DICT, index=False)

stamp("\n=== Dictionary v2.5.1 Complete ===")
stamp("Vehicle carriers now match Phase 1 vessel type classification")
