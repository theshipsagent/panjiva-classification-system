"""
Transform USACE Clearance Data (Outbound/Exports) v2.0.0

CRITICAL FIX: Use USACE waterway codes, NOT Census Sked D codes!

USACE data uses USACE waterway codes (code 4110 = Long Beach Harbor, CA)
Census Sked D uses different codes (code 4110 = Indianapolis, IN)

Dictionary Mapping:
- PORT (clearance port) → USACE waterway codes
- WHERE_PORT (domestic previous) → USACE waterway codes
- WHERE_SCHEDK (foreign previous) → USACE Sked K foreign ports

Author: WSD3 / Claude Code
Date: 2026-01-15
Version: 2.0.0 - Clearance/Outbound/Exports transformation
"""

import pandas as pd
import re
from pathlib import Path

def transform_clearance_data(input_file, output_file, test_mode=False):
    """Transform USACE clearance/outbound data"""

    print("=" * 80)
    print("USACE Clearance Data Transformation v2.0.0 (Outbound/Exports)")
    print("=" * 80)
    print()

    # Load USACE dictionaries
    print("Loading USACE port dictionaries...")

    dict_path = Path(r"G:\My Drive\LLM\project_manifest\01.01_dictionary")

    # USACE Port Codes (extracted from USACE entrance data itself)
    # This contains ALL port codes used in USACE data (PORT and WHERE_PORT columns)
    df_usace_ports = pd.read_csv(dict_path / "usace_port_codes_from_data.csv", dtype=str)
    usace_port_lookup = {}
    for _, row in df_usace_ports.iterrows():
        code = str(row['Port_Code']).strip()
        usace_port_lookup[code] = str(row['Port_Name']).strip()
    print(f"  Loaded {len(usace_port_lookup)} USACE port codes (from source data)")

    # Foreign ports dictionary (Sked K)
    df_foreign_ports = pd.read_csv(dict_path / "usace_sked_k_foreign_ports.csv", dtype=str)
    foreign_port_lookup = {}
    for _, row in df_foreign_ports.iterrows():
        code = str(row['FORPORT_CD']).strip()
        foreign_port_lookup[code] = {
            'Foreign_Port': str(row.get('FORPORT_NAME', '')).strip(),
            'Foreign_Country': str(row.get('CTRY_NAME', '')).strip()
        }
    print(f"  Loaded {len(foreign_port_lookup)} foreign ports (Sked K)")

    # Ships Register (for vessel matching)
    print("  Loading ships register...")
    df_ships = pd.read_csv(dict_path / "01_ships_register.csv", dtype=str)

    # Build IMO lookup (primary match)
    imo_lookup = {}
    for _, row in df_ships.iterrows():
        imo = str(row.get('IMO', '')).strip()
        if imo and imo != '' and imo != 'nan':
            imo_lookup[imo] = {
                'Type': str(row.get('Type', '')).strip(),
                'DWT': str(row.get('DWT', '')).strip(),
                'Grain': str(row.get('Grain', '')).strip(),
                'TPC': str(row.get('TPC', '')).strip(),
                'Dwt_Draft_m': str(row.get('Dwt_Draft(m)', '')).strip()
            }

    # Build vessel name lookup (secondary match) - normalize names
    def normalize_vessel_name(name):
        """Remove special chars, punctuation, convert to lowercase"""
        if pd.isna(name) or name == '':
            return ''
        # Remove punctuation and special chars, keep only alphanumeric
        normalized = re.sub(r'[^a-zA-Z0-9\s]', '', str(name))
        # Convert to lowercase and remove extra spaces
        normalized = ' '.join(normalized.lower().split())
        return normalized

    vessel_lookup = {}
    for _, row in df_ships.iterrows():
        vessel = str(row.get('Vessel', '')).strip()
        normalized = normalize_vessel_name(vessel)
        if normalized and normalized != '':
            vessel_lookup[normalized] = {
                'Type': str(row.get('Type', '')).strip(),
                'DWT': str(row.get('DWT', '')).strip(),
                'Grain': str(row.get('Grain', '')).strip(),
                'TPC': str(row.get('TPC', '')).strip(),
                'Dwt_Draft_m': str(row.get('Dwt_Draft(m)', '')).strip()
            }

    print(f"    IMO matches: {len(imo_lookup)} vessels")
    print(f"    Name matches: {len(vessel_lookup)} vessels")

    # Cargo Classification Dictionary (for ICST_DESC matching)
    print("  Loading cargo classification dictionary...")
    df_cargo_class = pd.read_csv(dict_path / "usace_cargoclass.csv", dtype=str)
    cargo_class_lookup = {}
    for _, row in df_cargo_class.iterrows():
        icst_type = str(row['icst type']).strip().upper()
        cargo_class_lookup[icst_type] = {
            'Group': str(row.get('Group', '')).strip(),
            'Commodity': str(row.get('Commodity', '')).strip()
        }
    print(f"    Loaded {len(cargo_class_lookup)} cargo classifications")
    print()

    # Read data
    print(f"Reading: {input_file.name}")

    if test_mode:
        df = pd.read_csv(input_file, nrows=15000)
        print(f"  TEST MODE: Loaded first 15,000 rows")
    else:
        df = pd.read_csv(input_file)
        print(f"  Loaded {len(df):,} rows")

    print(f"  Original columns: {len(df.columns)}")
    print()

    # Convert numeric code columns to clean text (no decimals, preserve zeros)
    print("Converting numeric codes to text format...")

    code_columns = ['PORT', 'WHERE_PORT', 'WHERE_SCHEDK', 'NRT', 'GRT', 'IMO']

    for col in code_columns:
        if col in df.columns:
            # Convert to string, remove .0 decimals, handle NaN
            df[col] = df[col].apply(lambda x: str(int(x)) if pd.notna(x) and x != '' else '')

    print(f"  Converted {len(code_columns)} code columns to text")
    print()

    # TRANSFORMATIONS
    print("Applying transformations...")
    print()

    # 1. TYPEDOC: 0->Imports, 1->Exports
    print("  [1] TYPEDOC: 0->Imports, 1->Exports")
    df['TYPEDOC'] = df['TYPEDOC'].replace({0: 'Imports', 1: 'Exports', '0': 'Imports', '1': 'Exports'})
    print(f"      Values: {df['TYPEDOC'].value_counts().to_dict()}")

    # 2. PWW_IND: P->Port, W->Waterway
    print("  [2] PWW_IND: P->Port, W->Waterway")
    df['PWW_IND'] = df['PWW_IND'].replace({'P': 'Port', 'W': 'Waterway'})
    print(f"      Values: {df['PWW_IND'].value_counts().to_dict()}")

    # 3. WHERE_IND: F->Foreign, D->Coastwise
    print("  [3] WHERE_IND: F->Foreign, D->Coastwise")
    df['WHERE_IND'] = df['WHERE_IND'].replace({'F': 'Foreign', 'D': 'Coastwise'})
    print(f"      Values: {df['WHERE_IND'].value_counts().to_dict()}")

    print()

    # PORT DICTIONARY MAPPING (using USACE waterway codes)
    print("Mapping ports to USACE waterway codes...")
    print()

    # Map Clearance Port (PORT column)
    print("  Mapping Clearance Port (PORT)...")
    df['US_Port_USACE'] = df['PORT'].apply(
        lambda x: usace_port_lookup.get(str(x), '') if pd.notna(x) and x != '' else ''
    )
    matched_clearance = len(df[df['US_Port_USACE'] != ''])
    print(f"    Matched: {matched_clearance}/{len(df)} ({matched_clearance/len(df)*100:.1f}%)")

    # Map Previous Port - Domestic (WHERE_PORT when WHERE_IND = Coastwise)
    print("  Mapping Previous Port - Domestic (WHERE_PORT)...")
    df['Previous_US_Port_USACE'] = df['WHERE_PORT'].apply(
        lambda x: usace_port_lookup.get(str(x), '') if pd.notna(x) and x != '' else ''
    )
    matched_prev_us = len(df[df['Previous_US_Port_USACE'] != ''])
    print(f"    Matched: {matched_prev_us}/{len(df)} ({matched_prev_us/len(df)*100:.1f}%)")

    # Map Previous Port - Foreign (WHERE_SCHEDK when WHERE_IND = Foreign)
    print("  Mapping Previous Port - Foreign (WHERE_SCHEDK)...")
    df['Previous_Foreign_Port'] = df['WHERE_SCHEDK'].apply(
        lambda x: foreign_port_lookup.get(str(x), {}).get('Foreign_Port', '') if pd.notna(x) and x != '' else ''
    )
    df['Previous_Foreign_Country'] = df['WHERE_SCHEDK'].apply(
        lambda x: foreign_port_lookup.get(str(x), {}).get('Foreign_Country', '') if pd.notna(x) and x != '' else ''
    )
    matched_foreign = len(df[df['Previous_Foreign_Port'] != ''])
    print(f"    Matched: {matched_foreign}/{len(df)} ({matched_foreign/len(df)*100:.1f}%)")

    print()

    # VESSEL MATCHING (add vessel specifications from ships register)
    print("Matching vessels to ships register...")

    # Initialize vessel spec columns
    df['Vessel_Type'] = ''
    df['Vessel_DWT'] = ''
    df['Vessel_Grain'] = ''
    df['Vessel_TPC'] = ''
    df['Vessel_Dwt_Draft_m'] = ''
    df['Vessel_Dwt_Draft_ft'] = ''
    df['Vessel_Match_Method'] = ''  # Track how vessel was matched

    matched_imo = 0
    matched_name = 0
    unmatched = 0

    for idx, row in df.iterrows():
        imo = str(row['IMO']).strip()
        vessel_name = str(row['VESSNAME']).strip()

        # Try IMO match first
        if imo and imo != '' and imo != 'nan' and imo in imo_lookup:
            vessel_data = imo_lookup[imo]
            df.at[idx, 'Vessel_Type'] = vessel_data['Type']
            df.at[idx, 'Vessel_DWT'] = vessel_data['DWT']
            df.at[idx, 'Vessel_Grain'] = vessel_data['Grain']
            df.at[idx, 'Vessel_TPC'] = vessel_data['TPC']
            df.at[idx, 'Vessel_Dwt_Draft_m'] = vessel_data['Dwt_Draft_m']

            # Convert meters to feet (1m = 3.28084 ft)
            draft_m = vessel_data['Dwt_Draft_m']
            if draft_m and draft_m != '' and draft_m != '0':
                try:
                    draft_ft = float(draft_m) * 3.28084
                    df.at[idx, 'Vessel_Dwt_Draft_ft'] = f"{draft_ft:.2f}"
                except:
                    df.at[idx, 'Vessel_Dwt_Draft_ft'] = ''

            df.at[idx, 'Vessel_Match_Method'] = 'IMO'
            matched_imo += 1

        # Try vessel name match if no IMO match
        elif vessel_name and vessel_name != '':
            normalized = normalize_vessel_name(vessel_name)
            if normalized and normalized in vessel_lookup:
                vessel_data = vessel_lookup[normalized]
                df.at[idx, 'Vessel_Type'] = vessel_data['Type']
                df.at[idx, 'Vessel_DWT'] = vessel_data['DWT']
                df.at[idx, 'Vessel_Grain'] = vessel_data['Grain']
                df.at[idx, 'Vessel_TPC'] = vessel_data['TPC']
                df.at[idx, 'Vessel_Dwt_Draft_m'] = vessel_data['Dwt_Draft_m']

                # Convert meters to feet
                draft_m = vessel_data['Dwt_Draft_m']
                if draft_m and draft_m != '' and draft_m != '0':
                    try:
                        draft_ft = float(draft_m) * 3.28084
                        df.at[idx, 'Vessel_Dwt_Draft_ft'] = f"{draft_ft:.2f}"
                    except:
                        df.at[idx, 'Vessel_Dwt_Draft_ft'] = ''

                df.at[idx, 'Vessel_Match_Method'] = 'Name'
                matched_name += 1
            else:
                unmatched += 1
        else:
            unmatched += 1

    print(f"  Matched by IMO:   {matched_imo:,} ({matched_imo/len(df)*100:.1f}%)")
    print(f"  Matched by Name:  {matched_name:,} ({matched_name/len(df)*100:.1f}%)")
    print(f"  Total Matched:    {matched_imo + matched_name:,} ({(matched_imo + matched_name)/len(df)*100:.1f}%)")
    print(f"  Unmatched:        {unmatched:,} ({unmatched/len(df)*100:.1f}%)")

    print()

    # CALCULATE DRAFT PERCENTAGE AND FORECASTED ACTIVITY
    print("Calculating draft percentage and forecasted activity...")

    df['Draft_Pct_of_Max'] = ''
    df['Forecasted_Activity'] = ''

    draft_calcs = 0
    for idx, row in df.iterrows():
        try:
            # Get actual draft (feet + inches/12)
            draft_ft = float(row['DRAFT_FT']) if pd.notna(row['DRAFT_FT']) and row['DRAFT_FT'] != '' else 0
            draft_in = float(row['DRAFT_IN']) if pd.notna(row['DRAFT_IN']) and row['DRAFT_IN'] != '' else 0
            actual_draft = draft_ft + (draft_in / 12.0)

            # Get max draft from vessel specs
            max_draft_str = row['Vessel_Dwt_Draft_ft']
            if max_draft_str and max_draft_str != '':
                max_draft = float(max_draft_str)

                if max_draft > 0 and actual_draft > 0:
                    # Calculate percentage
                    draft_pct = (actual_draft / max_draft) * 100
                    df.at[idx, 'Draft_Pct_of_Max'] = f"{draft_pct:.1f}"

                    # Forecast activity based on draft
                    if draft_pct > 50:
                        df.at[idx, 'Forecasted_Activity'] = 'Discharge'
                    else:
                        df.at[idx, 'Forecasted_Activity'] = 'Load'

                    draft_calcs += 1
        except:
            # Skip if any conversion fails
            pass

    print(f"  Calculated draft % and forecast for {draft_calcs:,} vessels ({draft_calcs/len(df)*100:.1f}%)")
    print()

    # CARGO CLASSIFICATION (match ICST_DESC to cargo class dictionary)
    print("Matching cargo classification from ICST type...")

    df['Group'] = ''
    df['Commodity'] = ''

    cargo_matched = 0
    for idx, row in df.iterrows():
        icst_desc = str(row['ICST_DESC']).strip().upper()
        if icst_desc and icst_desc != '' and icst_desc in cargo_class_lookup:
            cargo_data = cargo_class_lookup[icst_desc]
            df.at[idx, 'Group'] = cargo_data['Group']
            df.at[idx, 'Commodity'] = cargo_data['Commodity']
            cargo_matched += 1

    print(f"  Matched {cargo_matched:,} records to cargo classification ({cargo_matched/len(df)*100:.1f}%)")
    print()

    # ADD COUNT AND RECID COLUMNS
    print("Adding Count and RECID columns...")
    df['Count'] = 1
    df['RECID'] = range(1, len(df) + 1)
    print("  Count column added (all values = 1)")
    print(f"  RECID column added (sequential 1 to {len(df):,})")
    print()

    # COLUMN RENAMING
    print("Renaming columns...")
    rename_map = {
        'ECDATE': 'Clearance_Date',
        'PORT_NAME': 'Clearance_Port_Name',
        'VESSNAME': 'Vessel'
    }

    df.rename(columns=rename_map, inplace=True)

    for old, new in rename_map.items():
        print(f"  {old:20s} -> {new}")

    print()

    # COLUMN SELECTION
    print("Selecting columns to retain...")

    columns_to_keep = [
        # Core identification
        'RECID',
        'Count',
        'TYPEDOC',
        'Clearance_Date',  # was ECDATE

        # Clearance Port (US)
        'PORT',
        'Clearance_Port_Name',  # was PORT_NAME
        'US_Port_USACE',  # mapped from USACE waterway codes
        'PWW_IND',

        # Vessel
        'Vessel',  # was VESSNAME
        'IMO',
        'RIG_DESC',
        'ICST_DESC',
        'FLAG_CTRY',
        'NRT',
        'GRT',
        'DRAFT_FT',
        'DRAFT_IN',
        'CONTAINER',

        # Vessel Specifications (from ships register)
        'Vessel_Type',
        'Vessel_DWT',
        'Vessel_Grain',
        'Vessel_TPC',
        'Vessel_Dwt_Draft_m',
        'Vessel_Dwt_Draft_ft',
        'Vessel_Match_Method',

        # Draft Analysis
        'Draft_Pct_of_Max',
        'Forecasted_Activity',

        # Previous Port
        'WHERE_IND',
        'WHERE_PORT',  # domestic code
        'Previous_US_Port_USACE',  # mapped domestic name
        'WHERE_SCHEDK',  # foreign code
        'Previous_Foreign_Port',  # mapped foreign name
        'Previous_Foreign_Country',  # mapped foreign country
        'WHERE_NAME',  # original name from source
        'WHERE_CTRY',  # original country from source

        # Cargo Classification (from ICST type)
        'Group',
        'Commodity'
    ]

    df_final = df[columns_to_keep]

    print(f"  Retained {len(columns_to_keep)} columns")
    print(f"  Includes RECID (unique ID) and Count (for statistics)")
    print(f"  Includes 3 mapped USACE port code columns")
    print(f"  Includes 7 vessel specification columns (Type, DWT, Grain, TPC, Dwt_Draft_m, Dwt_Draft_ft, Match_Method)")
    print(f"  Includes 2 draft analysis columns (Draft_Pct_of_Max, Forecasted_Activity)")
    print(f"  Includes 2 cargo classification columns (Group, Commodity from ICST type)")
    print(f"  Dropped {len(df.columns) - len(columns_to_keep)} columns")
    print()

    # SUMMARY STATISTICS
    print("=" * 80)
    print("TRANSFORMATION SUMMARY")
    print("=" * 80)
    print()
    print(f"Total Records:        {len(df_final):,}")
    print(f"Total Columns:        {len(df_final.columns)}")
    print()

    print("Value Distributions:")
    print(f"  TYPEDOC:            {dict(df_final['TYPEDOC'].value_counts())}")
    print(f"  PWW_IND:            {dict(df_final['PWW_IND'].value_counts())}")
    print(f"  WHERE_IND:          {dict(df_final['WHERE_IND'].value_counts())}")
    print()

    print("Port Mapping Success Rates:")
    clearance_mapped = len(df_final[df_final['US_Port_USACE'] != ''])
    prev_us_mapped = len(df_final[df_final['Previous_US_Port_USACE'] != ''])
    prev_foreign_mapped = len(df_final[df_final['Previous_Foreign_Port'] != ''])
    print(f"  Clearance Port (USACE):      {clearance_mapped:,} / {len(df_final):,} ({clearance_mapped/len(df_final)*100:.1f}%)")
    print(f"  Previous US Port (USACE):    {prev_us_mapped:,} / {len(df_final):,} ({prev_us_mapped/len(df_final)*100:.1f}%)")
    print(f"  Previous Foreign Port:       {prev_foreign_mapped:,} / {len(df_final):,} ({prev_foreign_mapped/len(df_final)*100:.1f}%)")
    print()

    print("Vessel Matching Success Rates:")
    vessel_matched_imo = len(df_final[df_final['Vessel_Match_Method'] == 'IMO'])
    vessel_matched_name = len(df_final[df_final['Vessel_Match_Method'] == 'Name'])
    vessel_matched_total = vessel_matched_imo + vessel_matched_name
    print(f"  Matched by IMO:              {vessel_matched_imo:,} / {len(df_final):,} ({vessel_matched_imo/len(df_final)*100:.1f}%)")
    print(f"  Matched by Name:             {vessel_matched_name:,} / {len(df_final):,} ({vessel_matched_name/len(df_final)*100:.1f}%)")
    print(f"  Total Matched:               {vessel_matched_total:,} / {len(df_final):,} ({vessel_matched_total/len(df_final)*100:.1f}%)")
    print()

    print("Draft Analysis & Forecasted Activity:")
    draft_analyzed = len(df_final[df_final['Draft_Pct_of_Max'] != ''])
    forecast_load = len(df_final[df_final['Forecasted_Activity'] == 'Load'])
    forecast_discharge = len(df_final[df_final['Forecasted_Activity'] == 'Discharge'])
    print(f"  Draft % Calculated:          {draft_analyzed:,} / {len(df_final):,} ({draft_analyzed/len(df_final)*100:.1f}%)")
    print(f"  Forecasted Load:             {forecast_load:,} ({forecast_load/len(df_final)*100:.1f}%)")
    print(f"  Forecasted Discharge:        {forecast_discharge:,} ({forecast_discharge/len(df_final)*100:.1f}%)")
    print()

    print("Cargo Classification (from ICST type):")
    cargo_classified = len(df_final[df_final['Group'] != ''])
    print(f"  Classified:                  {cargo_classified:,} / {len(df_final):,} ({cargo_classified/len(df_final)*100:.1f}%)")
    if cargo_classified > 0:
        print(f"  Top Groups:")
        for group, count in df_final['Group'].value_counts().head(5).items():
            print(f"    {group:25s}: {count:,} ({count/len(df_final)*100:.1f}%)")
    print()

    print("Sample Records:")
    print("-" * 80)
    for idx in range(min(3, len(df_final))):
        rec = df_final.iloc[idx]
        print(f"\nRecord {idx+1} (RECID={rec['RECID']}):")
        print(f"  Vessel: {rec['Vessel']} (IMO: {rec['IMO']})")
        if rec['Vessel_Match_Method']:
            print(f"  Vessel Match: {rec['Vessel_Match_Method']} - Type: {rec['Vessel_Type']}, DWT: {rec['Vessel_DWT']}, Draft: {rec['Vessel_Dwt_Draft_m']}m ({rec['Vessel_Dwt_Draft_ft']}ft)")
        else:
            print(f"  Vessel Match: No match in ships register")
        print(f"  Clearance: {rec['Clearance_Port_Name']}")
        print(f"  Mapped:  {rec['US_Port_USACE']}")
        print(f"  Previous ({rec['WHERE_IND']}): {rec['WHERE_NAME']}")
        if rec['WHERE_IND'] == 'Coastwise':
            print(f"  Mapped:  {rec['Previous_US_Port_USACE']}")
        else:
            print(f"  Mapped:  {rec['Previous_Foreign_Port']}, {rec['Previous_Foreign_Country']}")
    print()

    # Save output
    if not test_mode:
        print(f"Saving to: {output_file.name}")
        df_final.to_csv(output_file, index=False)
        print("[OK] File saved successfully")
    else:
        print("[TEST MODE] File not saved - review results above")

    print()
    print("=" * 80)

    return df_final

def main():
    """Main execution"""

    # Paths
    INPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_raw_data\00_03_usace_entrance_clearance_raw\Entrances_Clearances_2023_2023_Outbound.csv")
    OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\02_STAGE02_CLASSIFICATION\usace_2023_outbound_clearance_transformed_v2.1.0.csv")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Run in FULL mode
    print("\n\n")
    print("#" * 80)
    print("# RUNNING FULL DATASET - All records (Outbound/Exports)")
    print("#" * 80)
    print("\n")

    df_full = transform_clearance_data(INPUT_FILE, OUTPUT_FILE, test_mode=False)

    print("\n")
    print("=" * 80)
    print("TRANSFORMATION COMPLETE")
    print("=" * 80)
    print()
    print(f"Output saved to: {OUTPUT_FILE}")
    print()
    print("Next steps:")
    print("  1. Review output file for quality")
    print("  2. Process Outbound (exports) file")
    print()

if __name__ == "__main__":
    main()
