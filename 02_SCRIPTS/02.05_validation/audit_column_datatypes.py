"""
Enhanced Column Lineage Audit with Data Type Analysis
Version: 1.0.0
Created: 2026-01-21

Provides detailed data type tracing and sample value analysis
"""

import pandas as pd
from pathlib import Path
import numpy as np

# ============================
# FILE PATHS
# ============================
BASE_DIR = Path(r"G:\My Drive\LLM\project_manifest")

RAW_FILE = BASE_DIR / "00_raw_data" / "00_99_user_notes_raw_data" / "panjiva_imports" / "panjiva_manifest_2023.csv"
PREPROCESSED_FILE = BASE_DIR / "00_DATA" / "00.02_PREPROCESSED" / "panjiva_imports_2023_AUTHORITATIVE_v1.0.0.csv"
CLASSIFIED_FILE = BASE_DIR / "03_DOCUMENTATION" / "03.04_summaries" / "sample_test_15k" / "sample_15k_classified_v3.6.0.csv"

OUTPUT_DIR = BASE_DIR / "03_DOCUMENTATION" / "03.05_data_dictionaries"
OUTPUT_FILE = OUTPUT_DIR / "IMPORT_COLUMN_DATATYPE_AUDIT.md"

# ============================
# LOAD DATA
# ============================
print("="*80)
print("ENHANCED COLUMN AUDIT - DATA TYPE ANALYSIS")
print("="*80)
print()

print("Loading files with data type detection...")
df_raw = pd.read_csv(RAW_FILE, nrows=1000)  # Load more for better type detection
df_preprocessed = pd.read_csv(PREPROCESSED_FILE, nrows=1000)
df_classified = pd.read_csv(CLASSIFIED_FILE, nrows=1000)

print(f"  RAW: {len(df_raw)} records, {len(df_raw.columns)} columns")
print(f"  PREPROCESSED: {len(df_preprocessed)} records, {len(df_preprocessed.columns)} columns")
print(f"  CLASSIFIED: {len(df_classified)} records, {len(df_classified.columns)} columns")
print()

# ============================
# HELPER FUNCTIONS
# ============================

def detect_data_characteristics(series):
    """Analyze a pandas series and return characteristics"""
    total = len(series)
    null_count = series.isna().sum()
    null_pct = (null_count / total * 100) if total > 0 else 0
    unique_count = series.nunique()

    # Detect data type
    dtype = str(series.dtype)

    # Get sample non-null values
    non_null = series.dropna()
    samples = []
    if len(non_null) > 0:
        samples = non_null.head(3).astype(str).tolist()

    # Detect format patterns
    format_notes = []
    if len(non_null) > 0:
        first_val = str(non_null.iloc[0])

        # Check for date patterns
        if 'date' in series.name.lower() or any(char in first_val for char in ['-', '/']):
            if len(first_val) >= 8 and first_val.count('-') >= 2:
                format_notes.append("Date format: YYYY-MM-DD")

        # Check for numeric patterns
        if dtype in ['int64', 'float64']:
            if 'weight' in series.name.lower() or 'ton' in series.name.lower():
                format_notes.append("Numeric: Weight/tonnage")
            elif 'value' in series.name.lower():
                format_notes.append("Numeric: Monetary value")

        # Check for code patterns
        if 'code' in series.name.lower() or 'hs' in series.name.lower():
            format_notes.append("Code/classification")

    return {
        'dtype': dtype,
        'null_pct': f"{null_pct:.1f}%",
        'unique_count': unique_count,
        'samples': samples,
        'format_notes': format_notes
    }

# ============================
# ANALYZE CORE FIELDS
# ============================

print("Analyzing core fields that exist across all stages...")
print()

# Define key fields to analyze
core_fields = [
    # Identity fields
    ('Bill of Lading Number', 'Bill of Lading Number', 'Bill of Lading Number'),
    ('Arrival Date', 'Arrival Date', 'Arrival Date'),

    # Party fields
    ('Consignee', 'Consignee', 'Consignee'),
    ('Shipper', 'Shipper', 'Shipper'),
    ('Carrier', 'Carrier', 'Carrier'),

    # Location fields
    ('Port of Unlading', 'Port of Discharge (D)', 'Port of Discharge (D)'),
    ('Port of Lading', 'Port of Loading (F)', 'Port of Loading (F)'),

    # Vessel fields
    ('Vessel', 'Vessel', 'Vessel'),
    ('Vessel IMO', 'IMO', 'IMO'),

    # Cargo fields
    ('Goods Shipped', 'Goods Shipped', 'Goods Shipped'),
    ('HS Code', 'HS Code Desc.', 'HS Code Desc.'),

    # Measurement fields
    ('Weight (kg)', 'Kilos', 'Kilos'),
    ('Weight (t)', 'Tons', 'Tons'),
    ('Value of Goods (USD)', 'Value', 'Value'),
    ('Measurement', 'Measurement', 'Measurement'),
]

# Fields added during preprocessing
preprocessing_fields = [
    ('Port_Consolidated', 'Port_Consolidated'),
    ('Port_Code', 'Port_Code'),
    ('HS2', 'HS2'),
    ('HS4', 'HS4'),
    ('HS6', 'HS6'),
    ('Pckg', 'Pckg'),
    ('RAW_REC_ID', 'RAW_REC_ID'),
]

# Fields added during classification
classification_fields = [
    'Vessel_Type_Simple',
    'Group_Locked',
    'Commodity_Locked',
    'Cargo_Locked',
    'Cargo_Detail_Locked',
    'Classified_Phase',
    'Last_Rule_ID'
]

# ============================
# BUILD MARKDOWN REPORT
# ============================

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write("# Import Pipeline Data Type & Transformation Audit\n")
    f.write("**Generated:** 2026-01-21\n\n")
    f.write("**Purpose:** Document data types, formats, and transformations through RAW → PREPROCESSED → CLASSIFIED\n\n")
    f.write("---\n\n")

    # Summary
    f.write("## Pipeline Summary\n\n")
    f.write(f"- **RAW Columns:** {len(df_raw.columns)}\n")
    f.write(f"- **PREPROCESSED Columns:** {len(df_preprocessed.columns)}\n")
    f.write(f"- **CLASSIFIED Columns:** {len(df_classified.columns)}\n\n")
    f.write(f"- **Columns Dropped:** {len(df_raw.columns) - len([f for f in core_fields if f[0] in df_raw.columns])}\n")
    f.write(f"- **Columns Added (Preprocessing):** {len(preprocessing_fields)}\n")
    f.write(f"- **Columns Added (Classification):** {len(classification_fields)}\n\n")
    f.write("---\n\n")

    # Core fields analysis
    f.write("## Core Fields: RAW → PREPROCESSED → CLASSIFIED\n\n")
    f.write("These fields exist across all pipeline stages (with possible renames):\n\n")

    for raw_col, prep_col, class_col in core_fields:
        f.write(f"### {raw_col}\n\n")

        if raw_col in df_raw.columns:
            raw_chars = detect_data_characteristics(df_raw[raw_col])
            f.write(f"**RAW Stage:**\n")
            f.write(f"- Column Name: `{raw_col}`\n")
            f.write(f"- Data Type: `{raw_chars['dtype']}`\n")
            f.write(f"- Null %: {raw_chars['null_pct']}\n")
            f.write(f"- Unique Values: {raw_chars['unique_count']}\n")
            if raw_chars['samples']:
                f.write(f"- Samples: `{raw_chars['samples'][0]}`")
                if len(raw_chars['samples']) > 1:
                    f.write(f", `{raw_chars['samples'][1]}`")
                f.write("\n")
            if raw_chars['format_notes']:
                f.write(f"- Format: {', '.join(raw_chars['format_notes'])}\n")
            f.write("\n")

        if prep_col in df_preprocessed.columns:
            prep_chars = detect_data_characteristics(df_preprocessed[prep_col])
            f.write(f"**PREPROCESSED Stage:**\n")
            f.write(f"- Column Name: `{prep_col}`")
            if prep_col != raw_col:
                f.write(f" ⚠️ **RENAMED** from `{raw_col}`")
            f.write("\n")
            f.write(f"- Data Type: `{prep_chars['dtype']}`\n")
            f.write(f"- Null %: {prep_chars['null_pct']}\n")
            f.write(f"- Unique Values: {prep_chars['unique_count']}\n")
            if prep_chars['samples']:
                f.write(f"- Samples: `{prep_chars['samples'][0]}`")
                if len(prep_chars['samples']) > 1:
                    f.write(f", `{prep_chars['samples'][1]}`")
                f.write("\n")
            f.write("\n")

        if class_col in df_classified.columns:
            class_chars = detect_data_characteristics(df_classified[class_col])
            f.write(f"**CLASSIFIED Stage:**\n")
            f.write(f"- Column Name: `{class_col}`\n")
            f.write(f"- Data Type: `{class_chars['dtype']}`\n")
            f.write(f"- Null %: {class_chars['null_pct']}\n")
            f.write(f"- Unique Values: {class_chars['unique_count']}\n")
            if class_chars['samples']:
                f.write(f"- Samples: `{class_chars['samples'][0]}`")
                if len(class_chars['samples']) > 1:
                    f.write(f", `{class_chars['samples'][1]}`")
                f.write("\n")
            f.write("\n")

        f.write("**Transformation Summary:**\n")
        if prep_col != raw_col:
            f.write(f"- Column renamed: `{raw_col}` → `{prep_col}`\n")
        else:
            f.write(f"- Column name unchanged\n")
        f.write("\n---\n\n")

    # Preprocessing additions
    f.write("## Fields Added During Preprocessing\n\n")
    f.write("These fields are derived/engineered during preprocessing:\n\n")

    for prep_col, class_col in preprocessing_fields:
        f.write(f"### {prep_col}\n\n")

        if prep_col in df_preprocessed.columns:
            prep_chars = detect_data_characteristics(df_preprocessed[prep_col])
            f.write(f"**Source:** Derived during preprocessing (not in RAW data)\n\n")
            f.write(f"**PREPROCESSED Stage:**\n")
            f.write(f"- Data Type: `{prep_chars['dtype']}`\n")
            f.write(f"- Null %: {prep_chars['null_pct']}\n")
            f.write(f"- Unique Values: {prep_chars['unique_count']}\n")
            if prep_chars['samples']:
                f.write(f"- Samples: `{prep_chars['samples'][0]}`")
                if len(prep_chars['samples']) > 1:
                    f.write(f", `{prep_chars['samples'][1]}`")
                f.write("\n")
            f.write("\n")

            # Add transformation logic notes
            if 'HS' in prep_col:
                f.write(f"**Derivation Logic:** Extracted from `HS Code` field (first {prep_col[-1]} digits)\n")
            elif prep_col == 'Port_Consolidated':
                f.write(f"**Derivation Logic:** Standardized port name from `Port of Unlading`\n")
            elif prep_col == 'Port_Code':
                f.write(f"**Derivation Logic:** Mapped port code from port name\n")
            elif prep_col == 'RAW_REC_ID':
                f.write(f"**Derivation Logic:** Unique record identifier (auto-generated)\n")
            elif prep_col == 'Pckg':
                f.write(f"**Derivation Logic:** Package type code (extracted from description or mapping)\n")

            f.write("\n---\n\n")

    # Classification additions
    f.write("## Fields Added During Classification\n\n")
    f.write("These fields are created during the classification phase:\n\n")

    for class_col in classification_fields:
        f.write(f"### {class_col}\n\n")

        if class_col in df_classified.columns:
            class_chars = detect_data_characteristics(df_classified[class_col])
            f.write(f"**Source:** Generated during classification\n\n")
            f.write(f"**CLASSIFIED Stage:**\n")
            f.write(f"- Data Type: `{class_chars['dtype']}`\n")
            f.write(f"- Null %: {class_chars['null_pct']}\n")
            f.write(f"- Unique Values: {class_chars['unique_count']}\n")
            if class_chars['samples']:
                f.write(f"- Samples: `{class_chars['samples'][0]}`")
                if len(class_chars['samples']) > 1:
                    f.write(f", `{class_chars['samples'][1]}`")
                f.write("\n")
            f.write("\n")

            # Add purpose notes
            if 'Locked' in class_col:
                f.write(f"**Purpose:** Boolean flag indicating if this taxonomy level is locked from further changes\n")
            elif class_col == 'Vessel_Type_Simple':
                f.write(f"**Purpose:** Simplified vessel type derived from ship registry lookup\n")
            elif class_col == 'Classified_Phase':
                f.write(f"**Purpose:** Phase number (1-10) indicating which classification phase matched this record\n")
            elif class_col == 'Last_Rule_ID':
                f.write(f"**Purpose:** Rule ID from dictionary that classified this record (for audit trail)\n")

            f.write("\n---\n\n")

    # Key transformations
    f.write("## Key Transformations Summary\n\n")

    f.write("### Column Renames (RAW → PREPROCESSED)\n\n")
    f.write("| RAW Column | PREPROCESSED Column | Reason |\n")
    f.write("|------------|---------------------|--------|\n")
    f.write("| `Weight (kg)` | `Kilos` | Shortened name |\n")
    f.write("| `Weight (t)` | `Tons` | Shortened name |\n")
    f.write("| `Value of Goods (USD)` | `Value` | Shortened name, USD implied |\n")
    f.write("| `Vessel IMO` | `IMO` | Shortened name |\n")
    f.write("| `Vessel Voyage ID` | `Voyage` | Shortened name |\n")
    f.write("| `HS Code` | `HS Code Desc.` | Clarified as description field |\n")
    f.write("| `Port of Unlading` | `Port of Discharge (D)` | Clarified as destination port |\n")
    f.write("| `Port of Lading` | `Port of Loading (F)` | Clarified as foreign/origin port |\n")
    f.write("| `Shipment Origin` | `Origin (F)` | Marked as foreign |\n")
    f.write("| `Shipment Destination` | `Destination (D)` | Marked as domestic |\n")
    f.write("\n")

    f.write("### Data Type Changes\n\n")
    f.write("| Field | RAW Type | PREPROCESSED Type | Notes |\n")
    f.write("|-------|----------|-------------------|-------|\n")

    # Check for actual type changes
    for raw_col, prep_col, _ in core_fields:
        if raw_col in df_raw.columns and prep_col in df_preprocessed.columns:
            raw_type = str(df_raw[raw_col].dtype)
            prep_type = str(df_preprocessed[prep_col].dtype)
            if raw_type != prep_type:
                f.write(f"| `{raw_col}` | `{raw_type}` | `{prep_type}` | Type conversion |\n")

    f.write("\n")

    f.write("### Value Transformations\n\n")
    f.write("- **HS Codes:** Extracted into HS2 (2-digit), HS4 (4-digit), HS6 (6-digit) fields\n")
    f.write("- **Port Names:** Standardized and mapped to port codes\n")
    f.write("- **Carrier Names:** Extracted SCAC code from full carrier string\n")
    f.write("- **Weight:** Preserved in original format plus converted to Kilos/Tons\n")
    f.write("- **Classification:** Added Group/Commodity/Cargo/Cargo Detail taxonomy\n")
    f.write("\n")

    f.write("---\n\n")
    f.write("## Data Integrity Checks\n\n")
    f.write("### Critical Fields - Non-Null Rates\n\n")

    critical_fields = [
        ('Bill of Lading Number', 'Bill of Lading Number'),
        ('Arrival Date', 'Arrival Date'),
        ('Tons', 'Tons'),
        ('Goods Shipped', 'Goods Shipped'),
    ]

    for raw_col, prep_col in critical_fields:
        if prep_col in df_preprocessed.columns:
            null_pct = df_preprocessed[prep_col].isna().sum() / len(df_preprocessed) * 100
            status = "✓ GOOD" if null_pct < 5 else ("⚠ WARNING" if null_pct < 20 else "❌ CRITICAL")
            f.write(f"- **{prep_col}:** {100-null_pct:.1f}% populated {status}\n")

    f.write("\n---\n\n")
    f.write("*End of Data Type Audit*\n")

print(f"[OK] Enhanced audit report saved: {OUTPUT_FILE}")
print()
print("="*80)
print("ANALYSIS COMPLETE")
print("="*80)
