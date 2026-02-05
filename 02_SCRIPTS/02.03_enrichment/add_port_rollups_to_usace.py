"""
Add Port Rollup Columns to USACE Entrance and Clearance Data
Version: 1.0.0
Date: 2026-01-15

Purpose:
- Add Port_Consolidated, Port_Coast, Port_Region columns to USACE data
- These are primary statistical rollup columns for analysis
- Maps via USACE port codes to standardized port groupings
"""

import pandas as pd
from pathlib import Path

print("="*80)
print("ADD PORT ROLLUPS TO USACE DATA v1.0.0")
print("="*80)

# File paths
PORT_MAPPING = Path(r"G:\My Drive\LLM\project_manifest\01.01_dictionary\usace_to_census_port_mapping.csv")
ENTRANCE_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_entrance_with_panjiva_match_v1.3.0.csv")
CLEARANCE_FILE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_outbound_clearance_transformed_v2.1.0.csv")

OUTPUT_ENTRANCE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_entrance_with_panjiva_match_v1.3.1.csv")
OUTPUT_CLEARANCE = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_outbound_clearance_transformed_v2.2.0.csv")

# Load port mapping
print("\n1. Loading port mapping dictionary...")
port_map = pd.read_csv(PORT_MAPPING)
print(f"   Port mappings loaded: {len(port_map):,}")

# Create lookup dictionary
port_lookup = {}
for _, row in port_map.iterrows():
    usace_port = str(row['USACE_PORT']).strip()
    port_lookup[usace_port] = {
        'Port_Consolidated': row.get('Port_Consolidated', ''),
        'Port_Coast': row.get('Port_Coast', ''),
        'Port_Region': row.get('Port_Region', '')
    }

print(f"   Unique USACE ports in mapping: {len(port_lookup):,}")

# Process Entrance file
print(f"\n2. Processing Entrance file...")
print(f"   Loading: {ENTRANCE_FILE.name}")
entrance = pd.read_csv(ENTRANCE_FILE, low_memory=False)
print(f"   Records: {len(entrance):,}")
print(f"   Current columns: {len(entrance.columns)}")

# Add rollup columns
entrance['PORT'] = entrance['PORT'].astype(str).str.strip()
entrance['Port_Consolidated'] = entrance['PORT'].map(lambda x: port_lookup.get(x, {}).get('Port_Consolidated', ''))
entrance['Port_Coast'] = entrance['PORT'].map(lambda x: port_lookup.get(x, {}).get('Port_Coast', ''))
entrance['Port_Region'] = entrance['PORT'].map(lambda x: port_lookup.get(x, {}).get('Port_Region', ''))

# Count matches
matched = (entrance['Port_Consolidated'] != '').sum()
print(f"   Ports matched: {matched:,} ({matched/len(entrance)*100:.1f}%)")

# Save
entrance.to_csv(OUTPUT_ENTRANCE, index=False)
print(f"   Saved: {OUTPUT_ENTRANCE.name}")
print(f"   Total columns: {len(entrance.columns)}")

# Process Clearance file
print(f"\n3. Processing Clearance file...")
print(f"   Loading: {CLEARANCE_FILE.name}")
clearance = pd.read_csv(CLEARANCE_FILE, low_memory=False)
print(f"   Records: {len(clearance):,}")
print(f"   Current columns: {len(clearance.columns)}")

# Add rollup columns (use Clearance_Port instead of PORT if it exists)
if 'PORT' in clearance.columns:
    port_col = 'PORT'
elif 'Clearance_Port' in clearance.columns:
    port_col = 'Clearance_Port'
else:
    print("   ERROR: No port column found!")
    exit(1)

clearance[port_col] = clearance[port_col].astype(str).str.strip()
clearance['Port_Consolidated'] = clearance[port_col].map(lambda x: port_lookup.get(x, {}).get('Port_Consolidated', ''))
clearance['Port_Coast'] = clearance[port_col].map(lambda x: port_lookup.get(x, {}).get('Port_Coast', ''))
clearance['Port_Region'] = clearance[port_col].map(lambda x: port_lookup.get(x, {}).get('Port_Region', ''))

# Count matches
matched = (clearance['Port_Consolidated'] != '').sum()
print(f"   Ports matched: {matched:,} ({matched/len(clearance)*100:.1f}%)")

# Save
clearance.to_csv(OUTPUT_CLEARANCE, index=False)
print(f"   Saved: {OUTPUT_CLEARANCE.name}")
print(f"   Total columns: {len(clearance.columns)}")

# Summary statistics
print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

print(f"\nEntrance Data:")
print(f"  Port_Consolidated coverage: {(entrance['Port_Consolidated'] != '').sum():,} / {len(entrance):,} ({(entrance['Port_Consolidated'] != '').sum()/len(entrance)*100:.1f}%)")
print(f"  Unique Port_Consolidated values: {entrance['Port_Consolidated'].nunique()}")
print(f"  Unique Port_Coast values: {entrance['Port_Coast'].nunique()}")
print(f"  Unique Port_Region values: {entrance['Port_Region'].nunique()}")

print(f"\n  Top 10 Port_Consolidated (by vessel count):")
top_ports = entrance['Port_Consolidated'].value_counts().head(10)
for port, count in top_ports.items():
    if port:
        print(f"    {port:<25} {count:>6,} vessels ({count/len(entrance)*100:>5.1f}%)")

print(f"\n  By Coast:")
coast_counts = entrance['Port_Coast'].value_counts()
for coast, count in coast_counts.items():
    if coast:
        print(f"    {coast:<10} {count:>6,} vessels ({count/len(entrance)*100:>5.1f}%)")

print(f"\nClearance Data:")
print(f"  Port_Consolidated coverage: {(clearance['Port_Consolidated'] != '').sum():,} / {len(clearance):,} ({(clearance['Port_Consolidated'] != '').sum()/len(clearance)*100:.1f}%)")
print(f"  Unique Port_Consolidated values: {clearance['Port_Consolidated'].nunique()}")
print(f"  Unique Port_Coast values: {clearance['Port_Coast'].nunique()}")
print(f"  Unique Port_Region values: {clearance['Port_Region'].nunique()}")

print("\n" + "="*80)
print("COMPLETE!")
print("="*80)
print("\nNew columns added:")
print("  - Port_Consolidated: Main port grouping (e.g., 'LA-Long Beach', 'New York')")
print("  - Port_Coast: Regional coast (East, West, Gulf)")
print("  - Port_Region: Detailed region (e.g., 'California', 'Mid-Atlantic')")
