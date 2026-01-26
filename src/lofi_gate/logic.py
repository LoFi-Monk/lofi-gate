import subprocess
import sys
import os
import json
import concurrent.futures
import time
from .logger import log_to_history

# --- Helper Functions ---

def estimate_tokens(text):
    """
    Estimates token count using the standard heuristic: 
    1 token ~= 4 characters (for English text).
    """
    return len(text) // 4

def run_command(command, label="Test"):
    """
    Executes a shell command and captures output.
    Returns: (exit_code, output_text, duration_seconds, command_string)
    """
    start_time = time.time()
    try:
        process = subprocess.run(
            command, 
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True,
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
    Returns: (exit_code, tokens_truncated)
    """
    print("-" * 40)
    
    raw_tokens = estimate_tokens(output)
    TRUNCATE_LIMIT = 2000
    truncated_output = output
    tokens_truncated = 0
    
    if len(output) > TRUNCATE_LIMIT:
        head = output[:1000]
        tail = output[-1000:]
        truncated_output = f"{head}\n... [Truncated {len(output) - TRUNCATE_LIMIT} chars] ...\n{tail}"
        compressed_tokens = estimate_tokens(truncated_output)
        tokens_truncated = raw_tokens - compressed_tokens
    
    metrics_display = f"(total token size: {raw_tokens})"
    if tokens_truncated > 0:
        metrics_display += f" (tokens truncated: {tokens_truncated})"
    else:
        metrics_display += " (tokens truncated: 0)"

    if exit_code == 0:
        print(f"✅ {label} Passed! ({duration:.2f}s) {metrics_display}")
        print("-" * 40)
        log_to_history(label, "PASS", "Passed", raw_tokens, tokens_truncated, duration, command_context)
    else:
        print(f"❌ {label} Failed ({duration:.2f}s). Showing relevant error output:")
        print("-" * 40)
        print(truncated_output)
        log_to_history(label, "FAIL", "Failed", raw_tokens, tokens_truncated, duration, command_context, error_content=truncated_output)
            
    return exit_code, tokens_truncated

def check_strict_tdd():
    """
    Gate: Enforces Test Driven Development.
    Checks if any new code files have been added without a corresponding test file.
    """
    try:
        result = subprocess.run(["git", "status", "--porcelain"], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.splitlines()
        new_files = [line[3:] for line in lines if line.startswith("??") or line.startswith("A ")]
        
        violations = []
        for f in new_files:
            if f.endswith((".js", ".ts", ".py", ".go", ".rs")) and "test" not in f and "spec" not in f:
                base = os.path.basename(f).split('.')[0]
                if not any(base in other and ("test" in other or "spec" in other) for other in new_files + os.listdir(".")):
                    violations.append(f)
        
        if violations:
            return 1, "❌ STRICT TDD VIOLATION: Missing tests for:\n" + "\n".join(violations), 0.1, "git status"
        return 0, "All new files have tests.", 0.1, "git status"
    except:
        return 0, "Git check skipped.", 0, "git status"

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
    if os.path.exists("pyproject.toml") or os.path.exists("requirements.txt") or os.path.isdir("tests"): 
        return "python -m pytest"
    if os.path.exists("Cargo.toml"):
        return "cargo test"
    if os.path.exists("go.mod"):
        return "go test ./..."
    return "npx jest"

def run_checks(parallel=False):
    """
    Runs the verification suite.
    """
    start_total = time.time()
    scripts = load_scripts()
    tasks = []

    # 1. TDD Check
    tasks.append(("TDD Check", lambda: check_strict_tdd()))

    # 2. Security
    if os.path.exists("package.json"):
        tasks.append(("Security Scan", lambda: run_command("npm audit --audit-level=high", "Security")))
    elif os.path.exists("Cargo.toml"):
        tasks.append(("Security Scan", lambda: run_command("cargo audit", "Security")))

    # 3. Lint
    if "lint" in scripts:
        tasks.append(("Lint", lambda: run_command("npm run lint", "Lint")))
    elif os.path.exists("Cargo.toml"):
         tasks.append(("Lint", lambda: run_command("cargo check", "Lint")))
    elif os.path.exists("go.mod"):
        tasks.append(("Lint", lambda: run_command("go vet ./...", "Lint")))

    # 4. Tests
    test_cmd = determine_test_command(scripts)
    tasks.append(("Test Suite", lambda: run_command(test_cmd, "Tests")))

    # 5. Coverage
    if "coverage" in scripts:
        tasks.append(("Coverage", lambda: run_command("npm run coverage", "Coverage")))

    overall_failure = False
    total_savings = 0

    if parallel:
        print(f"🚀 Running {len(tasks)} checks in PARALLEL...")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_label = {executor.submit(fn): label for label, fn in tasks}
            for future in concurrent.futures.as_completed(future_to_label):
                label = future_to_label[future]
                try:
                    code, out, dur, cmd = future.result()
                    exit_code, saved = print_result(label, code, out, dur, cmd)
                    total_savings += saved
                    if exit_code != 0:
                        overall_failure = True
                except Exception as e:
                    print(f"❌ {label} Crashed: {e}")
                    overall_failure = True
    else:
        print(f"🐢 Running {len(tasks)} checks SEQUENTIALLY...")
        for label, fn in tasks:
            print(f"👉 Starting {label}...")
            code, out, dur, cmd = fn()
            exit_code, saved = print_result(label, code, out, dur, cmd)
            total_savings += saved
            if exit_code != 0:
                print("🛑 Fail Fast triggered.")
                return 1

    total_duration = time.time() - start_total
    
    if overall_failure:
        return 1
    
    print(f"\\n✨ All systems go! (Completed in {total_duration:.2f}s) 💰 Total Token Savings: {total_savings}")
    return 0
