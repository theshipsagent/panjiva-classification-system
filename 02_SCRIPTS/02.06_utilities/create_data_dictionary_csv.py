import pandas as pd
import csv

# Load the port call master
df = pd.read_csv(r'G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_portcall_master_v1.2.0.csv', low_memory=False)

columns_data = []

for i, col in enumerate(df.columns, 1):
    # Get sample value
    sample = df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else ''

    # Determine source
    if col.startswith('Entrance_'):
        if 'Vessel_' in col or 'Draft_Pct' in col:
            source = 'Ship Registry / Derived'
        elif 'Panjiva' in col or 'VOY_RECID' in col:
            source = 'Panjiva Import'
        elif any(x in col for x in ['Port_Consolidated', 'Port_Coast', 'Port_Region', 'Date_Parsed', 'Match_Method']):
            source = 'Derived'
        else:
            source = 'USACE Entrance'
    elif col.startswith('Clearance_'):
        if 'Vessel_' in col or 'Draft_Pct' in col:
            source = 'Ship Registry / Derived'
        elif 'Panjiva' in col or 'VOY_RECID' in col:
            source = 'Panjiva Export'
        elif any(x in col for x in ['Port_Consolidated', 'Port_Coast', 'Port_Region', 'Date_Parsed', 'Match_Method']):
            source = 'Derived'
        else:
            source = 'USACE Clearance'
    elif col.startswith('Grain_') or col == 'FGIS_RECID' or col == 'Match_Quality':
        source = 'FGIS Grain Export'
    elif col == 'PORTCALL_ID':
        source = 'Derived - Unique ID'
    elif any(x in col for x in ['Match', 'Port_Stay', 'Tug_Barge', 'Pairing']):
        source = 'Derived - Matching'
    else:
        source = 'Derived'

    # Simple description
    desc = f'{col} from {source}'

    columns_data.append([i, col, str(sample)[:60], source, desc])

# Save to CSV
output = r'G:\My Drive\LLM\project_manifest\03_DOCUMENTATION/03.04_summaries\PORT_CALL_MASTER_DATA_DICTIONARY_v1.2.0.csv'
with open(output, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Column_Number', 'Column_Name', 'Sample_Value', 'Source', 'Description'])
    writer.writerows(columns_data)

print(f'Data dictionary saved: {output}')
print(f'Total columns: {len(columns_data)}')
