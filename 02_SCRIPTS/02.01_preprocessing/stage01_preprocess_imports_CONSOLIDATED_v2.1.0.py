"""
Panjiva Import Preprocessing v2.1.0 - CONSOLIDATED
====================================================

Purpose: Transform raw Panjiva import data (135 cols) → preprocessed (60 cols)
         ALL transformations consolidated into single preprocessing step

CHANGES FROM v2.0.0:
- Added deduplication based on Bill of Lading Number (government unique ID)
- Handles overlapping raw file downloads

CHANGES FROM v1.0.0:
- Added vessel enrichment (Type, DWT, Vessel_Type_Simple)
- Added all lock flags (Group_Locked, Commodity_Locked, Cargo_Locked, Cargo_Detail_Locked)
- Added tracking columns (Classified_Phase, Last_Rule_ID)
- Added Package_Type (alias for Pckg, used by classification rules)
- Outputs to 00_DATA/00.02_PREPROCESSED/ as AUTHORITATIVE files

Operations:
1. Load raw files and concatenate
2. Remove duplicates based on Bill of Lading Number
3. Assign REC_ID (permanent unique identifier)
4. Drop 84 unnecessary columns
5. Rename 9 columns for clarity
6. Split Quantity → Qty + Pckg
7. Extract HS2, HS4, HS6 from HS Code
8. Harmonize Shipper/Consignee names
9. Add port rollups (placeholders)
10. Enrich vessel data from ship registry (Type, DWT, Vessel_Type_Simple)
11. Add metadata (Carrier Name, Package_Type, Count)
12. Initialize classification columns (Group, Commodity, Cargo, Cargo Detail) - EMPTY
13. Initialize lock flags (all FALSE)
14. Initialize tracking columns (Classified_Phase, Last_Rule_ID) - EMPTY
15. Initialize reporting columns (Report_One/Two/Three/Four, Filter, Note) - EMPTY

Input:  Raw Panjiva CSV files (135 columns)
Output: Preprocessed CSV (60 columns) ready for classification

Author: WSD3 / Claude Code
Date: 2026-02-09
Version: 2.1.0
"""

import pandas as pd
import numpy as np
import re
import glob
import logging
import sys
from pathlib import Path
from datetime import datetime
import traceback

# ============================================================================
# CONFIGURATION
# ============================================================================

# Project root
PROJECT_ROOT = Path(r"G:\My Drive\LLM\project_manifest")

# Paths
RAW_DATA_PATH = PROJECT_ROOT / "00_raw_data" / "00_01_panjiva_imports_raw"
SHIP_REGISTRY = PROJECT_ROOT / "01_DICTIONARIES" / "01.03_vessels" / "01_ships_register.csv"
OUTPUT_DIR = PROJECT_ROOT / "00_DATA" / "00.02_PREPROCESSED"
EXCLUDED_DIR = PROJECT_ROOT / "00_DATA" / "00_excluded"
LOG_DIR = PROJECT_ROOT / "logs"

# Create directories if needed
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
EXCLUDED_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Logging setup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = LOG_DIR / f"preprocess_v2.0.0_{timestamp}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

# ============================================================================
# COLUMN DEFINITIONS
# ============================================================================

# Columns to KEEP from raw data
COLUMNS_TO_KEEP = [
    'Bill of Lading Number',
    'Arrival Date',
    'Consignee',
    'Consignee (Original Format)',
    'Consignee SIC Codes',
    'Shipper',
    'Shipper (Original Format)',
    'Shipper SIC Codes',
    'Notify Party',
    'Carrier',
    'Shipment Origin',
    'Shipment Destination',
    'Port of Unlading',
    'Port of Lading',
    'Port of Lading Country',
    'Place of Receipt',
    'Vessel',
    'Vessel Voyage ID',
    'Vessel IMO',
    'Is Containerized',
    'Quantity',
    'Measurement',
    'Weight (kg)',
    'Weight (t)',
    'Weight (Original Format)',
    'Value of Goods (USD)',
    'HS Code',
    'Goods Shipped',
]

# Column renaming map
COLUMN_RENAME_MAP = {
    'Shipment Origin': 'Origin (F)',
    'Shipment Destination': 'Destination (D)',
    'Port of Unlading': 'Port of Discharge (D)',
    'Port of Lading': 'Port of Loading (F)',
    'Port of Lading Country': 'Country of Origin (F)',
    'Place of Receipt': 'Place of Receipt (F)',
    'Vessel Voyage ID': 'Voyage',
    'Vessel IMO': 'IMO',
    'Weight (kg)': 'Kilos',
    'Weight (t)': 'Tons',
    'Value of Goods (USD)': 'Value',
    'HS Code': 'HS Code Desc.',
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def stamp(msg):
    """Print timestamped message"""
    logging.info(msg)

def assign_rec_id(df, file_number):
    """
    Assign unique REC_ID to each row
    Format: PANV_IMP_FILE###_R######
    """
    rec_ids = [
        f"PANV_IMP_FILE{file_number:03d}_R{i:06d}"
        for i in range(len(df))
    ]
    return rec_ids

def harmonize_name(name):
    """
    Harmonize company names
    - Standardize capitalization
    - Expand abbreviations
    - Remove extra whitespace/punctuation
    """
    if pd.isna(name) or name == '':
        return ''

    # Convert to string and strip
    name = str(name).strip()

    # Title case
    name = name.title()

    # Expand common abbreviations
    abbrev_map = {
        ' Corp.': ' Corporation',
        ' Corp': ' Corporation',
        ' Co.': ' Company',
        ' Co': ' Company',
        ' Inc.': ' Incorporated',
        ' Inc': ' Incorporated',
        ' Ltd.': ' Limited',
        ' Ltd': ' Limited',
        ' Llc': ' LLC',
    }
    for abbrev, full in abbrev_map.items():
        name = name.replace(abbrev, full)

    # Remove punctuation (except periods in abbreviations)
    name = re.sub(r'[,\-]', ' ', name)

    # Normalize whitespace
    name = re.sub(r'\s+', ' ', name).strip()

    return name

def split_quantity(qty_str):
    """
    Split '3903 PCS' into (3903, 'PCS')
    Returns (qty_num, qty_pckg)
    """
    if pd.isna(qty_str) or qty_str == '':
        return None, None

    match = re.match(r'([0-9.,]+)\s*([A-Za-z]+.*)', str(qty_str))
    if match:
        try:
            qty_num = int(match.group(1).replace(',', ''))
            qty_pckg = match.group(2).strip()
            return qty_num, qty_pckg
        except:
            return None, None
    return None, None

def extract_hs_codes(hs_desc):
    """
    Extract HS2, HS4, HS6 from HS Code description
    Example: '1431.49 XXXX' → HS2='14', HS4='1431', HS6='143149'
    """
    if pd.isna(hs_desc) or hs_desc == '':
        return '', '', ''

    # Remove periods and extract first 6 digits
    hs_clean = str(hs_desc).replace('.', '').strip()
    match = re.match(r'(\d{2})(\d{2})(\d{2})', hs_clean)

    if match:
        hs2 = match.group(1)
        hs4 = match.group(1) + match.group(2)
        hs6 = match.group(1) + match.group(2) + match.group(3)
        return hs2, hs4, hs6

    # Fallback: extract what we can
    digits = re.findall(r'\d+', hs_clean)
    if digits:
        hs_str = ''.join(digits)[:6].ljust(6, '0')
        hs2 = hs_str[:2]
        hs4 = hs_str[:4]
        hs6 = hs_str[:6]
        return hs2, hs4, hs6

    return '', '', ''

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

def load_ship_registry():
    """Load ship registry and create lookup dictionary"""
    stamp("Loading ship registry...")

    try:
        df_ships = pd.read_csv(SHIP_REGISTRY, dtype=str)
        stamp(f"Loaded {len(df_ships):,} vessels from registry")

        # Create lookup: vessel_name → (Type, DWT, Vessel_Type_Simple)
        vessel_lookup = {}
        for _, row in df_ships.iterrows():
            vessel_name = str(row.get('Vessel', '')).upper().strip()
            if vessel_name:
                vessel_type = row.get('Type', '')
                vessel_dwt = row.get('DWT', '')
                vessel_simple = map_vessel_type(vessel_type)
                vessel_lookup[vessel_name] = (vessel_type, vessel_dwt, vessel_simple)

        stamp(f"Created lookup for {len(vessel_lookup):,} vessels")
        return vessel_lookup

    except Exception as e:
        stamp(f"WARNING: Could not load ship registry: {e}")
        return {}

# ============================================================================
# MAIN PROCESSING FUNCTIONS
# ============================================================================

def load_raw_files(sample_size=None, year=None):
    """
    Load raw Panjiva files

    Args:
        sample_size: Number of records to load (for testing)
        year: Year to filter (2023, 2024, 2025)

    Returns:
        DataFrame with raw data
        List of (file_number, file_path) tuples
    """
    stamp("\n" + "="*80)
    stamp("STEP 1: LOADING RAW DATA")
    stamp("="*80)

    # Find all CSV files
    pattern = str(RAW_DATA_PATH / "*.csv")
    files = sorted(glob.glob(pattern))

    if not files:
        raise FileNotFoundError(f"No CSV files found in {RAW_DATA_PATH}")

    stamp(f"Found {len(files)} raw files")

    # Load files
    dfs = []
    file_info = []
    total_loaded = 0

    for file_num, file_path in enumerate(files, start=1):
        try:
            # Load file
            df_file = pd.read_csv(file_path, dtype=str, low_memory=False)

            # Add file tracking
            file_info.extend([(file_num, file_path)] * len(df_file))
            dfs.append(df_file)

            total_loaded += len(df_file)
            stamp(f"File {file_num:03d}: {Path(file_path).name} ({len(df_file):,} records)")

            # Stop if sample size reached
            if sample_size and total_loaded >= sample_size:
                break

        except Exception as e:
            stamp(f"ERROR loading {file_path}: {e}")
            continue

    # Concatenate all files
    df = pd.concat(dfs, ignore_index=True)

    # Truncate to sample size if specified
    if sample_size and len(df) > sample_size:
        df = df.head(sample_size)
        file_info = file_info[:sample_size]

    stamp(f"\nLoaded {len(df):,} total records from {len(dfs)} files")
    stamp(f"Columns: {len(df.columns)}")

    return df, file_info

def remove_duplicates(df):
    """
    Remove duplicate records based on Bill of Lading Number
    BOL is a unique government-assigned identifier - duplicates indicate
    overlapping raw file downloads
    """
    stamp("\n" + "="*80)
    stamp("STEP 2: REMOVING DUPLICATES")
    stamp("="*80)

    initial_count = len(df)

    # Check for duplicates
    bol_duplicates = df['Bill of Lading Number'].duplicated(keep='first').sum()

    if bol_duplicates == 0:
        stamp("No duplicates found")
        return df

    stamp(f"Found {bol_duplicates:,} duplicate BOL numbers")

    # Remove duplicates, keeping first occurrence
    df = df.drop_duplicates(subset=['Bill of Lading Number'], keep='first')

    final_count = len(df)
    removed_count = initial_count - final_count

    stamp(f"Before: {initial_count:,} records")
    stamp(f"After:  {final_count:,} records")
    stamp(f"Removed: {removed_count:,} duplicates ({removed_count/initial_count*100:.1f}%)")

    return df

def assign_rec_ids(df, file_info):
    """Assign REC_ID to each row"""
    stamp("\n" + "="*80)
    stamp("STEP 3: ASSIGNING REC_ID")
    stamp("="*80)

    rec_ids = []
    for i, (file_num, _) in enumerate(file_info):
        rec_id = f"PANV_IMP_FILE{file_num:03d}_R{i:06d}"
        rec_ids.append(rec_id)

    df['REC_ID'] = rec_ids

    # Verify uniqueness
    if df['REC_ID'].is_unique:
        stamp(f"✅ REC_ID assigned: {len(df):,} unique identifiers")
    else:
        duplicates = df['REC_ID'].duplicated().sum()
        stamp(f"⚠️  WARNING: {duplicates} duplicate REC_IDs found!")

    return df

def select_and_rename_columns(df):
    """Select columns to keep and rename them"""
    stamp("\n" + "="*80)
    stamp("STEP 4: SELECTING & RENAMING COLUMNS")
    stamp("="*80)

    # Keep only specified columns
    available_cols = [col for col in COLUMNS_TO_KEEP if col in df.columns]
    missing_cols = [col for col in COLUMNS_TO_KEEP if col not in df.columns]

    if missing_cols:
        stamp(f"⚠️  WARNING: {len(missing_cols)} columns not found in data:")
        for col in missing_cols[:5]:
            stamp(f"  - {col}")

    df = df[available_cols + ['REC_ID']].copy()
    stamp(f"Kept {len(df.columns)} columns (dropped {135 - len(df.columns)})")

    # Rename columns
    df = df.rename(columns=COLUMN_RENAME_MAP)
    stamp(f"Renamed {len(COLUMN_RENAME_MAP)} columns")

    return df

def process_quantity_split(df):
    """Split Quantity column into Qty and Pckg"""
    stamp("\n" + "="*80)
    stamp("STEP 5: SPLITTING QUANTITY → QTY + PCKG")
    stamp("="*80)

    # Split quantity
    df[['Qty', 'Pckg']] = df['Quantity'].apply(
        lambda x: pd.Series(split_quantity(x))
    )

    # Drop original Quantity column
    df = df.drop(columns=['Quantity'])

    # Count successful splits
    valid_splits = df['Qty'].notna().sum()
    stamp(f"Split {valid_splits:,} / {len(df):,} quantities ({valid_splits/len(df)*100:.1f}%)")

    return df

def extract_hs_code_levels(df):
    """Extract HS2, HS4, HS6 from HS Code Desc."""
    stamp("\n" + "="*80)
    stamp("STEP 6: EXTRACTING HS CODES (HS2, HS4, HS6)")
    stamp("="*80)

    df[['HS2', 'HS4', 'HS6']] = df['HS Code Desc.'].apply(
        lambda x: pd.Series(extract_hs_codes(x))
    )

    # Count extractions
    hs2_count = (df['HS2'] != '').sum()
    hs4_count = (df['HS4'] != '').sum()
    hs6_count = (df['HS6'] != '').sum()

    stamp(f"Extracted HS2: {hs2_count:,} / {len(df):,} ({hs2_count/len(df)*100:.1f}%)")
    stamp(f"Extracted HS4: {hs4_count:,} / {len(df):,} ({hs4_count/len(df)*100:.1f}%)")
    stamp(f"Extracted HS6: {hs6_count:,} / {len(df):,} ({hs6_count/len(df)*100:.1f}%)")

    return df

def harmonize_names(df):
    """Harmonize Shipper and Consignee names"""
    stamp("\n" + "="*80)
    stamp("STEP 7: HARMONIZING SHIPPER/CONSIGNEE NAMES")
    stamp("="*80)

    # Harmonize (overwrite main columns, keep Original Format)
    df['Shipper'] = df['Shipper'].apply(harmonize_name)
    df['Consignee'] = df['Consignee'].apply(harmonize_name)

    stamp("✅ Harmonized Shipper and Consignee names")
    stamp("   Original values preserved in '(Original Format)' columns")

    return df

def add_port_rollups(df):
    """Add port rollup columns (placeholder for now)"""
    stamp("\n" + "="*80)
    stamp("STEP 8: ADDING PORT ROLLUPS")
    stamp("="*80)

    # Initialize columns (will be populated by port dictionary in future)
    df['Port_Consolidated'] = ''
    df['Port_Coast'] = ''
    df['Port_Region'] = ''
    df['Port_Code'] = ''

    stamp("✅ Port rollup columns added (empty - to be populated later)")

    return df

def enrich_vessel_data(df, vessel_lookup):
    """Add vessel Type, DWT, and Vessel_Type_Simple from registry"""
    stamp("\n" + "="*80)
    stamp("STEP 9: ENRICHING VESSEL DATA")
    stamp("="*80)

    # Initialize columns
    df['Type'] = ''
    df['DWT'] = ''
    df['Vessel_Type_Simple'] = ''

    # Lookup vessel data
    matched_count = 0
    for idx in df.index:
        vessel_name = str(df.at[idx, 'Vessel']).upper().strip()
        if vessel_name in vessel_lookup:
            vessel_type, vessel_dwt, vessel_simple = vessel_lookup[vessel_name]
            df.at[idx, 'Type'] = vessel_type
            df.at[idx, 'DWT'] = vessel_dwt
            df.at[idx, 'Vessel_Type_Simple'] = vessel_simple
            matched_count += 1

    # Count matches
    stamp(f"Matched vessels: {matched_count:,} / {len(df):,} ({matched_count/len(df)*100:.1f}%)")

    return df

def add_metadata_columns(df):
    """Add Carrier Name, Package_Type, and Count columns"""
    stamp("\n" + "="*80)
    stamp("STEP 10: ADDING METADATA COLUMNS")
    stamp("="*80)

    # Extract Carrier Name (first part before hyphen/dash)
    df['Carrier Name'] = df['Carrier'].apply(
        lambda x: str(x).split('-')[0].strip() if pd.notna(x) else ''
    )

    # Add Package_Type (alias for Pckg - used by classification rules)
    df['Package_Type'] = df['Pckg']

    # Add Count column (always 1 for aggregation)
    df['Count'] = 1

    stamp("✅ Added Carrier Name, Package_Type, and Count columns")

    return df

def initialize_classification_columns(df):
    """Initialize empty classification, lock, tracking, and reporting columns"""
    stamp("\n" + "="*80)
    stamp("STEP 11: INITIALIZING CLASSIFICATION COLUMNS")
    stamp("="*80)

    # Classification columns (empty)
    df['Group'] = ''
    df['Commodity'] = ''
    df['Cargo'] = ''
    df['Cargo Detail'] = ''

    # Lock flags (FALSE)
    df['Group_Locked'] = 'FALSE'
    df['Commodity_Locked'] = 'FALSE'
    df['Cargo_Locked'] = 'FALSE'
    df['Cargo_Detail_Locked'] = 'FALSE'

    # Tracking columns (empty)
    df['Classified_Phase'] = ''
    df['Last_Rule_ID'] = ''

    # Reporting columns (empty)
    df['Report_One'] = ''
    df['Report_Two'] = ''
    df['Report_Three'] = ''
    df['Report_Four'] = ''
    df['Filter'] = ''
    df['Note'] = ''

    stamp("✅ Initialized 18 classification/lock/tracking/reporting columns")

    return df

def save_output(df, sample_size=None, year=None):
    """Save preprocessed data"""
    stamp("\n" + "="*80)
    stamp("STEP 12: SAVING OUTPUT")
    stamp("="*80)

    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')

    if sample_size:
        filename = f"sample_{sample_size}_preprocessed_v2.1.0_{timestamp_str}.csv"
    elif year:
        filename = f"panjiva_imports_{year}_AUTHORITATIVE_v2.1.0.csv"
    else:
        filename = f"panjiva_imports_preprocessed_v2.1.0_{timestamp_str}.csv"

    output_path = OUTPUT_DIR / filename

    df.to_csv(output_path, index=False)

    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    stamp(f"✅ Saved: {output_path.name}")
    stamp(f"   Records: {len(df):,}")
    stamp(f"   Columns: {len(df.columns)}")
    stamp(f"   Size: {file_size_mb:.1f} MB")

    # Show first few column names
    stamp(f"\nFirst 10 columns:")
    for i, col in enumerate(df.columns[:10], 1):
        stamp(f"  {i}. {col}")

    stamp(f"\nLast 10 columns:")
    for i, col in enumerate(df.columns[-10:], len(df.columns)-9):
        stamp(f"  {i}. {col}")

    return output_path

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main(sample_size=None, year=None):
    """Main preprocessing pipeline"""

    try:
        stamp("\n" + "="*80)
        stamp("PANJIVA PREPROCESSING v2.1.0 - CONSOLIDATED")
        stamp("="*80)
        stamp(f"Start time: {datetime.now()}")
        stamp(f"Sample size: {sample_size if sample_size else 'FULL'}")
        stamp(f"Year filter: {year if year else 'ALL'}")

        # Step 1: Load raw data
        df, file_info = load_raw_files(sample_size=sample_size, year=year)

        # Step 2: Remove duplicates
        df = remove_duplicates(df)

        # Step 3: Assign REC_ID
        df = assign_rec_ids(df, file_info)

        # Step 4: Select and rename columns
        df = select_and_rename_columns(df)

        # Step 5: Split Quantity
        df = process_quantity_split(df)

        # Step 6: Extract HS codes
        df = extract_hs_code_levels(df)

        # Step 7: Harmonize names
        df = harmonize_names(df)

        # Step 8: Add port rollups
        df = add_port_rollups(df)

        # Step 9: Enrich vessel data
        vessel_lookup = load_ship_registry()
        df = enrich_vessel_data(df, vessel_lookup)

        # Step 10: Add metadata
        df = add_metadata_columns(df)

        # Step 11: Initialize classification columns
        df = initialize_classification_columns(df)

        # Step 12: Save output
        output_path = save_output(df, sample_size=sample_size, year=year)

        stamp("\n" + "="*80)
        stamp("PREPROCESSING COMPLETE ✅")
        stamp("="*80)
        stamp(f"End time: {datetime.now()}")
        stamp(f"Output: {output_path}")
        stamp(f"Log file: {log_file}")

        return df

    except Exception as e:
        stamp("\n" + "="*80)
        stamp("PREPROCESSING FAILED ❌")
        stamp("="*80)
        stamp(f"Error: {str(e)}")
        stamp(f"Traceback:\n{traceback.format_exc()}")

        sys.exit(1)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Preprocess Panjiva import data v2.1.0')
    parser.add_argument('--sample', type=int, help='Sample size (e.g., 5000 for 5K test)')
    parser.add_argument('--year', type=int, help='Year to process (2023, 2024, 2025)')

    args = parser.parse_args()

    main(sample_size=args.sample, year=args.year)
