"""
Add HS2 and HS4 description columns to dictionary (working draft)
Adds columns at END so existing scripts aren't disrupted

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
DICT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\cargo_classification_dictionary_v3.4.0_20260114_0400_user_editsv2.csv")
HS2_LOOKUP = Path(r"G:\My Drive\LLM\project_manifest\01.01_dictionary\hs2_lookup.csv")
HS4_LOOKUP = Path(r"G:\My Drive\LLM\project_manifest\01.01_dictionary\hs4_lookup.csv")

stamp("=== Add HS Descriptions to Dictionary ===")
stamp("")

# Load dictionary
stamp(f"Loading dictionary: {DICT_FILE.name}")
df_dict = pd.read_csv(DICT_FILE, dtype=str)
stamp(f"  Rules: {len(df_dict)}")
stamp(f"  Current columns: {len(df_dict.columns)}")

# Load HS lookups
stamp("")
stamp("Loading HS code lookups...")
df_hs2 = pd.read_csv(HS2_LOOKUP, dtype=str)
df_hs4 = pd.read_csv(HS4_LOOKUP, dtype=str)
stamp(f"  HS2 entries: {len(df_hs2)}")
stamp(f"  HS4 entries: {len(df_hs4)}")

# Create lookup dictionaries
hs2_lookup = dict(zip(df_hs2['HS2'], df_hs2['Description']))
hs4_lookup = dict(zip(df_hs4['HS4'], df_hs4['Description']))

stamp("")
stamp("Adding description columns at end...")

# Add HS2 Description column
df_dict['HS2_Description'] = df_dict['HS2'].map(hs2_lookup)

# Add HS4 Description column
df_dict['HS4_Description'] = df_dict['HS4'].map(hs4_lookup)

# Count matches
hs2_matches = df_dict['HS2_Description'].notna().sum()
hs4_matches = df_dict['HS4_Description'].notna().sum()

stamp(f"  HS2 descriptions matched: {hs2_matches} / {len(df_dict)}")
stamp(f"  HS4 descriptions matched: {hs4_matches} / {len(df_dict)}")

# Show sample
stamp("")
stamp("Sample rows with descriptions:")
sample = df_dict[df_dict['HS2'].notna() & df_dict['HS4'].notna()].head(5)
for idx, row in sample.iterrows():
    rule_id = row['Rule_ID']
    hs2 = row['HS2']
    hs4 = row['HS4']
    hs2_desc = row['HS2_Description']
    hs4_desc = row['HS4_Description']
    stamp(f"  {rule_id}: HS2={hs2} ({hs2_desc[:30]}...) | HS4={hs4} ({hs4_desc[:30]}...)")

stamp("")
stamp(f"New column count: {len(df_dict.columns)}")
stamp(f"New columns: HS2_Description, HS4_Description")

# Save back to same file
stamp("")
stamp(f"Saving to: {DICT_FILE.name}")
df_dict.to_csv(DICT_FILE, index=False)

stamp("")
stamp("Complete!")
stamp("")
stamp("Note: This is a WORKING DRAFT in user_notes folder.")
stamp("      No changes made to authoritative dictionary.")
