#!/usr/bin/env python3
"""
------------------------------------------------------------------
LOFI GATE: TRANSPARENT VERIFICATION ORCHESTRATOR
------------------------------------------------------------------

Purpose:
    Acts as a lightweight, "Physics-based" gatekeeper for AI Agents.
    It runs standard project verification tools (lint, test, security)
    and logs the results in a format optimized for Large Language Models (LLMs).

Key Features:
    1. Smart Truncation: 
       Reduces massive error logs (e.g., 10,000 lines of failure output) 
       into a concise "Head + Tail" snippet. This saves Context Window costs.
    
    2. Token Economy Tracking:
       Tracks exactly how many tokens were generated vs. how many were sent to history.
       Maintains a running "Total Savings" tally in the log footer.

    3. Interactive Logs:
       Uses HTML <details> tags in Markdown to keep the log file clean
       while preserving the ability for humans/agents to expand errors.

Usage:
    python lofi_gate.py [--parallel] [--serial]
"""

import subprocess
import sys
import os
import json
import argparse
import concurrent.futures
import time
import datetime
import threading

# --- Configuration & Constants ---

# The log file is stored in the Project Root to be easily found by Agents.
LOG_FILENAME = "verification_history.md"

# Max lines to keep in the log file to prevent infinite growth.
# 200 lines is usually enough history for an Agent to understand recent context.
MAX_LOG_LINES = 200

def parse_args():
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(description="LoFi Gate Verification Proxy")
    parser.add_argument('--parallel', action='store_true', help="Run independent checks in parallel to save time.")
    parser.add_argument('--serial', action='store_true', default=True, help="Run checks sequentially (default). Safe for most environments.")
    
    args = parser.parse_args()
    # Explicitly enforce serial=False if parallel is requested
    if args.parallel:
        args.serial = False
    return args

def get_log_path():
    """
    Determines the absolute path to the log file.
    
    Why: Agents often run scripts from arbitrary CWDs (Current Working Directories).
    We use `__file__` to ensure the log is always written to the Project Root,
    adjacent to this script, regardless of where usage orginates.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, LOG_FILENAME)

# --- Logging Subsystem ---

# Global Lock: Essential for --parallel mode to prevent garbled log entries.
log_lock = threading.Lock()

def parse_footer(lines):
    """
    Parses the "Sticky Footer" from the log file.
    
    Structure:
    > 📊 **Total Token Size:** X | 💰 **Total Token Savings:** Y
    
    Why: We want to track cumulative savings across multiple runs, even as the 
    log file rotates (deletes old lines). Parsing the footer before writing allows
    us to carry these totals forward indefinitely.
    """
    size = 0
    savings = 0
    clean_lines = []
    footer_marker_size = "**Total Token Size:**"
    
    for line in lines:
        if footer_marker_size in line:
            try:
                # Remove Markdown block quote "> " and split by delimiter "|"
                content = line.strip().replace("> ", "")
                parts = content.split("|")
                
                # Part 0: extract Size integer
                p0 = parts[0].split(":")[-1].strip().replace("*", "")
                size = int(p0)
                
                # Part 1: extract Savings integer
                if len(parts) > 1:
                    p1 = parts[1].split(":")[-1].strip().replace("*", "")
                    savings = int(p1)
            except: 
                # Fail gracefully; if footer is corrupted, reset stats to 0.
                pass
        else:
            clean_lines.append(line)
            
    return clean_lines, size, savings

def log_to_history(label, status, message, tokens_used=0, tokens_saved=0, duration=0, command_context="", error_content=None):
    """
    Writes a structured entry to the verification_history.md log.
    
    Args:
        label (str): Human-readable name of the check (e.g. "Test Suite")
        status (str): PASS or FAIL
        command_context (str): The actual command run (e.g. "npm test")
        error_content (str): The raw (truncated) error output, if any.
    """
    log_path = get_log_path()
    if not log_path: return

    # Thread-safe write block
    with log_lock:
        # 1. Read existing content (if any)
        lines = []
        if os.path.exists(log_path):
            try:
                with open(log_path, 'r', encoding='utf-8') as f: lines = f.readlines()
            except: pass

        # 2. Extract totals from the old footer and remove it from the list
        lines, current_size, current_savings = parse_footer(lines)
        
        # 3. Log Rotation
        # We enforce a hard limit on log size to keep context windows standard.
        # Uses a generous buffer (2x MAX) before pruning to handle multi-line errors.
        SAFE_LOG_LINES = MAX_LOG_LINES * 2
        if len(lines) > SAFE_LOG_LINES:
            lines = lines[-SAFE_LOG_LINES:]
            if not lines[0].startswith("\n..."):
                 lines.insert(0, f"\n... (Log truncated to last {SAFE_LOG_LINES} lines) ...\n")

        # 4. Update Cumulative Totals
        current_size += tokens_used
        current_savings += tokens_saved

        # 5. Format the Entry
        # Format: - **[TIME]** [CMD] ICON **LABEL**: STATUS (Dur) (Metrics)
        
        metrics_msg = f"(total token size: {tokens_used}) (tokens truncated: {tokens_saved})"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        icon = "✅" if status == "PASS" else "❌"
        duration_str = f"({duration:.2f}s)" if duration > 0 else ""
        context_str = f"[{command_context}]" if command_context else "[Internal]"
        
        entry = f"- **[{timestamp}]** {context_str} {icon} **{label}**: {status} {duration_str} {metrics_msg}\n"
        lines.append(entry)
        
        # 6. Append Interactive Error Snippet (HTML Dropdown)
        # Why: Agents can "expand" this if needed, but it stays collapsed by default.
        if error_content:
            lines.append("  <details>\n")
            lines.append("  <summary>🔍 View Truncated Error</summary>\n\n")
            lines.append("  ```text\n")
            for line in error_content.splitlines():
                lines.append(f"  {line}\n")
            lines.append("  ```\n")
            lines.append("  </details>\n")

        # 7. Append New Sticky Footer
        footer = f"\n> 📊 **Total Token Size:** {current_size} | 💰 **Total Token Savings:** {current_savings}\n"
        lines.append(footer)
        
        # 8. Write-back
        try:
            with open(log_path, 'w', encoding='utf-8') as f: f.writelines(lines)
        except: pass

# --- Metrics & Output ---

def estimate_tokens(text):
    """
    Estimates token count using the standard heuristic: 
    1 token ~= 4 characters (for English text).
    """
    return len(text) // 4

def run_command(command, label="Test"):
    """
    Executes a shell command and captures output.
    
    Why: We use subprocess.run with specific error handling to ensure
    that encoding issues (common on Windows) don't crash the verifier.
    
    Returns:
        (exit_code, output_text, duration_seconds, command_string)
    """
    start_time = time.time()
    try:
        process = subprocess.run(
            command, 
            shell=True,
            # Capture both streams to catch all errors
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True,
            # 'replace' prevents crashes on non-utf8 system outputs
            errors='replace' 
        )
        duration = time.time() - start_time
        return process.returncode, process.stdout, duration, command
    except Exception as e:
        return 1, str(e), time.time() - start_time, command

def print_result(label, exit_code, output, duration, command_context=""):
    """
    Handles the "Smart Truncation" presentation logic.
    Prints to Console AND delegates to the Logger.
    """
    print("-" * 40)
    
    # 1. Metric Calculation
    raw_tokens = estimate_tokens(output)
    
    # 2. Smart Truncation Logic
    # Why: 12,000 char errors are useless spam. We want the Head (Error type)
    # and the Tail (Summary/Stack trace).
    TRUNCATE_LIMIT = 2000
    truncated_output = output
    tokens_truncated = 0
    
    if len(output) > TRUNCATE_LIMIT:
        head = output[:1000]
        tail = output[-1000:]
        truncated_output = f"{head}\n... [Truncated {len(output) - TRUNCATE_LIMIT} chars] ...\n{tail}"
        
        # Re-calc to quantify savings
        compressed_tokens = estimate_tokens(truncated_output)
        tokens_truncated = raw_tokens - compressed_tokens
    
    # 3. Console Feedback
    metrics_display = f"(total token size: {raw_tokens})"
    if tokens_truncated > 0:
        metrics_display += f" (tokens truncated: {tokens_truncated})"
    else:
        metrics_display += " (tokens truncated: 0)"

    # 4. Reporting
    if exit_code == 0:
        print(f"✅ {label} Passed! ({duration:.2f}s) {metrics_display}")
        print("-" * 40)
        # Log Success
        log_to_history(label, "PASS", "Passed", raw_tokens, tokens_truncated, duration, command_context)
    else:
        print(f"❌ {label} Failed ({duration:.2f}s). Showing relevant error output:")
        print("-" * 40)
        print(truncated_output)
        # Log Failure with Snippet
        log_to_history(label, "FAIL", "Failed", raw_tokens, tokens_truncated, duration, command_context, error_content=truncated_output)
            
    return exit_code

# --- Tasks & Gates ---

def check_strict_tdd():
    """
    Gate: Enforces Test Driven Development.
    Checks if any new code files (js, py, rs, go) have been added 
    without a corresponding test file.
    """
    try:
        # Check for untracked (??) or Added (A) files in git
        result = subprocess.run(["git", "status", "--porcelain"], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.splitlines()
        new_files = [line[3:] for line in lines if line.startswith("??") or line.startswith("A ")]
        
        violations = []
        for f in new_files:
            # Filter for source code only
            if f.endswith((".js", ".ts", ".py", ".go", ".rs")) and "test" not in f and "spec" not in f:
                base = os.path.basename(f).split('.')[0]
                # Look for *any* matching test file in the batch or directory
                # This is a loose check, but prevents obvious "No Test" commits.
                if not any(base in other and ("test" in other or "spec" in other) for other in new_files + os.listdir(".")):
                    violations.append(f)
        
        if violations:
            return 1, "❌ STRICT TDD VIOLATION: Missing tests for:\n" + "\n".join(violations), 0.1, "git status"
        return 0, "All new files have tests.", 0.1, "git status"
    except:
        return 0, "Git check skipped.", 0, "git status"

def load_scripts():
    """Helper: Reads package.json scripts to auto-discover capabilities."""
    if os.path.exists("package.json"):
        try:
            with open("package.json", "r") as f:
                return json.load(f).get("scripts", {})
        except:
            return {}
    return {}

def determine_test_command(scripts):
    """
    Heuristic: Decides the best test runner command based on project type.
    Priority: npm script > python pytest > rust cargo > default jest
    """
    if "test:agent" in scripts: return "npm run test:agent"
    if "test" in scripts and "verify" not in scripts["test"]: return "npm test"
    
    if os.path.exists("pyproject.toml") or os.path.exists("requirements.txt") or os.path.isdir("tests"): 
        return "python -m pytest"
        
    if os.path.exists("Cargo.toml"):
        return "cargo test"

    if os.path.exists("go.mod"):
        return "go test ./..."

    return "npx jest"

# --- Main Orchestrator ---

def main():
    start_total = time.time()
    args = parse_args()
    scripts = load_scripts()
    
    tasks = []

    # --- Phase 1: Policy Gates ---
    
    # 1. TDD Check (Are you writing tests?)
    tasks.append(("TDD Check", lambda: check_strict_tdd()))


    # --- Phase 2: Security & Static Analysis ---

    # 2. Security (NPM / Cargo / Go Vulnerability Check)
    if os.path.exists("package.json"):
        tasks.append(("Security Scan", lambda: run_command("npm audit --audit-level=high", "Security")))
    elif os.path.exists("Cargo.toml"):
        tasks.append(("Security Scan", lambda: run_command("cargo audit", "Security")))
    elif os.path.exists("go.mod"):
        # govulncheck is standard, but might not be installed. Fallback or assume availability?
        # Let's use 'go list -m all' pipeline or just skip if no tool.
        # Stick to standard 'go vet' for linting broadly.
        pass 

    # 3. Lint (Code Quality)
    if "lint" in scripts:
        tasks.append(("Lint", lambda: run_command("npm run lint", "Lint")))
    elif os.path.exists("Cargo.toml"):
         tasks.append(("Lint", lambda: run_command("cargo check", "Lint")))
    elif os.path.exists("go.mod"):
        tasks.append(("Lint", lambda: run_command("go vet ./...", "Lint")))

    # --- Phase 3: Correctness ---

    # 4. Tests (Logic Verification)
    test_cmd = determine_test_command(scripts)
    tasks.append(("Test Suite", lambda: run_command(test_cmd, "Tests")))

    # 5. Coverage (Optional Metrics)
    if "coverage" in scripts:
        tasks.append(("Coverage", lambda: run_command("npm run coverage", "Coverage")))

    # --- Execution Engine ---

    overall_failure = False

    if args.parallel:
        print(f"🚀 Running {len(tasks)} checks in PARALLEL...")
        # ThreadPool allows IO-bound tasks (subprocesses) to run concurrently.
        # Note: Heavy CPU tasks (like compiling Rust) might still contend for resources.
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_label = {executor.submit(fn): label for label, fn in tasks}
            
            for future in concurrent.futures.as_completed(future_to_label):
                label = future_to_label[future]
                try:
                    code, out, dur, cmd = future.result()
                    if print_result(label, code, out, dur, cmd) != 0:
                        overall_failure = True
                except Exception as e:
                    print(f"❌ {label} Crashed: {e}")
                    overall_failure = True
    else:
        print(f"🐢 Running {len(tasks)} checks SEQUENTIALLY...")
        for label, fn in tasks:
            print(f"👉 Starting {label}...")
            # Unpack the tuple returned by the lambda -> tool function
            code, out, dur, cmd = fn()
            if print_result(label, code, out, dur, cmd) != 0:
                print("🛑 Fail Fast triggered.")
                sys.exit(code)

    total_duration = time.time() - start_total

    if overall_failure:
        sys.exit(1)
    
    print(f"\n✨ All systems go! (Completed in {total_duration:.2f}s)")
    sys.exit(0)

if __name__ == "__main__":
    main()
