#!/usr/bin/env python3
"""
Steel Fragmentation Analysis for 2024 Data
Analyzes classification outcomes for all steel-related records
"""

import pandas as pd
import sys
from pathlib import Path

# File paths
DATA_FILE = r"G:\My Drive\LLM\project_manifest\panjiva_production_v1\03_output\classified\panjiva_2024_classified_v4.0.0_OPTIMIZED.csv"
DICT_FILE = r"G:\My Drive\LLM\project_manifest\panjiva_production_v1\01_dictionary\cargo_classification_dictionary_v4.0.0_SIMPLE.csv"
OUTPUT_FILE = r"G:\My Drive\LLM\project_manifest\panjiva_production_v1\steel_analysis.txt"

# Steel keywords
STEEL_KEYWORDS = ["STEEL", "HOT ROLLED", "COLD ROLLED", "COIL", "SLAB", "PLATE", "CONTINUOUS CASTING", "REBAR", "WIRE ROD"]

def main():
    print("=" * 100)
    print("STEEL FRAGMENTATION ANALYSIS - 2024 DATA")
    print("=" * 100)

    # Load data
    print("\nLoading classified data...")
    df = pd.read_csv(DATA_FILE, dtype={'HS2': str, 'HS4': str, 'HS6': str})
    print(f"Total records: {len(df):,}")

    # Load dictionary
    print("Loading classification dictionary...")
    dict_df = pd.read_csv(DICT_FILE)
    print(f"Total rules: {len(dict_df)}")

    # Find steel records
    print("\nSearching for steel keywords...")
    steel_mask = df['Goods Shipped'].fillna('').str.upper().str.contains('|'.join(STEEL_KEYWORDS), regex=True, na=False)
    steel_df = df[steel_mask].copy()

    total_steel_tonnage = steel_df['Tons'].sum()

    print(f"Steel keyword records found: {len(steel_df):,}")
    print(f"Total tonnage: {total_steel_tonnage:,.0f} tons")

    # Initialize output
    output_lines = []
    output_lines.append("=" * 100)
    output_lines.append("STEEL FRAGMENTATION ANALYSIS - 2024 DATA")
    output_lines.append("=" * 100)
    output_lines.append(f"\nAnalysis Date: {pd.Timestamp.now()}")
    output_lines.append(f"Data File: {DATA_FILE}")
    output_lines.append(f"Dictionary: {DICT_FILE}")
    output_lines.append(f"\nTotal records in dataset: {len(df):,}")
    output_lines.append(f"Steel keyword records: {len(steel_df):,}")
    output_lines.append(f"Total steel tonnage: {total_steel_tonnage:,.0f} tons")
    output_lines.append(f"Percentage of total: {(total_steel_tonnage / df['Tons'].sum() * 100):.1f}%")

    # 1. Classification Breakdown by Outcome
    output_lines.append("\n" + "=" * 100)
    output_lines.append("1. CLASSIFICATION BREAKDOWN BY OUTCOME")
    output_lines.append("=" * 100)

    class_breakdown = steel_df.groupby(['Group', 'Commodity', 'Cargo']).agg({
        'Tons': 'sum',
        'Bill of Lading Number': 'count'
    }).reset_index()
    class_breakdown.columns = ['Group', 'Commodity', 'Cargo', 'Tonnage', 'Count']
    class_breakdown = class_breakdown.sort_values('Tonnage', ascending=False)

    output_lines.append("\nClassification Summary (sorted by tonnage):")
    output_lines.append(f"{'Group':<20} {'Commodity':<25} {'Cargo':<25} {'Tonnage':>15} {'Count':>10}")
    output_lines.append("-" * 100)

    for _, row in class_breakdown.iterrows():
        output_lines.append(f"{row['Group']:<20} {str(row['Commodity']):<25} {str(row['Cargo']):<25} {row['Tonnage']:>15,.0f} {row['Count']:>10,.0f}")

    # 2. EXCLUDED Records Analysis
    output_lines.append("\n" + "=" * 100)
    output_lines.append("2. EXCLUDED STEEL RECORDS - DETAILED ANALYSIS")
    output_lines.append("=" * 100)

    excluded_steel = steel_df[steel_df['Group'] == 'EXCLUDED'].copy()
    excluded_tonnage = excluded_steel['Tons'].sum()

    output_lines.append(f"\nTotal excluded records: {len(excluded_steel):,}")
    output_lines.append(f"Excluded tonnage: {excluded_tonnage:,.0f} tons")
    output_lines.append(f"Percentage of steel: {(excluded_tonnage / total_steel_tonnage * 100):.1f}%")

    if len(excluded_steel) > 0:
        output_lines.append("\nBreakdown by Filter/Rule:")
        filter_breakdown = excluded_steel.groupby('Filter').agg({
            'Tons': 'sum',
            'Bill of Lading Number': 'count',
            'Last_Rule_ID': 'first'
        }).reset_index()
        filter_breakdown.columns = ['Filter', 'Tonnage', 'Count', 'Last_Rule_ID']
        filter_breakdown = filter_breakdown.sort_values('Tonnage', ascending=False)

        output_lines.append(f"{'Filter':<30} {'Tonnage':>15} {'Count':>10} {'Sample Rule':>30}")
        output_lines.append("-" * 90)
        for _, row in filter_breakdown.iterrows():
            output_lines.append(f"{str(row['Filter']):<30} {row['Tonnage']:>15,.0f} {row['Count']:>10,.0f} {str(row['Last_Rule_ID']):<30}")

        # Top 10 excluded records by tonnage
        output_lines.append("\nTop 10 Excluded Records by Tonnage:")
        output_lines.append(f"{'Goods Shipped':<50} {'Tons':>12} {'Filter':<25} {'Rule ID':<20}")
        output_lines.append("-" * 110)

        top_excluded = excluded_steel.nlargest(10, 'Tons')[['Goods Shipped', 'Tons', 'Filter', 'Last_Rule_ID']]
        for _, row in top_excluded.iterrows():
            goods = str(row['Goods Shipped'])[:50] if pd.notna(row['Goods Shipped']) else 'N/A'
            output_lines.append(f"{goods:<50} {row['Tons']:>12,.0f} {str(row['Filter']):<25} {str(row['Last_Rule_ID']):<20}")

    # 3. SLAB CONTINUOUS CASTING Analysis
    output_lines.append("\n" + "=" * 100)
    output_lines.append("3. SLAB CONTINUOUS CASTING ANALYSIS")
    output_lines.append("=" * 100)

    slab_cc_mask = steel_df['Goods Shipped'].fillna('').str.upper().str.contains(r'SLAB|CONTINUOUS\s+CASTING', regex=True, na=False)
    slab_cc_records = steel_df[slab_cc_mask].copy()

    output_lines.append(f"\nRecords with 'SLAB' or 'CONTINUOUS CASTING': {len(slab_cc_records):,}")
    output_lines.append(f"Tonnage: {slab_cc_records['Tons'].sum():,.0f} tons")

    if len(slab_cc_records) > 0:
        output_lines.append("\nClassifications for SLAB/CONTINUOUS CASTING:")
        slab_class = slab_cc_records.groupby(['Group', 'Commodity', 'Cargo']).agg({
            'Tons': 'sum',
            'Bill of Lading Number': 'count'
        }).reset_index().sort_values('Tons', ascending=False)

        output_lines.append(f"{'Group':<20} {'Commodity':<25} {'Cargo':<25} {'Tonnage':>15} {'Count':>10}")
        output_lines.append("-" * 100)
        for _, row in slab_class.iterrows():
            output_lines.append(f"{row['Group']:<20} {str(row['Commodity']):<25} {str(row['Cargo']):<25} {row['Tons']:>15,.0f} {row['Count']:>10,.0f}")

        # Check for excluded SLAB records
        excluded_slab = slab_cc_records[slab_cc_records['Group'] == 'EXCLUDED']
        if len(excluded_slab) > 0:
            output_lines.append(f"\nEXCLUDED SLAB/CONTINUOUS CASTING Records: {len(excluded_slab):,}")
            output_lines.append(f"Tonnage: {excluded_slab['Tons'].sum():,.0f} tons")
            output_lines.append("\nTop 5 excluded SLAB records:")
            output_lines.append(f"{'Goods Shipped':<60} {'Tons':>12} {'Filter':<20}")
            output_lines.append("-" * 95)
            for _, row in excluded_slab.nlargest(5, 'Tons').iterrows():
                goods = str(row['Goods Shipped'])[:60] if pd.notna(row['Goods Shipped']) else 'N/A'
                output_lines.append(f"{goods:<60} {row['Tons']:>12,.0f} {str(row['Filter']):<20}")

    # 4. Package Type Analysis
    output_lines.append("\n" + "=" * 100)
    output_lines.append("4. PACKAGE TYPE ANALYSIS")
    output_lines.append("=" * 100)

    output_lines.append("\nPackage types for ALL steel records:")
    pkg_summary = steel_df.groupby('Package_Type').agg({
        'Tons': 'sum',
        'Bill of Lading Number': 'count'
    }).reset_index().sort_values('Tons', ascending=False)

    output_lines.append(f"{'Package Type':<20} {'Tonnage':>15} {'Count':>10}")
    output_lines.append("-" * 50)
    for _, row in pkg_summary.iterrows():
        pkg = str(row['Package_Type']) if pd.notna(row['Package_Type']) else 'NULL/UNKNOWN'
        output_lines.append(f"{pkg:<20} {row['Tons']:>15,.0f} {row['Count']:>10,.0f}")

    output_lines.append("\nPackage types for EXCLUDED steel records:")
    if len(excluded_steel) > 0:
        excluded_pkg = excluded_steel.groupby('Package_Type').agg({
            'Tons': 'sum',
            'Bill of Lading Number': 'count'
        }).reset_index().sort_values('Tons', ascending=False)

        output_lines.append(f"{'Package Type':<20} {'Tonnage':>15} {'Count':>10}")
        output_lines.append("-" * 50)
        for _, row in excluded_pkg.iterrows():
            pkg = str(row['Package_Type']) if pd.notna(row['Package_Type']) else 'NULL/UNKNOWN'
            output_lines.append(f"{pkg:<20} {row['Tons']:>15,.0f} {row['Count']:>10,.0f}")

    # 5. HS Code Analysis
    output_lines.append("\n" + "=" * 100)
    output_lines.append("5. HS CODE ANALYSIS")
    output_lines.append("=" * 100)

    output_lines.append("\nHS2 codes for ALL steel records:")
    hs2_summary = steel_df.groupby('HS2').agg({
        'Tons': 'sum',
        'Bill of Lading Number': 'count'
    }).reset_index().sort_values('Tons', ascending=False)

    output_lines.append(f"{'HS2':<10} {'Tonnage':>15} {'Count':>10}")
    output_lines.append("-" * 40)
    for _, row in hs2_summary.iterrows():
        hs2 = str(row['HS2']) if pd.notna(row['HS2']) else 'NULL'
        output_lines.append(f"{hs2:<10} {row['Tons']:>15,.0f} {row['Count']:>10,.0f}")

    output_lines.append("\nHS2 codes for EXCLUDED steel records:")
    if len(excluded_steel) > 0:
        excluded_hs2 = excluded_steel.groupby('HS2').agg({
            'Tons': 'sum',
            'Bill of Lading Number': 'count'
        }).reset_index().sort_values('Tons', ascending=False)

        output_lines.append(f"{'HS2':<10} {'Tonnage':>15} {'Count':>10}")
        output_lines.append("-" * 40)
        for _, row in excluded_hs2.iterrows():
            hs2 = str(row['HS2']) if pd.notna(row['HS2']) else 'NULL'
            output_lines.append(f"{hs2:<10} {row['Tons']:>15,.0f} {row['Count']:>10,.0f}")

    # 6. Steel Rules in Dictionary
    output_lines.append("\n" + "=" * 100)
    output_lines.append("6. STEEL RULES IN DICTIONARY")
    output_lines.append("=" * 100)

    steel_rules = dict_df[dict_df['Rule_ID'].str.contains('STEEL', case=False, na=False)]
    output_lines.append(f"\nTotal steel-specific rules: {len(steel_rules)}")

    if len(steel_rules) > 0:
        output_lines.append("\nSteel Rules Details:")
        output_lines.append(f"{'Rule_ID':<25} {'Phase':<8} {'Keywords':<50} {'Group':<15} {'Cargo':<25}")
        output_lines.append("-" * 130)

        for _, row in steel_rules.iterrows():
            keywords = str(row['Keywords'])[:50] if pd.notna(row['Keywords']) else ''
            output_lines.append(f"{row['Rule_ID']:<25} {int(row['Phase']):<8} {keywords:<50} {str(row['Group']):<15} {str(row['Cargo']):<25}")

    # 7. Root Cause Analysis
    output_lines.append("\n" + "=" * 100)
    output_lines.append("7. ROOT CAUSE ANALYSIS")
    output_lines.append("=" * 100)

    output_lines.append("\nKEY FINDINGS:")
    output_lines.append("-" * 100)

    output_lines.append(f"\n1. EXCLUDED RECORDS:")
    output_lines.append(f"   - {len(excluded_steel):,} steel records ({excluded_tonnage:,.0f} tons) are EXCLUDED")
    output_lines.append(f"   - This represents {(excluded_tonnage / total_steel_tonnage * 100):.1f}% of all steel-keyword records")

    if len(excluded_steel) > 0:
        top_filter = excluded_steel['Filter'].value_counts().index[0]
        top_filter_tonnage = excluded_steel[excluded_steel['Filter'] == top_filter]['Tons'].sum()
        output_lines.append(f"   - PRIMARY FILTER: '{top_filter}' accounts for {top_filter_tonnage:,.0f} tons")

    output_lines.append(f"\n2. PACKAGE TYPE CONFLICTS:")
    output_lines.append(f"   - Most common package type for excluded: {excluded_steel['Package_Type'].mode()[0] if len(excluded_steel) > 0 and len(excluded_steel['Package_Type'].mode()) > 0 else 'N/A'}")

    output_lines.append(f"\n3. HS CODE ISSUES:")
    output_lines.append(f"   - Excluded records with HS2=72: {len(excluded_steel[excluded_steel['HS2'] == '72']):,} records")
    output_lines.append(f"   - Excluded records with NULL HS2: {len(excluded_steel[excluded_steel['HS2'].isna()]):,} records")

    output_lines.append(f"\n4. SUCCESSFULLY CLASSIFIED STEEL:")
    classified_steel = steel_df[steel_df['Group'] != 'EXCLUDED'].copy()
    output_lines.append(f"   - {len(classified_steel):,} records classified successfully")
    output_lines.append(f"   - {classified_steel['Tons'].sum():,.0f} tons successfully classified")
    output_lines.append(f"   - Success rate: {(len(classified_steel) / len(steel_df) * 100):.1f}% of steel records")

    if len(classified_steel) > 0:
        output_lines.append(f"\n   Top 5 successful classifications:")
        top_classified = classified_steel.groupby('Cargo').agg({'Tons': 'sum'}).reset_index().nlargest(5, 'Tons')
        for _, row in top_classified.iterrows():
            output_lines.append(f"      - {row['Cargo']}: {row['Tons']:,.0f} tons")

    # Write output
    print("\nWriting analysis to file...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"\nAnalysis complete! Output saved to:")
    print(f"{OUTPUT_FILE}")
    print(f"\nTotal lines: {len(output_lines)}")

if __name__ == '__main__':
    main()
