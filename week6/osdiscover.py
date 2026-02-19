#!/usr/bin/env python3
"""
osdiscover.py

Performs OS detection on hosts listed in an input CSV file
using the nmap3 library.

Reads a CSV file containing IP addresses (one per line or in first column)
and outputs a CSV file with detected OS information.

Usage:
    ./osdiscover.py <input_csv> <output_csv>

Example:
    ./osdiscover.py scannet.csv osdiscover.csv
"""

import sys
import csv
import nmap3


def detect_os(ip_address):
    """
    Perform OS detection on a single IP address.

    Args:
        ip_address (str): Target IPv4 address.

    Returns:
        str: Best guess OS name or "Unknown"
    """
    nmap = nmap3.Nmap()

    try:
        result = nmap.nmap_os_detection(ip_address)

        if ip_address in result and "osmatch" in result[ip_address]:
            matches = result[ip_address]["osmatch"]
            if matches:
                return matches[0]["name"]

        return "Unknown"

    except Exception:
        return "Unknown"


def main():
    """
    Main function:
    - Validates arguments
    - Reads input CSV
    - Runs OS detection
    - Writes output CSV
    """
    if len(sys.argv) != 3:
        print("Usage: ./osdiscover.py <input_csv> <output_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        writer.writerow(["IP", "OS"])

        for row in reader:
            if not row:
                continue

            ip = row[0]

            # Skip header if present
            if ip.lower() == "ip":
                continue

            print(f"Detecting OS for {ip}...")
            os_name = detect_os(ip)

            writer.writerow([ip, os_name])

    print(f"Scan complete. Results written to {output_file}")


if __name__ == "__main__":
    main()

