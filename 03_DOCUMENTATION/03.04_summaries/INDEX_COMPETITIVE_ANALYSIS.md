# Competitive Landscape Analysis - File Index
**Version 1.0.0 | Generated: 2026-02-05**

---

## Analysis Overview

Comprehensive competitive relationship mapping for 2024 US maritime imports, identifying **17,208 competitive relationships** between entities operating on overlapping trade lanes and commodities.

**Data Source:** `panjiva_imports_2024_classified_v2.0.0.csv` (449K records)
**Analysis Script:** `analyze_competitive_landscape_v1.0.0.py`
**Runtime:** ~10 minutes

---

## Output Files

### 📊 Data Files

#### 1. **competitive_relationships_v1.0.0.csv** (3.8 MB, 17,208 rows)
**Primary deliverable** - Complete competition matrix

**Columns:**
- `Entity_Type` - "Shipper" or "Consignee"
- `Entity_1`, `Entity_2` - Competing entities
- `Entity_1_Total_Tons`, `Entity_2_Total_Tons` - Total annual tonnage
- `Overlapping_Trade_Lanes` - Number of shared routes
- `Overlap_Tonnage` - Competing volume (MIN of both entities)
- `Overlap_Pct_Entity_1`, `Overlap_Pct_Entity_2` - % of each entity's business
- `Max_Overlap_Pct` - Highest of the two percentages
- `Top_Competing_Lane_1/2/3` - Specific routes where competition occurs

**Use cases:**
- Identify direct competitors by entity name
- Quantify market overlap between entity pairs
- Discover shared trade lanes
- Measure competitive intensity

**Example record:**
```
Entity_Type: Shipper
Entity_1: CHEVRON MARINE PRODUCTS LLC
Entity_2: SOMO OIL AND MARKETING
Overlap_Tonnage: 4,766,327
Overlap_Pct_Entity_1: 82.0%
Overlap_Pct_Entity_2: 37.7%
Top_Competing_Lane_1: HIGH SEAS,NORTH PACIFIC→SAN FRANCISO|CRUDE OIL
```

---

#### 2. **commodity_competition_v1.0.0.csv** (15 rows)
Top 3 shippers and consignees by commodity

**Columns:**
- `Commodity` - Commodity name
- `Total_Tons` - Total commodity tonnage
- `Top_Shipper_1/2/3` - Leading exporters
- `Top_Shipper_1/2/3_Tons` - Their tonnages
- `Top_Consignee_1/2/3` - Leading importers
- `Top_Consignee_1/2/3_Tons` - Their tonnages

**Use cases:**
- Identify market leaders by commodity
- Compare market shares within commodities
- Spot dominant players

**Commodities covered:**
- General Cargo (179.4M tons)
- Crude Oil (104.4M tons)
- Petroleum Products (74.1M tons)
- Chemicals (38.2M tons)
- Construction Materials (35.0M tons)
- Ro/Ro (29.6M tons)
- Steel, Forestry, Agricultural Products, Refrigerated Products, Ferrous Raw Materials, LNG, Minerals & Ores, LPG, Misc Bulk

---

#### 3. **port_competition_v1.0.0.csv** (22 rows)
Major port competitive profiles (>5M tons)

**Columns:**
- `Port` - Port name
- `Total_Tons` - Total port tonnage
- `Unique_Shippers`, `Unique_Consignees` - Entity counts (diversity metric)
- `Top_Commodity_1/2/3` - Leading commodities
- `Top_Commodity_1/2/3_Tons` - Commodity tonnages
- `Top_Shipper_1`, `Top_Consignee_1` - Dominant entities
- `Top_Shipper_1_Tons`, `Top_Consignee_1_Tons` - Their volumes

**Use cases:**
- Assess port competitive intensity (high entity count = high competition)
- Identify port specializations (commodity mix)
- Find dominant players by port
- Compare port concentration (Herfindahl index)

**Top ports:**
1. Houston (97.7M tons) - 3,273 shippers, 4,033 consignees
2. New York (76.3M tons) - 2,184 shippers, 2,508 consignees
3. New Orleans (75.0M tons) - 1,325 shippers, 1,210 consignees
4. LA-Long Beach (60.5M tons) - 1,890 shippers, 2,497 consignees
5. San Francisco (50.6M tons) - 408 shippers, 547 consignees (CONCENTRATED)

---

#### 4. **competitive_examples_highlighted_v1.0.0.csv** (157 rows)
Filtered competition for user-requested examples

**Categories:**
- **Oil Refiners** (98 relationships) - Valero, Chevron, ExxonMobil, Marathon competition
- **Oil Traders** (59 relationships) - PMI Trading entities, Bolanter

**Columns:** Same as competitive_relationships_v1.0.0.csv

**Use cases:**
- Quick lookup for specific company competition
- Focus on oil industry dynamics
- Validate analysis with known market players

**Note:** Aggregates companies (Martin Marietta, Vulcan, Orca) found limited direct competition, suggesting regional market separation.

---

### 📄 Documentation Files

#### 5. **COMPETITIVE_LANDSCAPE_EXECUTIVE_SUMMARY_v1.0.0.md** (15 KB)
**Comprehensive analysis report**

**Contents:**
- Overview and key metrics
- Top competitive relationships (ranked tables)
- Commodity-specific competition (detailed breakdowns)
- Port-level competition analysis
- Strategic competitive patterns (6 patterns discovered)
- Oil refiner competitive matrix
- Data quality notes
- Recommended next steps
- Methodology

**Target audience:** Executive briefing, strategic analysis

**Key sections:**
- **Pattern 1:** PMI Trading internal competition
- **Pattern 2:** Middle East crude convergence on San Francisco
- **Pattern 3:** Venezuela oil fragmentation
- **Pattern 4:** UAE aluminum duopoly
- **Pattern 5:** Aggregates vertical integration
- **Oil refiner matrix:** Overlap volumes between majors

---

#### 6. **COMPETITIVE_ANALYSIS_QUICK_REFERENCE_v1.0.0.md** (12 KB)
**Fast lookup guide**

**Contents:**
- Summary statistics
- Top 10 competitive relationships (at a glance)
- Commodity leaders (quick tables)
- Port competition rankings
- Key patterns (6 patterns, condensed)
- Oil refiner intelligence
- Trade lane hotspots
- File locations
- Key insights Q&A
- Methodology summary

**Target audience:** Quick reference, dashboard builders

**Q&A format answers:**
- "Who are Martin Marietta's competitors?"
- "Where do oil refiners compete?"
- "Do Trafigura and Vitol compete?"

---

#### 7. **competitive_analysis_summary_v1.0.0.txt** (13 KB)
**Text-based summary report**

**Contents:**
- Top 10 shipper competitive relationships (with trade lanes)
- Top 10 consignee competitive relationships (with trade lanes)
- Commodity-specific competition (top 3 by commodity)
- Port-level competition (top ports with entity counts)

**Format:** Plain text, easy to read in terminal or text editor

**Target audience:** Quick scan, log review

---

#### 8. **INDEX_COMPETITIVE_ANALYSIS.md** (this file)
**File index and navigation guide**

---

## Quick Start Guide

### To find competitors for a specific company:

1. Open `competitive_relationships_v1.0.0.csv`
2. Filter `Entity_1` or `Entity_2` columns for company name
3. Sort by `Overlap_Tonnage` descending to see strongest competitors

**Example (Excel/Python):**
```python
import pandas as pd
df = pd.read_csv('competitive_relationships_v1.0.0.csv')

# Find Chevron's competitors
chevron = df[(df['Entity_1'].str.contains('CHEVRON', case=False)) |
             (df['Entity_2'].str.contains('CHEVRON', case=False))]

chevron.sort_values('Overlap_Tonnage', ascending=False).head(10)
```

---

### To see top competitors in a specific commodity:

1. Open `commodity_competition_v1.0.0.csv`
2. Find row for desired commodity
3. Read `Top_Shipper_1/2/3` and `Top_Consignee_1/2/3` columns

**Example:** Crude Oil top 3 importers:
1. Chevron Marine - 23.4M tons
2. Saudi Refining - 14.8M tons
3. Valero Marketing - 14.3M tons

---

### To analyze port competition:

1. Open `port_competition_v1.0.0.csv`
2. Check `Unique_Shippers` and `Unique_Consignees` columns
   - High counts = fragmented market (high competition)
   - Low counts = concentrated market (market power)
3. Compare `Top_Shipper_1_Tons` to `Total_Tons` for concentration ratio

**Example:** San Francisco concentration:
- Total: 50.6M tons
- Chevron receives: 15.4M tons (30% market share)
- Concentration: HIGH (oligopoly)

---

## Key Findings Summary

### 🔥 Hottest Competition (by tonnage overlap)

1. **Chevron vs SOMO (Iraq)** - 4.8M tons - San Francisco crude
2. **PDVSA vs Petropiar** - 3.4M tons - Venezuela crude (internal competition)
3. **Dubai Aluminium vs Emirates Aluminium** - 3.1M tons - UAE aluminum duopoly

### 🏢 Most Competitive Commodity

**Crude Oil (104.4M tons)** - Oil refiners compete intensely for Latin American imports

### 🏭 Most Competitive Port

**Houston (97.7M tons)** - 3,273 shippers, 4,033 consignees (highest diversity)

### 🎯 Most Concentrated Port

**San Francisco (50.6M tons)** - Chevron controls 30% of imports (oligopoly)

### 🤝 Most Interesting Pattern

**PMI Trading internal competition** - 4+ legal entities competing with each other (1-2M tons overlap), likely for tax/legal optimization

---

## Methodology Notes

### Trade Lane Definition
```
Origin_Port → Destination_Port | Commodity
```

Example: `HIGH SEAS,NORTH PACIFIC → SAN FRANCISO | CRUDE OIL`

### Overlap Calculation
```
For each shared trade lane:
  Overlap_Tonnage = MIN(Entity1_tonnage, Entity2_tonnage)

Total_Overlap = SUM(Overlap_Tonnage for all shared lanes)

Overlap_Pct_Entity_1 = Total_Overlap / Entity1_Total_Tonnage * 100
Overlap_Pct_Entity_2 = Total_Overlap / Entity2_Total_Tonnage * 100
```

### Filtering Thresholds

**Entity significance:**
- Minimum: 10,000 tons annual volume
- Rationale: Exclude insignificant players, noise

**Competition significance:**
- Minimum: 5% overlap for at least one entity
- Rationale: Exclude trivial competition

**Port analysis:**
- Minimum: 5,000,000 tons total port volume
- Rationale: Focus on major ports

**Commodity analysis:**
- Minimum: 100,000 tons total commodity volume
- Rationale: Focus on significant commodities

### Data Quality

**Strengths:**
- Uses classified data (v2.0.0) with commodity assignments
- Tonnage-weighted (not just record counts)
- Trade lane specificity (not just port-level)

**Limitations:**
- Uses raw Shipper/Consignee names (not harmonized entity IDs)
- Many records attributed to "Unknown/Unharmonized" entities
- Underestimates competition where entities not normalized

**Improvement path:**
- Re-run analysis using `panjiva_imports_2024_HARMONIZED_v1.0.0.csv`
- Expected: +20-30% more relationships discovered

---

## File Locations

**Analysis Script:**
```
G:\My Drive\LLM\project_manifest\02_SCRIPTS\02.04_analysis\
  analyze_competitive_landscape_v1.0.0.py
```

**Input Data:**
```
G:\My Drive\LLM\project_manifest\00_DATA\00.03_MATCHED\
  panjiva_imports_2024_classified_v2.0.0.csv (398 MB, 449K records)
```

**Output Files:**
```
G:\My Drive\LLM\project_manifest\03_DOCUMENTATION\03.04_summaries\
  competitive_relationships_v1.0.0.csv (3.8 MB)
  commodity_competition_v1.0.0.csv (1 KB)
  port_competition_v1.0.0.csv (2 KB)
  competitive_examples_highlighted_v1.0.0.csv (27 KB)
  competitive_analysis_summary_v1.0.0.txt (13 KB)
  COMPETITIVE_LANDSCAPE_EXECUTIVE_SUMMARY_v1.0.0.md (15 KB)
  COMPETITIVE_ANALYSIS_QUICK_REFERENCE_v1.0.0.md (12 KB)
  INDEX_COMPETITIVE_ANALYSIS.md (this file)
```

---

## Next Steps

1. **Review key findings** - Start with QUICK_REFERENCE for overview
2. **Explore data** - Open competitive_relationships_v1.0.0.csv in Excel/Python
3. **Deep dive** - Read EXECUTIVE_SUMMARY for detailed patterns
4. **Extract insights** - Filter for specific companies/commodities of interest
5. **Validate** - Cross-reference with industry knowledge
6. **Extend analysis** - Consider temporal analysis (2023-2025 comparison)

---

## Contact / Questions

For questions about methodology, data quality, or analysis extensions, refer to:
- **Script documentation:** Comments in `analyze_competitive_landscape_v1.0.0.py`
- **Project README:** `G:\My Drive\LLM\project_manifest\README.md`
- **Claude instructions:** `G:\My Drive\LLM\project_manifest\CLAUDE.md`

---

**Analysis completed: 2026-02-05**
**Version: 1.0.0**
**Status: COMPLETE**
