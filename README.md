
# OwlSafe

OwlSafe is a local password manager built with Python 3.13 and PyQt5. It uses strong encryption (Fernet, bcrypt, Scrypt) to store passwords securely in a local SQLite database. The app features a GUI for managing passwords, a master password system, and all encryption keys are stored locally.

## Features
- Local password storage (SQLite)
- Master password protection
- Password encryption with Fernet and bcrypt
- PyQt5 GUI
- No cloud or remote storage

## Requirements
- Python 3.13
- PyQt5
- cryptography
- bcrypt

## Setup
1. Install dependencies:
	```
	pip install -r requirements.txt
	```
2. Run the app:
	```
	python app.py
	```

## Screenshot
![OwlSafe GUI](screenshot/Screenshot%202025-09-02%20170907.png)

## Note
This is a learning project and not intended for production use.

