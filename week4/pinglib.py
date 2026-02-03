import subprocess
import re
import sys


def pingthis(ipordns):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", ipordns],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return [ipordns, "NotFound"]

        match = re.search(r'time=([\d.]+)', result.stdout)
        if match:
            return [ipordns, match.group(1)]
        else:
            return [ipordns, "NotFound"]

    except Exception:
        return [ipordns, "NotFound"]


def main():
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

