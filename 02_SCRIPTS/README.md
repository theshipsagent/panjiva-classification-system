# 02_SCRIPTS - Processing Scripts

This folder contains all data processing and analysis scripts, organized by purpose.

## Folder Structure

- **02.01_preprocessing/** - Data cleaning and standardization
  - Preprocess Panjiva imports/exports
  - Transform USACE entrance/clearance data

- **02.02_matching/** - Matching algorithms
  - Match Panjiva to USACE port calls
  - Match US Flag registry
  - Match FGIS grain certificates
  - Marry entrance to clearance

- **02.03_enrichment/** - Data enrichment
  - Add vessel types
  - Add agency fees
  - Add port statistics

- **02.04_analysis/** - Analysis and reporting
  - Tonnage analysis
  - Carrier analysis
  - Port call analysis
  - Quick reports

- **02.05_validation/** - Data quality checks
  - Validate port call master
  - Check data quality
  - Verify match quality

- **02.06_utilities/** - Shared helper functions
  - utilities/ - Python package with reusable functions
    - date_parsers.py
    - name_cleaners.py
    - match_helpers.py

- **02.07_production/** - Production pipeline
  - run_full_pipeline.py
  - generate_port_call_master.py

## Best Practices

- Keep LATEST version only in production folders
- Use descriptive function names
- Reference dictionaries from 01_DICTIONARIES/
- Reference data from 00_DATA/
- Log all major operations
