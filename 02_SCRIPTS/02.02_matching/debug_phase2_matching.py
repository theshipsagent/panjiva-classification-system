"""Debug why Phase 2 rules aren't matching Phase 5 records"""
import pandas as pd

df = pd.read_csv('../03_DOCUMENTATION/03.04_summaries/sample_test_15k/sample_15k_classified_v3.2.0.csv', dtype=str)
df_dict = pd.read_csv('../01_DICTIONARIES/03.01_cargo_classification/cargo_classification_dictionary_v3.2.0_20260114_0300.csv', dtype=str)

print('=== WHY PHASE 2 NOT MATCHING ===')
print()

# Get Phase 5 records for HS4=7214
phase5_7214 = df[(df['Classified_Phase'] == '5') & (df['HS4'] == '7214')]
print(f'Phase 5 records with HS4=7214: {len(phase5_7214)}')
print()

if len(phase5_7214) > 0:
    # Get sample record
    sample = phase5_7214.iloc[0]

    print('SAMPLE RECORD (HS4=7214):')
    print(f'  Goods: {sample["Goods Shipped"][:60]}')
    print(f'  HS2: {sample.get("HS2", "")}')
    print(f'  HS4: {sample.get("HS4", "")}')
    print(f'  HS6: {sample.get("HS6", "")}')
    print(f'  Tons: {sample.get("Tons", "")}')
    print(f'  Vessel Type: {sample.get("Vessel_Type_Simple", "")}')
    print(f'  Carrier: {sample.get("Carrier", "")}')
    print(f'  Group: {sample.get("Group", "")}')
    print(f'  Commodity: {sample.get("Commodity", "")}')
    print()

    # Check Phase 2 rules for HS4=7214
    phase2 = df_dict[df_dict['Phase'] == '2']
    rules_7214 = phase2[phase2['HS4'] == '7214']

    print(f'PHASE 2 RULES FOR HS4=7214: {len(rules_7214)}')
    print()

    if len(rules_7214) > 0:
        rule = rules_7214.iloc[0]

        print('PHASE 2 RULE REQUIREMENTS:')
        print(f'  Rule ID: {rule["Rule_ID"]}')
        print(f'  HS2: {rule.get("HS2", "")}')
        print(f'  HS4: {rule.get("HS4", "")}')
        print(f'  HS6: {rule.get("HS6", "")}')
        print(f'  Keywords: {rule.get("Keywords", "")}')
        print(f'  Vessel_Type: {rule.get("Vessel_Type", "")}')
        print(f'  Min_Tons: {rule.get("Min_Tons", "")}')
        print(f'  Max_Tons: {rule.get("Max_Tons", "")}')
        print(f'  Group: {rule.get("Group", "")}')
        print(f'  Commodity: {rule.get("Commodity", "")}')
        print()

        # Check why no match
        print('MATCHING ANALYSIS:')

        # Check HS codes
        sample_hs2 = str(sample.get('HS2', '')).strip()
        sample_hs4 = str(sample.get('HS4', '')).strip()
        rule_hs2 = str(rule.get('HS2', '')).strip()
        rule_hs4 = str(rule.get('HS4', '')).strip()

        if rule_hs2 and rule_hs2 != 'nan':
            if sample_hs2 == rule_hs2:
                print(f'  HS2 match: {sample_hs2} == {rule_hs2} OK')
            else:
                print(f'  HS2 NO MATCH: {sample_hs2} != {rule_hs2} FAIL')

        if rule_hs4 and rule_hs4 != 'nan':
            if sample_hs4 == rule_hs4:
                print(f'  HS4 match: {sample_hs4} == {rule_hs4} OK')
            else:
                print(f'  HS4 NO MATCH: {sample_hs4} != {rule_hs4} FAIL')

        # Check keywords
        rule_kw = str(rule.get('Keywords', '')).strip()
        if rule_kw and rule_kw != 'nan' and rule_kw != '':
            cargo_desc = str(sample.get('Goods Shipped', '')).upper()
            keyword_list = [k.strip().upper() for k in rule_kw.split(';')]
            has_match = any(kw in cargo_desc for kw in keyword_list)
            if has_match:
                print(f'  Keywords: Found in cargo description OK')
            else:
                print(f'  Keywords: NOT found in cargo description FAIL')
                print(f'    Required: {keyword_list}')
                print(f'    Cargo: {cargo_desc[:60]}')
        else:
            print('  Keywords: (none required)')

        # Check vessel type
        rule_vtype = str(rule.get('Vessel_Type', '')).strip()
        if rule_vtype and rule_vtype != 'nan' and rule_vtype != '':
            sample_vtype = str(sample.get('Vessel_Type_Simple', '')).upper()
            vessel_types = [v.strip().upper() for v in rule_vtype.split(';')]
            has_match = any(vt in sample_vtype for vt in vessel_types)
            if has_match:
                print(f'  Vessel Type: Match OK')
            else:
                print(f'  Vessel Type: NO MATCH FAIL')
                print(f'    Required: {vessel_types}')
                print(f'    Record: {sample_vtype}')
        else:
            print('  Vessel Type: (none required)')
