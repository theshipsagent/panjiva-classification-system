"""
Match USACE Entrance Data to Panjiva Import Port Calls - VECTORIZED VERSION
Version: 1.3.0
Date: 2026-01-15

FAST implementation using pandas merge operations instead of row iteration
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path
from datetime import timedelta

# File paths
USACE_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_inbound_entrance_transformed_v2.1.0.csv")
PANJIVA_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01.01_annual_files\panjiva_imports_2023_PORTCALL_v20260115_1530.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_entrance_with_panjiva_match_v1.3.0.csv")

print("="*80)
print("USACE-PANJIVA PORT CALL MATCHING v1.3.0 (FAST VECTORIZED)")
print("="*80)

# Load data
print(f"\n1. Loading USACE entrance data...")
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

usace['Arrival_Date'] = usace['Arrival_Date'].apply(parse_usace_date)
print(f"   Sample dates: {usace['Arrival_Date'].dropna().head(3).tolist()}")

print(f"\n3. Loading Panjiva port call data...")
panjiva = pd.read_csv(PANJIVA_FILE, low_memory=False)
panjiva['Arrival Date'] = pd.to_datetime(panjiva['Arrival Date'], errors='coerce')
print(f"   Records: {len(panjiva):,}")

# Aggregate Panjiva
print(f"\n4. Aggregating Panjiva by VOY_RECID...")
panjiva_agg = panjiva.groupby('VOY_RECID').agg({
    'Vessel': 'first',
    'Port of Discharge (D)': 'first',
    'Arrival Date': 'first',
    'Carrier Name': 'first',
    'Group_Concat': 'first',
    'Commodity_Concat': 'first',
    'Tons': 'sum',
    'IMO': 'first'
}).reset_index()
panjiva_agg.columns = ['VOY_RECID', 'Vessel', 'Port', 'Arrival_Date', 'Carrier', 'Group_Concat', 'Commodity_Concat', 'Total_Tons', 'IMO']
print(f"   Port calls: {len(panjiva_agg):,}")

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

def normalize_imo(imo_val):
    if pd.isna(imo_val):
        return ''
    try:
        imo_clean = re.sub(r'[^0-9]', '', str(imo_val))
        if imo_clean:
            return imo_clean
    except:
        pass
    return ''

print(f"\n5. Normalizing matching keys...")
usace['Vessel_Norm'] = usace['Vessel'].apply(normalize_vessel_name)
usace['Port_Norm'] = usace['Arrival_Port_Name'].apply(normalize_port_name)
usace['IMO_Norm'] = usace['IMO'].apply(normalize_imo)

panjiva_agg['Vessel_Norm'] = panjiva_agg['Vessel'].apply(normalize_vessel_name)
panjiva_agg['Port_Norm'] = panjiva_agg['Port'].apply(normalize_port_name)
panjiva_agg['IMO_Norm'] = panjiva_agg['IMO'].apply(normalize_imo)

# Create expanded Panjiva with date offsets
print(f"\n6. Creating date-expanded Panjiva dataset...")
panjiva_expanded = []
for offset in range(-4, 5):  # -4 to +4 days
    temp = panjiva_agg.copy()
    temp['Match_Date'] = temp['Arrival_Date'] + pd.Timedelta(days=offset)
    temp['Days_Offset'] = abs(offset)
    temp['Pass'] = 1 if abs(offset) <= 2 else 2
    panjiva_expanded.append(temp)

panjiva_expanded = pd.concat(panjiva_expanded, ignore_index=True)
print(f"   Expanded to {len(panjiva_expanded):,} date-offset combinations")

# Strategy 1: Match by IMO + Port + Date
print(f"\n7. MATCHING BY IMO + PORT + DATE...")
usace['Match_Date'] = usace['Arrival_Date']

# Filter Panjiva to records with IMO
panjiva_with_imo = panjiva_expanded[panjiva_expanded['IMO_Norm'] != ''].copy()
print(f"   Panjiva records with IMO: {panjiva_with_imo['VOY_RECID'].nunique():,}")

# Merge on IMO + Port + Date
matched_imo = usace.merge(
    panjiva_with_imo[['VOY_RECID', 'IMO_Norm', 'Port_Norm', 'Match_Date', 'Carrier', 'Group_Concat', 'Commodity_Concat', 'Total_Tons', 'Days_Offset', 'Pass']],
    on=['IMO_Norm', 'Port_Norm', 'Match_Date'],
    how='left',
    suffixes=('', '_panjiva')
)

# Keep best match per USACE record (lowest date offset)
matched_imo = matched_imo.sort_values('Days_Offset')
matched_imo_best = matched_imo.groupby(matched_imo.index).first()

# Count IMO matches
imo_matches = matched_imo_best['VOY_RECID'].notna().sum()
print(f"   [OK] IMO matches found: {imo_matches:,}")

# Strategy 2: Match by Vessel Name + Port + Date (for unmatched)
print(f"\n8. MATCHING BY VESSEL NAME + PORT + DATE (for unmatched)...")
# Reset indices
usace = usace.reset_index(drop=True)
matched_imo_best = matched_imo_best.reset_index(drop=True)

unmatched_mask = matched_imo_best['VOY_RECID'].isna()
print(f"   Unmatched records: {unmatched_mask.sum():,}")

if unmatched_mask.sum() > 0:
    # Match by vessel name
    usace['Match_Date'] = usace['Arrival_Date']
    matched_vessel = usace[unmatched_mask].merge(
        panjiva_expanded[['VOY_RECID', 'Vessel_Norm', 'Port_Norm', 'Match_Date', 'Carrier', 'Group_Concat', 'Commodity_Concat', 'Total_Tons', 'Days_Offset', 'Pass']],
        on=['Vessel_Norm', 'Port_Norm', 'Match_Date'],
        how='left',
        suffixes=('', '_panjiva')
    )

    # Keep best match per record
    matched_vessel = matched_vessel.sort_values('Days_Offset')
    matched_vessel_best = matched_vessel.groupby(matched_vessel.index).first()

    # Count vessel name matches
    vessel_matches = matched_vessel_best['VOY_RECID'].notna().sum()
    print(f"   [OK] Vessel name matches found: {vessel_matches:,}")

    # Update matched_imo_best with vessel name matches
    # Get indices where we found matches
    unmatched_indices = matched_imo_best[unmatched_mask].index
    for i, idx in enumerate(unmatched_indices):
        if i < len(matched_vessel_best):
            for col in ['VOY_RECID', 'Carrier', 'Group_Concat', 'Commodity_Concat', 'Total_Tons', 'Days_Offset', 'Pass']:
                if col in matched_vessel_best.columns and pd.notna(matched_vessel_best.iloc[i][col]):
                    matched_imo_best.at[idx, col] = matched_vessel_best.iloc[i][col]

# Prepare final output
print(f"\n9. Preparing final output...")
usace_final = usace.copy()
usace_final['VOY_RECID'] = matched_imo_best['VOY_RECID']
usace_final['Panjiva_Carrier'] = matched_imo_best['Carrier']
usace_final['Panjiva_Group'] = matched_imo_best['Group_Concat']
usace_final['Panjiva_Commodity'] = matched_imo_best['Commodity_Concat']
usace_final['Panjiva_Tons'] = matched_imo_best['Total_Tons']
usace_final['Match_Days_Offset'] = matched_imo_best['Days_Offset']
usace_final['Match_Pass'] = matched_imo_best['Pass']

# Determine match method
usace_final['Match_Method'] = np.nan
usace_final.loc[usace_final['VOY_RECID'].notna() & (usace_final['IMO_Norm'] != ''), 'Match_Method'] = 'IMO'
usace_final.loc[usace_final['VOY_RECID'].notna() & (usace_final['IMO_Norm'] == ''), 'Match_Method'] = 'Vessel_Name'

# Drop temporary columns
usace_final.drop(['Vessel_Norm', 'Port_Norm', 'IMO_Norm', 'Match_Date'], axis=1, inplace=True)

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

print(f"\nTotal USACE records: {len(usace_final):,}")
print(f"\nMatching Results:")
print(f"  [OK] Pass 1 (+/-2 days): {pass1_matches:,} ({pass1_matches/len(usace_final)*100:.1f}%)")
print(f"  [OK] Pass 2 (+/-4 days): {pass2_matches:,} ({pass2_matches/len(usace_final)*100:.1f}%)")
print(f"  [OK] Total matched:      {total_matched:,} ({total_matched/len(usace_final)*100:.1f}%)")
print(f"  [--] Unmatched:          {total_unmatched:,} ({total_unmatched/len(usace_final)*100:.1f}%)")

if total_matched > 0:
    print(f"\nMatch method breakdown:")
    method_counts = usace_final['Match_Method'].value_counts()
    for method, count in method_counts.items():
        print(f"  {method}: {count:,} ({count/total_matched*100:.1f}%)")

    print(f"\nDate offset distribution:")
    for offset in range(5):
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
    sample = usace_final[usace_final['VOY_RECID'].notna()][['Vessel', 'Arrival_Port_Name', 'Arrival_Date', 'VOY_RECID', 'Panjiva_Tons', 'Match_Days_Offset', 'Match_Method']].head(5)
    print(sample.to_string(index=False))

print(f"\n" + "="*80)
print("COMPLETE!")
print("="*80)
