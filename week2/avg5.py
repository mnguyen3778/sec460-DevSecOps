#!/usr/bin/env python3
import sys

def calculate_average(numbers):
    return sum(numbers) / len(numbers)

def usage():
    print("Usage: ./avg5.py n1 n2 n3 n4 n5 (all positive numbers)")

def main():
    if len(sys.argv) != 6:
        usage()
        return

    try:
        numbers = [float(arg) for arg in sys.argv[1:]]
        if any(n <= 0 for n in numbers):
            usage()
            return
    except ValueError:
        usage()
        return

    avg = calculate_average(numbers)
    print(f"{avg:.2f}")

if __name__ == "__main__":
    main()

