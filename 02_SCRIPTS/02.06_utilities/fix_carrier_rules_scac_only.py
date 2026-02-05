"""
Fix carrier rules to match SCAC ONLY (no vessel type, no keywords)

Carrier shortcuts:
- WLWH → RoRo (2,021 records)
- HOEG → RoRo (453 records)
- EUKO → RoRo (237 records)
- NYKS → Break-Bulk Steel (304 records)
- etc.

Match ONLY on Carrier_SCAC, lock all 4 columns, done!
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# Paths
INPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.3.0_20260113_1545.csv")
OUTPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.3.1_20260113_2030.csv")

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

stamp("=== Fixing Carrier Rules (SCAC Only Matching) ===")

# Load dictionary
stamp(f"Reading: {INPUT_DICT}")
df = pd.read_csv(INPUT_DICT, dtype=str)
stamp(f"Loaded {len(df)} rules")

# Find carrier rules
carrier_rules = df['Carrier_SCAC'].notna() & (df['Carrier_SCAC'] != '')
carrier_count = carrier_rules.sum()
stamp(f"Found {carrier_count} carrier rules")

# Clear Vessel_Type and Keywords for carrier rules
stamp("\nClearing Vessel_Type and Keywords from carrier rules...")
stamp("(Carrier SCAC matching only)")

for idx in df[carrier_rules].index:
    old_vtype = df.at[idx, 'Vessel_Type']
    old_keywords = df.at[idx, 'Keywords']

    # Clear Vessel_Type and Keywords - match SCAC ONLY
    # (Vessel_Type will be set by Phase 1 vessel rules anyway)
    df.at[idx, 'Vessel_Type'] = ''
    df.at[idx, 'Keywords'] = ''
    df.at[idx, 'Last_Modified'] = '2026-01-13'

    stamp(f"  {df.at[idx, 'Rule_ID']}")
    stamp(f"    Cleared: Vessel_Type (was: {old_vtype})")
    stamp(f"    Cleared: Keywords (was: {old_keywords})")
    stamp(f"    Match: SCAC {df.at[idx, 'Carrier_SCAC']} ONLY")

# Save v2.3.1
stamp(f"\nSaving v2.3.1: {OUTPUT_DICT}")
df.to_csv(OUTPUT_DICT, index=False)

stamp("\n=== Dictionary v2.3.1 Complete ===")
stamp("Carrier rules now match SCAC ONLY")
stamp("No vessel type or keyword requirements")
stamp("All 4 taxonomy levels locked on match")

# Show updated carrier rules
stamp("\n=== Updated Carrier Rules ===")
carrier_rules_updated = df[df['Carrier_SCAC'].notna() & (df['Carrier_SCAC'] != '')]
for _, row in carrier_rules_updated.iterrows():
    stamp(f"{row['Rule_ID']:30s} SCAC: {row['Carrier_SCAC']:6s} -> {row['Group']} > {row['Commodity']} > {row['Cargo']} > {row['Cargo_Detail']}")

stamp(f"\nReady to re-test!")
