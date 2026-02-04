#!/usr/bin/env python3

import csv
import sys


def read_users(input_file):
    """
    Reads users from a CSV file containing firstname, lastname.

    Args:
        input_file (str): Path to users.csv

    Returns:
        list: List of (firstname, lastname) tuples
    """
    users = []
    with open(input_file, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 2:
                continue
            users.append((row[0], row[1]))
    return users


def build_base_userid(firstname, lastname):
    """
    Builds the base userid using first initial + up to 7 chars of last name.

    Args:
        firstname (str)
        lastname (str)

    Returns:
        str: Base userid
    """
    return (firstname[0] + lastname[:7]).lower()


def generate_userid(base_id, counter_dict):
    """
    Appends a two-digit number to the base userid.

    Args:
        base_id (str)
        counter_dict (dict)

    Returns:
        str: Final userid
    """
    count = counter_dict.get(base_id, 0)
    counter_dict[base_id] = count + 1
    return f"{base_id}{count:02d}"


def write_userids(input_file, output_file):
    """
    Reads users from input CSV and writes firstname, lastname, userid
    to the output CSV file.

    Args:
        input_file (str)
        output_file (str)
    """
    users = read_users(input_file)
    counters = {}

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)

        # header row
        writer.writerow(["firstname", "lastname", "userid"])

        # data rows
        for firstname, lastname in users:
            base_id = build_base_userid(firstname, lastname)
            userid = generate_userid(base_id, counters)
            writer.writerow([firstname, lastname, userid])


def main():
    """
    Command-line entry point.
    """
    if len(sys.argv) != 2:
        print("Usage: ./userids.py users.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = "userids.csv"

    write_userids(input_file, output_file)


if __name__ == "__main__":
    main()
