"""
Fix typos in HS28-29 pure chemicals user edits and convert to production dictionary format

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def fix_typos(df):
    """Fix typos in user-edited file"""

    stamp("Fixing typos...")

    # Fix Caustic Sodea -> Caustic Soda
    df.loc[df['HS4'] == '2815', 'Cargo_Detail'] = df.loc[df['HS4'] == '2815', 'Cargo_Detail'].str.replace('Caustic Sodea', 'Caustic Soda')

    # Fix liquid gas -> Liquid Gas, lpg -> LPG for HS4 2804
    df.loc[df['HS4'] == '2804', 'Classification_Group'] = 'Liquid Gas'
    df.loc[df['HS4'] == '2804', 'Commodity'] = 'LPG'
    df.loc[df['HS4'] == '2804', 'Cargo'] = 'LPG'
    df.loc[df['HS4'] == '2804', 'Cargo_Detail'] = 'LPG'

    # Fix Nitrogen Fertiliers -> Nitrogen Fertilizers
    df.loc[df['HS4'] == '2834', 'Cargo'] = 'Nitrogen Fertilizers'
    df.loc[df['HS4'] == '2834', 'Cargo_Detail'] = 'Nitrogen Fertilizers'

    # Fix Tios -> TiO2
    df.loc[df['HS4'] == '2823', 'Cargo'] = 'TiO2'

    # Fix Mangeses -> Manganese
    df.loc[df['HS4'] == '2820', 'Cargo'] = 'Manganese'
    df.loc[df['HS4'] == '2820', 'Cargo_Detail'] = 'Manganese'

    # Fix Zinc concventreatre -> Zinc concentrate, and Metals -> Non Ferrous Raw Materials
    df.loc[df['HS4'] == '2817', 'Commodity'] = 'Non Ferrous Raw Materials'
    df.loc[df['HS4'] == '2817', 'Cargo'] = 'Zinc concentrate'
    df.loc[df['HS4'] == '2817', 'Cargo_Detail'] = 'Zinc concentrate'

    # Fix tbn bulkk -> TBN
    for hs4 in ['2849', '2832', '2826', '2825']:
        if hs4 in df['HS4'].values:
            df.loc[df['HS4'] == hs4, 'Cargo_Detail'] = 'TBN'

    stamp("  Typos fixed")
    return df

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
        # Chemicals generally need specific phrases if provided
        if key_phrases and key_phrases != 'nan':
            if any(term in key_phrases.upper() for term in ['AMMONIA', 'CAUSTIC', 'BENZENE', 'ALCOHOL', 'KETONE', 'ACETONE', 'METHANOL', 'GLYCOL', 'GLYCERINE', 'PHOSPHATE', 'RUTILE', 'TITANIUM', 'ILMENITE']):
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
INPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_hs28-29_pure_chemicals_user_edits_011426_1650.csv")
CORRECTED_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_hs28-29_pure_chemicals_CORRECTED.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_rules_DRAFT_hs28-29_pure_chemicals.csv")

stamp("=== Fix Typos and Convert HS28-29 Pure Chemicals ===" )
stamp("")

# Load user-edited file
stamp("Loading HS28-29 pure chemicals...")
df_hs28_29 = pd.read_csv(INPUT_FILE, dtype=str)
stamp(f"  Entries: {len(df_hs28_29)}")

# Fix typos
df_hs28_29 = fix_typos(df_hs28_29)

# Save corrected version
stamp("")
stamp(f"Saving corrected file: {CORRECTED_FILE.name}")
df_hs28_29.to_csv(CORRECTED_FILE, index=False)

# Show breakdown
stamp("")
stamp("Breakdown by Group:")
for group in df_hs28_29['Classification_Group'].unique():
    count = len(df_hs28_29[df_hs28_29['Classification_Group'] == group])
    stamp(f"  {group}: {count} HS4 codes")

# Convert to dictionary rules
stamp("")
stamp("Converting to dictionary rule format...")
df_rules = convert_to_dictionary_rules(df_hs28_29, '3', 'USER EDIT - Pure Chemicals')

stamp(f"  Total rules created: {len(df_rules)}")

# Show sample by group
stamp("")
stamp("Sample rules by Group:")
for group in ['Dry Bulk', 'Liquid Bulk', 'Liquid Gas']:
    rules_in_group = df_rules[df_rules['Group'] == group]
    if len(rules_in_group) > 0:
        stamp(f"\n  {group}:")
        for idx, row in rules_in_group.head(3).iterrows():
            rule_id = row['Rule_ID']
            cargo = str(row['Cargo'])[:20]
            match_strat = row['Match_Strategy']
            phrases = str(row['Key_Phrases'])[:35]
            stamp(f"    {rule_id}: {cargo:20s} | {match_strat:20s} | {phrases}")

# Save
stamp("")
stamp(f"Saving to: {OUTPUT_FILE.name}")
df_rules.to_csv(OUTPUT_FILE, index=False)

stamp("")
stamp("Complete!")
stamp("")
stamp("HS28-29 Pure Chemicals converted:")
stamp("  - Inorganic Chemicals (HS28)")
stamp("  - Organic Chemicals (HS29)")
stamp("  - Includes: Ammonia, Caustic Soda, Benzene, Alcohols, Acids, Fertilizers")
