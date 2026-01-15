"""
USACE User Edit Analysis Script v1.0.0
Created: 2026-01-15

Purpose:
    Analyze manual corrections made to USACE portcall data and extract
    automation patterns that can be incorporated into future processing scripts.

Input:
    - Original: usace_2023_portcall_master_v1.1.0.csv
    - User-edited: usace_2023_portcall_master_v1.1.0_USER_EDITS_20260115.csv

Output:
    - USER_EDIT_ANALYSIS_REPORT_20260115.md (pattern analysis and automation suggestions)

Usage:
    python analyze_user_edits_v1.0.0.py
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import re

# ============================================================================
# PATH CONFIGURATION
# ============================================================================

BASE_DIR = Path(r"G:\My Drive\LLM\project_manifest")

# Check both old and new folder structures
USACE_PATHS = [
    BASE_DIR / "00_raw_data" / "usace_vessel_entrances",
    BASE_DIR / "00_STAGE00_RAW_DATA" / "usace_vessel_entrances",
    BASE_DIR / "01_step_one" / "usace_vessel_entrances",
    BASE_DIR / "01_STAGE01_PREPROCESSING" / "usace",
]

# Find the actual data location
DATA_DIR = None
for path in USACE_PATHS:
    if path.exists():
        DATA_DIR = path
        break

if DATA_DIR is None:
    # Fallback to base directory
    DATA_DIR = BASE_DIR

ORIGINAL_FILE = "usace_2023_portcall_master_v1.1.0.csv"
EDITED_FILE = "usace_2023_portcall_master_v1.1.0_USER_EDITS_20260115.csv"
OUTPUT_REPORT = "USER_EDIT_ANALYSIS_REPORT_20260115.md"

OUTPUT_DIR = BASE_DIR / "build_documentation"
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def find_file(filename):
    """Search for file in multiple possible locations."""
    # Try data directory first
    if DATA_DIR:
        filepath = DATA_DIR / filename
        if filepath.exists():
            return filepath

    # Try other common locations
    search_paths = [
        BASE_DIR / filename,
        BASE_DIR / "build_documentation" / filename,
        BASE_DIR / "00_raw_data" / filename,
        BASE_DIR / "01_step_one" / filename,
    ]

    for path in search_paths:
        if path.exists():
            return path

    return None

def load_csv_safe(filepath):
    """Load CSV with error handling."""
    try:
        df = pd.read_csv(filepath, low_memory=False)
        print(f"✓ Loaded: {filepath.name}")
        print(f"  Rows: {len(df):,} | Columns: {len(df.columns)}")
        return df
    except Exception as e:
        print(f"✗ Error loading {filepath.name}: {e}")
        return None

def compare_rows(row_original, row_edited, index):
    """Compare two rows and return dictionary of changes."""
    changes = {}

    for col in row_original.index:
        if col not in row_edited.index:
            continue

        val_orig = row_original[col]
        val_edit = row_edited[col]

        # Handle NaN comparisons
        if pd.isna(val_orig) and pd.isna(val_edit):
            continue

        if pd.isna(val_orig) or pd.isna(val_edit) or str(val_orig) != str(val_edit):
            changes[col] = {
                'original': val_orig,
                'edited': val_edit,
                'row_index': index
            }

    return changes

def extract_vessel_name(row):
    """Extract vessel name from row for identification."""
    if 'VESSEL_NAME' in row.index:
        return str(row['VESSEL_NAME'])
    elif 'Vessel_Name' in row.index:
        return str(row['Vessel_Name'])
    return "UNKNOWN"

def extract_imo(row):
    """Extract IMO from row."""
    if 'IMO' in row.index:
        return str(row['IMO'])
    elif 'IMO_NUMBER' in row.index:
        return str(row['IMO_NUMBER'])
    return ""

# ============================================================================
# PATTERN ANALYSIS FUNCTIONS
# ============================================================================

def analyze_vessel_type_changes(changes_by_column):
    """Analyze patterns in vessel type modifications."""
    patterns = []

    # Columns that might contain vessel type info
    vtype_columns = [col for col in changes_by_column.keys()
                     if 'TYPE' in col.upper() or 'VTYPE' in col.upper()]

    for col in vtype_columns:
        changes = changes_by_column[col]

        # Count transformation patterns
        transformations = Counter()
        for change in changes:
            orig = str(change['original'])
            edit = str(change['edited'])
            transformations[(orig, edit)] += 1

        # Report significant patterns
        for (orig, edit), count in transformations.most_common(10):
            if count >= 2:  # Only show patterns that occur multiple times
                patterns.append({
                    'type': 'vessel_type_transformation',
                    'column': col,
                    'from': orig,
                    'to': edit,
                    'count': count,
                    'automation_potential': 'HIGH' if count >= 5 else 'MEDIUM'
                })

    return patterns

def analyze_match_type_changes(changes_by_column):
    """Analyze patterns in Match_Type modifications."""
    patterns = []

    match_columns = [col for col in changes_by_column.keys()
                     if 'MATCH' in col.upper()]

    for col in match_columns:
        changes = changes_by_column[col]

        # Count transformation patterns
        transformations = Counter()
        for change in changes:
            orig = str(change['original'])
            edit = str(change['edited'])
            transformations[(orig, edit)] += 1

        for (orig, edit), count in transformations.most_common(10):
            if count >= 1:
                patterns.append({
                    'type': 'match_type_transformation',
                    'column': col,
                    'from': orig,
                    'to': edit,
                    'count': count,
                    'automation_potential': 'HIGH' if count >= 3 else 'MEDIUM'
                })

    return patterns

def analyze_tug_barge_changes(all_changes, df_original, df_edited):
    """Analyze changes to tug-barge pairing logic."""
    patterns = []

    # Look for rows where tug/barge fields changed
    tug_barge_columns = [col for col in all_changes[0].keys() if col
                         if any(keyword in str(col).upper()
                               for keyword in ['TUG', 'BARGE', 'PAIR', 'TOW'])]

    if not tug_barge_columns:
        return patterns

    # Analyze specific pairing changes
    for change_dict in all_changes:
        if not change_dict:
            continue

        tug_barge_edits = {k: v for k, v in change_dict.items()
                           if any(keyword in str(k).upper()
                                 for keyword in ['TUG', 'BARGE', 'PAIR', 'TOW'])}

        if tug_barge_edits:
            row_idx = list(tug_barge_edits.values())[0]['row_index']
            vessel_name = extract_vessel_name(df_original.iloc[row_idx])

            patterns.append({
                'type': 'tug_barge_pairing',
                'vessel': vessel_name,
                'changes': tug_barge_edits,
                'row_index': row_idx
            })

    return patterns

def analyze_exclusion_patterns(all_changes, df_original):
    """Analyze if user excluded certain vessel types or categories."""
    patterns = []

    # Look for rows that were deleted or marked inactive
    status_changes = []
    for change_dict in all_changes:
        if not change_dict:
            continue

        for col, change_info in change_dict.items():
            if 'STATUS' in str(col).upper() or 'ACTIVE' in str(col).upper() or 'EXCLUDE' in str(col).upper():
                status_changes.append({
                    'column': col,
                    'from': change_info['original'],
                    'to': change_info['edited'],
                    'row_index': change_info['row_index']
                })

    if status_changes:
        # Group by vessel type to find exclusion patterns
        exclusions_by_type = defaultdict(list)

        for change in status_changes:
            row = df_original.iloc[change['row_index']]
            vtype = row.get('ICST_VESSEL_TYPE', row.get('Vessel_Type', 'UNKNOWN'))
            exclusions_by_type[str(vtype)].append(change)

        for vtype, changes in exclusions_by_type.items():
            if len(changes) >= 2:
                patterns.append({
                    'type': 'exclusion_pattern',
                    'vessel_type': vtype,
                    'count': len(changes),
                    'automation_potential': 'HIGH'
                })

    return patterns

def analyze_field_value_changes(changes_by_column):
    """Analyze general field value changes for other patterns."""
    patterns = []

    # Skip columns already analyzed
    skip_columns = ['MATCH', 'TYPE', 'VTYPE', 'TUG', 'BARGE', 'STATUS', 'ACTIVE', 'EXCLUDE']

    for col, changes in changes_by_column.items():
        if any(keyword in str(col).upper() for keyword in skip_columns):
            continue

        if len(changes) < 2:
            continue

        # Look for common patterns
        value_changes = Counter()
        for change in changes:
            orig = str(change['original'])
            edit = str(change['edited'])
            value_changes[(orig, edit)] += 1

        for (orig, edit), count in value_changes.most_common(5):
            patterns.append({
                'type': 'field_value_change',
                'column': col,
                'from': orig,
                'to': edit,
                'count': count,
                'automation_potential': 'MEDIUM' if count >= 3 else 'LOW'
            })

    return patterns

# ============================================================================
# REPORT GENERATION
# ============================================================================

def generate_automation_suggestions(patterns):
    """Generate Python pseudocode suggestions based on patterns."""
    suggestions = []

    for pattern in patterns:
        if pattern['type'] == 'vessel_type_transformation':
            code = f"""
# Vessel Type Transformation: {pattern['from']} → {pattern['to']}
# Occurrences: {pattern['count']}
# Automation Potential: {pattern['automation_potential']}

df.loc[df['{pattern['column']}'] == '{pattern['from']}', '{pattern['column']}'] = '{pattern['to']}'
"""
            suggestions.append(code)

        elif pattern['type'] == 'match_type_transformation':
            code = f"""
# Match Type Update: {pattern['from']} → {pattern['to']}
# Occurrences: {pattern['count']}
# Automation Potential: {pattern['automation_potential']}

df.loc[df['{pattern['column']}'] == '{pattern['from']}', '{pattern['column']}'] = '{pattern['to']}'
"""
            suggestions.append(code)

        elif pattern['type'] == 'exclusion_pattern':
            code = f"""
# Exclusion Pattern: Remove {pattern['vessel_type']} vessels
# Occurrences: {pattern['count']}
# Automation Potential: {pattern['automation_potential']}

# Option 1: Mark as excluded
df.loc[df['Vessel_Type'] == '{pattern['vessel_type']}', 'EXCLUDE'] = True

# Option 2: Filter out entirely
df = df[df['Vessel_Type'] != '{pattern['vessel_type']}']
"""
            suggestions.append(code)

        elif pattern['type'] == 'field_value_change':
            code = f"""
# Field Value Change: {pattern['column']}
# {pattern['from']} → {pattern['to']}
# Occurrences: {pattern['count']}
# Automation Potential: {pattern['automation_potential']}

df.loc[df['{pattern['column']}'] == '{pattern['from']}', '{pattern['column']}'] = '{pattern['to']}'
"""
            suggestions.append(code)

    return suggestions

def write_report(patterns, suggestions, stats, output_path):
    """Write comprehensive analysis report."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""# USACE User Edit Analysis Report
**Generated**: {timestamp}

---

## Executive Summary

**Total Changes Detected**: {stats['total_changes']:,}
**Rows Modified**: {stats['rows_modified']:,} / {stats['total_rows']:,} ({stats['rows_modified']/stats['total_rows']*100:.2f}%)
**Columns Modified**: {stats['columns_modified']}

**Pattern Categories**:
- Vessel Type Transformations: {stats['vessel_type_patterns']}
- Match Type Changes: {stats['match_type_patterns']}
- Tug-Barge Pairing Updates: {stats['tug_barge_patterns']}
- Exclusion Patterns: {stats['exclusion_patterns']}
- Other Field Changes: {stats['other_patterns']}

---

## Pattern Analysis

"""

    # Group patterns by type
    patterns_by_type = defaultdict(list)
    for p in patterns:
        patterns_by_type[p['type']].append(p)

    # Vessel Type Transformations
    if 'vessel_type_transformation' in patterns_by_type:
        report += "### Vessel Type Transformations\n\n"
        report += "| From | To | Count | Column | Automation Potential |\n"
        report += "|------|-----|-------|--------|---------------------|\n"

        for p in patterns_by_type['vessel_type_transformation']:
            report += f"| `{p['from']}` | `{p['to']}` | {p['count']} | {p['column']} | {p['automation_potential']} |\n"

        report += "\n"

    # Match Type Changes
    if 'match_type_transformation' in patterns_by_type:
        report += "### Match Type Changes\n\n"
        report += "| From | To | Count | Column | Automation Potential |\n"
        report += "|------|-----|-------|--------|---------------------|\n"

        for p in patterns_by_type['match_type_transformation']:
            report += f"| `{p['from']}` | `{p['to']}` | {p['count']} | {p['column']} | {p['automation_potential']} |\n"

        report += "\n"

    # Tug-Barge Patterns
    if 'tug_barge_pairing' in patterns_by_type:
        report += "### Tug-Barge Pairing Updates\n\n"

        for p in patterns_by_type['tug_barge_pairing']:
            report += f"**Vessel**: {p['vessel']} (Row {p['row_index']})\n\n"
            for col, change_info in p['changes'].items():
                report += f"- `{col}`: `{change_info['original']}` → `{change_info['edited']}`\n"
            report += "\n"

    # Exclusion Patterns
    if 'exclusion_pattern' in patterns_by_type:
        report += "### Exclusion Patterns\n\n"
        report += "| Vessel Type | Exclusions | Automation Potential |\n"
        report += "|-------------|------------|---------------------|\n"

        for p in patterns_by_type['exclusion_pattern']:
            report += f"| `{p['vessel_type']}` | {p['count']} | {p['automation_potential']} |\n"

        report += "\n"

    # Other Field Changes
    if 'field_value_change' in patterns_by_type:
        report += "### Other Field Value Changes\n\n"
        report += "| Column | From | To | Count | Automation Potential |\n"
        report += "|--------|------|-----|-------|---------------------|\n"

        for p in patterns_by_type['field_value_change']:
            report += f"| `{p['column']}` | `{p['from']}` | `{p['to']}` | {p['count']} | {p['automation_potential']} |\n"

        report += "\n"

    # Automation Suggestions
    report += "---\n\n## Automation Suggestions\n\n"
    report += "Below are Python code snippets that can be integrated into future processing scripts:\n\n"

    for i, suggestion in enumerate(suggestions, 1):
        report += f"### Suggestion {i}\n\n"
        report += "```python\n"
        report += suggestion.strip()
        report += "\n```\n\n"

    # Implementation Notes
    report += "---\n\n## Implementation Notes\n\n"
    report += "**How to Apply These Patterns**:\n\n"
    report += "1. Review each pattern for accuracy and appropriateness\n"
    report += "2. Add high-confidence rules (HIGH automation potential) to main processing script\n"
    report += "3. Test MEDIUM potential rules on sample data before full deployment\n"
    report += "4. Document rule rationale in script comments\n"
    report += "5. Version control: Increment script version when adding new rules\n\n"

    report += "**Integration Locations**:\n\n"
    report += "- `transform_usace_clearance_data_v*.py` - Main clearance transformation script\n"
    report += "- `transform_usace_entrance_data_v*.py` - Main entrance transformation script\n"
    report += "- Add as post-processing step after initial data load\n\n"

    report += "**Testing Checklist**:\n\n"
    report += "- [ ] Test on 2023 sample data\n"
    report += "- [ ] Verify tonnage calculations still accurate\n"
    report += "- [ ] Check vessel type distribution matches expectations\n"
    report += "- [ ] Validate tug-barge pairing logic\n"
    report += "- [ ] Run on full 2024/2025 data\n\n"

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✓ Report written to: {output_path}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("=" * 80)
    print("USACE USER EDIT ANALYSIS v1.0.0")
    print("=" * 80)
    print()

    # Find original file
    print("Searching for original file...")
    original_path = find_file(ORIGINAL_FILE)

    if original_path is None:
        print(f"✗ Original file not found: {ORIGINAL_FILE}")
        print(f"\nSearched locations:")
        for path in USACE_PATHS:
            print(f"  - {path}")
        print(f"  - {BASE_DIR}")
        return

    print(f"✓ Found original: {original_path}")

    # Find edited file
    print("\nSearching for user-edited file...")
    edited_path = find_file(EDITED_FILE)

    if edited_path is None:
        print(f"\n{'='*80}")
        print("WAITING FOR USER EDITS")
        print("=" * 80)
        print(f"\nThe edited file does not exist yet: {EDITED_FILE}")
        print("\nTo create the edited file:")
        print(f"1. Make a copy of: {original_path.name}")
        print(f"2. Rename to: {EDITED_FILE}")
        print(f"3. Open in Excel/CSV editor")
        print("4. Make your corrections:")
        print("   - Fix vessel type classifications")
        print("   - Correct Match_Type values")
        print("   - Adjust tug-barge pairings")
        print("   - Mark vessels for exclusion")
        print("   - Any other data quality improvements")
        print(f"5. Save in same directory: {original_path.parent}")
        print(f"6. Re-run this script: python analyze_user_edits_v1.0.0.py")
        print()
        print("Expected file location:")
        print(f"  {original_path.parent / EDITED_FILE}")
        print()
        return

    print(f"✓ Found edited file: {edited_path}")

    # Load both files
    print("\nLoading files...")
    df_original = load_csv_safe(original_path)
    df_edited = load_csv_safe(edited_path)

    if df_original is None or df_edited is None:
        print("✗ Failed to load files. Exiting.")
        return

    # Validate structure
    if len(df_original) != len(df_edited):
        print(f"\n⚠ WARNING: Row count mismatch!")
        print(f"  Original: {len(df_original):,} rows")
        print(f"  Edited: {len(df_edited):,} rows")
        print(f"  User may have deleted {abs(len(df_original) - len(df_edited)):,} rows")

    # Compare row by row
    print("\nAnalyzing changes row by row...")
    all_changes = []
    changes_by_column = defaultdict(list)

    rows_modified = 0
    total_changes = 0

    for idx in range(min(len(df_original), len(df_edited))):
        row_orig = df_original.iloc[idx]
        row_edit = df_edited.iloc[idx]

        changes = compare_rows(row_orig, row_edit, idx)

        if changes:
            rows_modified += 1
            total_changes += len(changes)
            all_changes.append(changes)

            for col, change_info in changes.items():
                changes_by_column[col].append(change_info)

    print(f"\n✓ Analysis complete")
    print(f"  Rows modified: {rows_modified:,}")
    print(f"  Total field changes: {total_changes:,}")
    print(f"  Columns modified: {len(changes_by_column)}")

    if total_changes == 0:
        print("\nNo changes detected. Files appear identical.")
        return

    # Extract patterns
    print("\nExtracting patterns...")

    patterns = []
    patterns.extend(analyze_vessel_type_changes(changes_by_column))
    patterns.extend(analyze_match_type_changes(changes_by_column))
    patterns.extend(analyze_tug_barge_changes(all_changes, df_original, df_edited))
    patterns.extend(analyze_exclusion_patterns(all_changes, df_original))
    patterns.extend(analyze_field_value_changes(changes_by_column))

    print(f"✓ Found {len(patterns)} patterns")

    # Generate automation suggestions
    print("\nGenerating automation suggestions...")
    suggestions = generate_automation_suggestions(patterns)
    print(f"✓ Generated {len(suggestions)} code suggestions")

    # Compile statistics
    stats = {
        'total_changes': total_changes,
        'rows_modified': rows_modified,
        'total_rows': len(df_original),
        'columns_modified': len(changes_by_column),
        'vessel_type_patterns': len([p for p in patterns if p['type'] == 'vessel_type_transformation']),
        'match_type_patterns': len([p for p in patterns if p['type'] == 'match_type_transformation']),
        'tug_barge_patterns': len([p for p in patterns if p['type'] == 'tug_barge_pairing']),
        'exclusion_patterns': len([p for p in patterns if p['type'] == 'exclusion_pattern']),
        'other_patterns': len([p for p in patterns if p['type'] == 'field_value_change']),
    }

    # Write report
    print("\nGenerating report...")
    output_path = OUTPUT_DIR / OUTPUT_REPORT
    write_report(patterns, suggestions, stats, output_path)

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nReport location: {output_path}")
    print(f"\nNext steps:")
    print("1. Review the report and automation suggestions")
    print("2. Integrate high-confidence patterns into processing scripts")
    print("3. Test on sample data before full deployment")
    print("4. Update script version numbers after integration")
    print()

if __name__ == "__main__":
    main()
