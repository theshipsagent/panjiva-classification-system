import pandas as pd
import numpy as np

# Load the reference data
print("Loading reference data...")
df = pd.read_csv(r"G:\My Drive\LLM\project_manifest\user_notes\hs_code_reference_complete.csv")

# Filter to HS2 codes 76, 78, 79, 80
print("Filtering to HS2 codes 76, 78, 79, 80...")
df['HS2'] = df['HS2'].astype(str).str.zfill(2)
metals_df = df[df['HS2'].isin(['76', '78', '79', '80'])].copy()

print(f"Found {len(metals_df)} rows for nonferrous metals")
print("\nHS2 distribution:")
print(metals_df['HS2'].value_counts().sort_index())

# Create dictionary with all required fields
print("\nBuilding specialized dictionary...")

dictionary = []

for _, row in metals_df.iterrows():
    hs2 = str(row['HS2']).zfill(2)
    hs4 = str(row['HS4']).zfill(4)

    # Determine metal type
    metal_map = {
        '76': 'Aluminum',
        '78': 'Lead',
        '79': 'Zinc',
        '80': 'Tin'
    }
    metal_type = metal_map.get(hs2, 'Unknown')

    # Determine if unwrought, scrap, or articles
    description = str(row['HTS_Description']).lower()

    if 'unwrought' in description or 'ingot' in description:
        form = 'Unwrought'
    elif 'waste' in description or 'scrap' in description:
        form = 'Scrap'
    elif 'powder' in description or 'flake' in description or 'dust' in description:
        form = 'Powder/Dust'
    elif 'plate' in description or 'sheet' in description or 'strip' in description or 'foil' in description:
        form = 'Flat Products'
    elif 'wire' in description or 'cable' in description:
        form = 'Wire Products'
    elif 'tube' in description or 'pipe' in description:
        form = 'Tubes/Pipes'
    elif 'bar' in description or 'rod' in description or 'profile' in description:
        form = 'Bars/Rods'
    else:
        form = 'Articles'

    # Build key phrases and keywords
    key_phrases_list = []
    primary_keywords = []

    # Add metal type
    primary_keywords.append(metal_type.upper())

    # Parse Key_Phrases if available
    if pd.notna(row.get('Key_Phrases')) and row['Key_Phrases']:
        phrases = str(row['Key_Phrases']).upper().split(', ')
        key_phrases_list.extend(phrases[:10])  # Limit to 10 terms

    # Add form-specific keywords
    if form == 'Unwrought':
        primary_keywords.extend(['INGOT', 'UNWROUGHT', 'BILLET'])
    elif form == 'Scrap':
        primary_keywords.extend(['SCRAP', 'WASTE'])
    elif form == 'Powder/Dust':
        primary_keywords.extend(['POWDER', 'DUST', 'FLAKE'])
    elif form == 'Flat Products':
        primary_keywords.extend(['SHEET', 'PLATE', 'FOIL', 'STRIP'])
    elif form == 'Wire Products':
        primary_keywords.extend(['WIRE', 'CABLE'])
    elif form == 'Tubes/Pipes':
        primary_keywords.extend(['TUBE', 'PIPE'])
    elif form == 'Bars/Rods':
        primary_keywords.extend(['BAR', 'ROD', 'PROFILE'])

    # Get package types from Top_Package_Types column
    package_types = []
    if pd.notna(row.get('Top_Package_Types')) and row['Top_Package_Types']:
        pkgs = str(row['Top_Package_Types']).split(', ')
        package_types.extend([p.strip() for p in pkgs[:5]])

    # Get tonnage info
    min_tons = row.get('Min_Tons', '')
    max_tons = row.get('Max_Tons', '')
    tonnage_range = f"{min_tons} - {max_tons}" if min_tons and max_tons else ''

    # Determine commodity classification
    if form == 'Unwrought':
        commodity = f"{metal_type} - Unwrought (Ingots/Billets)"
    elif form == 'Scrap':
        commodity = f"{metal_type} - Scrap/Waste"
    elif form == 'Powder/Dust':
        commodity = f"{metal_type} - Powder/Dust/Flakes"
    elif form == 'Flat Products':
        commodity = f"{metal_type} - Plates/Sheets/Foil"
    elif form == 'Wire Products':
        commodity = f"{metal_type} - Wire/Cable"
    elif form == 'Tubes/Pipes':
        commodity = f"{metal_type} - Tubes/Pipes"
    elif form == 'Bars/Rods':
        commodity = f"{metal_type} - Bars/Rods/Profiles"
    else:
        commodity = f"{metal_type} - Articles/Manufactured"

    # Determine cargo type based on form and package
    if form in ['Unwrought', 'Scrap']:
        cargo = 'Break Bulk - Metals'
    elif form == 'Powder/Dust':
        cargo = 'Bulk - Dry (Bagged)'
    else:
        cargo = 'General Cargo - Containerized'

    dictionary.append({
        'HS2': hs2,
        'HS4': hs4,
        'HTS_Description': row['HTS_Description'],
        'Metal_Type': metal_type,
        'Form': form,
        'Group': 'Dry Bulk',
        'Commodity': commodity,
        'Cargo': cargo,
        'Key_Phrases': ' | '.join(key_phrases_list[:10]),  # Limit phrases
        'Primary_Keywords': ', '.join(list(dict.fromkeys(primary_keywords))[:10]),  # Remove duplicates, limit
        'Package_Types': ', '.join(package_types[:5]),  # Limit to 5
        'Tonnage_Range': tonnage_range,
        'Record_Count': row.get('Record_Count', 0),
        'Total_Tonnage': row.get('Total_Tons', 0),
        'Top_Shippers': row.get('Top_Shippers', ''),
        'Top_Consignees': row.get('Top_Consignees', ''),
        'Top_Ports_Loading': row.get('Top_Ports_Loading', ''),
        'Top_Ports_Discharge': row.get('Top_Ports_Discharge', '')
    })

# Create DataFrame and sort by tonnage
dict_df = pd.DataFrame(dictionary)

# Convert Total_Tonnage to numeric for sorting
dict_df['Total_Tonnage'] = pd.to_numeric(dict_df['Total_Tonnage'], errors='coerce').fillna(0)
dict_df = dict_df.sort_values('Total_Tonnage', ascending=False)

# Save to CSV
output_path = r"G:\My Drive\LLM\project_manifest\user_notes\dictionary_hs76-79_nonferrous_metals.csv"
dict_df.to_csv(output_path, index=False)

print(f"\nDictionary saved to: {output_path}")
print(f"Total entries: {len(dict_df)}")

# Print summary statistics
print("\n=== SUMMARY STATISTICS ===")
print("\nBy Metal Type:")
print(dict_df.groupby('Metal_Type').agg({
    'Record_Count': 'sum',
    'Total_Tonnage': 'sum'
}).sort_values('Total_Tonnage', ascending=False))

print("\nBy Form:")
print(dict_df.groupby('Form').agg({
    'Record_Count': 'sum',
    'Total_Tonnage': 'sum'
}).sort_values('Total_Tonnage', ascending=False))

print("\nTop 15 by Tonnage:")
print(dict_df[['HS4', 'HTS_Description', 'Metal_Type', 'Form', 'Total_Tonnage', 'Record_Count']].head(15))

print("\nHS4 Code Distribution:")
print(dict_df.groupby('HS4').agg({
    'HTS_Description': 'first',
    'Metal_Type': 'first',
    'Record_Count': 'sum',
    'Total_Tonnage': 'sum'
}).sort_values('Total_Tonnage', ascending=False))
