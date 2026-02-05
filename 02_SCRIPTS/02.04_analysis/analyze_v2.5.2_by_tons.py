"""
Analyze v2.5.2 classification results by TONS, not records

Focus: What % of TONNAGE is classified, not record count

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd
import numpy as np

# Load latest classification results (from v2.5.1 test, revert to 2.5.2 pending)
df = pd.read_csv('../03_DOCUMENTATION/03.04_summaries/sample_test_15k/sample_15k_classified_v2.5.1.csv', dtype=str)

print('=== TONS-BASED ANALYSIS (15k Sample) ===')
print()

# Convert tons to numeric
df['Tons_Numeric'] = pd.to_numeric(df['Tons'].str.replace(',', ''), errors='coerce').fillna(0)

total_tons = df['Tons_Numeric'].sum()
print(f'Total Tonnage in Sample: {total_tons:,.0f} tons')
print()

# Group-level classification
group_classified = df[(df['Group'] != '') & (df['Group'].notna())]
group_tons = group_classified['Tons_Numeric'].sum()
print(f'1. GROUP CLASSIFIED:')
print(f'   Records: {len(group_classified):,} / {len(df):,} ({len(group_classified)/len(df)*100:.1f}%)')
print(f'   TONS:    {group_tons:,.0f} / {total_tons:,.0f} ({group_tons/total_tons*100:.1f}%)')
print()

# Fully classified (no TBN)
fully_classified = df[
    (df['Group'] != '') & (df['Group'].notna()) &
    (df['Commodity'] != 'TBN') & (df['Commodity'].notna()) &
    (df['Cargo'] != 'TBN') & (df['Cargo'].notna()) &
    (df['Cargo Detail'] != 'TBN') & (df['Cargo Detail'].notna())
]
fully_tons = fully_classified['Tons_Numeric'].sum()
print(f'2. FULLY CLASSIFIED (No TBN):')
print(f'   Records: {len(fully_classified):,} / {len(df):,} ({len(fully_classified)/len(df)*100:.1f}%)')
print(f'   TONS:    {fully_tons:,.0f} / {total_tons:,.0f} ({fully_tons/total_tons*100:.1f}%)')
print()

# TBN placeholders
tbn_records = df[(df['Commodity'] == 'TBN') | (df['Cargo'] == 'TBN')]
tbn_tons = tbn_records['Tons_Numeric'].sum()
print(f'3. TBN PLACEHOLDERS (Needs Refinement):')
print(f'   Records: {len(tbn_records):,} / {len(df):,} ({len(tbn_records)/len(df)*100:.1f}%)')
print(f'   TONS:    {tbn_tons:,.0f} / {total_tons:,.0f} ({tbn_tons/total_tons*100:.1f}%)')
print()

# Breakdown by Group
print('4. TONNAGE BY GROUP:')
group_summary = df.groupby('Group')['Tons_Numeric'].agg(['sum', 'count']).sort_values('sum', ascending=False)
for group, row in group_summary.head(10).iterrows():
    pct = row['sum'] / total_tons * 100
    print(f'   {str(group)[:20]:20s}: {row["sum"]:15,.0f} tons ({pct:5.1f}%) - {int(row["count"]):,} records')

print()
print('=== KEY INSIGHT ===')
print('Record count ≠ Tonnage')
print('Must focus on high-tonnage commodities (Dry Bulk, Liquid Bulk, Break-Bulk)')
print('Carriers (Ro/Ro) = High record count, LOW tonnage')
