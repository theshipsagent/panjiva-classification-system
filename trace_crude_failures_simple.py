import pandas as pd
import sys

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Load data
df = pd.read_csv(r'G:\My Drive\LLM\project_manifest\panjiva_production_v1\03_output\classified\panjiva_2024_classified_v4.0.0_OPTIMIZED.csv', low_memory=False)
dict_df = pd.read_csv(r'G:\My Drive\LLM\project_manifest\panjiva_production_v1\01_dictionary\cargo_classification_dictionary_v4.0.0_SIMPLE.csv')

print('='*80)
print('DETAILED TRACE ANALYSIS - WHY CRUDE OIL RECORDS FAIL TO MATCH')
print('='*80)

# Find crude oil rules in the dictionary
crude_rules = dict_df[dict_df['Keywords'].fillna('').str.contains('crude oil|crude', case=False, na=False, regex=True)]

print('\nCRUDE OIL RULES IN DICTIONARY:')
print('-'*80)
for idx, rule in crude_rules.iterrows():
    print(f"\nRule ID: {rule['Rule_ID']}")
    print(f"  Phase: {rule['Phase']}")
    print(f"  Active: {rule['Active']}")
    print(f"  Package Type: {rule['Package_Type']}")
    print(f"  HS2: {rule['HS2']}")
    print(f"  Keywords: {rule['Keywords'][:80]}...")
    print(f"  Min Tons: {rule['Min_Tons']} / Max Tons: {rule['Max_Tons']}")
    print(f"  Locks: Group={rule['Lock_Group']} Commodity={rule['Lock_Commodity']} Cargo={rule['Lock_Cargo']}")

# Find crude-related records
crude_pattern = 'crude oil|crude|maya|arab|basrah|isthmus|hibernia|cold lake|wti|syncrude|dco|oriente|forties|sarir|vasconia|blend crude|amenam|merey'
mask = df['Goods Shipped'].fillna('').str.contains(crude_pattern, case=False, na=False, regex=True)
crude_records = df[mask].copy()

print()
print('='*80)
print('BLANK/UNMATCHED EXAMPLES (Top 10 by tonnage)')
print('='*80)

# Focus on the blank/unmatched records
blank_records = crude_records[
    crude_records['Group'].isna() |
    (crude_records['Group'] == '') |
    ((crude_records['Group'] != 'Liquid Bulk') &
     (crude_records['Group'] != 'EXCLUDED') &
     (crude_records['Group'] != 'TBN'))
]

# Get top 10 by tonnage
top_failures = blank_records.nlargest(10, 'Tons')

for idx, row in top_failures.iterrows():
    print(f"\n{row['Goods Shipped'][:100]}")
    print(f"  Tons: {row['Tons']:,.2f}")
    print(f"  HS2={row['HS2']} HS4={row['HS4']} | Pkg={row['Package_Type']} | Phase={row['Classified_Phase']} Rule={row['Last_Rule_ID']}")
    print(f"  Group='{row['Group']}' Commodity='{row['Commodity']}' Cargo='{row['Cargo']}'")

    # Check matching criteria
    issues = []

    # HS2 check
    if pd.isna(row['HS2']) or row['HS2'] != 27.0:
        issues.append(f"WRONG HS2: {row['HS2']} (need 27)")

    # Package check
    if pd.isna(row['Package_Type']) or row['Package_Type'] not in ['LBK', 'BLK', 'BBL']:
        issues.append(f"WRONG PKG: {row['Package_Type']} (need LBK/BLK/BBL)")

    # Tonnage check
    tons = row['Tons']
    if pd.notna(tons):
        if tons < 250:
            issues.append(f"TOO LIGHT: {tons:,.0f} tons (need 250+)")
        elif tons > 175000:
            issues.append(f"TOO HEAVY: {tons:,.0f} tons (max 175,000)")

    if not issues:
        print(f"  >>> MYSTERY: Meets all criteria but not classified!")
    else:
        print(f"  >>> FAILED BECAUSE: {' | '.join(issues)}")

print()
print('='*80)
print('TBN EXAMPLES (Top 10 by tonnage)')
print('='*80)

tbn_records = crude_records[
    (crude_records['Group'] == 'TBN') |
    (crude_records['Commodity'] == 'TBN') |
    (crude_records['Cargo'] == 'TBN')
]

top_tbn = tbn_records.nlargest(10, 'Tons')

for idx, row in top_tbn.iterrows():
    print(f"\n{row['Goods Shipped'][:100]}")
    print(f"  Tons: {row['Tons']:,.2f}")
    print(f"  HS2={row['HS2']} HS4={row['HS4']} | Pkg={row['Package_Type']} | Phase={row['Classified_Phase']} Rule={row['Last_Rule_ID']}")
    print(f"  {row['Group']} -> {row['Commodity']} -> {row['Cargo']}")

    # Check why it didn't refine
    issues = []

    if pd.isna(row['HS2']) or row['HS2'] != 27.0:
        issues.append(f"WRONG HS2: {row['HS2']}")

    if pd.isna(row['Package_Type']) or row['Package_Type'] not in ['LBK', 'BLK', 'BBL']:
        issues.append(f"WRONG PKG: {row['Package_Type']}")

    tons = row['Tons']
    if pd.notna(tons):
        if tons < 250:
            issues.append(f"TOO LIGHT: {tons:,.0f} tons")
        elif tons > 175000:
            issues.append(f"TOO HEAVY: {tons:,.0f} tons")

    if issues:
        print(f"  >>> STOPPED AT TBN: {' | '.join(issues)}")
    else:
        print(f"  >>> MYSTERY: Should have refined to Crude Oil!")

print()
print('='*80)
print('ROOT CAUSE SUMMARY')
print('='*80)

# Detailed breakdown
total_crude_tons = crude_records['Tons'].sum()

# Properly classified
properly_classified = crude_records[
    (crude_records['Group'] == 'Liquid Bulk') &
    (crude_records['Commodity'] == 'Petroleum') &
    (crude_records['Cargo'] == 'Crude Oil')
]

print(f'\nTotal crude-related tonnage: {total_crude_tons:,.2f} tons')
print(f'Properly classified:         {properly_classified["Tons"].sum():,.2f} tons ({properly_classified["Tons"].sum()/total_crude_tons*100:.1f}%)')
print(f'TBN:                         {tbn_records["Tons"].sum():,.2f} tons ({tbn_records["Tons"].sum()/total_crude_tons*100:.1f}%)')
print(f'Blank/Unmatched:             {blank_records["Tons"].sum():,.2f} tons ({blank_records["Tons"].sum()/total_crude_tons*100:.1f}%)')

# Failure reasons for blank/unmatched
print(f'\nBLANK/UNMATCHED FAILURE BREAKDOWN ({len(blank_records):,} records, {blank_records["Tons"].sum():,.2f} tons):')

wrong_hs2 = blank_records[blank_records['HS2'] != 27.0]
print(f'  Wrong HS2 (not 27):          {len(wrong_hs2):,} records, {wrong_hs2["Tons"].sum():,.2f} tons')

wrong_pkg = blank_records[~blank_records['Package_Type'].isin(['LBK', 'BLK', 'BBL'])]
print(f'  Wrong Package Type:          {len(wrong_pkg):,} records, {wrong_pkg["Tons"].sum():,.2f} tons')

too_light = blank_records[blank_records['Tons'] < 250]
print(f'  Too light (<250 tons):       {len(too_light):,} records, {too_light["Tons"].sum():,.2f} tons')

too_heavy = blank_records[blank_records['Tons'] > 175000]
print(f'  Too heavy (>175K tons):      {len(too_heavy):,} records, {too_heavy["Tons"].sum():,.2f} tons')

# The mystery cases
mystery_blank = blank_records[
    (blank_records['HS2'] == 27.0) &
    (blank_records['Package_Type'].isin(['LBK', 'BLK', 'BBL'])) &
    (blank_records['Tons'] >= 250) &
    (blank_records['Tons'] <= 175000)
]
print(f'  MYSTERY (meets all criteria): {len(mystery_blank):,} records, {mystery_blank["Tons"].sum():,.2f} tons')

# Failure reasons for TBN
print(f'\nTBN FAILURE BREAKDOWN ({len(tbn_records):,} records, {tbn_records["Tons"].sum():,.2f} tons):')

tbn_wrong_hs2 = tbn_records[tbn_records['HS2'] != 27.0]
print(f'  Wrong HS2 (not 27):          {len(tbn_wrong_hs2):,} records, {tbn_wrong_hs2["Tons"].sum():,.2f} tons')

tbn_wrong_pkg = tbn_records[~tbn_records['Package_Type'].isin(['LBK', 'BLK', 'BBL'])]
print(f'  Wrong Package Type:          {len(tbn_wrong_pkg):,} records, {tbn_wrong_pkg["Tons"].sum():,.2f} tons')

tbn_too_light = tbn_records[tbn_records['Tons'] < 250]
print(f'  Too light (<250 tons):       {len(tbn_too_light):,} records, {tbn_too_light["Tons"].sum():,.2f} tons')

tbn_too_heavy = tbn_records[tbn_records['Tons'] > 175000]
print(f'  Too heavy (>175K tons):      {len(tbn_too_heavy):,} records, {tbn_too_heavy["Tons"].sum():,.2f} tons')

mystery_tbn = tbn_records[
    (tbn_records['HS2'] == 27.0) &
    (tbn_records['Package_Type'].isin(['LBK', 'BLK', 'BBL'])) &
    (tbn_records['Tons'] >= 250) &
    (tbn_records['Tons'] <= 175000)
]
print(f'  MYSTERY (meets all criteria): {len(mystery_tbn):,} records, {mystery_tbn["Tons"].sum():,.2f} tons')

print()
print('='*80)
print('CONCLUSION')
print('='*80)
print(f'\nMissed crude tonnage: {(tbn_records["Tons"].sum() + blank_records["Tons"].sum()):,.2f} tons ({(tbn_records["Tons"].sum() + blank_records["Tons"].sum())/total_crude_tons*100:.1f}%)')
print(f'\nPrimary failure modes:')
print(f'  1. Wrong HS2 codes: {wrong_hs2["Tons"].sum() + tbn_wrong_hs2["Tons"].sum():,.2f} tons')
print(f'  2. Wrong package types: {wrong_pkg["Tons"].sum() + tbn_wrong_pkg["Tons"].sum():,.2f} tons')
print(f'  3. Tonnage out of range: {(too_light["Tons"].sum() + too_heavy["Tons"].sum() + tbn_too_light["Tons"].sum() + tbn_too_heavy["Tons"].sum()):,.2f} tons')
print(f'  4. Mystery (should match): {mystery_blank["Tons"].sum() + mystery_tbn["Tons"].sum():,.2f} tons')
