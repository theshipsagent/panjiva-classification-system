import pandas as pd
import re

# Load the classified data
df = pd.read_csv(r'G:\My Drive\LLM\project_manifest\panjiva_production_v1\03_output\classified\panjiva_2024_classified_v4.0.0_OPTIMIZED.csv', low_memory=False)

print('='*80)
print('CRUDE OIL CLASSIFICATION INVESTIGATION - 2024 DATA')
print('='*80)

# Define crude oil search patterns
crude_patterns = [
    'crude oil', 'crude', 'maya', 'arab', 'basrah', 'isthmus',
    'hibernia', 'cold lake', 'wti', 'syncrude', 'dco', 'oriente',
    'forties', 'sarir', 'vasconia', 'blend crude', 'amenam', 'merey'
]

# Create a regex pattern to search for any crude variant
pattern = '|'.join(crude_patterns)

# Find all records with crude-related keywords (case insensitive)
mask = df['Goods Shipped'].fillna('').str.contains(pattern, case=False, na=False, regex=True)
crude_records = df[mask].copy()

print(f'\nTOTAL RECORDS WITH CRUDE-RELATED KEYWORDS: {len(crude_records):,}')
print(f'TOTAL TONNAGE: {crude_records["Tons"].sum():,.2f} tons')
print()

# Breakdown by classification outcome
print('='*80)
print('CLASSIFICATION OUTCOME BREAKDOWN')
print('='*80)

# Properly classified (Group = Liquid Bulk, Commodity = Petroleum, Cargo = Crude Oil)
properly_classified = crude_records[
    (crude_records['Group'] == 'Liquid Bulk') &
    (crude_records['Commodity'] == 'Petroleum') &
    (crude_records['Cargo'] == 'Crude Oil')
]

# TBN - any level
tbn_records = crude_records[
    (crude_records['Group'] == 'TBN') |
    (crude_records['Commodity'] == 'TBN') |
    (crude_records['Cargo'] == 'TBN') |
    (crude_records['Cargo Detail'] == 'TBN')
]

# Excluded
excluded_records = crude_records[crude_records['Group'] == 'EXCLUDED']

# Blank/unmatched (no Group assigned or empty)
blank_records = crude_records[
    crude_records['Group'].isna() |
    (crude_records['Group'] == '') |
    ((crude_records['Group'] != 'Liquid Bulk') &
     (crude_records['Group'] != 'EXCLUDED') &
     (crude_records['Group'] != 'TBN'))
]

print(f'\n1. PROPERLY CLASSIFIED (Liquid Bulk -> Petroleum -> Crude Oil):')
print(f'   Records: {len(properly_classified):,}')
print(f'   Tonnage: {properly_classified["Tons"].sum():,.2f} tons')
print(f'   Percentage: {len(properly_classified)/len(crude_records)*100:.1f}% of crude records')

print(f'\n2. TBN (To Be Named at any level):')
print(f'   Records: {len(tbn_records):,}')
print(f'   Tonnage: {tbn_records["Tons"].sum():,.2f} tons')
print(f'   Percentage: {len(tbn_records)/len(crude_records)*100:.1f}% of crude records')

print(f'\n3. EXCLUDED:')
print(f'   Records: {len(excluded_records):,}')
print(f'   Tonnage: {excluded_records["Tons"].sum():,.2f} tons')
print(f'   Percentage: {len(excluded_records)/len(crude_records)*100:.1f}% of crude records')

print(f'\n4. BLANK/UNMATCHED:')
print(f'   Records: {len(blank_records):,}')
print(f'   Tonnage: {blank_records["Tons"].sum():,.2f} tons')
print(f'   Percentage: {len(blank_records)/len(crude_records)*100:.1f}% of crude records')

print()
print('='*80)
print('SAMPLE GOODS DESCRIPTIONS BY OUTCOME')
print('='*80)

# Sample from each category
print('\n--- PROPERLY CLASSIFIED SAMPLES (5 examples) ---')
if len(properly_classified) > 0:
    samples = properly_classified[['Goods Shipped', 'Tons', 'HS2', 'HS4', 'HS6', 'Package_Type', 'Classified_Phase', 'Last_Rule_ID']].head(5)
    for idx, row in samples.iterrows():
        print(f"\nGoods: {row['Goods Shipped'][:100]}")
        print(f"  Tons: {row['Tons']:,.2f} | HS: {row['HS2']}/{row['HS4']}/{row['HS6']} | Pkg: {row['Package_Type']} | Phase: {row['Classified_Phase']} | Rule: {row['Last_Rule_ID']}")

print('\n--- TBN SAMPLES (5 examples) ---')
if len(tbn_records) > 0:
    samples = tbn_records[['Goods Shipped', 'Tons', 'HS2', 'HS4', 'HS6', 'Package_Type', 'Group', 'Commodity', 'Cargo', 'Classified_Phase', 'Last_Rule_ID']].head(5)
    for idx, row in samples.iterrows():
        print(f"\nGoods: {row['Goods Shipped'][:100]}")
        print(f"  Tons: {row['Tons']:,.2f} | HS: {row['HS2']}/{row['HS4']}/{row['HS6']} | Pkg: {row['Package_Type']}")
        print(f"  Classification: {row['Group']} -> {row['Commodity']} -> {row['Cargo']}")
        print(f"  Phase: {row['Classified_Phase']} | Rule: {row['Last_Rule_ID']}")

print('\n--- EXCLUDED SAMPLES (5 examples) ---')
if len(excluded_records) > 0:
    samples = excluded_records[['Goods Shipped', 'Tons', 'HS2', 'HS4', 'HS6', 'Package_Type', 'Classified_Phase', 'Last_Rule_ID']].head(5)
    for idx, row in samples.iterrows():
        print(f"\nGoods: {row['Goods Shipped'][:100]}")
        print(f"  Tons: {row['Tons']:,.2f} | HS: {row['HS2']}/{row['HS4']}/{row['HS6']} | Pkg: {row['Package_Type']} | Phase: {row['Classified_Phase']} | Rule: {row['Last_Rule_ID']}")

print('\n--- BLANK/UNMATCHED SAMPLES (5 examples) ---')
if len(blank_records) > 0:
    samples = blank_records[['Goods Shipped', 'Tons', 'HS2', 'HS4', 'HS6', 'Package_Type', 'Group', 'Commodity', 'Cargo']].head(5)
    for idx, row in samples.iterrows():
        print(f"\nGoods: {row['Goods Shipped'][:100]}")
        print(f"  Tons: {row['Tons']:,.2f} | HS: {row['HS2']}/{row['HS4']}/{row['HS6']} | Pkg: {row['Package_Type']}")
        print(f"  Classification: {row['Group']} -> {row['Commodity']} -> {row['Cargo']}")

print()
print('='*80)
print('TONNAGE BREAKDOWN BY OUTCOME')
print('='*80)
print(f'\nProperly Classified: {properly_classified["Tons"].sum():,.2f} tons')
print(f'TBN:                 {tbn_records["Tons"].sum():,.2f} tons')
print(f'Excluded:            {excluded_records["Tons"].sum():,.2f} tons')
print(f'Blank/Unmatched:     {blank_records["Tons"].sum():,.2f} tons')
print(f'TOTAL:               {crude_records["Tons"].sum():,.2f} tons')

# HS Code analysis
print()
print('='*80)
print('HS CODE DISTRIBUTION BY OUTCOME')
print('='*80)

print('\nProperly Classified - Top HS Codes:')
if len(properly_classified) > 0:
    hs_dist = properly_classified.groupby('HS2')['Tons'].sum().sort_values(ascending=False).head(5)
    for hs, tons in hs_dist.items():
        print(f"  HS{hs}: {tons:,.2f} tons")

print('\nTBN - Top HS Codes:')
if len(tbn_records) > 0:
    hs_dist = tbn_records.groupby('HS2')['Tons'].sum().sort_values(ascending=False).head(5)
    for hs, tons in hs_dist.items():
        print(f"  HS{hs}: {tons:,.2f} tons")

print('\nExcluded - Top HS Codes:')
if len(excluded_records) > 0:
    hs_dist = excluded_records.groupby('HS2')['Tons'].sum().sort_values(ascending=False).head(5)
    for hs, tons in hs_dist.items():
        print(f"  HS{hs}: {tons:,.2f} tons")

print('\nBlank/Unmatched - Top HS Codes:')
if len(blank_records) > 0:
    hs_dist = blank_records.groupby('HS2')['Tons'].sum().sort_values(ascending=False).head(5)
    for hs, tons in hs_dist.items():
        print(f"  HS{hs}: {tons:,.2f} tons")

# Package type analysis
print()
print('='*80)
print('PACKAGE TYPE DISTRIBUTION BY OUTCOME')
print('='*80)

print('\nProperly Classified - Top Package Types:')
if len(properly_classified) > 0:
    pkg_dist = properly_classified.groupby('Package_Type')['Tons'].sum().sort_values(ascending=False).head(5)
    for pkg, tons in pkg_dist.items():
        print(f"  {pkg}: {tons:,.2f} tons")

print('\nTBN - Top Package Types:')
if len(tbn_records) > 0:
    pkg_dist = tbn_records.groupby('Package_Type')['Tons'].sum().sort_values(ascending=False).head(5)
    for pkg, tons in pkg_dist.items():
        print(f"  {pkg}: {tons:,.2f} tons")

print('\nExcluded - Top Package Types:')
if len(excluded_records) > 0:
    pkg_dist = excluded_records.groupby('Package_Type')['Tons'].sum().sort_values(ascending=False).head(5)
    for pkg, tons in pkg_dist.items():
        print(f"  {pkg}: {tons:,.2f} tons")

print('\nBlank/Unmatched - Top Package Types:')
if len(blank_records) > 0:
    pkg_dist = blank_records.groupby('Package_Type')['Tons'].sum().sort_values(ascending=False).head(5)
    for pkg, tons in pkg_dist.items():
        print(f"  {pkg}: {tons:,.2f} tons")
