"""
Quick diagnostic: Why are entrance->imports showing 0% match?
"""
import pandas as pd
from pathlib import Path

BASE = Path(r"G:\My Drive\LLM\project_manifest")
ENTRANCE = BASE / "00_DATA" / "00.02_PREPROCESSED" / "usace_2023_entrance_AUTHORITATIVE_v1.0.0.csv"
IMPORTS = BASE / "00_DATA" / "00.02_PREPROCESSED" / "panjiva_imports_2023_AUTHORITATIVE_v1.0.0.csv"

print("Loading data...")
entrance = pd.read_csv(ENTRANCE, low_memory=False)
imports = pd.read_csv(IMPORTS, low_memory=False)

print(f"\nEntrance records: {len(entrance):,}")
print(f"Import records: {len(imports):,}")

# Check IMO overlap
print("\n--- IMO Analysis ---")
ent_imos = set(entrance['IMO'].dropna().astype(int).astype(str))
imp_imos = set(imports['IMO'].dropna().astype(int).astype(str))
print(f"Entrance unique IMOs: {len(ent_imos):,}")
print(f"Imports unique IMOs: {len(imp_imos):,}")
print(f"IMO overlap: {len(ent_imos & imp_imos):,}")

# Check port overlap
print("\n--- Port Analysis ---")
print(f"Entrance PORT sample: {entrance['PORT'].head(10).tolist()}")
print(f"Imports Port of Discharge sample: {imports['Port of Discharge (D)'].head(10).tolist()}")

ent_ports = set(entrance['PORT'].dropna().astype(str).str.strip().str.upper())
imp_ports = set(imports['Port of Discharge (D)'].dropna().astype(str).str.strip().str.upper())
print(f"\nEntrance unique ports: {len(ent_ports):,}")
print(f"Imports unique ports: {len(imp_ports):,}")
print(f"Port overlap: {len(ent_ports & imp_ports):,}")

# Check date ranges
print("\n--- Date Analysis ---")
entrance['Arrival_Date_Parsed'] = pd.to_datetime(entrance['Arrival_Date'], errors='coerce')
imports['Arrival_Date_Parsed'] = pd.to_datetime(imports['Arrival Date'], errors='coerce')

print(f"Entrance date range: {entrance['Arrival_Date_Parsed'].min()} to {entrance['Arrival_Date_Parsed'].max()}")
print(f"Imports date range: {imports['Arrival_Date_Parsed'].min()} to {imports['Arrival_Date_Parsed'].max()}")

# Try to find a manual match
print("\n--- Manual Match Test ---")
test_ent = entrance[entrance['IMO'].notna()].iloc[0]
test_imo = str(int(test_ent['IMO']))
test_port = str(test_ent['PORT']).strip().upper()
test_date = test_ent['Arrival_Date_Parsed']

print(f"\nTest entrance record:")
print(f"  IMO: {test_imo}")
print(f"  PORT: {test_port}")
print(f"  Date: {test_date}")

# Look for matches in imports
import_matches = imports[
    (imports['IMO'].dropna().astype(int).astype(str) == test_imo)
]
print(f"\nImports with same IMO: {len(import_matches)}")

if len(import_matches) > 0:
    print("\nSample import match:")
    print(f"  IMO: {import_matches.iloc[0]['IMO']}")
    print(f"  Port: {import_matches.iloc[0]['Port of Discharge (D)']}")
    print(f"  Date: {import_matches.iloc[0]['Arrival Date']}")
