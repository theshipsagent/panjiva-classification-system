"""
Marry USACE Entrance and Clearance Records into Port Call Master File
Version: 1.0.0
Date: 2026-01-15

Purpose:
- Merge entrance (arrival) and clearance (departure) into single port call record
- Sequential matching: vessel enters -> clears -> enters again
- Preserve ALL records (entrance-only, clearance-only, both)
- Genesis Event: Ship arriving and departing a port is the atomic unit

Matching Logic:
- Primary: IMO + PORT + sequential date (clearance after arrival)
- Fallback: Vessel Name + PORT + sequential date (if IMO missing)
- Take FIRST clearance after each entrance (closest in time)

Input:
- Entrance: 02_STAGE02_CLASSIFICATION/usace_2023_entrance_with_panjiva_match_v1.3.1.csv
- Clearance: 02_STAGE02_CLASSIFICATION/usace_2023_clearance_with_panjiva_match_v1.0.1.csv

Output:
- Port Call Master: 02_STAGE02_CLASSIFICATION/usace_2023_portcall_master_v1.0.0.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

print("="*80)
print("MARRY ENTRANCE AND CLEARANCE v1.0.0")
print("="*80)
print("\nGenesis Event: Ship Arriving + Departing = Port Call")
print("Preserving ALL vessel movements (matched or unmatched)")

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# File paths
ENTRANCE_FILE = Path(r"G:\My Drive\LLM\project_manifest\02_STAGE02_CLASSIFICATION\usace_2023_entrance_with_panjiva_match_v1.3.1.csv")
CLEARANCE_FILE = Path(r"G:\My Drive\LLM\project_manifest\02_STAGE02_CLASSIFICATION\usace_2023_clearance_with_panjiva_match_v1.0.1.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\02_STAGE02_CLASSIFICATION\usace_2023_portcall_master_v1.0.0.csv")

# Parse USACE dates (mmydd format)
def parse_usace_date(date_val):
    """Convert mmydd integer to timestamp (e.g., 8329 -> 2023-08-29)"""
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

# Load entrance data
print(f"\n1. Loading entrance data...")
entrance = pd.read_csv(ENTRANCE_FILE, low_memory=False)
print(f"   Entrance records: {len(entrance):,}")

# Parse entrance dates (already in YYYY-MM-DD format from v1.3.1)
entrance['Arrival_Date_Parsed'] = pd.to_datetime(entrance['Arrival_Date'], errors='coerce')
print(f"   Dates parsed: {entrance['Arrival_Date_Parsed'].notna().sum():,}")

# Load clearance data
print(f"\n2. Loading clearance data...")
clearance = pd.read_csv(CLEARANCE_FILE, low_memory=False)
print(f"   Clearance records: {len(clearance):,}")

# Parse clearance dates
clearance['Clearance_Date_Parsed'] = clearance['Clearance_Date'].apply(parse_usace_date)
print(f"   Dates parsed: {clearance['Clearance_Date_Parsed'].notna().sum():,}")

# Sort by vessel, port, date for sequential matching
print(f"\n3. Sorting data for sequential matching...")
entrance_sorted = entrance.sort_values(['IMO', 'PORT', 'Arrival_Date_Parsed']).reset_index(drop=True)
clearance_sorted = clearance.sort_values(['IMO', 'PORT', 'Clearance_Date_Parsed']).reset_index(drop=True)

# Track which clearances have been matched (prevent double-matching)
clearance_matched = set()

# Sequential matching
print(f"\n4. Sequential matching: For each entrance, find NEXT clearance...")
matched_records = []
match_stats = {'IMO': 0, 'Vessel_Name': 0, 'No_Match': 0}

for idx, ent_row in entrance_sorted.iterrows():
    if idx % 5000 == 0:
        print(f"   Processing entrance {idx:,}/{len(entrance_sorted):,}")

    vessel_imo = ent_row.get('IMO', '')
    vessel_name = ent_row.get('Vessel', '')
    port = ent_row.get('PORT', '')
    arrival_date = ent_row['Arrival_Date_Parsed']

    if pd.isna(arrival_date):
        # Can't match without arrival date
        merged_row = {f"Entrance_{k}": v for k, v in ent_row.items()}
        merged_row.update({
            'Port_Stay_Days_Decimal': None,
            'Port_Stay_Days_Int': None,
            'Match_Score': None,
            'Match_Type': 'ENTRANCE_ONLY',
            'Match_Method': 'NO_DATE'
        })
        matched_records.append(merged_row)
        match_stats['No_Match'] += 1
        continue

    # Try IMO match first (if IMO exists and is not null)
    clear_match = None
    match_method = None

    if pd.notna(vessel_imo) and str(vessel_imo).strip() != '':
        # Find clearances: same IMO + same PORT + after arrival + not already matched
        candidates = clearance_sorted[
            (clearance_sorted['IMO'] == vessel_imo) &
            (clearance_sorted['PORT'] == port) &
            (clearance_sorted['Clearance_Date_Parsed'] > arrival_date) &
            (~clearance_sorted.index.isin(clearance_matched))
        ]

        if len(candidates) > 0:
            # Take FIRST clearance (closest in time)
            clear_match = candidates.iloc[0]
            clearance_matched.add(clear_match.name)  # Mark as matched
            match_method = 'IMO'
            match_stats['IMO'] += 1

    # Fallback to vessel name if IMO didn't match
    if clear_match is None and pd.notna(vessel_name) and str(vessel_name).strip() != '':
        candidates = clearance_sorted[
            (clearance_sorted['Vessel'] == vessel_name) &
            (clearance_sorted['PORT'] == port) &
            (clearance_sorted['Clearance_Date_Parsed'] > arrival_date) &
            (~clearance_sorted.index.isin(clearance_matched))
        ]

        if len(candidates) > 0:
            clear_match = candidates.iloc[0]
            clearance_matched.add(clear_match.name)
            match_method = 'Vessel_Name'
            match_stats['Vessel_Name'] += 1

    # Build merged row
    if clear_match is not None:
        # Calculate port stay in DECIMAL DAYS
        port_stay_decimal = (clear_match['Clearance_Date_Parsed'] - arrival_date).total_seconds() / (24 * 3600)
        port_stay_int = int(port_stay_decimal)

        # Match confidence based on port stay duration
        if port_stay_decimal <= 15:
            match_score = 1.0  # High confidence
        elif port_stay_decimal <= 45:
            match_score = 0.8  # Medium confidence
        else:
            match_score = 0.5  # Low confidence (extended stay)

        # Merge entrance + clearance columns
        merged_row = {f"Entrance_{k}": v for k, v in ent_row.items()}
        merged_row.update({f"Clearance_{k}": v for k, v in clear_match.items()})
        merged_row.update({
            'Port_Stay_Days_Decimal': port_stay_decimal,
            'Port_Stay_Days_Int': port_stay_int,
            'Match_Score': match_score,
            'Match_Type': 'BOTH',
            'Match_Method': match_method
        })
        matched_records.append(merged_row)
    else:
        # No matching clearance - entrance only
        merged_row = {f"Entrance_{k}": v for k, v in ent_row.items()}
        merged_row.update({
            'Port_Stay_Days_Decimal': None,
            'Port_Stay_Days_Int': None,
            'Match_Score': None,
            'Match_Type': 'ENTRANCE_ONLY',
            'Match_Method': None
        })
        matched_records.append(merged_row)
        match_stats['No_Match'] += 1

print(f"\n5. Adding unmatched clearances (CLEARANCE_ONLY)...")
# Add clearances that were never matched to any entrance
unmatched_clearance_count = 0
for idx, clear_row in clearance_sorted.iterrows():
    if idx not in clearance_matched:
        # This clearance has no entrance match
        merged_row = {f"Clearance_{k}": v for k, v in clear_row.items()}
        merged_row.update({
            'Port_Stay_Days_Decimal': None,
            'Port_Stay_Days_Int': None,
            'Match_Score': None,
            'Match_Type': 'CLEARANCE_ONLY',
            'Match_Method': None
        })
        matched_records.append(merged_row)
        unmatched_clearance_count += 1

print(f"   Unmatched clearances added: {unmatched_clearance_count:,}")

# Convert to DataFrame
print(f"\n6. Creating port call master DataFrame...")
portcall_master = pd.DataFrame(matched_records)
print(f"   Total port call records: {len(portcall_master):,}")

# Add unique port call ID
portcall_master.insert(0, 'PORTCALL_ID', range(1, len(portcall_master) + 1))
portcall_master['PORTCALL_ID'] = 'PC_' + portcall_master['PORTCALL_ID'].astype(str).str.zfill(6)

# Save
portcall_master.to_csv(OUTPUT_FILE, index=False)
print(f"\n7. Saved: {OUTPUT_FILE.name}")
print(f"   Columns: {len(portcall_master.columns)}")

# Summary statistics
print("\n" + "="*80)
print("MATCHING SUMMARY")
print("="*80)

match_type_counts = portcall_master['Match_Type'].value_counts()
print(f"\nTotal port call records: {len(portcall_master):,}")
print(f"\nMatch Type Distribution:")
for match_type, count in match_type_counts.items():
    pct = count / len(portcall_master) * 100
    print(f"  {match_type:<20} {count:>8,} ({pct:>5.1f}%)")

print(f"\nMatching Method (for BOTH):")
both_records = portcall_master[portcall_master['Match_Type'] == 'BOTH']
if len(both_records) > 0:
    for method, count in match_stats.items():
        if method != 'No_Match' and count > 0:
            pct = count / len(both_records) * 100
            print(f"  {method:<20} {count:>8,} ({pct:>5.1f}%)")

# Port stay statistics
if len(both_records) > 0:
    print(f"\nPort Stay Duration (for matched records):")
    print(f"  Average: {both_records['Port_Stay_Days_Decimal'].mean():.1f} days")
    print(f"  Median:  {both_records['Port_Stay_Days_Decimal'].median():.1f} days")
    print(f"  Min:     {both_records['Port_Stay_Days_Decimal'].min():.1f} days")
    print(f"  Max:     {both_records['Port_Stay_Days_Decimal'].max():.1f} days")

    # Distribution by duration
    print(f"\n  Duration Distribution:")
    print(f"    ≤15 days:  {(both_records['Port_Stay_Days_Decimal'] <= 15).sum():,} ({(both_records['Port_Stay_Days_Decimal'] <= 15).sum()/len(both_records)*100:.1f}%)")
    print(f"    16-45 days: {((both_records['Port_Stay_Days_Decimal'] > 15) & (both_records['Port_Stay_Days_Decimal'] <= 45)).sum():,} ({((both_records['Port_Stay_Days_Decimal'] > 15) & (both_records['Port_Stay_Days_Decimal'] <= 45)).sum()/len(both_records)*100:.1f}%)")
    print(f"    >45 days:  {(both_records['Port_Stay_Days_Decimal'] > 45).sum():,} ({(both_records['Port_Stay_Days_Decimal'] > 45).sum()/len(both_records)*100:.1f}%)")

# Match score distribution
if len(both_records) > 0:
    print(f"\n  Match Score Distribution:")
    score_counts = both_records['Match_Score'].value_counts().sort_index(ascending=False)
    for score, count in score_counts.items():
        pct = count / len(both_records) * 100
        print(f"    {score:.1f}: {count:,} ({pct:.1f}%)")

# Sample records
print(f"\n" + "="*80)
print("SAMPLE RECORDS (First 3 of each type)")
print("="*80)

for match_type in ['BOTH', 'ENTRANCE_ONLY', 'CLEARANCE_ONLY']:
    sample = portcall_master[portcall_master['Match_Type'] == match_type].head(3)
    if len(sample) > 0:
        print(f"\n{match_type}:")
        if match_type == 'BOTH':
            cols = ['PORTCALL_ID', 'Entrance_Vessel', 'Entrance_PORT', 'Entrance_Arrival_Date',
                    'Clearance_Clearance_Date', 'Port_Stay_Days_Decimal', 'Match_Score']
        elif match_type == 'ENTRANCE_ONLY':
            cols = ['PORTCALL_ID', 'Entrance_Vessel', 'Entrance_PORT', 'Entrance_Arrival_Date']
        else:  # CLEARANCE_ONLY
            cols = ['PORTCALL_ID', 'Clearance_Vessel', 'Clearance_PORT', 'Clearance_Clearance_Date']

        # Filter to columns that exist
        cols = [c for c in cols if c in sample.columns]
        try:
            print(sample[cols].to_string(index=False))
        except UnicodeEncodeError:
            print("   [Sample display skipped due to unicode characters]")

print(f"\n" + "="*80)
print("COMPLETE!")
print("="*80)
print(f"\nGenesis Event Established: {len(portcall_master):,} port calls")
print(f"Expected range: ~{len(entrance):,} to ~{len(entrance) + len(clearance):,}")
print(f"Output: {OUTPUT_FILE.name}")
