# 01_DICTIONARIES - Reference Data

This folder contains all reference dictionaries and lookup tables used by the data processing pipeline.

## Folder Structure

- **01.01_cargo_classification/** - Cargo classification rules
  - Main classification dictionary (CURRENT version marked)
  - Historical versions archived

- **01.02_ports/** - Port reference data
  - US port dictionary
  - USACE port mappings
  - Port code translations

- **01.03_vessels/** - Vessel registry data
  - Ship register (international)
  - US Flag inventory (domestic vessels)
  - Vessel type mappings

- **01.04_carriers/** - Carrier and shipping line data
  - Carrier SCAC codes
  - Carrier-cargo mappings

- **01.05_hs_codes/** - HS code hierarchies
  - HS code reference tables
  - HS2/HS4/HS6 descriptions

## Usage

All scripts should reference dictionaries in this centralized location. Do NOT duplicate reference files across the project.

## Versioning

Dictionary files use semantic versioning: `v{MAJOR}.{MINOR}.{PATCH}`

The CURRENT version is marked in the filename for production use.
