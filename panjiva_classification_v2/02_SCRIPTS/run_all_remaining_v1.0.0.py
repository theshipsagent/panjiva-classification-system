"""
Autonomous Pipeline Orchestrator v1.0.0
========================================

Completes all remaining classification and enrichment tasks:
1. Wait for 2024 Step 02 (classification) to complete
2. Run 2024 Step 03 (port enrichment)
3. Run 2023 full pipeline (Steps 01b → 02 → 03)
4. Run 2025 full pipeline (Steps 01b → 02 → 03)
5. Generate final summary

Author: WSD3 / Claude Code
Date: 2026-01-28
Version: 1.0.0
"""

import subprocess
import time
import logging
import sys
from pathlib import Path
from datetime import datetime

# Setup logging
LOG_DIR = Path(__file__).parent.parent / "05_LOGS"
LOG_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = LOG_DIR / f"run_all_remaining_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

SCRIPT_DIR = Path(__file__).parent

def run_step(script_name, args=None, description="", timeout=7200):
    """Run a pipeline step and wait for completion"""
    logging.info("="*70)
    logging.info(f"RUNNING: {description}")
    logging.info("="*70)

    cmd = [sys.executable, str(SCRIPT_DIR / script_name)]
    if args:
        cmd.extend(args)

    logging.info(f"Command: {' '.join(cmd)}")

    try:
        start_time = time.time()
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=SCRIPT_DIR,
            encoding='utf-8',
            errors='replace'
        )
        elapsed = time.time() - start_time

        if result.returncode == 0:
            logging.info(f"SUCCESS: {description} (elapsed: {elapsed/60:.1f} min)")
            logging.info("Output (last 30 lines):")
            for line in result.stdout.split('\n')[-30:]:
                if line.strip():
                    logging.info(f"  {line}")
            return True
        else:
            logging.error(f"FAILED: {description} (return code: {result.returncode})")
            logging.error("STDOUT:")
            logging.error(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
            logging.error("STDERR:")
            logging.error(result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr)
            return False

    except subprocess.TimeoutExpired:
        logging.error(f"TIMEOUT: {description} (exceeded {timeout}s)")
        return False
    except Exception as e:
        logging.error(f"ERROR: {description} - {e}")
        return False

def check_2024_classification_complete():
    """Check if 2024 classification is complete"""
    classified_dir = SCRIPT_DIR.parent / "03_DATA" / "02_classified"
    pattern = "panjiva_imports_2024_classified*.csv"
    files = list(classified_dir.glob(pattern))

    if not files:
        return False

    # Check if file is complete (has expected number of rows)
    latest = sorted(files, key=lambda x: x.stat().st_mtime)[-1]

    # Quick check - file should be ~360-370 MB
    size_mb = latest.stat().st_size / (1024*1024)
    if size_mb > 350:
        logging.info(f"2024 classification file exists: {latest.name} ({size_mb:.1f} MB)")
        return True

    return False

def wait_for_2024_classification(max_wait_minutes=60):
    """Wait for 2024 classification to complete"""
    logging.info("="*70)
    logging.info("WAITING FOR 2024 CLASSIFICATION TO COMPLETE")
    logging.info("="*70)

    start_time = time.time()
    check_interval = 120  # Check every 2 minutes

    while (time.time() - start_time) < (max_wait_minutes * 60):
        if check_2024_classification_complete():
            elapsed = (time.time() - start_time) / 60
            logging.info(f"2024 classification complete! (waited {elapsed:.1f} minutes)")
            return True

        elapsed = (time.time() - start_time) / 60
        logging.info(f"Still waiting... ({elapsed:.1f} / {max_wait_minutes} minutes)")
        time.sleep(check_interval)

    logging.error(f"Timeout: 2024 classification did not complete in {max_wait_minutes} minutes")
    return False

def main():
    logging.info("="*70)
    logging.info("AUTONOMOUS PIPELINE ORCHESTRATOR v1.0.0")
    logging.info("="*70)
    logging.info(f"Started: {datetime.now()}")
    logging.info(f"Log file: {log_file}")

    steps_completed = []
    steps_failed = []

    # Step 1: Wait for 2024 classification
    if not wait_for_2024_classification(max_wait_minutes=60):
        logging.error("Cannot proceed - 2024 classification not complete")
        sys.exit(1)

    # Step 2: 2024 Port Enrichment
    if run_step("step03_enrich_ports_v1.0.0.py", ["2024"],
                "2024 Step 03: Port Enrichment", timeout=600):
        steps_completed.append("2024 Port Enrichment")
    else:
        steps_failed.append("2024 Port Enrichment")
        logging.warning("Continuing despite failure...")

    # Step 3: 2023 Full Pipeline
    logging.info("\n" + "="*70)
    logging.info("STARTING 2023 FULL PIPELINE")
    logging.info("="*70)

    if run_step("step01b_enhance_authoritative_v1.0.0.py", ["2023"],
                "2023 Step 01b: Enhancement", timeout=300):
        steps_completed.append("2023 Enhancement")

        # Find the preprocessed file
        preproc_dir = SCRIPT_DIR.parent / "03_DATA" / "01_preprocessed"
        preproc_files = sorted(preproc_dir.glob("panjiva_imports_2023_preprocessed*.csv"),
                              key=lambda x: x.stat().st_mtime)

        if preproc_files:
            preproc_file = preproc_files[-1]

            if run_step("step02_classify_v1.0.0.py",
                       ["--input", str(preproc_file), "--year", "2023"],
                       "2023 Step 02: Classification", timeout=1800):
                steps_completed.append("2023 Classification")

                if run_step("step03_enrich_ports_v1.0.0.py", ["2023"],
                           "2023 Step 03: Port Enrichment", timeout=300):
                    steps_completed.append("2023 Port Enrichment")
                else:
                    steps_failed.append("2023 Port Enrichment")
            else:
                steps_failed.append("2023 Classification")
        else:
            logging.error("2023 preprocessed file not found")
            steps_failed.append("2023 Classification (file not found)")
    else:
        steps_failed.append("2023 Enhancement")

    # Step 4: 2025 Full Pipeline
    logging.info("\n" + "="*70)
    logging.info("STARTING 2025 FULL PIPELINE")
    logging.info("="*70)

    if run_step("step01b_enhance_authoritative_v1.0.0.py", ["2025"],
                "2025 Step 01b: Enhancement", timeout=300):
        steps_completed.append("2025 Enhancement")

        # Find the preprocessed file
        preproc_dir = SCRIPT_DIR.parent / "03_DATA" / "01_preprocessed"
        preproc_files = sorted(preproc_dir.glob("panjiva_imports_2025_preprocessed*.csv"),
                              key=lambda x: x.stat().st_mtime)

        if preproc_files:
            preproc_file = preproc_files[-1]

            if run_step("step02_classify_v1.0.0.py",
                       ["--input", str(preproc_file), "--year", "2025"],
                       "2025 Step 02: Classification", timeout=3600):
                steps_completed.append("2025 Classification")

                if run_step("step03_enrich_ports_v1.0.0.py", ["2025"],
                           "2025 Step 03: Port Enrichment", timeout=300):
                    steps_completed.append("2025 Port Enrichment")
                else:
                    steps_failed.append("2025 Port Enrichment")
            else:
                steps_failed.append("2025 Classification")
        else:
            logging.error("2025 preprocessed file not found")
            steps_failed.append("2025 Classification (file not found)")
    else:
        steps_failed.append("2025 Enhancement")

    # Final Summary
    logging.info("\n" + "="*70)
    logging.info("PIPELINE ORCHESTRATION COMPLETE")
    logging.info("="*70)
    logging.info(f"Completed: {datetime.now()}")
    logging.info(f"Total time: {(time.time() - start_time)/3600:.1f} hours")

    logging.info(f"\nSteps Completed ({len(steps_completed)}):")
    for step in steps_completed:
        logging.info(f"  + {step}")

    if steps_failed:
        logging.info(f"\nSteps Failed ({len(steps_failed)}):")
        for step in steps_failed:
            logging.info(f"  - {step}")

    # Check final outputs
    enriched_dir = SCRIPT_DIR.parent / "03_DATA" / "03_enriched"
    if enriched_dir.exists():
        files = list(enriched_dir.glob("*.csv"))
        logging.info(f"\nFinal enriched files ({len(files)}):")
        for f in sorted(files):
            size_mb = f.stat().st_size / (1024*1024)
            logging.info(f"  {f.name} ({size_mb:.1f} MB)")

    logging.info(f"\nLog file: {log_file}")

    if steps_failed:
        sys.exit(1)
    else:
        logging.info("\nSTATUS: ALL STEPS SUCCESSFUL")
        sys.exit(0)

if __name__ == "__main__":
    try:
        start_time = time.time()
        main()
    except KeyboardInterrupt:
        logging.warning("\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        logging.error(f"\nUnexpected error: {e}")
        import traceback
        logging.error(traceback.format_exc())
        sys.exit(1)
