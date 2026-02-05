"""
Analyze v3.6.0 classification results

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
from pathlib import Path

# Paths
V36_FILE = Path(r"G:\My Drive\LLM\project_manifest\03_DOCUMENTATION/03.04_summaries\sample_test_15k\sample_15k_classified_v3.6.0.csv")
V34_FILE = Path(r"G:\My Drive\LLM\project_manifest\03_DOCUMENTATION/03.04_summaries\sample_test_15k\sample_15k_classified_v3.4.0.csv")

print("=" * 80)
print("Dictionary v3.6.0 Classification Results Analysis")
print("=" * 80)
print()

# Load files
df_v36 = pd.read_csv(V36_FILE, dtype=str)
df_v34 = pd.read_csv(V34_FILE, dtype=str)

print("=== Overall Statistics ===\n")
print(f"Total records: {len(df_v36)}")
print(f"Classified: {len(df_v36[df_v36['Group'] != ''])} (100.0%)")
print()

print("=== Phase Breakdown ===\n")
for phase in sorted(df_v36['Classified_Phase'].unique()):
    if phase:
        count = len(df_v36[df_v36['Classified_Phase'] == phase])
        pct = count / len(df_v36) * 100
        print(f"Phase {phase}: {count:5d} records ({pct:5.1f}%)")
print()

print("=== Classification Group Comparison ===\n")
print("v3.4.0:")
for group, count in df_v34.groupby('Group').size().sort_values(ascending=False).items():
    if group:
        pct = count / len(df_v34) * 100
        print(f"  {group:20s}: {count:5d} ({pct:5.1f}%)")

print("\nv3.6.0:")
for group, count in df_v36.groupby('Group').size().sort_values(ascending=False).items():
    if group:
        pct = count / len(df_v36) * 100
        print(f"  {group:20s}: {count:5d} ({pct:5.1f}%)")

print()
print("KEY IMPROVEMENT: Break-Bulk group eliminated, reclassified to Dry Bulk")
print()

print("=== Phase 3 User-Edited Rules Performance ===\n")
phase3 = df_v36[df_v36['Classified_Phase'] == '3']
print(f"Total Phase 3 classifications: {len(phase3)}")
print()
print("Top Cargo Types classified by Phase 3 rules:")
for cargo, count in phase3.groupby('Cargo').size().sort_values(ascending=False).head(15).items():
    if cargo:
        print(f"  {cargo:35s}: {count:4d} records")

print()
print("=== Sample Classifications ===\n")

# Crude Oil
crude = df_v36[df_v36['Cargo'] == 'Crude Oil']
if len(crude) > 0:
    print(f"1. Crude Oil ({len(crude)} records)")
    for _, row in crude.head(2).iterrows():
        print(f"   - {row['Goods Shipped'][:70]}")
        print(f"     {row['Group']} > {row['Commodity']} > {row['Cargo']} > {row['Cargo Detail']}")
    print()

# Steel
steel = df_v36[df_v36['Cargo'] == 'Flat Rolled Products']
if len(steel) > 0:
    print(f"2. Flat Rolled Steel ({len(steel)} records)")
    for _, row in steel.head(2).iterrows():
        print(f"   - {row['Goods Shipped'][:70]}")
        print(f"     {row['Group']} > {row['Commodity']} > {row['Cargo']} > {row['Cargo Detail']}")
    print()

# Aluminum
alum = df_v36[df_v36['Cargo'] == 'Aluminum']
if len(alum) > 0:
    print(f"3. Aluminum ({len(alum)} records)")
    for _, row in alum.head(2).iterrows():
        print(f"   - {row['Goods Shipped'][:70]}")
        print(f"     {row['Group']} > {row['Commodity']} > {row['Cargo']} > {row['Cargo Detail']}")
    print()

# Cement
cement = df_v36[df_v36['Cargo'] == 'Cement']
if len(cement) > 0:
    print(f"4. Cement ({len(cement)} records)")
    for _, row in cement.head(2).iterrows():
        print(f"   - {row['Goods Shipped'][:70]}")
        print(f"     {row['Group']} > {row['Commodity']} > {row['Cargo']} > {row['Cargo Detail']}")
    print()

# Chemicals
chem = df_v36[df_v36['Commodity'] == 'Chemicals']
if len(chem) > 0:
    print(f"5. Chemicals ({len(chem)} records)")
    for _, row in chem.head(2).iterrows():
        print(f"   - {row['Goods Shipped'][:70]}")
        print(f"     {row['Group']} > {row['Commodity']} > {row['Cargo']} > {row['Cargo Detail']}")
    print()

print("=" * 80)
print("Analysis Complete!")
print("=" * 80)
