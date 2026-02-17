#!/usr/bin/env python3
"""
scandns.py

Week 6 – Network Scanning

This script performs a DNS brute-force scan against a specified domain
using the python3-nmap library. It retrieves discovered DNS hostnames
and their associated IPv4 addresses, then writes the results to a CSV file.

IPv6 addresses are ignored as required by the assignment.

Usage:
    ./scandns.py <domain> <outputfile>

Example:
    ./scandns.py bellevuecollege.edu scandns.csv

Output CSV Format:
    DNS,IP
    owa.bellevuecollege.edu,134.39.81.247
"""

import sys
import csv
import nmap3


def main():
    """
    Main execution function.

    Validates command-line arguments, performs a DNS brute-force scan
    using nmap3, filters out IPv6 results, and writes hostname/IP
    pairs to the specified CSV output file.
    """

    # Validate arguments
    if len(sys.argv) != 3:
        print("Usage: ./scandns.py <domain> <outputfile>")
        sys.exit(1)

    domain = sys.argv[1]
    outputfile = sys.argv[2]

    print(f"Running DNS brute scan on {domain}...")

    # Create Nmap object
    nm = nmap3.Nmap()

    # Perform DNS brute script scan
    results = nm.nmap_dns_brute_script(domain)

    # Write results to CSV
    with open(outputfile, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["DNS", "IP"])

        for host in results:
            if "hostname" in host and "address" in host:
                ip = host["address"]

                # Ignore IPv6 addresses
                if ":" in ip:
                    continue

                writer.writerow([host["hostname"], ip])

    print(f"Scan complete. Results written to {outputfile}")


if __name__ == "__main__":
    main()

