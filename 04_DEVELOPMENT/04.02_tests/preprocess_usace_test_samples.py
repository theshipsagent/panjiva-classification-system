"""
Quick preprocessing: Transform USACE test samples
- Convert mmydd dates to actual timestamps
- Keep port codes as-is (we'll match by IMO + date only)
"""
import pandas as pd
from pathlib import Path

BASE = Path(r"G:\My Drive\LLM\project_manifest")
TEST_DIR = BASE / "00_DATA" / "00.02_PREPROCESSED"

def parse_usace_date(date_val):
    """Convert mmydd integer to timestamp (e.g., 8329 -> 2023-08-29)"""
    if pd.isna(date_val):
        return None
    try:
        date_str = str(int(date_val)).zfill(5)
        month = int(date_str[:2])
        year_digit = int(date_str[2])
        day = int(date_str[3:])
        year = 2020 + year_digit
        return pd.Timestamp(year=year, month=month, day=day)
    except:
        return None

print("="*80)
print("PREPROCESSING USACE TEST SAMPLES")
print("="*80)

# Process entrance
print("\n1. Processing entrance data...")
ent_file = TEST_DIR / "usace_2023_entrance_AUTHORITATIVE_v1.0.0.csv"
ent = pd.read_csv(ent_file, low_memory=False)
print(f"   Records: {len(ent):,}")
print(f"   Original Arrival_Date sample: {ent['Arrival_Date'].head(5).tolist()}")

# Convert dates
ent['Arrival_Date'] = ent['Arrival_Date'].apply(parse_usace_date)
print(f"   Converted Arrival_Date sample: {ent['Arrival_Date'].head(5).tolist()}")
print(f"   Date range: {ent['Arrival_Date'].min()} to {ent['Arrival_Date'].max()}")

# Save
ent.to_csv(ent_file, index=False)
print(f"   Saved: {ent_file.name}")

# Process clearance
print("\n2. Processing clearance data...")
clr_file = TEST_DIR / "usace_2023_clearance_AUTHORITATIVE_v1.0.0.csv"
clr = pd.read_csv(clr_file, low_memory=False)
print(f"   Records: {len(clr):,}")

# Clearance date column might be different - check what it's called
if 'Clearance_Date' in clr.columns:
    date_col = 'Clearance_Date'
elif 'ECDATE' in clr.columns:
    date_col = 'ECDATE'
    clr = clr.rename(columns={'ECDATE': 'Clearance_Date'})
else:
    # Find any column with 'date' in name
    date_cols = [c for c in clr.columns if 'date' in c.lower()]
    if date_cols:
        date_col = date_cols[0]
        clr = clr.rename(columns={date_col: 'Clearance_Date'})
    else:
        print(f"   [ERROR] No date column found! Columns: {clr.columns.tolist()[:10]}")
        date_col = None

if date_col:
    print(f"   Original {date_col} sample: {clr['Clearance_Date'].head(5).tolist()}")
    clr['Clearance_Date'] = clr['Clearance_Date'].apply(parse_usace_date)
    print(f"   Converted Clearance_Date sample: {clr['Clearance_Date'].head(5).tolist()}")
    print(f"   Date range: {clr['Clearance_Date'].min()} to {clr['Clearance_Date'].max()}")

# Save
clr.to_csv(clr_file, index=False)
print(f"   Saved: {clr_file.name}")

print("\n" + "="*80)
print("PREPROCESSING COMPLETE")
print("="*80)
print("\nNote: Port codes remain numeric - matching will use IMO + date only")
