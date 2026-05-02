Secure Password Manager (Python Script Documentation)

Overview

This script is a lightweight command-line password manager that securely stores and retrieves credentials using symmetric encryption provided by the cryptography library (Fernet).

It allows users to:

Store encrypted website credentials

View all saved credentials (decrypted at runtime)

Search for saved credentials by website name

Automatically generate and manage an encryption key


All sensitive data is stored locally in an encrypted format.


---

Features

AES-based symmetric encryption using Fernet

Automatic encryption key generation and storage

Secure password input (hidden typing)

Local encrypted storage in a hidden directory

Add, view, and search password entries

Handles corrupted or invalid encrypted entries gracefully

File permission hardening (Linux/macOS support)



---

Requirements

Python Version

Python 3.7+


Dependencies

Install required library:

pip install cryptography


---

How It Works

1. Key Management

Function: load_or_create_key

The system uses a single encryption key stored locally.

Path: ~/.password_manager/key.key

If the key exists:

It is loaded and reused


If it does not exist:

A new Fernet key is generated

Saved to disk

File permissions are set to 600 (owner-only access where supported)



This ensures that only the local system can decrypt stored data.


---

2. Encryption System

Function: encrypt_entry

Each credential is stored in the format:

website|username|password

This string is:

1. Converted to bytes


2. Encrypted using Fernet


3. Stored as a base64 string



Example stored line:

gAAAAABlY...


---

Function: decrypt_entry

Takes encrypted token

Attempts decryption

Returns original string if valid

Returns None if data is corrupted or invalid



---

3. Data Storage

Credentials are stored in:

~/.password_manager/passwords.txt

Each line represents one encrypted entry.

Example structure:

encrypted_line_1
encrypted_line_2
encrypted_line_3


---

4. Adding Passwords

Function: save_password

User inputs:

Website

Username

Password (hidden input using getpass)


Process:

1. Data is formatted as:

website|username|password


2. Encrypted using Fernet


3. Appended to file



Output:

Password saved securely.


---

5. Viewing Passwords

Function: view_passwords

This feature:

Reads all encrypted entries

Decrypts each line

Displays formatted credentials


Output format:

Stored Credentials:
------------------------------
1. google.com | user@gmail.com | mypassword
2. github.com | devuser | securepass
------------------------------

If a line is invalid:

Corrupted or invalid entry


---

6. Searching Passwords

Function: search_password

Allows filtering by website name.

Process:

User enters search keyword

Script compares it against decrypted website names

Case-insensitive matching


Example:

Search website: github

Output:

github.com | devuser | securepass

If no match:

No matching entries found.


---

7. Application Flow

Main Loop

The application runs in an infinite loop:

Available commands:

add → Save new credential

view → Display all saved credentials

search → Find specific website entries

exit → Quit program



---

Example Usage

Start Program

python script.py


---

Add Password

Choose [add/view/search/exit]: add
Website: github.com
Username: devuser
Password (hidden): ********
Password saved securely.


---

View Passwords

Choose [add/view/search/exit]: view

Stored Credentials:
------------------------------
1. github.com | devuser | securepass
------------------------------


---

Search Password

Choose [add/view/search/exit]: search
Search website: github
github.com | devuser | securepass


---

Code Structure

Key Functions

Function	Purpose

load_or_create_key	Handles encryption key storage
encrypt_entry	Encrypts credential data
decrypt_entry	Decrypts stored credentials
save_password	Adds new credentials
view_passwords	Displays all entries
search_password	Searches stored data



---

Security Design

1. Encryption Standard

Uses Fernet, which provides:

AES 128 encryption (symmetric)

HMAC for integrity

Prevents tampering and unauthorized decoding



---

2. Local Storage Only

No network transmission

All data stored locally on disk



---

3. Hidden Password Input

Uses:

getpass()

So passwords are not visible during input.


---

4. File Permission Hardening

On supported systems:

chmod 600 key.key

Ensures only the owner can read the encryption key.


---

Limitations

No master password protection

No database support (uses plain text file storage for encrypted data)

No multi-device sync

No password strength validation

No GUI interface

No automatic backup system



---

Possible Improvements

Security Enhancements

Add master password authentication

Encrypt file storage itself (not just entries)

Add PBKDF2 password-derived keys


Feature Enhancements

Delete/update entries

Copy password to clipboard

Export/import encrypted vault

GUI interface (Tkinter or web-based)


Architecture Improvements

Replace text file with SQLite encrypted database

Add logging system

Add structured JSON storage instead of pipe-separated strings



---

Folder Structure

~/.password_manager/
│
├── key.key
└── passwords.txt


---

License

This project is free to use and modify for personal or commercial use.
