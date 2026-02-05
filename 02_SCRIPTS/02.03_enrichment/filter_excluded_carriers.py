"""
Filter out excluded carriers from Stage 00 preprocessed data
Removes cruise lines, container carriers, and other non-cargo carriers

This creates cleaner input files for classification by removing noise.

Author: WSD3 / Claude Code
Date: 2026-01-14
Version: 1.0.0
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
INPUT_DIR = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01_01_panjiva_imports_step_one")
OUTPUT_DIR = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01.01_annual_files")
EXCLUDE_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\carrier_exclude_update_011426_1230.csv")

# Create output directory if needed
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

stamp("=== Filter Excluded Carriers ===")
stamp("")

# Load exclusion list
stamp(f"Loading exclusion list: {EXCLUDE_FILE.name}")
df_exclude = pd.read_csv(EXCLUDE_FILE, dtype=str)

# Get carriers marked for exclusion (exe, EXE, x, X)
exclude_types = ['exe', 'EXE', 'x', 'X']
excluded_carriers = df_exclude[df_exclude['Rank'].isin(exclude_types)]
exclude_scac_list = excluded_carriers['SCAC'].str.strip().tolist()

stamp(f"Total carriers to exclude: {len(exclude_scac_list)}")
stamp("")
stamp("Exclusion types:")
for t in exclude_types:
    count = len(df_exclude[df_exclude['Rank'] == t])
    if count > 0:
        stamp(f"  {t}: {count} carriers")

stamp("")
stamp("Sample excluded carriers:")
for _, row in excluded_carriers.head(15).iterrows():
    scac = row['SCAC'].strip()
    name = row['Carrier_Name'].strip()[:35]
    records = row[' Record_Count '].strip()
    stamp(f"  {scac:6s} - {name:35s} ({records:>6s} records)")

stamp("")
stamp("=" * 70)
stamp("")

# Process each year
years = ['2023', '2024', '2025']
total_records_before = 0
total_records_after = 0
total_records_removed = 0

for year in years:
    stamp(f"Processing {year}...")

    # Input file
    input_file = INPUT_DIR / f"panjiva_imports_{year}_20260112_STAGE00_v20260112_2052.csv"

    # Output file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    output_file = OUTPUT_DIR / f"panjiva_imports_{year}_FILTERED_v{timestamp}.csv"

    # Load data
    stamp(f"  Loading: {input_file.name}")
    df = pd.read_csv(input_file, dtype=str)
    records_before = len(df)
    total_records_before += records_before
    stamp(f"  Records before: {records_before:,}")

    # Filter out excluded carriers
    # Check if SCAC code is in the exclusion list
    def should_exclude(carrier_str):
        """Check if carrier string contains any excluded SCAC code"""
        if pd.isna(carrier_str):
            return False
        carrier_upper = str(carrier_str).upper()
        for scac in exclude_scac_list:
            if scac.upper() in carrier_upper:
                return True
        return False

    df_filtered = df[~df['Carrier'].apply(should_exclude)].copy()

    records_after = len(df_filtered)
    records_removed = records_before - records_after
    total_records_after += records_after
    total_records_removed += records_removed

    stamp(f"  Records after:  {records_after:,}")
    stamp(f"  Records removed: {records_removed:,} ({records_removed/records_before*100:.1f}%)")

    # Save filtered data
    stamp(f"  Saving: {output_file.name}")
    df_filtered.to_csv(output_file, index=False)

    stamp("")

stamp("=" * 70)
stamp("")
stamp("=== SUMMARY ===")
stamp("")
stamp(f"Total records before:  {total_records_before:,}")
stamp(f"Total records after:   {total_records_after:,}")
stamp(f"Total records removed: {total_records_removed:,} ({total_records_removed/total_records_before*100:.1f}%)")
stamp("")
stamp(f"Carriers excluded: {len(exclude_scac_list)}")
stamp("")
stamp(f"Filtered files saved to: {OUTPUT_DIR}")
stamp("")
stamp("Complete!")
stamp("")
stamp("Next steps:")
stamp("  1. Review filtered files")
stamp("  2. Update classification scripts to use filtered files")
stamp("  3. Re-run 15K sample test with cleaner data")
