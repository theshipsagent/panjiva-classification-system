import pandas as pd
import re
from collections import defaultdict

# File paths
classified_file = r"G:\My Drive\LLM\project_manifest\panjiva_production_v1\03_output\classified\panjiva_2024_classified_v4.0.0_OPTIMIZED.csv"
dictionary_file = r"G:\My Drive\LLM\project_manifest\panjiva_production_v1\01_dictionary\cargo_classification_dictionary_v4.0.0_SIMPLE.csv"
output_file = r"G:\My Drive\LLM\project_manifest\panjiva_production_v1\sugar_analysis.txt"

print("=" * 80)
print("SUGAR FRAGMENTATION ANALYSIS - 2024 DATA")
print("=" * 80)
print()

# Load dictionary
print("[1] Loading dictionary...")
dict_df = pd.read_csv(dictionary_file)
sugar_rules = dict_df[dict_df['Rule_ID'].str.contains('SUGAR|MOLASSES', case=False, na=False)]
print(f"Found {len(sugar_rules)} sugar-related rules:")
print()
for idx, row in sugar_rules.iterrows():
    print(f"  Rule: {row['Rule_ID']}")
    print(f"    Phase: {row['Phase']}, Active: {row['Active']}")
    print(f"    HS2: {row['HS2']}, HS4: {row['HS4']}")
    print(f"    Keywords: {row['Keywords']}")
    print(f"    Package_Type: {row['Package_Type']}")
    print(f"    Output: {row['Group']} > {row['Commodity']} > {row['Cargo']} > {row['Cargo_Detail']}")
    print()

# Load classified data
print("[2] Loading classified data (~386MB)...")
df = pd.read_csv(classified_file, low_memory=False)
print(f"Total records: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print()

# Find sugar/cane records by multiple search methods
print("[3] Searching for SUGAR/CANE records...")
print()

# Method 1: HS Code 17 (Sugar)
hs17_mask = (df['HS2'] == '17') | (df['HS4'].astype(str).str.startswith('17', na=False))
sugar_by_hs = df[hs17_mask].copy()
print(f"Records with HS2/HS4 = 17 (Sugar): {len(sugar_by_hs):,} records, {sugar_by_hs['Tons'].sum():,.0f} MT")

# Method 2: Keywords containing SUGAR/CANE
keywords_sugar = (
    df['Goods Shipped'].fillna('').str.contains('SUGAR|CANE', case=False, na=False) |
    df['HS Code Desc.'].fillna('').str.contains('SUGAR|CANE', case=False, na=False)
)
sugar_by_keyword = df[keywords_sugar].copy()
print(f"Records with SUGAR/CANE in Goods Shipped or HS Code Desc: {len(sugar_by_keyword):,} records, {sugar_by_keyword['Tons'].sum():,.0f} MT")

# Combine both
sugar_combined_mask = hs17_mask | keywords_sugar
sugar_records = df[sugar_combined_mask].copy()
print(f"Combined (unique): {len(sugar_records):,} records, {sugar_records['Tons'].sum():,.0f} MT")
print()

# Classification breakdown
print("[4] CLASSIFICATION BREAKDOWN:")
print()

# Status by Group classification
print("Status by Group Classification:")
status_breakdown = {}
for status in sugar_records['Group'].unique():
    status_str = str(status) if pd.notna(status) else "NaN"
    count = len(sugar_records[sugar_records['Group'] == status])
    tonnage = sugar_records[sugar_records['Group'] == status]['Tons'].sum()
    status_breakdown[status_str] = {'count': count, 'tonnage': tonnage}
    print(f"  {status_str:30s}: {count:7,} records, {tonnage:12,.0f} MT")

print()

# Show classified vs TBN
classified = sugar_records[sugar_records['Group'] != 'TBN']
tbn = sugar_records[sugar_records['Group'] == 'TBN']

print(f"Classified (Group != TBN): {len(classified):,} records, {classified['Tons'].sum():,.0f} MT")
print(f"TBN (Group == TBN):        {len(tbn):,} records, {tbn['Tons'].sum():,.0f} MT")
print()

# Show commodity breakdown for classified records
if len(classified) > 0:
    print("Classified Records - Commodity Breakdown:")
    commodity_breakdown = classified.groupby('Commodity')['Tons'].agg(['sum', 'count'])
    commodity_breakdown = commodity_breakdown.sort_values('sum', ascending=False)
    for commodity, row in commodity_breakdown.iterrows():
        print(f"  {commodity:30s}: {int(row['count']):7,} records, {row['sum']:12,.0f} MT")
    print()

# Show TBN commodity breakdown
if len(tbn) > 0:
    print("TBN Records - Commodity Breakdown:")
    tbn_commodity = tbn.groupby('Commodity')['Tons'].agg(['sum', 'count'])
    tbn_commodity = tbn_commodity.sort_values('sum', ascending=False)
    for commodity, row in tbn_commodity.iterrows():
        print(f"  {commodity:30s}: {int(row['count']):7,} records, {row['sum']:12,.0f} MT")
    print()

# Check which rules classified them
print("[5] CLASSIFICATION RULES APPLIED:")
print()

print("Rules that classified sugar records:")
rules_applied = classified['Last_Rule_ID'].value_counts()
for rule_id, count in rules_applied.head(20).items():
    rule_tonnage = classified[classified['Last_Rule_ID'] == rule_id]['Tons'].sum()
    print(f"  {str(rule_id):25s}: {count:7,} records, {rule_tonnage:12,.0f} MT")

print()
print("Phase distribution:")
phase_dist = classified['Classified_Phase'].value_counts().sort_index()
for phase, count in phase_dist.items():
    phase_tonnage = classified[classified['Classified_Phase'] == phase]['Tons'].sum()
    print(f"  Phase {phase}: {count:7,} records, {phase_tonnage:12,.0f} MT")

print()

# Why aren't TBN records being matched?
if len(tbn) > 0:
    print("[6] ANALYSIS OF TBN RECORDS:")
    print()

    # Check HS codes
    print("HS Codes in TBN records:")
    hs_dist = tbn['HS4'].value_counts().head(10)
    for hs, count in hs_dist.items():
        print(f"  HS4 {hs}: {count} records")
    print()

    # Check package types
    if 'Package_Type' in tbn.columns:
        print("Package Types in TBN records:")
        pkg_dist = tbn['Package_Type'].value_counts().head(10)
        for pkg, count in pkg_dist.items():
            print(f"  {pkg}: {count} records")
        print()

    # Check weights
    print("Weight distribution in TBN records:")
    print(f"  Min: {tbn['Tons'].min():,.0f} MT")
    print(f"  Max: {tbn['Tons'].max():,.0f} MT")
    print(f"  Mean: {tbn['Tons'].mean():,.2f} MT")
    print(f"  Median: {tbn['Tons'].median():,.0f} MT")
    print()

    # Show sample TBN records
    print("Sample TBN records (first 10):")
    sample_cols = ['Bill of Lading Number', 'HS Code Desc.', 'Goods Shipped', 'Tons', 'HS2', 'HS4', 'Package_Type', 'Vessel_Type_Simple']
    sample = tbn[sample_cols].head(10)
    for idx, row in sample.iterrows():
        print(f"\n  Record: {row['Bill of Lading Number']}")
        print(f"    HS Code Desc: {row['HS Code Desc.']}")
        print(f"    Goods: {row['Goods Shipped']}")
        print(f"    HS4: {row['HS4']}, Tonnage: {row['Tons']:,.0f}")
        print(f"    Package: {row['Package_Type']}, Vessel: {row['Vessel_Type_Simple']}")

print()

# ROOT CAUSE ANALYSIS
print("[7] ROOT CAUSE ANALYSIS:")
print()

# Check dictionary has sugar rules
sugar_dict_rules = dict_df[dict_df['Rule_ID'].str.contains('SUGAR', case=False, na=False)]
print(f"[OK] Dictionary HAS sugar rules: {len(sugar_dict_rules)} rules found")
print()

# Why aren't they matching?
print("Checking rule matching criteria:")
print()

# Rule 1: SUGAR (HS4 1701, keywords, 2500-75000 tons)
sugar_rule = dict_df[dict_df['Rule_ID'] == 'SUGAR']
if len(sugar_rule) > 0:
    rule = sugar_rule.iloc[0]
    print(f"SUGAR rule requirements:")
    print(f"  HS4: {rule['HS4']}")
    print(f"  Keywords: {rule['Keywords']}")
    print(f"  Min/Max Tons: {rule['Min_Tons']}/{rule['Max_Tons']}")
    print(f"  Phase: {rule['Phase']}, Active: {rule['Active']}")
    print()

    # Check how many tbn records have HS4 1701
    tbn_1701 = tbn[tbn['HS4'].astype(str).str.strip() == '1701']
    print(f"  TBN records with HS4 1701: {len(tbn_1701):,} records, {tbn_1701['Tons'].sum():,.0f} MT")

    # Check tonnage range
    min_tons = rule['Min_Tons']
    max_tons = rule['Max_Tons']
    if pd.notna(min_tons) and pd.notna(max_tons):
        min_tons = float(min_tons)
        max_tons = float(max_tons)
        tbn_tonnage_ok = tbn[(tbn['Tons'].astype(float) >= min_tons) & (tbn['Tons'].astype(float) <= max_tons)]
        print(f"  TBN records in tonnage range ({min_tons}-{max_tons}): {len(tbn_tonnage_ok):,} records, {tbn_tonnage_ok['Tons'].sum():,.0f} MT")
    print()

# Check if rules are active
print(f"Sugar rules active status:")
for idx, row in sugar_rules.iterrows():
    print(f"  {row['Rule_ID']}: Active={row['Active']}, Phase={row['Phase']}")

print()

# Generate summary statistics
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print()

total_sugar_tonnage = sugar_records['Tons'].sum()
classified_sugar_tonnage = classified['Tons'].sum()
tbn_sugar_tonnage = tbn['Tons'].sum()

print(f"Total Sugar/Cane records found:        {len(sugar_records):,} records, {total_sugar_tonnage:,.0f} MT")
print(f"  - Classified:                        {len(classified):,} records, {classified_sugar_tonnage:,.0f} MT ({100*classified_sugar_tonnage/total_sugar_tonnage:.1f}%)")
print(f"  - TBN (To Be Named):                 {len(tbn):,} records, {tbn_sugar_tonnage:,.0f} MT ({100*tbn_sugar_tonnage/total_sugar_tonnage:.1f}%)")
print()

# Write findings to output file
with open(output_file, 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("SUGAR FRAGMENTATION ANALYSIS - 2024 DATA\n")
    f.write("=" * 80 + "\n\n")

    f.write("[1] DICTIONARY SUGAR RULES\n")
    f.write("-" * 80 + "\n")
    f.write(f"Status: [OK] Dictionary HAS sugar rules ({len(sugar_rules)} rules)\n\n")
    for idx, row in sugar_rules.iterrows():
        f.write(f"Rule: {row['Rule_ID']}\n")
        f.write(f"  Phase: {row['Phase']}, Active: {row['Active']}\n")
        f.write(f"  HS2: {row['HS2']}, HS4: {row['HS4']}\n")
        f.write(f"  Keywords: {row['Keywords']}\n")
        f.write(f"  Package_Type: {row['Package_Type']}\n")
        f.write(f"  Output: {row['Group']} > {row['Commodity']} > {row['Cargo']} > {row['Cargo_Detail']}\n\n")

    f.write("\n[2] CLASSIFICATION RESULTS\n")
    f.write("-" * 80 + "\n")
    f.write(f"Total Sugar/Cane records:  {len(sugar_records):,} records\n")
    f.write(f"Total Sugar/Cane tonnage:  {total_sugar_tonnage:,.0f} MT\n\n")

    f.write("Status Breakdown:\n")
    for status, data in sorted(status_breakdown.items()):
        pct = 100 * data['tonnage'] / total_sugar_tonnage
        f.write(f"  {status:30s}: {data['count']:7,} records, {data['tonnage']:12,.0f} MT ({pct:5.1f}%)\n")

    f.write(f"\nClassified:     {len(classified):,} records, {classified_sugar_tonnage:,.0f} MT ({100*classified_sugar_tonnage/total_sugar_tonnage:.1f}%)\n")
    f.write(f"TBN:            {len(tbn):,} records, {tbn_sugar_tonnage:,.0f} MT ({100*tbn_sugar_tonnage/total_sugar_tonnage:.1f}%)\n")

    f.write("\n\n[3] ROOT CAUSE ANALYSIS\n")
    f.write("-" * 80 + "\n")

    f.write("\nCONCLUSION:\n")
    if tbn_sugar_tonnage == 0:
        f.write("[OK] All sugar records are CLASSIFIED. No fragmentation gap found.\n")
    elif len(sugar_rules) == 0:
        f.write("[ERROR] NO SUGAR RULES IN DICTIONARY\n")
        f.write("  This is a missing commodity gap. Sugar rules need to be added.\n")
    else:
        f.write(f"[WARNING] PARTIAL CLASSIFICATION: {tbn_sugar_tonnage:,.0f} MT ({100*tbn_sugar_tonnage/total_sugar_tonnage:.1f}%) remains TBN\n\n")

        # Analyze why TBN records aren't matching
        f.write("Analyzing TBN records:\n")

        if len(tbn) > 0:
            # Check HS codes
            tbn_1701 = len(tbn[tbn['HS4'].astype(str).str.strip() == '1701'])
            f.write(f"  - TBN records with HS4 1701: {tbn_1701} records\n")

            # Check tonnage
            sugar_rule = dict_df[dict_df['Rule_ID'] == 'SUGAR']
            if len(sugar_rule) > 0:
                min_tons = sugar_rule.iloc[0]['Min_Tons']
                max_tons = sugar_rule.iloc[0]['Max_Tons']
                tbn_tonnage_ok = len(tbn[(tbn['Tons'] >= min_tons) & (tbn['Tons'] <= max_tons)])
                f.write(f"  - TBN records in range {min_tons}-{max_tons}: {tbn_tonnage_ok} records\n")

            # Check vessel types
            f.write(f"  - TBN vessel types: {tbn['Vessel_Type_Simple'].value_counts().to_dict()}\n")

            f.write(f"\n  Possible causes:\n")
            f.write(f"    1. Tonnage outside rule range (min {rule['Min_Tons']}, max {rule['Max_Tons']})\n")
            f.write(f"    2. HS4 code not 1701 (different sugar product)\n")
            f.write(f"    3. Keywords don't match exactly (spelling, abbreviations)\n")
            f.write(f"    4. Vessel type doesn't match rule criteria\n")
            f.write(f"    5. Phase ordering issue (later phases not refining early matches)\n")

print()
print(f"Analysis saved to: {output_file}")

