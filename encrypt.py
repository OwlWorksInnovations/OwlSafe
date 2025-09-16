import os
import base64
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

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

# Generate password hash
def generate_password_hash(password: str):
    salt: bytes = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return salt, hashed_password

# Verify password hash
def verify_password_hash(password: str, hash: bytes):
    return bcrypt.checkpw(password.encode(), hash)

# Derives the key using the master password
def derive_key_from_password(password: str, salt: bytes):
    #           I have no clue what these paramaters do.
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# Encrypts the master.key using the master password
def encrypt_master_key_file(password: str, keyfile: str):
    master_key = Fernet.generate_key()
    salt = os.urandom(16)

    wrapping_key = derive_key_from_password(password, salt)
    f = Fernet(wrapping_key)
    cipher_text = f.encrypt(master_key)

    with open(keyfile, "wb") as f:
        f.write(salt + cipher_text)

# Decrypts the master.key.enc so that we can load the actual key.
def load_master_key_file(password: str, keyfile: str):
    with open(keyfile, "rb") as f:
        data = f.read()
    
    salt, cipher_text = data[:16], data[16:]
    wrapping_key = derive_key_from_password(password, salt)
    f = Fernet(wrapping_key)
    return f.decrypt(cipher_text)