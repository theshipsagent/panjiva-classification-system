"""Quick tonnage report for v3.2.0"""
import pandas as pd

df = pd.read_csv('../03_DOCUMENTATION/03.04_summaries/sample_test_15k/sample_15k_classified_v3.2.0.csv', dtype=str)

print('=== v3.2.0 TONNAGE RESULTS (15k Sample) ===')
print()

df['Tons_Numeric'] = pd.to_numeric(df['Tons'].str.replace(',', ''), errors='coerce').fillna(0)
total_tons = df['Tons_Numeric'].sum()

print(f'Total Tonnage: {total_tons:,.0f} tons')
print()

# Group classified
group_class = df[(df['Group'] != '') & (df['Group'].notna())]
group_tons = group_class['Tons_Numeric'].sum()
print(f'GROUP CLASSIFIED:')
print(f'  Records: {len(group_class):,} / {len(df):,} ({len(group_class)/len(df)*100:.1f}%)')
print(f'  TONS:    {group_tons:,.0f} / {total_tons:,.0f} ({group_tons/total_tons*100:.1f}%)')
print()

# Fully classified
fully = df[(df['Commodity'] != 'TBN') & (df['Commodity'].notna()) & (df['Commodity'] != '')]
fully_tons = fully['Tons_Numeric'].sum()
print(f'FULLY CLASSIFIED (No TBN):')
print(f'  Records: {len(fully):,} / {len(df):,} ({len(fully)/len(df)*100:.1f}%)')
print(f'  TONS:    {fully_tons:,.0f} / {total_tons:,.0f} ({fully_tons/total_tons*100:.1f}%)')
print()

# TBN
tbn = df[(df['Commodity'] == 'TBN') | (df['Cargo'] == 'TBN')]
tbn_tons = tbn['Tons_Numeric'].sum()
print(f'TBN PLACEHOLDERS:')
print(f'  Records: {len(tbn):,} / {len(df):,} ({len(tbn)/len(df)*100:.1f}%)')
print(f'  TONS:    {tbn_tons:,.0f} / {total_tons:,.0f} ({tbn_tons/total_tons*100:.1f}%)')
print()

print('TONNAGE BY GROUP:')
groups = df.groupby('Group')['Tons_Numeric'].agg(['sum', 'count']).sort_values('sum', ascending=False)
for group, row in groups.head(6).iterrows():
    pct = row['sum'] / total_tons * 100
    print(f'  {str(group)[:15]:15s}: {row["sum"]:15,.0f} tons ({pct:5.1f}%) - {int(row["count"]):,} records')
print()

# Phase 6 performance
phase6 = df[df['Classified_Phase'] == '6']
phase6_tons = phase6['Tons_Numeric'].sum()
print(f'PHASE 6 (Your Authoritative Rules):')
print(f'  Matched: {len(phase6):,} records ({len(phase6)/len(df)*100:.1f}%)')
print(f'  TONS:    {phase6_tons:,.0f} ({phase6_tons/total_tons*100:.1f}%)')
