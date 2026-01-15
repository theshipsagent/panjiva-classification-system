import zipfile
import pandas as pd
import os

print("="*80)
print("IMPORT vs EXPORT COLUMN COMPARISON")
print("="*80)

# Read import sample
import_path = r"G:\My Drive\LLM\project_manifest\01_STAGE01_PREPROCESSING\01.01_annual_files\panjiva_imports_2023_PORTCALL_v20260115_1530.csv"
df_import = pd.read_csv(import_path, nrows=3)

# Read export sample
export_dir = r"G:\My Drive\LLM\project_manifest\00_raw_data\00_02_panjiva_exports_raw"
zips = [f for f in os.listdir(export_dir) if f.endswith('.zip')]
if zips:
    with zipfile.ZipFile(os.path.join(export_dir, zips[0]), 'r') as z:
        csv_files = [f for f in z.namelist() if f.endswith('.csv')]
        if csv_files:
            with z.open(csv_files[0]) as f:
                df_export = pd.read_csv(f, nrows=3)

print(f"\nIMPORT columns: {len(df_import.columns)}")
print(f"EXPORT columns: {len(df_export.columns)}")

# Key column mappings
print("\n" + "="*80)
print("KEY COLUMN MAPPINGS (Import → Export)")
print("="*80)

mappings = {
    'Arrival Date': 'Shipment Date',
    'Port of Discharge (D)': 'Port of Lading',
    'Port of Loading (F)': 'Port of Unlading',
    'Consignee': 'Shipper',
    'Shipper': '(No direct equivalent - foreign exporter)',
    'Destination (D)': 'Shipment Destination',
    'Origin (F)': 'Place of Receipt',
}

for imp_col, exp_col in mappings.items():
    imp_exists = imp_col in df_import.columns
    exp_exists = exp_col in df_export.columns if '(' not in exp_col else 'N/A'
    print(f"{imp_col:<30} → {exp_col:<30} [Import: {imp_exists}, Export: {exp_exists}]")

# Common columns that should match
print("\n" + "="*80)
print("COMMON COLUMNS (should exist in both)")
print("="*80)

common = ['Bill of Lading Number', 'Vessel', 'Voyage', 'IMO', 'Carrier', 'Is Containerized',
          'HS Code', 'Goods Shipped', 'Weight (kg)', 'Weight (t)', 'Value of Goods (USD)']

for col in common:
    imp_exists = col in df_import.columns
    exp_exists = col in df_export.columns
    match = "✓" if (imp_exists and exp_exists) else "✗"
    print(f"{col:<35} Import: {str(imp_exists):<5} Export: {str(exp_exists):<5} {match}")

# Export-specific columns not in imports
print("\n" + "="*80)
print("EXPORT-SPECIFIC COLUMNS (not in imports)")
print("="*80)

export_only = set(df_export.columns) - set(df_import.columns)
for col in sorted(export_only)[:20]:
    print(f"  - {col}")

print(f"\n  ... and {len(export_only) - 20} more export-only columns" if len(export_only) > 20 else "")

print("\n" + "="*80)
print("CRITICAL PORT COLUMNS FOR MATCHING")
print("="*80)
print("\nFor USACE CLEARANCE (outbound/exports) matching:")
print("  USACE Clearance Port → Panjiva 'Port of Lading' (US origin)")
print("  USACE Clearance Date → Panjiva 'Shipment Date'")
print("  USACE Vessel + IMO → Panjiva Vessel + IMO")
print("\nFor statistical rollups:")
print("  Need to add Port_Consolidated, Port_Coast, Port_Region to exports")
print("  Based on 'Port of Lading' (US export port)")
