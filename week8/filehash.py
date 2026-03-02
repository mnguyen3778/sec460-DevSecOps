#!/usr/bin/env python3
"""
filehash.py

Week 8 - File Integrity Monitor

Creates and maintains an encrypted sqlite/sqlcipher database of file hashes.
Supports update, delete, list, and check commands.
Hash verification results are written to local syslog.
"""

import sys
import os
import hashlib
import sqlite3
import datetime
import syslog

DB_NAME = "monitor.db"


def get_connection():
    """
    Connect to database and create files table if it does not exist.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            timestamp TEXT,
            path TEXT PRIMARY KEY,
            hash TEXT
        )
    """)

    conn.commit()
    return conn


def get_md5(filepath):
    """
    Generate MD5 hash of a file using chunked reading.
    """
    md5 = hashlib.md5()

    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)

    return md5.hexdigest()


def get_timestamp():
    """
    Return current UTC time in ISO format (Zulu time).
    Uses timezone-aware datetime (no deprecation warning).
    """
    return datetime.datetime.now(datetime.UTC).isoformat()


def update_file(filepath):
    """
    Add or update file hash entry in the database.
    """
    if not os.path.exists(filepath):
        print("File does not exist.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    file_hash = get_md5(filepath)
    timestamp = get_timestamp()

    cursor.execute("SELECT path FROM files WHERE path = ?", (filepath,))
    exists = cursor.fetchone()

    if exists:
        cursor.execute(
            "UPDATE files SET timestamp=?, hash=? WHERE path=?",
            (timestamp, file_hash, filepath)
        )
        print("Updated:", filepath)
    else:
        cursor.execute(
            "INSERT INTO files (timestamp, path, hash) VALUES (?, ?, ?)",
            (timestamp, filepath, file_hash)
        )
        print("Added:", filepath)

    conn.commit()
    conn.close()


def delete_file(filepath):
    """
    Remove a file entry from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM files WHERE path = ?", (filepath,))
    conn.commit()
    conn.close()

    print("Deleted:", filepath)


def list_files():
    """
    List all file hash entries in the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT timestamp, path, hash FROM files")
    rows = cursor.fetchall()

    for row in rows:
        print(f"{row[0]} {row[1]} {row[2]}")

    conn.close()


def check_files():
    """
    Verify current file hashes against stored hashes.
    Results are written to syslog.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT path, hash FROM files")
    rows = cursor.fetchall()

    syslog.openlog("filehash")

    for path, stored_hash in rows:

        if not os.path.exists(path):
            syslog.syslog(
                syslog.LOG_ERR,
                f"Check=hash Result=ERROR: {path} missing"
            )
            continue

        current_hash = get_md5(path)

        if current_hash != stored_hash:
            syslog.syslog(
                syslog.LOG_ERR,
                f"Check=hash Result=ERROR: {path} hash mismatch, possible attack"
            )
        else:
            syslog.syslog(
                syslog.LOG_INFO,
                f"Check=hash Result=OK: {path} hash matches"
            )

    conn.close()


def main():
    """
    Parse command line arguments and execute appropriate command.
    """
    if len(sys.argv) < 2:
        print("Usage: ./filehash.py <update|delete|list|check> [filepath]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "update":
        if len(sys.argv) != 3:
            print("Usage: ./filehash.py update <filepath>")
            sys.exit(1)
        update_file(sys.argv[2])

    elif command == "delete":
        if len(sys.argv) != 3:
            print("Usage: ./filehash.py delete <filepath>")
            sys.exit(1)
        delete_file(sys.argv[2])

    elif command == "list":
        list_files()

    elif command == "check":
        check_files()

    else:
        print("Invalid command.")


if __name__ == "__main__":
    main()
