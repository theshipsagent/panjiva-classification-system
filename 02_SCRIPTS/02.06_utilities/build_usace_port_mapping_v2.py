"""
Build USACE PORT Code to Census Code Mapping v2
Improved name matching with city extraction and state validation
"""

import pandas as pd
from pathlib import Path
import re

print('=' * 100)
print('BUILDING USACE PORT CODE TO CENSUS CODE MAPPING v2.0')
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

# State abbreviation mapping
state_abbrev_to_full = {
    'AL': 'alabama', 'AK': 'alaska', 'AZ': 'arizona', 'AR': 'arkansas', 'CA': 'california',
    'CO': 'colorado', 'CT': 'connecticut', 'DE': 'delaware', 'FL': 'florida', 'GA': 'georgia',
    'HI': 'hawaii', 'ID': 'idaho', 'IL': 'illinois', 'IN': 'indiana', 'IA': 'iowa',
    'KS': 'kansas', 'KY': 'kentucky', 'LA': 'louisiana', 'ME': 'maine', 'MD': 'maryland',
    'MA': 'massachusetts', 'MI': 'michigan', 'MN': 'minnesota', 'MS': 'mississippi', 'MO': 'missouri',
    'MT': 'montana', 'NE': 'nebraska', 'NV': 'nevada', 'NH': 'new hampshire', 'NJ': 'new jersey',
    'NM': 'new mexico', 'NY': 'new york', 'NC': 'north carolina', 'ND': 'north dakota', 'OH': 'ohio',
    'OK': 'oklahoma', 'OR': 'oregon', 'PA': 'pennsylvania', 'RI': 'rhode island', 'SC': 'south carolina',
    'SD': 'south dakota', 'TN': 'tennessee', 'TX': 'texas', 'UT': 'utah', 'VT': 'vermont',
    'VA': 'virginia', 'WA': 'washington', 'WV': 'west virginia', 'WI': 'wisconsin', 'WY': 'wyoming',
    'PR': 'puerto rico', 'VI': 'virgin islands', 'GU': 'guam'
}

def extract_city_state_usace(port_name):
    """
    Extract city and state from USACE PORT_NAME
    Handles various formats:
    - "Port of Houston, TX"
    - "Houston Ship Channel, TX"
    - "Port Authority of New York and New Jersey, NY & NJ"
    Returns (city, state_abbrev)
    """
    if pd.isna(port_name):
        return ('', '')

    # Extract state abbreviation (last 2 capital letters before possible comma/period)
    state_match = re.search(r',\s*([A-Z]{2})(?:\s*&\s*[A-Z]{2})?\s*$', port_name)
    if not state_match:
        return ('', '')
    state = state_match.group(1)

    # Remove state part to get city portion
    city_portion = port_name[:state_match.start()].strip()

    # Remove common port-related words
    city_portion = re.sub(r'^Port Authority of\s+', '', city_portion, flags=re.IGNORECASE)
    city_portion = re.sub(r'^Port of\s+', '', city_portion, flags=re.IGNORECASE)
    city_portion = re.sub(r'\s+Port Authority$', '', city_portion, flags=re.IGNORECASE)
    city_portion = re.sub(r'\s+Port District$', '', city_portion, flags=re.IGNORECASE)
    city_portion = re.sub(r'\s+Port Commission$', '', city_portion, flags=re.IGNORECASE)
    city_portion = re.sub(r'\s+Ship Channel$', '', city_portion, flags=re.IGNORECASE)
    city_portion = re.sub(r'\s+Harbor.*$', '', city_portion, flags=re.IGNORECASE)
    city_portion = re.sub(r'\s+River.*$', '', city_portion, flags=re.IGNORECASE)
    city_portion = re.sub(r'\s+of\s+.*$', '', city_portion, flags=re.IGNORECASE)
    city_portion = re.sub(r'\s+Regional.*$', '', city_portion, flags=re.IGNORECASE)
    city_portion = re.sub(r'\s+Unified.*$', '', city_portion, flags=re.IGNORECASE)
    city_portion = re.sub(r'\s+Authority$', '', city_portion, flags=re.IGNORECASE)
    city_portion = re.sub(r'\s+District$', '', city_portion, flags=re.IGNORECASE)

    # Clean up
    city = city_portion.strip().lower()
    city = re.sub(r'\s+', ' ', city)

    return (city, state)

def extract_city_state_census(sked_de):
    """
    Extract city and state from Census Sked_D_E
    Format: "Houston, Texas" or "New York, New York"
    Returns (city, state_abbrev)
    """
    if pd.isna(sked_de):
        return ('', '')

    # Split by comma
    parts = sked_de.split(',')
    if len(parts) < 2:
        return ('', '')

    city = parts[0].strip().lower()
    state_full = parts[1].strip().lower()

    # Find state abbreviation
    state_abbrev = ''
    for abbrev, full in state_abbrev_to_full.items():
        if state_full == full:
            state_abbrev = abbrev
            break

    return (city, state_abbrev)

# Extract cities and states
print('Extracting city and state information...')
usace_ports['city'], usace_ports['state'] = zip(*usace_ports['PORT_NAME'].apply(extract_city_state_usace))
df_census['city'], df_census['state'] = zip(*df_census['Sked_D_E'].apply(extract_city_state_census))
print()

# Attempt matching
print('Matching ports...')
mapping = []
manual_override = {
    # Major ports with official names that don't match simple pattern
    '398': '1001',   # NY & NJ → New York
    '2031': '5301',  # Houston Authority → Houston
    '4722': '3001',  # Seattle Port → Seattle
    '4110': '2709',  # Long Beach Port → Long Beach
    '4120': '2704',  # LA Port → Los Angeles
    # High-volume unmatched ports (from traffic analysis)
    '1992': '5201',  # PortMiami → Miami
    '5700': '1401',  # Port of Virginia → Norfolk
    '2160': '1816',  # Canaveral Port District → Port Canaveral
    '1983': '5204',  # Port of Palm Beach District → West Palm Beach
    '2252': '2004',  # Port of Greater Baton Rouge → Baton Rouge
    '1989': '5101',  # VI Port Authority - St. Thomas → Charlotte Amalie
    '2443': '5104',  # VI Port Authority - St. Croix → Christiansted
    '3924': '3510',  # Duluth-Superior → Duluth
    '4421': '3201',  # Honolulu, O'ahu → Honolulu
    '3217': '4101',  # Cleveland-Cuyahoga County → Cleveland
    '3204': '4105',  # Toledo-Lucas County → Toledo
    '3743': '3905',  # Northern Indiana Maritime District → Gary
    '3749': '3901',  # Illinois International Port District → Chicago
}

for _, usace_row in usace_ports.iterrows():
    usace_port = str(usace_row['PORT'])
    usace_name = usace_row['PORT_NAME']
    usace_city = usace_row['city']
    usace_state = usace_row['state']

    # Check manual override first
    if usace_port in manual_override:
        census_code = manual_override[usace_port]
        census_row = df_census[df_census['Code'] == census_code].iloc[0]
        mapping.append({
            'USACE_PORT': usace_port,
            'USACE_PORT_NAME': usace_name,
            'Census_Code': census_row['Code'],
            'Census_Sked_D_E': census_row['Sked_D_E'],
            'Port_Consolidated': census_row['Port_Consolidated'],
            'Port_Coast': census_row['Port_Coast'],
            'Port_Region': census_row['Port_Region'],
            'Match_Type': 'Manual Override',
            'State': usace_state
        })
        continue

    # Try exact city + state match
    if usace_city and usace_state:
        exact_match = df_census[(df_census['city'] == usace_city) & (df_census['state'] == usace_state)]
        if len(exact_match) > 0:
            # Prefer non-Land Ports
            water_ports = exact_match[exact_match['Port_Consolidated'] != 'Land Ports']
            if len(water_ports) > 0:
                census_row = water_ports.iloc[0]
            else:
                census_row = exact_match.iloc[0]

            mapping.append({
                'USACE_PORT': usace_port,
                'USACE_PORT_NAME': usace_name,
                'Census_Code': census_row['Code'],
                'Census_Sked_D_E': census_row['Sked_D_E'],
                'Port_Consolidated': census_row['Port_Consolidated'],
                'Port_Coast': census_row['Port_Coast'],
                'Port_Region': census_row['Port_Region'],
                'Match_Type': 'City+State Exact',
                'State': usace_state
            })
            continue

    # Try fuzzy city match within same state
    if usace_city and usace_state:
        # Split city into words and try matching on first word
        city_words = usace_city.split()
        if city_words:
            first_word = city_words[0]
            fuzzy_match = df_census[(df_census['city'].str.startswith(first_word)) & (df_census['state'] == usace_state)]
            if len(fuzzy_match) > 0:
                # Prefer non-Land Ports
                water_ports = fuzzy_match[fuzzy_match['Port_Consolidated'] != 'Land Ports']
                if len(water_ports) > 0:
                    census_row = water_ports.iloc[0]
                else:
                    census_row = fuzzy_match.iloc[0]

                mapping.append({
                    'USACE_PORT': usace_port,
                    'USACE_PORT_NAME': usace_name,
                    'Census_Code': census_row['Code'],
                    'Census_Sked_D_E': census_row['Sked_D_E'],
                    'Port_Consolidated': census_row['Port_Consolidated'],
                    'Port_Coast': census_row['Port_Coast'],
                    'Port_Region': census_row['Port_Region'],
                    'Match_Type': 'City Fuzzy+State',
                    'State': usace_state
                })
                continue

    # No match found - try state-level fallback
    mapping.append({
        'USACE_PORT': usace_port,
        'USACE_PORT_NAME': usace_name,
        'Census_Code': '',
        'Census_Sked_D_E': '',
        'Port_Consolidated': '',
        'Port_Coast': '',
        'Port_Region': '',
        'Match_Type': 'NO MATCH',
        'State': usace_state
    })

df_mapping = pd.DataFrame(mapping)

# Apply state-level fallback for unmatched ports
print('Applying state-level fallback for unmatched ports...')
no_match = df_mapping[df_mapping['Match_Type'] == 'NO MATCH'].copy()
state_fallback_count = 0

for idx, row in no_match.iterrows():
    state = row['State']
    if not state:
        continue

    # Find matched ports in same state
    same_state_matched = df_mapping[
        (df_mapping['State'] == state) &
        (df_mapping['Match_Type'] != 'NO MATCH') &
        (df_mapping['Port_Consolidated'] != 'Land Ports')  # Exclude land ports
    ]

    if len(same_state_matched) > 0:
        # Get most common Port_Consolidated, Port_Coast, Port_Region in this state
        most_common = same_state_matched.groupby(['Port_Consolidated', 'Port_Coast', 'Port_Region']).size().idxmax()

        df_mapping.at[idx, 'Port_Consolidated'] = most_common[0]
        df_mapping.at[idx, 'Port_Coast'] = most_common[1]
        df_mapping.at[idx, 'Port_Region'] = most_common[2]
        df_mapping.at[idx, 'Match_Type'] = 'State Fallback'
        state_fallback_count += 1

print(f'  Applied state fallback to {state_fallback_count} ports')
print()

# Statistics
total = len(df_mapping)
matched = len(df_mapping[df_mapping['Match_Type'] != 'NO MATCH'])
print(f'  Matched: {matched} / {total} ({matched/total*100:.1f}%)')
print()

# By match type
print('Match type breakdown:')
for match_type, count in df_mapping['Match_Type'].value_counts().sort_index().items():
    print(f'  {match_type}: {count} ({count/total*100:.1f}%)')
print()

# Save mapping (drop State column - it was only used for fallback logic)
output_file = dict_path / 'usace_to_census_port_mapping.csv'
df_mapping.drop(columns=['State'], errors='ignore').to_csv(output_file, index=False)
print(f'Mapping saved to: {output_file}')
print()

# Show unmatched ports
no_match = df_mapping[df_mapping['Match_Type'] == 'NO MATCH']
if len(no_match) > 0:
    print('=' * 100)
    print(f'UNMATCHED PORTS ({len(no_match)} ports)')
    print('=' * 100)
    for _, row in no_match.head(50).iterrows():
        print(f"  PORT {row['USACE_PORT']}: {row['USACE_PORT_NAME']}")
    if len(no_match) > 50:
        print(f'  ... and {len(no_match) - 50} more')
    print()
else:
    print('All ports matched successfully!')
    print()

print('=' * 100)
