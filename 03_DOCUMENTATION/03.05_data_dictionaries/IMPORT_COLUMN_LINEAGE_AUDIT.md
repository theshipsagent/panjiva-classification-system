# Import Data Column Lineage Audit
**Generated:** 2026-01-21

**Purpose:** Trace every column through the import pipeline from RAW → PREPROCESSED → CLASSIFIED

---

## Summary Statistics

- **RAW Columns:** 146
- **PREPROCESSED Columns:** 51
- **CLASSIFIED Columns:** 58

- **Columns Dropped (RAW → PREPROCESSED):** 113
- **Columns Kept (RAW → PREPROCESSED):** 33
- **Columns Added in PREPROCESSING:** 22
- **Columns Added in CLASSIFICATION:** 7

---

## Column Evolution Table

| RAW Column | PREPROCESSED Column | CLASSIFIED Column | Status | Transformation |
|------------|---------------------|-------------------|--------|----------------|
| Arrival Date | Arrival Date | Arrival Date | KEPT | Kept |
| Bill of Lading Number | Bill of Lading Number | Bill of Lading Number | KEPT | Kept |
| Bill of Lading Type | N/A | N/A | DROPPED | Dropped |
| Cargo | None | None | KEPT | Kept |
| Cargo Detail | None | None | KEPT | Kept |
| Carrier | Carrier | Carrier | KEPT | Kept |
| Category | N/A | N/A | DROPPED | Dropped |
| Consignee | Consignee | Consignee | KEPT | Kept |
| Consignee (Original Format) | Consignee (Original Format) | Consignee (Original Format) | KEPT | Kept |
| Consignee Address | N/A | N/A | DROPPED | Dropped |
| Consignee City | N/A | N/A | DROPPED | Dropped |
| Consignee Country | N/A | N/A | DROPPED | Dropped |
| Consignee D-U-N-S® | N/A | N/A | DROPPED | Dropped |
| Consignee Domestic HQ | N/A | N/A | DROPPED | Dropped |
| Consignee Domestic HQ Address | N/A | N/A | DROPPED | Dropped |
| Consignee Domestic HQ D-U-N-S® | N/A | N/A | DROPPED | Dropped |
| Consignee Email 1 | N/A | N/A | DROPPED | Dropped |
| Consignee Email 2 | N/A | N/A | DROPPED | Dropped |
| Consignee Email 3 | N/A | N/A | DROPPED | Dropped |
| Consignee Employees | N/A | N/A | DROPPED | Dropped |
| Consignee Fax | N/A | N/A | DROPPED | Dropped |
| Consignee Full Address | N/A | N/A | DROPPED | Dropped |
| Consignee Global HQ | N/A | N/A | DROPPED | Dropped |
| Consignee Global HQ Address | N/A | N/A | DROPPED | Dropped |
| Consignee Global HQ D-U-N-S® | N/A | N/A | DROPPED | Dropped |
| Consignee Incorporation Year | N/A | N/A | DROPPED | Dropped |
| Consignee Industry | N/A | N/A | DROPPED | Dropped |
| Consignee MI Key | N/A | N/A | DROPPED | Dropped |
| Consignee Market Capitalization | N/A | N/A | DROPPED | Dropped |
| Consignee Phone 1 | N/A | N/A | DROPPED | Dropped |
| Consignee Phone 2 | N/A | N/A | DROPPED | Dropped |
| Consignee Phone 3 | N/A | N/A | DROPPED | Dropped |
| Consignee Postal Code | N/A | N/A | DROPPED | Dropped |
| Consignee Profile | N/A | N/A | DROPPED | Dropped |
| Consignee Revenue | N/A | N/A | DROPPED | Dropped |
| Consignee SIC Codes | Consignee SIC Codes | Consignee SIC Codes | KEPT | Kept |
| Consignee SPCIQ ID | N/A | N/A | DROPPED | Dropped |
| Consignee State/Region | N/A | N/A | DROPPED | Dropped |
| Consignee Stock Tickers | N/A | N/A | DROPPED | Dropped |
| Consignee Trade Roles | N/A | N/A | DROPPED | Dropped |
| Consignee Ultimate Parent | N/A | N/A | DROPPED | Dropped |
| Consignee Ultimate Parent Headquarters Address | N/A | N/A | DROPPED | Dropped |
| Consignee Ultimate Parent MI Key | N/A | N/A | DROPPED | Dropped |
| Consignee Ultimate Parent Profile | N/A | N/A | DROPPED | Dropped |
| Consignee Ultimate Parent SPCIQ ID | N/A | N/A | DROPPED | Dropped |
| Consignee Ultimate Parent Stock Tickers | N/A | N/A | DROPPED | Dropped |
| Consignee Ultimate Parent Website | N/A | N/A | DROPPED | Dropped |
| Consignee Unified | N/A | N/A | DROPPED | Dropped |
| Consignee Website 1 | N/A | N/A | DROPPED | Dropped |
| Consignee Website 2 | N/A | N/A | DROPPED | Dropped |
| Container Marks | N/A | N/A | DROPPED | Dropped |
| Container Numbers | N/A | N/A | DROPPED | Dropped |
| Container Type of Service | N/A | N/A | DROPPED | Dropped |
| Container Types | N/A | N/A | DROPPED | Dropped |
| Count | Count | Count | KEPT | Kept |
| Dangerous Goods | N/A | N/A | DROPPED | Dropped |
| Divided/LCL | N/A | N/A | DROPPED | Dropped |
| FROB | N/A | N/A | DROPPED | Dropped |
| Filter | None | None | KEPT | Kept |
| Goods Shipped | Goods Shipped | Goods Shipped | KEPT | Kept |
| Group | None | None | KEPT | Kept |
| HS Code | HS Code Desc. | HS Code Desc. | KEPT | Renamed |
| Has LCL | N/A | N/A | DROPPED | Dropped |
| Inbond Code | N/A | N/A | DROPPED | Dropped |
| Industry - GICS | N/A | N/A | DROPPED | Dropped |
| Industry - GICS Description | N/A | N/A | DROPPED | Dropped |
| Is Containerized | Is Containerized | Is Containerized | KEPT | Kept |
| Manifest Number | N/A | N/A | DROPPED | Dropped |
| Master Bill of Lading Number | N/A | N/A | DROPPED | Dropped |
| Matching Fields | N/A | N/A | DROPPED | Dropped |
| Measurement | Measurement | Measurement | KEPT | Kept |
| Notify Party | Notify Party | Notify Party | KEPT | Kept |
| Notify Party SCAC | N/A | N/A | DROPPED | Dropped |
| Notify Unified | N/A | N/A | DROPPED | Dropped |
| Number of Containers | N/A | N/A | DROPPED | Dropped |
| Place of Receipt | Place of Receipt (F) | Place of Receipt (F) | KEPT | Renamed |
| Port of Lading | Port of Loading (F) | Port of Loading (F) | KEPT | Renamed |
| Port of Lading Country | Country of Origin (F) | Country of Origin (F) | KEPT | Renamed |
| Port of Lading Region | N/A | N/A | DROPPED | Dropped |
| Port of Unlading | Port of Discharge (D) | Port of Discharge (D) | KEPT | Renamed |
| Port of Unlading Region | N/A | N/A | DROPPED | Dropped |
| Quantity | Qty | Qty | KEPT | Renamed |
| Report 1 | N/A | N/A | DROPPED | Dropped |
| Report 2 | N/A | N/A | DROPPED | Dropped |
| Report 3 | N/A | N/A | DROPPED | Dropped |
| Report 4 | N/A | N/A | DROPPED | Dropped |
| Report 5 | N/A | N/A | DROPPED | Dropped |
| Report 6 | N/A | N/A | DROPPED | Dropped |
| Shipment Destination | Destination (D) | Destination (D) | KEPT | Renamed |
| Shipment Destination Region | N/A | N/A | DROPPED | Dropped |
| Shipment Origin | Origin (F) | Origin (F) | KEPT | Renamed |
| Shipper | Shipper | Shipper | KEPT | Kept |
| Shipper (Original Format) | Shipper (Original Format) | Shipper (Original Format) | KEPT | Kept |
| Shipper Address | N/A | N/A | DROPPED | Dropped |
| Shipper City | N/A | N/A | DROPPED | Dropped |
| Shipper Country | N/A | N/A | DROPPED | Dropped |
| Shipper D-U-N-S® | N/A | N/A | DROPPED | Dropped |
| Shipper Domestic HQ | N/A | N/A | DROPPED | Dropped |
| Shipper Domestic HQ Address | N/A | N/A | DROPPED | Dropped |
| Shipper Domestic HQ D-U-N-S® | N/A | N/A | DROPPED | Dropped |
| Shipper Email 1 | N/A | N/A | DROPPED | Dropped |
| Shipper Email 2 | N/A | N/A | DROPPED | Dropped |
| Shipper Email 3 | N/A | N/A | DROPPED | Dropped |
| Shipper Employees | N/A | N/A | DROPPED | Dropped |
| Shipper Fax | N/A | N/A | DROPPED | Dropped |
| Shipper Full Address | N/A | N/A | DROPPED | Dropped |
| Shipper Global HQ | N/A | N/A | DROPPED | Dropped |
| Shipper Global HQ Address | N/A | N/A | DROPPED | Dropped |
| Shipper Global HQ D-U-N-S® | N/A | N/A | DROPPED | Dropped |
| Shipper Incorporation Year | N/A | N/A | DROPPED | Dropped |
| Shipper Industry | N/A | N/A | DROPPED | Dropped |
| Shipper MI Key | N/A | N/A | DROPPED | Dropped |
| Shipper Market Capitalization | N/A | N/A | DROPPED | Dropped |
| Shipper Phone 1 | N/A | N/A | DROPPED | Dropped |
| Shipper Phone 2 | N/A | N/A | DROPPED | Dropped |
| Shipper Phone 3 | N/A | N/A | DROPPED | Dropped |
| Shipper Postal Code | N/A | N/A | DROPPED | Dropped |
| Shipper Profile | N/A | N/A | DROPPED | Dropped |
| Shipper Revenue | N/A | N/A | DROPPED | Dropped |
| Shipper SIC Codes | Shipper SIC Codes | Shipper SIC Codes | KEPT | Kept |
| Shipper SPCIQ ID | N/A | N/A | DROPPED | Dropped |
| Shipper State/Region | N/A | N/A | DROPPED | Dropped |
| Shipper Stock Tickers | N/A | N/A | DROPPED | Dropped |
| Shipper Trade Roles | N/A | N/A | DROPPED | Dropped |
| Shipper Ultimate Parent | N/A | N/A | DROPPED | Dropped |
| Shipper Ultimate Parent Headquarters Address | N/A | N/A | DROPPED | Dropped |
| Shipper Ultimate Parent MI Key | N/A | N/A | DROPPED | Dropped |
| Shipper Ultimate Parent Profile | N/A | N/A | DROPPED | Dropped |
| Shipper Ultimate Parent SPCIQ ID | N/A | N/A | DROPPED | Dropped |
| Shipper Ultimate Parent Stock Tickers | N/A | N/A | DROPPED | Dropped |
| Shipper Ultimate Parent Website | N/A | N/A | DROPPED | Dropped |
| Shipper Unified | N/A | N/A | DROPPED | Dropped |
| Shipper Website 1 | N/A | N/A | DROPPED | Dropped |
| Shipper Website 2 | N/A | N/A | DROPPED | Dropped |
| Transport Method | N/A | N/A | DROPPED | Dropped |
| Value of Goods (USD) | Value | Value | KEPT | Renamed |
| Vessel | Vessel | Vessel | KEPT | Kept |
| Vessel IMO | IMO | IMO | KEPT | Renamed |
| Vessel Voyage ID | Voyage | Voyage | KEPT | Renamed |
| Volume (Container TEU) | N/A | N/A | DROPPED | Dropped |
| Volume (TEU) | N/A | N/A | DROPPED | Dropped |
| Weight (Original Format) | Weight (Original Format) | Weight (Original Format) | KEPT | Kept |
| Weight (kg) | Kilos | Kilos | KEPT | Renamed |
| Weight (t) | Tons | Tons | KEPT | Renamed |
| _source_dir | N/A | N/A | DROPPED | Dropped |
| _source_file | N/A | N/A | DROPPED | Dropped |
| N/A | Cargo | Cargo | ADDED IN PREPROCESSING | Added |
| N/A | Cargo Detail | Cargo Detail | ADDED IN PREPROCESSING | Added |
| N/A | Carrier Name | Carrier Name | ADDED IN PREPROCESSING | Added |
| N/A | Commodity | Commodity | ADDED IN PREPROCESSING | Added |
| N/A | DWT | DWT | ADDED IN PREPROCESSING | Added |
| N/A | Filter | Filter | ADDED IN PREPROCESSING | Added |
| N/A | Group | Group | ADDED IN PREPROCESSING | Added |
| N/A | HS2 | HS2 | ADDED IN PREPROCESSING | Added |
| N/A | HS4 | HS4 | ADDED IN PREPROCESSING | Added |
| N/A | HS6 | HS6 | ADDED IN PREPROCESSING | Added |
| N/A | Note | Note | ADDED IN PREPROCESSING | Added |
| N/A | Pckg | Pckg | ADDED IN PREPROCESSING | Added |
| N/A | Port_Coast | Port_Coast | ADDED IN PREPROCESSING | Added |
| N/A | Port_Code | Port_Code | ADDED IN PREPROCESSING | Added |
| N/A | Port_Consolidated | Port_Consolidated | ADDED IN PREPROCESSING | Added |
| N/A | Port_Region | Port_Region | ADDED IN PREPROCESSING | Added |
| N/A | RAW_REC_ID | RAW_REC_ID | ADDED IN PREPROCESSING | Added |
| N/A | Report_Four | Report_Four | ADDED IN PREPROCESSING | Added |
| N/A | Report_One | Report_One | ADDED IN PREPROCESSING | Added |
| N/A | Report_Three | Report_Three | ADDED IN PREPROCESSING | Added |
| N/A | Report_Two | Report_Two | ADDED IN PREPROCESSING | Added |
| N/A | Type | Type | ADDED IN PREPROCESSING | Added |
| N/A | N/A | Cargo_Detail_Locked | ADDED IN CLASSIFICATION | Added |
| N/A | N/A | Cargo_Locked | ADDED IN CLASSIFICATION | Added |
| N/A | N/A | Classified_Phase | ADDED IN CLASSIFICATION | Added |
| N/A | N/A | Commodity_Locked | ADDED IN CLASSIFICATION | Added |
| N/A | N/A | Group_Locked | ADDED IN CLASSIFICATION | Added |
| N/A | N/A | Last_Rule_ID | ADDED IN CLASSIFICATION | Added |
| N/A | N/A | Vessel_Type_Simple | ADDED IN CLASSIFICATION | Added |

---

## Columns Dropped in Preprocessing

These columns existed in RAW data but were removed during preprocessing:

- **Bill of Lading Type**
  - Sample: `Simple`
- **Category**
- **Consignee Address**
  - Sample: `8050, Harrisburg Blvd`
- **Consignee City**
  - Sample: `Houston`
- **Consignee Country**
  - Sample: `United States`
- **Consignee D-U-N-S®**
  - Sample: `80861768.0`
- **Consignee Domestic HQ**
  - Sample: `Technip`
- **Consignee Domestic HQ Address**
  - Sample: `United States`
- **Consignee Domestic HQ D-U-N-S®**
  - Sample: `800763369.0`
- **Consignee Email 1**
  - Sample: `sales@fps-usa.com`
- **Consignee Email 2**
  - Sample: `i@chrobinson.com`
- **Consignee Email 3**
  - Sample: `raiz@chrobinson.com`
- **Consignee Employees**
  - Sample: `93.0`
- **Consignee Fax**
  - Sample: `+1 713 923 6272`
- **Consignee Full Address**
  - Sample: `8050, Harrisburg Blvd, Houston, Texas, 77012, United States`
- **Consignee Global HQ**
  - Sample: `Technip`
- **Consignee Global HQ Address**
  - Sample: `United States`
- **Consignee Global HQ D-U-N-S®**
- **Consignee Incorporation Year**
  - Sample: `1952.0`
- **Consignee Industry**
  - Sample: `Electronic Equipment, Instruments and Components`
- **Consignee MI Key**
  - Sample: `5048100.0`
- **Consignee Market Capitalization**
- **Consignee Phone 1**
  - Sample: `+1 713 924 9600`
- **Consignee Phone 2**
  - Sample: `+1 905 364 3153`
- **Consignee Phone 3**
  - Sample: `+1 346 229 2711`
- **Consignee Postal Code**
  - Sample: `77012`
- **Consignee Profile**
  - Sample: `https://panjiva.com/Fire-Protection-Service/3739601`
- **Consignee Revenue**
  - Sample: `16541450.0`
- **Consignee SPCIQ ID**
  - Sample: `4592672.0`
- **Consignee State/Region**
  - Sample: `Texas`
- **Consignee Stock Tickers**
- **Consignee Trade Roles**
  - Sample: `Manufacturer`
- **Consignee Ultimate Parent**
  - Sample: `Fire Protection Service, Inc.`
- **Consignee Ultimate Parent Headquarters Address**
  - Sample: `8050 Harrisburg Boulevard, Houston Texas 77012, United States`
- **Consignee Ultimate Parent MI Key**
  - Sample: `5048100.0`
- **Consignee Ultimate Parent Profile**
  - Sample: `https://panjiva.com/Fire-Protection-Service-Inc/54952351`
- **Consignee Ultimate Parent SPCIQ ID**
  - Sample: `4592672.0`
- **Consignee Ultimate Parent Stock Tickers**
  - Sample: `NYSE:HAL, BOVESPA:HALI34`
- **Consignee Ultimate Parent Website**
  - Sample: `www.fps-usa.com`
- **Consignee Unified**
- **Consignee Website 1**
  - Sample: `fps-usa.com`
- **Consignee Website 2**
- **Container Marks**
  - Sample: `424156 070004 574118 575077 564080`
- **Container Numbers**
  - Sample: `NC`
- **Container Type of Service**
  - Sample: `Non-containerized`
- **Container Types**
- **Dangerous Goods**
  - Sample: `false`
- **Divided/LCL**
  - Sample: `N`
- **FROB**
- **Has LCL**
- **Inbond Code**
- **Industry - GICS**
  - Sample: `25202010`
- **Industry - GICS Description**
  - Sample: `Leisure Products`
- **Manifest Number**
  - Sample: `139103.0`
- **Master Bill of Lading Number**
  - Sample: `IDMCB232652001`
- **Matching Fields**
- **Notify Party SCAC**
  - Sample: `IDMC - Industrial Maritime Carriers Llc`
- **Notify Unified**
- **Number of Containers**
  - Sample: `1.0`
- **Port of Lading Region**
  - Sample: `North America`
- **Port of Unlading Region**
  - Sample: `Southwest Region`
- **Report 1**
- **Report 2**
- **Report 3**
- **Report 4**
- **Report 5**
- **Report 6**
- **Shipment Destination Region**
  - Sample: `Southwest Region`
- **Shipper Address**
  - Sample: `38/21,38/43 Moo 5`
- **Shipper City**
  - Sample: `Si Racha`
- **Shipper Country**
  - Sample: `United States`
- **Shipper D-U-N-S®**
  - Sample: `131489817.0`
- **Shipper Domestic HQ**
  - Sample: `Shell Petroleum Group`
- **Shipper Domestic HQ Address**
  - Sample: `900 Louisiana Street, South Houston, TX 77587, USA`
- **Shipper Domestic HQ D-U-N-S®**
  - Sample: `131489817.0`
- **Shipper Email 1**
  - Sample: `emheidi.heslin@us.dsv.com`
- **Shipper Email 2**
  - Sample: `emricky.tinsley@shell.com`
- **Shipper Email 3**
  - Sample: `ema.yanaga@mitsui.com`
- **Shipper Employees**
  - Sample: `90.0`
- **Shipper Fax**
  - Sample: `+58 212 7084661`
- **Shipper Full Address**
  - Sample: `38/21,38/43 Moo 5, Si Racha 20230, Thailand`
- **Shipper Global HQ**
  - Sample: `Valero Energy`
- **Shipper Global HQ Address**
  - Sample: `One Valero Way, San Antonio Texas 78249, United States`
- **Shipper Global HQ D-U-N-S®**
- **Shipper Incorporation Year**
  - Sample: `2002.0`
- **Shipper Industry**
  - Sample: `Chemicals`
- **Shipper MI Key**
  - Sample: `8734802.0`
- **Shipper Market Capitalization**
  - Sample: `76352393139.11`
- **Shipper Phone 1**
  - Sample: `+1 242 351 9200`
- **Shipper Phone 2**
  - Sample: `+60 3 3375 1288`
- **Shipper Phone 3**
  - Sample: `+60 603337336`
- **Shipper Postal Code**
  - Sample: `20230`
- **Shipper Profile**
  - Sample: `https://panjiva.com/Viking-Life-Saving-Equipment/158754915`
- **Shipper Revenue**
  - Sample: `9158114.0`
- **Shipper SPCIQ ID**
  - Sample: `423075008.0`
- **Shipper State/Region**
  - Sample: `Delaware`
- **Shipper Stock Tickers**
  - Sample: `OTCPK:MITS.Y, TSE:8031`
- **Shipper Trade Roles**
  - Sample: `Manufacturer`
- **Shipper Ultimate Parent**
  - Sample: `Claus Sørensens Fond Holding A/S`
- **Shipper Ultimate Parent Headquarters Address**
  - Sample: `Auktionsgade 6-8, Esbjerg Region of Southern Denmark 6700, Denmark`
- **Shipper Ultimate Parent MI Key**
  - Sample: `8343019.0`
- **Shipper Ultimate Parent Profile**
  - Sample: `https://panjiva.com/Claus-S-rensens-Fond-Holding-A-S/56987237`
- **Shipper Ultimate Parent SPCIQ ID**
  - Sample: `242836490.0`
- **Shipper Ultimate Parent Stock Tickers**
  - Sample: `NasdaqGS:CHRW`
- **Shipper Ultimate Parent Website**
  - Sample: `www.csfond.dk`
- **Shipper Unified**
- **Shipper Website 1**
  - Sample: `pdvsa.com`
- **Shipper Website 2**
- **Transport Method**
  - Sample: `Maritime`
- **Volume (Container TEU)**
- **Volume (TEU)**
- **_source_dir**
  - Sample: `us_gulf`
- **_source_file**
  - Sample: `Panjiva-US_Imports-all-results_1_to_2638_of_2638-2025-12-03-11-09.csv`

---

## Columns Added in Preprocessing

These columns were created/derived during preprocessing:

- **Cargo**
  - Added during preprocessing (derived/engineered)
- **Cargo Detail**
  - Added during preprocessing (derived/engineered)
- **Carrier Name**
  - Added during preprocessing (derived/engineered)
  - Sample: `FSHP - Formel, Stevenson Freight Services Llc`
- **Commodity**
  - Added during preprocessing (derived/engineered)
- **DWT**
  - Added during preprocessing (derived/engineered)
- **Filter**
  - Added during preprocessing (derived/engineered)
- **Group**
  - Added during preprocessing (derived/engineered)
- **HS2**
  - Added during preprocessing (derived/engineered)
  - Sample: `23.0`
- **HS4**
  - Added during preprocessing (derived/engineered)
  - Sample: `2309.0`
- **HS6**
  - Added during preprocessing (derived/engineered)
  - Sample: `230910.0`
- **Note**
  - Added during preprocessing (derived/engineered)
- **Pckg**
  - Added during preprocessing (derived/engineered)
  - Sample: `PKG`
- **Port_Coast**
  - Added during preprocessing (derived/engineered)
  - Sample: `East`
- **Port_Code**
  - Added during preprocessing (derived/engineered)
  - Sample: `5101.0`
- **Port_Consolidated**
  - Added during preprocessing (derived/engineered)
  - Sample: `Virgin Islands`
- **Port_Region**
  - Added during preprocessing (derived/engineered)
  - Sample: `Caribbean`
- **RAW_REC_ID**
  - Added during preprocessing (derived/engineered)
  - Sample: `PANV-20260112-00106392`
- **Report_Four**
  - Added during preprocessing (derived/engineered)
- **Report_One**
  - Added during preprocessing (derived/engineered)
- **Report_Three**
  - Added during preprocessing (derived/engineered)
- **Report_Two**
  - Added during preprocessing (derived/engineered)
- **Type**
  - Added during preprocessing (derived/engineered)

---

## Columns Added in Classification

These columns were created during classification:

- **Cargo_Detail_Locked**
  - Added during classification (lock flags / metadata)
  - Sample: `FALSE`
- **Cargo_Locked**
  - Added during classification (lock flags / metadata)
  - Sample: `FALSE`
- **Classified_Phase**
  - Added during classification (lock flags / metadata)
  - Sample: `1`
- **Commodity_Locked**
  - Added during classification (lock flags / metadata)
  - Sample: `FALSE`
- **Group_Locked**
  - Added during classification (lock flags / metadata)
  - Sample: `TRUE`
- **Last_Rule_ID**
  - Added during classification (lock flags / metadata)
  - Sample: `CARR-MAET`
- **Vessel_Type_Simple**
  - Added during classification (lock flags / metadata)
  - Sample: `Tanker`
