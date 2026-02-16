#!/usr/bin/env python3

import sys
import csv
import nmap3

def main():
    if len(sys.argv) != 3:
        print("Usage: ./scandns.py <domain> <outputfile>")
        sys.exit(1)

    domain = sys.argv[1]
    outputfile = sys.argv[2]

    nmap = nmap3.Nmap()

    print(f"Running DNS brute scan on {domain}...")

    results = nmap.nmap_dns_brute_script(domain)

    with open(outputfile, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["DNS", "IP"])

        for host in results:
            if "hostname" in host and "address" in host:
                ip = host["address"]

                # Ignore IPv6
                if ":" in ip:
                    continue

                writer.writerow([host["hostname"], ip])

    print(f"Scan complete. Results written to {outputfile}")

if __name__ == "__main__":
    main()

