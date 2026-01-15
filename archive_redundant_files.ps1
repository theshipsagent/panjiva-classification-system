# Archive Redundant Draft Files - 2026-01-15
# This script moves old development/test files to _archive/redundant_drafts_20260115/

$archiveBase = "G:\My Drive\LLM\project_manifest\_archive\redundant_drafts_20260115"

# Create archive directory structure
New-Item -ItemType Directory -Force -Path "$archiveBase\04_SCRIPTS" | Out-Null
New-Item -ItemType Directory -Force -Path "$archiveBase\03_DICTIONARIES" | Out-Null

Write-Host "Archive folder created: $archiveBase"
Write-Host ""

# Files to archive from 04_SCRIPTS
$scriptsToArchive = @(
    # Old classify versions (v1.x - keep only v3.x)
    "classify_15k_sample_v1.0.0.py",
    "classify_15k_sample_v1.0.1.py",
    "classify_15k_sample_v1.0.2.py",
    "classify_15k_sample_v1.0.3.py",
    "classify_15k_sample_v1.1.0.py",
    "classify_15k_sample_v1.1.1.py",
    "classify_15k_sample_v1.2.0.py",
    "classify_15k_sample_v1.2.1.py",

    # Debug scripts
    "debug_carrier_matching.py",
    "debug_phase2_matching.py",

    # Analysis scripts (old)
    "analyze_what_was_lost.py",
    "analyze_v2.5.2_by_tons.py",
    "analyze_missing_hs4_by_tonnage.py",
    "analyze_tbn_remaining_v3.1.py",
    "analyze_vtype_impact.py",
    "analyze_phase5_v32.py",
    "analyze_tonnage_filter_blocks.py",
    "analyze_tbn_remaining_v3.3.py",
    "analyze_phase1_lock_problem.py",
    "analyze_tbn_remaining_v3.4.py",
    "analyze_chemicals_bulk.py",
    "analyze_v3.6.0_results.py",
    "analyze_clearance_by_region.py",

    # Check scripts
    "check_carrier_rules.py",
    "check_wlwh_classification.py",
    "check_results_v2.py",
    "check_results_FINAL.py",
    "check_phase1_locks.py",
    "check_pipeline_progress.py",
    "check_all_pipelines_progress.py",

    # Compare scripts
    "compare_v31_v32_tonnage.py",

    # Fix scripts
    "fix_carrier_scac_v1.0.0.py",
    "fix_carrier_rules_scac_only.py",
    "fix_vtype_roro_locks.py",
    "fix_carrier_rules_remove_hs.py",
    "fix_vehicle_carrier_groups.py",
    "fix_phase1_locks_v3.4.0.py",
    "fix_and_convert_hs28-29.py",
    "fix_and_convert_2mil_tons.py"
)

$movedCount = 0
$scriptPath = "G:\My Drive\LLM\project_manifest\04_SCRIPTS"

Write-Host "Moving scripts from 04_SCRIPTS/..."
foreach ($file in $scriptsToArchive) {
    $source = Join-Path $scriptPath $file
    $dest = Join-Path "$archiveBase\04_SCRIPTS" $file

    if (Test-Path $source) {
        Move-Item -Path $source -Destination $dest -Force
        Write-Host "  Moved: $file"
        $movedCount++
    }
}

Write-Host ""
Write-Host "Scripts moved: $movedCount"
Write-Host ""

# Move old dictionary versions (v2.x)
$dictPath = "G:\My Drive\LLM\project_manifest\03_DICTIONARIES\03.01_cargo_classification"
$dictFiles = Get-ChildItem -Path $dictPath -Filter "cargo_classification_dictionary_v2*.csv"

Write-Host "Moving old dictionary versions (v2.x)..."
$dictMoved = 0
foreach ($file in $dictFiles) {
    $dest = Join-Path "$archiveBase\03_DICTIONARIES" $file.Name
    Move-Item -Path $file.FullName -Destination $dest -Force
    Write-Host "  Moved: $($file.Name)"
    $dictMoved++
}

Write-Host ""
Write-Host "Dictionary files moved: $dictMoved"
Write-Host ""
Write-Host "Archive complete!"
Write-Host "Total files archived: $($movedCount + $dictMoved)"
