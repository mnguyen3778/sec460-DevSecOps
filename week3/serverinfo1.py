#!/usr/bin/env python3
import subprocess
import socket
import shutil
import platform


def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()


def get_hostname():
    return socket.gethostname()


def get_cpu_count():
    return run_cmd("nproc")


def get_ram_gb():
    mem_kb = int(run_cmd("grep MemTotal /proc/meminfo | awk '{print $2}'"))
    return round(mem_kb / 1024 / 1024)


def get_os_type():
    return platform.system()


def get_os_version():
    return platform.release()


def get_disk_size():
    total, _, _ = shutil.disk_usage("/")
    return round(total / 1024 / 1024 / 1024)


def get_disk_free():
    _, free, _ = shutil.disk_usage("/")
    return round(free / 1024 / 1024 / 1024)


def get_primary_ip():
    return run_cmd("hostname -I | awk '{print $1}'")


def get_primary_mac():
    return run_cmd("ip link show | awk '/link\\/ether/ {print $2; exit}'")


def main():
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

