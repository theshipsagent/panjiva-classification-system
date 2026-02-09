"""
Refinement Task Registry - Controlled Overwrite Permissions
============================================================
Central registry of all approved refinement tasks.

Each task has explicit permissions for what it can modify.
**NO DRIFT** - Only approved tasks can make changes.

Author: WSD3 / Claude Code
Date: 2026-02-09
"""

from datetime import datetime

# ============================================================================
# APPROVED REFINEMENT TASKS
# ============================================================================

REFINEMENT_TASK_REGISTRY = {

    # ------------------------------------------------------------------------
    # CONSTRUCTION MATERIALS - Priority 1
    # ------------------------------------------------------------------------

    "CEMENT_ORIGIN_v1.0": {
        "description": "Add origin detail to cement Cargo_Detail",
        "can_overwrite": {
            "Cargo_Detail": True,
            "Market_Segment": True,
            "Trade_Lane_ID": True
        },
        "conditions": {
            "Commodity": ["Cement"],
            "Current_Cargo_Detail": ["Cement NOS", "Cement", "Cement - Imported"]
        },
        "prevent_overwrite_if": [
            "contains:Cargo_Detail:Turkish",
            "contains:Cargo_Detail:Vietnamese",
            "contains:Cargo_Detail:Mexican",
            "gt:Refinement_Confidence:85"  # Don't overwrite high-confidence
        ],
        "audit": True,
        "version": "1.0.0",
        "approved_by": "WSD3",
        "approved_date": "2026-02-09",
        "status": "ACTIVE"
    },

    "SCM_PRODUCTS_v1.0": {
        "description": "Identify specific SCM product types (GGBFS, Fly Ash, Natural Pozzolan)",
        "can_overwrite": {
            "Cargo_Detail": True
        },
        "conditions": {
            "Commodity": ["Slag/Ash/Pozzolan", "SCM", "Pozzolan"],
            "Current_Cargo_Detail": ["SCM NOS", "Pozzolan NOS", "Slag", "Ash"]
        },
        "prevent_overwrite_if": [
            "contains:Cargo_Detail:GGBFS",
            "contains:Cargo_Detail:Fly Ash",
            "contains:Cargo_Detail:Natural Pozzolan",
            "gt:Refinement_Confidence:85"
        ],
        "audit": True,
        "version": "1.0.0",
        "approved_by": "WSD3",
        "approved_date": "2026-02-09",
        "status": "ACTIVE"
    },

    "AGGREGATES_DETAIL_v1.0": {
        "description": "Distinguish aggregate types (crushed stone, sand, gravel)",
        "can_overwrite": {
            "Cargo_Detail": True
        },
        "conditions": {
            "Commodity": ["Aggregates"],
            "Current_Cargo_Detail": ["Aggregates NOS", "Stone", "Sand"]
        },
        "prevent_overwrite_if": [
            "contains:Cargo_Detail:Crushed Stone",
            "contains:Cargo_Detail:Gravel",
            "gt:Refinement_Confidence:85"
        ],
        "audit": True,
        "version": "1.0.0",
        "approved_by": "WSD3",
        "approved_date": "2026-02-09",
        "status": "ACTIVE"
    },

    "CONSTRUCTION_TRADE_LANES_v1.0": {
        "description": "Tag construction material trade lanes for market analysis",
        "can_overwrite": {
            "Market_Segment": True,
            "Trade_Lane_ID": True,
            "Customer_Market": True
        },
        "conditions": {
            "Commodity": ["Cement", "Aggregates", "Slag/Ash/Pozzolan"]
        },
        "prevent_overwrite_if": [
            "notnull:Market_Segment"  # Don't overwrite if already set
        ],
        "audit": True,
        "version": "1.0.0",
        "approved_by": "WSD3",
        "approved_date": "2026-02-09",
        "status": "ACTIVE"
    },

    # ------------------------------------------------------------------------
    # STEEL - Priority 2
    # ------------------------------------------------------------------------

    "STEEL_PRODUCT_FORMS_v1.0": {
        "description": "Identify steel product forms (coils, slabs, bars, beams, pipe)",
        "can_overwrite": {
            "Cargo_Detail": True
        },
        "conditions": {
            "Commodity": ["Steel"],
            "Cargo": ["Steel Products", "Flat-Rolled Steel", "Long Steel"],
            "Current_Cargo_Detail": ["Steel Products NOS", "Steel NOS", "Flat-Rolled NOS"]
        },
        "prevent_overwrite_if": [
            "contains:Cargo_Detail:Hot-Rolled",
            "contains:Cargo_Detail:Cold-Rolled",
            "contains:Cargo_Detail:Coil",
            "contains:Cargo_Detail:Slab",
            "gt:Refinement_Confidence:85"
        ],
        "audit": True,
        "version": "1.0.0",
        "approved_by": "WSD3",
        "approved_date": "2026-02-09",
        "status": "PENDING"  # Not yet implemented
    },

    # ------------------------------------------------------------------------
    # WIND/SOLAR - Priority 3
    # ------------------------------------------------------------------------

    "WIND_COMPONENT_DETAIL_v1.0": {
        "description": "Identify wind turbine components (blades, nacelles, towers, etc.)",
        "can_overwrite": {
            "Cargo_Detail": True,
            "Market_Segment": True
        },
        "conditions": {
            "Current_Cargo_Detail": ["Project Cargo NOS", "Heavy Lift", "Breakbulk"]
        },
        "prevent_overwrite_if": [
            "contains:Cargo_Detail:Wind Turbine",
            "contains:Cargo_Detail:Blade",
            "contains:Cargo_Detail:Nacelle",
            "gt:Refinement_Confidence:85"
        ],
        "audit": True,
        "version": "1.0.0",
        "approved_by": "WSD3",
        "approved_date": "2026-02-09",
        "status": "PENDING"
    },

    "SOLAR_COMPONENT_DETAIL_v1.0": {
        "description": "Identify solar components (panels, inverters, trackers, etc.)",
        "can_overwrite": {
            "Cargo_Detail": True,
            "Market_Segment": True
        },
        "conditions": {
            "Current_Cargo_Detail": ["Project Cargo NOS", "General Cargo"]
        },
        "prevent_overwrite_if": [
            "contains:Cargo_Detail:Solar Panel",
            "contains:Cargo_Detail:Photovoltaic",
            "gt:Refinement_Confidence:85"
        ],
        "audit": True,
        "version": "1.0.0",
        "approved_by": "WSD3",
        "approved_date": "2026-02-09",
        "status": "PENDING"
    },
}


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def evaluate_condition(record, condition_str):
    """
    Evaluate a condition string against a record.

    Condition format:
        "contains:field:value"  → field contains value
        "gt:field:value"        → field > value
        "lt:field:value"        → field < value
        "eq:field:value"        → field == value
        "notnull:field"         → field is not null

    Args:
        record: DataFrame row
        condition_str: Condition string

    Returns:
        bool: True if condition met
    """
    import pandas as pd

    parts = condition_str.split(':')
    op = parts[0]

    if op == 'contains':
        field, value = parts[1], parts[2]
        field_value = str(record.get(field, ''))
        return value.upper() in field_value.upper()

    elif op == 'gt':
        field, value = parts[1], float(parts[2])
        field_value = record.get(field, 0)
        return pd.notna(field_value) and float(field_value) > value

    elif op == 'lt':
        field, value = parts[1], float(parts[2])
        field_value = record.get(field, 0)
        return pd.notna(field_value) and float(field_value) < value

    elif op == 'eq':
        field, value = parts[1], parts[2]
        return str(record.get(field, '')) == value

    elif op == 'notnull':
        field = parts[1]
        return pd.notna(record.get(field))

    return False


def validate_overwrite(record, task_name, field_name, new_value):
    """
    Check if a refinement task is allowed to overwrite a field.

    Args:
        record: DataFrame row
        task_name: Name of refinement task
        field_name: Field to overwrite
        new_value: New value to set

    Returns:
        tuple: (allowed: bool, reason: str)
    """
    # Check task exists and is approved
    if task_name not in REFINEMENT_TASK_REGISTRY:
        return False, f"Task {task_name} not in approved registry"

    task = REFINEMENT_TASK_REGISTRY[task_name]

    # Check task is active
    if task.get('status') != 'ACTIVE':
        return False, f"Task {task_name} status is {task.get('status')}, not ACTIVE"

    # Check field overwrite permission
    if not task['can_overwrite'].get(field_name, False):
        return False, f"Task {task_name} not permitted to overwrite {field_name}"

    # Check commodity conditions
    conditions = task.get('conditions', {})
    if 'Commodity' in conditions:
        if record.get('Commodity') not in conditions['Commodity']:
            return False, f"Record commodity '{record.get('Commodity')}' not in task scope"

    # Check current value conditions
    if 'Current_Cargo_Detail' in conditions and field_name == 'Cargo_Detail':
        if record.get(field_name) not in conditions['Current_Cargo_Detail']:
            return False, f"Current value '{record.get(field_name)}' not eligible for overwrite"

    # Check prevent conditions
    for prevent_condition in task.get('prevent_overwrite_if', []):
        if evaluate_condition(record, prevent_condition):
            return False, f"Prevented by condition: {prevent_condition}"

    return True, "Overwrite approved"


def get_active_tasks():
    """Get list of active refinement tasks"""
    return {
        name: task
        for name, task in REFINEMENT_TASK_REGISTRY.items()
        if task.get('status') == 'ACTIVE'
    }


def get_task_info(task_name):
    """Get information about a specific task"""
    if task_name not in REFINEMENT_TASK_REGISTRY:
        return None
    return REFINEMENT_TASK_REGISTRY[task_name]


# ============================================================================
# AUDIT LOGGING
# ============================================================================

def log_refinement_change(change_record, log_file="refinement_audit.csv"):
    """
    Log a refinement change to audit trail.

    Args:
        change_record: dict with change details
        log_file: Path to audit log file
    """
    import pandas as pd
    from pathlib import Path

    log_path = Path(log_file)

    # Append to existing log or create new
    if log_path.exists():
        log_df = pd.read_csv(log_path)
        log_df = pd.concat([log_df, pd.DataFrame([change_record])], ignore_index=True)
    else:
        log_df = pd.DataFrame([change_record])

    log_df.to_csv(log_path, index=False)


if __name__ == "__main__":
    # Display active tasks
    print("ACTIVE REFINEMENT TASKS")
    print("=" * 80)

    active_tasks = get_active_tasks()
    for task_name, task in active_tasks.items():
        print(f"\n{task_name} (v{task['version']})")
        print(f"  Description: {task['description']}")
        print(f"  Can overwrite: {', '.join(task['can_overwrite'].keys())}")
        print(f"  Approved by: {task['approved_by']} on {task['approved_date']}")
