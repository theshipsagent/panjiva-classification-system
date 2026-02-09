# Preprocessing Column Map
**Raw → Preprocessed Transformation**

---

## Starting Columns (RAW) - 135 columns

```
1. Bill of Lading Number
2. Bill of Lading Type
3. Master Bill of Lading Number
4. Arrival Date
5. Matching Fields
6. Consignee
7. Consignee Address
8. Consignee City
9. Consignee State/Region
10. Consignee Postal Code
11. Consignee Country
12. Consignee Full Address
13. Consignee Email 1
14. Consignee Email 2
15. Consignee Email 3
16. Consignee Phone 1
17. Consignee Phone 2
18. Consignee Phone 3
19. Consignee Fax
20. Consignee Website 1
21. Consignee Website 2
22. Consignee Profile
23. Consignee SPCIQ ID
24. Consignee MI Key
25. Consignee D-U-N-S®
26. Consignee Industry
27. Consignee Revenue
28. Consignee Employees
29. Consignee Market Capitalization
30. Consignee Incorporation Year
31. Consignee Trade Roles
32. Consignee SIC Codes
33. Consignee Stock Tickers
34. Consignee (Original Format)
35. Consignee Global HQ
36. Consignee Global HQ Address
37. Consignee Global HQ D-U-N-S®
38. Consignee Domestic HQ
39. Consignee Domestic HQ Address
40. Consignee Domestic HQ D-U-N-S®
41. Consignee Ultimate Parent
42. Consignee Ultimate Parent Website
43. Consignee Ultimate Parent Headquarters Address
44. Consignee Ultimate Parent Profile
45. Consignee Ultimate Parent SPCIQ ID
46. Consignee Ultimate Parent MI Key
47. Consignee Ultimate Parent Stock Tickers
48. Shipper
49. Shipper Address
50. Shipper City
51. Shipper State/Region
52. Shipper Postal Code
53. Shipper Country
54. Shipper Full Address
55. Shipper Email 1
56. Shipper Email 2
57. Shipper Email 3
58. Shipper Phone 1
59. Shipper Phone 2
60. Shipper Phone 3
61. Shipper Fax
62. Shipper Website 1
63. Shipper Website 2
64. Shipper Profile
65. Shipper SPCIQ ID
66. Shipper MI Key
67. Shipper D-U-N-S®
68. Shipper Industry
69. Shipper Revenue
70. Shipper Employees
71. Shipper Market Capitalization
72. Shipper Incorporation Year
73. Shipper Trade Roles
74. Shipper SIC Codes
75. Shipper Stock Tickers
76. Shipper (Original Format)
77. Shipper Global HQ
78. Shipper Global HQ Address
79. Shipper Global HQ D-U-N-S®
80. Shipper Domestic HQ
81. Shipper Domestic HQ Address
82. Shipper Domestic HQ D-U-N-S®
83. Shipper Ultimate Parent
84. Shipper Ultimate Parent Website
85. Shipper Ultimate Parent Headquarters Address
86. Shipper Ultimate Parent Profile
87. Shipper Ultimate Parent SPCIQ ID
88. Shipper Ultimate Parent MI Key
89. Shipper Ultimate Parent Stock Tickers
90. Carrier
91. Notify Party
92. Notify Party SCAC
93. Shipment Origin
94. Shipment Destination
95. Shipment Destination Region
96. Port of Unlading
97. Port of Unlading Region
98. Port of Lading
99. Port of Lading Region
100. Port of Lading Country
101. Place of Receipt
102. Transport Method
103. Vessel
104. Vessel Voyage ID
105. Vessel IMO
106. Is Containerized
107. Volume (TEU)
108. Quantity
109. Measurement
110. Weight (kg)
111. Weight (t)
112. Weight (Original Format)
113. Value of Goods (USD)
114. FROB
115. Manifest Number
116. Inbond Code
117. Industry - GICS
118. Industry - GICS Description
119. Number of Containers
120. Has LCL
121. Container Numbers
122. HS Code
123. Goods Shipped
124. Volume (Container TEU)
125. Container Marks
126. Divided/LCL
127. Container Type of Service
128. Container Types
129. Dangerous Goods
```

---

## Ending Columns (PREPROCESSED) - 51 columns

```
1. Bill of Lading Number                  [KEPT]
2. Arrival Date                           [KEPT]
3. Consignee                              [KEPT]
4. Consignee (Original Format)            [KEPT]
5. Consignee SIC Codes                    [KEPT]
6. Shipper                                [KEPT]
7. Shipper (Original Format)              [KEPT]
8. Shipper SIC Codes                      [KEPT]
9. Notify Party                           [KEPT]
10. Carrier                               [KEPT]
11. Origin (F)                            [RENAMED: Shipment Origin]
12. Destination (D)                       [RENAMED: Shipment Destination]
13. Port of Discharge (D)                 [RENAMED: Port of Unlading]
14. Port of Loading (F)                   [RENAMED: Port of Lading]
15. Country of Origin (F)                 [RENAMED: Port of Lading Country]
16. Place of Receipt (F)                  [RENAMED: Place of Receipt]
17. Port_Consolidated                     [NEW - ADDED]
18. Port_Coast                            [NEW - ADDED]
19. Port_Region                           [NEW - ADDED]
20. Port_Code                             [NEW - ADDED]
21. Vessel                                [KEPT]
22. Voyage                                [RENAMED: Vessel Voyage ID]
23. IMO                                   [RENAMED: Vessel IMO]
24. Is Containerized                      [KEPT]
25. Measurement                           [KEPT]
26. Kilos                                 [RENAMED: Weight (kg)]
27. Tons                                  [RENAMED: Weight (t)]
28. Weight (Original Format)              [KEPT]
29. Value                                 [RENAMED: Value of Goods (USD)]
30. HS Code Desc.                         [RENAMED: HS Code]
31. Goods Shipped                         [KEPT]
32. Carrier Name                          [NEW - EXTRACTED from Carrier]
33. Qty                                   [SPLIT from Quantity]
34. Pckg                                  [SPLIT from Quantity]
35. HS2                                   [EXTRACTED from HS Code]
36. HS4                                   [EXTRACTED from HS Code]
37. HS6                                   [EXTRACTED from HS Code]
38. RAW_REC_ID                            [NEW - GENERATED]
39. Count                                 [NEW - ADDED]
40. Group                                 [NEW - EMPTY]
41. Commodity                             [NEW - EMPTY]
42. Cargo                                 [NEW - EMPTY]
43. Cargo Detail                          [NEW - EMPTY]
44. Report_One                            [NEW - EMPTY]
45. Report_Two                            [NEW - EMPTY]
46. Report_Three                          [NEW - EMPTY]
47. Report_Four                           [NEW - EMPTY]
48. Filter                                [NEW - EMPTY]
49. Note                                  [NEW - EMPTY]
50. Type                                  [NEW - EMPTY (vessel type)]
51. DWT                                   [NEW - EMPTY (vessel deadweight)]
```

---

## Transformation Summary

| Action | Count | Details |
|--------|-------|---------|
| **DROPPED** | 84 columns | Detailed company info, container details |
| **KEPT** | 13 columns | Core shipment data |
| **RENAMED** | 9 columns | Simplified names |
| **SPLIT** | 1 → 2 columns | Quantity → Qty + Pckg |
| **EXTRACTED** | 3 columns | HS2, HS4, HS6 from HS Code |
| **ADDED** | 14 columns | Port rollups (4), classification (6), reporting (4) |
| **ENRICHED** | 2 columns | Carrier Name, Vessel Type/DWT (added later) |

---

## Key Transformations

### 1. Company Details → Simplified
```
BEFORE: 47 consignee + 42 shipper columns (addresses, phones, DUNS, etc.)
AFTER:  4 consignee + 4 shipper columns (name, original, SIC codes only)
```

### 2. Weights → Renamed
```
BEFORE: Weight (kg), Weight (t)
AFTER:  Kilos, Tons
```

### 3. Quantity → Split
```
BEFORE: "3903 PCS" (single column)
AFTER:  Qty = 3903, Pckg = "PCS" (two columns)
```

### 4. HS Code → Extracted
```
BEFORE: "1431.49 XXXX description" (single column)
AFTER:  HS2 = "14", HS4 = "1431", HS6 = "143149" (+ original kept)
```

### 5. Classification Columns → Added Empty
```
Group, Commodity, Cargo, Cargo Detail
(Populated later by classification script)
```

---

## Dropped Columns (84 total)

**Consignee Details (30 dropped):**
- Address, City, State, Postal, Country, Full Address
- Emails (3), Phones (3), Fax, Websites (2)
- Profile, SPCIQ ID, MI Key, DUNS
- Industry, Revenue, Employees, Market Cap, Incorporation Year, Trade Roles
- Global HQ Address/DUNS, Domestic HQ details, Ultimate Parent details

**Shipper Details (30 dropped):**
- Same structure as Consignee (parallel fields)

**Container Details (10 dropped):**
- Has LCL, Container Numbers, Volume (TEU)
- Container Marks, Divided/LCL
- Container Type of Service, Container Types
- Dangerous Goods

**Other (14 dropped):**
- Bill of Lading Type, Master Bill of Lading Number
- Matching Fields, Stock Tickers, HQ addresses
- Industry GICS codes, Transport Method
- Shipment Destination Region, Port of Unlading Region

---

**File:** `PREPROCESSING_COLUMN_MAP.md`
**Created:** 2026-01-28
**Purpose:** Reference for understanding preprocessing transformations
