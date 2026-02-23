#!/usr/bin/env python3
"""
update-device.py

Connects to an encrypted SQLCipher database and updates
the devices table with the current machine's server
information. If the hostname already exists in the table,
the existing row is replaced.


"""

# -------------------------------
# Initial variables and imports
# -------------------------------

import sqlcipher3
import subprocess
import socket
import shutil
import platform

database = 'etest.db'
table = 'devices'
password = 'MyStrongPassword123'


def run_cmd(cmd):
    """
    Executes a shell command and returns stripped stdout.
    """
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()


def get_hostname():
    """
    Returns system hostname.
    """
    return socket.gethostname()


def get_cpu_count():
    """
    Returns number of CPU cores.
    """
    return run_cmd("nproc")


def get_ram_gb():
    """
    Returns total RAM in GB.
    """
    mem_kb = int(run_cmd("grep MemTotal /proc/meminfo | awk '{print $2}'"))
    return round(mem_kb / 1024 / 1024)


def get_os_type():
    """
    Returns OS type.
    """
    return platform.system().lower()


def get_os_version():
    """
    Returns OS version.
    """
    return platform.release()


def get_disk_size():
    """
    Returns root filesystem size in GB.
    """
    total, _, _ = shutil.disk_usage("/")
    return round(total / 1024 / 1024 / 1024)


def get_disk_free():
    """
    Returns free disk space in GB.
    """
    _, free, _ = shutil.disk_usage("/")
    return round(free / 1024 / 1024 / 1024)


def get_primary_ip():
    """
    Returns primary IP address.
    """
    return run_cmd("hostname -I | awk '{print $1}'")


def get_primary_mac():
    """
    Returns primary MAC address.
    """
    return run_cmd("ip link show | awk '/link\\/ether/ {print $2; exit}'")


def main():
    """
    Connects to encrypted database and inserts or replaces
    the device record for the current machine.
    """

    try:
        db = sqlcipher3.connect(database)
        cur = db.cursor()
        cur.execute(f'pragma key="{password}";')

        hostname = get_hostname()
        mac = get_primary_mac()
        ip = get_primary_ip()
        cpu = get_cpu_count()
        disksize = get_disk_size()
        diskfree = get_disk_free()
        ram = get_ram_gb()
        ostype = get_os_type()
        osversion = get_os_version()

        # Remove existing row
        cur.execute(f"DELETE FROM {table} WHERE hostname = ?", (hostname,))

        # Insert updated row
        cur.execute(f"""
            INSERT INTO {table}
            (hostname, macaddress, ip, cpucount, disksize,
             diskfree, ram, ostype, osversion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (hostname, mac, ip, cpu, disksize,
              diskfree, ram, ostype, osversion))

        db.commit()
        db.close()

        print("Device updated successfully.")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
