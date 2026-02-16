#!/usr/bin/env python3

import sys
import csv
import nmap3

def main():

    if len(sys.argv) != 3:
        print("Usage: ./scannet.py <subnet> <outputfile>")
        sys.exit(1)

    subnet = sys.argv[1]
    outfile = sys.argv[2]

    print(f"Starting SYN scan on {subnet} (this may take several minutes)...")

    scanner = nmap3.NmapScanTechniques()

    # SYN scan
    results = scanner.nmap_syn_scan(subnet)

    with open(outfile, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IP", "Open Ports"])

        # python3-nmap returns dict keyed by IP
        for host in results:

            # Skip metadata entries
            if host == "stats":
                continue

            open_ports = []

            host_data = results.get(host, {})

            if isinstance(host_data, dict):

                ports = host_data.get("ports", [])

                for port in ports:
                    if port.get("state") == "open":
                        open_ports.append(str(port.get("portid")))

            if open_ports:
                writer.writerow([host, " ".join(open_ports)])

    print(f"Scan complete. Results written to {outfile}")

if __name__ == "__main__":
    main()

