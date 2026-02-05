"""
SIMPLIFIED MARRIAGE: Entrance + Clearance -> Port Call Master
Version: 2.0.0 - SIMPLIFIED APPROACH
Date: 2026-01-16

Purpose:
- Marry entrance (arrival) + clearance (departure) into port calls
- Preserve manifest flags from both sides
- NO cargo data duplication - just foreign keys
- Much cleaner, smaller files

Matching Logic:
- Primary: IMO + PORT + sequential date (clearance after arrival)
- Fallback: Vessel Name + PORT + sequential date
- Take FIRST clearance after each entrance

Input:
- Entrance with flags: 00_DATA/00.03_MATCHED/usace_2023_entrance_with_import_flags_v2.0.0_*.csv
- Clearance with flags: 00_DATA/00.03_MATCHED/usace_2023_clearance_with_export_flags_v2.0.0_*.csv

Output:
- Port Call Master: 00_DATA/00.04_FINAL/usace_2023_portcall_master_SIMPLE_v2.0.0.csv

Output Columns (SIMPLIFIED):
- Port call basics: PORTCALL_ID, Record_Type, Vessel_Name, IMO, etc.
- Entrance data: Arrival_Date, Entrance_Port, Entrance_Draft, etc.
- Clearance data: Clearance_Date, Clearance_Port, Clearance_Draft, etc.
- Import manifest flags: Has_Import_Manifest, Import_VOY_RECID
- Export manifest flags: Has_Export_Manifest, Export_VOY_RECID
- Port stay: Port_Stay_Days

NOTE: To get cargo details, join back to Panjiva files:
  SELECT * FROM portcall
  JOIN panjiva_imports ON portcall.Import_VOY_RECID = panjiva.VOY_RECID
  WHERE Has_Import_Manifest = TRUE
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

print("="*80)
print("SIMPLIFIED MARRIAGE: Entrance + Clearance -> Port Calls v2.0.0")
print("="*80)
print("\nNew approach: Foreign keys only, NO cargo data duplication")

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# File paths
BASE = Path(r"G:\My Drive\LLM\project_manifest")
MATCHED_DIR = BASE / "00_DATA" / "00.03_MATCHED"

# Find latest entrance and clearance files
entrance_files = list(MATCHED_DIR.glob("usace_2023_entrance_with_import_flags_v2.0.0_*.csv"))
clearance_files = list(MATCHED_DIR.glob("usace_2023_clearance_with_export_flags_v2.0.0_*.csv"))

if not entrance_files or not clearance_files:
    print("\n[ERROR] Matched files not found!")
    print(f"Run match_entrance_to_imports_SIMPLE.py first")
    print(f"Run match_clearance_to_exports_SIMPLE.py first")
    exit(1)

ENTRANCE_FILE = sorted(entrance_files)[-1]  # Latest
CLEARANCE_FILE = sorted(clearance_files)[-1]  # Latest
OUTPUT_FILE = BASE / "00_DATA" / "00.04_FINAL" / f"usace_2023_portcall_master_SIMPLE_v2.0.0_{timestamp}.csv"

print(f"\nInput files:")
print(f"  Entrance: {ENTRANCE_FILE.name}")
print(f"  Clearance: {CLEARANCE_FILE.name}")

# Load data
print(f"\n1. Loading entrance data...")
entrance = pd.read_csv(ENTRANCE_FILE, low_memory=False)
print(f"   Entrance records: {len(entrance):,}")
print(f"   With import manifest: {entrance['Has_Import_Manifest'].sum():,}")

print(f"\n2. Loading clearance data...")
clearance = pd.read_csv(CLEARANCE_FILE, low_memory=False)
print(f"   Clearance records: {len(clearance):,}")
print(f"   With export manifest: {clearance['Has_Export_Manifest'].sum():,}")

# Parse dates
print(f"\n3. Parsing dates...")
entrance['Arrival_Date_Parsed'] = pd.to_datetime(entrance['Arrival_Date'], errors='coerce')
clearance['Clearance_Date_Parsed'] = pd.to_datetime(clearance['Clearance_Date'], errors='coerce')

# Sort for sequential matching
entrance_sorted = entrance.sort_values(['IMO', 'PORT', 'Arrival_Date_Parsed']).reset_index(drop=True)
clearance_sorted = clearance.sort_values(['IMO', 'PORT', 'Clearance_Date_Parsed']).reset_index(drop=True)

# Track matched clearances
clearance_matched = set()

# Build port calls
print(f"\n4. Building port calls (entrance -> clearance matching)...")
port_calls = []
match_stats = {'BOTH': 0, 'ENTRANCE_ONLY': 0, 'CLEARANCE_ONLY': 0}

for idx, ent_row in entrance_sorted.iterrows():
    if idx % 5000 == 0:
        print(f"   Processing entrance {idx:,}/{len(entrance_sorted):,}")

    # Proper IMO conversion: float -> int -> string
    vessel_imo = str(int(ent_row.get('IMO'))) if pd.notna(ent_row.get('IMO')) else ''
    vessel_name = str(ent_row.get('Vessel', '')).strip()
    port = str(ent_row.get('PORT', '')).strip()
    arrival_date = ent_row['Arrival_Date_Parsed']

    if pd.isna(arrival_date):
        # Entrance-only (no clearance possible without date)
        port_call = {
            'PORTCALL_ID': f"PC_{idx:06d}",
            'Record_Type': 'ENTRANCE_ONLY',
            'Vessel_Name': vessel_name,
            'IMO': vessel_imo,
            'Arrival_Date': ent_row.get('Arrival_Date'),
            'Entrance_Port': port,
            'Has_Import_Manifest': ent_row.get('Has_Import_Manifest', False),
            'Import_VOY_RECID': ent_row.get('Import_VOY_RECID'),
            'Clearance_Date': None,
            'Clearance_Port': None,
            'Has_Export_Manifest': False,
            'Export_VOY_RECID': None,
            'Port_Stay_Days': None
        }
        port_calls.append(port_call)
        match_stats['ENTRANCE_ONLY'] += 1
        continue

    # Find matching clearance (IMO + Port, clearance AFTER arrival)
    # Convert clearance IMOs properly
    clearance_imos = clearance_sorted['IMO'].apply(lambda x: str(int(x)) if pd.notna(x) else '')
    candidates = clearance_sorted[
        (clearance_imos == vessel_imo) &
        (clearance_sorted['PORT'].astype(str).str.strip() == port) &
        (clearance_sorted['Clearance_Date_Parsed'].notna()) &
        (clearance_sorted['Clearance_Date_Parsed'] >= arrival_date) &
        (~clearance_sorted.index.isin(clearance_matched))
    ]

    if len(candidates) == 0 and vessel_name:
        # Fallback: vessel name match
        candidates = clearance_sorted[
            (clearance_sorted['Vessel'].astype(str).str.strip() == vessel_name) &
            (clearance_sorted['PORT'].astype(str).str.strip() == port) &
            (clearance_sorted['Clearance_Date_Parsed'].notna()) &
            (clearance_sorted['Clearance_Date_Parsed'] >= arrival_date) &
            (~clearance_sorted.index.isin(clearance_matched))
        ]

    if len(candidates) > 0:
        # Take FIRST clearance after this entrance
        clr_row = candidates.iloc[0]
        clearance_matched.add(candidates.index[0])

        # Calculate port stay
        clearance_date = clr_row['Clearance_Date_Parsed']
        port_stay_days = (clearance_date - arrival_date).days if pd.notna(clearance_date) else None

        port_call = {
            'PORTCALL_ID': f"PC_{idx:06d}",
            'Record_Type': 'BOTH',
            'Vessel_Name': vessel_name,
            'IMO': vessel_imo,
            'Arrival_Date': ent_row.get('Arrival_Date'),
            'Entrance_Port': port,
            'Has_Import_Manifest': ent_row.get('Has_Import_Manifest', False),
            'Import_VOY_RECID': ent_row.get('Import_VOY_RECID'),
            'Clearance_Date': clr_row.get('Clearance_Date'),
            'Clearance_Port': clr_row.get('PORT'),
            'Has_Export_Manifest': clr_row.get('Has_Export_Manifest', False),
            'Export_VOY_RECID': clr_row.get('Export_VOY_RECID'),
            'Port_Stay_Days': port_stay_days
        }
        match_stats['BOTH'] += 1
    else:
        # Entrance-only (no matching clearance found)
        port_call = {
            'PORTCALL_ID': f"PC_{idx:06d}",
            'Record_Type': 'ENTRANCE_ONLY',
            'Vessel_Name': vessel_name,
            'IMO': vessel_imo,
            'Arrival_Date': ent_row.get('Arrival_Date'),
            'Entrance_Port': port,
            'Has_Import_Manifest': ent_row.get('Has_Import_Manifest', False),
            'Import_VOY_RECID': ent_row.get('Import_VOY_RECID'),
            'Clearance_Date': None,
            'Clearance_Port': None,
            'Has_Export_Manifest': False,
            'Export_VOY_RECID': None,
            'Port_Stay_Days': None
        }
        match_stats['ENTRANCE_ONLY'] += 1

    port_calls.append(port_call)

# Add unmatched clearances
print(f"\n5. Adding unmatched clearances (clearance-only port calls)...")
unmatched_clearances = clearance_sorted[~clearance_sorted.index.isin(clearance_matched)]

for idx, clr_row in unmatched_clearances.iterrows():
    port_call = {
        'PORTCALL_ID': f"PC_CLR_{idx:06d}",
        'Record_Type': 'CLEARANCE_ONLY',
        'Vessel_Name': clr_row.get('Vessel'),
        'IMO': clr_row.get('IMO'),
        'Arrival_Date': None,
        'Entrance_Port': None,
        'Has_Import_Manifest': False,
        'Import_VOY_RECID': None,
        'Clearance_Date': clr_row.get('Clearance_Date'),
        'Clearance_Port': clr_row.get('PORT'),
        'Has_Export_Manifest': clr_row.get('Has_Export_Manifest', False),
        'Export_VOY_RECID': clr_row.get('Export_VOY_RECID'),
        'Port_Stay_Days': None
    }
    port_calls.append(port_call)
    match_stats['CLEARANCE_ONLY'] += 1

# Create DataFrame
print(f"\n6. Creating port call master...")
portcall_df = pd.DataFrame(port_calls)

# Results
print(f"\n7. Marriage results:")
print(f"   Complete port calls (BOTH): {match_stats['BOTH']:,}")
print(f"   Entrance-only: {match_stats['ENTRANCE_ONLY']:,}")
print(f"   Clearance-only: {match_stats['CLEARANCE_ONLY']:,}")
print(f"   Total port calls: {len(portcall_df):,}")

print(f"\n8. Manifest flag summary:")
print(f"   Port calls with import manifest: {portcall_df['Has_Import_Manifest'].sum():,}")
print(f"   Port calls with export manifest: {portcall_df['Has_Export_Manifest'].sum():,}")
print(f"   Port calls with both manifests: {((portcall_df['Has_Import_Manifest']) & (portcall_df['Has_Export_Manifest'])).sum():,}")

# Save
print(f"\n9. Saving port call master...")
print(f"   Output: {OUTPUT_FILE}")
portcall_df.to_csv(OUTPUT_FILE, index=False)

print(f"\n   Total columns: {len(portcall_df.columns)}")
print(f"   File size: {OUTPUT_FILE.stat().st_size / 1024 / 1024:.1f} MB")

print(f"\n{'='*80}")
print("SIMPLIFIED PORT CALL MASTER COMPLETE")
print("="*80)
print(f"\nTo get cargo details, join back to Panjiva:")
print(f"  - Import cargo: JOIN panjiva_imports ON Import_VOY_RECID = VOY_RECID")
print(f"  - Export cargo: JOIN panjiva_exports ON Export_VOY_RECID = VOY_RECID")
