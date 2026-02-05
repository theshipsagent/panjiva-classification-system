"""
Analyze chemicals in bulk - build reference dictionary
Focus on tonnage, record count, and chemical name patterns

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
CHEMICAL_NAMES = Path(r"G:\My Drive\LLM\project_manifest\user_notes\chemicalnames_gpt.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\chemicals_bulk_analysis.csv")

stamp("=== Analyze Chemicals in Bulk ===")
stamp("")

# Load reference data
stamp("Loading HS code reference...")
df_ref = pd.read_csv(REFERENCE_FILE, dtype=str)
stamp(f"  Total HS4 codes: {len(df_ref):,}")

# Load chemical names
stamp("")
stamp("Loading chemical names reference...")
df_chem = pd.read_csv(CHEMICAL_NAMES, dtype=str)
stamp(f"  Chemical names: {len(df_chem):,}")

# Filter to liquid bulk chemicals (HS2 28-29 = inorganic/organic chemicals)
stamp("")
stamp("Filtering to chemical HS2 chapters...")

chemical_hs2 = ['28', '29', '31', '32', '33', '34', '38']  # Chemicals, fertilizers, etc
df_chemicals = df_ref[df_ref['HS2'].isin(chemical_hs2)].copy()

stamp(f"  HS2 28-29, 31-34, 38: {len(df_chemicals)} HS4 codes")

# Also get Liquid Bulk from Group (if available)
liquid_bulk = df_ref[df_ref['Group'] == 'Liquid Bulk'].copy()
stamp(f"  Liquid Bulk classified: {len(liquid_bulk)} HS4 codes")

# Combine and deduplicate
df_chemicals = pd.concat([df_chemicals, liquid_bulk]).drop_duplicates(subset=['HS4'])
stamp(f"  Combined unique HS4 codes: {len(df_chemicals)}")

# Convert tonnage to numeric for sorting
df_chemicals['Total_Tons_Num'] = pd.to_numeric(df_chemicals['Total_Tons'], errors='coerce')
df_chemicals['Record_Count_Num'] = pd.to_numeric(df_chemicals['Record_Count'], errors='coerce')

# Sort by tonnage descending
df_chemicals = df_chemicals.sort_values('Total_Tons_Num', ascending=False)

# Select relevant columns
output_columns = [
    'HS2', 'HS4', 'HTS_Description',
    'Group', 'Commodity', 'Cargo', 'Cargo_Detail',
    'Key_Phrases', 'Primary_Keywords', 'Descriptor_Keywords',
    'Top_Package_Types',
    'Min_Tons', 'Max_Tons',
    'Record_Count', 'Total_Tons',
    'Top_Shippers', 'Top_Consignees',
    'Top_Ports_Loading', 'Top_Ports_Discharge'
]

df_output = df_chemicals[output_columns].copy()

# Show top chemicals by tonnage
stamp("")
stamp("Top 10 chemicals by tonnage:")
for idx, row in df_output.head(10).iterrows():
    hs4 = row['HS4']
    desc = row['HTS_Description'][:50] if row['HTS_Description'] else 'N/A'
    tons = row['Total_Tons']
    cargo = str(row['Cargo'])[:20] if pd.notna(row['Cargo']) else 'N/A'
    stamp(f"  {hs4}: {desc:50s} | {int(float(tons)):>12,} tons | {cargo}")

# Save
stamp("")
stamp(f"Saving to: {OUTPUT_FILE.name}")
df_output.to_csv(OUTPUT_FILE, index=False)

stamp("")
stamp("Complete!")
stamp("")
stamp("Chemical HS2 chapters analyzed:")
stamp("  HS2 28: Inorganic chemicals")
stamp("  HS2 29: Organic chemicals")
stamp("  HS2 31: Fertilizers")
stamp("  HS2 32: Tanning/dyeing extracts")
stamp("  HS2 33: Essential oils, perfumes")
stamp("  HS2 34: Soaps, lubricants")
stamp("  HS2 38: Miscellaneous chemical products")
