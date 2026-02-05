"""
Enrich Vessel Data for v2.0.0 Files
====================================

Populates empty Type, DWT, and Vessel_Type_Simple columns
by matching vessel names against ship registry.

Author: WSD3 / Claude Code
Date: 2026-01-28
Version: 1.0.0
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    """Print timestamped message"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def map_vessel_type(detailed_type):
    """Map detailed vessel type to simplified category"""
    if pd.isna(detailed_type) or detailed_type == '':
        return ''

    detailed_type = str(detailed_type).upper()

    if any(x in detailed_type for x in ['BULK CARRIER', 'BULKER', 'CAPESIZE', 'PANAMAX',
                                          'HANDYMAX', 'HANDYSIZE', 'SUPRAMAX', 'ULTRAMAX']):
        return 'Bulk Carrier'
    if any(x in detailed_type for x in ['TANKER', 'VLCC', 'SUEZMAX', 'AFRAMAX', 'MR', 'LR']):
        return 'Tanker'
    if any(x in detailed_type for x in ['LPG', 'LNG', 'GAS CARRIER']):
        return 'LPG/LNG Carrier'
    if any(x in detailed_type for x in ['CONTAINER', 'TEU', 'FEEDER']):
        return 'Container'
    if any(x in detailed_type for x in ['RO-RO', 'RORO', 'CAR CARRIER', 'PCTC']):
        return 'RoRo'
    if any(x in detailed_type for x in ['REEFER', 'REFRIGERAT']):
        return 'Reefer'
    if any(x in detailed_type for x in ['GENERAL CARGO', 'MULTI-PURPOSE']):
        return 'General Cargo'

    return ''

def enrich_vessel_data(file_path, ship_registry_path):
    """Enrich vessel data in place"""

    stamp("="*80)
    stamp("VESSEL DATA ENRICHMENT")
    stamp("="*80)
    stamp(f"File: {file_path.name}")

    # Load ship registry
    stamp("\n[1/4] Loading ship registry...")
    df_ships = pd.read_csv(ship_registry_path, dtype=str)
    stamp(f"      Loaded: {len(df_ships):,} vessels")

    # Create lookup dictionary
    vessel_lookup = {}
    for _, row in df_ships.iterrows():
        vessel_name = str(row.get('Vessel', '')).upper().strip()
        if vessel_name:
            vessel_type = row.get('Type', '')
            vessel_dwt = row.get('DWT', '')
            vessel_simple = map_vessel_type(vessel_type)
            vessel_lookup[vessel_name] = (vessel_type, vessel_dwt, vessel_simple)

    stamp(f"      Created lookup for {len(vessel_lookup):,} vessels")

    # Load data file
    stamp("\n[2/4] Loading data file...")
    df = pd.read_csv(file_path, dtype=str, low_memory=False)
    stamp(f"      Loaded: {len(df):,} records, {len(df.columns)} columns")

    # Check current vessel data population
    type_populated = (df['Type'].notna() & (df['Type'] != '')).sum() if 'Type' in df.columns else 0
    vessel_simple_populated = (df['Vessel_Type_Simple'].notna() & (df['Vessel_Type_Simple'] != '')).sum() if 'Vessel_Type_Simple' in df.columns else 0

    stamp(f"\n      Current vessel data:")
    stamp(f"        Type populated: {type_populated:,} / {len(df):,} ({type_populated/len(df)*100:.1f}%)")
    stamp(f"        Vessel_Type_Simple populated: {vessel_simple_populated:,} / {len(df):,} ({vessel_simple_populated/len(df)*100:.1f}%)")

    # Enrich vessel data
    stamp("\n[3/4] Enriching vessel data...")
    matched_count = 0

    # Process in batches for progress updates
    batch_size = 50000
    total_batches = (len(df) + batch_size - 1) // batch_size

    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min((batch_num + 1) * batch_size, len(df))

        for idx in range(start_idx, end_idx):
            vessel_name = str(df.at[idx, 'Vessel']).upper().strip() if pd.notna(df.at[idx, 'Vessel']) else ''

            if vessel_name and vessel_name in vessel_lookup:
                vessel_type, vessel_dwt, vessel_simple = vessel_lookup[vessel_name]
                df.at[idx, 'Type'] = vessel_type
                df.at[idx, 'DWT'] = vessel_dwt
                df.at[idx, 'Vessel_Type_Simple'] = vessel_simple
                matched_count += 1

        # Progress update
        if batch_num % 5 == 0:
            stamp(f"      Processing batch {batch_num + 1}/{total_batches}... ({matched_count:,} matched so far)")

    stamp(f"\n      Enrichment complete:")
    stamp(f"        Matched: {matched_count:,} / {len(df):,} ({matched_count/len(df)*100:.1f}%)")

    # Save enriched file
    stamp("\n[4/4] Saving enriched file...")
    df.to_csv(file_path, index=False)

    file_size_mb = file_path.stat().st_size / (1024 * 1024)
    stamp(f"      Saved: {file_path.name}")
    stamp(f"      Size: {file_size_mb:.1f} MB")

    stamp("\n" + "="*80)
    stamp("ENRICHMENT COMPLETE")
    stamp("="*80)

def main(year):
    """Main enrichment function"""

    # Paths
    DATA_DIR = Path(r"G:\My Drive\LLM\project_manifest\00_DATA\00.02_PREPROCESSED")
    SHIP_REGISTRY = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.03_vessels\01_ships_register.csv")

    if year:
        # Enrich specific year
        file_path = DATA_DIR / f"panjiva_imports_{year}_AUTHORITATIVE_v2.0.0.csv"

        if not file_path.exists():
            stamp(f"ERROR: File not found: {file_path}")
            return

        if not SHIP_REGISTRY.exists():
            stamp(f"ERROR: Ship registry not found: {SHIP_REGISTRY}")
            return

        enrich_vessel_data(file_path, SHIP_REGISTRY)

    else:
        # Enrich all years
        stamp("ERROR: Must specify --year argument")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Enrich vessel data for v2.0.0 files')
    parser.add_argument('--year', type=int, required=True, help='Year to enrich (2023, 2024, or 2025)')

    args = parser.parse_args()

    main(year=args.year)
