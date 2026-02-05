"""
Deep diagnostic: Understand why NO matches between entrance and imports
"""
import pandas as pd
from pathlib import Path

BASE = Path(r"G:\My Drive\LLM\project_manifest")
ENTRANCE = BASE / "00_DATA" / "00.02_PREPROCESSED" / "usace_2023_entrance_AUTHORITATIVE_v1.0.0.csv"
IMPORTS = BASE / "00_DATA" / "00.02_PREPROCESSED" / "panjiva_imports_2023_AUTHORITATIVE_v1.0.0.csv"

print("="*80)
print("DEEP DIAGNOSTIC: Why NO matches?")
print("="*80)

# Load
entrance = pd.read_csv(ENTRANCE, low_memory=False)
imports = pd.read_csv(IMPORTS, low_memory=False)

print(f"\nEntrance: {len(entrance):,} records")
print(f"Imports: {len(imports):,} records")

# Check IMO overlap
print("\n--- IMO OVERLAP CHECK ---")
ent_imos = set(entrance['IMO'].dropna().astype(int).astype(str))
imp_imos = set(imports['IMO'].dropna().astype(int).astype(str))

print(f"Entrance unique IMOs: {len(ent_imos):,}")
print(f"Imports unique IMOs: {len(imp_imos):,}")
print(f"OVERLAP: {len(ent_imos & imp_imos):,}")

if len(ent_imos & imp_imos) > 0:
    overlap_imos = list(ent_imos & imp_imos)[:10]
    print(f"\nSample overlapping IMOs: {overlap_imos}")

    # Test one overlapping IMO
    test_imo = overlap_imos[0]
    print(f"\n--- Testing IMO {test_imo} ---")

    # Find in entrance (handle NaN values)
    ent_imo_series = entrance['IMO'].apply(lambda x: str(int(x)) if pd.notna(x) else '')
    ent_matches = entrance[ent_imo_series == test_imo]
    print(f"Entrance records with this IMO: {len(ent_matches)}")
    if len(ent_matches) > 0:
        print(f"  Sample entrance:")
        print(f"    Vessel: {ent_matches.iloc[0]['Vessel']}")
        print(f"    Arrival_Date (raw): {ent_matches.iloc[0]['Arrival_Date']}")
        arrival_parsed = pd.to_datetime(ent_matches.iloc[0]['Arrival_Date'], errors='coerce')
        print(f"    Arrival_Date (parsed): {arrival_parsed}")

    # Find in imports (handle NaN values)
    imp_imo_series = imports['IMO'].apply(lambda x: str(int(x)) if pd.notna(x) else '')
    imp_matches = imports[imp_imo_series == test_imo]
    print(f"\nImports records with this IMO: {len(imp_matches)}")
    if len(imp_matches) > 0:
        print(f"  Sample import:")
        print(f"    Vessel: {imp_matches.iloc[0]['Vessel']}")
        print(f"    Arrival Date (raw): {imp_matches.iloc[0]['Arrival Date']}")
        imp_arrival_parsed = pd.to_datetime(imp_matches.iloc[0]['Arrival Date'], errors='coerce')
        print(f"    Arrival Date (parsed): {imp_arrival_parsed}")

    # Check if dates are within 3 days
    if len(ent_matches) > 0 and len(imp_matches) > 0:
        date_diff = abs((arrival_parsed - imp_arrival_parsed).days) if pd.notna(arrival_parsed) and pd.notna(imp_arrival_parsed) else None
        print(f"\n  Date difference: {date_diff} days")
        print(f"  Within ±3 days? {date_diff <= 3 if date_diff is not None else 'N/A (date parse failed)'}")

else:
    print("\n[CRITICAL] NO overlapping IMOs! The test samples have completely different vessels!")
    print("\nSample entrance IMOs:", list(ent_imos)[:20])
    print("\nSample import IMOs:", list(imp_imos)[:20])
