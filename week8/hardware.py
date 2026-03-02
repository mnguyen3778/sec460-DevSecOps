#!/usr/bin/env python3

"""
hardware.py

Monitors CPU load (1 minute), free memory, and root disk space.
Stores alert thresholds in monitor.db (hardware table).
Writes results to syslog.
"""

import sys
import sqlite3
import os
import shutil
import syslog

DB = "monitor.db"


# ---------------------------
# Database Setup
# ---------------------------

def init_db():
    """Create hardware table if it does not exist."""
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS hardware (
            cpuload REAL DEFAULT -1,
            memfree INTEGER DEFAULT -1,
            diskfree INTEGER DEFAULT -1
        )
    """)

    cur.execute("SELECT COUNT(*) FROM hardware")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO hardware VALUES (-1, -1, -1)")

    conn.commit()
    conn.close()


def get_thresholds():
    """Return current threshold values."""
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT cpuload, memfree, diskfree FROM hardware LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return row


def update_threshold(field, value):
    """Update a threshold value."""
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    if field == "cpu":
        cur.execute("UPDATE hardware SET cpuload=?", (float(value),))
    elif field == "mem":
        cur.execute("UPDATE hardware SET memfree=?", (int(value),))
    elif field == "disk":
        cur.execute("UPDATE hardware SET diskfree=?", (int(value),))
    else:
        print("Invalid field")
        conn.close()
        sys.exit(1)

    conn.commit()
    conn.close()


# ---------------------------
# Hardware Checks
# ---------------------------

def get_cpu_load():
    """Return 1-minute CPU load average."""
    return os.getloadavg()[0]


def get_mem_free():
    """Return available memory in MB."""
    with open("/proc/meminfo") as f:
        for line in f:
            if line.startswith("MemAvailable:"):
                kb = int(line.split()[1])
                return kb // 1024
    return 0


def get_disk_free():
    """Return free disk space in GB for root filesystem."""
    total, used, free = shutil.disk_usage("/")
    return round(free / (1024**3), 1)


# ---------------------------
# Check Logic
# ---------------------------

def check_hardware():
    """Check hardware against thresholds and write results to syslog."""
    cpu_threshold, mem_threshold, disk_threshold = get_thresholds()

    cpu = get_cpu_load()
    mem = get_mem_free()
    disk = get_disk_free()

    syslog.openlog("hardware")

    # CPU CHECK
    if cpu_threshold != -1 and cpu > cpu_threshold:
        syslog.syslog(syslog.LOG_ERR,
            f"Check=cpu Result=ERROR: cpu 1m load of {cpu:.2f} is above alert level of {cpu_threshold}")
    else:
        syslog.syslog(syslog.LOG_INFO,
            f"Check=cpu Result=OK: cpu 1m load is {cpu:.2f}")

    # MEMORY CHECK
    if mem_threshold != -1 and mem <= mem_threshold:
        syslog.syslog(syslog.LOG_ERR,
            f"Check=mem Result=ERROR: free memory of {mem}MB is less that alert level of {mem_threshold}MB")
    else:
        syslog.syslog(syslog.LOG_INFO,
            f"Check=mem Result=OK: free memory is {mem}MB")

    # DISK CHECK
    if disk_threshold != -1 and disk <= disk_threshold:
        syslog.syslog(syslog.LOG_ERR,
            f"Check=disk Result=ERROR: disk free of {disk}GB is less that alert level of {disk_threshold}GB")
    else:
        syslog.syslog(syslog.LOG_INFO,
            f"Check=disk Result=OK: disk free is {disk}GB")

    syslog.closelog()


# ---------------------------
# Main
# ---------------------------

def main():
    init_db()

    if len(sys.argv) < 2:
        print("Usage: ./hardware.py <list|update|check>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "list":
        cpu, mem, disk = get_thresholds()
        print(f"CPU alert level: {cpu}")
        print(f"Memory alert level: {mem}")
        print(f"Disk alert level: {disk}")

    elif cmd == "update":
        if len(sys.argv) != 4:
            print("Usage: ./hardware.py update <cpu|mem|disk> <value>")
            sys.exit(1)
        update_threshold(sys.argv[2], sys.argv[3])

    elif cmd == "check":
        check_hardware()

    else:
        print("Invalid command")
        sys.exit(1)


if __name__ == "__main__":
    main()
