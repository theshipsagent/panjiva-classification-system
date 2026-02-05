"""
Restructure Port Call Master - Eliminate Column Duplication
Version: 1.0.0
Date: 2026-01-16

Purpose:
- Consolidate duplicate vessel data (Entrance + Clearance have same IMO, DWT, etc)
- Create unified column structure:
  * PORTCALL_ID
  * Record_Type (ENTRANCE_ONLY, CLEARANCE_ONLY, BOTH, TUG_BARGE_PAIR)
  * Common vessel data (once)
  * Entrance-specific data
  * Clearance-specific data
  * Import cargo data
  * Export cargo data
  * Grain export data

Result: 115 columns → ~70 columns (eliminate ~45 duplicate columns)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

print("="*80)
print("RESTRUCTURE PORT CALL MASTER v1.0.0")
print("="*80)
print("\nEliminating column duplication...")

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# File paths
INPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_portcall_master_v1.2.0.csv")
OUTPUT_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_portcall_master_v1.3.0_restructured.csv")

# Load
print("\n1. Loading Port Call Master v1.2.0...")
df = pd.read_csv(INPUT_FILE, low_memory=False)
print(f"   Records: {len(df):,}")
print(f"   Columns (original): {len(df.columns)}")

# Create restructured dataframe
print("\n2. Restructuring columns...")

restructured = pd.DataFrame()

# ============================================================================
# CORE IDENTIFIERS
# ============================================================================
restructured['PORTCALL_ID'] = df['PORTCALL_ID']
restructured['Record_Type'] = df['Match_Type']  # BOTH, ENTRANCE_ONLY, CLEARANCE_ONLY, TUG_BARGE_PAIR

# ============================================================================
# VESSEL DATA (COMMON - from entrance as primary, clearance as fallback)
# ============================================================================
print("   Consolidating vessel data...")
restructured['Vessel_Name'] = df['Entrance_Vessel'].fillna(df['Clearance_Vessel'])
restructured['IMO'] = df['Entrance_IMO'].fillna(df['Clearance_IMO'])
restructured['Flag_Country'] = df['Entrance_FLAG_CTRY'].fillna(df['Clearance_FLAG_CTRY'])
restructured['ICST_Vessel_Type'] = df['Entrance_ICST_DESC'].fillna(df['Clearance_ICST_DESC'])
restructured['Rig_Description'] = df['Entrance_RIG_DESC'].fillna(df['Clearance_RIG_DESC'])

# Ship Registry Data (from entrance, fallback to clearance)
restructured['Vessel_Type_Registry'] = df['Entrance_Vessel_Type'].fillna(df['Clearance_Vessel_Type'])
restructured['DWT'] = df['Entrance_Vessel_DWT'].fillna(df['Clearance_Vessel_DWT'])
restructured['NRT'] = df['Entrance_NRT'].fillna(df['Clearance_NRT'])
restructured['GRT'] = df['Entrance_GRT'].fillna(df['Clearance_GRT'])
restructured['Grain_Capacity_m3'] = df['Entrance_Vessel_Grain'].fillna(df['Clearance_Vessel_Grain'])
restructured['TPC'] = df['Entrance_Vessel_TPC'].fillna(df['Clearance_Vessel_TPC'])
restructured['DWT_Draft_m'] = df['Entrance_Vessel_Dwt_Draft_m'].fillna(df['Clearance_Vessel_Dwt_Draft_m'])
restructured['DWT_Draft_ft'] = df['Entrance_Vessel_Dwt_Draft_ft'].fillna(df['Clearance_Vessel_Dwt_Draft_ft'])
restructured['Registry_Match_Method'] = df['Entrance_Vessel_Match_Method'].fillna(df['Clearance_Vessel_Match_Method'])

# ============================================================================
# PORT CALL TIMELINE
# ============================================================================
print("   Adding timeline data...")
restructured['Arrival_Date'] = df['Entrance_Arrival_Date']
restructured['Clearance_Date'] = df['Clearance_Clearance_Date_Parsed']
restructured['Port_Stay_Days'] = df['Port_Stay_Days_Decimal']

# ============================================================================
# ENTRANCE DATA (ARRIVAL-SPECIFIC)
# ============================================================================
print("   Adding entrance-specific data...")
restructured['Entrance_RECID'] = df['Entrance_RECID']
restructured['Entrance_Port_Name'] = df['Entrance_Arrival_Port_Name']
restructured['Entrance_Port_USACE'] = df['Entrance_US_Port_USACE']
restructured['Entrance_Port_Code'] = df['Entrance_PORT']
restructured['Entrance_Draft_ft'] = df['Entrance_DRAFT_FT']
restructured['Entrance_Draft_in'] = df['Entrance_DRAFT_IN']
restructured['Entrance_Draft_Pct_Max'] = df['Entrance_Draft_Pct_of_Max']
restructured['Entrance_Activity'] = df['Entrance_Forecasted_Activity']
restructured['Entrance_Origin'] = df['Entrance_WHERE_IND']  # Foreign/Coastwise
restructured['Entrance_Previous_Port'] = df['Entrance_Previous_Foreign_Port'].fillna(df['Entrance_Previous_US_Port_USACE'])
restructured['Entrance_Previous_Country'] = df['Entrance_Previous_Foreign_Country']

# ============================================================================
# CLEARANCE DATA (DEPARTURE-SPECIFIC)
# ============================================================================
print("   Adding clearance-specific data...")
restructured['Clearance_RECID'] = df['Clearance_RECID']
restructured['Clearance_Port_Name'] = df['Clearance_Clearance_Port_Name']
restructured['Clearance_Port_USACE'] = df['Clearance_US_Port_USACE']
restructured['Clearance_Port_Code'] = df['Clearance_PORT']
restructured['Clearance_Draft_ft'] = df['Clearance_DRAFT_FT']
restructured['Clearance_Draft_in'] = df['Clearance_DRAFT_IN']
restructured['Clearance_Draft_Pct_Max'] = df['Clearance_Draft_Pct_of_Max']
restructured['Clearance_Activity'] = df['Clearance_Forecasted_Activity']
restructured['Clearance_Destination'] = df['Clearance_WHERE_IND']  # Foreign/Coastwise
restructured['Clearance_Next_Port'] = df['Clearance_Previous_Foreign_Port'].fillna(df['Clearance_Previous_US_Port_USACE'])
restructured['Clearance_Next_Country'] = df['Clearance_Previous_Foreign_Country']

# ============================================================================
# PORT GEOGRAPHY (from entrance, single source)
# ============================================================================
print("   Adding port geography...")
restructured['Port_Consolidated'] = df['Entrance_Port_Consolidated'].fillna(df['Clearance_Port_Consolidated'])
restructured['Port_Coast'] = df['Entrance_Port_Coast'].fillna(df['Clearance_Port_Coast'])
restructured['Port_Region'] = df['Entrance_Port_Region'].fillna(df['Clearance_Port_Region'])

# ============================================================================
# IMPORT CARGO DATA (from Panjiva entrance match)
# ============================================================================
print("   Adding import cargo data...")
restructured['Import_VOY_RECID'] = df['Entrance_VOY_RECID']
restructured['Import_Carrier'] = df['Entrance_Panjiva_Carrier']
restructured['Import_Cargo_Group'] = df['Entrance_Panjiva_Group']
restructured['Import_Cargo_Commodity'] = df['Entrance_Panjiva_Commodity']
restructured['Import_Tons'] = df['Entrance_Panjiva_Tons']
restructured['Import_Match_Days_Offset'] = df['Entrance_Match_Days_Offset']
restructured['Import_Match_Pass'] = df['Entrance_Match_Pass']
restructured['Import_Match_Method'] = df['Entrance_Match_Method']

# ============================================================================
# EXPORT CARGO DATA (from Panjiva clearance match)
# ============================================================================
print("   Adding export cargo data...")
restructured['Export_VOY_RECID'] = df['Clearance_VOY_RECID']
restructured['Export_Shipper'] = df['Clearance_Panjiva_Shipper']
restructured['Export_Cargo_Group'] = df['Clearance_Group']
restructured['Export_Cargo_Commodity'] = df['Clearance_Commodity']
restructured['Export_Tons'] = df['Clearance_Panjiva_Tons']
restructured['Export_Match_Days_Offset'] = df['Clearance_Match_Days_Offset']
restructured['Export_Match_Pass'] = df['Clearance_Match_Pass']
restructured['Export_Match_Method'] = df['Clearance_Match_Method']

# ============================================================================
# GRAIN EXPORT DATA (from FGIS match)
# ============================================================================
print("   Adding grain export data...")
restructured['Grain_Export'] = df['Grain_Export']
restructured['FGIS_RECID'] = df['FGIS_RECID']
restructured['Grain_Type'] = df['Grain_Type']
restructured['Grain_Detail'] = df['Grain_Detail']
restructured['Grain_MT'] = df['Grain_MT']
restructured['Grain_Pounds'] = df['Grain_Pounds']
restructured['Grain_Match_Quality'] = df['Match_Quality']

# ============================================================================
# MATCHING METADATA
# ============================================================================
print("   Adding match metadata...")
restructured['Match_Score'] = df['Match_Score']
restructured['Match_Method'] = df['Match_Method']
restructured['Tug_Barge_Pair_ID'] = df['Tug_Barge_Pair_ID']
restructured['Tug_Barge_Confidence'] = df['Pairing_Confidence']

# Save
print(f"\n3. Saving restructured file...")
restructured.to_csv(OUTPUT_FILE, index=False)
print(f"   Saved: {OUTPUT_FILE.name}")
file_size = OUTPUT_FILE.stat().st_size / (1024 * 1024)
print(f"   Size: {file_size:.1f} MB")

# Summary
print("\n" + "="*80)
print("RESTRUCTURING SUMMARY")
print("="*80)
print(f"\nOriginal columns: {len(df.columns)}")
print(f"Restructured columns: {len(restructured.columns)}")
print(f"Columns eliminated: {len(df.columns) - len(restructured.columns)}")

print(f"\nColumn breakdown:")
print(f"  Core Identifiers: 2")
print(f"  Vessel Data (common): 13")
print(f"  Timeline: 3")
print(f"  Entrance-specific: 11")
print(f"  Clearance-specific: 11")
print(f"  Port Geography: 3")
print(f"  Import Cargo: 8")
print(f"  Export Cargo: 8")
print(f"  Grain Export: 7")
print(f"  Match Metadata: 4")
print(f"  TOTAL: {len(restructured.columns)}")

print(f"\nRecord Type Distribution:")
record_types = restructured['Record_Type'].value_counts()
for rtype, count in record_types.items():
    pct = count / len(restructured) * 100
    print(f"  {rtype:<20} {count:>7,} ({pct:>5.1f}%)")

print("\n" + "="*80)
print("COMPLETE!")
print("="*80)
print(f"\nOutput: {OUTPUT_FILE}")
