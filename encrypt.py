import os
import base64
import bcrypt
from cryptography.fernet import Fernet

# Generates a key for encryption and decryption
def generate_key():
    key: bytes = Fernet.generate_key()
    with open('master.key', 'wb') as f:
        f.write(key)

# Encrypts a password with the key
def encrypt_password(password: str, key: bytes):
    f = Fernet(key)
    return f.encrypt(password.encode())

# Decrypts a password with the key
def decrypt_password(password: str, key: bytes):
    f = Fernet(key)
    return f.decrypt(password.encode())