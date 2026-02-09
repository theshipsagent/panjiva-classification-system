"""
Refine Cement Classification with Entity Harmonization - v1.0.0
================================================================
Use harmonized entity data to lock cement classifications with high confidence.

Author: WSD3 / Claude Code
Date: 2026-02-09 (recreated from documentation)

Logic:
- If Shipper_Entity_ID matches known cement producer → lock cargo as Cement
- Example: Shipper_Entity_ID = "NUH-CIMENTO-001" → Cargo = Cement (99% confidence)

This demonstrates how entity-based rules can improve cargo classification.

Input:  panjiva_imports_{year}_HARMONIZED_v1.0.0.csv (with entity columns)
        panjiva_imports_{year}_classified.csv (with cargo classifications)
Output: panjiva_imports_{year}_classified_ENTITY_REFINED.csv
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import argparse

# Paths
BASE_DIR = Path(r"G:\My Drive\LLM\project_manifest")
DICT_PATH = BASE_DIR / "01_DICTIONARIES" / "01.06_parties" / "party_harmonization_master_v1.3.0.csv"
HARMONIZED_DIR = BASE_DIR / "00_DATA" / "00.03_MATCHED"
CLASSIFIED_DIR = BASE_DIR / "00_DATA" / "00.03_MATCHED"
OUTPUT_DIR = BASE_DIR / "00_DATA" / "00.03_MATCHED"

# Known cement producer entity IDs from dictionary
CEMENT_ENTITY_IDS = [
    'NUH-CIMENTO-001',      # Nuh Cimento (Turkey)
    'VISSAI-001',           # Vissai Ninh Binh (Vietnam)
    'LAFARGE-EMIRATES-001', # Lafarge Emirates (UAE)
    'SAUDI-CEMENT-001',     # Saudi Cement (Saudi Arabia)
    'AKCANSA-001',          # Akcansa Cimento (Turkey)
    'CEMTECH-001',          # Cemtech Global (Turkey)
    'TAIHEIYO-001',         # Taiheiyo Cement (Japan)
    'TITAN-001',            # Titan Cement (Greece)
    'ZONA-FRANCA-ARGOS-001',# Zona Franca Argos (Colombia)
    'ARGOS-001',            # Argos USA (Colombia/US)
    'CEMEX-001',            # Cemex (Mexico)
    'LAFARGE-001',          # Lafarge North America
    'ASH-GROVE-001',        # Ash Grove Cement (US)
    'HOUSTON-CEMENT-001',   # Houston Cement (US)
    'HOLLINGSHEAD-001',     # Hollingshead Cement (US)
    'SESCO-001',            # Sesco Cement (US)
    'MCINNIS-001',          # McInnis USA (Canada/US)
    'ST-MARYS-001',         # St. Marys Cement (Canada/US)
    'HM-SOUTHEAST-001',     # Heidelberg Materials Southeast (Germany/US)
]

def load_dictionary():
    """Load party harmonization dictionary"""
    print("Loading party harmonization dictionary...")
    df_dict = pd.read_csv(DICT_PATH, encoding='utf-8-sig')

    # Filter to cement entities only
    cement_entities = df_dict[df_dict['Entity_Type'].str.contains('Cement', case=False, na=False)]
    print(f"  Loaded {len(cement_entities)} cement entities")

    return cement_entities

def refine_cement_classification(df_classified, df_harmonized):
    """
    Refine cement classifications using entity harmonization.

    Args:
        df_classified: Classified data with cargo taxonomy
        df_harmonized: Harmonized data with entity columns

    Returns:
        DataFrame with entity-refined classifications
    """
    print("\nRefining cement classifications with entity data...")

    # Merge harmonized party data into classified data
    # Match on REC_ID
    if 'REC_ID' not in df_classified.columns or 'REC_ID' not in df_harmonized.columns:
        print("  ERROR: REC_ID column not found in one or both datasets")
        return df_classified

    # Get entity columns from harmonized data
    entity_cols = [
        'Shipper_Harmonized', 'Shipper_Entity_ID', 'Shipper_Match_Type',
        'Consignee_Harmonized', 'Consignee_Entity_ID', 'Consignee_Match_Type'
    ]

    # Merge entity data
    df_merged = df_classified.merge(
        df_harmonized[['REC_ID'] + entity_cols],
        on='REC_ID',
        how='left'
    )

    print(f"  Merged classified + harmonized data: {len(df_merged):,} records")

    # Track refinements
    refinements = {
        'previously_unclassified': 0,
        'upgraded_to_cement': 0,
        'locked_cement': 0,
        'tonnage_affected': 0
    }

    # Apply entity-based cement rules
    for idx, row in df_merged.iterrows():
        # Check if shipper is known cement producer
        shipper_entity = row.get('Shipper_Entity_ID')

        if pd.notna(shipper_entity) and shipper_entity in CEMENT_ENTITY_IDS:
            # Validate HS code is cement-related (HS 2523)
            hs4 = str(row.get('HS4', ''))

            if hs4 == '2523':
                # Get shipper name for cargo detail
                shipper_name = row.get('Shipper_Harmonized', 'Unknown')
                origin = row.get('Origin_Country', '')

                # Check current classification
                current_commodity = row.get('Commodity', '')

                if current_commodity != 'Cement':
                    if current_commodity == 'TBN':
                        refinements['previously_unclassified'] += 1
                    else:
                        refinements['upgraded_to_cement'] += 1

                    # Lock as cement with entity-specific detail
                    df_merged.at[idx, 'Group'] = 'Dry Bulk'
                    df_merged.at[idx, 'Commodity'] = 'Cement'
                    df_merged.at[idx, 'Cargo'] = 'Cement'
                    df_merged.at[idx, 'Cargo_Detail'] = f'Cement - {origin} ({shipper_name})'
                    df_merged.at[idx, 'Classification_Phase'] = 'Entity-Based'
                    df_merged.at[idx, 'Rule_ID'] = f'ENTITY-CEMENT-{shipper_entity}'

                    refinements['tonnage_affected'] += row.get('Tons', 0)
                else:
                    # Already classified as cement, just lock it
                    refinements['locked_cement'] += 1

        # Progress indicator
        if (idx + 1) % 50000 == 0:
            print(f"  Processed {idx + 1:,} / {len(df_merged):,} records...")

    # Print refinement statistics
    print(f"\n  Entity-Based Refinements:")
    print(f"    Previously Unclassified → Cement: {refinements['previously_unclassified']:,}")
    print(f"    Upgraded to Cement: {refinements['upgraded_to_cement']:,}")
    print(f"    Locked Existing Cement: {refinements['locked_cement']:,}")
    print(f"    Tonnage Affected: {refinements['tonnage_affected']:,.0f} tons")

    return df_merged, refinements

def generate_refinement_report(df, year, refinements, output_path):
    """Generate report on entity-based refinements"""
    print("\nGenerating refinement report...")

    report = []
    report.append(f"CEMENT ENTITY REFINEMENT REPORT")
    report.append(f"{'='*80}")
    report.append(f"Year: {year}")
    report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    # Refinement summary
    report.append(f"REFINEMENT SUMMARY")
    report.append(f"{'-'*80}")
    report.append(f"Previously Unclassified → Cement: {refinements['previously_unclassified']:,}")
    report.append(f"Upgraded to Cement: {refinements['upgraded_to_cement']:,}")
    report.append(f"Locked Existing Cement: {refinements['locked_cement']:,}")
    report.append(f"Total Tonnage Affected: {refinements['tonnage_affected']:,.0f} tons")
    report.append("")

    # Entity breakdown
    entity_cement = df[df['Classification_Phase'] == 'Entity-Based']
    if not entity_cement.empty:
        report.append(f"CEMENT BY ENTITY (Entity-Based Rules)")
        report.append(f"{'-'*80}")

        entity_summary = entity_cement.groupby('Shipper_Harmonized').agg({
            'REC_ID': 'count',
            'Tons': 'sum',
            'Origin_Country': lambda x: x.mode()[0] if not x.empty else ''
        }).sort_values('Tons', ascending=False)

        for entity, row in entity_summary.iterrows():
            report.append(f"\n{entity} ({row['Origin_Country']}):")
            report.append(f"  Records: {int(row['REC_ID']):,}")
            report.append(f"  Tonnage: {row['Tons']:,.0f} tons")

    # Write report
    report_text = '\n'.join(report)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)

    print(f"\n  Report saved: {output_path}")

def main(year):
    """Main execution"""
    print(f"\n{'='*80}")
    print(f"CEMENT ENTITY REFINEMENT v1.0.0")
    print(f"{'='*80}")
    print(f"Year: {year}")

    # File paths
    harmonized_file = HARMONIZED_DIR / f"panjiva_imports_{year}_HARMONIZED_v1.0.0.csv"
    classified_file = CLASSIFIED_DIR / f"panjiva_imports_{year}_classified.csv"
    output_file = OUTPUT_DIR / f"panjiva_imports_{year}_classified_ENTITY_REFINED.csv"
    report_file = OUTPUT_DIR / f"cement_refinement_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    # Check inputs exist
    if not harmonized_file.exists():
        print(f"\nERROR: Harmonized file not found: {harmonized_file}")
        print(f"  Run harmonize_party_names_v1.0.0.py first")
        return

    if not classified_file.exists():
        print(f"\nERROR: Classified file not found: {classified_file}")
        print(f"  This file should contain cargo classifications")
        return

    # Load data
    print(f"\nLoading harmonized data: {harmonized_file.name}")
    df_harmonized = pd.read_csv(harmonized_file, encoding='utf-8-sig', low_memory=False)
    print(f"  Loaded {len(df_harmonized):,} records")

    print(f"\nLoading classified data: {classified_file.name}")
    df_classified = pd.read_csv(classified_file, encoding='utf-8-sig', low_memory=False)
    print(f"  Loaded {len(df_classified):,} records")

    # Load dictionary
    df_dict = load_dictionary()

    # Refine classifications
    df_refined, refinements = refine_cement_classification(df_classified, df_harmonized)

    # Save output
    print(f"\nSaving entity-refined classifications...")
    df_refined.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"  Saved: {output_file}")
    print(f"  Records: {len(df_refined):,}")

    # Generate report
    generate_refinement_report(df_refined, year, refinements, report_file)

    print(f"\n{'='*80}")
    print("REFINEMENT COMPLETE")
    print(f"{'='*80}")
    print(f"Output: {output_file.name}")
    print(f"Report: {report_file.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Refine cement classification with entity data')
    parser.add_argument('--year', type=int, required=True, help='Year to process (e.g., 2024)')

    args = parser.parse_args()
    main(args.year)
