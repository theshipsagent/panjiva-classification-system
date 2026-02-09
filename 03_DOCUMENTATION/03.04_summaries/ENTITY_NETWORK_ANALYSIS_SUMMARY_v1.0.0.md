# Entity Network Analysis Summary v1.0.0
**Date**: 2026-02-06
**Data Source**: panjiva_imports_2024_HARMONIZED_v1.1.0.csv
**Analysis Script**: analyze_entity_networks_v1.0.0.py

---

## Executive Summary

Analyzed entity relationships and network patterns across 449,233 import records (2024) using harmonized party names. Identified 52,179 unique entities participating in 28,845 shipper-consignee relationships totaling 555 million tons of cargo. The analysis reveals highly concentrated supply chains with 70% of shippers maintaining exclusive customer relationships, while the top 10 shippers control 31% of total tonnage.

**Key Finding**: 1,290 multi-role entities (2.5% of all entities) handle traffic from all three perspectives (shipper, consignee, notify party), with major petroleum companies like Chevron, Valero, and ExxonMobil maintaining complex internal transfer networks.

---

## Harmonization Coverage

| Field | Records Harmonized | Coverage |
|-------|-------------------|----------|
| **Shipper_Harmonized** | 339,143 | 75.5% |
| **Consignee_Harmonized** | 379,245 | 84.4% |
| **Notify Party_Harmonized** | 278,434 | 62.0% |
| **Both Shipper + Consignee** | 307,795 | 68.5% |

---

## Network-Wide Statistics

| Metric | Value | Description |
|--------|-------|-------------|
| **Total Unique Entities** | 52,179 | All entities across all roles |
| **Unique Shippers** | 12,676 | Entities appearing as shippers |
| **Unique Consignees** | 17,009 | Entities appearing as consignees |
| **Unique Notify Parties** | 23,815 | Customs brokers/agents |
| **Multi-Role Entities** | 1,290 (2.5%) | Entities in 2+ roles |
| **Shipper-Consignee Pairs** | 28,845 | Unique relationships |
| **Total Tonnage** | 555,488,496 | Captured in shipper-consignee relationships |

### Network Density Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Avg Customers per Shipper** | 2.28 | Most shippers supply 2-3 customers |
| **Avg Suppliers per Consignee** | 1.70 | Most consignees source from 1-2 suppliers |
| **Exclusive Shippers** | 8,885 (70.1%) | Shippers with single customer |
| **Top 10 Shipper Concentration** | 30.6% | Moderately concentrated supply side |
| **Top 10 Consignee Concentration** | 39.0% | More concentrated demand side |

**Key Insight**: The network is characterized by **high exclusivity** (70% of shippers supply a single customer) combined with **moderate concentration** (top 10 entities control 30-40% of flows). This suggests a mix of dedicated supplier relationships and diversified sourcing strategies.

---

## 1. Top Shipper-Consignee Relationships

### Top 20 by Tonnage (555M tons total)

| Rank | Shipper | Consignee | Tons | Shipments | Pattern |
|------|---------|-----------|------|-----------|---------|
| 1 | **Chevron** | **Chevron** | 21,632,294 | 646 | Internal Transfer |
| 2 | **Irving Oil** | **Irving Oil** | 18,220,175 | 2,700 | Internal Transfer |
| 3 | **PMI Trading** | **Valero** | 16,424,365 | 332 | Trading → Refiner |
| 4 | **Bolanter Corporation** | **Saudi Refining Inc** | 14,980,446 | 216 | Trading → Refiner |
| 5 | **Valero** | **Valero** | 10,255,852 | 397 | Internal Transfer |
| 6 | **Ecopetrol** | **Ecopetrol** | 8,361,024 | 116 | Internal Transfer |
| 7 | **PBF Energy** | **PBF Energy** | 8,153,373 | 146 | Internal Transfer |
| 8 | **ExxonMobil** | **ExxonMobil** | 7,673,327 | 236 | Internal Transfer |
| 9 | **PDVSA** | **Chevron** | 7,228,288 | 116 | NOC → Refiner |
| 10 | **State Oil Marketing (SOMO)** | **Chevron** | 6,701,045 | 147 | NOC → Refiner |
| 11 | **PMI Trading** | **PMI Trading** | 6,541,391 | 97 | Internal Transfer |
| 12 | **Petropiar** | **Chevron** | 6,461,493 | 93 | JV → Parent |
| 13 | **Ternium** | **Ternium** | 6,202,458 | 131 | Internal Transfer |
| 14 | **Chevron** | **Valero** | 5,742,494 | 206 | Refiner → Refiner |
| 15 | **Orca Sand and Gravel** | **Emirates Aluminium** | 5,550,969 | 186 | Supplier → Manufacturer |
| 16 | **Martin Marietta** | **Martin Marietta** | 5,216,170 | 103 | Internal Transfer |
| 17 | **State Oil Marketing (SOMO)** | **Marathon Petroleum** | 4,861,911 | 30 | NOC → Refiner |
| 18 | **PMI Trading** | **Chevron** | 4,654,909 | 74 | Trading → Refiner |
| 19 | **Celanese** | **Celanese** | 4,588,386 | 199 | Internal Transfer |
| 20 | **Compania Minera** | **Mosaic** | 4,482,763 | 84 | Miner → Fertilizer |

### Relationship Patterns Identified

1. **Internal Transfers** (8 of top 20): Major refiners and manufacturers moving product between facilities
   - Chevron, Irving Oil, Valero, ExxonMobil, PBF Energy
   - Accounts for ~64M tons (11.5% of total)

2. **Trading Intermediaries** (5 of top 20): PMI Trading as dominant petroleum broker
   - PMI → Valero (16.4M), PMI → Chevron (4.7M), PMI → PMI (6.5M)
   - Total PMI relationships: ~27M tons

3. **National Oil Companies → Refiners** (4 of top 20): SOMO, PDVSA, Petropiar
   - Iraqi crude (SOMO), Venezuelan crude (PDVSA/Petropiar)
   - Accounts for ~24M tons (4.4% of total)

4. **Dedicated Supply Chains** (3 of top 20):
   - Bauxite: Orca → EGA (5.6M tons)
   - Phosphate: Compania Minera → Mosaic (4.5M tons)
   - Aggregates: Bahama Rock → Martin Marietta

---

## 2. Top 10 Shippers - Customer Analysis

### Shipper Profiles (170M tons, 31% of total)

| Rank | Shipper | Total Tons | Customers | Top Customer | Concentration |
|------|---------|-----------|-----------|--------------|---------------|
| 1 | **PMI Trading** | 40,848,650 | 27 | Valero (16.4M) | 50.6% to top 5 |
| 2 | **Chevron** | 28,006,105 | 13 | Chevron (21.6M) | 77.7% internal |
| 3 | **Irving Oil** | 18,945,929 | 15 | Irving Oil (18.2M) | 96.9% internal |
| 4 | **SOMO** | 15,507,624 | 15 | Chevron (6.7M) | 43.3% diversified |
| 5 | **Bolanter Corp** | 14,980,446 | 1 | Saudi Refining (15M) | 100% exclusive |
| 6 | **Ecopetrol** | 11,932,934 | 28 | Ecopetrol (8.4M) | 70.1% internal |
| 7 | **Valero** | 11,070,498 | 15 | Valero (10.3M) | 92.6% internal |
| 8 | **Trafigura** | 9,981,441 | 38 | Trafigura (3.9M) | 39.2% diversified |
| 9 | **ExxonMobil** | 9,563,714 | 20 | ExxonMobil (7.7M) | 80.3% internal |
| 10 | **Emirates Aluminium** | 9,379,132 | 65 | EGA (4.3M) | 45.3% diversified |

### Customer Concentration Patterns

**High Internal Transfer (>90%)**: Irving Oil, Valero, Bolanter
- Strategy: Self-supply, vertical integration
- Risk: Low external exposure

**Moderate Internal (70-80%)**: Chevron, Ecopetrol, ExxonMobil
- Strategy: Internal + strategic external sales
- Balance: Self-supply with market participation

**Diversified Shippers (<50%)**: PMI Trading, SOMO, Trafigura, EGA
- Strategy: Trading intermediaries or commodity exporters
- Pattern: Multiple customers, spread risk

### Top 5 Customer Breakdown (Full Details)

#### PMI Trading (40.8M tons → 27 customers)
1. Valero: 16,424,365 tons (40.2% share)
2. PMI Trading: 6,541,391 tons (16.0% - internal)
3. Chevron: 4,654,909 tons (11.4%)
4. PBF Energy: 2,595,396 tons (6.4%)
5. ExxonMobil: 2,226,446 tons (5.5%)

**Profile**: Dominant petroleum trading intermediary serving U.S. refining industry

#### Chevron (28.0M tons → 13 customers)
1. Chevron: 21,632,294 tons (77.2% - internal)
2. Valero: 5,742,494 tons (20.5%)
3. PBF Energy Ltd: 267,968 tons (1.0%)
4. Citgo: 97,880 tons (0.3%)
5. Houston Refining: 88,588 tons (0.3%)

**Profile**: Primarily self-supply with strategic sales to Valero

#### Irving Oil (18.9M tons → 15 customers)
1. Irving Oil: 18,220,175 tons (96.2% - internal)
2. Bitumar USA: 294,697 tons (1.6%)
3. Puerto Rico Energy: 196,125 tons (1.0%)
4. IIG Capital: 64,640 tons (0.3%)
5. Sunoco LLC: 29,404 tons (0.2%)

**Profile**: Highly vertically integrated Canadian refiner

#### SOMO (Iraqi Oil) (15.5M tons → 15 customers)
1. Chevron: 6,701,045 tons (43.2%)
2. Marathon Petroleum: 4,861,911 tons (31.4%)
3. Valero: 1,828,861 tons (11.8%)
4. Eni Trade & Biofuels: 857,808 tons (5.5%)
5. Raiffeisen Bank: 359,444 tons (2.3%)

**Profile**: Iraqi national oil company diversified across U.S. refiners

#### Emirates Aluminium (9.4M tons → 65 customers)
1. Emirates Aluminium: 4,250,608 tons (45.3% - internal)
2. Vulcan Materials: 2,889,136 tons (30.8%)
3. Blue Water Industries: 1,809,300 tons (19.3%)
4. Naturgy: 116,058 tons (1.2%)
5. Orca Sand and Gravel: 58,000 tons (0.6%)

**Profile**: Bauxite/aggregates exporter to construction materials sector

---

## 3. Notify Party Patterns

### Top 20 Customs Brokers/Agents (230,083 records with notify party data)

| Rank | Notify Party | Shipments | Shippers | Consignees | Role |
|------|--------------|-----------|----------|------------|------|
| 1 | **721 Logistics LLC** | 12,602 | 1 | 1 | Dedicated broker (UPM Naperville) |
| 2 | **Royal Caribbean/Celebrity** | 3,874 | 2 | 3 | Cruise line logistics |
| 3 | **Komatsu America Corp** | 3,816 | 1 | 1 | Self-notify (equipment) |
| 4 | **Valero** | 2,024 | 165 | 45 | Refiner self-notify |
| 5 | **John S James Company** | 1,856 | 1 | 1 | Volvo CE dedicated |
| 6 | **Del Monte Fresh Produce** | 1,761 | 6 | 6 | Self-notify (produce) |
| 7 | **GM Finance-Tax Staff** | 1,563 | 3 | 3 | Auto manufacturer |
| 8 | **Masterpiece International** | 1,259 | 6 | 71 | 3PL broker |
| 9 | **Okuma America Corp** | 1,249 | 1 | 1 | Self-notify (machinery) |
| 10 | **Volkswagen de Mexico** | 1,230 | 14 | 1 | Auto OEM |
| 11 | **John S James Company (Carson)** | 1,103 | 6 | 3 | 3PL broker |
| 12 | **Chevron** | 1,078 | 74 | 38 | Refiner self-notify |
| 13 | **Hyundai Motor America** | 1,036 | 3 | 1 | Auto OEM |
| 14 | **Expeditors International** | 993 | 5 | 1 | 3PL freight forwarder |
| 15 | **Masterpiece International (PA)** | 974 | 1 | 81 | 3PL broker |
| 16 | **GAC North America** | 966 | 197 | 320 | Diversified shipping agent |
| 17 | **Mazak Corporation** | 963 | 1 | 1 | Self-notify (machinery) |
| 18 | **Emirates Aluminium** | 960 | 130 | 136 | Self-notify (bulk) |
| 19 | **Subaru of America** | 940 | 2 | 2 | Auto OEM |
| 20 | **Axiom World Wide Logistics** | 923 | 3 | 4 | Tenaris dedicated |

### Notify Party Categories

1. **Self-Notify (Consignee as Notify)**: Large importers handle own customs
   - Valero, Chevron, EGA, Komatsu, Del Monte
   - Pattern: High-volume, sophisticated importers

2. **Dedicated Brokers**: Single client relationships
   - 721 Logistics → UPM (12,602 shipments)
   - Axiom → Tenaris (923 shipments)
   - John S James → Volvo CE (1,856 shipments)

3. **Third-Party Logistics (3PL)**: Multi-client brokers
   - Masterpiece International (2,233 shipments, 152 clients)
   - GAC North America (966 shipments, 517 combined entities)
   - Expeditors International (993 shipments)

4. **OEM Logistics**: Auto manufacturers
   - VW, Hyundai, GM, Subaru handle own import clearance

### Top Consignee-NotifyParty Pairs

| Consignee | Notify Party | Shipments | Tons | Pattern |
|-----------|--------------|-----------|------|---------|
| UPM Naperville | 721 Logistics | 12,602 | 764,135 | Dedicated broker |
| Komatsu America | Komatsu America | 3,816 | 145,435 | Self-notify |
| Royal Caribbean | Royal Caribbean | 3,688 | 7 | Self-notify |
| Volvo CE | John S James | 1,856 | 61,983 | Dedicated broker |
| Volkswagen Mexico | VW Mexico | 1,230 | 201,813 | Self-notify |
| **Valero** | **Valero** | 1,103 | **39,953,831** | Self-notify (petroleum) |
| **Chevron** | **Chevron** | 874 | **41,990,947** | Self-notify (petroleum) |

**Key Finding**: Petroleum refiners (Valero, Chevron) handle own customs clearance for massive tonnage shipments (40M+ tons each), while machinery importers use dedicated 3PL brokers.

---

## 4. Multi-Role Entities (1,290 entities)

### Top 30 Multi-Role Entities by Total Tonnage

Entities appearing in 2+ roles (shipper, consignee, notify party):

| Rank | Entity | Roles | Shipper Tons | Consignee Tons | Notify Tons | Total Tons |
|------|--------|-------|--------------|----------------|-------------|------------|
| 1 | **Chevron** | S+C+N | 28,006,105 | 56,791,997 | 48,973,769 | 133,771,871 |
| 2 | **Valero** | S+C+N | 11,070,498 | 43,375,095 | 51,680,822 | 106,126,416 |
| 3 | **PMI Trading** | S+C+N | 40,848,650 | 6,978,566 | 5,389,929 | 53,217,145 |
| 4 | **Irving Oil** | S+C+N | 18,945,929 | 18,220,175 | 486,444 | 37,652,548 |
| 5 | **PBF Energy** | S+C+N | 8,153,373 | 17,640,898 | 11,497,017 | 37,291,289 |
| 6 | **ExxonMobil** | S+C+N | 9,563,714 | 15,746,438 | 11,003,284 | 36,313,436 |
| 7 | **Marathon Petroleum** | S+C+N | 1,149,798 | 17,602,242 | 12,388,101 | 31,140,141 |
| 8 | **Emirates Aluminium** | S+C+N | 9,379,132 | 15,226,360 | 665,503 | 25,270,995 |
| 9 | **Ternium** | S+C+N | 6,259,517 | 8,372,262 | 8,185,548 | 22,817,327 |
| 10 | **Ecopetrol** | S+C+N | 11,932,934 | 8,441,056 | 1,326,812 | 21,700,803 |
| 11 | **ArcelorMittal** | S+C+N | 8,481,644 | 6,770,920 | 2,076,419 | 17,328,983 |
| 12 | **SOMO** | S+N | 15,507,624 | 0 | 63 | 15,507,687 |
| 13 | **Motiva Enterprises** | C+N | 0 | 474,163 | 14,807,533 | 15,281,696 |
| 14 | **Trafigura** | S+C+N | 9,981,441 | 4,734,766 | 82,130 | 14,798,337 |
| 15 | **Monroe Energy** | S+C+N | 1,106,323 | 5,483,735 | 7,909,919 | 14,499,978 |
| 16 | **Citgo** | S+C+N | 503,859 | 5,037,822 | 8,279,003 | 13,820,684 |
| 17 | **Celanese** | S+C+N | 4,588,391 | 4,592,362 | 4,590,323 | 13,771,075 |
| 18 | **Martin Marietta** | S+C | 5,216,170 | 8,481,079 | 0 | 13,697,249 |
| 19 | **Houston Refining** | C+N | 0 | 3,127,075 | 8,640,165 | 11,767,240 |
| 20 | **Eucatex** | S+C+N | 3,580,056 | 3,579,905 | 3,579,905 | 10,739,866 |

### Multi-Role Categories

#### Triple-Role Entities (S+C+N): 1,189 entities
- **Petroleum Majors**: Chevron, Valero, ExxonMobil, Marathon
  - Pattern: Ship crude, receive refined products, manage own clearance
  - Total involvement: 300M+ tons across all roles

- **Trading Intermediaries**: PMI Trading, Trafigura, Vitol
  - Pattern: Buy/sell as both shipper and consignee, self-clear

- **Vertically Integrated Manufacturers**: Ternium, Celanese, Eucatex
  - Pattern: Ship raw materials, receive finished goods, self-clear

#### Dual-Role Entities (S+C only): 72 entities
- **Aggregates**: Martin Marietta, Lafarge, Vulcan Materials
- **Commodity Exporters**: Orca Sand and Gravel, Interpipe

#### Dual-Role Entities (C+N only): 29 entities
- **Import-Only Refiners**: Houston Refining, Paulsboro Refining, Delaware City
- **Logistics Providers**: Motiva Enterprises (Shell JV)

**Key Pattern**: Entities with both S+C roles typically represent:
1. Internal transfers between facilities (Chevron, Valero)
2. Trading operations (buy as consignee, resell as shipper)
3. Tolling arrangements (ship crude, receive refined products)

---

## 5. Entity Clusters - Co-Occurrence Analysis

### Top 30 Entity Pairs (Frequently Trade Together)

| Rank | Entity 1 | Entity 2 | Co-occurrences | Cluster Type |
|------|----------|----------|----------------|--------------|
| 1 | Toyota Motor Corp | Toyota Motor Sales | 1,039 | **Auto OEM** |
| 2 | **Valero** | **PMI Trading** | 332 | **Petroleum Trading** |
| 3 | New Fortress Energy | NFE Transport Partners | 248 | **LNG/Energy** |
| 4 | Saudi Refining | Bolanter Corp | 216 | **Petroleum** |
| 5 | **Chevron** | **Valero** | 206 | **Refiner-to-Refiner** |
| 6 | Dubai Aluminium | Emirates Aluminium | 201 | **Aluminum** |
| 7 | Orca Sand | Emirates Aluminium | 188 | **Bauxite/Aggregates** |
| 8 | North American Marine | Interpipe | 187 | **Steel Pipe** |
| 9 | **SOMO** | **Chevron** | 147 | **Crude Oil Imports** |
| 10 | **PDVSA** | **Chevron** | 116 | **Venezuelan Crude** |
| 11 | Discovery Bauxite | Atalco Gramercy | 96 | **Bauxite** |
| 12 | Petropiar | Chevron | 93 | **Venezuelan JV** |
| 13 | Bahama Rock | Martin Marietta | 89 | **Aggregates** |
| 14 | Sociedad Punta de Lobos | Morton Salt | 88 | **Salt** |
| 15 | Compania Minera | Mosaic | 84 | **Phosphate** |
| 16 | PMI Trading | ExxonMobil | 83 | **Petroleum Trading** |
| 17 | Chevron | PMI Trading | 74 | **Petroleum Trading** |
| 18 | Taiheiyo Cement | Glacier Northwest | 73 | **Cement** |
| 19 | Vulcan Materials | Emirates Aluminium | 69 | **Aggregates** |
| 20 | PMI Trading | PBF Energy | 68 | **Petroleum Trading** |
| 21 | Drummond | AES Puerto Rico | 66 | **Coal Power** |
| 22 | Trafigura | Marathon Petroleum | 49 | **Petroleum Trading** |
| 23 | Eastern Salt | Compania Minera | 46 | **Salt** |
| 24 | EGA | Blue Water Industries | 36 | **Bauxite** |
| 25 | Vissai Ninh Binh | Cemex | 36 | **Cement** |
| 26 | Chevron | Trafigura | 35 | **Petroleum Trading** |
| 27 | Valero | Gunvor Group | 33 | **Petroleum Trading** |
| 28 | Marathon | PMI Trading | 32 | **Petroleum Trading** |
| 29 | Valero | SOMO | 32 | **Iraqi Crude** |
| 30 | Medcem Global | Cemex | 31 | **Cement** |

### Identified Industry Clusters

#### 1. Petroleum Trading Network (300+ co-occurrences)
**Core Entities**: PMI Trading, Chevron, Valero, ExxonMobil, Marathon, Trafigura, Vitol, Gunvor
- **Pattern**: PMI Trading as central hub connecting refiners
- **Key Relationships**:
  - PMI → Valero (332 shipments)
  - Chevron ↔ Valero (206 shipments)
  - PMI → ExxonMobil (83 shipments)
  - PMI → PBF Energy (68 shipments)
- **Interpretation**: Spot market crude oil trading network with PMI as dominant intermediary

#### 2. Iraqi Crude Import Network (209 co-occurrences)
**Core Entities**: SOMO (Iraqi national oil), Chevron, Marathon, Valero, Eni
- **Pattern**: SOMO supplies U.S. Gulf Coast refiners (Basrah crude)
- **Key Relationships**:
  - SOMO → Chevron (147 shipments)
  - SOMO → Marathon (30 shipments)
  - SOMO → Valero (32 shipments)

#### 3. Venezuelan Crude Network (209 co-occurrences)
**Core Entities**: PDVSA, Petropiar (Chevron JV), Chevron
- **Pattern**: Venezuelan heavy crude via Chevron JV and direct PDVSA
- **Key Relationships**:
  - PDVSA → Chevron (116 shipments)
  - Petropiar → Chevron (93 shipments)

#### 4. Bauxite/Alumina Network (421 co-occurrences)
**Core Entities**: Emirates Aluminium (EGA), Dubai Aluminium, Orca Sand, Vulcan, Blue Water, Discovery Bauxite, Atalco Gramercy
- **Pattern**: Middle East bauxite to U.S. aluminum smelters
- **Key Relationships**:
  - Dubai Al → EGA (201 shipments)
  - Orca Sand → EGA (188 shipments)
  - Discovery Bauxite → Atalco (96 shipments)

#### 5. Construction Materials Network (193 co-occurrences)
**Core Entities**: Martin Marietta, Bahama Rock, Vulcan Materials, Cemex, Taiheiyo Cement, Glacier Northwest
- **Pattern**: Caribbean aggregates + Asian cement to U.S. construction
- **Key Relationships**:
  - Bahama Rock → Martin Marietta (89 shipments)
  - Taiheiyo → Glacier Northwest (73 shipments)
  - Vissai Ninh Binh → Cemex (36 shipments)

#### 6. Phosphate/Fertilizer Network (130 co-occurrences)
**Core Entities**: Compania Minera, Mosaic, Eastern Salt
- **Pattern**: Latin American phosphate rock to U.S. fertilizer producers
- **Key Relationships**:
  - Compania Minera → Mosaic (84 shipments)
  - Compania Minera → Eastern Salt (46 shipments)

#### 7. Steel/Pipe Network (187 co-occurrences)
**Core Entities**: Ternium, ArcelorMittal, Interpipe, North American Marine
- **Pattern**: Steel products imports
- **Key Relationships**:
  - North American Marine → Interpipe (187 shipments)

#### 8. Automotive OEM Network (1,039 co-occurrences)
**Core Entities**: Toyota Motor Corp, Toyota Motor Sales, Hyundai, VW, GM, Subaru
- **Pattern**: Auto manufacturers to dealership networks
- **Key Relationships**:
  - Toyota Corp → Toyota Sales (1,039 shipments - highest co-occurrence)

---

## 6. Network Insights by Commodity

### Petroleum Products (Liquid Bulk)

**Network Structure**: Hub-and-spoke with trading intermediaries
- **Hubs**: PMI Trading, Chevron, Valero
- **Spokes**: National oil companies (SOMO, PDVSA, Ecopetrol) and refiners

**Relationship Patterns**:
1. **Internal Transfers** (64M tons): Refiners moving product between facilities
2. **Trading Intermediation** (50M+ tons): PMI Trading connecting suppliers to refiners
3. **Direct NOC Sales** (25M tons): SOMO, PDVSA selling directly to U.S. refiners

**Multi-Role Dynamics**:
- Chevron: Ships 28M tons, receives 57M tons, clears 49M tons
- Valero: Ships 11M tons, receives 43M tons, clears 52M tons
- **Interpretation**: Large refiners both export and import depending on facility needs and market conditions

### Bauxite/Alumina/Aggregates

**Network Structure**: Dedicated supply chains
- **Suppliers**: Emirates Aluminium (9.4M tons), Orca Sand (5.6M tons), Dubai Aluminium
- **Consumers**: Vulcan Materials, Martin Marietta, Blue Water Industries

**Relationship Patterns**:
1. **Single-Source Relationships**: Orca exclusively supplies EGA (188 shipments)
2. **Regional Clusters**: Middle East exporters → U.S. Gulf Coast + East Coast
3. **Construction Materials**: Bahama Rock → Martin Marietta (aggregates for concrete)

### Steel/Metals

**Network Structure**: Mixed internal transfers + trading
- **Shippers**: Ternium (6.3M tons), ArcelorMittal (8.5M tons)
- **Patterns**: High internal transfer rates (75%+)
- **Trading**: North American Marine as intermediary for Ukrainian steel (Interpipe)

### Cement

**Network Structure**: Asian cement → U.S. West Coast
- **Suppliers**: Taiheiyo Cement, Vissai Ninh Binh (Vietnam), Medcem
- **Consumers**: Cemex, Glacier Northwest
- **Pattern**: Import substitution for regional construction demand

---

## 7. Key Findings & Strategic Insights

### Finding 1: High Network Exclusivity (70%)
**Observation**: 8,885 shippers (70.1%) supply a single customer
**Interpretation**:
- Dedicated supply chain relationships dominate
- Examples: Bolanter → Saudi Refining (100%), Orca → EGA (100%)
- Indicates long-term contracts, vertical integration, or captive suppliers

**Business Implications**:
- Low supplier competition for many relationships
- High switching costs for consignees
- Potential supply chain vulnerability if single source fails

### Finding 2: Moderate Market Concentration (30-40%)
**Observation**: Top 10 shippers control 30.6% of tonnage, top 10 consignees receive 39%
**Interpretation**:
- Not dominated by a few players (vs. 50%+ in highly concentrated markets)
- Mix of large multinationals and mid-sized specialized traders
- Room for competitive dynamics and new entrants

**Strategic Insight**: Market is concentrated enough for scale advantages but diversified enough for competition

### Finding 3: Multi-Role Entities Control 40%+ of Flows
**Observation**: 1,290 multi-role entities (2.5% of all) handle disproportionate tonnage
**Interpretation**:
- Integrated petroleum companies (Chevron, Valero, ExxonMobil) control entire supply chain
- Trading firms (PMI, Trafigura) buy and resell within same dataset
- Self-clearance indicates sophisticated import operations

**Competitive Advantage**: Multi-role entities benefit from:
- Vertical integration (lower transaction costs)
- Market intelligence (visibility across supply chain)
- Operational control (self-clearance, logistics management)

### Finding 4: Trading Intermediaries Add 50M+ Tons of Flow
**Observation**: PMI Trading, Trafigura, Vitol, Gunvor appear in multiple relationships
**Interpretation**:
- Petroleum spot market relies on trading intermediaries
- PMI Trading alone handles 40.8M tons as shipper (7% of total tonnage)
- Trading firms connect NOCs (SOMO, PDVSA) to U.S. refiners

**Market Structure**: Petroleum imports operate on hub-and-spoke model with traders as hubs

### Finding 5: Industry-Specific Network Topologies
**Petroleum**: Hub-and-spoke (centralized trading)
**Bauxite/Aggregates**: Point-to-point (dedicated suppliers)
**Automotive**: Tree structure (OEM → dealerships)
**Cement**: Regional clusters (Asian imports → West Coast)

**Strategic Implication**: Different commodities require different sourcing strategies
- Petroleum: Access to trading networks critical
- Bauxite: Long-term supply contracts essential
- Automotive: Dealership network optimization
- Cement: Regional logistics efficiency

### Finding 6: Self-Clearance Indicates Sophistication
**Observation**: Top tonnage importers (Chevron, Valero) self-clear customs (C=N pattern)
**Interpretation**:
- High-volume importers invest in customs expertise
- Avoid 3PL fees, maintain control over clearance timing
- Machinery importers (Komatsu, Okuma) prefer dedicated 3PL brokers

**Operational Insight**: Customs clearance strategy correlates with:
- Import volume (high volume → self-clear)
- Commodity complexity (petroleum → self-clear; machinery → 3PL)
- Frequency (daily shipments → self-clear; occasional → 3PL)

---

## 8. Data Quality & Limitations

### Harmonization Gaps
- **Shipper Coverage**: 75.5% (110K records unharmonized)
- **Consignee Coverage**: 84.4% (70K records unharmonized)
- **Notify Party Coverage**: 62.0% (171K records unharmonized)

**Impact on Analysis**:
- 141,438 records (31.5%) excluded due to missing shipper or consignee harmonization
- Notify party analysis based on 51% of total records
- Potential bias toward large, well-known entities (easier to harmonize)

### Entity Name Variations
- Some relationships may be undercounted due to harmonization misses
- Example: "Chevron" vs "Chevron USA" vs "Chevron Products Company" (ideally consolidated)

### Role Ambiguity
- Notify party role varies:
  - Sometimes = customs broker (third party)
  - Sometimes = consignee self-notification
  - Sometimes = freight forwarder
- Analysis treats all as "notify party" without distinguishing subtype

### Temporal Coverage
- Analysis covers 2024 only (single year snapshot)
- Relationships may evolve year-over-year (supplier changes, market shifts)
- Seasonality not captured (e.g., heating oil imports higher in Q4)

---

## 9. Recommendations for Future Analysis

### 1. Multi-Year Network Evolution
- Compare 2023 vs 2024 vs 2025 networks
- Identify relationship churn (new suppliers, lost customers)
- Track market share shifts (e.g., PMI Trading growth)

### 2. Commodity-Specific Network Analysis
- Separate petroleum, steel, aggregates, grain networks
- Calculate commodity-specific concentration ratios
- Identify dominant players per commodity

### 3. Geographic Network Mapping
- Analyze port-to-port flows (origin → destination)
- Identify regional trade corridors (Gulf Coast crude, West Coast cement)
- Map entity presence by port (which refiners use which ports)

### 4. Network Centrality Metrics
- Calculate degree centrality (most-connected entities)
- Calculate betweenness centrality (entities bridging clusters)
- Calculate PageRank (influence within network)

### 5. Supply Chain Risk Analysis
- Identify single-source dependencies (consignees with 1 supplier)
- Map geopolitical risk (reliance on Venezuelan/Iraqi crude)
- Calculate supply chain concentration indices

### 6. Trading Pattern Classification
- Classify relationships as:
  - Internal transfer (S=C)
  - Direct trade (S≠C, no intermediary)
  - Intermediated trade (S→Trader→C)
- Quantify intermediation rates by commodity

### 7. Notify Party Deep Dive
- Separate customs brokers from self-notification
- Analyze broker market share (top 10 brokers)
- Map consignee-broker loyalty (exclusive vs. multi-broker)

---

## 10. Files Generated

| File | Records | Description |
|------|---------|-------------|
| **entity_relationships_shipper_consignee_v1.0.0.csv** | 28,845 | All shipper→consignee relationships with tonnage |
| **top_shippers_customer_analysis_v1.0.0.csv** | 50 | Top 10 shippers + their top 5 customers |
| **entity_multi_role_analysis_v1.0.0.csv** | 1,290 | Entities in 2+ roles with tonnage breakdown |
| **entity_relationships_all_roles_v1.0.0.csv** | 90,053 | All relationships (S→C, C→N, S→N) |
| **entity_network_statistics_v1.0.0.csv** | 13 | Summary metrics |
| **entity_cooccurrence_matrix_v1.0.0.csv** | 2,928 | Entity pairs that trade together (top 80 entities) |

**Total Dataset**: 307,795 records (68.5% of 2024 imports) with both shipper + consignee harmonized

---

## Conclusion

The 2024 U.S. import network reveals a complex maritime trade ecosystem characterized by:
1. **High exclusivity** (70% dedicated supplier relationships)
2. **Moderate concentration** (top 10 entities control 30-40% of flows)
3. **Sophisticated multi-role entities** (petroleum majors handling 100M+ tons across all roles)
4. **Industry-specific topologies** (hub-and-spoke petroleum vs. point-to-point aggregates)
5. **Strong intermediation** (trading firms bridge 50M+ tons of flows)

The petroleum sector dominates network complexity with entities like Chevron and Valero operating simultaneously as shippers, consignees, and notify parties handling 133M and 106M tons respectively. Trading intermediaries like PMI Trading serve as critical hubs connecting national oil companies to U.S. refiners, while dedicated supply chains (bauxite, phosphate) operate on exclusive long-term relationships.

This network structure reflects rational economic behavior: petroleum markets require liquidity and intermediation (spot trading), while bulk commodities benefit from dedicated supply relationships (contract mining). The high self-clearance rate among top importers (Chevron, Valero clearing own 40M+ ton shipments) demonstrates sophisticated logistics capabilities concentrated among market leaders.

---

**Analysis Completed**: 2026-02-06
**Script Version**: analyze_entity_networks_v1.0.0.py
**Data Version**: panjiva_imports_2024_HARMONIZED_v1.1.0.csv
