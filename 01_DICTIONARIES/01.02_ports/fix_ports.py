import pandas as pd

print("FIXING 00_ports_master.csv - filling all blanks...")

# Load master
master = pd.read_csv('00_ports_master.csv', dtype=str)
print(f"Total ports: {len(master)}")
print(f"Unmatched: {master['Port_Code'].isna().sum()}")

# Manual assignments for unmatched ports
fixes = {
    'Georgia Ports Authority, Savannah, Georgia': ('1701', 'Georgia Ports', 'East', 'South Atlantic'),
    'Philadelphia Regional Port Authority, Philadelphia, Pennsylvania': ('1101', 'Delaware River', 'East', 'Mid-Atlantic'),
    'Alabama State Port Authority, Mobile, Alabama': ('2002', 'Mobile', 'Gulf', 'Gulf East'),
    'Port of Virginia, Norfolk, Virginia': ('1501', 'Hampton Roads', 'East', 'South Atlantic'),
    'Port of Vancouver USA, Vancouver, Washington': ('3001', 'Columbia River', 'West', 'Pacific Northwest'),
    'Baton Rouge (BTR) Airport, Baton Rouge, Louisiana': ('2002', 'New Orleans', 'Gulf', 'Gulf East'),
    'Detroit/Wayne County Port Authority, Detroit, Michigan': ('3801', 'Great Lakes', 'Great Lakes', 'Great Lakes'),
    'ProvPort, Providence, Rhode Island': ('0601', 'Boston', 'East', 'North Atlantic'),
    'Port Of Entry-Port Everglades/Fort Lauderdale, Port Everglades, Florida': ('1801', 'South Florida', 'East', 'South Atlantic'),
    'Port Arthur, Texas': ('5301', 'Houston', 'Gulf', 'North Texas'),
    'Port Canaveral, Port Canaveral, Florida': ('1801', 'South Florida', 'East', 'South Atlantic'),
    'Port Of Entry-Miami Seaport, Miami, Florida': ('1801', 'South Florida', 'East', 'South Atlantic'),
    'Mississippi State Port Authority, Gulfport, Mississippi': ('2002', 'New Orleans', 'Gulf', 'Gulf East'),
    'Illinois International Port District, Chicago, Illinois': ('3801', 'Great Lakes', 'Great Lakes', 'Great Lakes'),
    'Service Port-San Francisco, San Francisco, California': ('2801', 'San Francisco Bay', 'West', 'California'),
    'Toledo-Lucas Port Authority, Toledo, Ohio': ('3801', 'Great Lakes', 'Great Lakes', 'Great Lakes'),
    'Port Hueneme, California': ('2704', 'LA-Long Beach', 'West', 'California'),
    'Sault Ste. Marie, Sault Ste Marie, Michigan': ('3801', 'Great Lakes', 'Great Lakes', 'Great Lakes'),
    'Port Of NewHampshire, Portsmouth, New Hampshire': ('0131', 'Boston', 'East', 'North Atlantic'),
    'Cyril E King Airport, Charlotte Amalie, Virgin Islands': ('5501', 'San Juan', 'East', 'South Atlantic'),
    'Service Port-Honolulu, Honolulu, Hawaii': ('3201', 'Honolulu', 'West', 'Pacific'),
    'Port of New Bedford Business Alliance, New Bedford, Massachusetts': ('0405', 'Boston', 'East', 'North Atlantic'),
    'Memphis, Memphis, Tennessee': ('2901', 'Lower Mississippi River', 'Gulf', 'Gulf East'),
    'Indiana Harbor, Indiana Harbor, Indiana': ('3801', 'Great Lakes', 'Great Lakes', 'Great Lakes'),
    'Port of Stockton, Stockton, California': ('2804', 'San Francisco Bay', 'West', 'California'),
    'Port Of Long Beach, Long Beach, California': ('2704', 'LA-Long Beach', 'West', 'California'),
    'Port Of Entry-Newark/Ny&Nj, Newark, New Jersey': ('1001', 'New York', 'East', 'North Atlantic'),
    'Lake Charles, Lake Charles, Louisiana': ('2001', 'New Orleans', 'Gulf', 'Gulf East'),
    'Savannah, Savannah, Georgia': ('1701', 'Georgia Ports', 'East', 'South Atlantic'),
    'Port Everglades, Port Everglades, Florida': ('1801', 'South Florida', 'East', 'South Atlantic'),
    'Cleveland, Cleveland, Ohio': ('3801', 'Great Lakes', 'Great Lakes', 'Great Lakes'),
    'Port of Wilmington, Wilmington, North Carolina': ('1704', 'North Carolina', 'East', 'South Atlantic'),
    'Searsport, Searsport, Maine': ('0152', 'Boston', 'East', 'North Atlantic'),
    'Green Bay, Green Bay, Wisconsin': ('3801', 'Great Lakes', 'Great Lakes', 'Great Lakes'),
    'Port of Everett, Everett, Washington': ('3010', 'Seattle-Tacoma', 'West', 'Pacific Northwest'),
    'Burns Harbor, Burns Harbor, Indiana': ('3801', 'Great Lakes', 'Great Lakes', 'Great Lakes'),
    'San Juan, San Juan, Puerto Rico': ('5501', 'San Juan', 'East', 'South Atlantic'),
    'Anchorage, Anchorage, Alaska': ('3301', 'Alaska', 'West', 'Alaska'),
    'Coos Bay, Coos Bay, Oregon': ('2901', 'Columbia River', 'West', 'Pacific Northwest'),
    'Kalama, Kalama, Washington': ('2904', 'Columbia River', 'West', 'Pacific Northwest'),
    'Cincinnati, Cincinnati, Ohio': ('3801', 'Great Lakes', 'Great Lakes', 'Great Lakes'),
    'Marcus Hook, Marcus Hook, Pennsylvania': ('1101', 'Delaware River', 'East', 'Mid-Atlantic'),
    'Pascagoula, Pascagoula, Mississippi': ('2002', 'Mobile', 'Gulf', 'Gulf East'),
    'Gloucester, Gloucester, Massachusetts': ('0404', 'Boston', 'East', 'North Atlantic'),
    'Grays Harbor, Grays Harbor, Washington': ('3001', 'Seattle-Tacoma', 'West', 'Pacific Northwest'),
    'St. Paul, St. Paul, Minnesota': ('2901', 'Upper Mississippi River', 'Gulf', 'Great Lakes'),
    'Milwaukee, Milwaukee, Wisconsin': ('3801', 'Great Lakes', 'Great Lakes', 'Great Lakes'),
    'Kenai, Kenai, Alaska': ('3301', 'Alaska', 'West', 'Alaska'),
    'Miami, Miami, Florida': ('1801', 'South Florida', 'East', 'South Atlantic'),
    'Eastport, Eastport, Maine': ('0103', 'Boston', 'East', 'North Atlantic'),
    'Ponce, Ponce, Puerto Rico': ('5501', 'San Juan', 'East', 'South Atlantic'),
}

# Apply fixes
for port_name, (code, consolidated, coast, region) in fixes.items():
    mask = master['Port of Discharge (D)'] == port_name
    if mask.any():
        master.loc[mask, 'Port_Code'] = code
        master.loc[mask, 'Port_Consolidated'] = consolidated
        master.loc[mask, 'Port_Coast'] = coast
        master.loc[mask, 'Port_Region'] = region

# Save
master.to_csv('00_ports_master.csv', index=False)

print(f"\nFIXED - Unmatched remaining: {master['Port_Code'].isna().sum()}")
