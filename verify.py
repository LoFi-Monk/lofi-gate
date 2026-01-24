#!/usr/bin/env python3
"""
------------------------------------------------------------------
TRANSPARENT VERIFICATION PROXY (Standalone)
------------------------------------------------------------------

Purpose: 
Orchestrates project verification (Lint, Test, Security, Coverage).
Optimized for AI Agents with "Smart Truncation" and optional Parallelism.

Usage:
    python verify.py [--parallel] [--serial]
"""

import subprocess
import sys
import os
import json
import argparse
import concurrent.futures
import time

# --- Configuration ---

def parse_args():
    parser = argparse.ArgumentParser(description="AI Verification Proxy")
    parser.add_argument('--parallel', action='store_true', help="Run independent checks in parallel")
    parser.add_argument('--serial', action='store_true', default=True, help="Run checks sequentially (default)")
    
    # Logic: if --parallel is set, serial is False. 
    args = parser.parse_args()
    if args.parallel:
        args.serial = False
    return args

# --- Core Logic ---

def run_command(command, label="Test"):
    """
    Runs a command and returns (exit_code, output_text).
    Does NOT print immediately to allow buffering for parallel execution.
    """
    start_time = time.time()
    try:
        process = subprocess.run(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True
        )
        duration = time.time() - start_time
        return process.returncode, process.stdout, duration
    except Exception as e:
        return 1, str(e), time.time() - start_time

def print_result(label, exit_code, output, duration):
    """
    Formats the output with Smart Truncation.
    """
    print("-" * 40)
    if exit_code == 0:
        print(f"✅ {label} Passed! ({duration:.2f}s)")
        print("-" * 40)
    else:
        print(f"❌ {label} Failed ({duration:.2f}s). Showing relevant error output:")
        print("-" * 40)
        lines = output.splitlines()
        if len(lines) > 100:
            print(f"... [Truncated {len(lines) - 100} lines] ...")
            print("\n".join(lines[-100:]))
        else:
            print(output)
    return exit_code

# --- Tasks ---

def check_strict_tdd():
    try:
        result = subprocess.run(["git", "status", "--porcelain"], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.splitlines()
        new_files = [line[3:] for line in lines if line.startswith("??") or line.startswith("A ")]
        
        violations = []
        for f in new_files:
            if f.endswith((".js", ".ts", ".py", ".go", ".rs")) and "test" not in f and "spec" not in f:
                base = os.path.basename(f).split('.')[0]
                # Loose check for matching test file
                if not any(base in other and ("test" in other or "spec" in other) for other in new_files + os.listdir(".")):
                    violations.append(f)
        
        if violations:
            return 1, "❌ STRICT TDD VIOLATION: Missing tests for:\n" + "\n".join(violations), 0.1
        return 0, "All new files have tests.", 0.1
    except:
        return 0, "Git check skipped.", 0

def load_scripts():
    if os.path.exists("package.json"):
        try:
            with open("package.json", "r") as f:
                return json.load(f).get("scripts", {})
        except:
            return {}
    return {}

def determine_test_command(scripts):
    if "test:agent" in scripts: return "npm run test:agent"
    if "test" in scripts and "verify" not in scripts["test"]: return "npm test"
    if os.path.exists("pyproject.toml"): return "pytest"
    return "npx jest"

# --- Orchestrator ---

def main():
    args = parse_args()
    scripts = load_scripts()
    
    tasks = []

    # 1. TDD Gate (Always run first? Or parallel? usually fast enough to be parallel)
    tasks.append(("TDD Check", lambda: check_strict_tdd()))

    # 2. Security
    if os.path.exists("package.json"):
        tasks.append(("Security Scan", lambda: run_command("npm audit --audit-level=high", "Security")))

    # 3. Lint
    if "lint" in scripts:
        tasks.append(("Lint", lambda: run_command("npm run lint", "Lint")))

    # 4. Tests
    test_cmd = determine_test_command(scripts)
    tasks.append(("Test Suite", lambda: run_command(test_cmd, "Tests")))

    # 5. Coverage
    if "coverage" in scripts:
        tasks.append(("Coverage", lambda: run_command("npm run coverage", "Coverage")))

    overall_failure = False

    if args.parallel:
        print(f"🚀 Running {len(tasks)} checks in PARALLEL...")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # map futures to labels
            future_to_label = {executor.submit(fn): label for label, fn in tasks}
            
            for future in concurrent.futures.as_completed(future_to_label):
                label = future_to_label[future]
                try:
                    code, out, dur = future.result()
                    # We output as they complete. 
                    # If users want strict ordering, they use serial.
                    if print_result(label, code, out, dur) != 0:
                        overall_failure = True
                except Exception as e:
                    print(f"❌ {label} Crashed: {e}")
                    overall_failure = True
    else:
        print(f"🐢 Running {len(tasks)} checks SEQUENTIALLY...")
        for label, fn in tasks:
            print(f"👉 Starting {label}...")
            code, out, dur = fn()
            if print_result(label, code, out, dur) != 0:
                print("🛑 Fail Fast triggered.")
                sys.exit(code)

    if overall_failure:
        sys.exit(1)
    
    print("\n✨ All systems go!")
    sys.exit(0)

if __name__ == "__main__":
    main()
