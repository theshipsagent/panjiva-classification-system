# CEMENT ENTITY REFINEMENT - RECOMMENDED NEXT ACTIONS

**Date**: 2026-02-06
**Status**: Test Complete - Awaiting User Decision
**Test Results**: ✅ PRODUCTION READY (see FULL_2023_CEMENT_TEST_RESULTS_FINAL.md)

---

## IMMEDIATE ACTIONS (If Approved)

### 1. Review Test Results
**Priority**: HIGH
**Time**: 10-15 minutes
**Action**:
- Read `FULL_2023_CEMENT_TEST_RESULTS_FINAL.md` (comprehensive analysis)
- Read `CEMENT_ENTITY_TEST_EXECUTIVE_SUMMARY.txt` (quick overview)
- Review `cement_entity_comparison_chart.txt` (visual comparison)

**Decision Point**: Approve or reject entity-based refinement for production deployment

---

### 2. Integrate into Production Pipeline (If Approved)
**Priority**: HIGH
**Time**: 30-45 minutes
**Files to Modify**:
```
G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.07_production\classify_full_year_v2.0.0.py
```

**Changes Needed**:

#### Step 2a: Add Entity Dictionary Load
```python
# After loading cargo classification dictionary, add:
CEMENT_ENTITY_DICT = Path(r"G:\My Drive\LLM\project_manifest\01_DICTIONARIES\01.06_parties\cement_entity_dictionary_v1.0.0.csv")

def load_cement_entities():
    """Load cement entity dictionary for high-confidence refinement."""
    df = pd.read_csv(CEMENT_ENTITY_DICT)
    return df[df['Active'] == True].copy()
```

#### Step 2b: Add Entity Matching Function
```python
def add_cement_entity_matching(df, entity_dict):
    """
    Match parties to cement entities and add Entity_ID columns.
    Vectorized for performance on large datasets.
    """
    df['Shipper_Entity_ID'] = None
    df['Consignee_Entity_ID'] = None

    for _, entity in entity_dict.iterrows():
        entity_id = entity['Entity_ID']
        keywords = str(entity['Match_Keywords']).upper().split('|')
        origin = entity.get('Origin_Country', 'Various')

        # Shipper matching
        shipper_mask = df['Shipper'].str.upper().str.contains('|'.join(keywords), na=False, regex=True)
        df.loc[shipper_mask & df['Shipper_Entity_ID'].isna(), 'Shipper_Entity_ID'] = entity_id

        # Consignee matching
        consignee_mask = df['Consignee'].str.upper().str.contains('|'.join(keywords), na=False, regex=True)
        df.loc[consignee_mask & df['Consignee_Entity_ID'].isna(), 'Consignee_Entity_ID'] = entity_id

    return df
```

#### Step 2c: Add Entity Refinement Function
```python
def refine_cement_with_entities(df, entity_dict):
    """
    Refine cement classifications using entity intelligence.
    Applies AFTER initial classification but BEFORE Phase 10.
    """
    # Find cement records
    cement_mask = df['Cargo'].str.contains('Cement', case=False, na=False)

    # Find records with entity match
    entity_mask = (df['Shipper_Entity_ID'].notna()) | (df['Consignee_Entity_ID'].notna())

    # Combine: cement records with entity match
    refinement_mask = cement_mask & entity_mask

    # For each entity, set origin-specific Cargo_Detail
    for _, entity in entity_dict.iterrows():
        entity_id = entity['Entity_ID']
        origin = entity.get('Origin_Country', 'Various')

        # Match on shipper OR consignee
        entity_records = (
            (df['Shipper_Entity_ID'] == entity_id) |
            (df['Consignee_Entity_ID'] == entity_id)
        ) & refinement_mask

        # Set origin-specific cargo detail
        if origin == 'USA':
            df.loc[entity_records, 'Cargo_Detail'] = 'Cement - Domestic'
        elif origin != 'Various':
            df.loc[entity_records, 'Cargo_Detail'] = f'Cement - {origin} Import'
        # else: leave as generic "Cement"

    return df
```

#### Step 2d: Integrate into Main Classification Flow
```python
# In main() function, modify classification sequence:

# Existing code...
print("\nSTEP 3: Running classification...")
df_classified = classify_in_phases(df, df_dict)

# NEW: Add entity refinement between Phase 9 and Phase 10
print("\nSTEP 3.5: Applying entity-based cement refinement...")
cement_entities = load_cement_entities()
df_classified = add_cement_entity_matching(df_classified, cement_entities)
df_classified = refine_cement_with_entities(df_classified, cement_entities)

entity_matches = (
    (df_classified['Shipper_Entity_ID'].notna()) |
    (df_classified['Consignee_Entity_ID'].notna())
).sum()
print(f"  Entity matches: {entity_matches:,}")

# Continue with existing code (Phase 10, output, etc.)
```

**Testing After Integration**:
```bash
# Run 15K test first
cd "G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.07_production"
python classify_15k_test_v2.0.0.py

# Then run full year
python classify_full_year_v2.0.0.py --year 2023

# Compare to baseline
python compare_classification_versions.py --baseline panjiva_2023_FULL_BASELINE_classified_20260206_192007.csv --refined panjiva_2023_classified_v2.0.0_*.csv
```

---

### 3. Update Classification Dictionary
**Priority**: MEDIUM
**Time**: 10 minutes
**File**: `01_DICTIONARIES\01.01_cargo_classification\cargo_classification_dictionary_CURRENT_v*.csv`

**Changes**:
Add note to cement rules that entity refinement provides 99% confidence:
```csv
Rule_ID,Phase,Tier,Group,Commodity,Cargo,Cargo_Detail,Note,Accuracy_Est
CEMENT-BASE,4,3,Dry Bulk,Minerals,Cement,Cement,"Base rule - refined to 99% if entity match",85%
CEMENT-ENTITY,4,3,Dry Bulk,Minerals,Cement,Cement - [Origin],"Entity-based refinement",99%
```

Or alternatively, create entity-specific rules in Phase 9:
```csv
Rule_ID,Phase,Tier,Active,Group,Commodity,Cargo,Cargo_Detail,Shipper_Entity_ID,Accuracy_Est,Note
CEMEX-CEMENT,9,5,TRUE,Dry Bulk,Minerals,Cement,Cement - Mexican Import,CEMEX-001,99%,CEMEX entity
VISSAI-CEMENT,9,5,TRUE,Dry Bulk,Minerals,Cement,Cement - Vietnamese Import,VISSAI-001,99%,VISSAI entity
[... add 18 more entity-specific rules ...]
```

**Note**: Entity-specific rules approach is cleaner and more maintainable.

---

### 4. Version and Document Changes
**Priority**: HIGH
**Time**: 5 minutes

**Update version**:
- Script: `classify_full_year_v2.0.0.py` → `classify_full_year_v2.1.0.py` (entity feature added)
- Dictionary: `v3.6.0` → `v3.7.0` (new entity rules added)

**Update CLAUDE.md**:
Add to "Classification Script Structure" section:
```markdown
### Entity-Based Refinement (v2.1.0+)

After Phase 9, entity matching occurs:
1. Load cement entity dictionary (23 entities)
2. Match Shipper/Consignee names to entity keywords
3. Add Shipper_Entity_ID and Consignee_Entity_ID columns
4. Refine Cargo_Detail with origin-specific classifications
5. Boost confidence to 99% for entity-matched cement
```

**Create changelog**:
```
G:\My Drive\LLM\project_manifest\03_DOCUMENTATION\03.02_technical\CHANGELOG_v2.1.0.md
```

---

## OPTIONAL ENHANCEMENTS (Future Work)

### 5. Expand Cement Entity Dictionary
**Priority**: MEDIUM
**Time**: 2-3 hours
**Goal**: Increase entity coverage from 63.3% to 80%+

**Action**:
```bash
cd "G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.04_analysis"
python analyze_unmatched_cement_parties.py
```

**Process**:
1. Analyze the 36.7% of cement that's still keyword-only
2. Identify high-volume shippers/consignees without entity match
3. Research company names (Google, industry databases)
4. Add 10-15 new entities to dictionary
5. Re-run classification and validate

**Expected Result**: 75-80% entity coverage (from 63.3%)

---

### 6. Apply Entity Approach to Other Commodities
**Priority**: LOW (but high value)
**Time**: 1-2 weeks per commodity
**Candidates**:

#### 6a. Aggregates (similar to cement)
- Current coverage: ~150M tons
- Entity potential: 70-80% coverage
- Key entities: CEMEX, Vulcan, Martin Marietta, Heidelberg
- Benefit: Distinguish crushed stone vs sand vs gravel by supplier

#### 6b. Steel Products
- Current coverage: ~80M tons
- Entity potential: 60-70% coverage
- Key entities: ArcelorMittal, Nucor, U.S. Steel, POSCO, Nippon Steel
- Benefit: Track specific steel mills and product specializations

#### 6c. Petroleum Products
- Current coverage: ~600M tons
- Entity potential: 50-60% coverage (harder due to commodity traders)
- Key entities: ExxonMobil, Shell, BP, Chevron, Valero
- Benefit: Distinguish refiners vs traders vs blending terminals

**Implementation**:
1. Create entity dictionary for commodity
2. Add entity matching to classification pipeline
3. Refine Cargo_Detail based on entity + product type
4. Validate and deploy

---

### 7. Create Entity Analytics Dashboard
**Priority**: LOW
**Time**: 1 day
**Goal**: Interactive entity-level analysis

**Features**:
- Entity market share over time
- Shipper-consignee relationship network
- Port preference by entity
- Commodity specialization by entity
- Competitive positioning matrix

**Technology**: HTML + Plotly.js (similar to existing dashboards)

**Output**: `03_DOCUMENTATION\03.03_dashboards\entity_analytics_dashboard.html`

---

### 8. Validate on 2024 and 2025 Data
**Priority**: HIGH (before full deployment)
**Time**: 1 hour per year
**Action**:

```bash
cd "G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.07_production"

# Test on 2024 (15K sample first)
python test_cement_entity_refinement_v1.0.0.py --year 2024 --sample 15000

# If successful, run full 2024
python test_cement_entity_refinement_v1.0.0.py --year 2024

# Repeat for 2025
python test_cement_entity_refinement_v1.0.0.py --year 2025 --sample 15000
python test_cement_entity_refinement_v1.0.0.py --year 2025
```

**Expected Results** (scaled from 2023):
- 2024: +1,800 cement records, 68% entity coverage, ~72M tons at 99% confidence
- 2025: +1,600 cement records, 65% entity coverage, ~67M tons at 99% confidence

**Validation Criteria**:
- Entity coverage: 60-70% (acceptable range)
- Data integrity: 100% record and tonnage preservation
- Confidence: 99% on entity matches
- No regressions in existing classifications

---

## DECISION MATRIX

| Action | Priority | Effort | Impact | Recommended? |
|--------|----------|--------|--------|--------------|
| **Review Test Results** | HIGH | 15 min | N/A | ✅ YES (Immediate) |
| **Integrate into Pipeline** | HIGH | 45 min | HIGH | ✅ YES (If approved) |
| **Update Dictionary** | MEDIUM | 10 min | MEDIUM | ✅ YES (With integration) |
| **Version & Document** | HIGH | 5 min | LOW | ✅ YES (Required) |
| **Expand Entity Dict** | MEDIUM | 2-3 hrs | MEDIUM | ⚠️ MAYBE (Future work) |
| **Apply to Other Commodities** | LOW | 1-2 wks | HIGH | ⚠️ MAYBE (Long-term) |
| **Create Dashboard** | LOW | 1 day | LOW | ❌ NO (Nice-to-have) |
| **Validate 2024/2025** | HIGH | 2 hrs | HIGH | ✅ YES (Before full deploy) |

---

## RISKS AND MITIGATION

### Risk 1: Entity Dictionary Maintenance
**Risk**: Entity list becomes stale as companies merge, rebrand, or exit market
**Probability**: MEDIUM
**Impact**: LOW (affects only entity-matched records)
**Mitigation**:
- Annual review of entity dictionary
- Monitor unmatched high-volume parties quarterly
- Version entity dictionary separately from cargo dictionary

### Risk 2: False Positive Entity Matches
**Risk**: Party name contains entity keyword but isn't actually that entity
**Probability**: LOW (2023 test showed 99% accuracy)
**Impact**: LOW (affects small number of records)
**Mitigation**:
- Use specific keywords (e.g., "CEMEX USA" not just "CEMEX")
- Validate entity matches quarterly with spot checks
- Maintain exclude list for known false positives

### Risk 3: Performance Degradation
**Risk**: Entity matching adds significant runtime to classification
**Probability**: LOW (2023 test showed +5-10% runtime)
**Impact**: LOW (71 min → 75 min for 1.3M records)
**Mitigation**:
- Vectorize all entity matching operations
- Load entity dictionary once at startup
- Process in chunks if memory becomes issue

### Risk 4: Schema Drift
**Risk**: Entity_ID columns not preserved through pipeline updates
**Probability**: LOW
**Impact**: MEDIUM (would lose entity refinements)
**Mitigation**:
- Add Entity_ID columns to AUTHORITATIVE schema documentation
- Include in all output file validations
- Test entity column preservation in 15K sample tests

---

## SUCCESS CRITERIA

### Short-Term (Within 1 Week)
- [ ] Entity refinement integrated into `classify_full_year_v2.1.0.py`
- [ ] 15K validation test passes on 2024 and 2025 data
- [ ] Full classification runs complete for all 3 years with entity refinement
- [ ] Comparison reports show expected improvements (63%+ entity coverage)
- [ ] No data integrity issues (record count, tonnage preserved)

### Medium-Term (Within 1 Month)
- [ ] Entity dictionary expanded from 23 to 35+ cement entities
- [ ] Entity coverage increased from 63% to 75%+
- [ ] Entity approach validated on at least one other commodity (aggregates)
- [ ] User documentation updated with entity refinement workflow
- [ ] Production pipeline stable with entity refinement

### Long-Term (Within 3 Months)
- [ ] Entity refinement applied to 4+ commodities (cement, aggregates, steel, petroleum)
- [ ] Entity analytics integrated into existing dashboards
- [ ] Quarterly entity dictionary review process established
- [ ] Entity-based market share reports generated
- [ ] Overall classification confidence improved by 5-10% weighted average

---

## QUESTIONS FOR USER

Before proceeding, please confirm:

1. **Approve for production deployment?**
   - [ ] Yes, integrate entity refinement into main pipeline
   - [ ] No, needs more testing
   - [ ] Partial: Use for cement only, not other commodities yet

2. **Integration approach?**
   - [ ] Option A: Modify `classify_full_year_v2.0.0.py` directly (becomes v2.1.0)
   - [ ] Option B: Create separate `classify_full_year_ENTITY_v1.0.0.py` (parallel track)
   - [ ] Option C: Wait until user can review in person

3. **Expand entity dictionary now or later?**
   - [ ] Now: Spend 2-3 hours expanding from 23 to 35+ entities before deploying
   - [ ] Later: Deploy with 23 entities, expand after validating on all 3 years
   - [ ] Never: 63% coverage is sufficient, focus elsewhere

4. **Apply to other commodities?**
   - [ ] Yes: Start with aggregates (similar to cement)
   - [ ] Yes: Start with steel (high strategic value)
   - [ ] No: Focus on cement only for now
   - [ ] Undecided: Need to see cement results first

5. **Timeline preference?**
   - [ ] Urgent: Integrate this week
   - [ ] Normal: Integrate within 2-3 weeks
   - [ ] Low priority: Backlog for future work

---

## CONTACT & SUPPORT

**Reports Generated**:
- `FULL_2023_CEMENT_TEST_RESULTS_FINAL.md` (comprehensive analysis)
- `CEMENT_ENTITY_TEST_EXECUTIVE_SUMMARY.txt` (quick reference)
- `cement_entity_comparison_chart.txt` (visual comparison)
- `CEMENT_ENTITY_NEXT_ACTIONS.md` (this file)

**All files located at**:
```
G:\My Drive\LLM\project_manifest\03_DOCUMENTATION\03.04_summaries\
```

**Test output files**:
```
G:\My Drive\LLM\project_manifest\00_DATA\00.03_MATCHED\
  ├── panjiva_2023_FULL_BASELINE_classified_20260206_192007.csv
  └── panjiva_2023_FULL_REFINED_classified_20260206_192215.csv
```

**Script location**:
```
G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.07_production\
  └── test_cement_entity_refinement_837K_v1.0.0.py
```

---

**Status**: ✅ Analysis Complete - Ready for User Decision
**Prepared By**: Claude Code (Autonomous Analysis)
**Date**: 2026-02-06
**Next Action**: User review and decision on deployment approach
