"""
Infer Parties from Trade Lane Patterns - v1.0.0
================================================
Use trade lane fingerprints to infer missing party information.

Author: WSD3 / Claude Code
Date: 2026-02-09 (recreated from documentation)

Logic:
- If Shipper is blank but origin port + HS4 + commodity match known patterns
  → infer likely shipper from entity database
- Example: Brazil + Tubarao Port + HS 2601 (iron ore) → likely Vale

Input:  panjiva_imports_{year}_HARMONIZED_v1.0.0.csv
Output: panjiva_imports_{year}_HARMONIZED_INFERRED_v1.0.0.csv
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import argparse

# Paths
BASE_DIR = Path(r"G:\My Drive\LLM\project_manifest")
DICT_PATH = BASE_DIR / "01_DICTIONARIES" / "01.06_parties" / "party_harmonization_master_v1.3.0.csv"
INPUT_DIR = BASE_DIR / "00_DATA" / "00.03_MATCHED"
OUTPUT_DIR = BASE_DIR / "00_DATA" / "00.03_MATCHED"

# Trade lane patterns for inference
# Format: (Origin_Country, HS4, Likely_Entity_ID, Confidence)
TRADE_LANE_PATTERNS = [
    # Iron Ore
    ('BRAZIL', '2601', 'VALE-001', 95),
    ('CANADA', '2601', 'IRON-ORE-001', 90),

    # Bauxite
    ('JAMAICA', '2606', 'DISCOVERY-001', 90),

    # Crude Oil
    ('ECUADOR', '2709', 'EP-PETROECUADOR-001', 95),
    ('IRAQ', '2709', 'SOMO-001', 90),
    ('VENEZUELA', '2709', 'PDVSA-001', 85),
    ('COLOMBIA', '2709', 'ECOPETROL-001', 85),
    ('LIBYA', '2709', 'NATIONAL-OIL-LIBYA-001', 85),
    ('BRAZIL', '2709', 'PETROBRAS-001', 80),

    # Cement (by country patterns)
    ('TURKEY', '2523', 'NUH-CIMENTO-001', 70),  # Lower confidence - multiple Turkish cement producers
    ('VIETNAM', '2523', 'VISSAI-001', 75),
    ('UAE', '2523', 'LAFARGE-EMIRATES-001', 70),

    # Aluminum
    ('UAE', '7601', 'EMIRATES-001', 90),

    # Salt
    ('BAHAMAS', '2501', 'MORTON-BAHAMAS-001', 85),
]

def load_dictionary():
    """Load party harmonization dictionary"""
    print("Loading party harmonization dictionary...")
    df_dict = pd.read_csv(DICT_PATH, encoding='utf-8-sig')
    print(f"  Loaded {len(df_dict)} entities")
    return df_dict

def infer_shipper_from_trade_lane(row, df_dict):
    """
    Infer likely shipper based on trade lane pattern.

    Args:
        row: DataFrame row with trade data
        df_dict: Entity dictionary

    Returns:
        tuple: (inferred_canonical_name, inferred_entity_id, confidence) or (None, None, None)
    """
    # Only infer if shipper is blank
    if pd.notna(row.get('Shipper_Entity_ID')):
        return None, None, None

    # Get trade lane characteristics
    origin = str(row.get('Origin_Country', '')).upper().strip()
    hs4 = str(row.get('HS4', '')).strip()

    # Check against patterns
    for pattern_origin, pattern_hs4, entity_id, confidence in TRADE_LANE_PATTERNS:
        if origin == pattern_origin and hs4 == pattern_hs4:
            # Look up entity details
            entity = df_dict[df_dict['Entity_ID'] == entity_id]
            if not entity.empty:
                return entity.iloc[0]['Canonical_Name'], entity_id, confidence

    return None, None, None

def infer_parties(df, df_dict):
    """
    Infer missing party information from trade lane patterns.

    Args:
        df: Input dataframe with harmonized party columns
        df_dict: Entity dictionary

    Returns:
        DataFrame with inferred party columns
    """
    print("\nInferring missing parties from trade lane patterns...")

    # Initialize inference columns
    df['Shipper_Inferred'] = None
    df['Shipper_Inferred_Entity_ID'] = None
    df['Shipper_Inferred_Confidence'] = None

    inferred_count = 0
    total_blank = df['Shipper_Entity_ID'].isna().sum()

    for idx, row in df.iterrows():
        canonical, entity_id, confidence = infer_shipper_from_trade_lane(row, df_dict)

        if canonical is not None:
            df.at[idx, 'Shipper_Inferred'] = canonical
            df.at[idx, 'Shipper_Inferred_Entity_ID'] = entity_id
            df.at[idx, 'Shipper_Inferred_Confidence'] = confidence
            inferred_count += 1

        # Progress indicator
        if (idx + 1) % 50000 == 0:
            print(f"  Processed {idx + 1:,} / {len(df):,} records...")

    print(f"\n  Blank shippers: {total_blank:,}")
    print(f"  Inferred: {inferred_count:,} ({inferred_count/total_blank*100:.1f}% of blanks)")

    return df

def generate_inference_report(df, year, output_path):
    """Generate report on inferred parties"""
    print("\nGenerating inference report...")

    report = []
    report.append(f"PARTY INFERENCE VALIDATION REPORT")
    report.append(f"{'='*80}")
    report.append(f"Year: {year}")
    report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    # Inference statistics
    inferred = df[df['Shipper_Inferred'].notna()]
    report.append(f"INFERENCE STATISTICS")
    report.append(f"{'-'*80}")
    report.append(f"Total Records: {len(df):,}")
    report.append(f"Blank Shippers: {df['Shipper_Entity_ID'].isna().sum():,}")
    report.append(f"Inferred Shippers: {len(inferred):,}")
    report.append(f"Inference Rate: {len(inferred)/df['Shipper_Entity_ID'].isna().sum()*100:.1f}%")
    report.append("")

    # Tonnage impact
    inferred_tonnage = inferred['Tons'].sum()
    report.append(f"Tonnage Impact: {inferred_tonnage:,.0f} tons")
    report.append("")

    # Inferred entities breakdown
    report.append(f"INFERRED ENTITIES (Top 10)")
    report.append(f"{'-'*80}")
    entity_counts = inferred.groupby('Shipper_Inferred_Entity_ID').agg({
        'REC_ID': 'count',
        'Tons': 'sum',
        'Shipper_Inferred_Confidence': 'mean'
    }).sort_values('Tons', ascending=False).head(10)

    for entity_id, row in entity_counts.iterrows():
        entity_name = inferred[inferred['Shipper_Inferred_Entity_ID'] == entity_id].iloc[0]['Shipper_Inferred']
        report.append(f"\n{entity_name} ({entity_id}):")
        report.append(f"  Records: {int(row['REC_ID']):,}")
        report.append(f"  Tonnage: {row['Tons']:,.0f} tons")
        report.append(f"  Avg Confidence: {row['Shipper_Inferred_Confidence']:.0f}%")

    # Write report
    report_text = '\n'.join(report)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)

    print(f"\n  Report saved: {output_path}")

def main(year):
    """Main execution"""
    print(f"\n{'='*80}")
    print(f"PARTY INFERENCE FROM TRADE LANES v1.0.0")
    print(f"{'='*80}")
    print(f"Year: {year}")

    # File paths
    input_file = INPUT_DIR / f"panjiva_imports_{year}_HARMONIZED_v1.0.0.csv"
    output_file = OUTPUT_DIR / f"panjiva_imports_{year}_HARMONIZED_INFERRED_v1.0.0.csv"
    report_file = OUTPUT_DIR / f"inference_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    # Check input exists
    if not input_file.exists():
        print(f"\nERROR: Input file not found: {input_file}")
        print(f"  Run harmonize_party_names_v1.0.0.py first")
        return

    # Load data
    print(f"\nLoading harmonized data: {input_file.name}")
    df = pd.read_csv(input_file, encoding='utf-8-sig', low_memory=False)
    print(f"  Loaded {len(df):,} records")

    # Load dictionary
    df_dict = load_dictionary()

    # Infer parties
    df = infer_parties(df, df_dict)

    # Save output
    print(f"\nSaving data with inferred parties...")
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"  Saved: {output_file}")
    print(f"  Records: {len(df):,}")
    print(f"  Columns: {len(df.columns)} (added 3 inference columns)")

    # Generate report
    generate_inference_report(df, year, report_file)

    print(f"\n{'='*80}")
    print("INFERENCE COMPLETE")
    print(f"{'='*80}")
    print(f"Output: {output_file.name}")
    print(f"Report: {report_file.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Infer missing parties from trade lane patterns')
    parser.add_argument('--year', type=int, required=True, help='Year to process (e.g., 2024)')

    args = parser.parse_args()
    main(args.year)
