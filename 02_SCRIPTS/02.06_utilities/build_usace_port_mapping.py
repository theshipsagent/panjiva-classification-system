"""
Build USACE PORT Code to Census Code Mapping
Matches USACE PORT_NAME to Census Sked_D_E by name similarity
"""

import pandas as pd
from pathlib import Path
import re

print('=' * 100)
print('BUILDING USACE PORT CODE TO CENSUS CODE MAPPING')
print('=' * 100)
print()

# Paths
data_path = Path(r'G:\My Drive\LLM\project_manifest\00_raw_data\00_03_usace_entrance_clearance_raw')
dict_path = Path(r'G:\My Drive\LLM\project_manifest\01.01_dictionary')

# Read USACE data to get unique ports
print('Reading USACE entrance data...')
df_usace = pd.read_csv(data_path / 'Entrances_Clearances_2023_2023_Inbound.csv')
usace_ports = df_usace[['PORT', 'PORT_NAME']].drop_duplicates().sort_values('PORT')
print(f'  Found {len(usace_ports)} unique USACE ports')
print()

# Read Census port dictionary
print('Reading Census port dictionary...')
df_census = pd.read_csv(dict_path / '01_us_port_dictionary.csv', dtype=str)
print(f'  Found {len(df_census)} Census ports')
print()

def normalize_port_name(name):
    """
    Normalize port name for matching
    - Remove "Port of", "Port Authority of", etc.
    - Remove extra spaces
    - Convert to lowercase
    - Extract main city name
    """
    if pd.isna(name):
        return ''

    name = str(name).lower().strip()

    # Remove common prefixes
    name = re.sub(r'^port authority of\s+', '', name)
    name = re.sub(r'^port of\s+', '', name)
    name = re.sub(r'\s+port authority', '', name)
    name = re.sub(r'\s+harbor', '', name)
    name = re.sub(r'\s+river', '', name)
    name = re.sub(r'\s+channel', '', name)

    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name).strip()

    return name

def extract_city_state(name):
    """
    Extract city and state from port name
    Returns (city, state) tuple
    """
    if pd.isna(name):
        return ('', '')

    name = str(name)

    # Look for patterns like "City, State" or "City, ST"
    match = re.search(r'([^,]+),\s*([A-Z]{2})', name)
    if match:
        return (match.group(1).strip().lower(), match.group(2).strip().upper())

    # Look for full state names
    match = re.search(r'([^,]+),\s*(\w+)$', name)
    if match:
        return (match.group(1).strip().lower(), match.group(2).strip().lower())

    return ('', '')

# Normalize all names
print('Normalizing port names...')
usace_ports['normalized'] = usace_ports['PORT_NAME'].apply(normalize_port_name)
usace_ports['city'], usace_ports['state'] = zip(*usace_ports['PORT_NAME'].apply(extract_city_state))

df_census['normalized'] = df_census['Sked_D_E'].apply(normalize_port_name)
df_census['city'], df_census['state'] = zip(*df_census['Sked_D_E'].apply(extract_city_state))

print()

# Try exact matches first (by normalized name)
print('Attempting exact matches by normalized name...')
mapping = []

for _, usace_row in usace_ports.iterrows():
    usace_port = str(usace_row['PORT'])
    usace_name = usace_row['PORT_NAME']
    usace_norm = usace_row['normalized']
    usace_city = usace_row['city']
    usace_state = usace_row['state']

    # Try exact normalized match
    exact_match = df_census[df_census['normalized'] == usace_norm]
    if len(exact_match) > 0:
        census_row = exact_match.iloc[0]
        mapping.append({
            'USACE_PORT': usace_port,
            'USACE_PORT_NAME': usace_name,
            'Census_Code': census_row['Code'],
            'Census_Sked_D_E': census_row['Sked_D_E'],
            'Port_Consolidated': census_row['Port_Consolidated'],
            'Port_Coast': census_row['Port_Coast'],
            'Port_Region': census_row['Port_Region'],
            'Match_Type': 'Exact'
        })
        continue

    # Try city + state match
    if usace_city and usace_state:
        city_state_match = df_census[(df_census['city'] == usace_city) & (df_census['state'] == usace_state)]
        if len(city_state_match) > 0:
            census_row = city_state_match.iloc[0]
            mapping.append({
                'USACE_PORT': usace_port,
                'USACE_PORT_NAME': usace_name,
                'Census_Code': census_row['Code'],
                'Census_Sked_D_E': census_row['Sked_D_E'],
                'Port_Consolidated': census_row['Port_Consolidated'],
                'Port_Coast': census_row['Port_Coast'],
                'Port_Region': census_row['Port_Region'],
                'Match_Type': 'City+State'
            })
            continue

    # Try substring match (city name appears in Sked_D_E)
    if usace_city:
        substring_match = df_census[df_census['normalized'].str.contains(usace_city, na=False)]
        if len(substring_match) > 0:
            census_row = substring_match.iloc[0]
            mapping.append({
                'USACE_PORT': usace_port,
                'USACE_PORT_NAME': usace_name,
                'Census_Code': census_row['Code'],
                'Census_Sked_D_E': census_row['Sked_D_E'],
                'Port_Consolidated': census_row['Port_Consolidated'],
                'Port_Coast': census_row['Port_Coast'],
                'Port_Region': census_row['Port_Region'],
                'Match_Type': 'Substring'
            })
            continue

    # No match found
    mapping.append({
        'USACE_PORT': usace_port,
        'USACE_PORT_NAME': usace_name,
        'Census_Code': '',
        'Census_Sked_D_E': '',
        'Port_Consolidated': '',
        'Port_Coast': '',
        'Port_Region': '',
        'Match_Type': 'NO MATCH'
    })

df_mapping = pd.DataFrame(mapping)

# Statistics
total = len(df_mapping)
matched = len(df_mapping[df_mapping['Match_Type'] != 'NO MATCH'])
print(f'  Matched: {matched} / {total} ({matched/total*100:.1f}%)')
print()

# By match type
print('Match type breakdown:')
for match_type, count in df_mapping['Match_Type'].value_counts().items():
    print(f'  {match_type}: {count} ({count/total*100:.1f}%)')
print()

# Save mapping
output_file = dict_path / 'usace_to_census_port_mapping.csv'
df_mapping.to_csv(output_file, index=False)
print(f'Mapping saved to: {output_file}')
print()

# Show unmatched ports
no_match = df_mapping[df_mapping['Match_Type'] == 'NO MATCH']
if len(no_match) > 0:
    print('=' * 100)
    print(f'UNMATCHED PORTS ({len(no_match)} ports)')
    print('=' * 100)
    print(no_match[['USACE_PORT', 'USACE_PORT_NAME']].to_string(index=False))
    print()
else:
    print('All ports matched successfully!')
    print()

print('=' * 100)
