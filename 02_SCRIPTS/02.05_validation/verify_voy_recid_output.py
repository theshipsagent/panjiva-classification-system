import pandas as pd

# Load the output file
df = pd.read_csv(r"G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01.01_annual_files\panjiva_imports_2023_PORTCALL_v20260115_1530.csv")

print("="*80)
print("VOY_RECID OUTPUT VERIFICATION")
print("="*80)

print(f"\nTotal records: {len(df):,}")
print(f"Total columns: {len(df.columns)}")
print(f"Unique VOY_RECID values: {df['VOY_RECID'].nunique():,}")

print(f"\n\nColumns in output file:")
for i, col in enumerate(df.columns, 1):
    print(f"{i}. {col}")

print(f"\n\nFirst 5 records:")
display_cols = ['VOY_RECID', 'Vessel', 'Port of Discharge (D)', 'Arrival Date', 'Voyage', 'IMO', 'Group', 'Commodity', 'Group_Concat', 'Commodity_Concat']
available = [c for c in display_cols if c in df.columns]
print(df[available].head(10).to_string(index=False))

# Check for port calls with multiple cargo records
print(f"\n\nPort call size distribution:")
voy_counts = df.groupby('VOY_RECID').size()
print(f"  Min records per port call: {voy_counts.min()}")
print(f"  Median: {voy_counts.median():.0f}")
print(f"  Max: {voy_counts.max()}")

# Example of a large port call
largest_voy = voy_counts.idxmax()
print(f"\n\nLargest port call: {largest_voy} ({voy_counts.max()} cargo records)")
large_example = df[df['VOY_RECID'] == largest_voy][['VOY_RECID', 'Vessel', 'Port of Discharge (D)', 'Arrival Date', 'Group', 'Commodity', 'Group_Concat', 'Commodity_Concat']].head(5)
print(large_example.to_string(index=False))

# Check for multi-value concatenations
print(f"\n\nPort calls with multiple Groups (concatenated):")
df['Group_Concat'] = df['Group_Concat'].astype(str)
multi_groups = df[df['Group_Concat'].str.contains(',', na=False)][['VOY_RECID', 'Vessel', 'Port of Discharge (D)', 'Group_Concat']].drop_duplicates('VOY_RECID').head(3)
if len(multi_groups) > 0:
    print(multi_groups.to_string(index=False))
else:
    print("  (None found)")

print(f"\n\nPort calls with multiple Commodities (concatenated):")
df['Commodity_Concat'] = df['Commodity_Concat'].astype(str)
multi_comms = df[df['Commodity_Concat'].str.contains(',', na=False)][['VOY_RECID', 'Vessel', 'Port of Discharge (D)', 'Commodity_Concat']].drop_duplicates('VOY_RECID').head(3)
if len(multi_comms) > 0:
    print(multi_comms.to_string(index=False))
else:
    print("  (None found)")

print("\n" + "="*80)
print("VERIFICATION COMPLETE!")
print("="*80)
