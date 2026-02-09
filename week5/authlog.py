#!/usr/bin/env python3
"""
authlog.py

Scan an auth.log file for failed SSH login attempts and
output a count of source IP addresses attempting to log in.

Usage:
    authlog.py <auth.log>
"""

import sys
import re
from collections import defaultdict


FAIL_PATTERNS = [
    "Failed password",
    "Invalid user",
    "authentication failure",
    "PAM authentication error"
]

IP_REGEX = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3})")


def main():
    """Main program logic."""
    if len(sys.argv) != 2:
        print("Usage: authlog.py <auth.log>")
        sys.exit(1)

    logfile = sys.argv[1]
    counts = defaultdict(int)

    try:
        with open(logfile, "r") as f:
            for line in f:
                if any(pattern in line for pattern in FAIL_PATTERNS):
                    match = IP_REGEX.search(line)
                    if match:
                        ip = match.group(1)
                        counts[ip] += 1
    except FileNotFoundError:
        print(f"Error: cannot open {logfile}")
        sys.exit(1)

    for ip, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{ip}, {count}")


if __name__ == "__main__":
    main()

