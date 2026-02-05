"""
Enhance AUTHORITATIVE Preprocessed Files v1.0.0
================================================

Purpose: Add missing columns to AUTHORITATIVE files for classification

The AUTHORITATIVE files (51 columns) have partial preprocessing but are missing:
- REC_ID (permanent unique identifier)
- Package_Type (alias for Pckg, needed by 218 classification rules)
- Vessel_Type_Simple (enrichment from ship registry)
- Carrier Name (extracted from Carrier field)
- Count (always 1)

This script adds these 5 columns to create full 59-column preprocessed files.

Input:  AUTHORITATIVE CSV (51 columns)
Output: Enhanced CSV (59 columns) ready for classification

Usage:
    python step01b_enhance_authoritative_v1.0.0.py 2024
    python step01b_enhance_authoritative_v1.0.0.py 2023
    python step01b_enhance_authoritative_v1.0.0.py 2025

Author: WSD3 / Claude Code
Date: 2026-01-28
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import sys
import logging
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
SHIP_REGISTRY = PROJECT_ROOT / "00_REFERENCE" / "ship_registry.csv"
OUTPUT_DIR = PROJECT_ROOT / "03_DATA" / "01_preprocessed"
LOG_DIR = PROJECT_ROOT / "05_LOGS"

# Parent project paths
PARENT_DATA = Path(r"G:\My Drive\LLM\project_manifest\00_DATA\00.02_PREPROCESSED")

# Create directories
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Logging setup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = LOG_DIR / f"step01b_enhance_{timestamp}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# ============================================================================
# VESSEL TYPE MAPPING
# ============================================================================

def map_vessel_type(detailed_type):
    """Map detailed vessel type to simplified category"""
    if pd.isna(detailed_type) or detailed_type == '':
        return ''

    detailed_type = str(detailed_type).upper()

    # RoRo vessels
    if any(x in detailed_type for x in ['PCC', 'PCTC', 'RO/RO', 'RORO', 'CAR CARRIER', 'VEHICLE']):
        return 'RoRo'

    # Tankers
    if any(x in detailed_type for x in ['TANKER', 'OIL', 'CHEMICAL', 'LNG', 'LPG', 'PRODUCT']):
        return 'Tanker'

    # Bulk Carriers
    if any(x in detailed_type for x in ['BULK', 'ORE', 'COAL', 'GRAIN']):
        return 'Bulk Carrier'

    # Container Ships
    if any(x in detailed_type for x in ['CONTAINER', 'FEEDER']):
        return 'Container Ship'

    # General Cargo
    if any(x in detailed_type for x in ['GENERAL CARGO', 'MULTIPURPOSE', 'BREAK BULK']):
        return 'General Cargo'

    # Reefers
    if 'REEF' in detailed_type:
        return 'Reefer'

    return 'Other'

# ============================================================================
# ENRICHMENT FUNCTIONS
# ============================================================================

def add_rec_id(df, file_number):
    """Add REC_ID: PANV_IMP_FILE###_R######"""
    logging.info(f"Adding REC_ID (file number: {file_number:03d})...")

    df['REC_ID'] = [
        f"PANV_IMP_FILE{file_number:03d}_R{i:06d}"
        for i in range(len(df))
    ]

    logging.info(f"  REC_ID added: {len(df):,} records")
    return df

def add_vessel_types(df):
    """Add Vessel_Type_Simple from ship registry"""
    logging.info("Enriching vessel types from ship registry...")

    # Load ship registry
    if not SHIP_REGISTRY.exists():
        logging.warning(f"  Ship registry not found: {SHIP_REGISTRY}")
        logging.warning("  Vessel_Type_Simple will be empty")
        df['Vessel_Type_Simple'] = ''
        return df

    ships = pd.read_csv(SHIP_REGISTRY, dtype=str, low_memory=False)
    ships['IMO'] = ships['IMO'].str.strip()
    ships['Type'] = ships['Type'].str.strip()

    # Map to simplified types
    ships['Vessel_Type_Simple'] = ships['Type'].apply(map_vessel_type)

    # Merge with main data
    df['IMO'] = df['IMO'].astype(str).str.strip()
    df = df.merge(
        ships[['IMO', 'Vessel_Type_Simple']],
        on='IMO',
        how='left'
    )

    # Fill blanks
    df['Vessel_Type_Simple'] = df['Vessel_Type_Simple'].fillna('')

    enriched = (df['Vessel_Type_Simple'] != '').sum()
    pct = enriched / len(df) * 100
    logging.info(f"  Vessel types enriched: {enriched:,} / {len(df):,} ({pct:.1f}%)")

    return df

def add_metadata_columns(df):
    """Add Carrier Name, Package_Type, Count"""
    logging.info("Adding metadata columns...")

    # Carrier Name (first part before '-')
    df['Carrier Name'] = df['Carrier'].apply(
        lambda x: str(x).split('-')[0].strip() if pd.notna(x) else ''
    )

    # Package_Type (alias for Pckg - used by 218 classification rules)
    if 'Pckg' in df.columns:
        df['Package_Type'] = df['Pckg']
    else:
        logging.warning("  Pckg column not found! Package_Type will be empty.")
        df['Package_Type'] = ''

    # Count (always 1)
    df['Count'] = 1

    logging.info("  Carrier Name, Package_Type, Count added")
    return df

def initialize_classification_columns(df):
    """Initialize classification columns if not present"""
    logging.info("Initializing classification columns...")

    classification_cols = {
        'Group': '',
        'Commodity': '',
        'Cargo': '',
        'Cargo Detail': '',
        'Group_Locked': 'FALSE',
        'Commodity_Locked': 'FALSE',
        'Cargo_Locked': 'FALSE',
        'Cargo_Detail_Locked': 'FALSE',
        'Classified_Phase': '',
        'Last_Rule_ID': ''
    }

    for col, default_value in classification_cols.items():
        if col not in df.columns:
            df[col] = default_value
            logging.info(f"  Added: {col}")
        else:
            # Clear existing values
            df[col] = default_value
            logging.info(f"  Cleared: {col}")

    return df

# ============================================================================
# MAIN PROCESSING
# ============================================================================

def process_year(year, file_number=1):
    """Process a single year's AUTHORITATIVE file"""

    input_file = PARENT_DATA / f"panjiva_imports_{year}_AUTHORITATIVE_v1.0.0.csv"
    output_file = OUTPUT_DIR / f"panjiva_imports_{year}_preprocessed_v1.0.0_{timestamp}.csv"

    if not input_file.exists():
        logging.error(f"Input file not found: {input_file}")
        return False

    logging.info("="*70)
    logging.info(f"PROCESSING YEAR {year}")
    logging.info("="*70)
    logging.info(f"Input: {input_file.name}")
    logging.info(f"Output: {output_file.name}")

    try:
        # Load data
        logging.info(f"\nLoading data...")
        df = pd.read_csv(input_file, dtype=str, low_memory=False)
        logging.info(f"  Loaded: {len(df):,} rows, {len(df.columns)} columns")

        # Apply transformations
        df = add_rec_id(df, file_number)
        df = add_vessel_types(df)
        df = add_metadata_columns(df)
        df = initialize_classification_columns(df)

        # Save output
        logging.info(f"\nSaving enhanced file...")
        df.to_csv(output_file, index=False)

        size_mb = output_file.stat().st_size / (1024*1024)
        logging.info(f"  Saved: {output_file.name}")
        logging.info(f"  Size: {size_mb:.1f} MB")
        logging.info(f"  Rows: {len(df):,}")
        logging.info(f"  Columns: {len(df.columns)}")

        # Verify output
        logging.info(f"\nVerifying output...")
        required_cols = ['REC_ID', 'Package_Type', 'Vessel_Type_Simple', 'Carrier Name', 'Count']
        missing = [col for col in required_cols if col not in df.columns]

        if missing:
            logging.error(f"  Missing columns: {missing}")
            return False
        else:
            logging.info(f"  All required columns present")

        logging.info(f"\nCOMPLETED SUCCESSFULLY")
        return True

    except Exception as e:
        logging.error(f"Error processing {year}: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return False

# ============================================================================
# MAIN
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python step01b_enhance_authoritative_v1.0.0.py <year>")
        print("Example: python step01b_enhance_authoritative_v1.0.0.py 2024")
        sys.exit(1)

    year = sys.argv[1]

    logging.info("="*70)
    logging.info("ENHANCE AUTHORITATIVE FILES v1.0.0")
    logging.info("="*70)
    logging.info(f"Year: {year}")
    logging.info(f"Timestamp: {timestamp}")
    logging.info(f"Log: {log_file}")

    success = process_year(year)

    if success:
        logging.info("\n" + "="*70)
        logging.info("STATUS: SUCCESS")
        logging.info("="*70)
        logging.info(f"\nNext step: Run classification")
        logging.info(f"  python step02_classify_v1.0.0.py {year}")
    else:
        logging.error("\n" + "="*70)
        logging.error("STATUS: FAILED")
        logging.error("="*70)
        sys.exit(1)

if __name__ == "__main__":
    main()
