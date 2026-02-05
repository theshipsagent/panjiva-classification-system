"""
Master Data Dictionary Builder v1.0.0
======================================

Scans ALL data sources across the project and builds:
1. MASTER_DATA_DICTIONARY.csv - Complete column mapping with semantic concepts
2. GRID_REFERENCE_LOOKUP.csv - Quick lookup table (grid ref → concept)
3. TRANSFORMATION_RULES_MANIFEST.csv - Reconciliation and validation rules

Grid Reference System: Excel-style (A-1, B-2, ... Z-26, AA-27, AB-28, ...)

Author: Maritime Cargo Classification Project
Date: 2026-01-21
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(r"G:\My Drive\LLM\project_manifest")
OUTPUT_DIR = PROJECT_ROOT / "03_DOCUMENTATION" / "03.05_data_dictionaries"

# Data source directories to scan
DATA_SOURCES = [
    PROJECT_ROOT / "00_DATA" / "00.02_PREPROCESSED",
    PROJECT_ROOT / "00_DATA" / "00.03_MATCHED",
    PROJECT_ROOT / "00_DATA" / "00.04_FINAL",
    PROJECT_ROOT / "01_DICTIONARIES" / "01.01_cargo_classification",
    PROJECT_ROOT / "01_DICTIONARIES" / "01.02_ports",
    PROJECT_ROOT / "01_DICTIONARIES" / "01.03_vessels",
    PROJECT_ROOT / "01_DICTIONARIES" / "01.04_carriers",
    PROJECT_ROOT / "01_DICTIONARIES" / "01.05_hs_codes",
]

# ============================================================================
# SEMANTIC CONCEPT DEFINITIONS
# ============================================================================

SEMANTIC_CONCEPTS = {
    # VESSEL CONCEPTS
    'VESSEL_001': {
        'name': 'Vessel Name',
        'category': 'VESSEL',
        'keywords': ['vessel', 'ship', 'vslnme', 'vessel_name', 'vessel name'],
        'validation': 'not_null, length < 100, alphanumeric + spaces',
    },
    'VESSEL_002': {
        'name': 'IMO Number',
        'category': 'VESSEL',
        'keywords': ['imo', 'vessel imo', 'vessel_imo'],
        'validation': '7 digits, numeric',
    },
    'VESSEL_003': {
        'name': 'Vessel Type',
        'category': 'VESSEL',
        'keywords': ['type', 'vessel_type', 'vessel type', 'icst', 'rig_desc'],
        'validation': 'categorical, not_null',
    },
    'VESSEL_004': {
        'name': 'Deadweight Tonnage (DWT)',
        'category': 'VESSEL',
        'keywords': ['dwt', 'vessel_dwt', 'deadweight'],
        'validation': 'numeric, > 0',
    },
    'VESSEL_005': {
        'name': 'Flag Country',
        'category': 'VESSEL',
        'keywords': ['flag', 'flag_ctry', 'flag_country', 'flag country'],
        'validation': '2-letter ISO code or full name',
    },
    'VESSEL_006': {
        'name': 'Length Overall (LOA)',
        'category': 'VESSEL',
        'keywords': ['loa', 'length', 'vessel_loa'],
        'validation': 'numeric, > 0',
    },
    'VESSEL_007': {
        'name': 'Beam',
        'category': 'VESSEL',
        'keywords': ['beam', 'width', 'vessel_beam'],
        'validation': 'numeric, > 0',
    },
    'VESSEL_008': {
        'name': 'Draft',
        'category': 'VESSEL',
        'keywords': ['draft', 'draught', 'vessel_draft'],
        'validation': 'numeric, > 0',
    },
    'VESSEL_009': {
        'name': 'Gross Tonnage (GT)',
        'category': 'VESSEL',
        'keywords': ['gt', 'gross', 'gross_tonnage'],
        'validation': 'numeric, > 0',
    },
    'VESSEL_010': {
        'name': 'Net Register Tonnage (NRT)',
        'category': 'VESSEL',
        'keywords': ['nrt', 'net', 'net_tonnage'],
        'validation': 'numeric, > 0',
    },

    # PORT CONCEPTS
    'PORT_001': {
        'name': 'Port Name',
        'category': 'PORT',
        'keywords': ['port', 'port_name', 'port name', 'arrival_port', 'discharge_port', 'us_port'],
        'validation': 'not_null, exists in port dictionary',
    },
    'PORT_002': {
        'name': 'Port Code',
        'category': 'PORT',
        'keywords': ['port_code', 'port code', 'ace_code', 'usace_code', 'unloc'],
        'validation': '2-5 alphanumeric characters',
    },
    'PORT_003': {
        'name': 'Port Region',
        'category': 'PORT',
        'keywords': ['region', 'port_region', 'port region'],
        'validation': 'categorical',
    },
    'PORT_004': {
        'name': 'Port Coast',
        'category': 'PORT',
        'keywords': ['coast', 'port_coast', 'seaboard'],
        'validation': 'categorical (Atlantic, Pacific, Gulf, Great Lakes)',
    },
    'PORT_005': {
        'name': 'Port Country',
        'category': 'PORT',
        'keywords': ['country', 'port_country', 'country_code'],
        'validation': '2-letter ISO code or full name',
    },

    # PARTY CONCEPTS
    'PARTY_001': {
        'name': 'Shipper',
        'category': 'PARTY',
        'keywords': ['shipper', 'exporter', 'seller', 'shipper_name'],
        'validation': 'not_null, length < 200',
    },
    'PARTY_002': {
        'name': 'Consignee',
        'category': 'PARTY',
        'keywords': ['consignee', 'importer', 'buyer', 'consignee_name'],
        'validation': 'not_null, length < 200',
    },
    'PARTY_003': {
        'name': 'Carrier',
        'category': 'PARTY',
        'keywords': ['carrier', 'scac', 'shipping_line', 'carrier_name'],
        'validation': 'not_null, SCAC format (4 letters)',
    },
    'PARTY_004': {
        'name': 'Notify Party',
        'category': 'PARTY',
        'keywords': ['notify', 'notify_party', 'contact'],
        'validation': 'optional, length < 200',
    },

    # CARGO CONCEPTS
    'CARGO_001': {
        'name': 'HS Code',
        'category': 'CARGO',
        'keywords': ['hs', 'hs2', 'hs4', 'hs6', 'hs_code', 'tariff'],
        'validation': 'numeric, 2/4/6 digits, exists in HS lookup',
    },
    'CARGO_002': {
        'name': 'Goods Description',
        'category': 'CARGO',
        'keywords': ['goods', 'description', 'product', 'cargo_description', 'goods_shipped'],
        'validation': 'not_null, length < 500',
    },
    'CARGO_003': {
        'name': 'Weight (Metric Tons)',
        'category': 'CARGO',
        'keywords': ['tons', 'tonnes', 'weight_tons', 'metric_tons'],
        'validation': 'numeric, > 0, < 1000000',
    },
    'CARGO_004': {
        'name': 'Weight (Kilograms)',
        'category': 'CARGO',
        'keywords': ['kilos', 'kg', 'weight_kg', 'kilograms'],
        'validation': 'numeric, > 0',
    },
    'CARGO_005': {
        'name': 'Weight (Original Format)',
        'category': 'CARGO',
        'keywords': ['weight', 'mass', 'qty'],
        'validation': 'numeric, > 0',
    },
    'CARGO_006': {
        'name': 'Value (USD)',
        'category': 'CARGO',
        'keywords': ['value', 'price', 'fob', 'cost'],
        'validation': 'numeric, >= 0',
    },
    'CARGO_007': {
        'name': 'Quantity',
        'category': 'CARGO',
        'keywords': ['quantity', 'qty', 'count', 'pieces'],
        'validation': 'integer, > 0',
    },
    'CARGO_008': {
        'name': 'Cargo Group',
        'category': 'CARGO',
        'keywords': ['group', 'cargo_group', 'classification_group'],
        'validation': 'categorical, top-level taxonomy',
    },
    'CARGO_009': {
        'name': 'Cargo Commodity',
        'category': 'CARGO',
        'keywords': ['commodity', 'cargo_commodity'],
        'validation': 'categorical, 2nd-level taxonomy',
    },
    'CARGO_010': {
        'name': 'Cargo Type',
        'category': 'CARGO',
        'keywords': ['cargo', 'cargo_type', 'cargo_detail'],
        'validation': 'categorical, 3rd-level taxonomy',
    },
    'CARGO_011': {
        'name': 'Cargo Detail',
        'category': 'CARGO',
        'keywords': ['cargo_detail', 'cargo detail', 'specific_grade'],
        'validation': 'categorical, 4th-level taxonomy',
    },

    # DOCUMENT CONCEPTS
    'DOCUMENT_001': {
        'name': 'Bill of Lading',
        'category': 'DOCUMENT',
        'keywords': ['bol', 'bill of lading', 'master_bol', 'manifest'],
        'validation': 'not_null, alphanumeric',
    },
    'DOCUMENT_002': {
        'name': 'Voyage ID',
        'category': 'DOCUMENT',
        'keywords': ['voyage', 'voyage_id', 'trip', 'voyage_number'],
        'validation': 'alphanumeric',
    },
    'DOCUMENT_003': {
        'name': 'Arrival Date',
        'category': 'DOCUMENT',
        'keywords': ['arrival', 'arrival_date', 'import_date', 'discharge_date'],
        'validation': 'date format YYYY-MM-DD',
    },
    'DOCUMENT_004': {
        'name': 'Clearance Date',
        'category': 'DOCUMENT',
        'keywords': ['clearance', 'clearance_date', 'departure_date'],
        'validation': 'date format YYYY-MM-DD',
    },
    'DOCUMENT_005': {
        'name': 'Shipment Date',
        'category': 'DOCUMENT',
        'keywords': ['shipment', 'shipment_date', 'loading_date'],
        'validation': 'date format YYYY-MM-DD',
    },

    # MEASUREMENT CONCEPTS
    'MEASUREMENT_001': {
        'name': 'Measurement Unit',
        'category': 'MEASUREMENT',
        'keywords': ['unit', 'measurement_unit', 'uom', 'measure'],
        'validation': 'categorical (TEU, CBM, CF, KGM, TNE)',
    },
    'MEASUREMENT_002': {
        'name': 'Package Type',
        'category': 'MEASUREMENT',
        'keywords': ['package', 'pckg', 'container_type', 'packaging'],
        'validation': 'categorical (LBK, DBK, BOX, etc.)',
    },
    'MEASUREMENT_003': {
        'name': 'Is Containerized',
        'category': 'MEASUREMENT',
        'keywords': ['containerized', 'is_containerized', 'container_flag'],
        'validation': 'boolean (Y/N, TRUE/FALSE)',
    },
}

# ============================================================================
# GRID REFERENCE FUNCTIONS
# ============================================================================

def number_to_column_letter(n):
    """Convert column number (1-based) to Excel-style letter (A, B, ... Z, AA, AB, ...)"""
    result = ""
    while n > 0:
        n -= 1
        result = chr(n % 26 + ord('A')) + result
        n //= 26
    return result

def create_grid_reference(column_number):
    """Create grid reference like 'A-1', 'B-2', 'AA-27', etc."""
    letter = number_to_column_letter(column_number)
    return f"{letter}-{column_number}"

# ============================================================================
# SEMANTIC MATCHING
# ============================================================================

def match_concept(column_name):
    """Match column name to semantic concept using keyword matching"""
    column_lower = column_name.lower().replace('_', ' ')

    # Track best match
    best_match = None
    best_score = 0

    for concept_id, concept_info in SEMANTIC_CONCEPTS.items():
        keywords = concept_info['keywords']

        # Check for exact keyword match
        for keyword in keywords:
            if keyword in column_lower:
                # Longer keywords score higher (more specific)
                score = len(keyword)
                if score > best_score:
                    best_score = score
                    best_match = concept_id

    return best_match

# ============================================================================
# FILE SCANNING
# ============================================================================

def get_column_metadata(df, file_path, source_name):
    """Extract metadata for all columns in a dataframe"""
    metadata = []

    for idx, col in enumerate(df.columns, start=1):
        # Grid reference
        grid_ref = create_grid_reference(idx)
        column_letter = number_to_column_letter(idx)

        # Data type detection
        dtype = str(df[col].dtype)
        if 'int' in dtype or 'float' in dtype:
            data_type = 'numeric'
        elif 'datetime' in dtype:
            data_type = 'date'
        elif 'bool' in dtype:
            data_type = 'boolean'
        else:
            data_type = 'text'

        # Sample values (first 3 non-null)
        samples = df[col].dropna().head(3).tolist()
        sample_str = ', '.join([str(s)[:50] for s in samples])

        # Null percentage
        null_pct = (df[col].isna().sum() / len(df)) * 100

        # Unique count
        unique_count = df[col].nunique()

        # Match to semantic concept
        concept_id = match_concept(col)

        metadata.append({
            'source_file': source_name,
            'file_path': str(file_path),
            'grid_reference': grid_ref,
            'column_letter': column_letter,
            'column_number': idx,
            'column_name': col,
            'data_type': data_type,
            'null_percentage': round(null_pct, 2),
            'unique_count': unique_count,
            'sample_values': sample_str,
            'concept_id': concept_id,
            'concept_name': SEMANTIC_CONCEPTS[concept_id]['name'] if concept_id else 'UNMAPPED',
            'semantic_category': SEMANTIC_CONCEPTS[concept_id]['category'] if concept_id else 'UNMAPPED',
            'validation_rule': SEMANTIC_CONCEPTS[concept_id]['validation'] if concept_id else '',
            'total_rows': len(df),
            'total_columns': len(df.columns),
        })

    return metadata

def scan_csv_file(file_path):
    """Scan a single CSV file and extract metadata"""
    try:
        print(f"  Scanning: {file_path.name}")
        df = pd.read_csv(file_path, nrows=1000)  # Sample first 1000 rows for speed
        source_name = file_path.stem
        return get_column_metadata(df, file_path, source_name)
    except Exception as e:
        print(f"  ERROR reading {file_path.name}: {e}")
        return []

def scan_all_sources():
    """Scan all data sources and build metadata catalog"""
    all_metadata = []

    print("\n" + "="*80)
    print("SCANNING DATA SOURCES")
    print("="*80)

    for source_dir in DATA_SOURCES:
        if not source_dir.exists():
            print(f"\nSkipping (not found): {source_dir}")
            continue

        print(f"\nScanning directory: {source_dir}")

        # Find all CSV files
        csv_files = list(source_dir.glob("*.csv"))
        print(f"Found {len(csv_files)} CSV files")

        for csv_file in csv_files:
            metadata = scan_csv_file(csv_file)
            all_metadata.extend(metadata)

    return pd.DataFrame(all_metadata)

# ============================================================================
# TRANSFORMATION RULES
# ============================================================================

def build_transformation_rules(metadata_df):
    """Build transformation rules for concepts appearing in multiple sources"""

    rules = []

    # Group by concept
    for concept_id in metadata_df['concept_id'].dropna().unique():
        concept_data = metadata_df[metadata_df['concept_id'] == concept_id]

        if len(concept_data) == 0:
            continue

        concept_name = concept_data.iloc[0]['concept_name']
        category = concept_data.iloc[0]['semantic_category']

        # Build grid reference list
        grid_refs = []
        for _, row in concept_data.iterrows():
            grid_refs.append(f"{row['source_file']}:{row['grid_reference']}")

        # Reconciliation logic based on concept type
        if concept_id == 'VESSEL_001':
            reconcile_logic = "Use Ships_Register as authority; match on IMO first, then fuzzy name match"
        elif concept_id.startswith('CARGO_001'):
            reconcile_logic = "Use HS6 if available, else HS4, else HS2 (most granular wins)"
        elif concept_id == 'CARGO_003' or concept_id == 'CARGO_004':
            reconcile_logic = "Convert all to metric tons: tons = kilos / 1000"
        elif concept_id == 'PORT_001':
            reconcile_logic = "Use us_port_dictionary Port_Consolidated as standard; map via Port_Code"
        elif concept_id == 'PARTY_003':
            reconcile_logic = "Extract 4-letter SCAC code; map to full name via carrier_scac_mappings"
        else:
            if len(concept_data) == 1:
                reconcile_logic = "Single source - use as-is"
            else:
                reconcile_logic = "If all sources match → use as-is; if 2+ match → majority value; else flag as error"

        # Validation checks
        validation = concept_data.iloc[0]['validation_rule']

        rules.append({
            'concept_id': concept_id,
            'concept_name': concept_name,
            'semantic_category': category,
            'source_count': len(concept_data),
            'source_grid_references': ', '.join(grid_refs),
            'target_column_name': concept_name.replace(' ', '_'),
            'target_data_type': concept_data.iloc[0]['data_type'],
            'reconciliation_logic': reconcile_logic,
            'validation_checks': validation,
            'error_handling': 'Flag as ERROR and log to validation report',
            'notes': f"Appears in {len(concept_data)} source(s)",
        })

    return pd.DataFrame(rules)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""

    print("\n" + "="*80)
    print("MASTER DATA DICTIONARY BUILDER v1.0.0")
    print("="*80)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # STEP 1: Scan all sources
    print("\n[STEP 1] Scanning all data sources...")
    metadata_df = scan_all_sources()

    print(f"\nTotal columns scanned: {len(metadata_df)}")
    print(f"Unique sources: {metadata_df['source_file'].nunique()}")
    print(f"Concepts mapped: {metadata_df['concept_id'].nunique()}")
    print(f"Unmapped columns: {len(metadata_df[metadata_df['concept_id'].isna()])}")

    # STEP 2: Build transformation rules
    print("\n[STEP 2] Building transformation rules...")
    rules_df = build_transformation_rules(metadata_df)
    print(f"Transformation rules generated: {len(rules_df)}")

    # STEP 3: Build grid reference lookup
    print("\n[STEP 3] Building grid reference lookup...")
    lookup_df = metadata_df[[
        'grid_reference', 'source_file', 'column_name', 'concept_id',
        'concept_name', 'data_type', 'sample_values'
    ]].copy()
    lookup_df.rename(columns={'sample_values': 'latest_sample_value'}, inplace=True)

    # STEP 4: Generate outputs
    print("\n[STEP 4] Generating output files...")

    timestamp = datetime.now().strftime('%Y%m%d_%H%M')

    # Output 1: Master Data Dictionary
    master_file = OUTPUT_DIR / f"MASTER_DATA_DICTIONARY_v1.0.0_{timestamp}.csv"
    metadata_df['created_date'] = datetime.now().strftime('%Y-%m-%d')
    metadata_df['last_updated'] = datetime.now().strftime('%Y-%m-%d')

    # Add transformation logic and reconciliation rule from rules
    metadata_df = metadata_df.merge(
        rules_df[['concept_id', 'reconciliation_logic']],
        on='concept_id',
        how='left'
    )
    metadata_df['reconciliation_logic'] = metadata_df['reconciliation_logic'].fillna('N/A')

    metadata_df.to_csv(master_file, index=False)
    print(f"[OK] Saved: {master_file.name}")

    # Output 2: Grid Reference Lookup
    lookup_file = OUTPUT_DIR / f"GRID_REFERENCE_LOOKUP_v1.0.0_{timestamp}.csv"
    lookup_df.to_csv(lookup_file, index=False)
    print(f"[OK] Saved: {lookup_file.name}")

    # Output 3: Transformation Rules Manifest
    rules_file = OUTPUT_DIR / f"TRANSFORMATION_RULES_MANIFEST_v1.0.0_{timestamp}.csv"
    rules_df.to_csv(rules_file, index=False)
    print(f"[OK] Saved: {rules_file.name}")

    # STEP 5: Generate summary statistics
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)

    print(f"\nTotal Columns Analyzed: {len(metadata_df)}")
    print(f"Total Sources: {metadata_df['source_file'].nunique()}")
    print(f"Total Rows Across All Sources: {metadata_df['total_rows'].sum():,}")

    print(f"\nSemantic Concepts:")
    for category in metadata_df['semantic_category'].unique():
        if pd.isna(category):
            continue
        count = len(metadata_df[metadata_df['semantic_category'] == category])
        print(f"  {category}: {count} columns")

    print(f"\nUnmapped Columns: {len(metadata_df[metadata_df['concept_id'].isna()])}")
    if len(metadata_df[metadata_df['concept_id'].isna()]) > 0:
        print("\nTop 10 Unmapped Column Names:")
        unmapped = metadata_df[metadata_df['concept_id'].isna()]['column_name'].value_counts().head(10)
        for col, count in unmapped.items():
            print(f"  {col}: {count} occurrence(s)")

    print(f"\nTop 10 Most Common Concepts:")
    concept_counts = metadata_df['concept_name'].value_counts().head(10)
    for concept, count in concept_counts.items():
        print(f"  {concept}: {count} column(s)")

    print("\n" + "="*80)
    print("MASTER DATA DICTIONARY BUILD COMPLETE")
    print("="*80)
    print(f"\nOutput files saved to:")
    print(f"  {OUTPUT_DIR}")
    print(f"\nFiles generated:")
    print(f"  1. {master_file.name}")
    print(f"  2. {lookup_file.name}")
    print(f"  3. {rules_file.name}")
    print("\n")

if __name__ == "__main__":
    main()
