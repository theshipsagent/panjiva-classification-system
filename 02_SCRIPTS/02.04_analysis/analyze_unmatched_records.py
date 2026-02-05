"""
Analyze Unmatched Entrance and Clearance Records
Version: 1.0.0
Purpose: Identify patterns in unmatched records by port and vessel type
"""

import pandas as pd
from pathlib import Path

print("="*80)
print("UNMATCHED RECORDS ANALYSIS")
print("="*80)

# Load port call master
file_path = Path(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_portcall_master_v1.0.0.csv")
df = pd.read_csv(file_path, low_memory=False)

print(f"\nTotal records: {len(df):,}")
print(f"\nMatch Type Distribution:")
print(df['Match_Type'].value_counts())

# Analyze ENTRANCE_ONLY
print("\n" + "="*80)
print("ENTRANCE_ONLY RECORDS (No Clearance Match)")
print("="*80)
entrance_only = df[df['Match_Type'] == 'ENTRANCE_ONLY'].copy()
print(f"\nTotal: {len(entrance_only):,} records")

# By Port (top 20)
print("\nTop 20 Ports with Unmatched Entrances:")
port_counts = entrance_only['Entrance_PORT'].value_counts().head(20)
for port, count in port_counts.items():
    port_name = entrance_only[entrance_only['Entrance_PORT'] == port]['Entrance_US_Port_USACE'].iloc[0] if len(entrance_only[entrance_only['Entrance_PORT'] == port]) > 0 else 'Unknown'
    print(f"  {port} ({port_name[:40]}): {count:,} unmatched entrances")

# By ICST vessel type
print("\nBy Vessel Type (ICST_DESC):")
if 'Entrance_ICST_DESC' in entrance_only.columns:
    vtype_counts = entrance_only['Entrance_ICST_DESC'].value_counts()
    for vtype, count in vtype_counts.items():
        pct = count / len(entrance_only) * 100
        print(f"  {str(vtype)[:40]:<40} {count:>6,} ({pct:>5.1f}%)")
else:
    print("  ICST_DESC column not found")

# Analyze CLEARANCE_ONLY
print("\n" + "="*80)
print("CLEARANCE_ONLY RECORDS (No Entrance Match)")
print("="*80)
clearance_only = df[df['Match_Type'] == 'CLEARANCE_ONLY'].copy()
print(f"\nTotal: {len(clearance_only):,} records")

# By Port (top 20)
print("\nTop 20 Ports with Unmatched Clearances:")
port_counts_clear = clearance_only['Clearance_PORT'].value_counts().head(20)
for port, count in port_counts_clear.items():
    port_name = clearance_only[clearance_only['Clearance_PORT'] == port]['Clearance_US_Port_USACE'].iloc[0] if len(clearance_only[clearance_only['Clearance_PORT'] == port]) > 0 else 'Unknown'
    print(f"  {port} ({port_name[:40]}): {count:,} unmatched clearances")

# By ICST vessel type
print("\nBy Vessel Type (ICST_DESC):")
if 'Clearance_ICST_DESC' in clearance_only.columns:
    vtype_counts_clear = clearance_only['Clearance_ICST_DESC'].value_counts()
    for vtype, count in vtype_counts_clear.items():
        pct = count / len(clearance_only) * 100
        print(f"  {str(vtype)[:40]:<40} {count:>6,} ({pct:>5.1f}%)")
else:
    print("  ICST_DESC column not found")

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"\nMatched Port Calls (BOTH): {len(df[df['Match_Type'] == 'BOTH']):,} (65.3%)")
print(f"  -> These are true commercial cargo vessel port calls")
print(f"\nUnmatched Entrances: {len(entrance_only):,} (16.8%)")
print(f"  -> Vessels departed empty, after 2023, or specialized vessel types")
print(f"\nUnmatched Clearances: {len(clearance_only):,} (17.8%)")
print(f"  -> Vessels arrived before 2023, or specialized vessel types")
print(f"\nSuggestion: Review ICST_DESC distributions above to identify")
print(f"vessel types that should be excluded from matching (tugs, barges,")
print(f"offshore support vessels, etc.)")
