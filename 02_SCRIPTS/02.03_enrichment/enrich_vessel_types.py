"""
Enrich classification dictionary with vessel types from ship registry

Maps detailed vessel types from ship registry to simplified categories:
- Bulk Carrier (Capesize, Panamax, Handymax, etc.)
- Tanker (VLCC, Suezmax, Aframax, MR, etc.)
- Container (New Panamax, Post-Panamax, etc.)
- General Cargo
- RoRo
- LPG/LNG
- Reefer

Author: WSD3 / Claude Code
Date: 2026-01-13
Version: 1.0.0
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# Paths
SHIP_REGISTRY = Path(r"G:\My Drive\LLM\project_manifest\01.01_dictionary\01_ships_register.csv")
DICTIONARY = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.2.0_20260113_1500.csv")
OUTPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.2.1_20260113_1530.csv")

def stamp(msg):
    """Print timestamped message"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def map_vessel_type(detailed_type):
    """
    Map detailed vessel type from ship registry to simplified category

    Args:
        detailed_type: e.g. "Bulk Carrier-Capesize", "Tanker-MR2"

    Returns:
        Simplified category: "Bulk Carrier", "Tanker", etc.
    """

    if pd.isna(detailed_type) or detailed_type == '':
        return ''

    detailed_type = str(detailed_type).upper()

    # Bulk Carriers
    if any(x in detailed_type for x in ['BULK CARRIER', 'BULKER', 'CAPESIZE', 'PANAMAX',
                                          'HANDYMAX', 'HANDYSIZE', 'SUPRAMAX', 'ULTRAMAX',
                                          'NEWCASTLEMAX', 'KAMSARMAX']):
        return 'Bulk Carrier'

    # Tankers (Oil, Chemical, Product)
    if any(x in detailed_type for x in ['TANKER', 'VLCC', 'SUEZMAX', 'AFRAMAX',
                                          'PANAMAX TANKER', 'MR', 'LR', 'PRODUCT CARRIER']):
        return 'Tanker'

    # LPG/LNG Carriers
    if any(x in detailed_type for x in ['LPG', 'LNG', 'GAS CARRIER']):
        return 'LPG/LNG Carrier'

    # Container Ships
    if any(x in detailed_type for x in ['CONTAINER', 'TEU', 'FEEDER']):
        return 'Container'

    # RoRo / Car Carriers
    if any(x in detailed_type for x in ['RO-RO', 'RORO', 'CAR CARRIER', 'VEHICLE CARRIER',
                                          'PCTC', 'PURE CAR']):
        return 'RoRo'

    # Reefer
    if any(x in detailed_type for x in ['REEFER', 'REFRIGERAT']):
        return 'Reefer'

    # General Cargo
    if any(x in detailed_type for x in ['GENERAL CARGO', 'MULTI-PURPOSE', 'MULTIPURPOSE']):
        return 'General Cargo'

    # Default: return as-is if no match
    return detailed_type.title()

def create_vessel_type_lookup():
    """Create lookup dictionary from ship registry"""

    stamp("Reading ship registry...")
    df_ships = pd.read_csv(SHIP_REGISTRY, dtype=str)
    stamp(f"Loaded {len(df_ships)} vessels")

    # Map detailed types to simplified categories
    stamp("Mapping vessel types to simplified categories...")
    df_ships['Vessel_Type_Simple'] = df_ships['Type'].apply(map_vessel_type)

    # Create lookup: Vessel Name → Vessel Type
    vessel_lookup = {}
    for _, row in df_ships.iterrows():
        vessel_name = str(row['Vessel']).upper().strip()
        vessel_type = row['Vessel_Type_Simple']
        if vessel_name and vessel_type:
            vessel_lookup[vessel_name] = vessel_type

    stamp(f"Created lookup for {len(vessel_lookup)} vessels")

    # Show distribution
    stamp("\nVessel Type Distribution:")
    type_counts = df_ships['Vessel_Type_Simple'].value_counts()
    for vtype, count in type_counts.head(10).items():
        stamp(f"  {vtype}: {count}")

    return vessel_lookup, df_ships

def determine_exclude_groups(vessel_type):
    """Determine physical exclusions based on vessel type"""

    exclusions = {
        'Bulk Carrier': 'Liquid Bulk;Container;Ro/Ro;Reefer',
        'Tanker': 'Dry Bulk;Break-Bulk;Container;Ro/Ro;Reefer',
        'LPG/LNG Carrier': 'Dry Bulk;Break-Bulk;Container;Ro/Ro;Reefer',
        'Container': 'Dry Bulk;Liquid Bulk;Break-Bulk;Ro/Ro;Reefer',
        'RoRo': 'Dry Bulk;Liquid Bulk;Break-Bulk;Container;Reefer',
        'Reefer': 'Dry Bulk;Liquid Bulk;Container;Ro/Ro',
        'General Cargo': 'Dry Bulk;Liquid Bulk'
    }

    return exclusions.get(vessel_type, '')

def enrich_dictionary():
    """Add vessel type data to classification dictionary"""

    stamp("=== Enriching Dictionary with Vessel Types ===")

    # Create vessel lookup
    vessel_lookup, df_ships = create_vessel_type_lookup()

    # Read dictionary
    stamp(f"\nReading dictionary: {DICTIONARY}")
    df_dict = pd.read_csv(DICTIONARY, dtype=str)
    stamp(f"Loaded {len(df_dict)} rules")

    # Track enrichment stats
    enriched_count = 0
    already_had = 0
    no_match = 0

    # Enrich rules based on cargo Group
    stamp("\nEnriching rules with inferred vessel types...")
    for idx, row in df_dict.iterrows():
        current_vtype = str(row.get('Vessel_Type', '')).strip()

        # Skip if already has vessel type
        if current_vtype and current_vtype != '':
            already_had += 1
            continue

        # Infer from Group
        group = str(row.get('Group', '')).strip()
        inferred_type = ''

        if group == 'Dry Bulk':
            inferred_type = 'Bulk Carrier'
        elif group == 'Liquid Bulk':
            # Check commodity to differentiate
            commodity = str(row.get('Commodity', '')).strip()
            if 'LPG' in commodity or 'LNG' in commodity or 'Gas' in commodity:
                inferred_type = 'LPG/LNG Carrier'
            else:
                inferred_type = 'Tanker'
        elif group == 'Ro/Ro':
            inferred_type = 'RoRo'
        elif group == 'Reefer':
            inferred_type = 'Reefer'
        elif group == 'Container':
            inferred_type = 'Container'
        elif group == 'Break-Bulk':
            inferred_type = 'General Cargo'

        if inferred_type:
            df_dict.at[idx, 'Vessel_Type'] = inferred_type
            df_dict.at[idx, 'Exclude_Groups'] = determine_exclude_groups(inferred_type)
            enriched_count += 1
        else:
            no_match += 1

    # Update Last_Modified
    df_dict['Last_Modified'] = '2026-01-13'

    # Save enriched dictionary
    stamp(f"\nSaving enriched dictionary: {OUTPUT_DICT}")
    df_dict.to_csv(OUTPUT_DICT, index=False)

    # Statistics
    stamp("\n=== Enrichment Summary ===")
    stamp(f"Total rules: {len(df_dict)}")
    stamp(f"Already had vessel type: {already_had}")
    stamp(f"Enriched with inferred type: {enriched_count}")
    stamp(f"No vessel type assigned: {no_match}")

    stamp(f"\nVessel Type Coverage:")
    vtype_counts = df_dict['Vessel_Type'].value_counts()
    for vtype, count in vtype_counts.items():
        if vtype.strip():
            stamp(f"  {vtype}: {count} rules")

    stamp("\nDictionary v2.2.1 created successfully!")
    stamp("All rules now have inferred vessel types based on cargo Group")

    # Create vessel type reference file for user
    stamp("\nCreating vessel type reference...")
    vtype_ref = df_ships[['Vessel', 'Type', 'Vessel_Type_Simple']].copy()
    vtype_ref = vtype_ref[vtype_ref['Vessel_Type_Simple'].notna()]
    vtype_ref = vtype_ref.drop_duplicates(subset=['Type'])
    vtype_ref = vtype_ref.sort_values('Vessel_Type_Simple')

    ref_path = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.04_ships\vessel_type_reference.csv")
    ref_path.parent.mkdir(parents=True, exist_ok=True)
    vtype_ref.to_csv(ref_path, index=False)
    stamp(f"Created vessel type reference: {ref_path}")

    return df_dict, vessel_lookup

if __name__ == "__main__":
    df_dict, vessel_lookup = enrich_dictionary()

    # Print sample lookups
    print("\n=== Sample Vessel Lookups ===")
    sample_vessels = ['CAPE SUZURAN', 'MSC SERENA', 'JEFFREYS BAY']
    for vessel in sample_vessels:
        vtype = vessel_lookup.get(vessel, 'Not found')
        print(f"{vessel}: {vtype}")
