"""Analyze how many Phase 5 records are blocked by tonnage filters"""
import pandas as pd

df = pd.read_csv('../03_DOCUMENTATION/03.04_summaries/sample_test_15k/sample_15k_classified_v3.2.0.csv', dtype=str)
df_dict = pd.read_csv('../01_DICTIONARIES/03.01_cargo_classification/cargo_classification_dictionary_v3.2.0_20260114_0300.csv', dtype=str)

print('=== TONNAGE FILTER BLOCKING ANALYSIS ===')
print()

df['Tons_Numeric'] = pd.to_numeric(df['Tons'].str.replace(',', ''), errors='coerce').fillna(0)

# Get Phase 5 records
phase5 = df[df['Classified_Phase'] == '5']
phase5_tons = phase5['Tons_Numeric'].sum()

print(f'Phase 5 (Default): {len(phase5):,} records, {phase5_tons:,.0f} tons')
print()

# Check how many have HS4 match in Phase 2
phase2 = df_dict[df_dict['Phase'] == '2']

blocked_by_tons = []

for idx, rec in phase5.head(100).iterrows():  # Sample first 100
    rec_hs4 = str(rec.get('HS4', '')).strip()
    rec_tons = rec['Tons_Numeric']

    # Find matching Phase 2 rule
    rule = phase2[phase2['HS4'] == rec_hs4]

    if len(rule) > 0:
        rule = rule.iloc[0]

        # Check tonnage filter
        min_tons = str(rule.get('Min_Tons', '')).strip()
        max_tons = str(rule.get('Max_Tons', '')).strip()

        blocked = False
        reason = ''

        if min_tons and min_tons != 'nan' and min_tons != '':
            try:
                if rec_tons < float(min_tons):
                    blocked = True
                    reason = f'below min {min_tons}'
            except:
                pass

        if max_tons and max_tons != 'nan' and max_tons != '':
            try:
                if rec_tons > float(max_tons):
                    blocked = True
                    reason = f'above max {max_tons}'
            except:
                pass

        if blocked:
            blocked_by_tons.append({
                'HS4': rec_hs4,
                'Tons': rec_tons,
                'Reason': reason,
                'Min': min_tons if min_tons and min_tons != 'nan' else '',
                'Max': max_tons if max_tons and max_tons != 'nan' else '',
                'Goods': str(rec.get('Goods Shipped', ''))[:40]
            })

print(f'Sampled {min(100, len(phase5))} Phase 5 records')
print(f'Found {len(blocked_by_tons)} blocked by tonnage filters')
print()

if len(blocked_by_tons) > 0:
    print('EXAMPLES OF TONNAGE-BLOCKED RECORDS:')
    print()
    for item in blocked_by_tons[:10]:
        print(f'HS4={item["HS4"]} - {item["Tons"]:,.0f} tons ({item["Reason"]})')
        print(f'  Filter: Min={item["Min"]}, Max={item["Max"]}')
        print(f'  Goods: {item["Goods"]}')
        print()

    # Calculate tonnage impact
    blocked_tons = sum(item['Tons'] for item in blocked_by_tons)
    print(f'Tonnage blocked in sample: {blocked_tons:,.0f} tons')
    print(f'Extrapolated to all Phase 5: ~{blocked_tons / min(100, len(phase5)) * len(phase5):,.0f} tons')
