"""Check WLWH classification results"""
import pandas as pd
from pathlib import Path

SAMPLE = Path(r"G:\My Drive\LLM\project_manifest\03_DOCUMENTATION/03.04_summaries\sample_test_15k\sample_15k_classified.csv")

df = pd.read_csv(SAMPLE, dtype=str)

# Filter WLWH records
wlwh = df[df['Carrier'].str.contains('WLWH', na=False)]

print(f"Total WLWH records: {len(wlwh)}")
print(f"\nPhase distribution:")
print(wlwh['Classified_Phase'].value_counts())

print(f"\n=== Sample Phase 1 WLWH Record ===")
p1_wlwh = wlwh[wlwh['Classified_Phase'] == '1'].iloc[0] if len(wlwh[wlwh['Classified_Phase'] == '1']) > 0 else None
if p1_wlwh is not None:
    print(f"Carrier: {p1_wlwh['Carrier']}")
    print(f"Group: {p1_wlwh['Group']}")
    print(f"Commodity: {p1_wlwh['Commodity']}")
    print(f"Cargo: {p1_wlwh['Cargo']}")
    print(f"Cargo Detail: {p1_wlwh['Cargo Detail']}")
    print(f"Group_Locked: {p1_wlwh.get('Group_Locked', 'N/A')}")
    print(f"Cargo_Detail_Locked: {p1_wlwh.get('Cargo_Detail_Locked', 'N/A')}")

print(f"\n=== Sample Phase 2 WLWH Record ===")
p2_wlwh = wlwh[wlwh['Classified_Phase'] == '2'].iloc[0] if len(wlwh[wlwh['Classified_Phase'] == '2']) > 0 else None
if p2_wlwh is not None:
    print(f"Carrier: {p2_wlwh['Carrier']}")
    print(f"Group: {p2_wlwh['Group']}")
    print(f"Commodity: {p2_wlwh['Commodity']}")
    print(f"Cargo: {p2_wlwh['Cargo']}")
    print(f"Cargo Detail: {p2_wlwh['Cargo Detail']}")
    print(f"Vessel_Type_Simple: {p2_wlwh.get('Vessel_Type_Simple', 'N/A')}")
