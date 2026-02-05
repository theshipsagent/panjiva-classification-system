"""
Debug carrier SCAC matching and identify specialty carriers

1. Check actual carrier format vs dictionary format
2. Test matching logic
3. Identify small specialty carriers (<1000 tons/year)
"""

import pandas as pd
from pathlib import Path

# Paths
SAMPLE = Path(r"G:\My Drive\LLM\project_manifest\03_DOCUMENTATION/03.04_summaries\sample_test_15k\sample_15k_classified.csv")
DICTIONARY = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.3.0_20260113_1545.csv")

def stamp(msg):
    print(msg)

# Load data
stamp("=== Loading Data ===")
df_sample = pd.read_csv(SAMPLE, dtype=str)
df_dict = pd.read_csv(DICTIONARY, dtype=str)

# Get carrier rules from dictionary
carrier_rules = df_dict[df_dict['Carrier_SCAC'].notna() & (df_dict['Carrier_SCAC'] != '')]

stamp(f"\n=== DICTIONARY CARRIER RULES ({len(carrier_rules)}) ===")
for _, rule in carrier_rules.iterrows():
    stamp(f"SCAC: {rule['Carrier_SCAC']:6s} - Name: {rule['Carrier_Name'][:50]}")

# Check actual carrier format in sample
stamp("\n=== TOP 20 CARRIERS IN SAMPLE (with SCAC extraction) ===")
carrier_counts = df_sample['Carrier'].value_counts().head(20)

for carrier, count in carrier_counts.items():
    # Extract SCAC (first 4 chars before " - ")
    scac = ''
    if ' - ' in str(carrier):
        scac = str(carrier).split(' - ')[0].strip()

    # Check if in dictionary
    in_dict = scac in carrier_rules['Carrier_SCAC'].values
    marker = 'DICT' if in_dict else '    '

    stamp(f"{count:5d} [{marker}] SCAC: {scac:6s} - {carrier[:60]}")

# Test SCAC matching logic
stamp("\n=== TESTING SCAC MATCHING LOGIC ===")

# Get a WLWH record
wlwh_records = df_sample[df_sample['Carrier'].str.contains('WLWH', na=False)]
if len(wlwh_records) > 0:
    test_record = wlwh_records.iloc[0]
    stamp(f"\nTest Record Carrier: {test_record['Carrier']}")

    # Get WLWH rule from dictionary
    wlwh_rule = carrier_rules[carrier_rules['Carrier_SCAC'] == 'WLWH'].iloc[0]
    stamp(f"Dictionary SCAC: {wlwh_rule['Carrier_SCAC']}")

    # Test matching
    record_carrier = str(test_record['Carrier']).upper()
    rule_scac = str(wlwh_rule['Carrier_SCAC']).upper()

    stamp(f"\nMatching test:")
    stamp(f"  Rule SCAC: '{rule_scac}'")
    stamp(f"  Record Carrier (upper): '{record_carrier}'")
    stamp(f"  SCAC in Carrier? {rule_scac in record_carrier}")

    # The issue is likely here - checking if "WLWH" is in "WLWH - Wallenius..."
    # This SHOULD work, so the issue might be elsewhere

# Identify specialty carriers
stamp("\n=== SPECIALTY CARRIER ANALYSIS ===")
stamp("Carriers with <1000 total tons in 15k sample:\n")

# Calculate total tonnage per carrier
df_sample['Tons_Numeric'] = pd.to_numeric(df_sample['Tons'].str.replace(',', ''), errors='coerce').fillna(0)
carrier_tonnage = df_sample.groupby('Carrier').agg({
    'Tons_Numeric': 'sum',
    'Carrier': 'count'
}).rename(columns={'Carrier': 'Record_Count'})

# Filter to <1000 tons
small_carriers = carrier_tonnage[carrier_tonnage['Tons_Numeric'] < 1000].sort_values('Tons_Numeric', ascending=False)

stamp(f"Found {len(small_carriers)} carriers with <1000 total tons")
stamp("\nTop 30 Small Specialty Carriers:")
stamp(f"{'Carrier':<60s} {'Records':>8s} {'Total Tons':>12s}")
stamp("-" * 85)

for carrier, row in small_carriers.head(30).iterrows():
    stamp(f"{str(carrier)[:60]:<60s} {int(row['Record_Count']):8d} {row['Tons_Numeric']:12.2f}")

# Identify vessel type patterns for small carriers
stamp("\n=== VESSEL TYPE PATTERNS (Small Carriers) ===")
small_carrier_names = small_carriers.index.tolist()
small_carrier_records = df_sample[df_sample['Carrier'].isin(small_carrier_names)]

if 'Vessel_Type_Simple' in small_carrier_records.columns:
    vtype_dist = small_carrier_records['Vessel_Type_Simple'].value_counts()
    stamp("\nVessel Type Distribution:")
    for vtype, count in vtype_dist.items():
        stamp(f"  {vtype:20s}: {count:5d}")

# Identify keywords in small carrier names
stamp("\n=== SPECIALTY CARRIER KEYWORDS ===")
keywords = {
    'YACHT': 0, 'TOW': 0, 'TUG': 0, 'FERRY': 0, 'RESEARCH': 0,
    'OFFSHORE': 0, 'SUPPLY': 0, 'CREW': 0, 'SERVICE': 0, 'PILOT': 0,
    'SALVAGE': 0, 'DREDGE': 0, 'BARGE': 0, 'SURVEY': 0, 'PATROL': 0
}

for carrier in small_carrier_names:
    carrier_upper = str(carrier).upper()
    for keyword in keywords.keys():
        if keyword in carrier_upper:
            keywords[keyword] += 1

stamp("\nKeyword occurrences in small carriers:")
for keyword, count in sorted(keywords.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        stamp(f"  {keyword:15s}: {count:3d}")

# Save specialty carrier list
specialty_carriers_df = small_carriers.copy()
specialty_carriers_df['Carrier_Name'] = specialty_carriers_df.index
output_file = Path(r"G:\My Drive\LLM\project_manifest\03_DOCUMENTATION/03.04_summaries\sample_test_15k\specialty_carriers_identified.csv")
specialty_carriers_df.to_csv(output_file, index=False)
stamp(f"\nSpecialty carriers saved: {output_file}")
