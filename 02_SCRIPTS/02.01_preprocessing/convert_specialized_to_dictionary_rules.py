"""
Convert user-edited specialized dictionaries to production dictionary format
Matches structure of v3.5.0 draft with refined keywords

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

        # Determine match strategy
        key_phrases = str(row.get('Key_Phrases', ''))
        primary_kw = str(row.get('Primary_Keywords', ''))

        # If key phrases exist and contain important terms, require phrase matching
        if key_phrases and key_phrases != 'nan':
            if any(term in key_phrases.upper() for term in ['SCRAP', 'CONCENTRATE', 'PIG IRON', 'IRON ORE']):
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
            'Descriptor_Keywords': str(row.get('Descriptor_Keywords', '')) if pd.notna(row.get('Descriptor_Keywords')) else '',
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
NONFERROUS_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_hs76-79_nonferrous_metals_user_edit_011426_1530.csv")
STEEL_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_hs72-73_iron_steel_USEREDIT_011426_1600.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_rules_DRAFT_hs72-73_76-79_user_edits.csv")

stamp("=== Convert User-Edited Specialized Dictionaries to Rules ===")
stamp("")

# Load user-edited files
stamp("Loading nonferrous metals (HS 76-79)...")
df_nonferrous = pd.read_csv(NONFERROUS_FILE, dtype=str)
stamp(f"  Entries: {len(df_nonferrous)}")

stamp("")
stamp("Loading iron & steel (HS 72-73)...")
df_steel = pd.read_csv(STEEL_FILE, dtype=str)
stamp(f"  Entries: {len(df_steel)}")

# Convert to dictionary rules
stamp("")
stamp("Converting to dictionary rule format...")
df_nonferrous_rules = convert_to_dictionary_rules(df_nonferrous, '3', 'USER EDIT - Nonferrous Metals')
df_steel_rules = convert_to_dictionary_rules(df_steel, '3', 'USER EDIT - Iron & Steel')

# Combine
df_combined = pd.concat([df_nonferrous_rules, df_steel_rules], ignore_index=True)

stamp(f"  Total rules created: {len(df_combined)}")
stamp(f"  Nonferrous: {len(df_nonferrous_rules)}")
stamp(f"  Steel: {len(df_steel_rules)}")

# Show sample
stamp("")
stamp("Sample rules created:")
for idx, row in df_combined.head(5).iterrows():
    rule_id = row['Rule_ID']
    hs4 = row['HS4']
    cargo = row['Cargo'][:20]
    match_strat = row['Match_Strategy']
    phrases = str(row['Key_Phrases'])[:40]
    stamp(f"  {rule_id} (HS4 {hs4}): {cargo:20s} | {match_strat:20s} | {phrases}")

# Save
stamp("")
stamp(f"Saving to: {OUTPUT_FILE.name}")
df_combined.to_csv(OUTPUT_FILE, index=False)

stamp("")
stamp("Complete!")
stamp("")
stamp("Next steps:")
stamp("  1. REVIEW: Check the generated rules")
stamp("  2. MERGE: Add these rules to main dictionary v3.5.0 draft")
stamp("  3. TEST: Run classification test on sample data")
stamp("  4. PRODUCTION: Move to authoritative dictionary when verified")
