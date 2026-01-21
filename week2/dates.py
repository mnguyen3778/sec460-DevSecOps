#!/usr/bin/env python3
from datetime import datetime, timedelta

def usage():
    """
    Print instructions for how to use the dates script.
    """
    print("Usage:")
    print("  Enter birthdate as mm-dd-yyyy")
    print("  Enter number of days to add as a positive integer")

def main():
    """
    Prompt the user for a birthdate and a number of days,
    validate the input, and print the resulting date.
    """
    try:
        birthdate_input = input("Enter your birthdate (mm-dd-yyyy): ")
        days_input = input("Enter number of days to add: ")

        # Validate and parse the date
        birthdate = datetime.strptime(birthdate_input, "%m-%d-%Y")

        # Validate days to add
        days = int(days_input)
        if days <= 0:
            raise ValueError

    except ValueError:
        usage()
        return

    future_date = birthdate + timedelta(days=days)
    print(future_date.strftime("%m-%d-%Y"))

if __name__ == "__main__":
    main()


