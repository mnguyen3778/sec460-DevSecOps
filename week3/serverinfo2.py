#!/usr/bin/env python3
"""
serverinfo2.py

Outputs server information in screen.
Uses serverinfo.py as an imported module.
"""

import sys
import csv
import json
import serverinfo


def collect_data():
    """
    Collects server information using functions imported
    from the serverinfo module and returns it as a dictionary.
    """
    return {
        "Hostname": serverinfo.get_hostname(),
        "CPU (count)": serverinfo.get_cpu_count(),
        "RAM (GB)": serverinfo.get_ram_gb(),
        "OSType": serverinfo.get_os_type(),
        "OSVersion": serverinfo.get_os_version(),
        "OS disk size (GB)": serverinfo.get_disk_size(),
        "OS disk free (GB)": serverinfo.get_disk_free(),
        "Primary IP": serverinfo.get_primary_ip(),
        "Primary Mac": serverinfo.get_primary_mac()
    }


def output_screen(data):
    """
    Prints server information to the screen.
    """
    for key, value in data.items():
        print(f"{key}: {value}")


def output_csv(data):
    """
    Writes server information to a CSV file named serverinfo.csv.
    One row per server, one column per attribute.
    """
    with open("serverinfo.csv", "w", newline="") as f:
        writer = csv.writer(f)

        # header (MUST match dictionary keys exactly)
        writer.writerow([
            "Hostname",
            "CPU (count)",
            "RAM (GB)",
            "OSType",
            "OSVersion",
            "OS disk size (GB)",
            "OS disk free (GB)",
            "Primary IP",
            "Primary Mac"
        ])

        # single server row
        writer.writerow([
            data["Hostname"],
            data["CPU (count)"],
            data["RAM (GB)"],
            data["OSType"],
            data["OSVersion"],
            data["OS disk size (GB)"],
            data["OS disk free (GB)"],
            data["Primary IP"],
            data["Primary Mac"]
        ])


def output_json(data):
    """
    Writes server information to a JSON file named serverinfo.json.
    """
    with open("serverinfo.json", "w") as f:
        json.dump(data, f, indent=4)


def usage():
    """
    Displays usage instructions and exits the program.
    """
    print("Usage: serverinfo2.py [screen|csv|json]")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()

    mode = sys.argv[1].lower()
    data = collect_data()

    if mode == "screen":
        output_screen(data)
    elif mode == "csv":
        output_csv(data)
    elif mode == "json":
        output_json(data)
    else:
        usage()

