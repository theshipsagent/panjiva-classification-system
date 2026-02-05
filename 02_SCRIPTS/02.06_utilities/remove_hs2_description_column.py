"""
Remove HS2_Description column from dictionary
Keep only HS4_Description which is correct

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Path
DICT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\cargo_classification_dictionary_v3.4.0_20260114_0400_user_editsv2.csv")

stamp("=== Remove HS2_Description Column ===")
stamp("")

# Load dictionary
stamp(f"Loading dictionary: {DICT_FILE.name}")
df_dict = pd.read_csv(DICT_FILE, dtype=str)
stamp(f"  Rows: {len(df_dict):,}")
stamp(f"  Columns before: {len(df_dict.columns)}")

# Remove HS2_Description column
if 'HS2_Description' in df_dict.columns:
    df_dict = df_dict.drop(columns=['HS2_Description'])
    stamp(f"  Removed: HS2_Description")
else:
    stamp(f"  HS2_Description column not found")

stamp(f"  Columns after: {len(df_dict.columns)}")

# Verify HS4_Description is still there
if 'HS4_Description' in df_dict.columns:
    hs4_matches = df_dict['HS4_Description'].notna().sum()
    stamp(f"  HS4_Description retained: {hs4_matches} descriptions")

    # Show sample
    stamp("")
    stamp("Sample HS4 descriptions:")
    sample = df_dict[df_dict['HS4_Description'].notna()].head(5)
    for idx, row in sample.iterrows():
        rule_id = row['Rule_ID'][:20]
        hs4 = row['HS4']
        hs4_desc = str(row['HS4_Description'])[:50]
        stamp(f"  {rule_id:20s} HS4:{hs4:5s} = {hs4_desc}")

# Save
stamp("")
stamp(f"Saving to: {DICT_FILE.name}")
df_dict.to_csv(DICT_FILE, index=False)

stamp("")
stamp("Complete!")
