#!/usr/bin/env python3
"""
mac-vendor.py

Given a list of IP addresses and a DHCP log file:
1. Find the MAC address associated with each IP
2. Query macvendors.com to identify the vendor
3. Write results to mac-vendor.csv

Usage:
    ./mac-vendor.py IPs.txt dhcpd.log
"""

import sys
import re
import csv
import urllib.request
import urllib.error
import time

API_URL = "https://api.macvendors.com/"

def load_ips(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def find_mac_for_ip(ip, dhcp_file):
    # Matches MAC address after the IP somewhere on the line
    pattern = re.compile(rf"{re.escape(ip)}.*?([0-9a-f]{{2}}(?::[0-9a-f]{{2}}){{5}})", re.IGNORECASE)

    with open(dhcp_file, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                return match.group(1).lower()

    return None

def lookup_vendor(mac):
    try:
        with urllib.request.urlopen(API_URL + mac, timeout=5) as response:
            vendor = response.read().decode().strip()
            return vendor if vendor else "Unknown"
    except urllib.error.HTTPError as e:
        if e.code == 429:
            # Rate limited — wait once and retry
            time.sleep(1)
            try:
                with urllib.request.urlopen(API_URL + mac, timeout=5) as response:
                    return response.read().decode().strip()
            except Exception:
                return "Unknown"
        return "Unknown"
    except Exception:
        return "Unknown"

def main():
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
            else:
                writer.writerow([ip, "Unknown", "Unknown"])

if __name__ == "__main__":
    main()

