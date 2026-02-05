"""
Add refined keyword columns to dictionary
Adds: Key_Phrases, Primary_Keywords, Descriptor_Keywords, Match_Strategy
Keeps old Keywords column for visual reference during transition

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def determine_match_strategy(key_phrases, primary_keywords):
    """
    Determine if phrase matching is required or if primary keywords are sufficient
    """
    # If no key phrases, use primary keywords
    if not key_phrases or key_phrases == 'nan' or pd.isna(key_phrases):
        return 'PRIMARY_SUFFICIENT'

    # Check for ambiguous terms that require phrases
    ambiguous_terms = [
        'SCRAP', 'CRUDE', 'ORE', 'CONCENTRATE', 'PELLETS'
    ]

    phrases = str(key_phrases).upper()

    # If key phrases contain ambiguous terms, require phrase matching
    for term in ambiguous_terms:
        if term in phrases:
            return 'PHRASE_REQUIRED'

    # Otherwise, primary keywords sufficient but phrases available
    return 'PRIMARY_SUFFICIENT'

# Paths
DICT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\cargo_classification_dictionary_v3.4.0_20260114_0400_user_editsv3.csv")
REFERENCE_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\hs_code_reference_complete.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\cargo_classification_dictionary_v3.5.0_DRAFT_refined_keywords.csv")

stamp("=== Add Refined Keywords to Dictionary ===")
stamp("")

# Load dictionary
stamp(f"Loading dictionary: {DICT_FILE.name}")
df_dict = pd.read_csv(DICT_FILE, dtype=str)
stamp(f"  Rules: {len(df_dict):,}")
stamp(f"  Current columns: {len(df_dict.columns)}")

# Load reference
stamp("")
stamp(f"Loading reference: {REFERENCE_FILE.name}")
df_ref = pd.read_csv(REFERENCE_FILE, dtype=str)
stamp(f"  HS4 codes: {len(df_ref):,}")

# Create lookup by HS4
stamp("")
stamp("Creating HS4 keyword lookup...")
hs4_keywords = {}
for _, row in df_ref.iterrows():
    hs4 = row['HS4']
    hs4_keywords[hs4] = {
        'Key_Phrases': row.get('Key_Phrases', ''),
        'Primary_Keywords': row.get('Primary_Keywords', ''),
        'Descriptor_Keywords': row.get('Descriptor_Keywords', '')
    }

stamp(f"  Lookup entries: {len(hs4_keywords)}")

# Add new columns after Keywords column
stamp("")
stamp("Adding new keyword columns...")

# Find position of Keywords column
keywords_col_idx = df_dict.columns.get_loc('Keywords')

# Create new columns
df_dict.insert(keywords_col_idx + 1, 'Key_Phrases', '')
df_dict.insert(keywords_col_idx + 2, 'Primary_Keywords', '')
df_dict.insert(keywords_col_idx + 3, 'Descriptor_Keywords', '')
df_dict.insert(keywords_col_idx + 4, 'Match_Strategy', '')

stamp(f"  New columns added after 'Keywords' column")

# Populate new columns from reference data
stamp("")
stamp("Populating new columns from reference data...")

matches = 0
no_matches = 0

for idx, row in df_dict.iterrows():
    hs4 = str(row.get('HS4', '')).strip()

    if hs4 and hs4 in hs4_keywords:
        # Get keywords from reference
        kw_data = hs4_keywords[hs4]

        df_dict.at[idx, 'Key_Phrases'] = kw_data['Key_Phrases']
        df_dict.at[idx, 'Primary_Keywords'] = kw_data['Primary_Keywords']
        df_dict.at[idx, 'Descriptor_Keywords'] = kw_data['Descriptor_Keywords']

        # Determine match strategy
        strategy = determine_match_strategy(
            kw_data['Key_Phrases'],
            kw_data['Primary_Keywords']
        )
        df_dict.at[idx, 'Match_Strategy'] = strategy

        matches += 1
    else:
        no_matches += 1

stamp(f"  Matched HS4 codes: {matches}")
stamp(f"  No match (Phase 1 carriers, etc.): {no_matches}")

# Show examples
stamp("")
stamp("Examples of refined keywords:")
stamp("")

# Find a rule with PHRASE_REQUIRED
phrase_required = df_dict[df_dict['Match_Strategy'] == 'PHRASE_REQUIRED'].head(3)
if len(phrase_required) > 0:
    stamp("Rules requiring PHRASE matching (disambiguation):")
    for idx, row in phrase_required.iterrows():
        rule_id = row['Rule_ID']
        hs4 = row['HS4']
        cargo = row.get('Cargo', 'N/A')
        phrases = str(row['Key_Phrases'])[:60]
        primary = str(row['Primary_Keywords'])[:40]
        stamp(f"  {rule_id} (HS4 {hs4}) - {cargo}")
        stamp(f"    Key Phrases: {phrases}")
        stamp(f"    Primary: {primary}")

stamp("")

# Find a rule with PRIMARY_SUFFICIENT
primary_sufficient = df_dict[
    (df_dict['Match_Strategy'] == 'PRIMARY_SUFFICIENT') &
    (df_dict['Primary_Keywords'].notna())
].head(3)

if len(primary_sufficient) > 0:
    stamp("Rules where PRIMARY keywords are sufficient:")
    for idx, row in primary_sufficient.iterrows():
        rule_id = row['Rule_ID']
        hs4 = row['HS4']
        cargo = row.get('Cargo', 'N/A')
        primary = str(row['Primary_Keywords'])[:50]
        stamp(f"  {rule_id} (HS4 {hs4}) - {cargo}")
        stamp(f"    Primary: {primary}")

stamp("")
stamp(f"Total columns: {len(df_dict.columns)}")
stamp(f"New columns: Key_Phrases, Primary_Keywords, Descriptor_Keywords, Match_Strategy")

# Save
stamp("")
stamp(f"Saving to: {OUTPUT_FILE.name}")
df_dict.to_csv(OUTPUT_FILE, index=False)

stamp("")
stamp("Complete!")
stamp("")
stamp("Next steps:")
stamp("  1. Review new keyword columns vs old Keywords column")
stamp("  2. Test classification with refined keywords")
stamp("  3. Once verified, drop old Keywords column before production")
stamp("")
stamp("Column layout:")
stamp("  - Keywords (OLD - keep for visual reference)")
stamp("  - Key_Phrases (NEW - strong multi-word matches)")
stamp("  - Primary_Keywords (NEW - standalone terms)")
stamp("  - Descriptor_Keywords (NEW - modifiers)")
stamp("  - Match_Strategy (NEW - PHRASE_REQUIRED or PRIMARY_SUFFICIENT)")
