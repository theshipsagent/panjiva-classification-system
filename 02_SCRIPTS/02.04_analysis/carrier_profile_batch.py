"""
Generate carrier profiles for multiple carriers
Shows port of loading, port of discharge, and HS4 codes

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def generate_carrier_profile(scac_code, carrier_list):
    """Generate profile for a single carrier by SCAC code"""

    # Paths
    DATA_DIR = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01_01_panjiva_imports_step_one")
    OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes") / f"carrier_profile_{scac_code}.csv"

    files = [
        DATA_DIR / "panjiva_imports_2023_20260112_STAGE00_v20260112_2052.csv",
        DATA_DIR / "panjiva_imports_2024_20260112_STAGE00_v20260112_2052.csv",
        DATA_DIR / "panjiva_imports_2025_20260112_STAGE00_v20260112_2052.csv"
    ]

    stamp(f"=== Carrier Profile: {scac_code} ===")

    # Load all years and filter for carrier
    all_data = []
    for file in files:
        year = file.stem.split('_')[2]
        df = pd.read_csv(file, dtype=str)

        # Filter for carrier by SCAC code
        df_carrier = df[df['Carrier'].str.contains(scac_code, na=False, case=False)].copy()

        if len(df_carrier) > 0:
            df_carrier['Year'] = year
            all_data.append(df_carrier)

    if not all_data:
        stamp(f"  No records found for {scac_code}")
        return None

    # Combine
    df_carrier = pd.concat(all_data, ignore_index=True)
    stamp(f"  Total records: {len(df_carrier):,}")

    # Convert Tons to numeric
    df_carrier['Tons_Numeric'] = pd.to_numeric(df_carrier['Tons'], errors='coerce').fillna(0)

    # Get carrier name
    carrier_name = df_carrier['Carrier'].iloc[0] if len(df_carrier) > 0 else scac_code
    total_tons = df_carrier['Tons_Numeric'].sum()
    stamp(f"  Carrier: {carrier_name}")
    stamp(f"  Total tonnage: {total_tons:,.0f} tons")

    # PORT OF LOADING
    pol_summary = df_carrier.groupby('Port of Loading (F)', dropna=False).agg({
        'Tons_Numeric': 'sum',
        'Port of Loading (F)': 'count'
    }).rename(columns={
        'Tons_Numeric': 'Total_Tons',
        'Port of Loading (F)': 'Record_Count'
    }).reset_index().sort_values('Total_Tons', ascending=False)

    # PORT OF DISCHARGE
    pou_summary = df_carrier.groupby('Port of Discharge (D)', dropna=False).agg({
        'Tons_Numeric': 'sum',
        'Port of Discharge (D)': 'count'
    }).rename(columns={
        'Tons_Numeric': 'Total_Tons',
        'Port of Discharge (D)': 'Record_Count'
    }).reset_index().sort_values('Total_Tons', ascending=False)

    # HS4
    hs4_summary = df_carrier.groupby('HS4', dropna=False).agg({
        'Tons_Numeric': 'sum',
        'HS4': 'count'
    }).rename(columns={
        'Tons_Numeric': 'Total_Tons',
        'HS4': 'Record_Count'
    }).reset_index().sort_values('Total_Tons', ascending=False)

    stamp(f"  Ports of loading: {len(pol_summary)}")
    stamp(f"  Ports of discharge: {len(pou_summary)}")
    stamp(f"  HS4 codes: {len(hs4_summary)}")

    # Create output
    output_data = []

    # Summary
    output_data.append({
        'Section': 'SUMMARY',
        'Item': 'Carrier',
        'Value': carrier_name,
        'Tons': int(total_tons),
        'Records': len(df_carrier)
    })

    # POL (top 20)
    for idx, row in pol_summary.head(20).iterrows():
        output_data.append({
            'Section': 'PORT_OF_LOADING',
            'Item': row['Port of Loading (F)'],
            'Value': '',
            'Tons': int(row['Total_Tons']),
            'Records': row['Record_Count']
        })

    # POU (top 20)
    for idx, row in pou_summary.head(20).iterrows():
        output_data.append({
            'Section': 'PORT_OF_DISCHARGE',
            'Item': row['Port of Discharge (D)'],
            'Value': '',
            'Tons': int(row['Total_Tons']),
            'Records': row['Record_Count']
        })

    # HS4 (top 30)
    for idx, row in hs4_summary.head(30).iterrows():
        output_data.append({
            'Section': 'HS4_COMMODITIES',
            'Item': str(row['HS4']),
            'Value': '',
            'Tons': int(row['Total_Tons']),
            'Records': row['Record_Count']
        })

    df_output = pd.DataFrame(output_data)
    df_output.to_csv(OUTPUT_FILE, index=False)
    stamp(f"  Saved: {OUTPUT_FILE}")

    return {
        'scac': scac_code,
        'name': carrier_name,
        'records': len(df_carrier),
        'tons': int(total_tons),
        'pol_count': len(pol_summary),
        'pou_count': len(pou_summary),
        'hs4_count': len(hs4_summary)
    }

# Carrier list
carriers = [
    'LLKT',    # Lower Lakes Towing Ltd
    'SYMQ',    # St Marys Cement Inc (Canada)
    'WETB',    # Western Towboat Company
    'MLTD',    # Mercury Launch & Tug Ltd
    'LOWK',    # Lower Lakes Transportation Company
    'OTNB',    # Olympic Tug & Barge
    'SBCG',    # Seabridge Marine Services Ltd
    'PCMV',    # Port City Marine Services
    'ISCH',    # Interlake Steamship Company, The
    'TCCQ',    # Transatlantic Cement Carriers Inc
    'PTYE',    # Pacific Tug Company Llc
    'ISLT',    # Island Tug And Barge Co.
    'VETB'     # Vanenkevort Tug & Barge Inc
]

stamp("=== Batch Carrier Profile Generation ===")
stamp(f"Processing {len(carriers)} carriers...")
stamp("")

results = []
for scac in carriers:
    result = generate_carrier_profile(scac, carriers)
    if result:
        results.append(result)
    stamp("")

# Summary report
stamp("=== SUMMARY REPORT ===")
stamp("")
stamp(f"{'SCAC':<6s} {'Records':>10s} {'Tons':>15s} {'POL':>6s} {'POU':>6s} {'HS4':>6s}")
stamp("-" * 70)

for r in results:
    stamp(f"{r['scac']:<6s} {r['records']:>10,d} {r['tons']:>15,d} {r['pol_count']:>6d} {r['pou_count']:>6d} {r['hs4_count']:>6d}")

stamp("")
stamp(f"Total carriers processed: {len(results)}")
stamp("Complete!")
