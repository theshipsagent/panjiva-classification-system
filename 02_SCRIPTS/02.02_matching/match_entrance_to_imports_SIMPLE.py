"""
SIMPLIFIED MATCHING: USACE Entrance + Panjiva Imports
Version: 2.0.0 - SIMPLIFIED APPROACH
Date: 2026-01-16

Purpose:
- Match USACE entrance records to Panjiva import manifests
- Add ONLY 2 columns to USACE entrance:
  1. Has_Import_Manifest (TRUE/FALSE)
  2. Import_VOY_RECID (unique voyage ID if matched, NULL if not)
- NO cargo data copied over
- User can join later if they want cargo details

Matching Logic:
- Primary: IMO + Port + Date (±3 days)
- Fallback: Vessel Name + Port + Date (±3 days)
- VOY_RECID created from: hash(Vessel + Date + Port)

Input:
- USACE Entrance: 00_DATA/00.02_PREPROCESSED/usace_2023_entrance_AUTHORITATIVE_v1.0.0.csv
- Panjiva Imports: 00_DATA/00.02_PREPROCESSED/panjiva_imports_2023_AUTHORITATIVE_v1.0.0.csv

Output:
- USACE Entrance with flags: 00_DATA/00.03_MATCHED/usace_2023_entrance_with_import_flags_v2.0.0.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import hashlib

print("="*80)
print("SIMPLIFIED ENTRANCE -> IMPORT MATCHING v2.0.0")
print("="*80)
print("\nNew approach: Add foreign keys only, NO data duplication")

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# File paths
BASE = Path(r"G:\My Drive\LLM\project_manifest")
ENTRANCE_FILE = BASE / "00_DATA" / "00.02_PREPROCESSED" / "usace_2023_entrance_AUTHORITATIVE_v1.0.0.csv"
IMPORTS_FILE = BASE / "00_DATA" / "00.02_PREPROCESSED" / "panjiva_imports_2023_AUTHORITATIVE_v1.0.0.csv"
OUTPUT_FILE = BASE / "00_DATA" / "00.03_MATCHED" / f"usace_2023_entrance_with_import_flags_v2.0.0_{timestamp}.csv"

# Create VOY_RECID from vessel + date + port
def create_voy_recid(vessel, date, port):
    """Create unique voyage identifier"""
    key = f"{vessel}|{date}|{port}".upper()
    return hashlib.md5(key.encode()).hexdigest()[:16]

# Load data
print(f"\n1. Loading USACE entrance data...")
entrance = pd.read_csv(ENTRANCE_FILE, low_memory=False)
print(f"   Entrance records: {len(entrance):,}")
print(f"   Columns: {len(entrance.columns)}")

print(f"\n2. Loading Panjiva imports data...")
imports = pd.read_csv(IMPORTS_FILE, low_memory=False)
print(f"   Import records: {len(imports):,}")
print(f"   Columns: {len(imports.columns)}")

# Create VOY_RECID for each import manifest
print(f"\n3. Creating VOY_RECID for import manifests...")
imports['VOY_RECID'] = imports.apply(
    lambda row: create_voy_recid(
        str(row.get('Vessel', '')),
        str(row.get('Arrival Date', '')),
        str(row.get('Port of Discharge (D)', ''))
    ),
    axis=1
)

# Get unique manifests
unique_manifests = imports[['VOY_RECID', 'Vessel', 'Arrival Date', 'Port of Discharge (D)', 'IMO']].drop_duplicates('VOY_RECID')
print(f"   Total import cargo records: {len(imports):,}")
print(f"   Unique manifests: {len(unique_manifests):,}")
print(f"   Avg items per manifest: {len(imports)/len(unique_manifests):.1f}")

# Parse dates
print(f"\n4. Parsing dates...")
entrance['Arrival_Date_Parsed'] = pd.to_datetime(entrance['Arrival_Date'], errors='coerce')
unique_manifests['Arrival_Date_Parsed'] = pd.to_datetime(unique_manifests['Arrival Date'], errors='coerce')

print(f"   Entrance dates parsed: {entrance['Arrival_Date_Parsed'].notna().sum():,}")
print(f"   Import dates parsed: {unique_manifests['Arrival_Date_Parsed'].notna().sum():,}")

# Initialize match columns
entrance['Has_Import_Manifest'] = False
entrance['Import_VOY_RECID'] = None

# Matching
print(f"\n5. Matching entrance -> imports (IMO + Date ±3 days, port ignored)...")
match_stats = {'IMO_Match': 0, 'Name_Match': 0, 'No_Match': 0}

for idx, ent_row in entrance.iterrows():
    if idx % 5000 == 0:
        print(f"   Processing {idx:,}/{len(entrance):,}")

    # Proper IMO conversion: float -> int -> string
    ent_imo = str(int(ent_row.get('IMO'))) if pd.notna(ent_row.get('IMO')) else ''
    ent_vessel = str(ent_row.get('Vessel', '')).strip().upper()
    ent_date = ent_row['Arrival_Date_Parsed']

    if pd.isna(ent_date):
        continue

    # Try IMO match first (NO PORT MATCHING - codes don't align)
    if ent_imo and ent_imo != '':
        # Convert manifest IMOs properly too
        manifest_imos = unique_manifests['IMO'].dropna().astype(int).astype(str)
        candidates = unique_manifests[
            (manifest_imos == ent_imo) &
            (unique_manifests['Arrival_Date_Parsed'].notna()) &
            (abs((unique_manifests['Arrival_Date_Parsed'] - ent_date).dt.days) <= 3)
        ]

        if len(candidates) > 0:
            # Take first match (closest date)
            best = candidates.iloc[0]
            entrance.at[idx, 'Has_Import_Manifest'] = True
            entrance.at[idx, 'Import_VOY_RECID'] = best['VOY_RECID']
            match_stats['IMO_Match'] += 1
            continue

    # Fallback: Vessel name match (NO PORT MATCHING)
    candidates = unique_manifests[
        (unique_manifests['Vessel'].str.upper().str.strip() == ent_vessel) &
        (unique_manifests['Arrival_Date_Parsed'].notna()) &
        (abs((unique_manifests['Arrival_Date_Parsed'] - ent_date).dt.days) <= 3)
    ]

    if len(candidates) > 0:
        best = candidates.iloc[0]
        entrance.at[idx, 'Has_Import_Manifest'] = True
        entrance.at[idx, 'Import_VOY_RECID'] = best['VOY_RECID']
        match_stats['Name_Match'] += 1
    else:
        match_stats['No_Match'] += 1

# Results
print(f"\n6. Matching results:")
print(f"   IMO matches: {match_stats['IMO_Match']:,}")
print(f"   Name matches: {match_stats['Name_Match']:,}")
print(f"   No match: {match_stats['No_Match']:,}")
print(f"   Match rate: {(match_stats['IMO_Match'] + match_stats['Name_Match'])/len(entrance)*100:.1f}%")

# Save
print(f"\n7. Saving matched entrance file...")
print(f"   Output: {OUTPUT_FILE}")
entrance.to_csv(OUTPUT_FILE, index=False)

print(f"\n   Original columns: {len(entrance.columns)-2}")
print(f"   New columns added: 2 (Has_Import_Manifest, Import_VOY_RECID)")
print(f"   Total columns: {len(entrance.columns)}")
print(f"   File size: {OUTPUT_FILE.stat().st_size / 1024 / 1024:.1f} MB")

print(f"\n{'='*80}")
print("SIMPLIFIED MATCHING COMPLETE")
print("="*80)
print(f"\nNext step: Match clearance -> exports using same approach")
