"""
Generate detailed carrier profile for MXRS - Marine Express Inc
Shows port of loading, port of unloading, and HS4 codes

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
DATA_DIR = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01_01_panjiva_imports_step_one")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\carrier_profile_MXRS.csv")

files = [
    DATA_DIR / "panjiva_imports_2023_20260112_STAGE00_v20260112_2052.csv",
    DATA_DIR / "panjiva_imports_2024_20260112_STAGE00_v20260112_2052.csv",
    DATA_DIR / "panjiva_imports_2025_20260112_STAGE00_v20260112_2052.csv"
]

stamp("=== Carrier Profile: MXRS - Marine Express Inc ===")
stamp("")

# Load all years and filter for MXRS
all_data = []
for file in files:
    year = file.stem.split('_')[2]
    stamp(f"Loading {year}...")
    df = pd.read_csv(file, dtype=str)

    # Filter for MXRS carrier
    df_mxrs = df[df['Carrier'].str.contains('MXRS', na=False, case=False)].copy()

    if len(df_mxrs) > 0:
        df_mxrs['Year'] = year
        all_data.append(df_mxrs)
        stamp(f"  Found {len(df_mxrs)} MXRS records")
    else:
        stamp(f"  No MXRS records found")

if not all_data:
    stamp("")
    stamp("ERROR: No records found for MXRS carrier!")
    exit(1)

# Combine
stamp("")
stamp("Combining MXRS records...")
df_mxrs = pd.concat(all_data, ignore_index=True)
stamp(f"Total MXRS records: {len(df_mxrs):,}")
stamp("")

# Convert Tons to numeric
df_mxrs['Tons_Numeric'] = pd.to_numeric(df_mxrs['Tons'], errors='coerce').fillna(0)

# Get carrier name
carrier_name = df_mxrs['Carrier'].iloc[0] if len(df_mxrs) > 0 else 'MXRS'
stamp(f"Carrier: {carrier_name}")
stamp(f"Total tonnage: {df_mxrs['Tons_Numeric'].sum():,.0f} tons")
stamp("")

# ===================================
# PORT OF LOADING ANALYSIS
# ===================================
stamp("=== PORT OF LOADING ===")
pol_summary = df_mxrs.groupby('Port of Loading (F)', dropna=False).agg({
    'Tons_Numeric': 'sum',
    'Port of Loading (F)': 'count'
}).rename(columns={
    'Tons_Numeric': 'Total_Tons',
    'Port of Loading (F)': 'Record_Count'
}).reset_index().sort_values('Total_Tons', ascending=False)

stamp(f"Total ports of loading: {len(pol_summary)}")
stamp("")
stamp("Top 15 ports of loading:")
for idx, row in pol_summary.head(15).iterrows():
    port = str(row['Port of Loading (F)'])[:50]
    tons = f"{row['Total_Tons']:,.0f}"
    records = row['Record_Count']
    pct = row['Total_Tons'] / df_mxrs['Tons_Numeric'].sum() * 100
    stamp(f"  {port:50s} {tons:>15s} tons ({pct:5.1f}%) - {records:4d} records")

stamp("")

# ===================================
# PORT OF DISCHARGE ANALYSIS
# ===================================
stamp("=== PORT OF DISCHARGE (UNLOADING) ===")
pou_summary = df_mxrs.groupby('Port of Discharge (D)', dropna=False).agg({
    'Tons_Numeric': 'sum',
    'Port of Discharge (D)': 'count'
}).rename(columns={
    'Tons_Numeric': 'Total_Tons',
    'Port of Discharge (D)': 'Record_Count'
}).reset_index().sort_values('Total_Tons', ascending=False)

stamp(f"Total ports of discharge: {len(pou_summary)}")
stamp("")
stamp("Top 15 ports of discharge:")
for idx, row in pou_summary.head(15).iterrows():
    port = str(row['Port of Discharge (D)'])[:50]
    tons = f"{row['Total_Tons']:,.0f}"
    records = row['Record_Count']
    pct = row['Total_Tons'] / df_mxrs['Tons_Numeric'].sum() * 100
    stamp(f"  {port:50s} {tons:>15s} tons ({pct:5.1f}%) - {records:4d} records")

stamp("")

# ===================================
# HS4 ANALYSIS
# ===================================
stamp("=== HS4 COMMODITIES ===")
hs4_summary = df_mxrs.groupby('HS4', dropna=False).agg({
    'Tons_Numeric': 'sum',
    'HS4': 'count'
}).rename(columns={
    'Tons_Numeric': 'Total_Tons',
    'HS4': 'Record_Count'
}).reset_index().sort_values('Total_Tons', ascending=False)

stamp(f"Total unique HS4 codes: {len(hs4_summary)}")
stamp("")
stamp("Top 20 HS4 codes by tonnage:")
for idx, row in hs4_summary.head(20).iterrows():
    hs4 = str(row['HS4'])
    tons = f"{row['Total_Tons']:,.0f}"
    records = row['Record_Count']
    pct = row['Total_Tons'] / df_mxrs['Tons_Numeric'].sum() * 100
    stamp(f"  HS4 {hs4:6s} {tons:>15s} tons ({pct:5.1f}%) - {records:4d} records")

stamp("")

# ===================================
# SAVE COMBINED PROFILE
# ===================================
stamp("Saving detailed profile...")

# Create comprehensive output
output_data = []

# Add summary
output_data.append({
    'Section': 'SUMMARY',
    'Item': 'Carrier',
    'Value': carrier_name,
    'Tons': df_mxrs['Tons_Numeric'].sum(),
    'Records': len(df_mxrs)
})

# Add POL
for idx, row in pol_summary.head(20).iterrows():
    output_data.append({
        'Section': 'PORT_OF_LOADING',
        'Item': row['Port of Loading (F)'],
        'Value': '',
        'Tons': row['Total_Tons'],
        'Records': row['Record_Count']
    })

# Add POU
for idx, row in pou_summary.head(20).iterrows():
    output_data.append({
        'Section': 'PORT_OF_DISCHARGE',
        'Item': row['Port of Discharge (D)'],
        'Value': '',
        'Tons': row['Total_Tons'],
        'Records': row['Record_Count']
    })

# Add HS4
for idx, row in hs4_summary.head(30).iterrows():
    output_data.append({
        'Section': 'HS4_COMMODITIES',
        'Item': str(row['HS4']),
        'Value': '',
        'Tons': row['Total_Tons'],
        'Records': row['Record_Count']
    })

df_output = pd.DataFrame(output_data)
df_output['Tons'] = df_output['Tons'].astype(int)
df_output.to_csv(OUTPUT_FILE, index=False)

stamp(f"Profile saved to: {OUTPUT_FILE}")
stamp("")
stamp("Complete!")
