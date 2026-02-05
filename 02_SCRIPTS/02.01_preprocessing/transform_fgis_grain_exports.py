"""
Transform FGIS Grain Export Data
Version: 1.0.0
Date: 2026-01-15

Purpose:
- Process FGIS (Federal Grain Inspection Service) grain export data
- Filter for ocean vessels only (Type Carrier = "1")
- Apply field transformations per data dictionary
- Output cleaned dataset for analysis

Transformations:
- Date format: YYYYMMDD → yyyy-MMM-dd
- Numeric format: Thousands separator, no decimals (Pounds, Metric Ton)
- TW: 2 decimal places
- Column renames: Port → Port_Consolidated, etc.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

print("="*80)
print("FGIS GRAIN EXPORT DATA TRANSFORMATION v1.0.0")
print("="*80)

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# File paths
INPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_raw_data\00_04_fgis_raw\CY2023.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\fgis_2023_grain_exports_v1.0.0.csv")

# Columns to retain (from data dictionary)
COLUMNS_TO_RETAIN = [
    'Thursday',
    'Serial No.',
    'Cert Date',
    'Type Carrier',
    'Carrier Name',
    'Grade',
    'Grain',
    'Class',
    'Pounds',
    'Destination',
    'Field Office',
    'Port',
    'AMS Reg',
    'FGIS Reg',
    'TW',
    'Metric Ton'
]

# Column renames (from data dictionary)
COLUMN_RENAMES = {
    'Port': 'Port_Consolidated',
    'AMS Reg': 'Port_Coast',
    'FGIS Reg': 'Port_Region',
    'Destination': 'Foreign_Destination',
    'Carrier Name': 'Vessel',
    'Grain': 'Cargo',
    'Class': 'Cargo_Detail'
}

# Load data
print("\n1. Loading FGIS data...")
df = pd.read_csv(INPUT_FILE, low_memory=False)
print(f"   Raw records: {len(df):,}")
print(f"   Total columns: {len(df.columns)}")

# Filter for ocean vessels (Type Carrier = "1")
print("\n2. Filtering for ocean vessels (Type Carrier = '1')...")
df_ocean = df[df['Type Carrier'] == 1].copy()
print(f"   Ocean vessel records: {len(df_ocean):,}")
print(f"   Records filtered out: {len(df) - len(df_ocean):,}")

# Retain only specified columns
print("\n3. Retaining specified columns...")
df_clean = df_ocean[COLUMNS_TO_RETAIN].copy()
print(f"   Columns retained: {len(COLUMNS_TO_RETAIN)}")
print(f"   Columns dropped: {len(df.columns) - len(COLUMNS_TO_RETAIN)}")

# Transform date columns (YYYYMMDD → yyyy-MMM-dd)
print("\n4. Transforming date formats...")

def format_fgis_date(date_val):
    """Convert YYYYMMDD to yyyy-MMM-dd format"""
    if pd.isna(date_val):
        return None
    try:
        date_str = str(int(date_val))
        if len(date_str) == 8:
            year = date_str[:4]
            month = date_str[4:6]
            day = date_str[6:8]
            dt = datetime(int(year), int(month), int(day))
            return dt.strftime("%Y-%b-%d")
        return None
    except:
        return None

df_clean['Thursday'] = df_clean['Thursday'].apply(format_fgis_date)
df_clean['Cert Date'] = df_clean['Cert Date'].apply(format_fgis_date)
print("   Date columns formatted: Thursday, Cert Date")

# Transform numeric columns
print("\n5. Formatting numeric columns...")

# Pounds and Metric Ton: will be formatted during CSV write
# TW: round to 2 decimal places
df_clean['TW'] = pd.to_numeric(df_clean['TW'], errors='coerce').round(2)
print("   TW rounded to 2 decimal places")

# Rename columns
print("\n6. Renaming columns per data dictionary...")
df_clean = df_clean.rename(columns=COLUMN_RENAMES)
print(f"   Columns renamed: {len(COLUMN_RENAMES)}")
for old, new in COLUMN_RENAMES.items():
    print(f"      {old} -> {new}")

# Clean vessel names (strip whitespace)
print("\n7. Cleaning vessel names...")
df_clean['Vessel'] = df_clean['Vessel'].str.strip()

# Summary statistics
print("\n" + "="*80)
print("DATA SUMMARY")
print("="*80)

print(f"\nRecords: {len(df_clean):,}")
print(f"Date range: {df_clean['Cert Date'].min()} to {df_clean['Cert Date'].max()}")

print(f"\nTop 10 Grain Types:")
grain_counts = df_clean['Cargo'].value_counts().head(10)
for grain, count in grain_counts.items():
    tons = df_clean[df_clean['Cargo'] == grain]['Metric Ton'].sum()
    print(f"   {grain:<20} {count:>7,} shipments  {tons:>12,.0f} MT")

print(f"\nTop 10 Destinations:")
dest_counts = df_clean['Foreign_Destination'].value_counts().head(10)
for dest, count in dest_counts.items():
    tons = df_clean[df_clean['Foreign_Destination'] == dest]['Metric Ton'].sum()
    print(f"   {dest:<20} {count:>7,} shipments  {tons:>12,.0f} MT")

print(f"\nTop 10 Ports:")
port_counts = df_clean['Port_Consolidated'].value_counts().head(10)
for port, count in port_counts.items():
    tons = df_clean[df_clean['Port_Consolidated'] == port]['Metric Ton'].sum()
    print(f"   {port:<25} {count:>7,} shipments  {tons:>12,.0f} MT")

print(f"\nPort Coast Distribution:")
coast_counts = df_clean['Port_Coast'].value_counts()
for coast, count in coast_counts.items():
    tons = df_clean[df_clean['Port_Coast'] == coast]['Metric Ton'].sum()
    pct = count / len(df_clean) * 100
    print(f"   {coast:<15} {count:>7,} ({pct:>5.1f}%)  {tons:>12,.0f} MT")

print(f"\nTotal Tonnage:")
total_pounds = df_clean['Pounds'].sum()
total_mt = df_clean['Metric Ton'].sum()
print(f"   Pounds: {total_pounds:,.0f}")
print(f"   Metric Tons: {total_mt:,.0f}")

# Save output
print("\n" + "="*80)
print("SAVING OUTPUT")
print("="*80)

# Format numeric columns for display (add thousands separator)
df_output = df_clean.copy()
df_output['Pounds'] = df_output['Pounds'].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "")
df_output['Metric Ton'] = df_output['Metric Ton'].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "")

df_output.to_csv(OUTPUT_FILE, index=False)
print(f"\nSaved: {OUTPUT_FILE.name}")
file_size = OUTPUT_FILE.stat().st_size / (1024 * 1024)
print(f"Size: {file_size:.1f} MB")

print("\n" + "="*80)
print("COMPLETE!")
print("="*80)
print(f"\nOutput: {OUTPUT_FILE}")
print(f"Records: {len(df_output):,}")
print(f"Columns: {len(df_output.columns)}")
