# Session Backup Strategy for Long Claude Code Sessions

**Created**: 2026-01-15
**Purpose**: Ensure continuity across CLI sessions and prevent work loss

---

## Problem Statement

Long development sessions with Claude Code can be interrupted by:
- CLI crashes or timeouts
- Network disconnections
- Context window limits
- Deliberate session breaks

Without proper checkpoints, resuming work requires extensive context rebuilding.

---

## Backup Strategy

### 1. Git Commits as Checkpoints

**Frequency**: After each major task completion

**What to Commit**:
- New/modified scripts (04_SCRIPTS/)
- Updated dictionaries (03_DICTIONARIES/, 01.01_dictionary/)
- Documentation files (05_DOCUMENTATION/, build_documentation/*.md)
- Configuration changes

**What NOT to Commit** (see .gitignore):
- Raw data files (00_raw_data/, 00_STAGE00_RAW_DATA/)
- Preprocessed CSVs (01_step_one/, 01_STAGE01_PREPROCESSING/)
- Large output files (02_STAGE02_CLASSIFICATION/*.csv)
- Checkpoint data (06_CHECKPOINTS/*.parquet)
- Archive folder (_archive/)

**Commit Message Format**:
```
[CHECKPOINT] <Brief description of work completed>

- Detailed change 1
- Detailed change 2
- Files affected: script1.py, dict.csv

Status: <Ready for next phase | In progress | Testing needed>
```

**Example**:
```bash
git add 04_SCRIPTS/transform_usace_entrance_data_v2.0.0.py
git add 04_SCRIPTS/transform_usace_clearance_data_v2.0.0.py
git add 01.01_dictionary/usace_port_codes_from_data.csv
git add 01.01_dictionary/usace_sked_k_foreign_ports.csv
git add 01.01_dictionary/usace_cargoclass.csv
git add 05_DOCUMENTATION/USACE_DATA_TRANSFORMATION_v2.0.0.md
git commit -m "[CHECKPOINT] USACE data transformation v2.1.0 complete

- Added entrance/clearance transformation scripts
- Created USACE port code dictionary (528 codes)
- Implemented vessel enrichment (85.7% match rate)
- Added draft analysis and forecasted activity
- Added cargo classification from ICST types
- Output: 165,683 records with 37 columns each

Files: transform_usace_entrance_data_v2.0.0.py, transform_usace_clearance_data_v2.0.0.py, usace_port_codes_from_data.csv, USACE_DATA_TRANSFORMATION_v2.0.0.md

Status: Complete - ready for analysis/next phase"
```

### 2. Session Documentation

**Create/Update**: `05_DOCUMENTATION/SESSION_LOG_<YYYYMMDD>.md`

**Template**:
```markdown
# Development Session Log - <YYYY-MM-DD>

## Session Start: <HH:MM>

### Current Task
[Description of what you're working on]

### Completed Today
- [x] Task 1
- [x] Task 2
- [ ] Task 3 (in progress)

### Key Decisions Made
- Decision 1: Why and what
- Decision 2: Why and what

### Files Modified
- file1.py (added feature X)
- file2.csv (updated with Y)

### Next Steps
1. Complete task 3
2. Test full pipeline
3. Update documentation

### Issues/Blockers
- Issue 1: Description and status

### Git Commits This Session
- commit_hash: Description

## Session End: <HH:MM>
```

### 3. Code Documentation

**In-Script Comments for Resume Points**:

```python
"""
USACE Data Transformation v2.0.0

RESUME POINT SUMMARY:
- Script processes USACE entrance/clearance data (2023)
- Input: 00_raw_data/00_03_usace_entrance_clearance_raw/
- Output: 02_STAGE02_CLASSIFICATION/usace_2023_*_transformed_v2.1.0.csv
- Dependencies: usace_port_codes_from_data.csv, 01_ships_register.csv, usace_cargoclass.csv

CRITICAL NOTES:
- USACE uses proprietary port codes (NOT Census Sked D)
- Vessel matching: IMO (primary) + Name (secondary)
- Draft analysis requires Vessel_Dwt_Draft_ft from ships register

STATUS: Complete and tested (2026-01-15)
NEXT: Analyze output for cargo flow patterns
"""
```

### 4. Output File Versioning

**Naming Convention**:
```
<dataset>_<year>_<type>_transformed_v<MAJOR>.<MINOR>.<PATCH>_<YYYYMMDD_HHMM>.csv
```

**Example**:
```
usace_2023_inbound_entrance_transformed_v2.1.0_20260115_1430.csv
```

**Benefits**:
- Timestamp shows when processing occurred
- Version shows what transformations were applied
- Can roll back to previous versions if needed

### 5. Build Documentation Updates

**Update After Each Milestone**:

Files to update:
- `README.md` (main project summary)
- `build_documentation/INDEX.html` (web dashboard)
- `05_DOCUMENTATION/PIPELINE_STATUS.md` (current state)

**Status Markers**:
```markdown
## Current Pipeline Status

### Panjiva Classification
- Status: ✅ Complete
- Version: v3.4.0
- Coverage: 71.3% tonnage
- Last Updated: 2026-01-14

### USACE Transformation
- Status: ✅ Complete
- Version: v2.1.0
- Records: 165,683
- Last Updated: 2026-01-15

### Next: USACE-Panjiva Integration
- Status: 🔄 Planning
- Start Date: 2026-01-15
```

---

## Recommended Checkpoint Frequency

| Activity Type | Checkpoint Frequency |
|--------------|---------------------|
| Script Development | After each working version |
| Dictionary Updates | After each version increment |
| Data Processing | Before and after full runs |
| Documentation | At end of session |
| Testing/Debugging | After fixing major bugs |
| Pipeline Milestones | Immediately upon completion |

---

## Recovery Procedure

### When CLI Crashes Mid-Session

1. **Check Latest Git Commit**:
```bash
git log -1
git show HEAD
```

2. **Read Session Log**:
```bash
cat "05_DOCUMENTATION/SESSION_LOG_<YYYYMMDD>.md"
```

3. **Check Script Status Comments**:
- Read "RESUME POINT SUMMARY" in latest modified scripts
- Check "STATUS" and "NEXT" notes

4. **Verify Output Files**:
```bash
# Check latest outputs by timestamp
dir "02_STAGE02_CLASSIFICATION\*.csv" /O-D
```

5. **Continue from Last Known State**:
- If script complete: Move to next task
- If script in progress: Review code, test, continue
- If unclear: Ask user where to resume

### When Starting New Session

1. **Read CLAUDE.md** (project instructions)
2. **Check git status** for uncommitted work
3. **Read latest session log**
4. **Review recent commits** (last 3-5)
5. **Ask user for confirmation** before proceeding

---

## Automation Script

**File**: `04_SCRIPTS/create_checkpoint.py`

```python
"""
Quick checkpoint creator for long sessions

Usage:
    python create_checkpoint.py "Completed USACE transformation"
"""

import sys
import subprocess
from datetime import datetime
from pathlib import Path

def create_checkpoint(message):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    # 1. Stage all tracked files
    subprocess.run(['git', 'add', '-u'])

    # 2. Create checkpoint commit
    commit_msg = f"[CHECKPOINT] {message}\n\nTimestamp: {timestamp}"
    subprocess.run(['git', 'commit', '-m', commit_msg])

    # 3. Push to remote
    subprocess.run(['git', 'push'])

    print(f"✅ Checkpoint created: {message}")
    print(f"   Timestamp: {timestamp}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_checkpoint.py 'Your message here'")
        sys.exit(1)

    create_checkpoint(sys.argv[1])
```

**Usage**:
```bash
python 04_SCRIPTS/create_checkpoint.py "USACE transformation complete"
```

---

## Best Practices

1. **Commit early, commit often** - Don't wait for perfection
2. **Write descriptive commit messages** - Future you will thank you
3. **Update documentation as you go** - Not at the end
4. **Use versioned filenames** - Easy rollback if needed
5. **Test before committing** - Broken code in checkpoints is useless
6. **Push to remote regularly** - Local commits won't survive hardware failure
7. **Document assumptions** - What seems obvious now won't be later

---

## Emergency Recovery Files

**Location**: `06_CHECKPOINTS/emergency_session_state.json`

**Auto-saved every major operation**:
```json
{
  "timestamp": "2026-01-15T14:30:00",
  "current_task": "USACE data transformation",
  "last_script_run": "transform_usace_clearance_data_v2.0.0.py",
  "last_output": "usace_2023_outbound_clearance_transformed_v2.1.0.csv",
  "next_steps": [
    "Commit USACE work to git",
    "Update documentation",
    "Begin USACE-Panjiva integration planning"
  ],
  "files_modified": [
    "04_SCRIPTS/transform_usace_entrance_data_v2.0.0.py",
    "04_SCRIPTS/transform_usace_clearance_data_v2.0.0.py",
    "01.01_dictionary/usace_port_codes_from_data.csv"
  ]
}
```

---

## Checkpoint Checklist

Before ending a session or taking a break:

- [ ] All scripts run successfully
- [ ] Output files verified
- [ ] Git status clean (all changes committed)
- [ ] Documentation updated
- [ ] Session log updated
- [ ] Next steps clearly documented
- [ ] Emergency state file saved
- [ ] Changes pushed to remote

---

**Remember**: The goal is not perfect documentation, but **enough context to resume work smoothly**.
