# Index: Autonomous Trend Discovery Analyses
**Date**: 2026-02-05
**Status**: ✅ ALL ANALYSES COMPLETE

---

## 📚 Quick Navigation Guide

When you return, start here to explore the autonomous discoveries:

### 🎯 START HERE
**`AUTONOMOUS_TREND_DISCOVERY_SUMMARY_v1.0.0.md`** (This directory)
- Master summary of all 5 analysis streams
- Top discoveries across all dimensions
- 8 most surprising findings
- Complete file inventory

---

## 📊 Analysis 1: Commodity Trade Patterns

**KEY FINDING**: Martin Marietta has 2.7x market advantage via vertical integration

**Executive Summary**:
- `commodity_trade_lanes_executive_summary_v1.0.0.md` (21KB) ⭐ START HERE

**Quick Reference**:
- `commodity_trade_lanes_quick_reference_v1.0.0.md` (10KB)

**Detailed Data**:
- `commodity_trade_patterns_v1.0.0.csv` (252 rows)
  - Trade lanes, shippers, consignees, HS codes, origins, vessel types

**Script** (reusable):
- `../../02_SCRIPTS/02.04_analysis/analyze_commodity_trade_lanes_v1.0.0.py`

**Top Insights**:
1. Brazil = critical hub (32.9M tons via Sepetiba Bay)
2. Martin Marietta 10.2% vs Vulcan 3.8% market share
3. Chemical market 28.2% concentration (highest)
4. Canadian multi-commodity pipeline (32.9M tons)

---

## 🚢 Analysis 2: Vessel-Entity Relationships

**KEY FINDING**: Irving Oil uses 100% coastal tankers (unique strategy)

**Executive Summary**:
- `VESSEL_ENTITY_ANALYSIS_SUMMARY_v1.0.0.md` (14KB) ⭐ START HERE

**Quick Reference**:
- `VESSEL_ENTITY_KEY_FINDINGS_v1.0.0.txt` (13KB)

**Detailed Data**:
- `vessel_entity_relationships_v1.0.0.csv` (537KB, 4,468 vessel-entity pairs)
  - Entity-vessel patterns, carrier preferences, fleet analysis

**Script** (reusable):
- `../../02_SCRIPTS/02.04_analysis/analyze_vessel_entity_patterns_v1.0.0.py`

**Top Insights**:
1. Irving Oil: 84% carrier concentration with Vroon B.V.
2. Saudi Refining: 99% concentration (exclusive AET contract)
3. Chevron: 21.9M tons via owned captive fleet
4. Valero: Spot market strategy (24% top carrier)
5. Ternium: MINANUR CEBI 1 makes 88 visits (weekly JIT)

---

## 🏢 Analysis 3: Parent Company Consolidation

**KEY FINDING**: Chemical duopoly - ExxonMobil + Celanese = 98% control

**Executive Summary**:
- `PARENT_COMPANY_CONSOLIDATION_INSIGHTS_v1.0.0.md` (15KB) ⭐ START HERE

**Quick Reference**:
- `PARENT_CONSOLIDATION_QUICK_REFERENCE.txt`

**Detailed Data**:
- `parent_company_market_share_v1.0.0.csv` (Parent rankings)
- `corporate_family_structures_v1.0.0.csv` (3 multi-subsidiary families)
- `parent_company_by_commodity_v1.0.0.csv` (Sector-specific shares)

**Script** (reusable):
- `../../02_SCRIPTS/02.04_analysis/analyze_parent_company_rollups_v1.0.0.py`

**Top Insights**:
1. Chemicals: 98% duopoly (ExxonMobil 51.7% + Celanese 46.3%)
2. Top 6 US refiners control 65.4% of imports (175.2M tons)
3. HHI Consignee (1,052) > HHI Shipper (817) - US more concentrated
4. State enterprises control ~31% of shipper tonnage
5. Emirates consolidation: Dubai + Emirates = #6 overall

---

## 🏛️ Analysis 4: Port Specialization

**KEY FINDING**: Richmond, CA is most specialized crude terminal (84.5%)

**Executive Summary**:
- `PORT_SPECIALIZATION_EXECUTIVE_SUMMARY.md` ⭐ START HERE

**Detailed Profiles**:
- `PORT_PROFILES_HIGHLIGHTS.md` (Deep dives on interesting ports)

**Detailed Data**:
- `port_specialization_profiles_v1.0.0.csv` (20 US ports)
- `foreign_port_profiles_v1.0.0.csv` (20 foreign loading ports)
- `crude_terminal_sources_v1.0.0.csv` (Crude terminal rankings)
- `port_commodity_matrix_v1.0.0.csv` (Port × commodity pivot)

**Script** (reusable):
- `../../02_SCRIPTS/02.04_analysis/analyze_port_specialization_v1.0.0.py`

**Top Insights**:
1. Richmond, CA: 84.5% crude (beats Port Arthur's 80.3%)
2. Philadelphia: Most diversified (HHI 0.22, 11 commodities)
3. Auld's Cove: 99.99% aggregates (mono-commodity)
4. Aruba: 99% crude transshipment (masking Venezuelan origin)
5. Rotterdam: 88.3% chemicals (21% of US imports)

---

## ⚔️ Analysis 5: Competitive Landscape

**KEY FINDING**: 17,208 competitive relationships mapped

**Executive Summary**:
- `COMPETITIVE_LANDSCAPE_EXECUTIVE_SUMMARY_v1.0.0.md` (15KB) ⭐ START HERE

**Quick Reference**:
- `COMPETITIVE_ANALYSIS_QUICK_REFERENCE_v1.0.0.md` (12KB)

**Detailed Data**:
- `competitive_relationships_v1.0.0.csv` (3.8MB, 17,208 competitive pairs)
- `commodity_competition_v1.0.0.csv` (Top 3 by commodity)
- `port_competition_v1.0.0.csv` (22 port profiles)
- `competitive_examples_highlighted_v1.0.0.csv` (Oil refiners/traders)

**Script** (reusable):
- `../../02_SCRIPTS/02.04_analysis/analyze_competitive_landscape_v1.0.0.py`

**Top Insights**:
1. Chevron vs SOMO (Iraq): 4.8M tons overlap at San Francisco
2. UAE aluminum duopoly: Dubai vs Emirates (3.1M tons overlap)
3. PMI Trading internal competition (4+ entities vs themselves)
4. ExxonMobil vs Valero: 2.5M tons overlap (Mexico → Houston)
5. Martin Marietta dual strategy (own subsidiary + competitor sourcing)

---

## 🎁 Cross-Cutting Master Insights

### 1. **Market Concentration Paradox**
- Entity-level = fragmented appearance
- Parent-level = hidden oligopolies revealed
- Chemicals (98%), Construction (100%), Crude (75%)

### 2. **Vertical Integration = Market Power**
- Martin Marietta: Quarries + distribution = 2.7x advantage
- ExxonMobil: Shipper (13.1%) + Consignee (13.3%)
- Chevron: Fleet + refineries + trading

### 3. **Coastal vs Offshore Strategy**
- Coastal refiners: Small tankers, regional (Irving Oil)
- Offshore refiners: VLCC/Suezmax, deep-water (Marathon, Chevron)
- Mixed: Spot market flexibility (Valero)

### 4. **Geographic Chokepoints**
- Brazil (Sepetiba Bay): 32.9M tons, single terminal
- Rotterdam: 21% of chemical imports, European gateway
- Aruba: Pure transshipment masking Venezuela

### 5. **State Enterprise Control**
- 31% shipper tonnage: Iraq, Venezuela, Colombia, Saudi Arabia
- Geopolitical risk concentration

### 6. **Carrier Concentration Strategies**
- Dedicated (>80%): Irving, Saudi Refining
- Spot (<30%): Valero, ExxonMobil
- Mixed (30-50%): Chevron

---

## 📁 Complete File Structure

```
03_DOCUMENTATION/03.04_summaries/
│
├── INDEX_AUTONOMOUS_ANALYSES_v1.0.0.md ⭐ YOU ARE HERE
├── AUTONOMOUS_TREND_DISCOVERY_SUMMARY_v1.0.0.md ⭐ MASTER SUMMARY
│
├── [Commodity Analysis - 4 files]
│   ├── commodity_trade_patterns_v1.0.0.csv
│   ├── commodity_trade_lanes_executive_summary_v1.0.0.md ⭐
│   ├── commodity_trade_lanes_quick_reference_v1.0.0.md
│   └── commodity_analysis_script.py → 02_SCRIPTS/02.04_analysis/
│
├── [Vessel Analysis - 4 files]
│   ├── vessel_entity_relationships_v1.0.0.csv
│   ├── VESSEL_ENTITY_ANALYSIS_SUMMARY_v1.0.0.md ⭐
│   ├── VESSEL_ENTITY_KEY_FINDINGS_v1.0.0.txt
│   └── vessel_analysis_script.py → 02_SCRIPTS/02.04_analysis/
│
├── [Parent Company Analysis - 8 files]
│   ├── parent_company_market_share_v1.0.0.csv
│   ├── corporate_family_structures_v1.0.0.csv
│   ├── parent_company_by_commodity_v1.0.0.csv
│   ├── PARENT_COMPANY_CONSOLIDATION_INSIGHTS_v1.0.0.md ⭐
│   ├── PARENT_CONSOLIDATION_QUICK_REFERENCE.txt
│   └── [3 additional files]
│
├── [Port Specialization - 7 files]
│   ├── port_specialization_profiles_v1.0.0.csv
│   ├── foreign_port_profiles_v1.0.0.csv
│   ├── crude_terminal_sources_v1.0.0.csv
│   ├── PORT_SPECIALIZATION_EXECUTIVE_SUMMARY.md ⭐
│   ├── PORT_PROFILES_HIGHLIGHTS.md
│   └── [2 additional files]
│
└── [Competitive Landscape - 8 files]
    ├── competitive_relationships_v1.0.0.csv (3.8MB)
    ├── commodity_competition_v1.0.0.csv
    ├── port_competition_v1.0.0.csv
    ├── COMPETITIVE_LANDSCAPE_EXECUTIVE_SUMMARY_v1.0.0.md ⭐
    ├── COMPETITIVE_ANALYSIS_QUICK_REFERENCE_v1.0.0.md
    └── [3 additional files]
```

---

## 🚀 Recommended Reading Order

### 1️⃣ **Quick Orientation (10 minutes)**
Start with these 2 files:
- `AUTONOMOUS_TREND_DISCOVERY_SUMMARY_v1.0.0.md` (this summary)
- `INDEX_AUTONOMOUS_ANALYSES_v1.0.0.md` (navigation guide)

### 2️⃣ **Executive Overviews (30 minutes)**
Read all 5 executive summaries (⭐ marked above):
1. `commodity_trade_lanes_executive_summary_v1.0.0.md`
2. `VESSEL_ENTITY_ANALYSIS_SUMMARY_v1.0.0.md`
3. `PARENT_COMPANY_CONSOLIDATION_INSIGHTS_v1.0.0.md`
4. `PORT_SPECIALIZATION_EXECUTIVE_SUMMARY.md`
5. `COMPETITIVE_LANDSCAPE_EXECUTIVE_SUMMARY_v1.0.0.md`

### 3️⃣ **Deep Dives (1-2 hours)**
Open CSV files in Excel for detailed analysis:
- `commodity_trade_patterns_v1.0.0.csv` (252 rows) - Trade lane details
- `vessel_entity_relationships_v1.0.0.csv` (4,468 rows) - Vessel patterns
- `competitive_relationships_v1.0.0.csv` (17,208 rows) - Competition matrix

### 4️⃣ **Customize & Extend**
Run scripts with your own filters:
- All scripts are in `02_SCRIPTS/02.04_analysis/`
- Modify parameters to focus on specific entities, ports, or commodities
- Scripts are commented and reusable

---

## 💡 How to Use These Analyses

### For Competitive Intelligence
→ `competitive_relationships_v1.0.0.csv`
- Find who competes with your target company
- Identify overlapping trade lanes
- Quantify competitive intensity (tonnage overlap)

### For Port Selection
→ `port_specialization_profiles_v1.0.0.csv`
- Check port commodity specialization
- Find alternative ports with similar cargo mix
- Identify diversified vs specialist terminals

### For Carrier Negotiations
→ `vessel_entity_relationships_v1.0.0.csv`
- Benchmark carrier concentration strategies
- See which carriers serve which entities
- Spot market vs contract patterns

### For Market Share Analysis
→ `parent_company_market_share_v1.0.0.csv`
- Roll up subsidiaries to parent companies
- Calculate true market concentration
- Identify oligopolies by commodity

### For Trade Route Planning
→ `commodity_trade_patterns_v1.0.0.csv`
- Top origin-destination pairs by commodity
- Which entities dominate which routes
- Tonnage volumes and HS codes

---

## 📊 Data Coverage

**Total Records Analyzed**: 449,233 (2024 harmonized imports)
**Total Tonnage**: 723.68 million tons
**Total Value**: $1.2 trillion
**Harmonized Entities**: 27 (31-37% tonnage coverage)
**Ports Profiled**: 40 (20 US + 20 foreign)
**Vessels Tracked**: 8,034 unique vessels
**Carriers Identified**: 1,173 unique carriers
**Competitive Pairs**: 17,208 relationships

---

## 🎯 8 Most Surprising Findings

1. **Irving Oil's coastal-only strategy** - 100% Handy/MR tankers (unique among major refiners)
2. **Richmond > Port Arthur specialization** - 84.5% vs 80.3% crude specialization
3. **Chemical duopoly** - ExxonMobil + Celanese = 98% market control
4. **Aruba 99% transshipment** - pure logistics hub masking Venezuelan crude
5. **PMI Trading self-competition** - 4+ entities competing with themselves
6. **Martin Marietta 2.7x advantage** - vertical integration dominance
7. **Philadelphia > Houston diversity** - more diversified despite reputation
8. **Saudi Refining 99% concentration** - single carrier exclusive contract

---

## ✅ Next Steps When You Return

1. **Skim master summary** (5 min) - `AUTONOMOUS_TREND_DISCOVERY_SUMMARY_v1.0.0.md`
2. **Review executive summaries** (30 min) - All files marked ⭐
3. **Open CSVs in Excel** (1 hour) - Pivot tables, filters, drill-downs
4. **Cross-reference with domain knowledge** - Validate surprising findings
5. **Identify gaps** - What's missing? What needs deeper analysis?
6. **Request follow-ups** - Temporal trends (2023-2025)? Specific commodities?

---

## 📞 Quick Reference: File Purposes

| File Type | Purpose | Examples |
|-----------|---------|----------|
| **Executive Summary (.md)** | Strategic overview, key findings | COMPETITIVE_LANDSCAPE_EXECUTIVE_SUMMARY |
| **Quick Reference (.md/.txt)** | Fast lookup, Q&A format | VESSEL_ENTITY_KEY_FINDINGS |
| **Data CSV** | Detailed analysis results | competitive_relationships_v1.0.0.csv |
| **Script (.py)** | Reusable analysis engine | analyze_competitive_landscape_v1.0.0.py |
| **Index (.md)** | Navigation and file organization | INDEX_AUTONOMOUS_ANALYSES (this file) |

---

**All analyses complete and ready for your review.**
**All files located in**: `G:\My Drive\LLM\project_manifest\03_DOCUMENTATION\03.04_summaries\`

---

*Autonomous execution completed: 2026-02-05*
*Total runtime: ~5 hours*
*Files generated: 25+*
*Status: ✅ READY FOR REVIEW*
