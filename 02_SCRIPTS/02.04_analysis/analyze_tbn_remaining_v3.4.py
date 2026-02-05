"""
Analyze remaining TBN records in v3.4.0 to identify missing rules

Focus: What HS4 codes represent the 38.4% TBN tonnage?

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd

df = pd.read_csv('../03_DOCUMENTATION/03.04_summaries/sample_test_15k/sample_15k_classified_v3.4.0.csv', dtype=str)

print('=== ANALYZING TBN REMAINING (v3.4.0) ===')
print()

# Convert tons
df['Tons_Numeric'] = pd.to_numeric(df['Tons'].str.replace(',', ''), errors='coerce').fillna(0)
total_tons = df['Tons_Numeric'].sum()

# Filter TBN records
tbn = df[(df['Commodity'] == 'TBN') | (df['Cargo'] == 'TBN')]
tbn_tons = tbn['Tons_Numeric'].sum()

print(f'Total TBN Tonnage: {tbn_tons:,.0f} tons ({tbn_tons/total_tons*100:.1f}% of total)')
print(f'Total TBN Records: {len(tbn):,} records')
print()

# Group by HS4 and sort by tonnage
hs4_tbn = tbn.groupby('HS4')['Tons_Numeric'].agg(['sum', 'count']).sort_values('sum', ascending=False)
hs4_tbn['pct_of_tbn'] = (hs4_tbn['sum'] / tbn_tons * 100)
hs4_tbn['pct_of_total'] = (hs4_tbn['sum'] / total_tons * 100)

print('TOP 20 HS4 CODES IN TBN (by tonnage):')
print()
print(f'{"Rank":<5} {"HS4":<6} {"TBN Tons":>15} {"% of TBN":>10} {"% of Total":>12} {"Records":>8}')
print('-' * 70)

rank = 1
for hs4, row in hs4_tbn.head(20).iterrows():
    print(f'{rank:<5} {hs4:<6} {row["sum"]:>15,.0f} {row["pct_of_tbn"]:>9.1f}% {row["pct_of_total"]:>11.1f}% {int(row["count"]):>8}')
    rank += 1

print()

# Show cumulative coverage
cumsum = 0
for i, (hs4, row) in enumerate(hs4_tbn.head(20).iterrows(), 1):
    cumsum += row['pct_of_tbn']
    if cumsum >= 75:
        print(f'Top {i} HS4 codes cover {cumsum:.1f}% of TBN tonnage')
        break

print()

# Sample goods for top 5 TBN HS4 codes
print('SAMPLE GOODS FOR TOP 5 TBN HS4 CODES:')
print()

for hs4, row in hs4_tbn.head(5).iterrows():
    print(f'HS4={hs4} ({row["sum"]:,.0f} tons, {row["pct_of_tbn"]:.1f}% of TBN):')

    # Get samples
    samples = tbn[tbn['HS4'] == hs4].head(3)
    for _, rec in samples.iterrows():
        goods = str(rec['Goods Shipped'])[:70]
        tons = rec['Tons']
        group = rec['Group']
        print(f'  {goods[:70]} | Group: {group} | Tons: {tons}')
    print()
