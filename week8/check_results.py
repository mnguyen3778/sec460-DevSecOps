#!/usr/bin/env python3
"""
check_results.py

Week 8 - Monitoring Results Viewer

Reads the local syslog and prints monitoring check entries.
Supports filtering for all checks, warnings only, or errors only.
"""

import sys

SYSLOG_PATH = "/var/log/syslog"


def matches_filter(line, option):
    """
    Determine whether a syslog line matches the selected filter.
    """

    # Only process monitoring check entries
    if "Check=" not in line:
        return False

    if option == "all":
        return True

    if option == "warn" and "Result=WARNING" in line:
        return True

    if option == "error" and "Result=ERROR" in line:
        return True

    return False


def main():
    """
    Parse command line arguments and display filtered
    monitoring check results from syslog.
    """

    if len(sys.argv) != 2:
        print("Usage: ./check_results.py <all|warn|error>")
        sys.exit(1)

    option = sys.argv[1]

    if option not in ["all", "warn", "error"]:
        print("Invalid option.")
        sys.exit(1)

    try:
        with open(SYSLOG_PATH, "r") as logfile:
            for line in logfile:
                if matches_filter(line, option):
                    print(line.strip())

    except PermissionError:
        print("Permission denied reading syslog.")
        sys.exit(1)


if __name__ == "__main__":
    main()
