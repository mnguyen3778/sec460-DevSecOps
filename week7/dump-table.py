#!/usr/bin/env python3

# -------------------------------
# Initial variables and imports
# -------------------------------

import sys
import json
import csv
import sqlcipher3

database = 'etest.db'
table = 'devices'
password = 'MyStrongPassword123'


# -------------------------------
# Main
# -------------------------------

def usage():
    print("Usage:")
    print("  dump-table.py screen")
    print("  dump-table.py json <outputfile>")
    print("  dump-table.py csv <outputfile>")
    sys.exit(1)


if len(sys.argv) < 2:
    usage()

mode = sys.argv[1]

if mode not in ['screen', 'json', 'csv']:
    usage()

if mode in ['json', 'csv'] and len(sys.argv) != 3:
    usage()

outputfile = None
if len(sys.argv) == 3:
    outputfile = sys.argv[2]

try:
    db = sqlcipher3.connect(database)
    cur = db.cursor()
    cur.execute(f'pragma key="{password}";')

    result = cur.execute(f"select * from {table};")
    rows = result.fetchall()

    columns = [description[0] for description in cur.description]

    if mode == 'screen':
        print(columns)
        for row in rows:
            print(row)

    elif mode == 'json':
        data = []
        for row in rows:
            data.append(dict(zip(columns, row)))

        with open(outputfile, 'w') as f:
            json.dump(data, f, indent=4)

    elif mode == 'csv':
        with open(outputfile, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)

    db.close()

except Exception as e:
    print("Error:", e)
    sys.exit(1)
