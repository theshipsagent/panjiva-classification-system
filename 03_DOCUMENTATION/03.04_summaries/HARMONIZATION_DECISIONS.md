# Harmonization & Transformation Decisions
**Date:** 2026-01-28
**Status:** APPROVED

---

## Decision Summary

### ✅ APPROVED: Overwrite Shipper/Consignee (Best Practice)

**Method:** Transform in place, keep "(Original Format)" for audit

```
Before Transform:
├── Shipper: "ABC CORP"
├── Shipper (Original Format): "ABC CORP"
├── Consignee: "XYZ CO."
└── Consignee (Original Format): "XYZ CO."

After Transform:
├── Shipper: "ABC Corporation"           ← HARMONIZED
├── Shipper (Original Format): "ABC CORP" ← ORIGINAL (unchanged)
├── Consignee: "XYZ Company"              ← HARMONIZED
└── Consignee (Original Format): "XYZ CO." ← ORIGINAL (unchanged)
```

**Why this is best practice:**
- ✅ Original values preserved in "(Original Format)" columns
- ✅ Harmonized values in main columns (easier to work with)
- ✅ No duplicate "_Harmonized" columns cluttering schema
- ✅ Can always audit back to original
- ✅ Standard approach in data engineering

**Alternative (NOT chosen):**
```
❌ Create Shipper_Harmonized / Consignee_Harmonized columns
   - Would have 4 shipper columns, 4 consignee columns (8 total)
   - Schema bloat
   - Confusing which to use
```

---

## Decision: Quantity Split (Only Destructive Transform)

### ✅ APPROVED: Drop Quantity after splitting

**Original:** `Quantity = "3903 PCS"`

**Split:**
- `Qty = 3903` (integer)
- `Pckg = "PCS"` (text)

**Original column DROPPED after split**

**Why this is safe:**
- Can reconstruct: `str(Qty) + " " + Pckg` → "3903 PCS"
- Split is deterministic (always same result)
- Provides more value than original (can do math on Qty)
- Never need original format

**This is the ONLY transformation that destroys original data**

---

## Decision: REC_ID for Complete Audit Trail

### ✅ APPROVED: Add REC_ID as position 61 (last column)

**Format:** `{SOURCE}_{FILENAME}_{ROWNUMBER}`

**Examples:**
```
PANV_IMP_FILE001_R000123    (Panjiva import, file 1, row 123)
PANV_IMP_FILE042_R005678    (Panjiva import, file 42, row 5678)
PANV_EXP_FILE003_R000045    (Panjiva export, file 3, row 45)
```

**Why:**
- Can trace EVERY row back to original raw file + row number
- Permanent identifier (never changes)
- Essential for auditing
- Allows excluded records to be brought back

**Note:** Also appears at position 38 for backwards compatibility with existing code

---

## Decision: Excluded Records Must Be Saved

### ✅ APPROVED: Save all excluded rows to separate file

**File:** `03_DATA/00_excluded/excluded_records_{year}_step{XX}_v{X.X.X}.csv`

**Columns:**
- REC_ID
- Exclusion_Step (which step excluded it)
- Exclusion_Reason (why excluded)
- Exclusion_Date (when excluded)
- All original row data

**Why:**
- Nothing is ever truly deleted
- Can bring back excluded records if rules change
- Can analyze exclusion patterns
- Complete audit trail

**Common exclusion reasons:**
- Duplicate BOL
- Missing required field (arrival date, vessel, etc.)
- FROB flag set (Foreign Cargo Remaining On Board)
- Invalid data (negative tonnage, future dates, etc.)
- User filter rules

---

## Harmonization Rules (To Be Implemented)

### Shipper/Consignee Name Standardization

**Capitalization:**
```
"ABC CORP" → "ABC Corporation"
"xyz company" → "XYZ Company"
"Abc Corp." → "ABC Corporation"
```

**Abbreviation Expansion:**
```
"CORP" → "Corporation"
"CO" → "Company"
"INC" → "Incorporated"
"LTD" → "Limited"
"LLC" → "Limited Liability Company"
```

**Punctuation Standardization:**
```
"ABC CORP." → "ABC Corporation"
"ABC, CORP" → "ABC Corporation"
"ABC - CORP" → "ABC Corporation"
```

**Whitespace Normalization:**
```
"ABC  CORP" → "ABC Corporation" (remove extra spaces)
"  ABC CORP  " → "ABC Corporation" (trim)
```

**Known Aliases (Example):**
```
"EXXONMOBIL" → "ExxonMobil Corporation"
"EXXON MOBIL" → "ExxonMobil Corporation"
"EXXON-MOBIL CORP" → "ExxonMobil Corporation"
```

**Implementation:**
```python
def harmonize_name(name):
    """Harmonize company name"""
    if pd.isna(name) or name == '':
        return ''

    # 1. Strip whitespace
    name = str(name).strip()

    # 2. Normalize capitalization (title case)
    name = name.title()

    # 3. Expand abbreviations
    abbrev_map = {
        ' Corp.': ' Corporation',
        ' Corp': ' Corporation',
        ' Co.': ' Company',
        ' Co': ' Company',
        ' Inc.': ' Incorporated',
        ' Inc': ' Incorporated',
        ' Ltd.': ' Limited',
        ' Ltd': ' Limited',
        ' Llc': ' LLC',
    }
    for abbrev, full in abbrev_map.items():
        name = name.replace(abbrev, full)

    # 4. Remove punctuation (except periods in known abbreviations)
    name = re.sub(r'[,\-]', ' ', name)

    # 5. Normalize whitespace
    name = re.sub(r'\s+', ' ', name).strip()

    # 6. Apply known aliases (from reference file)
    # aliases = load_alias_dict()
    # if name in aliases:
    #     name = aliases[name]

    return name
```

**Reference File:** `00_REFERENCE/company_aliases.json`

```json
{
  "EXXONMOBIL": "ExxonMobil Corporation",
  "EXXON MOBIL": "ExxonMobil Corporation",
  "EXXON-MOBIL CORP": "ExxonMobil Corporation",
  "CHEVRON": "Chevron Corporation",
  "CHEVRON CORP": "Chevron Corporation"
}
```

---

## Data Integrity Checks

### After Harmonization, Verify:

**1. No blank names where originals existed**
```python
assert not ((df['Shipper (Original Format)'] != '') & (df['Shipper'] == '')).any()
assert not ((df['Consignee (Original Format)'] != '') & (df['Consignee'] == '')).any()
```

**2. Can reconstruct Quantity**
```python
reconstructed = df['Qty'].astype(str) + ' ' + df['Pckg']
# (Can't test against original since Quantity column dropped)
```

**3. REC_ID is unique**
```python
assert df['REC_ID'].is_unique, "REC_IDs must be unique!"
```

**4. REC_ID format is valid**
```python
pattern = r'^[A-Z]{4}_[A-Z]{3}_FILE\d{3}_R\d{6}$'
assert df['REC_ID'].str.match(pattern).all(), "Invalid REC_ID format!"
```

**5. Excluded records saved**
```python
if excluded_count > 0:
    assert os.path.exists(excluded_file), "Excluded records file not created!"
    df_excluded = pd.read_csv(excluded_file)
    assert len(df_excluded) == excluded_count, "Excluded count mismatch!"
```

---

## Rollback Strategy

### If harmonization causes problems:

**Option 1: Restore originals**
```python
# Copy "(Original Format)" back to main columns
df['Shipper'] = df['Shipper (Original Format)']
df['Consignee'] = df['Consignee (Original Format)']
```

**Option 2: Re-run preprocessing with harmonization disabled**
```python
# In script, set flag:
ENABLE_HARMONIZATION = False

if ENABLE_HARMONIZATION:
    df['Shipper'] = df['Shipper'].apply(harmonize_name)
    df['Consignee'] = df['Consignee'].apply(harmonize_name)
else:
    # Keep original values
    pass
```

**Option 3: Fix harmonization rules and re-run**
```python
# Update harmonize_name() function
# Re-run preprocessing on raw data
# Compare old vs. new harmonized values
```

---

## Testing Strategy

### Test harmonization on 5K sample:

**1. Before/After Comparison**
```python
# Load 5K sample with harmonization disabled
df_original = preprocess(raw_data, harmonize=False)

# Load 5K sample with harmonization enabled
df_harmonized = preprocess(raw_data, harmonize=True)

# Compare
compare_df = pd.DataFrame({
    'Original': df_original['Shipper'],
    'Harmonized': df_harmonized['Shipper'],
    'Changed': df_original['Shipper'] != df_harmonized['Shipper']
})

# Show changes
print(f"Total names: {len(compare_df)}")
print(f"Changed: {compare_df['Changed'].sum()}")
print(f"Changed %: {compare_df['Changed'].sum() / len(compare_df) * 100:.1f}%")

# Show sample changes
print(compare_df[compare_df['Changed']].head(20))
```

**2. Spot Check**
- Manually review 50-100 harmonized names
- Verify they look correct
- Check for obvious errors

**3. Alias Testing**
```python
# Test known aliases
test_cases = {
    "EXXONMOBIL": "ExxonMobil Corporation",
    "EXXON MOBIL": "ExxonMobil Corporation",
    "CHEVRON CORP": "Chevron Corporation",
}

for input_name, expected_output in test_cases.items():
    actual_output = harmonize_name(input_name)
    assert actual_output == expected_output, f"Failed: {input_name} → {actual_output} (expected {expected_output})"

print("✅ All alias tests passed")
```

---

## Documentation Requirements

### Update these files after harmonization:

- [ ] `PIPELINE_RULES.md` - Rule 3 (already done ✅)
- [ ] `PREPROCESSING_CONSOLIDATION_PLAN.md` - Add harmonization section
- [ ] `README.md` - Note harmonization is enabled
- [ ] `00_REFERENCE/company_aliases.json` - Create/update alias dictionary
- [ ] `02_SCRIPTS/step01_preprocess_v1.0.0.py` - Implement harmonization
- [ ] Test results document - Show before/after comparison

---

## Summary

| Decision | Approach | Rationale |
|----------|----------|-----------|
| **Shipper/Consignee** | Overwrite with harmonized, keep "(Original Format)" | Best practice, clean data, auditability |
| **Quantity** | Split & drop original | Only destructive transform, can reconstruct |
| **REC_ID** | Add at position 61 | Complete audit trail to raw data |
| **Excluded Records** | Save to separate file | Nothing truly deleted, can bring back |

**Status:** ✅ All decisions approved and documented
**Next Step:** Implement in step01_preprocess_v1.0.0.py

---

**Document Version:** 1.0.0
**Created:** 2026-01-28
**Status:** APPROVED
