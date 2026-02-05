"""
Match FGIS Grain Exports to Port Call Master - Clearance Records
Version: 1.0.0
Date: 2026-01-15

Purpose:
- Match FGIS grain export records to clearance records in Port Call Master
- Add grain export flags and data to Port Call Master
- Create RECID cross-reference for linking

Logic:
- Grain loading REQUIRES vessel clearance (1:1 relationship expected)
- Match on: Vessel name + Port + Date proximity
- Add to Port Call Master: Grain_Export (TRUE/FALSE), FGIS_RECID, Grain_Type, Grain_MT
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from difflib import SequenceMatcher

print("="*80)
print("FGIS GRAIN EXPORT -> PORT CALL MASTER MATCHING v1.0.0")
print("="*80)

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# File paths
PORTCALL_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_portcall_master_v1.1.0.csv")
FGIS_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\fgis_2023_grain_exports_v1.0.0.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_portcall_master_v1.2.0.csv")
MATCH_REPORT = Path(r"G:\My Drive\LLM\project_manifest\03_DOCUMENTATION/03.04_summaries\fgis_portcall_match_report_v1.0.0.csv")

# FGIS port to USACE port mapping (based on actual Clearance_Clearance_Port_Name values)
FGIS_TO_USACE_PORT_MAP = {
    'MISSISSIPPI R.': [
        'Port of New Orleans, LA',
        'Port of South Louisiana, LA',
        'Port of Greater Baton Rouge, LA',
        'Greater Lafourche Port Commission, LA',
        'Lake Charles Harbor and Terminal District, LA',
        'Port of St. Bernard, LA'
    ],
    'COLUMBIA R.': [
        'Port of Portland, OR',
        'Port of Longview, WA',
        'Port of Kalama, WA',
        'Port of Vancouver, WA',
        'Port of Woodland, WA'
    ],
    'S. TEXAS': [
        'Corpus Christi, TX',
        'Port of Brownsville, TX',
        'Port Isabel, TX'
    ],
    'N. TEXAS': [
        'Port of Houston Authority of Harris County, TX',
        'Galveston, TX',
        'Port Freeport, TX',
        'Beaumont, TX',
        'Texas City, TX',
        'Port of Orange, TX'
    ],
    'PUGET SOUND': [
        'Port of Seattle, WA',
        'Port of Tacoma, WA',
        'Port of Olympia, WA',
        'Port of Everett, WA'
    ],
    'S. ATLANTIC': [
        'Port of Charleston, SC',
        'Port of Savannah, GA',
        'Wilmington, NC',
        'Port of Virginia, VA'
    ],
    'DULUTH-SUP': [
        'Duluth-Superior, MN & WI'
    ],
    'TOLEDO': [
        'Toledo, OH',
        'Port of Toledo, OH'
    ],
    'EAST GULF': [
        'Mobile, AL',
        'Pensacola, FL',
        'Panama City, FL'
    ],
    'SEAWAY': [
        'St. Lawrence Seaway'
    ]
}

def clean_vessel_name(name):
    """Standardize vessel name for matching"""
    if pd.isna(name):
        return ""
    name = str(name).upper().strip()
    # Remove common prefixes
    for prefix in ['M/V ', 'MV ', 'M.V. ', 'S/S ', 'SS ']:
        if name.startswith(prefix):
            name = name[len(prefix):]
    return name.strip()

def vessel_name_similarity(name1, name2):
    """Calculate similarity between two vessel names (0-1)"""
    name1 = clean_vessel_name(name1)
    name2 = clean_vessel_name(name2)
    if not name1 or not name2:
        return 0.0
    return SequenceMatcher(None, name1, name2).ratio()

def map_fgis_port_to_usace(fgis_port):
    """Map FGIS port to possible USACE ports"""
    if pd.isna(fgis_port):
        return []
    fgis_port = str(fgis_port).strip()
    return FGIS_TO_USACE_PORT_MAP.get(fgis_port, [])

# Load data
print("\n1. Loading data...")
portcall = pd.read_csv(PORTCALL_FILE, low_memory=False)
fgis = pd.read_csv(FGIS_FILE, low_memory=False)
print(f"   Port Call Master records: {len(portcall):,}")
print(f"   FGIS grain export records: {len(fgis):,}")

# Create FGIS_RECID
print("\n2. Creating FGIS_RECID...")
fgis['FGIS_RECID'] = fgis['Serial No.'].astype(str)
print(f"   FGIS_RECID created for {len(fgis):,} records")

# Parse USACE dates (mmydd format: e.g., 8329 -> 2023-08-29)
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

# Parse dates
print("\n3. Parsing dates...")
portcall['Clearance_Date_Parsed'] = portcall['Clearance_Clearance_Date'].apply(parse_usace_date)
fgis['Cert_Date_Parsed'] = pd.to_datetime(fgis['Cert Date'], format='%Y-%b-%d', errors='coerce')

# Clean vessel names
print("\n4. Standardizing vessel names...")
portcall['Clearance_Vessel_Clean'] = portcall['Clearance_Vessel'].apply(clean_vessel_name)
fgis['Vessel_Clean'] = fgis['Vessel'].apply(clean_vessel_name)

# Filter for clearance records only (grain must have clearance)
print("\n5. Filtering for clearance records...")
clearance_records = portcall[portcall['Clearance_Vessel'].notna()].copy()
print(f"   Records with clearance data: {len(clearance_records):,}")

# Initialize grain export columns in portcall master
print("\n6. Initializing grain export columns...")
portcall['Grain_Export'] = False
portcall['FGIS_RECID'] = None
portcall['Grain_Type'] = None
portcall['Grain_Detail'] = None
portcall['Grain_MT'] = None
portcall['Grain_Pounds'] = None
portcall['Match_Quality'] = None

# Matching logic
print("\n7. Matching FGIS records to clearance records...")
print("   Matching criteria:")
print("   - Vessel name similarity > 0.85")
print("   - Port match (FGIS port -> USACE port mapping)")
print("   - Date proximity: Cert Date within +/- 7 days of Clearance Date")

matches = []
unmatched_fgis = []

for idx, fgis_row in fgis.iterrows():
    fgis_vessel = fgis_row['Vessel_Clean']
    fgis_port = fgis_row['Port_Consolidated']
    fgis_date = fgis_row['Cert_Date_Parsed']

    if pd.isna(fgis_date):
        unmatched_fgis.append({
            'FGIS_RECID': fgis_row['FGIS_RECID'],
            'Vessel': fgis_row['Vessel'],
            'Port': fgis_port,
            'Cert_Date': fgis_row['Cert Date'],
            'Reason': 'Missing cert date'
        })
        continue

    # Get possible USACE ports
    usace_ports = map_fgis_port_to_usace(fgis_port)

    if not usace_ports:
        unmatched_fgis.append({
            'FGIS_RECID': fgis_row['FGIS_RECID'],
            'Vessel': fgis_row['Vessel'],
            'Port': fgis_port,
            'Cert_Date': fgis_row['Cert Date'],
            'Reason': f'No USACE port mapping for {fgis_port}'
        })
        continue

    # Find candidate clearance records
    candidates = clearance_records[
        (clearance_records['Clearance_Date_Parsed'].notna()) &
        (clearance_records['Clearance_Date_Parsed'] >= fgis_date - timedelta(days=7)) &
        (clearance_records['Clearance_Date_Parsed'] <= fgis_date + timedelta(days=7))
    ].copy()

    # Filter by port (using Clearance_Clearance_Port_Name)
    candidates = candidates[candidates['Clearance_Clearance_Port_Name'].isin(usace_ports)]

    if len(candidates) == 0:
        unmatched_fgis.append({
            'FGIS_RECID': fgis_row['FGIS_RECID'],
            'Vessel': fgis_row['Vessel'],
            'Port': fgis_port,
            'Cert_Date': fgis_row['Cert Date'],
            'Reason': f'No clearance records in date window for ports {usace_ports}'
        })
        continue

    # Calculate vessel name similarity for all candidates
    candidates['Vessel_Similarity'] = candidates['Clearance_Vessel_Clean'].apply(
        lambda x: vessel_name_similarity(x, fgis_vessel)
    )

    # Filter for high similarity matches
    high_similarity = candidates[candidates['Vessel_Similarity'] >= 0.85]

    if len(high_similarity) == 0:
        unmatched_fgis.append({
            'FGIS_RECID': fgis_row['FGIS_RECID'],
            'Vessel': fgis_row['Vessel'],
            'Port': fgis_port,
            'Cert_Date': fgis_row['Cert Date'],
            'Reason': f'No vessel name match (best similarity: {candidates["Vessel_Similarity"].max():.2f})'
        })
        continue

    # Take best match (highest similarity, closest date)
    high_similarity['Date_Diff'] = abs((high_similarity['Clearance_Date_Parsed'] - fgis_date).dt.days)
    best_match = high_similarity.sort_values(['Vessel_Similarity', 'Date_Diff'], ascending=[False, True]).iloc[0]

    # Record match
    match_quality = f"Similarity_{best_match['Vessel_Similarity']:.2f}_DateDiff_{best_match['Date_Diff']}d"

    matches.append({
        'FGIS_RECID': fgis_row['FGIS_RECID'],
        'FGIS_Vessel': fgis_row['Vessel'],
        'FGIS_Port': fgis_port,
        'FGIS_Cert_Date': fgis_row['Cert Date'],
        'Portcall_Index': best_match.name,
        'Portcall_Vessel': best_match['Clearance_Vessel'],
        'Portcall_Port': best_match['Clearance_Clearance_Port_Name'],
        'Portcall_Clearance_Date': best_match['Clearance_Clearance_Date'],
        'Vessel_Similarity': best_match['Vessel_Similarity'],
        'Date_Diff_Days': best_match['Date_Diff'],
        'Match_Quality': match_quality,
        'Grain_Type': fgis_row['Cargo'],
        'Grain_Detail': fgis_row['Cargo_Detail'],
        'Grain_MT': fgis_row['Metric Ton'],
        'Grain_Pounds': fgis_row['Pounds']
    })

print(f"\n   Matches found: {len(matches):,}")
print(f"   Unmatched FGIS records: {len(unmatched_fgis):,}")

# Update Port Call Master with grain export data
print("\n8. Updating Port Call Master with grain export data...")
for match in matches:
    pc_idx = match['Portcall_Index']
    portcall.loc[pc_idx, 'Grain_Export'] = True
    portcall.loc[pc_idx, 'FGIS_RECID'] = match['FGIS_RECID']
    portcall.loc[pc_idx, 'Grain_Type'] = match['Grain_Type']
    portcall.loc[pc_idx, 'Grain_Detail'] = match['Grain_Detail']
    portcall.loc[pc_idx, 'Grain_MT'] = match['Grain_MT']
    portcall.loc[pc_idx, 'Grain_Pounds'] = match['Grain_Pounds']
    portcall.loc[pc_idx, 'Match_Quality'] = match['Match_Quality']

# Save updated Port Call Master
print("\n9. Saving updated Port Call Master...")
portcall.to_csv(OUTPUT_FILE, index=False)
print(f"   Saved: {OUTPUT_FILE.name}")
file_size = OUTPUT_FILE.stat().st_size / (1024 * 1024)
print(f"   Size: {file_size:.1f} MB")

# Save match report
print("\n10. Saving match report...")
match_df = pd.DataFrame(matches)
if len(match_df) > 0:
    match_df.to_csv(MATCH_REPORT, index=False)
    print(f"   Saved: {MATCH_REPORT.name}")

# Statistics
print("\n" + "="*80)
print("MATCH STATISTICS")
print("="*80)

print(f"\nFGIS Grain Export Records: {len(fgis):,}")
print(f"  Matched to clearance: {len(matches):,} ({len(matches)/len(fgis)*100:.1f}%)")
print(f"  Unmatched: {len(unmatched_fgis):,} ({len(unmatched_fgis)/len(fgis)*100:.1f}%)")

print(f"\nPort Call Master Records: {len(portcall):,}")
grain_export_count = portcall['Grain_Export'].sum()
print(f"  With grain exports: {grain_export_count:,} ({grain_export_count/len(portcall)*100:.1f}%)")
print(f"  Without grain exports: {len(portcall) - grain_export_count:,}")

if len(matches) > 0:
    print(f"\nMatch Quality Distribution:")
    match_df = pd.DataFrame(matches)
    print(f"  Avg vessel similarity: {match_df['Vessel_Similarity'].mean():.3f}")
    print(f"  Avg date difference: {match_df['Date_Diff_Days'].mean():.1f} days")

    print(f"\n  Vessel similarity:")
    print(f"    Perfect match (1.00): {(match_df['Vessel_Similarity'] == 1.0).sum():,}")
    print(f"    High match (0.95-0.99): {((match_df['Vessel_Similarity'] >= 0.95) & (match_df['Vessel_Similarity'] < 1.0)).sum():,}")
    print(f"    Good match (0.85-0.94): {((match_df['Vessel_Similarity'] >= 0.85) & (match_df['Vessel_Similarity'] < 0.95)).sum():,}")

    print(f"\n  Date difference:")
    print(f"    Same day (0 days): {(match_df['Date_Diff_Days'] == 0).sum():,}")
    print(f"    Within 1-3 days: {((match_df['Date_Diff_Days'] >= 1) & (match_df['Date_Diff_Days'] <= 3)).sum():,}")
    print(f"    Within 4-7 days: {((match_df['Date_Diff_Days'] >= 4) & (match_df['Date_Diff_Days'] <= 7)).sum():,}")

    print(f"\nGrain Types Matched:")
    grain_types = match_df['Grain_Type'].value_counts()
    for grain, count in grain_types.items():
        print(f"  {grain:<15} {count:>5,} shipments")

if len(unmatched_fgis) > 0:
    print(f"\nUnmatched Reasons:")
    unmatched_df = pd.DataFrame(unmatched_fgis)
    reason_counts = unmatched_df['Reason'].value_counts()
    for reason, count in reason_counts.items():
        print(f"  {reason}: {count:,}")

    # Save unmatched records for review
    unmatched_file = Path(r"G:\My Drive\LLM\project_manifest\03_DOCUMENTATION/03.04_summaries\fgis_unmatched_records_v1.0.0.csv")
    unmatched_df.to_csv(unmatched_file, index=False)
    print(f"\n   Unmatched records saved: {unmatched_file.name}")

print("\n" + "="*80)
print("COMPLETE!")
print("="*80)
print(f"\nOutput: {OUTPUT_FILE}")
print(f"Match Report: {MATCH_REPORT}")
print(f"\nGrain export flags added to Port Call Master")
print(f"Cross-reference via FGIS_RECID column")
