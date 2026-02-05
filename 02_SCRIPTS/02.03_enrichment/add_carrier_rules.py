"""
Add carrier-based rules to cargo dictionary v2.0.0 -> v2.1.0
Implements carrier + HS2 shortcuts for major carriers

Author: WSD3 / Claude Code
Date: 2026-01-13
Version: 1.0.0
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# Paths
INPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.0.0_20260113_1430.csv")
OUTPUT_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.1.0_20260113_1445.csv")

def stamp(msg):
    """Print timestamped message"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def create_carrier_rules():
    """Define carrier-based classification rules"""

    carrier_rules = [
        # RORO CARRIERS (Tier 1 - Lock classification, never override)
        {
            'Rule_ID': 'CARR-WALLENIUS-RORO',
            'Phase': 2,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'TRUE',
            'Override_HS': 'FALSE',
            'Carrier_Name': 'WALLENIUS',
            'Package_Type': '',
            'HS2': '87',
            'HS4': '',
            'HS6': '',
            'Keywords': 'WALLENIUS',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Group': 'Ro/Ro',
            'Commodity': 'Vehicles',
            'Cargo': 'Motor Vehicles',
            'Cargo_Detail': 'Vehicles',
            'Filter': '',
            'Note': 'Carrier lock - WALLENIUS always RoRo vehicles',
            'Accuracy_Est': '100%',
            'Tonnage_Impact': 'Very High',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        },
        {
            'Rule_ID': 'CARR-WWL-RORO',
            'Phase': 2,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'TRUE',
            'Override_HS': 'FALSE',
            'Carrier_Name': 'WWL',
            'Package_Type': '',
            'HS2': '87',
            'HS4': '',
            'HS6': '',
            'Keywords': 'WWL;WALLENIUS WILHELMSEN',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Group': 'Ro/Ro',
            'Commodity': 'Vehicles',
            'Cargo': 'Motor Vehicles',
            'Cargo_Detail': 'Vehicles',
            'Filter': '',
            'Note': 'Carrier lock - WWL always RoRo vehicles',
            'Accuracy_Est': '100%',
            'Tonnage_Impact': 'Very High',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        },
        {
            'Rule_ID': 'CARR-HOEGH-RORO',
            'Phase': 2,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'TRUE',
            'Override_HS': 'FALSE',
            'Carrier_Name': 'HOEGH',
            'Package_Type': '',
            'HS2': '87',
            'HS4': '',
            'HS6': '',
            'Keywords': 'HOEGH;HÖEGH',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Group': 'Ro/Ro',
            'Commodity': 'Vehicles',
            'Cargo': 'Motor Vehicles',
            'Cargo_Detail': 'Vehicles',
            'Filter': '',
            'Note': 'Carrier lock - HOEGH always RoRo vehicles',
            'Accuracy_Est': '100%',
            'Tonnage_Impact': 'Very High',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        },
        {
            'Rule_ID': 'CARR-EUKOR-RORO',
            'Phase': 2,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'TRUE',
            'Override_HS': 'FALSE',
            'Carrier_Name': 'EUKOR',
            'Package_Type': '',
            'HS2': '87',
            'HS4': '',
            'HS6': '',
            'Keywords': 'EUKOR',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Group': 'Ro/Ro',
            'Commodity': 'Vehicles',
            'Cargo': 'Motor Vehicles',
            'Cargo_Detail': 'Vehicles',
            'Filter': '',
            'Note': 'Carrier lock - EUKOR always RoRo vehicles',
            'Accuracy_Est': '100%',
            'Tonnage_Impact': 'High',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        },

        # CHEMICAL CARRIERS (Tier 1 - Lock classification)
        {
            'Rule_ID': 'CARR-STOLT-CHEM',
            'Phase': 2,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'TRUE',
            'Override_HS': 'FALSE',
            'Carrier_Name': 'STOLT',
            'Package_Type': '',
            'HS2': '28;29',
            'HS4': '',
            'HS6': '',
            'Keywords': 'STOLT',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Group': 'Liquid Bulk',
            'Commodity': 'Chemicals',
            'Cargo': 'Chemicals',
            'Cargo_Detail': 'Chemicals',
            'Filter': '',
            'Note': 'Carrier lock - STOLT always liquid bulk chemicals',
            'Accuracy_Est': '100%',
            'Tonnage_Impact': 'Very High',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        },
        {
            'Rule_ID': 'CARR-ODFJELL-CHEM',
            'Phase': 2,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'TRUE',
            'Override_HS': 'FALSE',
            'Carrier_Name': 'ODFJELL',
            'Package_Type': '',
            'HS2': '28;29',
            'HS4': '',
            'HS6': '',
            'Keywords': 'ODFJELL',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Group': 'Liquid Bulk',
            'Commodity': 'Chemicals',
            'Cargo': 'Chemicals',
            'Cargo_Detail': 'Chemicals',
            'Filter': '',
            'Note': 'Carrier lock - ODFJELL always liquid bulk chemicals',
            'Accuracy_Est': '100%',
            'Tonnage_Impact': 'High',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        },

        # REEFER CARRIERS (Tier 1 - Lock classification)
        {
            'Rule_ID': 'CARR-COOLCARRIERS-REEF',
            'Phase': 2,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'TRUE',
            'Override_HS': 'FALSE',
            'Carrier_Name': 'COOL CARRIERS',
            'Package_Type': '',
            'HS2': '08;20',
            'HS4': '',
            'HS6': '',
            'Keywords': 'COOL CARRIERS',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Group': 'Reefer',
            'Commodity': 'Refrigerated Products',
            'Cargo': 'Refrigerated Cargo',
            'Cargo_Detail': 'Refrigerated Products',
            'Filter': '',
            'Note': 'Carrier lock - COOL CARRIERS always reefer',
            'Accuracy_Est': '100%',
            'Tonnage_Impact': 'High',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        },
        {
            'Rule_ID': 'CARR-SEATRADE-REEF',
            'Phase': 2,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'TRUE',
            'Override_HS': 'FALSE',
            'Carrier_Name': 'SEATRADE',
            'Package_Type': '',
            'HS2': '08;20',
            'HS4': '',
            'HS6': '',
            'Keywords': 'SEATRADE',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Group': 'Reefer',
            'Commodity': 'Refrigerated Products',
            'Cargo': 'Refrigerated Cargo',
            'Cargo_Detail': 'Refrigerated Products',
            'Filter': '',
            'Note': 'Carrier lock - SEATRADE always reefer',
            'Accuracy_Est': '100%',
            'Tonnage_Impact': 'Medium',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        },
        {
            'Rule_ID': 'CARR-DOLE-REEF',
            'Phase': 2,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'TRUE',
            'Override_HS': 'FALSE',
            'Carrier_Name': 'DOLE',
            'Package_Type': '',
            'HS2': '08',
            'HS4': '',
            'HS6': '',
            'Keywords': 'DOLE',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Group': 'Reefer',
            'Commodity': 'Agricultural Products',
            'Cargo': 'Fresh Fruit',
            'Cargo_Detail': 'Fresh Fruit',
            'Filter': '',
            'Note': 'Carrier lock - DOLE always fruit reefer',
            'Accuracy_Est': '100%',
            'Tonnage_Impact': 'Medium',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        },

        # STEEL CARRIERS (Tier 1 but allow refinement - user's suggestion)
        {
            'Rule_ID': 'CARR-NYK-STEEL',
            'Phase': 2,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'FALSE',
            'Override_HS': 'TRUE',
            'Carrier_Name': 'NYK',
            'Package_Type': '',
            'HS2': '72;73',
            'HS4': '',
            'HS6': '',
            'Keywords': 'NYK',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Group': 'Break-Bulk',
            'Commodity': 'Metals & Minerals',
            'Cargo': 'Steel',
            'Cargo_Detail': 'Steel Products',
            'Filter': '',
            'Note': 'Carrier + HS2 72/73 = Steel (90% accurate, allow Phase 6 refinement)',
            'Accuracy_Est': '90%',
            'Tonnage_Impact': 'Very High',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        },
        {
            'Rule_ID': 'CARR-MOL-STEEL',
            'Phase': 2,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'FALSE',
            'Override_HS': 'TRUE',
            'Carrier_Name': 'MOL',
            'Package_Type': '',
            'HS2': '72;73',
            'HS4': '',
            'HS6': '',
            'Keywords': 'MOL',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Group': 'Break-Bulk',
            'Commodity': 'Metals & Minerals',
            'Cargo': 'Steel',
            'Cargo_Detail': 'Steel Products',
            'Filter': '',
            'Note': 'Carrier + HS2 72/73 = Steel (90% accurate, allow Phase 6 refinement)',
            'Accuracy_Est': '90%',
            'Tonnage_Impact': 'Very High',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        },
        {
            'Rule_ID': 'CARR-KLINE-STEEL',
            'Phase': 2,
            'Tier': 1,
            'Active': 'TRUE',
            'Lock_Classification': 'FALSE',
            'Override_HS': 'TRUE',
            'Carrier_Name': 'K LINE',
            'Package_Type': '',
            'HS2': '72;73',
            'HS4': '',
            'HS6': '',
            'Keywords': 'K LINE',
            'Exclude_Keywords': '',
            'Min_Tons': '',
            'Max_Tons': '',
            'Port_Filter': '',
            'Country_Filter': '',
            'Group': 'Break-Bulk',
            'Commodity': 'Metals & Minerals',
            'Cargo': 'Steel',
            'Cargo_Detail': 'Steel Products',
            'Filter': '',
            'Note': 'Carrier + HS2 72/73 = Steel (90% accurate, allow Phase 6 refinement)',
            'Accuracy_Est': '90%',
            'Tonnage_Impact': 'High',
            'Date_Added': '2026-01-13',
            'Last_Modified': '2026-01-13'
        }
    ]

    return carrier_rules

def add_carrier_rules():
    """Add carrier rules to dictionary"""

    stamp("=== Adding Carrier Rules to Dictionary v2.0.0 -> v2.1.0 ===")

    # Read existing dictionary
    stamp(f"Reading dictionary: {INPUT_DICT}")
    df_existing = pd.read_csv(INPUT_DICT, dtype=str)
    stamp(f"Loaded {len(df_existing)} existing rules")

    # Create carrier rules
    stamp("\nCreating carrier-based rules...")
    carrier_rules = create_carrier_rules()
    df_carriers = pd.DataFrame(carrier_rules)
    stamp(f"Created {len(df_carriers)} carrier rules")

    # Display carrier rules summary
    stamp("\nCarrier Rules Summary:")
    stamp(f"  RoRo Carriers: {len(df_carriers[df_carriers['Group'] == 'Ro/Ro'])} rules")
    stamp(f"  Chemical Carriers: {len(df_carriers[df_carriers['Commodity'] == 'Chemicals'])} rules")
    stamp(f"  Reefer Carriers: {len(df_carriers[df_carriers['Group'] == 'Reefer'])} rules")
    stamp(f"  Steel Carriers: {len(df_carriers[df_carriers['Cargo'] == 'Steel'])} rules")

    # Combine
    df_combined = pd.concat([df_carriers, df_existing], ignore_index=True)
    stamp(f"\nTotal rules after merge: {len(df_combined)}")

    # Save new version
    stamp(f"\nSaving v2.1.0: {OUTPUT_DICT}")
    df_combined.to_csv(OUTPUT_DICT, index=False)

    # Final statistics
    stamp("\n=== Dictionary v2.1.0 Statistics ===")
    stamp(f"Total rules: {len(df_combined)}")
    stamp(f"\nRules by Phase:")
    for phase in sorted(df_combined['Phase'].astype(int).unique()):
        count = len(df_combined[df_combined['Phase'].astype(int) == phase])
        stamp(f"  Phase {phase}: {count} rules")

    stamp(f"\nRules by Tier:")
    tier_names = {1: 'Carrier Locks', 2: 'Package Types', 3: 'HS+Keywords',
                  4: 'Tonnage Override', 5: 'Specific Grades'}
    for tier in sorted(df_combined['Tier'].astype(int).unique()):
        count = len(df_combined[df_combined['Tier'].astype(int) == tier])
        stamp(f"  Tier {tier} ({tier_names.get(tier, 'Unknown')}): {count} rules")

    stamp("\nDictionary v2.1.0 created successfully!")
    stamp(f"New file: {OUTPUT_DICT}")

    return df_combined

if __name__ == "__main__":
    df = add_carrier_rules()
