import sys
import os
import re
from datetime import datetime

def main():
    # Join command line arguments into a single string and lowercase it for case-insensitive matching
    args = " ".join(sys.argv[1:])
    args_lower = args.lower()

    # Log all commands received, for debugging
    log_entry = f"[{datetime.now()}] Args: {args}\n"
    try:
        with open(".claude/hooks/hook_debug.log", "a") as f:
            f.write(log_entry)
    except Exception:
        pass

    CRITICAL_FILES = [
        "spendly.db",
        ".env",
        "CLAUDE.md",
        "requirements.txt"
    ]

    deletion_pattern = re.compile(r'\b(rm|delete|unlink)\b')

    if deletion_pattern.search(args_lower):
        for critical_file in CRITICAL_FILES:
            # Lowercase match critical file name
            if re.search(rf'\b{re.escape(critical_file.lower())}\b', args_lower):
                # Log the blocked attempt
                try:
                    with open(".claude/hooks/hook_debug.log", "a") as f:
                        f.write(f"[{datetime.now()}] ❌ BLOCKED: {critical_file}\n")
                except Exception:
                    pass

                print(f"❌ ERROR: Deletion of critical file '{critical_file}' is blocked by hook!")
                sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
