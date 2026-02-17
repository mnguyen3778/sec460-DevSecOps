#!/usr/bin/env python3
"""
scannet.py

Performs a SYN scan against a target network using python3-nmap.
Outputs a CSV file containing each discovered IP address and its open ports.

Usage:
    ./scannet.py <network_range> <output_csv>

Example:
    ./scannet.py 134.39.81.0/24 scannet.csv

Do NOT run this script as root unless required by your environment.
"""

import sys
import csv
import nmap


def syn_scan(network_range):
    """
    Perform a SYN scan against the provided network range.

    Args:
        network_range (str): Network in CIDR notation (e.g., 134.39.81.0/24)

    Returns:
        dict: Dictionary keyed by IP address containing open TCP ports
    """
    nm = nmap.PortScanner()

    print(f"Scanning network {network_range} with SYN scan...")

    nm.scan(hosts=network_range, arguments='-sS')

    results = {}

    for host in nm.all_hosts():
        open_ports = []

        if 'tcp' in nm[host]:
            for port in nm[host]['tcp']:
                if nm[host]['tcp'][port]['state'] == 'open':
                    open_ports.append(str(port))

        results[host] = " ".join(open_ports)

    return results


def write_csv(results, output_file):
    """
    Write scan results to a CSV file.

    Args:
        results (dict): Dictionary of IP addresses and open ports
        output_file (str): Name of CSV file to write
    """
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["IP", "Open Ports"])

        for ip, ports in results.items():
            writer.writerow([ip, ports])

    print(f"Scan complete. Results written to {output_file}")


def main():
    """
    Main entry point for the script.
    Validates arguments, runs scan, and writes output.
    """
    if len(sys.argv) != 3:
        print("Usage: ./scannet.py <network_range> <output_csv>")
        sys.exit(1)

    network_range = sys.argv[1]
    output_file = sys.argv[2]

    results = syn_scan(network_range)
    write_csv(results, output_file)


if __name__ == "__main__":
    main()

