"""Analyze what fell through to Phase 5 default in v3.2.0"""
import pandas as pd

df = pd.read_csv('../03_DOCUMENTATION/03.04_summaries/sample_test_15k/sample_15k_classified_v3.2.0.csv', dtype=str)

print('=== PHASE 5 DEFAULT ANALYSIS (v3.2.0) ===')
print()

df['Tons_Numeric'] = pd.to_numeric(df['Tons'].str.replace(',', ''), errors='coerce').fillna(0)
total_tons = df['Tons_Numeric'].sum()

# Filter Phase 5
phase5 = df[df['Classified_Phase'] == '5']
phase5_tons = phase5['Tons_Numeric'].sum()

print(f'Phase 5 (Default): {len(phase5):,} records, {phase5_tons:,.0f} tons ({phase5_tons/total_tons*100:.1f}%)')
print()

# Top HS4 codes in Phase 5
hs4_phase5 = phase5.groupby('HS4')['Tons_Numeric'].agg(['sum', 'count']).sort_values('sum', ascending=False)

print('TOP 20 HS4 CODES IN PHASE 5:')
print()
print(f'{"Rank":<5} {"HS4":<6} {"Tons":>15} {"% of Phase5":>12} {"Records":>8}')
print('-' * 60)

rank = 1
for hs4, row in hs4_phase5.head(20).iterrows():
    pct = row['sum'] / phase5_tons * 100
    print(f'{rank:<5} {hs4:<6} {row["sum"]:>15,.0f} {pct:>11.1f}% {int(row["count"]):>8}')
    rank += 1

print()
print()

# Sample goods for top 5
print('SAMPLE GOODS FOR TOP 5 PHASE 5 HS4 CODES:')
print()

for hs4, row in hs4_phase5.head(5).iterrows():
    print(f'HS4={hs4} ({row["sum"]:,.0f} tons):')

    samples = phase5[phase5['HS4'] == hs4].head(3)
    for _, rec in samples.iterrows():
        goods = str(rec['Goods Shipped'])[:60]
        tons = rec['Tons']
        vtype = rec.get('Vessel_Type_Simple', '')
        print(f'  {goods} | Vessel: {vtype} | Tons: {tons}')
    print()
