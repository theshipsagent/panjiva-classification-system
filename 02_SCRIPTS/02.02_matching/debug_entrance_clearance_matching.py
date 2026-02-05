"""
Debug Entrance-Clearance Matching Issue
Version: 1.0.0
Date: 2026-01-15

Purpose:
- Investigate why marry_entrance_clearance_v1.0.0.py produces zero matches
- Check data types for IMO, PORT, dates
- Test matching conditions step by step
- Find specific examples that should match
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

print("="*80)
print("DEBUG ENTRANCE-CLEARANCE MATCHING v1.0.0")
print("="*80)

# File paths
ENTRANCE_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_entrance_with_panjiva_match_v1.3.1.csv")
CLEARANCE_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_clearance_with_panjiva_match_v1.0.1.csv")

# Parse USACE dates (mmydd format)
def parse_usace_date(date_val):
    """Convert mmydd integer to timestamp (e.g., 8329 -> 2023-08-29)"""
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
print("\n1. Loading data...")
entrance = pd.read_csv(ENTRANCE_FILE, low_memory=False)
clearance = pd.read_csv(CLEARANCE_FILE, low_memory=False)
print(f"   Entrance: {len(entrance):,} records")
print(f"   Clearance: {len(clearance):,} records")

# Parse dates
print("\n2. Parsing dates...")
entrance['Arrival_Date_Parsed'] = pd.to_datetime(entrance['Arrival_Date'], errors='coerce')
clearance['Clearance_Date_Parsed'] = clearance['Clearance_Date'].apply(parse_usace_date)
print(f"   Entrance dates parsed: {entrance['Arrival_Date_Parsed'].notna().sum():,}")
print(f"   Clearance dates parsed: {clearance['Clearance_Date_Parsed'].notna().sum():,}")

# Check data types
print("\n3. Checking data types...")
print(f"   Entrance IMO type: {entrance['IMO'].dtype}")
print(f"   Clearance IMO type: {clearance['IMO'].dtype}")
print(f"   Entrance PORT type: {entrance['PORT'].dtype}")
print(f"   Clearance PORT type: {clearance['PORT'].dtype}")
print(f"   Entrance Arrival_Date_Parsed type: {entrance['Arrival_Date_Parsed'].dtype}")
print(f"   Clearance Clearance_Date_Parsed type: {clearance['Clearance_Date_Parsed'].dtype}")

# Check for NaN/null values
print("\n4. Checking for null values...")
print(f"   Entrance IMO nulls: {entrance['IMO'].isna().sum():,} ({entrance['IMO'].isna().sum()/len(entrance)*100:.1f}%)")
print(f"   Clearance IMO nulls: {clearance['IMO'].isna().sum():,} ({clearance['IMO'].isna().sum()/len(clearance)*100:.1f}%)")
print(f"   Entrance PORT nulls: {entrance['PORT'].isna().sum():,}")
print(f"   Clearance PORT nulls: {clearance['PORT'].isna().sum():,}")

# Find common IMOs
print("\n5. Finding overlaps...")
entrance_imos = set(entrance['IMO'].dropna().unique())
clearance_imos = set(clearance['IMO'].dropna().unique())
common_imos = entrance_imos & clearance_imos
print(f"   Common IMOs: {len(common_imos):,} (out of {len(entrance_imos):,} entrance IMOs)")

# Find common ports
entrance_ports = set(entrance['PORT'].dropna().astype(str).unique())
clearance_ports = set(clearance['PORT'].dropna().astype(str).unique())
common_ports = entrance_ports & clearance_ports
print(f"   Common PORTs: {len(common_ports):,} (out of {len(entrance_ports):,} entrance ports)")

# Test specific matching case
print("\n6. Testing specific matching case...")
print("   Looking for a vessel with both entrance and clearance...")

# Filter to records with valid IMO and dates
entrance_valid = entrance[
    (entrance['IMO'].notna()) &
    (entrance['Arrival_Date_Parsed'].notna())
].copy()

clearance_valid = clearance[
    (clearance['IMO'].notna()) &
    (clearance['Clearance_Date_Parsed'].notna())
].copy()

print(f"   Valid entrance records (IMO + date): {len(entrance_valid):,}")
print(f"   Valid clearance records (IMO + date): {len(clearance_valid):,}")

# Find a vessel that appears in both
if len(common_imos) > 0:
    test_imo = list(common_imos)[0]
    print(f"\n   Testing IMO: {test_imo}")

    # Get all entrance records for this IMO
    ent_records = entrance_valid[entrance_valid['IMO'] == test_imo]
    print(f"   Entrance records for this IMO: {len(ent_records)}")
    if len(ent_records) > 0:
        print(f"   Sample entrance:")
        sample_ent = ent_records.iloc[0]
        print(f"      Vessel: {sample_ent['Vessel']}")
        print(f"      PORT: {sample_ent['PORT']} (type: {type(sample_ent['PORT'])})")
        print(f"      Arrival_Date: {sample_ent['Arrival_Date']}")
        print(f"      Arrival_Date_Parsed: {sample_ent['Arrival_Date_Parsed']}")

    # Get all clearance records for this IMO
    clear_records = clearance_valid[clearance_valid['IMO'] == test_imo]
    print(f"\n   Clearance records for this IMO: {len(clear_records)}")
    if len(clear_records) > 0:
        print(f"   Sample clearance:")
        sample_clear = clear_records.iloc[0]
        print(f"      Vessel: {sample_clear['Vessel']}")
        print(f"      PORT: {sample_clear['PORT']} (type: {type(sample_clear['PORT'])})")
        print(f"      Clearance_Date: {sample_clear['Clearance_Date']}")
        print(f"      Clearance_Date_Parsed: {sample_clear['Clearance_Date_Parsed']}")

    # Test matching condition
    if len(ent_records) > 0 and len(clear_records) > 0:
        print(f"\n7. Testing matching condition for IMO {test_imo}...")

        test_entrance = ent_records.iloc[0]
        test_imo_val = test_entrance['IMO']
        test_port = test_entrance['PORT']
        test_arrival = test_entrance['Arrival_Date_Parsed']

        print(f"   Looking for clearances where:")
        print(f"      IMO == {test_imo_val}")
        print(f"      PORT == {test_port}")
        print(f"      Clearance_Date_Parsed > {test_arrival}")

        # Test each condition separately
        cond1 = clearance_valid['IMO'] == test_imo_val
        cond2 = clearance_valid['PORT'] == test_port
        cond3 = clearance_valid['Clearance_Date_Parsed'] > test_arrival

        print(f"\n   Results:")
        print(f"      Clearances with matching IMO: {cond1.sum()}")
        print(f"      Clearances with matching PORT: {cond2.sum()}")
        print(f"      Clearances after arrival date: {cond3.sum()}")
        print(f"      Clearances matching ALL conditions: {(cond1 & cond2 & cond3).sum()}")

        # Check PORT values directly
        print(f"\n   PORT comparison detail:")
        print(f"      Entrance PORT value: {test_port} (type: {type(test_port)})")
        clearance_ports_for_imo = clearance_valid[clearance_valid['IMO'] == test_imo_val]['PORT'].unique()
        print(f"      Clearance PORT values for this IMO: {clearance_ports_for_imo}")
        print(f"      PORT match check: {test_port in clearance_ports_for_imo}")

        # If we have matches, show them
        if (cond1 & cond2 & cond3).sum() > 0:
            matches = clearance_valid[cond1 & cond2 & cond3]
            print(f"\n   FOUND MATCHES! ({len(matches)} records)")
            print(matches[['Vessel', 'IMO', 'PORT', 'Clearance_Date', 'Clearance_Date_Parsed']].head())
        else:
            print(f"\n   NO MATCHES FOUND")

            # Show why no matches
            same_imo_port = clearance_valid[cond1 & cond2]
            if len(same_imo_port) > 0:
                print(f"\n   Found {len(same_imo_port)} clearances with same IMO+PORT:")
                print(f"      Entrance arrival: {test_arrival}")
                print(f"      Clearance dates:")
                for idx, row in same_imo_port.head(5).iterrows():
                    print(f"         {row['Clearance_Date_Parsed']} (diff: {(row['Clearance_Date_Parsed'] - test_arrival).days} days)")

print("\n" + "="*80)
print("DIAGNOSTIC COMPLETE")
print("="*80)
