#!/usr/bin/env python3
"""
pingcsv.py

This script accepts one required command-line argument and one optional argument.

Usage:
    pingcsv.py <filename | IP | Domainname> [output.csv]

Behavior:
- If the first argument is a file, each line is pinged.
- If the first argument is not a file, it is treated as a single IP or domain.
- Output is always printed to the screen.
- If a second argument is provided, results are also written to a CSV file.

The script uses the pinglib library for all ping operations.
"""

import sys
import os
import csv
import pinglib


def main():
    """
    Main function to process command-line arguments, perform pings,
    print results, and optionally write results to a CSV file.
    """
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: pingcsv.py <filename | IP | Domainname> [output.csv]")
        sys.exit(1)

    input_target = sys.argv[1]
    output_csv = sys.argv[2] if len(sys.argv) == 3 else None

    results = []

    # Print header (always)
    print("IP, TimeToPing (ms)")

    # Case 1: input is a file
    if os.path.isfile(input_target):
        try:
            with open(input_target, "r") as infile:
                for line in infile:
                    host = line.strip()
                    if not host:
                        continue

                    result = pinglib.pingthis(host)
                    if result[1] == "NotFound":
                        print(f"{result[0]},NotFound")
                        results.append([result[0], "NotFound"])
                    else:
                        time_ms = f"{float(result[1]):.2f}"
                        print(f"{result[0]},{time_ms}")
                        results.append([result[0], time_ms])
        except IOError:
            print("NotFound")

    # Case 2: input is a single IP or domain
    else:
        result = pinglib.pingthis(input_target)
        if result[1] == "NotFound":
            print(f"{result[0]},NotFound")
            results.append([result[0], "NotFound"])
        else:
            time_ms = f"{float(result[1]):.2f}"
            print(f"{result[0]},{time_ms}")
            results.append([result[0], time_ms])

    # Optional CSV output
    if output_csv:
        with open(output_csv, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["IP", "TimeToPing (ms)"])
            writer.writerows(results)


if __name__ == "__main__":
    main()

