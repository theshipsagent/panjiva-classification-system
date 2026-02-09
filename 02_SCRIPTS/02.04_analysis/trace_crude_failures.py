import pandas as pd

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
    print(f"  HS4: {rule['HS4']}")
    print(f"  Keywords: {rule['Keywords']}")
    print(f"  Min Tons: {rule['Min_Tons']}")
    print(f"  Max Tons: {rule['Max_Tons']}")
    print(f"  Lock Group: {rule['Lock_Group']}")
    print(f"  Lock Commodity: {rule['Lock_Commodity']}")
    print(f"  Lock Cargo: {rule['Lock_Cargo']}")
    print(f"  Lock Cargo Detail: {rule['Lock_Cargo_Detail']}")
    print(f"  Classification: {rule['Group']} -> {rule['Commodity']} -> {rule['Cargo']} -> {rule['Cargo_Detail']}")

# Find crude-related records
crude_pattern = 'crude oil|crude|maya|arab|basrah|isthmus|hibernia|cold lake|wti|syncrude|dco|oriente|forties|sarir|vasconia|blend crude|amenam|merey'
mask = df['Goods Shipped'].fillna('').str.contains(crude_pattern, case=False, na=False, regex=True)
crude_records = df[mask].copy()

print()
print('='*80)
print('DETAILED FAILURE ANALYSIS - BLANK/UNMATCHED EXAMPLES')
print('='*80)

# Focus on the blank/unmatched records (highest tonnage failures)
blank_records = crude_records[
    crude_records['Group'].isna() |
    (crude_records['Group'] == '') |
    ((crude_records['Group'] != 'Liquid Bulk') &
     (crude_records['Group'] != 'EXCLUDED') &
     (crude_records['Group'] != 'TBN'))
]

# Get top 10 by tonnage
top_failures = blank_records.nlargest(10, 'Tons')

print('\nTop 10 Blank/Unmatched Records (by tonnage):')
print('-'*80)
for idx, row in top_failures.iterrows():
    print(f"\n{row['Goods Shipped'][:120]}")
    print(f"  Tons: {row['Tons']:,.2f}")
    print(f"  HS Codes: HS2={row['HS2']} / HS4={row['HS4']} / HS6={row['HS6']}")
    print(f"  Package Type: {row['Package_Type']}")
    print(f"  Classification: Group='{row['Group']}' Commodity='{row['Commodity']}' Cargo='{row['Cargo']}'")
    print(f"  Phase: {row['Classified_Phase']} | Rule: {row['Last_Rule_ID']}")

    # Check why it didn't match crude oil rules
    print(f"\n  WHY IT DIDN'T MATCH CRUDE-OIL RULE (Phase 4):")

    # CRUDE-OIL rule criteria
    print(f"    ✓ Contains 'crude' keyword: YES (found in search)")

    # Check HS2
    if pd.notna(row['HS2']) and row['HS2'] == 27.0:
        print(f"    ✓ HS2 = 27: YES")
    else:
        print(f"    ✗ HS2 = 27: NO (actual: {row['HS2']})")

    # Check package type
    pkg_match = False
    if pd.notna(row['Package_Type']):
        if row['Package_Type'] in ['LBK', 'BLK', 'BBL']:
            print(f"    ✓ Package Type in [LBK, BLK, BBL]: YES ({row['Package_Type']})")
            pkg_match = True
        else:
            print(f"    ✗ Package Type in [LBK, BLK, BBL]: NO (actual: {row['Package_Type']})")
    else:
        print(f"    ✗ Package Type in [LBK, BLK, BBL]: NO (missing)")

    # Check tonnage range
    tons = row['Tons']
    if pd.notna(tons):
        if tons >= 250 and tons <= 175000:
            print(f"    ✓ Tonnage 250-175000: YES ({tons:,.2f})")
        elif tons < 250:
            print(f"    ✗ Tonnage 250-175000: NO - BELOW minimum ({tons:,.2f} < 250)")
        else:
            print(f"    ✗ Tonnage 250-175000: NO - ABOVE maximum ({tons:,.2f} > 175,000)")
    else:
        print(f"    ✗ Tonnage 250-175000: NO (missing)")

    # Check if it matched CRUDE-OIL-P5 (Phase 5 fallback)
    print(f"\n  WHY IT DIDN'T MATCH CRUDE-OIL-P5 RULE (Phase 5):")

    # CRUDE-OIL-P5 has no HS2 requirement, only package + keyword + tonnage
    if pkg_match:
        print(f"    ✓ Package Type in [LBK, BLK, BBL]: YES")
    else:
        print(f"    ✗ Package Type in [LBK, BLK, BBL]: NO")

    if pd.notna(tons) and tons >= 250 and tons <= 175000:
        print(f"    ✓ Tonnage 250-175000: YES")
    else:
        print(f"    ✗ Tonnage 250-175000: NO")

print()
print('='*80)
print('TBN EXAMPLES (Partial Classification)')
print('='*80)

# TBN records
tbn_records = crude_records[
    (crude_records['Group'] == 'TBN') |
    (crude_records['Commodity'] == 'TBN') |
    (crude_records['Cargo'] == 'TBN') |
    (crude_records['Cargo Detail'] == 'TBN')
]

# Get top 10 by tonnage
top_tbn = tbn_records.nlargest(10, 'Tons')

print('\nTop 10 TBN Records (by tonnage):')
print('-'*80)
for idx, row in top_tbn.iterrows():
    print(f"\n{row['Goods Shipped'][:120]}")
    print(f"  Tons: {row['Tons']:,.2f}")
    print(f"  HS Codes: HS2={row['HS2']} / HS4={row['HS4']} / HS6={row['HS6']}")
    print(f"  Package Type: {row['Package_Type']}")
    print(f"  Classification: {row['Group']} -> {row['Commodity']} -> {row['Cargo']}")
    print(f"  Phase: {row['Classified_Phase']} | Rule: {row['Last_Rule_ID']}")

    print(f"\n  WHY IT STOPPED AT TBN:")

    # Check what rule matched
    if pd.notna(row['Last_Rule_ID']):
        if row['Last_Rule_ID'] in ['CARRIER-TANKER', 'CARRIER-DRYBULK']:
            print(f"    → Matched {row['Last_Rule_ID']} in Phase 2 (vessel type hint)")
            print(f"    → This rule sets Group but leaves Commodity/Cargo as TBN")
            print(f"    → Should have been refined by later phases but wasn't")

    # Check why it didn't match crude oil rules
    print(f"\n  WHY IT DIDN'T GET REFINED TO CRUDE OIL:")

    if pd.notna(row['HS2']) and row['HS2'] == 27.0:
        print(f"    ✓ HS2 = 27: YES")
    else:
        print(f"    ✗ HS2 = 27: NO (actual: {row['HS2']})")

    if pd.notna(row['Package_Type']) and row['Package_Type'] in ['LBK', 'BLK', 'BBL']:
        print(f"    ✓ Package Type in [LBK, BLK, BBL]: YES ({row['Package_Type']})")
    else:
        print(f"    ✗ Package Type in [LBK, BLK, BBL]: NO (actual: {row['Package_Type']})")

    tons = row['Tons']
    if pd.notna(tons):
        if tons >= 250 and tons <= 175000:
            print(f"    ✓ Tonnage 250-175000: YES ({tons:,.2f})")
        elif tons < 250:
            print(f"    ✗ Tonnage 250-175000: NO - BELOW minimum ({tons:,.2f} < 250)")
        else:
            print(f"    ✗ Tonnage 250-175000: NO - ABOVE maximum ({tons:,.2f} > 175,000)")

print()
print('='*80)
print('EXCLUDED EXAMPLES')
print('='*80)

excluded_records = crude_records[crude_records['Group'] == 'EXCLUDED']
top_excluded = excluded_records.nlargest(10, 'Tons')

print('\nTop 10 Excluded Records (by tonnage):')
print('-'*80)
for idx, row in top_excluded.iterrows():
    print(f"\n{row['Goods Shipped'][:120]}")
    print(f"  Tons: {row['Tons']:,.2f}")
    print(f"  HS Codes: HS2={row['HS2']} / HS4={row['HS4']} / HS6={row['HS6']}")
    print(f"  Package Type: {row['Package_Type']}")
    print(f"  Phase: {row['Classified_Phase']} | Rule: {row['Last_Rule_ID']}")

    print(f"\n  WHY IT WAS EXCLUDED:")
    if pd.notna(row['Last_Rule_ID']):
        if 'NOISE' in row['Last_Rule_ID']:
            print(f"    → Matched noise exclusion rule: {row['Last_Rule_ID']}")
            print(f"    → This is a Phase 3 rule that excludes low-tonnage or non-cargo items")
        elif 'EXCLUDE' in row['Last_Rule_ID']:
            print(f"    → Matched exclusion rule: {row['Last_Rule_ID']}")

print()
print('='*80)
print('SUMMARY STATISTICS')
print('='*80)

# Tonnage summary
total_crude_tons = crude_records['Tons'].sum()
classified_tons = crude_records[
    (crude_records['Group'] == 'Liquid Bulk') &
    (crude_records['Commodity'] == 'Petroleum') &
    (crude_records['Cargo'] == 'Crude Oil')
]['Tons'].sum()
tbn_tons = tbn_records['Tons'].sum()
excluded_tons = excluded_records['Tons'].sum()
blank_tons = blank_records['Tons'].sum()

print(f'\nTotal crude-related tonnage: {total_crude_tons:,.2f} tons')
print(f'Properly classified:         {classified_tons:,.2f} tons ({classified_tons/total_crude_tons*100:.1f}%)')
print(f'TBN (partial):              {tbn_tons:,.2f} tons ({tbn_tons/total_crude_tons*100:.1f}%)')
print(f'Excluded:                   {excluded_tons:,.2f} tons ({excluded_tons/total_crude_tons*100:.1f}%)')
print(f'Blank/Unmatched:            {blank_tons:,.2f} tons ({blank_tons/total_crude_tons*100:.1f}%)')
print(f'\nMissed tonnage (TBN + Excluded + Blank): {tbn_tons + excluded_tons + blank_tons:,.2f} tons')
print(f'Percentage of crude tonnage missed: {(tbn_tons + excluded_tons + blank_tons)/total_crude_tons*100:.1f}%')

# Failure reasons summary
print()
print('='*80)
print('ROOT CAUSE ANALYSIS')
print('='*80)

# Count failure reasons for blank/unmatched
wrong_hs2 = blank_records[blank_records['HS2'] != 27.0].shape[0]
wrong_pkg = blank_records[~blank_records['Package_Type'].isin(['LBK', 'BLK', 'BBL'])].shape[0]
out_of_range = blank_records[(blank_records['Tons'] < 250) | (blank_records['Tons'] > 175000)].shape[0]

print(f'\nBlank/Unmatched Failure Reasons (total records: {len(blank_records):,}):')
print(f'  Wrong HS2 (not 27):          {wrong_hs2:,} records')
print(f'  Wrong Package Type:          {wrong_pkg:,} records')
print(f'  Tonnage out of range:        {out_of_range:,} records')

# Count failure reasons for TBN
tbn_wrong_hs2 = tbn_records[tbn_records['HS2'] != 27.0].shape[0]
tbn_wrong_pkg = tbn_records[~tbn_records['Package_Type'].isin(['LBK', 'BLK', 'BBL'])].shape[0]
tbn_out_of_range = tbn_records[(tbn_records['Tons'] < 250) | (tbn_records['Tons'] > 175000)].shape[0]

print(f'\nTBN Failure Reasons (total records: {len(tbn_records):,}):')
print(f'  Wrong HS2 (not 27):          {tbn_wrong_hs2:,} records')
print(f'  Wrong Package Type:          {tbn_wrong_pkg:,} records')
print(f'  Tonnage out of range:        {tbn_out_of_range:,} records')
