"""
Column Lineage Audit for Panjiva Import Pipeline
Version: 1.0.0
Created: 2026-01-21

Traces every column through: RAW → PREPROCESSED → CLASSIFIED
Shows transformations, renames, additions, deletions
"""

import pandas as pd
from pathlib import Path
import sys

# ============================
# FILE PATHS
# ============================
BASE_DIR = Path(r"G:\My Drive\LLM\project_manifest")

RAW_FILE = BASE_DIR / "00_raw_data" / "00_99_user_notes_raw_data" / "panjiva_imports" / "panjiva_manifest_2023.csv"
PREPROCESSED_FILE = BASE_DIR / "00_DATA" / "00.02_PREPROCESSED" / "panjiva_imports_2023_AUTHORITATIVE_v1.0.0.csv"
CLASSIFIED_FILE = BASE_DIR / "03_DOCUMENTATION" / "03.04_summaries" / "sample_test_15k" / "sample_15k_classified_v3.6.0.csv"

OUTPUT_DIR = BASE_DIR / "03_DOCUMENTATION" / "03.05_data_dictionaries"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "IMPORT_COLUMN_LINEAGE_AUDIT.csv"
OUTPUT_MD = OUTPUT_DIR / "IMPORT_COLUMN_LINEAGE_AUDIT.md"

# ============================
# LOAD DATA
# ============================
print("="*80)
print("COLUMN LINEAGE AUDIT - PANJIVA IMPORTS")
print("="*80)
print()

print("Loading files...")
print(f"  RAW: {RAW_FILE.name}")
df_raw = pd.read_csv(RAW_FILE, dtype=str, nrows=100)
print(f"    [OK] Loaded {len(df_raw)} sample records, {len(df_raw.columns)} columns")

print(f"  PREPROCESSED: {PREPROCESSED_FILE.name}")
df_preprocessed = pd.read_csv(PREPROCESSED_FILE, dtype=str, nrows=100)
print(f"    [OK] Loaded {len(df_preprocessed)} sample records, {len(df_preprocessed.columns)} columns")

print(f"  CLASSIFIED: {CLASSIFIED_FILE.name}")
df_classified = pd.read_csv(CLASSIFIED_FILE, dtype=str, nrows=100)
print(f"    [OK] Loaded {len(df_classified)} sample records, {len(df_classified.columns)} columns")

print()

# ============================
# COLUMN MAPPING LOGIC
# ============================

# Define known column mappings (RAW → PREPROCESSED)
COLUMN_MAPPING = {
    # Identity columns (kept as-is)
    "Bill of Lading Number": "Bill of Lading Number",
    "Arrival Date": "Arrival Date",
    "Consignee": "Consignee",
    "Consignee (Original Format)": "Consignee (Original Format)",
    "Consignee SIC Codes": "Consignee SIC Codes",
    "Shipper": "Shipper",
    "Shipper (Original Format)": "Shipper (Original Format)",
    "Shipper SIC Codes": "Shipper SIC Codes",
    "Notify Party": "Notify Party",
    "Carrier": "Carrier",
    "Vessel": "Vessel",
    "Vessel IMO": "IMO",
    "Is Containerized": "Is Containerized",
    "Measurement": "Measurement",
    "Weight (kg)": "Kilos",
    "Weight (t)": "Tons",
    "Weight (Original Format)": "Weight (Original Format)",
    "Value of Goods (USD)": "Value",
    "HS Code": "HS Code Desc.",
    "Goods Shipped": "Goods Shipped",
    "Quantity": "Qty",

    # Renamed columns
    "Shipment Origin": "Origin (F)",
    "Shipment Destination": "Destination (D)",
    "Port of Unlading": "Port of Discharge (D)",
    "Port of Lading": "Port of Loading (F)",
    "Port of Lading Country": "Country of Origin (F)",
    "Place of Receipt": "Place of Receipt (F)",
    "Vessel Voyage ID": "Voyage",

    # New columns added during preprocessing
    "Port_Consolidated": "Port_Consolidated",
    "Port_Coast": "Port_Coast",
    "Port_Region": "Port_Region",
    "Port_Code": "Port_Code",
    "Carrier Name": "Carrier Name",
    "Pckg": "Pckg",
    "HS2": "HS2",
    "HS4": "HS4",
    "HS6": "HS6",
    "RAW_REC_ID": "RAW_REC_ID",
    "Count": "Count",
}

# Columns added in preprocessing (derived/engineered)
PREPROCESSING_ADDS = [
    "Port_Consolidated",
    "Port_Coast",
    "Port_Region",
    "Port_Code",
    "Carrier Name",
    "Pckg",
    "HS2",
    "HS4",
    "HS6",
    "RAW_REC_ID",
    "Count",
    "Group",
    "Commodity",
    "Cargo",
    "Cargo Detail",
    "Report_One",
    "Report_Two",
    "Report_Three",
    "Report_Four",
    "Filter",
    "Note",
    "Type",
    "DWT"
]

# Columns added in classification
CLASSIFICATION_ADDS = [
    "Vessel_Type_Simple",
    "Group_Locked",
    "Commodity_Locked",
    "Cargo_Locked",
    "Cargo_Detail_Locked",
    "Classified_Phase",
    "Last_Rule_ID"
]

# ============================
# BUILD AUDIT TRAIL
# ============================
print("Building column audit trail...")
print()

audit_records = []

# Track all columns across stages
raw_cols = set(df_raw.columns)
preprocessed_cols = set(df_preprocessed.columns)
classified_cols = set(df_classified.columns)

# Process each column from RAW
for col in sorted(df_raw.columns):
    # Check if column exists in preprocessed
    mapped_name = None
    for raw_name, prep_name in COLUMN_MAPPING.items():
        if col == raw_name:
            mapped_name = prep_name
            break

    in_preprocessed = mapped_name in preprocessed_cols if mapped_name else col in preprocessed_cols
    in_classified = mapped_name in classified_cols if mapped_name else col in classified_cols

    # Get sample values
    raw_sample = df_raw[col].dropna().head(1).values[0] if len(df_raw[col].dropna()) > 0 else ""
    prep_sample = df_preprocessed[mapped_name].dropna().head(1).values[0] if mapped_name and mapped_name in df_preprocessed.columns and len(df_preprocessed[mapped_name].dropna()) > 0 else ""
    class_sample = df_classified[mapped_name].dropna().head(1).values[0] if mapped_name and mapped_name in df_classified.columns and len(df_classified[mapped_name].dropna()) > 0 else ""

    status = "KEPT" if in_preprocessed else "DROPPED"

    audit_records.append({
        "Stage_1_RAW_Column": col,
        "Stage_2_PREPROCESSED_Column": mapped_name if in_preprocessed else "N/A",
        "Stage_3_CLASSIFIED_Column": mapped_name if in_classified else "N/A",
        "Status": status,
        "RAW_Sample_Value": str(raw_sample)[:100],
        "PREPROCESSED_Sample_Value": str(prep_sample)[:100],
        "CLASSIFIED_Sample_Value": str(class_sample)[:100],
        "Transformation": "Renamed" if mapped_name and mapped_name != col else ("Kept" if in_preprocessed else "Dropped"),
        "Notes": ""
    })

# Add columns that appear in PREPROCESSED but not RAW
for col in sorted(preprocessed_cols):
    if col not in [r["Stage_2_PREPROCESSED_Column"] for r in audit_records]:
        in_classified = col in classified_cols

        prep_sample = df_preprocessed[col].dropna().head(1).values[0] if len(df_preprocessed[col].dropna()) > 0 else ""
        class_sample = df_classified[col].dropna().head(1).values[0] if col in df_classified.columns and len(df_classified[col].dropna()) > 0 else ""

        notes = ""
        if col in PREPROCESSING_ADDS:
            notes = "Added during preprocessing (derived/engineered)"

        audit_records.append({
            "Stage_1_RAW_Column": "N/A",
            "Stage_2_PREPROCESSED_Column": col,
            "Stage_3_CLASSIFIED_Column": col if in_classified else "N/A",
            "Status": "ADDED IN PREPROCESSING",
            "RAW_Sample_Value": "",
            "PREPROCESSED_Sample_Value": str(prep_sample)[:100],
            "CLASSIFIED_Sample_Value": str(class_sample)[:100],
            "Transformation": "Added",
            "Notes": notes
        })

# Add columns that appear in CLASSIFIED but not PREPROCESSED
for col in sorted(classified_cols):
    if col not in [r["Stage_3_CLASSIFIED_Column"] for r in audit_records if r["Stage_3_CLASSIFIED_Column"] != "N/A"]:
        class_sample = df_classified[col].dropna().head(1).values[0] if len(df_classified[col].dropna()) > 0 else ""

        notes = ""
        if col in CLASSIFICATION_ADDS:
            notes = "Added during classification (lock flags / metadata)"

        audit_records.append({
            "Stage_1_RAW_Column": "N/A",
            "Stage_2_PREPROCESSED_Column": "N/A",
            "Stage_3_CLASSIFIED_Column": col,
            "Status": "ADDED IN CLASSIFICATION",
            "RAW_Sample_Value": "",
            "PREPROCESSED_Sample_Value": "",
            "CLASSIFIED_Sample_Value": str(class_sample)[:100],
            "Transformation": "Added",
            "Notes": notes
        })

# Convert to DataFrame
df_audit = pd.DataFrame(audit_records)

# ============================
# SAVE AUDIT TRAIL
# ============================
print(f"Saving audit trail...")
df_audit.to_csv(OUTPUT_FILE, index=False)
print(f"  [OK] CSV saved: {OUTPUT_FILE}")

# ============================
# CREATE MARKDOWN REPORT
# ============================
print(f"Creating markdown report...")

with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
    f.write("# Import Data Column Lineage Audit\n")
    f.write("**Generated:** 2026-01-21\n\n")
    f.write("**Purpose:** Trace every column through the import pipeline from RAW → PREPROCESSED → CLASSIFIED\n\n")
    f.write("---\n\n")

    # Summary statistics
    f.write("## Summary Statistics\n\n")
    f.write(f"- **RAW Columns:** {len(raw_cols)}\n")
    f.write(f"- **PREPROCESSED Columns:** {len(preprocessed_cols)}\n")
    f.write(f"- **CLASSIFIED Columns:** {len(classified_cols)}\n\n")

    dropped = df_audit[df_audit['Status'] == 'DROPPED']
    kept = df_audit[df_audit['Status'] == 'KEPT']
    added_prep = df_audit[df_audit['Status'] == 'ADDED IN PREPROCESSING']
    added_class = df_audit[df_audit['Status'] == 'ADDED IN CLASSIFICATION']

    f.write(f"- **Columns Dropped (RAW → PREPROCESSED):** {len(dropped)}\n")
    f.write(f"- **Columns Kept (RAW → PREPROCESSED):** {len(kept)}\n")
    f.write(f"- **Columns Added in PREPROCESSING:** {len(added_prep)}\n")
    f.write(f"- **Columns Added in CLASSIFICATION:** {len(added_class)}\n\n")

    f.write("---\n\n")

    # Detailed column tracking
    f.write("## Column Evolution Table\n\n")
    f.write("| RAW Column | PREPROCESSED Column | CLASSIFIED Column | Status | Transformation |\n")
    f.write("|------------|---------------------|-------------------|--------|----------------|\n")

    for _, row in df_audit.iterrows():
        f.write(f"| {row['Stage_1_RAW_Column']} | {row['Stage_2_PREPROCESSED_Column']} | ")
        f.write(f"{row['Stage_3_CLASSIFIED_Column']} | {row['Status']} | {row['Transformation']} |\n")

    f.write("\n---\n\n")

    # Dropped columns details
    f.write("## Columns Dropped in Preprocessing\n\n")
    f.write("These columns existed in RAW data but were removed during preprocessing:\n\n")
    for _, row in dropped.iterrows():
        f.write(f"- **{row['Stage_1_RAW_Column']}**\n")
        if row['RAW_Sample_Value']:
            f.write(f"  - Sample: `{row['RAW_Sample_Value']}`\n")

    f.write("\n---\n\n")

    # Added columns details
    f.write("## Columns Added in Preprocessing\n\n")
    f.write("These columns were created/derived during preprocessing:\n\n")
    for _, row in added_prep.iterrows():
        f.write(f"- **{row['Stage_2_PREPROCESSED_Column']}**\n")
        if row['Notes']:
            f.write(f"  - {row['Notes']}\n")
        if row['PREPROCESSED_Sample_Value']:
            f.write(f"  - Sample: `{row['PREPROCESSED_Sample_Value']}`\n")

    f.write("\n---\n\n")

    f.write("## Columns Added in Classification\n\n")
    f.write("These columns were created during classification:\n\n")
    for _, row in added_class.iterrows():
        f.write(f"- **{row['Stage_3_CLASSIFIED_Column']}**\n")
        if row['Notes']:
            f.write(f"  - {row['Notes']}\n")
        if row['CLASSIFIED_Sample_Value']:
            f.write(f"  - Sample: `{row['CLASSIFIED_Sample_Value']}`\n")

print(f"  [OK] Markdown saved: {OUTPUT_MD}")

print()
print("="*80)
print("AUDIT COMPLETE")
print("="*80)
print()
print(f"Summary:")
print(f"  - {len(dropped)} columns DROPPED")
print(f"  - {len(kept)} columns KEPT")
print(f"  - {len(added_prep)} columns ADDED in preprocessing")
print(f"  - {len(added_class)} columns ADDED in classification")
print()
print(f"Review audit report:")
print(f"  {OUTPUT_MD}")
