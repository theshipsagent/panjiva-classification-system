"""
Generate list of all HS4 codes with 2+ million tons total tonnage
In same format as specialized dictionaries for user editing

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
REFERENCE_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\hs_code_reference_complete.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_all_hs4_2mil_tons_plus.csv")

stamp("=== Generate HS4 Codes with 2M+ Tons ===")
stamp("")

# Load reference file
stamp("Loading HS code reference...")
df_ref = pd.read_csv(REFERENCE_FILE, dtype=str)
stamp(f"  Total HS4 codes: {len(df_ref)}")

# Convert tonnage to numeric
df_ref['Total_Tons_Numeric'] = pd.to_numeric(
    df_ref['Total_Tons'].str.replace(',', ''),
    errors='coerce'
)

# Filter for 2M+ tons
df_filtered = df_ref[df_ref['Total_Tons_Numeric'] >= 2000000].copy()
stamp(f"  HS4 codes with 2M+ tons: {len(df_filtered)}")

# Sort by tonnage descending
df_filtered = df_filtered.sort_values('Total_Tons_Numeric', ascending=False)

# Create output in specialized dictionary format
output_columns = [
    'HS2',
    'HS4',
    'HTS_Description',
    'Commodity_Name',
    'Record_Count',
    'Total_Tons',
    'Classification_Group',
    'Commodity',
    'Cargo',
    'Cargo_Detail',
    'Key_Phrases',
    'Primary_Keywords',
    'Descriptor_Keywords',
    'Top_Package_Types',
    'Bundle_Coil_Packages',
    'Min_Tons',
    'Max_Tons',
    'Top_Shippers',
    'Top_Consignees',
    'Top_Ports_Loading',
    'Top_Ports_Discharge'
]

# Build output dataframe
df_output = pd.DataFrame()

for col in output_columns:
    if col in df_filtered.columns:
        df_output[col] = df_filtered[col]
    else:
        df_output[col] = ''

# Format Total_Tons with commas
df_output['Total_Tons'] = df_filtered['Total_Tons_Numeric'].apply(
    lambda x: f" {x:,.1f} " if pd.notna(x) else ''
)

# Add placeholder for Commodity_Name
df_output['Commodity_Name'] = 'x'

# Show summary by HS2 chapter
stamp("")
stamp("Breakdown by HS2 Chapter:")
for hs2 in sorted(df_output['HS2'].unique()):
    count = len(df_output[df_output['HS2'] == hs2])
    total_tons = df_filtered[df_filtered['HS2'] == hs2]['Total_Tons_Numeric'].sum()
    stamp(f"  HS{hs2}: {count:2d} codes | {total_tons:,.0f} tons")

# Show top 10
stamp("")
stamp("Top 10 by tonnage:")
for idx, row in df_output.head(10).iterrows():
    hs4 = row['HS4']
    desc = row['HTS_Description'][:45]
    tons = row['Total_Tons'].strip()
    stamp(f"  HS4 {hs4}: {tons:>15s} tons | {desc}")

# Save
stamp("")
stamp(f"Saving to: {OUTPUT_FILE.name}")
df_output.to_csv(OUTPUT_FILE, index=False)

stamp("")
stamp("Complete!")
stamp("")
stamp("This file includes ALL HS4 codes with 2M+ total tons")
stamp("You can now edit this master file to add classifications")
stamp("Or filter by HS2 chapter to work on specific commodity groups")
