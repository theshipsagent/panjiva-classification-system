import pandas as pd
import re

def normalize_port_name(name):
    if pd.isna(name) or name == '':
        return ''
    name = str(name).upper()
    parts = name.split(',')
    if len(parts) > 0:
        city = parts[0].strip()
        city = city.replace('PORT OF ', '').replace('PORT ', '').replace('THE ', '')
        state = ''
        for part in parts:
            part_clean = part.strip()
            if len(part_clean) == 2 and part_clean.isalpha():
                state = part_clean
                break
        return f"{city}|{state}".upper()
    return name.upper()

# Load data
usace = pd.read_csv(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_inbound_entrance_transformed_v2.1.0.csv", low_memory=False)
panjiva = pd.read_csv(r"G:\My Drive\LLM\project_manifest\00_DATA/00.02_PREPROCESSED\01.01_annual_files\panjiva_imports_2023_PORTCALL_v20260115_1530.csv", low_memory=False)

panjiva_agg = panjiva.groupby('VOY_RECID').agg({'Port of Discharge (D)': 'first'}).reset_index()

print("="*80)
print("PORT NORMALIZATION DEBUGGING")
print("="*80)

print("\nUSACE Sample Ports (original -> normalized):")
for port in usace['Arrival_Port_Name'].dropna().unique()[:10]:
    normalized = normalize_port_name(port)
    print(f"  {port:<50} -> {normalized}")

print("\n\nPanjiva Sample Ports (original -> normalized):")
for port in panjiva_agg['Port of Discharge (D)'].dropna().unique()[:10]:
    normalized = normalize_port_name(port)
    print(f"  {port:<50} -> {normalized}")

# Check for overlaps
usace['Port_Norm'] = usace['Arrival_Port_Name'].apply(normalize_port_name)
panjiva_agg['Port_Norm'] = panjiva_agg['Port of Discharge (D)'].apply(normalize_port_name)

usace_ports = set(usace['Port_Norm'].dropna().unique())
panjiva_ports = set(panjiva_agg['Port_Norm'].dropna().unique())
common_ports = usace_ports.intersection(panjiva_ports)

print(f"\n\nPort Overlap After Normalization:")
print(f"  USACE unique ports: {len(usace_ports)}")
print(f"  Panjiva unique ports: {len(panjiva_ports)}")
print(f"  Common ports: {len(common_ports)}")

if len(common_ports) > 0:
    print(f"\n  Sample common ports:")
    for port in list(common_ports)[:20]:
        print(f"    {port}")
else:
    print("\n  NO COMMON PORTS FOUND!")
    print("\n  Sample USACE normalized ports:")
    for port in list(usace_ports)[:10]:
        print(f"    {port}")
    print("\n  Sample Panjiva normalized ports:")
    for port in list(panjiva_ports)[:10]:
        print(f"    {port}")
