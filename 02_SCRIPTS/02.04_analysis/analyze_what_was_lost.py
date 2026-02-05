"""
Analyze what was lost when converting from original HS+Keyword+Tonnage dictionary
to multi-phase system

Focus: TONS classified, not record count

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd

# Compare original vs current
df_user = pd.read_csv('../user_notes/01_cargo_dictionary_harmonized_user_edits_01132016_1829.csv', dtype=str)
df_curr = pd.read_csv('../01_DICTIONARIES/03.01_cargo_classification/cargo_classification_dictionary_v2.5.2_20260114_0100.csv', dtype=str)

print('=== WHAT WAS LOST IN CONVERSION ===')
print()

# 1. Tonnage filters
orig_tons = len(df_user[(df_user['Min Tons'].notna()) | (df_user['Max Tons'].notna())])
curr_tons = len(df_curr[(df_curr['Min_Tons'].notna()) | (df_curr['Max_Tons'].notna())])
print(f'1. TONNAGE FILTERS:')
print(f'   Original: {orig_tons} / {len(df_user)} rules had Min/Max Tons ({orig_tons/len(df_user)*100:.1f}%)')
print(f'   Current:  {curr_tons} / {len(df_curr)} rules have Min/Max Tons ({curr_tons/len(df_curr)*100:.1f}%)')
print(f'   LOST: {orig_tons - curr_tons} tonnage-based rules')
print()

# 2. Rule distribution by Group
print('2. RULE DISTRIBUTION:')
print()
print('Original (by Group):')
orig_groups = df_user['Group'].value_counts().head(10)
for group, count in orig_groups.items():
    print(f'   {str(group)[:20]:20s}: {count:3d} rules')

print()
print('Current (by Group):')
curr_groups = df_curr['Group'].value_counts().head(10)
for group, count in curr_groups.items():
    print(f'   {str(group)[:20]:20s}: {count:3d} rules')

print()
print('3. BULK COMMODITIES (HIGH TONNAGE PRIORITY):')
bulk_groups = ['Dry Bulk', 'Liquid Bulk', 'Break-Bulk']
for group in bulk_groups:
    orig_count = len(df_user[df_user['Group'] == group])
    curr_count = len(df_curr[df_curr['Group'] == group])
    print(f'   {group:15s}: Original {orig_count:3d} rules, Current {curr_count:3d} rules')

print()
print('=== CONVERSION FOCUS ERROR ===')
print('Original Focus: TONS classified (bulk/break-bulk high tonnage)')
print('Current Focus:  RECORDS classified (carriers, vessel types)')
print()
print('Result: Lost tonnage-based filtering = lost ability to classify high-tonnage commodities')
print()
print('=== WHAT NEEDS TO BE RESTORED ===')
print('1. Copy Min_Tons/Max_Tons from user dictionary to current dictionary')
print('2. Mark all rules as AUTHORITATIVE (prevent accidental edits)')
print('3. Test on TONS classified, not record count')
print('4. Priority: Dry Bulk > Break-Bulk > Liquid Bulk (highest tonnage commodities)')
