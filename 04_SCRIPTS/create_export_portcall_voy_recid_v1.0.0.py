"""
Create Export Port Call Groups with VOY_RECID
Version: 1.0.0
Date: 2026-01-15

Purpose:
- Group export manifest records by unique vessel departure (port call)
- Create VOY_RECID identifier for each export port call
- Aggregate cargo records: concatenate Groups/Commodities, sum tonnage

Grouping Keys (Note: Voyage and IMO missing in export data):
- Vessel
- Port of Lading (US export port)
- Shipment Date
- Carrier

Input: 01_STAGE01_PREPROCESSING/01.01_annual_files/panjiva_exports_2023_PREPROCESSED_*.csv
Output: 01_STAGE01_PREPROCESSING/01.01_annual_files/panjiva_exports_2023_PORTCALL_*.csv
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

print("="*80)
print("CREATE EXPORT PORT CALL GROUPS (VOY_RECID) v1.0.0")
print("="*80)

# File paths
INPUT_DIR = Path(r"G:\My Drive\LLM\project_manifest\01_STAGE01_PREPROCESSING\01.01_annual_files")
OUTPUT_DIR = INPUT_DIR

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# Find latest preprocessed export file
print(f"\n1. Finding latest preprocessed export file...")
export_files = list(INPUT_DIR.glob("panjiva_exports_2023_PREPROCESSED_*.csv"))
if not export_files:
    print("   ERROR: No preprocessed export files found!")
    exit(1)

# Sort by name (timestamps in filename) and take latest
export_files.sort()
input_file = export_files[-1]
print(f"   Loading: {input_file.name}")

# Load data
df = pd.read_csv(input_file, low_memory=False)
print(f"   Records loaded: {len(df):,}")
print(f"   Columns: {len(df.columns)}")

# Define grouping columns
# Note: Voyage and IMO are MISSING in export data, so we group by fewer keys
GROUP_COLS = [
    'Vessel',
    'Port of Lading',
    'Shipment Date',
    'Carrier'
]

print(f"\n2. Grouping by port call...")
print(f"   Grouping keys: {', '.join(GROUP_COLS)}")

# Check if all grouping columns exist
missing_cols = [col for col in GROUP_COLS if col not in df.columns]
if missing_cols:
    print(f"   ERROR: Missing columns: {missing_cols}")
    exit(1)

# Create temporary grouping key
df['_temp_groupkey'] = (
    df['Vessel'].astype(str) + '|' +
    df['Port of Lading'].astype(str) + '|' +
    df['Shipment Date'].astype(str) + '|' +
    df['Carrier'].astype(str)
)

# Count unique port calls
unique_groups = df['_temp_groupkey'].unique()
print(f"   Unique port calls found: {len(unique_groups):,}")

# Assign VOY_RECID (use VOY_EXP_ prefix for exports)
print(f"\n3. Assigning VOY_RECID...")
group_to_recid = {group: f"VOY_EXP_{i+1:07d}" for i, group in enumerate(unique_groups)}
df['VOY_RECID'] = df['_temp_groupkey'].map(group_to_recid)

print(f"   VOY_RECID range: {df['VOY_RECID'].min()} to {df['VOY_RECID'].max()}")

# Aggregate by VOY_RECID
print(f"\n4. Aggregating cargo data by port call...")

def concat_unique(series):
    """Concatenate unique non-null values with comma separator"""
    values = series.dropna().unique()
    values = [str(v).strip() for v in values if str(v).strip() and str(v) != 'nan']
    return ', '.join(sorted(set(values))) if values else ''

# Check if Group and Commodity columns exist
has_group = 'Group' in df.columns
has_commodity = 'Commodity' in df.columns

agg_dict = {
    'Vessel': 'first',
    'Port of Lading': 'first',
    'Shipment Date': 'first',
    'Carrier': 'first',
    'Shipper': 'first',
    'Tons': 'sum'
}

# Add Group and Commodity if they exist
if has_group:
    agg_dict['Group'] = concat_unique
if has_commodity:
    agg_dict['Commodity'] = concat_unique

df_portcall = df.groupby('VOY_RECID').agg(agg_dict).reset_index()

# Rename aggregated columns
df_portcall.columns = ['VOY_RECID', 'Vessel', 'Port_of_Lading', 'Shipment_Date',
                        'Carrier', 'Shipper', 'Total_Tons'] + \
                       (['Group_Concat'] if has_group else []) + \
                       (['Commodity_Concat'] if has_commodity else [])

print(f"   Port call records created: {len(df_portcall):,}")

# Calculate average records per port call
avg_records = len(df) / len(df_portcall)
print(f"   Average cargo records per port call: {avg_records:.1f}")

# Save port call file
output_file = OUTPUT_DIR / f"panjiva_exports_2023_PORTCALL_v{timestamp}.csv"
df_portcall.to_csv(output_file, index=False)
print(f"\n5. Saved: {output_file.name}")
print(f"   Columns: {len(df_portcall.columns)}")

# Summary statistics
print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

print(f"\nInput records: {len(df):,}")
print(f"Unique port calls (VOY_RECID): {len(df_portcall):,}")
print(f"Consolidation ratio: {avg_records:.1f} records per port call")

print(f"\nTonnage statistics:")
print(f"  Total tonnage: {df_portcall['Total_Tons'].sum():,.0f} tons")
print(f"  Average per port call: {df_portcall['Total_Tons'].mean():,.0f} tons")
print(f"  Median per port call: {df_portcall['Total_Tons'].median():,.0f} tons")

print(f"\nTop 10 ports by export volume:")
top_ports = df_portcall.groupby('Port_of_Lading')['Total_Tons'].sum().sort_values(ascending=False).head(10)
for port, tons in top_ports.items():
    print(f"  {port:<50} {tons:>12,.0f} tons")

print(f"\nTop 10 carriers by export volume:")
top_carriers = df_portcall.groupby('Carrier')['Total_Tons'].sum().sort_values(ascending=False).head(10)
for carrier, tons in top_carriers.items():
    carrier_name = str(carrier)[:50] if pd.notna(carrier) else 'Unknown'
    print(f"  {carrier_name:<50} {tons:>12,.0f} tons")

# Verify carrier consistency within port calls
print(f"\n" + "="*80)
print("QUALITY CHECKS")
print("="*80)

# Check for any records with missing VOY_RECID
missing_voy = df['VOY_RECID'].isna().sum()
if missing_voy > 0:
    print(f"\n[WARNING] {missing_voy} records missing VOY_RECID!")
else:
    print(f"\n[OK] All records have VOY_RECID")

# Sample port calls
print(f"\n" + "="*80)
print("SAMPLE PORT CALLS (First 5)")
print("="*80)
sample_cols = ['VOY_RECID', 'Vessel', 'Port_of_Lading', 'Shipment_Date', 'Carrier', 'Total_Tons']
available_cols = [c for c in sample_cols if c in df_portcall.columns]
if len(available_cols) > 0:
    try:
        print(df_portcall[available_cols].head(5).to_string(index=False))
    except UnicodeEncodeError:
        print("   [Sample display skipped due to unicode characters in port/vessel names]")

print(f"\n" + "="*80)
print("COMPLETE!")
print("="*80)
print(f"\nNext step: Match USACE clearance records to these export port calls")
print(f"Output file: {output_file.name}")
