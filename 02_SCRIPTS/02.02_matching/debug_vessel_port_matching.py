import pandas as pd
import numpy as np

# Load data
usace = pd.read_csv(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_inbound_entrance_transformed_v2.1.0.csv", low_memory=False)
panjiva = pd.read_csv(r"G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01.01_annual_files\panjiva_imports_2023_PORTCALL_v20260115_1530.csv", low_memory=False)

# Aggregate Panjiva by VOY_RECID
panjiva_agg = panjiva.groupby('VOY_RECID').agg({
    'Vessel': 'first',
    'Port of Discharge (D)': 'first',
    'Arrival Date': 'first',
}).reset_index()

print("="*80)
print("DEBUGGING VESSEL AND PORT MATCHING")
print("="*80)

# Sample vessel names
print("\nUSACE Sample Vessel Names (first 20):")
print(usace['Vessel'].head(20).tolist())

print("\nPanjiva Sample Vessel Names (first 20):")
print(panjiva_agg['Vessel'].head(20).tolist())

# Sample port names
print("\n\nUSACE Sample Port Names (first 20):")
print(usace['Arrival_Port_Name'].head(20).tolist())

print("\nPanjiva Sample Port Names (first 20):")
print(panjiva_agg['Port of Discharge (D)'].head(20).tolist())

# Check for common vessels
usace_vessels = set(usace['Vessel'].dropna().unique())
panjiva_vessels = set(panjiva_agg['Vessel'].dropna().unique())
common_vessels = usace_vessels.intersection(panjiva_vessels)

print(f"\n\nVessel Name Overlap:")
print(f"  USACE unique vessels: {len(usace_vessels):,}")
print(f"  Panjiva unique vessels: {len(panjiva_vessels):,}")
print(f"  Common vessels (exact match): {len(common_vessels):,}")

if len(common_vessels) > 0:
    print(f"\n  Sample common vessels:")
    for v in list(common_vessels)[:10]:
        print(f"    - {v}")

# Check for common ports
usace_ports = set(usace['Arrival_Port_Name'].dropna().unique())
panjiva_ports = set(panjiva_agg['Port of Discharge (D)'].dropna().unique())
common_ports = usace_ports.intersection(panjiva_ports)

print(f"\n\nPort Name Overlap:")
print(f"  USACE unique ports: {len(usace_ports):,}")
print(f"  Panjiva unique ports: {len(panjiva_ports):,}")
print(f"  Common ports (exact match): {len(common_ports):,}")

if len(common_ports) > 0:
    print(f"\n  Sample common ports:")
    for p in list(common_ports)[:10]:
        print(f"    - {p}")

# Check a specific example - find a vessel that appears in both
print("\n\n" + "="*80)
print("DETAILED EXAMPLE: TONSBERG")
print("="*80)

usace_tonsberg = usace[usace['Vessel'] == 'TONSBERG'][['Vessel', 'Arrival_Port_Name', 'Arrival_Date']].head(5)
print("\nUSACE records for TONSBERG:")
if len(usace_tonsberg) > 0:
    print(usace_tonsberg.to_string(index=False))
else:
    print("  (Not found in USACE)")

panjiva_tonsberg = panjiva_agg[panjiva_agg['Vessel'] == 'TONSBERG'][['Vessel', 'Port of Discharge (D)', 'Arrival Date']].head(5)
print("\nPanjiva port calls for TONSBERG:")
if len(panjiva_tonsberg) > 0:
    print(panjiva_tonsberg.to_string(index=False))
else:
    print("  (Not found in Panjiva)")

# Try normalized comparison
def normalize_vessel(name):
    if pd.isna(name):
        return ''
    return str(name).upper().strip()

def normalize_port(name):
    if pd.isna(name):
        return ''
    return str(name).upper().strip().replace(' PORT', '').replace('PORT OF ', '').replace(',', '')

usace['Vessel_Norm'] = usace['Vessel'].apply(normalize_vessel)
usace['Port_Norm'] = usace['Arrival_Port_Name'].apply(normalize_port)
panjiva_agg['Vessel_Norm'] = panjiva_agg['Vessel'].apply(normalize_vessel)
panjiva_agg['Port_Norm'] = panjiva_agg['Port of Discharge (D)'].apply(normalize_port)

usace_vessels_norm = set(usace['Vessel_Norm'].dropna().unique())
panjiva_vessels_norm = set(panjiva_agg['Vessel_Norm'].dropna().unique())
common_vessels_norm = usace_vessels_norm.intersection(panjiva_vessels_norm)

print("\n\n" + "="*80)
print("NORMALIZED COMPARISON")
print("="*80)

print(f"\nVessel overlap (normalized):")
print(f"  Common vessels: {len(common_vessels_norm):,}")

if len(common_vessels_norm) > 0:
    print(f"  Sample:")
    for v in list(common_vessels_norm)[:20]:
        print(f"    - {v}")

usace_ports_norm = set(usace['Port_Norm'].dropna().unique())
panjiva_ports_norm = set(panjiva_agg['Port_Norm'].dropna().unique())
common_ports_norm = usace_ports_norm.intersection(panjiva_ports_norm)

print(f"\nPort overlap (normalized):")
print(f"  Common ports: {len(common_ports_norm):,}")

if len(common_ports_norm) > 0:
    print(f"  Sample:")
    for p in list(common_ports_norm)[:20]:
        print(f"    - {p}")
