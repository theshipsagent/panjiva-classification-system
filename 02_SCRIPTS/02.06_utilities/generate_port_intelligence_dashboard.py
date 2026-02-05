"""
Port Intelligence Dashboard Generator
Analyzes USACE port call master data and generates comprehensive HTML dashboard
Version: 1.0.0
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Paths
BASE_DIR = Path(r"G:\My Drive\LLM\project_manifest")
DATA_FILE = BASE_DIR / "00_DATA/00.03_MATCHED" / "usace_2023_portcall_master_v1.1.0.csv"
OUTPUT_FILE = BASE_DIR / "03_DOCUMENTATION/03.04_summaries" / "port_intelligence_dashboard.html"

# Ship Size Classifications
def classify_bulk_carrier(dwt):
    """Classify bulk carrier by DWT"""
    if pd.isna(dwt) or dwt == 0:
        return "Unknown"
    elif dwt < 10000:
        return "Small (<10k)"
    elif dwt < 35000:
        return "Handysize (10-35k)"
    elif dwt < 60000:
        return "Handymax (35-60k)"
    elif dwt < 80000:
        return "Panamax (60-80k)"
    elif dwt < 200000:
        return "Capesize (80-200k)"
    else:
        return "VLOC (200k+)"

def classify_tanker(dwt):
    """Classify tanker by DWT"""
    if pd.isna(dwt) or dwt == 0:
        return "Unknown"
    elif dwt < 10000:
        return "Small (<10k)"
    elif dwt < 55000:
        return "MR (10-55k)"
    elif dwt < 80000:
        return "LR1 (55-80k)"
    elif dwt < 120000:
        return "LR2/Aframax (80-120k)"
    elif dwt < 200000:
        return "Suezmax (120-200k)"
    elif dwt < 320000:
        return "VLCC (200-320k)"
    else:
        return "ULCC (320k+)"

def classify_container(dwt):
    """Classify container ship (simplified - using DWT as proxy)"""
    if pd.isna(dwt) or dwt == 0:
        return "Unknown"
    elif dwt < 15000:
        return "Feeder (<15k)"
    elif dwt < 40000:
        return "Panamax (15-40k)"
    elif dwt < 80000:
        return "Post-Panamax (40-80k)"
    elif dwt < 120000:
        return "New Panamax (80-120k)"
    else:
        return "ULCV (120k+)"

def classify_generic(dwt):
    """Generic classification for other vessel types"""
    if pd.isna(dwt) or dwt == 0:
        return "Unknown"
    elif dwt < 5000:
        return "Very Small (<5k)"
    elif dwt < 20000:
        return "Small (5-20k)"
    elif dwt < 50000:
        return "Medium (20-50k)"
    elif dwt < 100000:
        return "Large (50-100k)"
    else:
        return "Very Large (100k+)"

def classify_ship_size(dwt, vessel_type):
    """Classify ship size based on DWT and vessel type"""
    if pd.isna(vessel_type):
        return classify_generic(dwt)

    vtype_lower = str(vessel_type).lower()

    if 'bulk' in vtype_lower:
        return classify_bulk_carrier(dwt)
    elif 'tanker' in vtype_lower or 'tank' in vtype_lower:
        return classify_tanker(dwt)
    elif 'container' in vtype_lower:
        return classify_container(dwt)
    else:
        return classify_generic(dwt)

def extract_hs2(group_str):
    """Extract HS2 code from Group string"""
    if pd.isna(group_str):
        return None
    # Look for patterns like "HS27", "HS 27", etc.
    import re
    match = re.search(r'HS\s*(\d{2})', str(group_str))
    if match:
        return f"HS{match.group(1)}"
    return None

print("Loading port call master data...")
df = pd.read_csv(DATA_FILE, low_memory=False)
print(f"Loaded {len(df):,} records")

# Extract vessel types and DWTs for both entrance and clearance
df['Entrance_Ship_Size_Class'] = df.apply(
    lambda row: classify_ship_size(row['Entrance_Vessel_DWT'], row['Entrance_Vessel_Type']),
    axis=1
)
df['Clearance_Ship_Size_Class'] = df.apply(
    lambda row: classify_ship_size(row['Clearance_Vessel_DWT'], row['Clearance_Vessel_Type']),
    axis=1
)

# Extract HS2 codes
df['Entrance_HS2'] = df['Entrance_Group'].apply(extract_hs2)
df['Clearance_HS2'] = df['Clearance_Group'].apply(extract_hs2)

print("\nGenerating analytics...")

# ============================================================================
# 1. EXECUTIVE SUMMARY STATS
# ============================================================================
exec_stats = {
    'total_portcalls': len(df),
    'complete_portcalls': len(df[df['Match_Type'] == 'BOTH']),
    'entrance_only': len(df[df['Match_Type'] == 'ENTRANCE_ONLY']),
    'clearance_only': len(df[df['Match_Type'] == 'CLEARANCE_ONLY']),
    'tug_barge_pairs': len(df[df['Match_Type'] == 'TUG_BARGE_PAIR']),
    'avg_port_stay': df['Port_Stay_Days_Decimal'].mean(),
    'median_port_stay': df['Port_Stay_Days_Decimal'].median(),
    'unique_vessels': df['Entrance_IMO'].nunique() + df['Clearance_IMO'].nunique(),
    'unique_ports': len(set(df['Entrance_Port_Consolidated'].dropna()) |
                         set(df['Clearance_Port_Consolidated'].dropna())),
}

# Import/Export stats
entrance_df = df[df['Match_Type'].isin(['BOTH', 'ENTRANCE_ONLY'])].copy()
clearance_df = df[df['Match_Type'].isin(['BOTH', 'CLEARANCE_ONLY'])].copy()

exec_stats['total_imports'] = len(entrance_df)
exec_stats['total_exports'] = len(clearance_df)
exec_stats['avg_import_dwt'] = entrance_df['Entrance_Vessel_DWT'].mean()
exec_stats['avg_export_dwt'] = clearance_df['Clearance_Vessel_DWT'].mean()

# ============================================================================
# 2. REGIONAL ANALYSIS
# ============================================================================
regional_stats = []
for coast in df['Entrance_Port_Coast'].dropna().unique():
    coast_data = df[
        (df['Entrance_Port_Coast'] == coast) |
        (df['Clearance_Port_Coast'] == coast)
    ]

    regional_stats.append({
        'coast': coast,
        'total_calls': len(coast_data),
        'avg_dwt': coast_data[['Entrance_Vessel_DWT', 'Clearance_Vessel_DWT']].mean().mean(),
        'avg_stay': coast_data['Port_Stay_Days_Decimal'].mean(),
        'imports': len(coast_data[coast_data['Entrance_Port_Coast'] == coast]),
        'exports': len(coast_data[coast_data['Clearance_Port_Coast'] == coast]),
    })

regional_df = pd.DataFrame(regional_stats).sort_values('total_calls', ascending=False)

# ============================================================================
# 3. PORT PROFILES
# ============================================================================
port_profiles = []

# Get all unique ports
all_ports = set(df['Entrance_Port_Consolidated'].dropna()) | set(df['Clearance_Port_Consolidated'].dropna())

for port in sorted(all_ports):
    entrance_port = df[df['Entrance_Port_Consolidated'] == port]
    clearance_port = df[df['Clearance_Port_Consolidated'] == port]

    # Get coast info (prefer entrance, fallback to clearance)
    coast = entrance_port['Entrance_Port_Coast'].mode()[0] if len(entrance_port) > 0 else \
            (clearance_port['Clearance_Port_Coast'].mode()[0] if len(clearance_port) > 0 else 'Unknown')

    # Ship size distribution for imports
    import_sizes = entrance_port['Entrance_Ship_Size_Class'].value_counts().to_dict()

    # Ship size distribution for exports
    export_sizes = clearance_port['Clearance_Ship_Size_Class'].value_counts().to_dict()

    # Vessel types
    vessel_types_import = entrance_port['Entrance_Vessel_Type'].value_counts().to_dict()
    vessel_types_export = clearance_port['Clearance_Vessel_Type'].value_counts().to_dict()

    # Top HS2 codes
    top_hs2_import = entrance_port['Entrance_HS2'].value_counts().head(5).to_dict()
    top_hs2_export = clearance_port['Clearance_HS2'].value_counts().head(5).to_dict()

    # Complete port calls for this port
    complete_calls = df[
        (df['Match_Type'] == 'BOTH') &
        ((df['Entrance_Port_Consolidated'] == port) | (df['Clearance_Port_Consolidated'] == port))
    ]

    profile = {
        'port': port,
        'coast': coast,
        'total_calls': len(entrance_port) + len(clearance_port),
        'imports': len(entrance_port),
        'exports': len(clearance_port),
        'complete_calls': len(complete_calls),
        'avg_import_dwt': entrance_port['Entrance_Vessel_DWT'].mean(),
        'avg_export_dwt': clearance_port['Clearance_Vessel_DWT'].mean(),
        'avg_port_stay': complete_calls['Port_Stay_Days_Decimal'].mean(),
        'median_port_stay': complete_calls['Port_Stay_Days_Decimal'].median(),
        'import_ship_sizes': import_sizes,
        'export_ship_sizes': export_sizes,
        'vessel_types_import': vessel_types_import,
        'vessel_types_export': vessel_types_export,
        'top_hs2_import': top_hs2_import,
        'top_hs2_export': top_hs2_export,
    }

    port_profiles.append(profile)

# Sort by total calls
port_profiles = sorted(port_profiles, key=lambda x: x['total_calls'], reverse=True)

# ============================================================================
# 4. SHIP SIZE ANALYSIS (KEY SECTION)
# ============================================================================

# Import ship sizes
import_ship_sizes = entrance_df['Entrance_Ship_Size_Class'].value_counts().to_dict()
import_dwt_by_size = entrance_df.groupby('Entrance_Ship_Size_Class')['Entrance_Vessel_DWT'].agg(['mean', 'sum', 'count']).to_dict('index')

# Export ship sizes
export_ship_sizes = clearance_df['Clearance_Ship_Size_Class'].value_counts().to_dict()
export_dwt_by_size = clearance_df.groupby('Clearance_Ship_Size_Class')['Clearance_Vessel_DWT'].agg(['mean', 'sum', 'count']).to_dict('index')

# Complete port calls by ship size
both_df = df[df['Match_Type'] == 'BOTH'].copy()
both_df['Ship_Size_Class'] = both_df['Entrance_Ship_Size_Class']  # Use entrance as primary

complete_by_size_raw = both_df.groupby('Ship_Size_Class').agg({
    'Port_Stay_Days_Decimal': ['mean', 'median'],
    'Entrance_Vessel_DWT': 'count'
})

# Convert to simple dict
complete_by_size = {}
for size_class in complete_by_size_raw.index:
    complete_by_size[size_class] = {
        'avg_stay': complete_by_size_raw.loc[size_class, ('Port_Stay_Days_Decimal', 'mean')],
        'median_stay': complete_by_size_raw.loc[size_class, ('Port_Stay_Days_Decimal', 'median')],
        'count': int(complete_by_size_raw.loc[size_class, ('Entrance_Vessel_DWT', 'count')])
    }

# Top ports by ship size (imports)
ship_size_ports_import = {}
for size_class in import_ship_sizes.keys():
    if size_class != 'Unknown':
        top_ports = entrance_df[entrance_df['Entrance_Ship_Size_Class'] == size_class]\
            ['Entrance_Port_Consolidated'].value_counts().head(5).to_dict()
        ship_size_ports_import[size_class] = top_ports

# Top ports by ship size (exports)
ship_size_ports_export = {}
for size_class in export_ship_sizes.keys():
    if size_class != 'Unknown':
        top_ports = clearance_df[clearance_df['Clearance_Ship_Size_Class'] == size_class]\
            ['Clearance_Port_Consolidated'].value_counts().head(5).to_dict()
        ship_size_ports_export[size_class] = top_ports

# HS2 specialization by ship size (imports)
ship_size_hs2_import = {}
for size_class in import_ship_sizes.keys():
    if size_class != 'Unknown':
        top_hs2 = entrance_df[entrance_df['Entrance_Ship_Size_Class'] == size_class]\
            ['Entrance_HS2'].value_counts().head(5).to_dict()
        ship_size_hs2_import[size_class] = top_hs2

# ============================================================================
# 5. CARGO FLOW ANALYSIS
# ============================================================================

# Import cargo flows
import_cargo_flow = entrance_df.groupby(['Entrance_Port_Consolidated', 'Entrance_HS2']).size()\
    .reset_index(name='count').sort_values('count', ascending=False).head(50)

# Export cargo flows
export_cargo_flow = clearance_df.groupby(['Clearance_Port_Consolidated', 'Clearance_HS2']).size()\
    .reset_index(name='count').sort_values('count', ascending=False).head(50)

# Port-commodity matrix (top 20 ports, top 10 commodities)
top_ports = df['Entrance_Port_Consolidated'].value_counts().head(20).index.tolist()
top_hs2_import = entrance_df['Entrance_HS2'].value_counts().head(10).index.tolist()

port_commodity_matrix = []
for port in top_ports:
    row = {'port': port}
    for hs2 in top_hs2_import:
        if pd.notna(hs2):
            count = len(entrance_df[
                (entrance_df['Entrance_Port_Consolidated'] == port) &
                (entrance_df['Entrance_HS2'] == hs2)
            ])
            row[hs2] = count
    port_commodity_matrix.append(row)

# ============================================================================
# 6. OPERATIONAL METRICS
# ============================================================================

# Turnaround time by port (top 20)
turnaround_by_port = both_df.groupby('Entrance_Port_Consolidated')\
    .agg({'Port_Stay_Days_Decimal': ['mean', 'median', 'count']})\
    .sort_values(('Port_Stay_Days_Decimal', 'count'), ascending=False)\
    .head(20)

turnaround_stats = []
for port in turnaround_by_port.index:
    turnaround_stats.append({
        'port': port,
        'avg_days': turnaround_by_port.loc[port, ('Port_Stay_Days_Decimal', 'mean')],
        'median_days': turnaround_by_port.loc[port, ('Port_Stay_Days_Decimal', 'median')],
        'count': int(turnaround_by_port.loc[port, ('Port_Stay_Days_Decimal', 'count')])
    })

# Turnaround time by ship size
turnaround_by_size_raw = both_df.groupby('Ship_Size_Class')\
    .agg({'Port_Stay_Days_Decimal': ['mean', 'median', 'count']})

turnaround_by_size = {}
for size_class in turnaround_by_size_raw.index:
    turnaround_by_size[size_class] = {
        'avg_days': turnaround_by_size_raw.loc[size_class, ('Port_Stay_Days_Decimal', 'mean')],
        'median_days': turnaround_by_size_raw.loc[size_class, ('Port_Stay_Days_Decimal', 'median')],
        'count': int(turnaround_by_size_raw.loc[size_class, ('Port_Stay_Days_Decimal', 'count')])
    }

# ============================================================================
# EXPORT DATA TO JSON
# ============================================================================

dashboard_data = {
    'executive_summary': exec_stats,
    'regional_analysis': regional_df.to_dict('records'),
    'port_profiles': port_profiles[:50],  # Top 50 ports
    'ship_size_analysis': {
        'import_sizes': import_ship_sizes,
        'export_sizes': export_ship_sizes,
        'import_dwt_by_size': import_dwt_by_size,
        'export_dwt_by_size': export_dwt_by_size,
        'complete_by_size': complete_by_size,
        'ship_size_ports_import': ship_size_ports_import,
        'ship_size_ports_export': ship_size_ports_export,
        'ship_size_hs2_import': ship_size_hs2_import,
    },
    'cargo_flow': {
        'import_flow': import_cargo_flow.to_dict('records'),
        'export_flow': export_cargo_flow.to_dict('records'),
        'port_commodity_matrix': port_commodity_matrix,
    },
    'operational_metrics': {
        'turnaround_by_port': turnaround_stats,
        'turnaround_by_size': turnaround_by_size,
    },
    'metadata': {
        'generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data_source': 'usace_2023_portcall_master_v1.1.0.csv',
        'total_records': len(df),
    }
}

# Convert to JSON
json_data = json.dumps(dashboard_data, indent=2, default=str)

print(f"\nGenerated analytics for:")
print(f"  - {len(port_profiles)} ports")
print(f"  - {len(regional_df)} regions")
print(f"  - {len(import_ship_sizes)} ship size classes (import)")
print(f"  - {len(export_ship_sizes)} ship size classes (export)")

# Save JSON for verification
json_file = BASE_DIR / "03_DOCUMENTATION/03.04_summaries" / "port_intelligence_data.json"
with open(json_file, 'w') as f:
    f.write(json_data)
print(f"\nSaved analytics data to: {json_file}")

print("\nReady to generate HTML dashboard...")
print("Data summary:")
print(f"  Complete port calls: {exec_stats['complete_portcalls']:,}")
print(f"  Average port stay: {exec_stats['avg_port_stay']:.1f} days")
print(f"  Average import DWT: {exec_stats['avg_import_dwt']:,.0f}")
print(f"  Average export DWT: {exec_stats['avg_export_dwt']:,.0f}")
