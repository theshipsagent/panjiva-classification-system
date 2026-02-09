"""
Validate Party Harmonization Results - v1.0.0
==============================================
Generate detailed validation reports and coverage statistics.

Author: WSD3 / Claude Code
Date: 2026-02-09 (recreated from documentation)

Generates:
- Match rate by party role
- Tonnage coverage by entity
- Top unmatched party names
- Entity usage frequency
- Match type breakdown

Input:  panjiva_imports_{year}_HARMONIZED_v1.0.0.csv
Output: Multiple validation CSVs and summary report
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import argparse

# Paths
BASE_DIR = Path(r"G:\My Drive\LLM\project_manifest")
INPUT_DIR = BASE_DIR / "00_DATA" / "00.03_MATCHED"
OUTPUT_DIR = BASE_DIR / "03_DOCUMENTATION" / "03.04_summaries"

def analyze_match_rates(df):
    """Analyze match rates by party role"""
    print("\nAnalyzing match rates...")

    party_roles = ['Shipper', 'Consignee', 'Notify Party']
    results = []

    for role in party_roles:
        harmonized_col = f'{role}_Harmonized'
        entity_col = f'{role}_Entity_ID'

        if harmonized_col not in df.columns:
            continue

        # Record counts
        total_records = len(df)
        matched_records = df[harmonized_col].notna().sum()
        blank_records = df[role].isna().sum()

        # Tonnage
        total_tonnage = df['Tons'].sum()
        matched_tonnage = df[df[harmonized_col].notna()]['Tons'].sum()

        # Match types
        match_types = df[df[entity_col].notna()][f'{role}_Match_Type'].value_counts()

        results.append({
            'Party_Role': role,
            'Total_Records': total_records,
            'Matched_Records': matched_records,
            'Match_Rate_Pct': matched_records / total_records * 100,
            'Blank_Records': blank_records,
            'Total_Tonnage': total_tonnage,
            'Matched_Tonnage': matched_tonnage,
            'Tonnage_Coverage_Pct': matched_tonnage / total_tonnage * 100,
            'Exact_Matches': match_types.get('Exact', 0),
            'Contains_Matches': match_types.get('Contains', 0),
            'Fuzzy_Matches': match_types.get('Fuzzy', 0)
        })

    df_results = pd.DataFrame(results)
    print(f"  Analyzed {len(party_roles)} party roles")

    return df_results

def analyze_entity_coverage(df):
    """Analyze tonnage coverage by entity"""
    print("\nAnalyzing entity coverage...")

    party_roles = ['Shipper', 'Consignee', 'Notify Party']
    entity_tonnage = []

    for role in party_roles:
        harmonized_col = f'{role}_Harmonized'
        entity_col = f'{role}_Entity_ID'

        if harmonized_col not in df.columns:
            continue

        # Group by entity
        role_summary = df[df[harmonized_col].notna()].groupby([harmonized_col, entity_col]).agg({
            'REC_ID': 'count',
            'Tons': 'sum'
        }).reset_index()

        role_summary['Party_Role'] = role
        role_summary.columns = ['Entity_Name', 'Entity_ID', 'Records', 'Tonnage', 'Party_Role']

        entity_tonnage.append(role_summary)

    df_entities = pd.concat(entity_tonnage, ignore_index=True)

    # Aggregate across all roles
    entity_summary = df_entities.groupby(['Entity_Name', 'Entity_ID']).agg({
        'Records': 'sum',
        'Tonnage': 'sum'
    }).reset_index().sort_values('Tonnage', ascending=False)

    print(f"  Analyzed {len(entity_summary)} unique entities")

    return entity_summary

def analyze_unmatched_parties(df):
    """Identify top unmatched party names"""
    print("\nAnalyzing unmatched parties...")

    party_roles = ['Shipper', 'Consignee', 'Notify Party']
    unmatched_data = []

    for role in party_roles:
        harmonized_col = f'{role}_Harmonized'

        if role not in df.columns:
            continue

        # Get unmatched parties
        unmatched = df[df[harmonized_col].isna() & df[role].notna()]

        if len(unmatched) == 0:
            continue

        # Group by party name
        unmatched_summary = unmatched.groupby(role).agg({
            'REC_ID': 'count',
            'Tons': 'sum'
        }).reset_index().sort_values('Tons', ascending=False).head(100)

        unmatched_summary['Party_Role'] = role
        unmatched_summary.columns = ['Party_Name', 'Records', 'Tonnage', 'Party_Role']

        unmatched_data.append(unmatched_summary)

    df_unmatched = pd.concat(unmatched_data, ignore_index=True)

    print(f"  Identified {len(df_unmatched)} top unmatched parties")

    return df_unmatched

def generate_comprehensive_report(df, year, match_rates, entity_coverage, unmatched, output_path):
    """Generate comprehensive validation report"""
    print("\nGenerating comprehensive validation report...")

    report = []
    report.append(f"COMPREHENSIVE PARTY HARMONIZATION VALIDATION REPORT")
    report.append(f"{'='*80}")
    report.append(f"Year: {year}")
    report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Total Records: {len(df):,}")
    report.append(f"Total Tonnage: {df['Tons'].sum():,.0f} tons")
    report.append("")

    # SECTION 1: Match Rates by Role
    report.append(f"SECTION 1: MATCH RATES BY PARTY ROLE")
    report.append(f"{'-'*80}")

    for _, row in match_rates.iterrows():
        report.append(f"\n{row['Party_Role']}:")
        report.append(f"  Records: {row['Matched_Records']:,.0f} / {row['Total_Records']:,.0f} ({row['Match_Rate_Pct']:.1f}%)")
        report.append(f"  Tonnage: {row['Matched_Tonnage']:,.0f} / {row['Total_Tonnage']:,.0f} ({row['Tonnage_Coverage_Pct']:.1f}%)")
        report.append(f"  Blank Records: {row['Blank_Records']:,.0f}")
        report.append(f"  Match Types:")
        report.append(f"    Exact: {row['Exact_Matches']:,.0f}")
        report.append(f"    Contains: {row['Contains_Matches']:,.0f}")
        report.append(f"    Fuzzy: {row['Fuzzy_Matches']:,.0f}")

    # SECTION 2: Top Entities by Tonnage
    report.append(f"\n\nSECTION 2: TOP 20 ENTITIES BY TONNAGE")
    report.append(f"{'-'*80}")

    for i, (_, row) in enumerate(entity_coverage.head(20).iterrows(), 1):
        report.append(f"{i:2d}. {row['Entity_Name']:50s}")
        report.append(f"    Records: {row['Records']:8,.0f}  |  Tonnage: {row['Tonnage']:15,.0f} tons")

    # SECTION 3: Coverage Statistics
    total_tonnage = df['Tons'].sum()
    matched_tonnage = entity_coverage['Tonnage'].sum()

    report.append(f"\n\nSECTION 3: OVERALL COVERAGE STATISTICS")
    report.append(f"{'-'*80}")
    report.append(f"Unique Entities Matched: {len(entity_coverage)}")
    report.append(f"Total Tonnage Matched: {matched_tonnage:,.0f} tons")
    report.append(f"Overall Coverage: {matched_tonnage/total_tonnage*100:.1f}%")

    # SECTION 4: Top Unmatched Parties
    report.append(f"\n\nSECTION 4: TOP 20 UNMATCHED PARTIES (By Tonnage)")
    report.append(f"{'-'*80}")

    for i, (_, row) in enumerate(unmatched.head(20).iterrows(), 1):
        report.append(f"{i:2d}. [{row['Party_Role']}] {row['Party_Name']}")
        report.append(f"    Records: {row['Records']:8,.0f}  |  Tonnage: {row['Tonnage']:15,.0f} tons")

    # Write report
    report_text = '\n'.join(report)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)

    print(f"\n  Report saved: {output_path}")

def main(year):
    """Main execution"""
    print(f"\n{'='*80}")
    print(f"PARTY HARMONIZATION VALIDATION v1.0.0")
    print(f"{'='*80}")
    print(f"Year: {year}")

    # File paths
    input_file = INPUT_DIR / f"panjiva_imports_{year}_HARMONIZED_v1.0.0.csv"
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    match_rates_file = OUTPUT_DIR / f"harmonization_match_rates_{timestamp}.csv"
    entity_coverage_file = OUTPUT_DIR / f"entity_coverage_{timestamp}.csv"
    unmatched_file = OUTPUT_DIR / f"unmatched_parties_{timestamp}.csv"
    report_file = OUTPUT_DIR / f"harmonization_comprehensive_report_{timestamp}.txt"

    # Check input exists
    if not input_file.exists():
        print(f"\nERROR: Input file not found: {input_file}")
        print(f"  Run harmonize_party_names_v1.0.0.py first")
        return

    # Load data
    print(f"\nLoading harmonized data: {input_file.name}")
    df = pd.read_csv(input_file, encoding='utf-8-sig', low_memory=False)
    print(f"  Loaded {len(df):,} records")

    # Analyze match rates
    match_rates = analyze_match_rates(df)
    match_rates.to_csv(match_rates_file, index=False, encoding='utf-8-sig')
    print(f"  Saved match rates: {match_rates_file.name}")

    # Analyze entity coverage
    entity_coverage = analyze_entity_coverage(df)
    entity_coverage.to_csv(entity_coverage_file, index=False, encoding='utf-8-sig')
    print(f"  Saved entity coverage: {entity_coverage_file.name}")

    # Analyze unmatched parties
    unmatched = analyze_unmatched_parties(df)
    unmatched.to_csv(unmatched_file, index=False, encoding='utf-8-sig')
    print(f"  Saved unmatched parties: {unmatched_file.name}")

    # Generate comprehensive report
    generate_comprehensive_report(df, year, match_rates, entity_coverage, unmatched, report_file)

    print(f"\n{'='*80}")
    print("VALIDATION COMPLETE")
    print(f"{'='*80}")
    print(f"Match Rates: {match_rates_file.name}")
    print(f"Entity Coverage: {entity_coverage_file.name}")
    print(f"Unmatched Parties: {unmatched_file.name}")
    print(f"Comprehensive Report: {report_file.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Validate party harmonization results')
    parser.add_argument('--year', type=int, required=True, help='Year to process (e.g., 2024)')

    args = parser.parse_args()
    main(args.year)
