"""
Quick Analysis: USACE Clearance by Region and Vessel Type
Shows ship counts and total agency fees
"""

import pandas as pd

print('=' * 100)
print('USACE CLEARANCE (OUTBOUND) ANALYSIS BY REGION AND VESSEL TYPE')
print('=' * 100)
print()

# Read data
df = pd.read_csv(r'G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_outbound_clearance_transformed_v2.2.0.csv')

print(f'Total Records: {len(df):,}')
print()

# Filter to records with Port_Region
df_with_region = df[df['Port_Region'].notna() & (df['Port_Region'] != '')]
print(f'Records with Port_Region: {len(df_with_region):,} ({len(df_with_region)/len(df)*100:.1f}%)')
print()

# Clean up Agency_Fee column (remove $ and commas, convert to numeric)
def clean_fee(fee_str):
    if pd.isna(fee_str) or fee_str == '':
        return 0
    # Remove $, commas, and convert to float
    return float(str(fee_str).replace('$', '').replace(',', ''))

df_with_region['Agency_Fee_Numeric'] = df_with_region['Agency_Fee'].apply(clean_fee)

# Group by Port_Region and ICST_DESC
grouped = df_with_region.groupby(['Port_Region', 'ICST_DESC']).agg({
    'RECID': 'count',
    'Agency_Fee_Numeric': 'sum'
}).rename(columns={'RECID': 'Ship_Count', 'Agency_Fee_Numeric': 'Total_Fees'})

# Get unique regions
regions = sorted(df_with_region['Port_Region'].unique())

print('=' * 100)
print('ANALYSIS BY REGION')
print('=' * 100)
print()

for region in regions:
    region_data = grouped.loc[region].sort_values('Ship_Count', ascending=False)

    total_ships = int(region_data['Ship_Count'].sum())
    total_fees = region_data['Total_Fees'].sum()

    print(f'REGION: {region}')
    print(f'Total Ships: {total_ships:,} | Total Fees: ${total_fees:,.0f}')
    print('-' * 100)
    print(f"{'Vessel Type':<45} {'Ships':>10} {'Pct':>8} {'Total Fees':>15} {'Avg Fee':>12}")
    print('-' * 100)

    for icst, row in region_data.head(15).iterrows():
        ship_count = int(row['Ship_Count'])
        total_fee = row['Total_Fees']
        pct = (ship_count / total_ships) * 100
        avg_fee = total_fee / ship_count if ship_count > 0 else 0
        print(f'{icst:<45} {ship_count:>10,} {pct:>7.1f}% ${total_fee:>13,.0f} ${avg_fee:>10,.0f}')

    if len(region_data) > 15:
        print(f'... and {len(region_data) - 15} more vessel types')

    print()

# Overall summary
print('=' * 100)
print('OVERALL SUMMARY BY REGION')
print('=' * 100)
print()

region_totals = df_with_region.groupby('Port_Region').agg({
    'RECID': 'count',
    'Agency_Fee_Numeric': 'sum'
}).rename(columns={'RECID': 'Ship_Count', 'Agency_Fee_Numeric': 'Total_Fees'}).sort_values('Total_Fees', ascending=False)

print(f"{'Region':<30} {'Ship Count':>15} {'Total Fees':>20} {'Avg Fee':>15}")
print('-' * 100)

for region, row in region_totals.iterrows():
    ship_count = int(row['Ship_Count'])
    total_fee = row['Total_Fees']
    avg_fee = total_fee / ship_count if ship_count > 0 else 0
    print(f'{region:<30} {ship_count:>15,} ${total_fee:>18,.0f} ${avg_fee:>13,.0f}')

print()
print('=' * 100)
