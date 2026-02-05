"""
Generate enhanced HS code reference with full detail
Combines HTS descriptions, keywords, package types, classifications, ports, shippers, consignees

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
OLD_CARGO_DICT = Path(r"G:\My Drive\LLM\project_manifest\01.01_dictionary\01_cargo_dictionary.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\hs_code_reference_enhanced.csv")

stamp("=== Generate Enhanced HS Code Reference ===")
stamp("")

# Load HTS data for descriptions
stamp("Loading HTS data...")
df_hts = pd.read_csv(HTS_DATA, dtype=str, encoding='utf-8-sig')
stamp(f"  HTS entries: {len(df_hts):,}")

# Extract HS4 descriptions
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

# Load old cargo dictionary for classification patterns
stamp("")
stamp("Loading old cargo dictionary for classification patterns...")
df_old = pd.read_csv(OLD_CARGO_DICT, dtype=str)
stamp(f"  Old dictionary entries: {len(df_old)}")

# Create classification lookup by HS4
hs4_classifications = {}
for _, row in df_old.iterrows():
    hs4 = str(row.get('HS4', '')).strip()
    if hs4 and hs4 != 'nan':
        if hs4 not in hs4_classifications:
            hs4_classifications[hs4] = {
                'groups': [],
                'commodities': [],
                'cargos': [],
                'cargo_details': [],
                'min_tons': [],
                'max_tons': []
            }

        # Collect classification fields
        if pd.notna(row.get('Group')):
            hs4_classifications[hs4]['groups'].append(row['Group'])
        if pd.notna(row.get('Commodity')):
            hs4_classifications[hs4]['commodities'].append(row['Commodity'])
        if pd.notna(row.get('Cargo')):
            hs4_classifications[hs4]['cargos'].append(row['Cargo'])
        if pd.notna(row.get('Cargo_Detail')):
            hs4_classifications[hs4]['cargo_details'].append(row['Cargo_Detail'])
        if pd.notna(row.get('Min Tons')):
            try:
                hs4_classifications[hs4]['min_tons'].append(float(row['Min Tons']))
            except:
                pass
        if pd.notna(row.get('Max Tons')):
            try:
                hs4_classifications[hs4]['max_tons'].append(float(row['Max Tons']))
            except:
                pass

stamp(f"  HS4 codes with old classifications: {len(hs4_classifications)}")

# Load all Panjiva data
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
                'shippers': [],
                'consignees': [],
                'ports_loading': [],
                'ports_discharge': [],
                'record_count': 0,
                'total_tons': 0.0
            }

        # Collect Goods Shipped text
        goods = group['Goods Shipped'].dropna()
        hs4_data[hs4]['goods_shipped'].extend(goods.tolist())

        # Collect Package types
        pkgs = group['Pckg'].dropna()
        hs4_data[hs4]['package_types'].extend(pkgs.tolist())

        # Collect Shippers
        shippers = group['Shipper'].dropna()
        hs4_data[hs4]['shippers'].extend(shippers.tolist())

        # Collect Consignees
        consignees = group['Consignee'].dropna()
        hs4_data[hs4]['consignees'].extend(consignees.tolist())

        # Collect Ports
        ports_load = group['Port of Loading (F)'].dropna()
        hs4_data[hs4]['ports_loading'].extend(ports_load.tolist())

        ports_discharge = group['Port of Discharge (D)'].dropna()
        hs4_data[hs4]['ports_discharge'].extend(ports_discharge.tolist())

        # Count records and tons
        hs4_data[hs4]['record_count'] += len(group)
        tons = pd.to_numeric(group['Tons'], errors='coerce').sum()
        hs4_data[hs4]['total_tons'] += tons

stamp("")
stamp(f"Total unique HS4 codes found: {len(hs4_data)}")

# Build enhanced reference table
stamp("")
stamp("Building enhanced reference table...")

reference_data = []

for hs4 in sorted(hs4_data.keys()):
    data = hs4_data[hs4]

    # Get HTS description
    hts_desc = hs4_descriptions.get(hs4, '')

    # Get old classifications if available
    old_class = hs4_classifications.get(hs4, {})
    top_group = Counter(old_class.get('groups', [])).most_common(1)
    top_group_str = top_group[0][0] if top_group else ''

    top_commodity = Counter(old_class.get('commodities', [])).most_common(1)
    top_commodity_str = top_commodity[0][0] if top_commodity else ''

    top_cargo = Counter(old_class.get('cargos', [])).most_common(1)
    top_cargo_str = top_cargo[0][0] if top_cargo else ''

    top_cargo_detail = Counter(old_class.get('cargo_details', [])).most_common(1)
    top_cargo_detail_str = top_cargo_detail[0][0] if top_cargo_detail else ''

    # Get min/max tons from old dictionary
    min_tons = min(old_class.get('min_tons', [0])) if old_class.get('min_tons') else ''
    max_tons = max(old_class.get('max_tons', [0])) if old_class.get('max_tons') else ''

    # Extract top keywords from Goods Shipped
    goods_text = ' '.join(data['goods_shipped'][:1000])
    words = re.findall(r'\b[A-Z]{3,}\b|\b[A-Z][a-z]{2,}\b', goods_text)
    word_counts = Counter(words)
    top_keywords = [word for word, count in word_counts.most_common(15)]
    keywords_str = ', '.join(top_keywords)

    # Get top package types
    pkg_counts = Counter(data['package_types'])
    top_packages = [pkg for pkg, count in pkg_counts.most_common(5)]
    packages_str = ', '.join(top_packages)

    # Note bundles/coils specifically
    bundle_coil_types = [pkg for pkg in data['package_types']
                         if 'BUNDLE' in pkg.upper() or 'COIL' in pkg.upper() or
                            'ROLL' in pkg.upper() or 'SPOOL' in pkg.upper() or
                            'BDL' in pkg.upper() or 'COL' in pkg.upper()]
    bundle_coil_counts = Counter(bundle_coil_types)
    bundle_coil_str = ', '.join([f"{pkg}({ct})" for pkg, ct in bundle_coil_counts.most_common(3)])

    # Get top shippers
    shipper_counts = Counter(data['shippers'])
    top_shippers = [s for s, c in shipper_counts.most_common(5)]
    shippers_str = ' | '.join(top_shippers)

    # Get top consignees
    consignee_counts = Counter(data['consignees'])
    top_consignees = [c for c, ct in consignee_counts.most_common(5)]
    consignees_str = ' | '.join(top_consignees)

    # Get top ports
    port_load_counts = Counter(data['ports_loading'])
    top_ports_load = [p for p, c in port_load_counts.most_common(5)]
    ports_load_str = ' | '.join(top_ports_load)

    port_discharge_counts = Counter(data['ports_discharge'])
    top_ports_discharge = [p for p, c in port_discharge_counts.most_common(5)]
    ports_discharge_str = ' | '.join(top_ports_discharge)

    # Get HS2
    hs2 = hs4[:2] if len(hs4) >= 2 else ''

    reference_data.append({
        'HS2': hs2,
        'HS4': hs4,
        'HTS_Description': hts_desc,
        'Group': top_group_str,
        'Commodity': top_commodity_str,
        'Cargo': top_cargo_str,
        'Cargo_Detail': top_cargo_detail_str,
        'Min_Tons': min_tons,
        'Max_Tons': max_tons,
        'Keywords_from_Goods_Shipped': keywords_str,
        'Top_Package_Types': packages_str,
        'Bundle_Coil_Packages': bundle_coil_str,
        'Top_Shippers': shippers_str,
        'Top_Consignees': consignees_str,
        'Top_Ports_Loading': ports_load_str,
        'Top_Ports_Discharge': ports_discharge_str,
        'Record_Count': data['record_count'],
        'Total_Tons': int(data['total_tons'])
    })

# Create DataFrame
df_reference = pd.DataFrame(reference_data)

# Sort by record count descending
df_reference = df_reference.sort_values('Record_Count', ascending=False)

stamp(f"  Reference entries: {len(df_reference)}")

# Show top 5
stamp("")
stamp("Top 5 HS4 codes by record count:")
for idx, row in df_reference.head(5).iterrows():
    hs4 = row['HS4']
    desc = row['HTS_Description'][:50] if row['HTS_Description'] else 'N/A'
    count = row['Record_Count']
    cargo = row['Cargo'][:25] if row['Cargo'] else 'N/A'
    stamp(f"  {hs4}: {desc:50s} | {count:>7,} records | {cargo}")

# Save
stamp("")
stamp(f"Saving to: {OUTPUT_FILE.name}")
df_reference.to_csv(OUTPUT_FILE, index=False)

stamp("")
stamp("Complete!")
stamp("")
stamp("Enhanced reference includes:")
stamp("  - HTS official descriptions")
stamp("  - Classifications from old dictionaries")
stamp("  - Keywords from Goods Shipped")
stamp("  - Package types (bundles/coils)")
stamp("  - Top shippers and consignees")
stamp("  - Top loading and discharge ports")
stamp("  - Min/Max tonnage ranges")
stamp("")
stamp(f"Review file: {OUTPUT_FILE}")
