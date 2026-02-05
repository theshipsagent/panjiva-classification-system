"""
Analyze missing HS4 codes by TONNAGE priority

Strategy: Top 15-20 HS4 codes typically cover 75%+ of all tonnage
Focus on these high-tonnage HS4 codes first

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd

# Load data and dictionary
df = pd.read_csv('../03_DOCUMENTATION/03.04_summaries/sample_test_15k/sample_15k_classified_v3.0.0.csv', dtype=str)
df_dict = pd.read_csv('../01_DICTIONARIES/03.01_cargo_classification/cargo_classification_dictionary_v3.0.0_20260114_0200.csv', dtype=str)

print('=== TOP HS4 CODES BY TONNAGE (15k Sample) ===')
print()

# Convert tons
df['Tons_Numeric'] = pd.to_numeric(df['Tons'].str.replace(',', ''), errors='coerce').fillna(0)
total_tons = df['Tons_Numeric'].sum()

# Group by HS4 and sum tonnage
hs4_tons = df.groupby('HS4')['Tons_Numeric'].agg(['sum', 'count']).sort_values('sum', ascending=False)
hs4_tons['cumulative_pct'] = (hs4_tons['sum'].cumsum() / total_tons * 100)
hs4_tons['pct'] = (hs4_tons['sum'] / total_tons * 100)

print(f'Total Tonnage: {total_tons:,.0f} tons')
print()

# Get dictionary HS4 coverage
dict_hs4 = set()
for _, rule in df_dict.iterrows():
    hs4 = str(rule.get('HS4', '')).strip()
    hs2 = str(rule.get('HS2', '')).strip()
    if hs4 and hs4 != 'nan':
        dict_hs4.add(hs4)
    elif hs2 and hs2 != 'nan':
        # HS2 rules cover all HS4 under that HS2
        dict_hs4.add(hs2 + 'XX')  # Placeholder for HS2 coverage

print('TOP 20 HS4 CODES BY TONNAGE:')
print()
print(f'{"Rank":<5} {"HS4":<6} {"Tons":>15} {"% of Total":>10} {"Cumulative %":>13} {"Records":>8} {"Status":>15}')
print('-' * 85)

rank = 1
for hs4, row in hs4_tons.head(20).iterrows():
    # Check if dictionary has this HS4
    has_exact = hs4 in dict_hs4
    has_hs2 = hs4[:2] + 'XX' in dict_hs4 or any(r.get('HS2') == hs4[:2] for _, r in df_dict.iterrows())

    if has_exact:
        status = 'HAS HS4 RULE'
    elif has_hs2:
        status = 'HAS HS2 RULE'
    else:
        status = 'MISSING'

    print(f'{rank:<5} {hs4:<6} {row["sum"]:>15,.0f} {row["pct"]:>9.1f}% {row["cumulative_pct"]:>12.1f}% {int(row["count"]):>8} {status:>15}')
    rank += 1

print()
print('=== COVERAGE ANALYSIS ===')
print()

# Find where we hit 75% coverage
top_n_for_75 = len(hs4_tons[hs4_tons['cumulative_pct'] <= 75])
print(f'Top {top_n_for_75} HS4 codes cover 75% of tonnage')
print()

# Show missing HS4 in top 20
top20 = hs4_tons.head(20)
missing_hs4 = []
for hs4, row in top20.iterrows():
    has_rule = any(r.get('HS4') == hs4 or r.get('HS2') == hs4[:2] for _, r in df_dict.iterrows())
    if not has_rule:
        missing_hs4.append({
            'HS4': hs4,
            'Tons': row['sum'],
            'Pct': row['pct'],
            'Records': int(row['count'])
        })

if missing_hs4:
    print(f'MISSING HS4 CODES IN TOP 20 ({len(missing_hs4)} total):')
    print()
    for item in missing_hs4:
        print(f"  HS4={item['HS4']}: {item['Tons']:>15,.0f} tons ({item['Pct']:>5.1f}%) - {item['Records']:>5} records")
        # Show sample goods
        sample = df[df['HS4'] == item['HS4']]['Goods Shipped'].head(3)
        for goods in sample:
            print(f"    Sample: {str(goods)[:70]}")
else:
    print('OK: All top 20 HS4 codes have dictionary coverage')

print()
print('=== RECOMMENDATION ===')
print(f'Focus on top {top_n_for_75} HS4 codes to cover 75% of tonnage')
print('Create HS4-level rules (broader than HS6) with:')
print('  - HS4 code match')
print('  - Keywords for refinement')
print('  - Min/Max tons to filter misclassifications')
print('  - Vessel type constraints where applicable')
