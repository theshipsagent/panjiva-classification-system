"""
Create 3-Month Test Sample for Party Harmonization
===================================================
Extract a 3-month sample from production data for safe testing.

Author: WSD3 / Claude Code
Date: 2026-02-09

Strategy: Extract Q1 2024 (Jan-Mar) for testing
- Represents ~25% of year (3/12 months)
- Includes seasonal variety
- Safe to test without affecting production data

Input:  panjiva_imports_2024_AUTHORITATIVE_v2.0.0.csv
Output: panjiva_imports_2024_Q1_TEST_SAMPLE.csv
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(r"G:\My Drive\LLM\project_manifest")
INPUT_DIR = BASE_DIR / "00_DATA" / "00.02_PREPROCESSED"
OUTPUT_DIR = BASE_DIR / "05_TASKS" / "05.01_party_harmonization"

def create_sample(year=2024, months=[1, 2, 3]):
    """
    Create 3-month test sample.

    Args:
        year: Year to sample from
        months: List of months to include (1-12)

    Returns:
        Path to sample file
    """
    print(f"\n{'='*80}")
    print(f"CREATE 3-MONTH TEST SAMPLE")
    print(f"{'='*80}")
    print(f"Year: {year}")
    print(f"Months: {', '.join([datetime(year, m, 1).strftime('%B') for m in months])}")

    # Input file - use ALL_YEARS file
    input_file = INPUT_DIR / "panjiva_ALL_YEARS_preprocessed.csv"

    if not input_file.exists():
        print(f"\nERROR: Input file not found: {input_file}")
        return None

    # Load data
    print(f"\nLoading data: {input_file.name}")
    df = pd.read_csv(input_file, encoding='utf-8-sig', low_memory=False)
    print(f"  Loaded {len(df):,} records")
    print(f"  Total tonnage: {df['Tons'].sum():,.0f} tons")

    # Check if Arrival Date column exists
    date_col = None
    for col in ['Arrival Date', 'ArrivalDate', 'Date']:
        if col in df.columns:
            date_col = col
            break

    if date_col is None:
        print(f"\nERROR: No date column found in data")
        print(f"  Available columns: {', '.join(df.columns[:10])}...")
        return None

    print(f"\nUsing date column: '{date_col}'")

    # Parse dates
    print("\nParsing dates...")
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

    # Check for invalid dates
    invalid_dates = df[date_col].isna().sum()
    if invalid_dates > 0:
        print(f"  WARNING: {invalid_dates:,} records have invalid dates")

    # Extract year and month
    df['Year'] = df[date_col].dt.year
    df['Month'] = df[date_col].dt.month

    # Filter to specified year first
    print(f"\nFiltering to year {year}...")
    df_year = df[df['Year'] == year].copy()
    print(f"  Records in {year}: {len(df_year):,}")

    # Filter to specified months
    print(f"\nFiltering to months: {months}")
    df_sample = df_year[df_year['Month'].isin(months)].copy()

    # Remove temporary columns
    df_sample = df_sample.drop(columns=['Year', 'Month'])

    print(f"\n  Sample records: {len(df_sample):,} ({len(df_sample)/len(df)*100:.1f}% of year)")
    print(f"  Sample tonnage: {df_sample['Tons'].sum():,.0f} tons ({df_sample['Tons'].sum()/df['Tons'].sum()*100:.1f}% of year)")

    # Month breakdown
    print(f"\n  Month-by-month breakdown:")
    df_year_months = df_year[df_year['Month'].isin(months)]
    for month in months:
        month_data = df_year_months[df_year_months['Month'] == month]
        month_name = datetime(year, month, 1).strftime('%B')
        print(f"    {month_name:10s}: {len(month_data):7,} records  |  {month_data['Tons'].sum():12,.0f} tons")

    # Output file
    output_file = OUTPUT_DIR / f"panjiva_imports_{year}_Q1_TEST_SAMPLE.csv"

    # Save sample
    print(f"\nSaving test sample...")
    df_sample.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"  Saved: {output_file.name}")
    print(f"  Size: {output_file.stat().st_size / (1024*1024):.1f} MB")

    # Summary statistics
    print(f"\n{'='*80}")
    print("SAMPLE SUMMARY")
    print(f"{'='*80}")
    print(f"Records: {len(df_sample):,}")
    print(f"Tonnage: {df_sample['Tons'].sum():,.0f} tons")
    print(f"Columns: {len(df_sample.columns)}")
    print(f"Date Range: {df_sample[date_col].min()} to {df_sample[date_col].max()}")

    # Top 5 commodities (if HS4 exists)
    if 'HS4' in df_sample.columns:
        print(f"\nTop 5 HS4 Codes:")
        top_hs4 = df_sample.groupby('HS4').agg({
            'REC_ID': 'count',
            'Tons': 'sum'
        }).sort_values('Tons', ascending=False).head(5)

        for hs4, row in top_hs4.iterrows():
            print(f"  {hs4}: {int(row['REC_ID']):,} records  |  {row['Tons']:,.0f} tons")

    # Top 5 shippers (if Shipper exists)
    if 'Shipper' in df_sample.columns:
        print(f"\nTop 5 Shippers by tonnage:")
        top_shippers = df_sample[df_sample['Shipper'].notna()].groupby('Shipper').agg({
            'REC_ID': 'count',
            'Tons': 'sum'
        }).sort_values('Tons', ascending=False).head(5)

        for shipper, row in top_shippers.iterrows():
            shipper_short = shipper[:50] + '...' if len(shipper) > 50 else shipper
            print(f"  {shipper_short}")
            print(f"    {int(row['REC_ID']):,} records  |  {row['Tons']:,.0f} tons")

    print(f"\n{'='*80}")
    print("SAMPLE CREATION COMPLETE")
    print(f"{'='*80}")
    print(f"File: {output_file}")
    print(f"\nReady for testing!")
    print(f"Next step: Run harmonization on this sample")

    return output_file

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Create 3-month test sample for party harmonization')
    parser.add_argument('--year', type=int, default=2024, help='Year to sample from (default: 2024)')
    parser.add_argument('--months', type=int, nargs='+', default=[1, 2, 3],
                       help='Months to include (default: 1 2 3 for Q1)')

    args = parser.parse_args()

    create_sample(year=args.year, months=args.months)
