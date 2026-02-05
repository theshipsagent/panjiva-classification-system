"""
Build specialized dictionary for HS2 72-73 (Iron and Steel)
Same format as other specialized dictionaries

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
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_hs72-73_iron_steel.csv")

stamp("=== Build HS2 72-73 Iron & Steel Dictionary ===")
stamp("")

# Load reference data
stamp("Loading HS code reference...")
df_ref = pd.read_csv(REFERENCE_FILE, dtype=str)
stamp(f"  Total HS4 codes: {len(df_ref):,}")

# Filter to HS2 72-73
hs2_list = ['72', '73']
df_steel = df_ref[df_ref['HS2'].isin(hs2_list)].copy()
stamp(f"  HS4 codes found for HS2 72-73: {len(df_steel)}")

# Convert tonnage to numeric for sorting
df_steel['Total_Tons_Num'] = pd.to_numeric(df_steel['Total_Tons'], errors='coerce')
df_steel['Record_Count_Num'] = pd.to_numeric(df_steel['Record_Count'], errors='coerce')

# Sort by tonnage descending
df_steel = df_steel.sort_values('Total_Tons_Num', ascending=False)

# Build dictionary structure
dict_records = []

for idx, row in df_steel.iterrows():
    record = {
        'HS2': row['HS2'],
        'HS4': row['HS4'],
        'HTS_Description': row['HTS_Description'],
        'Commodity_Name': str(row.get('Cargo', '')),
        'Record_Count': row['Record_Count'],
        'Total_Tons': row['Total_Tons'],
        'Classification_Group': str(row.get('Group', '')),
        'Commodity': str(row.get('Commodity', '')),
        'Cargo': str(row.get('Cargo', '')),
        'Cargo_Detail': str(row.get('Cargo_Detail', '')),
        'Key_Phrases': str(row.get('Key_Phrases', '')),
        'Primary_Keywords': str(row.get('Primary_Keywords', '')),
        'Descriptor_Keywords': str(row.get('Descriptor_Keywords', '')),
        'Top_Package_Types': str(row.get('Top_Package_Types', '')),
        'Bundle_Coil_Packages': str(row.get('Bundle_Coil_Packages', '')),
        'Min_Tons': str(row.get('Min_Tons', '')),
        'Max_Tons': str(row.get('Max_Tons', '')),
        'Top_Shippers': str(row.get('Top_Shippers', ''))[:100],
        'Top_Consignees': str(row.get('Top_Consignees', ''))[:100],
        'Top_Ports_Loading': str(row.get('Top_Ports_Loading', ''))[:100],
        'Top_Ports_Discharge': str(row.get('Top_Ports_Discharge', ''))[:100]
    }
    dict_records.append(record)

# Create DataFrame
df_dict = pd.DataFrame(dict_records)

# Show top 15
stamp("")
stamp("Top 15 Iron & Steel products by tonnage:")
for idx, row in df_dict.head(15).iterrows():
    hs4 = row['HS4']
    desc = row['HTS_Description'][:45] if row['HTS_Description'] else 'N/A'
    tons = row['Total_Tons']
    cargo = row['Cargo'][:25] if row['Cargo'] and row['Cargo'] != 'nan' else 'N/A'
    packages = row['Top_Package_Types'][:25] if row['Top_Package_Types'] else 'N/A'
    bundles_coils = row['Bundle_Coil_Packages'][:20] if row['Bundle_Coil_Packages'] and row['Bundle_Coil_Packages'] != 'nan' else ''

    try:
        tons_int = int(float(tons))
        stamp(f"  {hs4}: {desc:45s} | {tons_int:>11,} tons | {packages:25s} | {bundles_coils:20s} | {cargo}")
    except:
        stamp(f"  {hs4}: {desc:45s} | {tons:>11s} tons | {packages:25s} | {bundles_coils:20s} | {cargo}")

# Save
stamp("")
stamp(f"Saving to: {OUTPUT_FILE.name}")
df_dict.to_csv(OUTPUT_FILE, index=False)

stamp("")
stamp("Complete!")
stamp("")
stamp("Dictionary includes:")
stamp("  HS2 72: Iron and steel products")
stamp("  HS2 73: Articles of iron or steel")
stamp("")
stamp("Categories covered:")
stamp("  - Flat-rolled products (coils, sheets)")
stamp("  - Long products (bars, rods, rebars)")
stamp("  - Tubular goods (pipes, tubes)")
stamp("  - Semi-finished (slabs, billets)")
stamp("  - Ferroalloys, pig iron, scrap")
stamp("")
stamp("Note: Bundle/Coil package counts are very high for steel products")
