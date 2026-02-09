"""
Deduplicate Preprocessed Data
==============================
Remove duplicate Bill of Lading numbers from existing preprocessed file.

BOL is a unique government-assigned identifier - duplicates indicate
overlapping raw file downloads that weren't caught during preprocessing.

Author: WSD3 / Claude Code
Date: 2026-02-09
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"G:\My Drive\LLM\project_manifest")
INPUT_FILE = BASE_DIR / "00_DATA" / "00.02_PREPROCESSED" / "panjiva_ALL_YEARS_preprocessed.csv"
OUTPUT_FILE = BASE_DIR / "00_DATA" / "00.02_PREPROCESSED" / "panjiva_ALL_YEARS_preprocessed_CLEAN.csv"

def stamp(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def deduplicate():
    stamp("="*80)
    stamp("DEDUPLICATING PREPROCESSED DATA")
    stamp("="*80)
    start = datetime.now()

    # Load data
    stamp("\n1. Loading preprocessed data...")
    df = pd.read_csv(INPUT_FILE, dtype=str, low_memory=False)
    initial_count = len(df)
    stamp(f"   Total records: {initial_count:,}")
    stamp(f"   Columns: {len(df.columns)}")

    # Check for duplicates
    stamp("\n2. Checking for duplicate BOL numbers...")
    bol_duplicates = df['Bill of Lading Number'].duplicated(keep='first').sum()
    stamp(f"   Found {bol_duplicates:,} duplicate BOL numbers")

    if bol_duplicates == 0:
        stamp("\n   No duplicates found. Data is clean.")
        return

    # Analyze duplicates
    stamp("\n3. Analyzing duplicates...")
    duplicate_bols = df[df['Bill of Lading Number'].duplicated(keep=False)]
    unique_duplicate_bols = duplicate_bols['Bill of Lading Number'].nunique()
    stamp(f"   Unique BOLs with duplicates: {unique_duplicate_bols:,}")
    stamp(f"   Total duplicate records: {len(duplicate_bols):,}")
    stamp(f"   Average duplicates per BOL: {len(duplicate_bols) / unique_duplicate_bols:.1f}")

    # Sample duplicates
    stamp("\n   Sample duplicate BOLs:")
    for i, bol in enumerate(duplicate_bols['Bill of Lading Number'].unique()[:5], 1):
        count = (duplicate_bols['Bill of Lading Number'] == bol).sum()
        stamp(f"   {i}. {bol} - {count} occurrences")

    # Remove duplicates
    stamp("\n4. Removing duplicates (keeping first occurrence)...")
    df_clean = df.drop_duplicates(subset=['Bill of Lading Number'], keep='first')
    final_count = len(df_clean)
    removed_count = initial_count - final_count

    stamp(f"   Before: {initial_count:,} records")
    stamp(f"   After:  {final_count:,} records")
    stamp(f"   Removed: {removed_count:,} duplicates ({removed_count/initial_count*100:.1f}%)")

    # Verify tonnage
    if 'Tons' in df.columns:
        tons_before = pd.to_numeric(df['Tons'], errors='coerce').sum()
        tons_after = pd.to_numeric(df_clean['Tons'], errors='coerce').sum()
        tons_removed = tons_before - tons_after
        stamp(f"\n   Tonnage before: {tons_before:,.0f}")
        stamp(f"   Tonnage after:  {tons_after:,.0f}")
        stamp(f"   Tonnage removed: {tons_removed:,.0f} ({tons_removed/tons_before*100:.1f}%)")

    # Save clean data
    stamp("\n5. Saving clean data...")
    df_clean.to_csv(OUTPUT_FILE, index=False)

    file_size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    stamp(f"   Saved: {OUTPUT_FILE.name}")
    stamp(f"   Records: {final_count:,}")
    stamp(f"   Size: {file_size_mb:.1f} MB")

    duration = (datetime.now() - start).total_seconds() / 60
    stamp(f"\n" + "="*80)
    stamp(f"DEDUPLICATION COMPLETE - Duration: {duration:.1f} minutes")
    stamp("="*80)

if __name__ == "__main__":
    deduplicate()
