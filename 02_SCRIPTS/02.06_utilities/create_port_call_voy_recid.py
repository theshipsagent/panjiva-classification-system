"""
Create Port Call Voyage Record ID (VOY_RECID) for Panjiva Data
Version: 1.0.0
Date: 2026-01-15

Purpose:
- Group Panjiva cargo records by "port call" (vessel arrival event)
- Assign unique VOY_RECID to each port call
- Allows matching USACE single-row entrance data to multiple Panjiva cargo records

Grouping Keys:
- Vessel
- Port of Discharge (D)
- Arrival Date
- Voyage
- IMO
- Carrier Name

Concatenation (within each group):
- Group: Comma-separated list of unique values
- Commodity: Comma-separated list of unique values
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# File paths
INPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01.01_annual_files\panjiva_imports_2023_FILTERED_v20260114_1236.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01.01_annual_files\panjiva_imports_2023_PORTCALL_v20260115_1530.csv")

print("="*80)
print("PANJIVA PORT CALL VOY_RECID CREATOR v1.0.0")
print("="*80)

# Load data
print(f"\n1. Loading data from: {INPUT_FILE.name}")
df = pd.read_csv(INPUT_FILE)
print(f"   Total records: {len(df):,}")

# Define grouping columns
GROUP_COLS = [
    'Vessel',
    'Port of Discharge (D)',
    'Arrival Date',
    'Voyage',
    'IMO',
    'Carrier Name'
]

print(f"\n2. Grouping by port call ({len(GROUP_COLS)} columns):")
for col in GROUP_COLS:
    print(f"   - {col}")

# Create a unique port call identifier for aggregation
print("\n3. Creating port call groupings...")
df['_temp_groupkey'] = (
    df['Vessel'].astype(str) + '|' +
    df['Port of Discharge (D)'].astype(str) + '|' +
    df['Arrival Date'].astype(str) + '|' +
    df['Voyage'].astype(str) + '|' +
    df['IMO'].astype(str) + '|' +
    df['Carrier Name'].astype(str)
)

# Get unique port calls and assign VOY_RECID
print("\n4. Assigning unique VOY_RECID to each port call...")
unique_groups = df['_temp_groupkey'].unique()
print(f"   Total unique port calls: {len(unique_groups):,}")

# Create mapping dictionary
group_to_recid = {group: f"VOY_{i+1:07d}" for i, group in enumerate(unique_groups)}

# Assign VOY_RECID to all records
df['VOY_RECID'] = df['_temp_groupkey'].map(group_to_recid)

# For each port call, concatenate unique Group and Commodity values
print("\n5. Concatenating Group and Commodity values within each port call...")

def concat_unique(series):
    """Concatenate unique non-null values, comma-separated"""
    unique_vals = series.dropna().unique()
    if len(unique_vals) == 0:
        return np.nan
    return ', '.join(sorted(str(v) for v in unique_vals))

# Create aggregation for Group and Commodity
group_aggregations = df.groupby('_temp_groupkey').agg({
    'Group': concat_unique,
    'Commodity': concat_unique
})

# Rename columns to indicate they're concatenated
group_aggregations.columns = ['Group_Concat', 'Commodity_Concat']

# Map back to original dataframe
df = df.merge(
    group_aggregations,
    left_on='_temp_groupkey',
    right_index=True,
    how='left'
)

# Drop temporary grouping key
df.drop('_temp_groupkey', axis=1, inplace=True)

# Reorder columns to put VOY_RECID, Group_Concat, Commodity_Concat near the front
cols = df.columns.tolist()
# Move these columns after RAW_REC_ID (or at the beginning if RAW_REC_ID doesn't exist)
if 'RAW_REC_ID' in cols:
    idx = cols.index('RAW_REC_ID') + 1
else:
    idx = 0

# Remove VOY_RECID, Group_Concat, Commodity_Concat from their current positions
for col in ['VOY_RECID', 'Group_Concat', 'Commodity_Concat']:
    if col in cols:
        cols.remove(col)

# Insert at desired position
cols.insert(idx, 'VOY_RECID')
cols.insert(idx + 1, 'Group_Concat')
cols.insert(idx + 2, 'Commodity_Concat')

df = df[cols]

# Save results
print(f"\n6. Saving results to: {OUTPUT_FILE.name}")
df.to_csv(OUTPUT_FILE, index=False)

# Print summary statistics
print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

print(f"\nTotal records processed: {len(df):,}")
print(f"Unique port calls (VOY_RECID): {df['VOY_RECID'].nunique():,}")
print(f"Average cargo records per port call: {len(df) / df['VOY_RECID'].nunique():.1f}")

# Show distribution of records per port call
records_per_call = df.groupby('VOY_RECID').size()
print(f"\nRecords per port call distribution:")
print(f"  Min: {records_per_call.min()}")
print(f"  25th percentile: {records_per_call.quantile(0.25):.0f}")
print(f"  Median: {records_per_call.median():.0f}")
print(f"  75th percentile: {records_per_call.quantile(0.75):.0f}")
print(f"  Max: {records_per_call.max()}")

# Show examples of concatenated groups
print(f"\nExample port calls with multiple Groups:")
multi_group = df[df['Group_Concat'].str.contains(',', na=False)][['VOY_RECID', 'Vessel', 'Port of Discharge (D)', 'Arrival Date', 'Group_Concat']].drop_duplicates('VOY_RECID').head(3)
if len(multi_group) > 0:
    print(multi_group.to_string(index=False))
else:
    print("  (None found)")

print(f"\nExample port calls with multiple Commodities:")
multi_commodity = df[df['Commodity_Concat'].str.contains(',', na=False)][['VOY_RECID', 'Vessel', 'Port of Discharge (D)', 'Arrival Date', 'Commodity_Concat']].drop_duplicates('VOY_RECID').head(3)
if len(multi_commodity) > 0:
    print(multi_commodity.to_string(index=False))
else:
    print("  (None found)")

# Show sample of output
print(f"\n" + "="*80)
print("SAMPLE OUTPUT (First 5 records)")
print("="*80)
display_cols = ['VOY_RECID', 'Vessel', 'Port of Discharge (D)', 'Arrival Date', 'Voyage', 'IMO', 'Group', 'Commodity', 'Group_Concat', 'Commodity_Concat']
available_display_cols = [c for c in display_cols if c in df.columns]
print(df[available_display_cols].head(5).to_string(index=False))

print(f"\n" + "="*80)
print("COMPLETE!")
print("="*80)
print(f"\nOutput file: {OUTPUT_FILE}")
print(f"Total columns: {len(df.columns)}")
print(f"Total records: {len(df):,}")
