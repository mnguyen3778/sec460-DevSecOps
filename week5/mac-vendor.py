#!/usr/bin/env python3
"""
mac-vendor.py

Given a list of IP addresses and a DHCP log file, this script:
1. Finds the MAC address associated with each IP in the DHCP log
2. Queries the macvendors.com API to identify the vendor
3. Writes results to mac-vendor.csv

Usage:
    mac-vendor.py <IPs.txt> <dhcpd.log>
"""

import sys
import re
import csv
import urllib.request


API_URL = "https://api.macvendors.com/"


def load_ips(filename):
    """Load IP addresses from a file into a list."""
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]


def find_mac_for_ip(ip, dhcp_file):
    """
    Search the DHCP log for a MAC address associated with an IP.
    Returns the MAC address or None.
    """
    pattern = re.compile(rf"({ip}).*?([0-9a-f]{{2}}(:[0-9a-f]{{2}}){{5}})", re.IGNORECASE)

    with open(dhcp_file, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                return match.group(2).lower()

    return None


def lookup_vendor(mac):
    """
    Query macvendors.com API for vendor name.
    Returns vendor string or 'Unknown'.
    """
    try:
        with urllib.request.urlopen(API_URL + mac, timeout=5) as response:
            return response.read().decode().strip()
    except Exception:
        return "Unknown"


def main():
    """Main execution logic."""
    if len(sys.argv) != 3:
        print("Usage: mac-vendor.py <IPs.txt> <dhcpd.log>")
        sys.exit(1)

    ip_file = sys.argv[1]
    dhcp_file = sys.argv[2]

    ips = load_ips(ip_file)

    with open("mac-vendor.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IP", "Mac Address", "Vendor"])

        for ip in ips:
            mac = find_mac_for_ip(ip, dhcp_file)
            if mac:
                vendor = lookup_vendor(mac)
                writer.writerow([ip, mac, vendor])


if __name__ == "__main__":
    main()

