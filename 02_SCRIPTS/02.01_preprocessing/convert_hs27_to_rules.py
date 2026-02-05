"""
Convert HS27 mineral fuels user edits to production dictionary format

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def convert_to_dictionary_rules(df_specialized, phase, note_prefix):
    """Convert specialized dictionary to production rule format"""

    rules = []

    for idx, row in df_specialized.iterrows():
        # Generate Rule_ID
        rule_id = f"HS4-{row['HS4']}"

        # Get keywords
        key_phrases = str(row.get('Key_Phrases', ''))
        primary_kw = str(row.get('Primary_Keywords', ''))
        descriptor_kw = str(row.get('Descriptor_Keywords', ''))

        # Determine match strategy
        # Crude Oil, Coal, Petcoke, LNG have specific phrases
        if key_phrases and key_phrases != 'nan':
            if any(term in key_phrases.upper() for term in ['CRUDE OIL', 'PETCOKE', 'COAL', 'LNG', 'BITUMEN']):
                match_strategy = 'PHRASE_REQUIRED'
            else:
                match_strategy = 'PRIMARY_SUFFICIENT'
        else:
            match_strategy = 'PRIMARY_SUFFICIENT'

        # Build rule record
        rule = {
            'Rule_ID': rule_id,
            'Phase': phase,
            'Tier': '',
            'Active': 'TRUE',
            'Lock_Classification': '',
            'Override_HS': '',
            'Carrier_SCAC': '',
            'Carrier_Name': '',
            'Package_Type': row.get('Top_Package_Types', ''),
            'Vessel_Type': '',
            'Exclude_Groups': '',
            'HS2': row['HS2'],
            'HS4': row['HS4'],
            'HS6': '',
            'Keywords': '',  # Old column - leave empty
            'Key_Phrases': key_phrases if key_phrases != 'nan' else '',
            'Primary_Keywords': primary_kw if primary_kw != 'nan' else '',
            'Descriptor_Keywords': descriptor_kw if descriptor_kw != 'nan' else '',
            'Match_Strategy': match_strategy,
            'Exclude_Keywords': '',
            'Min_Tons': str(row.get('Min_Tons', '')) if pd.notna(row.get('Min_Tons')) else '',
            'Max_Tons': str(row.get('Max_Tons', '')) if pd.notna(row.get('Max_Tons')) else '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Lock_Group': 'TRUE',
            'Lock_Commodity': 'TRUE',
            'Lock_Cargo': 'TRUE',
            'Lock_Cargo_Detail': 'TRUE',
            'Group': str(row.get('Classification_Group', '')),
            'Commodity': str(row.get('Commodity', '')),
            'Cargo': str(row.get('Cargo', '')),
            'Cargo_Detail': str(row.get('Cargo_Detail', '')),
            'Filter': '',
            'Note': f"{note_prefix} - {row['HTS_Description'][:50]}",
            'Accuracy_Est': '',
            'Tonnage_Impact': '',
            'Date_Added': datetime.now().strftime('%m/%d/%Y'),
            'Last_Modified': datetime.now().strftime('%m/%d/%Y'),
            'Priority': '1',
            'Public': 'FALSE',
            'Private': 'FALSE',
            'Source': 'User-edited specialized dictionary',
            'HS4_Description': row['HTS_Description']
        }

        rules.append(rule)

    return pd.DataFrame(rules)

# Paths
HS27_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_hs27_mineral_fuels_user_edits_011426_1620.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_rules_DRAFT_hs27_mineral_fuels.csv")

stamp("=== Convert HS27 Mineral Fuels User Edits to Rules ===")
stamp("")

# Load user-edited file
stamp("Loading HS27 mineral fuels...")
df_hs27 = pd.read_csv(HS27_FILE, dtype=str)
stamp(f"  Entries: {len(df_hs27)}")

# Show breakdown
stamp("")
stamp("Breakdown by Group:")
for group in df_hs27['Classification_Group'].unique():
    count = len(df_hs27[df_hs27['Classification_Group'] == group])
    stamp(f"  {group}: {count} HS4 codes")

# Convert to dictionary rules
stamp("")
stamp("Converting to dictionary rule format...")
df_rules = convert_to_dictionary_rules(df_hs27, '3', 'USER EDIT - Mineral Fuels')

stamp(f"  Total rules created: {len(df_rules)}")

# Show sample by group
stamp("")
stamp("Sample rules by Group:")
for group in ['Dry Bulk', 'Liquid Bulk', 'Liquid Gas']:
    rules_in_group = df_rules[df_rules['Group'] == group]
    if len(rules_in_group) > 0:
        stamp(f"\n  {group}:")
        for idx, row in rules_in_group.head(2).iterrows():
            rule_id = row['Rule_ID']
            cargo = row['Cargo'][:15]
            match_strat = row['Match_Strategy']
            phrases = str(row['Key_Phrases'])[:45]
            stamp(f"    {rule_id}: {cargo:15s} | {match_strat:20s} | {phrases}")

# Save
stamp("")
stamp(f"Saving to: {OUTPUT_FILE.name}")
df_rules.to_csv(OUTPUT_FILE, index=False)

stamp("")
stamp("Complete!")
stamp("")
stamp("HS27 Mineral Fuels converted:")
stamp("  - Dry Bulk: Coal, Petcoke")
stamp("  - Liquid Bulk: Crude Oil, Petroleum Products")
stamp("  - Liquid Gas: LNG")
