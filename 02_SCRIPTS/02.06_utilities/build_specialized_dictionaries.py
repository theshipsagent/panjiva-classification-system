"""
Build specialized dictionaries by HS2 chapter ranges
Format matches chemicalnames_gpt.csv structure for easy transfer to master dictionary

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def build_chapter_dictionary(df_ref, hs2_list, chapter_name, output_file):
    """Build specialized dictionary for HS2 chapter range"""

    stamp(f"\n=== Building {chapter_name} Dictionary ===")

    # Filter to specified HS2 codes
    df_filtered = df_ref[df_ref['HS2'].isin(hs2_list)].copy()
    stamp(f"  HS4 codes found: {len(df_filtered)}")

    if len(df_filtered) == 0:
        stamp(f"  WARNING: No data found for HS2 chapters {hs2_list}")
        return

    # Convert tonnage to numeric for sorting
    df_filtered['Total_Tons_Num'] = pd.to_numeric(df_filtered['Total_Tons'], errors='coerce')
    df_filtered['Record_Count_Num'] = pd.to_numeric(df_filtered['Record_Count'], errors='coerce')

    # Sort by tonnage descending
    df_filtered = df_filtered.sort_values('Total_Tons_Num', ascending=False)

    # Build dictionary structure matching chemicalnames_gpt.csv format
    dict_records = []

    for idx, row in df_filtered.iterrows():
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
            'Top_Shippers': str(row.get('Top_Shippers', ''))[:100],  # Truncate for readability
            'Top_Consignees': str(row.get('Top_Consignees', ''))[:100],
            'Top_Ports_Loading': str(row.get('Top_Ports_Loading', ''))[:100],
            'Top_Ports_Discharge': str(row.get('Top_Ports_Discharge', ''))[:100]
        }
        dict_records.append(record)

    # Create DataFrame
    df_dict = pd.DataFrame(dict_records)

    # Show top 5
    stamp(f"\n  Top 5 by tonnage:")
    for idx, row in df_dict.head(5).iterrows():
        hs4 = row['HS4']
        desc = row['HTS_Description'][:40] if row['HTS_Description'] else 'N/A'
        tons = row['Total_Tons']
        cargo = row['Cargo'][:20] if row['Cargo'] else 'N/A'
        packages = row['Top_Package_Types'][:20] if row['Top_Package_Types'] else 'N/A'
        try:
            tons_int = int(float(tons))
            stamp(f"    {hs4}: {desc:40s} | {tons_int:>12,} tons | {packages:20s} | {cargo}")
        except:
            stamp(f"    {hs4}: {desc:40s} | {tons:>12s} tons | {packages:20s} | {cargo}")

    # Save
    stamp(f"\n  Saving to: {output_file.name}")
    df_dict.to_csv(output_file, index=False)

    return df_dict

# Paths
REFERENCE_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\hs_code_reference_complete.csv")
OUTPUT_DIR = Path(r"G:\My Drive\LLM\project_manifest\user_notes")

stamp("=== Build Specialized Dictionaries by HS2 Chapter ===")
stamp("")

# Load reference data
stamp("Loading HS code reference...")
df_ref = pd.read_csv(REFERENCE_FILE, dtype=str)
stamp(f"  Total HS4 codes: {len(df_ref):,}")

# Build specialized dictionaries for each chapter range

# 1. HS2 Chapter 27 - Mineral Fuels
build_chapter_dictionary(
    df_ref,
    ['27'],
    "HS2-27 Mineral Fuels (Petroleum, Coal, Gas)",
    OUTPUT_DIR / "dictionary_hs27_mineral_fuels.csv"
)

# 2. HS2 Chapters 30-34 - Chemicals, Fertilizers, Soaps
build_chapter_dictionary(
    df_ref,
    ['30', '31', '32', '33', '34'],
    "HS2-30-34 Chemicals, Fertilizers, Soaps",
    OUTPUT_DIR / "dictionary_hs30-34_chemicals.csv"
)

# 3. HS2 Chapters 28-29 - Inorganic/Organic Chemicals
build_chapter_dictionary(
    df_ref,
    ['28', '29'],
    "HS2-28-29 Inorganic/Organic Chemicals",
    OUTPUT_DIR / "dictionary_hs28-29_pure_chemicals.csv"
)

# 4. HS2 Chapters 76-79 - Nonferrous Metals (Aluminum, Lead, Zinc, Tin)
build_chapter_dictionary(
    df_ref,
    ['76', '78', '79', '80'],
    "HS2-76-79 Nonferrous Metals",
    OUTPUT_DIR / "dictionary_hs76-79_nonferrous_metals.csv"
)

# 5. HS2 Chapters 67-69 - Stone, Ceramic, Glass
build_chapter_dictionary(
    df_ref,
    ['67', '68', '69'],
    "HS2-67-69 Stone, Ceramic, Glass",
    OUTPUT_DIR / "dictionary_hs67-69_stone_ceramic.csv"
)

# 6. HS2 Chapters 38 - Miscellaneous Chemical Products
build_chapter_dictionary(
    df_ref,
    ['38'],
    "HS2-38 Miscellaneous Chemical Products",
    OUTPUT_DIR / "dictionary_hs38_misc_chemicals.csv"
)

stamp("")
stamp("=== Complete! ===")
stamp("")
stamp("Specialized dictionaries created:")
stamp("  1. dictionary_hs27_mineral_fuels.csv")
stamp("  2. dictionary_hs28-29_pure_chemicals.csv")
stamp("  3. dictionary_hs30-34_chemicals.csv")
stamp("  4. dictionary_hs38_misc_chemicals.csv")
stamp("  5. dictionary_hs76-79_nonferrous_metals.csv")
stamp("  6. dictionary_hs67-69_stone_ceramic.csv")
stamp("")
stamp("Each dictionary includes:")
stamp("  - HS2, HS4, HTS Description")
stamp("  - Classification (Group, Commodity, Cargo, Cargo_Detail)")
stamp("  - Keywords (Key_Phrases, Primary, Descriptors)")
stamp("  - Package Types (Top_Package_Types, Bundle_Coil_Packages)")
stamp("  - Tonnage (Min, Max, Total, Record Count)")
stamp("  - Top Shippers, Consignees, Ports")
stamp("")
stamp("Ready for review and transfer to master dictionary!")
