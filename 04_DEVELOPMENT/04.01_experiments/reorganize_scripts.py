"""
Script to categorize and move 128 scripts to organized folder structure.
Identifies latest versions and archives old ones.
"""

import os
import shutil
import re
from pathlib import Path
from collections import defaultdict

# Define base paths
BASE = Path(r"G:\My Drive\LLM\project_manifest")
SCRIPTS_SRC = BASE / "04_SCRIPTS"
SCRIPTS_DST = BASE / "02_SCRIPTS"
DEPRECATED = BASE / "04_DEVELOPMENT" / "04.03_deprecated"

# Define categorization patterns (order matters - first match wins)
CATEGORIES = {
    "02.01_preprocessing": [
        r"^transform_.*",
        r"^preprocess_.*",
        r"^clean_.*",
        r"^split_.*",
        r"^convert_.*",
        r"^fix_and_convert.*"
    ],
    "02.02_matching": [
        r"^match_.*",
        r"^marry_.*",
        r"^debug_.*matching.*"
    ],
    "02.03_enrichment": [
        r"^add_.*",
        r"^enrich_.*",
        r"^filter_.*",
        r"^merge_.*"
    ],
    "02.04_analysis": [
        r"^analyze_.*",
        r"^carrier_.*",
        r"^quick_.*",
        r"^compare_.*",
        r"^diagnose_.*"
    ],
    "02.05_validation": [
        r"^check_.*",
        r"^verify_.*",
        r"^validate_.*"
    ],
    "02.06_utilities": [
        r"^build_.*dictionary.*",
        r"^build_.*mapping.*",
        r"^generate_.*",
        r"^reorganize_.*",
        r"^restore_.*",
        r"^restructure_.*",
        r"^upgrade_.*",
        r"^migrate_.*",
        r"^remove_.*column.*"
    ],
    "02.07_production": [
        r"^classify_.*",
        r"^run_.*pipeline.*",
        r"^stage\d+_.*"
    ]
}

def extract_version(filename):
    """Extract version number from filename like v1.2.3 or v20260115_1234"""
    # Try semantic version first (v1.2.3)
    match = re.search(r'v(\d+)\.(\d+)\.(\d+)', filename)
    if match:
        return tuple(map(int, match.groups()))

    # Try timestamp version (v20260115_1234)
    match = re.search(r'v(\d{8})_(\d{4})', filename)
    if match:
        return (int(match.group(1)), int(match.group(2)))

    # No version found
    return None

def get_base_name(filename):
    """Get base name without version suffix"""
    # Remove extension
    base = filename.replace('.py', '')

    # Remove version patterns
    base = re.sub(r'_v\d+\.\d+\.\d+$', '', base)  # v1.2.3
    base = re.sub(r'_v\d{8}_\d{4}$', '', base)     # v20260115_1234

    return base

def categorize_script(filename):
    """Determine which category a script belongs to"""
    for category, patterns in CATEGORIES.items():
        for pattern in patterns:
            if re.match(pattern, filename, re.IGNORECASE):
                return category

    # Default to utilities if no match
    return "02.06_utilities"

def main():
    # Get all Python scripts
    scripts = list(SCRIPTS_SRC.glob("*.py"))
    print(f"Found {len(scripts)} scripts to process\n")

    # Group by base name to identify versions
    script_families = defaultdict(list)
    for script in scripts:
        base_name = get_base_name(script.name)
        script_families[base_name].append(script)

    print(f"Identified {len(script_families)} unique script families\n")

    # Process each family
    moved_count = 0
    archived_count = 0

    for base_name, versions in sorted(script_families.items()):
        category = categorize_script(base_name)

        # Find latest version
        if len(versions) == 1:
            latest = versions[0]
            old_versions = []
        else:
            # Sort by version
            versioned = [(v, extract_version(v.name)) for v in versions]
            versioned = [(v, ver) for v, ver in versioned if ver is not None]

            if versioned:
                versioned.sort(key=lambda x: x[1], reverse=True)
                latest = versioned[0][0]
                old_versions = [v for v, _ in versioned[1:]]
            else:
                # No versions found, use alphabetically last
                versions.sort(key=lambda x: x.name, reverse=True)
                latest = versions[0]
                old_versions = versions[1:]

        # Determine destination name (remove version suffix)
        if extract_version(latest.name):
            dest_name = f"{base_name}.py"
        else:
            dest_name = latest.name

        dest_path = SCRIPTS_DST / category / dest_name

        # Move latest version
        print(f"Moving: {latest.name}")
        print(f"    To: {category}/{dest_name}")
        shutil.copy2(latest, dest_path)
        moved_count += 1

        # Archive old versions
        for old in old_versions:
            archive_path = DEPRECATED / old.name
            print(f"  Archiving: {old.name} -> deprecated/")
            shutil.copy2(old, archive_path)
            archived_count += 1

        print()

    print(f"\n=== Summary ===")
    print(f"Scripts moved to production: {moved_count}")
    print(f"Scripts archived: {archived_count}")
    print(f"Total processed: {moved_count + archived_count}")

    # Show distribution by category
    print(f"\n=== Distribution by Category ===")
    category_counts = defaultdict(int)
    for base_name in script_families.keys():
        category = categorize_script(base_name)
        category_counts[category] += 1

    for category in sorted(CATEGORIES.keys()):
        count = category_counts[category]
        print(f"{category}: {count} scripts")

if __name__ == "__main__":
    main()
