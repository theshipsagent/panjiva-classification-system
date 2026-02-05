"""Analyze Phase 1 carrier rules that lock Commodity but don't set it"""
import pandas as pd

df_dict = pd.read_csv('../01_DICTIONARIES/03.01_cargo_classification/cargo_classification_dictionary_v3.3.0_20260114_0330.csv', dtype=str)

print('=== PHASE 1 CARRIER LOCK PROBLEM ===')
print()

# Get Phase 1 rules
phase1 = df_dict[df_dict['Phase'] == '1']

print(f'Total Phase 1 rules: {len(phase1)}')
print()

# Find rules that lock Commodity but don't set it
problem_rules = phase1[
    (phase1['Lock_Commodity'] == 'TRUE') &
    ((phase1['Commodity'].isna()) | (phase1['Commodity'] == '') | (phase1['Commodity'] == 'nan'))
]

print(f'Rules that LOCK Commodity but DON\'T SET it: {len(problem_rules)}')
print()

if len(problem_rules) > 0:
    print('PROBLEM RULES (first 20):')
    print()

    for _, rule in problem_rules.head(20).iterrows():
        rule_id = str(rule['Rule_ID'])
        carrier = str(rule.get('Carrier_SCAC', '')).strip()
        group = str(rule.get('Group', '')).strip()
        commodity = str(rule.get('Commodity', '')).strip()
        lock_comm = str(rule.get('Lock_Commodity', '')).strip()

        carrier_str = f'SCAC={carrier}' if carrier and carrier != 'nan' else ''
        comm_str = commodity if commodity and commodity != 'nan' else '(empty)'

        print(f'{rule_id:30s} {carrier_str:10s} Group={group:15s} Commodity={comm_str:15s} Lock={lock_comm}')

print()
print('PROBLEM: These rules lock Commodity without setting it,')
print('preventing Phase 2 from refining the classification.')
print()
print('SOLUTION: Change Lock_Commodity=FALSE for carriers,')
print('let Phase 2 refine based on actual cargo HS codes.')
