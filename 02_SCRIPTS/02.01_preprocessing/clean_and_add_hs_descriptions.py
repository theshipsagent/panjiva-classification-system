"""
Clean dictionary and add CORRECT HS2/HS4 descriptions
Removes blank rows first, then adds descriptions from HTS data

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import re

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
DICT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\cargo_classification_dictionary_v3.4.0_20260114_0400_user_editsv2.csv")
HTS_DATA = Path(r"G:\My Drive\LLM\project_manifest\_archive\user_notes_old\htsdata.csv")

stamp("=== Clean Dictionary and Add CORRECT HS Descriptions ===")
stamp("")

# Load dictionary
stamp(f"Loading dictionary: {DICT_FILE.name}")
df_dict = pd.read_csv(DICT_FILE, dtype=str)
rows_before = len(df_dict)
stamp(f"  Rows before: {rows_before:,}")

# Remove blank rows (where Rule_ID is empty or NaN)
stamp("")
stamp("Removing blank/incomplete rows...")
df_dict = df_dict[df_dict['Rule_ID'].notna() & (df_dict['Rule_ID'].str.strip() != '')].copy()
rows_after = len(df_dict)
rows_removed = rows_before - rows_after
stamp(f"  Rows after:  {rows_after:,}")
stamp(f"  Rows removed: {rows_removed:,}")

# Remove old description columns if they exist
if 'HS2_Description' in df_dict.columns:
    df_dict = df_dict.drop(columns=['HS2_Description'])
if 'HS4_Description' in df_dict.columns:
    df_dict = df_dict.drop(columns=['HS4_Description'])

# Load HTS data
stamp("")
stamp(f"Loading HTS data: {HTS_DATA.name}")
df_hts = pd.read_csv(HTS_DATA, dtype=str, encoding='utf-8-sig')
stamp(f"  HTS entries: {len(df_hts):,}")

# Extract HS2 descriptions (2-digit codes at Indent 0)
stamp("")
stamp("Extracting HS2 descriptions...")
hs2_lookup = {}

for _, row in df_hts.iterrows():
    hts_num = str(row['HTS Number']).strip().replace('"', '')
    indent = str(row['Indent']).strip()
    desc = str(row['Description']).strip().replace('"', '')

    # HS2 level: 2-digit codes at chapter level (Indent 0)
    # Look for entries like "73" or "73.00" at Indent 0
    if indent == '0' and desc and desc != 'nan':
        # Extract 2-digit code
        match = re.match(r'^(\d{2})', hts_num)
        if match:
            hs2_code = match.group(1)
            # Only take first description for each HS2
            if hs2_code not in hs2_lookup:
                # Clean up description (remove trailing colons)
                desc_clean = desc.strip(':').strip()
                hs2_lookup[hs2_code] = desc_clean

stamp(f"  HS2 codes extracted: {len(hs2_lookup)}")

# Extract HS4 descriptions (4-digit codes at Indent 0)
stamp("")
stamp("Extracting HS4 descriptions...")
hs4_lookup = {}

for _, row in df_hts.iterrows():
    hts_num = str(row['HTS Number']).strip().replace('"', '')
    indent = str(row['Indent']).strip()
    desc = str(row['Description']).strip().replace('"', '')

    # HS4 level: 4-digit codes at Indent 0 (heading level)
    # Look for entries like "7304" at Indent 0
    if indent == '0' and desc and desc != 'nan':
        # Extract 4-digit code
        match = re.match(r'^(\d{4})', hts_num)
        if match:
            hs4_code = match.group(1)
            # Only take first description for each HS4
            if hs4_code not in hs4_lookup:
                # Clean up description (remove trailing colons)
                desc_clean = desc.strip(':').strip()
                # Skip empty or too short descriptions
                if len(desc_clean) > 3:
                    hs4_lookup[hs4_code] = desc_clean

stamp(f"  HS4 codes extracted: {len(hs4_lookup)}")

# Show samples to verify
stamp("")
stamp("Sample HS2 descriptions:")
for hs2 in ['10', '25', '27', '72', '73', '84']:
    if hs2 in hs2_lookup:
        stamp(f"  HS2 {hs2}: {hs2_lookup[hs2][:70]}")

stamp("")
stamp("Sample HS4 descriptions:")
for hs4 in ['1001', '2523', '2709', '7214', '7304', '8703']:
    if hs4 in hs4_lookup:
        stamp(f"  HS4 {hs4}: {hs4_lookup[hs4][:70]}")

# Add HS2 Description column
stamp("")
stamp("Adding description columns at end...")
df_dict['HS2_Description'] = df_dict['HS2'].map(hs2_lookup)

# Add HS4 Description column
df_dict['HS4_Description'] = df_dict['HS4'].map(hs4_lookup)

# Count matches
hs2_matches = df_dict['HS2_Description'].notna().sum()
hs4_matches = df_dict['HS4_Description'].notna().sum()

stamp(f"  HS2 descriptions matched: {hs2_matches} / {len(df_dict)}")
stamp(f"  HS4 descriptions matched: {hs4_matches} / {len(df_dict)}")

# Verify specific rule
stamp("")
stamp("Verifying HS4 7304 (Tubular Goods):")
test_7304 = df_dict[df_dict['HS4'] == '7304']
if len(test_7304) > 0:
    for idx, row in test_7304.iterrows():
        rule_id = row['Rule_ID']
        hs2_desc = str(row['HS2_Description'])[:50] if pd.notna(row['HS2_Description']) else 'N/A'
        hs4_desc = str(row['HS4_Description'])[:50] if pd.notna(row['HS4_Description']) else 'N/A'
        stamp(f"  Rule: {rule_id}")
        stamp(f"  HS2 73: {hs2_desc}")
        stamp(f"  HS4 7304: {hs4_desc}")

stamp("")
stamp(f"Total columns: {len(df_dict.columns)}")

# Save cleaned dictionary with descriptions
stamp("")
stamp(f"Saving cleaned dictionary to: {DICT_FILE.name}")
df_dict.to_csv(DICT_FILE, index=False)

stamp("")
stamp("Complete!")
stamp("")
stamp(f"Summary:")
stamp(f"  - Removed {rows_removed} blank rows")
stamp(f"  - Added HS2_Description and HS4_Description columns")
stamp(f"  - Dictionary is now clean and descriptions are aligned")
stamp("")
stamp("Note: This is a WORKING DRAFT in user_notes folder.")
