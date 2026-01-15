"""
Process Panjiva Export Raw Data
Version: 1.0.0
Date: 2026-01-15

Purpose:
- Unzip and consolidate raw export zip files
- Extract HS code levels (HS2, HS4, HS6)
- Standardize column names (Weight (t) → Tons)
- Add year column
- Generate unique RAW_REC_ID
- Split by year

Input: 00_raw_data/00_02_panjiva_exports_raw/*.zip (12 files)
Output: 01_STAGE01_PREPROCESSING/01.01_annual_files/panjiva_exports_{YEAR}_PREPROCESSED_*.csv
"""

import pandas as pd
import zipfile
import os
from pathlib import Path
from datetime import datetime

print("="*80)
print("PROCESS PANJIVA EXPORT DATA v1.0.0")
print("="*80)

# Paths
RAW_DIR = Path(r"G:\My Drive\LLM\project_manifest\00_raw_data\00_02_panjiva_exports_raw")
OUTPUT_DIR = Path(r"G:\My Drive\LLM\project_manifest\01_STAGE01_PREPROCESSING\01.01_annual_files")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# Find all zip files
print(f"\n1. Finding export zip files in: {RAW_DIR}")
zip_files = list(RAW_DIR.glob("*.zip"))
print(f"   Found {len(zip_files)} zip files")

# Extract and read all CSVs
print(f"\n2. Extracting and reading CSV files...")
all_dfs = []
total_records = 0

for i, zip_path in enumerate(zip_files, 1):
    print(f"   [{i}/{len(zip_files)}] Processing: {zip_path.name}")

    with zipfile.ZipFile(zip_path, 'r') as z:
        csv_files = [f for f in z.namelist() if f.endswith('.csv')]

        for csv_file in csv_files:
            with z.open(csv_file) as f:
                df = pd.read_csv(f, low_memory=False)
                all_dfs.append(df)
                total_records += len(df)
                print(f"      - {csv_file}: {len(df):,} records")

# Concatenate all dataframes
print(f"\n3. Concatenating all export data...")
df_all = pd.concat(all_dfs, ignore_index=True)
print(f"   Total records: {len(df_all):,}")
print(f"   Total columns: {len(df_all.columns)}")

# Add unique RAW_REC_ID
print(f"\n4. Adding RAW_REC_ID...")
df_all['RAW_REC_ID'] = range(1, len(df_all) + 1)

# Parse Shipment Date and add year
print(f"\n5. Parsing dates and adding year column...")
df_all['Shipment Date'] = pd.to_datetime(df_all['Shipment Date'], errors='coerce')
df_all['Year'] = df_all['Shipment Date'].dt.year

year_counts = df_all['Year'].value_counts().sort_index()
print(f"   Year distribution:")
for year, count in year_counts.items():
    print(f"     {year}: {count:,} records")

# Standardize tonnage column name
print(f"\n6. Standardizing column names...")
if 'Weight (t)' in df_all.columns:
    df_all['Tons'] = df_all['Weight (t)']
    print(f"   Renamed 'Weight (t)' -> 'Tons'")

# Extract HS code levels
print(f"\n7. Extracting HS code levels...")
def extract_hs_codes(hs_code):
    """Extract HS2, HS4, HS6 from HS Code"""
    if pd.isna(hs_code):
        return '', '', ''

    hs_str = str(hs_code).replace('.', '').strip()

    # Pad to 6 digits if shorter
    hs_str = hs_str.ljust(6, '0')

    hs2 = hs_str[:2] if len(hs_str) >= 2 else ''
    hs4 = hs_str[:4] if len(hs_str) >= 4 else ''
    hs6 = hs_str[:6] if len(hs_str) >= 6 else ''

    return hs2, hs4, hs6

# Apply extraction
hs_extracted = df_all['HS Code'].apply(extract_hs_codes)
df_all['HS2'] = [x[0] for x in hs_extracted]
df_all['HS4'] = [x[1] for x in hs_extracted]
df_all['HS6'] = [x[2] for x in hs_extracted]

print(f"   HS2 codes extracted: {df_all['HS2'].notna().sum():,}")
print(f"   HS4 codes extracted: {df_all['HS4'].notna().sum():,}")
print(f"   HS6 codes extracted: {df_all['HS6'].notna().sum():,}")

# Split by year and save
print(f"\n8. Splitting by year and saving...")

for year in sorted(df_all['Year'].dropna().unique()):
    year = int(year)
    df_year = df_all[df_all['Year'] == year].copy()

    output_file = OUTPUT_DIR / f"panjiva_exports_{year}_PREPROCESSED_v{timestamp}.csv"
    df_year.to_csv(output_file, index=False)

    print(f"   Year {year}: {len(df_year):,} records -> {output_file.name}")

# Summary statistics
print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

print(f"\nTotal export records processed: {len(df_all):,}")
print(f"Total columns: {len(df_all.columns)}")

print(f"\nColumn additions:")
print(f"  - RAW_REC_ID (unique row ID)")
print(f"  - Year (from Shipment Date)")
print(f"  - Tons (standardized from Weight (t))")
print(f"  - HS2, HS4, HS6 (extracted from HS Code)")

print(f"\nKey columns present:")
key_cols = ['Vessel', 'Port of Lading', 'Shipment Date', 'Voyage', 'IMO', 'Carrier',
            'Shipper', 'HS Code', 'Goods Shipped', 'Tons']
for col in key_cols:
    exists = col in df_all.columns
    print(f"  {col:<25} {'[OK]' if exists else '[--]'}")

# Check for carrier column name
if 'Carrier' in df_all.columns:
    print(f"\n  Carrier column name: 'Carrier' (not 'Carrier Name')")
elif 'Carrier Name' in df_all.columns:
    print(f"\n  Carrier column name: 'Carrier Name'")

# Sample data
print(f"\n" + "="*80)
print("SAMPLE DATA (First 3 Records)")
print("="*80)
sample_cols = ['Vessel', 'Port of Lading', 'Shipment Date', 'Carrier', 'Tons', 'HS2']
available_cols = [c for c in sample_cols if c in df_all.columns]
if len(available_cols) > 0:
    print(df_all[available_cols].head(3).to_string(index=False))

print(f"\n" + "="*80)
print("COMPLETE!")
print("="*80)
