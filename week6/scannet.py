#!/usr/bin/env python3
"""
scannet.py

Performs a SYN scan against a target network using the nmap3 library.
Outputs a CSV file containing each discovered IPv4 address and its open TCP ports.

Usage:
    ./scannet.py <network_range> <output_csv>

Example:
    ./scannet.py 134.39.81.0/24 scannet.csv
"""

import sys
import csv
import nmap3


def syn_scan(network_range):
    """
    Perform a SYN scan against the provided network range using nmap3.

    Args:
        network_range (str): Network in CIDR notation (e.g., 134.39.81.0/24)

    Returns:
        dict: Dictionary keyed by IP address containing open TCP ports.
    """
    nmap = nmap3.Nmap()

    print(f"Scanning network {network_range} with SYN scan...")

    results = nmap.scan_top_ports(network_range)

    scan_data = {}

    for host in results:
        if host == "stats":
            continue

        open_ports = []

        if "ports" in results[host]:
            for port in results[host]["ports"]:
                if port["state"] == "open":
                    open_ports.append(str(port["portid"]))

        if open_ports:
            scan_data[host] = open_ports

    return scan_data


def main():
    """
    Main execution function.
    Validates arguments, performs scan, and writes results to CSV.
    """
    if len(sys.argv) != 3:
        print("Usage: ./scannet.py <network_range> <output_csv>")
        sys.exit(1)

    network_range = sys.argv[1]
    output_file = sys.argv[2]

    scan_results = syn_scan(network_range)

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["IP Address", "Open Ports"])

        for ip in scan_results:
            ports = ",".join(scan_results[ip])
            writer.writerow([ip, ports])

    print(f"Scan complete. Results written to {output_file}")


if __name__ == "__main__":
    main()

