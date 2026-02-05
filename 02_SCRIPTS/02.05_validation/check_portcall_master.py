import pandas as pd

df = pd.read_csv(r"G:\My Drive\LLM\project_manifest\00_DATA/00.03_MATCHED\usace_2023_portcall_master_v1.0.0.csv", low_memory=False)

print(f"Total rows: {len(df):,}")
print(f"\nMatch_Type distribution:")
print(df['Match_Type'].value_counts())

print(f"\nSearching for HAMBURG CITY...")
hc = df[df['Entrance_Vessel'] == 'HAMBURG CITY']
print(f"Found {len(hc)} HAMBURG CITY entrance records")
if len(hc) > 0:
    print(hc[['PORTCALL_ID', 'Entrance_Vessel', 'Entrance_PORT', 'Entrance_Arrival_Date', 'Match_Type']].head())

# Check for any BOTH matches
both = df[df['Match_Type'] == 'BOTH']
print(f"\nTotal BOTH matches: {len(both)}")
if len(both) > 0:
    print("Sample BOTH matches:")
    print(both[['PORTCALL_ID', 'Entrance_Vessel', 'Entrance_PORT', 'Entrance_Arrival_Date', 'Match_Type']].head())
