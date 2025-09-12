import os, base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import bcrypt

def generate_key():
    key = Fernet.generate_key()
    with open("master.key", "wb") as f:
        f.write(key)
    
def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode())

def decrypt_password(token, key):
    f = Fernet(key)
    return f.decrypt(token).decode()

def generate_password_hash(password: str):
    password_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return salt, hashed_password

def verify_password_hash(password: str, hash: bytes):
    password_bytes = password.encode('utf-8')

    return bcrypt.checkpw(password_bytes, hash)

def derive_key_from_password(password: str, salt: bytes):
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)

    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_master_key_file(password: str, keyfile="master.key.enc"):
    master_key = Fernet.generate_key()
    salt = os.urandom(16)

    wrapping_key = derive_key_from_password(password, salt)
    f = Fernet(wrapping_key)
    ct = f.encrypt(master_key)

    with open(keyfile, "wb") as f_out:
        f_out.write(salt + ct)

def load_master_key_file(password: str, keyfile="master.key.enc"):
    data = open(keyfile, "rb").read()
    salt, ct = data[:16], data[16:]
    wrapping_key = derive_key_from_password(password, salt)
    f = Fernet(wrapping_key)
    return f.decrypt(ct)