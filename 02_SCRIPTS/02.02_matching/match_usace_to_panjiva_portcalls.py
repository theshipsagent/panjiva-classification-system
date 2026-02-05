"""
Match USACE Entrance Data to Panjiva Import Port Calls
Version: 1.2.0
Date: 2026-01-15

CRITICAL LOGIC:
- Panjiva import manifests = USACE entrance records (same vessel arrival event)
- Should achieve ~100% match rate for import vessels
- Use IMO as primary key, vessel name as fallback

Matching Strategy:
1. IMO + Port + Date (+/- tolerance)
2. Normalized Vessel Name + Port + Date (if IMO missing/mismatch)

Date Tolerance:
- Pass 1: +/- 2 days
- Pass 2: +/- 4 days (for remaining unmatched)
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path
from datetime import datetime, timedelta

# File paths
USACE_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_inbound_entrance_transformed_v2.1.0.csv")
PANJIVA_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01.01_annual_files\panjiva_imports_2023_PORTCALL_v20260115_1530.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_entrance_with_panjiva_match_v1.2.0.csv")

print("="*80)
print("USACE-PANJIVA PORT CALL MATCHING v1.2.0")
print("="*80)

# Load data
print(f"\n1. Loading USACE entrance data...")
usace = pd.read_csv(USACE_FILE, low_memory=False)
print(f"   Records: {len(usace):,}")

# Fix USACE date parsing (mmydd format: month, year digit, day)
print(f"\n2. Fixing USACE date format...")
def parse_usace_date(date_val):
    """Convert mmydd integer to proper date (e.g., 8329 -> 2023-08-29)
    Format: mmydd where mm=month, y=last digit of year, dd=day
    """
    if pd.isna(date_val):
        return None
    try:
        date_str = str(int(date_val)).zfill(5)  # Ensure 5 digits (mmydd)
        month = int(date_str[:2])
        year_digit = int(date_str[2])
        day = int(date_str[3:])

        # Year digit 3 = 2023, 2 = 2022, etc.
        # Assume 2020s decade
        year = 2020 + year_digit

        return pd.Timestamp(year=year, month=month, day=day)
    except Exception as e:
        return None

usace['Arrival_Date'] = usace['Arrival_Date'].apply(parse_usace_date)
print(f"   Sample dates: {usace['Arrival_Date'].head().tolist()}")

print(f"\n3. Loading Panjiva port call data...")
panjiva = pd.read_csv(PANJIVA_FILE, low_memory=False)
panjiva['Arrival Date'] = pd.to_datetime(panjiva['Arrival Date'], errors='coerce')
print(f"   Records: {len(panjiva):,}")
print(f"   Unique port calls (VOY_RECID): {panjiva['VOY_RECID'].nunique():,}")

# Aggregate Panjiva data by VOY_RECID
print(f"\n4. Aggregating Panjiva data by VOY_RECID...")
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
print(f"   Aggregated to {len(panjiva_agg):,} unique port calls")

# Normalize functions
def normalize_vessel_name(name):
    """Remove punctuation, special chars, lowercase for fuzzy matching"""
    if pd.isna(name) or name == '':
        return ''
    # Remove all non-alphanumeric, convert to lowercase
    normalized = re.sub(r'[^a-zA-Z0-9\s]', '', str(name))
    normalized = ' '.join(normalized.lower().split())
    return normalized

def normalize_port_name(name):
    """Extract city and state for fuzzy matching"""
    if pd.isna(name) or name == '':
        return ''
    name = str(name).upper()

    # Extract city - usually first part before comma
    parts = name.split(',')
    if len(parts) > 0:
        city = parts[0].strip()
        # Remove common prefixes
        city = city.replace('PORT OF ', '').replace('PORT ', '').replace('THE ', '')

        # Extract state abbreviation if present
        state = ''
        for part in parts:
            # Look for 2-letter state codes
            part_clean = part.strip()
            if len(part_clean) == 2 and part_clean.isalpha():
                state = part_clean
                break

        return f"{city}|{state}".upper()

    return name.upper()

def normalize_imo(imo_val):
    """Normalize IMO number"""
    if pd.isna(imo_val):
        return ''
    try:
        # Remove any non-numeric characters
        imo_clean = re.sub(r'[^0-9]', '', str(imo_val))
        if imo_clean:
            return imo_clean
    except:
        pass
    return ''

print(f"\n5. Normalizing matching keys...")
# USACE normalization
usace['Vessel_Norm'] = usace['Vessel'].apply(normalize_vessel_name)
usace['Port_Norm'] = usace['Arrival_Port_Name'].apply(normalize_port_name)
usace['IMO_Norm'] = usace['IMO'].apply(normalize_imo)

# Panjiva normalization
panjiva_agg['Vessel_Norm'] = panjiva_agg['Vessel'].apply(normalize_vessel_name)
panjiva_agg['Port_Norm'] = panjiva_agg['Port'].apply(normalize_port_name)
panjiva_agg['IMO_Norm'] = panjiva_agg['IMO'].apply(normalize_imo)

# Show sample normalization
print(f"\n   Sample USACE normalization:")
sample = usace[['Vessel', 'Vessel_Norm', 'Arrival_Port_Name', 'Port_Norm', 'IMO', 'IMO_Norm']].head(3)
print(sample.to_string(index=False))

print(f"\n   Sample Panjiva normalization:")
sample = panjiva_agg[['Vessel', 'Vessel_Norm', 'Port', 'Port_Norm', 'IMO', 'IMO_Norm']].head(3)
print(sample.to_string(index=False))

# Matching function
def match_with_tolerance(usace_df, panjiva_df, unmatched_mask, days_tolerance, pass_number):
    """
    Match USACE to Panjiva with date tolerance
    Strategy: IMO + Port + Date (primary), then Vessel Name + Port + Date (fallback)
    """
    matches_found = 0
    unmatched_usace = usace_df[unmatched_mask].copy()

    print(f"\n   Pass {pass_number}: Matching {len(unmatched_usace):,} records with +/-{days_tolerance} day tolerance...")

    for idx, usace_row in unmatched_usace.iterrows():
        imo = usace_row['IMO_Norm']
        vessel = usace_row['Vessel_Norm']
        port = usace_row['Port_Norm']
        date = usace_row['Arrival_Date']

        if pd.isna(date) or port == '':
            continue

        # Date range
        date_min = date - timedelta(days=days_tolerance)
        date_max = date + timedelta(days=days_tolerance)

        # Strategy 1: Match by IMO (if available)
        if imo != '':
            matches = panjiva_df[
                (panjiva_df['IMO_Norm'] == imo) &
                (panjiva_df['Port_Norm'] == port) &
                (panjiva_df['Arrival_Date'] >= date_min) &
                (panjiva_df['Arrival_Date'] <= date_max)
            ].copy()

            if len(matches) > 0:
                # Take closest date match
                matches['date_diff'] = (matches['Arrival_Date'] - date).abs()
                best_match = matches.loc[matches['date_diff'].idxmin()]

                usace_df.at[idx, 'VOY_RECID'] = best_match['VOY_RECID']
                usace_df.at[idx, 'Panjiva_Carrier'] = best_match['Carrier']
                usace_df.at[idx, 'Panjiva_Group'] = best_match['Group_Concat']
                usace_df.at[idx, 'Panjiva_Commodity'] = best_match['Commodity_Concat']
                usace_df.at[idx, 'Panjiva_Tons'] = best_match['Total_Tons']
                usace_df.at[idx, 'Match_Days_Offset'] = best_match['date_diff'].days
                usace_df.at[idx, 'Match_Pass'] = pass_number
                usace_df.at[idx, 'Match_Method'] = 'IMO'

                matches_found += 1
                continue

        # Strategy 2: Match by Vessel Name (fallback if IMO missing or no IMO match)
        if vessel != '':
            matches = panjiva_df[
                (panjiva_df['Vessel_Norm'] == vessel) &
                (panjiva_df['Port_Norm'] == port) &
                (panjiva_df['Arrival_Date'] >= date_min) &
                (panjiva_df['Arrival_Date'] <= date_max)
            ].copy()

            if len(matches) > 0:
                # Take closest date match
                matches['date_diff'] = (matches['Arrival_Date'] - date).abs()
                best_match = matches.loc[matches['date_diff'].idxmin()]

                usace_df.at[idx, 'VOY_RECID'] = best_match['VOY_RECID']
                usace_df.at[idx, 'Panjiva_Carrier'] = best_match['Carrier']
                usace_df.at[idx, 'Panjiva_Group'] = best_match['Group_Concat']
                usace_df.at[idx, 'Panjiva_Commodity'] = best_match['Commodity_Concat']
                usace_df.at[idx, 'Panjiva_Tons'] = best_match['Total_Tons']
                usace_df.at[idx, 'Match_Days_Offset'] = best_match['date_diff'].days
                usace_df.at[idx, 'Match_Pass'] = pass_number
                usace_df.at[idx, 'Match_Method'] = 'Vessel_Name'

                matches_found += 1

    print(f"      [OK] Found {matches_found:,} new matches")
    return matches_found

# Initialize match columns
usace['VOY_RECID'] = np.nan
usace['Panjiva_Carrier'] = np.nan
usace['Panjiva_Group'] = np.nan
usace['Panjiva_Commodity'] = np.nan
usace['Panjiva_Tons'] = np.nan
usace['Match_Days_Offset'] = np.nan
usace['Match_Pass'] = np.nan
usace['Match_Method'] = np.nan

# Pass 1: +/- 2 days
print(f"\n6. MATCHING PASS 1 (+/- 2 days)")
print(f"   " + "-"*76)
unmatched_mask = usace['VOY_RECID'].isna()
matches_pass1 = match_with_tolerance(usace, panjiva_agg, unmatched_mask, 2, 1)

# Pass 2: +/- 4 days for remaining
print(f"\n7. MATCHING PASS 2 (+/- 4 days)")
print(f"   " + "-"*76)
unmatched_mask = usace['VOY_RECID'].isna()
matches_pass2 = match_with_tolerance(usace, panjiva_agg, unmatched_mask, 4, 2)

# Drop temporary columns
usace.drop(['Vessel_Norm', 'Port_Norm', 'IMO_Norm'], axis=1, inplace=True)

# Save results
print(f"\n8. Saving results...")
usace.to_csv(OUTPUT_FILE, index=False)
print(f"   Output: {OUTPUT_FILE.name}")

# Summary statistics
print("\n" + "="*80)
print("MATCHING SUMMARY")
print("="*80)

total_usace = len(usace)
total_matched = usace['VOY_RECID'].notna().sum()
total_unmatched = usace['VOY_RECID'].isna().sum()

print(f"\nTotal USACE entrance records: {total_usace:,}")
print(f"\nMatching Results:")
print(f"  [OK] Pass 1 (+/-2 days): {matches_pass1:,} matches ({matches_pass1/total_usace*100:.1f}%)")
print(f"  [OK] Pass 2 (+/-4 days): {matches_pass2:,} matches ({matches_pass2/total_usace*100:.1f}%)")
print(f"  [OK] Total matched:      {total_matched:,} ({total_matched/total_usace*100:.1f}%)")
print(f"  [--] Unmatched:          {total_unmatched:,} ({total_unmatched/total_usace*100:.1f}%)")

# Match method breakdown
matched_records = usace[usace['VOY_RECID'].notna()]
if len(matched_records) > 0:
    print(f"\nMatch method breakdown:")
    method_counts = matched_records['Match_Method'].value_counts()
    for method, count in method_counts.items():
        print(f"  {method}: {count:,} ({count/len(matched_records)*100:.1f}%)")

    print(f"\nDate offset distribution:")
    for offset in range(5):
        count = (matched_records['Match_Days_Offset'] == offset).sum()
        if count > 0:
            print(f"  {offset} days: {count:,} ({count/len(matched_records)*100:.1f}%)")

# Tonnage statistics
matched_with_tons = matched_records[matched_records['Panjiva_Tons'].notna()]
if len(matched_with_tons) > 0:
    print(f"\nTonnage statistics:")
    print(f"  Total Panjiva tons: {matched_with_tons['Panjiva_Tons'].sum():,.0f}")
    print(f"  Average per port call: {matched_with_tons['Panjiva_Tons'].mean():,.0f}")

# Sample output
print(f"\n" + "="*80)
print("SAMPLE MATCHED RECORDS (First 5)")
print("="*80)
display_cols = ['Vessel', 'Arrival_Port_Name', 'Arrival_Date', 'VOY_RECID', 'Panjiva_Tons', 'Match_Days_Offset', 'Match_Method']
sample = usace[usace['VOY_RECID'].notna()][display_cols].head(5)
if len(sample) > 0:
    print(sample.to_string(index=False))
else:
    print("(No matches found)")

print(f"\n" + "="*80)
print("COMPLETE!")
print("="*80)
