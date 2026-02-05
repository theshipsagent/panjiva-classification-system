import pandas as pd

# Read first few rows to check structure
df = pd.read_csv(r"G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01.01_annual_files\panjiva_imports_2023_FILTERED_v20260114_1236.csv", nrows=10)

print("Column names:")
for i, col in enumerate(df.columns, 1):
    print(f"{i}. {col}")

print("\n\nFirst 3 rows of key columns:")
key_cols = ['Vessel', 'Port of Discharge (D)', 'Arrival Date', 'Voyage', 'IMO', 'Carrier Name', 'Group', 'Commodity']
available_cols = [c for c in key_cols if c in df.columns]
print(df[available_cols].head(3).to_string())

print(f"\n\nTotal records in file: {len(pd.read_csv(r'G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01.01_annual_files\panjiva_imports_2023_FILTERED_v20260114_1236.csv'))}")
