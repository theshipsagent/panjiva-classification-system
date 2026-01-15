"""
Classify 15k sample from 2024 data using v3.6.0 dictionary (REFINED KEYWORDS)

v3.6.0: Comprehensive user-edited classifications with refined keyword strategy
- 218 new user-edited rules across 31 HS2 chapters
- New keyword system: Key_Phrases, Primary_Keywords, Descriptor_Keywords
- Match_Strategy: PHRASE_REQUIRED vs PRIMARY_SUFFICIENT
- Major coverage: Mineral Fuels, Chemicals, Metals, Construction, Fertilizers

Author: WSD3 / Claude Code
Date: 2026-01-14
Version: 3.6.0
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import traceback

# Paths
INPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\01_step_one\01_01_panjiva_imports_step_one\panjiva_imports_2024_20260112_STAGE00_v20260112_2052.csv")
SHIP_REGISTRY = Path(r"G:\My Drive\LLM\project_manifest\01.01_dictionary\01_ships_register.csv")
DICTIONARY = Path(r"G:\My Drive\LLM\project_manifest\user_notes\cargo_classification_dictionary_v3.6.0_DRAFT_20260114.csv")
OUTPUT_DIR = Path(r"G:\My Drive\LLM\project_manifest\build_documentation\sample_test_15k")
OUTPUT_FILE = OUTPUT_DIR / "sample_15k_classified_v3.6.0.csv"
STATS_FILE = OUTPUT_DIR / "classification_stats_v3.6.0.csv"

def stamp(msg):
    """Print timestamped message"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def map_vessel_type(detailed_type):
    """Map detailed vessel type to simplified category"""
    if pd.isna(detailed_type) or detailed_type == '':
        return ''

    detailed_type = str(detailed_type).upper()

    if any(x in detailed_type for x in ['BULK CARRIER', 'BULKER', 'CAPESIZE', 'PANAMAX',
                                          'HANDYMAX', 'HANDYSIZE', 'SUPRAMAX', 'ULTRAMAX']):
        return 'Bulk Carrier'
    if any(x in detailed_type for x in ['TANKER', 'VLCC', 'SUEZMAX', 'AFRAMAX', 'MR', 'LR']):
        return 'Tanker'
    if any(x in detailed_type for x in ['LPG', 'LNG', 'GAS CARRIER']):
        return 'LPG/LNG Carrier'
    if any(x in detailed_type for x in ['CONTAINER', 'TEU', 'FEEDER']):
        return 'Container'
    if any(x in detailed_type for x in ['RO-RO', 'RORO', 'CAR CARRIER', 'PCTC']):
        return 'RoRo'
    if any(x in detailed_type for x in ['REEFER', 'REFRIGERAT']):
        return 'Reefer'
    if any(x in detailed_type for x in ['GENERAL CARGO', 'MULTI-PURPOSE']):
        return 'General Cargo'

    return ''

def add_vessel_types(df):
    """Add vessel types from ship registry"""
    stamp("\n=== Adding Vessel Types ===")

    # Load ship registry
    df_ships = pd.read_csv(SHIP_REGISTRY, dtype=str)
    stamp(f"Loaded {len(df_ships)} vessels from registry")

    # Create lookup
    vessel_lookup = {}
    for _, row in df_ships.iterrows():
        vessel_name = str(row['Vessel']).upper().strip()
        vessel_type = map_vessel_type(row.get('Type', ''))
        if vessel_name and vessel_type:
            vessel_lookup[vessel_name] = vessel_type

    stamp(f"Created lookup for {len(vessel_lookup)} vessels")

    # Add Vessel_Type_Simple column
    df['Vessel_Type_Simple'] = df['Vessel'].apply(
        lambda x: vessel_lookup.get(str(x).upper().strip(), '') if pd.notna(x) else ''
    )

    matched = len(df[df['Vessel_Type_Simple'] != ''])
    stamp(f"Matched vessel types: {matched} / {len(df)} ({matched/len(df)*100:.1f}%)")

    return df

def extract_sample():
    """Extract first 15k rows from 2024 file"""
    stamp("=== Extracting 15k Sample ===")
    stamp(f"Reading: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE, dtype=str, nrows=15000)
    stamp(f"Loaded {len(df)} records")

    return df

def load_dictionary():
    """Load classification dictionary"""
    stamp("\n=== Loading Dictionary ===")
    stamp(f"Reading: {DICTIONARY}")

    df_dict = pd.read_csv(DICTIONARY, dtype=str)
    stamp(f"Loaded {len(df_dict)} rules")

    # Filter active rules only
    df_dict = df_dict[df_dict['Active'] == 'TRUE']
    stamp(f"Active rules: {len(df_dict)}")

    # Show breakdown
    stamp("Breakdown by Phase:")
    for phase in sorted(df_dict['Phase'].unique()):
        count = len(df_dict[df_dict['Phase'] == phase])
        stamp(f"  Phase {phase}: {count} rules")

    return df_dict

def check_keyword_match(cargo_desc, rule):
    """Check keyword match using refined keyword strategy

    NEW in v3.6.0:
    - Key_Phrases: Multi-word phrases (e.g., "CRUDE OIL", "PIG IRON")
    - Primary_Keywords: Standalone product terms (e.g., "CEMENT", "STEEL")
    - Descriptor_Keywords: Modifiers (e.g., "HOT", "ROLLED", "PRIME")
    - Match_Strategy: PHRASE_REQUIRED or PRIMARY_SUFFICIENT
    """

    cargo_desc_upper = cargo_desc.upper()

    # Get keyword fields
    key_phrases = str(rule.get('Key_Phrases', '')).strip()
    primary_kw = str(rule.get('Primary_Keywords', '')).strip()
    descriptor_kw = str(rule.get('Descriptor_Keywords', '')).strip()
    match_strategy = str(rule.get('Match_Strategy', 'PRIMARY_SUFFICIENT')).strip()

    # Legacy Keywords column (if no new columns populated)
    legacy_keywords = str(rule.get('Keywords', '')).strip()

    # If no keywords at all, no keyword filter
    if not any([key_phrases != 'nan' and key_phrases,
                primary_kw != 'nan' and primary_kw,
                descriptor_kw != 'nan' and descriptor_kw,
                legacy_keywords != 'nan' and legacy_keywords]):
        return True

    # PHRASE_REQUIRED: Must match at least one key phrase
    if match_strategy == 'PHRASE_REQUIRED' and key_phrases and key_phrases != 'nan':
        phrase_list = [p.strip().upper() for p in key_phrases.split(',')]
        if any(phrase in cargo_desc_upper for phrase in phrase_list if phrase):
            return True
        return False

    # PRIMARY_SUFFICIENT: Match primary keywords or key phrases
    if primary_kw and primary_kw != 'nan':
        primary_list = [k.strip().upper() for k in primary_kw.split(',')]
        if any(kw in cargo_desc_upper for kw in primary_list if kw):
            return True

    if key_phrases and key_phrases != 'nan':
        phrase_list = [p.strip().upper() for p in key_phrases.split(',')]
        if any(phrase in cargo_desc_upper for phrase in phrase_list if phrase):
            return True

    # Fall back to legacy Keywords (semicolon separated)
    if legacy_keywords and legacy_keywords != 'nan':
        legacy_list = [k.strip().upper() for k in legacy_keywords.split(';')]
        if any(kw in cargo_desc_upper for kw in legacy_list if kw):
            return True

    return False

def check_match(record, rule):
    """Check if a rule matches a record"""

    # Carrier SCAC match
    carrier_scac = rule.get('Carrier_SCAC', '')
    if carrier_scac and pd.notna(carrier_scac) and carrier_scac.strip():
        record_carrier = str(record.get('Carrier', '')).upper()
        if carrier_scac.upper() not in record_carrier:
            return False

    # Vessel Type match
    vessel_type = rule.get('Vessel_Type', '')
    if vessel_type and pd.notna(vessel_type) and vessel_type.strip():
        record_vtype = str(record.get('Vessel_Type_Simple', '')).upper()
        vessel_types = [v.strip().upper() for v in str(vessel_type).split(';')]
        if not any(vt in record_vtype for vt in vessel_types):
            return False

    # HS Code matches
    for hs_level in ['HS2', 'HS4', 'HS6']:
        rule_hs = rule.get(hs_level, '')
        if rule_hs and pd.notna(rule_hs) and rule_hs.strip():
            record_hs = str(record.get(hs_level, '')).strip()
            if rule_hs.strip() != record_hs:
                return False

    # Keyword match using refined strategy
    cargo_desc = str(record.get('Goods Shipped', ''))
    if not check_keyword_match(cargo_desc, rule):
        return False

    # Exclude Keywords
    exclude_kw = rule.get('Exclude_Keywords', '')
    if exclude_kw and pd.notna(exclude_kw) and exclude_kw.strip():
        cargo_desc_upper = cargo_desc.upper()
        exclude_list = [k.strip().upper() for k in str(exclude_kw).split(';')]
        if any(ex in cargo_desc_upper for ex in exclude_list):
            return False

    # Tonnage filter
    min_tons = rule.get('Min_Tons', '')
    max_tons = rule.get('Max_Tons', '')
    if (min_tons and pd.notna(min_tons) and min_tons.strip()) or \
       (max_tons and pd.notna(max_tons) and max_tons.strip()):
        try:
            record_tons = float(str(record.get('Tons', '0')).replace(',', ''))
            if min_tons and pd.notna(min_tons) and min_tons.strip():
                if record_tons < float(min_tons):
                    return False
            if max_tons and pd.notna(max_tons) and max_tons.strip():
                if record_tons > float(max_tons):
                    return False
        except:
            pass

    return True

def can_apply_rule(record, rule):
    """Check if rule can be applied based on lock levels and exclusions"""

    # Check Exclude_Groups
    exclude_groups = rule.get('Exclude_Groups', '')
    if exclude_groups and pd.notna(exclude_groups) and exclude_groups.strip():
        current_group = str(record.get('Group', '')).strip()
        if current_group:
            exclude_list = [g.strip() for g in str(exclude_groups).split(';')]
            if current_group in exclude_list:
                return False

    # Check lock levels
    if record.get('Group_Locked') == 'TRUE':
        rule_group = str(rule.get('Group', '')).strip()
        current_group = str(record.get('Group', '')).strip()
        if rule_group and current_group and rule_group != current_group:
            return False

    if record.get('Commodity_Locked') == 'TRUE':
        rule_commodity = str(rule.get('Commodity', '')).strip()
        current_commodity = str(record.get('Commodity', '')).strip()
        if rule_commodity and current_commodity and rule_commodity != current_commodity:
            return False

    if record.get('Cargo_Locked') == 'TRUE':
        rule_cargo = str(rule.get('Cargo', '')).strip()
        current_cargo = str(record.get('Cargo', '')).strip()
        if rule_cargo and current_cargo and rule_cargo != current_cargo:
            return False

    if record.get('Cargo_Detail_Locked') == 'TRUE':
        return False  # All locked, no further classification

    return True

def apply_rule(record, rule):
    """Apply rule to record, respecting lock levels"""

    def clean_value(val):
        """Convert nan/empty to TBN"""
        if not val or pd.isna(val):
            return 'TBN'
        val_str = str(val).strip()
        if not val_str or val_str.lower() == 'nan':
            return 'TBN'
        return val_str

    # Set taxonomy values from rule
    group = rule.get('Group', '')
    if group and pd.notna(group) and str(group).strip() and str(group).strip().lower() != 'nan':
        record['Group'] = group

    commodity = rule.get('Commodity', '')
    record['Commodity'] = clean_value(commodity)

    cargo = rule.get('Cargo', '')
    record['Cargo'] = clean_value(cargo)

    cargo_detail = rule.get('Cargo_Detail', '')
    record['Cargo Detail'] = clean_value(cargo_detail)

    # Set lock status based on rule
    if rule.get('Lock_Group') == 'TRUE':
        record['Group_Locked'] = 'TRUE'

    if rule.get('Lock_Commodity') == 'TRUE':
        record['Commodity_Locked'] = 'TRUE'

    if rule.get('Lock_Cargo') == 'TRUE':
        record['Cargo_Locked'] = 'TRUE'

    if rule.get('Lock_Cargo_Detail') == 'TRUE':
        record['Cargo_Detail_Locked'] = 'TRUE'

    # Track classification
    if not record.get('Classified_Phase'):
        record['Classified_Phase'] = rule.get('Phase', '')

    record['Last_Rule_ID'] = rule.get('Rule_ID', '')

    return record

def classify_records(df, df_dict):
    """Classify all records using dictionary"""
    stamp("\n=== Classifying Records ===")

    # Initialize classification columns
    if 'Group' not in df.columns:
        df['Group'] = ''
    if 'Commodity' not in df.columns:
        df['Commodity'] = ''
    if 'Cargo' not in df.columns:
        df['Cargo'] = ''

    df['Group_Locked'] = 'FALSE'
    df['Commodity_Locked'] = 'FALSE'
    df['Cargo_Locked'] = 'FALSE'
    df['Cargo_Detail_Locked'] = 'FALSE'
    df['Classified_Phase'] = ''
    df['Last_Rule_ID'] = ''

    # Process by phase
    phases = sorted(df_dict['Phase'].astype(int).unique())

    for phase in phases:
        stamp(f"\nProcessing Phase {phase}...")
        phase_rules = df_dict[df_dict['Phase'] == str(phase)]
        stamp(f"  Rules in phase: {len(phase_rules)}")

        phase_matches = 0

        for idx, record in df.iterrows():
            # Skip if all locked
            if record['Cargo_Detail_Locked'] == 'TRUE':
                continue

            # Try each rule in phase
            for _, rule in phase_rules.iterrows():
                if check_match(record, rule) and can_apply_rule(record, rule):
                    df.loc[idx] = apply_rule(record, rule)
                    phase_matches += 1
                    break  # First match wins in phase

        stamp(f"  Matched: {phase_matches} records")

    # Count classified
    classified = len(df[df['Group'] != ''])
    stamp(f"\nTotal classified: {classified} / {len(df)} ({classified/len(df)*100:.1f}%)")

    return df

def generate_stats(df):
    """Generate classification statistics"""
    stamp("\n=== Generating Statistics ===")

    stats = []

    # Overall stats
    total = len(df)
    classified = len(df[df['Group'] != ''])
    stats.append({
        'Metric': 'Total Records',
        'Count': total,
        'Percentage': '100.0%'
    })
    stats.append({
        'Metric': 'Classified',
        'Count': classified,
        'Percentage': f'{classified/total*100:.1f}%'
    })
    stats.append({
        'Metric': 'Unclassified',
        'Count': total - classified,
        'Percentage': f'{(total-classified)/total*100:.1f}%'
    })

    # By Phase
    stats.append({'Metric': '', 'Count': '', 'Percentage': ''})
    stats.append({'Metric': 'By Phase:', 'Count': '', 'Percentage': ''})
    for phase in sorted(df['Classified_Phase'].unique()):
        if phase:
            count = len(df[df['Classified_Phase'] == phase])
            stats.append({
                'Metric': f'  Phase {phase}',
                'Count': count,
                'Percentage': f'{count/total*100:.1f}%'
            })

    # By Group
    stats.append({'Metric': '', 'Count': '', 'Percentage': ''})
    stats.append({'Metric': 'By Classification Group:', 'Count': '', 'Percentage': ''})
    group_counts = df.groupby('Group').size().sort_values(ascending=False)
    for group, count in group_counts.items():
        if group:
            stats.append({
                'Metric': f'  {group}',
                'Count': count,
                'Percentage': f'{count/total*100:.1f}%'
            })

    df_stats = pd.DataFrame(stats)
    df_stats.to_csv(STATS_FILE, index=False)
    stamp(f"Statistics saved to: {STATS_FILE.name}")

    # Print summary
    stamp("\nClassification Summary:")
    for _, row in df_stats.head(20).iterrows():
        if row['Metric']:
            stamp(f"{row['Metric']:40s} {str(row['Count']):>10s}  {row['Percentage']}")

    return df_stats

def main():
    """Main execution"""
    stamp("=" * 80)
    stamp("Dictionary v3.6.0 Classification Test")
    stamp("=" * 80)

    try:
        # Extract sample
        df = extract_sample()

        # Add vessel types
        df = add_vessel_types(df)

        # Load dictionary
        df_dict = load_dictionary()

        # Classify
        df = classify_records(df, df_dict)

        # Generate stats
        generate_stats(df)

        # Save results
        stamp(f"\n=== Saving Results ===")
        stamp(f"Writing: {OUTPUT_FILE}")
        df.to_csv(OUTPUT_FILE, index=False)

        stamp("\n" + "=" * 80)
        stamp("Classification Complete!")
        stamp("=" * 80)

    except Exception as e:
        stamp(f"\nERROR: {str(e)}")
        stamp(traceback.format_exc())

if __name__ == "__main__":
    main()
