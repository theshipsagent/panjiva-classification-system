"""Analyze VTYPE rule impact on TBN tonnage"""
import pandas as pd

df = pd.read_csv('../03_DOCUMENTATION/03.04_summaries/sample_test_15k/sample_15k_classified_v3.1.0.csv', dtype=str)

print('=== VTYPE RULE IMPACT ANALYSIS ===')
print()

df['Tons_Numeric'] = pd.to_numeric(df['Tons'].str.replace(',', ''), errors='coerce').fillna(0)
total_tons = df['Tons_Numeric'].sum()

# Filter records classified by VTYPE rules
vtype_records = df[df['Last_Rule_ID'].str.contains('VTYPE', na=False)]
vtype_tons = vtype_records['Tons_Numeric'].sum()

print(f'Records classified by VTYPE rules: {len(vtype_records):,} / {len(df):,} ({len(vtype_records)/len(df)*100:.1f}%)')
print(f'Tonnage from VTYPE rules: {vtype_tons:,.0f} / {total_tons:,.0f} ({vtype_tons/total_tons*100:.1f}%)')
print()

# How many VTYPE records have TBN?
vtype_tbn = vtype_records[(vtype_records['Commodity'] == 'TBN') | (vtype_records['Cargo'] == 'TBN')]
vtype_tbn_tons = vtype_tbn['Tons_Numeric'].sum()

print(f'VTYPE records with TBN: {len(vtype_tbn):,} / {len(vtype_records):,} ({len(vtype_tbn)/len(vtype_records)*100:.1f}%)')
print(f'VTYPE TBN tonnage: {vtype_tbn_tons:,.0f} / {vtype_tons:,.0f} ({vtype_tbn_tons/vtype_tons*100:.1f}%)')
print()

# Break down by VTYPE rule
print('BREAKDOWN BY VTYPE RULE:')
print()

for vtype in ['VTYPE-RORO', 'VTYPE-BULK-CARRIER', 'VTYPE-TANKER', 'VTYPE-REEFER']:
    vtype_df = df[df['Last_Rule_ID'] == vtype]
    if len(vtype_df) == 0:
        continue

    vtype_tons_rule = vtype_df['Tons_Numeric'].sum()
    vtype_tbn_rule = vtype_df[(vtype_df['Commodity'] == 'TBN') | (vtype_df['Cargo'] == 'TBN')]
    vtype_tbn_tons_rule = vtype_tbn_rule['Tons_Numeric'].sum()

    print(f'{vtype:25s}: {len(vtype_df):5,} records, {vtype_tons_rule:15,.0f} tons')
    print(f'  TBN: {len(vtype_tbn_rule):5,} records ({len(vtype_tbn_rule)/len(vtype_df)*100:.1f}%), {vtype_tbn_tons_rule:15,.0f} tons ({vtype_tbn_tons_rule/vtype_tons_rule*100:.1f}%)')
    print()

print()
print('=== RECOMMENDATION ===')
print('Remove VTYPE rules from Phase 1. They lock Group based on vessel type,')
print('blocking Phase 2 cargo-based classification.')
print()
print('Let Phase 2 classify by actual cargo HS codes, not vessel type.')
