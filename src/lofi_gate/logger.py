import os
import datetime
import threading

# --- Constants ---

# The log file is stored in the Project Root to be easily found by Agents.
LOG_FILENAME = "verification_history.md"

# Max lines to keep in the log file to prevent infinite growth.
MAX_LOG_LINES = 200

# Global Lock for thread-safety
log_lock = threading.Lock()

def get_log_path(project_root=None):
    """
    Determines the absolute path to the log file.
    If project_root is provided, uses that. Otherwise tries to find CWD.
    """
    if project_root:
        return os.path.join(project_root, LOG_FILENAME)
    return os.path.join(os.getcwd(), LOG_FILENAME)

def parse_footer(lines):
    """
    Parses the "Sticky Footer" from the log file to preserve stats.
    """
    size = 0
    savings = 0
    clean_lines = []
    footer_marker_size = "**Total Token Size:**"
    
    for line in lines:
        if footer_marker_size in line:
            try:
                content = line.strip().replace("> ", "")
                parts = content.split("|")
                p0 = parts[0].split(":")[-1].strip().replace("*", "")
                size = int(p0)
                if len(parts) > 1:
                    p1 = parts[1].split(":")[-1].strip().replace("*", "")
                    savings = int(p1)
            except: 
                pass
        else:
            clean_lines.append(line)
            
    return clean_lines, size, savings

def log_to_history(label, status, message, tokens_used=0, tokens_saved=0, duration=0, command_context="", error_content=None, project_root=None):
    """
    Writes a structured entry to the verification_history.md log.
    """
    log_path = get_log_path(project_root)
    if not log_path: return

    with log_lock:
        lines = []
        if os.path.exists(log_path):
            try:
                with open(log_path, 'r', encoding='utf-8') as f: lines = f.readlines()
            except: pass

        lines, current_size, current_savings = parse_footer(lines)
        
        SAFE_LOG_LINES = MAX_LOG_LINES * 2
        if len(lines) > SAFE_LOG_LINES:
            lines = lines[-SAFE_LOG_LINES:]
            if not lines[0].startswith("\n..."):
                 lines.insert(0, f"\n... (Log truncated to last {SAFE_LOG_LINES} lines) ...\n")

        current_size += tokens_used
        current_savings += tokens_saved

        metrics_msg = f"(total token size: {tokens_used}) (tokens truncated: {tokens_saved})"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        icon = "✅" if status == "PASS" else "❌"
        duration_str = f"({duration:.2f}s)" if duration > 0 else ""
        context_str = f"[{command_context}]" if command_context else "[Internal]"
        
        entry = f"- **[{timestamp}]** {context_str} {icon} **{label}**: {status} {duration_str} {metrics_msg}\n"
        lines.append(entry)
        
        if error_content:
            lines.append("  <details>\n")
            lines.append("  <summary>🔍 View Truncated Error</summary>\n\n")
            lines.append("  ```text\n")
            for line in error_content.splitlines():
                lines.append(f"  {line}\n")
            lines.append("  ```\n")
            lines.append("  </details>\n")

        footer = f"\n> 📊 **Total Token Size:** {current_size} | 💰 **Total Token Savings:** {current_savings}\n"
        lines.append(footer)
        
        try:
            with open(log_path, 'w', encoding='utf-8') as f: f.writelines(lines)
        except: pass
