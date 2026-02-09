#!/usr/bin/env python3
"""
pingfile.py

Reads a file of IPs or domain names and pings each one using pinglib.
Prints results in CSV format.
"""

import sys
import os
import pinglib


def main():
    """
    Main entry point.
    Expects one filename argument containing IPs or domain names.
    """
    if len(sys.argv) != 2:
        print("Usage: pingfile.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print(f"Error: {filename} not found")
        sys.exit(1)

    print("IP, TimeToPing (ms)")

    with open(filename, "r") as f:
        for line in f:
            target = line.strip()
            if not target:
                continue

            result = pinglib.pingthis(target)

            if result[1] == "NotFound":
                print(f"{result[0]},NotFound")
            else:
                print(f"{result[0]},{float(result[1]):.2f}")


if __name__ == "__main__":
    main()

