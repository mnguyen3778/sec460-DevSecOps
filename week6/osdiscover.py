#!/usr/bin/env python3
"""
osdiscover.py

Week 6 Assignment – OS Discovery using python3-nmap

This script reads a CSV file generated from scannet.py that contains
IP addresses and open ports. It performs OS detection using the
nmap_os_detection capability of python3-nmap and writes the results
to a new CSV file including the best OS guess.

Usage:
    sudo ./osdiscover.py scannet.csv osdiscover.csv

Note:
    This script must be run with sudo because OS detection requires
    raw socket access.
"""

import sys
import csv
import nmap


def detect_os(ip):
    """
    Perform OS detection on a single IP address.

    Parameters:
        ip (str): The IP address to scan.

    Returns:
        str: The best guess of the operating system, or "Unknown"
             if no OS match is found.
    """
    nm = nmap.PortScanner()

    try:
        nm.scan(ip, arguments='-O')
    except Exception:
        return "Unknown"

    if 'osmatch' in nm[ip] and len(nm[ip]['osmatch']) > 0:
        return nm[ip]['osmatch'][0]['name']

    return "Unknown"


def main():
    """
    Main execution function.

    Reads input CSV containing IP and open ports.
    Performs OS detection on each IP.
    Writes results to output CSV with columns:
        IP, Open Ports, OS
    """
    if len(sys.argv) != 3:
        print("Usage: sudo ./osdiscover.py <input.csv> <output.csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write header
        writer.writerow(["IP", "Open Ports", "OS"])

        next(reader)  # Skip header from scannet.csv

        for row in reader:
            ip = row[0]
            open_ports = row[1]

            print(f"Detecting OS for {ip}...")

            os_guess = detect_os(ip)

            writer.writerow([ip, open_ports, os_guess])

    print(f"Scan complete. Results written to {output_file}")


if __name__ == "__main__":
    main()

