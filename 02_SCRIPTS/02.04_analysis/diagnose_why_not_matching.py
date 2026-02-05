"""
Diagnose why rules exist but don't match

Top 20 HS4 codes have dictionary coverage but only 0.1% of tonnage classified

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd

df = pd.read_csv('../03_DOCUMENTATION/03.04_summaries/sample_test_15k/sample_15k_classified_v3.0.0.csv', dtype=str)
df_dict = pd.read_csv('../01_DICTIONARIES/03.01_cargo_classification/cargo_classification_dictionary_v3.0.0_20260114_0200.csv', dtype=str)

print('=== WHY RULES NOT MATCHING ===')
print()

# Take top HS4 by tonnage - HS4=2709 (Petroleum oils, crude)
df['Tons_Numeric'] = pd.to_numeric(df['Tons'].str.replace(',', ''), errors='coerce').fillna(0)

# Sample: HS4=2709 records with TBN
hs2709_tbn = df[(df['HS4'] == '2709') & (df['Commodity'] == 'TBN')]
print(f'HS4=2709 (Petroleum oils, crude): {len(hs2709_tbn)} records with TBN')
print(f'  Total tons: {hs2709_tbn["Tons_Numeric"].sum():,.0f}')
print()

# Check dictionary rules for HS4=2709
dict_2709 = df_dict[(df_dict['HS4'] == '2709') | (df_dict['HS2'] == '27')]
print(f'Dictionary rules for HS4=2709 or HS2=27: {len(dict_2709)}')
print()

if len(dict_2709) > 0:
    print('Sample rules:')
    for _, rule in dict_2709.head(5).iterrows():
        rule_id = rule['Rule_ID']
        phase = rule['Phase']
        hs2 = rule.get('HS2', '')
        hs4 = rule.get('HS4', '')
        hs6 = rule.get('HS6', '')
        kw = str(rule.get('Keywords', ''))[:30]
        min_tons = rule.get('Min_Tons', '')
        max_tons = rule.get('Max_Tons', '')
        print(f'  {rule_id:15s} Phase={phase} HS={hs2}/{hs4}/{hs6:6s} KW=[{kw}] Tons:{min_tons}-{max_tons}')
print()

# Sample data record
if len(hs2709_tbn) > 0:
    sample = hs2709_tbn.iloc[0]
    print('Sample HS4=2709 record NOT matching:')
    print(f'  HS2/HS4/HS6: {sample["HS2"]}/{sample["HS4"]}/{sample["HS6"]}')
    print(f'  Goods: {sample["Goods Shipped"][:70]}')
    print(f'  Tons: {sample["Tons"]}')
    print(f'  Group: {sample["Group"]}')
    print(f'  Commodity: {sample["Commodity"]}')
    print(f'  Phase: {sample["Classified_Phase"]}')
    print(f'  Last Rule: {sample["Last_Rule_ID"]}')
    print()

print('=== THE PROBLEM ===')
print()
print('Phase 6 rules require EXACT HS6 match:')
print('  - Rule: HS6=270900')
print('  - Data: HS6=270900 → MATCH ✓')
print('  - Data: HS6=270190 → NO MATCH ✗')
print()
print('But Phase 6 runs AFTER Phase 1/2 already locked the Group!')
print()

# Check lock status of TBN records
print('Lock Status of HS4=2709 TBN records:')
if len(hs2709_tbn) > 0:
    sample = hs2709_tbn.iloc[0]
    print(f'  Group Locked: {sample.get("Group_Locked", "")}')
    print(f'  Current Group: {sample.get("Group", "")}')
    print()

# Check if dictionary rule wants different Group
if len(dict_2709) > 0:
    dict_rule = dict_2709.iloc[0]
    print(f'Dictionary rule wants:')
    print(f'  Group: {dict_rule.get("Group", "")}')
    print()

    if len(hs2709_tbn) > 0:
        print('Match failure reason:')
        if sample.get('Group') != dict_rule.get('Group'):
            print(f'  ✗ Group mismatch: Data has "{sample.get("Group")}" but rule wants "{dict_rule.get("Group")}"')
            print(f'    Physical constraint check blocks rule application')
        else:
            print(f'  ✓ Group matches: {sample.get("Group")}')
            # Check other requirements
            if dict_rule.get('HS6'):
                print(f'  ✗ HS6 too specific: Rule requires HS6={dict_rule.get("HS6")}, data has HS6={sample.get("HS6")}')
            if dict_rule.get('Keywords'):
                print(f'  ✗ Keyword required: Rule requires [{dict_rule.get("Keywords")}]')

print()
print('=== ROOT CAUSE ===')
print('1. Phase 1 sets Group=Liquid Bulk (from vessel type)')
print('2. Phase 2 skips (no carrier match)')
print('3. Phase 6 rules require:')
print('   a) EXACT HS6 match (too specific)')
print('   b) Keyword match (may not be in Goods Shipped)')
print('   c) Tonnage range (may filter out record)')
print('4. If ANY requirement fails → No match → Stays TBN')
print()
print('=== SOLUTION ===')
print('Create Phase 4 rules:')
print('  - Match at HS4 level (broader)')
print('  - Use HS2 when HS4 has many variants')
print('  - Keywords optional, for refinement only')
print('  - Group already locked from Phase 1, just refine Commodity')
