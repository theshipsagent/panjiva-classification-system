"""
Upgrade AUTHORITATIVE v1.0.0 to v2.0.0
========================================

Adds missing columns to existing v1.0.0 files to make them v2.0.0 compatible.

CHANGES:
- Add Vessel_Type_Simple (mapped from existing Type column)
- Add Group_Locked, Commodity_Locked, Cargo_Locked, Cargo_Detail_Locked (FALSE)
- Add Classified_Phase, Last_Rule_ID (empty)
- Add Package_Type (copy from Pckg)

Input:  v1.0.0 files (51 columns)
Output: v2.0.0 files (59 columns)

Author: WSD3 / Claude Code
Date: 2026-01-28
Version: 1.0.0
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

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

def upgrade_file(input_file, output_file):
    """Upgrade v1.0.0 file to v2.0.0"""

    stamp("="*80)
    stamp("UPGRADE v1.0.0 to v2.0.0")
    stamp("="*80)
    stamp(f"Input:  {input_file.name}")
    stamp(f"Output: {output_file.name}")

    # Load v1.0.0 file
    stamp("\n[1/4] Loading v1.0.0 file...")
    df = pd.read_csv(input_file, dtype=str, low_memory=False)
    stamp(f"      Loaded: {len(df):,} records, {len(df.columns)} columns")

    # Verify it's a v1.0.0 file (should have ~51 columns, missing v2.0.0 columns)
    v2_columns = ['Vessel_Type_Simple', 'Group_Locked', 'Commodity_Locked',
                  'Cargo_Locked', 'Cargo_Detail_Locked', 'Classified_Phase',
                  'Last_Rule_ID', 'Package_Type']

    existing_v2_cols = [col for col in v2_columns if col in df.columns]
    if existing_v2_cols:
        stamp(f"      WARNING: File already has some v2.0.0 columns: {existing_v2_cols}")
        stamp(f"      This may already be a v2.0.0 file!")
        response = input("      Continue anyway? (y/n): ")
        if response.lower() != 'y':
            stamp("      Aborted by user")
            return False

    # Add missing columns
    stamp("\n[2/4] Adding v2.0.0 columns...")

    # Vessel_Type_Simple (map from Type column)
    if 'Type' in df.columns and 'Vessel_Type_Simple' not in df.columns:
        stamp("      Adding Vessel_Type_Simple...")
        df['Vessel_Type_Simple'] = df['Type'].apply(map_vessel_type)
        mapped = (df['Vessel_Type_Simple'] != '').sum()
        stamp(f"        Mapped: {mapped:,} / {len(df):,} ({mapped/len(df)*100:.1f}%)")
    elif 'Vessel_Type_Simple' in df.columns:
        stamp("      Vessel_Type_Simple already exists, skipping")
    else:
        stamp("      WARNING: No 'Type' column found, adding empty Vessel_Type_Simple")
        df['Vessel_Type_Simple'] = ''

    # Lock flags (all FALSE)
    for lock_col in ['Group_Locked', 'Commodity_Locked', 'Cargo_Locked', 'Cargo_Detail_Locked']:
        if lock_col not in df.columns:
            df[lock_col] = 'FALSE'
            stamp(f"      Added {lock_col} = FALSE")

    # Tracking columns (empty)
    for track_col in ['Classified_Phase', 'Last_Rule_ID']:
        if track_col not in df.columns:
            df[track_col] = ''
            stamp(f"      Added {track_col} = (empty)")

    # Package_Type (copy from Pckg)
    if 'Pckg' in df.columns and 'Package_Type' not in df.columns:
        df['Package_Type'] = df['Pckg']
        stamp("      Added Package_Type (copied from Pckg)")
    elif 'Package_Type' in df.columns:
        stamp("      Package_Type already exists, skipping")
    else:
        stamp("      WARNING: No 'Pckg' column found, adding empty Package_Type")
        df['Package_Type'] = ''

    stamp(f"\n[3/4] Final schema: {len(df.columns)} columns")

    # Save v2.0.0 file
    stamp("\n[4/4] Saving v2.0.0 file...")
    df.to_csv(output_file, index=False)

    file_size_mb = output_file.stat().st_size / (1024 * 1024)
    stamp(f"      Saved: {output_file.name}")
    stamp(f"      Size: {file_size_mb:.1f} MB")
    stamp(f"      Records: {len(df):,}")
    stamp(f"      Columns: {len(df.columns)}")

    stamp("\n" + "="*80)
    stamp("UPGRADE COMPLETE")
    stamp("="*80)

    return True

def main(year=None):
    """Main upgrade function"""

    # Paths
    INPUT_DIR = Path(r"G:\My Drive\LLM\project_manifest\00_DATA\00.02_PREPROCESSED")

    if year:
        # Upgrade specific year
        input_file = INPUT_DIR / f"panjiva_imports_{year}_AUTHORITATIVE_v1.0.0.csv"
        output_file = INPUT_DIR / f"panjiva_imports_{year}_AUTHORITATIVE_v2.0.0.csv"

        if not input_file.exists():
            stamp(f"ERROR: Input file not found: {input_file}")
            sys.exit(1)

        if output_file.exists():
            stamp(f"WARNING: Output file already exists: {output_file}")
            response = input("Overwrite? (y/n): ")
            if response.lower() != 'y':
                stamp("Aborted by user")
                sys.exit(1)

        upgrade_file(input_file, output_file)

    else:
        # Upgrade all years (2023, 2024, 2025)
        years = [2023, 2024, 2025]
        for yr in years:
            stamp(f"\n{'='*80}")
            stamp(f"PROCESSING YEAR {yr}")
            stamp(f"{'='*80}\n")

            input_file = INPUT_DIR / f"panjiva_imports_{yr}_AUTHORITATIVE_v1.0.0.csv"
            output_file = INPUT_DIR / f"panjiva_imports_{yr}_AUTHORITATIVE_v2.0.0.csv"

            if not input_file.exists():
                stamp(f"SKIP: Input file not found: {input_file.name}")
                continue

            if output_file.exists():
                stamp(f"SKIP: Output file already exists: {output_file.name}")
                continue

            try:
                upgrade_file(input_file, output_file)
            except Exception as e:
                stamp(f"ERROR upgrading {yr}: {str(e)}")
                import traceback
                stamp(traceback.format_exc())

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Upgrade AUTHORITATIVE v1.0.0 to v2.0.0')
    parser.add_argument('--year', type=int, help='Year to upgrade (2023, 2024, or 2025). If not specified, upgrades all.')

    args = parser.parse_args()

    main(year=args.year)
