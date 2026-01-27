#!/usr/bin/env python3
import csv


def read_users(filename):
    """
    Reads a CSV file containing firstname, lastname records.

    Args:
        filename (str): Path to the input CSV file.

    Returns:
        list: A list of (firstname, lastname) tuples.
    """
    users = []
    with open(filename, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                users.append((row[0].strip(), row[1].strip()))
    return users


def build_base_userid(firstname, lastname):
    """
    Builds the base userid using:
    first up to 5 letters of the lastname +
    first up to 3 letters of the firstname.

    All characters are lowercase.

    Args:
        firstname (str): User's first name.
        lastname (str): User's last name.

    Returns:
        str: Base userid without the numeric suffix.
    """
    return (lastname[:5] + firstname[:3]).lower()


def generate_userid(base_id, counter_dict):
    """
    Appends a two-digit number to the base userid.

    Uses a dictionary to track how many times the base
    userid has already been used.

    Args:
        base_id (str): Base userid (first 8 characters).
        counter_dict (dict): Dictionary tracking counts.

    Returns:
        str: Final userid with numeric suffix.
    """
    count = counter_dict.get(base_id, 0)
    counter_dict[base_id] = count + 1
    return f"{base_id}{count:02d}"


def write_userids(input_file, output_file):
    """
    Reads users from the input CSV file and writes
    firstname, lastname, userid to the output CSV file.

    Args:
        input_file (str): Path to users.csv.
        output_file (str): Path to userids.csv.
    """
    users = read_users(input_file)
    counters = {}

    with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)

    # write header row (required)
    writer.writerow(["firstname", "lastname", "userid"])

    # write data rows
    for firstname, lastname in users:
        base_id = build_base_userid(firstname, lastname)
        userid = generate_userid(base_id, counters)
        writer.writerow([firstname, lastname, userid])



def main():
    """
    Main program execution.
    """
    write_userids("users.csv", "userids.csv")


if __name__ == "__main__":
    main()

