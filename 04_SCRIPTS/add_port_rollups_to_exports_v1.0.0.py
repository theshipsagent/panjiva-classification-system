"""
Add Port Rollup Columns to Export and Clearance Data
Version: 1.0.0
Date: 2026-01-15

Purpose:
- Add Port_Consolidated, Port_Coast, Port_Region columns to export and clearance data
- These are primary statistical rollup columns for analysis
- Maps via port names to standardized port groupings

Input:
- Port mapping: 01.01_dictionary/usace_to_census_port_mapping.csv
- Panjiva exports: 01_STAGE01_PREPROCESSING/01.01_annual_files/panjiva_exports_2023_PORTCALL_*.csv
- USACE clearance: 02_STAGE02_CLASSIFICATION/usace_2023_clearance_with_panjiva_match_v1.0.0.csv

Output:
- Panjiva exports with port rollups
- USACE clearance with port rollups
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

print("="*80)
print("ADD PORT ROLLUPS TO EXPORT/CLEARANCE DATA v1.0.0")
print("="*80)

timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# File paths
PORT_MAPPING = Path(r"G:\My Drive\LLM\project_manifest\01.01_dictionary\usace_to_census_port_mapping.csv")
EXPORT_DIR = Path(r"G:\My Drive\LLM\project_manifest\01_STAGE01_PREPROCESSING\01.01_annual_files")
CLEARANCE_FILE = Path(r"G:\My Drive\LLM\project_manifest\02_STAGE02_CLASSIFICATION\usace_2023_clearance_with_panjiva_match_v1.0.0.csv")

OUTPUT_EXPORT_DIR = EXPORT_DIR
OUTPUT_CLEARANCE_FILE = Path(r"G:\My Drive\LLM\project_manifest\02_STAGE02_CLASSIFICATION\usace_2023_clearance_with_panjiva_match_v1.0.1.csv")

# Load port mapping
print("\n1. Loading port mapping dictionary...")
port_map = pd.read_csv(PORT_MAPPING)
print(f"   Port mappings loaded: {len(port_map):,}")

# Create lookup dictionaries
# For USACE ports (code-based)
port_lookup_usace = {}
for _, row in port_map.iterrows():
    usace_port = str(row['USACE_PORT']).strip()
    port_lookup_usace[usace_port] = {
        'Port_Consolidated': row.get('Port_Consolidated', ''),
        'Port_Coast': row.get('Port_Coast', ''),
        'Port_Region': row.get('Port_Region', '')
    }

# For Panjiva ports (name-based - need fuzzy matching)
# Use USACE_PORT_NAME column for matching
port_lookup_name = {}
for _, row in port_map.iterrows():
    usace_name = str(row.get('USACE_PORT_NAME', '')).strip().upper()
    if usace_name:
        # Extract city portion for matching
        city = usace_name.split(',')[0].strip()
        city = city.replace('PORT OF ', '').replace('PORT ', '').replace('THE ', '')
        port_lookup_name[city] = {
            'Port_Consolidated': row.get('Port_Consolidated', ''),
            'Port_Coast': row.get('Port_Coast', ''),
            'Port_Region': row.get('Port_Region', '')
        }

print(f"   USACE port codes: {len(port_lookup_usace):,}")
print(f"   Census port names: {len(port_lookup_name):,}")

# Function to match Panjiva port names to USACE port names
def match_port_name(panjiva_port):
    """Match Panjiva port name to USACE port for rollup lookup"""
    if pd.isna(panjiva_port) or panjiva_port == '':
        return None, None, None

    # Normalize the port name
    port_str = str(panjiva_port).upper().strip()

    # Extract city portion (first part before comma)
    parts = port_str.split(',')
    if len(parts) > 0:
        city = parts[0].strip()
        # Also try to get second part which might be city name
        city2 = parts[1].strip() if len(parts) > 1 else None

        # Clean city names
        city = city.replace('PORT OF ', '').replace('PORT ', '').replace('THE ', '')
        city = city.replace('ENTRY-', '').replace('PORT ENTRY-', '')

        # Try exact match on first city
        if city in port_lookup_name:
            return (port_lookup_name[city]['Port_Consolidated'],
                    port_lookup_name[city]['Port_Coast'],
                    port_lookup_name[city]['Port_Region'])

        # Try second part (e.g., "Port Freeport, Freeport, Texas" -> "FREEPORT")
        if city2:
            city2_clean = city2.replace('PORT OF ', '').replace('PORT ', '').replace('THE ', '')
            if city2_clean in port_lookup_name:
                return (port_lookup_name[city2_clean]['Port_Consolidated'],
                        port_lookup_name[city2_clean]['Port_Coast'],
                        port_lookup_name[city2_clean]['Port_Region'])

        # Try partial matching
        for port_name, rollup in port_lookup_name.items():
            if city in port_name or port_name in city:
                return rollup['Port_Consolidated'], rollup['Port_Coast'], rollup['Port_Region']
            if city2 and (city2_clean in port_name or port_name in city2_clean):
                return rollup['Port_Consolidated'], rollup['Port_Coast'], rollup['Port_Region']

    return None, None, None

# Process Panjiva Exports
print(f"\n2. Processing Panjiva export port call file...")
export_files = list(EXPORT_DIR.glob("panjiva_exports_2023_PORTCALL_*.csv"))
if not export_files:
    print("   ERROR: No export port call files found!")
else:
    export_files.sort()
    export_file = export_files[-1]
    print(f"   Loading: {export_file.name}")

    exports = pd.read_csv(export_file, low_memory=False)
    print(f"   Records: {len(exports):,}")
    print(f"   Current columns: {len(exports.columns)}")

    # Add rollup columns using name matching
    print(f"   Matching ports to rollup categories...")
    rollup_results = exports['Port_of_Lading'].apply(match_port_name)
    exports['Port_Consolidated'] = [r[0] for r in rollup_results]
    exports['Port_Coast'] = [r[1] for r in rollup_results]
    exports['Port_Region'] = [r[2] for r in rollup_results]

    # Count matches
    matched = (exports['Port_Consolidated'].notna()).sum()
    print(f"   Ports matched: {matched:,} ({matched/len(exports)*100:.1f}%)")

    # Save
    output_file = OUTPUT_EXPORT_DIR / f"panjiva_exports_2023_PORTCALL_v{timestamp}.csv"
    exports.to_csv(output_file, index=False)
    print(f"   Saved: {output_file.name}")
    print(f"   Total columns: {len(exports.columns)}")

# Process USACE Clearance
print(f"\n3. Processing USACE clearance file...")
print(f"   Loading: {CLEARANCE_FILE.name}")
clearance = pd.read_csv(CLEARANCE_FILE, low_memory=False)
print(f"   Records: {len(clearance):,}")
print(f"   Current columns: {len(clearance.columns)}")

# Add rollup columns (use PORT code if it exists)
if 'PORT' in clearance.columns:
    port_col = 'PORT'
elif 'Clearance_Port' in clearance.columns:
    port_col = 'Clearance_Port'
else:
    print("   WARNING: No port column found, trying name-based matching...")
    port_col = None

if port_col:
    clearance[port_col] = clearance[port_col].astype(str).str.strip()
    clearance['Port_Consolidated'] = clearance[port_col].map(lambda x: port_lookup_usace.get(x, {}).get('Port_Consolidated', ''))
    clearance['Port_Coast'] = clearance[port_col].map(lambda x: port_lookup_usace.get(x, {}).get('Port_Coast', ''))
    clearance['Port_Region'] = clearance[port_col].map(lambda x: port_lookup_usace.get(x, {}).get('Port_Region', ''))
else:
    # Fall back to name matching
    rollup_results = clearance['Clearance_Port_Name'].apply(match_port_name)
    clearance['Port_Consolidated'] = [r[0] for r in rollup_results]
    clearance['Port_Coast'] = [r[1] for r in rollup_results]
    clearance['Port_Region'] = [r[2] for r in rollup_results]

# Count matches
matched = (clearance['Port_Consolidated'] != '').sum()
print(f"   Ports matched: {matched:,} ({matched/len(clearance)*100:.1f}%)")

# Save
clearance.to_csv(OUTPUT_CLEARANCE_FILE, index=False)
print(f"   Saved: {OUTPUT_CLEARANCE_FILE.name}")
print(f"   Total columns: {len(clearance.columns)}")

# Summary statistics
print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

if 'exports' in locals():
    print(f"\nExport Data:")
    print(f"  Port_Consolidated coverage: {(exports['Port_Consolidated'].notna()).sum():,} / {len(exports):,} ({(exports['Port_Consolidated'].notna()).sum()/len(exports)*100:.1f}%)")
    print(f"  Unique Port_Consolidated values: {exports['Port_Consolidated'].nunique()}")
    print(f"  Unique Port_Coast values: {exports['Port_Coast'].nunique()}")
    print(f"  Unique Port_Region values: {exports['Port_Region'].nunique()}")

    print(f"\n  Top 10 Export Ports (by tonnage):")
    top_ports = exports.groupby('Port_Consolidated')['Total_Tons'].sum().sort_values(ascending=False).head(10)
    for port, tons in top_ports.items():
        if pd.notna(port) and port:
            print(f"    {str(port):<35} {tons:>15,.0f} tons")

    print(f"\n  By Coast:")
    coast_counts = exports.groupby('Port_Coast')['Total_Tons'].sum().sort_values(ascending=False)
    for coast, tons in coast_counts.items():
        if pd.notna(coast) and coast:
            print(f"    {str(coast):<15} {tons:>15,.0f} tons")

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
print("\nExport -> Clearance pipeline complete!")
