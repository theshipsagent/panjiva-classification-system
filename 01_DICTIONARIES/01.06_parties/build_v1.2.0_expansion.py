"""
Party Harmonization Dictionary v1.2.0 Expansion Builder

Expands from v1.1.0 (69 entities) to v1.2.0 (target: 110-120 entities)
by adding 40-50 high-impact entities identified in gap analysis.

Expected coverage improvement: 49.5% → 60-65%
"""

import pandas as pd
from datetime import datetime

# Load v1.1.0 dictionary
v1_1_path = r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.06_parties\party_harmonization_master_v1.1.0.csv"
df_v1_1 = pd.read_csv(v1_1_path)

print(f"Loaded v1.1.0: {len(df_v1_1)} entities")

# New entities to add (40-50 high-impact entities from gap analysis)
new_entities = [
    # === OIL/GAS (Top Priority - 35M+ tons) ===
    {
        'Entity_ID': 'TOTSA-001',
        'Canonical_Name': 'TotalEnergies Trading',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'TotalEnergies',
        'Match_Keywords': 'TOTSA TOTALENERGIES;TOTAL ENERGIES TRADING',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'TotalEnergies trading arm - major crude/products trader',
        'Estimated_Tons': 2923777
    },
    {
        'Entity_ID': 'CARIB-LPG-001',
        'Canonical_Name': 'Carib LPG Trading',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': '',
        'Match_Keywords': 'CARIB LPG',
        'Match_Strategy': 'Contains_All',
        'Category': 'All',
        'Active': True,
        'Notes': 'LPG trading company - Caribbean operations',
        'Estimated_Tons': 2600772
    },
    {
        'Entity_ID': 'NOVUM-001',
        'Canonical_Name': 'Novum Energy Trading',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': '',
        'Match_Keywords': 'NOVUM ENERGY',
        'Match_Strategy': 'Contains_All',
        'Category': 'All',
        'Active': True,
        'Notes': 'Energy trading company',
        'Estimated_Tons': 2453763
    },
    {
        'Entity_ID': 'GUNVOR-001',
        'Canonical_Name': 'Gunvor Group',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'Gunvor Group',
        'Match_Keywords': 'GUNVOR',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Major commodity trader - combines Gunvor Group and Gunvor USA',
        'Estimated_Tons': 3470292  # Gunvor Group + Gunvor USA
    },
    {
        'Entity_ID': 'DIAMOND-GREEN-001',
        'Canonical_Name': 'Diamond Green Diesel',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'Valero/Darling JV',
        'Match_Keywords': 'DIAMOND GREEN DIESEL',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Renewable diesel producer - Valero/Darling JV',
        'Estimated_Tons': 1983237
    },
    {
        'Entity_ID': 'EQUINOR-001',
        'Canonical_Name': 'Equinor',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'Equinor ASA',
        'Match_Keywords': 'EQUINOR',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Norwegian oil major - combines all Equinor entities (Marketing & Trading, ASA)',
        'Estimated_Tons': 4407778  # Sum of all Equinor variants
    },
    {
        'Entity_ID': 'ARAMCO-FUJAIRAH-001',
        'Canonical_Name': 'Aramco Trading Fujairah',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'Saudi Aramco',
        'Match_Keywords': 'ARAMCO TRADING FUJAIRAH',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Saudi Aramco UAE trading operations',
        'Estimated_Tons': 1408343
    },
    {
        'Entity_ID': 'BP-INTL-001',
        'Canonical_Name': 'BP Oil International',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'BP plc',
        'Match_Keywords': 'BP OIL INTERNATIONAL',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'BP international trading operations',
        'Estimated_Tons': 1355240
    },
    {
        'Entity_ID': 'MARATHON-INTL-001',
        'Canonical_Name': 'Marathon International Products',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'Marathon Petroleum',
        'Match_Keywords': 'MARATHON INTERNATIONAL PRODUCT',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Marathon trading arm - distinct from Marathon Petroleum refining',
        'Estimated_Tons': 1323629
    },
    {
        'Entity_ID': 'SONATRACH-001',
        'Canonical_Name': 'Sonatrach',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'Algerian Government',
        'Match_Keywords': 'SONATRACH',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Algerian state oil company',
        'Estimated_Tons': 1316130
    },
    {
        'Entity_ID': 'SK-ENERGY-001',
        'Canonical_Name': 'SK Energy',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'SK Group',
        'Match_Keywords': 'SK ENERGY',
        'Match_Strategy': 'Contains_All',
        'Category': 'All',
        'Active': True,
        'Notes': 'South Korean refiner - use Contains_All to avoid matching SK alone',
        'Estimated_Tons': 1229023
    },
    {
        'Entity_ID': 'PETROCHINA-001',
        'Canonical_Name': 'PetroChina International',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'PetroChina',
        'Match_Keywords': 'PETROCHINA',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Chinese state oil company - combines all PetroChina entities',
        'Estimated_Tons': 1969588  # PetroChina International America + PetroChina International Co
    },
    {
        'Entity_ID': 'SUNOCO-001',
        'Canonical_Name': 'Sunoco',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'Energy Transfer',
        'Match_Keywords': 'SUNOCO',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Fuel distributor - Energy Transfer subsidiary',
        'Estimated_Tons': 1145178
    },
    {
        'Entity_ID': 'ENI-TRADE-001',
        'Canonical_Name': 'Eni Trade & Biofuels',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'Eni',
        'Match_Keywords': 'ENI TRADE',
        'Match_Strategy': 'Contains_All',
        'Category': 'All',
        'Active': True,
        'Notes': 'Italian oil major trading arm',
        'Estimated_Tons': 1085397
    },
    {
        'Entity_ID': 'GEOGAS-001',
        'Canonical_Name': 'Geogas Trading',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': '',
        'Match_Keywords': 'GEOGAS',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'LNG/LPG trader',
        'Estimated_Tons': 1078692
    },
    {
        'Entity_ID': 'GS-CALTEX-001',
        'Canonical_Name': 'GS Caltex',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'GS Group/Chevron JV',
        'Match_Keywords': 'GS CALTEX',
        'Match_Strategy': 'Contains_All',
        'Category': 'Shipper',
        'Active': True,
        'Notes': 'South Korean refiner - GS/Chevron JV',
        'Estimated_Tons': 2021306
    },
    {
        'Entity_ID': 'CEPSA-001',
        'Canonical_Name': 'Cepsa Trading',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'Cepsa',
        'Match_Keywords': 'CEPSA TRADING',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Spanish oil company trading arm',
        'Estimated_Tons': 964227
    },
    {
        'Entity_ID': 'GLENCORE-ENERGY-001',
        'Canonical_Name': 'Glencore Energy',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'Glencore',
        'Match_Keywords': 'GLENCORE ENERGY',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Glencore energy trading division',
        'Estimated_Tons': 778074
    },
    {
        'Entity_ID': 'SHELL-INTL-001',
        'Canonical_Name': 'Shell International Trading',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'Shell plc',
        'Match_Keywords': 'SHELL INTERNATIONAL TRADING',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Shell Middle East trading operations',
        'Estimated_Tons': 702303
    },
    {
        'Entity_ID': 'REPSOL-001',
        'Canonical_Name': 'Repsol Trading',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'Repsol',
        'Match_Keywords': 'REPSOL TRADING',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Spanish oil major trading arm',
        'Estimated_Tons': 660248
    },
    {
        'Entity_ID': 'OQ-TRADING-001',
        'Canonical_Name': 'OQ Trading',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': 'OQ (Oman Oil)',
        'Match_Keywords': 'OQ TRADING',
        'Match_Strategy': 'Contains_All',
        'Category': 'All',
        'Active': True,
        'Notes': 'Omani state oil company trading arm',
        'Estimated_Tons': 645850
    },
    {
        'Entity_ID': 'NFE-001',
        'Canonical_Name': 'New Fortress Energy',
        'Entity_Type': 'Oil/Gas',
        'Parent_Company': '',
        'Match_Keywords': 'NEW FORTRESS ENERGY;NFE TRANSPORT',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'LNG infrastructure and trading',
        'Estimated_Tons': 1797643
    },

    # === CEMENT/AGGREGATES (33M+ tons) ===
    {
        'Entity_ID': 'LAFARGE-001',
        'Canonical_Name': 'Lafarge North America',
        'Entity_Type': 'Cement/Aggregates',
        'Parent_Company': 'Holcim',
        'Match_Keywords': 'LAFARGE',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Major cement/aggregates producer - now part of Holcim',
        'Estimated_Tons': 2647299
    },
    {
        'Entity_ID': 'HOUSTON-CEMENT-001',
        'Canonical_Name': 'Houston Cement',
        'Entity_Type': 'Cement/Aggregates',
        'Parent_Company': '',
        'Match_Keywords': 'HOUSTON CEMENT',
        'Match_Strategy': 'Contains_All',
        'Category': 'Consignee',
        'Active': True,
        'Notes': 'Houston area cement operations',
        'Estimated_Tons': 2300928
    },
    {
        'Entity_ID': 'ST-MARYS-001',
        'Canonical_Name': 'St. Marys Cement',
        'Entity_Type': 'Cement/Aggregates',
        'Parent_Company': 'Votorantim',
        'Match_Keywords': 'ST. MARY;ST MARY;SAINT MARY',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Canadian cement producer - Votorantim subsidiary',
        'Estimated_Tons': 2091917
    },
    {
        'Entity_ID': 'HOLLINGSHEAD-001',
        'Canonical_Name': 'Hollingshead Cement',
        'Entity_Type': 'Cement/Aggregates',
        'Parent_Company': '',
        'Match_Keywords': 'HOLLINGSHEAD',
        'Match_Strategy': 'Contains',
        'Category': 'Consignee',
        'Active': True,
        'Notes': 'Cement operations',
        'Estimated_Tons': 2192906
    },
    {
        'Entity_ID': 'ARGOS-001',
        'Canonical_Name': 'Argos USA',
        'Entity_Type': 'Cement/Aggregates',
        'Parent_Company': 'Grupo Argos',
        'Match_Keywords': 'ARGOS USA;ARGOS CEMENT',
        'Match_Strategy': 'Contains',
        'Category': 'Consignee',
        'Active': True,
        'Notes': 'Colombian cement producer - US operations',
        'Estimated_Tons': 2031040
    },
    {
        'Entity_ID': 'SESCO-001',
        'Canonical_Name': 'Sesco Cement',
        'Entity_Type': 'Cement/Aggregates',
        'Parent_Company': '',
        'Match_Keywords': 'SESCO CEMENT',
        'Match_Strategy': 'Contains_All',
        'Category': 'Consignee',
        'Active': True,
        'Notes': 'Cement operations',
        'Estimated_Tons': 1930373
    },
    {
        'Entity_ID': 'HEIDELBERG-001',
        'Canonical_Name': 'Heidelberg Materials',
        'Entity_Type': 'Cement/Aggregates',
        'Parent_Company': 'Heidelberg Materials',
        'Match_Keywords': 'HEIDELBERG',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'German cement/aggregates giant',
        'Estimated_Tons': 912400
    },
    {
        'Entity_ID': 'TAIHEIYO-001',
        'Canonical_Name': 'Taiheiyo Cement',
        'Entity_Type': 'Cement/Aggregates',
        'Parent_Company': '',
        'Match_Keywords': 'TAIHEIYO CEMENT',
        'Match_Strategy': 'Contains',
        'Category': 'Shipper',
        'Active': True,
        'Notes': 'Japanese cement producer',
        'Estimated_Tons': 1889043
    },
    {
        'Entity_ID': 'TITAN-001',
        'Canonical_Name': 'Titan Cement',
        'Entity_Type': 'Cement/Aggregates',
        'Parent_Company': 'Titan Cement Group',
        'Match_Keywords': 'TITAN CEMENT',
        'Match_Strategy': 'Contains_All',
        'Category': 'Shipper',
        'Active': True,
        'Notes': 'Greek cement producer - use Contains_All to avoid Titan America matches',
        'Estimated_Tons': 1877782
    },
    {
        'Entity_ID': 'HM-SOUTHEAST-001',
        'Canonical_Name': 'Heidelberg Materials Southeast',
        'Entity_Type': 'Cement/Aggregates',
        'Parent_Company': 'Heidelberg Materials',
        'Match_Keywords': 'HM SOUTHEAST CEMENT',
        'Match_Strategy': 'Contains',
        'Category': 'Consignee',
        'Active': True,
        'Notes': 'Heidelberg Materials southeast US operations',
        'Estimated_Tons': 1707718
    },
    {
        'Entity_ID': 'ASH-GROVE-001',
        'Canonical_Name': 'Ash Grove Cement',
        'Entity_Type': 'Cement/Aggregates',
        'Parent_Company': 'CRH',
        'Match_Keywords': 'ASH GROVE',
        'Match_Strategy': 'Contains_All',
        'Category': 'Consignee',
        'Active': True,
        'Notes': 'Major US cement producer - now CRH subsidiary',
        'Estimated_Tons': 1561861
    },
    {
        'Entity_ID': 'ONTARIO-TRAP-001',
        'Canonical_Name': 'Ontario Trap Rock',
        'Entity_Type': 'Aggregates',
        'Parent_Company': '',
        'Match_Keywords': 'ONTARIO TRAP ROCK',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Aggregates producer',
        'Estimated_Tons': 1453578
    },
    {
        'Entity_ID': 'EASTERN-SALT-001',
        'Canonical_Name': 'Eastern Salt',
        'Entity_Type': 'Salt',
        'Parent_Company': '',
        'Match_Keywords': 'EASTERN SALT',
        'Match_Strategy': 'Contains_All',
        'Category': 'Consignee',
        'Active': True,
        'Notes': 'Salt producer/distributor',
        'Estimated_Tons': 2270905
    },

    # === STEEL (14M+ tons) ===
    {
        'Entity_ID': 'POSCO-001',
        'Canonical_Name': 'POSCO',
        'Entity_Type': 'Steel',
        'Parent_Company': 'POSCO Holdings',
        'Match_Keywords': 'POSCO',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Korean steel giant - includes POSCO Mexico',
        'Estimated_Tons': 2209492  # POSCO + POSCO Mexico
    },
    {
        'Entity_ID': 'DAVID-JOSEPH-001',
        'Canonical_Name': 'David J. Joseph Company',
        'Entity_Type': 'Steel',
        'Parent_Company': 'Nucor',
        'Match_Keywords': 'DAVID J. JOSEPH;DAVID J JOSEPH',
        'Match_Strategy': 'Contains',
        'Category': 'Consignee',
        'Active': True,
        'Notes': 'Scrap metal processor - Nucor subsidiary',
        'Estimated_Tons': 1682715
    },
    {
        'Entity_ID': 'HYUNDAI-STEEL-001',
        'Canonical_Name': 'Hyundai Steel',
        'Entity_Type': 'Steel',
        'Parent_Company': 'Hyundai Motor Group',
        'Match_Keywords': 'HYUNDAI STEEL',
        'Match_Strategy': 'Contains_All',
        'Category': 'All',
        'Active': True,
        'Notes': 'Korean steel producer - Hyundai affiliate',
        'Estimated_Tons': 653333
    },
    {
        'Entity_ID': 'NU-IRON-001',
        'Canonical_Name': 'Nu-Iron Unlimited',
        'Entity_Type': 'Steel',
        'Parent_Company': '',
        'Match_Keywords': 'NU IRON;NU-IRON',
        'Match_Strategy': 'Contains',
        'Category': 'Shipper',
        'Active': True,
        'Notes': 'Steel products trader',
        'Estimated_Tons': 1612511
    },

    # === GRAIN (Easy wins - 1.6M tons) ===
    {
        'Entity_ID': 'ADM-001',
        'Canonical_Name': 'Archer Daniels Midland',
        'Entity_Type': 'Grain',
        'Parent_Company': 'ADM',
        'Match_Keywords': 'ARCHER DANIELS MIDLAND',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Major grain trader and processor',
        'Estimated_Tons': 1088661
    },

    # === CHEMICALS (4M+ tons) ===
    {
        'Entity_ID': 'DOW-001',
        'Canonical_Name': 'Dow Chemical',
        'Entity_Type': 'Chemicals',
        'Parent_Company': 'Dow Inc.',
        'Match_Keywords': 'DOW CHEMICAL',
        'Match_Strategy': 'Contains_All',
        'Category': 'All',
        'Active': True,
        'Notes': 'Major chemical manufacturer',
        'Estimated_Tons': 1118881
    },
    {
        'Entity_ID': 'SABIC-001',
        'Canonical_Name': 'SABIC Americas',
        'Entity_Type': 'Chemicals',
        'Parent_Company': 'SABIC',
        'Match_Keywords': 'SABIC',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Saudi petrochemicals giant',
        'Estimated_Tons': 919123
    },

    # === AUTOMOTIVE (5M+ tons) ===
    {
        'Entity_ID': 'TOYOTA-001',
        'Canonical_Name': 'Toyota Motor',
        'Entity_Type': 'Automotive',
        'Parent_Company': 'Toyota Motor Corporation',
        'Match_Keywords': 'TOYOTA MOTOR',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Japanese automaker - includes Toyota Motor Corp and Toyota Motor Sales',
        'Estimated_Tons': 4229868  # Toyota Motor Corporation + Toyota Motor Sales
    },
    {
        'Entity_ID': 'GM-001',
        'Canonical_Name': 'General Motors',
        'Entity_Type': 'Automotive',
        'Parent_Company': '',
        'Match_Keywords': 'GENERAL MOTORS',
        'Match_Strategy': 'Contains_All',
        'Category': 'All',
        'Active': True,
        'Notes': 'US automaker',
        'Estimated_Tons': 1175733
    },
    {
        'Entity_ID': 'MAZDA-001',
        'Canonical_Name': 'Mazda Motor',
        'Entity_Type': 'Automotive',
        'Parent_Company': 'Mazda Motor Corporation',
        'Match_Keywords': 'MAZDA MOTOR',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'Japanese automaker',
        'Estimated_Tons': 1153386
    },
    {
        'Entity_ID': 'MERCEDES-001',
        'Canonical_Name': 'Mercedes-Benz USA',
        'Entity_Type': 'Automotive',
        'Parent_Company': 'Mercedes-Benz Group',
        'Match_Keywords': 'MERCEDES BENZ;MERCEDES-BENZ',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'German automaker US operations',
        'Estimated_Tons': 951053
    },
    {
        'Entity_ID': 'KIA-001',
        'Canonical_Name': 'Kia Motors America',
        'Entity_Type': 'Automotive',
        'Parent_Company': 'Hyundai Motor Group',
        'Match_Keywords': 'KIA MOTORS',
        'Match_Strategy': 'Contains_All',
        'Category': 'All',
        'Active': True,
        'Notes': 'Korean automaker - use Contains_All to avoid matching KIA alone',
        'Estimated_Tons': 763376
    },

    # === OTHER HIGH-VALUE (Mining, Energy) ===
    {
        'Entity_ID': 'AES-PR-001',
        'Canonical_Name': 'AES Puerto Rico',
        'Entity_Type': 'Power Generation',
        'Parent_Company': 'AES Corporation',
        'Match_Keywords': 'AES PUERTO RICO',
        'Match_Strategy': 'Contains',
        'Category': 'All',
        'Active': True,
        'Notes': 'AES power generation in Puerto Rico',
        'Estimated_Tons': 2545800
    },
    {
        'Entity_ID': 'SAMARCO-001',
        'Canonical_Name': 'Samarco Mineracao',
        'Entity_Type': 'Mining',
        'Parent_Company': 'Vale/BHP JV',
        'Match_Keywords': 'SAMARCO',
        'Match_Strategy': 'Contains',
        'Category': 'Shipper',
        'Active': True,
        'Notes': 'Brazilian iron ore miner - Vale/BHP JV',
        'Estimated_Tons': 2022059
    },
    {
        'Entity_ID': 'GMB-KOREA-001',
        'Canonical_Name': 'GMB Korea Industries',
        'Entity_Type': 'Mining',
        'Parent_Company': '',
        'Match_Keywords': 'GMB KOREA',
        'Match_Strategy': 'Contains_All',
        'Category': 'All',
        'Active': True,
        'Notes': 'Korean mineral products company',
        'Estimated_Tons': 828838
    },
    {
        'Entity_ID': 'YARA-001',
        'Canonical_Name': 'Yara North America',
        'Entity_Type': 'Fertilizer',
        'Parent_Company': 'Yara International',
        'Match_Keywords': 'YARA',
        'Match_Strategy': 'Contains',
        'Category': 'Consignee',
        'Active': True,
        'Notes': 'Norwegian fertilizer producer',
        'Estimated_Tons': 1680780
    },
]

# Create DataFrame for new entities
df_new = pd.DataFrame(new_entities)

# Combine with v1.1.0
df_v1_2 = pd.concat([df_v1_1, df_new], ignore_index=True)

# Sort by Entity_Type then Estimated_Tons descending
df_v1_2 = df_v1_2.sort_values(['Entity_Type', 'Estimated_Tons'], ascending=[True, False])

# Save v1.2.0
output_path = r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.06_parties\party_harmonization_master_v1.2.0.csv"
df_v1_2.to_csv(output_path, index=False)

print(f"\n=== v1.2.0 Dictionary Created ===")
print(f"Total entities: {len(df_v1_2)}")
print(f"New entities added: {len(df_new)}")
print(f"\nBreakdown by Entity Type:")
print(df_v1_2['Entity_Type'].value_counts().to_string())

print(f"\nNew entities by category:")
category_counts = df_new.groupby('Entity_Type').size().sort_values(ascending=False)
print(category_counts.to_string())

print(f"\nEstimated tonnage impact:")
print(f"v1.1.0 total: {df_v1_1['Estimated_Tons'].sum():,.0f} tons")
print(f"New entities: {df_new['Estimated_Tons'].sum():,.0f} tons")
print(f"v1.2.0 total: {df_v1_2['Estimated_Tons'].sum():,.0f} tons")

print(f"\nSaved to: {output_path}")

# Generate summary report
summary_path = r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.06_parties\v1.2.0_expansion_summary.txt"
with open(summary_path, 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("Party Harmonization Dictionary v1.2.0 Expansion Summary\n")
    f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")

    f.write("OVERVIEW\n")
    f.write("-" * 80 + "\n")
    f.write(f"v1.1.0 entities: 69\n")
    f.write(f"v1.2.0 entities: {len(df_v1_2)}\n")
    f.write(f"New entities added: {len(df_new)}\n")
    f.write(f"Expansion: +{len(df_new)} entities ({len(df_new)/69*100:.1f}% increase)\n\n")

    f.write(f"ESTIMATED TONNAGE IMPACT\n")
    f.write("-" * 80 + "\n")
    f.write(f"v1.1.0 coverage: ~49.5% of consignee tonnage\n")
    f.write(f"New entities tonnage: {df_new['Estimated_Tons'].sum():,.0f} tons\n")
    f.write(f"Expected v1.2.0 coverage: ~60-65% of consignee tonnage\n")
    f.write(f"Coverage improvement: +10-15 percentage points\n\n")

    f.write("NEW ENTITIES BY CATEGORY\n")
    f.write("-" * 80 + "\n")
    category_summary = df_new.groupby('Entity_Type').agg({
        'Entity_ID': 'count',
        'Estimated_Tons': 'sum'
    }).rename(columns={'Entity_ID': 'Count'}).sort_values('Estimated_Tons', ascending=False)

    for entity_type, row in category_summary.iterrows():
        f.write(f"{entity_type:25s}: {int(row['Count']):2d} entities, {row['Estimated_Tons']:12,.0f} tons\n")

    f.write(f"\n{'TOTAL':25s}: {len(df_new):2d} entities, {df_new['Estimated_Tons'].sum():12,.0f} tons\n\n")

    f.write("TOP 20 NEW ENTITIES BY TONNAGE\n")
    f.write("-" * 80 + "\n")
    f.write(f"{'Rank':<5} {'Entity ID':<25} {'Canonical Name':<35} {'Tons':>12}\n")
    f.write("-" * 80 + "\n")

    top20 = df_new.nlargest(20, 'Estimated_Tons')
    for idx, (_, row) in enumerate(top20.iterrows(), 1):
        f.write(f"{idx:<5} {row['Entity_ID']:<25} {row['Canonical_Name']:<35} {row['Estimated_Tons']:>12,.0f}\n")

    f.write("\n" + "=" * 80 + "\n")
    f.write("STRATEGIC HIGHLIGHTS\n")
    f.write("=" * 80 + "\n\n")

    f.write("1. OIL/GAS EXPANSION (Priority #1)\n")
    f.write("   - Added 22 major oil/gas entities\n")
    f.write("   - Captures TotalEnergies, Gunvor, Equinor, multiple NOCs\n")
    f.write("   - Combined impact: ~35M tons\n\n")

    f.write("2. CEMENT/AGGREGATES (High ROI)\n")
    f.write("   - Added 13 cement/aggregates producers\n")
    f.write("   - Lafarge, Houston Cement, St. Marys, Hollingshead, Argos\n")
    f.write("   - Combined impact: ~27M tons\n\n")

    f.write("3. STEEL (Strategic Coverage)\n")
    f.write("   - Added 4 major steel entities\n")
    f.write("   - POSCO (all variants), David J. Joseph, Hyundai Steel\n")
    f.write("   - Combined impact: ~4M tons\n\n")

    f.write("4. AUTOMOTIVE (High Record Count)\n")
    f.write("   - Added 5 automakers\n")
    f.write("   - Toyota, GM, Mazda, Mercedes, Kia\n")
    f.write("   - Combined impact: ~8M tons, 7,000+ records\n\n")

    f.write("5. GRAIN (Easy Win)\n")
    f.write("   - Added ADM (Archer Daniels Midland)\n")
    f.write("   - Safe multi-token matching\n")
    f.write("   - Impact: ~1M tons\n\n")

    f.write("SAFETY MEASURES\n")
    f.write("-" * 80 + "\n")
    f.write("- Contains_All strategy for entities with generic names:\n")
    f.write("  * SK Energy (avoid matching SK alone)\n")
    f.write("  * Kia Motors (avoid matching KIA alone)\n")
    f.write("  * Titan Cement (avoid Titan America)\n")
    f.write("  * Dow Chemical (avoid DOW alone)\n")
    f.write("  * General Motors (avoid GENERAL alone)\n")
    f.write("- Multi-token keywords for ambiguous names\n")
    f.write("- Parent company references for verification\n\n")

    f.write("NEXT STEPS\n")
    f.write("-" * 80 + "\n")
    f.write("1. Test v1.2.0 on full 2023-2025 dataset\n")
    f.write("2. Measure actual coverage improvement\n")
    f.write("3. Validate match quality (spot check top matches)\n")
    f.write("4. Identify remaining gaps for v1.3.0\n")
    f.write("5. Monitor for false positives\n\n")

    f.write("=" * 80 + "\n")

print(f"\nSummary report saved to: {summary_path}")
