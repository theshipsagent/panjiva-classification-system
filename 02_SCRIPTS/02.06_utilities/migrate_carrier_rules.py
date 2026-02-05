"""
Migrate carrier rules from 01_carrier_scac_cargo.csv to cargo_classification_dictionary

Restores the complete carrier classification system that was missing

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
CARRIER_DICT = Path(r"G:\My Drive\LLM\project_manifest\01.01_dictionary\01_carrier_scac_cargo.csv")
CARGO_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.4.0_20260113_2330.csv")
OUTPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.5.0_20260114_0000.csv")

stamp("=== Migrating Carrier Rules from Original Dictionary ===")

# Load both dictionaries
df_carriers = pd.read_csv(CARRIER_DICT, dtype=str)
df_cargo = pd.read_csv(CARGO_DICT, dtype=str)

stamp(f"Loaded {len(df_carriers)} carrier records")
stamp(f"Loaded {len(df_cargo)} cargo dictionary rules")

# Find current max Rule_ID number for CARR- rules
carr_rules = df_cargo[df_cargo['Rule_ID'].str.contains('CARR-', na=False)]
if len(carr_rules) > 0:
    # Extract numbers from existing CARR rules to find next ID
    max_carr = len(carr_rules)
else:
    max_carr = 0

stamp(f"Current CARR rules in dictionary: {max_carr}")

# Process carrier dictionary
new_rules = []
exclude_list = []
skip_list = []

for idx, row in df_carriers.iterrows():
    scac = str(row['Carrier']).strip()
    carrier_name = str(row['Carrier Name']).strip()
    action = str(row['action']).lower().strip()
    group = str(row.get('Group', '')).strip()
    commodity = str(row.get('Commodity', '')).strip()
    cargo = str(row.get('Cargo', '')).strip()
    cargo_detail = str(row.get('CargoDetail', '')).strip()

    # Skip empty rows
    if not scac or scac == 'nan':
        continue

    # Handle exclusions
    if 'exclude' in action or 'always exclude' in action:
        exclude_list.append(f"{scac} ({carrier_name})")
        continue

    # Handle "no matches" / "leave for later stage"
    if 'no matches' in action or 'leave for later stage' in action:
        skip_list.append(f"{scac} ({carrier_name})")
        continue

    # Handle carriers with classification rules
    if group and group != 'nan':
        # Check if this SCAC already exists in cargo dictionary
        existing = df_cargo[df_cargo['Carrier_SCAC'] == scac]
        if len(existing) > 0:
            stamp(f"  SKIP (already exists): {scac} - {carrier_name}")
            continue

        # Create rule ID
        rule_id = f"CARR-{scac}"

        # Build Exclude_Groups based on action text
        exclude_groups = []
        if 'never liquid bulk' in action or 'can never be' in action:
            if 'liquid bulk' in action:
                exclude_groups.append('Liquid Bulk')
            if 'dry bulk' in action:
                exclude_groups.append('Dry Bulk')
            if 'liquified gas' in action or 'liquided gas' in action:
                exclude_groups.append('LPG/LNG')
            if 'roro' in action:
                exclude_groups.append('Ro/Ro')
            if 'reefer' in action:
                exclude_groups.append('Reefer')
            if 'break bulk' in action or 'break-bulk' in action:
                exclude_groups.append('Break-Bulk')

        exclude_groups_str = ';'.join(exclude_groups) if exclude_groups else ''

        # Determine lock behavior
        # Original says "lock from further processing" = lock ALL 4
        # Or for dry bulk: "allow permission to be overwritten only with Break-Bulk" = lock Group only
        lock_all = 'lock from further processing' in action
        lock_group_only = 'allow per ission' in action or 'default dry bulk' in action

        if lock_all:
            lock_group = 'TRUE'
            lock_commodity = 'TRUE'
            lock_cargo = 'TRUE'
            lock_cargo_detail = 'TRUE'
        elif lock_group_only:
            lock_group = 'TRUE'
            lock_commodity = 'FALSE'
            lock_cargo = 'FALSE'
            lock_cargo_detail = 'FALSE'
        else:
            lock_group = 'TRUE'
            lock_commodity = 'FALSE'
            lock_cargo = 'FALSE'
            lock_cargo_detail = 'FALSE'

        # Create rule
        new_rule = {
            'Rule_ID': rule_id,
            'Phase': '2',
            'Priority': '1',
            'Active': 'TRUE',
            'Public': 'TRUE',
            'Private': 'FALSE',
            'Carrier_SCAC': scac,
            'Carrier_Name': carrier_name,
            'Vessel_Type': '',
            'HS2': '',
            'HS4': '',
            'HS6': '',
            'Keywords': '',
            'Exclude_Keywords': '',
            'Exclude_Groups': exclude_groups_str,
            'Min_Tons': '',
            'Max_Tons': '',
            'Group': group,
            'Commodity': commodity,
            'Cargo': cargo,
            'Cargo_Detail': cargo_detail,
            'Lock_Group': lock_group,
            'Lock_Commodity': lock_commodity,
            'Lock_Cargo': lock_cargo,
            'Lock_Cargo_Detail': lock_cargo_detail,
            'Note': f"Migrated from 01_carrier_scac_cargo.csv",
            'Last_Modified': '2026-01-14',
            'Source': 'Carrier Dictionary v2026-01-11'
        }

        new_rules.append(new_rule)
        stamp(f"  ADD: {rule_id:30s} -> {group} > {commodity} > {cargo} > {cargo_detail} (Locks: {'ALL' if lock_all else 'Group only'})")

stamp(f"\n=== Summary ===")
stamp(f"New carrier rules to add: {len(new_rules)}")
stamp(f"Excluded carriers (cruise lines, logistics): {len(exclude_list)}")
stamp(f"Skipped carriers (multi-cargo, later stage): {len(skip_list)}")

# Add new rules to cargo dictionary
if len(new_rules) > 0:
    df_new_rules = pd.DataFrame(new_rules)
    df_combined = pd.concat([df_cargo, df_new_rules], ignore_index=True)

    # Save v2.5.0
    stamp(f"\nSaving v2.5.0: {OUTPUT_DICT}")
    df_combined.to_csv(OUTPUT_DICT, index=False)

    stamp(f"\n=== Dictionary v2.5.0 Complete ===")
    stamp(f"Total rules: {len(df_combined)}")
    stamp(f"Carrier rules (Phase 2): {len(df_combined[df_combined['Phase'] == '2'])}")
else:
    stamp("\nNo new rules to add - all carriers already in dictionary")

# Show excluded carriers for reference
if len(exclude_list) > 0:
    stamp(f"\n=== Excluded Carriers ({len(exclude_list)}) ===")
    for carrier in exclude_list[:10]:
        stamp(f"  {carrier}")
    if len(exclude_list) > 10:
        stamp(f"  ... and {len(exclude_list) - 10} more")

# Show skipped carriers
if len(skip_list) > 0:
    stamp(f"\n=== Skipped Carriers ({len(skip_list)}) - Multi-Cargo ===")
    for carrier in skip_list:
        stamp(f"  {carrier}")
