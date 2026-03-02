#!/usr/bin/env python3

"""
service.py

Week 8 Monitoring Assignment

Creates and manages a simple monitoring system backed by a SQLite
database named monitor.db.

Table: devices
    dns_ip (TEXT PRIMARY KEY) – Server name or IP address
    warn   (INTEGER) – Warning threshold in milliseconds

Commands:
    ./service.py update <dns_or_ip> <warn_ms>
    ./service.py delete <dns_or_ip>
    ./service.py list
    ./service.py check
"""

import sys
import sqlite3
import syslog

sys.path.append("../week4")
import pinglib

DB_NAME = "monitor.db"


def print_usage():
    """
    Print valid commands and usage options.
    """
    print("Usage:")
    print("    ./service.py update <dns_or_ip> <warn_ms>")
    print("    ./service.py delete <dns_or_ip>")
    print("    ./service.py list")
    print("    ./service.py check")
    print("")
    print("Commands:")
    print("    update  - add or update a device and warning threshold")
    print("    delete  - remove a device from monitoring")
    print("    list    - list all monitored devices")
    print("    check   - ping all devices and log results")


def init_db():
    """
    Create the devices table if it does not already exist.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            dns_ip TEXT PRIMARY KEY,
            warn INTEGER
        )
    """)
    conn.commit()
    conn.close()


def update_device(dns_ip, warn):
    """
    Insert or update a device in the database.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO devices (dns_ip, warn)
        VALUES (?, ?)
        ON CONFLICT(dns_ip)
        DO UPDATE SET warn=excluded.warn
    """, (dns_ip, warn))
    conn.commit()
    conn.close()


def delete_device(dns_ip):
    """
    Remove a device from the monitoring table.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM devices WHERE dns_ip=?", (dns_ip,))
    conn.commit()
    conn.close()


def list_devices():
    """
    Print all monitored devices and their warning thresholds.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT dns_ip, warn FROM devices")
    rows = cur.fetchall()
    conn.close()

    for dns_ip, warn in rows:
        print(f"{dns_ip} warn={warn}ms")


def check_devices():
    """
    Ping all monitored devices and log results to syslog.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT dns_ip, warn FROM devices")
    rows = cur.fetchall()
    conn.close()

    syslog.openlog("service")

    for dns_ip, warn in rows:
        result = pinglib.pingthis(dns_ip)

        if isinstance(result, list) and len(result) == 2:
            status = result[0]
            ping_time = result[1]
        else:
            status = False
            ping_time = None

        if not status or ping_time is None:
            message = f"Check=service Result=ERROR: Device {dns_ip} is down"
            syslog.syslog(syslog.LOG_ERR, message)
            print(message)
        else:
            ping_time = float(ping_time)

            if ping_time > warn:
                message = (
                    f"Check=service Result=WARNING: Device {dns_ip} "
                    f"ping time is {ping_time}ms, warn level set to {warn}ms"
                )
                syslog.syslog(syslog.LOG_WARNING, message)
                print(message)
            else:
                message = (
                    f"Check=service Result=OK: Device {dns_ip} "
                    f"ping time is {ping_time}ms"
                )
                syslog.syslog(syslog.LOG_INFO, message)
                print(message)


def main():
    """
    Command dispatcher for monitoring operations.
    """
    init_db()

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "update" and len(sys.argv) == 4:
        update_device(sys.argv[2], int(sys.argv[3]))

    elif cmd == "delete" and len(sys.argv) == 3:
        delete_device(sys.argv[2])

    elif cmd == "list" and len(sys.argv) == 2:
        list_devices()

    elif cmd == "check" and len(sys.argv) == 2:
        check_devices()

    else:
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
