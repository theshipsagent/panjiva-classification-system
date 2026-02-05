import pandas as pd
import sys

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Load data
df = pd.read_csv(r'G:\My Drive\LLM\project_manifest\panjiva_production_v1\03_output\classified\panjiva_2024_classified_v4.0.0_OPTIMIZED.csv', low_memory=False)

print('='*80)
print('INVESTIGATING MYSTERY CRUDE OIL CASES')
print('='*80)

# Find crude-related records
crude_pattern = 'crude oil|crude|maya|arab|basrah|isthmus|hibernia|cold lake|wti|syncrude|dco|oriente|forties|sarir|vasconia|blend crude|amenam|merey'
mask = df['Goods Shipped'].fillna('').str.contains(crude_pattern, case=False, na=False, regex=True)
crude_records = df[mask].copy()

# Find TBN mystery cases
tbn_records = crude_records[
    (crude_records['Group'] == 'TBN') |
    (crude_records['Commodity'] == 'TBN') |
    (crude_records['Cargo'] == 'TBN')
]

mystery_tbn = tbn_records[
    (tbn_records['HS2'] == 27.0) &
    (tbn_records['Package_Type'].isin(['LBK', 'BLK', 'BBL'])) &
    (tbn_records['Tons'] >= 250) &
    (tbn_records['Tons'] <= 175000)
]

print(f'\nMYSTERY TBN CASES: {len(mystery_tbn)} records, {mystery_tbn["Tons"].sum():,.2f} tons')
print('These records meet ALL criteria for CRUDE-OIL rule but stopped at TBN')
print()

# Sample top 20 mystery cases
print('Top 20 Mystery TBN Cases:')
print('-'*80)

samples = mystery_tbn.nlargest(20, 'Tons')
for idx, row in samples.iterrows():
    print(f"\n{row['Goods Shipped'][:100]}")
    print(f"  Tons: {row['Tons']:,.2f} | HS2={row['HS2']} HS4={row['HS4']} | Pkg={row['Package_Type']}")
    print(f"  Phase={row['Classified_Phase']} | Rule={row['Last_Rule_ID']}")
    print(f"  Classification: {row['Group']} -> {row['Commodity']} -> {row['Cargo']}")

    # Check if goods description contains crude keywords
    goods = str(row['Goods Shipped']).lower()
    crude_keywords = ['crude oil', 'crude', 'maya', 'arab', 'basrah', 'amenam', 'payara', 'utapate']
    matched_keywords = [kw for kw in crude_keywords if kw in goods]
    print(f"  Matched keywords: {matched_keywords}")

# Find blank/unmatched mystery cases
blank_records = crude_records[
    crude_records['Group'].isna() |
    (crude_records['Group'] == '') |
    ((crude_records['Group'] != 'Liquid Bulk') &
     (crude_records['Group'] != 'EXCLUDED') &
     (crude_records['Group'] != 'TBN'))
]

mystery_blank = blank_records[
    (blank_records['HS2'] == 27.0) &
    (blank_records['Package_Type'].isin(['LBK', 'BLK', 'BBL'])) &
    (blank_records['Tons'] >= 250) &
    (blank_records['Tons'] <= 175000)
]

print()
print('='*80)
print(f'\nMYSTERY BLANK CASES: {len(mystery_blank)} records, {mystery_blank["Tons"].sum():,.2f} tons')
print('These records meet ALL criteria but have no classification at all')
print()

print('Top 20 Mystery Blank Cases:')
print('-'*80)

samples = mystery_blank.nlargest(20, 'Tons')
for idx, row in samples.iterrows():
    print(f"\n{row['Goods Shipped'][:100]}")
    print(f"  Tons: {row['Tons']:,.2f} | HS2={row['HS2']} HS4={row['HS4']} | Pkg={row['Package_Type']}")
    print(f"  Phase={row['Classified_Phase']} | Rule={row['Last_Rule_ID']}")
    print(f"  Classification: Group='{row['Group']}' Commodity='{row['Commodity']}'")

    # Check if goods description contains crude keywords
    goods = str(row['Goods Shipped']).lower()
    crude_keywords = ['crude oil', 'crude', 'maya', 'arab', 'basrah', 'amenam', 'payara', 'utapate', 'mero', 'hibernia']
    matched_keywords = [kw for kw in crude_keywords if kw in goods]
    print(f"  Matched keywords: {matched_keywords}")

# Check for specific keyword coverage issues
print()
print('='*80)
print('KEYWORD COVERAGE ANALYSIS')
print('='*80)

# Dictionary keywords
dict_keywords = ['crude oil', 'maya', 'arab', 'basrah', 'isthmus', 'hibernia', 'cold lake', 'wti', 'syncrude', 'dco', 'oriente', 'forties', 'sarir', 'vasconia', 'blend crude']

# Combine both mystery sets
all_mystery = pd.concat([mystery_tbn, mystery_blank])

print(f'\nTotal mystery cases: {len(all_mystery)} records, {all_mystery["Tons"].sum():,.2f} tons')
print('\nChecking which keywords appear in mystery cases but are NOT in dictionary:')

# Extract unique keywords from mystery cases
mystery_keywords = set()
for goods in all_mystery['Goods Shipped'].fillna(''):
    goods_lower = goods.lower()
    # Look for crude-related terms
    if 'crude' in goods_lower:
        # Extract words around 'crude'
        words = goods_lower.split()
        for i, word in enumerate(words):
            if 'crude' in word:
                # Get 2 words before and after
                context = ' '.join(words[max(0, i-2):min(len(words), i+3)])
                mystery_keywords.add(context)

print('\nSample mystery keywords not in dictionary:')
for i, kw in enumerate(sorted(mystery_keywords)[:20]):
    print(f"  {kw}")

# Check specific examples
print()
print('='*80)
print('SPECIFIC VARIANT ANALYSIS')
print('='*80)

# Check for specific crude variants that might be missing
variants_to_check = {
    'amenam': mystery_tbn[mystery_tbn['Goods Shipped'].str.contains('amenam', case=False, na=False)],
    'payara': mystery_tbn[mystery_tbn['Goods Shipped'].str.contains('payara', case=False, na=False)],
    'utapate': mystery_tbn[mystery_tbn['Goods Shipped'].str.contains('utapate', case=False, na=False)],
    'mero': mystery_blank[mystery_blank['Goods Shipped'].str.contains('mero', case=False, na=False)]
}

for variant, variant_df in variants_to_check.items():
    if len(variant_df) > 0:
        print(f"\n{variant.upper()}: {len(variant_df)} records, {variant_df['Tons'].sum():,.2f} tons")
        print(f"  Sample: {variant_df.iloc[0]['Goods Shipped'][:100]}")
        print(f"  IN DICTIONARY? {'YES' if variant in ' '.join(dict_keywords).lower() else 'NO'}")

# Phase analysis
print()
print('='*80)
print('PHASE ANALYSIS OF MYSTERY CASES')
print('='*80)

print('\nPhase distribution for mystery TBN cases:')
phase_dist = mystery_tbn['Classified_Phase'].value_counts().sort_index()
for phase, count in phase_dist.items():
    tons = mystery_tbn[mystery_tbn['Classified_Phase'] == phase]['Tons'].sum()
    print(f"  Phase {phase}: {count} records, {tons:,.2f} tons")

print('\nRule distribution for mystery TBN cases:')
rule_dist = mystery_tbn['Last_Rule_ID'].value_counts()
for rule, count in rule_dist.items():
    tons = mystery_tbn[mystery_tbn['Last_Rule_ID'] == rule]['Tons'].sum()
    print(f"  {rule}: {count} records, {tons:,.2f} tons")

print()
print('='*80)
print('DIAGNOSIS')
print('='*80)

print('\nThe mystery cases appear to be:')
print('  1. Records that matched Phase 2 (CARRIER-TANKER) which set Group=Liquid Bulk')
print('  2. But then did NOT match Phase 4 (CRUDE-OIL) or Phase 5 (CRUDE-OIL-P5)')
print('  3. Despite having correct HS2, Package Type, and tonnage')
print('\nPossible root causes:')
print('  A. Keyword matching is case-sensitive or has whitespace issues')
print('  B. Missing crude oil variants in dictionary (AMENAM, PAYARA, MERO, etc.)')
print('  C. Lock flags from Phase 2 preventing Phase 4/5 from refining')
print('  D. Classification script logic error in apply_rule or can_apply_rule functions')
