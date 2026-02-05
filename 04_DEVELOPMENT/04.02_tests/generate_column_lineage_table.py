"""
Generate column lineage table showing transformation across all pipeline stages
"""
import pandas as pd
from pathlib import Path

BASE = Path(r"G:\My Drive\LLM\project_manifest")

# Define all stages and their files
stages = {
    "STAGE 1: Raw USACE Entrance": BASE / "04_DEVELOPMENT" / "04.02_tests" / "test_samples_15k" / "usace_entrance_2023_sample_15k.csv",
    "STAGE 2: Raw USACE Clearance": BASE / "04_DEVELOPMENT" / "04.02_tests" / "test_samples_15k" / "usace_clearance_2023_sample_15k.csv",
    "STAGE 3: Raw Panjiva Imports": BASE / "04_DEVELOPMENT" / "04.02_tests" / "test_samples_15k" / "panjiva_imports_2023_sample_15k.csv",
    "STAGE 4: Raw Panjiva Exports": BASE / "04_DEVELOPMENT" / "04.02_tests" / "test_samples_15k" / "panjiva_exports_2023_sample_15k.csv",
    "STAGE 5: Preprocessed Entrance": BASE / "00_DATA" / "00.02_PREPROCESSED" / "usace_2023_entrance_AUTHORITATIVE_v1.0.0.csv",
    "STAGE 6: Preprocessed Clearance": BASE / "00_DATA" / "00.02_PREPROCESSED" / "usace_2023_clearance_AUTHORITATIVE_v1.0.0.csv",
    "STAGE 7: Entrance + Import Flags": BASE / "00_DATA" / "00.03_MATCHED" / "usace_2023_entrance_with_import_flags_v2.0.0_20260116_1759.csv",
    "STAGE 8: Clearance + Export Flags": BASE / "00_DATA" / "00.03_MATCHED" / "usace_2023_clearance_with_export_flags_v2.0.0_20260116_1803.csv",
    "STAGE 9: Port Call Master SIMPLE": BASE / "00_DATA" / "00.04_FINAL" / "usace_2023_portcall_master_SIMPLE_v2.0.0_20260116_1804.csv"
}

print("="*120)
print("COLUMN LINEAGE TABLE - Pipeline Transformation Tracker")
print("="*120)
print("\nReading files...\n")

# Collect all data
lineage_data = []

for stage_name, file_path in stages.items():
    if not file_path.exists():
        print(f"[WARNING] File not found: {file_path}")
        continue

    print(f"Reading: {stage_name}")
    df = pd.read_csv(file_path, nrows=1)  # Just need first row for sample

    for col_num, col_name in enumerate(df.columns, start=1):
        sample_value = df.iloc[0][col_name]

        # Truncate long values
        if pd.notna(sample_value):
            sample_str = str(sample_value)
            if len(sample_str) > 50:
                sample_str = sample_str[:47] + "..."
        else:
            sample_str = "NULL"

        lineage_data.append({
            'Stage': stage_name,
            'Col_Num': col_num,
            'Column_Name': col_name,
            'Sample_Value': sample_str
        })

# Create DataFrame
lineage_df = pd.DataFrame(lineage_data)

# Save to CSV
output_csv = BASE / "04_DEVELOPMENT" / "04.02_tests" / "COLUMN_LINEAGE_TABLE.csv"
lineage_df.to_csv(output_csv, index=False)
print(f"\n[OK] Saved CSV: {output_csv.name}")

# Also create a summary showing NEW columns added at each stage
print("\n" + "="*120)
print("NEW COLUMNS ADDED AT EACH STAGE")
print("="*120)

prev_cols = set()
for stage_name in stages.keys():
    stage_data = lineage_df[lineage_df['Stage'] == stage_name]
    current_cols = set(stage_data['Column_Name'].tolist())
    new_cols = current_cols - prev_cols

    if new_cols:
        print(f"\n{stage_name}:")
        for col in sorted(new_cols):
            sample = stage_data[stage_data['Column_Name'] == col]['Sample_Value'].iloc[0]
            print(f"  + {col} = {sample}")

    prev_cols = current_cols

print("\n" + "="*120)
print(f"Total rows in lineage table: {len(lineage_df):,}")
print(f"Output: {output_csv}")
print("="*120)

# Also create a pivot view showing which columns exist in which stages
print("\n" + "="*120)
print("COLUMN PRESENCE ACROSS STAGES (Pivot View)")
print("="*120)

# Get unique columns
all_columns = lineage_df['Column_Name'].unique()

# Create pivot showing presence
pivot_data = []
for col in all_columns:
    row = {'Column_Name': col}
    for stage in stages.keys():
        exists = col in lineage_df[lineage_df['Stage'] == stage]['Column_Name'].values
        row[stage.split(':')[0]] = 'X' if exists else ''
    pivot_data.append(row)

pivot_df = pd.DataFrame(pivot_data)
pivot_csv = BASE / "04_DEVELOPMENT" / "04.02_tests" / "COLUMN_PRESENCE_PIVOT.csv"
pivot_df.to_csv(pivot_csv, index=False)
print(f"\n[OK] Saved pivot table: {pivot_csv.name}")

# Print key transformations
print("\n" + "="*120)
print("KEY COLUMN TRANSFORMATIONS")
print("="*120)

key_columns = ['Arrival_Date', 'Clearance_Date', 'IMO', 'Vessel', 'Has_Import_Manifest',
               'Import_VOY_RECID', 'Has_Export_Manifest', 'Export_VOY_RECID']

for col in key_columns:
    col_data = lineage_df[lineage_df['Column_Name'] == col]
    if len(col_data) > 0:
        print(f"\n{col}:")
        for _, row in col_data.iterrows():
            print(f"  {row['Stage']}: {row['Sample_Value']}")

print("\n" + "="*120)
print("COMPLETE - Check the CSV files for full details")
print("="*120)
