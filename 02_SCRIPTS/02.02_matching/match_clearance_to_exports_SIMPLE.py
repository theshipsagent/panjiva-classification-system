"""
SIMPLIFIED MATCHING: USACE Clearance + Panjiva Exports
Version: 2.0.0 - SIMPLIFIED APPROACH
Date: 2026-01-16

Purpose:
- Match USACE clearance records to Panjiva export manifests
- Add ONLY 2 columns to USACE clearance:
  1. Has_Export_Manifest (TRUE/FALSE)
  2. Export_VOY_RECID (unique voyage ID if matched, NULL if not)
- NO cargo data copied over
- User can join later if they want cargo details

Matching Logic:
- Primary: IMO + Port + Date (±3 days)
- Fallback: Vessel Name + Port + Date (±3 days)
- VOY_RECID created from: hash(Vessel + Date + Port)

Input:
- USACE Clearance: 00_DATA/00.02_PREPROCESSED/usace_2023_clearance_AUTHORITATIVE_v1.0.0.csv
- Panjiva Exports: 00_DATA/00.02_PREPROCESSED/panjiva_exports_2023_AUTHORITATIVE_v1.0.0.csv

Output:
- USACE Clearance with flags: 00_DATA/00.03_MATCHED/usace_2023_clearance_with_export_flags_v2.0.0.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import hashlib

print("="*80)
print("SIMPLIFIED CLEARANCE -> EXPORT MATCHING v2.0.0")
print("="*80)
print("\nNew approach: Add foreign keys only, NO data duplication")

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# File paths
BASE = Path(r"G:\My Drive\LLM\project_manifest")
CLEARANCE_FILE = BASE / "00_DATA" / "00.02_PREPROCESSED" / "usace_2023_clearance_AUTHORITATIVE_v1.0.0.csv"
EXPORTS_FILE = BASE / "00_DATA" / "00.02_PREPROCESSED" / "panjiva_exports_2023_AUTHORITATIVE_v1.0.0.csv"
OUTPUT_FILE = BASE / "00_DATA" / "00.03_MATCHED" / f"usace_2023_clearance_with_export_flags_v2.0.0_{timestamp}.csv"

# Create VOY_RECID from vessel + date + port
def create_voy_recid(vessel, date, port):
    """Create unique voyage identifier"""
    key = f"{vessel}|{date}|{port}".upper()
    return hashlib.md5(key.encode()).hexdigest()[:16]

# Parse USACE date (mmydd format)
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

# Load data
print(f"\n1. Loading USACE clearance data...")
clearance = pd.read_csv(CLEARANCE_FILE, low_memory=False)
print(f"   Clearance records: {len(clearance):,}")
print(f"   Columns: {len(clearance.columns)}")

print(f"\n2. Loading Panjiva exports data...")
exports = pd.read_csv(EXPORTS_FILE, low_memory=False)
print(f"   Export records: {len(exports):,}")
print(f"   Columns: {len(exports.columns)}")

# Create VOY_RECID for each export manifest (use Shipment Date and Port of Lading)
print(f"\n3. Creating VOY_RECID for export manifests...")
exports['VOY_RECID'] = exports.apply(
    lambda row: create_voy_recid(
        str(row.get('Vessel', '')),
        str(row.get('Shipment Date', '')),
        str(row.get('Port of Lading', ''))
    ),
    axis=1
)

# Get unique manifests (NOTE: exports has NO IMO column)
unique_manifests = exports[['VOY_RECID', 'Vessel', 'Shipment Date', 'Port of Lading']].drop_duplicates('VOY_RECID')
print(f"   Total export cargo records: {len(exports):,}")
print(f"   Unique manifests: {len(unique_manifests):,}")
print(f"   Avg items per manifest: {len(exports)/len(unique_manifests):.1f}")

# Parse dates
print(f"\n4. Parsing dates...")
clearance['Clearance_Date_Parsed'] = pd.to_datetime(clearance['Clearance_Date'], errors='coerce')
unique_manifests['Shipment_Date_Parsed'] = pd.to_datetime(unique_manifests['Shipment Date'], errors='coerce')

print(f"   Clearance dates parsed: {clearance['Clearance_Date_Parsed'].notna().sum():,}")
print(f"   Export dates parsed: {unique_manifests['Shipment_Date_Parsed'].notna().sum():,}")

# Initialize match columns
clearance['Has_Export_Manifest'] = False
clearance['Export_VOY_RECID'] = None

# Matching (NOTE: exports has NO IMO - match by vessel name + date only)
print(f"\n5. Matching clearance -> exports (Vessel Name + Date ±3 days)...")
match_stats = {'Name_Match': 0, 'No_Match': 0}

for idx, clr_row in clearance.iterrows():
    if idx % 5000 == 0:
        print(f"   Processing {idx:,}/{len(clearance):,}")

    clr_vessel = str(clr_row.get('Vessel', '')).strip().upper()
    clr_date = clr_row['Clearance_Date_Parsed']

    if pd.isna(clr_date):
        match_stats['No_Match'] += 1
        continue

    # Match by vessel name + date (exports has no IMO)
    candidates = unique_manifests[
        (unique_manifests['Vessel'].str.upper().str.strip() == clr_vessel) &
        (unique_manifests['Shipment_Date_Parsed'].notna()) &
        (abs((unique_manifests['Shipment_Date_Parsed'] - clr_date).dt.days) <= 3)
    ]

    if len(candidates) > 0:
        best = candidates.iloc[0]
        clearance.at[idx, 'Has_Export_Manifest'] = True
        clearance.at[idx, 'Export_VOY_RECID'] = best['VOY_RECID']
        match_stats['Name_Match'] += 1
    else:
        match_stats['No_Match'] += 1

# Results
print(f"\n6. Matching results:")
print(f"   Name matches: {match_stats['Name_Match']:,}")
print(f"   No match: {match_stats['No_Match']:,}")
print(f"   Match rate: {match_stats['Name_Match']/len(clearance)*100:.1f}%")

# Save
print(f"\n7. Saving matched clearance file...")
print(f"   Output: {OUTPUT_FILE}")
clearance.to_csv(OUTPUT_FILE, index=False)

print(f"\n   Original columns: {len(clearance.columns)-2}")
print(f"   New columns added: 2 (Has_Export_Manifest, Export_VOY_RECID)")
print(f"   Total columns: {len(clearance.columns)}")
print(f"   File size: {OUTPUT_FILE.stat().st_size / 1024 / 1024:.1f} MB")

print(f"\n{'='*80}")
print("SIMPLIFIED MATCHING COMPLETE")
print("="*80)
print(f"\nNext step: Marry entrance + clearance -> port calls")
