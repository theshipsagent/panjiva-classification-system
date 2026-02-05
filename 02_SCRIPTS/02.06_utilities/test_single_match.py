"""
Test Single Vessel Match
Version: 1.0.0
Purpose: Debug why HAMBURG CITY doesn't match in marry script
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Parse USACE dates
def parse_usace_date(date_val):
    if pd.isna(date_val):
        return None
    try:
        date_str = str(int(date_val)).zfill(5)
        month = int(date_str[:2])
        year_digit = int(date_str[2])
        day = int(date_str[3:])
        year = 2020 + year_digit
        return pd.Timestamp(year=year, month=month, day=day)
    except:
        return None

# Load data
ENTRANCE_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_entrance_with_panjiva_match_v1.3.1.csv")
CLEARANCE_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_clearance_with_panjiva_match_v1.0.1.csv")

entrance = pd.read_csv(ENTRANCE_FILE, low_memory=False)
clearance = pd.read_csv(CLEARANCE_FILE, low_memory=False)

# Parse dates
entrance['Arrival_Date_Parsed'] = pd.to_datetime(entrance['Arrival_Date'], errors='coerce')
clearance['Clearance_Date_Parsed'] = clearance['Clearance_Date'].apply(parse_usace_date)

# Sort (exactly as in marry script)
entrance_sorted = entrance.sort_values(['IMO', 'PORT', 'Arrival_Date_Parsed']).reset_index(drop=True)
clearance_sorted = clearance.sort_values(['IMO', 'PORT', 'Clearance_Date_Parsed']).reset_index(drop=True)

# Find HAMBURG CITY entrance at PORT 1506
test_ent = entrance_sorted[(entrance_sorted['IMO'] == 9863170.0) & (entrance_sorted['PORT'] == 1506)]
print("HAMBURG CITY Entrance records:")
print(test_ent[['Vessel', 'IMO', 'PORT', 'Arrival_Date', 'Arrival_Date_Parsed']])
print()

if len(test_ent) > 0:
    # Get the first entrance record (as series, like iterrows returns)
    ent_row = test_ent.iloc[0]

    print("Testing matching logic (EXACT code from marry script):")
    print("="*60)

    # EXACT code from marry script lines 93-96
    vessel_imo = ent_row.get('IMO', '')
    vessel_name = ent_row.get('Vessel', '')
    port = ent_row.get('PORT', '')
    arrival_date = ent_row['Arrival_Date_Parsed']

    print(f"Extracted values:")
    print(f"  vessel_imo: {vessel_imo} (type: {type(vessel_imo)})")
    print(f"  vessel_name: {vessel_name} (type: {type(vessel_name)})")
    print(f"  port: {port} (type: {type(port)})")
    print(f"  arrival_date: {arrival_date} (type: {type(arrival_date)})")
    print()

    # Check the condition at line 116
    print(f"Condition check (line 116):")
    print(f"  pd.notna(vessel_imo): {pd.notna(vessel_imo)}")
    print(f"  str(vessel_imo).strip() != '': {str(vessel_imo).strip() != ''}")
    print(f"  Combined: {pd.notna(vessel_imo) and str(vessel_imo).strip() != ''}")
    print()

    if pd.notna(vessel_imo) and str(vessel_imo).strip() != '':
        print("Entering IMO matching block...")
        print()

        # Test each condition separately
        clearance_matched = set()  # Empty set (first iteration)

        print("Testing matching conditions:")
        cond1 = (clearance_sorted['IMO'] == vessel_imo)
        cond2 = (clearance_sorted['PORT'] == port)
        cond3 = (clearance_sorted['Clearance_Date_Parsed'] > arrival_date)
        cond4 = (~clearance_sorted.index.isin(clearance_matched))

        print(f"  Condition 1 (IMO == {vessel_imo}): {cond1.sum()} matches")
        print(f"  Condition 2 (PORT == {port}): {cond2.sum()} matches")
        print(f"  Condition 3 (Clearance_Date > {arrival_date}): {cond3.sum()} matches")
        print(f"  Condition 4 (not already matched): {cond4.sum()} matches")
        print()

        # Combined
        combined = (cond1 & cond2 & cond3 & cond4)
        print(f"  Combined (all 4 conditions): {combined.sum()} matches")
        print()

        if combined.sum() > 0:
            candidates = clearance_sorted[combined]
            print("FOUND CANDIDATES!")
            print(candidates[['Vessel', 'IMO', 'PORT', 'Clearance_Date', 'Clearance_Date_Parsed']].head())
            print()

            # Take first
            clear_match = candidates.iloc[0]
            print(f"Selected match:")
            print(f"  Vessel: {clear_match['Vessel']}")
            print(f"  IMO: {clear_match['IMO']}")
            print(f"  PORT: {clear_match['PORT']}")
            print(f"  Clearance_Date: {clear_match['Clearance_Date']}")
            print(f"  Clearance_Date_Parsed: {clear_match['Clearance_Date_Parsed']}")
            print(f"  Index (clear_match.name): {clear_match.name}")

            # Calculate port stay
            port_stay_decimal = (clear_match['Clearance_Date_Parsed'] - arrival_date).total_seconds() / (24 * 3600)
            print(f"\n  Port stay: {port_stay_decimal:.2f} days")
        else:
            print("NO MATCHES FOUND - investigating why...")
            print()

            # Check each combination
            print("Pairwise condition checks:")
            print(f"  IMO + PORT: {(cond1 & cond2).sum()}")
            print(f"  IMO + DATE: {(cond1 & cond3).sum()}")
            print(f"  PORT + DATE: {(cond2 & cond3).sum()}")
            print(f"  IMO + PORT + DATE: {(cond1 & cond2 & cond3).sum()}")
