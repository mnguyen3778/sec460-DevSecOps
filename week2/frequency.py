#!/usr/bin/env python3
import sys

VOWELS = set("aeiou")

def usage():
    print("Usage: ./frequency.py <filename>")

def count_letters(filename):
    counts = {}

    try:
        with open(filename, "r") as f:
            for line in f:
                for char in line.lower():
                    if char.isalpha():
                        counts[char] = counts.get(char, 0) + 1
    except FileNotFoundError:
        usage()
        return None

    return counts

def main():
    if len(sys.argv) != 2:
        usage()
        return

    filename = sys.argv[1]
    counts = count_letters(filename)
    if counts is None:
        return

    for letter in sorted(counts):
        print(f"{letter} - {counts[letter]}")

if __name__ == "__main__":
    main()

