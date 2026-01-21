#!/usr/bin/env python3
import sys

VOWELS = set("aeiou")

def usage():
    """Print usage instructions for the frequency script."""
    print("Usage: ./frequency.py <filename>")

def count_letters(filename):
    """
    Read the given file and count occurrences of each alphabetic character.
    Letters are treated case-sensitive and stored in a dictionary.
    """
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
    """
    Validate command-line arguments, process the input file,
    and print letter frequencies one per line.
    """
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


