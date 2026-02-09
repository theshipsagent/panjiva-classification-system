"""
Validation script for Party Harmonization Dictionary v1.2.0

Checks for:
- Duplicate Entity_IDs
- Duplicate Match_Keywords conflicts
- Invalid Match_Strategy values
- Missing required fields
- Tonnage coverage analysis
"""

import pandas as pd

# Load v1.2.0
dict_path = r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.06_parties\party_harmonization_master_v1.2.0.csv"
df = pd.read_csv(dict_path)

print("=" * 80)
print("PARTY HARMONIZATION DICTIONARY v1.2.0 VALIDATION")
print("=" * 80)
print()

# Basic stats
print("BASIC STATISTICS")
print("-" * 80)
print(f"Total entities: {len(df)}")
print(f"Active entities: {df['Active'].sum()}")
print(f"Inactive entities: {(~df['Active']).sum()}")
print()

# Check for duplicates
print("DUPLICATE CHECKS")
print("-" * 80)

# Entity_ID duplicates
dup_ids = df[df.duplicated('Entity_ID', keep=False)]
if len(dup_ids) > 0:
    print(f"WARNING: Found {len(dup_ids)} duplicate Entity_IDs:")
    print(dup_ids[['Entity_ID', 'Canonical_Name']])
else:
    print("[OK] No duplicate Entity_IDs found")

# Check for potential keyword conflicts (keywords that appear in multiple entities)
print("\nKEYWORD OVERLAP ANALYSIS")
print("-" * 80)

# Expand keywords
keyword_map = []
for _, row in df.iterrows():
    keywords = str(row['Match_Keywords']).split(';')
    for kw in keywords:
        kw = kw.strip()
        if kw and kw != 'nan':
            keyword_map.append({
                'Entity_ID': row['Entity_ID'],
                'Canonical_Name': row['Canonical_Name'],
                'Keyword': kw,
                'Match_Strategy': row['Match_Strategy']
            })

df_kw = pd.DataFrame(keyword_map)

# Find keywords used by multiple entities
kw_counts = df_kw.groupby('Keyword').size()
overlapping = kw_counts[kw_counts > 1]

if len(overlapping) > 0:
    print(f"WARNING: Found {len(overlapping)} keywords used by multiple entities:")
    for kw, count in overlapping.head(10).items():
        entities = df_kw[df_kw['Keyword'] == kw][['Entity_ID', 'Canonical_Name']].values
        print(f"\n  '{kw}' used by {count} entities:")
        for ent_id, name in entities:
            print(f"    - {ent_id}: {name}")
else:
    print("[OK] No keyword overlaps found")

print()

# Validate Match_Strategy values
print("MATCH STRATEGY VALIDATION")
print("-" * 80)
valid_strategies = ['Contains', 'Contains_All', 'Exact']
invalid_strat = df[~df['Match_Strategy'].isin(valid_strategies)]
if len(invalid_strat) > 0:
    print(f"WARNING: Found {len(invalid_strat)} entities with invalid Match_Strategy:")
    print(invalid_strat[['Entity_ID', 'Match_Strategy']])
else:
    print("[OK] All Match_Strategy values are valid")

strategy_counts = df['Match_Strategy'].value_counts()
print("\nMatch Strategy distribution:")
for strat, count in strategy_counts.items():
    print(f"  {strat}: {count} entities ({count/len(df)*100:.1f}%)")

print()

# Category validation
print("CATEGORY VALIDATION")
print("-" * 80)
valid_categories = ['All', 'Consignee', 'Shipper']
invalid_cat = df[~df['Category'].isin(valid_categories)]
if len(invalid_cat) > 0:
    print(f"WARNING: Found {len(invalid_cat)} entities with invalid Category:")
    print(invalid_cat[['Entity_ID', 'Category']])
else:
    print("[OK] All Category values are valid")

cat_counts = df['Category'].value_counts()
print("\nCategory distribution:")
for cat, count in cat_counts.items():
    print(f"  {cat}: {count} entities ({count/len(df)*100:.1f}%)")

print()

# Missing values check
print("MISSING VALUES CHECK")
print("-" * 80)
required_fields = ['Entity_ID', 'Canonical_Name', 'Entity_Type', 'Match_Keywords',
                   'Match_Strategy', 'Category', 'Active']

for field in required_fields:
    missing = df[field].isna().sum()
    if missing > 0:
        print(f"WARNING: {field} has {missing} missing values")
    else:
        print(f"[OK] {field}: no missing values")

print()

# Entity Type distribution
print("ENTITY TYPE BREAKDOWN")
print("-" * 80)
type_stats = df.groupby('Entity_Type').agg({
    'Entity_ID': 'count',
    'Estimated_Tons': 'sum'
}).rename(columns={'Entity_ID': 'Count'}).sort_values('Estimated_Tons', ascending=False)

print(f"{'Entity Type':<30} {'Count':>8} {'Total Tons':>15} {'% Tons':>8}")
print("-" * 80)
total_tons = type_stats['Estimated_Tons'].sum()
for entity_type, row in type_stats.iterrows():
    pct = row['Estimated_Tons'] / total_tons * 100
    print(f"{entity_type:<30} {int(row['Count']):>8} {int(row['Estimated_Tons']):>15,} {pct:>7.1f}%")

print("-" * 80)
print(f"{'TOTAL':<30} {len(df):>8} {int(total_tons):>15,} {100.0:>7.1f}%")

print()

# Top entities by tonnage
print("TOP 30 ENTITIES BY ESTIMATED TONNAGE")
print("-" * 80)
print(f"{'Rank':<5} {'Entity ID':<25} {'Entity Type':<20} {'Tons':>15}")
print("-" * 80)

top30 = df.nlargest(30, 'Estimated_Tons')
for idx, (_, row) in enumerate(top30.iterrows(), 1):
    print(f"{idx:<5} {row['Entity_ID']:<25} {row['Entity_Type']:<20} {int(row['Estimated_Tons']):>15,}")

print()

# Safety analysis - Contains_All usage
print("SAFETY ANALYSIS - Contains_All Strategy")
print("-" * 80)
contains_all = df[df['Match_Strategy'] == 'Contains_All']
print(f"Entities using Contains_All: {len(contains_all)}")
print("\nContains_All entities (safe multi-token matching):")
for _, row in contains_all.iterrows():
    print(f"  {row['Entity_ID']:<25} {row['Match_Keywords']:<40} - {row['Notes'][:60]}")

print()

# Version comparison
print("VERSION COMPARISON")
print("-" * 80)
v1_1_path = r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.06_parties\party_harmonization_master_v1.1.0.csv"
df_v1_1 = pd.read_csv(v1_1_path)

print(f"v1.1.0 entities: {len(df_v1_1)}")
print(f"v1.2.0 entities: {len(df)}")
print(f"New entities: {len(df) - len(df_v1_1)}")
print(f"Growth: {(len(df) - len(df_v1_1)) / len(df_v1_1) * 100:.1f}%")
print()
print(f"v1.1.0 tonnage: {df_v1_1['Estimated_Tons'].sum():,.0f} tons")
print(f"v1.2.0 tonnage: {df['Estimated_Tons'].sum():,.0f} tons")
print(f"New tonnage: {df['Estimated_Tons'].sum() - df_v1_1['Estimated_Tons'].sum():,.0f} tons")

print()
print("=" * 80)
print("VALIDATION COMPLETE")
print("=" * 80)
