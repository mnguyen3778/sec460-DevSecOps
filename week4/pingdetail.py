#!/usr/bin/env python3
"""
pingdetail.py

Extra credit script that extends pingcsv behavior by displaying
additional network details:
- Pinged name
- Reverse DNS name (if available)
- IP address
- Ping time (ms) or NotFound

This script DOES NOT modify earlier assignments.
"""

import sys
import os
import csv
import socket

import pinglib   # uses your existing pinglib.py


def reverse_lookup(ip):
    """
    Attempt reverse DNS lookup on an IP address.

    Args:
        ip (str): IP address

    Returns:
        str: DNS name or 'Unknown'
    """
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "Unknown"


def resolve_ip(host):
    """
    Resolve a hostname to an IP address.

    Args:
        host (str): Hostname or IP

    Returns:
        str: IP address or 'Unknown'
    """
    try:
        return socket.gethostbyname(host)
    except Exception:
        return "Unknown"


def process_target(target):
    """
    Ping a single target and return detailed info.

    Returns:
        list: [pinged_name, dns_name, ip_address, time_or_NotFound]
    """
    result = pinglib.pingthis(target)

    pinged_name = target

    # If ping failed
    if result[1] == "NotFound":
        return [pinged_name, "Unknown", "Unknown", "NotFound"]

    ip_address = resolve_ip(target)
    dns_name = reverse_lookup(ip_address) if ip_address != "Unknown" else "Unknown"

    return [pinged_name, dns_name, ip_address, result[1]]


def main():
    """
    Command-line entry point.
    """
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: pingdetail.py <filename | IP | Domainname> [output.csv]")
        sys.exit(1)

    input_arg = sys.argv[1]
    output_csv = sys.argv[2] if len(sys.argv) == 3 else None

    results = []

    # Header
    header = ["Pinged IP/Name", "DNS", "IP", "TimeToPing (ms)"]
    print(",".join(header))

    # If input is a file
    if os.path.isfile(input_arg):
        with open(input_arg, "r") as f:
            for line in f:
                target = line.strip()
                if not target:
                    continue
                row = process_target(target)
                results.append(row)
                print(",".join(row))
    else:
        # Single host
        row = process_target(input_arg)
        results.append(row)
        print(",".join(row))

    # Optional CSV output
    if output_csv:
        with open(output_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(results)


if __name__ == "__main__":
    main()

