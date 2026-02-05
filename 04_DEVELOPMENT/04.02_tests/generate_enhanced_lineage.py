"""
Enhanced Column Lineage with Transformation Tracking
Shows: Origin, Renames, Derivations, Matches, References
"""
import pandas as pd
from pathlib import Path

BASE = Path(r"G:\My Drive\LLM\project_manifest")

# Read the basic lineage table
lineage = pd.read_csv(BASE / "04_DEVELOPMENT" / "04.02_tests" / "COLUMN_LINEAGE_TABLE.csv")

print("="*120)
print("ENHANCED LINEAGE TABLE - Adding Transformation Metadata")
print("="*120)

# Define transformation metadata for key columns
transformations = {
    # DATE TRANSFORMATIONS
    'Arrival_Date': {
        'origin': 'USACE Entrance (ECDATE)',
        'transformation_type': 'Renamed + Date Parsed',
        'derived_from': 'ECDATE (mmydd integer)',
        'formula': 'parse_usace_date(ECDATE) -> YYYY-MM-DD',
        'matches_to': 'Panjiva Imports: Arrival Date',
        'lifecycle': 'STAGE 1 -> STAGE 9 (Final)',
        'notes': 'Raw ECDATE (12316) renamed to Arrival_Date, then parsed to 2023-12-16'
    },
    'Clearance_Date': {
        'origin': 'USACE Clearance (ECDATE)',
        'transformation_type': 'Renamed + Date Parsed',
        'derived_from': 'ECDATE (mmydd integer)',
        'formula': 'parse_usace_date(ECDATE) -> YYYY-MM-DD',
        'matches_to': 'Panjiva Exports: Shipment Date',
        'lifecycle': 'STAGE 2 -> STAGE 9 (Final)',
        'notes': 'Raw ECDATE (12306) renamed to Clearance_Date, then parsed to 2023-12-06'
    },

    # IMO TRANSFORMATIONS
    'IMO': {
        'origin': 'USACE Entrance/Clearance + Panjiva Imports',
        'transformation_type': 'Original (with type conversion)',
        'derived_from': 'Original column',
        'formula': 'float -> int -> string for matching',
        'matches_to': 'Used to match USACE <-> Panjiva Imports (NOT in Exports!)',
        'lifecycle': 'STAGE 1 -> STAGE 9 (Final)',
        'notes': 'Primary matching key. CRITICAL: Panjiva Exports has NO IMO column!'
    },

    # VESSEL NAME TRANSFORMATIONS
    'Vessel': {
        'origin': 'USACE + Panjiva (all sources)',
        'transformation_type': 'Original',
        'derived_from': 'VESSNAME (USACE) or Vessel (Panjiva)',
        'formula': 'str.upper().strip() for matching',
        'matches_to': 'Fallback matching key when IMO not available',
        'lifecycle': 'STAGE 1 -> STAGE 8 (then becomes Vessel_Name in STAGE 9)',
        'notes': 'Renamed to Vessel_Name in Port Call Master'
    },
    'Vessel_Name': {
        'origin': 'Port Call Master',
        'transformation_type': 'Renamed from Vessel',
        'derived_from': 'Vessel (USACE Entrance or Clearance)',
        'formula': 'Direct copy',
        'matches_to': 'N/A',
        'lifecycle': 'STAGE 9 only',
        'notes': 'Final column name in Port Call Master'
    },

    # PORT TRANSFORMATIONS
    'PORT': {
        'origin': 'USACE Entrance/Clearance',
        'transformation_type': 'Original',
        'derived_from': 'Original USACE port code',
        'formula': 'Numeric code (e.g., 2160, 3926)',
        'matches_to': 'NO MATCH - Panjiva uses text names not codes',
        'lifecycle': 'STAGE 1 -> STAGE 8 (dropped in STAGE 9)',
        'notes': 'NOT used for matching due to code vs name mismatch'
    },
    'Entrance_Port': {
        'origin': 'Port Call Master',
        'transformation_type': 'Renamed from PORT',
        'derived_from': 'PORT (USACE Entrance)',
        'formula': 'Direct copy of numeric code',
        'matches_to': 'N/A',
        'lifecycle': 'STAGE 9 only',
        'notes': 'Preserves USACE numeric port code in final output'
    },
    'Clearance_Port': {
        'origin': 'Port Call Master',
        'transformation_type': 'Renamed from PORT',
        'derived_from': 'PORT (USACE Clearance)',
        'formula': 'Direct copy of numeric code',
        'matches_to': 'N/A',
        'lifecycle': 'STAGE 9 only',
        'notes': 'Preserves USACE numeric port code in final output'
    },

    # NEW FLAGS ADDED BY MATCHING
    'Has_Import_Manifest': {
        'origin': 'STAGE 7: Entrance + Import Matching',
        'transformation_type': 'Calculated Boolean Flag',
        'derived_from': 'Result of IMO/Vessel/Date matching',
        'formula': 'TRUE if matched to Panjiva Imports, FALSE otherwise',
        'matches_to': 'Indicates match to Panjiva Imports dataset',
        'lifecycle': 'STAGE 7 -> STAGE 9 (Final)',
        'notes': 'NEW COLUMN - Added by simplified pipeline v2.0.0'
    },
    'Import_VOY_RECID': {
        'origin': 'STAGE 7: Entrance + Import Matching',
        'transformation_type': 'Foreign Key',
        'derived_from': 'MD5 hash of Vessel + Date + Port from Panjiva Imports',
        'formula': 'md5(Vessel|Arrival_Date|Port).hexdigest()[:16]',
        'matches_to': 'Points back to Panjiva Imports: VOY_RECID',
        'references_back_to': 'Panjiva Imports manifest (same VOY_RECID)',
        'lifecycle': 'STAGE 7 -> STAGE 9 (Final)',
        'notes': 'NEW COLUMN - Foreign key for joining back to import cargo data'
    },
    'Has_Export_Manifest': {
        'origin': 'STAGE 8: Clearance + Export Matching',
        'transformation_type': 'Calculated Boolean Flag',
        'derived_from': 'Result of Vessel/Date matching (NO IMO in exports)',
        'formula': 'TRUE if matched to Panjiva Exports, FALSE otherwise',
        'matches_to': 'Indicates match to Panjiva Exports dataset',
        'lifecycle': 'STAGE 8 -> STAGE 9 (Final)',
        'notes': 'NEW COLUMN - Added by simplified pipeline v2.0.0'
    },
    'Export_VOY_RECID': {
        'origin': 'STAGE 8: Clearance + Export Matching',
        'transformation_type': 'Foreign Key',
        'derived_from': 'MD5 hash of Vessel + Date + Port from Panjiva Exports',
        'formula': 'md5(Vessel|Shipment_Date|Port).hexdigest()[:16]',
        'matches_to': 'Points back to Panjiva Exports: VOY_RECID',
        'references_back_to': 'Panjiva Exports manifest (same VOY_RECID)',
        'lifecycle': 'STAGE 8 -> STAGE 9 (Final)',
        'notes': 'NEW COLUMN - Foreign key for joining back to export cargo data'
    },

    # PORT CALL MASTER COLUMNS
    'PORTCALL_ID': {
        'origin': 'STAGE 9: Port Call Master',
        'transformation_type': 'Generated Primary Key',
        'derived_from': 'Sequential ID',
        'formula': 'PC_{index:06d} or PC_CLR_{index:06d}',
        'matches_to': 'N/A',
        'lifecycle': 'STAGE 9 only',
        'notes': 'NEW COLUMN - Unique identifier for each port call'
    },
    'Record_Type': {
        'origin': 'STAGE 9: Port Call Master',
        'transformation_type': 'Calculated Enum',
        'derived_from': 'Whether entrance/clearance/both matched',
        'formula': 'BOTH | ENTRANCE_ONLY | CLEARANCE_ONLY',
        'matches_to': 'N/A',
        'lifecycle': 'STAGE 9 only',
        'notes': 'NEW COLUMN - Indicates completeness of port call record'
    },
    'Port_Stay_Days': {
        'origin': 'STAGE 9: Port Call Master',
        'transformation_type': 'Calculated Duration',
        'derived_from': 'Clearance_Date - Arrival_Date',
        'formula': '(Clearance_Date - Arrival_Date).days',
        'matches_to': 'N/A',
        'lifecycle': 'STAGE 9 only',
        'notes': 'NEW COLUMN - Days vessel stayed in port'
    },

    # PANJIVA SPECIFIC COLUMNS
    'Arrival Date': {
        'origin': 'Panjiva Imports',
        'transformation_type': 'Original',
        'derived_from': 'Original Panjiva column',
        'formula': 'Already YYYY-MM-DD format',
        'matches_to': 'USACE Entrance: Arrival_Date (±3 days)',
        'lifecycle': 'STAGE 3 only (not carried forward)',
        'notes': 'Used for matching but not in final output'
    },
    'Shipment Date': {
        'origin': 'Panjiva Exports',
        'transformation_type': 'Original',
        'derived_from': 'Original Panjiva column',
        'formula': 'Already YYYY-MM-DD format',
        'matches_to': 'USACE Clearance: Clearance_Date (±3 days)',
        'lifecycle': 'STAGE 4 only (not carried forward)',
        'notes': 'Used for matching but not in final output'
    },

    # INTERMEDIATE PARSING COLUMNS
    'Arrival_Date_Parsed': {
        'origin': 'STAGE 7: Matching Process',
        'transformation_type': 'Temporary Parsed Column',
        'derived_from': 'Arrival_Date',
        'formula': 'pd.to_datetime(Arrival_Date)',
        'matches_to': 'Used internally for date comparison',
        'lifecycle': 'STAGE 7 only (dropped after matching)',
        'notes': 'TEMPORARY - Not in final output'
    },
    'Clearance_Date_Parsed': {
        'origin': 'STAGE 8: Matching Process',
        'transformation_type': 'Temporary Parsed Column',
        'derived_from': 'Clearance_Date',
        'formula': 'pd.to_datetime(Clearance_Date)',
        'matches_to': 'Used internally for date comparison',
        'lifecycle': 'STAGE 8 only (dropped after matching)',
        'notes': 'TEMPORARY - Not in final output'
    }
}

# Add metadata columns to lineage
enhanced = lineage.copy()
enhanced['Column_Origin'] = enhanced['Column_Name'].map(lambda x: transformations.get(x, {}).get('origin', 'Original source column'))
enhanced['Transformation_Type'] = enhanced['Column_Name'].map(lambda x: transformations.get(x, {}).get('transformation_type', 'Original'))
enhanced['Derived_From'] = enhanced['Column_Name'].map(lambda x: transformations.get(x, {}).get('derived_from', 'N/A'))
enhanced['Formula'] = enhanced['Column_Name'].map(lambda x: transformations.get(x, {}).get('formula', 'N/A'))
enhanced['Matches_To'] = enhanced['Column_Name'].map(lambda x: transformations.get(x, {}).get('matches_to', 'N/A'))
enhanced['References_Back_To'] = enhanced['Column_Name'].map(lambda x: transformations.get(x, {}).get('references_back_to', 'N/A'))
enhanced['Lifecycle'] = enhanced['Column_Name'].map(lambda x: transformations.get(x, {}).get('lifecycle', 'See Stage column'))
enhanced['Notes'] = enhanced['Column_Name'].map(lambda x: transformations.get(x, {}).get('notes', ''))

# Reorder columns for better readability
enhanced = enhanced[[
    'Stage',
    'Col_Num',
    'Column_Name',
    'Sample_Value',
    'Column_Origin',
    'Transformation_Type',
    'Derived_From',
    'Formula',
    'Matches_To',
    'References_Back_To',
    'Lifecycle',
    'Notes'
]]

# Save enhanced version
output_file = BASE / "04_DEVELOPMENT" / "04.02_tests" / "COLUMN_LINEAGE_ENHANCED.csv"
enhanced.to_csv(output_file, index=False)

print(f"\n[OK] Enhanced lineage saved to: {output_file.name}")
print(f"    Total rows: {len(enhanced):,}")
print(f"    Total columns: {len(enhanced.columns)}")

# Print examples of key transformations
print("\n" + "="*120)
print("EXAMPLE TRANSFORMATIONS")
print("="*120)

examples = [
    'Arrival_Date',
    'IMO',
    'Has_Import_Manifest',
    'Import_VOY_RECID',
    'Vessel_Name',
    'PORTCALL_ID'
]

for col in examples:
    col_data = enhanced[enhanced['Column_Name'] == col]
    if len(col_data) > 0:
        first_row = col_data.iloc[0]
        print(f"\n{col}:")
        print(f"  Origin: {first_row['Column_Origin']}")
        print(f"  Type: {first_row['Transformation_Type']}")
        print(f"  Derived From: {first_row['Derived_From']}")
        print(f"  Formula: {first_row['Formula']}")
        print(f"  Matches To: {first_row['Matches_To']}")
        if first_row['References_Back_To'] != 'N/A':
            print(f"  References: {first_row['References_Back_To']}")
        print(f"  Lifecycle: {first_row['Lifecycle']}")
        if first_row['Notes']:
            print(f"  Notes: {first_row['Notes']}")

print("\n" + "="*120)
print("NEW COLUMNS ADDED BY SIMPLIFIED PIPELINE (v2.0.0)")
print("="*120)

new_cols = enhanced[enhanced['Transformation_Type'].str.contains('Foreign Key|Boolean Flag|Generated|Calculated', na=False)]
new_cols_unique = new_cols.drop_duplicates('Column_Name')

for _, row in new_cols_unique.iterrows():
    print(f"\n+ {row['Column_Name']}")
    print(f"    Type: {row['Transformation_Type']}")
    print(f"    Added: {row['Stage']}")
    print(f"    Purpose: {row['Notes']}")

print("\n" + "="*120)
print("COMPLETE")
print("="*120)
print(f"\nOutput file: {output_file}")
print("\nThis enhanced table now shows:")
print("  - Where each column originates")
print("  - What transformations were applied")
print("  - What it was derived from")
print("  - What it matches to in other datasets")
print("  - What it references (foreign keys)")
print("  - Its lifecycle through the pipeline")
