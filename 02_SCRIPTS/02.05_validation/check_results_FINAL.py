"""Check classification results v2"""
import pandas as pd
from pathlib import Path

SAMPLE = Path(r"G:\My Drive\LLM\project_manifest\03_DOCUMENTATION/03.04_summaries\sample_test_15k\sample_15k_classified_FINAL.csv")

df = pd.read_csv(SAMPLE, dtype=str)

# Overall stats
print("=== OVERALL RESULTS ===")
print(f"Total records: {len(df)}")
print(f"Group classified: {len(df[(df['Group'] != '') & (df['Group'].notna())])}")
print(f"Commodity TBN: {len(df[df['Commodity'] == 'TBN'])}")
print(f"Fully classified (not TBN): {len(df[(df['Commodity'] != 'TBN') & (df['Commodity'].notna())])}")

# WLWH stats
wlwh = df[df['Carrier'].str.contains('WLWH', na=False)]
print(f"\n=== WLWH RESULTS (2,021 records) ===")
print(f"Fully classified: {len(wlwh[(wlwh['Commodity'] != 'TBN') & (wlwh['Commodity'].notna())])}")
print(f"TBN Commodity: {len(wlwh[wlwh['Commodity'] == 'TBN'])}")

print("\nSample fully classified WLWH:")
full = wlwh[(wlwh['Commodity'] != 'TBN') & (wlwh['Commodity'].notna())].head(5)
for _, r in full.iterrows():
    print(f"  {r['Group']} > {r['Commodity']} > {r['Cargo']} > {r['Cargo Detail']}")

print("\nSample TBN WLWH:")
tbn = wlwh[wlwh['Commodity'] == 'TBN'].head(3)
for _, r in tbn.iterrows():
    print(f"  {r['Group']} > {r['Commodity']} > {r['Cargo']} > {r['Cargo Detail']}")
    print(f"    Vessel_Type_Simple: {r.get('Vessel_Type_Simple', 'N/A')}")

# Phase 2 detailed stats
print(f"\n=== PHASE 2 CARRIER MATCHING ===")
print(f"Total Phase 2 matches (by Last_Rule_ID):")
phase2_rules = df[df['Last_Rule_ID'].str.contains('CARR-', na=False)]
print(f"  Records with CARR- rules: {len(phase2_rules)}")

carrier_rule_dist = phase2_rules['Last_Rule_ID'].value_counts().head(10)
print("\nTop 10 carrier rules applied:")
for rule, count in carrier_rule_dist.items():
    print(f"  {rule:30s}: {count:5d} records")

# Check all carriers
all_carriers = df['Carrier'].value_counts().head(10)
print("\n=== TOP 10 CARRIERS ===")
for carrier, count in all_carriers.items():
    # Check if classified
    carrier_df = df[df['Carrier'] == carrier]
    fully_classified = len(carrier_df[(carrier_df['Commodity'] != 'TBN') & (carrier_df['Commodity'].notna())])
    pct = fully_classified / count * 100
    print(f"{count:5d} - {carrier[:60]}")
    print(f"       Fully classified: {fully_classified} ({pct:.1f}%)")
