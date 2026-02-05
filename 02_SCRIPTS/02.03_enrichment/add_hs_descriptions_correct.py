"""
Add CORRECT HS2 and HS4 descriptions to dictionary from HTS data
Uses the proper HTS tariff data file we created earlier

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

stamp("=== Add CORRECT HS Descriptions to Dictionary ===")
stamp("")

# Load HTS data
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

    # HS2 level: 2-digit codes at chapter level (e.g., "27" or "27.00")
    if indent == '0' and desc and desc != 'nan':
        # Extract 2-digit code
        match = re.match(r'^(\d{2})', hts_num)
        if match:
            hs2_code = match.group(1)
            # Only take first description for each HS2
            if hs2_code not in hs2_lookup:
                # Clean up description
                desc_clean = desc.strip(':').strip()
                hs2_lookup[hs2_code] = desc_clean

stamp(f"  HS2 codes extracted: {len(hs2_lookup)}")

# Extract HS4 descriptions (4-digit codes)
stamp("")
stamp("Extracting HS4 descriptions...")
hs4_lookup = {}

for _, row in df_hts.iterrows():
    hts_num = str(row['HTS Number']).strip().replace('"', '')
    indent = str(row['Indent']).strip()
    desc = str(row['Description']).strip().replace('"', '')

    # HS4 level: 4-digit codes (e.g., "2709", "2709.00")
    # Usually at Indent 0 or 1
    if desc and desc != 'nan':
        # Extract 4-digit code
        match = re.match(r'^(\d{4})', hts_num)
        if match:
            hs4_code = match.group(1)
            # Only take first meaningful description for each HS4
            if hs4_code not in hs4_lookup or indent in ['0', '1']:
                # Clean up description
                desc_clean = desc.strip(':').strip()
                # Skip empty or generic descriptions
                if len(desc_clean) > 3:
                    hs4_lookup[hs4_code] = desc_clean

stamp(f"  HS4 codes extracted: {len(hs4_lookup)}")

# Show samples
stamp("")
stamp("Sample HS2 descriptions:")
for hs2 in ['10', '25', '27', '72', '84']:
    if hs2 in hs2_lookup:
        stamp(f"  HS2 {hs2}: {hs2_lookup[hs2][:60]}")

stamp("")
stamp("Sample HS4 descriptions:")
for hs4 in ['1001', '2523', '2709', '7214', '8703']:
    if hs4 in hs4_lookup:
        stamp(f"  HS4 {hs4}: {hs4_lookup[hs4][:60]}")

# Load dictionary
stamp("")
stamp(f"Loading dictionary: {DICT_FILE.name}")
df_dict = pd.read_csv(DICT_FILE, dtype=str)
stamp(f"  Rules: {len(df_dict)}")

# Remove old description columns if they exist
if 'HS2_Description' in df_dict.columns:
    df_dict = df_dict.drop(columns=['HS2_Description'])
if 'HS4_Description' in df_dict.columns:
    df_dict = df_dict.drop(columns=['HS4_Description'])

stamp("")
stamp("Adding CORRECT description columns at end...")

# Add HS2 Description
df_dict['HS2_Description'] = df_dict['HS2'].map(hs2_lookup)

# Add HS4 Description
df_dict['HS4_Description'] = df_dict['HS4'].map(hs4_lookup)

# Count matches
hs2_matches = df_dict['HS2_Description'].notna().sum()
hs4_matches = df_dict['HS4_Description'].notna().sum()

stamp(f"  HS2 descriptions matched: {hs2_matches} / {len(df_dict)}")
stamp(f"  HS4 descriptions matched: {hs4_matches} / {len(df_dict)}")

# Show sample with real cargo
stamp("")
stamp("Sample rules with CORRECT descriptions:")
sample = df_dict[df_dict['HS2'].notna() & df_dict['HS4'].notna()].head(10)
for idx, row in sample.iterrows():
    rule_id = row['Rule_ID'][:20]
    hs2 = row['HS2']
    hs4 = row['HS4']
    hs2_desc = str(row['HS2_Description'])[:40] if pd.notna(row['HS2_Description']) else 'N/A'
    hs4_desc = str(row['HS4_Description'])[:40] if pd.notna(row['HS4_Description']) else 'N/A'
    stamp(f"  {rule_id:20s} HS2:{hs2:3s}={hs2_desc:40s} HS4:{hs4:5s}={hs4_desc}")

stamp("")
stamp(f"Total columns: {len(df_dict.columns)}")

# Save
stamp("")
stamp(f"Saving to: {DICT_FILE.name}")
df_dict.to_csv(DICT_FILE, index=False)

stamp("")
stamp("Complete!")
stamp("")
stamp("Note: This is a WORKING DRAFT in user_notes folder.")
stamp("      Descriptions now match the actual HTS tariff data.")
