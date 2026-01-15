"""
Match USACE Clearance Data to Panjiva Export Port Calls - VECTORIZED VERSION
Version: 1.0.0
Date: 2026-01-15

Purpose:
- Match USACE outbound clearance records to Panjiva export port calls
- Binary matching: exact match (Vessel + Port + Date +/-tolerance) or no match
- No "smart" logic - if keys don't match, leave unmatched

Strategy:
- Pass 1: Vessel Name + Port + Date (+/-2 days)
- Pass 2: Extended tolerance (+/-4 days)
- Pass 3: Final tolerance (+/-7 days)

Note: Export data lacks IMO, so matching by vessel name only

Input:
- USACE: 02_STAGE02_CLASSIFICATION/usace_2023_outbound_clearance_transformed_v2.2.0.csv
- Panjiva: 01_STAGE01_PREPROCESSING/01.01_annual_files/panjiva_exports_2023_PORTCALL_*.csv

Output: 02_STAGE02_CLASSIFICATION/usace_2023_clearance_with_panjiva_match_v1.0.0.csv
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path
from datetime import timedelta

# File paths
USACE_FILE = Path(r"G:\My Drive\LLM\project_manifest\02_STAGE02_CLASSIFICATION\usace_2023_outbound_clearance_transformed_v2.2.0.csv")
PANJIVA_DIR = Path(r"G:\My Drive\LLM\project_manifest\01_STAGE01_PREPROCESSING\01.01_annual_files")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\02_STAGE02_CLASSIFICATION\usace_2023_clearance_with_panjiva_match_v1.0.0.csv")

print("="*80)
print("USACE-PANJIVA CLEARANCE MATCHING v1.0.0 (FAST VECTORIZED)")
print("="*80)

# Load USACE clearance data
print(f"\n1. Loading USACE clearance data...")
usace = pd.read_csv(USACE_FILE, low_memory=False)
print(f"   Records: {len(usace):,}")

# Parse USACE dates (mmydd format)
print(f"\n2. Parsing USACE dates (mmydd format)...")
def parse_usace_date(date_val):
    """Convert mmydd integer to proper date (e.g., 8329 -> 2023-08-29)"""
    if pd.isna(date_val):
        return None
    try:
        date_str = str(int(date_val)).zfill(5)
        month = int(date_str[:2])
        year_digit = int(date_str[2])
        day = int(date_str[3:])
        year = 2020 + year_digit
        return pd.Timestamp(year=year, month=month, day=day)
    except:
        return None

usace['Clearance_Date_Parsed'] = usace['Clearance_Date'].apply(parse_usace_date)
print(f"   Sample dates: {usace['Clearance_Date_Parsed'].dropna().head(3).tolist()}")

# Load Panjiva export port call data
print(f"\n3. Loading Panjiva export port call data...")
export_files = list(PANJIVA_DIR.glob("panjiva_exports_2023_PORTCALL_*.csv"))
if not export_files:
    print("   ERROR: No export port call files found!")
    exit(1)

export_files.sort()
panjiva_file = export_files[-1]
print(f"   Loading: {panjiva_file.name}")

panjiva = pd.read_csv(panjiva_file, low_memory=False)
panjiva['Shipment_Date'] = pd.to_datetime(panjiva['Shipment_Date'], errors='coerce')
print(f"   Port calls: {len(panjiva):,}")

# Normalize functions
def normalize_vessel_name(name):
    if pd.isna(name) or name == '':
        return ''
    normalized = re.sub(r'[^a-zA-Z0-9\s]', '', str(name))
    return ' '.join(normalized.lower().split())

def normalize_port_name(name):
    """Extract city name only for matching (state codes don't match between datasets)"""
    if pd.isna(name) or name == '':
        return ''
    name = str(name).upper()
    parts = name.split(',')
    if len(parts) > 0:
        city = parts[0].strip()
        # Remove common prefixes
        city = city.replace('PORT OF ', '').replace('PORT ', '').replace('THE ', '')
        # Remove suffixes that vary
        city = city.replace(' UNIFIED PORT DISTRICT', '').replace(' PORT DISTRICT', '')
        city = city.replace(' PORT AUTHORITY', '').replace(' AUTHORITY OF HARRIS COUNTY', '')
        city = city.replace(' STATE PORT AUTHORITY', '').replace(' STATE AUTHORITY', '')
        return city.strip()
    return name.upper()

print(f"\n4. Normalizing matching keys...")
usace['Vessel_Norm'] = usace['Vessel'].apply(normalize_vessel_name)
usace['Port_Norm'] = usace['Clearance_Port_Name'].apply(normalize_port_name)

panjiva['Vessel_Norm'] = panjiva['Vessel'].apply(normalize_vessel_name)
panjiva['Port_Norm'] = panjiva['Port_of_Lading'].apply(normalize_port_name)

# Create expanded Panjiva with date offsets
print(f"\n5. Creating date-expanded Panjiva dataset...")
panjiva_expanded = []
for offset in range(-7, 8):  # -7 to +7 days
    temp = panjiva.copy()
    temp['Match_Date'] = temp['Shipment_Date'] + pd.Timedelta(days=offset)
    temp['Days_Offset'] = abs(offset)
    # Assign Pass based on tolerance
    if abs(offset) <= 2:
        temp['Pass'] = 1
    elif abs(offset) <= 4:
        temp['Pass'] = 2
    else:
        temp['Pass'] = 3
    panjiva_expanded.append(temp)

panjiva_expanded = pd.concat(panjiva_expanded, ignore_index=True)
print(f"   Expanded to {len(panjiva_expanded):,} date-offset combinations")

# Match by Vessel Name + Port + Date
print(f"\n6. MATCHING BY VESSEL NAME + PORT + DATE...")
usace['Match_Date'] = usace['Clearance_Date_Parsed']

# Merge on Vessel + Port + Date
matched = usace.merge(
    panjiva_expanded[['VOY_RECID', 'Vessel_Norm', 'Port_Norm', 'Match_Date', 'Carrier',
                      'Shipper', 'Total_Tons', 'Days_Offset', 'Pass']],
    on=['Vessel_Norm', 'Port_Norm', 'Match_Date'],
    how='left',
    suffixes=('', '_panjiva')
)

# Keep best match per USACE record (lowest date offset)
matched = matched.sort_values('Days_Offset')
matched_best = matched.groupby(matched.index).first()

# Count matches
total_matched = matched_best['VOY_RECID'].notna().sum()
print(f"   [OK] Total matches found: {total_matched:,}")

# Prepare final output
print(f"\n7. Preparing final output...")
usace_final = usace.copy()
usace_final['VOY_RECID'] = matched_best['VOY_RECID']
usace_final['Panjiva_Carrier'] = matched_best['Carrier']
usace_final['Panjiva_Shipper'] = matched_best['Shipper']
usace_final['Panjiva_Tons'] = matched_best['Total_Tons']
usace_final['Match_Days_Offset'] = matched_best['Days_Offset']
usace_final['Match_Pass'] = matched_best['Pass']
usace_final['Match_Method'] = 'Vessel_Name'
usace_final.loc[usace_final['VOY_RECID'].isna(), 'Match_Method'] = None

# Drop temporary columns
usace_final.drop(['Vessel_Norm', 'Port_Norm', 'Match_Date', 'Clearance_Date_Parsed'],
                 axis=1, inplace=True, errors='ignore')

# Save
usace_final.to_csv(OUTPUT_FILE, index=False)
print(f"   Saved: {OUTPUT_FILE.name}")

# Summary
print("\n" + "="*80)
print("MATCHING SUMMARY")
print("="*80)

total_matched = usace_final['VOY_RECID'].notna().sum()
total_unmatched = usace_final['VOY_RECID'].isna().sum()
pass1_matches = usace_final[usace_final['Match_Pass'] == 1].shape[0]
pass2_matches = usace_final[usace_final['Match_Pass'] == 2].shape[0]
pass3_matches = usace_final[usace_final['Match_Pass'] == 3].shape[0]

print(f"\nTotal USACE clearance records: {len(usace_final):,}")
print(f"\nMatching Results:")
print(f"  [OK] Pass 1 (+/-2 days): {pass1_matches:,} ({pass1_matches/len(usace_final)*100:.1f}%)")
print(f"  [OK] Pass 2 (+/-4 days): {pass2_matches:,} ({pass2_matches/len(usace_final)*100:.1f}%)")
print(f"  [OK] Pass 3 (+/-7 days): {pass3_matches:,} ({pass3_matches/len(usace_final)*100:.1f}%)")
print(f"  [OK] Total matched:      {total_matched:,} ({total_matched/len(usace_final)*100:.1f}%)")
print(f"  [--] Unmatched:          {total_unmatched:,} ({total_unmatched/len(usace_final)*100:.1f}%)")

if total_matched > 0:
    print(f"\nDate offset distribution:")
    for offset in range(8):
        count = (usace_final['Match_Days_Offset'] == offset).sum()
        if count > 0:
            print(f"  {offset} days: {count:,} ({count/total_matched*100:.1f}%)")

    matched_with_tons = usace_final[usace_final['Panjiva_Tons'].notna()]
    if len(matched_with_tons) > 0:
        print(f"\nTonnage statistics:")
        print(f"  Total: {matched_with_tons['Panjiva_Tons'].sum():,.0f} tons")
        print(f"  Average: {matched_with_tons['Panjiva_Tons'].mean():,.0f} tons/port call")

    # Sample
    print(f"\n" + "="*80)
    print("SAMPLE MATCHED RECORDS (First 5)")
    print("="*80)
    sample = usace_final[usace_final['VOY_RECID'].notna()][
        ['Vessel', 'Clearance_Port_Name', 'Clearance_Date', 'VOY_RECID', 'Panjiva_Tons', 'Match_Days_Offset', 'Match_Method']
    ].head(5)
    try:
        print(sample.to_string(index=False))
    except UnicodeEncodeError:
        print("   [Sample display skipped due to unicode characters]")

print(f"\n" + "="*80)
print("COMPLETE!")
print("="*80)
print(f"\nOutput: {OUTPUT_FILE.name}")
print(f"Next step: Add port rollups to export data")
