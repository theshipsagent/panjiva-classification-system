"""
Generate comprehensive HS code reference list
Combines HTS descriptions, Panjiva keywords, package types, and classifications

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
from collections import Counter
import re

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
HTS_DATA = Path(r"G:\My Drive\LLM\project_manifest\_archive\user_notes_old\htsdata.csv")
PANJIVA_DIR = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01_01_panjiva_imports_step_one")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\hs_code_reference_analysis.csv")

stamp("=== Generate HS Code Reference Analysis ===")
stamp("")

# Load HTS data for descriptions
stamp("Loading HTS data...")
df_hts = pd.read_csv(HTS_DATA, dtype=str, encoding='utf-8-sig')
stamp(f"  HTS entries: {len(df_hts):,}")

# Extract HS4 descriptions (4-digit codes at Indent 0)
stamp("")
stamp("Extracting HS4 descriptions from HTS data...")
hs4_descriptions = {}

for _, row in df_hts.iterrows():
    hts_num = str(row['HTS Number']).strip().replace('"', '')
    indent = str(row['Indent']).strip()
    desc = str(row['Description']).strip().replace('"', '')

    if indent == '0' and desc and desc != 'nan':
        match = re.match(r'^(\d{4})', hts_num)
        if match:
            hs4_code = match.group(1)
            if hs4_code not in hs4_descriptions:
                desc_clean = desc.strip(':').strip()
                if len(desc_clean) > 3:
                    hs4_descriptions[hs4_code] = desc_clean

stamp(f"  HS4 codes with descriptions: {len(hs4_descriptions)}")

# Load all Panjiva data to extract keywords and package types
stamp("")
stamp("Loading Panjiva data (all 3 years)...")
panjiva_files = list(PANJIVA_DIR.glob("*.csv"))
stamp(f"  Files found: {len(panjiva_files)}")

# Dictionary to accumulate data by HS4
hs4_data = {}

for file in panjiva_files:
    stamp(f"  Processing: {file.name}")
    df = pd.read_csv(file, dtype=str, low_memory=False)

    # Filter to records with HS4 codes
    df_with_hs4 = df[df['HS4'].notna()].copy()

    stamp(f"    Records with HS4: {len(df_with_hs4):,}")

    # Group by HS4 and collect data
    for hs4, group in df_with_hs4.groupby('HS4'):
        if hs4 not in hs4_data:
            hs4_data[hs4] = {
                'goods_shipped': [],
                'package_types': [],
                'groups': [],
                'commodities': [],
                'cargos': [],
                'cargo_details': [],
                'record_count': 0,
                'total_tons': 0.0
            }

        # Collect Goods Shipped text
        goods = group['Goods Shipped'].dropna()
        hs4_data[hs4]['goods_shipped'].extend(goods.tolist())

        # Collect Package types
        pkgs = group['Pckg'].dropna()
        hs4_data[hs4]['package_types'].extend(pkgs.tolist())

        # Collect classifications
        groups_col = group['Group'].dropna()
        hs4_data[hs4]['groups'].extend(groups_col.tolist())

        comms = group['Commodity'].dropna()
        hs4_data[hs4]['commodities'].extend(comms.tolist())

        cargos = group['Cargo'].dropna()
        hs4_data[hs4]['cargos'].extend(cargos.tolist())

        details = group['Cargo Detail'].dropna()
        hs4_data[hs4]['cargo_details'].extend(details.tolist())

        # Count records and tons
        hs4_data[hs4]['record_count'] += len(group)
        tons = pd.to_numeric(group['Tons'], errors='coerce').sum()
        hs4_data[hs4]['total_tons'] += tons

stamp("")
stamp(f"Total unique HS4 codes found: {len(hs4_data)}")

# Build reference table
stamp("")
stamp("Building reference table...")

reference_data = []

for hs4 in sorted(hs4_data.keys()):
    data = hs4_data[hs4]

    # Get HTS description
    hts_desc = hs4_descriptions.get(hs4, '')

    # Extract top keywords from Goods Shipped (max 10)
    goods_text = ' '.join(data['goods_shipped'][:1000])  # Sample first 1000
    # Extract meaningful words (3+ chars, uppercase words are product names)
    words = re.findall(r'\b[A-Z]{3,}\b|\b[A-Z][a-z]{2,}\b', goods_text)
    word_counts = Counter(words)
    top_keywords = [word for word, count in word_counts.most_common(15)]
    keywords_str = ', '.join(top_keywords)

    # Get top package types (max 5)
    pkg_counts = Counter(data['package_types'])
    top_packages = [pkg for pkg, count in pkg_counts.most_common(5)]
    packages_str = ', '.join(top_packages)

    # Note bundles/coils specifically
    bundle_coil_types = [pkg for pkg in data['package_types']
                         if 'BUNDLE' in pkg.upper() or 'COIL' in pkg.upper() or
                            'ROLL' in pkg.upper() or 'SPOOL' in pkg.upper()]
    bundle_coil_counts = Counter(bundle_coil_types)
    bundle_coil_str = ', '.join([f"{pkg}({ct})" for pkg, ct in bundle_coil_counts.most_common(3)])

    # Get top classifications
    top_group = Counter(data['groups']).most_common(1)
    top_group_str = top_group[0][0] if top_group else ''

    top_commodity = Counter(data['commodities']).most_common(1)
    top_commodity_str = top_commodity[0][0] if top_commodity else ''

    top_cargo = Counter(data['cargos']).most_common(1)
    top_cargo_str = top_cargo[0][0] if top_cargo else ''

    top_cargo_detail = Counter(data['cargo_details']).most_common(1)
    top_cargo_detail_str = top_cargo_detail[0][0] if top_cargo_detail else ''

    # Get HS2
    hs2 = hs4[:2] if len(hs4) >= 2 else ''

    reference_data.append({
        'HS2': hs2,
        'HS4': hs4,
        'HTS_Description': hts_desc,
        'Top_Group': top_group_str,
        'Top_Commodity': top_commodity_str,
        'Top_Cargo': top_cargo_str,
        'Top_Cargo_Detail': top_cargo_detail_str,
        'Keywords_from_Goods_Shipped': keywords_str,
        'Top_Package_Types': packages_str,
        'Bundle_Coil_Packages': bundle_coil_str,
        'Record_Count': data['record_count'],
        'Total_Tons': int(data['total_tons'])
    })

# Create DataFrame
df_reference = pd.DataFrame(reference_data)

# Sort by record count descending
df_reference = df_reference.sort_values('Record_Count', ascending=False)

stamp(f"  Reference entries: {len(df_reference)}")

# Show top 10
stamp("")
stamp("Top 10 HS4 codes by record count:")
for idx, row in df_reference.head(10).iterrows():
    hs4 = row['HS4']
    desc = row['HTS_Description'][:40] if row['HTS_Description'] else 'N/A'
    count = row['Record_Count']
    cargo = row['Top_Cargo'][:20] if row['Top_Cargo'] else 'N/A'
    stamp(f"  {hs4}: {desc:40s} | {count:>7,} records | {cargo}")

# Save
stamp("")
stamp(f"Saving to: {OUTPUT_FILE.name}")
df_reference.to_csv(OUTPUT_FILE, index=False)

stamp("")
stamp("Complete!")
stamp("")
stamp("Review the file before updating the dictionary.")
stamp(f"File location: {OUTPUT_FILE}")
