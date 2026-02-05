"""
Fix carrier codes in dictionary to use proper SCAC format

Changes:
- Add new column: Carrier_SCAC (4-char code for matching)
- Update Carrier_Name to full format from raw data
- Map existing carrier rules to SCAC codes

Author: WSD3 / Claude Code
Date: 2026-01-13
Version: 1.0.0
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# Paths
SCAC_FILE = Path(r"G:\My Drive\LLM\project_manifest\01.01_dictionary\01_carrier_scac_cargo.csv")
DICTIONARY = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.2.1_20260113_1530.csv")
OUTPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.3.0_20260113_1545.csv")

def stamp(msg):
    """Print timestamped message"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def create_scac_mapping():
    """Create SCAC code to full name mapping from reference file"""

    stamp("Reading SCAC carrier file...")
    df_scac = pd.read_csv(SCAC_FILE, dtype=str)
    stamp(f"Loaded {len(df_scac)} SCAC carriers")

    # Create mapping: Partial name → (SCAC, Full Name)
    scac_map = {}

    for _, row in df_scac.iterrows():
        scac = str(row['Carrier']).strip()
        full_name = str(row['Carrier Name']).strip()

        # Create searchable variations
        # WLWH → Wallenius Wilhelmsen Logistics Americas Llc
        scac_map[scac] = full_name

        # Also map short names for matching
        if 'WALLENIUS' in full_name.upper():
            scac_map['WALLENIUS'] = (scac, full_name)
        if 'HOEGH' in full_name.upper() or 'HÖEGH' in full_name.upper():
            scac_map['HOEGH'] = (scac, full_name)
            scac_map['HÖEGH'] = (scac, full_name)
        if 'EUKOR' in full_name.upper():
            scac_map['EUKOR'] = (scac, full_name)
        if 'NYK' in full_name.upper() and 'GROUP' in full_name.upper():
            scac_map['NYK'] = (scac, full_name)
        if 'MOL' in full_name.upper() or 'MITSUI O S K' in full_name.upper():
            scac_map['MOL'] = (scac, full_name)
        if 'K LINE' in full_name.upper() or 'KAWASAKI KISEN' in full_name.upper():
            scac_map['K LINE'] = (scac, full_name)
        if 'COOL CARRIERS' in full_name.upper():
            scac_map['COOL CARRIERS'] = (scac, full_name)
        if 'STOLT' in full_name.upper():
            scac_map['STOLT'] = (scac, full_name)
        if 'ODFJELL' in full_name.upper():
            scac_map['ODFJELL'] = (scac, full_name)
        if 'SEATRADE' in full_name.upper():
            scac_map['SEATRADE'] = (scac, full_name)
        if 'DOLE' in full_name.upper():
            scac_map['DOLE'] = (scac, full_name)
        # WWL is same as WALLENIUS
        if scac == 'WLWH':
            scac_map['WWL'] = (scac, full_name)

    stamp(f"Created SCAC mapping for {len(scac_map)} carriers")
    return scac_map

def fix_carrier_codes():
    """Update dictionary with proper SCAC codes"""

    stamp("=== Fixing Carrier Codes to SCAC Format ===")

    # Create SCAC mapping
    scac_map = create_scac_mapping()

    # Read dictionary
    stamp(f"\nReading dictionary: {DICTIONARY}")
    df_dict = pd.read_csv(DICTIONARY, dtype=str)
    stamp(f"Loaded {len(df_dict)} rules")

    # Add new column after Carrier_Name
    stamp("\nAdding Carrier_SCAC column...")

    # Find position of Carrier_Name column
    cols = df_dict.columns.tolist()
    carrier_name_idx = cols.index('Carrier_Name')

    # Insert new column
    df_dict.insert(carrier_name_idx, 'Carrier_SCAC', '')

    # Update carrier rules
    stamp("\nUpdating carrier rules with SCAC codes...")
    fixed_count = 0
    not_found = []

    for idx, row in df_dict.iterrows():
        carrier_name = str(row.get('Carrier_Name', '')).strip()

        if not carrier_name or carrier_name == '':
            continue

        # Try to find SCAC mapping
        scac = None
        full_name = None

        # Check if already in SCAC format
        if carrier_name in scac_map and isinstance(scac_map[carrier_name], tuple):
            scac, full_name = scac_map[carrier_name]
        # Check for partial match
        else:
            for key, value in scac_map.items():
                if isinstance(value, tuple) and key.upper() in carrier_name.upper():
                    scac, full_name = value
                    break

        if scac and full_name:
            df_dict.at[idx, 'Carrier_SCAC'] = scac
            df_dict.at[idx, 'Carrier_Name'] = full_name
            df_dict.at[idx, 'Last_Modified'] = '2026-01-13'
            fixed_count += 1
            stamp(f"  Fixed: {carrier_name} -> SCAC: {scac}, Name: {full_name}")
        else:
            not_found.append(carrier_name)
            stamp(f"  NOT FOUND: {carrier_name}")

    # Update Keywords column to include SCAC for matching
    stamp("\nUpdating Keywords to include SCAC codes...")
    for idx, row in df_dict.iterrows():
        scac = str(row.get('Carrier_SCAC', '')).strip()
        keywords = str(row.get('Keywords', '')).strip()

        if scac and scac not in keywords:
            # Add SCAC to keywords
            if keywords:
                df_dict.at[idx, 'Keywords'] = f"{scac};{keywords}"
            else:
                df_dict.at[idx, 'Keywords'] = scac

    # Column order for v2.3.0 (new column added)
    column_order = [
        'Rule_ID', 'Phase', 'Tier', 'Active', 'Lock_Classification', 'Override_HS',
        'Carrier_SCAC', 'Carrier_Name', 'Package_Type', 'Vessel_Type', 'Exclude_Groups',
        'HS2', 'HS4', 'HS6',
        'Keywords', 'Exclude_Keywords', 'Min_Tons', 'Max_Tons',
        'Port_Filter', 'Country_Filter',
        'Lock_Group', 'Lock_Commodity', 'Lock_Cargo', 'Lock_Cargo_Detail',
        'Group', 'Commodity', 'Cargo', 'Cargo_Detail', 'Filter',
        'Note', 'Accuracy_Est', 'Tonnage_Impact', 'Date_Added', 'Last_Modified'
    ]

    df_dict = df_dict[column_order]

    # Save v2.3.0
    stamp(f"\nSaving v2.3.0: {OUTPUT_DICT}")
    df_dict.to_csv(OUTPUT_DICT, index=False)

    # Statistics
    stamp("\n=== Fix Summary ===")
    stamp(f"Total rules: {len(df_dict)}")
    stamp(f"Carrier rules fixed: {fixed_count}")
    stamp(f"Carriers not found: {len(not_found)}")

    if not_found:
        stamp("\nCarriers not found in SCAC file:")
        for carrier in not_found:
            stamp(f"  - {carrier}")

    stamp("\n=== Dictionary v2.3.0 Statistics ===")
    stamp(f"Total rules: {len(df_dict)}")
    stamp(f"Rules with SCAC: {len(df_dict[df_dict['Carrier_SCAC'].notna() & (df_dict['Carrier_SCAC'] != '')])}")

    stamp("\nDictionary v2.3.0 created successfully!")
    stamp("New features:")
    stamp("  - Carrier_SCAC column added (4-char code)")
    stamp("  - Carrier_Name updated to full format")
    stamp("  - Keywords include SCAC codes for matching")

    # Show sample carrier rules
    stamp("\n=== Sample Carrier Rules ===")
    carrier_rules = df_dict[df_dict['Carrier_SCAC'].notna() & (df_dict['Carrier_SCAC'] != '')]
    for _, row in carrier_rules.head(5).iterrows():
        stamp(f"{row['Rule_ID']}: SCAC={row['Carrier_SCAC']}, Name={row['Carrier_Name'][:50]}...")

    return df_dict

if __name__ == "__main__":
    df = fix_carrier_codes()
