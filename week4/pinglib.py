import subprocess
import re
import sys


def pingthis(ipordns):
    """
    Ping an IP address or domain name once and extract the response time.

    Args:
        ipordns (str): An IP address or domain name to ping.

    Returns:
        list: A two-element list containing:
              - The IP or domain name
              - The ping time in milliseconds as a string, or 'NotFound' if unreachable
    """
    try:
        result = subprocess.run(
            ["ping", "-c", "1", ipordns],
            capture_output=True,
            text=True,
            timeout=5
        )

        # If ping failed (host unreachable, DNS failure, etc.)
        if result.returncode != 0:
            return [ipordns, "NotFound"]

        # Extract time=XX.X from ping output using regex
        match = re.search(r'time=([\d.]+)', result.stdout)
        if match:
            return [ipordns, match.group(1)]
        else:
            return [ipordns, "NotFound"]

    except Exception:
        return [ipordns, "NotFound"]


def main():
    """
    Command-line entry point for pinglib.py.

    Reads a single argument from the command line (IP or domain),
    calls pingthis(), and prints the result in CSV format:
    IP,TimeToPing(ms)
    """
    if len(sys.argv) != 2:
        print("Usage: pinglib.py <IP | Domainname>")
        sys.exit(1)

    ipordns = sys.argv[1]
    result = pingthis(ipordns)

    if result[1] == "NotFound":
        print(f"{result[0]},NotFound")
    else:
        print(f"{result[0]},{float(result[1]):.2f}")


if __name__ == "__main__":
    main()

