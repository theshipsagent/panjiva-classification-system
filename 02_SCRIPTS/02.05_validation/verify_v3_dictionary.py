"""
Verify v3.0.0 dictionary structure and report any missing pieces

Author: WSD3 / Claude Code
Date: 2026-01-14
"""

import pandas as pd

df = pd.read_csv('../01_DICTIONARIES/03.01_cargo_classification/cargo_classification_dictionary_v3.0.0_20260114_0200.csv', dtype=str)
df_user = pd.read_csv('../user_notes/01_cargo_dictionary_harmonized_user_edits_01132016_1829.csv', dtype=str)

print('=== DICTIONARY v3.0.0 VERIFICATION ===')
print()
print(f'Total Rules: {len(df)}')
print()

# Phase distribution
print('Phase Distribution:')
for phase in sorted(df['Phase'].unique(), key=lambda x: int(x)):
    count = len(df[df['Phase'] == phase])
    print(f'  Phase {phase}: {count:3d} rules')
print()

# Tonnage filters
has_either = len(df[((df['Min_Tons'].notna()) & (df['Min_Tons'] != '')) |
                     ((df['Max_Tons'].notna()) & (df['Max_Tons'] != ''))])
print(f'Tonnage Filters: {has_either} / {len(df)} rules ({has_either/len(df)*100:.1f}%)')
print()

# Authoritative rules
auth_rules = df[df['Note'].str.contains('AUTHORITATIVE', na=False)]
print(f'Authoritative Rules: {len(auth_rules)} (marked DO NOT EDIT)')
print()

# Group distribution
print('Top 5 Groups:')
groups = df['Group'].value_counts().head(5)
for group, count in groups.items():
    print(f'  {str(group)[:20]:20s}: {count:3d} rules')
print()

# Compare to original
print('=== COMPARISON TO ORIGINAL USER DICTIONARY ===')
print(f'Original user dictionary: {len(df_user)} rules')
print(f'Phase 6 in v3.0.0:        {len(df[df["Phase"] == "6"])} rules')
print()

# Check for missing rules
if len(df[df['Phase'] == '6']) == len(df_user):
    print('OK: All user rules successfully migrated to Phase 6')
else:
    diff = len(df_user) - len(df[df['Phase'] == '6'])
    print(f'WARNING: {diff} rules may be missing from Phase 6')
print()

# Sample Phase 6 rules
print('Sample Phase 6 (User Authoritative) Rules:')
phase6 = df[df['Phase'] == '6'].head(5)
for _, rule in phase6.iterrows():
    hs = rule.get('HS6') or rule.get('HS4') or rule.get('HS2') or ''
    kw = str(rule.get('Keywords', ''))[:25]
    group = str(rule.get('Group', ''))[:15]
    commodity = str(rule.get('Commodity', ''))[:15]
    print(f'  {rule["Rule_ID"]:15s} HS={hs:6s} {group:15s} > {commodity:15s} [{kw}]')
print()

print('=== MISSING COMPONENTS CHECK ===')
missing = []

# Check Phase 4 (should be empty)
phase4 = len(df[df['Phase'] == '4'])
if phase4 == 0:
    missing.append('Phase 4: No rules (needs commodity-level refinement)')

# Check Phase 5 (should have 1 rule)
phase5 = len(df[df['Phase'] == '5'])
print(f'Phase 5 (special cases): {phase5} rules')

# Check tonnage coverage on Phase 6
phase6_tons = df[df['Phase'] == '6']
phase6_with_tons = len(phase6_tons[((phase6_tons['Min_Tons'].notna()) & (phase6_tons['Min_Tons'] != '')) |
                                    ((phase6_tons['Max_Tons'].notna()) & (phase6_tons['Max_Tons'] != ''))])
if phase6_with_tons < len(phase6_tons) * 0.8:
    missing.append(f'Phase 6 tonnage coverage: Only {phase6_with_tons}/{len(phase6_tons)} rules have Min/Max Tons')

if missing:
    print()
    print('MISSING COMPONENTS:')
    for item in missing:
        print(f'  - {item}')
else:
    print('OK: No missing components detected')
