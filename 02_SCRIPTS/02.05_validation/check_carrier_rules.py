"""Check carrier rule criteria"""
import pandas as pd
from pathlib import Path

DICTIONARY = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.3.0_20260113_1545.csv")

df = pd.read_csv(DICTIONARY, dtype=str)
carrier_rules = df[df['Carrier_SCAC'].notna() & (df['Carrier_SCAC'] != '')]

print("=== CARRIER RULES CRITERIA ===\n")
for _, r in carrier_rules.iterrows():
    print(f"Rule: {r['Rule_ID']}")
    print(f"  Phase: {r.get('Phase', '')}, Tier: {r.get('Tier', '')}")
    print(f"  SCAC: {r['Carrier_SCAC']}")
    print(f"  Vessel_Type: {r.get('Vessel_Type', 'NONE')}")
    print(f"  Keywords: {str(r.get('Keywords', 'NONE'))[:60]}")
    print(f"  Exclude_Keywords: {r.get('Exclude_Keywords', 'NONE')}")
    print(f"  Min_Tons: {r.get('Min_Tons', 'NONE')}, Max_Tons: {r.get('Max_Tons', 'NONE')}")
    print(f"  Lock levels: Group={r.get('Lock_Group', '')}, Commodity={r.get('Lock_Commodity', '')}, Cargo={r.get('Lock_Cargo', '')}, Cargo_Detail={r.get('Lock_Cargo_Detail', '')}")
    print(f"  Classification: {r.get('Group', '')} > {r.get('Commodity', '')} > {r.get('Cargo', '')} > {r.get('Cargo_Detail', '')}")
    print()
