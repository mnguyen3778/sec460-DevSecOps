#!/usr/bin/env python3

import sys
import csv
import nmap3

def get_best_os(os_results):
    """
    Takes list returned from nmap_os_detection()
    Returns best guess OS string
    """
    if not isinstance(os_results, list) or len(os_results) == 0:
        return "Unknown"

    best_guess = None
    highest_accuracy = -1

    for entry in os_results:
        try:
            accuracy = int(entry.get("accuracy", 0))
            name = entry.get("name", "Unknown")

            if accuracy > highest_accuracy:
                highest_accuracy = accuracy
                best_guess = name
        except:
            continue

    return best_guess if best_guess else "Unknown"


def main():
    if len(sys.argv) != 3:
        print("Usage: sudo ./osdiscover.py input.csv output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    nmap = nmap3.Nmap()

    with open(input_file, newline="") as infile, \
         open(output_file, "w", newline="") as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)  # Skip header
        writer.writerow(["IP", "Open Ports", "OS"])

        for row in reader:
            if len(row) < 2:
                continue

            ip = row[0]
            ports = row[1]

            print(f"Detecting OS for {ip}...")

            try:
                result = nmap.nmap_os_detection(ip)
                best_os = get_best_os(result)
            except:
                best_os = "ScanError"

            writer.writerow([ip, ports, best_os])

    print(f"Scan complete. Results written to {output_file}")


if __name__ == "__main__":
    main()

