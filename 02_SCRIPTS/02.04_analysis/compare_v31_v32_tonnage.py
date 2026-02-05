"""Compare v3.1.0 vs v3.2.0 tonnage by phase"""
import pandas as pd

df_v31 = pd.read_csv('../03_DOCUMENTATION/03.04_summaries/sample_test_15k/sample_15k_classified_v3.1.0.csv', dtype=str)
df_v32 = pd.read_csv('../03_DOCUMENTATION/03.04_summaries/sample_test_15k/sample_15k_classified_v3.2.0.csv', dtype=str)

print('=== COMPARING v3.1.0 vs v3.2.0 TONNAGE ===')
print()

df_v31['Tons_Numeric'] = pd.to_numeric(df_v31['Tons'].str.replace(',', ''), errors='coerce').fillna(0)
df_v32['Tons_Numeric'] = pd.to_numeric(df_v32['Tons'].str.replace(',', ''), errors='coerce').fillna(0)

total_tons = df_v31['Tons_Numeric'].sum()

print(f'Total Tonnage: {total_tons:,.0f} tons')
print()

# Compare by phase
print('TONNAGE BY PHASE:')
print()
print(f'{"Phase":<10} {"v3.1.0 Tons":>20} {"v3.1.0 Recs":>12} {"v3.2.0 Tons":>20} {"v3.2.0 Recs":>12} {"Difference":>15}')
print('-' * 100)

phases_v31 = df_v31.groupby('Classified_Phase')['Tons_Numeric'].agg(['sum', 'count']).to_dict('index')
phases_v32 = df_v32.groupby('Classified_Phase')['Tons_Numeric'].agg(['sum', 'count']).to_dict('index')

all_phases = sorted(set(list(phases_v31.keys()) + list(phases_v32.keys())))

for phase in all_phases:
    v31_tons = phases_v31.get(phase, {}).get('sum', 0)
    v31_count = int(phases_v31.get(phase, {}).get('count', 0))
    v32_tons = phases_v32.get(phase, {}).get('sum', 0)
    v32_count = int(phases_v32.get(phase, {}).get('count', 0))
    diff = v32_tons - v31_tons

    print(f'{str(phase):10s} {v31_tons:>20,.0f} {v31_count:>12,} {v32_tons:>20,.0f} {v32_count:>12,} {diff:>+15,.0f}')

print()
print()

# Compare TBN status
v31_tbn = df_v31[(df_v31['Commodity'] == 'TBN') | (df_v31['Cargo'] == 'TBN')]
v31_tbn_tons = v31_tbn['Tons_Numeric'].sum()

v32_tbn = df_v32[(df_v32['Commodity'] == 'TBN') | (df_v32['Cargo'] == 'TBN')]
v32_tbn_tons = v32_tbn['Tons_Numeric'].sum()

print('TBN COMPARISON:')
print(f'v3.1.0: {v31_tbn_tons:,.0f} tons ({v31_tbn_tons/total_tons*100:.1f}%) - {len(v31_tbn):,} records')
print(f'v3.2.0: {v32_tbn_tons:,.0f} tons ({v32_tbn_tons/total_tons*100:.1f}%) - {len(v32_tbn):,} records')
print(f'Change: {v32_tbn_tons - v31_tbn_tons:+,.0f} tons')
print()

# Compare fully classified
v31_full = df_v31[(df_v31['Commodity'] != 'TBN') & (df_v31['Commodity'].notna()) & (df_v31['Commodity'] != '')]
v31_full_tons = v31_full['Tons_Numeric'].sum()

v32_full = df_v32[(df_v32['Commodity'] != 'TBN') & (df_v32['Commodity'].notna()) & (df_v32['Commodity'] != '')]
v32_full_tons = v32_full['Tons_Numeric'].sum()

print('FULLY CLASSIFIED COMPARISON:')
print(f'v3.1.0: {v31_full_tons:,.0f} tons ({v31_full_tons/total_tons*100:.1f}%) - {len(v31_full):,} records')
print(f'v3.2.0: {v32_full_tons:,.0f} tons ({v32_full_tons/total_tons*100:.1f}%) - {len(v32_full):,} records')
print(f'Change: {v32_full_tons - v31_full_tons:+,.0f} tons')
