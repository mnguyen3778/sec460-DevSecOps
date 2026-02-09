#!/usr/bin/env python3
"""
pingany.py

This script accepts a single command-line argument that can be either:
- a filename containing IP addresses or domain names (one per line), OR
- a single IP address or domain name.

If the argument is a file, each entry in the file is pinged.
If the argument is not a file, it is treated as a single IP or domain.

The script uses the pinglib library to perform all ping operations.
"""

import sys
import os
import pinglib


def main():
    """
    Main function that parses command-line arguments, determines whether
    the input is a file or a single host, and prints ping results.
    """
    if len(sys.argv) != 2:
        print("Usage: pingany.py <filename | IP | Domainname>")
        sys.exit(1)

    target = sys.argv[1]

    # Print header (always printed once)
    print("IP, TimeToPing (ms)")

    # Case 1: argument is a file in the current directory
    if os.path.isfile(target):
        try:
            with open(target, "r") as infile:
                for line in infile:
                    host = line.strip()
                    if not host:
                        continue

                    result = pinglib.pingthis(host)
                    if result[1] == "NotFound":
                        print(f"{result[0]},NotFound")
                    else:
                        print(f"{result[0]},{float(result[1]):.2f}")
        except IOError:
            print("NotFound")

    # Case 2: argument is a single IP or domain
    else:
        result = pinglib.pingthis(target)
        if result[1] == "NotFound":
            print(f"{result[0]},NotFound")
        else:
            print(f"{result[0]},{float(result[1]):.2f}")


if __name__ == "__main__":
    main()

