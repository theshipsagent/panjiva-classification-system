"""
Fix typos in 2M+ tons user edits and convert to production dictionary format

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

    # Remove blank rows
    df = df[df['HS4'].notna() & (df['HS4'].str.strip() != '')].copy()

    # Fix chemicals capitalization (HS4 3901, 3811, 3824, 3820)
    for hs4 in ['3901', '3811', '3824', '3820']:
        if hs4 in df['HS4'].values:
            df.loc[df['HS4'] == hs4, 'Commodity'] = 'Chemicals'
            df.loc[df['HS4'] == hs4, 'Cargo'] = 'Chemicals'

    # Fix copper cathodes typo (HS4 7403)
    df.loc[df['HS4'] == '7403', 'Key_Phrases'] = df.loc[df['HS4'] == '7403', 'Key_Phrases'].str.replace('csthodes', 'cathodes')

    # Fix Phosphorous Fertilizers typo (HS4 2510)
    df.loc[df['HS4'] == '2510', 'Cargo'] = 'Phosphorous Fertilizers'
    df.loc[df['HS4'] == '2510', 'Key_Phrases'] = 'phos rock, phosphate rock'

    # Fix fly ash typo (HS4 2620)
    df.loc[df['HS4'] == '2620', 'Key_Phrases'] = df.loc[df['HS4'] == '2620', 'Key_Phrases'].str.replace('flay ash', 'fly ash')
    df.loc[df['HS4'] == '2620', 'Cargo'] = 'SCMs'

    # Fix iron concentrates typo (HS4 2601)
    df.loc[df['HS4'] == '2601', 'Key_Phrases'] = 'iron concentrates'

    # Fix cement articles - remove wrong COPPER keyword (HS4 6810)
    df.loc[df['HS4'] == '6810', 'Key_Phrases'] = ''

    # Fix aggregates typo (HS4 6802)
    df.loc[df['HS4'] == '6802', 'Cargo_Detail'] = 'Aggregates'

    # Fix ceramic bricks - remove wrong CEMENT CLINKER keyword (HS4 6904)
    df.loc[df['HS4'] == '6904', 'Key_Phrases'] = ''

    stamp(f"  Typos fixed, {len(df)} entries ready for conversion")
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

        # Determine match strategy based on cargo type
        classification_group = str(row.get('Classification_Group', ''))
        cargo = str(row.get('Cargo', ''))

        if key_phrases and key_phrases != 'nan':
            # Specific phrases that require phrase matching
            upper_phrases = key_phrases.upper()
            if any(term in upper_phrases for term in [
                'CRUDE OIL', 'PETROLEUM', 'CEMENT', 'PORTLAND', 'PIG IRON', 'IRON ORE',
                'CATHODE', 'BAUXITE', 'BARITE', 'PALM OIL', 'COCONUT OIL', 'TALLOW',
                'ORANGE JUICE', 'UREA', 'POTASH', 'SUGAR', 'COFFEE', 'RUBBER',
                'PHOSPHATE', 'GYPSUM', 'SALT', 'SLAG', 'MAGNESIA', 'FLUORSPAR'
            ]):
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
INPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_all_hs4_2mil_tons_plus_USER_EDIT_011426_1825.csv")
CORRECTED_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_all_hs4_2mil_tons_plus_CORRECTED.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_rules_DRAFT_2mil_tons_plus.csv")

stamp("=== Fix Typos and Convert 2M+ Tons User Edits ===")
stamp("")

# Load user-edited file
stamp("Loading 2M+ tons user edits...")
df_2mil = pd.read_csv(INPUT_FILE, dtype=str)
stamp(f"  Entries loaded: {len(df_2mil)}")

# Fix typos
df_2mil = fix_typos(df_2mil)

# Save corrected version
stamp("")
stamp(f"Saving corrected file: {CORRECTED_FILE.name}")
df_2mil.to_csv(CORRECTED_FILE, index=False)

# Show breakdown
stamp("")
stamp("Breakdown by Group:")
for group in sorted(df_2mil['Classification_Group'].unique()):
    count = len(df_2mil[df_2mil['Classification_Group'] == group])
    stamp(f"  {group}: {count} HS4 codes")

# Convert to dictionary rules
stamp("")
stamp("Converting to dictionary rule format...")
df_rules = convert_to_dictionary_rules(df_2mil, '3', 'USER EDIT - 2M+ Tons')

stamp(f"  Total rules created: {len(df_rules)}")

# Show sample by group
stamp("")
stamp("Sample rules by Group:")
for group in ['Dry Bulk', 'Liquid Bulk']:
    rules_in_group = df_rules[df_rules['Group'] == group]
    if len(rules_in_group) > 0:
        stamp(f"\n  {group}:")
        for idx, row in rules_in_group.head(5).iterrows():
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
stamp("2M+ Tons commodities converted:")
stamp("  - Agricultural Products (Grain, Oils, Coffee, Sugar)")
stamp("  - Chemicals (Organic, Inorganic, Additives)")
stamp("  - Construction Materials (Cement, Aggregates, Gypsum)")
stamp("  - Metals (Copper, Aluminum, Bauxite)")
stamp("  - Fertilizers (Nitrogen, Potash, Phosphorous)")
stamp("  - Forestry (Lumber, Paper, Wood Pulp)")
stamp("  - General Cargo (Vehicles, Machinery)")
