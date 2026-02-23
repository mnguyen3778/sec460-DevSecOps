#!/usr/bin/env python3
"""
dump-table.py

Connects to an encrypted SQLCipher database and
outputs the devices table either to the screen,
a JSON file, or a CSV file.

Usage:
    dump-table.py screen
    dump-table.py json output.json
    dump-table.py csv output.csv


"""

import sys
import sqlcipher3
import json
import csv

database = 'etest.db'
table = 'devices'
password = 'MyStrongPassword123'


def main():
    """
    Handles database connection and output formatting.
    """

    if len(sys.argv) < 2:
        print("Usage: dump-table.py <screen|json|csv> <outputfile>")
        sys.exit(1)

    mode = sys.argv[1]

    try:
        db = sqlcipher3.connect(database)
        cur = db.cursor()
        cur.execute(f'pragma key="{password}";')

        result = cur.execute(f"SELECT * FROM {table};")
        rows = result.fetchall()

        headers = [description[0] for description in result.description]

        if mode == "screen":
            print(headers)
            for row in rows:
                print(row)

        elif mode == "json":
            if len(sys.argv) != 3:
                print("JSON mode requires output filename.")
                sys.exit(1)

            output_file = sys.argv[2]
            data = [dict(zip(headers, row)) for row in rows]

            with open(output_file, "w") as f:
                json.dump(data, f, indent=4)

        elif mode == "csv":
            if len(sys.argv) != 3:
                print("CSV mode requires output filename.")
                sys.exit(1)

            output_file = sys.argv[2]

            with open(output_file, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)

        else:
            print("Invalid mode. Use screen, json, or csv.")

        db.close()

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
