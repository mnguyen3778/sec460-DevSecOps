#!/usr/bin/env python3

"""
scanlocation.py

Reads a CSV file containing DNS names and IP addresses, queries the ip-api.com
JSON API for geographic and ISP information, and writes the enriched data
to a new CSV file.

Usage:
    ./scanlocation.py scandns.csv scanlocation.csv

This script should NOT be run as root.
"""

import sys
import csv
import requests


def get_location(ip):
    """
    Query the ip-api.com JSON API for geolocation data.

    Args:
        ip (str): IPv4 address to query.

    Returns:
        tuple: (country, regionName, city, zip, isp)
               Returns "Unknown" values if lookup fails.
    """
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("status") == "success":
            return (
                data.get("country", "Unknown"),
                data.get("regionName", "Unknown"),
                data.get("city", "Unknown"),
                data.get("zip", "Unknown"),
                data.get("isp", "Unknown"),
            )
        else:
            return ("Unknown", "Unknown", "Unknown", "Unknown", "Unknown")

    except Exception:
        return ("Unknown", "Unknown", "Unknown", "Unknown", "Unknown")


def main():
    """
    Main execution function.

    - Reads input CSV (DNS,IP)
    - Queries location data for each IP
    - Writes output CSV with added columns:
      DNS,IP,Country,RegionName,City,Zipcode,ISP
    """
    if len(sys.argv) != 3:
        print("Usage: ./scanlocation.py input.csv output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, newline='') as infile, \
         open(output_file, 'w', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write header
        writer.writerow([
            "DNS", "IP",
            "Country", "RegionName",
            "City", "Zipcode", "ISP"
        ])

        next(reader)  # Skip header row

        for row in reader:
            if len(row) < 2:
                continue

            dns = row[0].strip()
            ip = row[1].strip()

            print(f"Looking up location for {ip}...")

            country, region, city, zipcode, isp = get_location(ip)

            writer.writerow([
                dns, ip,
                country, region,
                city, zipcode, isp
            ])

    print(f"Scan complete. Results written to {output_file}")


if __name__ == "__main__":
    main()

