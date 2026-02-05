"""
Remove HS code requirements from carrier rules

Carrier rules should match SCAC ONLY - no HS codes, no vessel type, no keywords

Author: WSD3 / Claude Code
Date: 2026-01-13
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# Paths
INPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.3.2_20260113_2300.csv")
OUTPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.4.0_20260113_2330.csv")

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

stamp("=== Removing HS Code Requirements from Carrier Rules ===")

# Load dictionary
df = pd.read_csv(INPUT_DICT, dtype=str)

# Find carrier rules
carrier_rules = df['Carrier_SCAC'].notna() & (df['Carrier_SCAC'] != '')
carrier_count = carrier_rules.sum()
stamp(f"Found {carrier_count} carrier rules")

# Clear HS codes from carrier rules
stamp("\nClearing HS2, HS4, HS6 from carrier rules...")
for idx in df[carrier_rules].index:
    old_hs2 = df.at[idx, 'HS2']
    old_hs4 = df.at[idx, 'HS4']
    old_hs6 = df.at[idx, 'HS6']

    # Clear HS codes
    df.at[idx, 'HS2'] = ''
    df.at[idx, 'HS4'] = ''
    df.at[idx, 'HS6'] = ''
    df.at[idx, 'Last_Modified'] = '2026-01-13'

    if pd.notna(old_hs2) or pd.notna(old_hs4) or pd.notna(old_hs6):
        stamp(f"  {df.at[idx, 'Rule_ID']}")
        stamp(f"    Cleared: HS2={old_hs2}, HS4={old_hs4}, HS6={old_hs6}")

# Save v2.4.0
stamp(f"\nSaving v2.4.0: {OUTPUT_DICT}")
df.to_csv(OUTPUT_DICT, index=False)

stamp("\n=== Dictionary v2.4.0 Complete ===")
stamp("Carrier rules now match SCAC ONLY")
stamp("No HS codes, no vessel type, no keywords")
stamp("Pure carrier-based classification shortcuts")

# Show updated rules
stamp("\n=== Updated Carrier Rules ===")
carrier_rules_updated = df[df['Carrier_SCAC'].notna() & (df['Carrier_SCAC'] != '')]
for _, row in carrier_rules_updated.iterrows():
    stamp(f"{row['Rule_ID']:30s} SCAC: {row['Carrier_SCAC']:6s} -> {row['Group']} > {row['Commodity']} > {row['Cargo']} > {row['Cargo_Detail']}")

stamp(f"\nReady to re-test - expecting 2,021 WLWH matches!")
