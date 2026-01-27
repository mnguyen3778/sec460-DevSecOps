#!/usr/bin/env python3

import subprocess
import socket
import shutil
import platform


def run_cmd(cmd):
    """
    Run a shell command and return its standard output as a string.
    """
    return subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    ).stdout.strip()


def get_hostname():
    """
    Return the hostname of the current machine.
    """
    return socket.gethostname()


def get_cpu_count():
    """
    Return the number of CPU cores available on the system.
    """
    return run_cmd("nproc")


def get_ram_gb():
    """
    Return the total system memory in gigabytes.
    """
    mem_kb = int(
        run_cmd("grep MemTotal /proc/meminfo | awk '{print $2}'")
    )
    return round(mem_kb / 1024 / 1024)


def get_os_type():
    """
    Return the operating system type.
    """
    return platform.system()


def get_os_version():
    """
    Return the operating system version.
    """
    return platform.release()


def get_disk_size():
    """
    Return the total size of the root filesystem in gigabytes.
    """
    total, _, _ = shutil.disk_usage("/")
    return round(total / 1024 / 1024 / 1024)


def get_disk_free():
    """
    Return the free space of the root filesystem in gigabytes.
    """
    _, free, _ = shutil.disk_usage("/")
    return round(free / 1024 / 1024 / 1024)


def get_primary_ip():
    """
    Return the primary IP address of the system.
    """
    return run_cmd("hostname -I | awk '{print $1}'")


def get_primary_mac():
    """
    Return the primary MAC address of the system.
    """
    return run_cmd("ip link show | awk '/link\\/ether/ {print $2; exit}'")


def main():
    """
    Display server information to the screen.
    """
    print(f"Hostname: {get_hostname()}")
    print(f"CPU (count): {get_cpu_count()}")
    print(f"RAM (GB): {get_ram_gb()}")
    print(f"OSType: {get_os_type()}")
    print(f"OSVersion: {get_os_version()}")
    print(f"OS disk size (GB): {get_disk_size()}")
    print(f"OS disk free (GB): {get_disk_free()}")
    print(f"Primary IP: {get_primary_ip()}")
    print(f"Primary Mac: {get_primary_mac()}")


if __name__ == "__main__":
    main()

    main()

