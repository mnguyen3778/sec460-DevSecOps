#!/usr/bin/env python3
"""
mac-count.py

Analyze a DHCP log file to identify MAC address and IP address pairs
and count the number of DHCPACK messages associated with each pair.

This script outputs:
1. mac-count.csv      -> All MAC/IP pairs with ACK counts
2. problem-macs.csv   -> Top two MAC/IP pairs generating the most ACKs
                          (potential DOS offenders)

Usage:
    mac-count.py <filename>
"""

import sys
import re
import csv
from collections import defaultdict


def parse_dhcp_log(filename):
    """
    Parse the DHCP log file and count DHCPACK occurrences
    per (MAC address, IP address) pair.

    Args:
        filename (str): Path to the DHCP log file.

    Returns:
        dict: Dictionary with (mac, ip) as keys and ACK counts as values.
    """
    pattern = re.compile(
        r"DHCPACK.*?(\d+\.\d+\.\d+\.\d+).*?([0-9a-fA-F:]{17})"
    )

    counts = defaultdict(int)

    try:
        with open(filename, "r") as logfile:
            for line in logfile:
                match = pattern.search(line)
                if match:
                    ip = match.group(1)
                    mac = match.group(2)
                    counts[(mac, ip)] += 1
    except FileNotFoundError:
        print(f"Error: cannot open {filename}")
        sys.exit(1)

    return counts


def write_mac_count_csv(counts):
    """
    Write all MAC/IP ACK counts to mac-count.csv.

    Args:
        counts (dict): Dictionary of (mac, ip) -> ACK count.
    """
    with open("mac-count.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Macs", "IPs", "ACKs"])
        for (mac, ip), ack_count in counts.items():
            writer.writerow([mac, ip, ack_count])


def write_problem_macs_csv(counts):
    """
    Identify the top two MAC/IP pairs with the highest ACK counts
    and write them to problem-macs.csv.

    Args:
        counts (dict): Dictionary of (mac, ip) -> ACK count.
    """
    top_two = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:2]

    with open("problem-macs.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Macs", "IPs", "ACKs"])
        for (mac, ip), ack_count in top_two:
            writer.writerow([mac, ip, ack_count])


def main():
    """
    Main program entry point.
    Validates arguments, processes the log file,
    and generates the required CSV output files.
    """
    if len(sys.argv) != 2:
        print("Usage: mac-count.py <filename>")
        sys.exit(1)

    logfile = sys.argv[1]

    counts = parse_dhcp_log(logfile)
    write_mac_count_csv(counts)
    write_problem_macs_csv(counts)


if __name__ == "__main__":
    main()

