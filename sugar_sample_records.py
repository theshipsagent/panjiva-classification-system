import pandas as pd

# File paths
classified_file = r"G:\My Drive\LLM\project_manifest\panjiva_production_v1\03_output\classified\panjiva_2024_classified_v4.0.0_OPTIMIZED.csv"
output_file = r"G:\My Drive\LLM\project_manifest\panjiva_production_v1\sugar_sample_records.txt"

# Load data
df = pd.read_csv(classified_file, low_memory=False)

# Find sugar/cane records
mask1 = df['HS2'].astype(str).str.strip() == '17'
mask2 = df['Goods Shipped'].fillna('').str.contains('SUGAR|CANE', case=False, na=False)
mask3 = df['HS Code Desc.'].fillna('').str.contains('SUGAR|CANE', case=False, na=False)
sugar_records = df[mask1 | mask2 | mask3].copy()

# Categorize
correct = sugar_records[sugar_records['Commodity'] == 'Sugar']
partial = sugar_records[(sugar_records['Group'] != 'TBN') & (sugar_records['Commodity'] == 'TBN')]
misclassified = sugar_records[sugar_records['Last_Rule_ID'].isin(['CARRIER-DRYBULK', 'CARRIER-RORO'])]
excluded = sugar_records[sugar_records['Group'] == 'EXCLUDED']

with open(output_file, 'w') as f:
    f.write("=" * 100 + "\n")
    f.write("SUGAR RECORD SAMPLES - 2024 DATA\n")
    f.write("=" * 100 + "\n\n")

    # Correctly classified
    f.write("\n[1] CORRECTLY CLASSIFIED (Commodity=Sugar) - Sample of 10 records\n")
    f.write("-" * 100 + "\n\n")
    if len(correct) > 0:
        cols = ['Bill of Lading Number', 'HS Code Desc.', 'Goods Shipped', 'Tons', 'HS4', 'Group', 'Commodity', 'Cargo', 'Last_Rule_ID']
        sample = correct[cols].head(10)
        for idx, (i, row) in enumerate(sample.iterrows(), 1):
            f.write(f"\nRecord {idx}:\n")
            f.write(f"  Bill of Lading: {row['Bill of Lading Number']}\n")
            f.write(f"  HS Code Desc: {row['HS Code Desc.']}\n")
            f.write(f"  Goods Shipped: {row['Goods Shipped']}\n")
            f.write(f"  Tonnage: {row['Tons']:,.0f} MT\n")
            f.write(f"  HS4: {row['HS4']}\n")
            f.write(f"  Classification: {row['Group']} > {row['Commodity']} > {row['Cargo']}\n")
            f.write(f"  Rule Applied: {row['Last_Rule_ID']}\n")

    # Partially classified
    f.write("\n\n[2] PARTIALLY CLASSIFIED (Group!=TBN, Commodity=TBN) - Sample of 10 records\n")
    f.write("-" * 100 + "\n\n")
    if len(partial) > 0:
        cols = ['Bill of Lading Number', 'HS Code Desc.', 'Goods Shipped', 'Tons', 'HS4', 'Group', 'Commodity', 'Cargo', 'Last_Rule_ID']
        sample = partial[cols].head(10)
        for idx, (i, row) in enumerate(sample.iterrows(), 1):
            f.write(f"\nRecord {idx}:\n")
            f.write(f"  Bill of Lading: {row['Bill of Lading Number']}\n")
            f.write(f"  HS Code Desc: {row['HS Code Desc.']}\n")
            f.write(f"  Goods Shipped: {row['Goods Shipped']}\n")
            f.write(f"  Tonnage: {row['Tons']:,.0f} MT\n")
            f.write(f"  HS4: {row['HS4']}\n")
            f.write(f"  Classification: {row['Group']} > {row['Commodity']} > {row['Cargo']}\n")
            f.write(f"  Rule Applied: {row['Last_Rule_ID']}\n")
            f.write(f"  NOTE: Group set by {row['Last_Rule_ID']}, but Commodity not classified\n")

    # Misclassified
    f.write("\n\n[3] MISCLASSIFIED (Non-Sugar Rules) - Sample of 10 records\n")
    f.write("-" * 100 + "\n\n")
    if len(misclassified) > 0:
        cols = ['Bill of Lading Number', 'HS Code Desc.', 'Goods Shipped', 'Tons', 'HS4', 'Group', 'Commodity', 'Cargo', 'Last_Rule_ID']
        sample = misclassified[cols].head(10)
        for idx, (i, row) in enumerate(sample.iterrows(), 1):
            f.write(f"\nRecord {idx}:\n")
            f.write(f"  Bill of Lading: {row['Bill of Lading Number']}\n")
            f.write(f"  HS Code Desc: {row['HS Code Desc.']}\n")
            f.write(f"  Goods Shipped: {row['Goods Shipped']}\n")
            f.write(f"  Tonnage: {row['Tons']:,.0f} MT\n")
            f.write(f"  HS4: {row['HS4']}\n")
            f.write(f"  Classification: {row['Group']} > {row['Commodity']} > {row['Cargo']}\n")
            f.write(f"  Rule Applied: {row['Last_Rule_ID']}\n")
            f.write(f"  NOTE: Misclassified by vessel-type rule (should be Sugar)\n")

    # Excluded
    f.write("\n\n[4] EXCLUDED (Noise Filters) - Sample of 10 records\n")
    f.write("-" * 100 + "\n\n")
    if len(excluded) > 0:
        cols = ['Bill of Lading Number', 'HS Code Desc.', 'Goods Shipped', 'Tons', 'HS4', 'Group', 'Last_Rule_ID']
        sample = excluded[cols].head(10)
        for idx, (i, row) in enumerate(sample.iterrows(), 1):
            f.write(f"\nRecord {idx}:\n")
            f.write(f"  Bill of Lading: {row['Bill of Lading Number']}\n")
            f.write(f"  HS Code Desc: {row['HS Code Desc.']}\n")
            f.write(f"  Goods Shipped: {row['Goods Shipped']}\n")
            f.write(f"  Tonnage: {row['Tons']:,.0f} MT\n")
            f.write(f"  HS4: {row['HS4']}\n")
            f.write(f"  Status: {row['Group']}\n")
            f.write(f"  Rule Applied: {row['Last_Rule_ID']}\n")
            f.write(f"  NOTE: Very small shipment, excluded by noise filter (typical for testing/samples)\n")

    f.write("\n\n" + "=" * 100 + "\n")
    f.write("END OF SAMPLE RECORDS\n")
    f.write("=" * 100 + "\n")

print(f"Sample records written to: {output_file}")

