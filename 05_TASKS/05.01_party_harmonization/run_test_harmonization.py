"""
Test Party Harmonization on Q1 Sample
======================================
Run party harmonization on the 3-month test sample (safe test).

Author: WSD3 / Claude Code
Date: 2026-02-09

Input:  panjiva_imports_2024_JAN_TEST_SAMPLE.csv (74K records)
Output: panjiva_imports_2024_JAN_TEST_HARMONIZED.csv
"""

import pandas as pd
import re
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(r"G:\My Drive\LLM\project_manifest")
TASK_DIR = BASE_DIR / "05_TASKS" / "05.01_party_harmonization"
DICT_PATH = BASE_DIR / "01_DICTIONARIES" / "01.06_parties" / "party_harmonization_master_v1.3.0.csv"

# Test files
TEST_INPUT = TASK_DIR / "panjiva_imports_2024_JAN_TEST_SAMPLE.csv"
TEST_OUTPUT = TASK_DIR / "panjiva_imports_2024_JAN_TEST_HARMONIZED.csv"
TEST_REPORT = TASK_DIR / "test_harmonization_report.txt"

def load_dictionary():
    """Load party harmonization dictionary"""
    print("Loading party harmonization dictionary...")
    df_dict = pd.read_csv(DICT_PATH, encoding='utf-8-sig')
    print(f"  Loaded {len(df_dict)} entities")
    return df_dict

def normalize_name(name):
    """Normalize party name for matching"""
    if pd.isna(name):
        return ""

    name = str(name).upper().strip()

    # FIX PREPROCESSING CORRUPTIONS
    # These exist in the source data due to preprocessing bugs
    name = re.sub(r'COMPANYMPANY', 'COMPANY', name)
    name = re.sub(r'COMPANYRPORATION(ORPORATION)?', 'CORPORATION', name)
    name = re.sub(r'COMPANYNSORP?ORATED', 'INCORPORATED', name)
    name = re.sub(r'COMPANYNSTRUC[AO]+', 'CONSTRUCAO', name)
    name = re.sub(r'LIMITEDTD', 'LIMITED', name)

    # Remove common suffixes/prefixes
    name = re.sub(r'\b(INC|LLC|LTD|CORP|CO|SA|SL|GMBH|AG|NV|BV)\b', '', name)
    name = re.sub(r'\b(CORPORATION|COMPANY|LIMITED|INCORPORATED)\b', '', name)

    # Remove punctuation except spaces
    name = re.sub(r'[^\w\s]', ' ', name)

    # Collapse multiple spaces
    name = re.sub(r'\s+', ' ', name).strip()

    return name

def match_entity(party_name, df_dict, party_role=None):
    """
    Match party name against dictionary entities.

    Args:
        party_name: Raw party name from data
        df_dict: Entity dictionary
        party_role: 'Shipper', 'Consignee', or 'Notify Party' (optional filter)

    Returns:
        tuple: (canonical_name, entity_id, match_type) or (None, None, None)
    """
    if pd.isna(party_name) or party_name == "":
        return None, None, None

    normalized = normalize_name(party_name)

    # Filter dictionary by category if specified
    if party_role:
        # Check entities that apply to this role or 'All'
        role_dict = df_dict[
            (df_dict['Category'] == 'All') |
            (df_dict['Category'] == party_role)
        ]
    else:
        role_dict = df_dict

    # Try exact matches first
    for _, entity in role_dict[role_dict['Match_Strategy'] == 'EXACT'].iterrows():
        keywords = str(entity['Match_Keywords']).split('|')
        for keyword in keywords:
            keyword_norm = normalize_name(keyword)
            if normalized == keyword_norm:
                return entity['Canonical_Name'], entity['Entity_ID'], 'Exact'

    # Try Contains matches (keyword appears in party name)
    for _, entity in role_dict[role_dict['Match_Strategy'] == 'Contains'].iterrows():
        keywords = str(entity['Match_Keywords']).split('|')
        for keyword in keywords:
            keyword_norm = normalize_name(keyword)
            if keyword_norm and keyword_norm in normalized:
                return entity['Canonical_Name'], entity['Entity_ID'], 'Contains'

    # Try Contains_All matches (all keywords must appear)
    for _, entity in role_dict[role_dict['Match_Strategy'] == 'Contains_All'].iterrows():
        keywords = str(entity['Match_Keywords']).split('|')
        for keyword_set in keywords:
            # Split on semicolons for multiple required keywords
            required_keywords = [k.strip() for k in keyword_set.split(';')]
            all_keywords_norm = [normalize_name(k) for k in required_keywords]

            # Check if all required keywords are in the party name
            if all(kw in normalized for kw in all_keywords_norm if kw):
                return entity['Canonical_Name'], entity['Entity_ID'], 'Contains_All'

    # Try fuzzy matches
    for _, entity in role_dict[role_dict['Match_Strategy'] == 'FUZZY'].iterrows():
        keywords = str(entity['Match_Keywords']).split('|')
        for keyword in keywords:
            keyword_norm = normalize_name(keyword)
            keyword_words = set(keyword_norm.split())
            party_words = set(normalized.split())

            if len(keyword_words) > 0:
                overlap = len(keyword_words & party_words) / len(keyword_words)
                if overlap > 0.75:
                    return entity['Canonical_Name'], entity['Entity_ID'], 'Fuzzy'

    return None, None, None

def harmonize_parties(df, df_dict):
    """Add harmonized party columns"""
    print("\nHarmonizing party names...")

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
            canonical, entity_id, match_type = match_entity(party_name, df_dict, party_role=col_name)

            if canonical is not None:
                df.at[idx, f'{col_name}_Harmonized'] = canonical
                df.at[idx, f'{col_name}_Entity_ID'] = entity_id
                df.at[idx, f'{col_name}_Match_Type'] = match_type
                matched_count += 1

            # Progress indicator
            if (idx + 1) % 10000 == 0:
                print(f"    Processed {idx + 1:,} / {total_records:,} records...")

        match_rate = (matched_count / total_records) * 100
        print(f"    Matched: {matched_count:,} / {total_records:,} ({match_rate:.1f}%)")

    return df

def generate_test_report(df, output_path):
    """Generate test validation report"""
    print("\nGenerating test report...")

    report = []
    report.append(f"PARTY HARMONIZATION TEST REPORT")
    report.append(f"{'='*80}")
    report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Test Sample: January 2024 (1 month)")
    report.append(f"Total Records: {len(df):,}")
    report.append(f"Total Tonnage: {df['Tons'].sum():,.0f} tons")
    report.append("")

    # Match rates
    report.append(f"MATCH RATES BY PARTY ROLE")
    report.append(f"{'-'*80}")

    party_roles = ['Shipper', 'Consignee', 'Notify Party']

    for role in party_roles:
        harmonized_col = f'{role}_Harmonized'
        if harmonized_col not in df.columns:
            continue

        matched_records = df[harmonized_col].notna().sum()
        match_rate = (matched_records / len(df)) * 100

        matched_tonnage = df[df[harmonized_col].notna()]['Tons'].sum()
        tonnage_rate = (matched_tonnage / df['Tons'].sum()) * 100

        report.append(f"\n{role}:")
        report.append(f"  Records Matched: {matched_records:,} / {len(df):,} ({match_rate:.1f}%)")
        report.append(f"  Tonnage Matched: {matched_tonnage:,.0f} / {df['Tons'].sum():,.0f} ({tonnage_rate:.1f}%)")

        # Match types
        if df[harmonized_col].notna().any():
            match_types = df[df[harmonized_col].notna()][f'{role}_Match_Type'].value_counts()
            report.append(f"  Match Types:")
            for match_type, count in match_types.items():
                report.append(f"    {match_type}: {count:,}")

    # Top entities
    report.append(f"\n\nTOP 10 ENTITIES BY TONNAGE")
    report.append(f"{'-'*80}")

    entity_tonnage = {}
    for role in party_roles:
        harmonized_col = f'{role}_Harmonized'
        if harmonized_col not in df.columns:
            continue

        role_tonnage = df[df[harmonized_col].notna()].groupby(harmonized_col)['Tons'].sum()
        for entity, tons in role_tonnage.items():
            entity_tonnage[entity] = entity_tonnage.get(entity, 0) + tons

    top_entities = sorted(entity_tonnage.items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (entity, tons) in enumerate(top_entities, 1):
        report.append(f"{i:2d}. {entity:50s} {tons:15,.0f} tons")

    # Write report
    report_text = '\n'.join(report)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)

    print(f"  Report saved: {output_path.name}")

    # Print summary
    print("\n" + "="*80)
    print("TEST HARMONIZATION SUMMARY")
    print("="*80)
    for line in report[5:20]:
        print(line)

def main():
    """Main test execution"""
    print(f"\n{'='*80}")
    print(f"PARTY HARMONIZATION TEST - Q1 2024 SAMPLE")
    print(f"{'='*80}")

    # Check test sample exists
    if not TEST_INPUT.exists():
        print(f"\nERROR: Test sample not found: {TEST_INPUT}")
        print(f"  Run create_test_sample.py first")
        return

    # Load test sample
    print(f"\nLoading test sample: {TEST_INPUT.name}")
    df = pd.read_csv(TEST_INPUT, encoding='utf-8-sig', low_memory=False)
    print(f"  Loaded {len(df):,} records, {len(df.columns)} columns")
    print(f"  Tonnage: {df['Tons'].sum():,.0f} tons")

    # Load dictionary
    df_dict = load_dictionary()

    # Harmonize parties
    df = harmonize_parties(df, df_dict)

    # Save output
    print(f"\nSaving harmonized test results...")
    df.to_csv(TEST_OUTPUT, index=False, encoding='utf-8-sig')
    print(f"  Saved: {TEST_OUTPUT.name}")
    print(f"  Records: {len(df):,}")
    print(f"  Columns: {len(df.columns)} (added 9 harmonization columns)")

    # Generate report
    generate_test_report(df, TEST_REPORT)

    print(f"\n{'='*80}")
    print("TEST HARMONIZATION COMPLETE")
    print(f"{'='*80}")
    print(f"Harmonized Data: {TEST_OUTPUT.name}")
    print(f"Test Report: {TEST_REPORT.name}")
    print(f"\nTest was successful! Review results before running on full data.")

if __name__ == "__main__":
    main()
