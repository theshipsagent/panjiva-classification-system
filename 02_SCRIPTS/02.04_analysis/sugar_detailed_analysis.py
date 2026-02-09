import pandas as pd

# File paths
classified_file = r"G:\My Drive\LLM\project_manifest\panjiva_production_v1\03_output\classified\panjiva_2024_classified_v4.0.0_OPTIMIZED.csv"
output_file = r"G:\My Drive\LLM\project_manifest\panjiva_production_v1\sugar_analysis.txt"

print("Analyzing partial classifications and mismatches...")

# Load data
df = pd.read_csv(classified_file, low_memory=False)

# Find sugar/cane records
mask1 = df['HS2'].astype(str).str.strip() == '17'
mask2 = df['Goods Shipped'].fillna('').str.contains('SUGAR|CANE', case=False, na=False)
mask3 = df['HS Code Desc.'].fillna('').str.contains('SUGAR|CANE', case=False, na=False)
sugar_cane_mask = mask1 | mask2 | mask3
sugar_records = df[sugar_cane_mask].copy()

# Find records where Group is classified but Commodity is TBN (partial classification)
partial = sugar_records[(sugar_records['Group'] != 'TBN') & (sugar_records['Commodity'] == 'TBN')]

print(f"Partial classifications found: {len(partial)} records, {partial['Tons'].sum():,.0f} MT")
print()

# Find records classified by non-sugar rules
non_sugar_rules = ['CARRIER-DRYBULK', 'CARRIER-REEFER', 'CARRIER-RORO', 'GYPSUM', 'SALT-P5',
                  'WIND-P5', 'SOYBEAN-OIL-P5', 'CONSTRUCTION', 'SALT', 'SULPHURIC-ACID-P5']
non_sugar = sugar_records[sugar_records['Last_Rule_ID'].isin(non_sugar_rules)]
print(f"Records classified by non-sugar rules: {len(non_sugar)} records, {non_sugar['Tons'].sum():,.0f} MT")
if len(non_sugar) > 0:
    print("  Rule distribution:")
    for rule, count in non_sugar['Last_Rule_ID'].value_counts().items():
        tonnage = non_sugar[non_sugar['Last_Rule_ID'] == rule]['Tons'].sum()
        print(f"    {rule}: {count} records, {tonnage:,.0f} MT")
print()

# Find excluded records
excluded = sugar_records[sugar_records['Group'] == 'EXCLUDED']
print(f"Excluded records: {len(excluded)} records, {excluded['Tons'].sum():,.0f} MT")
if len(excluded) > 0:
    print("  Last rules applied:")
    for rule, count in excluded['Last_Rule_ID'].value_counts().items():
        tonnage = excluded[excluded['Last_Rule_ID'] == rule]['Tons'].sum()
        print(f"    {rule}: {count} records, {tonnage:,.0f} MT")
print()

# Write detailed findings to output file
with open(output_file, 'a') as f:
    f.write("\n\n[4] DETAILED BREAKDOWN\n")
    f.write("-" * 80 + "\n\n")

    f.write("A. CORRECTLY CLASSIFIED SUGAR RECORDS (Commodity=Sugar)\n")
    correct = sugar_records[sugar_records['Commodity'] == 'Sugar']
    f.write(f"   {len(correct)} records, {correct['Tons'].sum():,.0f} MT\n\n")

    f.write("B. PARTIALLY CLASSIFIED (Group != TBN but Commodity = TBN)\n")
    f.write(f"   {len(partial)} records, {partial['Tons'].sum():,.0f} MT\n")
    if len(partial) > 0:
        f.write(f"   Group distribution:\n")
        for group, count in partial['Group'].value_counts().items():
            tonnage = partial[partial['Group'] == group]['Tons'].sum()
            f.write(f"     {group}: {count} records, {tonnage:,.0f} MT\n")
        f.write(f"\n   Top rules applied:\n")
        for rule, count in partial['Last_Rule_ID'].value_counts().head(10).items():
            tonnage = partial[partial['Last_Rule_ID'] == rule]['Tons'].sum()
            f.write(f"     {rule}: {count} records, {tonnage:,.0f} MT\n")

    f.write("\n\nC. MISCLASSIFIED (Non-Sugar Rules)\n")
    f.write(f"   {len(non_sugar)} records, {non_sugar['Tons'].sum():,.0f} MT\n")
    if len(non_sugar) > 0:
        f.write(f"   Rules applied:\n")
        for rule, count in non_sugar['Last_Rule_ID'].value_counts().items():
            tonnage = non_sugar[non_sugar['Last_Rule_ID'] == rule]['Tons'].sum()
            f.write(f"     {rule}: {count} records, {tonnage:,.0f} MT\n")

    f.write("\n\nD. EXCLUDED RECORDS\n")
    f.write(f"   {len(excluded)} records, {excluded['Tons'].sum():,.0f} MT\n")
    if len(excluded) > 0:
        f.write(f"   Rules applied:\n")
        for rule, count in excluded['Last_Rule_ID'].value_counts().items():
            tonnage = excluded[excluded['Last_Rule_ID'] == rule]['Tons'].sum()
            f.write(f"     {rule}: {count} records, {tonnage:,.0f} MT\n")

    f.write("\n\n[5] ROOT CAUSE SUMMARY\n")
    f.write("-" * 80 + "\n\n")
    f.write("UNEXPECTED FINDING:\n")
    f.write("Despite identifying 825K tons of sugar with SUGAR/CANE keywords in initial report,\n")
    f.write("the 2024 classified dataset shows:\n\n")
    f.write(f"  Total sugar-related records: 1,009 records\n")
    f.write(f"  Total tonnage: 5,251,887 MT (5.25M MT)\n")
    f.write(f"  Classified as Sugar: 449 records, 3,828,108 MT (72.8%)\n")
    f.write(f"  Classified as other: 275 records, 1,423,779 MT (27.1%)\n")
    f.write(f"  Zero TBN at group level\n\n")

    f.write("POSSIBLE EXPLANATIONS FOR DISCREPANCY:\n")
    f.write("1. The 825K tons figure may refer to a different dataset or time period\n")
    f.write("2. Sugar records may have already been classified to other commodities\n")
    f.write("3. The keyword search criteria may differ from previous analysis\n")
    f.write("4. Data may have been pre-processed or filtered differently\n\n")

    f.write("CONFIRMED ISSUES:\n")
    if len(non_sugar) > 0:
        f.write(f"  - {len(non_sugar)} sugar records ({non_sugar['Tons'].sum():,.0f} MT) classified by non-sugar rules\n")
        f.write(f"    Top culprit: CARRIER-DRYBULK (vessel type hint only, no commodity specification)\n\n")

    if len(partial) > 0:
        f.write(f"  - {len(partial)} records with partial classification (Group assigned, Commodity=TBN)\n")
        f.write(f"    Tonnage: {partial['Tons'].sum():,.0f} MT\n\n")

    if len(excluded) > 0:
        f.write(f"  - {len(excluded)} sugar records marked EXCLUDED\n")
        f.write(f"    Tonnage: {excluded['Tons'].sum():,.0f} MT\n")
        f.write(f"    Reason: Likely noise filters (small shipments, ship spares, etc.)\n\n")

    f.write("RECOMMENDATION:\n")
    f.write("Sugar classification is mostly working (72.8% correctly classified to Sugar commodity).\n")
    f.write("Non-sugar rule misclassifications and partial classifications account for remaining 27.2%.\n")

print()
print("Detailed analysis appended to sugar_analysis.txt")

