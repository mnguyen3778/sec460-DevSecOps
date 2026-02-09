#!/usr/bin/env python3
"""
iphones.py

Scan a dhcpd log file and print all unique iPhone MAC addresses
that successfully received a DHCPACK. Also prints a total count.

Usage:
    ./iphones.py <dhcpd.log>
"""

import sys
import re


def find_iphone_macs(filename):
    """
    Parse the dhcpd log file and return a set of unique iPhone MAC addresses.

    A device is considered:
    - Connected if it received a DHCPACK
    - An iPhone if the vendor string contains 'iphone' (case-insensitive)

    Args:
        filename (str): Path to dhcpd.log

    Returns:
        set: Unique MAC addresses of iPhones
    """
    iphone_macs = set()

    # Example DHCPACK line contains:
    # DHCPACK on <ip> to <mac> (<hostname>) via <interface>
    mac_regex = re.compile(
        r"DHCPACK.*?to\s+([0-9a-f:]{17}).*?(iphone)",
        re.IGNORECASE
    )

    try:
        with open(filename, "r", errors="ignore") as f:
            for line in f:
                match = mac_regex.search(line)
                if match:
                    mac = match.group(1)
                    iphone_macs.add(mac)
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        sys.exit(1)

    return iphone_macs


def main():
    if len(sys.argv) != 2:
        print("Usage: ./iphones.py <dhcpd.log>")
        sys.exit(1)

    filename = sys.argv[1]
    iphones = find_iphone_macs(filename)

    for mac in sorted(iphones):
        print(mac)

    print(f"Count = {len(iphones)}")


if __name__ == "__main__":
    main()

