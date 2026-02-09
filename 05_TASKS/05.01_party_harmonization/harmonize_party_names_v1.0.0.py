"""
Party Name Harmonization - v1.0.0
==================================
Match raw party names to standardized entities and add harmonized columns.

Author: WSD3 / Claude Code
Date: 2026-02-09 (recreated from documentation)
Original: 2026-02-05

Input:  panjiva_imports_{year}_AUTHORITATIVE_v2.0.0.csv
Output: panjiva_imports_{year}_HARMONIZED_v1.0.0.csv

Adds 9 columns:
- Shipper_Harmonized, Shipper_Entity_ID, Shipper_Match_Type
- Consignee_Harmonized, Consignee_Entity_ID, Consignee_Match_Type
- Notify Party_Harmonized, Notify Party_Entity_ID, Notify Party_Match_Type
"""

import pandas as pd
import re
from pathlib import Path
from datetime import datetime
import argparse

# Paths
BASE_DIR = Path(r"G:\My Drive\LLM\project_manifest")
DICT_PATH = BASE_DIR / "01_DICTIONARIES" / "01.06_parties" / "party_harmonization_master_v1.3.0.csv"
INPUT_DIR = BASE_DIR / "00_DATA" / "00.02_PREPROCESSED"
OUTPUT_DIR = BASE_DIR / "00_DATA" / "00.03_MATCHED"
REPORT_DIR = OUTPUT_DIR

def load_dictionary():
    """Load party harmonization dictionary"""
    print("Loading party harmonization dictionary...")
    df_dict = pd.read_csv(DICT_PATH, encoding='utf-8-sig')
    print(f"  Loaded {len(df_dict)} entities")

    # Validate required columns
    required = ['Entity_ID', 'Canonical_Name', 'Match_Keywords', 'Match_Strategy']
    missing = [c for c in required if c not in df_dict.columns]
    if missing:
        raise ValueError(f"Dictionary missing required columns: {missing}")

    return df_dict

def normalize_name(name):
    """Normalize party name for matching"""
    if pd.isna(name):
        return ""

    name = str(name).upper().strip()

    # Remove common suffixes/prefixes
    name = re.sub(r'\b(INC|LLC|LTD|CORP|CO|SA|SL|GMBH|AG|NV|BV)\b', '', name)
    name = re.sub(r'\b(CORPORATION|COMPANY|LIMITED|INCORPORATED)\b', '', name)

    # Remove punctuation except spaces
    name = re.sub(r'[^\w\s]', ' ', name)

    # Collapse multiple spaces
    name = re.sub(r'\s+', ' ', name).strip()

    return name

def match_entity(party_name, df_dict):
    """
    Match party name against dictionary entities.

    Returns:
        tuple: (canonical_name, entity_id, match_type) or (None, None, None)
    """
    if pd.isna(party_name) or party_name == "":
        return None, None, None

    normalized = normalize_name(party_name)

    # Try exact matches first (highest confidence)
    for _, entity in df_dict[df_dict['Match_Strategy'] == 'EXACT'].iterrows():
        keywords = str(entity['Match_Keywords']).split('|')
        for keyword in keywords:
            keyword_norm = normalize_name(keyword)
            if normalized == keyword_norm:
                return entity['Canonical_Name'], entity['Entity_ID'], 'Exact'

    # Try contains matches (medium confidence)
    for _, entity in df_dict[df_dict['Match_Strategy'] == 'CONTAINS'].iterrows():
        keywords = str(entity['Match_Keywords']).split('|')
        for keyword in keywords:
            keyword_norm = normalize_name(keyword)
            if keyword_norm in normalized or normalized in keyword_norm:
                return entity['Canonical_Name'], entity['Entity_ID'], 'Contains'

    # Try fuzzy matches (lower confidence) - simple word overlap
    for _, entity in df_dict[df_dict['Match_Strategy'] == 'FUZZY'].iterrows():
        keywords = str(entity['Match_Keywords']).split('|')
        for keyword in keywords:
            keyword_norm = normalize_name(keyword)
            keyword_words = set(keyword_norm.split())
            party_words = set(normalized.split())

            # If >75% words match, consider it a fuzzy match
            if len(keyword_words) > 0:
                overlap = len(keyword_words & party_words) / len(keyword_words)
                if overlap > 0.75:
                    return entity['Canonical_Name'], entity['Entity_ID'], 'Fuzzy'

    return None, None, None

def harmonize_parties(df, df_dict):
    """
    Add harmonized party columns to dataframe.

    Args:
        df: Input dataframe with raw party names
        df_dict: Party harmonization dictionary

    Returns:
        DataFrame with 9 new harmonized columns
    """
    print("\nHarmonizing party names...")

    # Party roles to harmonize
    party_roles = [
        ('Shipper', 'Shipper'),
        ('Consignee', 'Consignee'),
        ('Notify Party', 'Notify Party')
    ]

    total_records = len(df)

    for col_name, display_name in party_roles:
        print(f"\n  Processing {display_name}...")

        if col_name not in df.columns:
            print(f"    WARNING: Column '{col_name}' not found, skipping")
            df[f'{col_name}_Harmonized'] = None
            df[f'{col_name}_Entity_ID'] = None
            df[f'{col_name}_Match_Type'] = None
            continue

        # Initialize new columns
        df[f'{col_name}_Harmonized'] = None
        df[f'{col_name}_Entity_ID'] = None
        df[f'{col_name}_Match_Type'] = None

        # Match each party name
        matched_count = 0
        for idx, row in df.iterrows():
            party_name = row[col_name]
            canonical, entity_id, match_type = match_entity(party_name, df_dict)

            if canonical is not None:
                df.at[idx, f'{col_name}_Harmonized'] = canonical
                df.at[idx, f'{col_name}_Entity_ID'] = entity_id
                df.at[idx, f'{col_name}_Match_Type'] = match_type
                matched_count += 1

            # Progress indicator
            if (idx + 1) % 50000 == 0:
                print(f"    Processed {idx + 1:,} / {total_records:,} records...")

        match_rate = (matched_count / total_records) * 100
        print(f"    Matched: {matched_count:,} / {total_records:,} ({match_rate:.1f}%)")

    return df

def generate_validation_report(df, year, output_path):
    """Generate validation report with coverage statistics"""
    print("\nGenerating validation report...")

    report = []
    report.append(f"PARTY HARMONIZATION VALIDATION REPORT")
    report.append(f"{'='*80}")
    report.append(f"Year: {year}")
    report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Total Records: {len(df):,}")
    report.append(f"Total Tonnage: {df['Tons'].sum():,.0f} tons")
    report.append("")

    # Party roles
    party_roles = ['Shipper', 'Consignee', 'Notify Party']

    report.append(f"MATCH RATES BY PARTY ROLE")
    report.append(f"{'-'*80}")

    for role in party_roles:
        harmonized_col = f'{role}_Harmonized'
        entity_col = f'{role}_Entity_ID'

        if harmonized_col not in df.columns:
            continue

        # Record match rate
        matched_records = df[harmonized_col].notna().sum()
        match_rate = (matched_records / len(df)) * 100

        # Tonnage match rate
        matched_tonnage = df[df[harmonized_col].notna()]['Tons'].sum()
        tonnage_rate = (matched_tonnage / df['Tons'].sum()) * 100

        report.append(f"\n{role}:")
        report.append(f"  Records Matched: {matched_records:,} / {len(df):,} ({match_rate:.1f}%)")
        report.append(f"  Tonnage Matched: {matched_tonnage:,.0f} / {df['Tons'].sum():,.0f} ({tonnage_rate:.1f}%)")

        # Match type breakdown
        if df[entity_col].notna().any():
            match_types = df[df[entity_col].notna()][f'{role}_Match_Type'].value_counts()
            report.append(f"  Match Types:")
            for match_type, count in match_types.items():
                report.append(f"    {match_type}: {count:,} ({count/matched_records*100:.1f}%)")

    # Top entities by tonnage
    report.append(f"\n\nTOP 20 ENTITIES BY TONNAGE")
    report.append(f"{'-'*80}")

    # Combine all entity columns
    entity_tonnage = {}
    for role in party_roles:
        harmonized_col = f'{role}_Harmonized'
        if harmonized_col not in df.columns:
            continue

        role_tonnage = df[df[harmonized_col].notna()].groupby(harmonized_col)['Tons'].sum()
        for entity, tons in role_tonnage.items():
            entity_tonnage[entity] = entity_tonnage.get(entity, 0) + tons

    top_entities = sorted(entity_tonnage.items(), key=lambda x: x[1], reverse=True)[:20]
    for i, (entity, tons) in enumerate(top_entities, 1):
        report.append(f"{i:2d}. {entity:50s} {tons:15,.0f} tons")

    # Write report
    report_text = '\n'.join(report)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)

    print(f"\n  Report saved: {output_path}")

    # Also print summary to console
    print("\n" + "="*80)
    print("HARMONIZATION SUMMARY")
    print("="*80)
    for line in report[6:20]:  # Print match rates section
        print(line)

def main(year):
    """Main execution"""
    print(f"\n{'='*80}")
    print(f"PARTY NAME HARMONIZATION v1.0.0")
    print(f"{'='*80}")
    print(f"Year: {year}")

    # File paths
    input_file = INPUT_DIR / f"panjiva_imports_{year}_AUTHORITATIVE_v2.0.0.csv"
    output_file = OUTPUT_DIR / f"panjiva_imports_{year}_HARMONIZED_v1.0.0.csv"
    report_file = REPORT_DIR / f"harmonization_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    # Check input exists
    if not input_file.exists():
        print(f"\nERROR: Input file not found: {input_file}")
        return

    # Load data
    print(f"\nLoading data: {input_file.name}")
    df = pd.read_csv(input_file, encoding='utf-8-sig', low_memory=False)
    print(f"  Loaded {len(df):,} records, {len(df.columns)} columns")

    # Load dictionary
    df_dict = load_dictionary()

    # Harmonize parties
    df = harmonize_parties(df, df_dict)

    # Save output
    print(f"\nSaving harmonized data...")
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"  Saved: {output_file}")
    print(f"  Records: {len(df):,}")
    print(f"  Columns: {len(df.columns)} (added 9 harmonization columns)")

    # Generate validation report
    generate_validation_report(df, year, report_file)

    print(f"\n{'='*80}")
    print("HARMONIZATION COMPLETE")
    print(f"{'='*80}")
    print(f"Output: {output_file.name}")
    print(f"Report: {report_file.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Harmonize party names to standardized entities')
    parser.add_argument('--year', type=int, required=True, help='Year to process (e.g., 2024)')

    args = parser.parse_args()
    main(args.year)
