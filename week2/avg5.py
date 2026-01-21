#!/usr/bin/env python3
import sys

def calculate_average(numbers):
    """
    Calculate and return the average of a list of numbers.
    """
    return sum(numbers) / len(numbers)

def usage():
    """
    Print usage instructions for the avg5 script.
    """
    print("Usage: ./avg5.py n1 n2 n3 n4 n5 (all positive numbers)")

def main():
    """
    Validate command-line arguments, compute the average of five
    positive numbers, and print the result to two decimal places.
    """
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


