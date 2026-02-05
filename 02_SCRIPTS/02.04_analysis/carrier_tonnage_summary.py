"""
Generate carrier tonnage and record count summary from raw merged data
Analyzes all 3 years (2023-2025) combined

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def stamp(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Paths
DATA_DIR = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01_01_panjiva_imports_step_one")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\user_notes\carrier_tonnage_summary_all_years.csv")

files = [
    DATA_DIR / "panjiva_imports_2023_20260112_STAGE00_v20260112_2052.csv",
    DATA_DIR / "panjiva_imports_2024_20260112_STAGE00_v20260112_2052.csv",
    DATA_DIR / "panjiva_imports_2025_20260112_STAGE00_v20260112_2052.csv"
]

stamp("=== Carrier Tonnage Summary ===")
stamp("")

# Load all years
all_data = []
for file in files:
    year = file.stem.split('_')[2]
    stamp(f"Loading {year}...")
    df = pd.read_csv(file, dtype=str)
    df['Year'] = year
    all_data.append(df)
    stamp(f"  {len(df):,} records")

# Combine
stamp("")
stamp("Combining all years...")
df_all = pd.concat(all_data, ignore_index=True)
stamp(f"Total records: {len(df_all):,}")
stamp("")

# Convert Tons to numeric
df_all['Tons_Numeric'] = pd.to_numeric(df_all['Tons'], errors='coerce').fillna(0)

# Group by Carrier
stamp("Grouping by carrier...")
carrier_summary = df_all.groupby('Carrier', dropna=False).agg({
    'Tons_Numeric': 'sum',
    'Carrier': 'count'
}).rename(columns={
    'Tons_Numeric': 'Total_Tons',
    'Carrier': 'Record_Count'
}).reset_index()

# Sort by tonnage descending
carrier_summary = carrier_summary.sort_values('Total_Tons', ascending=False)

# Split Carrier into SCAC and Name
def split_carrier(carrier_str):
    """Split 'XXXX - Carrier Name' into SCAC and Name"""
    carrier_str = str(carrier_str)
    if ' - ' in carrier_str:
        parts = carrier_str.split(' - ', 1)
        scac = parts[0].strip()
        name = parts[1].strip()
        return scac, name
    else:
        # No dash, treat whole thing as name
        return '', carrier_str.strip()

carrier_summary[['SCAC', 'Carrier_Name']] = carrier_summary['Carrier'].apply(
    lambda x: pd.Series(split_carrier(x))
)

# Drop original combined column
carrier_summary = carrier_summary.drop(columns=['Carrier'])

# Reorder columns: Rank, SCAC, Carrier_Name, Total_Tons, Record_Count
carrier_summary = carrier_summary[['SCAC', 'Carrier_Name', 'Total_Tons', 'Record_Count']]

# Add rank
carrier_summary.insert(0, 'Rank', range(1, len(carrier_summary) + 1))

# Format tonnage
carrier_summary['Total_Tons'] = carrier_summary['Total_Tons'].astype(int)

stamp(f"Found {len(carrier_summary)} unique carriers")
stamp("")

# Show top 20
stamp("Top 20 carriers by tonnage:")
for _, row in carrier_summary.head(20).iterrows():
    scac = str(row['SCAC'])[:10]
    name = str(row['Carrier_Name'])[:35]
    tons = f"{row['Total_Tons']:,}"
    records = f"{row['Record_Count']:,}"
    stamp(f"  {row['Rank']:3d}. {scac:6s} - {name:35s} {tons:>15s} tons  {records:>8s} records")

stamp("")

# Save
stamp(f"Saving to: {OUTPUT_FILE}")
carrier_summary.to_csv(OUTPUT_FILE, index=False)

stamp("")
stamp("=== Summary Statistics ===")
stamp(f"Total carriers: {len(carrier_summary):,}")
stamp(f"Total tonnage: {carrier_summary['Total_Tons'].sum():,.0f} tons")
stamp(f"Total records: {carrier_summary['Record_Count'].sum():,}")
stamp("")
stamp("Complete!")
