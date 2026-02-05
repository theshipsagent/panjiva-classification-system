"""
Upgrade cargo dictionary v2.1.0 to v2.2.0
Adds granular column-level locking and vessel type matching

Author: WSD3 / Claude Code
Date: 2026-01-13
Version: 1.0.0

New Features in v2.2.0:
- Column-level locking (Lock_Group, Lock_Commodity, Lock_Cargo, Lock_Cargo_Detail)
- Vessel type matching
- Physical constraint validation (Exclude_Groups)
- Progressive record exclusion for performance
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# Paths
INPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.1.0_20260113_1445.csv")
OUTPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.2.0_20260113_1500.csv")

def stamp(msg):
    """Print timestamped message"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def determine_lock_levels(row):
    """
    Determine which taxonomy levels should be locked based on rule characteristics

    Returns: (lock_group, lock_commodity, lock_cargo, lock_cargo_detail)
    """

    phase = int(row.get('Phase', 7))
    tier = int(row.get('Tier', 3))
    rule_id = str(row.get('Rule_ID', ''))
    lock_class = str(row.get('Lock_Classification', 'FALSE')).upper()

    # TIER 1 CARRIER LOCKS - Lock all 4 levels if Lock_Classification=TRUE
    if tier == 1 and lock_class == 'TRUE':
        return True, True, True, True

    # TIER 1 CARRIER LOCKS - Lock only Group if Lock_Classification=FALSE (allow refinement)
    if tier == 1 and lock_class == 'FALSE':
        return True, False, False, False

    # PHASE 2: Carrier/vessel type - lock Group only (allow later refinement)
    if phase == 2:
        return True, False, False, False

    # PHASE 4: HS2 - lock Group + Commodity
    if phase == 4:
        return True, True, False, False

    # PHASE 5: HS4 - lock Group + Commodity + Cargo
    if phase == 5:
        return True, True, True, False

    # PHASE 6: HS6 - lock Group + Commodity + Cargo (allow Cargo_Detail refinement)
    if phase == 6:
        return True, True, True, False

    # PHASE 7: Keywords only - lock Group + Commodity
    if phase == 7:
        return True, True, False, False

    # PHASE 8-9: Combinatorial - lock all 4 (final classification)
    if phase in [8, 9]:
        return True, True, True, True

    # PHASE 10: Specific grades - lock all 4 (highly specific)
    if phase == 10:
        return True, True, True, True

    # Default: lock nothing (shouldn't happen)
    return False, False, False, False

def determine_vessel_type(row):
    """Determine vessel type from carrier name or cargo type"""

    carrier = str(row.get('Carrier_Name', '')).upper()
    group = str(row.get('Group', '')).upper()
    commodity = str(row.get('Commodity', '')).upper()

    # RoRo carriers
    if any(x in carrier for x in ['WALLENIUS', 'WWL', 'HOEGH', 'EUKOR']):
        return 'RoRo'

    # Chemical tankers
    if any(x in carrier for x in ['STOLT', 'ODFJELL']):
        return 'Tanker'

    # Reefer ships
    if any(x in carrier for x in ['COOL CARRIERS', 'SEATRADE', 'DOLE']):
        return 'Reefer'

    # Steel carriers (general cargo/break bulk)
    if any(x in carrier for x in ['NYK', 'MOL', 'K LINE']):
        return 'General Cargo'

    # Infer from Group
    if 'LIQUID BULK' in group:
        return 'Tanker'
    elif 'DRY BULK' in group:
        return 'Bulk Carrier'
    elif 'RO/RO' in group:
        return 'RoRo'
    elif 'REEFER' in group:
        return 'Reefer'
    elif 'BREAK-BULK' in group:
        return 'General Cargo'
    elif 'CONTAINER' in group:
        return 'Container'

    return ''  # Unknown

def determine_exclude_groups(vessel_type):
    """
    Determine which cargo Groups are physically impossible for this vessel type

    Physical constraints:
    - Bulk Carrier: Can ONLY carry Dry Bulk or Break-Bulk (NEVER Liquid Bulk, Container, RoRo, Reefer)
    - Tanker: Can ONLY carry Liquid Bulk (NEVER Dry Bulk, Container, RoRo, Reefer, Break-Bulk)
    - Container: Can ONLY carry Container (NEVER bulk)
    - RoRo: Can ONLY carry RoRo (NEVER bulk or container)
    - Reefer: Can carry Reefer or Break-Bulk (NEVER bulk)
    - General Cargo: Can carry Break-Bulk, some containers (NEVER pure bulk)
    """

    exclusions = {
        'Bulk Carrier': 'Liquid Bulk;Container;Ro/Ro;Reefer',
        'Tanker': 'Dry Bulk;Break-Bulk;Container;Ro/Ro;Reefer',
        'Container': 'Dry Bulk;Liquid Bulk;Break-Bulk;Ro/Ro;Reefer',
        'RoRo': 'Dry Bulk;Liquid Bulk;Break-Bulk;Container;Reefer',
        'Reefer': 'Dry Bulk;Liquid Bulk;Container;Ro/Ro',
        'General Cargo': 'Dry Bulk;Liquid Bulk'
    }

    return exclusions.get(vessel_type, '')

def create_vessel_type_rules():
    """Create Phase 1 vessel type rules (highest priority after filters)"""

    vessel_rules = [
        # Bulk Carriers - Lock Group only
        {
            'Rule_ID': 'VTYPE-BULK-CARRIER',
            'Phase': 1,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'FALSE',  # Allow refinement
            'Override_HS': 'FALSE',
            'Carrier_Name': '',
            'Package_Type': '',
            'HS2': '',
            'HS4': '',
            'HS6': '',
            'Keywords': '',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Vessel_Type': 'Bulk Carrier;Bulker;Dry Bulk Carrier',
            'Exclude_Groups': 'Liquid Bulk;Container;Ro/Ro;Reefer',
            'Lock_Group': 'TRUE',
            'Lock_Commodity': 'FALSE',
            'Lock_Cargo': 'FALSE',
            'Lock_Cargo_Detail': 'FALSE',
            'Group': 'Dry Bulk',
            'Commodity': 'TBN',
            'Cargo': 'TBN',
            'Cargo_Detail': 'TBN',
            'Filter': '',
            'Note': 'Vessel type: Bulk Carrier can only carry Dry Bulk or Break-Bulk',
            'Accuracy_Est': '100%',
            'Tonnage_Impact': 'Very High',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        },
        # Tankers - Lock Group only
        {
            'Rule_ID': 'VTYPE-TANKER',
            'Phase': 1,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'FALSE',
            'Override_HS': 'FALSE',
            'Carrier_Name': '',
            'Package_Type': '',
            'HS2': '',
            'HS4': '',
            'HS6': '',
            'Keywords': '',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Vessel_Type': 'Tanker;Oil Tanker;Chemical Tanker;Product Tanker',
            'Exclude_Groups': 'Dry Bulk;Break-Bulk;Container;Ro/Ro;Reefer',
            'Lock_Group': 'TRUE',
            'Lock_Commodity': 'FALSE',
            'Lock_Cargo': 'FALSE',
            'Lock_Cargo_Detail': 'FALSE',
            'Group': 'Liquid Bulk',
            'Commodity': 'TBN',
            'Cargo': 'TBN',
            'Cargo_Detail': 'TBN',
            'Filter': '',
            'Note': 'Vessel type: Tanker can only carry Liquid Bulk',
            'Accuracy_Est': '100%',
            'Tonnage_Impact': 'Very High',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        },
        # RoRo vessels - Lock all 4 (very specific)
        {
            'Rule_ID': 'VTYPE-RORO',
            'Phase': 1,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'TRUE',  # 100% certain
            'Override_HS': 'FALSE',
            'Carrier_Name': '',
            'Package_Type': '',
            'HS2': '',
            'HS4': '',
            'HS6': '',
            'Keywords': '',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Vessel_Type': 'RoRo;Vehicle Carrier;Car Carrier',
            'Exclude_Groups': 'Dry Bulk;Liquid Bulk;Break-Bulk;Container;Reefer',
            'Lock_Group': 'TRUE',
            'Lock_Commodity': 'TRUE',
            'Lock_Cargo': 'TRUE',
            'Lock_Cargo_Detail': 'TRUE',
            'Group': 'Ro/Ro',
            'Commodity': 'Vehicles',
            'Cargo': 'Motor Vehicles',
            'Cargo_Detail': 'Vehicles',
            'Filter': '',
            'Note': 'Vessel type: RoRo can only carry vehicles',
            'Accuracy_Est': '100%',
            'Tonnage_Impact': 'Very High',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        },
        # Reefer vessels - Lock Group only
        {
            'Rule_ID': 'VTYPE-REEFER',
            'Phase': 1,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'FALSE',
            'Override_HS': 'FALSE',
            'Carrier_Name': '',
            'Package_Type': '',
            'HS2': '',
            'HS4': '',
            'HS6': '',
            'Keywords': '',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Vessel_Type': 'Reefer;Refrigerated Cargo Ship',
            'Exclude_Groups': 'Dry Bulk;Liquid Bulk;Container;Ro/Ro',
            'Lock_Group': 'TRUE',
            'Lock_Commodity': 'FALSE',
            'Lock_Cargo': 'FALSE',
            'Lock_Cargo_Detail': 'FALSE',
            'Group': 'Reefer',
            'Commodity': 'TBN',
            'Cargo': 'TBN',
            'Cargo_Detail': 'TBN',
            'Filter': '',
            'Note': 'Vessel type: Reefer carries refrigerated products',
            'Accuracy_Est': '100%',
            'Tonnage_Impact': 'High',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        }
    ]

    return vessel_rules

def upgrade_dictionary():
    """Main upgrade function"""

    stamp("=== Upgrading Dictionary v2.1.0 to v2.2.0 ===")

    # Read v2.1.0
    stamp(f"Reading v2.1.0: {INPUT_DICT}")
    df_old = pd.read_csv(INPUT_DICT, dtype=str)
    stamp(f"Loaded {len(df_old)} rules")

    # Add new columns
    stamp("\nAdding new v2.2.0 columns...")

    # Granular locking columns
    df_old['Lock_Group'] = ''
    df_old['Lock_Commodity'] = ''
    df_old['Lock_Cargo'] = ''
    df_old['Lock_Cargo_Detail'] = ''

    # Vessel type matching
    df_old['Vessel_Type'] = ''
    df_old['Exclude_Groups'] = ''

    # Determine lock levels for each rule
    stamp("Setting lock levels based on Phase/Tier...")
    for idx, row in df_old.iterrows():
        lock_g, lock_c, lock_cg, lock_cd = determine_lock_levels(row)
        df_old.at[idx, 'Lock_Group'] = 'TRUE' if lock_g else 'FALSE'
        df_old.at[idx, 'Lock_Commodity'] = 'TRUE' if lock_c else 'FALSE'
        df_old.at[idx, 'Lock_Cargo'] = 'TRUE' if lock_cg else 'FALSE'
        df_old.at[idx, 'Lock_Cargo_Detail'] = 'TRUE' if lock_cd else 'FALSE'

        # Set vessel type and exclusions
        vessel_type = determine_vessel_type(row)
        df_old.at[idx, 'Vessel_Type'] = vessel_type
        df_old.at[idx, 'Exclude_Groups'] = determine_exclude_groups(vessel_type)

    # Create vessel type rules
    stamp("\nCreating vessel type rules (Phase 1)...")
    vessel_rules = create_vessel_type_rules()
    df_vessels = pd.DataFrame(vessel_rules)
    stamp(f"Created {len(df_vessels)} vessel type rules")

    # Combine: Vessel rules first (Phase 1), then existing rules
    df_new = pd.concat([df_vessels, df_old], ignore_index=True)

    # Column order for v2.2.0
    column_order = [
        'Rule_ID', 'Phase', 'Tier', 'Active', 'Lock_Classification', 'Override_HS',
        'Carrier_Name', 'Package_Type', 'Vessel_Type', 'Exclude_Groups',
        'HS2', 'HS4', 'HS6',
        'Keywords', 'Exclude_Keywords', 'Min_Tons', 'Max_Tons',
        'Port_Filter', 'Country_Filter',
        'Lock_Group', 'Lock_Commodity', 'Lock_Cargo', 'Lock_Cargo_Detail',
        'Group', 'Commodity', 'Cargo', 'Cargo_Detail', 'Filter',
        'Note', 'Accuracy_Est', 'Tonnage_Impact', 'Date_Added', 'Last_Modified'
    ]

    df_new = df_new[column_order]

    # Update Last_Modified for all rules
    df_new['Last_Modified'] = '2026-01-13'

    # Save v2.2.0
    stamp(f"\nSaving v2.2.0: {OUTPUT_DICT}")
    df_new.to_csv(OUTPUT_DICT, index=False)

    # Statistics
    stamp("\n=== Dictionary v2.2.0 Statistics ===")
    stamp(f"Total rules: {len(df_new)}")

    stamp(f"\nRules by Phase:")
    for phase in sorted(df_new['Phase'].astype(int).unique()):
        count = len(df_new[df_new['Phase'].astype(int) == phase])
        stamp(f"  Phase {phase}: {count} rules")

    stamp(f"\nLock Level Distribution:")
    lock_levels = []
    for _, row in df_new.iterrows():
        locked = sum([
            row['Lock_Group'] == 'TRUE',
            row['Lock_Commodity'] == 'TRUE',
            row['Lock_Cargo'] == 'TRUE',
            row['Lock_Cargo_Detail'] == 'TRUE'
        ])
        lock_levels.append(locked)

    for level in range(5):
        count = lock_levels.count(level)
        if count > 0:
            stamp(f"  {level} columns locked: {count} rules")

    stamp(f"\nVessel Type Rules:")
    vtype_count = len(df_new[df_new['Vessel_Type'] != ''])
    stamp(f"  Rules with vessel type: {vtype_count}")

    stamp("\nDictionary v2.2.0 created successfully!")
    stamp("New features:")
    stamp("  - Column-level locking (Lock_Group, Lock_Commodity, Lock_Cargo, Lock_Cargo_Detail)")
    stamp("  - Vessel type matching")
    stamp("  - Physical constraint validation (Exclude_Groups)")
    stamp("  - Progressive record exclusion for performance")

    return df_new

if __name__ == "__main__":
    df = upgrade_dictionary()
