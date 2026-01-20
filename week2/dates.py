#!/usr/bin/env python3
from datetime import datetime, timedelta

def usage():
    print("Usage:")
    print("  Enter birthdate as mm-dd-yyyy")
    print("  Enter number of days to add as a positive integer")

def main():
    try:
        birthdate_input = input("Enter your birthdate (mm-dd-yyyy): ")
        days_input = input("Enter number of days to add: ")

        # Parse and validate date
        birthdate = datetime.strptime(birthdate_input, "%m-%d-%Y")

        # Parse and validate days
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

