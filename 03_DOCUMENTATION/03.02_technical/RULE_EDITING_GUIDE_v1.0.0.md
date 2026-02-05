# Dictionary v2.2.0 Rule Editing Guide

**Version:** 1.0.0
**Date:** 2026-01-13
**For Dictionary:** v2.2.0 and later

---

## Quick Start

**Dictionary Location:**
```
G:\My Drive\LLM\project_manifest\03_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.2.1_20260113_1530.csv
```

**Open in:** Excel, Google Sheets, or any CSV editor

**After editing:** Save as CSV (not Excel format), increment version number

---

## Understanding Lock Levels

### The 4 Locking Columns

| Column | What It Locks | When to Use |
|--------|---------------|-------------|
| `Lock_Group` | Group level (Dry Bulk, Liquid Bulk, etc.) | Phase 1-2 (vessel type, carrier shortcuts) |
| `Lock_Commodity` | Group + Commodity | Phase 4-5 (HS2/HS4 matching) |
| `Lock_Cargo` | Group + Commodity + Cargo | Phase 6 (HS6/keywords) |
| `Lock_Cargo_Detail` | All 4 levels (final) | Phase 8-10 (specific grades, final classification) |

### Locking Patterns

**Pattern 1: Lock Group Only** (Most flexible - allows full refinement)
```csv
Lock_Group: TRUE
Lock_Commodity: FALSE
Lock_Cargo: FALSE
Lock_Cargo_Detail: FALSE
```
**Use for:** Vessel type rules, carrier shortcuts where you want later phases to refine

**Pattern 2: Lock Group + Commodity** (Allow Cargo refinement)
```csv
Lock_Group: TRUE
Lock_Commodity: TRUE
Lock_Cargo: FALSE
Lock_Cargo_Detail: FALSE
```
**Use for:** HS2 rules, broad categorization

**Pattern 3: Lock Group + Commodity + Cargo** (Allow Cargo_Detail refinement)
```csv
Lock_Group: TRUE
Lock_Commodity: TRUE
Lock_Cargo: TRUE
Lock_Cargo_Detail: FALSE
```
**Use for:** HS6 rules, keyword rules

**Pattern 4: Lock All 4** (Final classification, no refinement)
```csv
Lock_Group: TRUE
Lock_Commodity: TRUE
Lock_Cargo: TRUE
Lock_Cargo_Detail: TRUE
```
**Use for:** 100% certain classifications (WALLENIUS=RoRo, specific crude grades)

---

## Common Editing Scenarios

### Scenario 1: Add New Carrier Rule (Lock Group Only)

**Goal:** Add MAERSK LINE as bulk carrier, lock Group, allow refinement

**Steps:**
1. Open dictionary in Excel
2. Go to last row, add new row
3. Fill in:

```csv
Rule_ID: CARR-MAERSK-BULK
Phase: 2
Tier: 1
Active: TRUE
Lock_Classification: FALSE
Override_HS: FALSE
Carrier_Name: MAERSK LINE
Package_Type: [leave blank]
Vessel_Type: Bulk Carrier
Exclude_Groups: Liquid Bulk;Container;Ro/Ro;Reefer
HS2: [leave blank]
HS4: [leave blank]
HS6: [leave blank]
Keywords: MAERSK LINE
Exclude_Keywords: [leave blank]
Min_Tons: [leave blank]
Max_Tons: [leave blank]
Port_Filter: [leave blank]
Country_Filter: [leave blank]
Lock_Group: TRUE              ← LOCK GROUP ONLY
Lock_Commodity: FALSE         ← Allow refinement
Lock_Cargo: FALSE
Lock_Cargo_Detail: FALSE
Group: Dry Bulk
Commodity: TBN                ← Placeholder
Cargo: TBN
Cargo_Detail: TBN
Filter: [leave blank]
Note: Carrier shortcut - MAERSK bulk vessels
Accuracy_Est: 90%
Tonnage_Impact: Very High
Date_Added: 2026-01-13
Last_Modified: 2026-01-13
```

4. Save as `cargo_classification_dictionary_v2.2.2_YYYYMMDD_HHMM.csv`

---

### Scenario 2: Add High-Confidence Rule (Lock All 4)

**Goal:** Add BASRAH HEAVY crude oil with 100% certainty

**Steps:**
```csv
Rule_ID: CRUDE-BASRAH-HEAVY
Phase: 10
Tier: 5
Active: TRUE
Lock_Classification: TRUE     ← Also set this for backward compatibility
Override_HS: TRUE
Carrier_Name: [leave blank]
Vessel_Type: Tanker
Exclude_Groups: Dry Bulk;Break-Bulk;Container;Ro/Ro;Reefer
HS2: 27
HS4: 2709
HS6: 270900
Keywords: BASRAH HEAVY
Exclude_Keywords: [leave blank]
Lock_Group: TRUE              ← LOCK ALL 4
Lock_Commodity: TRUE
Lock_Cargo: TRUE
Lock_Cargo_Detail: TRUE
Group: Liquid Bulk
Commodity: Petroleum
Cargo: Crude Oil
Cargo_Detail: Basrah Heavy
Note: Phase 10 specific grade - 100% certain
Accuracy_Est: 100%
Tonnage_Impact: Very High
Date_Added: 2026-01-13
Last_Modified: 2026-01-13
```

---

### Scenario 3: Modify Existing Rule to Allow Refinement

**Goal:** Change NYK steel rule to lock Commodity too (not just Group)

**Current:**
```csv
CARR-NYK-STEEL,...,Lock_Group=TRUE,Lock_Commodity=FALSE,...
```

**Edit to:**
```csv
CARR-NYK-STEEL,...,Lock_Group=TRUE,Lock_Commodity=TRUE,Lock_Cargo=FALSE,...
```

**Result:**
- Phase 2: Locks Group + Commodity
- Phase 6: Can only refine Cargo + Cargo_Detail

---

### Scenario 4: Disable Rule Temporarily

**Goal:** Test classification without a specific rule

**Edit:**
```csv
Active: FALSE
```

**Save and re-run classification.** Rule will be skipped.

**To re-enable:**
```csv
Active: TRUE
```

---

### Scenario 5: Add Vessel Type Rule (Phase 1)

**Goal:** Add Container ship vessel type

**Steps:**
```csv
Rule_ID: VTYPE-CONTAINER
Phase: 1                      ← Phase 1 for vessel type
Tier: 1
Active: TRUE
Lock_Classification: FALSE
Override_HS: FALSE
Vessel_Type: Container;Containership
Exclude_Groups: Dry Bulk;Liquid Bulk;Break-Bulk;Ro/Ro;Reefer
Lock_Group: TRUE              ← Lock Group only
Lock_Commodity: FALSE
Lock_Cargo: FALSE
Lock_Cargo_Detail: FALSE
Group: Container
Commodity: TBN
Cargo: TBN
Cargo_Detail: TBN
Note: Vessel type: Container ships carry containers
Accuracy_Est: 100%
Tonnage_Impact: Very High
Date_Added: 2026-01-13
Last_Modified: 2026-01-13
```

---

## Physical Constraint Validation

### Setting Exclude_Groups

**Purpose:** Prevent physically impossible cargo classifications

**By Vessel Type:**
```
Bulk Carrier   → Exclude_Groups: Liquid Bulk;Container;Ro/Ro;Reefer
Tanker         → Exclude_Groups: Dry Bulk;Break-Bulk;Container;Ro/Ro;Reefer
LPG/LNG        → Exclude_Groups: Dry Bulk;Break-Bulk;Container;Ro/Ro;Reefer
Container      → Exclude_Groups: Dry Bulk;Liquid Bulk;Break-Bulk;Ro/Ro;Reefer
RoRo           → Exclude_Groups: Dry Bulk;Liquid Bulk;Break-Bulk;Container;Reefer
Reefer         → Exclude_Groups: Dry Bulk;Liquid Bulk;Container;Ro/Ro
General Cargo  → Exclude_Groups: Dry Bulk;Liquid Bulk
```

**Example:**
```csv
# Bulk carrier can NEVER carry liquid bulk
Vessel_Type: Bulk Carrier
Exclude_Groups: Liquid Bulk;Container;Ro/Ro;Reefer
```

**What Happens:**
```
Record: Bulk Carrier with cargo "METHANOL" (Liquid Bulk)
Phase 1: Group = Dry Bulk (locked)
Phase 6: "METHANOL" rule wants Group = Liquid Bulk
CHECK: "Liquid Bulk" in Exclude_Groups? YES!
REJECT RULE (physically impossible)
```

---

## TBN Placeholder Strategy

### Why Use TBN?

**TBN = To Be Named**

Use when you want to:
1. Lock higher-level taxonomy (Group, Commodity)
2. Let later phases fill in details (Cargo, Cargo_Detail)
3. Track unclassified subcategories for analysis

### Example:

**Phase 2 Rule:**
```csv
Group: Dry Bulk
Commodity: TBN          ← Placeholder
Cargo: TBN
Cargo_Detail: TBN
Lock_Group: TRUE        ← Lock Group only
Lock_Commodity: FALSE   ← Allow refinement
```

**Phase 6 Refines:**
```csv
Group: Dry Bulk         ← Kept from Phase 2
Commodity: Metals & Minerals  ← Filled in
Cargo: Iron Products
Cargo_Detail: Iron Ore
```

### Analysis:

```sql
-- Find records that need refinement
SELECT * WHERE Commodity = 'TBN'
SELECT * WHERE Cargo_Detail = 'TBN'
```

---

## Testing Your Edits

### Step 1: Save New Version

**Naming:**
```
cargo_classification_dictionary_v2.2.2_20260113_1600.csv
                                  ↑ ↑ ↑
                                  │ │ └─ PATCH (bug fix, typo)
                                  │ └─── MINOR (new rules)
                                  └───── MAJOR (breaking changes)
```

### Step 2: Update Classification Script

**If using Python:**
```python
CARGO_DICT = Path(r"G:\My Drive\LLM\project_manifest\03_DICTIONARIES\03.01_cargo_classification\cargo_classification_dictionary_v2.2.2_20260113_1600.csv")
```

### Step 3: Run Classification

**On sample data first:**
```python
# Test with 1000 records
df_sample = df.head(1000)
classify(df_sample, cargo_dict)
```

### Step 4: Verify Results

**Check:**
1. ✅ New rules are firing (check Rule_ID in output)
2. ✅ Lock levels are working (Group locked, Commodity refined)
3. ✅ Physical constraints enforced (no impossible classifications)
4. ✅ No unexpected overrides

### Step 5: Run Full Classification

**If sample looks good:**
```python
df_full = classify(df_all, cargo_dict)
```

---

## Common Mistakes & Fixes

### Mistake 1: Locking Too Much Too Early

**Problem:**
```csv
Phase: 2
Lock_Group: TRUE
Lock_Commodity: TRUE
Lock_Cargo: TRUE
Lock_Cargo_Detail: TRUE    ← TOO AGGRESSIVE!
Group: Break-Bulk
Commodity: TBN            ← Can't be refined!
```

**Fix:**
```csv
Lock_Group: TRUE
Lock_Commodity: FALSE      ← Allow refinement
Lock_Cargo: FALSE
Lock_Cargo_Detail: FALSE
```

### Mistake 2: Forgetting Exclude_Groups

**Problem:**
```csv
Vessel_Type: Bulk Carrier
Exclude_Groups: [blank]    ← MISSING!
```

**Risk:** Could classify liquid bulk on bulk carrier

**Fix:**
```csv
Exclude_Groups: Liquid Bulk;Container;Ro/Ro;Reefer
```

### Mistake 3: Wrong Phase Order

**Problem:**
```csv
Phase: 10                  ← Too late!
Keywords: WHEAT            ← Common commodity
```

**Fix:**
```csv
Phase: 6                   ← Keywords should be Phase 6-7
```

### Mistake 4: Conflicting Locks

**Problem:**
```csv
Lock_Classification: TRUE
Lock_Group: FALSE          ← CONFLICT!
```

**Fix:** Be consistent
```csv
Lock_Classification: TRUE
Lock_Group: TRUE
Lock_Commodity: TRUE
Lock_Cargo: TRUE
Lock_Cargo_Detail: TRUE
```

Or use granular:
```csv
Lock_Classification: FALSE
Lock_Group: TRUE
Lock_Commodity: FALSE
Lock_Cargo: FALSE
Lock_Cargo_Detail: FALSE
```

---

## Advanced Techniques

### Hierarchical Classification Chain

**Build classification in stages:**

**Phase 1: Vessel Type (Lock Group)**
```csv
Vessel_Type: Bulk Carrier
Lock_Group: TRUE
Group: Dry Bulk
Commodity: TBN
```

**Phase 4: HS2 (Lock Group + Commodity)**
```csv
HS2: 26
Lock_Group: TRUE
Lock_Commodity: TRUE
Group: Dry Bulk (kept)
Commodity: Metals & Minerals
Cargo: TBN
```

**Phase 6: HS6 + Keywords (Lock Group + Commodity + Cargo)**
```csv
HS6: 260111
Keywords: IRON ORE
Lock_Group: TRUE
Lock_Commodity: TRUE
Lock_Cargo: TRUE
Group: Dry Bulk (kept)
Commodity: Metals & Minerals (kept)
Cargo: Iron Products
Cargo_Detail: TBN
```

**Phase 10: Specific Grade (Lock All)**
```csv
Keywords: TUBARAO
Lock_Group: TRUE
Lock_Commodity: TRUE
Lock_Cargo: TRUE
Lock_Cargo_Detail: TRUE
Group: Dry Bulk (kept)
Commodity: Metals & Minerals (kept)
Cargo: Iron Products (kept)
Cargo_Detail: Tubarao Iron Ore
```

---

## Quick Reference Card

### Lock Level Cheat Sheet

| Locked Columns | TBN Columns | Use Case | Phase |
|----------------|-------------|----------|-------|
| 1 (Group) | Commodity, Cargo, Cargo_Detail | Vessel type, carrier shortcut | 1-2 |
| 2 (Group + Commodity) | Cargo, Cargo_Detail | HS2 matching | 4 |
| 3 (Group + Commodity + Cargo) | Cargo_Detail | HS6/keyword matching | 5-7 |
| 4 (All) | None | Final classification | 8-10 |

### Validation Checklist

Before saving edits:
- [ ] Rule_ID is unique
- [ ] Phase is appropriate (1-10)
- [ ] Tier is correct (1-5)
- [ ] Lock levels make sense (don't lock TBN values)
- [ ] Vessel_Type set if applicable
- [ ] Exclude_Groups set for vessel types
- [ ] Keywords separated by semicolons
- [ ] Last_Modified updated to today
- [ ] Version number incremented

---

## Examples by Cargo Type

### Steel (Break-Bulk)

**Carrier Shortcut (Phase 2):**
```csv
CARR-NYK-STEEL,2,1,Lock_Group=TRUE,Lock_Commodity=FALSE,Break-Bulk,TBN,TBN,TBN
```

**HS2 Match (Phase 4):**
```csv
HS2-72-STEEL,4,3,Lock_Group=TRUE,Lock_Commodity=TRUE,Break-Bulk,Metals & Minerals,TBN,TBN
```

**Keyword Refinement (Phase 6):**
```csv
KW-STEEL-PLATE,6,3,Lock_Group=TRUE,Lock_Commodity=TRUE,Lock_Cargo=TRUE,Break-Bulk,Metals & Minerals,Steel,Steel Plate
```

### Crude Oil (Liquid Bulk)

**Vessel Type (Phase 1):**
```csv
VTYPE-TANKER,1,1,Lock_Group=TRUE,Liquid Bulk,TBN,TBN,TBN
```

**HS6 Match (Phase 6):**
```csv
HS6-CRUDE,6,3,Lock_Group=TRUE,Lock_Commodity=TRUE,Lock_Cargo=TRUE,Liquid Bulk,Petroleum,Crude Oil,TBN
```

**Specific Grade (Phase 10):**
```csv
CRUDE-BASRAH,10,5,Lock_All=TRUE,Liquid Bulk,Petroleum,Crude Oil,Basrah Heavy
```

---

**End of Rule Editing Guide v1.0.0**

*For questions, see DICTIONARY_V2.2.0_RELEASE_NOTES.md or NAMING_CONVENTIONS_v1.0.0.md*
