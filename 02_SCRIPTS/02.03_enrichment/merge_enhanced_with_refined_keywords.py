"""
Merge enhanced reference with refined keywords
Combines full detail (ports, shippers, tonnage) with categorized keywords

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
ENHANCED_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\hs_code_reference_enhanced.csv")
REFINED_KEYWORDS = Path(r"G:\My Drive\LLM\project_manifest\user_notes\hs_code_keywords_refined.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\hs_code_reference_complete.csv")

stamp("=== Merge Enhanced Reference with Refined Keywords ===")
stamp("")

# Load files
stamp("Loading enhanced reference...")
df_enhanced = pd.read_csv(ENHANCED_FILE, dtype=str)
stamp(f"  Entries: {len(df_enhanced)}")

stamp("")
stamp("Loading refined keywords...")
df_keywords = pd.read_csv(REFINED_KEYWORDS, dtype=str)
stamp(f"  Entries: {len(df_keywords)}")

# Merge on HS4
stamp("")
stamp("Merging data...")
df_merged = df_enhanced.merge(
    df_keywords[['HS4', 'Key_Phrases', 'Primary_Keywords', 'Descriptor_Keywords']],
    on='HS4',
    how='left'
)

# Drop old keyword column and reorder
if 'Keywords_from_Goods_Shipped' in df_merged.columns:
    df_merged = df_merged.drop(columns=['Keywords_from_Goods_Shipped'])

# Reorder columns for better readability
column_order = [
    'HS2', 'HS4', 'HTS_Description',
    'Group', 'Commodity', 'Cargo', 'Cargo_Detail',
    'Key_Phrases', 'Primary_Keywords', 'Descriptor_Keywords',
    'Top_Package_Types', 'Bundle_Coil_Packages',
    'Min_Tons', 'Max_Tons',
    'Top_Shippers', 'Top_Consignees',
    'Top_Ports_Loading', 'Top_Ports_Discharge',
    'Record_Count', 'Total_Tons'
]

df_merged = df_merged[column_order]

stamp(f"  Merged entries: {len(df_merged)}")
stamp(f"  Total columns: {len(df_merged.columns)}")

# Show examples
stamp("")
stamp("Examples of complete reference:")
stamp("")

# Steel pipe example
steel_pipe = df_merged[df_merged['HS4'] == '7304'].iloc[0] if '7304' in df_merged['HS4'].values else None
if steel_pipe is not None:
    stamp("HS4 7304 (Seamless Steel Tubes/Pipes):")
    stamp(f"  HTS Desc: {steel_pipe['HTS_Description'][:60]}")
    stamp(f"  Classification: {steel_pipe['Group']} > {steel_pipe['Commodity']} > {steel_pipe['Cargo']}")
    stamp(f"  Key Phrases: {steel_pipe['Key_Phrases']}")
    stamp(f"  Primary Keywords: {steel_pipe['Primary_Keywords'][:60]}")
    stamp(f"  Descriptors: {steel_pipe['Descriptor_Keywords']}")
    stamp(f"  Packages: {steel_pipe['Top_Package_Types']}")
    stamp(f"  Bundles/Coils: {steel_pipe['Bundle_Coil_Packages']}")
    stamp(f"  Records: {steel_pipe['Record_Count']:>8s} | Tons: {steel_pipe['Total_Tons']:>10s}")
    stamp(f"  Top Shippers: {steel_pipe['Top_Shippers'][:80]}")
    stamp(f"  Top Ports (Load): {steel_pipe['Top_Ports_Loading'][:80]}")
    stamp("")

# Crude oil example
crude = df_merged[df_merged['HS4'] == '2709'].iloc[0] if '2709' in df_merged['HS4'].values else None
if crude is not None:
    stamp("HS4 2709 (Crude Petroleum Oil):")
    stamp(f"  HTS Desc: {crude['HTS_Description'][:60]}")
    stamp(f"  Key Phrases: {crude['Key_Phrases']}")
    stamp(f"  Primary Keywords: {crude['Primary_Keywords'][:60]}")
    stamp(f"  Descriptors: {crude['Descriptor_Keywords']}")
    stamp(f"  Records: {crude['Record_Count']:>8s} | Tons: {crude['Total_Tons']:>10s}")
    stamp("")

# Save
stamp("")
stamp(f"Saving complete reference to: {OUTPUT_FILE.name}")
df_merged.to_csv(OUTPUT_FILE, index=False)

stamp("")
stamp("Complete!")
stamp("")
stamp("Complete reference includes:")
stamp("  - HTS descriptions")
stamp("  - Group/Commodity/Cargo/Cargo_Detail classifications")
stamp("  - Key Phrases (strong multi-word matches)")
stamp("  - Primary Keywords (standalone product terms)")
stamp("  - Descriptor Keywords (modifiers/qualifiers)")
stamp("  - Package types and bundle/coil counts")
stamp("  - Min/Max tonnage ranges")
stamp("  - Top shippers and consignees")
stamp("  - Top loading and discharge ports")
stamp("  - Record counts and total tonnage")
