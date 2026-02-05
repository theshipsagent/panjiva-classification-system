"""Quick verification of v2.3.0 carrier SCAC codes"""
import pandas as pd
from pathlib import Path

DICT_FILE = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.3.0_20260113_1545.csv")

df = pd.read_csv(DICT_FILE, dtype=str)

# Show carrier rules with SCAC codes
carrier_rules = df[df['Carrier_SCAC'].notna() & (df['Carrier_SCAC'] != '')]

print("Carrier Rules with SCAC Codes:")
print("=" * 100)
for _, row in carrier_rules.iterrows():
    print(f"{row['Rule_ID']:30s} SCAC: {row['Carrier_SCAC']:6s} Name: {row['Carrier_Name']}")

print(f"\nTotal: {len(carrier_rules)} carrier rules with SCAC codes")
print(f"Total dictionary rules: {len(df)}")
