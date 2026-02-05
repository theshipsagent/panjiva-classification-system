"""Check Phase 1 carrier rule lock status"""
import pandas as pd

df = pd.read_csv('../01_DICTIONARIES/03.01_cargo_classification/cargo_classification_dictionary_v3.1.0_20260114_0230.csv', dtype=str)

# Check Phase 1 carrier rules
phase1 = df[df['Phase'] == '1']

print('PHASE 1 CARRIER RULES - LOCK STATUS:')
print()

# Sample first 15 carrier rules
for _, rule in phase1.head(15).iterrows():
    rule_id = str(rule['Rule_ID'])
    carrier = str(rule.get('Carrier_SCAC', '')).strip()
    group = str(rule.get('Group', '')).strip()
    lock_group = str(rule.get('Lock_Group', '')).strip()
    lock_commodity = str(rule.get('Lock_Commodity', '')).strip()

    scac_str = f'SCAC={carrier}' if carrier and carrier != 'nan' else ''
    group_str = f'Group={group}' if group and group != 'nan' else 'Group=(none)'

    print(f'{rule_id:30s} {scac_str:10s} {group_str:25s}')
    print(f'  Lock_Group={lock_group:5s} Lock_Commodity={lock_commodity:5s}')
    print()
